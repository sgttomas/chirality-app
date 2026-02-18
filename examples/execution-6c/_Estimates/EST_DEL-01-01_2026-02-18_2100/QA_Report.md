# QA Report: EST_DEL-01-01_2026-02-18_2100

## RUN_STATUS: OK

---

## S1 -- Write Quarantine

| Check | Result |
|---|---|
| All writes under `_Estimates/` | PASS |
| No project truth modified | PASS |

---

## S2 -- Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists | PASS |
| Folder: `EST_DEL-01-01_2026-02-18_2100` | Confirmed |

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
| All required columns present | PASS (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Method values valid | PASS (all = RATE_TABLE) |
| Allowance/parametric convention | N/A (no ALLOWANCE or PARAMETRIC method rows) |
| Amount computation | PASS (8 hr x $105/hr = $840 = Amount) |
| Rounding (DOLLAR) | PASS ($840 is a whole dollar amount) |

---

## S6 -- Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows | 1 |
| Rows with SourceRef | 1 |
| Rows with `location TBD` | 0 |
| **Provenance completeness** | **100%** |

Top missing-source offenders: None.

---

## S7 -- Status Reporting

| Check | Result |
|---|---|
| RUN_STATUS declared | OK |
| Justification | All line items priced with rate table evidence; no TBDs; no critical input gaps; single deliverable fully covered |

---

## S8 -- Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or bounded WARNINGS | PASS (OK) |
| Basis-consistency check | PASS (all Method = RATE_TABLE = BASIS_OF_ESTIMATE) |
| Provenance completeness reported | PASS (100%) |
| Scope coverage explicit | PASS (1 in-scope, 1 estimated, 0 blocked, 0 excluded) |
| No writes outside _Estimates/ | PASS |

---

## Coverage Analysis

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables estimated | 1 |
| Deliverables blocked | 0 |
| Deliverables with TBD amounts | 0 |
| Line items total | 1 |
| Line items priced | 1 |

---

## Basis-Consistency Check

| Method | Count | % of Lines | Consistent with BASIS_OF_ESTIMATE? |
|---|---|---|---|
| RATE_TABLE | 1 | 100% | YES |

No mixed methods detected. ALLOW_MIXED_METHODS = FALSE requirement satisfied.

---

## Blocker Analysis (from Dependency Evidence)

| Metric | Value |
|---|---|
| Dependencies.csv rows | 26 |
| ANCHOR rows | 4 |
| EXECUTION rows | 22 |
| Upstream PREREQUISITE (document) | 5 (RFP, Add 01-03, Decomposition) |
| Upstream INTERFACE (deliverable) | 2 (DEL-01-02, DEL-01-03 -- status tracking only) |
| Downstream PREREQUISITE | 1 (DEL-01-01 gates DEL-01-02) |
| Downstream INTERFACE | 14 (compliance matrix monitors coverage of other DELs) |
| **Estimating blockers identified** | **0** |

No dependency blocks the ability to estimate this deliverable. All upstream prerequisites are document-type inputs (available). The upstream interface dependencies to DEL-01-02 and DEL-01-03 are status-tracking interfaces (compliance matrix receives confirmation from them), not pricing inputs.

---

## What to Fix for a Cleaner Rerun

Nothing required. This is a clean run with no warnings or gaps.

- If the LOE hours for DEL-01-01 are updated in `Level_of_Effort.csv`, rerun to pick up the change.
- If a firm-specific rate replaces the market parametric rate for R-22, rerun with updated `Professional_Staff_Rates.csv`.
