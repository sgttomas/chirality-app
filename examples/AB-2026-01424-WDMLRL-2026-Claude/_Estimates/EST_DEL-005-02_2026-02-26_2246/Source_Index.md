# Source Index — EST_DEL-005-02_2026-02-26_2246

## Indexed Price Sources

### PS-STAFF — Professional_Staff_Rates.csv

- **Path:** _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv
- **Source Type:** PARAMETRIC (staff hourly rate table)
- **Parsing Notes:** CSV with columns RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. 25 rows.
- **Supports:** Hourly rates for all professional staff roles. Used roles for DEL-005-02: R-01 (Project Manager, $165/hr), R-08 (Cost Estimator, $135/hr), R-13 (BIM Technician, $95/hr), R-17 (Civil Engineer, $160/hr). All rates are PARAMETRIC basis, MEDIUM confidence.
- **Cannot Support:** Construction labour rates, material costs, equipment pricing.

### PS-LOE — Level_of_Effort.csv

- **Path:** _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv
- **Source Type:** PARAMETRIC (deliverable-level effort allocation)
- **Parsing Notes:** CSV with columns Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. 577 rows total; 4 rows for DEL-005-02.
- **Supports:** Hour allocations per role per deliverable. DEL-005-02 allocations: R-01=6hr, R-08=4hr, R-13=36hr, R-17=84hr. Total: 130 hours. All PARAMETRIC basis.
- **Cannot Support:** Material quantities, equipment counts, construction labour.

### PS-PARAMS — Assumed_Project_Parameters.csv

- **Path:** _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv
- **Source Type:** PARAMETRIC (project parameters and assumptions)
- **Parsing Notes:** CSV with 18 rows. Key parameter for this estimate: PP-17 (Currency=CAD, ASSUMPTION, MEDIUM confidence).
- **Supports:** Project context parameters (identity, location, schedule, facility dimensions, currency).
- **Cannot Support:** Direct pricing evidence.

### PS-DF — Professional_Design_Fees.csv

- **Path:** _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv
- **Source Type:** PARAMETRIC (fee percentage model)
- **Parsing Notes:** CSV with 5 rows. Relevant row: DF-05 (Civil/site design fee, 0.6%-1.5% of construction value, recommended 1.0%).
- **Supports:** Cross-check of LOE-based estimate against fee-percentage model. Not used as primary pricing method for this run (LOE x rate is primary method).
- **Cannot Support:** Direct line-item pricing.

## Source Coverage Summary

| Item | Source Match | Coverage |
|---|---|---|
| ITEM-001 (PM) | PS-LOE row DEL-005-02/R-01 + PS-STAFF row R-01 | Full |
| ITEM-002 (Cost Estimator) | PS-LOE row DEL-005-02/R-08 + PS-STAFF row R-08 | Full |
| ITEM-003 (BIM Technician) | PS-LOE row DEL-005-02/R-13 + PS-STAFF row R-13 | Full |
| ITEM-004 (Civil Engineer) | PS-LOE row DEL-005-02/R-17 + PS-STAFF row R-17 | Full |
