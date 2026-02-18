# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-08-02_2026-02-18_2359 |
| **AsOf** | 2026-02-18T23:59:00-07:00 |
| **Scope** | DEL-08-02 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | test/execution-6b/_PriceSources/Professional_Staff_Rates.csv, test/execution-6b/_PriceSources/Level_of_Effort.csv, test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO -- read from test/execution-6b/PKG-008_Commissioning_Closeout_and_Warranty/1_Working/DEL-08-02_DeficienciesManagementNarrative/Dependencies.csv |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Scope Resolution

| DeliverableID | PackageID | Path | InScope |
|---|---|---|---|
| DEL-08-02 | PKG-008 | test/execution-6b/PKG-008_Commissioning_Closeout_and_Warranty/1_Working/DEL-08-02_DeficienciesManagementNarrative/ | TRUE |

## CBS Mapping Rule

CBS codes are assigned deterministically based on role category from Professional_Staff_Rates.csv:
- Management roles (R-01, R-02, R-03, R-23) -> CBS: MGMT
- Construction roles (R-15, R-16, R-17, R-20, R-21) -> CBS: CX (Commissioning for PKG-008 context)

For this deliverable (PKG-008 Commissioning, Closeout & Warranty), the CBS categories used are:
- **CX** -- Commissioning Lead hours (deficiency management process authoring)
- **MGMT** -- Project Manager hours (process review and input)

## Pricing Method

Hours sourced from Level_of_Effort.csv (filtered to Execution=6b, DeliverableID=DEL-08-02).
Rates sourced from Professional_Staff_Rates.csv (matched by RoleID).
Method = RATE_TABLE (hours x hourly rate).
Rounding applied at the line-item level to the nearest whole dollar.
