import frappe
from fbr_integration.fbr_api import send_invoice_to_fbr

@frappe.whitelist()
def send_to_fbr_si(name):
    doc = frappe.get_doc("Sales Invoice", name)
    return send_invoice_to_fbr(doc)
