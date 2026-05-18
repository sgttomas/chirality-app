# QA Report -- EST_DEL-01-03_2026-02-18_1720

## RUN_STATUS: WARNINGS

Totals exist for labour line items but material TBDs remain for training costs and PPE/signage supplies. The priced total ($7,240 CAD) represents labour only and is an understatement of the full deliverable cost.

---

## S1 -- Write Quarantine

| Check | Result |
|---|---|
| All writes under ESTIMATES_ROOT? | PASS |
| Files outside _Estimates/ modified? | NONE |

## S2 -- Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists? | PASS -- EST_DEL-01-03_2026-02-18_1720/ |

## S3 -- BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE provided? | YES -- RATE_TABLE |
| Valid enum value? | PASS |

## S4 -- Required Artifacts

| Artifact | Exists |
|---|---|
| Run_Context.md | YES |
| Summary.md | YES |
| QA_Report.md | YES (this file) |
| Source_Index.md | YES |
| Decision_Log.md | YES |
| Assumptions_Log.md | YES |
| WBS_CBS_Matrix.csv | YES |
| Detail.csv | YES |

## S5 -- Detail Schema Integrity

| Check | Result |
|---|---|
| Detail.csv parseable? | PASS |
| All required columns present? | PASS (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Method values valid? | PASS (all rows = RATE_TABLE) |
| Allowance/parametric convention? | N/A (no ALLOWANCE or PARAMETRIC method rows) |
| TBD rows handled correctly? | PASS (Qty/Unit/UnitRate/Amount = TBD for unpriced lines; SourceRef = "location TBD") |

## S6 -- Provenance Discipline

| Metric | Value |
|---|---|
| Total line items | 4 |
| Lines with substantive SourceRef | 2 (L-0103-001, L-0103-002) |
| Lines with "location TBD" SourceRef | 2 (L-0103-003, L-0103-004) |
| Provenance completeness (priced lines) | 100% (2/2 priced lines have full source references) |
| Provenance completeness (all lines) | 50% (2/4 total lines) |

### Top Missing-Source Offenders

| LineID | Description | Missing Source |
|---|---|---|
| L-0103-003 | Training costs | No training material/fee rate table or quote |
| L-0103-004 | PPE / signage supplies | No supply cost or quantity source |

## S7 -- Status Reporting

**RUN_STATUS = WARNINGS**

Rationale: Labour costs are meaningfully priced ($7,240 CAD) with full provenance. However, 2 of 4 line items representing non-labour cost drivers have no pricing source and are TBD. The total is a known understatement.

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| Method values in Detail.csv | All rows = RATE_TABLE |
| Mixed methods detected? | NO |
| ALLOW_MIXED_METHODS | FALSE |
| Consistency | PASS |

## Coverage Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables with at least 1 priced line | 1 |
| Deliverables fully priced (all lines) | 0 |
| Deliverables blocked | 0 |
| Deliverables excluded | 0 |

## Blocker Summary (from dependency evidence)

| Metric | Value |
|---|---|
| Total dependencies parsed | 9 (from Dependencies.csv) |
| Pricing blockers identified | 0 |
| Sequencing dependencies noted | 1 (DEP-0103-E005: DEL-01-06 prerequisite for construction-phase finalization) |

## What to Fix for a Cleaner Rerun

1. **Provide training cost data**: A rate table or quote covering site orientation/training costs (instructor time, materials, certification fees) would allow L-0103-003 to be priced.
2. **Provide PPE/signage supply cost data**: A rate table or quote covering PPE quantities and unit costs (hard hats, hi-vis vests, safety glasses, signage) would allow L-0103-004 to be priced.
3. With both items resolved, RUN_STATUS would likely upgrade to OK.
