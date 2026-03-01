# Source Index — EST_DEL-015-02_2026-02-27_0848

## Price Sources Indexed

| # | Source File | Source Type | Coverage | Parsing Notes |
|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | Rate Table | 25 roles with hourly CAD rates; PARAMETRIC basis; MEDIUM confidence | Clean CSV; RoleID key; used for DL-022 through DL-027 |
| 2 | Level_of_Effort.csv | Parametric Model | Hours by role by deliverable; DEL-015-02 has 6 role entries (R-01, R-02, R-03, R-05, R-06, R-08) totalling 38 hours | Clean CSV; keyed by Execution + DeliverableID + RoleID |
| 3 | Assumed_Project_Parameters.csv | Parametric Parameters | 18 parameters; key values used: PP-10 (13000 sqft floor area), PP-11 (35ft ceiling), PP-12/PP-13 (2x5-ton cranes), PP-17 (CAD currency) | Clean CSV; ParameterID key |
| 4 | Electrical_System_Rates.csv | Rate Table / Parametric | 6 items; ES-01 (high-bay LED installed: 520 CAD/EA) directly applicable; ES-02 through ES-06 not used for lighting scope | Clean CSV; ItemID key; ES-01 is primary rate for high-bay fixtures |
| 5 | Underground_Utility_Rates.csv | Rate Table / Parametric | 5 items; NOT applicable to lighting scope (covers underground water, sanitary, conduit, septic, cistern) | Clean CSV; not used in this estimate |
| 6 | Construction_Labour_Rates.csv | Rate Table | 10 trade rates; T-04 Electrician (fully burdened: 96.00 CAD/hr) is primary rate used; T-08 Labourer (65.10 CAD/hr) not needed for this scope | Clean CSV; TradeID key |

## Source Gaps

| Gap | Impact | Resolution |
|---|---|---|
| No 8-foot LED linear fixture rate in Electrical_System_Rates.csv | ITM-003, ITM-004, ITM-005 (9 fixtures total) priced via parametric estimate (280 CAD/EA) | A-003 in Assumptions_Log; based on industry parametric for installed 8ft LED linear fixtures |
| No branch circuit wiring rate table (per-fixture or per-metre) | ITM-009, ITM-010, ITM-011 priced as parametric lump-sum allowances | A-006 in Assumptions_Log |
| No switching/controls rate | ITM-012 priced as allowance | A-007 in Assumptions_Log; controls strategy TBD |
| No aerial platform rental rate | ITM-013 priced as parametric allowance | A-008 in Assumptions_Log |
| No mounting hardware rate | ITM-006, ITM-007, ITM-008 priced as parametric per-unit allowances | A-004, A-005 in Assumptions_Log |

## Deliverable Documents Read

| Document | Status | Items Extracted |
|---|---|---|
| Datasheet.md | Read | Fixture schedule (ITM-001 through ITM-005), mounting hardware (ITM-006 through ITM-008), building context parameters |
| Specification.md | Read | REQ-L-01 through REQ-L-16; scope boundaries; verification requirements; professional oversight needs |
| Guidance.md | Read | Design principles, trade-offs, conflict table; informed assumptions for wet-rating premium, controls allowance |
| Procedure.md | Read | Work steps informed labour hours (ITM-009 through ITM-021, ITM-028, ITM-029); equipment needs (ITM-013) |
