# Run Context — EST_DEL-008-02_2026-02-26_2232

| Field | Value |
|---|---|
| **RunID** | EST_DEL-008-02_2026-02-26_2232 |
| **AsOf** | 2026-02-26T22:32:00 |
| **Scope** | DEL-008-02 (Preliminary Survey) |
| **ScopeResolvedSummary** | 1 deliverable: DEL-008-02 in PKG-008 (Geotechnical Investigation & Surveying) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE |
| **OUTPUT_LABEL** | DEL-008-02 |

## Resolved Paths

| Source | Absolute Path |
|---|---|
| Professional_Staff_Rates.csv | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` |
| Level_of_Effort.csv | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` |
| Assumed_Project_Parameters.csv | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` |
| Deliverable Folder | `PKG-008_Geotechnical Investigation & Surveying/1_Working/DEL-008-02_Preliminary-Survey/` |
| Decomposition | `_Decomposition/WDMLRL_Decomposition_Claude.md` |

## Warnings

- Level_of_Effort.csv provides hours for R-01 (Project Manager, 6 hr) and R-08 (Cost Estimator, 4 hr) only for DEL-008-02. Surveyor (R-21) hours are listed as TBD in the source notes. Surveyor effort has been estimated parametrically per FALLBACK_POLICY=ALLOW_PARAMETRIC.
- Multiple Datasheet attributes are TBD (horizontal datum, vertical datum, coordinate system, survey accuracy class, mapping scale/contour interval, control point count). These do not affect the cost estimate structure but indicate scope definition is incomplete.
