# Source Index — EST_DEL-004-03_2026-02-27_0834

## Price Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | Professional_Staff_Rates.csv | Rate Table (hourly) | 25 roles; CSV with columns RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes | Hourly rates for all professional staff roles; PARAMETRIC basis; MEDIUM confidence |
| PS-02 | Level_of_Effort.csv | Parametric (hours allocation) | Multi-deliverable CSV; columns Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes | Estimated hours per role per deliverable; 4 rows matched to DEL-004-03 |
| PS-03 | Assumed_Project_Parameters.csv | Parametric (project context) | 19 parameters; columns ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes | Project-level parameters: building area (~13,000 sqft), ceiling height (35 ft), cranes (2), currency (CAD), etc. |
| PS-04 | Professional_Design_Fees.csv | Parametric (fee percentages) | 5 disciplines; columns ItemID, Discipline, Description, FeePercentMin/Max, RecommendedPercent, FeeBase, Basis, Confidence, Notes | Alternative fee-based pricing for electrical design (DF-04: 1.0%-2.2%, recommended 1.6% of construction value); NOT used as primary method — LOE-based pricing preferred for this deliverable |

## Document Sources (Quantity Takeoff)

| # | Document | Path | Used For |
|---|---|---|---|
| DS-01 | _CONTEXT.md | DEL-004-03_Power-Plans/_CONTEXT.md | Deliverable identification: ID, name, package, discipline, type |
| DS-02 | Datasheet.md | DEL-004-03_Power-Plans/Datasheet.md | Load inventory: 2 cranes, overhead doors, 40A compressor, 70A fire hose pump, 70A pressure washer, welding receptacles, mixed-grade receptacles, exhaust fans, ceiling fans, lighting loads, mechanical equipment |
| DS-03 | Specification.md | DEL-004-03_Power-Plans/Specification.md | 18 requirements (REQ-003-01 through REQ-003-18); verification criteria; code compliance |
| DS-04 | Guidance.md | DEL-004-03_Power-Plans/Guidance.md | Design principles, trade-offs, drawing organization, MEP coordination, code interpretation notes, risks |
| DS-05 | Procedure.md | DEL-004-03_Power-Plans/Procedure.md | 7-step workflow (plus sub-steps 1A, 2B); personnel prerequisites; verification checks; records |

## Decomposition Source

| # | Document | Path | Used For |
|---|---|---|---|
| DC-01 | WDMLRL_Decomposition_Claude.md | _Decomposition/WDMLRL_Decomposition_Claude.md | WBS traceability: PKG-004 Electrical Design; DEL-004-03 Power Distribution Plans; SOW-0014; OBJ-001, OBJ-003, OBJ-005 |
