# Decision Log

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-D-01 | CBS mapped to DESIGN_SERVICES for all DEL-05-04 line items | R-13 (Electrical Engineer, Senior) is categorized as Design in Professional_Staff_Rates.csv. Deterministic CBS mapping rule applied per Run_Context.md. |
| EST-D-02 | Single line item produced for DEL-05-04 (one role, one CBS) | Level_of_Effort.csv contains exactly one row for DEL-05-04 (R-13, 8 hrs). No basis to further decompose into sub-line items without additional source evidence. |
| EST-D-03 | ROUNDING=DOLLAR applied; no rounding adjustment needed | 8 hrs x $155/hr = $1,240.00 exactly; no rounding delta. |
| EST-D-04 | Confidence set to MED for L-01 | Both source inputs carry MEDIUM confidence (rate table = MARKET/MEDIUM; hours = PARAMETRIC with no explicit confidence). MED is the appropriate passthrough. |
| EST-D-05 | Assumed_Project_Parameters.csv not used for pricing | No parameters in the file are directly applicable to DEL-05-04 pricing. File indexed for completeness but contributes no line items. |
| EST-D-06 | Dependency rows treated as execution sequencing information, not pricing evidence | Per AGENT_ESTIMATING invariant: "Dependencies are not pricing evidence." Dependency data informs blocker reporting only. |
