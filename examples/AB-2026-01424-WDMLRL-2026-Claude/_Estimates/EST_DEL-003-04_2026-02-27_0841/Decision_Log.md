# Decision Log — EST_DEL-003-04_2026-02-27_0841

| DecID | Decision | Rationale | Source |
|---|---|---|---|
| DEC-001 | Use LOE-based parametric pricing (hours x rates) rather than percentage-of-construction-value fee model | LOE model provides bottom-up estimate with role-specific hours directly from Level_of_Effort.csv. Fee-percentage model requires construction value denominator not available at this stage. LOE approach is more granular and traceable. | Level_of_Effort.csv; Professional_Design_Fees.csv (available but not applied) |
| DEC-002 | Price the aggregate R-15 Mechanical Engineer hours (84 hr) as a single Detail.csv line rather than splitting across sub-tasks | The LOE source provides only a single aggregate hour estimate for R-15 on DEL-003-04. Splitting into sub-tasks would require invention of hour allocations not supported by source data. Sub-tasks are recorded in Items.csv with TBD quantities for documentation purposes. | Level_of_Effort.csv (single row for DEL-003-04/R-15) |
| DEC-003 | Include P.Eng. stamp at $0.00 rather than omitting or inventing a separate cost | The LOE model does not provide a separate P.Eng. review line. The P.Eng. stamp is assumed to be performed by the same R-15 Mechanical Engineer. Recording at $0.00 preserves traceability without inventing a cost. | ASM-003; Level_of_Effort.csv |
| DEC-004 | Assign CBS categories as Design-Management / Design-Production / Design-Engineering | CBS categories derived from role categories in Professional_Staff_Rates.csv (Management, Design) mapped to the design service nature of this deliverable. | Professional_Staff_Rates.csv (Category column) |
| DEC-005 | Do not apply rounding (NONE default) | No rounding parameter specified in brief; default NONE applied per protocol. | AGENT_ESTIMATING.md protocol defaults |
| DEC-006 | Do not update _LATEST.md pointer | UPDATE_LATEST_POINTER = FALSE per brief. | INIT-TASK brief |
