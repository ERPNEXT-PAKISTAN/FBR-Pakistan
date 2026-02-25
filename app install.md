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

```
cd ~/frappe-bench
bench get-app https://github.com/ERPNEXT-PAKISTAN/FBR_Integration.git --branch main
bench --site site1.local install-app fbr_integration
bench migrate
bench restart
```
## System Dependencies (Required)
#### wkhtmltopdf (patched)
#### ERPNext PDF printing requires the patched build of wkhtmltopdf.
#### Ubuntu Jammy example:

```
sudo apt install -y fontconfig xfonts-75dpi xfonts-base \
  libxrender1 libxext6 libfontconfig1 libfreetype6 libjpeg-turbo8
```
wget -O wkhtmltox.deb \
https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
```
sudo apt install -y ./wkhtmltox.deb
wkhtmltopdf --version
```

##### Then set Bench Config:
```
bench set-config -g wkhtmltopdf_path "$(which wkhtmltopdf)"
bench restart
```

Python Dependencies
Installed automatically via pyproject.toml:
    requests
    qrcode
    pillow
    python-barcode

Configuration
FBR Invoice Settings

Go to: FBR Invoice Settings
      Enable integration
      Choose Sandbox / Production
      Add API URL + Security Token
Usage
1. Create Sales Invoice
2. Submit Sales Invoice (docstatus=1)
3. Click Send to FBR
4. On success:
      FBR Invoice No stored
      Full response stored in Sales Invoice
      QR + Barcode displayed in dialog + HTML field


Reports (Module: FBR Integration)
    FBR Sales Summary
    FBR Item Wise


Troubleshooting
UnicodeDecodeError (UTF-8)

If you see errors like 0x96 or 0x92, convert JS/PY files to UTF-8 and ensure .editorconfig + .gitattributes exist.



License / Commercial Use
This project can be distributed commercially. For commercial licensing, support, and custom deployments, contact:
Email: taimoor986@gmail.com


Support
  Open an issue on GitHub with:
      ERPNext/Frappe versions
      Exact error log
      Screenshot (if UI issue)



---
## 3) SaaS deployment + commercial packaging structure
For **SaaS / marketplace / commercial ERP**, add these **folders/files** (recommended):


fbr_integration/
├── README.md
├── LICENSE
├── pyproject.toml
├── MANIFEST.in
├── .editorconfig
├── .gitattributes
├── .github/
│ └── workflows/
│ └── ci.yml
├── fbr_integration/
│ ├── hooks.py
│ ├── patches.txt
│ ├── patches/
│ ├── fixtures/
│ ├── public/
│ ├── templates/
│ ├── www/
│ └── ...
└── deployment/
├── docker/
│ ├── Dockerfile
│ └── docker-compose.yml
├── bench_install.sh
└── saas_checklist.md



```

### What to put inside `deployment/`
- **bench_install.sh**: installs dependencies, wkhtmltopdf, pip libs, installs app, runs migrate/build.
- **saas_checklist.md**: checklist for tenants (token setup, roles, workspace, print format defaults).

This makes it “marketplace-grade”.

---

## 4) Step-by-step: Upload to GitHub (from your server)

### Step 0 — Go to app folder
```bash
cd ~/frappe-bench/apps/fbr_integration
```



Step 1 — Ensure git is initialized
```
git status
```











