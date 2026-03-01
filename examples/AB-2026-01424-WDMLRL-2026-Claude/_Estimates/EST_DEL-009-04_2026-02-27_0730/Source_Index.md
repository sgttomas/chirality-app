# Source_Index.md

## Pricing Sources Indexed

### Source 1 — Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv |
| **Type** | Rate table (parametric) |
| **Content** | 25 professional staff roles with hourly rates in CAD, basis PARAMETRIC, confidence MEDIUM |
| **Supports** | Unit rate pricing for all professional labor line items |
| **Limitations** | Rates are parametric estimates, not confirmed quotes; no escalation factors included |
| **Roles used for DEL-009-04** | R-01 Project Manager ($165/h), R-08 Cost Estimator ($135/h) |

### Source 2 — Level_of_Effort.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv |
| **Type** | Parametric level-of-effort model |
| **Content** | Estimated hours per role per deliverable across the full project |
| **Supports** | Quantity (hours) for labor line items |
| **Limitations** | DEL-009-04 has only 2 rows (R-01 6h, R-08 4h = 10h total). This covers register setup/management only. Ongoing construction-phase and guarantee-period operational effort is NOT included. |
| **Rows used** | Row 255: DEL-009-04, R-01, 6h; Row 256: DEL-009-04, R-08, 4h |

### Source 3 — Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv |
| **Type** | Parametric project parameters |
| **Content** | 18 project parameters including identity, location, schedule, facility, equipment, and currency |
| **Supports** | Context validation (currency = CAD, completion deadline Dec 31 2026, project identity) |
| **Limitations** | Does not contain pricing data; used for context and assumption validation only |

## Source Coverage Assessment

- **Priced items (DL-001 through DL-008, DL-019, DL-020):** Fully supported by LOE + rate table sources.
- **TBD items (DL-009 through DL-018):** No pricing source available. These represent construction-phase and guarantee-period operational effort that depends on permit condition counts, inspection counts, and construction duration — none of which are known at this stage.
