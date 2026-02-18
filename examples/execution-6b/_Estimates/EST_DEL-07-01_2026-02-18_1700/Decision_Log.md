# Decision Log -- EST_DEL-07-01_2026-02-18_1700

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS codes assigned by role Category from Professional_Staff_Rates.csv: Management -> MGMT, Construction -> CONST | Deterministic mapping rule; no explicit CBSHint found in decomposition for DEL-07-01; role category is the most defensible automated mapping |
| EST-DEC-002 | Rounding applied at DOLLAR level per brief instruction | ROUNDING=DOLLAR; all amounts happen to be whole dollars already (155 x 12 = 1860; 175 x 4 = 700) so no rounding adjustment was needed |
| EST-DEC-003 | Assumed_Project_Parameters.csv reviewed but not used as a pricing input for DEL-07-01 | No parameters in the file directly drive hours or rates for this narrative deliverable; file provides project context only |
| EST-DEC-004 | Cost ownership boundary enforced: DEL-07-01 covers methodology framework only; administration content (DEL-07-02) excluded | Per brief Cost Ownership Rules; prevents double-counting between DEL-07-01 and DEL-07-02 |
| EST-DEC-005 | All defaults applied as specified in brief: FALLBACK_POLICY=STRICT, ALLOW_MIXED_METHODS=FALSE, UPDATE_LATEST_POINTER=FALSE | No deviations from brief defaults were needed |
