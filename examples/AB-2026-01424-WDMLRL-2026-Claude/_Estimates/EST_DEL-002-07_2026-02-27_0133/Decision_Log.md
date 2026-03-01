# Decision Log — EST_DEL-002-07_2026-02-27_0133

| DecisionID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Used LOE-based parametric pricing (hours x rates) rather than fee-percentage-based pricing from Professional_Design_Fees.csv | Level_of_Effort.csv provides deliverable-specific hour allocations by role, which is more granular and traceable than a percentage-of-construction-value approach. The fee-percentage method also requires a construction value input that is not yet established. | Pricing is role-specific and traceable to two source files (LOE + Rates). |
| DEC-002 | Scope resolved to single deliverable DEL-002-07 only | SCOPE parameter specified DEL-002-07 explicitly. No package-level or multi-deliverable rollup was requested. | 1 deliverable, 4 priced roles, 8 line items total. |
| DEC-003 | CBS categories assigned as Design-Structural (engineering + drafting + QA + stamp) and Management (PM + estimating + County review) | CBS not defined in decomposition or project parameters; categories assigned based on role function per Professional_Staff_Rates.csv Category field. | WBS_CBS_Matrix groups costs into two categories. |
| DEC-004 | Lump-sum items for review, coordination, County approval, and P.Eng. stamp priced at $0 | These activities are represented in the LOE hour allocations for Structural Engineer and Project Manager. Double-counting would overstate the estimate. Items retained in Items.csv for completeness and traceability. | Zero-cost lines visible in Detail.csv with explanation in Notes. |
| DEC-005 | No fallback pricing required | All items have parametric pricing sources available (LOE + Rates). FALLBACK_POLICY = ALLOW_PARAMETRIC was not exercised because primary PARAMETRIC sources covered all items. | No TBD amounts in Detail.csv. |
| DEC-006 | UPDATE_LATEST_POINTER = FALSE respected | Per brief instruction; no _LATEST.md pointer file created or modified. | No pointer file changes. |
