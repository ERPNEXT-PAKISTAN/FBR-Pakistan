## 🔹 Create Doctype for FBR Data

---
#### *1️⃣ Create From `Copy to Clipboard`*  
🔗 *https://github.com/ERPNEXT-PAKISTAN/FBR-Pakistan/tree/main/Doctype*   

#### *2️⃣ Create Doctype Step by Step:*   
---
---
---
### 1️⃣📑🏗️ Create Doctype Step by Step:


| Field Name         |  Field Name             |   Type        |    Doctype Name         |  Naming/Naming Rule    |                    Auto Name                |
|--------------------|-------------------------|---------------|-------------------------|------------------------|---------------------------------------------|
| HS Code            | HS Code Detail          |  Float        |   HS Code               | Expression             | `format:{hs_code} - {hs_code_detail}`  |
| Scenario ID        | Scenario Detail         |  Data         |   Scenario ID           | Expression             | `format:{scenario_id} - {scenario_detail}`  |
| FBR UoM            |                         |  Data         |   FBR UoM               | By Fieldname           | `field:fbr_uom`                             |
| SRO Item SNo       |                         |  Data         |   SRO Item SNo          | By Fieldname           | `field:sro_item_sno`                        |
| SRO Schedule No    |                         |  Data         |   SRO Schedule No       | By Fieldname           | `field:sro_schedule_no`                     |
| Sale Type          |                         |  Data         |   Sale Type             | By Fieldname           | `field:sale_type`                           |
| Tax Payer Type     |                         |  Data         |   Tax Payer Type        | By Fieldname           | `field:tax_payer_type`                      |
| Invoice Type       |                         |  Data         |   Invoice Type          | By Fieldname           | `field:invoice_type`                        |
| Buyer Province     |                         |  Data         |   Buyer Province        | By Fieldname           | `field:buyer_province`                      |

---

### ⚙️ Settings For Import Data:

| Setting      | Details                          |  Tool   |    Check      |
|--------------|----------------------------------|---------|---------------|
| Form Setting | Allow Import (via Import Tool)   |         |   ✅ Enabled |
| Permissions  | System Manager                   | Import  |   ✅ Enabled |

---
---

### 2️⃣📑🏗️ 🏷️ Create Field on Sales Invoice :


| Field Name           |  Field Name             |   Type    |     Option          |    Fetch From              |  Select Field       |   
|----------------------|-------------------------|-----------|---------------------|----------------------------|---------------------|
| HS Code              |                         |  Data     |                     | custom_hs_code_detail      | HS Code (Data)      | 
| HS Code Detail       |                         |  Link     |  HS Code            |                            |                     |
| Scenario ID          |                         |  Data     |                     | custom_scenario_detail     | Senario ID (Data)   |   
| Scenario Detail      |                         |  Link     |  Scenario ID        |                            |                     |  
| FBR UoM              |                         |  Link     |  FBR UoM            |                            | 
| SRO Item SNo         |                         |  Link     |  SRO Item SNo       |                            | 
| SRO Schedule No      |                         |  Link     |  SRO Schedule No    |                            |
| Sale Type            |                         |  Link     |  Sale Type          |                            | 
| Tax Payer Type       |                         |  Link     |  Tax Payer Type     |                            |
| Invoice Type         |                         |  Link     |  Invoice Type       |                            | 
| Buyer Province       |                         |  Link     |  Buyer Province     |                            | 


---
---

### 3️⃣🎯📑🏷️ FBR Response


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
