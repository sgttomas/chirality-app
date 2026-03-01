# Source Index — EST_DEL-001-03_2026-02-27_0545

## Indexed Price Sources

| # | File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | `PriceSources/Professional_Staff_Rates.csv` | Rate Table | 25 roles with hourly rates in CAD; basis PARAMETRIC; confidence MEDIUM | Hourly rates for all design and management roles (R-01 through R-25) |
| PS-02 | `PriceSources/Level_of_Effort.csv` | Parametric Model | Hour allocations by deliverable and role; includes DEL-001-03 rows for 5 roles | Hours for ITM-001 through ITM-005 (Senior Architect 54h, Architect 42h, BIM Tech 24h, PM 6h, Cost Estimator 4h) |
| PS-03 | `PriceSources/Assumed_Project_Parameters.csv` | Parametric Model | 19 project parameters including facility dimensions, equipment, currency | Context parameters; confirms CAD currency (PP-17), building area ~13,000 sqft (PP-10), 35' ceiling (PP-11) |
| PS-04 | `PriceSources/Professional_Design_Fees.csv` | Parametric Model | 5 discipline fee percentages as percent of construction value | Not directly used for this deliverable — fee-based pricing is an alternative to LOE-based pricing; LOE approach used here per Level_of_Effort.csv |
| PS-05 | `PriceSources/Parametric_Building_Rates.csv` | Parametric Model | 2 building-level parametric rates (per sqft) | Not directly used for this deliverable — applies to construction cost cross-check, not design effort pricing |

## Source Coverage Assessment

- **DEL-001-03 has direct LOE data** in Level_of_Effort.csv (PS-02), rows 12-16, specifying hours for 5 roles.
- **Hourly rates** are available in Professional_Staff_Rates.csv (PS-01) for all 5 roles referenced.
- **Coverage: 100%** — All 5 line items can be priced from PS-01 + PS-02 using PARAMETRIC method.
- **No gaps requiring fallback.**
