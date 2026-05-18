# Source_Index.md

## Price Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | RATE_TABLE | 30 roles with RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. All rates in CAD. Basis = MARKET for all priced roles. Confidence = MEDIUM for all priced roles. | Unit rates for all professional staff roles |
| 2 | Level_of_Effort.csv | RATE_TABLE (hours) | 73 rows mapping Execution 6b deliverables to RoleID + EstimatedHours. Basis = PARAMETRIC for all rows. Filtered to DEL-05-02: 1 row (R-09, 8 hrs). | Hour quantities per deliverable per role |
| 3 | Assumed_Project_Parameters.csv | PARAMETRIC (reference) | 29 parameters covering duration, area, quantities, and financial estimates. Used for context validation only; not directly used for pricing DEL-05-02. | Project-level context and validation |

## Source Usage for DEL-05-02

| LineID | Rate Source | Hours Source | Rate Value | Hours Value |
|---|---|---|---|---|
| L-001 | Professional_Staff_Rates.csv, row R-09 | Level_of_Effort.csv, row DEL-05-02/R-09 | $155/hr CAD | 8 hr |

## Limitations

- Rate table basis is MARKET with MEDIUM confidence; rates are not based on signed contracts or firm quotes.
- Level of effort basis is PARAMETRIC with no explicit sizing model documented; hours represent professional judgment.
- No independent validation source for hours or rates is available in the provided inputs.
