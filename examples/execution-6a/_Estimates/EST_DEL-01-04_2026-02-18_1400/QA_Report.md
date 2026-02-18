# QA Report

**RunID:** EST_DEL-01-04_2026-02-18_1400
**RUN_STATUS: WARNINGS**

---

## S1 -- Write Quarantine

**PASS.** All output files written exclusively under `_Estimates/EST_DEL-01-04_2026-02-18_1400/`. No files outside the estimating tool root were modified.

## S2 -- Snapshot Created

**PASS.** Snapshot folder `EST_DEL-01-04_2026-02-18_1400` created under `_Estimates/`.

## S3 -- BASIS_OF_ESTIMATE Validated

**PASS.** `RATE_TABLE` is a valid enum value. Mixed methods authorized by `ALLOW_MIXED_METHODS=TRUE` and `FALLBACK_POLICY=ALLOW_ALLOWANCE`.

## S4 -- Required Artifacts Exist

**PASS.** All required files present:
- [x] Run_Context.md
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv
- [x] Detail.csv (recommended; produced)
- [x] Blockers.md (produced; no critical blockers)

## S5 -- Detail Schema Integrity

**PASS.** Detail.csv contains all 14 required columns: LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes.

- Method values: `RATE_TABLE` (2 rows), `ALLOWANCE` (5 rows). Both are valid enum values.
- Allowance convention check: all ALLOWANCE rows have Qty=1, Unit=LS, UnitRate=Amount. **PASS.**
- Line count: 7 data rows.
- Computed total: $7,000 + $960 + $65,250 + $1,200 + $2,500 + $2,000 + $1,000 = **$79,910 CAD.**
- WBS_CBS_Matrix total: $7,960 + $71,950 = **$79,910 CAD.** Reconciles. **PASS.**

## S6 -- Provenance Discipline

**PASS.** All 7 rows have non-TBD `SourceRef` values pointing to specific files and row/item IDs.

| Metric | Value |
|---|---|
| Total priced rows | 7 |
| Rows with complete SourceRef | 7 |
| Rows with `location TBD` | 0 |
| Provenance completeness | **100%** |

## S7 -- Status Reporting

**RUN_STATUS: WARNINGS**

Rationale for WARNINGS (not OK):
1. Building permit fee (L-03, $65,250) relies on PP-24 which is PARAMETRIC / LOW confidence. The actual Penhold fee schedule is TBD.
2. Development permit fee (L-04, $1,200) confidence is LOW; Penhold fee schedule TBD.
3. All 5 permit fee lines use ALLOWANCE method (not the primary RATE_TABLE method). This is authorized by brief (ALLOW_MIXED_METHODS=TRUE, FALLBACK_POLICY=ALLOW_ALLOWANCE) but represents 90% of the dollar value of the estimate.
4. Permit fees represent 90% of the estimate total; the underlying fee schedules are unconfirmed.

These warnings are bounded and actionable (see "What to fix" below).

## Basis-Consistency Check

| Method | Row Count | Dollar Value | % of Total |
|---|---|---|---|
| RATE_TABLE | 2 | $7,960 | 10.0% |
| ALLOWANCE | 5 | $71,950 | 90.0% |
| **Total** | **7** | **$79,910** | **100%** |

Mixed methods authorized per brief. The dominance of ALLOWANCE by dollar value is expected for a permitting/fees deliverable and is logged in Decision_Log.md (DEC-EST-01).

## Coverage

| Metric | Value |
|---|---|
| In-scope deliverables | 1 (DEL-01-04) |
| Deliverables priced | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |

## Blocker Summary

No critical blockers. Dependency evidence identifies 10 dependency rows (anchors, prerequisites, interfaces, handovers). None block pricing at this stage. See Blockers.md.

---

## What to Fix for a Cleaner Rerun

1. **Obtain Town of Penhold permit fee schedule.** Replace ALLOWANCE lines L-03, L-04 with confirmed fee amounts. This would convert them to RATE_TABLE or QUOTE method and significantly increase confidence.
2. **Confirm total construction value.** PP-24 ($8,700,000) is a rough parametric estimate. Once a firmer construction value is available, rerun to update building permit fee calculation.
3. **Verify whether AEP environmental approval triggers additional fees.** If so, determine which deliverable carries those costs (likely DEL-03-05, not DEL-01-04).
