# Decision Log — EST_DEL-002-02_2026-02-26_2246

| DecisionID | Decision | Rationale | Source |
|---|---|---|---|
| DEC-001 | Scope limited to DEL-002-02 (Foundation Plan) only; no other PKG-002 deliverables included | Scope parameter specifies DEL-002-02 only | Run brief: SCOPE = DEL-002-02 |
| DEC-002 | Deliverable classified as a design deliverable (professional services labour); no construction materials or labour included | DEL-002-02 is a Drawing Set type per _CONTEXT.md; construction is covered by separate deliverables (DEL-010-01 in PKG-010) | _CONTEXT.md: Type = Drawing Set |
| DEC-003 | Pricing derived from LOE hours x staff rates (PARAMETRIC method) | BASIS_OF_ESTIMATE = PARAMETRIC; Level_of_Effort.csv provides role-specific hours for DEL-002-02; Professional_Staff_Rates.csv provides hourly rates | Run brief; LOE and rate sources |
| DEC-004 | Four roles assigned to DEL-002-02: Structural Engineer (R-14), BIM Technician (R-13), Project Manager (R-01), Cost Estimator (R-08) | Level_of_Effort.csv contains exactly 4 rows for DEL-002-02 | Level_of_Effort.csv |
| DEC-005 | CBS categories assigned as Design-Structural (for R-14 and R-13) and Management (for R-01 and R-08) | Role categories from Professional_Staff_Rates.csv: R-14 is Design, R-13 is Design, R-01 is Management, R-08 is Management | Professional_Staff_Rates.csv |
| DEC-006 | All items classified as UNIT_RATE (hours x rate) rather than LUMP_SUM | Each item has a measurable quantity (hours) and unit rate ($/hr); UNIT_RATE is more transparent for review | Schema convention; standard for LOE-based estimates |
| DEC-007 | No fallback pricing required | All 4 items fully matched to pricing sources; FALLBACK_POLICY not triggered | 100% pricing coverage |
| DEC-008 | Professional_Design_Fees.csv noted but not used for primary pricing; reserved as cross-check | LOE-based pricing is more granular and traceable than percentage-of-construction-value; fee model requires a construction value that is not within this deliverable's scope | Source_Index.md |
