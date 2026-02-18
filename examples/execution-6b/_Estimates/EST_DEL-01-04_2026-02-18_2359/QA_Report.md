# QA Report

**RunID:** EST_DEL-01-04_2026-02-18_2359
**RUN_STATUS:** WARNINGS

---

## S1 -- Write Quarantine

**PASS.** All output files written exclusively under `_Estimates/EST_DEL-01-04_2026-02-18_2359/`. No project truth files modified.

## S2 -- Snapshot Created

**PASS.** Snapshot folder exists at `_Estimates/EST_DEL-01-04_2026-02-18_2359/`.

## S3 -- BASIS_OF_ESTIMATE Validated

**PASS.** `RATE_TABLE` is a valid enum value. Mixed methods (PARAMETRIC, ALLOWANCE) enabled via `ALLOW_MIXED_METHODS=TRUE` and `FALLBACK_POLICY=ALLOW_ALLOWANCE`.

## S4 -- Required Artifacts Exist

**PASS.** All required files present:
- [x] Run_Context.md
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv
- [x] Detail.csv (recommended; present)

## S5 -- Detail Schema Integrity

**PASS.** Detail.csv contains all 14 required columns:
- LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes

Method values validated:
- RATE_TABLE: 86 lines
- PARAMETRIC: 1 line (B-1000 cold storage PEMB)
- ALLOWANCE: 4 lines (B-598, B-960, B-1180, C-600)

Allowance/parametric convention check:
- All ALLOWANCE and PARAMETRIC lines use Qty=1, Unit=LS, UnitRate=Amount: **PASS**

## S6 -- Provenance Discipline

**Provenance completeness: 100%** -- All 91 lines have non-TBD SourceRef values.

Every priced line includes a specific file reference (e.g., `SC-14 ($3000/ea x 80 piles)`) or multiple references where composite pricing was used.

Top provenance quality notes:
- All SourceRef entries cite specific item IDs from price source CSVs
- Quantity derivations are documented in the Notes column
- Cross-references to Assumed_Project_Parameters.csv (PP-series) are implicit in quantity assumptions

## S7 -- Status Reporting

**RUN_STATUS: WARNINGS**

Rationale for WARNINGS (not OK):
1. **DB margin, contingency, and escalation NOT included.** The $7,327,000 base construction estimate represents direct costs + general requirements. The gap to the PP-25 $12M target requires commercial decisions outside ESTIMATING scope.
2. **Fire protection (B-420, $108k):** LOW confidence -- AHJ determination pending; sprinkler may not be required.
3. **Generator system (B-530, $150k):** LOW confidence -- depends on detailed load calculations.
4. **CCIP insurance (B-1130, $240k):** LOW confidence -- actual premium depends on project risk profile.
5. **Several quantities are assumed** from PP-series parameters at MEDIUM confidence -- will be refined during design.
6. **Schedule A / Schedule B reconciliation not performed** -- DEL-01-05 estimate needed for cross-check.
7. **Town of Penhold fee schedule unknown** -- building permit fee (B-1160, $65k) is estimated.

## S8 -- Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or bounded WARNINGS | PASS | WARNINGS with clearly identified gaps |
| Basis-consistency | PASS | RATE_TABLE primary (86 lines); PARAMETRIC (1 line) and ALLOWANCE (4 lines) used per FALLBACK_POLICY |
| Provenance completeness reported | PASS | 100% -- all 91 lines have SourceRef |
| Scope coverage explicit | PASS | 1 deliverable (DEL-01-04); dual cost nature addressed; 91 line items |
| No writes outside _Estimates/ | PASS | Verified |

---

## Coverage Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-01-04) |
| Deliverables estimated | 1 |
| Deliverables blocked | 0 |
| Total line items | 91 |
| Group A (production) line items | 3 |
| Group B (base construction) line items | 82 |
| Group C (options) line items | 6 |
| Total CBS categories | 17 |
| Lines with Confidence=HIGH | 2 |
| Lines with Confidence=MED | 76 |
| Lines with Confidence=LOW | 13 |

## Method Distribution

| Method | Line Count | Amount (CAD) | % of Grand Total |
|---|---:|---:|---:|
| RATE_TABLE | 86 | $7,315,960 | 94.8% |
| PARAMETRIC | 1 | $288,000 | 3.7% |
| ALLOWANCE | 4 | $116,000 | 1.5% |
| **Total** | **91** | **$7,719,960** | **100.0%** |

## What to Fix for a Cleaner Rerun

1. **Add DB margin/contingency/escalation inputs** -- provide commercial markup parameters to bridge the gap between direct costs ($7.3M) and target proposal price (~$12M). This is a commercial decision requiring human input.
2. **Confirm fire protection requirement** with AHJ before finalizing -- currently priced at $108k; could be $0 if not required.
3. **Refine generator sizing** when detailed load calculations are available -- current $150k is parametric.
4. **Obtain Town of Penhold fee schedule** to replace estimated building permit cost.
5. **Reconcile with DEL-01-05 estimate** once Schedule B detail is available.
6. **Obtain CCIP insurance quote** to replace percentage-based estimate.
