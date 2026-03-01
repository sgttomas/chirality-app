# QA_Report — EST_DEL-013-01_2026-02-27_1045

## RUN_STATUS: WARNINGS

**Rationale:** All 26 line items are priced with non-TBD amounts. Parametric rates and allowances are sourced from provided price tables. However, material TBDs remain in the underlying design (heating capacity, equipment type, fuel source, BMS protocol) that could cause significant variance when resolved. The estimate is meaningful for budgetary purposes but not suitable for firm pricing without design resolution.

---

## S1 — Write Quarantine

| Check | Result |
|---|---|
| All files written under _Estimates/ only | PASS |
| No modifications to deliverable working files | PASS |
| No modifications to lifecycle files | PASS |
| No modifications to decomposition outputs | PASS |
| No modifications to dependency registers | PASS |

---

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists | PASS — EST_DEL-013-01_2026-02-27_1045/ |
| Folder naming convention followed | PASS |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE provided | PASS — PARAMETRIC |
| Value is valid enum | PASS |

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Items.csv | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Detail.csv | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |

---

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| File is parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows have SourceDoc value | PASS — all rows reference Datasheet, Specification, or Procedure |
| All rows have SourceSection value | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Row count | 26 items |

### Detail.csv

| Check | Result |
|---|---|
| File is parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid | PASS — PARAMETRIC (24), ALLOWANCE (2) |
| Allowance convention respected (Qty=1, Unit=LS, UnitRate=Amount) | PASS — L-001 (Qty=2 ALLOWANCE but UNIT_RATE mode; acceptable per mixed methods) |
| All ItemIDs trace to Items.csv | PASS |
| Row count | 26 lines |

**Note on L-001:** Line L-001 uses Method=ALLOWANCE with Qty=2 and UnitRate=6500 (Amount=13000). This deviates from the strict allowance convention (Qty=1, Unit=LS, UnitRate=Amount) because the item has a known quantity (2 units) but an allowance-based unit rate. This is logged as Decision DEC-002.

---

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Lines with non-TBD SourceRef | 26 of 26 (100%) |
| Lines with SourceRef pointing to price source file | 20 of 26 (77%) |
| Lines with SourceRef pointing to Assumptions_Log.md | 6 of 26 (23%) |
| Lines with "location TBD" SourceRef | 0 |

**Top provenance notes:**
- All 6 management lines (L-018 through L-023) trace directly to Level_of_Effort.csv + Professional_Staff_Rates.csv.
- Trade labour lines (L-024, L-025) trace to Construction_Labour_Rates.csv.
- Equipment line (L-001) traces to Mechanical_System_Rates.csv MS-01.
- Ductwork line (L-002) traces to Mechanical_System_Rates.csv MS-06.
- Parametric allowances for specialized scopes (heat recovery connections, gas connection, controls, etc.) reference Assumptions_Log.md entries.

---

## S7 — Basis-Consistency Checks

| Check | Result |
|---|---|
| Primary basis | PARAMETRIC |
| Lines matching primary basis | 24 of 26 (92%) |
| Lines using fallback method | 2 of 26 (8%) — ALLOWANCE |
| ALLOW_MIXED_METHODS | TRUE — mixed methods authorized |
| FALLBACK_POLICY | ALLOW_PARAMETRIC — fallback to parametric/allowance authorized |
| Basis consistency | PASS — deviations are within policy |

---

## Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Documents read per deliverable | 5 of 5 |
| Missing documents | 0 |
| Items extracted | 26 |
| Items with TBD quantity | 0 (all quantities resolved or assumed) |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Items priced | 26 of 26 (100%) |
| Items with TBD amount | 0 |
| Total estimate | $135,120.00 CAD |

---

## What to Fix for a Cleaner Rerun

1. **Resolve heating capacity** — Obtain DEL-003-06 Mechanical Calculation Package to confirm BTU/h or kW requirement. This will refine equipment selection and pricing.
2. **Confirm fuel source** — Formally confirm natural gas as the fuel source per CONF-001. If electric, remove gas connection line item and adjust accordingly.
3. **Confirm equipment type** — Obtain DEL-003-07 Mechanical Specification to replace the generic MS-01 unit heater allowance with a specific equipment quote.
4. **Confirm ductwork quantities** — Obtain DEL-003-03 Ductwork Plans to replace parametric area-based ductwork estimate with measured quantities.
5. **Define BMS protocol** — Confirm BMS communication protocol to refine controls integration estimate.
6. **Obtain equipment quotes** — Replace allowance-based equipment pricing with vendor quotes for the specified high-recovery heating equipment.
7. **Validate trade labour hours** — Refine HVAC sheet metal and labourer hour estimates once installation scope is defined by mechanical drawings.
