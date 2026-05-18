# Source Index — EST_DEL-005-05_2026-02-27_0630

## Price Sources Indexed

### Source 1: Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv |
| **Type** | PARAMETRIC (rate table) |
| **Contents** | 25 role entries with hourly rates in CAD. Each entry includes RoleID, Role name, Category, HourlyRate_CAD, Basis (all PARAMETRIC), and Confidence (all MEDIUM). |
| **Relevant Roles for DEL-005-05** | R-01 Project Manager ($165/hr), R-08 Cost Estimator ($135/hr), R-13 BIM Technician ($95/hr), R-17 Civil Engineer ($160/hr) |
| **Parsing Notes** | Standard CSV; no parsing issues. |
| **Can Support** | Unit rate pricing for all professional staff line items in this deliverable. |
| **Cannot Support** | Non-staff items (materials, subconsultant fees, disbursements). |

### Source 2: Level_of_Effort.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv |
| **Type** | PARAMETRIC (effort model) |
| **Contents** | Estimated hours by deliverable and role for the entire project. Each row specifies Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, and Notes. |
| **Relevant Rows for DEL-005-05** | R-01 Project Manager: 6 hr; R-08 Cost Estimator: 4 hr; R-13 BIM Technician: 36 hr; R-17 Civil Engineer: 84 hr. Total: 130 hr. |
| **Parsing Notes** | Standard CSV; large file covering all deliverables. Filtered to DEL-005-05 rows only. |
| **Can Support** | Hour quantities for all staff roles assigned to this deliverable. |
| **Cannot Support** | Non-staff items; does not contain rates (rates sourced from Professional_Staff_Rates.csv). |

### Source 3: Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv |
| **Type** | PARAMETRIC (parameter inputs) |
| **Contents** | 19 project parameters: identity, location, contract, schedule, facility, equipment, plumbing, mechanical, currency, and economics parameters. |
| **Relevant Parameters for DEL-005-05** | PP-10 Addition Floor Area approx 13,000 sqft; PP-17 Currency CAD; PP-18 Base Year 2026. |
| **Parsing Notes** | Standard CSV; no parsing issues. |
| **Can Support** | Contextual parameters for parametric models; currency confirmation. |
| **Cannot Support** | Direct pricing; does not contain rates or costs. |

### Source 4: Professional_Design_Fees.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv |
| **Type** | PARAMETRIC (fee percentage model) |
| **Contents** | 5 discipline entries with fee percentage ranges (min, max, recommended) as percentage of construction value. |
| **Relevant Entry for DEL-005-05** | DF-05 Civil/site design fee: 0.6%–1.5% of construction value, recommended 1.0%. |
| **Parsing Notes** | Standard CSV; no parsing issues. Fee-based approach requires a construction_value input which is not available in this scope (single deliverable estimate). |
| **Can Support** | Cross-check / validation of staff-hours-based estimate if construction value were known. |
| **Cannot Support** | Direct pricing for this run — construction_value is not provided as an input. Used for cross-reference only. |

## Summary

| Metric | Value |
|---|---|
| Sources indexed | 4 |
| Sources directly used for pricing | 2 (Professional_Staff_Rates.csv, Level_of_Effort.csv) |
| Sources used for context/validation | 2 (Assumed_Project_Parameters.csv, Professional_Design_Fees.csv) |
| Pricing method supported | PARAMETRIC (staff hours x hourly rates) |
