# QA Report

## Run: EST_DEL-09-01_2026-02-18_1500

---

## RUN_STATUS: OK

All inputs loaded successfully. All line items are fully priced with complete provenance. No critical input gaps. Basis-consistency checks pass.

---

## S1 -- Write Quarantine

| Check | Result |
|---|---|
| All writes under _Estimates/ | PASS |
| No project truth files modified | PASS |

---

## S2 -- Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists | PASS |
| Path | EST_DEL-09-01_2026-02-18_1500/ |

---

## S3 -- BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| Value provided | RATE_TABLE |
| Valid enum | PASS |

---

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
| Detail.csv | PRESENT |

---

## S5 -- Detail Schema Integrity

| Check | Result |
|---|---|
| Detail.csv parseable | PASS |
| All 14 required columns present | PASS |
| Column list | LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes |
| Method values valid | PASS (all RATE_TABLE) |
| Allowance/parametric convention | N/A (no ALLOWANCE or PARAMETRIC lines) |
| Amount = Qty x UnitRate check | PASS (all 3 lines verified: 10x175=1750, 8x130=1040, 4x155=620) |
| Total reconciliation | PASS (1750+1040+620 = 3410 = WBS_CBS_Matrix total) |

---

## S6 -- Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows | 3 |
| Rows with complete SourceRef | 3 |
| Rows with TBD SourceRef | 0 |
| Provenance completeness | **100%** |
| Top missing-source offenders | None |

---

## S7 -- Status Reporting

| Field | Value |
|---|---|
| RUN_STATUS | **OK** |
| Totals meaningful | YES ($3,410 CAD) |
| Critical input gaps | NONE |
| TBD amounts | NONE |

---

## Coverage Report

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-09-01) |
| Deliverables covered | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| SOW items addressed | SOW-026 (risk register), SOW-027 (quality management plan) |

---

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| Methods used in Detail.csv | RATE_TABLE (3/3 lines) |
| Mixed methods detected | NO |
| ALLOW_MIXED_METHODS | FALSE |
| Consistency | **PASS** |

---

## Dependency / Blocker Analysis

| Metric | Value |
|---|---|
| Dependency register loaded | YES (Dependencies.csv, 18 rows) |
| Upstream prerequisites (documents) | 8 (RFP, Addendum 03, geotech, wetland, enviro, flood, grading, adjacent subdivision) |
| Upstream interfaces (deliverables) | 1 (DEL-09-02) |
| Downstream handovers | 4 (DEL-08-01, DEL-05-03, DEL-06-01, DEL-04-01) |
| Blockers to production cost estimate | **0** (document prerequisites are reference inputs; they do not block the hours-based production cost estimate) |

---

## What to Fix for a Cleaner Rerun

Nothing required. This run is clean:
- All 3 line items are fully priced with RATE_TABLE method.
- 100% provenance completeness.
- No TBD amounts.
- No mixed methods.
- No blockers.
- Basis-consistency passes.

---

## S8 -- Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK |
| Basis-consistency checks pass | PASS |
| Provenance completeness reported | 100% |
| Scope coverage explicit | 1/1 deliverable covered |
| No writes outside _Estimates/ | CONFIRMED |
| **Snapshot publishable** | **YES** |
