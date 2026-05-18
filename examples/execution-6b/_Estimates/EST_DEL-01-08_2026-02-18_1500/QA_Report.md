# QA Report — EST_DEL-01-08_2026-02-18_1500

**RUN_STATUS: OK**

---

## S1 — Write Quarantine

| Check | Result |
|---|---|
| All outputs written under _Estimates/ only | PASS |
| No deliverable working files modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition outputs modified | PASS |
| No dependency registers modified | PASS |

---

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists: EST_DEL-01-08_2026-02-18_1500/ | PASS |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = RATE_TABLE | PASS |
| Value is a valid enum member | PASS |

---

## S4 — Required Artifacts Exist

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

## S5 — Detail Schema Integrity

| Check | Result |
|---|---|
| Detail.csv is parseable CSV | PASS |
| All required columns present (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (all = RATE_TABLE) | PASS |
| Allowance/parametric convention | NOT_APPLICABLE (no ALLOWANCE or PARAMETRIC lines) |
| Row count | 2 |
| Amount computation check: L-001 = 12 x 85 = 1020 | PASS |
| Amount computation check: L-002 = 8 x 105 = 840 | PASS |
| Sum check: 1020 + 840 = 1860 = WBS_CBS_Matrix total | PASS |

---

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows | 2 |
| Rows with non-TBD SourceRef | 2 |
| Provenance completeness | **100%** |
| Rows with "location TBD" | 0 |
| Top missing-source offenders | None |

---

## S7 — Status Reporting

| Check | Result |
|---|---|
| RUN_STATUS declared | PASS |
| RUN_STATUS = OK | Totals are meaningful; no critical input gaps; all lines priced with complete provenance |

---

## S8 — Operator Acceptance Checklist

| Check | Result | Notes |
|---|---|---|
| RUN_STATUS is OK or bounded WARNINGS | PASS | OK |
| Basis-consistency check | PASS | All Method values = RATE_TABLE, matching BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% |
| Scope coverage explicit | PASS | 1 deliverable in scope; 0 excluded; 0 blocked |
| No writes outside _Estimates/ | PASS | |

---

## Coverage Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-01-08) |
| Deliverables with priced lines | 1 |
| Deliverables blocked | 0 |
| Deliverables excluded | 0 |
| Total line items | 2 |
| Total amount (CAD) | $1,860 |
| Unique roles priced | 2 (R-26, R-22) |
| Total hours | 20 |

---

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| ALLOW_MIXED_METHODS | FALSE |
| Detail.csv Method values | All = RATE_TABLE |
| Mixed methods detected | NO |
| Consistency | PASS |

---

## Dependency-Informed Observations

From Dependencies.csv (8 rows):
- 2 upstream prerequisites (DEL-01-07, DEL-01-09) with SatisfactionStatus = TBD. These affect execution sequencing but do not block pricing.
- 1 downstream handover (DEL-01-02). Not a pricing concern.
- 1 interface dependency (DEL-01-09 consistency). Not a pricing concern.
- 3 anchor dependencies (scope/objective/requirement traceability). Informational.
- No unresolved inputs that would prevent meaningful cost estimation.

---

## What to Fix for a Cleaner Rerun

Nothing. This run is clean. All checks pass. RUN_STATUS = OK.
