# QA Report — EST_DEL-002-05_2026-02-27_0600

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and all 12 line items are priced with traceable sources. However, 8 of 12 items are parametric lump-sum allowances with assumed hours (not directly from Level_of_Effort.csv), and 1 item is conditional on an unresolved conflict ruling (CF-DS-002). Rate confidence is MEDIUM across all sources.

---

## 1. Schema Validity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows have non-empty ItemID | PASS |
| All rows trace to a source document and section | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Row count | 12 items |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All rows have non-empty LineID and ItemID | PASS |
| Method values valid (all PARAMETRIC) | PASS |
| Allowance/parametric convention: Qty=1, Unit=LS, UnitRate=Amount for lump-sum items | PASS |
| Row count | 12 lines |
| All ItemIDs in Detail.csv exist in Items.csv | PASS |

---

## 2. Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-002-05) |
| Documents read | 4 of 4 (Datasheet, Specification, Guidance, Procedure) + _CONTEXT.md |
| Missing documents | 0 |
| Items extracted | 12 |
| Items with TBD quantity | 0 |
| Items with determined quantity | 12 (4 from LOE.csv, 8 parametric LS) |

**Coverage assessment:** All four production documents were read. Priceable items span the full lifecycle of the deliverable: design (Steps 2-4), QA (Step 5), IFC release (Step 6), and construction support (Step 7). Regulatory determination items (seismic, fire protection, corrosion) are extracted from Specification requirements.

---

## 3. Pricing Coverage

| Metric | Value |
|---|---|
| Total line items | 12 |
| Items priced (non-TBD Amount) | 12 (100%) |
| Items with TBD Amount | 0 (0%) |
| Total estimate | $27,730 CAD |
| Direct LOE items (from Level_of_Effort.csv) | 4 items, $19,230 (69.4% of total) |
| Parametric allowance items (assumed hours) | 8 items, $8,500 (30.6% of total) |

---

## 4. Provenance Completeness

| Metric | Value |
|---|---|
| Rows with non-TBD SourceRef | 12 of 12 (100%) |
| Rows with "location TBD" | 0 |
| Top missing-source offenders | None |

**Assessment:** All 12 rows have traceable SourceRef pointing to specific pricing evidence files (Level_of_Effort.csv, Professional_Staff_Rates.csv) and/or Assumptions_Log.md entries for parametric allowances.

---

## 5. Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| All Method values | PARAMETRIC |
| Method mix consistent with basis | PASS (100% PARAMETRIC) |
| ALLOW_MIXED_METHODS | TRUE (not exercised — all methods match) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC (not exercised — no missing pricing) |

---

## 6. Scope Coverage

| Metric | Value |
|---|---|
| Deliverables included | 1: DEL-002-05 Mezzanine Framing Details |
| Deliverables excluded | N/A (single-deliverable scope) |
| SOW items covered | SOW-0012, SOW-0032, SOW-0033, SOW-0034 |

---

## 7. Warnings

| ID | Severity | Description |
|---|---|---|
| W-001 | MEDIUM | 8 of 12 items ($8,500 / 30.6% of total) are parametric allowances with assumed hours not directly from Level_of_Effort.csv. Hour assumptions documented in Assumptions_Log.md. |
| W-002 | LOW | ITEM-009 ($680) is conditional on unresolved conflict CF-DS-002 (mezzanine extent over wash bay). If wash bay mezzanine is eliminated, this item may be reduced. |
| W-003 | LOW | Field review effort (ITEM-008, $2,720) has highest variability risk. Actual effort depends on construction complexity and inspection schedule. |
| W-004 | LOW | All staff rates are MEDIUM confidence (per Professional_Staff_Rates.csv). Rates should be validated against actual contract rates when available. |
| W-005 | INFO | This estimate covers professional design services only. Construction material/labour costs for the mezzanine itself are not included. |

---

## 8. What to Fix for a Cleaner Rerun

1. **Resolve CF-DS-002** (mezzanine extent over wash bay) to confirm or remove ITEM-009 conditional status.
2. **Validate parametric hour assumptions** (ASM-002 through ASM-009) against actual project experience or historical data for similar mezzanine drawing sets.
3. **Update staff rates** from MEDIUM to HIGH confidence when actual contract rates are available.
4. **Separate construction support** into its own deliverable or CBS if the project tracks design vs. construction support costs independently.

---

## 9. Operator Acceptance Checklist (S8)

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS — WARNINGS with clearly bounded gaps (see W-001 through W-005) |
| Items.csv reviewed for completeness | PASS — 12 items covering full deliverable lifecycle |
| Basis-consistency checks pass | PASS — 100% PARAMETRIC |
| Provenance completeness reported | PASS — 100% SourceRef coverage |
| Scope coverage explicit | PASS — 1 deliverable, 4 SOW items covered |
| No writes outside _Estimates/ | PASS — all output in EST_DEL-002-05_2026-02-27_0600/ |
