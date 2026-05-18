# QA Report — EST_DEL-003-05_2026-02-27_0833

**RunID:** EST_DEL-003-05_2026-02-27_0833
**AsOf:** 2026-02-27T08:33Z
**RUN_STATUS: OK**

---

## S1 — Write Quarantine Respected

**PASS.** All output files written exclusively under `_Estimates/EST_DEL-003-05_2026-02-27_0833/`. No files outside the estimating tool root were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-003-05_2026-02-27_0833` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value. Parametric method applied using Level_of_Effort.csv hours and Professional_Staff_Rates.csv rates.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts produced:
- [x] Run_Context.md
- [x] Items.csv
- [x] Detail.csv
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv

## S5 — CSV Schema Integrity

### Items.csv
**PASS.**
- Columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes — all 9 required columns present.
- Row count: 10 items.
- PricingMode values: UNIT_RATE (7 rows), LUMP_SUM (3 rows) — all valid enum values.
- Lump-sum convention: ITEM-008/009/010 have Qty=1, Unit=LS — compliant.
- All rows have SourceDoc and SourceSection populated — no blanks.
- No TBD quantities: all quantities are numeric.

### Detail.csv
**PASS.**
- Columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes — all 15 required columns present.
- Row count: 10 lines.
- Method values: PARAMETRIC (10 rows) — all valid; consistent with BASIS_OF_ESTIMATE.
- Allowance/parametric convention for LS items: L-008/009/010 have Qty=1, Unit=LS, UnitRate=Amount=0.00 — compliant (these are zero-cost consolidation items).
- All amounts are numeric; no TBD values.

## S6 — Provenance Discipline

**PASS.**
- Provenance completeness: 10 of 10 lines (100%) have non-TBD SourceRef values.
- All SourceRef values point to specific pricing source files (Professional_Staff_Rates.csv and Level_of_Effort.csv) with row/role identifiers.
- No `location TBD` entries.
- Top missing-source offenders: None.

## S7 — Status Reporting

**RUN_STATUS: OK**
- All items priced with meaningful totals.
- No TBD amounts.
- Provenance completeness: 100%.
- Basis consistency: 100% PARAMETRIC (matches BASIS_OF_ESTIMATE).
- Warnings exist (W-001 through W-003) but are informational: they note that the estimate covers design labour only, not equipment procurement or installation — this is a limitation of the available price sources, not a gap in the estimate within its defined scope.

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK | Status is OK; warnings are informational |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 10 items extracted from 4 deliverable documents covering all 3 production phases, equipment register, coordination, and QC |
| Basis-consistency checks pass | PASS | 100% PARAMETRIC method; no mixed methods required |
| Provenance completeness reported | PASS | 100% — all lines have SourceRef |
| Scope coverage explicit | PASS | 1 deliverable in scope, 1 estimated; 10/10 items priced |
| No writes outside _Estimates/ | PASS | Confirmed |

---

## Quantity Takeoff Coverage

| Document | Items Extracted | Notes |
|---|---|---|
| Datasheet.md | 1 (ITEM-007: equipment register population) | Equipment register contains 8 equipment types (HTG-001 through CF-006); work effort to populate is captured |
| Specification.md | 2 (ITEM-008: County review coordination; ITEM-010: P.Eng. stamp) | 17 requirements identified; priceable activities extracted |
| Guidance.md | 0 direct items | Guidance informs design considerations but does not add discrete priceable items beyond those in Procedure |
| Procedure.md | 7 (ITEM-001 through ITEM-006, ITEM-009) | 3 production phases with 14 steps; all phases covered by allocated professional hours |

## Pricing Coverage

- Items priced: 10 of 10 (100%)
- Items with TBD amounts: 0 of 10 (0%)
- Total amount: $7,290.00 CAD
- Method mix: 100% PARAMETRIC

## Basis-Consistency Check

| Method | Line Count | Amount | Percentage |
|---|---|---|---|
| PARAMETRIC | 10 | $7,290.00 | 100% |
| TOTAL | 10 | $7,290.00 | 100% |

BASIS_OF_ESTIMATE = PARAMETRIC. All lines use PARAMETRIC method. No fallback required. **CONSISTENT.**

---

## What to Fix for a Cleaner Rerun

1. **No critical fixes required.** The estimate is internally consistent and fully priced.
2. If construction value becomes established (for the overall project), a cross-check using the Professional_Design_Fees.csv percentage method (DF-03: 1.6% of construction value for mechanical design) would provide a useful benchmark against the LOE-based estimate.
3. If equipment procurement pricing sources are added to PRICE_SOURCES in a future run, additional line items for equipment capital costs could be extracted from the Datasheet equipment register (8 equipment types, all with TBD performance and pricing in current documents).
