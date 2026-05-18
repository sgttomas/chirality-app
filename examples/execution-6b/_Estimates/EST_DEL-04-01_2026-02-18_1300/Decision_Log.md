# Decision Log

**RunID:** EST_DEL-04-01_2026-02-18_1300

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS mapped to `PROF_SERVICES` for all DEL-04-01 line items | No explicit CBSHint in decomposition. Deterministic rule applied: narrative deliverables composed entirely of professional consulting hours are mapped to CBS = PROF_SERVICES. |
| EST-DEC-002 | Used Level_of_Effort.csv as the quantity source (hours) and Professional_Staff_Rates.csv as the rate source | Brief instructs: "Use Level_of_Effort.csv for hours, Professional_Staff_Rates.csv for rates." Both sources are listed in PRICE_SOURCES. |
| EST-DEC-003 | Assumed_Project_Parameters.csv loaded but not used for pricing | Project parameters provide context (building areas, quantities) but do not drive professional hours for this narrative deliverable. Included in Source_Index for completeness. |
| EST-DEC-004 | No fallback pricing applied | FALLBACK_POLICY = STRICT. All line items have rate table evidence. No TBD amounts required. |
| EST-DEC-005 | Cross-discipline sustainability coordination hours attributed to DEL-04-01 | Per brief: "Cross-discipline coordination hours for sustainability belong in DEL-04-01." The Building Science Consultant 12 hours includes this coordination effort. |
| EST-DEC-006 | Rounding applied at DOLLAR level | Per brief ROUNDING = DOLLAR. Both line item amounts ($1,980 and $580) are already whole dollars; no rounding adjustment needed. |
