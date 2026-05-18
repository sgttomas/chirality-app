# QA Report — EST_DEL-004-05_2026-02-27_0630

## RUN_STATUS: OK

**Justification:** All required inputs were available. All line items were priced with full provenance. No critical input gaps. Totals are meaningful.

---

## 1. Schema Validity

### Items.csv

| Check | Result |
|---|---|
| File parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All ItemIDs unique | PASS (ITEM-001 through ITEM-012) |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| All rows trace to a source document | PASS (Datasheet, Specification, Procedure) |
| All rows trace to a source section | PASS |

### Detail.csv

| Check | Result |
|---|---|
| File parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All LineIDs unique | PASS (DL-001 through DL-004) |
| Method values valid (PARAMETRIC for all) | PASS |
| Allowance/parametric convention respected (N/A — all lines are UNIT_RATE with Qty > 1) | PASS (not applicable; no LS lines in Detail.csv) |
| All ItemIDs trace back to Items.csv | PASS (ITEM-001 through ITEM-004) |

---

## 2. Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-004-05) |
| Documents read | 5 (_CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md) |
| Missing documents | 0 |
| Items extracted (Items.csv) | 12 |
| Items with numeric Qty | 4 (ITEM-001 through ITEM-004: hours-based) |
| Items with Qty = 1 / LS | 8 (ITEM-005 through ITEM-012: traceability items embedded in primary labour lines) |
| Items with Qty = TBD | 0 |

**Note:** Items ITEM-005 through ITEM-012 are extracted for traceability to specific deliverable content (GFCI assessment, AFCI determination, legend preparation, etc.). Their effort is embedded within the primary labour lines (ITEM-001 through ITEM-004) and they are not independently priced in Detail.csv to avoid double-counting.

---

## 3. Pricing Coverage

| Metric | Value |
|---|---|
| Total line items in Detail.csv | 4 |
| Items priced (Amount != TBD) | 4 (100%) |
| Items with TBD Amount | 0 (0%) |
| Total estimated amount | $18,810.00 CAD |

---

## 4. Provenance Completeness

| Metric | Value |
|---|---|
| Detail.csv rows with non-TBD SourceRef | 4 of 4 (100%) |
| Detail.csv rows with "location TBD" SourceRef | 0 |
| Top missing-source offenders | None |

All priced rows reference both the rate source (Professional_Staff_Rates.csv with role ID) and the quantity source (Level_of_Effort.csv with deliverable/role combination).

---

## 5. Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE declared | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (100%) |
| Method mix consistent with basis | PASS — all lines use PARAMETRIC method, matching declared basis |
| Fallback used | No — all items were priced from primary sources |
| ALLOW_MIXED_METHODS exercised | No — not needed; all lines are PARAMETRIC |

---

## 6. Scope Coverage

| Item | Status |
|---|---|
| DEL-004-05 Receptacle Layout Plans | INCLUDED — fully estimated |
| Deliverables excluded | None within declared scope |
| Construction material/installation scope | EXCLUDED by design — this estimate covers professional design fees only |

**Scope boundary note:** The four deliverable documents describe significant engineering content (9 zones, 5 receptacle types, GFCI/AFCI requirements, code compliance, multi-deliverable coordination). The Level_of_Effort.csv parametric model allocates 130 total hours across 4 roles, which is consistent with a Drawing Set deliverable for a ~13,000 sqft industrial maintenance shop.

---

## 7. Write Quarantine Check

| Check | Result |
|---|---|
| All files written under _Estimates/ | PASS |
| No files modified outside _Estimates/ | PASS |
| Snapshot folder is new (no overwrite of existing) | PASS |
| UPDATE_LATEST_POINTER = FALSE respected | PASS (no pointer file modified) |

---

## 8. Operator Acceptance Checklist (S8)

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS — OK |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS — 12 items extracted covering all major work activities from all 4 documents |
| Basis-consistency checks pass | PASS — 100% PARAMETRIC |
| Provenance completeness reported | PASS — 100% provenance |
| Scope coverage explicit | PASS — 1 deliverable included; construction scope explicitly excluded |
| No writes outside _Estimates/ | PASS |

---

## What to Fix for a Cleaner Rerun

1. **Nothing critical.** This run completed successfully with full pricing coverage and provenance.
2. **Optional enhancement:** If construction cost estimates become available, the Professional_Design_Fees.csv cross-check (DF-04: 1.6% of construction value) could be used to validate the LOE-based estimate against a percentage-of-construction benchmark.
3. **Watch item:** If County-supplied welder specifications change the 50 A/240 V assumption (D-009), a re-estimation may be warranted to account for potential redesign effort.
