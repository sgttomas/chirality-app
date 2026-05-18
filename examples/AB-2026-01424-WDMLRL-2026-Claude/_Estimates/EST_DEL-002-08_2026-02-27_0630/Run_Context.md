# Run Context — EST_DEL-002-08_2026-02-27_0630

| Field | Value |
|---|---|
| **RunID** | EST_DEL-002-08_2026-02-27_0630 |
| **AsOf** | 2026-02-27T06:30:00-07:00 |
| **Scope** | DEL-002-08 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-002-08 Steel Plate Embedment Plan) in PKG-002 Structural Design |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | (1) Professional_Staff_Rates.csv, (2) Level_of_Effort.csv, (3) Assumed_Project_Parameters.csv, (4) Professional_Design_Fees.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-002-08 |

## Resolved Price Sources

| # | Path | Type | Notes |
|---|---|---|---|
| 1 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv | PARAMETRIC (rate table) | 25 roles with hourly rates in CAD; Confidence MEDIUM |
| 2 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv | PARAMETRIC (hours model) | Per-deliverable hours allocation by role; Confidence MEDIUM |
| 3 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv | PARAMETRIC (parameters) | 19 project parameters; used for context validation |
| 4 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv | PARAMETRIC (fee model) | Percentage-based design fees; not used for this deliverable (LOE pricing preferred) |

## Warnings

- None. All four deliverable documents (Datasheet, Specification, Guidance, Procedure) are present and readable.
- LOE pricing source provides direct hours allocation for DEL-002-08.
