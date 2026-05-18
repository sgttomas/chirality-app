# QA Report — EST_DEL-003-07_2026-02-27_0841

## RUN_STATUS: OK

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All outputs written under `_Estimates/EST_DEL-003-07_2026-02-27_0841/` | PASS |
| No files modified outside `_Estimates/` | PASS |

---

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder `EST_DEL-003-07_2026-02-27_0841` exists | PASS |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = `PARAMETRIC` | PASS (valid enum value) |

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
| `Detail.csv` | PRESENT (optional; produced) |

---

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes | PASS (all present) |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Every row has SourceDoc and SourceSection | PASS |
| Row count | 20 items |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes | PASS (all present) |
| Method values valid (PARAMETRIC for all rows) | PASS |
| Allowance/parametric convention: N/A (all rows are UNIT_RATE with real Qty/Unit) | N/A |
| Row count | 4 lines |

### WBS_CBS_Matrix.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns: WBS_PackageID, WBS_DeliverableID, CBS, Currency, Amount_Total, LineCount | PASS |
| Totals reconcile with Detail.csv | PASS (Management: $1,530 + Design: $8,640 = $10,170) |

---

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Detail.csv rows with non-TBD SourceRef | 4 / 4 (100%) |
| Detail.csv rows with `location TBD` | 0 |
| Top missing-source offenders | None |

All priced rows have complete provenance tracing to `Professional_Staff_Rates.csv` (rate source) and `Level_of_Effort.csv` (hours source).

---

## S7 — Status Reporting

| Field | Value |
|---|---|
| **RUN_STATUS** | **OK** |
| Rationale | All line items priced; no TBD amounts; all provenance complete; basis consistency met |

---

## S8 — Operator Acceptance Checklist

| Check | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK |
| Quantity takeoff (Items.csv) reviewed for completeness | 20 items extracted from 4 documents; covers all 15 specification requirements plus coordination/review activities |
| Basis-consistency checks pass | All 4 Detail.csv lines use PARAMETRIC method, matching BASIS_OF_ESTIMATE |
| Provenance completeness reported | 100% (4/4 lines) |
| Scope coverage explicit | 1 deliverable (DEL-003-07); all LOE rows consumed; no excluded scope |
| No writes outside _Estimates/ | Confirmed |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Documents Missing | Items Extracted |
|---|---|---|---|
| DEL-003-07 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | 0 | 20 |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total Items in Items.csv | 20 |
| Items with corresponding Detail.csv lines | 4 (ITEM-001 through ITEM-004 — the billable staff roles) |
| Items that are specification section identifiers (non-additive) | 16 (ITEM-005 through ITEM-020 — specification content sections included in engineering hours) |
| Items priced as TBD | 0 |
| Pricing coverage | 100% of billable items priced |

**Note:** ITEM-005 through ITEM-020 represent individual specification sections (REQ-M-001 through REQ-M-015 and coordination activities) that are included within the Mechanical Engineer's 42 hours (ITEM-004). They are listed in Items.csv for traceability to specification content but are not independently priced in Detail.csv to avoid double-counting.

---

## Basis-Consistency Check

| Method in Detail.csv | Count | % | Consistent with BASIS_OF_ESTIMATE (PARAMETRIC)? |
|---|---|---|---|
| PARAMETRIC | 4 | 100% | YES |

No fallback methods were needed. ALLOW_MIXED_METHODS = TRUE was authorized but not exercised.

---

## What to Fix for a Cleaner Rerun

1. **No critical fixes required.** This is a clean run.
2. **Optional cross-check:** If a construction value estimate for PKG-013 becomes available, the mechanical design fee percentage can be cross-checked against the Professional_Design_Fees.csv benchmark (DF-03: recommended 1.6% of construction value).
3. **Confidence upgrade:** Source rates and hours are MEDIUM confidence. If actual negotiated rates or firmer LOE estimates become available, re-running with those inputs would upgrade to HIGH confidence.
