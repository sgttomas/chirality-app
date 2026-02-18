# QA Report

**RunID:** EST_DEL-02-05_2026-02-18_2200
**RUN_STATUS: OK**

---

## S1 -- Write Quarantine Respected

**PASS.** All files written under `_Estimates/EST_DEL-02-05_2026-02-18_2200/`. No files outside `_Estimates/` were modified.

---

## S2 -- Snapshot Created

**PASS.** Snapshot folder `EST_DEL-02-05_2026-02-18_2200` created under `_Estimates/`.

---

## S3 -- BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = RATE_TABLE` -- valid enum value.

---

## S4 -- Required Artifacts Exist

**PASS.** All required files present:
- [x] Run_Context.md
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv
- [x] Detail.csv (recommended; included)
- [x] Blockers.md (included; no blockers found)

---

## S5 -- Detail Schema Integrity

**PASS.**
- Detail.csv contains all 14 required columns: LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- 2 data rows, both with `Method = RATE_TABLE` (valid enum)
- No ALLOWANCE or PARAMETRIC rows, so convention check is N/A
- Amount computation verified: L-0205-01: 16 x 155 = 2,480; L-0205-02: 8 x 125 = 1,000; Total: 3,480

---

## S6 -- Provenance Discipline

**PASS.**
- **Provenance completeness: 100%** (2/2 rows have non-TBD SourceRef)
- Both rows reference specific files and row identifiers:
  - L-0205-01: Level_of_Effort.csv row DEL-02-05/R-13 + Professional_Staff_Rates.csv row R-13
  - L-0205-02: Level_of_Effort.csv row DEL-02-05/R-14 + Professional_Staff_Rates.csv row R-14
- No `location TBD` entries.

---

## S7 -- Status Reporting

**RUN_STATUS: OK**
- All line items priced from basis evidence.
- No TBD amounts.
- No critical input gaps.
- Totals are meaningful.

---

## S8 -- Operator Acceptance Checklist

| Check | Result |
|---|---|
| RUN_STATUS is OK or bounded WARNINGS | OK |
| Basis-consistency: all Method values match BASIS_OF_ESTIMATE | PASS (2/2 = RATE_TABLE) |
| Provenance completeness reported | 100% (2/2 rows) |
| Scope coverage explicit | 1 deliverable in scope; 0 excluded; 0 blocked |
| No writes outside _Estimates/ | PASS |

---

## Coverage Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables with priced lines | 1 |
| Deliverables blocked | 0 |
| Total line items | 2 |
| Lines with TBD amount | 0 |
| Lines with TBD SourceRef | 0 |
| Total hours | 24 |
| Total amount (CAD) | $3,480 |

---

## Basis-Consistency Check

| Method | Count | % |
|---|---|---|
| RATE_TABLE | 2 | 100% |

All methods match `BASIS_OF_ESTIMATE = RATE_TABLE`. No fallback methods used. **PASS.**

---

## Blocker Summary (from dependency evidence)

- 0 blockers identified for estimating purposes.
- 4 upstream information prerequisites exist (DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04) but these affect content production sequencing, not the cost estimate.

---

## What to Fix for a Cleaner Rerun

Nothing. This run produced a clean, fully-sourced estimate. No remediation items.
