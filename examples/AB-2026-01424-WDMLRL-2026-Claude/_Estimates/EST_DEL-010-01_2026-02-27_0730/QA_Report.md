# QA Report — EST_DEL-010-01_2026-02-27_0730

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and all 31 line items are priced (no TBD amounts). However, material assumptions remain regarding foundation type, excavation volumes, and concrete quantities — all pending the geotechnical investigation report (PKG-008). The estimate is a preliminary parametric basis for a variable-price scope item.

---

## S1 — Write Quarantine Respected

**PASS.** All output files are written exclusively under `_Estimates/EST_DEL-010-01_2026-02-27_0730/`. No files outside the estimating tool root were modified.

---

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-010-01_2026-02-27_0730` created under `_Estimates/`.

---

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

---

## S4 — Required Artifacts Exist

**PASS.** All required artifacts are present:

| Artifact | Status |
|---|---|
| Run_Context.md | Present |
| Items.csv | Present |
| Detail.csv | Present |
| Summary.md | Present |
| QA_Report.md | Present (this file) |
| Source_Index.md | Present |
| Decision_Log.md | Present |
| Assumptions_Log.md | Present |
| WBS_CBS_Matrix.csv | Present |

---

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | Yes — all 9 columns present |
| PricingMode values valid | Yes — all values are UNIT_RATE or LUMP_SUM |
| Every row has SourceDoc | Yes — all 31 rows trace to Datasheet, Specification, or Procedure |
| Every row has SourceSection | Yes |
| Lump-sum convention (Qty=1, Unit=LS) | Yes — all 8 LUMP_SUM items have Qty=1, Unit=LS |
| TBD quantities | 0 of 31 rows |
| Row count | 31 |

### Detail.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | Yes — all 15 columns present |
| Method values valid | Yes — all values are PARAMETRIC |
| Allowance/parametric convention (LS items: Qty=1, Unit=LS, UnitRate=Amount) | Yes — all 8 LUMP_SUM items follow convention |
| Currency consistent | Yes — all rows CAD |
| Amount = Qty x UnitRate | Yes — verified for all 31 rows |
| TBD amounts | 0 of 31 rows |
| Row count | 31 |

---

## S6 — Provenance Discipline

**PASS (with notes).**

| Metric | Value |
|---|---|
| Total priced rows | 31 |
| Rows with non-TBD SourceRef | 31 (100%) |
| Rows referencing rate table source files | 23 of 31 (74.2%) |
| Rows referencing Assumptions_Log.md entries | 8 of 31 (25.8%) |
| Rows with `location TBD` | 0 |

**Top provenance observations:**
- The 8 lump-sum allowance items (DL-012 through DL-020) reference Assumptions_Log.md entries rather than external price sources. These are parametric allowances without direct rate table support.
- All earthwork, concrete, professional staff, and labour line items reference specific rate table files and row IDs.

---

## S7 — Status Reporting

**RUN_STATUS = WARNINGS**

Warnings:
1. Foundation type is TBD pending geotechnical investigation (PKG-008). All quantities are preliminary.
2. This is a variable-price scope item; final pricing is negotiated post-geotech per RFP §4.8.2.
3. Service pit scope boundary (CF-010-01) is unresolved; excluded from estimate.
4. 8 of 31 items (25.8%) are LOW confidence parametric allowances.
5. No cold-weather construction premium is included.
6. Concrete design parameters (f'c, reinforcement details, depths) are TBD.

---

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS — gaps are clearly bounded (geotech TBD, service pit TBD, variable-price) |
| Quantity takeoff (Items.csv) reviewed for completeness | REVIEW NEEDED | 31 items extracted from 4 documents; human should verify no material scope items are missing |
| Basis-consistency checks pass | PASS | All 31 lines use Method=PARAMETRIC, consistent with BASIS_OF_ESTIMATE=PARAMETRIC |
| Provenance completeness reported | PASS | 100% provenance (31/31 rows have SourceRef) |
| Scope coverage explicit | PASS | 1 deliverable (DEL-010-01) in scope; service pit excluded per CF-010-01 |
| No writes outside _Estimates/ | PASS | Verified — all outputs in snapshot folder |

---

## Quantity Takeoff Coverage

| Source Document | Items Extracted | Notes |
|---|---|---|
| Datasheet.md | 10 | Building footprint, excavation, concrete, slab, rebar, grade beams, fill |
| Specification.md | 4 | Testing requirements, compaction acceptance, inspection, quality documentation |
| Procedure.md | 13 | Formwork, survey, embedded items, backfill, labour, handoff, as-built |
| Guidance.md | 0 | Guidance is directional; priceable items derived from other documents |
| Level_of_Effort.csv | 6 | Professional staff hours for DEL-010-01 |

**Missing documents:** None — all 4 production documents were read successfully.

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Items priced | 31 of 31 (100%) |
| Items with TBD amount | 0 |
| Items priced via rate table | 23 (74.2%) |
| Items priced via parametric allowance | 8 (25.8%) |

---

## What to Fix for a Cleaner Rerun

1. **Resolve geotechnical investigation (PKG-008)** — enables actual foundation type, excavation depths, and concrete volumes to replace parametric assumptions.
2. **Resolve service pit scope boundary (CF-010-01)** — enables service pit to be included in or excluded from the estimate with certainty.
3. **Obtain Foundation Design Package (DEL-002-11)** — provides actual footing dimensions, reinforcement details, and concrete specifications.
4. **Obtain structural and MEP drawings** — enables actual embedded item quantities to replace the $12,000 allowance.
5. **Confirm aggregate supply arrangement** — verify whether the County-supplied aggregate applies to foundation sub-base or only to driving surfaces.
6. **Assess cold-weather risk** — if foundation construction schedule extends into winter months, add a cold-weather premium line item.
