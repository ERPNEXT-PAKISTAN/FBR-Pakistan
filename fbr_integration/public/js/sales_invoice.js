// Copyright (c) 2026, FBR Pakistan Integration and contributors
// For license information, please see license.txt
//
// Sales Invoice client script:
//   1. Live tax breakup preview while editing item rows (mirrors the
//      server-side calculation in fbr_integration/tax_calculation.py so the
//      user sees the numbers update instantly, before the row is saved).
//   2. "Send to FBR" button on submitted invoices, calling the whitelisted
//      fbr_integration.fbr_integration.handler.send_to_fbr_si method.

frappe.ui.form.on("Sales Invoice Item", {
	qty: calculate_tax_preview,
	rate: calculate_tax_preview,
	item_tax_template: function (frm, cdt, cdn) {
		calculate_tax_preview(frm, cdt, cdn);
	},
});

function calculate_tax_preview(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	let qty = parseFloat(row.qty) || 0;
	let rate = parseFloat(row.rate) || 0;
	let amount = qty * rate;

	row.custom_sales_tax = 0;
	row.custom_further_tax = 0;
	row.custom_extra_tax = 0;
	row.custom_other_tax_1 = 0;
	row.custom_other_tax_2 = 0;
	row.custom_total_tax_amount = 0;
	row.custom_tax_inclusive_amount = amount;

	if (!row.item_tax_template) {
		frm.refresh_field("items");
		return;
	}

	frappe.db.get_list("Item Tax Template Detail", {
		filters: { parent: row.item_tax_template },
		fields: ["tax_type", "tax_rate"],
	}).then((rows) => {
		let sales = 0, further = 0, extra = 0, other1 = 0, other2 = 0;

		rows.forEach((tax) => {
			// Update these labels if your Chart of Accounts tax names differ
			if (
				tax.tax_type.includes("General Sales Tax") ||
				tax.tax_type.startsWith("Sales Tax -") ||
				tax.tax_type.startsWith("GST -")
			) {
				sales = (amount * (tax.tax_rate || 0)) / 100;
			} else if (tax.tax_type.includes("Further Tax")) {
				further = (amount * (tax.tax_rate || 0)) / 100;
			} else if (tax.tax_type.includes("Extra Tax")) {
				extra = (amount * (tax.tax_rate || 0)) / 100;
			} else if (tax.tax_type.includes("Other Tax 1")) {
				other1 = (amount * (tax.tax_rate || 0)) / 100;
			} else if (tax.tax_type.includes("Other Tax 2")) {
				other2 = (amount * (tax.tax_rate || 0)) / 100;
			}
		});

		row.custom_sales_tax = sales;
		row.custom_further_tax = further;
		row.custom_extra_tax = extra;
		row.custom_other_tax_1 = other1;
		row.custom_other_tax_2 = other2;
		row.custom_total_tax_amount = sales + further + extra + other1 + other2;
		row.custom_tax_inclusive_amount = amount + row.custom_total_tax_amount;

		frm.refresh_field("items");
	});
}

frappe.ui.form.on("Sales Invoice", {
	refresh: function (frm) {
		if (frm.doc.docstatus !== 1) {
			return;
		}

		let btn = frm.add_custom_button(__("Send to FBR"), function () {
			if (frm.doc.custom_fbr_invoice_no) {
				frappe.msgprint({
					title: __("Already Submitted"),
					indicator: "orange",
					message: __(
						"This invoice was already sent to the IRIS FBR Portal.<br>FBR Invoice No: <b>{0}</b>",
						[frm.doc.custom_fbr_invoice_no]
					),
				});
				return;
			}

			frappe.call({
				method: "fbr_integration.fbr_integration.handler.prepare_fbr_si",
				args: { name: frm.doc.name },
				freeze: true,
				freeze_message: __("Preparing FBR invoice preview..."),
				callback: function (r) {
					let preview = r && r.message;
					if (!preview || preview.success === false) {
						frappe.msgprint({
							title: __("FBR Error"),
							indicator: "red",
							message: frappe.utils.escape_html((preview && preview.error) || __("Could not prepare the FBR payload.")),
						});
						return;
					}

					frm.doc.custom_fbr_invoice_date = preview.invoice_date;
					frm.doc.custom_fbr_invoice_ref_no = preview.invoice_ref_no;
					frm.doc.custom_fbr_request_payload = preview.payload_json;
					frm.refresh_fields();

					let payload = frappe.utils.escape_html(preview.payload_json);
					frappe.confirm(
						__("Review the exact payload below. Send this invoice to FBR?<pre style='max-height: 55vh; overflow: auto; white-space: pre-wrap; text-align: left;'>") +
							payload + "</pre>",
						function () {
							frappe.call({
								method: "fbr_integration.fbr_integration.handler.send_to_fbr_si",
								args: { name: frm.doc.name },
								freeze: true,
								freeze_message: __("Sending invoice to FBR..."),
								callback: function (send_response) {
									let result = send_response && send_response.message;
									if (!result || result.success === false) {
										frappe.msgprint({
											title: __("FBR Error"),
											indicator: "red",
											message: `<pre>${frappe.utils.escape_html((result && result.error) || __("No response received from the server."))}</pre>`,
										});
										frm.reload_doc();
										return;
									}

									frappe.msgprint({
										title: __("Invoice Sent"),
										indicator: "green",
										message: __(
											"Sales Invoice {0} was submitted to the IRIS FBR Portal.<br>FBR Invoice No: <b>{1}</b>",
											[frm.doc.name, result.invoice_no]
										),
									});
									frm.reload_doc();
								},
							});
						}
					);
				},
			});
		});

		btn.removeClass("btn-default").addClass("btn-primary");
	},
});
