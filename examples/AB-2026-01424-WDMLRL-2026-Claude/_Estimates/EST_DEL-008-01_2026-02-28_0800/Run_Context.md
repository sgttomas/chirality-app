# Run Context — EST_DEL-008-01_2026-02-28_0800

| Field | Value |
|-------|-------|
| **RunID** | EST_DEL-008-01_2026-02-28_0800 |
| **AsOf** | 2026-02-28T08:00:00-07:00 |
| **Scope** | DEL-008-01 (Geotech Investigation) |
| **ScopeResolvedSummary** | 1 deliverable in 1 package (PKG-008); 26 items, 26 detail lines |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Geotechnical_Investigation_Rates.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE |
| **OUTPUT_LABEL** | DEL-008-01 |

## Prior Snapshot

| Field | Value |
|-------|-------|
| **Prior RunID** | EST_DEL-008-01_2026-02-26_2232 |
| **Prior Status** | WARNINGS (21 of 23 lines TBD; $1,530 CAD priced) |
| **Change Summary** | All 21 TBD lines resolved; 3 new items added; total now $46,130 CAD |

## Resolved Paths

- **RUN_ROOT:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude`
- **ESTIMATES_ROOT:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Estimates`
- **Snapshot:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Estimates/EST_DEL-008-01_2026-02-28_0800`
- **Prior Snapshot:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Estimates/EST_DEL-008-01_2026-02-26_2232`
- **Deliverable folder:** `PKG-008_Geotechnical Investigation & Surveying/1_Working/DEL-008-01_Geotech-Investigation`

## Price Sources (resolved)

| Source File | Source Type | Notes |
|-------------|-----------|-------|
| `Professional_Staff_Rates.csv` | Rate Table (parametric) | 25 roles with hourly rates in CAD; Confidence MEDIUM; R-20 Geotech Engineer $175/hr used for project team items |
| `Level_of_Effort.csv` | Parametric model (hours by role by deliverable) | DEL-008-01 has 3 rows: PM (6 hr), Cost Estimator (4 hr), Geotechnical Engineer (60 hr: 16 program dev + 24 field supervision + 20 analysis/review) |
| `Assumed_Project_Parameters.csv` | Parametric parameters | 18 project parameters; currency CAD |
| `Geotechnical_Investigation_Rates.csv` | Rate Table (parametric) | 15 rows (GI-01..GI-15); Alberta 2026 geotechnical investigation rates for drilling, lab testing, professional services, mobilization, restoration |

## Documents Read

| Document | Status |
|----------|--------|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |
| Decomposition (PKG-008 section) | Read |
| Prior estimate EST_DEL-008-01_2026-02-26_2232 | Read (Items.csv, Detail.csv, all supporting files) |

## Changes from Prior Snapshot

1. **New price source:** Geotechnical_Investigation_Rates.csv (15 rows GI-01..GI-15) now available, resolving the critical gap identified in the prior snapshot (W-002).
2. **New LOE data:** Level_of_Effort.csv now includes R-20 Geotechnical Engineer at 60 hours for DEL-008-01, resolving W-001.
3. **21 TBD lines resolved:** All previously TBD lines (L-003 through L-023) now have quantities, unit rates, and amounts.
4. **3 new items added:** ITEM-024 (consolidation/oedometer), ITEM-025 (direct shear/triaxial), ITEM-026 (chemical analysis) — specialized lab tests identified during pricing that were not in the original takeoff.
5. **Investigation program quantified:** 4 boreholes to 10m, 3 test pits, 1 monitoring well, 25 soil samples, 3-day field program.
