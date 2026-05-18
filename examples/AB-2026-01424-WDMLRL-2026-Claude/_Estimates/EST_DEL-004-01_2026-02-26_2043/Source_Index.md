# Source Index — EST_DEL-004-01_2026-02-26_2043

## Price Sources Indexed

| Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|
| Professional_Staff_Rates.csv | Rate Table (parametric) | 25 roles with hourly rates in CAD; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes | Unit rates for all labour line items. R-01 ($165/hr), R-08 ($135/hr), R-13 ($95/hr), R-16 ($165/hr) used for DEL-004-01. |
| Level_of_Effort.csv | Parametric (hours by deliverable) | Rows keyed by Execution + DeliverableID + RoleID; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes | Hour quantities for DEL-004-01: R-01=6h, R-08=4h, R-13=18h, R-16=42h. Total=70h. |
| Assumed_Project_Parameters.csv | Parametric (project parameters) | 18 parameter rows; covers project identity, location, contract form, schedule, facility dimensions, equipment, currency | Provides project context (building area ~13,000 sqft, 35' ceiling, 2 cranes, CAD currency). Not directly priced. |
| Professional_Design_Fees.csv | Parametric (fee percentage model) | 5 discipline rows with fee % ranges against construction_value | DF-04 (Electrical: 1.0%–2.2%, recommended 1.6%) available as cross-check. Not used as primary pricing method for this run; LOE-based pricing used instead. |

## Document Sources Read

| Document | Path | Role in Estimate |
|---|---|---|
| _CONTEXT.md | PKG-004_Electrical Design/1_Working/DEL-004-01_Preliminary-Design/_CONTEXT.md | Deliverable identification: DEL-004-01, PKG-004, Electrical Engineering, Design Presentation |
| Datasheet.md | PKG-004_Electrical Design/1_Working/DEL-004-01_Preliminary-Design/Datasheet.md | Quantity takeoff: attributes, lighting counts, receptacle types, equipment circuits, low-voltage systems |
| Specification.md | PKG-004_Electrical Design/1_Working/DEL-004-01_Preliminary-Design/Specification.md | Requirements R-001 through R-019; verification criteria; scope boundaries |
| Guidance.md | PKG-004_Electrical Design/1_Working/DEL-004-01_Preliminary-Design/Guidance.md | Design principles, trade-offs, conflict table (CF-004-001, CF-004-002), considerations |
| Procedure.md | PKG-004_Electrical Design/1_Working/DEL-004-01_Preliminary-Design/Procedure.md | Work steps (7 steps), prerequisites, verification checks, records |
| WDMLRL_Decomposition_Claude.md | _Decomposition/WDMLRL_Decomposition_Claude.md | WBS traceability: PKG-004, DEL-004-01, SOW-0010d, OBJ-003/OBJ-005 |
