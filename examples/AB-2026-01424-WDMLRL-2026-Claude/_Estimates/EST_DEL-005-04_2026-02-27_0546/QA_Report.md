# QA Report — EST_DEL-005-04_2026-02-27_0546

## RUN_STATUS: OK

---

## Schema Validity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows have non-empty ItemID | PASS |
| All rows trace to a source document and section | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS — all 4 rows are UNIT_RATE |
| Row count | 4 |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All ItemIDs reference Items.csv | PASS — I-001, I-002, I-003, I-004 all present in Items.csv |
| Method values valid (QUOTE, RATE_TABLE, HISTORICAL, ALLOWANCE, PARAMETRIC) | PASS — all 4 rows are PARAMETRIC |
| Allowance/parametric convention respected | N/A — all items are UNIT_RATE with actual quantities (hours), not lump-sum parametric |
| Amount = Qty x UnitRate for all rows | PASS (84x160=13440; 36x95=3420; 6x165=990; 4x135=540) |
| Row count | 4 |

---

## Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-005-04) |
| Items extracted | 4 |
| Items with TBD quantities | 0 |
| Documents read | 4 of 4 (Datasheet, Specification, Guidance, Procedure) |
| Missing documents | 0 |

### Item Coverage by Source Document

| SourceDoc | Items |
|---|---|
| Procedure | 4 (all items derive work activities from the Procedure steps; quantities from Level_of_Effort.csv) |

**Note:** This is a design deliverable. Priceable items are professional services hours, not material quantities. The Procedure document defines the work steps; the Level_of_Effort.csv provides the parametric hour estimates per role. Datasheet, Specification, and Guidance were read to understand scope and confirm the work content but do not directly generate separate priceable items for a design drawing set.

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total line items in Detail.csv | 4 |
| Items with Amount = TBD | 0 |
| Items with numeric Amount | 4 |
| **Pricing coverage** | **100%** |

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Total rows in Detail.csv | 4 |
| Rows with non-TBD SourceRef | 4 |
| Rows with TBD SourceRef | 0 |
| **Provenance completeness** | **100%** |

### Top Missing-Source Offenders

None. All rows have complete provenance referencing both Level_of_Effort.csv (for hours) and Professional_Staff_Rates.csv (for rates).

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (4 of 4) |
| Non-basis methods used | None |
| Fallback policy invoked | No |
| **Basis consistency** | **PASS** — 100% of lines match the declared basis |

---

## Scope Coverage

| Metric | Value |
|---|---|
| Deliverables included | 1 — DEL-005-04 |
| Deliverables excluded | 0 |
| Packages touched | 1 — PKG-005 |

**Scope notes:**
- This estimate covers design services only (producing the Drawing Set).
- Construction scope for driving surfaces, cement pad, and gravel pad falls under PKG-018 (Sitework & Civil Construction) and is not included.
- Geotechnical investigation (PKG-008), which is a design input, is estimated separately.

---

## Write Quarantine Check

| Check | Result |
|---|---|
| All outputs written under _Estimates/ | PASS |
| No modifications to deliverable working files | PASS |
| No modifications to lifecycle files | PASS |
| No modifications to decomposition outputs | PASS |

---

## What to Fix for a Cleaner Rerun

1. No fixes required — this run produced complete, consistent outputs with 100% pricing coverage and 100% provenance completeness.
2. **Optional enhancement:** If construction value for the overall project becomes available, a cross-check against Professional_Design_Fees.csv (DF-05: civil design fee at 1.0% of construction value) could validate the LOE-based total as a reasonableness check.
