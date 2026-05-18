# QA Report — EST_DEL-011-02_2026-02-27_0848

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and a full set of line items has been priced, but material TBDs and assumptions remain due to upstream design deliverables not yet being issued. The estimate is suitable for budgetary planning but not for firm commitment.

---

## S1 — Write Quarantine Respected

**PASS.** All files written under `_Estimates/EST_DEL-011-02_2026-02-27_0848/`. No files outside `_Estimates/` were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-011-02_2026-02-27_0848` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts produced:
- [x] Run_Context.md
- [x] Items.csv (23 items)
- [x] Summary.md
- [x] QA_Report.md (this file)
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv
- [x] Detail.csv (23 lines — optional but produced)

## S5 — CSV Schema Integrity

### Items.csv
**PASS.**
- Columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes
- All 23 rows have valid PricingMode values (21x UNIT_RATE, 2x LUMP_SUM)
- All rows trace to a SourceDoc (Datasheet, Specification, Procedure, or Guidance) and SourceSection
- No TBD quantities in Qty field (all quantities are parametric estimates with documented basis)

### Detail.csv
**PASS.**
- Columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- All 23 rows have valid Method values (22x PARAMETRIC, 1x ALLOWANCE)
- Allowance/parametric convention: L-009 (LS, Qty=1, UnitRate=Amount), L-013 (LS, Qty=1, UnitRate=Amount), L-022 (LS, Qty=1, UnitRate=Amount) — all comply
- Amount = Qty x UnitRate for all rows: **PASS** (verified)

## S6 — Provenance Discipline

**PASS with notes.**
- Provenance completeness: **23/23 lines (100%)** have non-TBD SourceRef values
- All SourceRef entries point to specific price source files, rate table rows, or explicit assumption IDs
- Top provenance quality concerns (8 LOW confidence lines):
  1. L-001/L-002 (steel plate material): parametric derivation from SC-08 base + assumption; no direct quote — LOW confidence
  2. L-003/L-004 (anchorage hardware): parametric with no direct source — LOW confidence
  3. L-009 (plate surface protection): parametric lump sum with no direct source — LOW confidence
  4. L-015 (welding inspector): proxy rate with no direct source — LOW confidence
  5. L-022 (corrosion protection): ALLOWANCE with no direct source — LOW confidence
  6. L-023 (equipment rental): parametric with no direct source — LOW confidence

## S7 — Status Reporting

**RUN_STATUS = WARNINGS**

Reasons for WARNINGS (not OK):
1. Multiple line items at LOW confidence due to missing upstream engineering data (plate dimensions, anchorage details, design loads all TBD)
2. Steel plate material pricing is parametric without a direct supplier quote
3. Wash bay scope boundary unresolved (CON-011-02-03)
4. 8 of 23 line items (34.8%) have LOW confidence ratings

Reasons this is not FAILED_INPUTS:
1. All items are priced (no TBD amounts)
2. Pricing sources are sufficient for parametric estimates
3. Professional staff rates and construction labour rates have MEDIUM confidence from validated rate tables
4. Quantity takeoff is complete with documented assumptions

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS; gaps are clearly identified and bounded |
| Items.csv reviewed for completeness | PASS | 23 items covering materials, labour, professional services, equipment |
| Basis-consistency checks | PASS | 22/23 PARAMETRIC, 1/23 ALLOWANCE; consistent with ALLOW_MIXED_METHODS=TRUE |
| Provenance completeness reported | PASS | 100% SourceRef coverage; 5 lines with proxy/assumption-based rates |
| Scope coverage explicit | PASS | 1 deliverable (DEL-011-02) fully covered; wash bay scope inclusion noted |
| No writes outside _Estimates/ | PASS | Verified |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 23 |
| Items priced in Detail.csv | 23 |
| Items with TBD Amount | 0 |
| Pricing coverage | 100% |
| Lines with HIGH confidence | 0 |
| Lines with MEDIUM confidence | 15 (65.2%) |
| Lines with LOW confidence | 8 (34.8%) |

---

## Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-011-02) |
| Documents read — Datasheet | YES |
| Documents read — Specification | YES |
| Documents read — Guidance | YES |
| Documents read — Procedure | YES |
| Missing documents | NONE |
| Items extracted from Datasheet | 2 (ITEM-001, ITEM-002) |
| Items extracted from Specification | 6 (ITEM-003, ITEM-004, ITEM-012, ITEM-013, ITEM-015, ITEM-016) |
| Items extracted from Procedure | 8 (ITEM-005–ITEM-011, ITEM-014) |
| Items extracted from Guidance | 1 (ITEM-022) |
| Items from Level_of_Effort.csv | 5 (ITEM-017–ITEM-021) |
| Items from Procedure (equipment) | 1 (ITEM-023) |

---

## What to Fix for a Cleaner Rerun

1. **Obtain IFC drawings (DEL-002-08)** — Once the Steel Plate Embedment Plan is issued, update plate dimensions, thicknesses, exact count, and anchorage details. This will convert the parametric quantity estimates to measured quantities and significantly improve confidence.

2. **Obtain structural specification (DEL-002-12)** — Confirms material grade, welding standards, and installer qualification requirements.

3. **Obtain steel plate supplier quote** — Replace the parametric $3.80/kg material rate with a direct quote for the specified grade/thickness/quantity. This single change affects $9,804 (25.6% of total).

4. **Resolve wash bay scope boundary (CON-011-02-03)** — Confirm whether wash bay steel plates are in DEL-011-02 scope or reallocated to SOW-0027a/DEL-018-05.

5. **Confirm corrosion protection requirement** — Structural engineer decision on wash bay plate protection method will replace the $2,500 allowance with a costed specification.

6. **Obtain welding inspector quote** — Replace proxy rate with actual third-party welding inspection service quote.

7. **Obtain equipment rental quote** — Replace parametric telehandler rate with local rental house quote.
