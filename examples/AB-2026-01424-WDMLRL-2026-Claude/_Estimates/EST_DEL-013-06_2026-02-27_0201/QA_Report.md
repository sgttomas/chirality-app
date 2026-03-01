# QA Report — EST_DEL-013-06_2026-02-27_0201

## RUN_STATUS: WARNINGS

---

## S1 — Write Quarantine Respected

**PASS.** All output files written exclusively under `{RUN_ROOT}/_Estimates/EST_DEL-013-06_2026-02-27_0201/`. No project truth files were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-013-06_2026-02-27_0201` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` is a valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts produced:
- [x] Run_Context.md
- [x] Items.csv (13 items)
- [x] Detail.csv (13 lines)
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] WBS_CBS_Matrix.csv
- [x] Decision_Log.md
- [x] Assumptions_Log.md

## S5 — CSV Schema Integrity

### Items.csv
**PASS.**
- All 9 required columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes
- 13 rows; all parseable
- PricingMode values: UNIT_RATE (5 rows), LUMP_SUM (8 rows) — all valid
- Lump-sum rows: Qty=1, Unit=LS — convention respected
- All rows have non-empty SourceDoc and SourceSection

### Detail.csv
**PASS.**
- All 14 required columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- 13 rows; all parseable
- Method values: PARAMETRIC (13 rows) — consistent with BASIS_OF_ESTIMATE
- Lump-sum rows (Qty=1, Unit=LS): UnitRate = Amount — convention respected
- Currency: CAD (all rows)
- No TBD amounts — all items priced (parametrically)

## S6 — Provenance Discipline

**PASS (with warnings).**
- 13/13 rows (100%) have non-empty SourceRef
- 8/13 rows (62%) reference specific PRICE_SOURCES files (rates or LOE)
- 5/13 rows (38%) cite "Parametric — [description]; no quote in PRICE_SOURCES"

### Top Missing-Source Offenders

| LineID | Description | SourceRef Issue |
|---|---|---|
| L-01 | HVLS fan units supply ($33,000) | No source file — parametric industry estimate |
| L-02 | Mounting hardware ($6,600) | No source file — parametric industry estimate |
| L-05 | Speed controllers ($2,850) | No source file — parametric industry estimate |
| L-10 | Permits ($1,000) | No source file — parametric fee estimate |
| L-12 | Scaffolding/lift ($2,500) | No source file — parametric rental estimate |

**Total unsourced amount: $45,950 of $70,234.40 (65.4%)**

## S7 — Status Reporting

**RUN_STATUS = WARNINGS**

Rationale:
- Totals are meaningful and represent a complete scope decomposition of DEL-013-06
- Material TBDs exist: fan model/diameter/power; ceiling structure type; control type; acceptance criteria
- 65.4% of total cost lacks PRICE_SOURCES evidence (parametric only)
- Overall confidence is LOW for equipment-dominant items
- No critical input gaps that would make totals meaningless (all items have parametric pricing)
- Status is not FAILED_INPUTS because FALLBACK_POLICY=ALLOW_PARAMETRIC permits parametric pricing
- Status is not OK because >50% of cost is unsourced and multiple design parameters are TBD

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS; gaps are identified and bounded in Summary |
| Items.csv reviewed for completeness | PASS | 13 items covering supply, installation, design, commissioning, documentation, management |
| Basis-consistency checks pass | PASS | All 13 lines use Method=PARAMETRIC, consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 62% sourced; top 5 unsourced offenders listed |
| Scope coverage explicit | PASS | 1 deliverable (DEL-013-06); all 4 documents read; no missing documents |
| No writes outside _Estimates/ | PASS | Verified |

## Quantity Takeoff Coverage

| Document | Items Extracted | Notes |
|---|---|---|
| Datasheet.md | ITEM-01, ITEM-02 | Fan quantity (6); mounting hardware |
| Specification.md | ITEM-05, ITEM-10 | Controls; permits; product certification |
| Guidance.md | ITEM-12 | Elevated access; HVLS selection rationale |
| Procedure.md | ITEM-03, ITEM-04, ITEM-06, ITEM-07, ITEM-08, ITEM-09, ITEM-11 | Installation; design coordination; commissioning; documentation |
| Level_of_Effort.csv | ITEM-13 | Management/supervision hours |

All 4 deliverable documents read and contributing to takeoff. No missing documents.

## What to Fix for a Cleaner Rerun

1. **Obtain HVLS fan quotes** — Add ceiling fan equipment quotes to PRICE_SOURCES (reduces 47% of cost from PARAMETRIC/LOW to QUOTE/HIGH)
2. **Resolve ceiling structure type** (CF-013-06-03) — Determines mounting hardware type and cost
3. **Resolve control type decision** (D-003) — Wall switches vs. centralized panel significantly affects ITEM-05
4. **Add ceiling fan line item to Mechanical_System_Rates.csv** — Currently absent
5. **Confirm HVLS voltage requirement** (B-002) — May invalidate 120V assumption and change electrical scope
6. **Add permit fee schedule to PRICE_SOURCES** — Currently absent
7. **Add scaffolding/equipment rental rates to PRICE_SOURCES** — Currently absent
