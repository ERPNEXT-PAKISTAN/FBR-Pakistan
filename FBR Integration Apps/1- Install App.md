<img src="https://github.com/user-attachments/assets/d23aa314-1b8b-4a67-a518-d3bde2aca452" width="200" align="left"/>
<img src="https://github.com/user-attachments/assets/40c6f01b-d18d-4178-b507-cda0a9280e8f" width="200" align="right"/>
<br clear="both"/>
<hr/>

# 🚀 FBR Pakistan App Integration Guide

#### Welcome to the **FBR Pakistan** integration documentation! Enhance your ERPNext experience with seamless FBR data management.
---

### 1- 🛠️ Installation Steps

Follow these steps to set up the FBR Integration app in your ERPNext bench:

---

##### 🏁 **Step 1️⃣: Create the App inside your Bench**
```bash
bench new-app fbr_integration
```
---

##### ⚙️ **Step 2️⃣: Install the App on Your Site**
```bash
bench --site site1.local install-app fbr_integration
```
---

##### 🔄 **Step 3️⃣: Migrate & Restart Bench**
```bash
bench migrate && bench restart
```
---

> 💡 **Note:**  
> Replace `site1.local` with your actual site name.  
> Make sure your bench is active and running before executing these commands.

---

---

### 2- 📦 Create Doctype For FBR Invoice Taypes:  

---
### 1️⃣📑🏗️ Create Doctype Step by Step:


| Field Name         |  Field Name             |   Type            |    Doctype Name         |  Naming/Naming Rule    |                    Auto Name                |
|--------------------|-------------------------|-------------------|-------------------------|------------------------|---------------------------------------------|
| HS Code            | HS Code Detail          |  Data/Small Text  |   HS Code               | By Fieldname           | `field:hs_code`                             |
| Scenario ID        | Scenario Detail         |  Data/Data        |   Scenario ID           | Expression             | `format:{scenario_id} - {scenario_detail}`  |
| FBR UoM            |                         |  Data             |   FBR UoM               | By Fieldname           | `field:fbr_uom`                             |
| SRO Item SNo       |                         |  Data             |   SRO Item SNo          | By Fieldname           | `field:sro_item_sno`                        |
| SRO Schedule No    |                         |  Data             |   SRO Schedule No       | By Fieldname           | `field:sro_schedule_no`                     |
| Sale Type          |                         |  Data             |   Sale Type             | By Fieldname           | `field:sale_type`                           |
| Tax Payer Type     |                         |  Data             |   Tax Payer Type        | By Fieldname           | `field:tax_payer_type`                      |
| Invoice Type       |                         |  Data             |   Invoice Type          | By Fieldname           | `field:invoice_type`                        |
| Buyer Province     |                         |  Data             |   Buyer Province        | By Fieldname           | `field:buyer_province`                      |

---

### ⚙️ Settings For Import Data:

| Setting      | Details                          |  Tool   |    Check      |
|--------------|----------------------------------|---------|---------------|
| Form Setting | Allow Import (via Import Tool)   |         |   ✅ Enabled |
| Permissions  | System Manager                   | Import  |   ✅ Enabled |
---

### 🛠️ FBR Integration Settings Doctype:
#### ⚙ Doctype Name : `FBR Invoice Settings`

| Field Label                    | Type        |  Field Name                   |
|--------------------------------|-------------|-------------------------------|
| Enabled                        |   Check     | enabled                       | 
| SSL Applied                    |   Check     | ssl_applied                   |
| Integration Type               |   Select    | integration_type              |
| Sandbox API URL                |   Data      | sandbox_api_rul               | 
| Sandbox Security Token         |   Data      | sandbox_security_token        |
| Production API URL             |   Data      | production_api_url            |
| Production Security Token      |   Data      | production_security_token     |


---
⬆️
### 🔸⬅ OR ➡🔸
⬇️


---

### *1️⃣ Create From `Copy to Clipboard`* 

