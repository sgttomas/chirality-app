# Source Index — EST_DEL-02-01_2026-02-18_1400

## Indexed Price Sources

### PS-01: Professional_Staff_Rates.csv
- **Path:** `_PriceSources/Professional_Staff_Rates.csv`
- **Type:** Rate table (hourly rates)
- **Format:** CSV; 30 roles with RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes
- **Roles used for DEL-02-01:** R-02, R-04, R-05, R-06, R-07, R-08, R-09, R-10, R-11, R-12, R-13, R-14 (12 of 30 roles)
- **Basis:** MARKET rates; Confidence: MEDIUM across all used roles
- **Parsing notes:** Clean CSV; no parsing issues
- **Supports:** UnitRate ($/hr) for all 12 line items in Detail.csv

### PS-02: Level_of_Effort.csv
- **Path:** `_PriceSources/Level_of_Effort.csv`
- **Type:** Rate table (hours per deliverable per role)
- **Format:** CSV; 65 rows total; 12 rows for DEL-02-01 (Execution=6c)
- **Basis:** PARAMETRIC effort estimates based on comparable proposal efforts
- **Parsing notes:** Clean CSV; filtered on Execution=6c and DeliverableID=DEL-02-01
- **Supports:** Qty (hours) for all 12 line items in Detail.csv

### PS-03: Assumed_Project_Parameters.csv
- **Path:** `_PriceSources/Assumed_Project_Parameters.csv`
- **Type:** Parameters / context
- **Format:** CSV; 29 parameters
- **Parsing notes:** Clean CSV; used for context validation only
- **Supports:** Contextual validation — PP-05 (18,000 sf main building), PP-07 (6,000 sf cold storage), PP-09 (12 acres total site), PP-10 (4.5 acres developed) inform scope calibration for civil/site effort hours
- **Cannot support:** Direct pricing (no unit rates or quantities for DEL-02-01 line items)

---

## Source Coverage Summary

| Line Item | Qty Source | Rate Source | Coverage |
|---|---|---|---|
| L-001 through L-012 | Level_of_Effort.csv | Professional_Staff_Rates.csv | 100% |

All 12 line items have complete provenance from two rate table sources.

---

## Sources NOT Used

The following price source files from the _PriceSources directory are NOT relevant to DEL-02-01 (they support construction pricing for PKG-02 deliverables):
- Structural_Concrete_Rates.csv
- Building_Envelope_Rates.csv
- Interior_Architectural_Rates.csv
- Mechanical_System_Rates.csv
- Electrical_System_Rates.csv
- Earthwork_Civil_Rates.csv
- Paving_Surfacing_Rates.csv
- Underground_Utility_Rates.csv
- Equipment_Pricing.csv
- Optional_Items_Pricing.csv
- Parametric_Building_Rates.csv
- Construction_Labour_Rates.csv
- Professional_Design_Fees.csv
- Fees_Permits_Insurance.csv
