# QA Report — EST_DEL-017-03_2026-02-27_0730

**RUN_STATUS: WARNINGS**

---

## 1. Schema Validity

### Items.csv
| Check | Result |
|---|---|
| Parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to SourceDoc and SourceSection | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Total rows | 35 |

### Detail.csv
| Check | Result |
|---|---|
| Parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (all PARAMETRIC) | PASS |
| Allowance/parametric convention respected (Qty=1, Unit=LS, UnitRate=Amount for LS items) | PASS |
| Total rows | 35 |

---

## 2. Quantity Takeoff Coverage

| Deliverable | Items Extracted | Documents Read | Missing Documents |
|---|---|---|---|
| DEL-017-03 | 35 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | None |

### Items by Source Document
| SourceDoc | Item Count |
|---|---|
| Procedure | 29 |
| Datasheet | 6 |

### TBD Quantities in Items.csv
| ItemID | Description | Notes |
|---|---|---|
| ITEM-014 | Framing and partition work | Qty TBD; ASSUMPTION: 15 m2 |
| ITEM-015 | Wall finishes | Qty TBD; ASSUMPTION: 30 m2 |
| ITEM-016 | Floor finishes | Qty TBD; ASSUMPTION: 12 m2 |
| ITEM-023 | Paint | Qty TBD; ASSUMPTION: 15 m2 |
| ITEM-035 | Ceiling finish | Qty TBD; ASSUMPTION: 12 m2 |

**Assessment:** 5 of 35 items have TBD quantities with parametric assumptions applied. All TBDs are due to the conceptual-level scope definition; existing washroom footprint is not dimensioned in available drawings. Quantities will be refined after existing condition survey (Procedure Step 1.1).

---

## 3. Pricing Coverage

| Metric | Value |
|---|---|
| Total line items (Detail.csv) | 35 |
| Items priced | 35 (100%) |
| Items with TBD Amount | 0 (0%) |
| Items priced via PARAMETRIC | 35 (100%) |

**Assessment:** All items are priced. No TBD amounts remain. However, 9 line items (DL-006, DL-009, DL-015, DL-017, DL-018, DL-019, DL-020, DL-021, DL-022) use parametric estimates without direct pricing source evidence; they carry `location TBD` or partial source references.

---

## 4. Provenance Completeness

| Metric | Value |
|---|---|
| Total line items | 35 |
| Lines with non-TBD SourceRef | 26 (74.3%) |
| Lines with `location TBD` in SourceRef | 9 (25.7%) |

### Top Missing-Source Offenders

| LineID | Description | Amount (CAD) | SourceRef Issue |
|---|---|---|---|
| DL-006 | Hazardous materials assessment | $2,500.00 | No hazmat pricing source; parametric allowance |
| DL-009 | Waste disposal | $800.00 | No waste disposal pricing source |
| DL-015 | Wall finishes (ceramic tile) | $2,700.00 | Ceramic tile rate not in PRICE_SOURCES |
| DL-017 | Toilet supply/install | $1,200.00 | No fixture pricing source |
| DL-018 | Sink supply/install | $900.00 | No fixture pricing source |
| DL-019 | Urinal supply/install | $1,100.00 | No fixture pricing source |
| DL-020 | Washroom accessories | $1,500.00 | No accessories pricing source |
| DL-021 | Exhaust fan | $650.00 | No mechanical equipment pricing source |
| DL-022 | Lighting fixtures | $700.00 | No lighting pricing source |

**Total amount with incomplete provenance:** $12,050.00 (28.0% of grand total)

---

## 5. Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Method values in Detail.csv | All PARAMETRIC (35 of 35) |
| Method mix deviation | NONE — 100% PARAMETRIC |
| Consistency | PASS |

---

## 6. Scope Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-017-03) |
| Deliverables estimated | 1 |
| SOW items covered | SOW-0072 (renovation), SOW-0074 (urinal expansion) |
| Excluded scope (per documents) | Locker/change room (DEL-017-04), plumbing system design (PKG-006), plumbing installation (PKG-014), mezzanine renovation (DEL-017-02), permit fees (County) |

---

## 7. Write Quarantine Verification

| Check | Result |
|---|---|
| All outputs written under `_Estimates/` | PASS |
| No modifications to deliverable content | PASS |
| No modifications to lifecycle files | PASS |
| No modifications to decomposition outputs | PASS |
| No modifications to dependency registers | PASS |

---

## 8. Operator Acceptance Checklist (S8)

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | WARNINGS | Material TBDs in quantities (5 items) and 9 lines without direct source evidence |
| Quantity takeoff reviewed for completeness | REVIEWED | 35 items extracted from all 4 documents; 5 items have assumed quantities |
| Basis-consistency checks pass | PASS | 100% PARAMETRIC |
| Provenance completeness reported | REPORTED | 74.3% complete; top 9 gaps identified and actionable |
| Scope coverage explicit | EXPLICIT | 1 deliverable, 2 SOW items; exclusions documented |
| No writes outside `_Estimates/` | PASS | Verified |

---

## 9. What to Fix for a Cleaner Rerun

1. **Add fixture pricing source** — provide quotes or rate tables for plumbing fixtures (toilet, sink, urinal), accessories, exhaust fan, and lighting fixtures. This would resolve 9 lines with incomplete provenance ($12,050 / 28% of total).
2. **Add ceramic tile pricing source** — wall tile rate ($90/m2) is parametric without direct source.
3. **Populate TBD quantities** — after existing condition survey (Procedure Step 1.1), update Datasheet with actual washroom footprint, fixture inventory, and expansion area. This would firm up 5 assumed quantities.
4. **Add waste disposal and hazmat pricing sources** — these are parametric allowances with no direct evidence.
5. **Confirm hot water requirement** — Procedure Step 3.1 [A-004] flags that hot water supply requirement is TBD; this may affect plumbing rough-in scope and cost.
