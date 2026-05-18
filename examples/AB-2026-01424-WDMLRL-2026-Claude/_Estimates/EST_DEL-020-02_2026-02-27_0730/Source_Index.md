# Source Index — EST_DEL-020-02_2026-02-27_0730

## Indexed Price Sources

### 1. Professional_Staff_Rates.csv
- **Path:** _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv
- **Type:** Rate table (parametric hourly rates)
- **Content:** 25 professional staff roles with RoleID, Role name, Category, HourlyRate_CAD, Basis (all PARAMETRIC), and Confidence (all MEDIUM)
- **Supports:** Unit rate pricing for all labour line items in DEL-020-02
- **Parsing notes:** Standard CSV; clean; no parsing issues. All rates in CAD.
- **Roles used for DEL-020-02:** R-01 ($165), R-02 ($155), R-03 ($145), R-05 ($140), R-06 ($135), R-08 ($135), R-09 ($75), R-23 ($160)

### 2. Level_of_Effort.csv
- **Path:** _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv
- **Type:** Parametric model (estimated hours by role per deliverable)
- **Content:** Hours allocation for each deliverable in the project, by role. Basis is PARAMETRIC for all entries.
- **Supports:** Quantity (hours) input for all labour line items in DEL-020-02
- **Parsing notes:** Standard CSV; large file (~530+ rows). 8 rows matched for DEL-020-02. All entries under Execution ID AB-2026-01424-WDMLRL-2026-Claude.
- **DEL-020-02 rows:** R-01 (6 hr), R-02 (8 hr), R-03 (10 hr), R-05 (4 hr), R-06 (6 hr), R-08 (4 hr), R-09 (12 hr), R-23 (30 hr)

### 3. Assumed_Project_Parameters.csv
- **Path:** _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv
- **Type:** Parametric parameters
- **Content:** 18 project parameters (identity, location, contract, schedule, facility, equipment, plumbing, mechanical, currency, economics)
- **Supports:** Context and validation only; no direct pricing for DEL-020-02. Confirms CAD currency (PP-17) and December 31, 2026 deadline (PP-07).
- **Parsing notes:** Standard CSV; clean. Confidence ranges from MEDIUM to HIGH.

### 4. Optional_Items_Pricing.csv
- **Path:** _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Optional_Items_Pricing.csv
- **Type:** Allowance table
- **Content:** 2 optional/alternate items (OPT-01: winter conditions allowance; OPT-02: contaminated soils allowance)
- **Supports:** Not applicable to DEL-020-02 (no optional items relevant to final inspection and CCC)
- **Parsing notes:** Standard CSV; clean. Both items are ALLOWANCE basis with LOW confidence.

## Sources Not Applicable

No additional sources were identified or required. All pricing for DEL-020-02 is fully supported by the combination of Professional_Staff_Rates.csv (unit rates) and Level_of_Effort.csv (quantities).
