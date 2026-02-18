# QA Report — EST_DEL-07-01_2026-02-18_2010

## RUN_STATUS: OK

All inputs validated. All line items priced from basis evidence. No critical gaps.

---

## S1 -- Write Quarantine

| Check | Result |
|---|---|
| All writes under _Estimates/? | PASS |
| No modifications to deliverable working files? | PASS |
| No modifications to decomposition? | PASS |
| No modifications to dependency registers? | PASS |

---

## S2 -- Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists? | PASS |
| Folder name: EST_DEL-07-01_2026-02-18_2010 | PASS |

---

## S3 -- BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE provided? | PASS |
| Value = RATE_TABLE (valid enum)? | PASS |

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
| Detail.csv | PRESENT (optional; included) |
| Blockers.md | PRESENT (optional; included) |

---

## S5 -- Detail Schema Integrity

| Check | Result |
|---|---|
| Detail.csv parseable? | PASS |
| Required columns present? | PASS (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Method values valid? | PASS (all RATE_TABLE) |
| Allowance/parametric convention? | N/A (no ALLOWANCE or PARAMETRIC rows) |
| Qty x UnitRate = Amount? | PASS (16 x 105 = 1680; 4 x 175 = 700) |
| Sum of amounts = total? | PASS (1680 + 700 = 2380) |

---

## S6 -- Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows | 2 |
| Rows with non-TBD SourceRef | 2 |
| Provenance completeness | **100%** |
| Top missing-source offenders | None |

All rows reference specific rows in Level_of_Effort.csv and Professional_Staff_Rates.csv.

---

## S7 -- Status Reporting

| Check | Result |
|---|---|
| RUN_STATUS declared? | PASS |
| RUN_STATUS = OK | Totals meaningful; no critical input gaps |

---

## S8 -- Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps? | PASS (OK) |
| Basis-consistency: all Methods match BASIS_OF_ESTIMATE? | PASS (2/2 lines = RATE_TABLE) |
| Provenance completeness reported? | PASS (100%) |
| Scope coverage explicit? | PASS (1 deliverable in scope, 1 covered, 0 missing, 0 blocked) |
| No writes outside _Estimates/? | PASS |

---

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables covered (priced) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |

---

## Basis-Consistency Check

| Method | Count | Percentage |
|---|---|---|
| RATE_TABLE | 2 | 100% |

ALLOW_MIXED_METHODS = FALSE. All methods match BASIS_OF_ESTIMATE = RATE_TABLE. PASS.

---

## Blocker Count (from Dependency Evidence)

| Blocker Type | Count | Impact on Estimate |
|---|---|---|
| EXECUTION/PREREQUISITE (PENDING) | 3 | None -- cost estimate uses LOE hours + rates; content prerequisites do not affect cost |
| EXECUTION/INTERFACE (PENDING) | 3 | None -- interface alignment is content-level, not cost-level |
| EXECUTION/HANDOVER (PENDING) | 1 | None -- downstream; DEL-07-01 must complete before handover |

No dependency blockers prevent meaningful cost estimation.

---

## What to Fix for a Cleaner Rerun

Nothing. This run is clean:
- All line items fully priced
- All provenance complete
- Basis is consistent
- Scope is fully covered
- No TBD amounts
