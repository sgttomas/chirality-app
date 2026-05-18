# Run Context — EST_DEL-018-02_2026-02-27_0730

## Run Identity

| Field | Value |
|-------|-------|
| **RunID** | EST_DEL-018-02_2026-02-27_0730 |
| **AsOf** | 2026-02-27T07:30:00-07:00 |
| **Agent** | ESTIMATING (Type 2) |

## Scope

| Field | Value |
|-------|-------|
| **Scope** | DEL-018-02 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-018-02: Site Grading & Landscaping) in PKG-018 (Sitework & Civil Construction) |
| **Deliverable Name** | Site Grading & Landscaping |
| **Package** | PKG-018 — Sitework & Civil Construction |
| **SOW Reference** | SOW-0076: "Grade and landscape the proposed lot" |
| **Responsible Party** | General Contractor |
| **Type** | Construction |

## Configuration

| Parameter | Value |
|-----------|-------|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **OUTPUT_LABEL** | DEL-018-02 |
| **Rounding** | NONE (default) |

## Price Sources (Resolved)

1. `Professional_Staff_Rates.csv` — Professional staff hourly rates (25 roles), PARAMETRIC basis
2. `Level_of_Effort.csv` — Level of effort hours by deliverable and role, PARAMETRIC basis
3. `Assumed_Project_Parameters.csv` — Project parameters (18 entries), CONFIRMED/DERIVED/ASSUMPTION basis
4. `Earthwork_Civil_Rates.csv` — Earthwork unit rates (4 items), PARAMETRIC basis
5. `Paving_Surfacing_Rates.csv` — Paving and surfacing unit rates (4 items), PARAMETRIC basis
6. `Underground_Utility_Rates.csv` — Underground utility unit rates (5 items), PARAMETRIC/ALLOWANCE basis
7. `Construction_Labour_Rates.csv` — Trade labour rates (10 trades), PARAMETRIC basis

All sources located under: `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/`

## Decomposition

| Field | Value |
|-------|-------|
| **DECOMPOSITION_PATH** | `_Decomposition/WDMLRL_Decomposition_Claude.md` |
| **WBS_PackageID** | PKG-018 |
| **WBS_DeliverableID** | DEL-018-02 |

## Warnings

- Multiple TBD quantities in deliverable documents: grading elevations, grading slopes, and landscape scope are all TBD pending upstream design deliverables (DEL-005-02, DEL-007-02, DEL-007-03).
- Landscape species, areas, and quantities cannot be priced from available sources; PARAMETRIC allowance applied.
- Compaction acceptance criteria are TBD pending civil specification (DEL-005-07).
- Fine grading tolerances are TBD pending civil specification (DEL-005-07).
- No specific grading area quantity (m2) is stated in the deliverable documents; area is estimated parametrically from project parameters (PP-10: ~13,000 sqft addition footprint, with assumed site grading area of approximately 2,500 m2 for the expansion lot).
