# Source_Index.md

## Pricing Sources Indexed

### Source 1: Professional_Staff_Rates.csv

| Field | Value |
|-------|-------|
| **Path** | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` |
| **Type** | PARAMETRIC (rate table) |
| **Content** | 25 professional roles with hourly rates in CAD |
| **Basis** | PARAMETRIC; Confidence: MEDIUM for all roles |
| **Roles used in this estimate** | R-01 (Project Manager, $165/hr), R-08 (Cost Estimator, $135/hr), R-09 (Document Controller, $75/hr), R-11 (Senior Architect, $180/hr), R-14 (Structural Engineer, $170/hr), R-15 (Mechanical Engineer, $165/hr), R-16 (Electrical Engineer, $165/hr), R-17 (Civil Engineer, $160/hr), R-18 (Plumbing Engineer, $160/hr), R-22 (Permitting Specialist, $125/hr) |
| **Parsing notes** | Standard CSV; header row + 25 data rows; all rates in CAD |

### Source 2: Level_of_Effort.csv

| Field | Value |
|-------|-------|
| **Path** | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` |
| **Type** | PARAMETRIC (effort allocation) |
| **Content** | Estimated hours by deliverable and role across all project deliverables |
| **Basis** | PARAMETRIC; all entries |
| **DEL-009-02 entries** | 2 rows: R-01 Project Manager (6 hrs), R-08 Cost Estimator (4 hrs) |
| **Parsing notes** | Standard CSV; large file covering all deliverables. DEL-009-02 has minimal coverage (2 roles only). Note: "PKG-009 Project Manager -- TBD" in Notes column indicates the LOE for this deliverable is preliminary/incomplete. |
| **Limitations** | Does not include Permitting Specialist (R-22), Document Controller (R-09), or design discipline review hours for DEL-009-02. These were estimated parametrically from Procedure.md scope. |

### Source 3: Assumed_Project_Parameters.csv

| Field | Value |
|-------|-------|
| **Path** | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` |
| **Type** | PARAMETRIC (project context) |
| **Content** | 18 project parameters including facility identity, location, contract form, schedule, facility attributes, and currency |
| **Basis** | Mix of CONFIRMED, DERIVED, DESIGN_BASIS, and ASSUMPTION |
| **Parameters used in this estimate** | PP-17 (Currency: CAD), PP-10 (Floor area: ~13,000 sqft — used for permit scope sizing), PP-07 (Completion deadline: 2026-12-31 — schedule context) |
| **Parsing notes** | Standard CSV; 18 rows |

---

## Source Coverage Assessment

| Coverage Aspect | Status |
|----------------|--------|
| Hourly rates for all roles used | COMPLETE — all 10 roles have rates in Professional_Staff_Rates.csv |
| LOE from Level_of_Effort.csv | PARTIAL — only 2 of 10 roles covered; remaining 8 roles estimated parametrically |
| Project parameters for scope sizing | ADEQUATE — facility size and schedule available |
| Permit fee amount | NOT APPLICABLE — County responsibility, excluded from Proponent estimate |
