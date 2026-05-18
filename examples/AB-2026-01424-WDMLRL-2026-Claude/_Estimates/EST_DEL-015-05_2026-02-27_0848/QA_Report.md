# QA Report — EST_DEL-015-05_2026-02-27_0848

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and all 22 line items are priced, but material TBDs remain in underlying quantities (camera count, conduit lengths, cable types) and two scope boundary confirmations (CONF-015-05-01, CONF-015-05-02) are unresolved. The estimate is suitable for budgetary planning but not for firm commitment.

---

## S1 — Write Quarantine Respected

- **PASS.** All files written under `_Estimates/EST_DEL-015-05_2026-02-27_0848/`. No project truth files modified.

## S2 — Snapshot Created

- **PASS.** Snapshot folder `EST_DEL-015-05_2026-02-27_0848` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

- **PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` is a valid enum value.

## S4 — Required Artifacts Exist

- **PASS.** All required artifacts present:
  - Run_Context.md
  - Items.csv (22 rows)
  - Detail.csv (22 rows)
  - Summary.md
  - QA_Report.md
  - Source_Index.md
  - WBS_CBS_Matrix.csv (8 rows)
  - Decision_Log.md
  - Assumptions_Log.md

## S5 — CSV Schema Integrity

### Items.csv
- **PASS.** All required columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes.
- **PASS.** All PricingMode values are valid (UNIT_RATE or LUMP_SUM).
- **PASS.** All 22 rows have non-empty SourceDoc and SourceSection.
- **PASS.** Lump-sum items (ITM-014, ITM-015, ITM-022) have Qty=1, Unit=LS.

### Detail.csv
- **PASS.** All required columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes.
- **PASS.** All Method values are valid (all PARAMETRIC).
- **PASS.** Lump-sum items (DL-014, DL-015, DL-022) have Qty=1, Unit=LS, UnitRate=Amount.
- **PASS.** All Amount values = Qty x UnitRate (verified).

## S6 — Provenance Discipline

- **PASS.** All 22 priced rows include a non-TBD SourceRef.
- **Provenance completeness:** 100% (22/22 rows have explicit SourceRef).
- **Top source references:**
  - Construction_Labour_Rates.csv T-04: 7 line items
  - Professional_Staff_Rates.csv + Level_of_Effort.csv: 6 line items
  - Electrical_System_Rates.csv ES-05: 2 line items
  - ASSUMPTION references: 7 line items (parametric material estimates)

### Provenance quality note
While 100% of rows have a SourceRef, 7 line items reference assumptions rather than direct rate evidence. These are parametric material cost estimates (conduit per meter, cable per meter, junction boxes, weatherhead, sleeves) where no direct rate was available in the provided price sources. See Assumptions_Log.md for details.

## S7 — Status Reporting

- **RUN_STATUS: WARNINGS**
- Totals exist and are meaningful for budgetary purposes.
- Material TBDs remain:
  - Camera count (assumed 8; actual TBD pending DEL-004-07)
  - Antenna count (assumed 1; actual TBD pending DEL-004-07)
  - Conduit and cable lengths (parametric estimates)
  - Cable type specifications (TBD pending DEL-004-07/DEL-004-09)
  - Scope boundary (CONF-015-05-01, CONF-015-05-02)

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS; gaps are clearly identified and bounded |
| Items.csv reviewed for completeness | PASS | 22 items covering both SOWs, all procedure phases, and professional oversight |
| Basis-consistency checks pass | PASS | All 22 lines use PARAMETRIC method, consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% SourceRef coverage; 7 items reference assumptions |
| Scope coverage explicit | PASS | 1 deliverable, 2 SOWs, all included; excluded items documented |
| No writes outside _Estimates/ | PASS | Verified |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Documents Missing | Items Extracted |
|---|---|---|---|
| DEL-015-05 | Datasheet.md, Specification.md, Guidance.md, Procedure.md | None | 22 |

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items | 22 |
| Items priced | 22 (100%) |
| Items with Amount=TBD | 0 |
| Confidence LOW | 2 items (DL-002 antenna rough-in, DL-015 inspection fees) |
| Confidence MED | 20 items |
| Confidence HIGH | 0 items |

## What to Fix for a Cleaner Rerun

1. **Resolve DEL-004-07 (IFC Low-Voltage System Plans):** Once issued, replace assumed camera count (8), antenna count (1), conduit lengths, and cable lengths with actuals from the drawings.
2. **Resolve CONF-015-05-01 and CONF-015-05-02:** Confirm scope boundary (wiring-only vs. equipment supply) to validate exclusion of camera/radio hardware from this estimate.
3. **Add material rate sources:** Provide supplier quotes or rate tables for conduit ($$/m), cable ($$/m), junction boxes ($$/ea), and weatherhead assemblies to replace parametric material assumptions.
4. **Confirm AHJ inspection fee schedule:** Replace inspection allowance (DL-015) with actual AHJ fee schedule for the jurisdiction.
5. **Add contingency policy:** Determine whether a contingency factor should be applied given the parametric basis and TBD quantities.
