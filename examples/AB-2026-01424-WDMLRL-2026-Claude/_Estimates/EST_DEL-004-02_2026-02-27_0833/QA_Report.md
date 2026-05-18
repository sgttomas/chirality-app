# QA Report — EST_DEL-004-02_2026-02-27_0833

**RunID:** EST_DEL-004-02_2026-02-27_0833
**Scope:** DEL-004-02 (Single-Line Diagram)
**As Of:** 2026-02-27

---

## RUN_STATUS: WARNINGS

**Rationale:** All line items are priced (100% pricing coverage, 0% TBD amounts). However, all pricing is based on PARAMETRIC sources at MEDIUM confidence, and multiple TBD design inputs in the source engineering documents introduce effort uncertainty.

---

## S1 — Write Quarantine Respected

**PASS.** All outputs written under `_Estimates/EST_DEL-004-02_2026-02-27_0833/`. No files outside `_Estimates/` were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-004-02_2026-02-27_0833` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts present:
- [x] Run_Context.md
- [x] Items.csv
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv
- [x] Detail.csv (recommended; produced)

## S5 — CSV Schema Integrity

### Items.csv
**PASS.**
- Columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes
- 16 rows; all rows have valid PricingMode (UNIT_RATE or LUMP_SUM)
- All rows trace to a source document (Procedure or Specification) and section
- No TBD quantities in labor lines (ITEM-001 through ITEM-004); activity lines (ITEM-005 through ITEM-016) use Qty=1, Unit=LS

### Detail.csv
**PASS.**
- Columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- 16 rows; all Method values = PARAMETRIC (valid enum)
- Allowance/parametric convention: activity lines (L-005 through L-016) with zero cost set Qty=1, Unit=LS, UnitRate=0.00, Amount=0.00 — convention respected for zero-cost traceability lines
- Priced lines (L-001 through L-004) have Qty=hours, Unit=hr, UnitRate=hourly rate, Amount=Qty*UnitRate — correct

## S6 — Provenance Discipline

**PASS.**
- **Provenance completeness:** 100% (16/16 rows have non-TBD SourceRef)
- All priced lines (L-001 through L-004) reference both Professional_Staff_Rates.csv (role ID) and Level_of_Effort.csv (deliverable/role combination)
- Activity lines (L-005 through L-016) reference Level_of_Effort.csv with note that effort is included in parent labor lines
- **Top missing-source offenders:** None

## S7 — Status Reporting

**RUN_STATUS: WARNINGS**

Declared in this report and in Summary.md. Rationale:
- All items priced (0% TBD amounts) — meets OK threshold for pricing coverage
- Downgraded to WARNINGS because:
  - All rates and hours are PARAMETRIC at MEDIUM confidence (no firm quotes)
  - Source engineering documents contain multiple TBD items (crane ratings, system voltage, overhead door specs, mechanical equipment specs) that could cause actual effort to deviate from estimate

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS — gaps are clearly bounded (confidence level + TBD design inputs) |
| Items.csv reviewed for completeness | PASS | 16 items covering all procedure steps, specification requirements, and role allocations |
| Basis-consistency checks pass | PASS | All 16 lines use Method=PARAMETRIC, consistent with BASIS_OF_ESTIMATE=PARAMETRIC |
| Provenance completeness reported | PASS | 100% provenance; no gaps |
| Scope coverage explicit | PASS | 1 deliverable (DEL-004-02) in scope; 1 deliverable estimated |
| No writes outside _Estimates/ | PASS | Confirmed |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Documents Missing | Items Extracted |
|---|---|---|---|
| DEL-004-02 | 4/4 (Datasheet, Specification, Guidance, Procedure) | 0 | 16 |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 16 |
| Items with Amount > 0 in Detail.csv | 4 (labor lines) |
| Items with Amount = 0 in Detail.csv | 12 (activity traceability lines — effort included in labor lines) |
| Items with Amount = TBD | 0 |
| **Pricing coverage** | **100%** |

---

## Basis-Consistency Check

| Method | Count | Percentage |
|---|---|---|
| PARAMETRIC | 16 | 100% |
| Other | 0 | 0% |

**Consistent with BASIS_OF_ESTIMATE = PARAMETRIC.** No fallback methods used.

---

## What to Fix for a Cleaner Rerun

1. **Obtain firm rate quotes** for Electrical Engineer, BIM Technician, and PM roles to move from PARAMETRIC/MEDIUM to QUOTE/HIGH confidence.
2. **Resolve TBD design inputs** (crane circuit ratings, system voltage, overhead door specs, mechanical equipment ratings) before re-estimating — these may increase Electrical Engineer hours if resolution requires multiple design iterations.
3. **Validate LOE hours against historical data** for comparable Alberta industrial SLD projects to improve confidence from MEDIUM to HIGH.
4. **Cross-check against Professional_Design_Fees.csv** — if a total construction value is established, the fee-percentage model can serve as an independent validation of the LOE total.
