# Source Index

**RunID:** EST_DEL-07-03_2026-02-18_2000

## Indexed Price Sources

| # | Source Path | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | 30 roles with RoleID, HourlyRate_CAD, Category; all MARKET basis | Hourly rates for all staff roles; used for UnitRate in Detail.csv |
| 2 | `_PriceSources/Level_of_Effort.csv` | Rate Table (hours) | 73 rows; filtered to Execution=6b, DeliverableID=DEL-07-03; 1 matching row found | Estimated hours by role by deliverable; used for Qty in Detail.csv |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Parametric parameters | 29 parameters; categories: Duration, Area, Quantity, Financial | Context parameters for project scope; not directly used for DEL-07-03 pricing but available for validation |

## Source Usage for DEL-07-03

| LineID | Hours Source | Rate Source | Notes |
|---|---|---|---|
| L-001 | Level_of_Effort.csv row DEL-07-03/R-02 (8 hrs) | Professional_Staff_Rates.csv row R-02 ($175/hr) | Fully sourced; no TBDs |

## Source Gaps

None identified. All line items have complete source references.
