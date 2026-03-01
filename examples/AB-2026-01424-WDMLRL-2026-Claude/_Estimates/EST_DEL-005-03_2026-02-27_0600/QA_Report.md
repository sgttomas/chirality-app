# QA Report — EST_DEL-005-03_2026-02-27_0600

## RUN_STATUS: OK

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All output files written under _Estimates/ | PASS |
| No files outside _Estimates/ modified | PASS |

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder EST_DEL-005-03_2026-02-27_0600 exists | PASS |

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
| File is parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS — all 13 rows are LUMP_SUM |
| Every row traces to a source document and section | PASS — all 13 rows have SourceDoc and SourceSection populated |
| Row count | 13 items |

### Detail.csv

| Check | Result |
|---|---|
| File is parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All Method values valid (PARAMETRIC) | PASS — 100% PARAMETRIC |
| Allowance/parametric convention respected | PASS — Qty=1, Unit=LS, UnitRate=Amount for $0 lump sum lines; hour-based lines use actual hours |
| Row count | 14 lines |

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows (Amount > 0) | 8 of 14 |
| Rows with non-TBD SourceRef | 14 of 14 (100%) |
| Provenance completeness | **100%** |
| Top missing-source offenders | None |

All 14 lines in Detail.csv have SourceRef values pointing to specific price source files (PS-1 and PS-2) with role IDs and rates.

## S7 — Status Reporting

| Field | Value |
|---|---|
| RUN_STATUS | **OK** |
| Rationale | All items are priced with parametric basis evidence from Level_of_Effort.csv and Professional_Staff_Rates.csv. No TBD amounts. Total is meaningful ($18,390.00 CAD). |

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS — OK | |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 13 items extracted from all 4 documents; covers Phases A-E plus specific requirements |
| Basis-consistency checks pass | PASS | 100% PARAMETRIC; consistent with BASIS_OF_ESTIMATE=PARAMETRIC |
| Provenance completeness reported | PASS | 100% provenance; all lines trace to PS-1 and PS-2 |
| Scope coverage explicit | PASS | 1 deliverable (DEL-005-03) included; scope exclusions listed in Specification (DEL-005-02, DEL-005-04, DEL-005-05, DEL-005-06, DEL-005-07, PKG-018, etc.) |
| No writes outside _Estimates/ | PASS | |

## Quantity Takeoff Coverage

| Source Document | Items Extracted | Notes |
|---|---|---|
| Datasheet.md | 2 (ITEM-006, ITEM-007) | PM and estimator support items derived from role/condition context |
| Specification.md | 6 (ITEM-008 through ITEM-013) | Requirement-level items (REQ-001 through REQ-008); priced at $0 as effort is included in Procedure phase items |
| Guidance.md | 1 (ITEM-012) | Stormwater detention/retention trade-off consideration |
| Procedure.md | 5 (ITEM-001 through ITEM-005) | Phase A-E work activities — primary cost-bearing items |
| **Total** | **13 unique items** (some items trace to multiple docs) | |

## Pricing Coverage

| Metric | Value |
|---|---|
| Items priced (Amount > 0) | 8 of 14 lines (57%) |
| Items at $0 (requirement-level; effort included elsewhere) | 6 of 14 lines (43%) |
| Items with Amount = TBD | 0 |
| Total estimated amount | $18,390.00 CAD |

## Basis-Consistency

| Method | Line Count | Amount | % of Total |
|---|---|---|---|
| PARAMETRIC | 14 | $18,390.00 | 100% |
| Other | 0 | $0 | 0% |

Consistent with BASIS_OF_ESTIMATE = PARAMETRIC. No fallback methods used.

## What to Fix for a Cleaner Rerun

1. **Confirm design storm parameters** (Specification A-001 / Conflict C-001) — once resolved, drainage design complexity can be better estimated and hours may need adjustment.
2. **Confirm stormwater detention requirement** — if on-site detention is required, additional Civil Engineer hours for Phase B may be needed.
3. **Confirm geotechnical data availability** — drainage design revision after geotech report could add hours.
4. **Consider subconsultant costs** — if environmental assessment is needed for landfill-adjacent stormwater management, add a subconsultant line item.
5. **Refine phase allocation** — the 84 Civil Engineer hours are allocated across phases based on engineering judgment; actual phase splits may differ during execution.
