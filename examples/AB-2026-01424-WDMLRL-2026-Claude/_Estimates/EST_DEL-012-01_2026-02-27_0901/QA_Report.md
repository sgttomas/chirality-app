# QA Report

**RunID:** EST_DEL-012-01_2026-02-27_0901
**RUN_STATUS: WARNINGS**

---

## S1 -- Write Quarantine Respected

**PASS.** All output files written exclusively under `{RUN_ROOT}/_Estimates/EST_DEL-012-01_2026-02-27_0901/`. No files outside `_Estimates/` were modified.

---

## S2 -- Snapshot Created

**PASS.** Snapshot folder `EST_DEL-012-01_2026-02-27_0901` created under `_Estimates/`.

---

## S3 -- BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` -- valid enum value.

---

## S4 -- Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Items.csv | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Detail.csv | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |

**PASS.** All required artifacts present. Optional `Detail.csv` also produced.

---

## S5 -- CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable | PASS |
| Required columns (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS -- all 9 columns present |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS -- all 18 rows use valid values |
| All rows trace to source document and section | PASS -- SourceDoc and SourceSection populated for all rows |
| ITM-018 has Qty=0 | NOTE -- intentional zero-quantity row to document material inclusion in IA-01 rate; not a defect |

### Detail.csv

| Check | Result |
|---|---|
| Parseable | PASS |
| Required columns (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS -- all 15 columns present |
| Method values valid | PASS -- all 17 rows use PARAMETRIC |
| Allowance/parametric convention | PASS -- lump sum items (L-002, L-003, L-007) use Qty=1, Unit=LS, UnitRate=Amount |
| Amount computation (Qty x UnitRate = Amount) | PASS for all rows |

**PASS.**

---

## S6 -- Provenance Discipline

### Provenance Completeness

| Metric | Value |
|---|---|
| Total priced lines in Detail.csv | 17 |
| Lines with non-TBD SourceRef | 17 |
| Provenance completeness | **100%** |

### Top Missing-Source Offenders

None. All lines have SourceRef populated.

### Provenance Quality Notes

| LineID | SourceRef Quality | Note |
|---|---|---|
| L-002 | INDIRECT | Roll-up door priced by parametric scaling from BE-03 (24-ft class); no direct rate for 6-ft interior door |
| L-006 | INDIRECT | Shelving priced by parametric assumption; no shelving rate table in sources |
| L-007 | INDIRECT | Anchoring priced by parametric assumption |
| L-003 | INDIRECT | Door framing priced by parametric labour calculation |

**PASS with NOTE:** 4 of 17 lines (23.5%) rely on indirect/derived parametric evidence rather than direct rate table entries.

---

## S7 -- Status Reporting

**RUN_STATUS: WARNINGS**

Rationale: Totals are meaningful and all items are priced (no TBD amounts), but material assumptions remain:

1. Shelving specification TBD -- largest single cost category (31.5% of total) at LOW confidence.
2. Roll-up door priced by parametric scaling (LOW confidence).
3. Potential partial labour double-count between IA-01 composite rate and trade labour lines.
4. Finish schedule dependency (DEL-001-08) unresolved.
5. Partition height assumed (mezzanine deck elevation not confirmed).

Status is WARNINGS (not FAILED_INPUTS) because all items have been priced using available parametric sources and the FALLBACK_POLICY permits parametric derivation.

---

## S8 -- Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS with 5 bounded gaps documented above |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 18 items extracted from 4 documents; covers partitions, door, finishes, shelving, management, and trade labour |
| Basis-consistency checks | PASS | All methods = PARAMETRIC; consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% SourceRef coverage; 76.5% direct, 23.5% indirect |
| Scope coverage explicit | PASS | 1 deliverable in scope (DEL-012-01); exclusions documented (PKG-013 HVAC, PKG-015 Electrical, PKG-011 Structure, PKG-010 Foundation) |
| No writes outside _Estimates/ | PASS | Verified |

---

## Quantity Takeoff Coverage

| Source Document | Items Extracted | Notes |
|---|---|---|
| Datasheet.md | 6 items (ITM-001 through ITM-007) | Spatial attributes, construction attributes, fit-out attributes |
| Specification.md | 1 item (ITM-007 shelving anchoring) | REQ-012-01-011a |
| Guidance.md | 0 direct items | Informed trade-off decisions (DEC-002, DEC-003) but no standalone priceable items |
| Procedure.md | 11 items (ITM-008 through ITM-017, ITM-003) | Work steps, coordination, supervision, labour |

All 4 documents read successfully; no MISSING_DOCUMENT warnings.

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 18 (17 with Qty > 0) |
| Items priced (Amount != TBD) | 17 of 17 |
| Items with TBD amount | 0 |
| Pricing coverage | **100%** |

---

## What to Fix for a Cleaner Rerun

1. **Obtain finish schedule (DEL-001-08)** to replace assumed paint/sealer rates for walls and floors.
2. **Obtain shelving specification and supplier quote** to replace $1,500/bay parametric assumption.
3. **Obtain roll-up door supplier quote** for 6-ft motorized insulated unit to replace parametric scaling from 24-ft class.
4. **Confirm mezzanine deck elevation** to validate partition height assumption (10 ft) and derived wall area (74 m2).
5. **Clarify IA-01 rate scope** (supply-only vs. supply-and-install) to resolve potential labour double-count (ASM-006).
6. **Confirm fire code requirements** (Alberta Fire Code) to determine if fire-rated partitions are needed (Specification CF-005).
