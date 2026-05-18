# Decision Log -- EST_DEL-05-01_2026-02-18_2350

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS assigned as CBS-100 (Professional Fees / Design Services) for all DEL-05-01 line items | No CBSHint in decomposition. DEL-05-01 is a narrative deliverable; all cost is professional labour for design services. Deterministic rule documented in Run_Context.md. |
| EST-DEC-002 | Single line item used for DEL-05-01 (one role, one activity) | Level_of_Effort.csv contains exactly one row for DEL-05-01: R-04 Architect (Project) at 10 hours. No basis to subdivide further without inventing scope splits. |
| EST-DEC-003 | Coordination effort with DEL-05-02, DEL-05-03, DEL-05-04 is treated as embedded in the 10-hour allocation | Level_of_Effort.csv does not break out coordination hours separately. Dependencies.csv confirms interfaces exist but does not quantify coordination time. No invention of additional hours. |
| EST-DEC-004 | Assumed_Project_Parameters.csv used for context only (not for pricing) | Parameters such as building areas and design life targets provide scope context for DEL-05-01 but do not drive line item pricing. Pricing is fully determined by LoE hours x rate table rates. |
| EST-DEC-005 | Confidence set to MED for the single line item | Professional_Staff_Rates.csv rates are MEDIUM confidence; Level_of_Effort.csv hours are PARAMETRIC basis. Combined confidence is MED. |
