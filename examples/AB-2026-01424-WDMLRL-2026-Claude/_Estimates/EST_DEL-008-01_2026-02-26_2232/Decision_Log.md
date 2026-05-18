# Decision Log — EST_DEL-008-01_2026-02-26_2232

| DecisionID | Decision | Rationale | Impact |
|------------|----------|-----------|--------|
| DEC-001 | Used PARAMETRIC method for all line items | BASIS_OF_ESTIMATE = PARAMETRIC; ALLOW_MIXED_METHODS = TRUE but no other source types available | All lines use PARAMETRIC method |
| DEC-002 | Applied R-20 Geotechnical Engineer rate ($175/hr) to all geotech professional service lines even though LoE hours are not provided | Rate is available in Professional_Staff_Rates.csv; FALLBACK_POLICY = ALLOW_PARAMETRIC permits parametric pricing with available rate data; quantities remain TBD | Amounts remain TBD but unit rates are populated where applicable |
| DEC-003 | Recorded field investigation items (drilling, test pits, monitoring, sampling, lab testing) as fully TBD | No rate sources exist for these items in PRICE_SOURCES; agent must not invent prices per non-negotiable invariants | 10 line items have both rate and amount as TBD |
| DEC-004 | Broke out 23 distinct line items from engineering documents | Procedure describes 7 major steps with multiple sub-activities; Specification defines 12 requirements; items were identified at a level of granularity useful for pricing when rates become available | Provides a structured takeoff for future pricing once sources are available |
| DEC-005 | Applied CBS categories based on work type rather than formal CBS code structure | No formal CBS structure provided in PRICE_SOURCES or decomposition; CBS categories are descriptive and consistent across the deliverable | CBS rollups are by work category |
| DEC-006 | Marked photographic documentation (ITEM-011) and P.Eng. seal (ITEM-020) as separate lump-sum items | These are distinct deliverable requirements per Specification and Procedure but may be bundled into other activities in practice | Separate line items improve traceability to requirements |
| DEC-007 | Used LoE hours directly for PM and Cost Estimator without applying any efficiency factor or overhead markup | Level_of_Effort.csv provides direct hours; no overhead/markup structure is defined in PRICE_SOURCES | Amounts may understate actual cost if overhead is applicable |
