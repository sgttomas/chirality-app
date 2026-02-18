# Decision Log — EST_DEL-04-01_2026-02-18_2300

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-EST-001 | CBS assigned as `PROF_SERVICES` for all line items | No `CBSHint` present in decomposition. DEL-04-01 is a proposal production deliverable; all costs are professional staff hours. Deterministic mapping rule documented in Run_Context.md. |
| DEC-EST-002 | LOE hours taken directly from Level_of_Effort.csv without adjustment | LOE source (PS-02) provides hours per role for DEL-04-01 in execution 6c. No basis to adjust; STRICT fallback policy prohibits invention. |
| DEC-EST-003 | Hourly rates taken directly from Professional_Staff_Rates.csv without adjustment | Rate table (PS-01) provides market-based Alberta 2024 rates. No override or adjustment factor specified in brief. |
| DEC-EST-004 | Upstream dependencies (DEL-02-01, DEL-08-01, DEL-09-02) do not block estimating | Cost is driven by staff effort allocation, not by upstream content. Dependencies affect deliverable execution readiness but not the cost estimate. |
| DEC-EST-005 | SOW-020 scope included per brief instructions | Brief explicitly states SOW-019 and SOW-020 are BOTH mapped to DEL-04-01. The LOE allocation (14 hours CM) includes both scope items per the Notes column in Level_of_Effort.csv ("Consolidated: SOW-019 methodology + SOW-020 administration in one DEL"). |
| DEC-EST-006 | No fallback pricing applied | All line items have complete basis evidence from rate table sources. STRICT fallback policy not triggered. |
| DEC-EST-007 | Rounding applied at DOLLAR level | Per brief instruction. All computed amounts are already whole dollar amounts (155 x 14 = 2170; 175 x 4 = 700), so rounding had no effect. |
