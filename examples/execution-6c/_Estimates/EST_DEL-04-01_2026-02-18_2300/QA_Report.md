# QA Report — EST_DEL-04-01_2026-02-18_2300

## RUN_STATUS: OK

All inputs resolved. Totals are meaningful. No critical input gaps.

---

## S1 — Write Quarantine

**PASS.** All outputs written exclusively under `_Estimates/EST_DEL-04-01_2026-02-18_2300/`. No files outside the estimating tool root were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-04-01_2026-02-18_2300` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `RATE_TABLE` is a valid enum value.

## S4 — Required Artifacts Exist

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

## S5 — Detail Schema Integrity

**PASS.**

| Check | Result |
|---|---|
| CSV parseable | Yes |
| All required columns present | Yes (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Method values valid | Yes (all = RATE_TABLE) |
| Allowance/parametric convention | N/A (no ALLOWANCE or PARAMETRIC lines) |
| Row count | 2 |
| Arithmetic check (Qty x UnitRate = Amount) | L-01: 14 x 155 = 2170 PASS; L-02: 4 x 175 = 700 PASS |
| Currency consistent | Yes (all CAD) |

## S6 — Provenance Discipline

**PASS.** 100% provenance completeness.

| Metric | Value |
|---|---|
| Total priced rows | 2 |
| Rows with complete SourceRef | 2 (100%) |
| Rows with `location TBD` | 0 (0%) |
| Top missing-source offenders | None |

## S7 — Status Reporting

**PASS.** `RUN_STATUS = OK` declared. Justification:
- All line items priced with evidence-backed rates and hours
- No TBD amounts
- No fallback pricing used
- Provenance is 100% complete
- Basis consistency is 100% (all lines = RATE_TABLE, matching BASIS_OF_ESTIMATE)

## S8 — Operator Acceptance Checklist

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
| RATE_TABLE | 2 | 100% | $2,870 | 100% |
| **Total** | **2** | **100%** | **$2,870** | **100%** |

ALLOW_MIXED_METHODS = FALSE. No mixed methods detected. **PASS.**

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-04-01) |
| Deliverables covered | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| SOW items covered | 2 (SOW-019, SOW-020) |

## Dependency / Blocker Summary

| Metric | Value |
|---|---|
| Total dependency rows | 14 |
| Upstream prerequisites (PENDING) | 3 |
| Upstream interfaces (PENDING) | 1 |
| Upstream constraints (PENDING) | 2 |
| Downstream (informational) | 4 |
| Blockers to estimating | 0 |

## What to Fix for a Cleaner Rerun

Nothing required. This run is clean. If the operator wants to improve confidence:

1. **Rate validation:** Obtain actual firm-specific hourly rates to replace parametric market rates (currently MEDIUM confidence).
2. **LOE validation:** Confirm 14h CM + 4h PM is adequate for the consolidated SOW-019 + SOW-020 scope once the proposal effort is underway.
3. **Safety Officer allocation:** Consider whether a separate Safety Officer (R-20) review should be charged to DEL-04-01 for the H&S plan content.
