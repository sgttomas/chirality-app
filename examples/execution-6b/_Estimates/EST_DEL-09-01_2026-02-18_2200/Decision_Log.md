# Decision Log -- EST_DEL-09-01_2026-02-18_2200

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS codes assigned by role Category from Professional_Staff_Rates.csv: R-17 (Construction) -> LABOUR.CONST; R-02 (Management) -> LABOUR.MGMT; R-15 (Construction) -> LABOUR.CONST | Deterministic CBS mapping rule established in prior runs and documented in Run_Context.md. Consistent with all prior DEL estimates in this execution. |
| EST-DEC-002 | No scheduling software line item included | Brief states "Scheduling software costs if applicable (PS-10: embedded in hourly rate per INDEX.md)." Software costs are embedded in the Scheduler's hourly rate of $130/hr. No separate line item warranted. |
| EST-DEC-003 | All 3 Level_of_Effort.csv rows for DEL-09-01 used without modification | Hours are sourced directly from Level_of_Effort.csv (PARAMETRIC basis); no reason to deviate under STRICT fallback policy. |
| EST-DEC-004 | Execution dependencies treated as non-blocking for estimate | Dependencies (DEL-06-02, DEL-07-01, DEL-08-01, DEL-10-02) affect content production but not the cost of producing DEL-09-01. Hours are defined by the Level_of_Effort table regardless of upstream deliverable completion status. |
| EST-DEC-005 | Rounding applied to DOLLAR level per brief | All amounts are whole-dollar values as computed (no fractional cents in any line item), so rounding had no arithmetic effect. |
