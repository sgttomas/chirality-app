# Decision_Log.md
## Estimate Decision Log — DEL-009-04

**RunID:** EST_DEL-009-04_2026-02-27_0730

---

| Decision ID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Allocated LOE source hours (6h PM + 4h CE = 10h) across Phase 1 and Phase 2 setup activities (DL-001 through DL-008) rather than treating as a single lump sum | The deliverable procedure defines 5 distinct phases with granular steps; allocating hours across the identifiable setup steps improves traceability and review | Changes the line-item breakdown but not the total priced amount ($1,530 CAD) |
| DEC-002 | DL-019 and DL-020 are presented as aggregate LOE-source cross-check lines, not additive with DL-001 through DL-008 | The allocated detail lines (DL-001 through DL-008) sum to $1,530 and represent the same hours as the LOE source rows; presenting both allows independent verification without double-counting | WBS_CBS_Matrix notes this explicitly; total is $1,530, not $3,060 |
| DEC-003 | Set Amount = TBD for all Phase 3, Phase 4, and Phase 5 items rather than applying an allowance or parametric model | The FALLBACK_POLICY permits parametric estimates, but no parametric model for construction-phase compliance register operation exists in the provided PRICE_SOURCES. Inventing hours would violate the no-invention invariant. | 10 of 20 lines remain TBD; RUN_STATUS = WARNINGS |
| DEC-004 | Used a single CBS category "Professional Services" for all line items | DEL-009-04 is entirely a professional-services deliverable (register/log type with no materials, equipment, or construction labor); a single CBS is appropriate | Simplifies rollup; all costs are labor |
| DEC-005 | Did not include R-22 Permitting Specialist hours despite role relevance | LOE source does not allocate R-22 hours to DEL-009-04; adding hours not in the source would constitute invention. Flagged in QA as improvement. | Potential underestimate of operational effort; documented in QA recommendations |
| DEC-006 | Permit fees excluded from estimate | RFP §3.3.1 explicitly states permit fees are paid by Camrose County. Confirmed by Datasheet Condition "Permit fee exclusion." | No permit fee line items in estimate |
