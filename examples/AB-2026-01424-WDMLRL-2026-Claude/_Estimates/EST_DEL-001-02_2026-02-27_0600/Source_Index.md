# Source Index — EST_DEL-001-02_2026-02-27_0600

## Indexed Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | Rate Table (hourly rates by role) | 25 roles; all rates in CAD/hr; Basis=PARAMETRIC; Confidence=MEDIUM | Provides unit rates for all professional staff line items |
| 2 | Level_of_Effort.csv | Parametric Model (hours by deliverable and role) | Multi-deliverable; filtered for DEL-001-02 rows; 5 roles assigned to this deliverable | Provides quantity (hours) for each role on DEL-001-02 |
| 3 | Assumed_Project_Parameters.csv | Reference Parameters | 19 parameters covering identity, location, facility, equipment, schedule | Background context; confirms building area (~13,000 sqft), currency (CAD), and facility attributes |
| 4 | Professional_Design_Fees.csv | Parametric Model (fee percentages) | 5 discipline fee ranges based on construction value | Not directly used for this deliverable (LOE-based pricing preferred over fee-percentage method for individual deliverable estimates); available as cross-check |
| 5 | Parametric_Building_Rates.csv | Parametric Model (building cost rates) | 2 items: base industrial rate ($285/sf recommended) and wash bay premium ($70/sf) | Not directly used for DEL-001-02 (construction cost model, not design fee); available as cross-check for overall project value |

## Source Usage Summary

- **Primary pricing method:** PARAMETRIC — hours from Level_of_Effort.csv multiplied by hourly rates from Professional_Staff_Rates.csv.
- **Sources used for pricing:** Professional_Staff_Rates.csv (unit rates), Level_of_Effort.csv (quantities/hours).
- **Sources used for context only:** Assumed_Project_Parameters.csv, Professional_Design_Fees.csv, Parametric_Building_Rates.csv.
- **Sources not usable for this scope:** None — all sources are parseable and relevant at either pricing or context level.
