# QA Report — EST_DEL-011-05_2026-02-27_0848

**RUN_STATUS: WARNINGS**

---

## S1 — Write Quarantine Respected

**PASS.** All output files are written under `_Estimates/EST_DEL-011-05_2026-02-27_0848/`. No files outside `_Estimates/` were modified.

---

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-011-05_2026-02-27_0848` exists under `_Estimates/`.

---

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

---

## S4 — Required Artifacts Exist

**PASS.** All required files present:
- [x] Run_Context.md
- [x] Items.csv
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv
- [x] Detail.csv (optional but produced)

---

## S5 — CSV Schema Integrity

### Items.csv
**PASS.**
- Columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes
- 24 rows, all with valid DeliverableID (DEL-011-05)
- PricingMode values: UNIT_RATE (12 rows), LUMP_SUM (12 rows) — all valid
- All rows trace to a source document (Datasheet, Specification, or Procedure) and section
- No TBD quantities (all quantities are numerically resolved, though some are ASSUMPTIONS)

### Detail.csv
**PASS.**
- Columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- 24 rows, all with valid Method values
- Method distribution: PARAMETRIC (20 rows, 83.3%), ALLOWANCE (4 rows, 16.7%)
- Allowance/parametric convention: All LUMP_SUM items have Qty=1, Unit=LS, UnitRate=Amount — **PASS**
- All ItemIDs in Detail.csv trace back to Items.csv — **PASS**

---

## S6 — Provenance Discipline

**PASS (with notes).**
- **Provenance completeness:** 24/24 rows (100%) have non-TBD SourceRef values.
- 17 rows reference specific price source files (PS-01 through PS-06) with item IDs.
- 7 rows reference Decision_Log.md entries (DEC-003 through DEC-012) for items where rates were derived parametrically from comparable items.
- **No rows have `location TBD` SourceRef.**

---

## S7 — Status Reporting

**RUN_STATUS: WARNINGS**

Rationale:
- Totals are meaningful ($145,257 CAD for 24 line items).
- Material TBDs remain in the underlying engineering documents (steel plate dimensions, wall material, overhead door height, clear ceiling height, floor drainage slope).
- 4 of 24 lines (16.7%) use ALLOWANCE method, which is permitted under ALLOW_MIXED_METHODS=TRUE but introduces uncertainty.
- Gantry provisions ($5,000) are conditional and may be removed.
- Steel plate scope ownership conflict (C-01) creates risk of double-counting with DEL-011-02.

---

## Quantity Takeoff Coverage

| Source Document | Items Extracted | Notes |
|---|---|---|
| Datasheet | 9 items (I-001 through I-009, I-015) | All major physical elements identified |
| Specification | 4 items (I-010, I-011, I-012, I-019) | Structural provisions, drainage coordination, professional staff |
| Procedure | 8 items (I-013, I-014, I-016, I-017, I-018, I-020 through I-024) | Labour, inspections, coordination, documentation |
| Guidance | 0 items directly | Guidance informed interpretation of other items but no unique priceable items |

**Deliverables with missing documents:** None. All 4 documents present for DEL-011-05.

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total line items | 24 |
| Items priced (non-TBD Amount) | 24 (100%) |
| Items with TBD Amount | 0 (0%) |
| PARAMETRIC method | 20 (83.3%) |
| ALLOWANCE method | 4 (16.7%) |

---

## Basis-Consistency Checks

- **Primary basis:** PARAMETRIC
- **Method mix:** 83.3% PARAMETRIC, 16.7% ALLOWANCE
- **ALLOW_MIXED_METHODS:** TRUE — method mix is permitted
- **FALLBACK_POLICY:** ALLOW_PARAMETRIC — parametric derivations for items without direct rate evidence are permitted
- **Assessment:** Basis-consistent. ALLOWANCE items are limited to cases where specifications are genuinely TBD (steel plates, overhead door, gantry). All ALLOWANCE items are documented in Decision_Log.md.

---

## What to Fix for a Cleaner Rerun

1. **Resolve TBD attributes in Datasheet:** Steel plate dimensions (B-001), wall construction material (B-003), overhead door height (A-001), clear ceiling height (C-001), floor drainage slope (F-002). These would allow replacing ALLOWANCE lines with PARAMETRIC lines at higher confidence.

2. **Resolve steel plate scope ownership (Conflict C-01):** Confirm whether DEL-011-05 or DEL-011-02 owns the wash bay floor steel plates to eliminate double-counting risk.

3. **Confirm or remove gantry provisions (B-002):** Owner confirmation would either firm up the $5,000 allowance or allow its removal.

4. **Obtain IFC drawings:** Most TBD items depend on IFC drawing issuance. Once IFC drawings are available, a rerun would significantly improve confidence across all CBS categories.

5. **Detailed crew-day analysis:** Replace parametric labour hours with a bottom-up crew-day estimate based on actual crew sizes and productivity rates for the site.

---

## S8 — Operator Acceptance Checklist

| Check | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with clearly bounded gaps | WARNINGS — gaps are bounded and documented |
| Quantity takeoff (Items.csv) reviewed for completeness | 24 items extracted from 4 documents; no missing documents |
| Basis-consistency checks pass | PASS — 83.3% PARAMETRIC, 16.7% ALLOWANCE permitted |
| Provenance completeness reported and top gaps actionable | 100% provenance; 7 lines reference Decision_Log entries |
| Scope coverage explicit | 1 deliverable in scope; exclusions documented |
| No writes outside _Estimates/ | PASS |
