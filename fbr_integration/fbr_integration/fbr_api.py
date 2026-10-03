# Copyright (c) 2026, FBR Pakistan Integration and contributors
# For license information, please see license.txt
"""
Builds the FBR IRIS Digital Invoicing payload from a submitted Sales Invoice
and posts it to FBR's Sandbox or Production endpoint, per the FBR-Pakistan
integration guide (PRAL Digital Invoicing API).
"""

import json

import frappe
import requests
import urllib3
from erpnext.accounts.utils import get_fiscal_year
from frappe.model.naming import getseries

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

REDUCED_SALE_TYPES = ("goodsatreducedrate", "reducedrate", "rr")


def safe_float(val):
	"""Return a non-negative float, or 0 for blank / invalid / negative input."""
	try:
		num = float(val)
		return num if num >= 0 else 0
	except (TypeError, ValueError):
		return 0


def fbr_value(item, fieldname, fallback):
	"""Use an explicit FBR payload override when present, otherwise use the invoice value."""
	value = item.get(fieldname)
	return fallback if value in (None, "", 0, "0") else value


def extra_tax_value(val, sale_type_str):
	"""
	FBR expects an empty string (not 0) for extraTax when the sale type is a
	reduced-rate type, or when the value is blank/zero/negative.
	"""
	if sale_type_str in REDUCED_SALE_TYPES:
		return ""
	try:
		num = float(val)
		return num if num > 0 else ""
	except (TypeError, ValueError):
		return ""


def get_fbr_settings():
	settings = frappe.get_single("FBR Invoice Settings")

	if not settings.enabled:
		frappe.throw(
			frappe._("FBR Integration is disabled. Enable it in FBR Invoice Settings first."),
			title=frappe._("FBR Integration Disabled"),
		)

	if settings.integration_type == "Sandbox":
		api_url = settings.sandbox_api_url
		token = settings.get_password("sandbox_security_token", raise_exception=False)
	elif settings.integration_type == "Production":
		api_url = settings.production_api_url
		token = settings.get_password("production_security_token", raise_exception=False)
	else:
		frappe.throw(frappe._("Invalid FBR Integration Type. Set it to Sandbox or Production."))

	if not api_url or not token:
		frappe.throw(
			frappe._("Please configure the API URL and Security Token in FBR Invoice Settings for {0}.").format(
				settings.integration_type
			)
		)

	return settings, api_url, token


def build_address(address_name):
	"""Returns (address_line, province) for a given Address doctype name."""
	if not address_name:
		return "", ""
	address_doc = frappe.get_doc("Address", address_name)
	address_line = ", ".join(dict.fromkeys(filter(None, [address_doc.address_line1, address_doc.city])))
	return address_line, (address_doc.state or "")


