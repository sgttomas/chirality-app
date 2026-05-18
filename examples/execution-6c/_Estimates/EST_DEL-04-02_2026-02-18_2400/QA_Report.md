# QA Report -- EST_DEL-04-02_2026-02-18_2400

## RUN_STATUS: OK

All inputs resolved. Totals are meaningful. No critical input gaps.

---

## S1 -- Write Quarantine

**PASS.** All outputs written exclusively under `_Estimates/EST_DEL-04-02_2026-02-18_2400/`. No files outside the estimating tool root were modified.

## S2 -- Snapshot Created

**PASS.** Snapshot folder `EST_DEL-04-02_2026-02-18_2400` created under `_Estimates/`.

## S3 -- BASIS_OF_ESTIMATE Validated

**PASS.** `RATE_TABLE` is a valid enum value. Confirmed against BOE document (BASIS_OF_ESTIMATE.md Section 4, PKG-06 table, DEL-04-02 row).

## S4 -- Required Artifacts Exist

**PASS.** All required files present:

| File | Status |
|---|---|
| Run_Context.md | Present |
| Summary.md | Present |
| QA_Report.md | Present (this file) |
| Source_Index.md | Present |
| Decision_Log.md | Present |
| Assumptions_Log.md | Present |
| WBS_CBS_Matrix.csv | Present |
| Detail.csv | Present (optional but recommended; included) |
| Blockers.md | Present (optional; included) |
| Run_Brief.md | Present (optional; included) |

## S5 -- Detail Schema Integrity

**PASS.**

| Check | Result |
|---|---|
| CSV parseable | Yes |
| All required columns present | Yes (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Method values valid | Yes (all = RATE_TABLE) |
| Allowance/parametric convention | N/A (no ALLOWANCE or PARAMETRIC lines) |
| Row count | 2 |
| Arithmetic check (Qty x UnitRate = Amount) | L-01: 8 x 175 = 1400 PASS; L-02: 4 x 155 = 620 PASS |
| Sum check | 1400 + 620 = 2020 PASS (matches WBS_CBS_Matrix total) |
| Currency consistent | Yes (all CAD) |

## S6 -- Provenance Discipline

**PASS.** 100% provenance completeness.

| Metric | Value |
|---|---|
| Total priced rows | 2 |
| Rows with complete SourceRef | 2 (100%) |
| Rows with `location TBD` | 0 (0%) |
| Top missing-source offenders | None |

## S7 -- Status Reporting

**PASS.** `RUN_STATUS = OK` declared. Justification:
- All line items priced with evidence-backed rates and hours
- No TBD amounts
- No fallback pricing used
- Provenance is 100% complete
- Basis consistency is 100% (all lines = RATE_TABLE, matching BASIS_OF_ESTIMATE)

## S8 -- Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or bounded WARNINGS | OK |
| Basis-consistency checks pass | PASS (100% RATE_TABLE) |
| Provenance completeness reported | PASS (100%) |
| Scope coverage explicit | PASS (1/1 in-scope deliverable covered; 0 excluded; 0 blocked) |
| No writes outside _Estimates/ | PASS |

---

## Basis Consistency

| Method | Line Count | % of Lines | Amount (CAD) | % of Total |
|---|---:|---:|---:|---:|
| RATE_TABLE | 2 | 100% | $2,020 | 100% |
| **Total** | **2** | **100%** | **$2,020** | **100%** |

ALLOW_MIXED_METHODS = FALSE. No mixed methods detected. **PASS.**

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-04-02) |
| Deliverables covered | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| SOW items covered | 1 (SOW-020 per _CONTEXT.md assignment) |

## Dependency / Blocker Summary

| Metric | Value |
|---|---|
| Total dependency rows | 13 |
| Upstream prerequisites (PENDING) | 3 (DEL-05-01, DEL-05-02, DEL-05-03) |
| Upstream interfaces (PENDING) | 4 (DEL-04-03, DEL-08-01, DEL-09-01, DEL-04-01) |
| Upstream constraints (PENDING) | 2 (RFP Section 7, Addendum 03) |
| Downstream (informational) | 1 (DEL-01-02) |
| Anchors | 3 |
| Blockers to estimating | 0 |

## What to Fix for a Cleaner Rerun

Nothing required. This run is clean. If the operator wants to improve confidence:

1. **Rate validation:** Obtain actual firm-specific hourly rates to replace parametric market rates (currently MEDIUM confidence).
2. **LOE validation:** Confirm 8h PM + 4h CM is adequate for the budget control and change management plan scope once the proposal effort is underway.
3. **Scope boundary check:** Verify that SOW-020 scope assignment to DEL-04-02 (per _CONTEXT.md) versus DEL-04-01 (per decomposition scope ledger) is correctly reflected in the LOE allocation. The Level_of_Effort.csv treats them as distinct: DEL-04-01 covers methodology (SOW-019 + SOW-020 admin), DEL-04-02 covers budget control/change management.
