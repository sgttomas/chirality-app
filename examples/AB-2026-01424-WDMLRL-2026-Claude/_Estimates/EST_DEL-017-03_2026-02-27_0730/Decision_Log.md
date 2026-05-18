# Decision Log — EST_DEL-017-03_2026-02-27_0730

| Decision ID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Scope resolved as single deliverable DEL-017-03 | SCOPE parameter specifies DEL-017-03 only; confirmed in Decomposition PKG-017 table | 1 deliverable estimated |
| DEC-002 | BASIS_OF_ESTIMATE validated as PARAMETRIC | Matches allowed enum values; all pricing sources are parametric-basis | Drives method selection for all line items |
| DEC-003 | FALLBACK_POLICY = ALLOW_PARAMETRIC applied | 9 items lack direct source evidence in PRICE_SOURCES; parametric estimates generated rather than TBD amounts | $12,050 priced parametrically without direct source; flagged in QA |
| DEC-004 | Professional staff hours taken directly from Level_of_Effort.csv | LOE CSV provides explicit per-deliverable, per-role hour allocations for DEL-017-03 | 38 total professional hours across 6 roles = $5,590 |
| DEC-005 | Washroom area assumed at 12 m2 for floor/ceiling and 30 m2 for walls | Existing footprint not dimensioned in App B drawings; Datasheet records as TBD | Affects ITEM-015, ITEM-016, ITEM-023, ITEM-035 pricing |
| DEC-006 | Minimum fixture count assumed: 1 toilet, 1 sink, 1 urinal | SOW-0074 requires "at minimum one urinal"; existing fixture count TBD; design-build context means minimum counts are appropriate for parametric estimate | Affects ITEM-017, ITEM-018, ITEM-019 |
| DEC-007 | Partition area assumed at 15 m2 | Urinal privacy screen, layout modifications; extent TBD pending design | Affects ITEM-014 pricing |
| DEC-008 | Hazmat assessment included as $2,500 parametric allowance | Procedure Step 2.0 flags as TBD; existing building demolition context makes this prudent to include | DL-006 = $2,500 LOW confidence |
| DEC-009 | Permit fees excluded | RFP section 3.3.1 assigns permit fees to County; per Specification exclusions | No permit fee line items in estimate |
| DEC-010 | DEL-017-04 (locker/change room) excluded per scope boundary | Decomposition and Guidance Conflict Table C-01 separate washroom (DEL-017-03) from locker room (DEL-017-04) | Only SOW-0072 + SOW-0074 scope estimated |
| DEC-011 | Rounding applied as NONE (default) | No ROUNDING parameter specified in brief; default applied | Amounts carried to cent precision |
| DEC-012 | UPDATE_LATEST_POINTER = FALSE | Brief specifies FALSE; no pointer file modified | _LATEST.md not touched |
| DEC-013 | Design development costs included under DEL-017-03 | Renovation layout design (DL-003) is part of the design-build scope for this deliverable, distinct from the architectural drawing set deliverables in PKG-001 | $3,500 design cost included |
