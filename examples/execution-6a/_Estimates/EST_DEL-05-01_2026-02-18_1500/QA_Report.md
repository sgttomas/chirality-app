# QA Report

## RUN_STATUS: WARNINGS

The estimate is usable as a preliminary budget figure but has material gaps that must be resolved before contract pricing.

---

## S1 -- Write Quarantine Respected

| Check | Result |
|---|---|
| All output files under _Estimates/ only | **PASS** |
| No modifications to deliverable working files | **PASS** |
| No modifications to lifecycle files | **PASS** |
| No modifications to decomposition outputs | **PASS** |
| No modifications to dependency registers | **PASS** |

## S2 -- Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists | **PASS** -- EST_DEL-05-01_2026-02-18_1500 |

## S3 -- BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE provided | **PASS** -- QUOTE |
| Enum valid | **PASS** -- QUOTE is a valid enum value |
| Actual method matches declared basis | **FAIL (expected)** -- ALLOWANCE used instead of QUOTE; justified by FALLBACK_POLICY=ALLOW_ALLOWANCE and ALLOW_MIXED_METHODS=TRUE; logged in DEC-EST-001 |

## S4 -- Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | **PASS** |
| Summary.md | **PASS** |
| QA_Report.md | **PASS** |
| Source_Index.md | **PASS** |
| Decision_Log.md | **PASS** |
| Assumptions_Log.md | **PASS** |
| WBS_CBS_Matrix.csv | **PASS** |
| Detail.csv | **PASS** (optional but recommended; produced) |
| Blockers.md | **PASS** (produced; dependencies found) |
| Risk_Register.md | **PASS** (produced; risks identified) |

## S5 -- Detail Schema Integrity

| Check | Result |
|---|---|
| Detail.csv parseable | **PASS** |
| All required columns present | **PASS** (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Method values valid | **PASS** -- all ALLOWANCE (valid enum) |
| Allowance convention (Qty=1, Unit=LS, UnitRate=Amount) | **PASS** -- all 3 rows comply |
| Currency consistent | **PASS** -- all CAD |
| Rounding applied | **PASS** -- all amounts are whole dollars (ROUNDING=DOLLAR) |

## S6 -- Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows | 3 |
| Rows with non-TBD SourceRef | 3 (100%) |
| Provenance completeness | **100%** |
| Top missing-source offenders | None |

All rows reference Optional_Items_Pricing.csv with specific row IDs (OPT-01, OPT-02, OPT-03) plus the fallback decision reference (DEC-EST-001).

## S7 -- Status Reporting

| Check | Result |
|---|---|
| RUN_STATUS declared | **PASS** |
| RUN_STATUS value | **WARNINGS** |
| Justification | Totals exist and are meaningful as budget-level allowances, but: (a) no vendor quote backing; (b) environmental requirements unresolved; (c) all items LOW confidence; (d) PW bay layout prerequisite not yet satisfied |

## S8 -- Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | **PASS** -- WARNINGS with clearly identified gaps |
| Basis-consistency checks pass or deviations approved | **PASS** -- deviation from QUOTE to ALLOWANCE is approved by FALLBACK_POLICY and logged in DEC-EST-001 |
| Provenance completeness reported | **PASS** -- 100% (3/3 rows) |
| Top gaps actionable | **PASS** -- 3 actions identified: (1) obtain vendor quotes, (2) resolve AEP requirements, (3) confirm PW bay layout |
| Scope coverage explicit | **PASS** -- 1 deliverable in scope, 1 covered, 0 missing, 0 blocked |
| No writes outside _Estimates/ | **PASS** |

## Coverage Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables covered (with pricing) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Line items produced | 3 |
| Total estimate (CAD) | $123,000 |

## Basis-Consistency Check

| Check | Result |
|---|---|
| Declared basis | QUOTE |
| Methods actually used | ALLOWANCE (3/3 rows) |
| Mixed methods present | YES |
| ALLOW_MIXED_METHODS | TRUE |
| FALLBACK_POLICY | ALLOW_ALLOWANCE |
| Deviation justified | YES -- DEC-EST-001 |
| **Basis-consistency** | **PASS (with approved deviation)** |

## Blocker Summary (from dependency evidence)

| Metric | Value |
|---|---|
| Total dependencies loaded | 11 |
| Anchor dependencies | 2 |
| Execution dependencies | 9 |
| Unresolved (TBD) | 9 |
| Critical for estimate accuracy | 3 |

## What to Fix for a Cleaner Rerun

1. **Obtain vendor quotes** for wash bay system, plumbing modifications, and environmental compliance. Replace ALLOWANCE method with QUOTE and update SourceRef to quote documents.
2. **Resolve AEP/Town environmental requirements** (DEP-05-01-E04) to narrow OPT-03 range and increase confidence.
3. **Confirm PW bay layout** (DEP-05-01-E01 via DEL-02-03) to validate that fourth bay conversion assumption holds.
4. **Review fleet vehicle dimensions** (DEP-05-01-E02, Appendix B) to confirm wash bay clear dimensions and equipment sizing.
5. **Establish project-level CBS structure** to replace provisional CBS-0500-* codes.
