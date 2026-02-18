# Decision Log

**RunID:** EST_DEL-02-03_2026-02-18_2100

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-D-001 | CBS code `PROF-STRUCT` assigned to all DEL-02-03 line items | No explicit CBSHint in decomposition. Both roles (R-09, R-10) are structural engineering professionals; deterministic mapping to professional services -- structural discipline. |
| EST-D-002 | Method set to `RATE_TABLE` for all line items | BASIS_OF_ESTIMATE=RATE_TABLE; hours from Level_of_Effort.csv joined with rates from Professional_Staff_Rates.csv constitutes a rate-table pricing approach. No fallback was needed. |
| EST-D-003 | ROUNDING=DOLLAR applied; no rounding impact on this run | All computed amounts (16x155=2480; 8x125=1000) are already whole-dollar values. No rounding adjustments required. |
| EST-D-004 | Assumed_Project_Parameters.csv indexed but not used for pricing | Parameters file provides building areas and bay counts for context. No line-item pricing was derived from it. It is retained in Source_Index for audit completeness. |
| EST-D-005 | No blocker report produced | Dependencies.csv loaded successfully; no unresolved inputs block the estimate. Production-readiness dependencies (DEL-02-01, DEL-02-02, Appendix D) are noted in Run_Context but do not affect pricing evidence availability. |
