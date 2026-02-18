# Run Context -- EST_DEL-09-02_2026-02-18_1600

## Run Identity

| Field | Value |
|---|---|
| **RunID** | EST_DEL-09-02_2026-02-18_1600 |
| **AsOf** | 2026-02-18T16:00:00-07:00 |
| **Agent** | ESTIMATING (Type 2) |

---

## Inputs (as provided)

| Parameter | Value |
|---|---|
| **Scope** | DEL-09-02 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **RUN_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-09_Due Diligence & Risk Register/1_Working/DEL-09-02_SiteConditionsAndDueDiligenceSummary |
| **ESTIMATES_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Estimates/ |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **DECOMPOSITION_PATH** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md |
| **DEPENDENCY_SOURCES** | AUTO (resolved to DEL-09-02/Dependencies.csv) |
| **PRICE_SOURCES** | See list below |
| **OUTPUT_LABEL** | DEL-09-02 |
| **UPDATE_LATEST_POINTER** | FALSE |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **ROUNDING** | DOLLAR |

---

## Resolved PRICE_SOURCES

| # | File | Status |
|---|---|---|
| 1 | Professional_Staff_Rates.csv | LOADED -- 30 roles; R-02, R-07, R-29 applicable to DEL-09-02 |
| 2 | Level_of_Effort.csv | LOADED -- 3 rows for DEL-09-02 (R-02: 8h, R-07: 6h, R-29: 4h) |
| 3 | Assumed_Project_Parameters.csv | LOADED -- 29 parameters; used for context only (no direct pricing impact on DEL-09-02) |

---

## CBS Mapping Rule

No explicit `CBSHint` is provided in the decomposition for DEL-09-02. The deterministic CBS mapping used is:

- **PROF-PM** = Professional services -- Project Management (R-02 hours)
- **PROF-CIVIL** = Professional services -- Civil Engineering (R-07 hours)
- **PROF-GEOTECH** = Professional services -- Geotechnical Engineering (R-29 hours)

This mapping derives CBS codes from role categories in Professional_Staff_Rates.csv: Management roles map to PROF-PM, Civil Engineering roles to PROF-CIVIL, and Specialty (Geotechnical) roles to PROF-GEOTECH.

---

## Warnings

- None. All 3 price source files loaded successfully. Decomposition found. Dependency register found with 15 rows (6 upstream prerequisites are PENDING -- reference reports currently inaccessible -- but this does not block proposal production cost estimation).

---

## Exclusions Applied

- `_Estimates/**`
- `_Aggregation/**`
- `_Reconciliation/**`
- `_Archive/**`
