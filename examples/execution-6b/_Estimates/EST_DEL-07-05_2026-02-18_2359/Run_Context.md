# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-07-05_2026-02-18_2359 |
| **AsOf** | 2026-02-18T23:59:00-07:00 |
| **Scope** | DEL-07-05 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-07-05/Dependencies.csv -- 13 ACTIVE rows found) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |

## Resolved Paths

| Source | Resolved Path | Status |
|---|---|---|
| Professional_Staff_Rates.csv | test/execution-6b/_PriceSources/Professional_Staff_Rates.csv | OK -- 30 roles loaded |
| Level_of_Effort.csv | test/execution-6b/_PriceSources/Level_of_Effort.csv | OK -- 2 rows matching DEL-07-05 |
| Assumed_Project_Parameters.csv | test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv | OK -- 29 parameters loaded (reference context) |
| Decomposition | test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md | OK -- v2.3 FINAL |
| Dependencies.csv | test/execution-6b/PKG-007_.../DEL-07-05_.../Dependencies.csv | OK -- 13 ACTIVE rows |

## CBS Mapping Rule

CBS codes are assigned deterministically using the role Category from Professional_Staff_Rates.csv:
- Management category roles -> CBS = `MGMT` (project management and quality leadership)
- No other role categories appear for DEL-07-05.

## Warnings

- None.
