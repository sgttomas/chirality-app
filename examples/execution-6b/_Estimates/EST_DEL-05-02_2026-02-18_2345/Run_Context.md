# Run_Context.md

| Field | Value |
|---|---|
| **RunID** | EST_DEL-05-02_2026-02-18_2345 |
| **AsOf** | 2026-02-18T23:45:00 |
| **Scope** | DEL-05-02 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-05-02/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |

## Resolved Paths

- **ESTIMATES_ROOT:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Estimates/
- **Deliverable path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-005_Building_Durability_and_Maintenance/1_Working/DEL-05-02_StructuralDurabilityAndMaintenance/
- **Decomposition:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md
- **Rate table:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_PriceSources/Professional_Staff_Rates.csv
- **Level of effort:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_PriceSources/Level_of_Effort.csv
- **Project parameters:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv

## CBS Mapping Rule

CBS codes are assigned deterministically based on the role category from Professional_Staff_Rates.csv:
- Design roles -> CBS = `DESIGN_SERVICES`
- Management roles -> CBS = `MANAGEMENT`
- Construction roles -> CBS = `CONSTRUCTION_SERVICES`
- Financial roles -> CBS = `FINANCIAL_SERVICES`
- Administrative roles -> CBS = `ADMINISTRATIVE`
- Specialty roles -> CBS = `SPECIALTY_CONSULTING`
- Legal roles -> CBS = `LEGAL`
- External roles -> CBS = `EXTERNAL`

For DEL-05-02, the only role is R-09 (Structural Engineer Senior, Category: Design), so CBS = `DESIGN_SERVICES`.

## Warnings

None.
