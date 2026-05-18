# QA Report — EST_DEL-001-10_2026-02-27_0600

## RUN_STATUS: OK

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All files written under `_Estimates/EST_DEL-001-10_2026-02-27_0600/` only | PASS |
| No files modified outside `_Estimates/` | PASS |

---

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder `EST_DEL-001-10_2026-02-27_0600` exists | PASS |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| `BASIS_OF_ESTIMATE` = `PARAMETRIC` | PASS (valid enum value) |

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| `Run_Context.md` | PRESENT |
| `Items.csv` | PRESENT |
| `Summary.md` | PRESENT |
| `QA_Report.md` | PRESENT (this file) |
| `Source_Index.md` | PRESENT |
| `Decision_Log.md` | PRESENT |
| `Assumptions_Log.md` | PRESENT |
| `WBS_CBS_Matrix.csv` | PRESENT |
| `Detail.csv` (optional, recommended) | PRESENT |

---

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| File is parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows have valid PricingMode (UNIT_RATE or LUMP_SUM) | PASS |
| All rows trace to a SourceDoc and SourceSection | PASS |
| Row count | 12 items |
| Lump-sum convention (Qty=1, Unit=LS for LUMP_SUM rows) | PASS (ITM-006 through ITM-012) |

### Detail.csv

| Check | Result |
|---|---|
| File is parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All Method values valid (PARAMETRIC) | PASS |
| All rows have ItemID tracing back to Items.csv | PASS |
| Row count | 5 priced lines |
| Allowance/parametric convention | N/A — all lines are UNIT_RATE with explicit Qty and UnitRate |

---

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows in Detail.csv | 5 |
| Rows with non-TBD SourceRef | 5 (100%) |
| Rows with `location TBD` SourceRef | 0 |
| **Provenance completeness** | **100%** |

### Top Missing-Source Offenders

None. All priced rows have complete provenance referencing both Professional_Staff_Rates.csv (for rate) and Level_of_Effort.csv (for hours).

---

## S7 — Status Reporting

| Field | Value |
|---|---|
| **RUN_STATUS** | **OK** |
| Rationale | All items priced; no TBD amounts; 100% provenance; basis-consistent (all PARAMETRIC); no critical input gaps |

---

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | RUN_STATUS = OK |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 12 items extracted covering all 5 SOW items; 5 priced labor lines + 7 scope-descriptive items embedded in labor hours |
| Basis-consistency checks pass | PASS | All 5 Detail.csv lines use Method=PARAMETRIC, matching BASIS_OF_ESTIMATE |
| Provenance completeness reported and gaps actionable | PASS | 100% provenance; no gaps |
| Scope coverage explicit | PASS | 1 deliverable in scope (DEL-001-10); 0 excluded; all 4 documents read |
| No writes outside _Estimates/ | PASS | Verified |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Found | Documents Missing | Items Extracted |
|---|---|---|---|
| DEL-001-10 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | 0 | 12 |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 12 |
| Items with corresponding priced lines in Detail.csv | 5 (labor items ITM-001 through ITM-005) |
| Items described as scope-embedded in labor hours (no separate pricing) | 7 (ITM-006 through ITM-012) |
| Items with Amount=TBD | 0 |
| **Pricing coverage** | **100% of priceable items** |

Note: Items ITM-006 through ITM-012 are scope-descriptive items (field survey, preliminary design, IFC production, discipline coordination, code review, demolition coordination, QA review) whose effort is embedded in the 130 labor hours distributed across the 5 priced roles. They are not separately priced to avoid double-counting.

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = PARAMETRIC | PASS |
| All Detail.csv Method values = PARAMETRIC | PASS |
| Mixed methods used? | NO (all PARAMETRIC) |
| ALLOW_MIXED_METHODS = TRUE but not exercised | N/A |
| FALLBACK_POLICY = ALLOW_PARAMETRIC (not exercised; primary basis sufficient) | N/A |

---

## What to Fix for a Cleaner Rerun

1. **No critical fixes required.** This run produced complete, fully-sourced outputs.
2. **Optional enhancement:** Break out ITM-006 through ITM-012 as separately priced items if the estimator wants more granular cost allocation across activities (currently embedded in labor hours).
3. **Optional enhancement:** Add a renovation-specific parametric building rate to Parametric_Building_Rates.csv to enable a construction cost cross-check for the renovation scope (currently only new-build rates are available).
4. **Data dependency:** If the Old North Shop field survey reveals significantly different existing conditions from the Appendix B conceptual plan, the LOE hours may need adjustment. Consider a rerun after survey completion.
