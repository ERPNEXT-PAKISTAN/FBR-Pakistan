import frappe
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def send_invoice_to_fbr(doc, method=None):
    try:
        settings = frappe.get_single("FBR Invoice Settings")

        # Use 'enabled' instead of 'enable_fbr_integration'
        if not settings.enabled:
            frappe.logger().info("FBR Integration Disabled")
            return

        # Dynamic API URL and Token selection
        if settings.integration_type == "Sandbox":
            api_url = settings.sandbox_api_url
            token = settings.sandbox_security_token
        elif settings.integration_type == "Production":
            api_url = settings.production_api_url
            token = settings.production_security_token
        else:
            frappe.throw("Invalid FBR integration type. Please set to Sandbox or Production.")

        # --- Get seller and buyer address ---
        seller_address = ""
        if getattr(doc, "company_address", None):
            company_address_doc = frappe.get_doc("Address", doc.company_address)
            seller_address = f"{company_address_doc.address_line1}, {company_address_doc.city}"

        buyer_address = ""
        if getattr(doc, "customer_address", None):
            customer_address_doc = frappe.get_doc("Address", doc.customer_address)
            buyer_address = f"{customer_address_doc.address_line1}, {customer_address_doc.city}"

        # --- Build items list ---
        items_list = [
            {
                "hsCode": item.custom_hs_code,
                "productDescription": item.item_name,
                "rate": "{:.2f}%".format(item.custom_sales_tax_rate or 0),
                "uoM": item.custom_fbr_uom,
                "quantity": item.qty,
                "totalValues": item.custom_tax_inclusive_amount,
                "valueSalesExcludingST": item.amount,
                "fixedNotifiedValueOrRetailPrice": item.rate,
                "salesTaxApplicable": item.custom_sales_tax,
                "salesTaxWithheldAtSource": 0,  # Static
                "extraTax": item.custom_extra_tax,
                "furtherTax": item.custom_further_tax,
                "sroScheduleNo": item.custom_sro_schedule_no,
                "fedPayable": 0,  # Static
                "discount": item.discount_amount,
                "saleType": item.custom_sale_type,
                "sroItemSerialNo": item.custom_sro_item_sno
            }
            for item in doc.items
        ]

        payload = {
            "invoiceType": doc.custom_invoice_type,
            "invoiceDate": str(doc.posting_date),
            "sellerNTNCNIC": doc.company_tax_id,
            "sellerBusinessName": doc.company,
            "sellerProvince": frappe.get_doc("Address", doc.company_address).state if getattr(doc, "company_address", None) else "",
            "sellerAddress": seller_address,
            "buyerNTNCNIC": doc.tax_id,
            "buyerBusinessName": doc.customer,
            "buyerProvince": frappe.get_doc("Address", doc.customer_address).state if getattr(doc, "customer_address", None) else "",
            "buyerAddress": buyer_address,
            "buyerRegistrationType": doc.custom_tax_payer_type,
            "invoiceRefNo": doc.name,
            "scenarioId": doc.custom_scenario_id,
            "items": items_list
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        frappe.logger().info(f"📤 Sending Invoice to FBR ({settings.integration_type}): {json.dumps(payload, indent=2)}")

        response = requests.post(api_url, headers=headers, json=payload, verify=False)
        response.raise_for_status()
        res_json = response.json()

        frappe.logger().info(f"✅ FBR Response: {json.dumps(res_json, indent=2)}")

        validation = res_json.get("validationResponse", {})
        if validation.get("statusCode") == "00":
            doc.custom_fbr_integration_type = settings.integration_type
            doc.custom_fbr_invoice_no = res_json.get("invoiceNumber", "")
            doc.custom_fbr_submission_time = res_json.get("dated", frappe.utils.now_datetime())
            doc.custom_fbr_invoice_status = validation.get("status", "")
            doc.custom_fbr_invoice_status_code = validation.get("statusCode", "")
            doc.custom_fbr_invoice_error = validation.get("error", "")
            doc.custom_fbr_invoice_statuses = json.dumps(validation.get("invoiceStatuses", []), indent=2)
            invoice_item_nos = []
            for status in validation.get("invoiceStatuses", []):
                invoice_item_no = status.get("invoiceNo", "")
                if invoice_item_no:
                    invoice_item_nos.append(invoice_item_no)
            doc.custom_fbr_invoice_item_no = ", ".join(invoice_item_nos)
            doc.custom_fbr_qr_code = res_json.get("invoiceNumber", "")
            doc.custom_fbr_digital_invoice_response = json.dumps(res_json, indent=2)
            doc.custom_fbr_responsed = "Success"
            doc.save(ignore_permissions=True)

            # --- Styled Success Message ---
            fbr_invoice_no = res_json.get("invoiceNumber", "")
            frappe.msgprint(
                msg=f"""
                    <div style="font-size:14px; line-height:1.6;">
                        <p>🟢 <b>Invoice Sent</b></p>
                        <p>🎉 <b>Congratulations!</b></p>
                        <p>
                            Your Sales Invoice <b>{doc.name}</b> has been successfully submitted 
                            to the <b>IRIS Portal – FBR</b>.
                        </p>
                        <p>
                            <b>FBR Invoice No:</b> {fbr_invoice_no}
                        </p>
                        <p style="color:green;">
                            ☑ Thank you for staying compliant and digital by Fibersoft ERP-Pakistan!
                        </p>
                    </div>
                """,
                title="Invoice Sent",
                indicator="green"
            )

        else:
            doc.custom_fbr_responsed = "Error"
            doc.custom_fbr_digital_invoice_response = json.dumps(res_json, indent=2)
            doc.save(ignore_permissions=True)
            frappe.throw(
                f"""
                <div style="font-size:14px; line-height:1.6; color:red;">
                    ❌ <b>FBR Error</b><br>
                    Response: {json.dumps(res_json)}
                </div>
                """
            )

    except requests.exceptions.HTTPError as e:
        doc.custom_fbr_responsed = "HTTPError"
        doc.custom_fbr_digital_invoice_response = str(e)
        doc.save(ignore_permissions=True)
        frappe.throw(
            f"""
            <div style="font-size:14px; line-height:1.6; color:red;">
                ❌ <b>FBR HTTP Exception</b><br>
                {str(e)}
            </div>
            """
        )
    except Exception as e:
        doc.custom_fbr_responsed = "Exception"
        doc.custom_fbr_digital_invoice_response = str(e)
        doc.save(ignore_permissions=True)
        frappe.throw(
            f"""
            <div style="font-size:14px; line-height:1.6; color:red;">
                ❌ <b>FBR Exception</b><br>
                {str(e)}
            </div>
            """
        )

def after_submit_invoice(doc, method=None):
    send_invoice_to_fbr(doc)
