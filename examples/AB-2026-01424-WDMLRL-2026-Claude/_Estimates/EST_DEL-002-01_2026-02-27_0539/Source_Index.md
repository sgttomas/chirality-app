# Source Index

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | Rate Table (PARAMETRIC) | 25 roles with CAD hourly rates; RoleID R-01 through R-25; Confidence: MEDIUM for all rates | Hourly rate lookup for labour line items |
| PS-02 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | Parametric Model (PARAMETRIC) | Estimated hours by deliverable and role; DEL-002-01 has 4 role entries (R-01, R-08, R-13, R-14) totaling 70 hours | Hour estimates for DEL-002-01 labour |
| PS-03 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` | Parametric Context | 19 project parameters (PP-01 through PP-18); includes facility dimensions, equipment counts, and project context | Context and validation for quantity takeoff |
| PS-04 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` | Parametric Model (PARAMETRIC) | 5 discipline-level fee percentages (DF-01 through DF-05); DF-02 is Structural at 1.8% recommended of construction value | Alternative fee-based pricing for structural design; not used as primary method since LOE is available |

## Source Applicability to DEL-002-01

DEL-002-01 is a professional services (design presentation) deliverable. The primary pricing approach is **labour hours x hourly rate** using PS-01 (rates) and PS-02 (hours). PS-03 provides context validation. PS-04 provides an alternative cross-check method (fee-based) but is not used as the primary pricing basis because the Level_of_Effort model provides role-specific hour estimates for this deliverable.

### DEL-002-01 Level of Effort (from PS-02)

| RoleID | Role | EstimatedHours | HourlyRate_CAD (from PS-01) |
|---|---|---|---|
| R-01 | Project Manager | 6 | 165 |
| R-08 | Cost Estimator | 4 | 135 |
| R-13 | BIM Technician | 18 | 95 |
| R-14 | Structural Engineer | 42 | 170 |

**Total Hours:** 70
