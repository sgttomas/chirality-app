# Source Index — EST_DEL-004-05_2026-02-27_0630

## Pricing Sources Indexed

### 1. Professional_Staff_Rates.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`
- **Source Type:** PARAMETRIC (rate table)
- **Content:** Hourly rates (CAD) for 25 professional roles (R-01 through R-25), with basis, confidence, and notes.
- **Roles Used for DEL-004-05:**
  - R-01 Project Manager: $165/hr
  - R-08 Cost Estimator: $135/hr
  - R-13 BIM Technician: $95/hr
  - R-16 Electrical Engineer: $165/hr
- **Parsing Notes:** Standard CSV; all rates in CAD. Confidence is MEDIUM for all roles. Basis is PARAMETRIC for all entries.
- **Supports:** Unit rate pricing for all labour line items.

### 2. Level_of_Effort.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`
- **Source Type:** PARAMETRIC (effort model)
- **Content:** Estimated hours by deliverable, role, and execution. Covers all deliverables in the project.
- **Entries Used for DEL-004-05:**
  - DEL-004-05 / R-01 (Project Manager): 6 hrs
  - DEL-004-05 / R-08 (Cost Estimator): 4 hrs
  - DEL-004-05 / R-13 (BIM Technician): 36 hrs
  - DEL-004-05 / R-16 (Electrical Engineer): 84 hrs
- **Parsing Notes:** Standard CSV. Category column maps to PKG-004 Electrical Engineer Drawing Set. Basis is PARAMETRIC for all entries.
- **Supports:** Quantity (hours) for all labour line items.

### 3. Assumed_Project_Parameters.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`
- **Source Type:** PARAMETRIC (context parameters)
- **Content:** 18 project parameters including building area (~13,000 sqft), ceiling height (35 ft), currency (CAD), equipment counts, and facility specifications.
- **Entries Referenced:**
  - PP-10: Addition floor area ~13,000 sqft (context for receptacle density assessment)
  - PP-11: Ceiling height 35 ft (context for mounting height considerations)
  - PP-17: Currency CAD
- **Parsing Notes:** Standard CSV. Provides context but not direct pricing data.
- **Supports:** Contextual validation of scope and assumptions. Not directly used for line-item pricing.

### 4. Professional_Design_Fees.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv`
- **Source Type:** PARAMETRIC (fee percentage benchmarks)
- **Content:** Design fee percentages by discipline (5 entries, DF-01 through DF-05). Electrical design fee (DF-04) is 1.0%-2.2% of construction value, recommended 1.6%.
- **Entries Referenced:**
  - DF-04: Electrical design fee — 1.0%-2.2% of construction_value, recommended 1.6%
- **Parsing Notes:** Standard CSV. Fee base is "construction_value" which is not available for this run (construction cost estimate not in scope). This source is used for cross-check/validation only, not for primary pricing.
- **Supports:** Cross-check only. Primary pricing uses LOE x rates method.

## Sources Not Used

- No sources were excluded or found unusable. All four provided sources were indexed and referenced.
