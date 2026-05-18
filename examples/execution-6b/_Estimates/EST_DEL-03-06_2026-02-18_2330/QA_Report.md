# QA Report -- DEL-03-06

**RunID:** EST_DEL-03-06_2026-02-18_2330
**RUN_STATUS: OK**

---

## S1 -- Write Quarantine

**PASS.** All files written under `_Estimates/EST_DEL-03-06_2026-02-18_2330/`. No files outside the estimating tool root were modified.

## S2 -- Snapshot Created

**PASS.** Snapshot folder `EST_DEL-03-06_2026-02-18_2330` exists.

## S3 -- BASIS_OF_ESTIMATE Validated

**PASS.** `RATE_TABLE` is a valid enum value.

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
- [x] Blockers.md (optional; produced)

## S5 -- Detail Schema Integrity

**PASS.**
- Detail.csv contains all 14 required columns: LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes.
- 1 row; Method = `RATE_TABLE` (valid enum).
- No ALLOWANCE or PARAMETRIC rows; convention check not applicable.
- Amount = Qty x UnitRate: 8 x 145 = 1,160. PASS.

## S6 -- Provenance Discipline

**PASS.**
- Provenance completeness: **100%** (1/1 rows have non-TBD SourceRef).
- All SourceRef values point to specific files + row/column identifiers.
- No missing-source offenders.

## S7 -- Status Reporting

**RUN_STATUS = OK**
- All totals are meaningful.
- No critical input gaps.
- No TBD amounts.
- No fallback pricing used.

## S8 -- Operator Acceptance Checklist

| Check | Result |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK |
| Basis-consistency: all Method values match BASIS_OF_ESTIMATE | PASS (1/1 = RATE_TABLE) |
| Provenance completeness reported | 100% |
| Scope coverage explicit | 1 deliverable in scope; 0 excluded; 0 blocked |
| No writes outside _Estimates/ | PASS |

---

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables with priced lines | 1 |
| Deliverables blocked | 0 |
| Deliverables missing | 0 |
| Total line items | 1 |
| Total amount (CAD) | $1,160 |

## Basis-Consistency Check

| Method | Line Count | % of Lines |
|---|---:|---:|
| RATE_TABLE | 1 | 100% |

No method mix. PASS.

## Blocker Summary

- 0 blockers affect estimate pricing.
- 5 PENDING upstream dependencies affect content production only (see Blockers.md).
- 1 external constraint (Alberta Building Code edition TBD) does not affect estimate.

---

## What to Fix for a Cleaner Rerun

Nothing required. This is a clean run with no warnings, no TBDs, and full provenance. No action items.
