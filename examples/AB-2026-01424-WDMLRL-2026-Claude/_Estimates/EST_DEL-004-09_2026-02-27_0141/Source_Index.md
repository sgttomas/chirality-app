# Source Index — EST_DEL-004-09_2026-02-27_0141

## Price Sources Indexed

| Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|
| Professional_Staff_Rates.csv | Rate Table (parametric) | 25 roles with hourly rates in CAD; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes | Unit rates for all labour line items. R-01 ($165/hr), R-08 ($135/hr), R-13 ($95/hr), R-16 ($165/hr) used for DEL-004-09. |
| Level_of_Effort.csv | Parametric (hours by deliverable) | Rows keyed by Execution + DeliverableID + RoleID; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes | Hour quantities for DEL-004-09: R-01=6h, R-08=4h, R-13=18h, R-16=42h. Total=70h. |
| Assumed_Project_Parameters.csv | Parametric (project parameters) | 18 parameter rows; covers project identity, location, contract form, schedule, facility dimensions, equipment, currency | Provides project context (building area ~13,000 sqft, 35' ceiling, 2 cranes, CAD currency). Not directly priced. |
| Professional_Design_Fees.csv | Parametric (fee percentage model) | 5 discipline rows with fee % ranges against construction_value | DF-04 (Electrical: 1.0%–2.2%, recommended 1.6%) available as cross-check. Not used as primary pricing method for this run; LOE-based pricing used instead. |

## Document Sources Read

| Document | Path | Role in Estimate |
|---|---|---|
| _CONTEXT.md | PKG-004_Electrical Design/1_Working/DEL-004-09_Specification/_CONTEXT.md | Deliverable identification: DEL-004-09, PKG-004, Electrical Engineering, Specification |
| Datasheet.md | PKG-004_Electrical Design/1_Working/DEL-004-09_Specification/Datasheet.md | Quantity takeoff: power supply attributes, lighting fixtures (main shop 20, wash bay 6, ancillary 9), ceiling fans (6), receptacle types (5 circuit types), dedicated equipment circuits, exhaust fans, low-voltage systems |
| Specification.md | PKG-004_Electrical Design/1_Working/DEL-004-09_Specification/Specification.md | Requirements REQ-001 through REQ-027; verification criteria; standards; scope boundaries; documentation artifacts |
| Guidance.md | PKG-004_Electrical Design/1_Working/DEL-004-09_Specification/Guidance.md | Design principles (7), considerations (8), trade-offs (3), conflict table (CONF-004-09-01 through CONF-004-09-04) |
| Procedure.md | PKG-004_Electrical Design/1_Working/DEL-004-09_Specification/Procedure.md | Work steps (9 steps), prerequisites (7 TBD inputs), 5 hold points (HOLD-01 through HOLD-05), verification checks, records |
| WDMLRL_Decomposition_Claude.md | _Decomposition/WDMLRL_Decomposition_Claude.md | WBS traceability: PKG-004, DEL-004-09, SOW-0014, OBJ-003/OBJ-005 |
