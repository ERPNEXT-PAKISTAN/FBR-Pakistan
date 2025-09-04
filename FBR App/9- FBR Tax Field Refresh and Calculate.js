// Client Script
// Doctype : Sales invoice
// Purpose
//Extend ERPNext item-level tax handling beyond the built-in tax table.
//Allow custom tax breakdowns per line item (e.g., GST, Further Tax, Extra Tax, etc.).
//Automatically recalculate when quantity, rate, or template changes.
//Store results in custom fields for reporting, FBR integration, or invoice printi



frappe.ui.form.on('Sales Invoice Item', {
    qty: calculate_tax_fields,
    rate: calculate_tax_fields,
    item_tax_template: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        let qty = parseFloat(row.qty) || 0;
        let rate = parseFloat(row.rate) || 0;
        let amount = qty * rate;
        row.amount = amount;

        // Reset values
        row.custom_sales_tax = 0;
        row.custom_further_tax = 0;
        row.custom_extra_tax = 0;
        row.custom_other_tax_1 = 0;
        row.custom_other_tax_2 = 0;
        row.custom_total_tax_amount = 0;
        row.custom_tax_inclusive_amount = amount;

        if (row.item_tax_template) {
            frappe.db.get_list('Item Tax Template Detail', {
                filters: { parent: row.item_tax_template },
                fields: ['tax_type', 'tax_rate']
            }).then(r => {
                let sales = 0, further = 0, extra = 0, other1 = 0, other2 = 0;

                r.forEach(tax => {
                    if (tax.tax_type.includes("General Sales Tax")) {
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

                // Set calculated values
                row.custom_sales_tax = sales;
                row.custom_further_tax = further;
                row.custom_extra_tax = extra;
                row.custom_other_tax_1 = other1;
                row.custom_other_tax_2 = other2;

                row.custom_total_tax_amount = sales + further + extra + other1 + other2;
                row.custom_tax_inclusive_amount = amount + row.custom_total_tax_amount;

                frm.refresh_field("items");
            });
        } else {
            frm.refresh_field("items");
        }
    }
});

function calculate_tax_fields(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let qty = parseFloat(row.qty) || 0;
    let rate = parseFloat(row.rate) || 0;
    let amount = qty * rate;
    row.amount = amount;

    row.custom_tax_inclusive_amount = amount + (
        (row.custom_sales_tax || 0) +
        (row.custom_further_tax || 0) +
        (row.custom_extra_tax || 0) +
        (row.custom_other_tax_1 || 0) +
        (row.custom_other_tax_2 || 0)
    );

    frm.refresh_field("items");
}
