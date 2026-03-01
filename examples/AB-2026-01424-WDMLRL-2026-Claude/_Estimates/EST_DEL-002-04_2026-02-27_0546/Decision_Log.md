# Decision Log — EST_DEL-002-04_2026-02-27_0546

| ID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Used LOE-based parametric pricing (hours x rates) rather than fee-percentage method | Level_of_Effort.csv provides role-level hours specific to DEL-002-04; this gives more granular and traceable pricing than applying a blanket 1.8% structural fee percentage from Professional_Design_Fees.csv | Primary pricing method; all line items derived from this approach |
| DEC-002 | Mapped ITEM-005 through ITEM-008 as zero-cost lump-sum activities with effort embedded in parent labour items | QC review (Step 14), coordination review (Step 15), P.Eng. stamp (Step 16), and IFC issue (Step 17) are procedural milestones whose labour effort is already captured in the Structural Engineer and PM hourly allocations | Prevents double-counting while maintaining traceability to all Procedure steps |
| DEC-003 | Classified CBS as Design-Structural for Structural Engineer and BIM Technician; Management for PM and Cost Estimator | Consistent with role categories in Professional_Staff_Rates.csv (Design vs Management) and the deliverable's nature as a design drawing set | Affects WBS_CBS_Matrix rollup groupings |
| DEC-004 | Did not apply contingency or escalation | No contingency table or escalation factors provided in PRICE_SOURCES; FALLBACK_POLICY = ALLOW_PARAMETRIC does not mandate contingency; flagged in warnings | Estimate represents base-case parametric cost without risk adjustment |
| DEC-005 | Did not include material/printing/reproduction costs | No material cost source provided in PRICE_SOURCES for this deliverable scope; Drawing Set deliverable is a professional services output | W-001 warning issued; estimate is design-labour-only |
| DEC-006 | No fallback pricing required | All items priced from primary PARAMETRIC sources (LOE + Staff Rates); FALLBACK_POLICY not triggered | Full pricing coverage achieved without fallback |