def build_payload(doc):
	seller_address, seller_province = build_address(getattr(doc, "company_address", None))
	buyer_address, buyer_province = build_address(getattr(doc, "customer_address", None))
	scenario_link = doc.get("custom_scenario_id")
	scenario_id = frappe.db.get_value("Scenario ID", scenario_link, "scenario_id") or scenario_link

	# Prefer the explicit link fields when set; fall back to values fetched onto the address
	seller_province = seller_province or ""
	buyer_province = doc.get("custom_buyer_province") or buyer_province

	items_list = []
	for item in doc.items:
		sale_type_str = str(item.get("custom_sale_type") or "").lower().replace(" ", "")
		extra_tax = extra_tax_value(item.get("custom_extra_tax"), sale_type_str)

		if scenario_id == "SN006":
			rate_val = "Exempt"
		else:
			rate_val = "{:g}%".format(safe_float(item.get("custom_sales_tax_rate")))
		fixed_price = item.get("custom_fbr_fixed_notified_value_or_retail_price")
		if fixed_price is None or fixed_price == "":
			fixed_price = 0
		discount = item.get("custom_fbr_discount")
		if discount is None or discount == "":
			discount = item.discount_amount

		payload_item = {
			"hsCode": item.get("custom_hs_code"),
			"productDescription": item.item_name,
			"rate": rate_val,
			"uoM": item.get("custom_fbr_uom"),
			"quantity": safe_float(item.qty),
			# "totalValues": safe_float(
			# 	fbr_value(item, "custom_fbr_total_values", item.get("custom_tax_inclusive_amount"))
			# ),
			"totalValues": safe_float(item.get("custom_tax_inclusive_amount")),
			"valueSalesExcludingST": safe_float(
				fbr_value(item, "custom_fbr_value_sales_excluding_st", item.amount)
			),
			"fixedNotifiedValueOrRetailPrice": safe_float(fixed_price),
			"salesTaxApplicable": safe_float(
				fbr_value(item, "custom_fbr_sales_tax_applicable", item.get("custom_sales_tax"))
			),
			"salesTaxWithheldAtSource": safe_float(item.get("custom_fbr_sales_tax_withheld_at_source")),
			"extraTax": extra_tax,
			"furtherTax": safe_float(
				fbr_value(item, "custom_fbr_further_tax", item.get("custom_further_tax"))
			),
			"sroScheduleNo": item.get("custom_sro_schedule_no") or "",
			"fedPayable": safe_float(item.get("custom_fbr_fed_payable")),
			"discount": safe_float(discount),
			"saleType": item.get("custom_sale_type"),
			"sroItemSerialNo": item.get("custom_sro_item_sno") or "",
		}

		item_override = item.get("custom_fbr_payload_override")
		if item_override:
			if isinstance(item_override, str):
				item_override = json.loads(item_override)
			if not isinstance(item_override, dict):
				frappe.throw(frappe._("FBR item payload override must be a JSON object."))
			payload_item.update(item_override)

		items_list.append(payload_item)

	return {
		"invoiceType": doc.get("custom_invoice_type"),
		"invoiceDate": frappe.utils.getdate(doc.custom_fbr_invoice_date).strftime("%Y-%m-%d"),
		"sellerNTNCNIC": doc.company_tax_id,
		"sellerBusinessName": doc.company,
		"sellerAddress": seller_address,
		"sellerProvince": seller_province,
		"buyerNTNCNIC": doc.tax_id,
		"buyerBusinessName": doc.customer,
		"buyerAddress": buyer_address,
		"buyerProvince": buyer_province,
		"invoiceRefNo": doc.custom_fbr_invoice_ref_no,
		"scenarioId": scenario_id,
		"buyerRegistrationType": (
			"Registered" if doc.get("custom_tax_payer_type") == "Registered" else "Unregistered"
			if doc.get("custom_tax_payer_type")
			else ""
		),
		"items": items_list,
	}


def prepare_fbr_request(doc):
	if not doc.get("custom_fbr_invoice_date"):
		doc.custom_fbr_invoice_date = frappe.utils.today()

	if not doc.get("custom_fbr_invoice_ref_no"):
		fiscal_year = get_fiscal_year(frappe.utils.today(), company=doc.company, as_dict=True)
		year_suffix = frappe.utils.getdate(fiscal_year.year_end_date).strftime("%y")
		sequence = getseries(f"FBR-SI-{year_suffix}", 3)
		doc.custom_fbr_invoice_ref_no = f"{year_suffix}{sequence}"

	if doc.get("custom_fbr_request_payload"):
		payload_json = doc.custom_fbr_request_payload
		payload = json.loads(payload_json)
	else:
		payload = build_payload(doc)
		payload_json = json.dumps(payload, ensure_ascii=False, allow_nan=False, indent=2)
		doc.custom_fbr_request_payload = payload_json

	frappe.db.set_value(
		"Sales Invoice",
		doc.name,
		{
			"custom_fbr_invoice_date": doc.custom_fbr_invoice_date,
			"custom_fbr_invoice_ref_no": doc.custom_fbr_invoice_ref_no,
			"custom_fbr_request_payload": payload_json,
		},
		update_modified=False,
	)
	return payload, payload_json


