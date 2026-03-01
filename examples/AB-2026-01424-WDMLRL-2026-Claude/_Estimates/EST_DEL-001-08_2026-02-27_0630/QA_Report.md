# QA Report — EST_DEL-001-08_2026-02-27_0630

## RUN_STATUS: OK

Totals are meaningful. No critical input gaps. All line items priced with full provenance.

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All output files written under `_Estimates/EST_DEL-001-08_2026-02-27_0630/` | PASS |
| No files modified outside `_Estimates/` | PASS |

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder `EST_DEL-001-08_2026-02-27_0630` exists | PASS |

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
| Detail.csv | PRESENT (optional; produced for full run) |
| WBS_CBS_Matrix.csv | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| File is parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to a source document and section | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS — 5 UNIT_RATE rows, 6 LUMP_SUM rows |
| Row count | 11 data rows |

### Detail.csv

| Check | Result |
|---|---|
| File is parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (PARAMETRIC) | PASS — all 5 rows are PARAMETRIC |
| Allowance/parametric convention | N/A — all rows are UNIT_RATE with actual Qty and UnitRate; no lump-sum parametric lines |
| Row count | 5 data rows |
| All ItemID values trace to Items.csv | PASS (ITEM-001 through ITEM-005) |

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows in Detail.csv | 5 |
| Rows with non-TBD SourceRef | 5 (100%) |
| Rows with SourceRef = "location TBD" | 0 (0%) |
| Provenance completeness | **100%** |
| Top missing-source offenders | None |

## S7 — Status Reporting

| Field | Value |
|---|---|
| RUN_STATUS | **OK** |
| Justification | All 5 line items are priced. No TBD amounts. 100% provenance. No critical input gaps. Basis is consistent (all PARAMETRIC). |

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | OK |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 11 items identified from all 4 documents; covers all procedure steps and LOE roles |
| Basis-consistency checks pass | PASS | All 5 Detail.csv rows use Method=PARAMETRIC, matching BASIS_OF_ESTIMATE=PARAMETRIC |
| Provenance completeness reported | PASS | 100% — no gaps |
| Scope coverage explicit | PASS | 1 deliverable in scope (DEL-001-08); all 4 production documents read; 0 missing documents |
| No writes outside _Estimates/ | PASS | Verified |

---

## Quantity Takeoff Coverage

| Source Document | Items Extracted | Notes |
|---|---|---|
| Datasheet | 2 | ITEM-006 (room list — 14 rooms/areas), ITEM-007 (finish selections across 5 categories) |
| Specification | 1 | ITEM-008 (code compliance review — REQ-DS-007a, REQ-DS-008) |
| Procedure | 4 | ITEM-009 (cross-coordination), ITEM-010 (County submission), ITEM-011 (IFC issue), plus labour items ITEM-001 through ITEM-005 mapped to procedure steps |
| Guidance | 0 direct items | Guidance informed finish category selections but did not generate distinct priceable items |

## Pricing Coverage

| Metric | Value |
|---|---|
| Items in Items.csv | 11 |
| Items with corresponding Detail.csv lines | 5 (ITEM-001 through ITEM-005, the labour LOE items) |
| Items not separately priced (scope traceability only) | 6 (ITEM-006 through ITEM-011 — work activities covered by labour LOE; not separately priced to avoid double-counting) |
| % of cost captured | 100% of design labour cost |
| TBD amounts | 0 |

## Basis-Consistency

| Method | Line Count | Amount (CAD) | % of Total |
|---|---|---|---|
| PARAMETRIC | 5 | $7,420.00 | 100% |
| Other | 0 | $0.00 | 0% |
| **Consistent with BASIS_OF_ESTIMATE=PARAMETRIC** | **YES** | | |

## What to Fix for a Cleaner Rerun

- No issues identified. This is a clean run.
- If future runs require greater granularity, the 6 scope-traceability items (ITEM-006 through ITEM-011) could be broken into sub-tasks with independent LOE, but this would require a more detailed LOE model than currently available in the price sources.
