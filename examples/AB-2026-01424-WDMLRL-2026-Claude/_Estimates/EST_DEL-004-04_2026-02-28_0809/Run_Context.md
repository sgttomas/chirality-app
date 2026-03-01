# Run Context — EST_DEL-004-04_2026-02-28_0809

| Field | Value |
|---|---|
| **RunID** | EST_DEL-004-04_2026-02-28_0809 |
| **AsOf** | 2026-02-28T08:09:00-07:00 |
| **Scope** | DEL-004-04 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-004-04 Lighting Plans) in PKG-004 Electrical Design |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Professional_Design_Fees.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-004-04 |
| **PriorSnapshot** | EST_DEL-004-04_2026-02-27_0630 |

## Resolved Price Source Paths

1. `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`
2. `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`
3. `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`
4. `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv`

## Deliverable Context

| Field | Value |
|---|---|
| Deliverable ID | DEL-004-04 |
| Name | Lighting Plans |
| Package | PKG-004 Electrical Design |
| Discipline | Electrical Engineering |
| Type | Drawing Set |
| Responsible | Electrical Engineer |
| Covers SOW | SOW-0014 |
| Supports Objectives | OBJ-001, OBJ-003, OBJ-005 |

## Changes from Prior Snapshot

| Change | Description |
|---|---|
| Resolved 6 hardware TBDs | DL-005 through DL-010 set to $0 (hardware cost in PKG-015 Electrical Installation scope, not PKG-004 design). SourceRef updated to Decision_Log DEC-R01. Confidence upgraded from LOW to MED. |
| DL-010 unit clarified | Changed from TBD EA to 1 LS at $0 (lump-sum reference placeholder; fixture count still TBD per CONF-LT-002). |
| DL-015 notes updated | Added conditional allowance note: ~$5,800 carried in project notes pending code review (CONF-LT-003). Amount remains TBD. |
| TBD count reduced | 7 TBDs reduced to 1 residual TBD (DL-015 emergency/exit lighting). |

## Warnings

- 1 residual TBD: DL-015 (emergency/exit lighting assessment) remains unpriced pending CONF-LT-003 resolution.
