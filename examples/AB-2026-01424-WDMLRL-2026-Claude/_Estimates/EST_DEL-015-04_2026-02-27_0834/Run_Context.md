# Run Context — EST_DEL-015-04_2026-02-27_0834

| Field | Value |
|---|---|
| **RunID** | EST_DEL-015-04_2026-02-27_0834 |
| **AsOf** | 2026-02-27T08:34:00Z |
| **Scope** | DEL-015-04 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-015-04 Equipment Power Circuits) in PKG-015 (Electrical & Low-Voltage Installation) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-015-04 |

## PRICE_SOURCES (resolved)

| # | Path | Type |
|---|---|---|
| 1 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | Rate Table (professional staff hourly rates) |
| 2 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | Parametric (hours by role per deliverable) |
| 3 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` | Reference (project parameters and assumptions) |
| 4 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Electrical_System_Rates.csv` | Rate Table (electrical material/installation rates) |
| 5 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Underground_Utility_Rates.csv` | Rate Table (underground utility rates) |
| 6 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Construction_Labour_Rates.csv` | Rate Table (construction trade labour rates) |

## DECOMPOSITION_PATH

`_Decomposition/WDMLRL_Decomposition_Claude.md`

## Warnings

- Multiple equipment circuit ratings (crane voltage/amperage, overhead door count, exhaust fan count) are TBD in the engineering documents; parametric allowances applied per FALLBACK_POLICY.
- No bill of materials exists for this deliverable; material quantities are parametric estimates based on available rate tables and engineering document content.
