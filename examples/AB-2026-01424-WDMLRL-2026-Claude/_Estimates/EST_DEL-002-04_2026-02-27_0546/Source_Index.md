# Source Index — EST_DEL-002-04_2026-02-27_0546

## Price Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | Rate Table (PARAMETRIC) | 25 roles with hourly rates in CAD; all marked PARAMETRIC basis, MEDIUM confidence | Unit rates for all labour line items; R-01 (PM $165/hr), R-08 (Cost Est $135/hr), R-13 (BIM Tech $95/hr), R-14 (Struct Eng $170/hr) |
| 2 | Level_of_Effort.csv | Parametric Model (hours by deliverable x role) | ~400+ rows; DEL-002-04 has 4 rows (R-01: 6 hr, R-08: 4 hr, R-13: 36 hr, R-14: 84 hr); all PARAMETRIC basis | Quantity (hours) for each role on DEL-002-04 |
| 3 | Assumed_Project_Parameters.csv | Project Parameters | 18 parameters; key entries: CAD currency (PP-17), 13,000 sqft floor area (PP-10), 35 ft ceiling (PP-11), 2 x 5-tonne cranes (PP-12/PP-13) | Context validation; currency confirmation; no direct pricing |
| 4 | Professional_Design_Fees.csv | Fee Table (PARAMETRIC) | 5 discipline fee percentages against construction value; Structural = 1.2%–2.5% (recommended 1.8%) | Alternative fee-based pricing method (not used as primary; LOE-based approach preferred for this deliverable) |

## Source Coverage Assessment

- **Primary pricing method:** PARAMETRIC (labour hours x hourly rates)
- **Quantity source:** Level_of_Effort.csv provides role-level hours for DEL-002-04
- **Rate source:** Professional_Staff_Rates.csv provides hourly rates per role
- **Coverage:** 100% of labour line items (L-001 through L-004) have both quantity and rate from price sources
- **Gap:** No material/printing/reproduction costs are captured in the price sources; this estimate covers professional services (design labour) only
