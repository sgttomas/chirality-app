# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-05-04_2026-02-18_2355 |
| **AsOf** | 2026-02-18T23:55:00-07:00 |
| **Scope** | DEL-05-04 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-05-04/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Resolved Paths

- **ESTIMATES_ROOT:** `test/execution-6b/_Estimates/`
- **DELIVERABLE_PATH:** `test/execution-6b/PKG-005_Building_Durability_and_Maintenance/1_Working/DEL-05-04_ElectricalMaintainability/`
- **Professional_Staff_Rates.csv:** `test/execution-6b/_PriceSources/Professional_Staff_Rates.csv`
- **Level_of_Effort.csv:** `test/execution-6b/_PriceSources/Level_of_Effort.csv`
- **Assumed_Project_Parameters.csv:** `test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv`
- **Dependencies.csv:** `test/execution-6b/PKG-005_Building_Durability_and_Maintenance/1_Working/DEL-05-04_ElectricalMaintainability/Dependencies.csv`

## CBS Mapping Rule

CBS codes are assigned deterministically based on RoleID category from Professional_Staff_Rates.csv:
- Design roles (R-04 through R-14) -> CBS = `DESIGN_SERVICES`
- Management roles (R-01 through R-03) -> CBS = `MANAGEMENT`
- Construction roles (R-15 through R-21) -> CBS = `CONSTRUCTION_SERVICES`
- Administrative roles (R-22 through R-24) -> CBS = `ADMINISTRATIVE`
- Financial roles (R-18 through R-19) -> CBS = `FINANCIAL`
- Specialty roles (R-27 through R-29) -> CBS = `SPECIALTY_CONSULTING`
- Legal/External (R-25, R-30) -> CBS = `EXTERNAL_SERVICES`

For DEL-05-04, all hours are R-13 (Electrical Engineer, Senior, Design category) -> CBS = `DESIGN_SERVICES`.

## Pricing Method

Hours sourced from Level_of_Effort.csv (DEL-05-04 rows, Execution=6b). Rates sourced from Professional_Staff_Rates.csv (matching RoleID). Amount = Hours x HourlyRate, rounded to nearest whole dollar per ROUNDING=DOLLAR.
