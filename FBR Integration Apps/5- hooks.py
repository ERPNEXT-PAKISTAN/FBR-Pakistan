app_name = "fbr_integration"
app_title = "FBR Integration"
app_publisher = "Taimoor"
app_description = "FBR Digital Invoice Integration"
app_email = "tymuur@outlook.com"
app_license = "MIT"

# include client side JS (this path is relative to /assets after build)
app_include_js = "/assets/fbr_integration/js/sales_invoice.js"

doc_events = {
    "Sales Invoice": {
        "on_submit": "fbr_integration.fbr_api.after_submit_invoice"
    }
}
