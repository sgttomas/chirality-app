# QA Report — EST_DEL-017-01_2026-02-28_0807

## RUN_STATUS: OK

**Rationale:** All 32 line items are priced. The two previously-TBD conditional items (L-019 gas fitting, L-020 HVAC/mechanical) have been resolved using recommended rates from Mechanical_System_Rates.csv (MS-07 and MS-08). Zero TBDs remain. Totals are complete and traceable. The estimate is suitable for budgeting and planning, though design-gated scope uncertainties remain for several items.

---

## S1 -- Write Quarantine Respected

**PASS.** All output files written under `_Estimates/EST_DEL-017-01_2026-02-28_0807/`. No files outside `_Estimates/` were modified.

## S2 -- Snapshot Created

**PASS.** Snapshot folder `EST_DEL-017-01_2026-02-28_0807` created at `_Estimates/`.

## S3 -- BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` -- valid enum value.

## S4 -- Required Artifacts Exist

**PASS.** All required artifacts present:

| Artifact | Status |
|----------|--------|
| Run_Context.md | Present |
| Items.csv | Present |
| Summary.md | Present |
| QA_Report.md | Present (this file) |
| Source_Index.md | Present |
| Decision_Log.md | Present |
| Assumptions_Log.md | Present |
| WBS_CBS_Matrix.csv | Present |
| Detail.csv | Present (optional; produced) |

## S5 -- CSV Schema Integrity

### Items.csv

**PASS.**

| Check | Result |
|-------|--------|
| Parseable CSV | Yes |
| Required columns present | Yes (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) |
| Row count | 32 rows |
| All rows have DeliverableID = DEL-017-01 | Yes |
| PricingMode values valid | Yes (UNIT_RATE: 6 rows; LUMP_SUM: 26 rows) |
| All rows have SourceDoc | Yes (Datasheet: 1, Specification: 2, Procedure: 29) |
| All rows have SourceSection | Yes |
| Qty values | Numeric for all 32 rows |

### Detail.csv

**PASS.**

| Check | Result |
|-------|--------|
| Parseable CSV | Yes |
| Required columns present | Yes (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Row count | 32 rows |
| All LineIDs unique | Yes (L-001 to L-032) |
| All ItemIDs trace to Items.csv | Yes |
| Method values valid | Yes (all PARAMETRIC) |
| Currency values | All CAD |
| Amount = Qty x UnitRate check | PASS for all 32 rows |
| Lump-sum convention (Qty=1, Unit=LS, UnitRate=Amount) | PASS for all LS items |
| TBD items | 0 (previously 2; both resolved) |

## S6 -- Provenance Discipline

**PASS.**

| Metric | Value |
|--------|-------|
| Rows with non-TBD SourceRef | 32/32 (100%) |
| Rows referencing a specific price source file | 30/32 (93.8%) |
| Rows with parametric allowance (no rate table) | 2/32 (6.3%) -- L-012, L-016 |
| Rows with TBD SourceRef | 0/32 (0%) |

**Top provenance gaps:**

| LineID | Description | Amount (CAD) | Issue |
|--------|------------|-------------|-------|
| L-012 | Hazmat Assessment | 2,500 | No hazmat rate table; parametric allowance |
| L-016 | Waste Disposal | 1,200 | No disposal rate table; parametric allowance |

Total with rate-table-unsupported parametric allowances: 3,700 CAD (7.7% of priced total).

## S7 -- Status Reporting

**RUN_STATUS = OK** (declared above).

Justification:
- All 32 lines priced (47,901.44 CAD). Zero TBDs remain.
- Two previously-TBD conditional items (L-019, L-020) resolved using Mechanical_System_Rates.csv (MS-07, MS-08).
- 21 assumptions logged; 10 decisions logged.
- Pricing coverage is 100% (32/32 lines priced).
- Of priced items, 7.7% (3,700 CAD) is rate-table-unsupported parametric allowance.
- Design-gated scope uncertainties remain but all items have defensible parametric prices.

## S8 -- Operator Acceptance Checklist

| Check | Status | Notes |
|-------|--------|-------|
| RUN_STATUS is OK | PASS | OK; all items priced |
| Items.csv reviewed for completeness | REVIEW NEEDED | 32 items extracted from 4 documents; human review recommended |
| Basis-consistency checks pass | PASS | All methods = PARAMETRIC; consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% non-TBD SourceRef; 93.8% rate-table-backed |
| Scope coverage explicit | PASS | 1 deliverable (DEL-017-01), 4/4 documents read, 0 missing documents |
| No writes outside _Estimates/ | PASS | Verified |

---

## Quantity Takeoff Coverage

| Source Document | Items Extracted | Notes |
|----------------|----------------|-------|
| Datasheet | 1 (ITM-023) | Scope components and attributes informed multiple items; 1 item directly sourced to Datasheet Construction section |
| Specification | 2 (ITM-022, ITM-032) | REQ-007/REQ-008 drove fixture/finish items; Documentation section drove photo documentation |
| Procedure | 29 (ITM-001 to ITM-021, ITM-024 to ITM-031) | Primary source for work activities and steps across all 5 phases |
| Guidance | 0 directly | Guidance informed trade-off decisions and identified conditional scope but did not generate additional priceable items |
| _CONTEXT.md | N/A | Used for deliverable identity; not a source for priceable items |

---

## What Changed from Previous Snapshot

| Item | Previous | Current | Notes |
|------|----------|---------|-------|
| L-019 Gas Fitting | TBD | 2,500 CAD | Priced using Mechanical_System_Rates.csv MS-07 recommended rate |
| L-020 HVAC/Mechanical | TBD | 3,500 CAD | Priced using Mechanical_System_Rates.csv MS-08 recommended rate |
| TBD count | 2 | 0 | Both conditional items resolved |
| RUN_STATUS | WARNINGS | OK | All items now priced |
| Total | 41,901.44 CAD | 47,901.44 CAD | +6,000 CAD |
| PRICE_SOURCES | 5 files | 6 files | Added Mechanical_System_Rates.csv |

## What to Fix for a Cleaner Rerun

1. **Complete the appliance and cabinetry schedule.** This will confirm whether gas fitting (L-019) and HVAC/ventilation (L-020) are actually required or should be removed. It will also resolve procurement responsibility and specific fixture/appliance costs.

2. **Complete the kitchenette renovation design (IFC drawings).** This will resolve actual plumbing rough-in scope, electrical rough-in scope, wall partition layout, and finish specifications.

3. **Conduct hazardous materials assessment.** If ACM or lead paint is found, add abatement line items and revise waste disposal allowance.

4. **Determine accessibility applicability.** Owner/Architect to confirm whether barrier-free requirements apply (Specification REQ-014).

5. **Confirm fire separation status.** Identify any fire-rated assemblies affected by the renovation.

6. **Provide material-only rate tables** for plumbing fixtures, electrical fixtures, cabinetry, and appliances.
