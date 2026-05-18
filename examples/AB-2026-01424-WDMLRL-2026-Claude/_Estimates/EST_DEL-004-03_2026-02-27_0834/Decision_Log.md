# Decision Log — EST_DEL-004-03_2026-02-27_0834

| DecisionID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Use LOE-based pricing (hours x rates) as primary method, not fee-percentage method | Level_of_Effort.csv provides deliverable-specific, role-level hour allocations that are more granular than a percentage-of-construction-value approach. The fee-percentage method (Professional_Design_Fees.csv, DF-04) requires a construction value estimate not available at this scope level. | All 4 priced lines use PARAMETRIC method via LOE x Rate Table. |
| DEC-002 | Items ITEM-005 through ITEM-008 (MEP coordination, utility coordination, County submission, code review) are not separately priced | These activities are embedded within the Electrical Engineer and Project Manager hours from Level_of_Effort.csv. Pricing them separately would double-count effort. They are recorded in Items.csv for takeoff completeness. | 4 items in Items.csv have no corresponding Detail.csv line; no cost is missing. |
| DEC-003 | CBS assignment: Design-Electrical for engineer and BIM roles; Management for PM and estimator roles | Consistent with role Category values in Professional_Staff_Rates.csv (Design vs. Management/Admin) and standard cost breakdown practice. | WBS_CBS_Matrix.csv shows two CBS categories. |
| DEC-004 | FALLBACK_POLICY (ALLOW_PARAMETRIC) not exercised | All items had direct PARAMETRIC pricing evidence from LOE + Rate Table. No fallback was needed. | No warnings generated. |
| DEC-005 | ALLOW_MIXED_METHODS (TRUE) not exercised | All lines priced as PARAMETRIC. No mixed-method situation arose. | Basis-consistency check passes cleanly. |
