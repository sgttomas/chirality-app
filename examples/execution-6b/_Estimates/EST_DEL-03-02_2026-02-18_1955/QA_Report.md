# QA Report

**RunID:** EST_DEL-03-02_2026-02-18_1955
**RUN_STATUS: OK**

---

## S1 -- Write Quarantine Respected

**PASS.** All files written exclusively under `_Estimates/EST_DEL-03-02_2026-02-18_1955/`. No files outside `_Estimates/` were modified.

## S2 -- Snapshot Created

**PASS.** Snapshot folder `EST_DEL-03-02_2026-02-18_1955` created.

## S3 -- BASIS_OF_ESTIMATE Validated

**PASS.** `RATE_TABLE` is a valid enum value.

## S4 -- Required Artifacts Exist

**PASS.** All required files produced:
- [x] Run_Context.md
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv
- [x] Detail.csv (recommended; produced)

## S5 -- Detail Schema Integrity

**PASS.**
- Detail.csv contains all 14 required columns: LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes.
- Method value `RATE_TABLE` is valid.
- No allowance/parametric rows present (convention not applicable).
- Arithmetic check: 10 x 155 = 1,550. Matches Amount column. PASS.

## S6 -- Provenance Discipline

**PASS.**
- 1 of 1 priced rows (100%) have non-TBD SourceRef.
- SourceRef points to specific rows in Level_of_Effort.csv (DEL-03-02/R-07) and Professional_Staff_Rates.csv (R-07).
- No missing-source offenders.

## S7 -- Status Reporting

**RUN_STATUS = OK**
- All totals are meaningful.
- No critical input gaps.
- No TBD amounts.
- Single basis method used throughout (RATE_TABLE).

## S8 -- Operator Acceptance Checklist

| Check | Status |
|---|---|
| RUN_STATUS is OK or bounded WARNINGS | OK |
| Basis-consistency check (all methods = RATE_TABLE) | PASS |
| Provenance completeness | 100% (1/1 rows) |
| Scope coverage | 1 deliverable in scope; 1 estimated; 0 missing; 0 blocked |
| No writes outside _Estimates/ | PASS |

---

## Schema Validation Detail

| Column | Expected | Actual | Valid |
|---|---|---|---|
| LineID | non-empty | L-001 | YES |
| CBS | non-empty | PROF_SERVICES | YES |
| WBS_PackageID | non-empty | PKG-003 | YES |
| WBS_DeliverableID | non-empty | DEL-03-02 | YES |
| Description | non-empty | present | YES |
| Qty | numeric | 10 | YES |
| Unit | non-empty | hr | YES |
| UnitRate | numeric | 155 | YES |
| Amount | numeric | 1550 | YES |
| Currency | non-empty | CAD | YES |
| Method | valid enum | RATE_TABLE | YES |
| SourceRef | non-empty | present | YES |
| Confidence | valid enum | MED | YES |
| Notes | any | present | YES |

---

## Basis Consistency

| Method | Line Count | % of Lines |
|---|---|---|
| RATE_TABLE | 1 | 100% |

ALLOW_MIXED_METHODS = FALSE. Only RATE_TABLE used. **PASS.**

---

## Dependency-Derived Observations

18 dependency rows reviewed from `Dependencies.csv`. Key findings:
- **Upstream prerequisites (DEL-02-02, DEL-02-01):** Required for brief production but do not affect the estimate amount. No blocker to estimating.
- **Reference documents (Appendix D, E, F, RFP 7.1.2, Addendum 03):** Input context for brief content, not for pricing. No blocker to estimating.
- **Downstream interfaces (DEL-01-06, DEL-10-02, DEL-03-01, DEL-01-01):** Coordination outputs from DEL-03-02. No impact on estimate.

**Blocker count for estimating purposes: 0.**

---

## What to Fix for a Cleaner Rerun

Nothing required. This is a clean run with full provenance and no TBDs.
