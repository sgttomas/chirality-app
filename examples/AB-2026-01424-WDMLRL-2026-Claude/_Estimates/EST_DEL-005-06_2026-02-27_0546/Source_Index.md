# Source Index — EST_DEL-005-06_2026-02-27_0546

## Price Sources Indexed

### PS-STAFF: Professional_Staff_Rates.csv

- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`
- **Type:** PARAMETRIC (hourly rate table)
- **Rows used:** 4 of 25
  - R-01 Project Manager: $165/hr (MEDIUM confidence)
  - R-08 Cost Estimator: $135/hr (MEDIUM confidence)
  - R-13 BIM Technician: $95/hr (MEDIUM confidence)
  - R-17 Civil Engineer: $160/hr (MEDIUM confidence)
- **Parsing notes:** Clean CSV; all rates in CAD; all PARAMETRIC basis.
- **Supports:** Unit rate pricing for all labour line items.

### PS-LOE: Level_of_Effort.csv

- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`
- **Type:** PARAMETRIC (estimated hours by deliverable x role)
- **Rows used:** 4 of 577 (filtered to DEL-005-06)
  - DEL-005-06, R-01 Project Manager: 6 hr
  - DEL-005-06, R-08 Cost Estimator: 4 hr
  - DEL-005-06, R-13 BIM Technician: 24 hr
  - DEL-005-06, R-17 Civil Engineer: 56 hr
- **Total hours:** 90 hr
- **Parsing notes:** Clean CSV; filtered by Execution and DeliverableID columns.
- **Supports:** Quantity (hours) for all labour line items.

### PS-PARAMS: Assumed_Project_Parameters.csv

- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`
- **Type:** Project parameters and assumptions
- **Rows used for context:** PP-17 Currency = CAD; PP-18 Base Year = 2026; PP-10 Floor Area approx 13,000 sqft
- **Parsing notes:** Clean CSV; used for context and currency confirmation only.
- **Supports:** Currency confirmation; project context.

### PS-DF: Professional_Design_Fees.csv

- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv`
- **Type:** PARAMETRIC (design fee percentage model)
- **Row applicable:** DF-05 Civil/site design fee: 0.6%–1.5% of construction value (recommended 1.0%)
- **Parsing notes:** Clean CSV; fee percentages require a construction value base to compute. Construction value is not available for this deliverable in isolation.
- **Supports:** Cross-check only (cannot compute fee amount without construction value estimate). Not used for primary pricing.

## Sources Not Used

The following price source files exist in the PriceSources folder but are not applicable to this professional services / calculation package deliverable:

- Building_Envelope_Rates.csv — construction material rates; not applicable to a design calculation deliverable
- Construction_Labour_Rates.csv — trade labour rates; not applicable to professional design services
- Earthwork_Civil_Rates.csv — construction earthwork rates; not applicable
- Electrical_System_Rates.csv — electrical construction; not applicable
- Equipment_Pricing.csv — major equipment; not applicable
- Fees_Permits_Insurance.csv — permits/insurance; not applicable to this deliverable
- Interior_Architectural_Rates.csv — interior construction; not applicable
- Mechanical_System_Rates.csv — mechanical construction; not applicable
- Optional_Items_Pricing.csv — optional/contingency; not applicable
- Parametric_Building_Rates.csv — building construction cross-check; not applicable
- Paving_Surfacing_Rates.csv — surfacing construction; not applicable
- Structural_Concrete_Rates.csv — concrete construction; not applicable
- Underground_Utility_Rates.csv — underground construction; not applicable
