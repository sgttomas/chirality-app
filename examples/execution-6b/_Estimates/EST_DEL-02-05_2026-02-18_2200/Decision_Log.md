# Decision Log

**RunID:** EST_DEL-02-05_2026-02-18_2200

---

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-D-001 | CBS assigned as `PROFESSIONAL_SERVICES` for all line items | DEL-02-05 is a proposal-production narrative; all costs are professional service hours (electrical engineering labour). No CBSHint was provided in the decomposition. Deterministic rule: all labour-hour line items on proposal-production deliverables map to PROFESSIONAL_SERVICES. |
| EST-D-002 | Hours sourced from Level_of_Effort.csv, rates from Professional_Staff_Rates.csv | Level_of_Effort.csv provides deliverable-level hour estimates by role; Professional_Staff_Rates.csv provides the corresponding hourly rates. Both are explicit PRICE_SOURCES in the brief. |
| EST-D-003 | Assumed_Project_Parameters.csv not used for direct pricing | This file provides project-level parameters (areas, durations, quantities) that are contextual but not applicable to pricing a narrative deliverable. No line items reference it. |
| EST-D-004 | Rounding applied at DOLLAR level | Per brief ROUNDING=DOLLAR. All computed amounts were already whole-dollar values (16x155=2480, 8x125=1000), so no rounding adjustment was needed. |
| EST-D-005 | No fallback pricing applied | FALLBACK_POLICY=STRICT. All line items had complete basis evidence (hours + rates). No TBD amounts were generated. |
| EST-D-006 | Dependency evidence used for blocker assessment only, not pricing | Per non-negotiable invariant: "Dependencies are not pricing evidence." Dependencies.csv was read to identify potential blockers; none were found that would prevent estimating. |
