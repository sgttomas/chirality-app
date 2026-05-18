# Decision Log -- EST_DEL-07-04_2026-02-18_2355

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-EST-0704-01 | Assigned CBS code `CBS-01-PROF` (Professional Services / Staff Time) to all DEL-07-04 line items | No CBSHint provided in decomposition; deterministic rule applied: all proposal-stage narrative deliverables priced on professional hours are classified under professional services |
| DEC-EST-0704-02 | Accepted Level_of_Effort.csv as the sole hours source for DEL-07-04, which assigns only R-02 (Project Manager) at 6 hours | Level_of_Effort.csv is the provided hours basis; the agent does not invent additional hours even when the decomposition suggests dual responsible parties (PM + CM). A warning (W-001) is raised for human review. |
| DEC-EST-0704-03 | No fallback pricing was required or applied | All line items for DEL-07-04 are fully priced from RATE_TABLE evidence (hours x rate). FALLBACK_POLICY=STRICT was not triggered. |
| DEC-EST-0704-04 | Assumed_Project_Parameters.csv was indexed but not used for DEL-07-04 pricing | No parameters in the file directly drive DEL-07-04 scope or quantities. It is included in Source_Index for traceability since it was provided as a PRICE_SOURCE. |
| DEC-EST-0704-05 | Dependencies used for blocker analysis only, not for pricing | Per non-negotiable invariant: "Dependencies are not pricing evidence." All 9 dependency rows from DEL-07-04/Dependencies.csv were loaded for blocker/interface analysis and reported in QA. |
