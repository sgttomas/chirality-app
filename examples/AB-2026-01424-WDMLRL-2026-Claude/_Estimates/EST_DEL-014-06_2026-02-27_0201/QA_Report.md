# QA_Report — EST_DEL-014-06_2026-02-27_0201

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and all line items are priced, but material TBDs remain in fixture specifications (pending DEL-006-06), a conditional item is included (point-of-use water heater), and fixture material pricing is entirely parametric (no quote or rate table evidence for fixtures). The estimate is suitable for early-stage budgeting but requires quote replacement before commitment.

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All files written under `_Estimates/EST_DEL-014-06_2026-02-27_0201/` | PASS |
| No files modified outside `_Estimates/` | PASS |

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists | PASS |
| Folder name follows convention `EST_{LABEL}_{DATE}_{TIME}` | PASS |

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
| QA_Report.md | PRESENT |
| Source_Index.md | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Detail.csv | PRESENT (optional; produced) |

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to source document and section | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Row count | 20 |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (QUOTE, RATE_TABLE, HISTORICAL, ALLOWANCE, PARAMETRIC) | PASS |
| Allowance/parametric convention: Qty=1, Unit=LS for lump-sum items | PASS (DL-007, DL-009, DL-019, DL-020 use Qty=1, Unit=LS) |
| Row count | 20 |

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows | 20 |
| Rows with non-TBD SourceRef | 20 (100%) |
| Rows with `location TBD` SourceRef | 0 (0%) |
| Provenance completeness | 100% |

**Top missing-source offenders:** None. All rows have source references.

## S7 — Status Reporting

| Field | Value |
|---|---|
| RUN_STATUS | WARNINGS |
| Reason | Fixture material pricing is entirely PARAMETRIC (no quote/rate table evidence); conditional item included; fixture specifications TBD pending DEL-006-06 |

## Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-014-06) |
| Documents read | 5 (_CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md) |
| Missing documents | 0 |
| Items extracted | 20 |
| Items per source document: Datasheet | 4 (fixture inventory) |
| Items per source document: Specification | 5 (verification, interface, submittal) |
| Items per source document: Procedure | 9 (installation labour, testing, commissioning, inspection) |
| Items per source document: Guidance | 1 (conditional heater) |
| Items per source document: Multiple | 1 (trim/misc) |

## Pricing Coverage

| Metric | Value |
|---|---|
| Items priced | 20 / 20 (100%) |
| Items with TBD Amount | 0 |
| Items at LOW confidence | 2 (10%) |
| Items at MED confidence | 18 (90%) |
| Items at HIGH confidence | 0 (0%) |

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Methods used: PARAMETRIC | 11 lines (55%) |
| Methods used: RATE_TABLE | 9 lines (45%) |
| Methods used: other | 0 lines |
| Basis consistency | PASS — RATE_TABLE usage is consistent with ALLOW_MIXED_METHODS=TRUE; RATE_TABLE lines use direct rate table evidence from PRICE_SOURCES |

## What to Fix for a Cleaner Rerun

1. **Obtain fixture vendor quotes** for water taps, pressure washer hose reel, industrial wash station, and backflow prevention devices. Replace PARAMETRIC estimates (DL-001 through DL-004, DL-008) with QUOTE method.
2. **Resolve CONF-014-06-01** (hot water for wash station) to confirm or remove the conditional point-of-use water heater (DL-007).
3. **Resolve CONF-014-06-02** (pressure washer unit ownership) to confirm reel-only scope.
4. **Obtain DEL-006-06 Fixture Schedule** to confirm fixture types, quantities, and specifications. This may change the fixture inventory and pricing.
5. **Obtain AHJ fee schedule** for Safety Code inspection to replace parametric allowance (DL-020).
6. **Confirm backflow prevention requirements** with AHJ to validate quantity and type (DL-008).
7. **Review plumber labour hours** (24 hr install, 8 hr test, 4 hr commissioning = 36 hr total) against contractor input once IFC drawings are available.
