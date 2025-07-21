# this script is used to link item tax template with custom fiel create on delivery note item table.
# field name is "custom_taxs_rate" and "custom_taxs_amount" & "custom_tax_inclusive"


for item in doc.items:
    item.custom_taxs_rate = 0
    item.custom_taxs_amount = 0
    item.custom_tax_inclusive = 0

    if item.item_tax_template:
        tax_details = frappe.get_all("Item Tax Template Detail",
            filters={"parent": item.item_tax_template},
            fields=["tax_type", "tax_rate"]
        )

        if tax_details:
            item.custom_taxs_rate = tax_details[0].tax_rate or 0

            if item.amount:
                item.custom_taxs_amount = (item.amount * item.custom_taxs_rate) / 100
                item.custom_tax_inclusive = item.amount + item.custom_taxs_amount
