# Decision_Log.md
## Estimate Decision Log — DEL-009-04

**RunID:** EST_DEL-009-04_2026-02-28_0806

---

| Decision ID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Allocated LOE source hours (6h PM + 4h CE = 10h) across Phase 1 and Phase 2 setup activities (DL-001 through DL-008) rather than treating as a single lump sum | The deliverable procedure defines 5 distinct phases with granular steps; allocating hours across the identifiable setup steps improves traceability and review | Changes the line-item breakdown but not the total priced amount ($1,530 CAD); carried forward from prior snapshot |
| DEC-002 | DL-019 and DL-020 are presented as aggregate LOE-source cross-check lines, not additive with DL-001 through DL-008 | The allocated detail lines (DL-001 through DL-008) sum to $1,530 and represent the same hours as the LOE source rows; presenting both allows independent verification without double-counting | WBS_CBS_Matrix notes this explicitly; carried forward from prior snapshot |
| DEC-003 | Resolved DL-009, DL-010, DL-011, DL-012, DL-013, DL-014, DL-018 using newly available R-06, R-09, R-22 LOE allocations and parametric pricing | Level_of_Effort.csv now includes R-06 (16h), R-09 (12h), R-22 (20h) for DEL-009-04 with activity-level notes enabling allocation to specific detail lines | 7 former TBD lines now priced at $3,680 total via PARAMETRIC method |
| DEC-004 | Carried DL-015 (deficiency tracking), DL-016 (regulatory change), DL-017 (guarantee maintenance) as fixed ALLOWANCE items rather than PARAMETRIC | These 3 activities are operationally contingent: deficiency count is unknown, regulatory changes may not occur, and guarantee-period scope depends on CCC status. No parametric model exists in the LOE source for these. | $3,900 in ALLOWANCE at LOW confidence; RUN_STATUS remains WARNINGS |
| DEC-005 | Set DL-013 (County notification) to $0 with note that effort is included in DL-011 | LOE row 582 note states R-22 hours cover "County coordination per inspection (~12 x 1hr)"; DL-013 is a sub-activity of DL-011 and pricing it separately would double-count | Avoids double-counting; DL-013 shows as $0 with explanatory note |
| DEC-006 | Priced DL-018 (final compliance summary) as a blended LS of $670 using 3 roles | Closeout requires multi-role effort: R-06 for QA review (2h x $135), R-09 for document assembly (2h x $75), R-22 for final compliance verification (2h x $125) | $670 blended unit rate; 6 hours consumed across 3 roles |
| DEC-007 | Used a single CBS category "Professional Services" for all line items | DEL-009-04 is entirely a professional-services deliverable (register/log type with no materials, equipment, or construction labor); a single CBS is appropriate | Simplifies rollup; all costs are labor; carried forward from prior snapshot |
| DEC-008 | Permit fees excluded from estimate | RFP S3.3.1 explicitly states permit fees are paid by Camrose County. Confirmed by Datasheet Condition "Permit fee exclusion." | No permit fee line items in estimate; carried forward from prior snapshot |
