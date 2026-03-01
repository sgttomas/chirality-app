# Run Context — EST_DEL-008-03_2026-02-27_0630

| Field | Value |
|---|---|
| **RunID** | EST_DEL-008-03_2026-02-27_0630 |
| **AsOf** | 2026-02-27T06:30:00-07:00 |
| **Scope** | DEL-008-03 (Construction Survey) |
| **ScopeResolvedSummary** | 1 deliverable: DEL-008-03 in PKG-008 (Geotechnical Investigation & Surveying) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE |
| **OUTPUT_LABEL** | DEL-008-03 |

## Resolved Paths

| Source | Absolute Path |
|---|---|
| Professional_Staff_Rates.csv | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` |
| Level_of_Effort.csv | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` |
| Assumed_Project_Parameters.csv | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` |
| Deliverable Folder | `PKG-008_Geotechnical Investigation & Surveying/1_Working/DEL-008-03_Construction-Survey/` |
| Decomposition | `_Decomposition/WDMLRL_Decomposition_Claude.md` |

## Warnings

- Level_of_Effort.csv provides hours for R-01 (Project Manager, 6 hr) and R-08 (Cost Estimator, 4 hr) only for DEL-008-03. Surveyor (R-21) hours are not provided in the Level_of_Effort source (Notes column shows "PKG-008 TBD — TBD"). Surveyor effort has been estimated parametrically per FALLBACK_POLICY=ALLOW_PARAMETRIC.
- Construction survey is substantially larger in scope than preliminary survey (DEL-008-02) — it covers multiple construction phases, repeated site visits, and 17 procedural steps across 4 phases. Parametric hours are estimated at approximately 3x the preliminary survey effort to reflect this expanded scope.
- Multiple Datasheet attributes are TBD (geodetic datum, map projection, vertical datum, accuracy tolerances). These do not affect the cost estimate structure but indicate scope definition is incomplete pending Surveyor confirmation.
- Foundation staking may require re-staking after geotech-informed foundation design is finalized (RFP §4.8.2). No contingency for re-staking is included; this is flagged as a risk.
