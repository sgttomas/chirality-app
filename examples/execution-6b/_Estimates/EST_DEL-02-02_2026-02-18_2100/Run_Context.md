# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-02-02_2026-02-18_2100 |
| **AsOf** | 2026-02-18T21:00:00-07:00 |
| **Scope** | DEL-02-02 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | (1) `_PriceSources/Professional_Staff_Rates.csv` -- staff hourly rates by role; (2) `_PriceSources/Level_of_Effort.csv` -- hours by deliverable and role; (3) `_PriceSources/Assumed_Project_Parameters.csv` -- project parameters |
| **DECOMPOSITION_PATH** | `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO -- read `DEL-02-02_CivilSiteConceptPlan/Dependencies.csv` (20 rows loaded) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **OUTPUT_LABEL** | DEL-02-02 |

## Resolved Paths

| Input | Resolved Path |
|---|---|
| ESTIMATES_ROOT | `test/execution-6b/_Estimates/` |
| Snapshot folder | `test/execution-6b/_Estimates/EST_DEL-02-02_2026-02-18_2100/` |
| Decomposition | `test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` |
| Rate Table | `test/execution-6b/_PriceSources/Professional_Staff_Rates.csv` |
| Level of Effort | `test/execution-6b/_PriceSources/Level_of_Effort.csv` |
| Project Parameters | `test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv` |
| Dependency Register | `test/execution-6b/PKG-002_Conceptual_Design/1_Working/DEL-02-02_CivilSiteConceptPlan/Dependencies.csv` |

## CBS Mapping Rule

CBS codes are assigned based on role category from `Professional_Staff_Rates.csv`:

| Role Category | CBS Code | Rationale |
|---|---|---|
| Design | CBS-200 (Design Labour) | Engineering design hours (civil senior, civil intermediate) |
| Production | CBS-210 (Drawing Production) | CAD/BIM production hours |

This mapping is deterministic: each role's `Category` field in the rate table drives the CBS code. No `CBSHint` was present in the decomposition for DEL-02-02.

## Warnings

None.
