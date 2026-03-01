# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-002-10_2026-02-26_2239 |
| **AsOf** | 2026-02-27T05:39:52Z |
| **Scope** | DEL-002-10 (Structural Calculation Package) |
| **ScopeResolvedSummary** | 1 deliverable, 1 package (PKG-002 Structural Design) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Professional_Design_Fees.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE |
| **OUTPUT_LABEL** | DEL-002-10 |

## Resolved Price Source Paths

| Source | Absolute Path | Type |
|---|---|---|
| Professional_Staff_Rates.csv | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | Rate Table (hourly rates by role) |
| Level_of_Effort.csv | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | Parametric (hours by deliverable and role) |
| Assumed_Project_Parameters.csv | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` | Parametric (project parameters) |
| Professional_Design_Fees.csv | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` | Parametric (percentage-based fee model — not used for this run) |

## Scope Notes

- DEL-002-10 is the Structural Calculation Package under PKG-002 Structural Design.
- It is part of an SCC bundle with DEL-002-01 (Preliminary Structural Design) within T1 iterative coordination. Estimated independently per brief instructions.
- SOW coverage: SOW-0012 (structural design), SOW-0019 (foundation variable-price scope).
- Deliverable type: Calculation Package (professional engineering labor).

## Warnings

- None at run level. All required inputs resolved.
