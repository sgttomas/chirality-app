# QA Report — EST_DEL-002-07_2026-02-27_0133

## RUN_STATUS: OK

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All output files written under `_Estimates/EST_DEL-002-07_2026-02-27_0133/` | PASS |
| No files outside `_Estimates/` modified | PASS |

---

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists: `_Estimates/EST_DEL-002-07_2026-02-27_0133/` | PASS |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = PARAMETRIC | PASS (valid enum value) |

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Items.csv | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT |
| Source_Index.md | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Detail.csv | PRESENT (optional; produced) |

---

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to a source document and section | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS (4 UNIT_RATE, 4 LUMP_SUM) |
| Row count | 8 items |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid | PASS (all PARAMETRIC) |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount for LS items) | PASS for zero-cost LS items (LN-005 through LN-008: Qty=1, Unit=LS, UnitRate=0=Amount) |
| Row count | 8 lines |

---

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows (Amount > 0) | 4 |
| Rows with non-TBD SourceRef | 4 |
| Provenance completeness (priced rows) | **100%** |
| Total rows (including zero-cost) | 8 |
| Rows with non-TBD SourceRef (all) | 8 |
| Provenance completeness (all rows) | **100%** |
| Top missing-source offenders | None |

All priced lines cite both a rate source (Professional_Staff_Rates.csv with RoleID) and an hours source (Level_of_Effort.csv with DeliverableID + RoleID).

---

## S7 — Status Reporting

| Check | Result |
|---|---|
| Totals meaningful | PASS — $19,230.00 CAD total from fully priced parametric sources |
| Critical input gaps | NONE |
| TBD amounts | 0 of 8 lines |
| **RUN_STATUS** | **OK** |

---

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK | No TBDs, no critical gaps |
| Items.csv reviewed for completeness | PASS | 8 items covering all 4 LOE roles + 4 lump-sum activity items from Procedure steps |
| Basis-consistency checks pass | PASS | 100% PARAMETRIC method; matches BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% provenance on all rows |
| Scope coverage explicit | PASS | 1 deliverable (DEL-002-07) in scope; all 4 documents read; no missing documents |
| No writes outside _Estimates/ | PASS | Verified |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Documents Missing | Items Extracted |
|---|---|---|---|
| DEL-002-07 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | 0 | 8 |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Items priced (Amount > 0) | 4 of 8 (50%) |
| Items at $0 (embedded cost) | 4 of 8 (50%) |
| Items TBD | 0 of 8 (0%) |
| Total priced amount | $19,230.00 CAD |

Note: The 4 zero-cost items represent activities whose effort is embedded in the hourly allocations of the 4 priced items. This is not a gap; it is a modelling choice documented in Decision_Log.md (DEC-004) and Assumptions_Log.md (ASM-003 through ASM-006).

---

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods in Detail.csv | 100% PARAMETRIC |
| Mixed methods | NO |
| ALLOW_MIXED_METHODS setting | TRUE (not exercised) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC (not exercised; all items had primary pricing) |

---

## What to Fix for a Cleaner Rerun

1. **No critical fixes required.** This run completed with RUN_STATUS = OK.
2. **Optional improvement:** If vendor rate quotes become available, re-run with BASIS_OF_ESTIMATE = QUOTE or RATE_TABLE for higher confidence pricing.
3. **Optional improvement:** If historical actuals for similar crane support design scopes become available, re-run with BASIS_OF_ESTIMATE = HISTORICAL for benchmarking.
4. **Optional improvement:** Consider adding disbursement, travel, and printing cost lines if those are within the estimating scope for professional design deliverables.
