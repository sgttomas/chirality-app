# Source Index

## Pricing Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | Rate Table (Parametric) | 25 roles (R-01 through R-25); hourly rates in CAD; Confidence = MEDIUM for all roles. CSV is well-formed with headers: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. | Provides unit rates ($/hr) for all professional staff roles. Directly applicable to DEL-005-07 labour pricing. Key roles used: R-01 ($165), R-08 ($135), R-13 ($95), R-17 ($160). |
| PS-02 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | Parametric LOE Model | Multi-deliverable LOE table; rows filtered for DEL-005-07 yield 4 role assignments (R-01, R-08, R-13, R-17). CSV headers: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. | Provides estimated hours per role for DEL-005-07. Combined with PS-01 rates to produce labour cost estimates. Total: 70 hours across 4 roles. |
| PS-03 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` | Parametric Parameters | 19 parameter rows (PP-01 through PP-18); provides project identity, location, facility dimensions, equipment counts, and economic assumptions. CSV headers: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes. | Context parameters for parametric sizing. Key parameters used: PP-03 (site location near Ferintosh, Alberta), PP-10 (13,000 sqft building area), PP-17 (CAD currency). Site context informs civil specification scope (landfill site, Central Alberta climate). |
| PS-04 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` | Parametric Fee Model | 5 discipline fee rows (DF-01 through DF-05); percentage-of-construction-value basis. CSV headers: ItemID, Discipline, Description, FeePercentMin, FeePercentMax, RecommendedPercent, FeeBase, Basis, Confidence, Notes. | Alternative pricing method for civil design fee (DF-05: 0.6%--1.5%, recommended 1.0% of construction_value). Not used as primary method because construction value is not yet established; LOE method (PS-01 + PS-02) is preferred for this run. Retained as cross-check reference. |

## Source Coverage Assessment

| Item Category | Primary Source | Gap |
|---|---|---|
| Labour hours (LOE) | PS-02 (Level_of_Effort.csv) | None -- 4 roles fully specified for DEL-005-07 |
| Labour rates ($/hr) | PS-01 (Professional_Staff_Rates.csv) | None -- all 4 required roles (R-01, R-08, R-13, R-17) present with rates |
| Project parameters | PS-03 (Assumed_Project_Parameters.csv) | None for context validation |
| Fee-based cross-check | PS-04 (Professional_Design_Fees.csv) | Construction value not available; fee cross-check cannot be completed |
| Material / equipment costs | None | Not applicable -- DEL-005-07 is a design services deliverable (specification authoring); no materials |
| Subcontractor quotes | None | Not applicable -- civil specification authored by in-house civil engineering team per LOE model |
