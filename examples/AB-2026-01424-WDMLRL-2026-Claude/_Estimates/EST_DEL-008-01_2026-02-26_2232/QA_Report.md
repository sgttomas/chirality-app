# QA Report — EST_DEL-008-01_2026-02-26_2232

## RUN_STATUS: WARNINGS

The run produced valid artifacts with traceability, but the overwhelming majority of line items (91.3%) have TBD amounts due to missing price sources for the core scope of this deliverable (geotechnical field investigation, laboratory testing, and geotechnical engineer effort hours). The priced total of $1,530 CAD represents management overhead only and is not a meaningful estimate of the geotechnical investigation cost.

---

## S1 — Write Quarantine Respected

**PASS.** All outputs written to `_Estimates/EST_DEL-008-01_2026-02-26_2232/`. No files outside `_Estimates/` were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-008-01_2026-02-26_2232` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required files produced:

| File | Status |
|------|--------|
| Run_Context.md | Created |
| Items.csv | Created (23 rows) |
| Detail.csv | Created (23 rows) |
| Summary.md | Created |
| QA_Report.md | Created (this file) |
| Source_Index.md | Created |
| Decision_Log.md | Created (7 decisions) |
| Assumptions_Log.md | Created (9 assumptions) |
| WBS_CBS_Matrix.csv | Created (10 CBS categories + total) |
| Risk_Register.md | Created |

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**

| Check | Result |
|-------|--------|
| Parseable CSV | Yes |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | Yes — all 9 columns present |
| PricingMode values valid | Yes — all values are UNIT_RATE or LUMP_SUM |
| Every row traces to SourceDoc and SourceSection | Yes |
| Row count | 23 |
| Items with Qty = TBD | 16 of 23 (70%) |

### Detail.csv

**PASS.**

| Check | Result |
|-------|--------|
| Parseable CSV | Yes |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | Yes — all 15 columns present |
| Method values valid | Yes — all values are PARAMETRIC |
| Allowance/parametric convention respected | N/A — no ALLOWANCE lines; lump-sum PARAMETRIC lines have Qty=1, Unit=LS where applicable |
| ItemID traceability | All 23 Detail lines map to a valid Items.csv ItemID |
| Row count | 23 |

## S6 — Provenance Discipline

| Metric | Value |
|--------|-------|
| Lines with non-TBD SourceRef | 13 of 23 (56.5%) |
| Lines with SourceRef = "location TBD" | 10 of 23 (43.5%) |

**Top missing-source offenders** (lines with `location TBD` in SourceRef):

| LineID | Description | Reason |
|--------|-------------|--------|
| L-005 | Drill rig mob/demob | No subcontractor/equipment rates in PRICE_SOURCES |
| L-006 | Borehole drilling | No drilling rates in PRICE_SOURCES |
| L-007 | Test pit excavation | No excavation rates in PRICE_SOURCES |
| L-008 | Groundwater monitoring wells | No equipment rates in PRICE_SOURCES |
| L-009 | Soil sample collection | No rates in PRICE_SOURCES |
| L-011 | Photographic documentation | No standalone rate; typically bundled |
| L-012 | Laboratory testing | No lab test rates in PRICE_SOURCES |
| L-020 | P.Eng. certification/seal | No standalone rate; typically bundled |
| L-021 | Report delivery | No admin rate applied |
| L-023 | Site restoration | No restoration rates in PRICE_SOURCES |

## S7 — Status Reporting

**RUN_STATUS = WARNINGS**

Rationale: Some totals exist ($1,530 CAD for management overhead) but material TBDs remain. The priced amount covers only 8.7% of line items and represents a negligible fraction of the expected total investigation cost. The estimate cannot be used as a meaningful cost forecast without additional pricing sources.

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|-----------|--------|-------|
| RUN_STATUS is OK or WARNINGS with clearly bounded gaps | WARNINGS — gaps clearly identified | Gaps are well-defined: missing LoE for geotech engineer, missing subcontractor/equipment rates |
| Quantity takeoff (Items.csv) reviewed for completeness | 23 items extracted from all 4 documents | Coverage appears thorough for the deliverable scope; TBD quantities are appropriately flagged |
| Basis-consistency checks pass | PASS — all lines use PARAMETRIC | Consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | 56.5% non-TBD SourceRef | Top gaps listed above |
| Scope coverage explicit | 1 deliverable, 1 package | DEL-008-01 fully scoped; no excluded deliverables in scope |
| No writes outside _Estimates/ | PASS | Verified |

---

## What to Fix for a Cleaner Rerun

1. **Add Geotechnical Engineer hours to Level_of_Effort.csv** for DEL-008-01. Minimum needed: investigation program development, field supervision, data analysis (bearing capacity, settlement, service pit, deleterious materials), report preparation, peer review. Estimated range for a typical investigation of this scale: 40-80 hours total.

2. **Obtain geotechnical drilling subcontractor rates or quote** covering:
   - Mobilization/demobilization (lump sum)
   - Borehole drilling per metre or per borehole
   - In-situ testing (SPT) per test
   - Monitoring well installation per well (if applicable)
   - Test pit excavation per pit (if applicable)

3. **Obtain laboratory testing unit costs** for typical soil tests (grain size, Atterberg limits, moisture content, consolidation, etc.) from a geotechnical laboratory.

4. **Define investigation program scope** (borehole count, depths, test program) so that TBD quantities in Items.csv can be resolved. This requires the Geotechnical Engineer to design the program based on the building footprint (~13,000 sqft) and loading conditions.

5. **Consider overhead/markup structure.** Current rates are bare hourly rates with no overhead, profit, or indirect cost multiplier. If applicable, define the markup structure in PRICE_SOURCES.
