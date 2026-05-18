# Source Index — EST_DEL-008-04_2026-02-27_0700

## Price Sources

| # | Source File | Source Type | Parsing Notes | Supports | Gaps |
|---|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | Rate Table (PARAMETRIC) | 25 roles; CSV with RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes columns | Hourly rates for all professional staff roles including R-21 Surveyor ($140/hr), R-01 PM ($165/hr), R-08 Cost Estimator ($135/hr) | No field technician / survey assistant rates; no equipment rates; no per-diem/travel rates; no CAD drafting technician rate |
| 2 | Level_of_Effort.csv | Level of Effort (PARAMETRIC) | Multi-deliverable CSV with Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes columns | PM (6 hr) and Cost Estimator (4 hr) hours for DEL-008-04 | Surveyor (R-21) hours for DEL-008-04 not provided -- Notes show "PKG-008 TBD -- TBD". Only 2 of expected 3+ roles have LOE data |
| 3 | Assumed_Project_Parameters.csv | Parametric Parameters | 19 parameters; CSV with ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes | Site location, building footprint (~13,000 sqft), building height (35 ft), crane count/capacity, cistern volume (50,000 L), septic tank (2,000 US gal), currency (CAD) | No as-built survey-specific parameters (e.g., expected deliverable format, number of drawing sheets, feature count) |

## Document Sources (Read-Only -- Not Price Sources)

| Document | Path | Content Used |
|---|---|---|
| Datasheet.md | DEL-008-04_As-Built-Survey/Datasheet.md | Survey type; scope; datum (TBD); accuracy class (TBD); components to be documented; building footprint; construction elements; conditions and prerequisites |
| Specification.md | DEL-008-04_As-Built-Survey/Specification.md | 8 requirements (REQ-001 through REQ-008); verification approaches; standards; documentation artifacts; exclusions |
| Guidance.md | DEL-008-04_As-Built-Survey/Guidance.md | 5 principles; considerations (timeline/access/underground infrastructure/accuracy gap); trade-offs (survey timing/underground docs/deliverable format); 9 gaps (GAP-001 through GAP-009) |
| Procedure.md | DEL-008-04_As-Built-Survey/Procedure.md | 6 steps with sub-steps; 8 prerequisites; verification checks; records table |
| _CONTEXT.md | DEL-008-04_As-Built-Survey/_CONTEXT.md | Deliverable identity; responsible role (Surveyor); SOW reference (SOW-0004); objectives (OBJ-001, OBJ-002); scope elements |
| WDMLRL_Decomposition_Claude.md | _Decomposition/WDMLRL_Decomposition_Claude.md | PKG-008 package definition; DEL-008-04 deliverable entry; SOW-0004; scope ledger |
