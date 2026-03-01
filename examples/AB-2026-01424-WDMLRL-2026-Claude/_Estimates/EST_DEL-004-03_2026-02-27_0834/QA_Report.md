# QA Report — EST_DEL-004-03_2026-02-27_0834

## RUN_STATUS: OK

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All outputs written under _Estimates/ | PASS |
| No files modified outside _Estimates/ | PASS |

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists: EST_DEL-004-03_2026-02-27_0834/ | PASS |

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = PARAMETRIC | PASS (valid enum value) |
| All Detail.csv Method values consistent with basis | PASS (all 4 lines = PARAMETRIC) |

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Items.csv | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT |
| Source_Index.md | PRESENT |
| Detail.csv | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS — 4 UNIT_RATE, 4 LUMP_SUM |
| All rows trace to a source document and section | PASS |
| Row count | 8 items |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All Method values valid (PARAMETRIC) | PASS |
| Allowance/parametric convention | N/A — all lines are UNIT_RATE with natural Qty and Unit (hours) |
| ItemID references valid (L-001 to L-004 reference ITEM-001 to ITEM-004) | PASS |
| Row count | 4 priced lines |

### WBS_CBS_Matrix.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present | PASS |
| Totals consistent with Detail.csv | PASS ($17,280.00 + $1,530.00 = $18,810.00) |

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total priced lines | 4 |
| Lines with non-TBD SourceRef | 4 |
| **Provenance completeness** | **100%** |
| Lines with Amount = TBD | 0 |
| Top missing-source offenders | None |

## S7 — Status Reporting

| Check | Result |
|---|---|
| RUN_STATUS declared | PASS |
| RUN_STATUS value | **OK** |
| Rationale | All 4 lines priced; 0 TBDs; 100% provenance; single consistent method (PARAMETRIC); no critical input gaps |

## S8 — Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (OK) |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS — 8 items extracted from 4 documents; 4 priced, 4 embedded activities |
| Basis-consistency checks pass | PASS — all lines PARAMETRIC, matching BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS — 100% |
| Scope coverage explicit | PASS — 1 deliverable (DEL-004-03); all 4 documents read; 0 missing documents |
| No writes outside _Estimates/ | PASS |

---

## Quantity Takeoff Coverage

| Document | Items Extracted | Notes |
|---|---|---|
| Datasheet.md | Load inventory informing ITEM-001 scope | 2 cranes, overhead doors, compressor, fire hose pump, pressure washer, welding receptacles, mixed receptacles, exhaust fans, ceiling fans, lighting, mechanical equipment |
| Specification.md | 18 requirements (REQ-003-01 to REQ-003-18) informing scope | Code compliance, GFCI/AFCI, grounding/bonding |
| Guidance.md | Design principles, trade-offs, risks informing ITEM-001 scope | Drawing organization, panelboard location, service entry coordination |
| Procedure.md | 7 steps (plus 1A, 2B) mapped to ITEM-001 through ITEM-008 | Full workflow from info gathering through IFC issue |

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 8 |
| Items priced in Detail.csv | 4 (ITEM-001 to ITEM-004) |
| Items with embedded cost (not separately priced) | 4 (ITEM-005 to ITEM-008) |
| Items with Amount = TBD | 0 |
| **Pricing coverage** | **100% of cost-bearing items** |

## What to Fix for a Cleaner Rerun

- No fixes required. This run is fully priced with complete provenance.
- Optional enhancement: If construction value estimate becomes available, a cross-check against Professional_Design_Fees.csv (DF-04: 1.6% of construction value for electrical design) could be performed to validate the LOE-based estimate against an independent parametric benchmark.
