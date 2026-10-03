# Copyright (c) 2026, FBR Pakistan Integration and contributors
# For license information, please see license.txt
"""
Runs once, right after `bench --site <site> install-app fbr_integration`.

Loads the FBR reference/master data (HS Codes, Scenario IDs, Buyer
Provinces, Sale Types, Tax Payer Types, Invoice Types, FBR UoM, SRO
Schedule/Item numbers) shipped as CSVs in fbr_integration/data/, so the app
is usable immediately without a manual Data Import.
"""

import csv
import os

import frappe
from frappe.utils import cint, flt

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# doctype -> (csv filename, [fieldnames in column order])
MASTER_DATA_MAP = {
	"Buyer Province": ("buyer_province.csv", ["buyer_province"]),
	"FBR UoM": ("fbr_uom.csv", ["fbr_uom"]),
	"Invoice Type": ("invoice_type.csv", ["invoice_type"]),
	"Sale Type": ("sale_type.csv", ["sale_type"]),
	"SRO Item SNo": ("sro_item_sno.csv", ["sro_item_sno"]),
	"SRO Schedule No": ("sro_schedule_no.csv", ["sro_schedule_no"]),
	"Tax Payer Type": ("tax_payer_type.csv", ["tax_payer_type"]),
	"HS Code": ("hs_code.csv", ["hs_code", "hs_code_detail"]),
	"Scenario ID": ("scenario_id.csv", ["scenario_id", "scenario_detail"]),
}


def after_install():
	for doctype, (filename, fieldnames) in MASTER_DATA_MAP.items():
		_load_master_csv(doctype, filename, fieldnames)

	_load_accounts()
	_create_default_settings()
	_create_item_tax_templates_from_accounts()
	_create_unregistered_item_tax_templates()
	_create_tax_category()

	frappe.db.commit()


def after_migrate():
	_create_unregistered_item_tax_templates()


def _load_accounts():
    path = os.path.join(DATA_DIR, "accounts.csv")

    if not os.path.exists(path):
        return

    companies = frappe.get_all("Company", pluck="name")

    if not companies:
        return

    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for company in companies:
        _import_accounts_for_company(company, rows)


def _load_master_csv(doctype, filename, fieldnames):
	path = os.path.join(DATA_DIR, filename)
	if not os.path.exists(path):
		return

	with open(path, newline="", encoding="utf-8-sig") as f:
		reader = csv.reader(f)
		next(reader, None)  # skip header row

		for row in reader:
			if not row or not row[0].strip():
				continue

			values = {fieldnames[i]: (row[i].strip() if i < len(row) else "") for i in range(len(fieldnames))}
			key_field = fieldnames[0]

			if frappe.db.exists(doctype, {key_field: values[key_field]}):
				continue

			try:
				doc = frappe.new_doc(doctype)
				doc.update(values)
				doc.insert(ignore_permissions=True, ignore_mandatory=True)
			except Exception:
				frappe.log_error(frappe.get_traceback(), f"fbr_integration.install: {doctype} import failed")


def _import_accounts_for_company(company, rows):
	abbr = frappe.db.get_value("Company", company, "abbr")

	# Existing accounts lookup
	account_lookup = {
		d.account_name: d.name
		for d in frappe.get_all(
			"Account",
			filters={"company": company},
			fields=["name", "account_name"],
		)
	}

	pending = list(rows)

	while pending:
		imported = 0
		remaining = []

		for row in pending:
			account_name = (row.get("Account Name") or "").strip()

			if not account_name:
				continue

			parent_name = (row.get("Parent Account") or "").strip()
			root_type = (row.get("Root Type") or "").strip()
			account_type = (row.get("Account Type") or "").strip()

			is_group = cint(row.get("Is Group") or 0)

			tax_rate = flt(row.get("Tax Rate") or 0)

			# Already exists
			if account_name in account_lookup:
				imported += 1
				continue

			parent = None

			if parent_name:
				parent = account_lookup.get(parent_name)

				# Parent not imported yet
				if not parent:
					remaining.append(row)
					continue

			try:
				doc = frappe.new_doc("Account")

				doc.account_name = account_name
				doc.company = company
				doc.parent_account = parent
				doc.root_type = root_type
				doc.is_group = is_group

				if account_type:
					doc.account_type = account_type

				if frappe.get_meta("Account").has_field("tax_rate"):
					doc.tax_rate = tax_rate

				doc.insert(ignore_permissions=True)

				account_lookup[account_name] = doc.name

				imported += 1

			except Exception:
				frappe.log_error(
					frappe.get_traceback(),
					f"Failed importing account '{account_name}' ({company})",
				)
				pass

		if not remaining:
			break

		if imported == 0:
			frappe.log_error(
				"\n".join(
					f"{r.get('Account Name')} --> {r.get('Parent Account')}"
					for r in remaining
				),
				f"Accounts still pending for company {company}",
			)
			break

		pending = remaining


def _create_default_settings():
	if frappe.db.exists("DocType", "FBR Invoice Settings") and not frappe.db.get_single_value(
		"FBR Invoice Settings", "integration_type"
	):
		settings = frappe.get_single("FBR Invoice Settings")
		settings.integration_type = "Sandbox"
		settings.enabled = 0
		settings.save(ignore_permissions=True)


def _create_single_item_tax_template(company, title, taxes):

	if frappe.db.exists(
		"Item Tax Template",
		{
			"title": title,
			"company": company,
		},
	):
		return

	doc = frappe.new_doc("Item Tax Template")
	doc.title = title
	doc.company = company

	for tax_type, tax_rate in taxes:
		doc.append(
			"taxes",
			{
				"tax_type": tax_type,
				"tax_rate": tax_rate,
				"not_applicable": 0,
			},
		)

	doc.insert(ignore_permissions=True)
	

