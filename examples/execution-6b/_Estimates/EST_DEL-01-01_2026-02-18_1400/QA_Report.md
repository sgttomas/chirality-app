# QA Report -- EST_DEL-01-01_2026-02-18_1400

## RUN_STATUS: OK

---

## S1 -- Write Quarantine Respected

- **PASS.** All files written exclusively under `_Estimates/EST_DEL-01-01_2026-02-18_1400/`. No files outside the estimating tool root were modified.

## S2 -- Snapshot Created

- **PASS.** Snapshot folder `EST_DEL-01-01_2026-02-18_1400` exists.

## S3 -- BASIS_OF_ESTIMATE Validated

- **PASS.** `RATE_TABLE` is a valid enum value.

## S4 -- Required Artifacts Exist

- **PASS.** All required files present:
  - [x] Run_Context.md
  - [x] Summary.md
  - [x] QA_Report.md
  - [x] Source_Index.md
  - [x] Decision_Log.md
  - [x] Assumptions_Log.md
  - [x] WBS_CBS_Matrix.csv
  - [x] Detail.csv (recommended; produced)

## S5 -- Detail Schema Integrity

- **PASS.** `Detail.csv` contains all 14 required columns:
  - LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- **Method values:** 1 row, all `RATE_TABLE` -- valid.
- **Allowance/parametric convention:** Not applicable (no ALLOWANCE or PARAMETRIC rows).
- **Arithmetic check:** 8 (Qty) x 105 (UnitRate) = 840 (Amount) -- correct.

## S6 -- Provenance Discipline

- **PASS.** Provenance completeness: **100%** (1 of 1 priced rows have non-TBD SourceRef).
- **Top missing-source offenders:** None.
- SourceRef for L-001: `Level_of_Effort.csv row DEL-01-01/R-22 + Professional_Staff_Rates.csv row R-22`

## S7 -- Status Reporting

- **RUN_STATUS: OK**
- Totals are meaningful; no critical input gaps.
- All quantities and rates sourced from provided PRICE_SOURCES files.

## S8 -- Operator Acceptance Checklist

| Check | Status |
|---|---|
| RUN_STATUS is OK or bounded WARNINGS | OK |
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
| Deliverables missing/blocked | 0 |
| Total line items | 1 |
| Total amount (CAD) | $840 |

## Basis-Consistency Check

| Method | Count | Percentage |
|---|---|---|
| RATE_TABLE | 1 | 100% |

- **PASS.** All methods match `BASIS_OF_ESTIMATE = RATE_TABLE`. No mixed methods.

## Dependency/Blocker Summary

- Dependencies.csv loaded: 18 rows.
- Blocking dependencies: 0.
- No blockers identified that would prevent meaningful estimation.

## What to Fix for a Cleaner Rerun

- Nothing. This run is clean with full provenance, no TBDs, and no blockers.
