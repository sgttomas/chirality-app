# QA Report — EST_DEL-018-02_2026-02-27_0730

**RUN_STATUS: WARNINGS**

---

## 1. Schema Validity

### Items.csv
| Check | Result |
|-------|--------|
| File parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All ItemIDs unique | PASS (ITM-001 through ITM-023) |
| All DeliverableIDs match scope | PASS (all = DEL-018-02) |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| All rows trace to a source document | PASS (Datasheet: 2, Specification: 5, Procedure: 11, Guidance: 1, mixed: 4) |
| All rows have SourceSection populated | PASS |
| Qty populated for all rows | PASS (no TBD quantities; parametric estimates used where exact values unknown) |
| Row count | 23 items |

### Detail.csv
| Check | Result |
|-------|--------|
| File parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All LineIDs unique | PASS (DL-001 through DL-023) |
| All ItemIDs trace to Items.csv | PASS (1:1 mapping ITM-001 through ITM-023) |
| Method values valid | PASS (all = PARAMETRIC) |
| Allowance/parametric convention respected (LS items: Qty=1, Unit=LS, UnitRate=Amount) | PASS (DL-013 through DL-023 follow convention) |
| Currency consistent | PASS (all = CAD) |
| Amount = Qty x UnitRate for all rows | PASS |
| Row count | 23 lines |

### WBS_CBS_Matrix.csv
| Check | Result |
|-------|--------|
| File parseable | PASS |
| Required columns present | PASS |
| TOTAL row matches sum of CBS rows | PASS ($121,442.00) |
| LineCount total matches Detail.csv row count | PASS (23) |

---

## 2. Quantity Takeoff Coverage

| Deliverable | Documents Read | Items Extracted | Missing Documents |
|-------------|---------------|-----------------|-------------------|
| DEL-018-02 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | 23 | None |

### Coverage by Source Document

| Source Document | Items Sourced | Notes |
|-----------------|---------------|-------|
| Datasheet | 2 | Grading requirements and construction attributes |
| Specification | 5 | REQ-02, REQ-04, REQ-06, REQ-08, Documentation |
| Procedure | 11 | Phases A through E work steps |
| Guidance | 1 | C-07 erosion control consideration |
| Mixed/derived | 4 | Items sourced from multiple documents |

### Key Scope Items Identified

- Professional staff supervision and coordination: 6 roles, 38 total hours (from Level_of_Effort.csv)
- Earthworks: rough grading, fine grading, compaction, granular fill placement, utility trench restoration
- Construction labour: equipment operator + general labourer
- Site services: drainage verification, stormwater control, erosion control, inspection coordination, survey/stakes
- Quality assurance: compaction testing
- Landscaping: preparation and planting/restoration
- Documentation: as-built records and closeout

---

## 3. Pricing Coverage

| Metric | Value |
|--------|-------|
| Total line items | 23 |
| Items priced (non-TBD Amount) | 23 (100%) |
| Items with TBD Amount | 0 (0%) |
| Total estimate | $121,442.00 CAD |

All items are priced. However, 11 of 23 line items (48%) are lump-sum parametric allowances with LOW confidence due to TBD scope pending upstream design deliverables.

---

## 4. Provenance Completeness

| Metric | Value |
|--------|-------|
| Lines with non-TBD SourceRef | 23 of 23 (100%) |
| Lines with `location TBD` SourceRef | 0 |

All lines have provenance references pointing to specific price source files, deliverable documents, and/or assumption/decision log entries.

### Top Provenance Concerns

1. **DL-010 (Granular fill placement):** Rate derived by deducting material component from EC-02 supply+place rate. Deduction amount ($30/m3) is an estimate (DEC-003).
2. **DL-007 (Rough grading):** Rate derived by converting EC-01 volumetric rate to area rate using assumed depth (DEC-008, ASM-002).
3. **DL-017/DL-018 (Landscaping):** Amounts are parametric allowances with no design basis. Provenance is the parametric model itself, not a rate table or quote.

---

## 5. Basis-Consistency Checks

