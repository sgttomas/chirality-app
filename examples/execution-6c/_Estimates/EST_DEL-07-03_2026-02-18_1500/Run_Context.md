# Run Context — EST_DEL-07-03_2026-02-18_1500

| Field | Value |
|-------|-------|
| **RunID** | EST_DEL-07-03_2026-02-18_1500 |
| **AsOf** | 2026-02-18T15:00:00-07:00 |
| **Scope** | DEL-07-03 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 1 resolved; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | `_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md` (FOUND) |
| **DEPENDENCY_SOURCES** | AUTO (read `Dependencies.csv` from DEL-07-03 deliverable folder) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

---

## Resolved Paths

| Item | Path |
|------|------|
| RUN_ROOT | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c` |
| ESTIMATES_ROOT | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Estimates` |
| Snapshot | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Estimates/EST_DEL-07-03_2026-02-18_1500/` |
| Decomposition | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md` |
| DEL-07-03 folder | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-03_Team Qualifications (Appendix I + resumes)/1_Working/DEL-07-03_AppendixI_SubtradeAndConsultantList/` |
| Dependencies.csv | `{DEL-07-03 folder}/Dependencies.csv` |
| Professional_Staff_Rates.csv | `_PriceSources/Professional_Staff_Rates.csv` |
| Level_of_Effort.csv | `_PriceSources/Level_of_Effort.csv` |
| Assumed_Project_Parameters.csv | `_PriceSources/Assumed_Project_Parameters.csv` |

---

## BOE Context (from brief)

- **Name:** Appendix I -- Subtrade & Consultant List
- **Tier:** T3
- **Substance:** Administrative
- **Cost Drivers:** PM hours; subtrade/consultant procurement coordination; Appendix I form completion. Depends on DEL-02-01 (concept informs required specialties) and DEL-05-02 (pricing scopes must align).
- **Cost Ownership:** Subtrade/consultant list compilation belongs here. Firm experience narrative is in DEL-07-01. Resume assembly is in DEL-07-02. Subconsultant APPROACH is in DEL-04-03; the LIST is here.
- **Package:** PKG-03 -- Team Qualifications (Appendix I + resumes)

---

## CBS Mapping Rule

DEL-07-03 is an administrative deliverable (Appendix I form completion). CBS assigned as `PROPOSAL_PRODUCTION.ADMIN` based on deliverable substance = Administrative and the BOE classification of proposal production costs.

---

## Defaults Applied

- `OUTPUT_LABEL`: EST_DEL-07-03 (from brief)
- `RUN_TIMESTAMP`: 2026-02-18T15:00:00 (generated)
- `DEPENDENCY_SOURCES`: AUTO -- resolved to DEL-07-03 deliverable folder Dependencies.csv
- `ROUNDING`: DOLLAR -- amounts rounded to nearest dollar
