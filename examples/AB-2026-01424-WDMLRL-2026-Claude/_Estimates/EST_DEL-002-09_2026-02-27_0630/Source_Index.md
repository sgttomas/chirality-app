# Source Index — EST_DEL-002-09_2026-02-27_0630

## Indexed Price Sources

### Source 1 — Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| **Path** | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` |
| **Type** | Rate Table (PARAMETRIC) |
| **Content** | 25 professional roles (R-01 through R-25) with hourly rates in CAD |
| **Basis** | PARAMETRIC; Confidence = MEDIUM for all entries |
| **Coverage** | Covers all four roles used for DEL-002-09: R-01 Project Manager ($165/hr), R-08 Cost Estimator ($135/hr), R-13 BIM Technician ($95/hr), R-14 Structural Engineer ($170/hr) |
| **Parsing Notes** | Clean CSV; 7 columns; no parsing issues |

### Source 2 — Level_of_Effort.csv

| Field | Value |
|---|---|
| **Path** | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` |
| **Type** | Parametric model (Level of Effort hours by deliverable and role) |
| **Content** | Estimated hours for each deliverable-role combination across the full project |
| **Basis** | PARAMETRIC; all entries for DEL-002-09 |
| **Coverage** | Provides hours for DEL-002-09: R-01 (6 hr), R-08 (4 hr), R-13 (36 hr), R-14 (84 hr) |
| **Parsing Notes** | Large CSV (400+ rows); filtered to DEL-002-09 rows; 8 columns; no parsing issues |

### Source 3 — Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| **Path** | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` |
| **Type** | Parametric context (project parameters supporting estimate assumptions) |
| **Content** | 19 parameters (PP-01 through PP-19) covering identity, location, contract, schedule, facility, equipment, plumbing, mechanical, currency, economics |
| **Basis** | Mixed (CONFIRMED, DERIVED, DESIGN_BASIS, ASSUMPTION) |
| **Coverage** | Provides project context (currency = CAD, facility area ~13,000 sqft, 35 ft ceiling, concrete structure). Does not directly price line items but supports parametric assumptions. |
| **Parsing Notes** | Clean CSV; 8 columns; no parsing issues |

### Source 4 — Professional_Design_Fees.csv

| Field | Value |
|---|---|
| **Path** | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` |
| **Type** | Parametric model (percentage-based design fee benchmarks) |
| **Content** | 5 discipline fee ranges (DF-01 through DF-05) as percentage of construction value |
| **Basis** | PARAMETRIC; Confidence = MEDIUM |
| **Coverage** | DF-02 (Structural design fee: 1.2%–2.5%, recommended 1.8% of construction value) is relevant as a cross-check benchmark. Not used for primary pricing because LOE-based parametric method provides greater granularity for a single-deliverable estimate. |
| **Parsing Notes** | Clean CSV; 10 columns; no parsing issues |

## Source-to-Item Mapping Summary

| Item Range | Primary Source | Secondary Source |
|---|---|---|
| ITM-001 (PM hours) | Level_of_Effort.csv (DEL-002-09, R-01) | Professional_Staff_Rates.csv (R-01) |
| ITM-002 (Estimator hours) | Level_of_Effort.csv (DEL-002-09, R-08) | Professional_Staff_Rates.csv (R-08) |
| ITM-003 (BIM Tech hours) | Level_of_Effort.csv (DEL-002-09, R-13) | Professional_Staff_Rates.csv (R-13) |
| ITM-004 (Structural Eng hours) | Level_of_Effort.csv (DEL-002-09, R-14) | Professional_Staff_Rates.csv (R-14) |
| ITM-005 through ITM-016 | Included in ITM-001 through ITM-004 | Activity breakdowns from Procedure.md (scope composition only; no separate pricing) |
