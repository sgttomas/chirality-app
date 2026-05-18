# Decision Log -- EST_DEL-08-03_2026-02-18_2359

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS assigned as `PROFESSIONAL_SERVICES` for all DEL-08-03 line items | No explicit `CBSHint` in decomposition. Deterministic rule: deliverable type is "Commissioning / Narrative" with cost driven entirely by professional staff labour hours. No construction materials, equipment, or subcontract costs apply. |
| EST-DEC-002 | Hours sourced from `Level_of_Effort.csv` rows matching `Execution=6b` and `DeliverableID=DEL-08-03` | Level_of_Effort.csv is the designated hours source per the run brief. Two rows matched: R-02 @ 4 hrs, R-21 @ 4 hrs. |
| EST-DEC-003 | Rates sourced from `Professional_Staff_Rates.csv` by matching `RoleID` | Professional_Staff_Rates.csv is the designated rate table per the run brief. R-02 = $175/hr, R-21 = $140/hr. Both rates confirmed in source with Confidence = MEDIUM. |
| EST-DEC-004 | `Assumed_Project_Parameters.csv` not used for pricing | This file contains construction duration, area, and quantity parameters that are not applicable to a narrative deliverable. Referenced in Source_Index.md for completeness but no pricing values derived from it. |
| EST-DEC-005 | Dependency evidence used for blocker reporting only, not for pricing | Per AGENT_ESTIMATING invariant: "Dependencies are not pricing evidence." DEP-08-03-003 and DEP-08-03-004 noted as authoring readiness blockers in Blockers.md. |
| EST-DEC-006 | ROUNDING=DOLLAR applied; no rounding adjustment needed | Line 1: 4 x $175 = $700.00 (exact dollar). Line 2: 4 x $140 = $560.00 (exact dollar). Total = $1,260.00. No rounding adjustments required. |
