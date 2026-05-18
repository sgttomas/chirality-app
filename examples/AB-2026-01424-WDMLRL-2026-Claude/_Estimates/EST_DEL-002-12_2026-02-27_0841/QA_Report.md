# QA Report — EST_DEL-002-12_2026-02-27_0841

## RUN_STATUS: OK

---

## S1 — Write Quarantine

| Check | Result |
|---|---|
| All outputs written under _Estimates/ only | PASS |
| No modifications to deliverable working files | PASS |
| No modifications to lifecycle files (_STATUS.md) | PASS |
| No modifications to decomposition outputs | PASS |
| No modifications to dependency registers | PASS |

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder EST_DEL-002-12_2026-02-27_0841 exists | PASS |

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = PARAMETRIC | PASS (valid enum value) |

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Items.csv | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Detail.csv | PRESENT (optional; produced) |
| WBS_CBS_Matrix.csv | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes | PASS — all present |
| All rows trace to a source document and section | PASS — 13 rows, all with SourceDoc and SourceSection |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS — 4 UNIT_RATE, 9 LUMP_SUM |
| Row count | 13 items (4 priced staff lines + 9 procedural activity items included in staff hours) |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes | PASS — all present |
| Method values valid | PASS — all PARAMETRIC |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount) | N/A — all items are UNIT_RATE with explicit Qty and Unit |
| Row count | 4 priced lines |

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows in Detail.csv | 4 |
| Rows with non-TBD SourceRef | 4 |
| Provenance completeness | **100%** |
| Top missing-source offenders | None |

All 4 priced rows reference both a rate source file (Professional_Staff_Rates.csv) and an hours source file (Level_of_Effort.csv) with specific row identifiers.

## S7 — Status Reporting

| Criterion | Assessment |
|---|---|
| Totals meaningful? | YES — $10,380.00 CAD total across 4 priced lines |
| Critical input gaps? | NO — all four documents present; all price sources accessible and used |
| Material TBDs/assumptions? | NO TBD amounts. Assumptions documented but non-blocking |
| **RUN_STATUS** | **OK** |

## Quantity Takeoff Coverage

| Deliverable | Documents Present | Documents Missing | Items Extracted |
|---|---|---|---|
| DEL-002-12 | Datasheet.md, Specification.md, Guidance.md, Procedure.md | None | 13 (4 staff lines + 9 procedural activity items) |

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 13 |
| Items with pricing in Detail.csv | 4 (staff effort lines; procedural items ITM-005 through ITM-013 are sub-activities included within staff hours, not independently priced) |
| Items with Amount = TBD | 0 |
| Pricing coverage | **100%** of independent priceable items |

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (4/4 lines) |
| Method mix consistent with basis? | PASS — 100% PARAMETRIC |
| ALLOW_MIXED_METHODS = TRUE | Enabled but not needed; all lines match basis |
| FALLBACK_POLICY = ALLOW_PARAMETRIC | Enabled but not exercised; all lines priced from primary sources |

## What to Fix for a Cleaner Rerun

1. **Nothing critical.** This run is clean with OK status.
2. **Optional enhancement:** If construction value becomes available, a cross-check against Professional_Design_Fees.csv (DF-02: Structural design fee at 1.8% of construction value) could validate the LOE-based total.
3. **Confidence upgrade path:** Rates and hours are MEDIUM confidence. To upgrade to HIGH, obtain actual contracted rates from the Structural Engineer's firm and task-level time estimates based on their standard practice for a similar-scope specification.
