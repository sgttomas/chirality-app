# Source Index — EST_DEL-003-06_2026-02-27_0134

## Price Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | PriceSources/Professional_Staff_Rates.csv | PARAMETRIC (rate table) | 25 roles with hourly rates in CAD; Basis=PARAMETRIC; Confidence=MEDIUM | Hourly rates for all staff roles (R-01 through R-25) |
| PS-02 | PriceSources/Level_of_Effort.csv | PARAMETRIC (effort model) | Deliverable-level hour allocations by role; 4 rows for DEL-003-06 totalling 90 hours | Hour quantities for DEL-003-06: R-01 (6h), R-08 (4h), R-13 (24h), R-15 (56h) |
| PS-03 | PriceSources/Assumed_Project_Parameters.csv | PARAMETRIC (context) | 19 project parameters; PP-17 confirms CAD currency; PP-10 confirms ~13,000 sqft floor area | Building parameters and project context; not direct pricing but informs parametric sizing |
| PS-04 | PriceSources/Professional_Design_Fees.csv | PARAMETRIC (fee model) | 5 discipline fee percentages as % of construction value; DF-03 Mechanical at 1.6% recommended | Alternative fee-based pricing for mechanical design; not used as primary method for this deliverable (LOE method preferred for calculation package) |

## Source Coverage Assessment

- **Roles priced:** R-01 (Project Manager), R-08 (Cost Estimator), R-13 (BIM Technician), R-15 (Mechanical Engineer) — all have rates in PS-01
- **Hours sourced:** All 4 role-hour allocations for DEL-003-06 found in PS-02
- **Coverage:** 100% of line items have both rate and quantity from provided sources
- **Gaps:** None — all items priced from PARAMETRIC sources
