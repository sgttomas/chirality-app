# QA Report -- EST_DEL-10-02_2026-02-18_1900

## RUN_STATUS: OK

---

## S1 -- Write Quarantine

| Check | Result |
|---|---|
| All outputs written under `_Estimates/EST_DEL-10-02_2026-02-18_1900/` | PASS |
| No files modified outside `_Estimates/` | PASS |

## S2 -- Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists: `EST_DEL-10-02_2026-02-18_1900/` | PASS |

## S3 -- BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| `BASIS_OF_ESTIMATE=RATE_TABLE` is a valid enum value | PASS |

## S4 -- Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Detail.csv | PRESENT |

## S5 -- Detail Schema Integrity

| Check | Result |
|---|---|
| Detail.csv is parseable CSV | PASS |
| All required columns present (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values are valid (`RATE_TABLE` x3) | PASS |
| No ALLOWANCE/PARAMETRIC rows requiring LS convention | N/A (all rows are RATE_TABLE with hr units) |
| Amount = Qty x UnitRate for all rows | PASS (L-001: 8x175=1400; L-002: 6x155=930; L-003: 4x155=620) |

## S6 -- Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows | 3 |
| Rows with non-TBD SourceRef | 3 |
| Provenance completeness | **100%** |
| Top missing-source offenders | None |

All 3 line items reference specific rows in Level_of_Effort.csv (for hours) and Professional_Staff_Rates.csv (for rates).

## S7 -- Status Reporting

| Check | Result |
|---|---|
| Totals are meaningful | PASS ($2,950 CAD fully substantiated) |
| No critical input gaps | PASS |
| No TBD amounts | PASS |
| RUN_STATUS | **OK** |

## S8 -- Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK |
| Basis-consistency: all Method values match BASIS_OF_ESTIMATE (RATE_TABLE) | PASS (3/3 = RATE_TABLE) |
| Provenance completeness reported | PASS (100%) |
| Scope coverage explicit | PASS (1 deliverable in scope; 1 estimated; 0 excluded; 0 blocked) |
| No writes outside `_Estimates/` | PASS |

---

## Coverage Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-10-02) |
| Deliverables estimated | 1 |
| Deliverables excluded | 0 |
| Deliverables blocked | 0 |
| Line items produced | 3 |
| Total estimated amount | $2,950 CAD |

---

## What to Fix for a Cleaner Rerun

Nothing. This run is clean. All inputs were available and complete. No TBDs, no fallbacks, no warnings.

If rates or hours change in the price sources, a rerun with identical brief parameters will produce updated totals automatically.