def _set_fbr_response(doc, values):
	frappe.db.set_value("Sales Invoice", doc.name, values, update_modified=False)
	doc.update(values)


def send_invoice_to_fbr(doc, method=None):
	settings, api_url, token = get_fbr_settings()
	_, payload_json = prepare_fbr_request(doc)
	if token.strip().lower().startswith("bearer "):
		token = token.strip()[7:].strip()

	headers = {
		"Authorization": f"Bearer {token}",
		"Content-Type": "application/json",
	}

	frappe.logger().info(f"Sending Sales Invoice {doc.name} to FBR ({settings.integration_type})")

	try:
		response = requests.post(
			api_url,
			headers=headers,
			data=payload_json,
			verify=bool(settings.ssl_applied),
			timeout=(10, 60),
		)
		response.raise_for_status()
		res_json = response.json()
	except requests.exceptions.HTTPError as e:
		body = response.text or str(e)
		error = f"FBR returned HTTP {response.status_code}: {body}"
		_set_fbr_response(
			doc,
			{
				"custom_fbr_responsed": "Error",
				"custom_fbr_digital_invoice_response": error,
			},
		)
		frappe.throw(frappe._("FBR request failed: {0}").format(error), title=frappe._("FBR Error"))
	except ValueError as e:
		error = f"FBR returned invalid JSON (HTTP {response.status_code}): {response.text}"
		_set_fbr_response(
			doc,
			{
				"custom_fbr_responsed": "Error",
				"custom_fbr_digital_invoice_response": error,
			},
		)
		frappe.throw(frappe._("FBR request failed: {0}").format(error), title=frappe._("FBR Error"))
	except requests.exceptions.RequestException as e:
		error = str(e)
		if getattr(e, "response", None) is not None and e.response.text:
			error = f"{error}: {e.response.text}"
		_set_fbr_response(
			doc,
			{
				"custom_fbr_responsed": "Error",
				"custom_fbr_digital_invoice_response": error,
			},
		)
		frappe.throw(frappe._("FBR request failed: {0}").format(error), title=frappe._("FBR Error"))

	frappe.logger().info(f"FBR response for {doc.name}: {json.dumps(res_json, indent=2)}")

	validation = res_json.get("validationResponse", {})
	if validation.get("statusCode") == "00":
		invoice_item_nos = [
			status.get("invoiceNo", "")
			for status in validation.get("invoiceStatuses", [])
			if status.get("invoiceNo")
		]

		_set_fbr_response(
			doc,
			{
				"custom_fbr_integration_type": settings.integration_type,
				"custom_fbr_invoice_no": res_json.get("invoiceNumber", ""),
				"custom_fbr_submission_time": res_json.get("dated") or frappe.utils.now_datetime(),
				"custom_fbr_invoice_status": validation.get("status", ""),
				"custom_fbr_invoice_status_code": validation.get("statusCode", ""),
				"custom_fbr_invoice_error": validation.get("error", ""),
				"custom_fbr_invoice_statuses": json.dumps(validation.get("invoiceStatuses", []), indent=2),
				"custom_fbr_invoice_item_no": ", ".join(invoice_item_nos),
				"custom_fbr_qr_code": res_json.get("invoiceNumber", ""),
				"custom_fbr_digital_invoice_response": json.dumps(res_json, indent=2),
				"custom_fbr_responsed": "Success",
			},
		)
		return res_json

	_set_fbr_response(
		doc,
		{
			"custom_fbr_responsed": "Error",
			"custom_fbr_digital_invoice_response": json.dumps(res_json, indent=2),
		},
	)
	frappe.throw(
		frappe._("FBR rejected the invoice: {0}").format(json.dumps(res_json)),
		title=frappe._("FBR Error"),
	)


def after_submit_invoice(doc, method=None):
	"""Optional: wire this into hooks.py doc_events['Sales Invoice']['on_submit']
	if you want invoices pushed to FBR automatically on submit instead of via
	the 'Send to FBR' button."""
	send_invoice_to_fbr(doc)
