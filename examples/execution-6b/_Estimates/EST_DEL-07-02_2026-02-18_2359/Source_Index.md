# Source Index

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| S-01 | `test/execution-6b/_PriceSources/Professional_Staff_Rates.csv` | Rate Table | CSV; 30 roles; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes | Provides hourly rates (CAD) for all professional staff roles; Basis = MARKET; Confidence = MEDIUM for all roles except R-30 (N/A) |
| S-02 | `test/execution-6b/_PriceSources/Level_of_Effort.csv` | Level of Effort (Hours) | CSV; 73 rows; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes | Provides estimated hours by deliverable and role; filtered to Execution=6b; Basis = PARAMETRIC for all rows |
| S-03 | `test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv` | Project Parameters | CSV; 29 rows; columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes | Provides project-level parameters (durations, areas, quantities, financial estimates); used for context/validation only -- no direct pricing impact on DEL-07-02 |

## Dependency Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| D-01 | `test/execution-6b/PKG-007_.../DEL-07-02_.../Dependencies.csv` | Dependency Register | CSV; 10 dependency rows (v3.1 schema); covers anchors, upstream prerequisites, interfaces, downstream handovers | Identifies DEL-07-01 as prerequisite; DEL-07-04, DEL-07-05 as interfaces; CCDC 14-2013 as unresolved constraint; DEL-01-02 as downstream consumer |

## Decomposition Source

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| X-01 | `test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | Decomposition (v2.3 FINAL) | Markdown; 38 deliverables in 10 packages; FINAL ACCEPTED status | Provides stable IDs, scope mappings, and deliverable definitions for all WBS items |

## Source Coverage for DEL-07-02

| Item | Source Available | Notes |
|---|---|---|
| Hours (R-15, Construction Manager) | S-02 (row 55: 8 hrs) | Single role assignment; Basis = PARAMETRIC |
| Rate (R-15, Construction Manager) | S-01 (row 16: $155/hr CAD) | Basis = MARKET; Confidence = MEDIUM |
| Dependencies | D-01 | 10 rows; 1 unresolved constraint (CCDC 14-2013) |
| Deliverable definition | X-01 (Section 9, DEL-07-02) | Construction Administration Narrative; SOW-0020; OBJ-002 |
