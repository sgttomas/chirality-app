# Source Index — EST_DEL-003-01_2026-03-26_1400

## Pricing Sources Indexed

| # | Source File | PS-ID | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|---|
| 1 | `PriceSources/Professional_Staff_Rates.csv` | PS-STAFF | Rate Table | 25 roles (R-01 through R-25); hourly rates in CAD; Confidence = MEDIUM for all roles. CSV is well-formed with headers: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. | Provides unit rates ($/hr) for all professional staff roles. Directly applicable to DEL-003-01 labour pricing. Primary pricing source for this run. |
| 2 | `PriceSources/Level_of_Effort.csv` | PS-LOE | LOE Model | Multi-deliverable LOE table; rows filtered for DEL-003-01 yield 4 role assignments (R-01, R-08, R-13, R-15). CSV headers: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. | Provides estimated hours per role for DEL-003-01. Combined with PS-STAFF rates to produce labour cost estimates. |
| 3 | `PriceSources/Assumed_Project_Parameters.csv` | PS-PARAMS | Parametric Parameters | 18 parameter rows; provides project identity, location, facility dimensions, equipment counts, and economic assumptions. | Context parameters for validation. Key parameters: PP-10 (13,000 sqft), PP-11 (35 ft ceiling), PP-12 (2 cranes), PP-17 (CAD currency). Does not directly price items. |
| 4 | `PriceSources/Professional_Design_Fees.csv` | PS-DF | Fee Model | 5 discipline fee rows (DF-01 through DF-05); percentage-of-construction-value basis. | Alternative pricing method for mechanical design fee (DF-03: 1.0%-2.2%, recommended 1.6% of construction_value). Not used because construction_value is not yet established. Retained as cross-check reference. |
| 5 | `PriceSources/Mechanical_System_Rates.csv` | PS-MS | Rate Table (Allowance) | 8 mechanical system items (MS-01 through MS-08). Equipment and installation allowances. | Not applicable to DEL-003-01 (design services deliverable, not construction). Available for DEL-003-05 and PKG-013 estimates. |
| 6 | `PriceSources/CBS_Taxonomy.csv` | PS-CBS | CBS Reference | 29 CBS L2 categories. | Used for CBS code assignment. CBS-01 and CBS-02 applicable to this deliverable. |

## Source Coverage Assessment

| Item Category | Primary Source | Gap |
|---|---|---|
| Labour hours (LOE) | PS-LOE (Level_of_Effort.csv) | None -- 4 roles fully specified for DEL-003-01 |
| Labour rates ($/hr) | PS-STAFF (Professional_Staff_Rates.csv) | None -- all 4 required roles (R-01, R-08, R-13, R-15) present with rates |
| Project parameters | PS-PARAMS (Assumed_Project_Parameters.csv) | None for context validation |
| Fee-based cross-check | PS-DF (Professional_Design_Fees.csv) | Construction value not available; fee cross-check cannot be completed |
| Material / equipment costs | None | Not applicable -- DEL-003-01 is a design services deliverable (no materials) |
| Subcontractor quotes | None | Not applicable -- design performed by in-house team per LOE model |
