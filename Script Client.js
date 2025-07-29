frappe.ui.form.on('Sales Invoice Item', {
    qty: calculate_tax_fields,
    rate: calculate_tax_fields,
    custom_sales_tax_rate: calculate_tax_fields,
    custom_further_tax_rate: calculate_tax_fields,
    custom_extra_tax_rate: calculate_tax_fields
});

function calculate_tax_fields(frm, cdt, cdn) {
    let row = locals[cdt][cdn];

    let qty = parseFloat(row.qty) || 0;
    let rate = parseFloat(row.rate) || 0;
    let amount = qty * rate;
    row.amount = amount;

    // Reset tax values
    row.custom_sales_tax = 0;
    row.custom_further_tax = 0;
    row.custom_extra_tax = 0;
    row.custom_total_tax_amount = 0;
    row.custom_tax_inclusive_amount = amount;

    if (amount) {
        if (row.custom_sales_tax_rate) {
            row.custom_sales_tax = (amount * row.custom_sales_tax_rate) / 100;
            row.custom_tax_inclusive_amount += row.custom_sales_tax;
        }
        if (row.custom_further_tax_rate) {
            row.custom_further_tax = (amount * row.custom_further_tax_rate) / 100;
            row.custom_tax_inclusive_amount += row.custom_further_tax;
        }
        if (row.custom_extra_tax_rate) {
            row.custom_extra_tax = (amount * row.custom_extra_tax_rate) / 100;
            row.custom_tax_inclusive_amount += row.custom_extra_tax;
        }

        row.custom_total_tax_amount = (
            row.custom_sales_tax +
            row.custom_further_tax +
            row.custom_extra_tax
        );
    }

    frm.refresh_field("items");
}
