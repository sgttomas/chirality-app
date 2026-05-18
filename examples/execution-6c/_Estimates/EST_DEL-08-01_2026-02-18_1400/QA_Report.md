# QA Report -- EST_DEL-08-01_2026-02-18_1400

## RUN_STATUS: OK

Totals are meaningful; no critical input gaps. All line items priced with full provenance.

---

## S1 -- Write Quarantine Respected

**PASS.** All files written exclusively under `_Estimates/EST_DEL-08-01_2026-02-18_1400/`. No project truth files modified.

## S2 -- Snapshot Created

**PASS.** Snapshot folder `EST_DEL-08-01_2026-02-18_1400` created under `_Estimates/`.

## S3 -- BASIS_OF_ESTIMATE Validated

**PASS.** `RATE_TABLE` is a valid enum value.

## S4 -- Required Artifacts Exist

**PASS.** All required artifacts produced:
- [x] Run_Context.md
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv

Optional artifacts also produced:
- [x] Detail.csv
- [x] Blockers.md
- [x] Risk_Register.md
- [x] Run_Brief.md

## S5 -- Detail Schema Integrity

**PASS.**
- Detail.csv is parseable CSV with all 14 required columns present.
- 3 data rows; all pass validation.
- `Method` values: all `RATE_TABLE` -- valid enum.
- No ALLOWANCE or PARAMETRIC rows, so convention check is N/A.
- Column inventory: LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes -- **all present**.

## S6 -- Provenance Discipline

**PASS.**
- 3/3 priced rows (100%) have non-TBD SourceRef.
- Each SourceRef cites both the rate table row and the LOE row.
- 0 rows with `location TBD`.
- Top missing-source offenders: none.

## S7 -- Status Reporting

**PASS.** `RUN_STATUS = OK` declared. Justification:
- All line items priced with complete basis evidence.
- No TBD amounts.
- No fallback methods used.
- No critical input gaps.

## S8 -- Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or bounded WARNINGS | OK | |
| Basis-consistency checks pass | PASS | All 3 lines use RATE_TABLE; matches BASIS_OF_ESTIMATE |
| Provenance completeness reported | 100% | 3/3 lines with full SourceRef |
| Scope coverage explicit | 1 in-scope, 0 excluded, 0 blocked | |
| No writes outside _Estimates/ | Confirmed | |

---

## Detailed Checks

### Schema Validation (Detail.csv)

| Column | Present | Valid |
|---|---|---|
| LineID | Yes | 3 unique values (L-08-01-001 through L-08-01-003) |
| CBS | Yes | 3 values: PROF-SCHED, PROF-PM, PROF-CM |
| WBS_PackageID | Yes | All PKG-08 |
| WBS_DeliverableID | Yes | All DEL-08-01 |
| Description | Yes | Non-empty for all rows |
| Qty | Yes | 20, 8, 4 (all numeric, non-zero) |
| Unit | Yes | All "hr" |
| UnitRate | Yes | 130, 175, 155 (all numeric, non-zero) |
| Amount | Yes | 2600, 1400, 620 (computed: Qty x UnitRate) |
| Currency | Yes | All CAD |
| Method | Yes | All RATE_TABLE (valid enum) |
| SourceRef | Yes | All non-TBD |
| Confidence | Yes | All MED (valid enum) |
| Notes | Yes | Non-empty for all rows |

### Arithmetic Verification

| LineID | Qty x UnitRate | Amount | Match |
|---|---:|---:|---|
| L-08-01-001 | 20 x 130 = 2,600 | 2,600 | Yes |
| L-08-01-002 | 8 x 175 = 1,400 | 1,400 | Yes |
| L-08-01-003 | 4 x 155 = 620 | 620 | Yes |
| **TOTAL** | | **4,620** | Yes |

### Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables covered (at least 1 priced line) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Total priced lines | 3 |
| Total TBD-amount lines | 0 |

### Basis Consistency

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| Methods used | RATE_TABLE (3/3 lines) |
| Mixed methods detected | No |
| ALLOW_MIXED_METHODS | FALSE |
| Consistency | PASS -- 100% alignment |

### Blocker Summary (from dependency evidence)

| Category | Count |
|---|---|
| ANCHOR dependencies (ACTIVE) | 3 |
| EXECUTION dependencies (ACTIVE) | 8 |
| PREREQUISITE (upstream) | 3 (DEL-02-01, DEL-04-01, DEL-09-02) |
| INTERFACE (upstream) | 4 (DEL-05-01, DEL-05-02, DEL-06-01, DEL-09-01) |
| HANDOVER (downstream) | 1 (DEL-01-02) |
| All SatisfactionStatus = PENDING | Yes |

These are **content coordination** dependencies, not pricing blockers. The estimate (proposal production cost) can proceed regardless of whether upstream deliverables are complete, because the effort to produce DEL-08-01 is independent of the content it will contain.

---

## What to Fix for a Cleaner Rerun

No fixes needed. This is a clean run with RUN_STATUS = OK. For future improvement:
1. If actual firm hourly rates become available, replace MARKET-based rates in Professional_Staff_Rates.csv and re-run.
2. If effort estimates are refined post-production, update Level_of_Effort.csv and re-run.
