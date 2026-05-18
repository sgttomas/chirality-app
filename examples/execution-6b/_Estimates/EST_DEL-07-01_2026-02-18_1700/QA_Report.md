# QA Report -- EST_DEL-07-01_2026-02-18_1700

**RUN_STATUS: OK**

---

## S1 -- Write Quarantine Respected

- PASS. All files written under `_Estimates/EST_DEL-07-01_2026-02-18_1700/` only.
- No modifications to deliverable content, lifecycle files, decomposition, or dependency registers.

## S2 -- Snapshot Created

- PASS. Snapshot folder `EST_DEL-07-01_2026-02-18_1700` created.

## S3 -- BASIS_OF_ESTIMATE Validated

- PASS. `RATE_TABLE` is a valid enum value.

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
| Blockers.md | PRESENT |

- PASS. All required and recommended artifacts emitted.

## S5 -- Detail Schema Integrity

| Check | Result |
|---|---|
| Detail.csv parseable | PASS |
| All 14 required columns present | PASS (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Method values valid | PASS (all RATE_TABLE) |
| Allowance/parametric convention | N/A (no ALLOWANCE or PARAMETRIC rows) |
| Amount = Qty x UnitRate | PASS (L-001: 12 x 155 = 1860; L-002: 4 x 175 = 700) |
| Currency consistent | PASS (all CAD) |

## S6 -- Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows | 2 |
| Rows with non-TBD SourceRef | 2 |
| Provenance completeness | **100%** |
| Top missing-source offenders | None |

- PASS. All rows have explicit source references to both Level_of_Effort.csv and Professional_Staff_Rates.csv.

## S7 -- Status Reporting

- **RUN_STATUS: OK**
- Totals are meaningful ($2,560 CAD).
- No critical input gaps.
- No TBD amounts.

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| Detail.csv Method values | All RATE_TABLE |
| ALLOW_MIXED_METHODS | FALSE |
| Mixed methods detected? | No |

- PASS. All methods consistent with declared basis.

## Coverage Check

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-07-01) |
| Deliverables covered | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |

- PASS. Full scope coverage.

## Dependency / Blocker Summary

- 15 dependency rows loaded from Dependencies.csv.
- 4 upstream deliverable prerequisites identified (DEL-02-02, DEL-10-02, DEL-09-01, DEL-07-03).
- 4 upstream document prerequisites identified (RFP Sections 7.2, 7.3; Appendix J; Addenda 01-03).
- 3 downstream handovers identified (DEL-07-02, DEL-07-04, DEL-07-05).
- **No dependencies block the estimating process itself.** Dependencies are execution-order constraints for content production, not pricing inputs.

## What to Fix for a Cleaner Rerun

- Nothing required. Run is clean.
- Optional: if firm-specific rate cards become available (replacing MARKET-basis rates), re-run with updated `Professional_Staff_Rates.csv` for higher-confidence pricing.
- Optional: if actual time tracking data becomes available for similar proposal deliverables, Level_of_Effort.csv hours could be validated.
