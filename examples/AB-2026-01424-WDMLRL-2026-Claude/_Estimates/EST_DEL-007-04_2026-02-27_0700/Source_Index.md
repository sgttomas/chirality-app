# Source Index — EST_DEL-007-04_2026-02-27_0700

## Indexed Pricing Sources

### Source 1 — Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| Path | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv |
| Source Type | PARAMETRIC (rate table) |
| Content | 25 professional staff roles with hourly rates in CAD; each tagged PARAMETRIC basis with MEDIUM confidence |
| Parsing Notes | Standard CSV; headers: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes |
| Supports | Unit rate pricing for all labour line items (ITEM-001 through ITEM-003) |
| Limitations | Rates are parametric estimates, not firm quotes; MEDIUM confidence throughout |

### Source 2 — Level_of_Effort.csv

| Field | Value |
|---|---|
| Path | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv |
| Source Type | PARAMETRIC (effort model) |
| Content | Estimated hours by role for each deliverable across all packages in the project; DEL-007-04 has 3 rows (R-01, R-08, R-19) totalling 80 hours |
| Parsing Notes | Standard CSV; headers: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes |
| Supports | Quantity (hours) for labour line items ITEM-001, ITEM-002, ITEM-003 |
| Limitations | Effort is parametric estimate; PARAMETRIC basis; no firm schedule or timesheet basis |

### Source 3 — Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| Path | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv |
| Source Type | PARAMETRIC (project parameters) |
| Content | 18 project-level parameters including identity, location, contract, schedule, facility, equipment, and currency assumptions |
| Parsing Notes | Standard CSV; headers: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes |
| Supports | Context and traceability for project-level assumptions (currency CAD, base year 2026, project identity) |
| Limitations | Does not directly price any line items; contextual/traceability source only |

### Source 4 — Professional_Design_Fees.csv

| Field | Value |
|---|---|
| Path | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv |
| Source Type | PARAMETRIC (fee percentage model) |
| Content | 5 discipline fee percentages (Architecture, Structural, Mechanical, Electrical, Civil) as percentage of construction value |
| Parsing Notes | Standard CSV; headers: ItemID, Discipline, Description, FeePercentMin, FeePercentMax, RecommendedPercent, FeeBase, Basis, Confidence, Notes |
| Supports | Alternative fee-based pricing approach; not used for this run since Level_of_Effort provides direct hour-based pricing |
| Limitations | No landscape-specific fee percentage row exists; this source does not support DEL-007-04 pricing directly. Landscape Architectural design fees would require extrapolation not supported by the data. |
