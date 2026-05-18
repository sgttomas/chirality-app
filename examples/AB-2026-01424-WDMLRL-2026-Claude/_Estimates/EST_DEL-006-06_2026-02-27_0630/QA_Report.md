# QA Report — EST_DEL-006-06_2026-02-27_0630

## RUN_STATUS: OK

---

## 1. Schema Validity

### Items.csv

| Check | Result |
|---|---|
| File exists and parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| All rows trace to a source document and section | PASS |
| Row count | 17 items |

### Detail.csv

| Check | Result |
|---|---|
| File exists and parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (PARAMETRIC for all 4 rows) | PASS |
| Allowance/parametric convention: N/A (all rows are UNIT_RATE with hours, not lump-sum parametric) | N/A |
| Row count | 4 detail lines |

### WBS_CBS_Matrix.csv

| Check | Result |
|---|---|
| File exists and parseable | PASS |
| Required columns present | PASS |
| Totals consistent with Detail.csv | PASS — Management: $990 + $540 = $1,530; Design: $1,995 + $7,840 = $9,835; Grand: $11,365 |

---

## 2. Quantity Takeoff Coverage

| Deliverable | Documents Read | Documents Missing | Items Extracted |
|---|---|---|---|
| DEL-006-06 | _CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md | None | 17 |

All four production documents and _CONTEXT.md were successfully read. No missing documents.

### Item Coverage by Source Document

| SourceDoc | Item Count |
|---|---|
| Procedure | 7 (ITEM-001 through ITEM-004, ITEM-015, ITEM-016, ITEM-017) |
| Datasheet | 2 (ITEM-005, ITEM-008) |
| Specification | 8 (ITEM-006, ITEM-007, ITEM-009, ITEM-010, ITEM-011, ITEM-012, ITEM-013, ITEM-014) |
| Guidance | 0 (guidance principles informed interpretation but no standalone priceable items) |

---

## 3. Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 17 |
| Items with priced Detail.csv lines | 4 (ITEM-001 through ITEM-004) |
| Items without Detail.csv pricing | 13 (ITEM-005 through ITEM-017) |
| Pricing coverage (priced / total items) | 23.5% |
| Pricing coverage (by dollar value) | 100% of professional services estimate is priced |
| TBD amounts in Detail.csv | 0 |

**Explanation:** ITEM-005 through ITEM-017 represent the *content* of the fixture schedule (the fixtures and activities being scheduled). These are design scope items documented in Items.csv for completeness and traceability but are not separately priced in the Detail.csv because:
- DEL-006-06 is a design deliverable (Schedule artifact type) whose cost is the professional effort to produce it
- The professional LOE (ITEM-001 through ITEM-004) inherently covers the work of scheduling all fixtures listed in ITEM-005 through ITEM-017
- Material/equipment costs for the fixtures themselves belong to a procurement or construction estimate (PKG-014), not the design deliverable estimate

---

## 4. Provenance Completeness

| Metric | Value |
|---|---|
| Detail.csv rows with non-TBD SourceRef | 4 / 4 (100%) |
| Detail.csv rows with TBD SourceRef | 0 |
| Top missing-source offenders | None |

All four priced detail lines have full provenance tracing to both the rate source (Professional_Staff_Rates.csv) and the effort source (Level_of_Effort.csv).

---

## 5. Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Method values in Detail.csv | All PARAMETRIC (4/4) |
| Mixed methods used | No |
| FALLBACK_POLICY invoked | No |
| Consistency | PASS — all methods match BASIS_OF_ESTIMATE |

---

## 6. Scope Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-006-06) |
| Deliverables estimated | 1 (DEL-006-06) |
| Deliverables excluded | 0 |
| Package | PKG-006 — Plumbing Design |

---

## 7. What to Fix for a Cleaner Rerun

1. **No critical fixes needed.** The estimate is complete for the professional services scope of DEL-006-06.

2. **Optional improvement — fixture material/equipment pricing.** If a future estimate run needs to price the actual fixtures (floor drains, emergency shower, industrial wash sink, etc.), a material/equipment price source for plumbing fixtures would need to be provided in PRICE_SOURCES. This is outside the current design deliverable scope.

3. **TBD fixture quantities.** Three items have TBD quantities (ITEM-006 sump drains, ITEM-010 Old North Shop washroom fixtures, ITEM-012 New North Shop washroom fixtures). These do not affect the current estimate but would need resolution if material pricing were added.

4. **Building occupancy classification (Specification C-007).** Confirmation of the Alberta Building Code occupancy classification would strengthen the code compliance items but does not affect professional LOE pricing.

---

## 8. Operator Acceptance Checklist (S8)

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (OK) |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS — 17 items extracted from all four documents |
| Basis-consistency checks pass | PASS — all PARAMETRIC |
| Provenance completeness reported | PASS — 100% |
| Scope coverage explicit | PASS — 1/1 deliverable estimated |
| No writes outside _Estimates/ | PASS |
