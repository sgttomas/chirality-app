# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-01-09_2026-02-18_1500 |
| **AsOf** | 2026-02-18T15:00:00-07:00 |
| **Scope** | DEL-01-09 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-01-09/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Resolved Paths

| Input | Resolved Path |
|---|---|
| ESTIMATES_ROOT | test/execution-6b/_Estimates/ |
| Snapshot Folder | test/execution-6b/_Estimates/EST_DEL-01-09_2026-02-18_1500/ |
| Decomposition | test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md |
| Professional_Staff_Rates.csv | test/execution-6b/_PriceSources/Professional_Staff_Rates.csv |
| Level_of_Effort.csv | test/execution-6b/_PriceSources/Level_of_Effort.csv |
| Assumed_Project_Parameters.csv | test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv |
| Dependencies.csv | test/execution-6b/PKG-001_.../DEL-01-09_.../Dependencies.csv |

## Pricing Method

Cost = SUM( Hours_per_role x Hourly_rate_per_role )

- Hours sourced from Level_of_Effort.csv (filtered to DeliverableID = DEL-01-09)
- Rates sourced from Professional_Staff_Rates.csv (joined on RoleID)
- Method recorded as RATE_TABLE (hours x rate = amount)

## CBS Mapping Rule

CBS for DEL-01-09 is assigned as `LABOUR` since all cost drivers are professional staff hours for administrative/coordination work (subtrade list compilation and form completion). No materials, equipment, or subcontract costs are present.
