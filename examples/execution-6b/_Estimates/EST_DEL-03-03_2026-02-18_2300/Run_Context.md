# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-03-03_2026-02-18_2300 |
| **AsOf** | 2026-02-18T23:00:00-07:00 |
| **Scope** | DEL-03-03 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-03-03/Dependencies.csv -- 15 dependency rows found) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Resolved Paths

| Source | Resolved Path |
|---|---|
| Professional_Staff_Rates.csv | `_PriceSources/Professional_Staff_Rates.csv` |
| Level_of_Effort.csv | `_PriceSources/Level_of_Effort.csv` |
| Assumed_Project_Parameters.csv | `_PriceSources/Assumed_Project_Parameters.csv` |
| Decomposition | `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` |
| Dependency Register | `PKG-003_Design_Brief/1_Working/DEL-03-03_StructuralDesignBrief/Dependencies.csv` |

## CBS Mapping Rule

CBS codes are assigned using the following deterministic rule:
- All hours for DEL-03-03 are professional services (structural engineering consulting) associated with proposal preparation.
- CBS = `PROF_SERVICES.STRUCTURAL` for structural engineer hours.
- This mapping is derived from the role category in `Professional_Staff_Rates.csv` (Category = "Design") combined with the discipline assignment in `Level_of_Effort.csv`.

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-03-03 | PKG-003 | PKG-003_Design_Brief/1_Working/DEL-03-03_StructuralDesignBrief/ | TRUE | Structural Design Brief -- single-role deliverable |
