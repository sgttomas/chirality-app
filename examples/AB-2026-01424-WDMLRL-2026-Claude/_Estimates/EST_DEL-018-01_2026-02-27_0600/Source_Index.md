# Source Index — EST_DEL-018-01_2026-02-27_0600

## Indexed Price Sources

### 1. Professional_Staff_Rates.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`
- **Type:** Rate table (PARAMETRIC basis)
- **Content:** 25 professional roles (R-01 through R-25) with hourly rates in CAD. Covers management, design, specialty, and admin categories.
- **Applicable to DEL-018-01:** R-01 (Project Manager, $165/hr), R-02 (Construction PM, $155/hr), R-03 (Site Superintendent, $145/hr), R-05 (HSE Manager, $140/hr), R-06 (QA/QC Lead, $135/hr), R-08 (Cost Estimator, $135/hr).
- **Confidence:** MEDIUM (all rates are PARAMETRIC basis).

### 2. Level_of_Effort.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`
- **Type:** Parametric (estimated hours per deliverable per role)
- **Content:** Estimated hours for all deliverables across the project. DEL-018-01 entries at rows 455-460.
- **Applicable to DEL-018-01:** 6 role entries totaling 38 professional staff hours (R-01: 6h, R-02: 8h, R-03: 10h, R-05: 4h, R-06: 6h, R-08: 4h).
- **Confidence:** MEDIUM (PARAMETRIC basis).
- **Notes:** Notes column shows "PKG-018 TBD -- TBD" indicating these are preliminary parametric estimates.

### 3. Assumed_Project_Parameters.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`
- **Type:** Parametric (project-level parameters)
- **Content:** 18 parameters covering identity, location, contract, schedule, facility, equipment, plumbing, mechanical, currency, and economics.
- **Applicable to DEL-018-01:** PP-10 (Addition Floor Area ~13,000 sqft), PP-17 (Currency CAD), PP-18 (Base Year 2026).
- **Notes:** PP-10 describes the building floor area, not the full driving surface area for topsoil stripping. Stripping area requires separate parametric assumption.

### 4. Earthwork_Civil_Rates.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Earthwork_Civil_Rates.csv`
- **Type:** Rate table (PARAMETRIC basis)
- **Content:** 4 earthwork items (EC-01 through EC-04).
- **Applicable to DEL-018-01:** EC-04 (Topsoil stripping + stockpile, $3.20/m2 recommended rate, range $2.00-$4.50/m2). Directly relevant.
- **Confidence:** MEDIUM.

### 5. Paving_Surfacing_Rates.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Paving_Surfacing_Rates.csv`
- **Type:** Rate table (PARAMETRIC basis)
- **Content:** 4 paving/surfacing items (PS-01 through PS-04).
- **Applicable to DEL-018-01:** Not directly applicable. (Driving surface construction is DEL-018-03, not DEL-018-01.)

### 6. Underground_Utility_Rates.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Underground_Utility_Rates.csv`
- **Type:** Rate table (PARAMETRIC/ALLOWANCE basis)
- **Content:** 5 underground utility items (UU-01 through UU-05).
- **Applicable to DEL-018-01:** Not directly applicable. (Utility installation is DEL-018-06, not DEL-018-01.)

### 7. Construction_Labour_Rates.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Construction_Labour_Rates.csv`
- **Type:** Rate table (PARAMETRIC basis)
- **Content:** 10 construction trades (T-01 through T-10) with base hourly rates, burden multipliers, and fully burdened rates.
- **Applicable to DEL-018-01:** T-07 (Equipment Operator, $88.00/hr fully burdened), T-08 (Labourer, $65.10/hr fully burdened).
- **Confidence:** MEDIUM.

## Source Coverage Summary

| Source Type | Count Applicable | Items Supported |
|-------------|-----------------|-----------------|
| Rate table — professional staff | 6 roles | ITEM-009 through ITEM-014 |
| Rate table — earthwork | 1 item (EC-04) | ITEM-001 |
| Rate table — construction labour | 2 trades (T-07, T-08) | ITEM-015, ITEM-016 |
| Parametric — level of effort | 6 entries | ITEM-009 through ITEM-014 (hours) |
| Not covered by rate evidence | 6 items | ITEM-002 through ITEM-008 (priced as ALLOWANCE) |
