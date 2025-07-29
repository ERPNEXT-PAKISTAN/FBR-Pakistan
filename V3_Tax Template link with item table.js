# Client Script (JavaScript):
# Make two separate Client Scripts — one for:
# Doctype: Sales Invoice
# Doctype: Delivery Note
# Paste the same script for both, since the field logic applies to both.
-----------------------------------------------

  


frappe.ui.form.on('Delivery Note Item', {
    qty: calculate_tax_fields,
    rate: calculate_tax_fields,
    custom_sale_tax: calculate_tax_fields,
    custom_further_tax: calculate_tax_fields,
    custom_extra_tax: calculate_tax_fields,
    custom_city_tax: calculate_tax_fields, // optional future
});

function calculate_tax_fields(frm, cdt, cdn) {
    let row = locals[cdt][cdn];

    let qty = parseFloat(row.qty) || 0;
    let rate = parseFloat(row.rate) || 0;
    let amount = qty * rate;

    let sale_tax = parseFloat(row.custom_sale_tax) || 0;
    let further_tax = parseFloat(row.custom_further_tax) || 0;
    let extra_tax = parseFloat(row.custom_extra_tax) || 0;
    let city_tax = parseFloat(row.custom_city_tax) || 0;  // optional

    let total_tax_percent = sale_tax + further_tax + extra_tax + city_tax;
    let tax_amount = amount * (total_tax_percent / 100);
    let total_with_tax = amount + tax_amount;

    frappe.model.set_value(cdt, cdn, "custom_tax_amount", tax_amount.toFixed(2));
    frappe.model.set_value(cdt, cdn, "custom_tax_inclusive", total_with_tax.toFixed(2));
}
