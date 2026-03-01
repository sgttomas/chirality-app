# QA Report — EST_DEL-005-01_2026-02-27_0539

## RUN_STATUS: OK

All totals are meaningful. No critical input gaps. All priced items have full provenance.

---

## S1 — Write Quarantine Respected

**PASS.** All files written exclusively under `_Estimates/EST_DEL-005-01_2026-02-27_0539/`. No files outside the estimating tool root were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-005-01_2026-02-27_0539` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts present:

| File | Status |
|---|---|
| Run_Context.md | Created |
| Items.csv | Created |
| Summary.md | Created |
| QA_Report.md | Created (this file) |
| Source_Index.md | Created |
| Detail.csv | Created |
| WBS_CBS_Matrix.csv | Created |
| Decision_Log.md | Created |
| Assumptions_Log.md | Created |

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | Yes — all 9 columns present |
| Row count | 17 items |
| PricingMode values valid | Yes — 4 x UNIT_RATE, 13 x LUMP_SUM |
| All rows trace to a SourceDoc | Yes — Procedure (7), Specification (7), Datasheet (3) |
| All rows trace to a SourceSection | Yes |
| TBD quantities | 0 |

### Detail.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | Yes — all 15 columns present |
| Row count | 4 priced lines |
| Method values valid | Yes — all 4 lines are PARAMETRIC |
| Allowance/parametric convention | N/A — all lines are UNIT_RATE with Qty > 1; convention applies only to LS items |
| Amount computation verified | DL-001: 6 x 165 = 990 PASS; DL-002: 4 x 135 = 540 PASS; DL-003: 18 x 95 = 1,710 PASS; DL-004: 42 x 160 = 6,720 PASS |
| Grand total | 990 + 540 + 1,710 + 6,720 = 9,960 CAD PASS |

## S6 — Provenance Discipline

**PASS.**

| Metric | Value |
|---|---|
| Priced rows in Detail.csv | 4 |
| Rows with non-TBD SourceRef | 4 (100%) |
| Rows with TBD SourceRef | 0 |
| Top missing-source offenders | None |

Every priced row includes a SourceRef pointing to the specific Level_of_Effort.csv row (deliverable + RoleID) and Professional_Staff_Rates.csv row (RoleID + HourlyRate_CAD).

## S7 — Status Reporting

**RUN_STATUS = OK**

Totals are meaningful. No critical input gaps. No TBD amounts. All 4 priced lines have full provenance.

## Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 17 |
| Deliverables in scope | 1 (DEL-005-01) |
| Documents read | 5 (_CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md) |
| Missing documents | 0 |
| Items from Datasheet | 3 (ITM-008, ITM-009, and pad/construction scope items) |
| Items from Specification | 7 (requirement-driven scope items) |
| Items from Procedure | 7 (activity-driven scope items including labour lines) |
| Items from Guidance | 0 directly (Guidance informs design rationale; no separate priceable items identified beyond those already captured) |

## Pricing Coverage

| Metric | Value |
|---|---|
| Items with standalone pricing (Detail.csv lines) | 4 |
| Items with embedded pricing (scope items whose cost is within the 4 labour lines) | 13 |
| Items with TBD amounts | 0 |
| Pricing coverage | 100% |

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (4 of 4 lines) |
| Mixed methods | No — all lines consistent with declared basis |
| Fallback used | No — no fallback required |

**PASS.** Method usage is fully consistent with the declared PARAMETRIC basis.

## S8 — Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK |
| Items.csv reviewed for completeness | 17 items covering all major scope elements from all 4 documents |
| Basis-consistency checks pass | PASS — all PARAMETRIC |
| Provenance completeness reported | 100% — all priced rows have SourceRef |
| Scope coverage explicit | 1 deliverable in scope; 0 excluded; all 4 documents read |
| No writes outside _Estimates/ | Confirmed |

---

## What to Fix for a Cleaner Rerun

1. **Nothing critical.** This run produced a clean OK result.
2. **Rate confidence uplift:** If contracted rates become available (replacing MEDIUM-confidence parametric rates), rerun with updated Professional_Staff_Rates.csv to produce HIGH-confidence amounts.
3. **Cross-check with fee model:** When construction value estimates are available, cross-check the $9,960 total against DF-05 (Civil design fee at 1.0% of construction value) from Professional_Design_Fees.csv for reasonableness.
4. **Hours validation:** The 70-hour total (particularly the 42 Civil Engineer hours) could be validated against comparable preliminary design scope from historical projects if historical data becomes available.
