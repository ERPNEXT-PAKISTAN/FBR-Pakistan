## 🔹 Create Doctype for FBR Data

---

### 🏷️ List of Doctype


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

### 🏷️ List of Doctype


| Field Name           |  Field Name             |   Type        |     Option          |    Fetch From              |  Select Field       |   
|----------------------|-------------------------|---------------|---------------------|----------------------------|---------------------|
| HS Code              |                         |  Data         |                     |                            |                     | 
| HS Code Detail       |                         |  Link         |  HS Code            | 
| Scenario ID          |                         |  Link         |  Scenario ID        |                            |                     |    
| Scenario Detail      |                         |  Data         |                     | custom_scenario_details    | Senario ID (Data)   |   
| FBR UoM              |                         |  Link         |  FBR UoM            |                            | 
| SRO Item SNo         |                         |  Link         |  SRO Item SNo       |                            | 
| SRO Schedule No      |                         |  Link         |  SRO Schedule No    |                            |
| Sale Type            |                         |  Link         |  Sale Type          |                            | 
| Tax Payer Type       |                         |  Link         |  Tax Payer Type     |                            |
| Invoice Type         |                         |  Link         |  Invoice Type       |                            | 
| Buyer Province       |                         |  Link         |  Buyer Province     |                            | 


---
### ⚙️ Settings For Import Data:

| Setting      | Details                          |  Tool   |    Check      |
|--------------|----------------------------------|---------|---------------|
| Form Setting | Allow Import (via Import Tool)   |         |   ✅ Enabled |
| Permissions  | System Manager                   | Import  |   ✅ Enabled |

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
