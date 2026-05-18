# QA Report — EST_DEL-019-01_2026-02-27_0600

## RUN_STATUS: OK

---

## S1 — Write Quarantine Respected

**PASS.** All outputs written exclusively under `_Estimates/EST_DEL-019-01_2026-02-27_0600/`. No files outside `_Estimates/` were created or modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-019-01_2026-02-27_0600` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required files present:

| File | Status |
|---|---|
| `Run_Context.md` | Present |
| `Items.csv` | Present |
| `Summary.md` | Present |
| `QA_Report.md` | Present (this file) |
| `Source_Index.md` | Present |
| `Decision_Log.md` | Present |
| `Assumptions_Log.md` | Present |
| `WBS_CBS_Matrix.csv` | Present |
| `Detail.csv` | Present (optional; produced) |

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | Yes — all 9 columns present |
| Row count | 16 items |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | Yes — 6 UNIT_RATE, 10 LUMP_SUM |
| Every row traces to a source document | Yes — all SourceDoc values are one of Datasheet, Specification, Procedure |
| Every row has a SourceSection | Yes |
| Qty values | 6 rows with numeric hours; 10 rows with Qty=1 (LS convention) |

### Detail.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | Yes — all 15 columns present |
| Row count | 16 lines |
| Method values valid | Yes — all 16 rows use PARAMETRIC |
| Allowance/parametric convention | Respected — lump-sum items (Qty=1, Unit=LS, UnitRate=Amount) where Amount=0.00 |
| All ItemIDs trace to Items.csv | Yes — 1:1 correspondence |

## S6 — Provenance Discipline

**PASS.**

| Metric | Value |
|---|---|
| Rows with non-TBD SourceRef | 16 / 16 (100%) |
| Rows with `location TBD` | 0 |
| Top missing-source offenders | None |

All priced rows reference specific price source files and row IDs (Professional_Staff_Rates.csv role IDs and Level_of_Effort.csv deliverable/role combinations).

## S7 — Status Reporting

**RUN_STATUS: OK**

Rationale: All items are priced with parametric method using available rate tables and level-of-effort estimates. No TBD amounts. No critical input gaps. Totals are meaningful.

Minor observations (do not affect OK status):
- HSE Manager hours (4 hr) appear low relative to deliverable scope breadth; flagged in Summary as a review recommendation.
- Insurance premiums are correctly excluded (PKG-021 scope) but noted for boundary clarity.

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK | No unbounded gaps |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 16 items extracted from all 4 documents; covers all priceable scope identified |
| Basis-consistency checks pass | PASS | All 16 Detail.csv rows use Method=PARAMETRIC, consistent with BASIS_OF_ESTIMATE=PARAMETRIC |
| Provenance completeness reported | PASS | 100% of rows have SourceRef |
| Scope coverage explicit | PASS | 1 deliverable (DEL-019-01) in scope; 0 excluded; all 4 documents read successfully |
| No writes outside _Estimates/ | PASS | Confirmed |

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Items Extracted | Missing Documents |
|---|---|---|---|
| DEL-019-01 | 4/4 (Datasheet, Specification, Guidance, Procedure) | 16 | None |

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 16 |
| Items priced in Detail.csv | 16 (100%) |
| Items with Amount > $0 | 6 (37.5%) |
| Items with Amount = $0 | 10 (62.5%) — labour absorbed in other line items; no double-counting |
| Items with Amount = TBD | 0 (0%) |

## Basis-Consistency

| Method | Count | % of Detail rows |
|---|---|---|
| PARAMETRIC | 16 | 100% |
| Other methods | 0 | 0% |

Consistent with BASIS_OF_ESTIMATE = PARAMETRIC. No mixed-method deviation.

## What to Fix for a Cleaner Rerun

1. **Review HSE Manager hours.** If the 4-hour allocation for R-05 is confirmed as intentional (e.g., additional hours allocated to DEL-019-02 through DEL-019-04), no action needed. If underestimated, update Level_of_Effort.csv and rerun.
2. **Confirm landfill-specific hazard assessment effort.** The 3 TBD hazard categories in the Datasheet (waste gas, heavy equipment interaction, access/egress) may require specialized assessment hours not currently reflected in Level_of_Effort.csv.
3. **No action required for insurance premiums.** Correctly excluded from DEL-019-01 scope; tracked under PKG-021.
