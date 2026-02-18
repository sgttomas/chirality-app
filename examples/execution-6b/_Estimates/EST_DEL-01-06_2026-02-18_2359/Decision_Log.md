# Decision Log -- EST_DEL-01-06_2026-02-18_2359

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS codes assigned as `PROF_SERVICES.PM` and `PROF_SERVICES.ESTIMATING` based on role Category in Professional_Staff_Rates.csv | Deterministic mapping: Management category + PM role = PROF_SERVICES.PM; Financial category = PROF_SERVICES.ESTIMATING. Documented in Run_Context.md. |
| EST-DEC-002 | All hours sourced from Level_of_Effort.csv rather than independent estimation | Brief instructs: "Use the Level_of_Effort.csv for production hours for DEL-01-06." Compliant with RATE_TABLE basis. |
| EST-DEC-003 | All rates sourced from Professional_Staff_Rates.csv without adjustment | Brief instructs: "Use Professional_Staff_Rates.csv for hourly rates." No markup, escalation, or adjustment applied. |
| EST-DEC-004 | Dependency blockers (DEL-01-03, DEL-01-04, DEL-01-05) noted but not treated as estimate blockers | Dependencies affect execution sequencing of the deliverable, not the validity of the production hour estimate. Hours required to write the narrative are independent of whether predecessor deliverables are complete. |
| EST-DEC-005 | No fallback pricing used | FALLBACK_POLICY = STRICT; all items have direct source evidence from both rate table and LoE files. No fallback needed. |
| EST-DEC-006 | Assumed_Project_Parameters.csv indexed but not used for pricing | This source provides background context (construction values, areas, durations) relevant to the content of the pricing narrative, but DEL-01-06 is a production-cost estimate (hours to write), not a construction estimate. |
