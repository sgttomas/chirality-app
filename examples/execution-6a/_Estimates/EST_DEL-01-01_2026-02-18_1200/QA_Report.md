# QA Report

## RUN_STATUS: OK

Totals are meaningful; no critical input gaps. All line items priced with rate table evidence.

---

## S1 -- Write Quarantine Respected

- **PASS.** All outputs written under `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Estimates/EST_DEL-01-01_2026-02-18_1200/`. No files modified outside `_Estimates/`.

## S2 -- Snapshot Created

- **PASS.** Snapshot folder `EST_DEL-01-01_2026-02-18_1200` created.

## S3 -- BASIS_OF_ESTIMATE Validated

- **PASS.** `BASIS_OF_ESTIMATE = RATE_TABLE` is a valid enum value.

## S4 -- Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Detail.csv | PRESENT (optional but recommended; emitted) |

- **PASS.** All required and recommended artifacts present.

## S5 -- Detail Schema Integrity

| Check | Result |
|---|---|
| Detail.csv parseable | PASS |
| Required columns present (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS (all 14 columns present) |
| Method values valid | PASS (all 4 rows = RATE_TABLE) |
| Allowance/parametric convention | N/A (no ALLOWANCE or PARAMETRIC method rows) |
| Amount = Qty x UnitRate | PASS (L-001: 120x175=21000; L-002: 80x165=13200; L-003: 40x145=5800; L-004: 60x80=4800) |

- **PASS.**

## S6 -- Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows | 4 |
| Rows with non-TBD SourceRef | 4 |
| Rows with TBD SourceRef | 0 |
| Provenance completeness | **100%** |

- **PASS.** Every priced row has a SourceRef citing specific file paths and row identifiers.

## S7 -- Status Reporting

- **RUN_STATUS: OK** declared at top of this file.

## S8 -- Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK |
| Basis-consistency: all Method values match BASIS_OF_ESTIMATE (RATE_TABLE) | PASS (4/4 rows = RATE_TABLE) |
| Provenance completeness reported | 100% (4/4 rows) |
| Scope coverage explicit | 1 deliverable in scope, 1 covered, 0 missing, 0 blocked |
| No writes outside _Estimates/ | PASS |

- **PASS.** Snapshot is acceptable for publication.

---

## Coverage Report

| Metric | Count |
|---|---|
| Deliverables in SCOPE | 1 |
| Deliverables covered (at least 1 priced line) | 1 |
| Deliverables missing (no lines) | 0 |
| Deliverables blocked | 0 |
| Total line items | 4 |
| Total amount (CAD) | $44,800 |

## Basis-Consistency Check

| Method | Count | Expected (per BASIS_OF_ESTIMATE=RATE_TABLE) |
|---|---|---|
| RATE_TABLE | 4 | Primary method |
| Other | 0 | None expected (ALLOW_MIXED_METHODS=FALSE) |

- **PASS.** No mixed methods.

## Blocker Assessment (from dependency evidence)

- 21 dependency rows reviewed from Dependencies.csv.
- 9 ANCHOR rows (structural traceability; not blockers).
- 12 EXECUTION rows (10 UPSTREAM prerequisites/interfaces, 2 DOWNSTREAM handovers).
- **No cost-estimating blockers identified.** All upstream prerequisites are document-type inputs (RFP, addenda, appendices, contract) or deliverable interfaces. None block the ability to produce a rate-table estimate for labor hours.

## What to Fix for a Cleaner Rerun

- Nothing required. This is a clean run with full coverage and full provenance.
- Future improvement: if actual staff assignments or negotiated rates become available, re-run with QUOTE basis for higher confidence.