def _create_item_tax_templates_from_accounts():
	for company in frappe.get_all("Company", pluck="name"):

		sales_tax_accounts = frappe.get_all(
			"Account",
			filters={
				"company": company,
				"is_group": 0,
				"account_name": ["like", "Sales Tax -%"],
			},
			fields=["name", "account_name", "tax_rate"],
			order_by="account_name",
		)

		if not sales_tax_accounts:
			continue

		extra_tax = frappe.db.get_value(
			"Account",
			{
				"company": company,
				"is_group": 0,
				"account_name": ["like", "%Extra Tax -%"],
			},
			["name", "tax_rate"],
			as_dict=True,
		)

		further_tax = frappe.db.get_value(
			"Account",
			{
				"company": company,
				"is_group": 0,
				"account_name": ["like", "%Further Tax -%"],
			},
			["name", "tax_rate"],
			as_dict=True,
		)

		for sales in sales_tax_accounts:

			_create_single_item_tax_template(
				company=company,
				title=f"{sales.account_name} (Registered)",
				taxes=[
					(sales.name, sales.tax_rate),
				],
			)

			registered_extra = [
				(sales.name, sales.tax_rate),
			]

			if extra_tax:
				registered_extra.append((extra_tax.name, extra_tax.tax_rate))

			_create_single_item_tax_template(
				company=company,
				title=f"{sales.account_name} (Registered + Extra)",
				taxes=registered_extra,
			)

			unregistered = [
				(sales.name, sales.tax_rate),
			]

			if further_tax:
				unregistered.append((further_tax.name, further_tax.tax_rate))

			_create_single_item_tax_template(
				company=company,
				title=f"{sales.account_name} (Unregistered)",
				taxes=unregistered,
			)

			unregistered_extra = [
				(sales.name, sales.tax_rate),
			]

			if extra_tax:
				unregistered_extra.append((extra_tax.name, extra_tax.tax_rate))

			if further_tax:
				unregistered_extra.append((further_tax.name, further_tax.tax_rate))

			_create_single_item_tax_template(
				company=company,
				title=f"{sales.account_name} (Unregistered + Extra)",
				taxes=unregistered_extra,
			)


def _create_unregistered_item_tax_templates():
	for company in frappe.get_all("Company", pluck="name"):
		further_tax = _ensure_unregistered_tax_account(company)
		if not further_tax:
			continue

		for template_row in frappe.get_all(
			"Item Tax Template", filters={"company": company}, fields=["name", "title"]
		):
			title = template_row.title or template_row.name
			if title.casefold().endswith(
				(" (registered)", " (registered + extra)", " (unregistered)", " (unregistered + extra)")
			):
				continue

			unregistered_title = f"{title} (Unregistered)"
			if frappe.db.exists("Item Tax Template", {"title": unregistered_title, "company": company}):
				continue

			source = frappe.get_doc("Item Tax Template", template_row.name)
			if any("further tax" in (tax.tax_type or "").casefold() for tax in source.taxes):
				continue

			taxable_sales_tax = any(
				any(label in (tax.tax_type or "").casefold() for label in ("sales tax", "gst"))
				for tax in source.taxes
			)
			if not taxable_sales_tax:
				continue

			variant = frappe.new_doc("Item Tax Template")
			variant.title = unregistered_title
			variant.company = company
			if source.meta.has_field("tax_category"):
				variant.tax_category = source.get("tax_category")

			for tax in source.taxes:
				variant.append(
					"taxes",
					{
						"tax_type": tax.tax_type,
						"tax_rate": tax.tax_rate,
						"not_applicable": tax.not_applicable,
					},
				)

			variant.append(
				"taxes",
				{
					"tax_type": further_tax.name,
					"tax_rate": further_tax.tax_rate,
					"not_applicable": 0,
				},
			)
			variant.insert(ignore_permissions=True)


def _ensure_unregistered_tax_account(company):
	account_name = "Further Tax - 4% on Unregistered Supplies"
	account = frappe.db.get_value(
		"Account",
		{"company": company, "account_name": account_name, "is_group": 0},
		"name",
	)
	if account:
		tax_rate = 4
		if frappe.get_meta("Account").has_field("tax_rate"):
			tax_rate = flt(frappe.db.get_value("Account", account, "tax_rate") or 4)
		return frappe._dict(name=account, tax_rate=tax_rate)

	parent = None
	for parent_name in ("Sales Tax on Goods", "Duties and Taxes"):
		parent = frappe.db.get_value(
			"Account",
			{"company": company, "account_name": parent_name, "is_group": 1},
			"name",
		)
		if parent:
			break

	if not parent:
		parent = frappe.db.get_value(
			"Account", {"company": company, "account_type": "Tax", "is_group": 1}, "name"
		)
	if not parent:
		frappe.log_error(
			f"No tax liability group exists for company {company}.",
			"fbr_integration: Further Tax account not created",
		)
		return None

	doc = frappe.new_doc("Account")
	doc.account_name = account_name
	doc.company = company
	doc.parent_account = parent
	doc.root_type = "Liability"
	doc.account_type = "Tax"
	doc.is_group = 0
	if frappe.get_meta("Account").has_field("tax_rate"):
		doc.tax_rate = 4
	doc.insert(ignore_permissions=True)
	return frappe._dict(name=doc.name, tax_rate=4)


def _create_tax_category():
    if frappe.db.exists("DocType", "Tax Category"):
        for title in ("Registered", "Unregistered", "Exempt"):
            if not frappe.db.exists("Tax Category", {"title": title}):
                doc = frappe.new_doc("Tax Category")
                doc.title = title
                doc.insert(ignore_permissions=True)