# QA Report — EST_DEL-01-06_2026-02-18_2100

## RUN_STATUS: OK

**Rationale:** All 4 line items are priced ($263,700 CAD). No TBD lines remain. Two lines (L-0106-003, L-0106-004) are ALLOWANCE at LOW confidence, representing $60,000 (23% of total).

---

## S1 — Write Quarantine

**PASS.** All files written under `{ESTIMATES_ROOT}/EST_DEL-01-06_2026-02-18_2100/`.

## S2 — Snapshot Created

**PASS.** Snapshot folder exists.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `RATE_TABLE` is a valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts present:
- [x] Run_Context.md
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv
- [x] Detail.csv
- [x] Blockers.md

## S5 — Detail Schema Integrity

**PASS.** Detail.csv contains all 14 required columns. Method values are RATE_TABLE (2 lines) and ALLOWANCE (2 lines). Mixed methods authorized per DEC-EST-005.

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total line items | 4 |
| Lines with non-TBD SourceRef | 4 |
| Provenance completeness | 100% |

## S7 — Status Reporting

**RUN_STATUS = OK**

All line items priced. Two ALLOWANCE lines at LOW confidence — bounded and explicitly flagged.

## Coverage Report

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables covered (all lines priced) | 1 |
| Total line items | 4 |
| Priced line items | 4 |
| TBD line items | 0 |
| Total | $263,700 CAD |

## S8 — Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (OK) |
| Basis-consistency checks pass | PASS (mixed methods authorized) |
| Provenance completeness reported | PASS (100%) |
| Scope coverage explicit | PASS (1 deliverable; 4 lines; all priced) |
| No writes outside _Estimates/ | PASS |
