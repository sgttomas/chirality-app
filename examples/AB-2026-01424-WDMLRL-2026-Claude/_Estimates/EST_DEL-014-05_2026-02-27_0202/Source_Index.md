# Source_Index — EST_DEL-014-05_2026-02-27_0202

## Price Sources Indexed

| Source File | Source Type | Parsing Notes | Supports | Does Not Support |
|---|---|---|---|---|
| Professional_Staff_Rates.csv | PARAMETRIC (rate table) | 25 roles with hourly rates in CAD. Basis = PARAMETRIC, Confidence = MEDIUM. | Staff oversight costs for PM (R-01), CPM (R-02), Site Supt (R-03), Cost Est (R-08), QA/QC (R-06), HSE (R-05) | No plumbing trade labour; no equipment/material pricing |
| Level_of_Effort.csv | PARAMETRIC (effort matrix) | 577 rows total; 6 rows for DEL-014-05 (R-01: 6h, R-02: 8h, R-03: 10h, R-08: 4h, R-06: 6h, R-05: 4h). Basis = PARAMETRIC. | Staff hours allocation for DEL-014-05 professional oversight | No trade labour hours; no material quantities |
| Assumed_Project_Parameters.csv | PARAMETRIC (parameters) | 18 rows of project-level parameters. Relevant: PP-17 Currency=CAD, PP-18 Base Year=2026. | Project context, currency confirmation | No direct pricing for emergency shower components |
| Underground_Utility_Rates.csv | PARAMETRIC / ALLOWANCE | 5 rows. UU-01 water line $130/m; UU-02 sanitary $160/m. | General reference for water line pricing (not directly applicable — interior branch piping, not underground) | No emergency shower equipment pricing; no interior piping rates |
| Construction_Labour_Rates.csv | PARAMETRIC (rate table) | 10 trades. T-05 Plumber: $92.80/hr fully burdened (base $58 x 1.6 burden). Basis = PARAMETRIC, Confidence = MEDIUM. | Plumber labour rate for installation, commissioning, inspections | No material pricing |
| Equipment_Pricing.csv | ALLOWANCE | 3 rows (cranes, pressure washer, compressor). No emergency shower or plumbing fixture items. | Not applicable to this deliverable | No emergency shower unit pricing; no TMV pricing; no signage pricing |

## Coverage Assessment

- **Well covered:** Professional staff overhead hours and rates (PARAMETRIC, MEDIUM confidence)
- **Well covered:** Plumber trade labour rate (PARAMETRIC, MEDIUM confidence)
- **Not covered — PARAMETRIC fallback applied:** Emergency shower unit material cost, thermostatic mixing valve material cost, supply branch piping material cost, signage material cost, permit fees
- **Note:** FALLBACK_POLICY = ALLOW_PARAMETRIC permits parametric estimation for items without direct pricing evidence in PRICE_SOURCES
