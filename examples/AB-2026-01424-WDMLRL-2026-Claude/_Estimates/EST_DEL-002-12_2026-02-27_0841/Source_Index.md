# Source Index — EST_DEL-002-12_2026-02-27_0841

## Price Sources Indexed

| # | Source File | Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-1 | Professional_Staff_Rates.csv | PARAMETRIC (rate table) | 25 rows; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. All rates PARAMETRIC basis, MEDIUM confidence. | Hourly rates for all professional staff roles (R-01 through R-25) |
| PS-2 | Level_of_Effort.csv | PARAMETRIC (effort model) | Multi-deliverable; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. Filtered to DEL-002-12 rows only. | Hour allocations per role per deliverable |
| PS-3 | Assumed_Project_Parameters.csv | PARAMETRIC (context) | 19 rows; columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes. | Project identity, location, facility parameters, currency. Not directly priced but supports context and assumptions. |
| PS-4 | Professional_Design_Fees.csv | PARAMETRIC (fee model) | 5 rows; columns: ItemID, Discipline, Description, FeePercentMin/Max/Recommended, FeeBase, Basis, Confidence, Notes. | Alternative fee-based pricing method. Not used for this run — LOE method preferred for single-deliverable scope. |

## Source Usage Summary

- **PS-1 (Professional_Staff_Rates.csv):** Used for all 4 priced line items. Rates applied: R-01 ($165/hr), R-08 ($135/hr), R-13 ($95/hr), R-14 ($170/hr).
- **PS-2 (Level_of_Effort.csv):** Used for all 4 priced line items. Hours applied: R-01 (6 hr), R-08 (4 hr), R-13 (18 hr), R-14 (42 hr).
- **PS-3 (Assumed_Project_Parameters.csv):** Referenced for project context (PP-17 Currency = CAD). Not directly used for line-item pricing.
- **PS-4 (Professional_Design_Fees.csv):** Not used. Fee-based method (DF-02 Structural design fee = 1.8% of construction value) is an alternative approach but not applied here because: (a) construction value is not established, (b) LOE-based parametric pricing is more granular for a single deliverable.

## Notes

- All pricing follows the PARAMETRIC basis of estimate.
- All rates and hours have MEDIUM confidence per source files.
- No external sources were fetched; all pricing derived from local PRICE_SOURCES.
