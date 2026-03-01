# Source Index — EST_DEL-021-05_2026-02-27_0834

## Indexed Price Sources

### 1. Professional_Staff_Rates.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`
- **Source Type:** Rate table (PARAMETRIC)
- **Content:** 25 professional roles with hourly rates in CAD, confidence levels, and category tags
- **Supports:** Hourly rate lookup for all labour line items (roles R-01 through R-25)
- **Parsing Notes:** Standard CSV; header row present; rates are in CAD

### 2. Level_of_Effort.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`
- **Source Type:** Parametric model (PARAMETRIC)
- **Content:** Estimated hours per role per deliverable across the full project scope
- **Supports:** Hour estimates for DEL-021-05 (8 role-rows found: R-01, R-02, R-03, R-25, R-08, R-06, R-05, R-09)
- **Parsing Notes:** Standard CSV; filtered to rows where DeliverableID = DEL-021-05

### 3. Assumed_Project_Parameters.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`
- **Source Type:** Project parameters
- **Content:** 18 parameters covering identity, location, contract, schedule, facility, equipment, and economics
- **Supports:** Context for parametric model (currency = CAD, base year = 2026, warranty = 2 years post-CCC)
- **Parsing Notes:** Standard CSV; used for context validation only — no direct unit pricing

### 4. Fees_Permits_Insurance.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Fees_Permits_Insurance.csv`
- **Source Type:** Fee/permit/insurance allowances
- **Content:** 5 line items covering bonding premiums, insurance, and permit fees
- **Supports:** Not directly applicable to DEL-021-05 (warranty administration); these items cover pre-construction bonding/insurance/permits
- **Parsing Notes:** Standard CSV; items FP-01 through FP-05. None pertain to warranty-period administration costs.

## Source Coverage Assessment

| Source | Applicable to DEL-021-05 | Notes |
|---|---|---|
| Professional_Staff_Rates.csv | YES | Provides hourly rates for all 8 roles assigned to this deliverable |
| Level_of_Effort.csv | YES | Provides estimated hours for all 8 roles assigned to this deliverable |
| Assumed_Project_Parameters.csv | CONTEXT ONLY | Confirms currency, warranty duration, project identity |
| Fees_Permits_Insurance.csv | NO | Covers bonding/insurance procurement, not warranty administration |

## Gaps

- No gaps identified for professional services labour pricing. Both rate and hours sources are available.
- Fees_Permits_Insurance.csv does not contain warranty-period-specific costs (e.g., remediation contingency, inspection travel costs). These are outside the administrative scope of DEL-021-05 as defined.
