# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-10-02_2026-02-18_1900 |
| **AsOf** | 2026-02-18T19:00:00-07:00 |
| **Scope** | DEL-10-02 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read `DEL-10-02/Dependencies.csv`) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **OUTPUT_LABEL** | DEL-10-02 |

## Resolved Paths

| Source | Resolved Path |
|---|---|
| Professional_Staff_Rates.csv | `_PriceSources/Professional_Staff_Rates.csv` |
| Level_of_Effort.csv | `_PriceSources/Level_of_Effort.csv` |
| Assumed_Project_Parameters.csv | `_PriceSources/Assumed_Project_Parameters.csv` |
| Decomposition | `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` |
| Dependencies | `PKG-010_.../DEL-10-02_.../Dependencies.csv` |

## CBS Mapping Rule

No explicit `CBSHint` was provided in the decomposition for DEL-10-02. CBS is assigned as follows:
- PM hours for site conditions summary and due diligence coordination: **CBS = GR-PM** (General Requirements -- Project Management)
- Civil Engineer (Senior) hours for technical review of site conditions reports: **CBS = GR-DESIGN** (General Requirements -- Design / Engineering)
- Geotechnical Engineer hours for existing report interpretation: **CBS = GR-DESIGN** (General Requirements -- Design / Engineering)

This mapping follows the convention that proposal production professional services fall under General Requirements CBS categories.

## Warnings

None.
