# QA Report

**RunID:** EST_DEL-07-05_2026-02-18_2359
**Date:** 2026-02-18

---

## RUN_STATUS: OK

Totals are meaningful; no critical input gaps.

---

## S1 -- Write Quarantine Respected

**PASS.** All files written under `test/execution-6b/_Estimates/EST_DEL-07-05_2026-02-18_2359/`. No files outside `_Estimates/` modified.

## S2 -- Snapshot Created

**PASS.** Snapshot folder `EST_DEL-07-05_2026-02-18_2359` created.

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

Optional files also produced:
- [x] Detail.csv
- [x] Blockers.md
- [x] Run_Brief.md

## S5 -- Detail Schema Integrity

**PASS.**
- Detail.csv contains all 14 required columns: LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes.
- 2 data rows; both parseable.
- Method values: both `RATE_TABLE` -- valid enum.
- No ALLOWANCE or PARAMETRIC lines present, so allowance/parametric convention check is N/A.
- Amounts verified: 8 x 130 = 1040; 4 x 175 = 700. Total = 1740. Matches WBS_CBS_Matrix.csv.

## S6 -- Provenance Discipline

**PASS.**
- Provenance completeness: **100%** (2/2 rows have non-TBD SourceRef).
- L-0705-01: SourceRef = Level_of_Effort.csv row DEL-07-05 R-23 + Professional_Staff_Rates.csv R-23.
- L-0705-02: SourceRef = Level_of_Effort.csv row DEL-07-05 R-02 + Professional_Staff_Rates.csv R-02.
- No missing-source offenders.

## S7 -- Status Reporting

**PASS.** RUN_STATUS = OK declared above.

## S8 -- Operator Acceptance Checklist

| Check | Result |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK |
| Basis-consistency: all Method values match BASIS_OF_ESTIMATE | PASS -- both lines are RATE_TABLE |
| Provenance completeness reported | PASS -- 100% |
| Scope coverage explicit | PASS -- 1 deliverable in scope, 1 covered, 0 excluded, 0 blocked |
| No writes outside _Estimates/ | PASS |

---

## Coverage Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables covered (priced) | 1 |
| Deliverables excluded | 0 |
| Deliverables blocked | 0 |
| Total line items | 2 |
| Total hours | 12 |
| Total amount (CAD) | $1,740 |

## Basis-Consistency Check

| Method | Line Count | Consistent with BASIS_OF_ESTIMATE? |
|---|---|---|
| RATE_TABLE | 2 | YES |

No mixed methods. ALLOW_MIXED_METHODS = FALSE constraint satisfied.

## Blocker Summary

| Source | Blockers Found |
|---|---|
| Dependencies.csv (13 ACTIVE rows) | 0 estimate-blocking dependencies |

3 upstream prerequisites (DEL-07-01, DEL-07-03, DEL-06-02) have TBD satisfaction status but do not block cost estimation.

## What to Fix for a Cleaner Rerun

Nothing. This run produced a clean snapshot with:
- Full scope coverage (1/1 deliverables priced)
- Full provenance (100% SourceRef populated)
- Full basis consistency (100% RATE_TABLE)
- No blockers, no TBD amounts, no warnings
