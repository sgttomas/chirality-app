# Source Index — EST_DEL-003-05_2026-02-27_0833

## Pricing Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports | Limitations |
|---|---|---|---|---|---|
| PS-01 | Professional_Staff_Rates.csv | Rate Table (PARAMETRIC) | 25 roles with hourly rates in CAD; all rates basis = PARAMETRIC, confidence = MEDIUM | Hourly rate lookup for all professional staff roles (R-01 through R-25) | Rates are parametric estimates, not firm quotes; no overtime/premium rates included |
| PS-02 | Level_of_Effort.csv | Parametric Model | Multi-deliverable LOE table; each row maps (Execution, DeliverableID, RoleID) to EstimatedHours | Hour allocations per deliverable per role; DEL-003-05 has 4 role assignments (R-01, R-08, R-13, R-15) totalling 50 hours | Hours are parametric estimates; no task-level breakdown within the deliverable; confidence = PARAMETRIC basis |
| PS-03 | Assumed_Project_Parameters.csv | Parametric Context | 19 parameter rows covering project identity, location, facility, equipment, schedule, economics | Contextual parameters for scope confirmation (building area, crane count, cistern volume, currency, etc.) | Does not contain pricing data directly; provides parametric context |
| PS-04 | Professional_Design_Fees.csv | Parametric Model | 5 discipline-level fee percentages (min/max/recommended) applied to construction_value | Alternative pricing method: Mechanical design fee = 1.0%-2.2% (recommended 1.6%) of construction value | Cannot be used without an established construction value; not applied in this run because construction value is unknown |

## Deliverable Documents Read (Quantity Takeoff Sources)

| Document | Path | Items Extracted |
|---|---|---|
| _CONTEXT.md | PKG-003_Mechanical Design/1_Working/DEL-003-05_Equipment-Schedule/_CONTEXT.md | Deliverable identity, package, discipline, type |
| Datasheet.md | PKG-003_Mechanical Design/1_Working/DEL-003-05_Equipment-Schedule/Datasheet.md | Equipment register (8 equipment types: HTG-001, AEX-001, MAU-001, EXH-001/002/003/004, CF-001-006); building parameters; operating conditions |
| Specification.md | PKG-003_Mechanical Design/1_Working/DEL-003-05_Equipment-Schedule/Specification.md | 17 requirements (REQ-001 through REQ-017); verification matrix; format and coordination requirements |
| Guidance.md | PKG-003_Mechanical Design/1_Working/DEL-003-05_Equipment-Schedule/Guidance.md | Design principles; technology trade-offs; 6 conflict items (CON-001 through CON-006); applicable standards |
| Procedure.md | PKG-003_Mechanical Design/1_Working/DEL-003-05_Equipment-Schedule/Procedure.md | 3-phase production workflow (14 steps); prerequisites; QC review checklist; records requirements |

## Decomposition Reference

| Source | Path | Use |
|---|---|---|
| WDMLRL_Decomposition_Claude.md | _Decomposition/WDMLRL_Decomposition_Claude.md | WBS traceability: DEL-003-05 under PKG-003 Mechanical Design; parent scope SOW-0013; supports OBJ-003, OBJ-004 |
