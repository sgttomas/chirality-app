# QA Report -- EST_DEL-02-04_2026-02-18_2200

## RUN_STATUS: OK

Totals are meaningful; no critical input gaps.

---

## S1 -- Write Quarantine Respected

- **PASS.** All files written exclusively under `test/execution-6b/_Estimates/EST_DEL-02-04_2026-02-18_2200/`.
- No project truth files modified.

## S2 -- Snapshot Created

- **PASS.** Snapshot folder `EST_DEL-02-04_2026-02-18_2200` created.

## S3 -- BASIS_OF_ESTIMATE Validated

- **PASS.** `RATE_TABLE` is a valid enum value.

## S4 -- Required Artifacts Exist

- **PASS.** All required files present:
  - Run_Context.md
  - Summary.md
  - QA_Report.md
  - Source_Index.md
  - Decision_Log.md
  - Assumptions_Log.md
  - WBS_CBS_Matrix.csv
  - Detail.csv (recommended; included)

## S5 -- Detail Schema Integrity

- **PASS.** Detail.csv contains all 14 required columns.
- **PASS.** Method values: all `RATE_TABLE` (valid enum).
- **PASS.** No allowance/parametric rows present (convention check N/A).
- **PASS.** 2 data rows; all parseable.

### Column Verification

| Column | Present | Valid |
|---|---|---|
| LineID | YES | YES (L-0204-01, L-0204-02) |
| CBS | YES | YES (DESIGN_SERVICES) |
| WBS_PackageID | YES | YES (PKG-002) |
| WBS_DeliverableID | YES | YES (DEL-02-04) |
| Description | YES | YES |
| Qty | YES | YES (16, 8) |
| Unit | YES | YES (hr, hr) |
| UnitRate | YES | YES (160, 130) |
| Amount | YES | YES (2560, 1040) |
| Currency | YES | YES (CAD) |
| Method | YES | YES (RATE_TABLE) |
| SourceRef | YES | YES (non-TBD) |
| Confidence | YES | YES (MED) |
| Notes | YES | YES |

## S6 -- Provenance Discipline

- **PASS.** 2/2 priced rows have non-TBD SourceRef (100% provenance completeness).
- **Top missing-source offenders:** None.
- Each SourceRef traces to specific rows in Level_of_Effort.csv and Professional_Staff_Rates.csv.

## S7 -- Status Reporting

- **PASS.** RUN_STATUS = OK declared in this report and in Summary.md.

## S8 -- Operator Acceptance Checklist

| Check | Result |
|---|---|
| RUN_STATUS is OK or bounded WARNINGS | OK |
| Basis-consistency: all Method values match BASIS_OF_ESTIMATE | PASS (all RATE_TABLE) |
| Provenance completeness reported | PASS (100%) |
| Scope coverage explicit | PASS (1 deliverable in scope; 1 covered; 0 missing; 0 blocked) |
| No writes outside _Estimates/ | PASS |

---

## Coverage Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables covered (priced) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Total line items | 2 |
| Priced line items | 2 |
| TBD line items | 0 |
| Total hours | 24 |
| Total amount (CAD) | $3,600 |

## Basis-Consistency Check

- BASIS_OF_ESTIMATE = RATE_TABLE
- All Detail.csv Method values = RATE_TABLE
- **PASS.** No method mixing detected.
- ALLOW_MIXED_METHODS = FALSE; no violations.

## Dependency / Blocker Summary

- Dependencies.csv loaded: 13 rows (4 anchor, 9 execution).
- 3 upstream execution prerequisites identified (DEL-02-01, DEL-02-02, DEL-02-03): informational for production sequencing.
- 0 blockers to pricing (hours and rates are available regardless of upstream deliverable status).

## Arithmetic Verification

| LineID | Qty | UnitRate | Expected Amount | Actual Amount | Check |
|---|---|---|---|---|---|
| L-0204-01 | 16 | 160 | 2,560 | 2,560 | PASS |
| L-0204-02 | 8 | 130 | 1,040 | 1,040 | PASS |
| **Total** | | | **3,600** | **3,600** | **PASS** |

## What to Fix for a Cleaner Rerun

- Nothing. This run is clean. All inputs present, all lines priced, all provenance complete.
