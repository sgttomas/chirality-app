# QA Report -- EST_DEL-09-01_2026-02-18_2200

## RUN_STATUS: OK

---

## S1 -- Write Quarantine

| Check | Result |
|---|---|
| All files written under `_Estimates/EST_DEL-09-01_2026-02-18_2200/` | PASS |
| No files modified outside `_Estimates/` | PASS |

## S2 -- Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists: `EST_DEL-09-01_2026-02-18_2200/` | PASS |

## S3 -- BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = `RATE_TABLE` | PASS (valid enum) |

## S4 -- Required Artifacts Exist

| Artifact | Status |
|---|---|
| `Run_Context.md` | PRESENT |
| `Summary.md` | PRESENT |
| `QA_Report.md` | PRESENT (this file) |
| `Source_Index.md` | PRESENT |
| `Decision_Log.md` | PRESENT |
| `Assumptions_Log.md` | PRESENT |
| `WBS_CBS_Matrix.csv` | PRESENT |
| `Detail.csv` | PRESENT |
| `Scope_Resolved.csv` | PRESENT |
| `Blockers.md` | PRESENT |

## S5 -- Detail Schema Integrity

| Check | Result |
|---|---|
| Detail.csv is parseable CSV | PASS |
| All required columns present (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (all = RATE_TABLE) | PASS |
| No ALLOWANCE or PARAMETRIC convention rows (none needed) | PASS |
| Qty * UnitRate = Amount for all rows | PASS (20*130=2600; 8*175=1400; 4*155=620) |
| Sum of line amounts = $4,620 | PASS |

## S6 -- Provenance Discipline

| Check | Result |
|---|---|
| Rows with non-TBD SourceRef | 3 / 3 (100%) |
| Top missing-source offenders | None |
| All SourceRef values reference PS-01 (rates) and PS-02 (hours) with specific row numbers | PASS |

## S7 -- Status Determination

| Criterion | Assessment |
|---|---|
| Totals are meaningful | YES -- all 3 line items fully priced |
| Critical input gaps | NONE |
| TBD amounts | 0 |
| Material assumptions | 6 (all documented; none critical) |
| **RUN_STATUS** | **OK** |

## S8 -- Operator Acceptance Checklist

| Check | Result | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK | No gaps |
| Basis-consistency: all Methods match BASIS_OF_ESTIMATE | PASS | All 3 lines = RATE_TABLE; ALLOW_MIXED_METHODS=FALSE respected |
| Provenance completeness reported | PASS | 100% (3/3 rows have SourceRef) |
| Scope coverage explicit | PASS | 1 deliverable in scope, 1 estimated, 0 excluded, 0 blocked |
| No writes outside _Estimates/ | PASS | All 10 files under snapshot folder |

## Coverage Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables estimated | 1 |
| Deliverables blocked | 0 |
| Deliverables excluded | 0 |
| Total line items | 3 |
| Total hours | 32 |
| Total amount (CAD) | $4,620 |
| Provenance completeness | 100% |
| TBD amounts | 0 |
| Warnings | 0 |
| Blockers (for estimation) | 0 |

## What to Fix for a Cleaner Rerun

Nothing. This is a clean run with no warnings, no TBDs, and full provenance. All inputs were available and sufficient.
