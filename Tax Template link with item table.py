for item in doc.items:
    # Reset tax rates and amounts
    item.custom_sale_tax = 0  # ← updated name
    item.custom_further_tax = 0
    item.custom_extra_tax = 0
    item.custom_sales_tax_amount = 0
    item.custom_further_tax_amount = 0
    item.custom_extra_tax_amount = 0
    item.custom_taxs_amount = 0
    item.custom_tax_inclusive = 0

    if item.item_tax_template:
        tax_details = frappe.get_all("Item Tax Template Detail",
            filters={"parent": item.item_tax_template},
            fields=["tax_type", "tax_rate"]
        )

        for tax in tax_details:
            if "Sales Tax - CCPL" in tax.tax_type:
                item.custom_sale_tax = tax.tax_rate or 0  # ← updated
            elif "Further Tax - CCPL" in tax.tax_type:
                item.custom_further_tax = tax.tax_rate or 0
            elif "Extra Tax - CCPL" in tax.tax_type:
                item.custom_extra_tax = tax.tax_rate or 0

        if item.amount:
            item.custom_sales_tax_amount = (item.amount * item.custom_sale_tax) / 100  # ← updated
            item.custom_further_tax_amount = (item.amount * item.custom_further_tax) / 100
            item.custom_extra_tax_amount = (item.amount * item.custom_extra_tax) / 100

            total_tax_amount = (
                item.custom_sales_tax_amount +
                item.custom_further_tax_amount +
                item.custom_extra_tax_amount
            )

            item.custom_taxs_amount = total_tax_amount
            item.custom_tax_inclusive = item.amount + total_tax_amount
