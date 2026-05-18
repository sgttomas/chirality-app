# Source Index — EST_DEL-008-03_2026-02-27_0630

## Price Sources

| # | Source File | Source Type | Parsing Notes | Supports | Gaps |
|---|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | Rate Table (PARAMETRIC) | 25 roles; CSV with RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes columns | Hourly rates for all professional staff roles including R-21 Surveyor ($140/hr), R-01 PM ($165/hr), R-08 Cost Estimator ($135/hr) | No field technician / survey assistant rates; no equipment rates; no per-diem/travel rates |
| 2 | Level_of_Effort.csv | Level of Effort (PARAMETRIC) | Multi-deliverable CSV with Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes columns | PM (6 hr) and Cost Estimator (4 hr) hours for DEL-008-03 | Surveyor (R-21) hours for DEL-008-03 not provided — Notes show "PKG-008 TBD — TBD". Only 2 of expected 3+ roles have LOE data |
| 3 | Assumed_Project_Parameters.csv | Parametric Parameters | 19 parameters; CSV with ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes | Site location, building footprint (~13,000 sqft), building height (35 ft), crane count/capacity, cistern volume (50,000 L), septic tank (2,000 US gal), currency (CAD) | No construction survey-specific parameters (e.g., site area for survey, number of staking visits, control point count) |

## Document Sources (Read-Only — Not Price Sources)

| Document | Path | Content Used |
|---|---|---|
| Datasheet.md | DEL-008-03_Construction-Survey/Datasheet.md | Survey scope elements; site information; upstream inputs; downstream users; building elements requiring survey |
| Specification.md | DEL-008-03_Construction-Survey/Specification.md | 13 requirements (REQ-008-03-01 through REQ-008-03-10); element layout table; verification approaches |
| Guidance.md | DEL-008-03_Construction-Survey/Guidance.md | Principles; trade-offs; site conditions; building complexity; quality acceptance framework |
| Procedure.md | DEL-008-03_Construction-Survey/Procedure.md | 4 phases (A-D); 17 steps; prerequisites; verification checklist; records table |
| _CONTEXT.md | DEL-008-03_Construction-Survey/_CONTEXT.md | Deliverable identity; responsible role; SOW reference; objectives; scope elements |
| WDMLRL_Decomposition_Claude.md | _Decomposition/WDMLRL_Decomposition_Claude.md | PKG-008 package definition; DEL-008-03 deliverable entry; SOW-0003; scope ledger |
