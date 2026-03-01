# Source Index — EST_DEL-005-04_2026-02-27_0546

## Price Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | Rate Table (Parametric) | 25 roles with hourly rates in CAD; all PARAMETRIC basis, MEDIUM confidence | Provides hourly rates for all roles referenced in Level_of_Effort.csv |
| 2 | Level_of_Effort.csv | Parametric Model (Hours) | 4 rows matched for DEL-005-04: R-01 (6 hr), R-08 (4 hr), R-13 (36 hr), R-17 (84 hr) | Provides estimated hours per role per deliverable; primary quantity source for design deliverables |
| 3 | Assumed_Project_Parameters.csv | Project Parameters | 18 parameters covering identity, location, contract, schedule, facility, equipment, plumbing, currency | Context parameters; confirms CAD currency (PP-17), project identity, facility size |
| 4 | Professional_Design_Fees.csv | Parametric Model (Fee %) | DF-05: Civil/site design fee 0.6%-1.5% of construction value (recommended 1.0%) | Alternative pricing method (fee-based); not used as primary method — LOE-based pricing preferred for individual deliverables |

## Additional Rate Sources Consulted (Not in PRICE_SOURCES but available)

| Source File | Relevance to DEL-005-04 |
|---|---|
| Earthwork_Civil_Rates.csv | Relevant to construction scope (PKG-018), not to design deliverable DEL-005-04 |
| Paving_Surfacing_Rates.csv | Relevant to construction scope (PKG-018), not to design deliverable DEL-005-04 |
| Structural_Concrete_Rates.csv | Relevant to cement pad construction (PKG-018), not to design deliverable DEL-005-04 |

## Coverage Assessment

- **All 4 line items** in Detail.csv are fully priced using the PARAMETRIC method from the specified PRICE_SOURCES.
- **No TBD amounts** remain.
- **Professional_Design_Fees.csv** provides an alternative fee-based pricing method (DF-05: 1.0% of construction value for civil design). This was not used because: (a) construction value is not confirmed; (b) the fee covers all of PKG-005, not a single deliverable; (c) LOE-based pricing from Level_of_Effort.csv provides deliverable-level granularity.
