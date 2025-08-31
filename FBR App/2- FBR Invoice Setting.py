{
  "doctype": "DocType",
  "name": "FBR Invoivr Settings",
  "module": "FBR Integration",
  "custom": 0,
  "is_single": 1,
  "fields": [
    {"fieldname": "enabled", "label": "Enabled", "fieldtype": "Check", "default": 1},
    {"fieldname": "ssl_applied", "label": "SSL Applied", "fieldtype": "Check", "default": 1},
    {"fieldname": "integration_type", "label": "Integration Type", "fieldtype": "Select", "options": "Sandbox\nLive", "default": "Sandbox"},
    {"fieldname": "sandbox_api_url", "label": "Sandbox API URL", "fieldtype": "Data", "reqd": 1},
    {"fieldname": "live_api_url", "label": "Live API URL", "fieldtype": "Data"},
    {"fieldname": "sandbox_token", "label": "Sandbox Security Token", "fieldtype": "Password"},
    {"fieldname": "live_token", "label": "Live Security Token", "fieldtype": "Password"},
    {"fieldname": "seller_ntn", "label": "Seller NTN/REG", "fieldtype": "Data", "reqd": 1},
    {"fieldname": "seller_province", "label": "Seller Province", "fieldtype": "Data", "default": "Punjab"},
    {"fieldname": "api_timeout", "label": "API Timeout (sec)", "fieldtype": "Int", "default": 30}
  ]
}
