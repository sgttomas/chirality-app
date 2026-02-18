# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-03-04_2026-02-18_2300 |
| **AsOf** | 2026-02-18T23:00:00-07:00 |
| **Scope** | DEL-03-04 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-03-04/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |

## Resolved Paths

- **ESTIMATES_ROOT:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Estimates/
- **Snapshot:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Estimates/EST_DEL-03-04_2026-02-18_2300/
- **Decomposition:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md
- **Rate Table:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_PriceSources/Professional_Staff_Rates.csv
- **Level of Effort:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_PriceSources/Level_of_Effort.csv
- **Project Parameters:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv
- **Dependency Source:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-003_Design_Brief/1_Working/DEL-03-04_MechanicalDesignBrief/Dependencies.csv

## CBS Mapping Rule

CBS codes are assigned using the following deterministic rule:
- Professional services hours for proposal-phase design deliverables are mapped to CBS = `PROF_SERVICES_DESIGN`.
- This mapping is applied uniformly because all line items for DEL-03-04 represent professional engineering labor for producing a design brief narrative.

## Warnings

None.
