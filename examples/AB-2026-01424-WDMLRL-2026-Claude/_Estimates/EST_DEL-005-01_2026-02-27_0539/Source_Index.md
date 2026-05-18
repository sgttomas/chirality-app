# Source Index — EST_DEL-005-01_2026-02-27_0539

## Pricing Sources

| Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|
| `Professional_Staff_Rates.csv` | RATE_TABLE (parametric hourly rates) | 25 roles; RoleID R-01 through R-25; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. All rates are PARAMETRIC basis with MEDIUM confidence. | Provides hourly rates for all staff roles. Used to price ITM-001 through ITM-004. |
| `Level_of_Effort.csv` | PARAMETRIC (estimated hours by deliverable and role) | Multi-deliverable LOE table; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. Filtered to DEL-005-01 rows for this estimate. | Provides estimated hours for each role assigned to DEL-005-01. Directly supplies Qty for ITM-001 through ITM-004. |
| `Assumed_Project_Parameters.csv` | PARAMETRIC (project parameters) | 19 parameters (PP-01 through PP-18 plus header); columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes. | Context parameters (facility size, equipment, location). Not directly used for pricing but provides project context for assumptions. |
| `Professional_Design_Fees.csv` | PARAMETRIC (percentage-of-construction fee model) | 5 discipline fee entries (DF-01 through DF-05); columns: ItemID, Discipline, Description, FeePercentMin, FeePercentMax, RecommendedPercent, FeeBase, Basis, Confidence, Notes. DF-05 is Civil/site design fee at 1.0% recommended. | Alternative pricing method (fee-as-%-of-construction). Not used as primary method for this estimate because LOE-based parametric model provides more granular data. Retained for cross-check reference. |

## Source Coverage Assessment

| Item Range | Primary Source | Coverage |
|---|---|---|
| ITM-001 (PM hours) | Level_of_Effort.csv (DEL-005-01, R-01) + Professional_Staff_Rates.csv (R-01) | FULL — hours and rate both available |
| ITM-002 (Estimator hours) | Level_of_Effort.csv (DEL-005-01, R-08) + Professional_Staff_Rates.csv (R-08) | FULL — hours and rate both available |
| ITM-003 (BIM Tech hours) | Level_of_Effort.csv (DEL-005-01, R-13) + Professional_Staff_Rates.csv (R-13) | FULL — hours and rate both available |
| ITM-004 (Civil Eng hours) | Level_of_Effort.csv (DEL-005-01, R-17) + Professional_Staff_Rates.csv (R-17) | FULL — hours and rate both available |
| ITM-005 through ITM-017 | No separate pricing — design activities captured in labour hours ITM-001 through ITM-004 | N/A — scope coverage items; cost is zero (embedded in labour) |

## Notes

- The primary pricing method for this deliverable is PARAMETRIC: estimated hours (from Level_of_Effort.csv) multiplied by hourly rates (from Professional_Staff_Rates.csv).
- Professional_Design_Fees.csv provides an alternative fee-percentage model (DF-05: Civil design at 1.0% of construction value). This is not used as the primary pricing method because (a) construction value is not established at preliminary design stage, and (b) the LOE model is more granular. The fee model is noted in the Decision_Log for cross-check purposes.
- All rate confidences are MEDIUM per the source file.
