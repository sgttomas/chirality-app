# Source_Index.md

## Pricing Sources Indexed

### Source 1 — Professional_Staff_Rates.csv (PS-STAFF)

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv |
| **Type** | Rate table (parametric) |
| **Content** | 25 professional staff roles with hourly rates in CAD, basis PARAMETRIC, confidence MEDIUM |
| **Supports** | Unit rate pricing for all professional labor line items |
| **Limitations** | Rates are parametric estimates, not confirmed quotes; no escalation factors included |
| **Roles used for DEL-009-04** | R-01 Project Manager ($165/h), R-06 QA/QC Lead ($135/h), R-08 Cost Estimator ($135/h), R-09 Document Controller ($75/h), R-22 Permitting Specialist ($125/h) |

### Source 2 — Level_of_Effort.csv (PS-LOE)

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv |
| **Type** | Parametric level-of-effort model |
| **Content** | Estimated hours per role per deliverable across the full project |
| **Supports** | Quantity (hours) for labor line items |
| **Limitations** | DEL-009-04 has 5 rows totalling 58 hours across 5 roles. Allocation to individual procedure steps requires professional judgment. |
| **Rows used** | Row 255: R-01 6h; Row 256: R-08 4h; Row 580: R-06 16h; Row 581: R-09 12h; Row 582: R-22 20h |

### Source 3 — Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv |
| **Type** | Parametric project parameters |
| **Content** | 18 project parameters including identity, location, schedule, facility, equipment, and currency |
| **Supports** | Context validation (currency = CAD, completion deadline Dec 31 2026, project identity) |
| **Limitations** | Does not contain pricing data; used for context and assumption validation only |

## Source Coverage Assessment

- **PARAMETRIC items (DL-001 through DL-014, DL-018 through DL-020):** Fully supported by LOE hours + rate table sources. 17 lines priced via hours x rate.
- **ALLOWANCE items (DL-015, DL-016, DL-017):** No parametric source available. These are fixed allowances based on professional judgment for operationally contingent activities (deficiency tracking, regulatory change, guarantee maintenance). Amounts are not derived from the LOE or rate table sources.
