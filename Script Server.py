for item in doc.items:
    # Reset tax values
    item.custom_sales_tax_rate = 0
    item.custom_further_tax_rate = 0
    item.custom_extra_tax_rate = 0
    item.custom_sales_tax = 0
    item.custom_further_tax = 0
    item.custom_extra_tax = 0
    item.custom_total_tax_amount = 0
    item.custom_tax_inclusive_amount = 0

    if item.item_tax_template:
        tax_details = frappe.get_all("Item Tax Template Detail",
            filters={"parent": item.item_tax_template},
            fields=["tax_type", "tax_rate"]
        )

        for tax in tax_details:
            if "General Sales Tax - TCPLD" in tax.tax_type:         # Use your Own GL Account From Chart of Account...
                item.custom_sales_tax_rate = tax.tax_rate or 0
            elif "Further Tax - TCPLD" in tax.tax_type:             # Use your Own GL Account From Chart of Account...
                item.custom_further_tax_rate = tax.tax_rate or 0
            elif "Extra Tax - TCPLD" in tax.tax_type:               # Use your Own GL Account From Chart of Account...
                item.custom_extra_tax_rate = tax.tax_rate or 0

        if item.amount:
            item.custom_sales_tax = (item.amount * item.custom_sales_tax_rate) / 100
            item.custom_further_tax = (item.amount * item.custom_further_tax_rate) / 100
            item.custom_extra_tax = (item.amount * item.custom_extra_tax_rate) / 100

            item.custom_total_tax_amount = (
                item.custom_sales_tax +
                item.custom_further_tax +
                item.custom_extra_tax
            )

            item.custom_tax_inclusive_amount = item.amount + item.custom_total_tax_amount
