# Run Context — EST_DEL-008-01_2026-02-26_2232

| Field | Value |
|-------|-------|
| **RunID** | EST_DEL-008-01_2026-02-26_2232 |
| **AsOf** | 2026-02-26T22:32:00-07:00 |
| **Scope** | DEL-008-01 (Geotech Investigation) |
| **ScopeResolvedSummary** | 1 deliverable in 1 package (PKG-008) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE |
| **OUTPUT_LABEL** | DEL-008-01 |

## Resolved Paths

- **RUN_ROOT:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude`
- **ESTIMATES_ROOT:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Estimates`
- **Snapshot:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Estimates/EST_DEL-008-01_2026-02-26_2232`
- **Deliverable folder:** `PKG-008_Geotechnical Investigation & Surveying/1_Working/DEL-008-01_Geotech-Investigation`

## Price Sources (resolved)

| Source File | Source Type | Notes |
|-------------|-----------|-------|
| `Professional_Staff_Rates.csv` | Rate Table (parametric) | 25 roles with hourly rates in CAD; Confidence MEDIUM |
| `Level_of_Effort.csv` | Parametric model (hours by role by deliverable) | DEL-008-01 has 2 rows: PM (6 hr), Cost Estimator (4 hr); no Geotechnical Engineer hours provided |
| `Assumed_Project_Parameters.csv` | Parametric parameters | 18 project parameters; currency CAD |

## Documents Read

| Document | Status |
|----------|--------|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |
| Decomposition (PKG-008 section) | Read |

## Warnings

- **W-001**: Level_of_Effort.csv provides only PM (6 hr) and Cost Estimator (4 hr) for DEL-008-01. No hours are provided for Geotechnical Engineer (R-20), Surveyor (R-21), or any field/lab roles. The major cost components of this deliverable (field investigation, laboratory testing, report preparation by geotechnical engineer) have no level-of-effort basis in the provided price sources.
- **W-002**: No subcontractor or equipment rates are provided in PRICE_SOURCES. Geotechnical field investigation typically requires drill rig mobilization, drilling crew, and laboratory testing — none of which are covered by Professional_Staff_Rates.csv (which covers professional staff only).
- **W-003**: Multiple quantities in the deliverable documents are TBD (borehole count, investigation depth, lab test count, etc.). These are to be determined by the Geotechnical Engineer and are not available for pricing.
