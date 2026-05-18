# QA Report — EST_DEL-001-04_2026-02-27_0840

**RUN_STATUS: OK**

---

## S1 — Write Quarantine Respected

- **PASS.** All output files written exclusively under `_Estimates/EST_DEL-001-04_2026-02-27_0840/`. No files outside the estimating tool root were modified.

## S2 — Snapshot Created

- **PASS.** Snapshot folder `EST_DEL-001-04_2026-02-27_0840` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

- **PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | Present |
| Items.csv | Present |
| Detail.csv | Present |
| Summary.md | Present |
| QA_Report.md | Present (this file) |
| Source_Index.md | Present |
| Decision_Log.md | Present |
| Assumptions_Log.md | Present |
| WBS_CBS_Matrix.csv | Present |

- **PASS.** All required artifacts exist.

## S5 — CSV Schema Integrity

### Items.csv

| Check | Status |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to source document and section | PASS (5/5 rows) |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS (all UNIT_RATE) |
| Row count | 5 items |

### Detail.csv

| Check | Status |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid | PASS (all PARAMETRIC) |
| Allowance/parametric convention | N/A — all items are UNIT_RATE with explicit Qty and UnitRate |
| Row count | 5 line items |
| Arithmetic check | PASS — all Amount = Qty x UnitRate |

## S6 — Provenance Discipline

- **Provenance completeness: 100%** (5/5 rows have non-TBD SourceRef).
- Every priced row references both `Level_of_Effort.csv` (for hours) and `Professional_Staff_Rates.csv` (for rates).
- **No missing-source offenders.**

## S7 — Status Reporting

**RUN_STATUS: OK**

- All 5 items are priced with parametric evidence.
- No TBD amounts.
- No critical input gaps.
- Totals are meaningful.

## S8 — Operator Acceptance Checklist

| Check | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK |
| Items.csv reviewed for completeness | 5 items covering all assigned roles for DEL-001-04 |
| Basis-consistency checks pass | PASS — all methods are PARAMETRIC, matching BASIS_OF_ESTIMATE |
| Provenance completeness reported | 100% |
| Scope coverage explicit | 1 deliverable in scope; 1 deliverable estimated; 0 excluded |
| No writes outside _Estimates/ | Confirmed |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 5 |
| Items priced in Detail.csv | 5 |
| Items with TBD amount | 0 |
| Pricing coverage | 100% |

## Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Documents read | 5 (CONTEXT + Datasheet + Specification + Guidance + Procedure) |
| Missing documents | 0 |
| Items extracted | 5 |

## Warnings (non-blocking)

- **W-001:** LOE allocation is uniform across all PKG-001 Drawing Set deliverables. Building Sections may warrant differentiated effort given its coordination complexity (service pit, mezzanine, crane clearance). Parametric model does not differentiate.
- **W-002:** All hourly rates carry MEDIUM confidence. Actual rates may differ from the parametric assumptions.

## What to Fix for a Cleaner Rerun

1. If actual negotiated staff rates become available, replace Professional_Staff_Rates.csv with confirmed rates (would raise confidence from MEDIUM to HIGH).
2. If differentiated LOE by drawing complexity becomes available, update Level_of_Effort.csv with deliverable-specific hour allocations for DEL-001-04.
