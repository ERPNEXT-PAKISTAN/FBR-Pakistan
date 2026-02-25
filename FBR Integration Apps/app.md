# FBR Integration (ERPNext / Frappe v15)

FBR Integration is a Frappe/ERPNext v15 application for submitting Sales Invoices to Pakistan FBR (IRIS Digital Invoicing) with:
- One-click “Send to FBR”
- Auto tax calculation from Item Tax Template
- Storage of full FBR response in Sales Invoice
- QR Code + Barcode generation (UI + optional print format)
- Reports + Workspace + Dashboard shipped via fixtures

---

## Compatibility
- Frappe: v15.x
- ERPNext: v15.x
- Python: >= 3.10

---

## Features
### Sales Invoice
- Live tax calculation while editing (`fbr_tax_calculation_clear.js`)
- “Send to FBR” button (purple) with:
  - Duplicate submission protection
  - Success dialog showing FBR Invoice No
  - QR Code + Barcode rendering
  - Print + PDF download actions

### FBR Masters (Doctypes shipped in the app)
- Buyer Province
- Tax Payer Type
- Scenario ID
- Sale Type
- SRO Schedule No
- SRO Item SNo
- Invoice Type
- HS Code
- FBR UOM
- FBR Invoice Settings

### Fixtures (auto-created on install)
- Custom Fields (Sales Invoice, Sales Invoice Item)
- Reports
- Dashboards
- Workspaces
- Print Formats (if created under module “FBR Integration”)

---

## Installation

### 1) Get the app
```bash
cd ~/frappe-bench
bench get-app https://github.com/<your-org-or-user>/fbr_integration.git
