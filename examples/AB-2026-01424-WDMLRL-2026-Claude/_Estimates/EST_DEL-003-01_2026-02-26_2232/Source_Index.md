# Source Index

## Pricing Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | Rate Table (Parametric) | 25 roles (R-01 through R-25); hourly rates in CAD; Confidence = MEDIUM for all roles. CSV is well-formed with headers: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. | Provides unit rates ($/hr) for all professional staff roles. Directly applicable to DEL-003-01 labour pricing. |
| PS-02 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | Parametric LOE Model | Multi-deliverable LOE table; rows filtered for DEL-003-01 yield 4 role assignments (R-01, R-08, R-13, R-15). CSV headers: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. | Provides estimated hours per role for DEL-003-01. Combined with PS-01 rates to produce labour cost estimates. |
| PS-03 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` | Parametric Parameters | 19 parameter rows (PP-01 through PP-18, noting PP-19 is absent); provides project identity, location, facility dimensions, equipment counts, and economic assumptions. CSV headers: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes. | Context parameters for parametric sizing. Key parameters used: PP-10 (13,000 sqft), PP-11 (35 ft ceiling), PP-12 (2 cranes), PP-17 (CAD currency). Does not directly price items but validates assumptions. |
| PS-04 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` | Parametric Fee Model | 5 discipline fee rows (DF-01 through DF-05); percentage-of-construction-value basis. CSV headers: ItemID, Discipline, Description, FeePercentMin, FeePercentMax, RecommendedPercent, FeeBase, Basis, Confidence, Notes. | Alternative pricing method for mechanical design fee (DF-03: 1.0%--2.2%, recommended 1.6% of construction_value). Not used as primary method because construction_value is not yet established; LOE method (PS-01 + PS-02) is preferred for this run. Retained as cross-check reference. |

## Source Coverage Assessment

| Item Category | Primary Source | Gap |
|---|---|---|
| Labour hours (LOE) | PS-02 (Level_of_Effort.csv) | None -- 4 roles fully specified for DEL-003-01 |
| Labour rates ($/hr) | PS-01 (Professional_Staff_Rates.csv) | None -- all 4 required roles (R-01, R-08, R-13, R-15) present with rates |
| Project parameters | PS-03 (Assumed_Project_Parameters.csv) | None for context validation |
| Fee-based cross-check | PS-04 (Professional_Design_Fees.csv) | Construction value not available; fee cross-check cannot be completed |
| Material / equipment costs | None | Not applicable -- DEL-003-01 is a design services deliverable (no materials) |
| Subcontractor quotes | None | Not applicable -- design performed by in-house team per LOE model |
