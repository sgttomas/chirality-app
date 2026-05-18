# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-04-02_2026-02-18_2300 |
| **AsOf** | 2026-02-18T23:00:00-07:00 |
| **Scope** | DEL-04-02 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-04-02/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-04-02 | PKG-004 | PKG-004_Sustainability_and_Energy/1_Working/DEL-04-02_MechanicalEnergyAndSolarReadiness/ | TRUE | Mechanical Energy and Solar Readiness |

## CBS Mapping Rule

CBS assignment is derived deterministically from the role category in Professional_Staff_Rates.csv:
- Design roles -> CBS = DESIGN_SERVICES
- All line items for DEL-04-02 use Design-category roles (Mechanical Engineer Senior), so CBS = DESIGN_SERVICES.

## Pricing Method

- Hourly quantities from Level_of_Effort.csv (DEL-04-02 rows, Execution=6b)
- Unit rates from Professional_Staff_Rates.csv (matched by RoleID)
- Method = RATE_TABLE for all lines
- Rounding = DOLLAR (amounts rounded to nearest whole dollar)

## Source Files (Resolved Paths)

- `test/execution-6b/_PriceSources/Professional_Staff_Rates.csv`
- `test/execution-6b/_PriceSources/Level_of_Effort.csv`
- `test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv`
- `test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md`
- `test/execution-6b/PKG-004_Sustainability_and_Energy/1_Working/DEL-04-02_MechanicalEnergyAndSolarReadiness/Dependencies.csv`
