# QA Report — EST_DEL-007-01_2026-02-27_0546

## RUN_STATUS: OK

Totals are meaningful; no critical input gaps. All items are fully priced with traceable provenance.

---

## S1 — Write Quarantine Respected

**PASS.** All output files written exclusively under `_Estimates/EST_DEL-007-01_2026-02-27_0546/`. No files outside the estimating tool root were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-007-01_2026-02-27_0546` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required files present:
- [x] Run_Context.md
- [x] Items.csv
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv
- [x] Detail.csv (optional but produced)

## S5 — CSV Schema Integrity

### Items.csv
**PASS.**
- Columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes (all 9 required columns)
- 3 rows; all parseable
- PricingMode values: all `UNIT_RATE` (valid enum)
- All rows trace to a SourceDoc (Procedure) and SourceSection
- No TBD quantities

### Detail.csv
**PASS.**
- Columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes (all 15 required columns)
- 3 rows; all parseable
- Method values: all `PARAMETRIC` (valid enum; consistent with BASIS_OF_ESTIMATE)
- No allowance/parametric convention violations (all items are UNIT_RATE with actual quantities)
- Amount = Qty x UnitRate for all rows (verified):
  - DL-001: 70 x 135.00 = 9,450.00 (correct)
  - DL-002: 6 x 165.00 = 990.00 (correct)
  - DL-003: 4 x 135.00 = 540.00 (correct)

## S6 — Provenance Discipline

**PASS.**
- Provenance completeness: **100%** (3/3 rows have non-TBD SourceRef)
- All SourceRef values point to specific source files (Level_of_Effort.csv row + Professional_Staff_Rates.csv role)
- No missing-source offenders

## S7 — Status Reporting

**RUN_STATUS: OK**
- Totals are meaningful ($10,980.00 CAD)
- No critical input gaps
- No TBD amounts
- No fallback pricing used

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|-------|--------|-------|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK | Status is OK |
| Items.csv reviewed for completeness | PASS | 3 items covering all LOE roles allocated to DEL-007-01 |
| Basis-consistency checks pass | PASS | All methods are PARAMETRIC; matches BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% (3/3) |
| Scope coverage explicit | PASS | 1 deliverable (DEL-007-01); 0 excluded; 4/4 documents read |
| No writes outside _Estimates/ | PASS | Verified |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Documents Missing | Items Extracted |
|-------------|---------------|-------------------|-----------------|
| DEL-007-01 | 4/4 (Datasheet, Specification, Guidance, Procedure) | 0 | 3 |

**Note:** DEL-007-01 is a design presentation deliverable. The engineering content describes professional design activities (not physical construction items). The 3 priceable items correspond to the 3 roles assigned in the Level_of_Effort model, covering all design, management, and estimating labour for this deliverable.

## Pricing Coverage

| Metric | Value |
|--------|-------|
| Total items in Items.csv | 3 |
| Items priced (non-TBD Amount in Detail.csv) | 3 |
| Items with TBD Amount | 0 |
| **Pricing coverage** | **100%** |

## Basis Consistency

| Method | Count | % |
|--------|-------|---|
| PARAMETRIC | 3 | 100% |

All items use the primary BASIS_OF_ESTIMATE (PARAMETRIC). No mixed methods. No fallback methods used.

## What to Fix for a Cleaner Rerun

Nothing. This run is clean and complete. All items fully priced, all provenance traceable, all schemas valid.

Potential improvements for future runs:
- If Professional_Design_Fees.csv is extended to include a Landscape Architect fee line, a cross-check between the LOE-based estimate and the fee-percentage method could provide a reasonableness benchmark.
- Staff rate confidence is MEDIUM; if firm-specific rates become available, re-run with RATE_TABLE basis for higher confidence.
