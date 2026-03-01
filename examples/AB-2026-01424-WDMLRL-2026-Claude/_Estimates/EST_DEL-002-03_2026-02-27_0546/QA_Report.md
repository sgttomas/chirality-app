# QA Report — EST_DEL-002-03_2026-02-27_0546

## RUN_STATUS: OK

Totals are meaningful; no critical input gaps. All line items priced with PARAMETRIC method consistent with BASIS_OF_ESTIMATE.

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All files written under _Estimates/ only | PASS |
| No modifications to deliverable content, lifecycle files, decomposition, or dependency registers | PASS |

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder EST_DEL-002-03_2026-02-27_0546 exists | PASS |

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = PARAMETRIC | PASS (valid enum value) |

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
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
|---|---|
| Parseable CSV | PASS |
| Required columns (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS — all 9 columns present |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS — 4 UNIT_RATE, 3 LUMP_SUM |
| Every row traces to a source document and section | PASS — 7/7 rows have SourceDoc and SourceSection |
| No TBD quantities | PASS — all Qty values are numeric |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS — all 15 columns present |
| Method values valid | PASS — all 7 rows are PARAMETRIC |
| Allowance/parametric convention for LS items | PASS — LS items (L-005, L-006, L-007) have Qty=1, Unit=LS, UnitRate=Amount=0 (zero-incremental cost items included in other lines) |
| All amounts are numeric (no TBD) | PASS |

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows (Amount > 0) | 4 |
| Rows with non-TBD SourceRef | 4 |
| Provenance completeness (priced rows) | **100%** |
| Total rows (including zero-incremental) | 7 |
| Rows with non-TBD SourceRef (all) | 7 |
| Provenance completeness (all rows) | **100%** |
| Top missing-source offenders | None |

## S7 — Status Reporting

| Field | Value |
|---|---|
| RUN_STATUS | **OK** |
| Justification | All items priced; 100% provenance completeness; no TBD amounts; method consistency with PARAMETRIC basis; no critical input gaps. |

## S8 — Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (OK) |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS — 7 items extracted from Procedure, Specification, and Datasheet covering all production activities |
| Basis-consistency checks pass | PASS — all methods are PARAMETRIC, matching BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS — 100% |
| Scope coverage explicit | PASS — 1 deliverable (DEL-002-03); all 4 documents read; no missing documents |
| No writes outside _Estimates/ | PASS |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Documents Missing | Items Extracted |
|---|---|---|---|
| DEL-002-03 | Datasheet.md, Specification.md, Guidance.md, Procedure.md | None | 7 |

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 7 |
| Items priced (Amount > 0 in Detail.csv) | 4 |
| Items with zero incremental cost (included in other lines) | 3 |
| Items with TBD amounts | 0 |
| Pricing coverage | **100%** |

## Basis-Consistency Check

| Metric | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Lines with Method=PARAMETRIC | 7/7 (100%) |
| Lines with other methods | 0 |
| Basis consistency | **PASS** |

## What to Fix for a Cleaner Rerun

1. No material issues identified. This is a clean run.
2. If higher confidence is desired, obtain actual structural engineering firm fee quotes to replace parametric LOE with QUOTE method.
3. Consider whether 84 hours for Structural Engineer is adequate for a complex industrial building with crane runways, mezzanine, and service pit framing. The parametric LOE is MEDIUM confidence (+/-20-30%). An actual time study or firm-specific estimate could improve confidence.
