# QA Report — EST_DEL-020-03_2026-02-27_0900

## RUN_STATUS: OK

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All outputs written under `_Estimates/` | PASS |
| No deliverable content modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition outputs modified | PASS |

---

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists: `EST_DEL-020-03_2026-02-27_0900/` | PASS |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = `PARAMETRIC` | PASS (valid enum) |

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Items.csv | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Detail.csv | PRESENT (optional; produced) |

---

## S5 — CSV Schema Integrity

### Items.csv

| Column | Present | Valid |
|---|---|---|
| ItemID | Yes | ITEM-001 through ITEM-008 (unique) |
| DeliverableID | Yes | All = DEL-020-03 |
| Description | Yes | Non-empty for all rows |
| Qty | Yes | Numeric for all rows (no TBD values) |
| Unit | Yes | All = hr |
| PricingMode | Yes | All = UNIT_RATE (valid enum) |
| SourceDoc | Yes | Procedure (6), Specification (1), Datasheet (0), Guidance (0) |
| SourceSection | Yes | Non-empty for all rows |
| Notes | Yes | Non-empty for all rows |

**Result:** PASS — 8 rows, all columns present, all values valid.

### Detail.csv

| Column | Present | Valid |
|---|---|---|
| LineID | Yes | L-001 through L-008 (unique) |
| ItemID | Yes | Maps to Items.csv ITEM-001 through ITEM-008 |
| CBS | Yes | Management / Construction / Admin / Specialty |
| WBS_PackageID | Yes | All = PKG-020 |
| WBS_DeliverableID | Yes | All = DEL-020-03 |
| Description | Yes | Non-empty |
| Qty | Yes | Numeric (no TBD) |
| Unit | Yes | All = hr |
| UnitRate | Yes | Numeric (no TBD) |
| Amount | Yes | Numeric (Qty x UnitRate verified) |
| Currency | Yes | All = CAD |
| Method | Yes | All = PARAMETRIC (valid enum) |
| SourceRef | Yes | All reference specific CSV source files and role IDs |
| Confidence | Yes | All = MED |
| Notes | Yes | Non-empty |

**Result:** PASS — 8 rows, all columns present, all values valid.

---

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows | 8 |
| Rows with SourceRef | 8 |
| Rows with `location TBD` SourceRef | 0 |
| **Provenance completeness** | **100%** |

**Top missing-source offenders:** None. All rows have complete provenance.

---

## S7 — Status Reporting

| Check | Result |
|---|---|
| Totals meaningful? | Yes — $11,290.00 CAD |
| Critical input gaps? | No |
| TBD amounts? | 0 of 8 lines |
| **RUN_STATUS** | **OK** |

---

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK | No gaps |
| Items.csv reviewed for completeness | 8 items extracted from 4 documents + LOE | All Level_of_Effort rows for DEL-020-03 represented |
| Basis-consistency checks pass | PASS | All 8 lines use PARAMETRIC method; matches BASIS_OF_ESTIMATE |
| Provenance completeness reported | 100% | No missing sources |
| Scope coverage explicit | 1 deliverable in scope; 1 deliverable estimated | Full coverage |
| No writes outside _Estimates/ | Confirmed | Write quarantine respected |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Items Extracted | Missing Documents |
|---|---|---|---|
| DEL-020-03 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | 8 | None |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Items priced | 8 of 8 (100%) |
| Items TBD | 0 |
| Total amount | $11,290.00 CAD |

---

## Basis-Consistency Check

| Metric | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Lines using PARAMETRIC | 8 of 8 (100%) |
| Lines using other methods | 0 |
| ALLOW_MIXED_METHODS | TRUE (not exercised; no mixed methods needed) |
| **Consistency** | **PASS** |

---

## What to Fix for a Cleaner Rerun

1. **No critical fixes required.** All items are fully priced with complete provenance.
2. **Minor enhancement:** The Level_of_Effort.csv notes column for DEL-020-03 rows shows "PKG-020 TBD -- TBD" suggesting the sub-category within PKG-020 was not fully resolved at LOE preparation time. This has no impact on pricing but could be refined for traceability.
3. **Scope clarity:** The broader closeout scope (as-builts, O&M manuals, warranty docs) is ASSUMPTION-based per _CONTEXT.md. Human confirmation would move these from ASSUMPTION to confirmed scope.
4. **Confidence upgrade:** Both rates and hours are MEDIUM confidence. Firming up effort estimates based on actual project complexity would increase confidence.
