import frappe


def execute():
	field_name = "Sales Invoice Item-custom_fbr_total_values"
	if frappe.db.exists("Custom Field", field_name):
		frappe.delete_doc("Custom Field", field_name, force=True)