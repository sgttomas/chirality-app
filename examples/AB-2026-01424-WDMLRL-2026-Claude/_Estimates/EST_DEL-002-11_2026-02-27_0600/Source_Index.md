# Source Index — EST_DEL-002-11_2026-02-27_0600

## Price Sources Indexed

### Source 1 — Professional_Staff_Rates.csv

- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`
- **Type:** RATE_TABLE (parametric hourly rates)
- **Content:** 25 roles with hourly rates in CAD, each tagged with PARAMETRIC basis and MEDIUM confidence
- **Relevant roles for DEL-002-11:**
  - R-01 Project Manager: $165/hr
  - R-08 Cost Estimator: $135/hr
  - R-13 BIM Technician: $95/hr
  - R-14 Structural Engineer: $170/hr
- **Parsing notes:** Clean CSV; all rates in CAD; no currency conversion needed
- **Supports:** Unit rate pricing for all four role-based line items (ITEM-001 through ITEM-004)

### Source 2 — Level_of_Effort.csv

- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`
- **Type:** PARAMETRIC (estimated hours by role per deliverable)
- **Content:** Multi-deliverable LOE table; 4 rows for DEL-002-11 Foundation Design Package (Variable-Price)
- **DEL-002-11 rows:**
  - R-01 Project Manager: 6 hr
  - R-08 Cost Estimator: 4 hr
  - R-13 BIM Technician: 21 hr
  - R-14 Structural Engineer: 49 hr
- **Total hours for DEL-002-11:** 80 hr
- **Parsing notes:** Clean CSV; all hours are integers; basis is PARAMETRIC for all rows
- **Supports:** Quantity (hours) for all four role-based line items

### Source 3 — Assumed_Project_Parameters.csv

- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`
- **Type:** PARAMETRIC (project context parameters)
- **Content:** 20 project parameters covering identity, location, contract, schedule, facility, equipment, plumbing, mechanical, currency, and economics
- **Relevant parameters for DEL-002-11:**
  - PP-10: Addition Floor Area ~13,000 sqft (DERIVED, MEDIUM confidence)
  - PP-11: Ceiling Height 35 ft (CONFIRMED, HIGH)
  - PP-12: Overhead Cranes: 2 each (CONFIRMED, HIGH)
  - PP-13: Crane Capacity: 5 ton (CONFIRMED, HIGH)
  - PP-14: Cistern Volume: 50,000 L (CONFIRMED, HIGH)
  - PP-17: Currency: CAD (ASSUMPTION, MEDIUM)
- **Parsing notes:** Clean CSV; provides contextual confirmation but not direct pricing data
- **Supports:** Contextual validation of deliverable scope; does not directly generate pricing

### Source 4 — Professional_Design_Fees.csv

- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv`
- **Type:** PARAMETRIC (percentage-of-construction-value design fees)
- **Content:** 5 discipline-level fee percentages (Architecture, Structural, Mechanical, Electrical, Civil)
- **Relevant for DEL-002-11:**
  - DF-02 Structural design fee: 1.2%–2.5% of construction value; recommended 1.8%
- **Parsing notes:** Clean CSV; fee percentages require a construction value base which is not available in this run scope (construction value is TBD for the variable-price foundation). This source is not directly usable for this deliverable without a construction value estimate.
- **Supports:** Cannot be used as primary pricing basis for this run; retained as cross-check reference. See Decision_Log.md DEC-002.

## Sources Not Available / Not Applicable

- No QUOTE sources provided for this scope.
- No HISTORICAL data provided.
- No ALLOWANCE tables provided.
- Professional_Design_Fees.csv cannot be applied without a construction value base (TBD for variable-price foundation scope).
