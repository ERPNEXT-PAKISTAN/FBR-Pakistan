## 🔹 Create Doctype & Field on Sales Invoice for FBR Data

---

### 🏷️ List of Doctype


| Field Name         |  Field Name             | Doctype Name          |  Naming/Naming Rule |                    Auto Name                |
|--------------------|-------------------------|-----------------------|---------------------|---------------------------------------------|
| HS Code            | HS Code Description     | HS Code               | Expression          | `format:{hs_code} - {hs_code_description}`  |
| Scenario ID        | Scenario Detail         | Scenario ID           | Expression          | `format:{scenario_id} - {scenario_detail}`  |
| FBR UoM            |                         | FBR UoM               | By Fieldname        | `field:fbr_uom`                             |
| SRO Item SNo       |                         | SRO Item SNo          | By Fieldname        | `field:sro_item_sno`                        |
| SRO Schedule No    |                         | SRO Schedule No       | By Fieldname        | `field:sro_schedule_no`                     |
| Sale Type          |                         | Sale Type             | By Fieldname        | `field:sale_type`                           |
| Tax Payer Type     |                         | Tax Payer Type        | By Fieldname        | `field:tax_payer_type`                      |
| Invoice Type       |                         | Invoice Type          | By Fieldname        | `field:invoice_type`                        |
| Buyer Province     |                         | Buyer Province        | By Fieldname        | `field:buyer_province`                      |

---


### ⚙️ Settings For Import Data:

| Setting         | Details                          |  Tool      |    Check    |
|-----------------|----------------------------------|------------|-------------|
| Form Setting    | Allow Import (via Import Tool)   |            | ✅ Enabled  |
| Permissions     | System Manager                   | Import     | ✅ Enabled  |

---

### 🏷️ FBR Response


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


### 🏷️| Doctype Name & Field Name
---

```
 HS Code 
```
```
HS Code Description
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
