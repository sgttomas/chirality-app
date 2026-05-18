# QA Report — EST_DEL-019-04_2026-02-27_0630

## RUN_STATUS: OK

---

## S1 — Write Quarantine Respected

**PASS.** All outputs written exclusively under `_Estimates/EST_DEL-019-04_2026-02-27_0630/`. No files outside `_Estimates/` were created or modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-019-04_2026-02-27_0630` created under `_Estimates/`.

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
| Row count | 20 items |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | Yes — 6 UNIT_RATE, 14 LUMP_SUM |
| Every row traces to a source document | Yes — all SourceDoc values are one of Datasheet, Specification, Procedure, Guidance |
| Every row has a SourceSection | Yes |
| Qty values | 6 rows with numeric hours; 14 rows with Qty=1 (LS convention) |

### Detail.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | Yes — all 15 columns present |
| Row count | 20 lines |
| Method values valid | Yes — all 20 rows use PARAMETRIC |
| Allowance/parametric convention | Respected — lump-sum items (Qty=1, Unit=LS, UnitRate=Amount) where Amount=0.00 |
| All ItemIDs trace to Items.csv | Yes — 1:1 correspondence |

## S6 — Provenance Discipline

**PASS.**

| Metric | Value |
|---|---|
| Rows with non-TBD SourceRef | 20 / 20 (100%) |
| Rows with `location TBD` | 0 |
| Top missing-source offenders | None |

All priced rows reference specific price source files and row IDs (Professional_Staff_Rates.csv role IDs and Level_of_Effort.csv deliverable/role combinations).

## S7 — Status Reporting

**RUN_STATUS: OK**

Rationale: All items are priced with parametric method using available rate tables and level-of-effort estimates. No TBD amounts. No critical input gaps. Totals are meaningful.

Minor observations (do not affect OK status):
- QA/QC Lead hours (6 hr) appear low relative to the breadth of QC program activities (18 specification requirements, 24 procedure steps, 16 record types); flagged in Summary as a review recommendation.
- Third-party testing costs not captured; applicability TBD pending IFC specifications.
- Acceptance criteria and test method standards TBD pending IFC specifications; may generate additional QC effort once defined.

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK | No unbounded gaps |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 20 items extracted from all 4 documents; covers all priceable scope identified across 18 specification requirements and 24 procedure steps |
| Basis-consistency checks pass | PASS | All 20 Detail.csv rows use Method=PARAMETRIC, consistent with BASIS_OF_ESTIMATE=PARAMETRIC |
| Provenance completeness reported | PASS | 100% of rows have SourceRef |
| Scope coverage explicit | PASS | 1 deliverable (DEL-019-04) in scope; 0 excluded; all 4 documents read successfully |
| No writes outside _Estimates/ | PASS | Confirmed |

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Items Extracted | Missing Documents |
|---|---|---|---|
| DEL-019-04 | 4/4 (Datasheet, Specification, Guidance, Procedure) | 20 | None |

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 20 |
| Items priced in Detail.csv | 20 (100%) |
| Items with Amount > $0 | 6 (30%) |
| Items with Amount = $0 | 14 (70%) — labour absorbed in other line items; no double-counting |
| Items with Amount = TBD | 0 (0%) |

## Basis-Consistency

| Method | Count | % of Detail rows |
|---|---|---|
| PARAMETRIC | 20 | 100% |
| Other methods | 0 | 0% |

Consistent with BASIS_OF_ESTIMATE = PARAMETRIC. No mixed-method deviation.

## What to Fix for a Cleaner Rerun

1. **Review QA/QC Lead hours.** If the 6-hour allocation for R-06 is confirmed as intentional (e.g., representing only initial QC program establishment with ongoing inspection hours allocated to project overhead or other deliverables), no action needed. If the allocation is intended to cover the full construction-phase QC operations, it appears significantly underestimated given the scope breadth (18 requirements, 24 procedure steps, monthly self-assessments, weekly reporting). Update Level_of_Effort.csv and rerun if adjustment needed.

2. **Add third-party testing costs when IFC specifications are available.** Once materials and systems requiring testing are identified, third-party laboratory costs (concrete testing, soil compaction, etc.) should be estimated and added either to DEL-019-04 or to the respective trade packages.

3. **Confirm County notification lead time.** The recommended 48-hour minimum has not been confirmed with the County PM. If a longer lead time is required, coordination effort may increase.

4. **No action required for Fees_Permits_Insurance.csv.** No fees, permits, or insurance costs fall within DEL-019-04 scope.
