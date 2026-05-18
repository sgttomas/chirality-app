# Run Context — EST_DEL-003-02_2026-02-27_0841

| Field | Value |
|---|---|
| **RunID** | EST_DEL-003-02_2026-02-27_0841 |
| **AsOf** | 2026-02-27T08:41Z |
| **Scope** | DEL-003-02 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-003-02 HVAC Layout Plans) in PKG-003 (Mechanical Design) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Professional_Design_Fees.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **OUTPUT_LABEL** | DEL-003-02 |
| **Rounding** | NONE (default) |
| **RUN_TIMESTAMP** | 2026-02-27T08:41Z |

## Resolved Price Sources

| Source File | Type | Notes |
|---|---|---|
| Professional_Staff_Rates.csv | PARAMETRIC rate table | 25 roles with hourly rates in CAD; basis = PARAMETRIC; confidence = MEDIUM |
| Level_of_Effort.csv | PARAMETRIC LOE model | Estimated hours by deliverable and role; basis = PARAMETRIC |
| Assumed_Project_Parameters.csv | Project parameters | 19 parameters (facility dimensions, equipment counts, schedule, currency) |
| Professional_Design_Fees.csv | PARAMETRIC fee model | Percentage-of-construction-value design fees by discipline |

## Warnings

- LOE model provides hours for 4 roles only (R-01, R-08, R-13, R-15) for DEL-003-02. Additional roles (e.g., R-06 QA/QC, R-09 Document Controller, R-24 Controls Specialist) are not included in the LOE but may contribute effort to this deliverable.
- Professional_Design_Fees.csv provides an alternative parametric method (% of construction value) but construction value is not established; LOE-based pricing is used as primary method.
- All rate confidence levels are MEDIUM per source data.
