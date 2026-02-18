# QA Report

## RUN_STATUS: OK

Totals are meaningful. No critical input gaps. The estimate consists of a single fixed cash allowance with full provenance.

---

## S1 -- Write Quarantine

**PASS.** All files written under `_Estimates/EST_DEL-05-07_2026-02-18_2200/` only. No project truth files were modified.

## S2 -- Snapshot Created

**PASS.** Snapshot folder `EST_DEL-05-07_2026-02-18_2200/` created.

## S3 -- BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = ALLOWANCE` -- valid enum value.

## S4 -- Required Artifacts Exist

**PASS.** All required files present:
- [x] `Run_Context.md`
- [x] `Summary.md`
- [x] `QA_Report.md`
- [x] `Source_Index.md`
- [x] `Decision_Log.md`
- [x] `Assumptions_Log.md`
- [x] `WBS_CBS_Matrix.csv`
- [x] `Detail.csv` (recommended; included)

## S5 -- Detail Schema Integrity

**PASS.**

| Check | Result |
|---|---|
| Detail.csv parseable | YES |
| All required columns present | YES (14/14) |
| Method values valid | YES -- `ALLOWANCE` (valid enum) |
| Allowance convention (Qty=1, Unit=LS, UnitRate=Amount) | YES -- Qty=1, Unit=LS, UnitRate=20000, Amount=20000 |
| Rounding applied (DOLLAR) | YES -- Amount is whole dollar |

## S6 -- Provenance Discipline

**PASS.**

| Metric | Value |
|---|---|
| Total priced rows | 1 |
| Rows with non-TBD SourceRef | 1 (100%) |
| Rows with `location TBD` | 0 (0%) |
| Provenance completeness | **100%** |

Top missing-source offenders: None.

## S7 -- Status Reporting

**RUN_STATUS = OK**
- Totals are meaningful ($20,000 CAD, single line).
- No TBDs, no critical input gaps.
- Basis-consistency: 100% ALLOWANCE (matches declared BASIS_OF_ESTIMATE).

## S8 -- Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK |
| Basis-consistency checks pass | PASS (100% ALLOWANCE) |
| Provenance completeness reported | 100% |
| Scope coverage explicit | 1 deliverable in scope; 0 excluded; 0 blocked |
| No writes outside `_Estimates/` | Confirmed |

---

## Coverage

| Metric | Count |
|---|---|
| Deliverables in scope | 1 |
| Deliverables covered (with priced lines) | 1 |
| Deliverables missing (no lines) | 0 |
| Deliverables blocked | 0 |

## Basis-Consistency

| Method | Line Count | % of Total |
|---|---|---|
| ALLOWANCE | 1 | 100% |

Mixed methods: NONE. `ALLOW_MIXED_METHODS=FALSE` -- compliant.

## Dependency / Blocker Summary

| DependencyID | Class | Type | Target | Impact |
|---|---|---|---|---|
| DEP-0507-E002 | EXECUTION | INTERFACE | DEL-05-06 (Appliances & Laundry) | Scope boundary coordination required to prevent double-counting. Brief provides explicit exclusion rules; no blocker to estimating. |

Blocker count: **0** (interface dependency noted but does not block pricing).

## What to Fix for a Cleaner Rerun

Nothing. This run is clean:
- Fixed allowance value confirmed from two independent sources (DEC-005 and OPT-18).
- Single line item with full provenance.
- No TBDs, no warnings, no blockers.
