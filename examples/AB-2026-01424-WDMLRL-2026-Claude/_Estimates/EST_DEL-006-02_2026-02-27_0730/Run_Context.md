# Run Context — EST_DEL-006-02_2026-02-27_0730

| Field | Value |
|---|---|
| **RunID** | EST_DEL-006-02_2026-02-27_0730 |
| **AsOf** | 2026-02-27T07:30:00-07:00 |
| **Scope** | DEL-006-02 (Water Distribution Plans) |
| **ScopeResolvedSummary** | 1 deliverable; 1 package (PKG-006); 4 documents read (Datasheet, Specification, Guidance, Procedure) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |

## PRICE_SOURCES (resolved)

| # | Path | Type |
|---|---|---|
| 1 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv | Rate Table (hourly rates by role) |
| 2 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv | Parametric LOE model (hours by deliverable and role) |
| 3 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv | Project parameters (facility, equipment, plumbing attributes) |
| 4 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv | Fee percentages (not used for this deliverable; LOE approach preferred) |

## Warnings

- None. All four deliverable documents present. Pricing sources provide direct LOE data for DEL-006-02.
