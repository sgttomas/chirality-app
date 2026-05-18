# Source Index — EST_DEL-006-07_2026-02-27_0700

## Indexed Price Sources

### Source 1 — Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| Path | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` |
| Source Type | PARAMETRIC (rate table) |
| Format | CSV — 25 roles with RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes |
| Parsing Notes | Clean CSV; all rates in CAD; Basis = PARAMETRIC for all rows; Confidence = MEDIUM |
| Supports | Hourly rates for all professional staff roles (PM, engineers, BIM, admin, specialty) |
| Does Not Support | Hours/quantities (requires Level_of_Effort.csv for hour allocations) |
| Roles Used for DEL-006-07 | R-01 (Project Manager, $165/hr), R-08 (Cost Estimator, $135/hr), R-13 (BIM Technician, $95/hr), R-18 (Plumbing Engineer, $160/hr) |

### Source 2 — Level_of_Effort.csv

| Field | Value |
|---|---|
| Path | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` |
| Source Type | PARAMETRIC (effort model) |
| Format | CSV — rows per Execution/DeliverableID/RoleID combination; columns include EstimatedHours, Basis, Notes |
| Parsing Notes | Clean CSV; filtered for DEL-006-07: 4 rows (R-01: 6 hr, R-08: 4 hr, R-13: 21 hr, R-18: 49 hr) |
| Supports | Hour allocations by role for each deliverable; basis = PARAMETRIC |
| Does Not Support | Rates (requires Professional_Staff_Rates.csv for unit rates) |

### Source 3 — Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| Path | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` |
| Source Type | PARAMETRIC (project parameters) |
| Format | CSV — 18 parameters (ParameterID PP-01 through PP-18) covering identity, location, contract, schedule, facility, equipment, plumbing, currency, economics |
| Parsing Notes | Clean CSV; provides context for plumbing-specific parameters (PP-14: cistern 50,000 L, PP-15: septic 2,000 US gal, PP-17: currency CAD) |
| Supports | Contextual parameters for scope validation and assumption grounding |
| Does Not Support | Direct pricing; no unit rates or cost figures |

### Source 4 — Professional_Design_Fees.csv

| Field | Value |
|---|---|
| Path | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` |
| Source Type | PARAMETRIC (fee percentage model) |
| Format | CSV — 5 discipline-level fee entries (DF-01 through DF-05); columns include FeePercentMin, FeePercentMax, RecommendedPercent, FeeBase |
| Parsing Notes | Clean CSV; fee-based model applies percentage to construction value |
| Supports | Alternative fee-based pricing for design disciplines (architecture, structural, mechanical, electrical, civil) |
| Does Not Support | No plumbing-specific design fee entry exists (DF-03 is Mechanical only). Not used for this estimate — Level_of_Effort approach provides more granular basis for DEL-006-07 |

## Source Coverage Summary

| Aspect | Coverage |
|---|---|
| Hourly rates for all 4 roles on DEL-006-07 | FULL — all rates sourced from Professional_Staff_Rates.csv |
| Hour allocations for DEL-006-07 | FULL — all hours sourced from Level_of_Effort.csv |
| Project parameters (plumbing context) | FULL — cistern, septic, currency confirmed |
| Design fee alternative | NOT USED — no plumbing design fee entry; LOE method preferred |