| Check | Result |
|-------|--------|
| BASIS_OF_ESTIMATE valid enum | PASS (PARAMETRIC) |
| All Method values match BASIS_OF_ESTIMATE | PASS (23/23 = PARAMETRIC) |
| FALLBACK_POLICY applied | Yes — ALLOW_PARAMETRIC used for lump-sum items without rate table evidence |
| Mixed methods detected | No (100% PARAMETRIC) |
| ALLOW_MIXED_METHODS setting | TRUE (but not exercised) |

---

## 6. Warnings

### Material Warnings

| ID | Warning | Severity | Affected Lines |
|----|---------|----------|----------------|
| W-001 | Grading area (2,500 m2) is a parametric estimate; actual area TBD pending DEL-005-02 IFC civil grading plan | HIGH | DL-007, DL-008, DL-009, DL-010 |
| W-002 | Landscape scope (species, areas, quantities) is entirely TBD pending DEL-007-02/03; $23,000 is an unsupported allowance | HIGH | DL-017, DL-018 |
| W-003 | Compaction acceptance criteria TBD pending DEL-005-07; testing frequency and cost may vary | MED | DL-009, DL-014 |
| W-004 | Fine grading tolerances TBD pending DEL-005-07 | MED | DL-008 |
| W-005 | Granular fill volume (500 m3) is parametric; placement rate is a deduction estimate | MED | DL-010 |
| W-006 | Equipment operator and labourer hours are parametric estimates without detailed task-level buildup | MED | DL-011, DL-012 |
| W-007 | Active landfill site context may impose additional environmental compliance costs not captured | LOW | DL-015, DL-016 |

### Scope Boundary Warnings

| ID | Warning |
|----|---------|
| W-008 | Aggregate supply excluded (County scope) — coordinate timing per Guidance C-02 |
| W-009 | Bulk cut/fill excluded (County scope) — GC scope boundary at DEC-008 (0.4m assumed cut depth for fine grading) |
| W-010 | Utility trench restoration scope depends on DEL-018-06 extent (not yet estimated in this run) |

---

## 7. What to Fix for a Cleaner Rerun

1. **Obtain IFC civil grading plan (DEL-005-02)** to replace parametric area and volume estimates with design quantities.
2. **Obtain landscape plans (DEL-007-02, DEL-007-03)** to replace landscape allowances with designed scope and quantities.
3. **Obtain civil specification (DEL-005-07)** to confirm compaction acceptance criteria, fine grading tolerances, and testing requirements.
4. **Confirm actual grading area** from site survey and civil design to replace the 2,500 m2 parametric estimate.
5. **Confirm granular fill design** (volume, depth, material specification) from civil grading plan.
6. **Obtain quotes** for compaction testing from local Alberta testing laboratories to replace parametric allowance.
7. **Confirm landscape specification (DEL-007-04)** for completion criteria and seasonal provisions.

---

## 8. SPEC Compliance Summary

| SPEC | Requirement | Status |
|------|------------|--------|
| S1 | Write quarantine respected | PASS — all outputs under `_Estimates/EST_DEL-018-02_2026-02-27_0730/` |
| S2 | Snapshot created | PASS |
| S3 | BASIS_OF_ESTIMATE validated | PASS — PARAMETRIC is a valid enum value |
| S4 | Required artifacts exist | PASS — Run_Context.md, Items.csv, Summary.md, QA_Report.md, Source_Index.md all present |
| S5 | CSV schema integrity | PASS — Items.csv and Detail.csv parseable with all required columns and valid enum values |
| S6 | Provenance discipline | PASS — 100% of lines have non-TBD SourceRef; top concerns listed above |
| S7 | Status reporting | PASS — RUN_STATUS = WARNINGS declared |
| S8 | Operator acceptance checklist | See below |

### S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|-------|--------|-------|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS: gaps are bounded (landscape design + civil design pending) |
| Items.csv reviewed for completeness | PASS | 23 items extracted from 4 documents covering all identified priceable scope |
| Basis-consistency checks pass | PASS | 100% PARAMETRIC; no deviations |
| Provenance completeness reported | PASS | 100% non-TBD SourceRef; top concerns documented |
| Scope coverage explicit | PASS | Inclusions and exclusions documented in Summary.md |
| No writes outside _Estimates/ | PASS | All 10 files written to snapshot folder only |
