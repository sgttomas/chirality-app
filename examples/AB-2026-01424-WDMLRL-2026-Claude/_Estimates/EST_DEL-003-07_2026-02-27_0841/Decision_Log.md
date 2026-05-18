# Decision Log — EST_DEL-003-07_2026-02-27_0841

## Decisions Applied During This Run

| DecisionID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Used PARAMETRIC method for all line items (LOE hours x staff rates) | BASIS_OF_ESTIMATE = PARAMETRIC; Level_of_Effort.csv provides hours per role for DEL-003-07; Professional_Staff_Rates.csv provides hourly rates | All 4 Detail.csv lines use PARAMETRIC method; no fallback needed |
| DEC-002 | Did not use Professional_Design_Fees.csv as primary pricing method | Fee-percentage method requires a construction value baseline (PKG-013 total) which is not available; LOE-based method is more granular and directly traceable | Fee-percentage source retained in Source_Index.md as cross-check benchmark only |
| DEC-003 | Items.csv contains 20 rows (4 billable roles + 16 specification section identifiers) but Detail.csv contains only 4 priced lines | ITEM-005 through ITEM-020 represent specification content sections that are produced within the Mechanical Engineer's 42 hours; pricing them separately would double-count | No double-counting; Items.csv provides traceability without inflation |
| DEC-004 | CBS categories assigned as Management (PM + Estimator) and Design (BIM Tech + Mech Eng) | Category assignments follow the Category column in Professional_Staff_Rates.csv (R-01: Management, R-08: Management, R-13: Design, R-15: Design) | WBS_CBS_Matrix.csv totals split Management ($1,530) and Design ($8,640) |
| DEC-005 | Did not update _LATEST.md pointer | UPDATE_LATEST_POINTER = FALSE per run brief | No pointer file modified |
| DEC-006 | Rounding set to NONE (default) | No ROUNDING parameter provided in run brief; using protocol default | All amounts at full precision |
