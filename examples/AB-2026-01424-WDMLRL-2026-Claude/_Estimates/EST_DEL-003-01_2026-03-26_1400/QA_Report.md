# QA Report — EST_DEL-003-01_2026-03-26_1400

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
| Snapshot folder exists: `EST_DEL-003-01_2026-03-26_1400/` | PASS |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| `BASIS_OF_ESTIMATE = RATE_TABLE` | PASS (valid enum value) |
| All Detail.csv Method values = RATE_TABLE | PASS (consistent with basis) |

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| `Run_Context.md` | PRESENT |
| `Summary.md` | PRESENT |
| `QA_Report.md` | PRESENT (this file) |
| `Source_Index.md` | PRESENT |
| `Detail.csv` | PRESENT |
| `WBS_CBS_Matrix.csv` | PRESENT |
| `Decision_Log.md` | PRESENT |
| `Assumptions_Log.md` | PRESENT |
| `Change_Log.md` | PRESENT |

---

## S5 — CSV Schema Integrity

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All Method values valid (RATE_TABLE) | PASS |
| Allowance/parametric convention: milestone lines (DL-005 through DL-012) have Qty=1, Unit=LS, UnitRate=Amount=0 | PASS |
| Row count | 12 lines |
| Lines with Amount = TBD | 0 |

### WBS_CBS_Matrix.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present | PASS |
| Totals reconcile with Detail.csv | PASS (CBS-01: $8,640 + CBS-02: $1,530 = $10,170 TOTAL) |

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
| Critical input gaps | NONE — all LOE hours and rates are sourced from rate tables |
| Material TBDs | N/A — design services deliverable, no materials |
| Assumptions remaining | 3 assumptions logged (see Assumptions_Log.md), all bounded |
| **RUN_STATUS** | **OK** |

---

## Scope Coverage

| Check | Result |
|---|---|
| Deliverables in scope | 1 (DEL-003-01) |
| Deliverables included | 1 |
| Deliverables excluded | 0 |
| Deliverables blocked | 0 |
| Documents read | 4 of 4 (Datasheet, Specification, Guidance, Procedure) |
| Missing documents | 0 |
| Items extracted | 12 (4 priced labour lines + 8 activity/milestone markers) |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Detail.csv | 12 |
| Items priced (Amount > 0) | 4 |
| Items at $0 (milestones, effort included elsewhere) | 8 |
| Items with Amount = TBD | 0 |
| **Pricing Coverage** | **100%** (all items either priced or confirmed as $0 milestones) |

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| Detail.csv Methods used | RATE_TABLE only |
| ALLOW_MIXED_METHODS = TRUE | Not triggered — single method used |
| FALLBACK_POLICY = ALLOW_ALLOWANCE | Not triggered — primary basis sufficient |
| **Basis Consistency** | **PASS** |

---

## Dependency / Blocker Assessment

| Blocker | Status (Prior) | Status (This Run) | Impact |
|---|---|---|---|
| DEP-003-01-011: Natural gas tie-in availability (C-001) | OPEN (gas availability TBD) | RESOLVED (Add. 3, Q8: 2" PVC, 50 PSI confirmed) | Information blocker removed. No cost impact on DEL-003-01 design hours. Downstream heating system sizing can now proceed with known gas supply parameters. |
| DEP-003-01-018: County approval gate | OPEN | OPEN | Execution gate; does not affect estimate pricing. |
| DEP-003-01-021: P.Eng. review | OPEN | OPEN | Covered by assumption A-003 (Mech Eng = P.Eng. of Record). |

---

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK | No unbounded gaps |
| Basis-consistency checks pass | PASS | RATE_TABLE throughout |
| Provenance completeness reported | PASS | 100% |
| Scope coverage explicit | PASS | 1 deliverable (DEL-003-01); exclusions documented |
| No writes outside `_Estimates/` | PASS | All writes quarantined |
| Change vs prior snapshot documented | PASS | See Change_Log.md |

---

## What to Fix for a Cleaner Rerun

1. **Construction value establishment.** Once a construction cost estimate is available, the fee-based cross-check (DF-03 @ 1.6% of construction value) can be completed to validate the rate-table-derived total.
2. **Confidence upgrade.** All rates and hours are MEDIUM confidence. As the project progresses and actuals are available, rates and LOE estimates can be refined to HIGH confidence.
3. **P.Eng. hours separation.** If the P.Eng. of Record is a different person from the Mechanical Engineer (R-15), a separate line item and hours allocation should be added.
