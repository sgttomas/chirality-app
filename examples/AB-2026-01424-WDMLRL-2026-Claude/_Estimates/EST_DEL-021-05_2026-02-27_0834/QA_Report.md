# QA Report — EST_DEL-021-05_2026-02-27_0834

## RUN_STATUS: OK

---

## S1 — Write Quarantine Respected

**PASS.** All outputs written exclusively under `_Estimates/EST_DEL-021-05_2026-02-27_0834/`. No project truth files were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-021-05_2026-02-27_0834` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` is a valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required files are present:

| File | Status |
|---|---|
| Run_Context.md | Present |
| Items.csv | Present |
| Detail.csv | Present |
| Summary.md | Present |
| QA_Report.md | Present (this file) |
| Source_Index.md | Present |
| Decision_Log.md | Present |
| Assumptions_Log.md | Present |
| WBS_CBS_Matrix.csv | Present |

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | Yes |
| All PricingMode values valid (UNIT_RATE or LUMP_SUM) | Yes (14 LUMP_SUM, 1 UNIT_RATE) |
| Every row traces to SourceDoc + SourceSection | Yes |
| Row count | 15 items |

### Detail.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | Yes |
| All Method values valid | Yes (8x PARAMETRIC) |
| Allowance/parametric convention | N/A — all lines use hr-based unit rates (not LS convention) |
| Row count | 8 lines |

## S6 — Provenance Discipline

**PASS.**

| Metric | Value |
|---|---|
| Lines with non-TBD SourceRef | 8 / 8 (100%) |
| Lines with TBD SourceRef | 0 |
| Top missing-source offenders | None |

All 8 Detail.csv lines reference both `Professional_Staff_Rates.csv` (role + rate) and `Level_of_Effort.csv` (deliverable + role + hours).

## S7 — Status Reporting

**RUN_STATUS = OK**

Rationale:
- All totals are meaningful and based on parametric evidence.
- No critical input gaps.
- All lines are priced with provenance.
- Basis consistency: 100% PARAMETRIC, matching BASIS_OF_ESTIMATE.

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS | OK | |
| Quantity takeoff reviewed for completeness | PASS | 15 items extracted from all 4 documents |
| Basis-consistency checks pass | PASS | 100% PARAMETRIC |
| Provenance completeness reported | PASS | 100% |
| Scope coverage explicit | PASS | 1 deliverable, 2 SOW items, 0 missing documents |
| No writes outside _Estimates/ | PASS | |

## Additional QA Notes

1. **Activity-to-role mapping:** The Items.csv contains 15 discrete activity-level items extracted from the four documents. The pricing model (Level_of_Effort.csv) provides hours at the role level (8 roles), not the activity level. Each Detail.csv line maps a role's hours to the most representative activity item. This is an inherent granularity mismatch in the parametric model and is documented in the Decision_Log.
2. **Warranty remediation costs excluded by design:** DEL-021-05 covers warranty administration, not the cost of rectifying defects (which is borne by the Contractor per RFP §2.10.7). This is not a gap in the estimate.
3. **No TBD amounts:** All 8 lines are fully priced.
