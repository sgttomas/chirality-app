# Source Index — EST_DEL-007-02_2026-02-27_0600

## Indexed Price Sources

### 1. Professional_Staff_Rates.csv

- **Path**: `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`
- **Source Type**: Rate Table (parametric hourly rates)
- **Parsing Notes**: CSV with columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. 25 roles defined.
- **Supports**: Unit rate pricing for professional staff hours. All rates stated in CAD with PARAMETRIC basis and MEDIUM confidence.
- **Roles Used for DEL-007-02**:
  - R-01 Project Manager: 165 CAD/hr
  - R-08 Cost Estimator: 135 CAD/hr
  - R-19 Landscape Architect: 135 CAD/hr

### 2. Level_of_Effort.csv

- **Path**: `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`
- **Source Type**: Parametric LOE Model (estimated hours by deliverable and role)
- **Parsing Notes**: CSV with columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. Contains rows for all deliverables in the execution.
- **Supports**: Hour quantities per role per deliverable. All entries have PARAMETRIC basis.
- **Rows Used for DEL-007-02**:
  - DEL-007-02 / R-01 Project Manager: 6 hours
  - DEL-007-02 / R-08 Cost Estimator: 4 hours
  - DEL-007-02 / R-19 Landscape Architect: 70 hours
- **Limitations**: LOE notes for DEL-007-02 rows state "PKG-007 Landscape Architect -- TBD" suggesting the LOE allocation may be preliminary/placeholder.

### 3. Assumed_Project_Parameters.csv

- **Path**: `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`
- **Source Type**: Parameter Set
- **Parsing Notes**: CSV with columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes. 19 parameters defined.
- **Supports**: Project-level context parameters (currency, facility dimensions, equipment counts). Used for context validation, not direct pricing.
- **Key Parameters Used**: PP-17 Currency = CAD (ASSUMPTION, MEDIUM confidence); PP-10 Floor Area approx 13,000 sqft.

### 4. Professional_Design_Fees.csv

- **Path**: `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv`
- **Source Type**: Fee Percentage Model (parametric)
- **Parsing Notes**: CSV with columns: ItemID, Discipline, Description, FeePercentMin, FeePercentMax, RecommendedPercent, FeeBase, Basis, Confidence, Notes. 5 discipline fees defined.
- **Supports**: Alternative pricing method for design deliverables as a percentage of construction value. Not directly used for DEL-007-02 (LOE model preferred for individual deliverable estimate).
- **Limitations**: Requires a construction value estimate to apply; no landscape-specific fee row defined (closest would be a subset of Architecture or a custom entry). Not used in this run.

## Sources Not Used

- Professional_Design_Fees.csv was indexed but not applied because the LOE + Rate Table approach provides more granular, deliverable-specific pricing than a fee-percentage method for a single deliverable estimate.
