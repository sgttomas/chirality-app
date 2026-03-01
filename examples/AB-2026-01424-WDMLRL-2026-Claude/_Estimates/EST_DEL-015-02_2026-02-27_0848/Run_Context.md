# Run Context — EST_DEL-015-02_2026-02-27_0848

| Field | Value |
|---|---|
| **RunID** | EST_DEL-015-02_2026-02-27_0848 |
| **AsOf** | 2026-02-27T08:48Z |
| **Scope** | DEL-015-02 (Lighting Installation) |
| **ScopeResolvedSummary** | 1 deliverable in PKG-015 (Electrical & Low-Voltage Installation) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-015-02 |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |

## PRICE_SOURCES (resolved)

| # | Path | Type |
|---|---|---|
| 1 | PriceSources/Professional_Staff_Rates.csv | Rate Table (professional staff hourly rates) |
| 2 | PriceSources/Level_of_Effort.csv | Parametric (hours by role by deliverable) |
| 3 | PriceSources/Assumed_Project_Parameters.csv | Parametric (facility parameters) |
| 4 | PriceSources/Electrical_System_Rates.csv | Rate Table / Parametric (electrical material + install rates) |
| 5 | PriceSources/Underground_Utility_Rates.csv | Rate Table / Parametric (underground utility rates) |
| 6 | PriceSources/Construction_Labour_Rates.csv | Rate Table (trade labour rates) |

All paths relative to: `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/`

## Warnings

- W-01: Several design parameters for DEL-015-02 are TBD pending IFC drawings (Wash Bay fixture wattage/lumens, mounting method, controls/switching, conduit type, panel/circuit assignments, emergency lighting scope).
- W-02: 8-foot LED linear fixture pricing not directly present in Electrical_System_Rates.csv (ES-01 covers high-bay only). Parametric estimate derived from industry data.
- W-03: Controls/switching scope is TBD; allowance included.
- W-04: Emergency/exit lighting scope is unresolved; excluded from this estimate per current scope definition. If added, cost will increase.
- W-05: Ceiling fan coordination interface identified but fans are out of scope for DEL-015-02.
