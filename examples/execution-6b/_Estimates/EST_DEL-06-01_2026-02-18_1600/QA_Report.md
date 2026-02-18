# QA Report

**RunID:** EST_DEL-06-01_2026-02-18_1600
**RUN_STATUS: OK**

---

## S1 -- Write Quarantine Respected

PASS. All files written exclusively under `_Estimates/EST_DEL-06-01_2026-02-18_1600/`. No project truth files modified.

## S2 -- Snapshot Created

PASS. Snapshot folder `EST_DEL-06-01_2026-02-18_1600` created under `_Estimates/`.

## S3 -- BASIS_OF_ESTIMATE Validated

PASS. `RATE_TABLE` is a valid enum value.

## S4 -- Required Artifacts Exist

PASS. All required files present:
- [x] Run_Context.md
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv
- [x] Detail.csv (optional but produced)
- [x] Blockers.md (optional but produced)

## S5 -- Detail Schema Integrity

PASS.
- Detail.csv contains all 14 required columns: LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes.
- All `Method` values = `RATE_TABLE` (valid enum).
- No ALLOWANCE or PARAMETRIC lines present, so allowance/parametric convention does not apply.
- Row count: 2.
- Arithmetic check: L-0601-01: 10 x 165 = 1650 (PASS); L-0601-02: 4 x 175 = 700 (PASS).
- Total: 1650 + 700 = 2350 (matches WBS_CBS_Matrix Amount_Total). PASS.

## S6 -- Provenance Discipline

PASS.
- Provenance completeness: **100%** (2/2 rows have non-TBD SourceRef).
- All SourceRef values cite specific source files and row identifiers.
- No `location TBD` entries.

## S7 -- Status Reporting

**RUN_STATUS: OK**
- Totals are meaningful ($2,350 CAD).
- No critical input gaps.
- No TBD amounts.
- No missing provenance.

## S8 -- Operator Acceptance Checklist

| Check | Result |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK |
| Basis-consistency: all Method values match BASIS_OF_ESTIMATE | PASS (2/2 = RATE_TABLE) |
| Provenance completeness reported | 100% |
| Scope coverage explicit | 1 deliverable in scope; 0 excluded; 0 blocked |
| No writes outside _Estimates/ | PASS |

---

## Coverage Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables priced | 1 |
| Deliverables blocked | 0 |
| Deliverables with TBD amounts | 0 |
| Total line items | 2 |
| Lines with SourceRef | 2 (100%) |
| Lines with TBD SourceRef | 0 |
| Method consistency | 2/2 RATE_TABLE (100%) |
| Blocker count (from dependencies) | 0 |

---

## What to Fix for a Cleaner Rerun

Nothing. This run is clean. All inputs were available and all line items are fully priced with complete provenance.

Optional improvements for future runs:
- Consider whether Assumed_Project_Parameters.csv should inform any parametric cross-check of the estimate total against project value benchmarks.
- Rate confidence is MEDIUM across all roles; obtaining confirmed rates would increase confidence to HIGH.
