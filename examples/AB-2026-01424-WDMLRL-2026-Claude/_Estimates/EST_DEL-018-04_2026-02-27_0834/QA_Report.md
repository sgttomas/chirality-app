# QA Report — EST_DEL-018-04_2026-02-27_0834

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and all items are priced. However, material TBDs remain (pad dimensions from conceptual drawings only, concrete mix design TBD, crane pad structural design TBD). The estimate is suitable for budgeting purposes with the understanding that IFC civil drawings will refine quantities.

---

## S1 — Write Quarantine Respected

| Check | Result |
|-------|--------|
| All files written under `_Estimates/EST_DEL-018-04_2026-02-27_0834/` | PASS |
| No modifications to deliverable working files, lifecycle files, decomposition, or dependency registers | PASS |

## S2 — Snapshot Created

| Check | Result |
|-------|--------|
| Snapshot folder `EST_DEL-018-04_2026-02-27_0834` exists | PASS |

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|-------|--------|
| BASIS_OF_ESTIMATE = PARAMETRIC | PASS (valid enum value) |

## S4 — Required Artifacts Exist

| Artifact | Status |
|----------|--------|
| Run_Context.md | PRESENT |
| Items.csv | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Detail.csv | PRESENT (optional; produced) |

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|-------|--------|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All PricingMode values are UNIT_RATE or LUMP_SUM | PASS |
| Every row traces to a SourceDoc and SourceSection | PASS |
| Row count | 21 items |
| TBD quantities | 0 (all quantities resolved with parametric assumptions) |

### Detail.csv

| Check | Result |
|-------|--------|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All Method values are valid (PARAMETRIC) | PASS |
| Allowance/parametric convention respected (LS items: Qty=1, Unit=LS, UnitRate=Amount) | PASS |
| Row count | 21 lines |
| All Amounts are numeric (no TBD) | PASS |

## S6 — Provenance Discipline

| Metric | Value |
|--------|-------|
| Total priced rows | 21 |
| Rows with non-TBD SourceRef | 21 (100%) |
| Rows with TBD SourceRef | 0 (0%) |
| Provenance completeness | **100%** |

**Top missing-source offenders:** None. All rows have SourceRef populated.

**Note:** While all SourceRefs are populated, several lines use parametric derivations (e.g., LN-007 crane pad uplift, LN-009 gravel placement) where the rate is computed from multiple source inputs rather than a single line item. These derivations are documented in the Notes column.

## S7 — Status Reporting

| Field | Value |
|-------|-------|
| **RUN_STATUS** | **WARNINGS** |
| Reason | All items are priced (0% TBD amounts). However, underlying quantities are derived from conceptual drawings with multiple assumptions. Key uncertainties: cement pad width (south zone), crane pad structural requirements, concrete mix design. These are documented in Summary.md warnings W-001 through W-007. |

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|-------|--------|-------|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS with 7 clearly documented gaps |
| Items.csv reviewed for completeness | PASS | 21 items covering both pad types, earthwork, concrete, gravel, QA, survey, and management |
| Basis-consistency checks pass | PASS | All 21 lines use PARAMETRIC method, consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% SourceRef coverage |
| Scope coverage explicit | PASS | 1 deliverable (DEL-018-04), 2 SOW items (SOW-0078, SOW-0079) covered |
| No writes outside _Estimates/ | PASS | Verified |

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Items Extracted | Missing Documents |
|-------------|---------------|-----------------|-------------------|
| DEL-018-04 | 4/4 (Datasheet, Specification, Guidance, Procedure) | 21 | None |

## Pricing Coverage

| Metric | Value |
|--------|-------|
| Items priced | 21/21 (100%) |
| Items with TBD amount | 0/21 (0%) |
| Total estimated cost | $95,799.00 CAD |

## Basis-Consistency

| Method | Line Count | % of Lines | Amount | % of Amount |
|--------|-----------|------------|--------|-------------|
| PARAMETRIC | 21 | 100% | $95,799.00 | 100% |
| Other methods | 0 | 0% | $0.00 | 0% |

**Conclusion:** 100% method consistency with BASIS_OF_ESTIMATE = PARAMETRIC.

## What to Fix for a Cleaner Rerun

1. **Obtain IFC civil drawings** to replace assumed cement pad dimensions (especially south zone width and east-side pad area).
2. **Obtain crane supplier data** (anchor bolt pattern, base plate dimensions, static/dynamic loads) to refine crane pad structural uplift estimate.
3. **Confirm concrete mix design** (MPa class, reinforcement type) to validate or adjust the $190/m2 parametric rate.
4. **Obtain geotechnical report** to confirm subgrade conditions and required gravel pad depth.
5. **Confirm gravel aggregate supply scope** (CONF-018-04-02): does County supply concrete aggregate in addition to gravel pad fill?
6. **Determine construction season** to confirm or remove cold weather concreting allowance.
