# Source Index

## Pricing Sources

| # | Source File | Source Type | Content Summary | Coverage for DEL-02-02 |
|---|---|---|---|---|
| S-01 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | 30 roles with hourly rates in CAD, role categories, confidence levels | Provides unit rates for R-06, R-07, R-08 (the three roles assigned to DEL-02-02) |
| S-02 | `_PriceSources/Level_of_Effort.csv` | Level of Effort Table | 73 rows across all deliverables; 3 rows for DEL-02-02 specifying estimated hours by role | Provides quantities (hours) for all 3 line items |
| S-03 | `_PriceSources/Assumed_Project_Parameters.csv` | Project Parameters | 29 parameters covering duration, area, quantities, and financial assumptions | Context only; no direct pricing data used for DEL-02-02 line items; PP-09 (12-acre site) and PP-10 (4.5 ac developed) confirm scope scale |

## Dependency Sources

| # | Source File | Source Type | Content Summary | Usage |
|---|---|---|---|---|
| D-01 | `DEL-02-02_CivilSiteConceptPlan/Dependencies.csv` | Dependency Register | 20 dependency rows (v3.1 schema); 4 anchor, 11 upstream prerequisite/interface/constraint, 2 downstream handover | Blocker/readiness assessment only; not used for pricing evidence |

## Decomposition Source

| # | Source File | Source Type | Content Summary | Usage |
|---|---|---|---|---|
| X-01 | `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | Decomposition (v2.3 FINAL) | 10 packages, 38 deliverables, 32 scope items | Package/deliverable ID validation; scope item traceability; CBS mapping hints (none found for DEL-02-02) |

## Parsing Notes

- Rate table uses comma-separated format with header row; all rates in CAD; confidence uniformly MEDIUM.
- Level of effort table uses comma-separated format; filtered to rows where `DeliverableID = DEL-02-02` and `Execution = 6b`.
- All three DEL-02-02 rows in Level_of_Effort.csv have `Basis = PARAMETRIC` (the LoE estimation method). For the estimate snapshot, `Method = RATE_TABLE` because the pricing calculation uses rate table unit rates applied to LoE quantities.
