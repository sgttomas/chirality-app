# Source Index

## Pricing Sources Used

| # | Source File | Source Type | Parsing Notes | Coverage |
|---|---|---|---|---|
| PS-01 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | Rate Table | CSV; 25 roles with hourly rates in CAD; all PARAMETRIC basis, MEDIUM confidence | Provides hourly rates for all roles assigned to DEL-002-10 (R-01, R-08, R-13, R-14) |
| PS-02 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | Parametric (hours model) | CSV; estimated hours by deliverable and role; all PARAMETRIC basis | Provides hour allocations for DEL-002-10: R-01=6h, R-08=4h, R-13=24h, R-14=56h |
| PS-03 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` | Parametric (project context) | CSV; 19 parameters covering identity, location, contract, schedule, facility, equipment, economics | Provides project context (building dimensions, crane count, cistern, currency); no direct pricing data used from this source |
| PS-04 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` | Parametric (percentage fee model) | CSV; 5 disciplines with min/max/recommended fee percentages of construction value | Not used for this run — LOE-based parametric model (PS-01 + PS-02) provides direct pricing; fee percentage model is an alternative approach not applied |

## Source Coverage Assessment

- **Fully covered items:** ITEM-001 through ITEM-004 (all labor line items with hours and rates from PS-01 and PS-02).
- **Scope traceability items (ITEM-005 through ITEM-016):** These are scope decomposition items that trace to the engineering content of the Calculation Package. Their cost is captured within the labor line items (ITEM-001 through ITEM-004). They carry $0 amounts in Detail.csv to avoid double-counting.
- **No material/equipment/subcontract costs:** DEL-002-10 is a professional engineering calculation package — all costs are professional labor. No material, equipment, or subcontract pricing sources are needed.

## Key Rates Used

| RoleID | Role | Hourly Rate (CAD) | Source |
|---|---|---|---|
| R-01 | Project Manager | 165 | PS-01 row R-01 |
| R-08 | Cost Estimator | 135 | PS-01 row R-08 |
| R-13 | BIM Technician | 95 | PS-01 row R-13 |
| R-14 | Structural Engineer | 170 | PS-01 row R-14 |

## Key Hours Used

| RoleID | Role | Hours | Source |
|---|---|---|---|
| R-01 | Project Manager | 6 | PS-02 row DEL-002-10/R-01 |
| R-08 | Cost Estimator | 4 | PS-02 row DEL-002-10/R-08 |
| R-13 | BIM Technician | 24 | PS-02 row DEL-002-10/R-13 |
| R-14 | Structural Engineer | 56 | PS-02 row DEL-002-10/R-14 |
