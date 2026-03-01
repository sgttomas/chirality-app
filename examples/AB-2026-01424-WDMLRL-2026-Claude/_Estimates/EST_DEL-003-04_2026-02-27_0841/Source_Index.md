# Source Index — EST_DEL-003-04_2026-02-27_0841

## Pricing Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-1 | Professional_Staff_Rates.csv | PARAMETRIC (rate table) | 25 rows; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. All rates PARAMETRIC basis, MEDIUM confidence. | Hourly rates for all professional roles. Used for R-01 ($165), R-08 ($135), R-13 ($95), R-15 ($165). |
| PS-2 | Level_of_Effort.csv | PARAMETRIC (effort model) | Multi-deliverable file; filtered to DEL-003-04 rows. Columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. | Hour estimates per role per deliverable. DEL-003-04 has 4 rows: R-01 (6 hr), R-08 (4 hr), R-13 (36 hr), R-15 (84 hr). |
| PS-3 | Assumed_Project_Parameters.csv | PARAMETRIC (parameters) | 20 rows of project context parameters. Used for project identity, facility size, currency, and completion date. | Context parameters only; no direct pricing. Confirms CAD currency (PP-17), facility ~13,000 sqft (PP-10), 35 ft ceiling (PP-11). |
| PS-4 | Professional_Design_Fees.csv | PARAMETRIC (fee model) | 5 rows; percentage-of-construction-value fee model by discipline. Mechanical recommended = 1.6%. | Not used for this estimate (LOE-based approach preferred over percentage-of-construction-value). Available as cross-check. |

## Source Limitations

- **PS-4 (Professional_Design_Fees.csv):** Not applied. The LOE-based approach (PS-1 + PS-2) provides a bottom-up parametric estimate. The fee-percentage model requires a construction value denominator that is not available at this stage. Could be used as a reasonableness cross-check once construction value is established.
- **All rates at MEDIUM confidence:** The professional staff rates are parametric estimates, not contracted rates. Actual costs will depend on contracted team composition and rates.
- **LOE hours are estimates, not actuals:** The 84 mechanical engineering hours and supporting hours are parametric estimates from the LOE model, not derived from historical project actuals for exhaust system drawing sets.
