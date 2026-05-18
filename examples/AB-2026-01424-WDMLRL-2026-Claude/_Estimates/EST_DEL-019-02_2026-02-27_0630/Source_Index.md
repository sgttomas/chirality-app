# Source Index — EST_DEL-019-02_2026-02-27_0630

## Pricing Sources Indexed

### 1. Professional_Staff_Rates.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`
- **Source Type:** PARAMETRIC (rate table with parametric basis)
- **Parsing Notes:** 25 roles defined with RoleID, Role name, Category, HourlyRate_CAD, Basis, Confidence, Notes. All rates marked PARAMETRIC with MEDIUM confidence.
- **Supports:** Unit rates for all staff roles referenced in Level_of_Effort.csv. Roles used for DEL-019-02: R-01 (PM, $165/hr), R-02 (CPM, $155/hr), R-03 (Site Supt, $145/hr), R-05 (HSE Mgr, $140/hr), R-06 (QA/QC Lead, $135/hr), R-08 (Cost Est, $135/hr).
- **Cannot Support:** Non-labour costs, material costs, equipment, third-party fees.

### 2. Level_of_Effort.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`
- **Source Type:** PARAMETRIC (estimated hours by deliverable and role)
- **Parsing Notes:** Multi-row CSV, one row per deliverable-role combination. Columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. All marked PARAMETRIC.
- **Supports:** Hour estimates for DEL-019-02 across 6 roles (R-01, R-02, R-03, R-05, R-06, R-08). Total: 38 hours.
- **Cannot Support:** Non-labour items, per-occurrence breakdown, frequency scaling for recurring deliverables. Notes column shows "PKG-019 TBD -- TBD" indicating placeholder-level detail.

### 3. Assumed_Project_Parameters.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`
- **Source Type:** PARAMETRIC (project-level parameters)
- **Parsing Notes:** 19 parameters covering identity, location, contract, schedule, facility, equipment, plumbing, mechanical, and currency. Mixed confidence (HIGH to MEDIUM).
- **Supports:** Project duration context (completion deadline 2026-12-31), currency (CAD), contract form (CCDC 14-2013). Used for contextual validation only — no direct pricing from this source for DEL-019-02.
- **Cannot Support:** Direct pricing or quantity derivation for DEL-019-02 line items.

### 4. Fees_Permits_Insurance.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Fees_Permits_Insurance.csv`
- **Source Type:** PARAMETRIC / ALLOWANCE (fee and insurance allowances)
- **Parsing Notes:** 5 items covering bonding, insurance, and permits. All project-level allowances.
- **Supports:** Not applicable to DEL-019-02. These are project-level commercial costs assigned to PKG-021.
- **Cannot Support:** Any DEL-019-02 line items.

## Source Coverage Summary

| Item Category | Source Available | Coverage |
|---|---|---|
| Staff hourly rates | Professional_Staff_Rates.csv | Full — all 6 roles matched |
| Level of effort (hours) | Level_of_Effort.csv | Full — all 6 roles have hour estimates |
| Project parameters (context) | Assumed_Project_Parameters.csv | Partial — duration context only |
| Fees/permits/insurance | Fees_Permits_Insurance.csv | Not applicable to this deliverable |
| Non-labour costs (meetings, travel, printing) | None | No source available |
| Phase A setup effort (separate from recurring) | None | Not separately broken out in LOE |
| Phase D closeout effort (separate from recurring) | None | Not separately broken out in LOE |
