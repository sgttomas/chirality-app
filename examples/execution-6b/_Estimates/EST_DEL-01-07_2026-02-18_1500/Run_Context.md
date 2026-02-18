# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-01-07_2026-02-18_1500 |
| **AsOf** | 2026-02-18T15:00:00-07:00 |
| **Scope** | DEL-01-07 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-01-07/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Resolved Paths

| Input | Resolved Path |
|---|---|
| ESTIMATES_ROOT | test/execution-6b/_Estimates/ |
| Snapshot | test/execution-6b/_Estimates/EST_DEL-01-07_2026-02-18_1500/ |
| Decomposition | test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md |
| Dependencies (AUTO) | test/execution-6b/PKG-001_.../DEL-01-07_DesignBuildFirmExperienceProfile/Dependencies.csv |
| Professional_Staff_Rates.csv | test/execution-6b/_PriceSources/Professional_Staff_Rates.csv |
| Level_of_Effort.csv | test/execution-6b/_PriceSources/Level_of_Effort.csv |
| Assumed_Project_Parameters.csv | test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv |

## CBS Mapping Rule

CBS codes are assigned deterministically based on the `Category` field in Professional_Staff_Rates.csv:
- Management roles -> CBS `MGMT`
- Administrative roles -> CBS `ADMIN`
- All other roles contributing to DEL-01-07 -> CBS `PROP_PRODUCTION` (proposal production labor)

For DEL-01-07 specifically, all labor is proposal production work, so CBS = `PROP_PRODUCTION` is applied uniformly. This is consistent with the deliverable's nature as a qualifications narrative document.

## Pricing Method

Cost = SUM(Hours_per_role x HourlyRate_per_role) for each role assigned to DEL-01-07 in Level_of_Effort.csv, with rates drawn from Professional_Staff_Rates.csv. Method = RATE_TABLE for all lines.
