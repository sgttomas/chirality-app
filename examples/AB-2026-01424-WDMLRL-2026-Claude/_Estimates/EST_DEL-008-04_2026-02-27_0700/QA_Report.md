# QA Report — EST_DEL-008-04_2026-02-27_0700

## RUN_STATUS: WARNINGS

**Rationale:** All 13 items are priced and totals are meaningful ($9,930 CAD). However, Surveyor hours are fully parametric (LOE source shows TBD), several scope definition items remain TBD (accuracy standard, deliverable format, conformance tolerance), and no equipment/travel costs are included. The estimate is suitable for budgeting purposes with the caveats documented below.

---

## S1 — Write Quarantine Respected

**PASS.** All outputs written under `_Estimates/EST_DEL-008-04_2026-02-27_0700/`. No files outside the estimating tool root were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-008-04_2026-02-27_0700` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` -- valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts present:
- [x] Run_Context.md
- [x] Items.csv
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv
- [x] Detail.csv (recommended; produced)
- [x] Risk_Register.md (optional; produced)

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**
- Parseable: Yes (13 data rows + 1 header)
- Required columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes
- All rows trace to a source document (Procedure: 13 items)
- PricingMode values: LUMP_SUM (11 items), UNIT_RATE (2 items) -- all valid
- Lump-sum convention: Qty=1, Unit=LS for all LUMP_SUM items -- correct
- No TBD quantities (all items have defined Qty)

### Detail.csv

**PASS.**
- Parseable: Yes (13 data rows + 1 header)
- Required columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- Method values: PARAMETRIC (13/13) -- all valid; consistent with BASIS_OF_ESTIMATE=PARAMETRIC
- No allowance/parametric convention violations for lump-sum items (lump-sum items are priced as hour-based line items with explicit Qty/Unit/UnitRate, not as Qty=1/LS/Amount convention -- this is acceptable because the pricing is genuinely unit-rate at the hour level even though the takeoff item is lump-sum)
- Currency: CAD (13/13) -- consistent
- Amount arithmetic verified: all 13 rows satisfy Amount = Qty x UnitRate

## S6 — Provenance Discipline

**PASS (with notes).**
- SourceRef completeness: 13/13 rows (100%) have non-TBD SourceRef values
- All SourceRef values point to Professional_Staff_Rates.csv with role ID, and where applicable to Level_of_Effort.csv
- Surveyor hour quantities are parametric estimates (not sourced from LOE) -- this is documented in SourceRef as "parametric estimate of effort" and in the Decision_Log

### Top provenance gaps:
1. Surveyor hours (DL-001 through DL-011): quantities are parametric estimates, not sourced from Level_of_Effort.csv. Rates are sourced. This is the primary provenance gap.
2. Drawing preparation effort (DL-007, 12 hr): depends on the TBD deliverable format (CAD vs PDF). If format is confirmed, hours could be adjusted.

## S7 — Status Reporting

**RUN_STATUS: WARNINGS**

Material TBDs/assumptions:
- Surveyor hours for DEL-008-04 are TBD in Level_of_Effort.csv; 60 hours estimated parametrically
- Deliverable format (CAD/PDF/digital) is TBD per Guidance GAP-002; affects drawing preparation effort
- Accuracy standard is TBD per Guidance GAP-001 (does not materially affect cost estimate)
- Conformance tolerance for IFC comparison is TBD per Guidance GAP-004 (does not materially affect cost estimate)
- No equipment, travel, or field technician costs included
- One Owner revision cycle assumed

Totals are meaningful for budgeting with the above caveats.

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS -- gaps are bounded and documented |
| Items.csv reviewed for completeness | PASS | 13 items covering all 6 Procedure steps including pre-field prep, field survey (control + topo + infrastructure + notes), office reduction (data processing + drawings + IFC comparison + report), QA, submission, and PM/CE |
| Basis-consistency checks pass | PASS | All 13 lines use Method=PARAMETRIC; consistent with BASIS_OF_ESTIMATE=PARAMETRIC |
| Provenance completeness reported | PASS | 100% SourceRef populated; parametric hour gaps documented |
| Scope coverage explicit | PASS | 1 deliverable (DEL-008-04) in scope; all 6 Procedure steps covered plus PM/CE |
| No writes outside _Estimates/ | PASS | Confirmed |

---

## What to Fix for a Cleaner Rerun

1. **Provide Surveyor (R-21) hours in Level_of_Effort.csv for DEL-008-04.** Currently shows "TBD". Providing sourced hours would upgrade 11 of 13 lines from parametric estimate to sourced LOE.
2. **Confirm deliverable format (CAD/PDF/digital).** This resolves Guidance GAP-002 and allows drawing preparation hours (DL-007, currently 12 hr / $1,680) to be calibrated to the actual output requirements.
3. **Add equipment and travel rates to PRICE_SOURCES** if survey equipment and mobilization are priced separately from the Surveyor's hourly rate.
4. **Add field technician / survey assistant role and rate** if a two-person crew is required for the field survey.
5. **Confirm whether Owner revision cycle effort is appropriate.** DL-011 assumes one round of comments; if multiple rounds are expected, adjust accordingly.
