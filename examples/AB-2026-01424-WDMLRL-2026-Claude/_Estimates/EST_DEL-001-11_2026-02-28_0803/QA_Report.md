# QA_Report — EST_DEL-001-11_2026-02-28_0803

## RUN_STATUS: OK

**Rationale:** All 11 line items are priced with traceable source references. Total deliverable estimate is $25,105 CAD across 86 professional hours and 2 fee/permit allowances. No TBD items remain. Provenance completeness is 100%.

---

## S1 -- Write Quarantine Respected

| Check | Result |
|---|---|
| All outputs under `_Estimates/` | PASS |
| No modification to deliverable files | PASS |
| No modification to lifecycle files | PASS |
| No modification to decomposition | PASS |
| No modification to prior snapshot | PASS |

## S2 -- Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists | PASS -- `EST_DEL-001-11_2026-02-28_0803/` |

## S3 -- BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| `BASIS_OF_ESTIMATE` = `PARAMETRIC` | PASS -- valid enum value |

## S4 -- Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PASS |
| Items.csv | PASS |
| Summary.md | PASS |
| QA_Report.md | PASS (this file) |
| Source_Index.md | PASS |
| Detail.csv | PASS |
| WBS_CBS_Matrix.csv | PASS |
| Decision_Log.md | PASS |
| Assumptions_Log.md | PASS |

## S5 -- CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to source document and section | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS -- 5 UNIT_RATE, 6 LUMP_SUM |
| Row count | 11 items |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid | PASS -- all PARAMETRIC |
| Qty x UnitRate = Amount for all lines | PASS |
| No TBD values in UnitRate or Amount | PASS |
| Row count | 11 lines |

### Arithmetic Verification

| LineID | Qty | UnitRate | Expected Amount | Actual Amount | Check |
|---|---|---|---|---|---|
| DL-001 | 6 | 165 | 990 | 990 | PASS |
| DL-002 | 4 | 135 | 540 | 540 | PASS |
| DL-003 | 27 | 180 | 4,860 | 4,860 | PASS |
| DL-004 | 21 | 135 | 2,835 | 2,835 | PASS |
| DL-005 | 12 | 95 | 1,140 | 1,140 | PASS |
| DL-006 | 16 | 140 | 2,240 | 2,240 | PASS |
| DL-007 | 1 | 0 | 0 | 0 | PASS |
| DL-008 | 1 | 0 | 0 | 0 | PASS |
| DL-009 | 1 | 0 | 0 | 0 | PASS |
| DL-010 | 1 | 2,500 | 2,500 | 2,500 | PASS |
| DL-011 | 1 | 10,000 | 10,000 | 10,000 | PASS |
| **SUM** | | | **25,105** | **25,105** | **PASS** |

## S6 -- Provenance Discipline

| Metric | Value |
|---|---|
| Total rows in Detail.csv | 11 |
| Rows with substantive SourceRef | 11 (100%) |
| Rows with `location TBD` SourceRef | 0 (0%) |
| Provenance completeness | 100% |

## S7 -- Status Reporting

| Field | Value |
|---|---|
| RUN_STATUS | OK |
| Justification | 100% provenance completeness; 0 TBD items; total ($25,105) is complete; arithmetic verified |

## S8 -- Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK | PASS | All items priced with traceable sources |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 11 items covering all Procedure steps and Specification requirements |
| Basis-consistency checks pass | PASS | All methods = PARAMETRIC; consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% |
| Scope coverage explicit | PASS | 1 deliverable (DEL-001-11); 6 LOE roles; 5 additional activity items |
| Arithmetic verified | PASS | All Qty x UnitRate = Amount; sum = $25,105 |
| No writes outside _Estimates/ | PASS | Confirmed |

---

## Pricing Coverage

| Category | Count | Percentage |
|---|---|---|
| Priced (Amount >= 0) | 11 | 100% |
| TBD (Amount = TBD) | 0 | 0% |
| Total | 11 | 100% |

## Quantity Takeoff Coverage

| Source Document | Items Extracted | Notes |
|---|---|---|
| Datasheet | 0 direct (attributes inform context) | Datasheet attributes inform specification scope but do not generate separate priceable items for the specification deliverable |
| Specification | 3 items (ITEM-007, ITEM-010, ITEM-011) | Code review, stamp fees, permit fees identified from requirements/standards/verification |
| Guidance | 0 direct (informs context) | Guidance trade-offs and considerations inform specification scope |
| Procedure | 8 items (ITEM-001 through ITEM-006, ITEM-008, ITEM-009) | Work steps generate effort-based priceable items |

## Delta from Prior Snapshot

| Field | Prior (EST_DEL-001-11_2026-02-26_2245) | Current (EST_DEL-001-11_2026-02-28_0803) |
|---|---|---|
| RUN_STATUS | WARNINGS | OK |
| TBD count | 3 | 0 |
| Provenance completeness | 73% | 100% |
| Total (priced) | $10,365 | $25,105 |
| Price sources used | 5 | 6 (+Fees_Permits_Insurance.csv) |
| LOE roles | 5 | 6 (+R-21 Surveyor) |
