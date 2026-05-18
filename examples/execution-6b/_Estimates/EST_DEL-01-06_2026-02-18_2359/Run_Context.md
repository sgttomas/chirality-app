# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-01-06_2026-02-18_2359 |
| **AsOf** | 2026-02-18T23:59:00-07:00 |
| **Scope** | DEL-01-06 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 1 resolved; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (DEL-01-06/Dependencies.csv loaded) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **OUTPUT_LABEL** | DEL-01-06 |

## Resolved Paths

| Source | Resolved Path |
|---|---|
| Professional_Staff_Rates.csv | `_PriceSources/Professional_Staff_Rates.csv` |
| Level_of_Effort.csv | `_PriceSources/Level_of_Effort.csv` |
| Assumed_Project_Parameters.csv | `_PriceSources/Assumed_Project_Parameters.csv` |
| Decomposition | `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` |
| DEL-01-06 Dependencies | `PKG-001_.../DEL-01-06_.../Dependencies.csv` |

## CBS Mapping Rule

CBS codes are assigned deterministically using the following convention:
- `PROF_SERVICES.PM` = Project Manager hours (role category: Management, role: PM)
- `PROF_SERVICES.ESTIMATING` = Estimator hours (role category: Financial)

This mapping is derived from the `Category` column in `Professional_Staff_Rates.csv`.

## Warnings

None.
