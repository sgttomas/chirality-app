# Estimate Summary — DEL-013-03: Forced-Air Makeup System

**RunID:** EST_DEL-013-03_2026-02-27_0901
**Date:** 2026-02-27
**Basis of Estimate:** PARAMETRIC
**Currency:** CAD
**RUN_STATUS:** WARNINGS

---

## Basis of Estimate Used

| Field | Value |
|---|---|
| Primary Method | PARAMETRIC |
| Fallback Policy | ALLOW_PARAMETRIC |
| Mixed Methods Allowed | TRUE |
| Methods Actually Used | PARAMETRIC (100% of lines) |
| Rate-Table-Sourced Lines | 8 of 31 lines (26%) have direct price source evidence (MS-02, MS-06, LOE + Staff Rates) |
| ASSUMPTION-Based Lines | 23 of 31 lines (74%) priced via parametric ASSUMPTION |

---

## Total by Deliverable

| WBS_DeliverableID | Description | Amount (CAD) | Line Count |
|---|---|---|---|
| DEL-013-03 | Forced-Air Makeup System | **186,590.00** | 31 |

---

## Total by CBS Category

| CBS | Amount (CAD) | % of Total | Lines |
|---|---|---|---|
| MECHANICAL-DUCTWORK | 92,250.00 | 49.4% | 4 |
| MECHANICAL-EQUIP | 46,550.00 | 24.9% | 3 |
| MECHANICAL-COMMISSIONING | 14,000.00 | 7.5% | 5 |
| MECHANICAL-CONTROLS | 10,000.00 | 5.4% | 2 |
| MECHANICAL-ADMIN | 6,200.00 | 3.3% | 4 |
| MANAGEMENT (all) | 5,590.00 | 3.0% | 6 |
| MECHANICAL-LOGISTICS | 3,500.00 | 1.9% | 1 |
| MECHANICAL-FIRE-PROTECTION | 2,600.00 | 1.4% | 1 |
| MECHANICAL-PIPING | 2,500.00 | 1.3% | 1 |
| MECHANICAL-PERMIT | 2,200.00 | 1.2% | 2 |
| MECHANICAL-ELECTRICAL | 1,200.00 | 0.6% | 1 |
| **TOTAL** | **186,590.00** | **100%** | **31** |

---

## Key Warnings and Coverage Gaps

1. **W-01 (BLOCKING):** MUA supply airflow rate is TBD -- the essential design fact that drives equipment selection, duct sizing, and heating capacity has not been established. This makes the MUA unit cost (MS-02, $45,000) a parametric placeholder subject to significant revision.

2. **W-02:** Design outdoor air temperature TBD -- heating capacity cannot be independently verified; affects whether MUA heating coil/burner is adequate.

3. **W-03:** MUA make/model TBD -- equipment cost is a parametric range midpoint ($45,000 from $28,000-$65,000 range). Actual cost could vary +44% / -38% from estimate.

4. **W-04:** Ductwork quantities are parametric (normalized per floor area at $60/m2). Actual ductwork scope depends on routing, number of distribution points, and zone layout (all TBD per mechanical design).

5. **W-05:** Fire/smoke damper quantity (4 EA) is ASSUMPTION -- actual count depends on fire separation drawings (not available).

6. **W-06:** No trade labour LOE available from Level_of_Effort.csv for HVAC Sheet Metal (T-06) or other field trades. Field labour is embedded in unit rates (MS-02, MS-06) rather than separately quantified.

7. **W-07:** 74% of line items (23 of 31) are priced via parametric ASSUMPTION without direct price source evidence. Only MUA unit, ductwork, and management LOE have traceable price sources.

---

## Scope Coverage

| Scope Element | Status |
|---|---|
| MUA unit procurement/install | Priced (parametric) |
| Fresh air intake ductwork | Priced (parametric) |
| Supply ductwork distribution | Priced (parametric per m2) |
| Dampers and controls | Priced (parametric) |
| Fire/smoke dampers | Priced (parametric; qty ASSUMPTION) |
| Filtration | Priced (parametric) |
| Insulation | Priced (parametric % of ductwork) |
| Electrical disconnect/LOTO | Priced (parametric) |
| Condensate management | Priced (parametric) |
| Controls/BAS integration | Priced (parametric) |
| Permits and inspections | Priced (parametric) |
| TAB, duct leakage, commissioning | Priced (parametric) |
| Integrated system test | Priced (parametric) |
| Documentation (as-built, O&M) | Priced (parametric) |
| Owner training | Priced (parametric) |
| Management overhead (LOE) | Priced (from LOE + Staff Rates) |
| Delivery/rigging | Priced (parametric) |
| Gas connection | Priced (parametric) |
| Warranty/deficiency correction | NOT PRICED -- TBD per CCDC 14 contract terms |
| Post-commissioning monitoring | NOT PRICED -- optional consideration per Guidance C8 |
