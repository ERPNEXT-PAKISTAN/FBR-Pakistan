app_name = "fbr_integration"
app_title = "FBR Integration"
app_publisher = "FBR Pakistan / ERPNext Pakistan Community"
app_description = "FBR (Federal Board of Revenue) Digital Invoicing Integration for ERPNext / Frappe v16"
app_email = "mail@agrovisions.com"
app_license = "MIT"
app_version = "2.0.0"

# Required apps
# ------------------
# ERPNext v16.x is required (Sales Invoice / Sales Invoice Item / Item / Customer
# doctypes this app extends). Frappe itself is implicit and doesn't need listing.
required_apps = ["erpnext"]

# Includes in <head>
# ------------------
# app_include_css = "/assets/fbr_integration/css/fbr_integration.css"
# app_include_js = "/assets/fbr_integration/js/fbr_integration.js"

# Client side script attached to specific doctypes
# -------------------------------------------------
doctype_js = {
	"Sales Invoice": "public/js/sales_invoice.js",
}

# Fixtures
# --------
# Custom Fields (Item, Customer, Sales Invoice, Sales Invoice Item) are shipped
# as fixtures so `bench migrate` recreates them automatically on every site.
fixtures = [
	{
		"dt": "Custom Field",
		"filters": [["module", "in", ["FBR Integration"]], ["dt", "in", [
			"Item", "Customer", "Sales Invoice", "Sales Invoice Item"
		]]]
	}
]

# Document Events
# ---------------
# 1) `before_save` recalculates the FBR tax breakup on every Sales Invoice save
#    (equivalent to the "FBR Tax Calculation" server script in the guide).
# 2) `on_submit` is left commented out by default: the app ships with a
#    "Send to FBR" button (see public/js/sales_invoice.js) instead of an
#    automatic submit-time push. Uncomment on_submit below if you prefer the
#    invoice to be sent to FBR automatically the moment it is submitted.
doc_events = {
	"Sales Invoice": {
		"before_validate": "fbr_integration.fbr_integration.tax_calculation.apply_unregistered_tax_templates",
		"before_save": "fbr_integration.fbr_integration.tax_calculation.calculate_fbr_taxes",
		"before_submit": "fbr_integration.fbr_integration.tax_calculation.calculate_fbr_taxes",
		# "on_submit": "fbr_integration.fbr_integration.fbr_api.after_submit_invoice",
	}
}

# Installation
# ------------
after_install = "fbr_integration.setup.install.after_install"
after_migrate = "fbr_integration.setup.install.after_migrate"

# Whitelisted API surface used by the client script
# --------------------------------------------------
# fbr_integration.fbr_integration.handler.send_to_fbr_si

# Desktop / App switcher icon
# ----------------------------
app_logo_url = "/assets/fbr_integration/images/fbr_integration-logo.svg"

add_to_apps_screen = [
	{
		"name": "fbr_integration",
		"logo": "/assets/fbr_integration/images/fbr_integration-logo.svg",
		"title": "FBR Integration",
		"route": "/app/fbr-integration",
	}
]

