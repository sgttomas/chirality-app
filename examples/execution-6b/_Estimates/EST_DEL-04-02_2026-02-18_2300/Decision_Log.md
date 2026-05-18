# Decision Log

| DecisionID | Decision | Rationale |
|---|---|---|
| D-0402-01 | CBS assigned as DESIGN_SERVICES for all DEL-04-02 line items | R-11 (Mechanical Engineer Senior) is categorized as "Design" in Professional_Staff_Rates.csv. Deterministic mapping: Design category -> DESIGN_SERVICES CBS. |
| D-0402-02 | Single line item produced for DEL-04-02 (1 role) | Level_of_Effort.csv contains exactly 1 row for DEL-04-02 (R-11, 10 hrs). No intermediate mechanical engineer hours are assigned to this deliverable in the source data. STRICT fallback policy prevents adding unsupported line items. |
| D-0402-03 | Scope boundary: mechanical energy efficiency narrative only | Per brief Cost Ownership rules: DEL-04-02 owns mechanical energy efficiency content. Base mechanical system selection is DEL-02-04 (Mechanical Concept Narrative). Mechanical maintainability is DEL-05-03. Solar-ready structural provisions are DEL-02-03. Solar-ready electrical provisions are DEL-04-03. |
| D-0402-04 | Dependencies treated as informational, not pricing blockers | All 5 upstream execution dependencies (DEL-04-01, DEL-02-04, DEL-02-01, DEL-02-02, DEL-02-03) inform production sequencing and content quality but do not affect the availability of hours or rates for pricing purposes. |
| D-0402-05 | Rounding applied as DOLLAR | Per run brief ROUNDING=DOLLAR. Amount 10 x 160 = 1600 is already a whole dollar value; no rounding adjustment needed. |
