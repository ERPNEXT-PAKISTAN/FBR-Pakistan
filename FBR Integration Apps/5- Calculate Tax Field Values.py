# Server Script to Calculate Tax Values on Sales Invoice Item:
# Script Type : DocType Event
# Reference Document Type : Sales Invoice
# DocType Event : Before Save



for item in doc.items:
    # Reset tax values
    item.custom_sales_tax_rate = 0
    item.custom_further_tax_rate = 0
    item.custom_extra_tax_rate = 0
    item.custom_other_tax_1_rate = 0
    item.custom_other_tax_2_rate = 0

    item.custom_sales_tax = 0
    item.custom_further_tax = 0
    item.custom_extra_tax = 0
    item.custom_other_tax_1 = 0
    item.custom_other_tax_2 = 0

    item.custom_total_tax_amount = 0
    item.custom_tax_inclusive_amount = item.amount or 0

    if item.item_tax_template:
        tax_details = frappe.get_all(
            "Item Tax Template Detail",
            filters={"parent": item.item_tax_template},
            fields=["tax_type", "tax_rate"]
        )

        for tax in tax_details:
            tax_type = tax.tax_type or ""

            if "General Sales Tax" in tax_type:                                 # Use your Own GL Account From Chart of Account...
                item.custom_sales_tax_rate = tax.tax_rate or 0
            elif "Further Tax" in tax_type:                                     # Use your Own GL Account From Chart of Account...
                item.custom_further_tax_rate = tax.tax_rate or 0
            elif "Extra Tax" in tax_type:                                       # Use your Own GL Account From Chart of Account...
                item.custom_extra_tax_rate = tax.tax_rate or 0
            elif "Other Tax 1" in tax_type:                                     # Use your Own GL Account From Chart of Account...
                item.custom_other_tax_1_rate = tax.tax_rate or 0 
            elif "Other Tax 2" in tax_type:                                     # Use your Own GL Account From Chart of Account...
                item.custom_other_tax_2_rate = tax.tax_rate or 0

        # Calculate tax amounts
        if item.amount:
            item.custom_sales_tax = (item.amount * item.custom_sales_tax_rate) / 100       
            item.custom_further_tax = (item.amount * item.custom_further_tax_rate) / 100   
            item.custom_extra_tax = (item.amount * item.custom_extra_tax_rate) / 100      
            item.custom_other_tax_1 = (item.amount * item.custom_other_tax_1_rate) / 100 
            item.custom_other_tax_2 = (item.amount * item.custom_other_tax_2_rate) / 100 

            item.custom_total_tax_amount = (
                item.custom_sales_tax
                + item.custom_further_tax
                + item.custom_extra_tax
                + item.custom_other_tax_1
                + item.custom_other_tax_2
            )

            item.custom_tax_inclusive_amount = item.amount + item.custom_total_tax_amount
