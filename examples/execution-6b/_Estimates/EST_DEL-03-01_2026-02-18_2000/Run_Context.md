# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-03-01_2026-02-18_2000 |
| **AsOf** | 2026-02-18T20:00:00Z |
| **Scope** | DEL-03-01 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-03-01/Dependencies.csv; 17 rows found) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Resolved Paths

- **ESTIMATES_ROOT:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Estimates/
- **Decomposition:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md
- **Dependencies:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-003_Design_Brief/1_Working/DEL-03-01_ArchitecturalDesignBrief/Dependencies.csv
- **Rate Table:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_PriceSources/Professional_Staff_Rates.csv
- **Level of Effort:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_PriceSources/Level_of_Effort.csv
- **Parameters:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv

## CBS Mapping Rule

CBS code assigned as `PROF-ARCH` for Architect (Project) hours on Design Brief deliverables. This follows a deterministic rule: `PROF-{discipline abbreviation}` where discipline is derived from the role category in Professional_Staff_Rates.csv. R-04 (Architect, Project) is in the Design category, discipline = Architecture, abbreviation = ARCH.

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-03-01 | PKG-003 | PKG-003_Design_Brief/1_Working/DEL-03-01_ArchitecturalDesignBrief/ | TRUE | Architectural Design Brief; single role (R-04) per Level_of_Effort.csv |
