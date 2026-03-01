# QA Report — EST_DEL-017-02_2026-02-27_0532

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and traceable, but material TBDs and parametric assumptions remain. The mezzanine area is unconfirmed, structural condition is unknown, and several construction scope items are design-gated. The estimate is suitable for budgeting and planning but requires rerun after the structural assessment and design are complete.

---

## S1 — Write Quarantine Respected

**PASS.** All output files written under `_Estimates/EST_DEL-017-02_2026-02-27_0532/`. No files outside `_Estimates/` were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-017-02_2026-02-27_0532` created at `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

## S4 — Required Artifacts Exist

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

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**

| Check | Result |
|-------|--------|
| Parseable CSV | Yes |
| Required columns present | Yes (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) |
| Row count | 30 rows |
| All rows have DeliverableID = DEL-017-02 | Yes |
| PricingMode values valid | Yes (UNIT_RATE: 6 rows; LUMP_SUM: 24 rows) |
| All rows have SourceDoc | Yes (Datasheet: 1, Specification: 2, Procedure: 26, Guidance: 0, mixed: 1) |
| All rows have SourceSection | Yes |
| Qty values | Numeric (no TBD values) |

### Detail.csv

**PASS.**

| Check | Result |
|-------|--------|
| Parseable CSV | Yes |
| Required columns present | Yes (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Row count | 30 rows |
| All LineIDs unique | Yes (L-001 to L-030) |
| All ItemIDs trace to Items.csv | Yes |
| Method values valid | Yes (all PARAMETRIC) |
| Currency values | All CAD |
| Amount = Qty x UnitRate check | PASS for all rows |
| Lump-sum convention (Qty=1, Unit=LS, UnitRate=Amount) | PASS for all LS items |

## S6 — Provenance Discipline

**PASS with notes.**

| Metric | Value |
|--------|-------|
| Rows with non-TBD SourceRef | 30/30 (100%) |
| Rows referencing a specific price source file | 26/30 (87%) |
| Rows with parametric allowance (no rate table) | 4/30 (13%) — L-012, L-014, L-016, L-029 |

**Top provenance gaps (parametric allowances without rate table):**

| LineID | Description | Amount (CAD) | Issue |
|--------|------------|-------------|-------|
| L-014 | Structural Repairs | 7,500 | No structural repair rate table; parametric allowance |
| L-016 | Stair and Railing | 6,000 | No stair/railing rate table; parametric allowance |
| L-012 | Hazmat Assessment | 2,500 | No hazmat rate table; parametric allowance |
| L-029 | Waste Disposal | 1,500 | No disposal rate table; parametric allowance |

Total with rate-table-unsupported parametric allowances: 17,500 CAD (23.4% of total).

## S7 — Status Reporting

**RUN_STATUS = WARNINGS** (declared above).

Justification:
- Totals exist and are meaningful (74,902.90 CAD).
- Material TBDs remain: mezzanine area (ASM-001), structural condition (ASM-009), stair condition (ASM-011).
- 20 assumptions logged; 9 decisions logged; 7 risks identified.
- Pricing coverage is 100% (no TBD amounts), but 23.4% of total is rate-table-unsupported parametric allowance.

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|-------|--------|-------|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS; gaps are enumerated and bounded |
| Items.csv reviewed for completeness | REVIEW NEEDED | 30 items extracted from 4 documents; human review recommended |
| Basis-consistency checks pass | PASS | All methods = PARAMETRIC; consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% SourceRef; 87% rate-table-backed |
| Scope coverage explicit | PASS | 1 deliverable, 4/4 documents read, 0 missing documents |
| No writes outside _Estimates/ | PASS | Verified |

---

## Quantity Takeoff Coverage

| Source Document | Items Extracted | Notes |
|----------------|----------------|-------|
| Datasheet | 1 (ITM-019) | Scope components and attributes informed multiple items; 1 item directly sourced |
| Specification | 2 (ITM-007, ITM-028) | Requirements drove structural assessment and documentation items |
| Procedure | 26 (ITM-001 to ITM-006, ITM-008 to ITM-027, ITM-029, ITM-030) | Primary source for work activities and steps |
| Guidance | 0 directly | Guidance informed trade-off decisions but did not generate additional priceable items |
| _CONTEXT.md | N/A | Used for deliverable identity; not a source for priceable items |

**Note:** Most items trace to Procedure because the Procedure document contains the detailed work steps. The Datasheet and Specification informed the scope and requirements that the Procedure implements.

---

## What to Fix for a Cleaner Rerun

1. **Obtain mezzanine floor area** from field measurement or original drawings. Replace ASM-001 (30 m2) with actual dimension. This will improve accuracy for 5 area-based line items.

2. **Complete the structural engineering assessment** (STRUCT-ASSESS-001). This will resolve:
   - Structural repair scope and cost (currently 7,500 CAD allowance)
   - Stair/railing condition and required upgrades (currently 6,000 CAD allowance)

3. **Complete the renovation design package.** This will resolve:
   - Actual flooring type and specification
   - Actual electrical scope
   - Actual finishes scope
   - Fixtures and fittings list

4. **Conduct hazardous materials assessment.** If ACM or lead paint is found, add abatement line items.

5. **Add HVAC/ventilation scope** if the design determines mechanical work is needed (Guidance identifies this gap at D-002). Currently not estimated.

6. **Provide material-only rate tables** for structural steel, electrical fixtures, stair components, and plumbing fixtures to improve provenance beyond labour-rate-only parametric estimates.

7. **Add Level_of_Effort.csv entries for design roles** on DEL-017-02 (currently only management/construction roles are present in the LOE file).
