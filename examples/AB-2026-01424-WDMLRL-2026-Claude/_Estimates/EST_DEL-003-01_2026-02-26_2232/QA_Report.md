# QA Report — EST_DEL-003-01_2026-02-26_2232

**RUN_STATUS: OK**

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All outputs written under `_Estimates/` | PASS |
| No files outside `_Estimates/` modified | PASS |

---

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists: `EST_DEL-003-01_2026-02-26_2232/` | PASS |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| `BASIS_OF_ESTIMATE = PARAMETRIC` | PASS (valid enum value) |
| All Detail.csv Method values = PARAMETRIC | PASS (consistent with basis) |

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| `Run_Context.md` | PRESENT |
| `Items.csv` | PRESENT |
| `Summary.md` | PRESENT |
| `QA_Report.md` | PRESENT (this file) |
| `Source_Index.md` | PRESENT |
| `Detail.csv` | PRESENT (optional but produced) |
| `WBS_CBS_Matrix.csv` | PRESENT |
| `Decision_Log.md` | PRESENT |
| `Assumptions_Log.md` | PRESENT |

---

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Every row has SourceDoc and SourceSection | PASS |
| Row count | 12 items |
| Items with Qty = TBD | 0 |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All Method values valid (PARAMETRIC) | PASS |
| Allowance/parametric convention: milestone lines (DL-005 through DL-012) have Qty=1, Unit=LS, UnitRate=Amount=0 | PASS |
| Row count | 12 lines |
| Lines with Amount = TBD | 0 |

---

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total Detail.csv rows | 12 |
| Rows with non-TBD SourceRef | 12 (100%) |
| Rows with SourceRef = "location TBD" | 0 |
| **Provenance Completeness** | **100%** |

Top missing-source offenders: None.

---

## S7 — Status Reporting

| Criterion | Assessment |
|---|---|
| Totals meaningful | YES — $10,170 CAD total from 70 labour hours across 4 roles |
| Critical input gaps | NONE — all LOE hours and rates are sourced |
| Material TBDs | N/A — design services deliverable, no materials |
| Assumptions remaining | 3 assumptions logged (see Assumptions_Log.md), all bounded |
| **RUN_STATUS** | **OK** |

---

## Quantity Takeoff Coverage

| Check | Result |
|---|---|
| Deliverables in scope | 1 (DEL-003-01) |
| Documents read | 4 of 4 (Datasheet, Specification, Guidance, Procedure) — all present |
| Missing documents | 0 |
| Items extracted | 12 (4 priced labour lines + 8 activity/milestone markers) |
| Items with Qty = TBD | 0 |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 12 |
| Items priced (Amount > 0) | 4 |
| Items at $0 (milestones, effort included elsewhere) | 8 |
| Items with Amount = TBD | 0 |
| **Pricing Coverage** | **100%** (all items either priced or confirmed as $0 milestones) |

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Detail.csv Methods used | PARAMETRIC only |
| ALLOW_MIXED_METHODS = TRUE | Not triggered — single method used |
| FALLBACK_POLICY = ALLOW_PARAMETRIC | Not triggered — primary basis sufficient |
| **Basis Consistency** | **PASS** |

---

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK | No unbounded gaps |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 12 items extracted from 4 documents |
| Basis-consistency checks pass | PASS | PARAMETRIC throughout |
| Provenance completeness reported | PASS | 100% |
| Scope coverage explicit | PASS | 1 deliverable (DEL-003-01); exclusions documented |
| No writes outside `_Estimates/` | PASS | All writes quarantined |

---

## What to Fix for a Cleaner Rerun

1. **Construction value establishment.** Once a construction cost estimate is available, the fee-based cross-check (DF-03 @ 1.6% of construction value) can be completed to validate the LOE-derived total.
2. **Confidence upgrade.** All rates and hours are MEDIUM confidence. As the project progresses and actuals are available, rates and LOE estimates can be refined to HIGH confidence.
3. **P.Eng. hours separation.** If the P.Eng. of Record is a different person from the Mechanical Engineer (R-15), a separate line item and hours allocation should be added.
