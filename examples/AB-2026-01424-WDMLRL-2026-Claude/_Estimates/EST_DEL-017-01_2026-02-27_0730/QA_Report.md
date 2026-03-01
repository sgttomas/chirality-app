# QA Report — EST_DEL-017-01_2026-02-27_0730

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and traceable, but material TBDs and parametric assumptions remain. Two conditional line items (gas fitting and HVAC/mechanical) are unpriced pending design resolution. Appliance and cabinetry scope, plumbing/electrical rough-in scope, and several other items are design-gated. The estimate is suitable for budgeting and planning but requires rerun after the design phase and appliance schedule are complete.

---

## S1 -- Write Quarantine Respected

**PASS.** All output files written under `_Estimates/EST_DEL-017-01_2026-02-27_0730/`. No files outside `_Estimates/` were modified.

## S2 -- Snapshot Created

**PASS.** Snapshot folder `EST_DEL-017-01_2026-02-27_0730` created at `_Estimates/`.

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
| Risk_Register.md | Present (optional; produced) |

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
| Qty values | Numeric for 30 rows; 2 conditional items have Qty=1 with TBD pricing in Detail.csv |

### Detail.csv

**PASS with notes.**

| Check | Result |
|-------|--------|
| Parseable CSV | Yes |
| Required columns present | Yes (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Row count | 32 rows |
| All LineIDs unique | Yes (L-001 to L-032) |
| All ItemIDs trace to Items.csv | Yes |
| Method values valid | Yes (all PARAMETRIC) |
| Currency values | All CAD |
| Amount = Qty x UnitRate check | PASS for all 30 priced rows; 2 rows (L-019, L-020) have Amount=TBD |
| Lump-sum convention (Qty=1, Unit=LS, UnitRate=Amount) | PASS for all priced LS items |
| TBD items | 2 rows (L-019 gas fitting, L-020 HVAC) have UnitRate=TBD and Amount=TBD -- explicitly conditional pending design; flagged with `location TBD` SourceRef |

## S6 -- Provenance Discipline

**PASS with notes.**

| Metric | Value |
|--------|-------|
| Rows with non-TBD SourceRef | 30/32 (93.8%) |
| Rows referencing a specific price source file | 28/32 (87.5%) |
| Rows with parametric allowance (no rate table) | 2/32 (6.3%) -- L-012, L-016 |
| Rows with TBD SourceRef (conditional items) | 2/32 (6.3%) -- L-019, L-020 |

**Top provenance gaps:**

| LineID | Description | Amount (CAD) | Issue |
|--------|------------|-------------|-------|
| L-019 | Gas Fitting Rough-In | TBD | Conditional; scope depends on appliance schedule |
| L-020 | HVAC/Mechanical Rough-In | TBD | Conditional; scope depends on appliance schedule |
| L-012 | Hazmat Assessment | 2,500 | No hazmat rate table; parametric allowance |
| L-016 | Waste Disposal | 1,200 | No disposal rate table; parametric allowance |

Total with rate-table-unsupported parametric allowances: 3,700 CAD (8.8% of priced total).

## S7 -- Status Reporting

**RUN_STATUS = WARNINGS** (declared above).

Justification:
- Totals exist and are meaningful (41,901.44 CAD priced; 2 conditional lines TBD).
- Material TBDs remain: appliance schedule, cabinetry specifications, gas/HVAC scope, plumbing/electrical scope details.
- 21 assumptions logged; 9 decisions logged; 9 risks identified.
- Pricing coverage is 93.8% (30/32 lines priced); 2 conditional lines intentionally left TBD.
- Of priced items, 8.8% (3,700 CAD) is rate-table-unsupported parametric allowance.

## S8 -- Operator Acceptance Checklist

| Check | Status | Notes |
|-------|--------|-------|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS; gaps are enumerated and bounded |
| Items.csv reviewed for completeness | REVIEW NEEDED | 32 items extracted from 4 documents; human review recommended |
| Basis-consistency checks pass | PASS | All methods = PARAMETRIC; consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 93.8% non-TBD SourceRef; 87.5% rate-table-backed |
| Scope coverage explicit | PASS | 1 deliverable (DEL-017-01), 4/4 documents read, 0 missing documents |
| No writes outside _Estimates/ | PASS | Verified |

---

## Quantity Takeoff Coverage

| Source Document | Items Extracted | Notes |
|----------------|----------------|-------|
| Datasheet | 1 (ITM-023) | Scope components and attributes informed multiple items; 1 item directly sourced to Datasheet Construction section |
| Specification | 2 (ITM-022, ITM-032) | REQ-007/REQ-008 drove fixture/finish items; Documentation section drove photo documentation |
| Procedure | 29 (ITM-001 to ITM-021, ITM-024 to ITM-031) | Primary source for work activities and steps across all 5 phases |
| Guidance | 0 directly | Guidance informed trade-off decisions (phasing, fixture quality, cabinetry type, appliance scope) and identified conditional scope (HVAC, accessibility, fire separation) but did not generate additional priceable items beyond what Specification and Procedure already captured |
| _CONTEXT.md | N/A | Used for deliverable identity; not a source for priceable items |

**Note:** Most items trace to Procedure because the Procedure document contains the detailed 18-step work sequence across 5 phases. The Datasheet and Specification informed the scope and requirements that the Procedure implements. Guidance provided directional context and identified design-gated conditional scope.

---

## What to Fix for a Cleaner Rerun

1. **Complete the appliance and cabinetry schedule.** This will resolve:
   - Whether gas appliances are included (triggers ITM-019 gas fitting -- currently TBD)
   - Whether cooking appliances are included (triggers ITM-020 HVAC/ventilation -- currently TBD)
   - Procurement responsibility (Contractor-furnished vs. Owner-furnished per Lensing E-001)
   - Specific fixture and appliance costs to replace the IA-05 allowance allocation

2. **Complete the kitchenette renovation design (IFC drawings).** This will resolve:
   - Actual plumbing rough-in scope (currently 30 hr parametric estimate)
   - Actual electrical rough-in scope (currently 30 hr parametric estimate)
   - Actual wall partition layout (currently using floor area as proxy)
   - Finish specifications (currently using recommended rates from IA rate table)

3. **Conduct hazardous materials assessment.** If ACM or lead paint is found, add abatement line items and revise waste disposal allowance.

4. **Determine accessibility applicability.** Owner/Architect to confirm whether barrier-free requirements apply (Specification REQ-014). If applicable, add accessible design elements.

5. **Confirm fire separation status.** Existing conditions survey and IFC drawings should identify any fire-rated assemblies affected by the renovation. If firestopping is required, it may warrant a separate line item beyond substrate preparation.

6. **Provide material-only rate tables** for plumbing fixtures, electrical fixtures, cabinetry, and appliances to improve provenance beyond labour-rate-only parametric estimates and IA-05 allowance.

7. **Resolve kitchenette spatial identity.** Confirm whether the 250 sqft kitchenette is a distinct space from the mezzanine coffee room and wash station shown in Appendix B (Guidance CF-001).
