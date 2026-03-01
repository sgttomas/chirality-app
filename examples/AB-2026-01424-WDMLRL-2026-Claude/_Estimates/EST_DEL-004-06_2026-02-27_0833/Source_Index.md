# Source Index — EST_DEL-004-06_2026-02-27_0833

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-1 | Professional_Staff_Rates.csv | PARAMETRIC (rate table) | 25 roles with RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence. All rates are PARAMETRIC / MEDIUM confidence. | Hourly rates for all professional staff roles used in LOE-based pricing. Directly supports DL-001 through DL-004. |
| PS-2 | Level_of_Effort.csv | PARAMETRIC (effort model) | Multi-deliverable LOE table. Columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. DEL-004-06 has 4 rows (R-01, R-08, R-13, R-16). All PARAMETRIC basis. | Estimated hours per role per deliverable. Directly drives quantity (hours) for ITEM-001 through ITEM-004. |
| PS-3 | Assumed_Project_Parameters.csv | PARAMETRIC (project parameters) | 19 rows of project context parameters (identity, location, contract, schedule, facility, equipment, plumbing, mechanical, currency, economics). | Context parameters. Not directly used for line-item pricing but confirms project scope, building area (~13,000 sqft), equipment counts (2 cranes, 5-ton), and currency (CAD). |
| PS-4 | Professional_Design_Fees.csv | PARAMETRIC (fee-based) | 5 discipline rows with fee percentage ranges (min/max/recommended) applied to construction_value. | Alternative fee-based pricing method (DF-04 Electrical: 1.0%–2.2%, recommended 1.6% of construction value). Not used for this run because LOE-based pricing is available and more granular. Could be used as a cross-check. |

## Document Sources (Engineering Content)

| # | Document | Path | Used For |
|---|---|---|---|
| DS-1 | _CONTEXT.md | PKG-004_Electrical Design/1_Working/DEL-004-06_Panel-Schedules/_CONTEXT.md | Deliverable ID, name, package, discipline, type |
| DS-2 | Datasheet.md | PKG-004_Electrical Design/1_Working/DEL-004-06_Panel-Schedules/Datasheet.md | Known loads to be scheduled; building attributes; conditions |
| DS-3 | Specification.md | PKG-004_Electrical Design/1_Working/DEL-004-06_Panel-Schedules/Specification.md | Requirements (REQ-004-06-01 through REQ-004-06-13); verification criteria; standards |
| DS-4 | Guidance.md | PKG-004_Electrical Design/1_Working/DEL-004-06_Panel-Schedules/Guidance.md | Design principles; considerations; trade-offs; conflict table |
| DS-5 | Procedure.md | PKG-004_Electrical Design/1_Working/DEL-004-06_Panel-Schedules/Procedure.md | Work steps (Phase 1 preliminary, Phase 2 IFC); prerequisites; verification; records |

## Decomposition Source

| # | Document | Path | Used For |
|---|---|---|---|
| DC-1 | WDMLRL_Decomposition_Claude.md | _Decomposition/WDMLRL_Decomposition_Claude.md | WBS traceability: PKG-004 Electrical Design; DEL-004-06 Panel Schedules; SOW-0014; OBJ-003, OBJ-005 |
