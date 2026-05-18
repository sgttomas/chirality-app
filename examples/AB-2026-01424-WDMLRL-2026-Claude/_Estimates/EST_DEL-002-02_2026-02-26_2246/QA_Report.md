# QA Report — EST_DEL-002-02_2026-02-26_2246

## RUN_STATUS: OK

Totals are meaningful. No critical input gaps. All line items are fully priced from parametric sources with complete provenance.

---

## S1 — Write Quarantine Respected

PASS. All outputs written to `_Estimates/EST_DEL-002-02_2026-02-26_2246/`. No files outside the estimating tool root were modified.

## S2 — Snapshot Created

PASS. Snapshot folder `EST_DEL-002-02_2026-02-26_2246` exists.

## S3 — BASIS_OF_ESTIMATE Validated

PASS. `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

## S4 — Required Artifacts Exist

PASS. All required files produced:
- [x] Run_Context.md
- [x] Items.csv
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv
- [x] Detail.csv (recommended; produced)

## S5 — CSV Schema Integrity

### Items.csv

PASS.
- Columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes
- Row count: 4
- All `PricingMode` values are `UNIT_RATE` — valid enum
- All `Qty` values are numeric (no TBD)
- All rows have `SourceDoc` and `SourceSection` populated
- All `DeliverableID` values = `DEL-002-02`

### Detail.csv

PASS.
- Columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- Row count: 4
- All `Method` values are `PARAMETRIC` — valid enum and consistent with `BASIS_OF_ESTIMATE`
- No allowance/parametric convention violations (all items are UNIT_RATE with actual qty/unit/rate)
- All `Amount` values = `Qty x UnitRate` (verified: 84x170=14280, 36x95=3420, 6x165=990, 4x135=540)
- All `Currency` values = `CAD`

## S6 — Provenance Discipline

PASS.
- 4 of 4 Detail.csv rows (100%) have non-TBD `SourceRef` values
- Each `SourceRef` traces to specific rows in Level_of_Effort.csv (hours) and Professional_Staff_Rates.csv (rates)
- No missing-source offenders

### Provenance Completeness

| Metric | Value |
|---|---|
| Total detail lines | 4 |
| Lines with SourceRef | 4 |
| Lines with `location TBD` | 0 |
| Provenance completeness | 100% |

## S7 — Status Reporting

PASS. `RUN_STATUS = OK`.
- All line items priced (0 TBD amounts)
- No critical input gaps
- All sources indexed and traceable
- Basis is consistent (PARAMETRIC throughout)

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or bounded WARNINGS | OK | No warnings |
| Items.csv reviewed for completeness | 4 items extracted across 4 roles | Covers all LOE roles assigned to DEL-002-02 |
| Basis-consistency checks pass | PASS | All methods = PARAMETRIC; matches BASIS_OF_ESTIMATE |
| Provenance completeness reported | 100% | No gaps |
| Scope coverage explicit | 1 deliverable, 1 package, 4 line items | DEL-002-02 only |
| No writes outside _Estimates/ | Confirmed | All output in snapshot folder |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Items Extracted | Missing Documents |
|---|---|---|---|
| DEL-002-02 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | 4 | None |

## Pricing Coverage

| Metric | Value |
|---|---|
| Items in Items.csv | 4 |
| Items priced in Detail.csv | 4 |
| Items with TBD amount | 0 |
| Pricing coverage | 100% |

## Basis Consistency

| Method | Count | % |
|---|---|---|
| PARAMETRIC | 4 | 100% |
| Other | 0 | 0% |

Consistent with `BASIS_OF_ESTIMATE = PARAMETRIC`. No mixed methods required.

---

## What to Fix for a Cleaner Rerun

Nothing required. This run produced a clean, fully-priced estimate with complete provenance. Potential future improvements:

1. **Cross-check against fee-based model.** The Professional_Design_Fees.csv provides a structural design fee of 1.8% (recommended) of construction value. If a construction value estimate for the foundation becomes available, the LOE-based estimate ($19,230 CAD) could be cross-checked against the fee percentage model for reasonableness.

2. **Geotech impact on design hours.** The current LOE assumes normal ground conditions. If geotechnical results (DEL-008-01) reveal unusual conditions, the Structural Engineer hours (84 hr) may need to increase to account for redesign effort. This would require updating the Level_of_Effort.csv source and rerunning.
