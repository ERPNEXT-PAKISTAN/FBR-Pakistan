# Copyright (c) 2026, FBR Pakistan Integration and contributors
# For license information, please see license.txt
"""
Recomputes the FBR tax breakup (Sales Tax, Further Tax, Extra Tax,
Other Tax 1/2 and the Tax Inclusive Amount) on every Sales Invoice Item,
reading the rates from the Item Tax Template attached to each row.

This is the app equivalent of the "FBR Tax Calculation" Server Script
described in the FBR-Pakistan integration guide
(DocType Event: Sales Invoice, Before Save).

Map your own Chart of Accounts tax account names to the tax_type checks
below if your GL account labels differ from the defaults:
	General Sales Tax, Further Tax, Extra Tax, Other Tax 1, Other Tax 2
"""

import frappe
from erpnext.stock.get_item_details import get_item_tax_map
from frappe.utils import flt


def _has_further_tax(template_name):
	return any(
		"further tax" in (tax.tax_type or "").casefold()
		for tax in frappe.get_all(
			"Item Tax Template Detail", filters={"parent": template_name}, fields=["tax_type"]
		)
	)


def _is_taxable_sales_template(template_name):
	return any(
		any(label in (tax.tax_type or "").casefold() for label in ("sales tax", "gst"))
		for tax in frappe.get_all(
			"Item Tax Template Detail", filters={"parent": template_name}, fields=["tax_type"]
		)
	)


def _template_variant_title(title, unregistered, company):
	if unregistered:
		if title.endswith((" (Unregistered)", " (Unregistered + Extra)")):
			return None
		if title.endswith(" (Registered + Extra)"):
			return title[: -len(" (Registered + Extra)")] + " (Unregistered + Extra)"
		if title.endswith(" (Registered)"):
			return title[: -len(" (Registered)")] + " (Unregistered)"
		return f"{title} (Unregistered)"

	if title.endswith(" (Unregistered + Extra)"):
		base_title = title[: -len(" (Unregistered + Extra)")]
		registered_extra = f"{base_title} (Registered + Extra)"
		return registered_extra if frappe.db.exists(
			"Item Tax Template", {"title": registered_extra, "company": company}
		) else base_title
	if title.endswith(" (Unregistered)"):
		base_title = title[: -len(" (Unregistered)")]
		registered_title = f"{base_title} (Registered)"
		return registered_title if frappe.db.exists(
			"Item Tax Template", {"title": registered_title, "company": company}
		) else base_title
	return None


def apply_unregistered_tax_templates(doc, method=None):
	payer_type = doc.get("custom_tax_payer_type")
	if not payer_type and doc.get("customer"):
		payer_type = frappe.db.get_value("Customer", doc.customer, "custom_tax_payer_type")
	scenario_link = doc.get("custom_scenario_id")
	scenario_id = frappe.db.get_value("Scenario ID", scenario_link, "scenario_id") or scenario_link
	unregistered = (
		payer_type in {"Unregistered", "Unregistered Distributor", "Retail Consumer"}
		and scenario_id != "SN006"
	)

	for item in doc.items:
		if not item.item_tax_template:
			continue
		item_is_unregistered = unregistered and "exempt" not in (item.get("custom_sale_type") or "").casefold()

		template = frappe.db.get_value(
			"Item Tax Template", item.item_tax_template, ["title", "company"], as_dict=True
		)
		if not template:
			continue

		if item_is_unregistered and _has_further_tax(item.item_tax_template):
			item.item_tax_rate = get_item_tax_map(doc=doc, tax_template=item.item_tax_template, as_json=True)
			continue
		if item_is_unregistered and not _is_taxable_sales_template(item.item_tax_template):
			continue

		target_title = _template_variant_title(template.title, item_is_unregistered, template.company)
		if not target_title:
			continue

		target = frappe.db.get_value(
			"Item Tax Template", {"title": target_title, "company": template.company}, "name"
		)
		if target:
			item.item_tax_template = target
			item.item_tax_rate = get_item_tax_map(doc=doc, tax_template=target, as_json=True)
		elif item_is_unregistered:
			frappe.throw(
				frappe._("No 4% further-tax template exists for {0}. Run bench migrate and check the company tax accounts.").format(
					template.title
				)
			)


def calculate_fbr_taxes(doc, method=None):
	for item in doc.items:
		# Reset tax values
		item.custom_sales_tax_rate = 0
		item.custom_further_tax_rate = 0
		item.custom_extra_tax_rate = 0
		item.custom_other_tax_1_rate = 0
		item.custom_other_tax_2_rate = 0

		item.custom_sales_tax = 0
		item.custom_further_tax = 0
		item.custom_extra_tax = 0
		item.custom_other_tax_1 = 0
		item.custom_other_tax_2 = 0

		item.custom_total_tax_amount = 0
		item.custom_tax_inclusive_amount = item.amount or 0

		if not item.item_tax_template:
			continue

		tax_details = frappe.get_all(
			"Item Tax Template Detail",
			filters={"parent": item.item_tax_template},
			fields=["tax_type", "tax_rate"],
		)

		for tax in tax_details:
			tax_type = tax.tax_type or ""

			# Update the tax account names below if your Chart of Accounts differs
			if (
				"General Sales Tax" in tax_type
				or tax_type.startswith("Sales Tax -")
				or tax_type.startswith("GST -")
			):
				item.custom_sales_tax_rate = tax.tax_rate or 0
			elif "Further Tax" in tax_type:
				item.custom_further_tax_rate = tax.tax_rate or 0
			elif "Extra Tax" in tax_type:
				item.custom_extra_tax_rate = tax.tax_rate or 0
			elif "Other Tax 1" in tax_type:
				item.custom_other_tax_1_rate = tax.tax_rate or 0
			elif "Other Tax 2" in tax_type:
				item.custom_other_tax_2_rate = tax.tax_rate or 0

		if not item.amount:
			continue

		item.custom_sales_tax = (item.amount * item.custom_sales_tax_rate) / 100
		item.custom_further_tax = (item.amount * item.custom_further_tax_rate) / 100
		item.custom_extra_tax = (item.amount * item.custom_extra_tax_rate) / 100
		item.custom_other_tax_1 = (item.amount * item.custom_other_tax_1_rate) / 100
		item.custom_other_tax_2 = (item.amount * item.custom_other_tax_2_rate) / 100

		item.custom_total_tax_amount = (
			item.custom_sales_tax
			+ item.custom_further_tax
			+ item.custom_extra_tax
			+ item.custom_other_tax_1
			+ item.custom_other_tax_2
		)

		item.custom_tax_inclusive_amount = item.amount + item.custom_total_tax_amount
