# Source Index — EST_DEL-019-03_2026-02-27_0630

## Indexed Price Sources

### 1. Professional_Staff_Rates.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`
- **Source Type:** PARAMETRIC (rate table)
- **Content:** 25 roles (R-01 through R-25) with hourly rates in CAD. All rates have PARAMETRIC basis with MEDIUM confidence.
- **Parsing Notes:** Standard CSV; clean parse. RoleID is the join key to Level_of_Effort.csv.
- **Supports:** Unit rate pricing for all professional staff labour line items. Directly applicable roles for DEL-019-03:
  - R-01 Project Manager: $165/hr
  - R-02 Construction Project Manager: $155/hr
  - R-03 Site Superintendent: $145/hr
  - R-05 HSE Manager: $140/hr
  - R-06 QA/QC Lead: $135/hr
  - R-08 Cost Estimator: $135/hr
- **Cannot Support:** Material costs, subcontractor contract values, third-party fees.

### 2. Level_of_Effort.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`
- **Source Type:** PARAMETRIC (effort model)
- **Content:** Estimated hours per role per deliverable. For DEL-019-03 (Subcontractor Management), 6 role assignments are present:
  - R-01 Project Manager: 6 hr
  - R-02 Construction Project Manager: 8 hr
  - R-03 Site Superintendent: 10 hr
  - R-05 HSE Manager: 4 hr
  - R-06 QA/QC Lead: 6 hr
  - R-08 Cost Estimator: 4 hr
- **Parsing Notes:** Standard CSV; clean parse. Filtered by DeliverableID = DEL-019-03.
- **Supports:** Hour quantities for all staff line items in DEL-019-03.
- **Cannot Support:** Non-labour costs, material quantities.

### 3. Assumed_Project_Parameters.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`
- **Source Type:** PARAMETRIC (project context parameters)
- **Content:** 19 parameters (PP-01 through PP-19) covering project identity, location, contract form, schedule, facility attributes, and currency.
- **Parsing Notes:** Standard CSV; clean parse.
- **Supports:** Project context validation; currency confirmation (PP-17: CAD); completion deadline confirmation (PP-07: 2026-12-31).
- **Cannot Support:** Direct pricing of line items. Provides context only.

### 4. Fees_Permits_Insurance.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Fees_Permits_Insurance.csv`
- **Source Type:** PARAMETRIC / ALLOWANCE (fee estimates)
- **Content:** 5 items (FP-01 through FP-05) covering bonding, insurance, and permits. All project-level items.
- **Parsing Notes:** Standard CSV; clean parse. Contains RecommendedRate with RateMin/RateMax ranges.
- **Supports:** Not directly applicable to DEL-019-03 labour estimate. These are project-level fee items (bonding, insurance, permits) that belong to PKG-021 or project overhead, not to the subcontractor management deliverable.
- **Cannot Support:** DEL-019-03 line items. Noted for completeness only.

## Source Coverage Assessment

| Coverage Area | Status | Notes |
|---|---|---|
| Staff hourly rates | COVERED | Professional_Staff_Rates.csv provides all 6 required roles |
| Staff hour quantities | COVERED | Level_of_Effort.csv provides parametric hours for all 6 roles assigned to DEL-019-03 |
| Non-labour costs | NOT COVERED | No price source provides material, software, or third-party costs for subcontractor management activities |
| Project context | COVERED | Assumed_Project_Parameters.csv confirms currency, deadline, and project identity |
