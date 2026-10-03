# Copyright (c) 2026, FBR Pakistan Integration and contributors
# For license information, please see license.txt

import frappe

from fbr_integration.fbr_integration.fbr_api import prepare_fbr_request, send_invoice_to_fbr


def _get_submitted_invoice(name):
	doc = frappe.get_doc("Sales Invoice", name)
	doc.check_permission("write")
	if doc.docstatus != 1:
		frappe.throw(frappe._("Sales Invoice must be submitted before sending to FBR."))
	return doc


@frappe.whitelist()
def prepare_fbr_si(name):
	"""Prepare and persist the exact payload for user review before submission."""
	try:
		doc = _get_submitted_invoice(name)
		if doc.custom_fbr_invoice_no:
			return {"success": False, "error": frappe._("This invoice was already sent to FBR.")}

		payload, payload_json = prepare_fbr_request(doc)
		return {
			"success": True,
			"invoice_date": doc.custom_fbr_invoice_date,
			"invoice_ref_no": doc.custom_fbr_invoice_ref_no,
			"payload": payload,
			"payload_json": payload_json,
		}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "fbr_integration.prepare_fbr_si")
		frappe.clear_last_message()
		return {"success": False, "error": str(e)}


@frappe.whitelist()
def send_to_fbr_si(name):
	"""
	Called by the "Send to FBR" client script button on Sales Invoice.

	Returns:
		{"success": True, "invoice_no": "..."}
		{"success": False, "error": "..."}
	"""
	try:
		doc = _get_submitted_invoice(name)
		if doc.custom_fbr_invoice_no:
			return {"success": False, "error": frappe._("This invoice was already sent to FBR.")}

		send_invoice_to_fbr(doc)
		return {"success": True, "invoice_no": doc.get("custom_fbr_invoice_no", "")}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "fbr_integration.send_to_fbr_si")
		frappe.clear_last_message()
		return {"success": False, "error": str(e)}
