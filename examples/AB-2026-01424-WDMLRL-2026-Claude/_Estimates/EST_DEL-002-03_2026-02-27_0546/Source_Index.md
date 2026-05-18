# Source Index — EST_DEL-002-03_2026-02-27_0546

## Price Sources Indexed

| Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|
| Professional_Staff_Rates.csv | PARAMETRIC (rate table) | 25 rows; CSV with RoleID, Role, HourlyRate_CAD, Basis, Confidence columns. All rates PARAMETRIC/MEDIUM confidence. | Hourly rates for all professional staff roles (R-01 through R-25). Provides unit rates for effort-based costing. |
| Level_of_Effort.csv | PARAMETRIC (effort model) | 577 rows; CSV with Execution, DeliverableID, RoleID, EstimatedHours columns. Filtered to DEL-002-03: 4 rows (R-01: 6 hr, R-08: 4 hr, R-13: 36 hr, R-14: 84 hr). | Hours by role for DEL-002-03 Structural Framing Plans. Direct effort input for parametric costing. |
| Assumed_Project_Parameters.csv | PARAMETRIC (parameters) | 18 rows; CSV with project identity, location, facility, equipment, and economic parameters. | Project context: 13,000 sqft addition, 35 ft ceiling, 2 x 5-tonne cranes, CAD currency, 2026 base year. Used for scope validation, not direct pricing. |
| Professional_Design_Fees.csv | PARAMETRIC (fee model) | 5 rows; CSV with discipline, fee percentage ranges, and recommended percentages. DF-02 (Structural): 1.2%-2.5%, recommended 1.8% of construction value. | Alternative fee-based pricing method. Not used as primary method for this run (LOE-based approach preferred for single-deliverable scope). Available as cross-check. |

## Sources Not Used

| Source | Reason |
|---|---|
| Professional_Design_Fees.csv (DF-02) | Fee-based method not applied as primary for this deliverable; LOE-based parametric is more granular for a single drawing set deliverable. Fee-based method is a package-level cross-check and does not decompose to individual deliverables. |

## Coverage Assessment

| Coverage Aspect | Status |
|---|---|
| All 4 LOE rows for DEL-002-03 matched to staff rates | COMPLETE |
| Hourly rates available for all 4 roles | COMPLETE |
| Parametric basis for all items | COMPLETE |
| Fee-based cross-check available | AVAILABLE (not applied) |
