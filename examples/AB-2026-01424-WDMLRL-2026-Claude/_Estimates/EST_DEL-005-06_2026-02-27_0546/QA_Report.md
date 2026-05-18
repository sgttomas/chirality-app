# QA Report — EST_DEL-005-06_2026-02-27_0546

## RUN_STATUS: OK

All items are priced with traceable sources. No critical input gaps. Totals are meaningful.

---

## Schema Validity

### Items.csv

| Check | Result |
|---|---|
| File parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| Row count | 21 rows (4 priced labour items + 17 scope traceability items) |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS — 4 UNIT_RATE, 17 LUMP_SUM |
| All rows trace to a SourceDoc | PASS |
| All rows trace to a SourceSection | PASS |
| No TBD quantities on priced labour items | PASS |

### Detail.csv

| Check | Result |
|---|---|
| File parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Row count | 4 rows |
| Method values valid (all PARAMETRIC) | PASS |
| Allowance/parametric convention respected | N/A — all items are UNIT_RATE with hr quantities; not lump-sum parametric |
| All ItemIDs trace back to Items.csv | PASS |
| All Amounts are numeric (no TBD) | PASS |
| Amount = Qty x UnitRate for all rows | PASS (6x165=990; 4x135=540; 24x95=2280; 56x160=8960) |

### WBS_CBS_Matrix.csv

| Check | Result |
|---|---|
| File parseable | PASS |
| Required columns present | PASS |
| LABOUR-MGMT total (1,530) = DL-001 (990) + DL-002 (540) | PASS |
| LABOUR-DESIGN total (11,240) = DL-003 (2,280) + DL-004 (8,960) | PASS |
| Grand total (12,770) = LABOUR-MGMT (1,530) + LABOUR-DESIGN (11,240) | PASS |

---

## Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Total items extracted | 21 |
| Priced labour items (ITM-001 to ITM-004) | 4 |
| Scope traceability items (ITM-005 to ITM-021) | 17 |
| Items with TBD quantities | 0 |
| Deliverables with missing documents | 0 (all 4 documents + _CONTEXT.md read successfully) |

### Items by Source Document

| SourceDoc | Count |
|---|---|
| Procedure | 11 |
| Specification | 7 |
| Datasheet | 3 |
| Guidance | 1 (ITM-021 interdisciplinary coordination — also references Procedure) |

### Calculation Topic Coverage (Datasheet Construction Table)

| Datasheet Topic | Covered By |
|---|---|
| Drainage system sizing | ITM-005 |
| Stormwater detention/retention | ITM-006 |
| Hydrologic and hydraulic analysis | ITM-005 (combined) |
| Finish grading and cut/fill volume calculations | ITM-007 |
| Pavement / driving surface design | ITM-008 |
| Slope stability analysis | ITM-009 |
| Utility sizing calculations | ITM-010 |
| Design compliance verification | ITM-016 |
| Summary of design assumptions | ITM-020 |
| References to design standards and codes | ITM-020 |

All 10 calculation topics from the Datasheet Construction table are covered.

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Items with pricing (Amount != TBD) | 4 of 4 priced items (100%) |
| Items with TBD pricing | 0 |
| Scope traceability items (no standalone price; embedded in labour) | 17 |
| Total estimated amount | $12,770 CAD |

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Detail.csv rows with non-TBD SourceRef | 4 of 4 (100%) |
| Provenance completeness | 100% |
| Top missing-source offenders | None |

All SourceRef entries reference specific rows in Level_of_Effort.csv and Professional_Staff_Rates.csv with role IDs and rate values.

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE declared | PARAMETRIC |
| All Detail.csv Method values | PARAMETRIC (4/4) |
| Method mix consistent with basis | PASS — 100% PARAMETRIC, consistent with declared basis |
| FALLBACK_POLICY invoked | No — no fallback required; all items priced via primary basis |
| ALLOW_MIXED_METHODS relevant | No — single method used throughout |

---

## Scope Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-005-06) |
| Deliverables estimated | 1 |
| Packages in scope | 1 (PKG-005) |
| Documents read | 5 (_CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md) |
| Documents missing | 0 |
| Specification requirements covered by items | REQ-001 through REQ-014 (14 of 14) |
| Procedure steps covered by items | Steps 1 through 9 including 4A (all steps) |

---

## What to Fix for a Cleaner Rerun

1. **Nothing critical.** This run produced complete, traceable outputs with no TBD amounts.
2. **Optional enhancement — bottom-up hours validation:** The parametric hours from Level_of_Effort.csv could be validated against a bottom-up task estimate derived from the 9 Procedure steps (plus Step 4A). This would strengthen confidence from MEDIUM to HIGH.
3. **Optional enhancement — fee cross-check:** When a construction value estimate for the civil works is available, the Professional_Design_Fees.csv DF-05 cross-check (civil design at 1.0% of construction value) can be computed. The calculation package is a subset of the full civil design scope, so only a portion of the fee percentage would apply.
4. **Upstream dependency tracking:** If DEL-008-01 or DEL-008-02 are delayed, the calculation package schedule will shift but the effort estimate remains valid. If geotechnical conditions are significantly adverse, additional engineering hours for slope stability analysis may be required.

---

## Write Quarantine Verification

All files written to: `_Estimates/EST_DEL-005-06_2026-02-27_0546/`

No files outside `_Estimates/` were modified. Write quarantine respected.
