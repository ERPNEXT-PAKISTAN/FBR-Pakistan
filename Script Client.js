frappe.ui.form.on('Sales Invoice Item', {
    qty: calculate_tax_inclusive,
    rate: calculate_tax_inclusive,
    custom_total_tax_amount: calculate_tax_inclusive
});

function calculate_tax_inclusive(frm, cdt, cdn) {
    let row = locals[cdt][cdn];

    let qty = parseFloat(row.qty) || 0;
    let rate = parseFloat(row.rate) || 0;
    let amount = qty * rate;

    let total_tax = parseFloat(row.custom_total_tax_amount) || 0;
    let inclusive_amount = amount + total_tax;

    frappe.model.set_value(cdt, cdn, "amount", amount.toFixed(2));
    frappe.model.set_value(cdt, cdn, "custom_tax_inclusive_amount", inclusive_amount.toFixed(2));
}
