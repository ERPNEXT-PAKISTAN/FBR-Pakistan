import frappe
from fbr_integration.fbr_api import send_invoice_to_fbr

@frappe.whitelist()
def send_to_fbr_si(name):
    """
    Called by client script. Returns a dict:
      { "success": True, "invoice_no": "..."}
    or { "success": False, "error": "..." }
    """
    doc = frappe.get_doc("Sales Invoice", name)
    try:
        # send_invoice_to_fbr already does msgprint / save / throw as needed
        send_invoice_to_fbr(doc)
        # on success, custom_fbr_invoice_no should be set on doc
        return {"success": True, "invoice_no": doc.get("custom_fbr_invoice_no", "")}
    except Exception as e:
        # log full traceback to Error Log for debugging
        frappe.log_error(frappe.get_traceback(), "fbr_integration.send_to_fbr_si")
        return {"success": False, "error": str(e)}
