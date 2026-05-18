# QA Report — EST_DEL-008-03_2026-02-27_0630

## RUN_STATUS: WARNINGS

**Rationale:** All 23 items are priced and totals are meaningful ($26,450 CAD). However, Surveyor hours are fully parametric (LOE source shows TBD), progress survey frequency is undefined, and several material TBDs remain in the scope definition. The estimate is suitable for budgeting purposes with the caveats documented below.

---

## S1 — Write Quarantine Respected

**PASS.** All outputs written under `_Estimates/EST_DEL-008-03_2026-02-27_0630/`. No files outside the estimating tool root were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-008-03_2026-02-27_0630` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

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
- Parseable: Yes (23 data rows + 1 header)
- Required columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes
- All rows trace to a source document (Procedure: 22 items; Guidance: 1 item)
- PricingMode values: LUMP_SUM (21 items), UNIT_RATE (2 items) — all valid
- Lump-sum convention: Qty=1, Unit=LS for all LUMP_SUM items — correct
- No TBD quantities (all items have defined Qty)

### Detail.csv

**PASS.**
- Parseable: Yes (23 data rows + 1 header)
- Required columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- Method values: PARAMETRIC (23/23) — all valid; consistent with BASIS_OF_ESTIMATE=PARAMETRIC
- No allowance/parametric convention violations for lump-sum items (lump-sum items are priced as hour-based line items with explicit Qty/Unit/UnitRate, not as Qty=1/LS/Amount convention — this is acceptable because the pricing is genuinely unit-rate at the hour level even though the takeoff item is lump-sum)
- Currency: CAD (23/23) — consistent

## S6 — Provenance Discipline

**PASS (with notes).**
- SourceRef completeness: 23/23 rows (100%) have non-TBD SourceRef values
- All SourceRef values point to Professional_Staff_Rates.csv with role ID, and where applicable to Level_of_Effort.csv
- Surveyor hour quantities are parametric estimates (not sourced from LOE) — this is documented in SourceRef as "parametric estimate of effort" and in the Decision_Log

### Top provenance gaps:
1. Surveyor hours (DL-001 through DL-021): quantities are parametric estimates, not sourced from Level_of_Effort.csv. Rates are sourced. This is the primary provenance gap.
2. Progress survey visits (DL-016): 8 visits is a parametric assumption; actual frequency TBD per Construction Survey Plan.

## S7 — Status Reporting

**RUN_STATUS: WARNINGS**

Material TBDs/assumptions:
- Surveyor hours for DEL-008-03 are TBD in Level_of_Effort.csv; 178 hours estimated parametrically
- Progress survey frequency TBD (8 visits assumed)
- Survey accuracy tolerances TBD (does not affect cost estimate)
- Geodetic datum/projection/vertical datum TBD (does not affect cost estimate)
- Foundation re-staking extent depends on geotech report outcome (risk)
- No equipment, travel, or field technician costs included

Totals are meaningful for budgeting with the above caveats.

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS — gaps are bounded and documented |
| Items.csv reviewed for completeness | PASS | 23 items covering all 4 Procedure phases (A-D) + OH&S + PM + CE |
| Basis-consistency checks pass | PASS | All 23 lines use Method=PARAMETRIC; consistent with BASIS_OF_ESTIMATE=PARAMETRIC |
| Provenance completeness reported | PASS | 100% SourceRef populated; parametric hour gaps documented |
| Scope coverage explicit | PASS | 1 deliverable (DEL-008-03) in scope; all 17 Procedure steps covered plus PM/CE/OH&S |
| No writes outside _Estimates/ | PASS | Confirmed |

---

## What to Fix for a Cleaner Rerun

1. **Provide Surveyor (R-21) hours in Level_of_Effort.csv for DEL-008-03.** Currently shows "TBD". Providing sourced hours would upgrade 21 of 23 lines from parametric estimate to sourced LOE.
2. **Define progress survey frequency.** Currently estimated at 8 visits; actual frequency should be defined in the Construction Survey Plan or construction schedule. This would improve confidence on the single largest line item (DL-016, $4,480).
3. **Confirm whether Construction Survey Summary Report is required.** ITEM-019 / DL-019 ($1,120) is included as likely but conditional per Procedure Step D2.
4. **Add equipment and travel rates to PRICE_SOURCES** if survey equipment and mobilization are priced separately from the Surveyor's hourly rate.
5. **Add field technician / survey assistant role and rate** if a two-person crew is required.
