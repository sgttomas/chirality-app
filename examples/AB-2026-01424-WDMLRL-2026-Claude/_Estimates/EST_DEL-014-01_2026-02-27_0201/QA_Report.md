# QA_Report.md — EST_DEL-014-01_2026-02-27_0201

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and all 22 line items are priced (no TBD amounts). However, material TBDs remain in the engineering documents (tank type, tank material, pump type, pipe material, freeze protection method), the dominant cost item (cistern vessel) has LOW confidence with a wide variance band ($42K-$95K), and no vendor quotes have been obtained. The estimate provides a parametric baseline suitable for budgeting but requires quote replacement for key items before finalizing.

---

## S1 — Write Quarantine Respected

**PASS.** All output files written exclusively to `_Estimates/EST_DEL-014-01_2026-02-27_0201/`. No files outside the estimating tool root were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-014-01_2026-02-27_0201` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` is a valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts created:
- [x] Run_Context.md
- [x] Items.csv (22 rows)
- [x] Detail.csv (22 rows)
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv (7 CBS categories + total row)

## S5 — CSV Schema Integrity

### Items.csv
**PASS.**
- Columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes
- 22 rows; all rows have valid PricingMode (UNIT_RATE or LUMP_SUM)
- All rows trace to a source document (Datasheet, Specification, or Procedure) and section
- No TBD quantities (all quantified or set to 1/LS for lump sums)

### Detail.csv
**PASS.**
- Columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- 22 rows; all Method values valid (PARAMETRIC or ALLOWANCE)
- Allowance convention respected: DET-001 (ALLOWANCE) has Qty=1, Unit=EA, UnitRate=Amount=65000
- All amounts are numeric (no TBDs)

## S6 — Provenance Discipline

**PASS with notes.**
- **Provenance completeness: 100%** — all 22 rows have a non-TBD SourceRef.
- 1 row (DET-001) references a specific price source file and item ID (UU-05).
- 6 rows (DET-015 through DET-020) reference specific price source files (Professional_Staff_Rates.csv + Level_of_Effort.csv).
- 2 rows (DET-021, DET-022) reference Construction_Labour_Rates.csv > T-05.
- 13 rows reference parametric estimates with described basis but no external file line item.

**Top provenance gaps (items with weakest source backing):**
1. DET-002 (Distribution pump, $8,500) — parametric estimate with no price source file reference
2. DET-003 (Distribution piping, $12,000) — adapted from UU-01 rate with parametric adjustment
3. DET-008 (Freeze protection, $5,000) — parametric allowance with no price source file reference

## S7 — Status Reporting

**RUN_STATUS = WARNINGS**

Summary of status determination:
- All 22 items priced (0 TBD amounts) — supports meaningful totals
- 1 of 22 lines uses ALLOWANCE method (DET-001: cistern vessel, $65,000)
- 21 of 22 lines use PARAMETRIC method
- Dominant cost item (52.6% of total) has LOW confidence
- Multiple engineering TBDs remain in source documents (tank type, material, pump type, pipe material)
- No vendor quotes obtained
- Water quality classification unresolved (4 conflict table items in Guidance)

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS; gaps are bounded and identified |
| Items.csv reviewed for completeness | PASS | 22 items covering all identified priceable scope from 4 documents |
| Basis-consistency checks | PASS | Mixed methods (PARAMETRIC + ALLOWANCE) permitted by ALLOW_MIXED_METHODS=TRUE |
| Provenance completeness reported | PASS | 100% non-TBD SourceRef; top gaps identified |
| Scope coverage explicit | PASS | 1 deliverable (DEL-014-01); in-scope and out-of-scope clearly defined in Specification |
| No writes outside _Estimates/ | PASS | Verified |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Documents Missing | Items Extracted |
|---|---|---|---|
| DEL-014-01 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | 0 | 22 |

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 22 |
| Items priced (non-TBD amount) | 22 (100%) |
| Items with TBD amount | 0 (0%) |
| Lines with PARAMETRIC method | 21 (95.5%) |
| Lines with ALLOWANCE method | 1 (4.5%) |

## What to Fix for a Cleaner Rerun

1. **Obtain vendor quote for 50,000L cistern vessel** — replace UU-05 allowance ($65,000) with an actual supplier quote. This is the highest-impact improvement (52.6% of total cost).
2. **Resolve tank type and material** — above-grade vs below-grade, HDPE vs concrete vs fiberglass vs steel. This decision changes procurement, structural requirements, and installation method.
3. **Obtain vendor quote for distribution pump** — replace $8,500 parametric estimate with manufacturer's pricing for the selected pump type and motor configuration.
4. **Confirm pipe material and obtain IFC routing lengths** — replace $12,000 parametric piping estimate with measured quantities from IFC plumbing drawings.
5. **Resolve water quality classification** (CONF-014-01-01, CONF-014-01-02) — potable vs non-potable determination may add treatment, testing, and additional backflow prevention costs.
6. **Confirm freeze protection method** — IFC plumbing design to specify insulation class and heat trace requirements; replace $5,000 parametric allowance.
7. **Resolve emergency shower feed source** (CONF-014-01-03) — if cistern feeds emergency shower, add corresponding distribution piping and code compliance scope.
8. **Add PRICE_SOURCES for plumbing-specific items** — interior piping rate table, plumbing fixture/fitting pricing, permit fee schedule.
