# Decision Log — EST_DEL-004-02_2026-02-27_0833

| DecisionID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Used PARAMETRIC method (LOE hours x staff rates) as primary pricing approach | BASIS_OF_ESTIMATE=PARAMETRIC specified in run brief; Level_of_Effort.csv provides granular hour estimates by role for DEL-004-02; Professional_Staff_Rates.csv provides matching hourly rates | All 4 priced lines use PARAMETRIC method |
| DEC-002 | Did not use Professional_Design_Fees.csv as primary method | Fee-percentage model requires a construction value estimate which is not in scope for this single-deliverable run; LOE method is more granular and preferred when available | Fee model used only as a cross-check in Summary.md |
| DEC-003 | Activity items (ITEM-005 through ITEM-016) priced at $0 with effort included in labor lines | Procedure steps and specification requirements represent work activities performed by the 4 staff roles; their effort is captured in the LOE hour allocations (ITEM-001 through ITEM-004); separate activity line items maintained for traceability | 12 zero-cost traceability lines in Detail.csv; total cost unchanged |
| DEC-004 | CBS categories assigned as Management (PM + Cost Estimator) and Design (BIM Technician + Electrical Engineer) | Based on Category field in Professional_Staff_Rates.csv: R-01=Management, R-08=Management, R-13=Design, R-16=Design | WBS_CBS_Matrix shows Management=$1,530 and Design=$17,280 |
| DEC-005 | FALLBACK_POLICY=ALLOW_PARAMETRIC not exercised | No items required fallback — all items matched to PARAMETRIC pricing sources | No fallback lines in Detail.csv |
| DEC-006 | UPDATE_LATEST_POINTER=FALSE respected | Per run brief instruction; no pointer files modified | No _LATEST.md file created or modified |
| DEC-007 | Rounding=NONE applied (default) | No rounding instruction provided in run brief; NONE is the protocol default | All amounts expressed to 2 decimal places as computed |