#### 📝 Doctype Links  
[Go to Doctype Directory »](https://github.com/ERPNEXT-PAKISTAN/FBR-Pakistan/tree/main/Doctype)

---
---

### 3- 📥 Download & Upload Excel Data into ERPNext:  
[![Excel Icon](https://img.icons8.com/fluency/24/000000/ms-excel.png)](https://github.com/ERPNEXT-PAKISTAN/FBR-Pakistan/tree/main/FBR%20Tax%20Type%20Excel%20Data)  
**Download Excel Data and Upload into Doctype:**  
[Go to FBR Invoice Tax Type »](https://github.com/ERPNEXT-PAKISTAN/FBR-Pakistan/tree/main/FBR%20Tax%20Type%20Excel%20Data)

---

> 🚀 **Tip:**  

---

### 4- 📑🏗️ 🏷️ Create Field on Sales Invoice, Sales Invoice Item & on Item Master :


| Field Name           |   Create & Link On    |   Type    |     Option          |    Fetch From              |  Select Field       |  Create On          | 
|----------------------|-----------------------|-----------|---------------------|----------------------------|---------------------|---------------------|
| Scenario ID          | Sales Invoice         |  Data     |                     | custom_scenario_detail     | Senario ID (Data)   |  Sales Invoice      |
| Scenario Detail      | Sales Invoice         |  Link     |  Scenario ID        |                            |                     |  Sales Invoice      |
| Tax Payer Type       | Sales Invoice         |  Link     |  Tax Payer Type     |                            |                     |  Customer Master    |
| Buyer Province       | Sales Invoice         |  Link     |  Buyer Province     |                            |                     |  Customer Master    |
| Invoice Type         | Sales Invoice         |  Link     |  Invoice Type       |                            |                     |  Sales Invoice      |
| HS Code              | Sales Invoice Item    |  Link     |  HS Code            |                            |                     |  Item Master        |
| FBR UoM              | Sales Invoice Item    |  Link     |  FBR UoM            |                            |                     |  Item Master        |
| SRO Item SNo         | Sales Invoice Item    |  Link     |  SRO Item SNo       |                            |                     |  Item Master        |
| SRO Schedule No      | Sales Invoice Item    |  Link     |  SRO Schedule No    |                            |                     |  Item Master        |
| Sale Type            | Sales Invoice Item    |  Link     |  Sale Type          |                            |                     |  Item Master        |


---
---

### 5- 🎯📑🏷️ FBR Response


| Field Name                      |  Field Name                          |    Data Type          | 
|---------------------------------|--------------------------------------|-----------------------|
| FBR Integration Type            | custom_fbr_integration_type          |   Data                | 
| FBR Invoice No                  | custom_fbr_invoice_no                |   Data                | 
| FBR Invoice Status              | custom_fbr_invoice_status            |   Data                |                   
| FBR Submission Time             | custom_fbr_submission_time           |   DateTime            |                   
| FBR Invoice Status Code         | custom_fbr_invoice_status_code       |   Data                |                   
| FBR QR Code                     | custom_fbr_qr_code                   |   Barcode             |                    
| FBR Responsed                   | custom_fbr_responsed                 |   Data                |                    
| FBR Invoice Item No             | custom_fbr_invoice_item_no           |   Long Text           |                    
| FBR Invoice Statuses            | custom_fbr_invoice_statuses          |   Long Text           |                    
| FBR Digital Invoice Response    | custom_fbr_digital_invoice_response  |   Long Text           |                    

---
---

### 6- 📑🏷️ Create Tax Fiels on Sales Invoice Item :

| Tax Rate Fields          | Tax Amount Fields    | 
|--------------------------|----------------------|
| Sales Tax Rate           | Sales Tax            |  
| Further Tax Rate         | Further Tax          | 
| Extra Tax Rate           | Extra Tax            |                  
| Other Tax 1 Rate         | Other Tax 1          |                  
| Other Tax 2 Rate         | Other Tax 2          |                 
| Tax Inclusive Amount     | Total Tax Amount     |          
---
```
 `Rate     ➡ Tax Exclusive Rate`
 `Amount   ➡ Change to Tax Exclusive Amount`  
```
---
---

### 7- 🚀 **Install the Following Script**
#### 🛠️ ➡ handler.py
#### 🛠️ ➡ hooks.py
#### 🛠️ ➡ fbr_api.py
#### 🛠️ ➡ FBR Tax Calculation.py
#### 🛠️ ➡ FBR Tax Calculation Clear/Refresh.js
#### 🛠️ ➡ Send to FBR.js
---
---

#### 🏷️ Tax Rate Fields :
```
Sales Tax Rate 
```
```
Further Tax Rate
```
```
Extra Tax Rate
```
```
Other Tax 1 Rate
```
```
Other Tax 2 Rate
```
```
Tax Inclusive Amount
```
```
Total Tax Amount
```
---

#### 🏷️ Tax Amount Fields :
```
Sales Tax 
```
```
Further Tax
```
```
Extra Tax
```
```
Other Tax 1
```
```
Other Tax 2
```

---
---
### 8- 📑 Chart of Account - Create GL Tax Accounts
```
General Sales Tax 
```
```
Further Tax
```
```
Extra Tax
```
```
Other Tax 1
```
```
Other Tax 2
```
---
---

### 9- 🏷️📑 Item Tax Template - Tax Masters
➡ Create Tax Templates     
➡ Attach with Item     



---
---
---
### 🏷️💡📑| Doctype Name & Field Name
---

```
HS Code 
```
```
HS Code Detail
```
```
Scenario ID
```
```
Scenario Detail
```
```
BR UoM
```
```
SRO Item SNo
```
```
SRO Schedule No
```
```
Sale Type
```
```
Tax Payer Type
```
```
Invoice Type     
```
```
Buyer Province
```
---


---
<img src="https://img.icons8.com/fluency/48/workspace.png" width="32" alt="workspace icon" />
Happy Integrating with FBR Pakistan!
