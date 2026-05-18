# QA Report — EST_DEL-005-02_2026-02-26_2246

## RUN_STATUS: OK

---

## Schema Validity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to a source document and section | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS — all 4 rows are UNIT_RATE |
| No TBD quantities | PASS — all quantities are numeric |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid | PASS — all 4 rows are PARAMETRIC |
| Allowance/parametric convention | N/A — all items are UNIT_RATE with hours as quantity (not lump sum) |
| Amount computation check | PASS — all Amount = Qty x UnitRate verified |

**Amount verification:**
- L-001: 6 x 165 = 990 PASS
- L-002: 4 x 135 = 540 PASS
- L-003: 36 x 95 = 3420 PASS
- L-004: 84 x 160 = 13440 PASS
- Total: 990 + 540 + 3420 + 13440 = 18390 PASS

---

## Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-005-02) |
| Items extracted | 4 |
| Items with numeric quantities | 4 / 4 (100%) |
| Items with TBD quantities | 0 / 4 (0%) |
| Source documents read | 5 / 5 (_CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md) |
| Missing documents | 0 |

**Notes:** DEL-005-02 is a design deliverable (IFC Drawing Set). Priceable items are professional design labour hours, not construction materials or equipment. All four roles identified in Level_of_Effort.csv for this deliverable are captured.

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Items priced | 4 / 4 (100%) |
| Items with TBD amounts | 0 / 4 (0%) |
| Total priced amount | $18,390.00 CAD |
| Pricing method distribution | PARAMETRIC: 4/4 (100%) |

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Rows with non-TBD SourceRef | 4 / 4 (100%) |
| Rows with TBD SourceRef | 0 / 4 (0%) |

All SourceRef values point to specific rows in Level_of_Effort.csv (for quantities) and Professional_Staff_Rates.csv (for unit rates).

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE declared | PARAMETRIC |
| All Detail.csv Method values | PARAMETRIC |
| Method mix consistent with basis | PASS — 100% PARAMETRIC, matches declared basis |
| ALLOW_MIXED_METHODS exercised | No — not needed (all lines consistent) |
| FALLBACK_POLICY exercised | No — all items have full pricing evidence |

---

## Scope Coverage

| Item | Status |
|---|---|
| DEL-005-02 in-scope items identified | 4 (professional design roles) |
| Construction items explicitly excluded | Yes — construction execution under PKG-018 (out of scope per Specification) |
| Bulk cut/fill | Out of scope — County forces (R-01 SS3.3.1) |
| Aggregate supply | Out of scope — County (R-01 SS3.3.1) |
| Drainage Plan (DEL-005-03) | Out of scope — separate deliverable |
| Driving Surface and Pad Layout (DEL-005-04) | Out of scope — separate deliverable |

---

## Warnings

None. All items are fully priced with traceable provenance.

---

## What to Fix for a Cleaner Rerun

1. **Replace PARAMETRIC rates with contracted/quoted rates** when actual staff rates are confirmed for this project.
2. **Validate hour allocations** against actual project complexity once geotechnical report (DEL-008-01) and preliminary survey (DEL-008-02) are available — site complexity may increase or decrease required design hours.
3. **Cross-check fee percentage** once a confirmed civil construction value is available for the sitework scope (DF-05 suggests 1.0% of construction value for civil design).
4. **Consider adding allowance hours** for design iterations if County review of preliminary design (DEL-005-01) requires significant revision cycles.
