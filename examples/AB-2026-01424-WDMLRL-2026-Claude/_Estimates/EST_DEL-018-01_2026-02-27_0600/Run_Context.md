# Run Context — EST_DEL-018-01_2026-02-27_0600

## Run Identity

| Field | Value |
|-------|-------|
| **RunID** | EST_DEL-018-01_2026-02-27_0600 |
| **AsOf** | 2026-02-27T06:00:00-07:00 |
| **Scope** | DEL-018-01 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-018-01 — Topsoil Stripping) within PKG-018 (Sitework & Civil Construction) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-018-01 |

## Price Sources (Resolved)

| # | Path | Type |
|---|------|------|
| 1 | PriceSources/Professional_Staff_Rates.csv | Rate table (professional staff hourly rates) |
| 2 | PriceSources/Level_of_Effort.csv | Parametric (estimated hours by deliverable and role) |
| 3 | PriceSources/Assumed_Project_Parameters.csv | Parametric (project parameters and assumptions) |
| 4 | PriceSources/Earthwork_Civil_Rates.csv | Rate table (earthwork unit rates) |
| 5 | PriceSources/Paving_Surfacing_Rates.csv | Rate table (paving/surfacing unit rates) |
| 6 | PriceSources/Underground_Utility_Rates.csv | Rate table (underground utility unit rates) |
| 7 | PriceSources/Construction_Labour_Rates.csv | Rate table (construction trade labour rates) |

All price source paths are relative to:
`{RUN_ROOT}/_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/`

## Decomposition

| Field | Value |
|-------|-------|
| **DECOMPOSITION_PATH** | `{RUN_ROOT}/_Decomposition/WDMLRL_Decomposition_Claude.md` |
| **Package** | PKG-018 — Sitework & Civil Construction |
| **Deliverable** | DEL-018-01 — Topsoil Stripping |
| **SOW Reference** | SOW-0075 |
| **Objective** | OBJ-001 |

## Deliverable Documents Read

| Document | Status | Path |
|----------|--------|------|
| _CONTEXT.md | Read | `PKG-018_Sitework & Civil Construction/1_Working/DEL-018-01_Topsoil-Strip/_CONTEXT.md` |
| Datasheet.md | Read | `PKG-018_Sitework & Civil Construction/1_Working/DEL-018-01_Topsoil-Strip/Datasheet.md` |
| Specification.md | Read | `PKG-018_Sitework & Civil Construction/1_Working/DEL-018-01_Topsoil-Strip/Specification.md` |
| Guidance.md | Read | `PKG-018_Sitework & Civil Construction/1_Working/DEL-018-01_Topsoil-Strip/Guidance.md` |
| Procedure.md | Read | `PKG-018_Sitework & Civil Construction/1_Working/DEL-018-01_Topsoil-Strip/Procedure.md` |

## Warnings

- **[W-001]** Topsoil stripping area (m2) is TBD pending site survey (SURVEY-001) and IFC drawings (DEL-005-02). A parametric assumption of 3,500 m2 has been used for pricing purposes (see Assumptions_Log.md, ASM-002).
- **[W-002]** Topsoil depth is TBD pending site survey (SURVEY-001). A parametric assumption of 200 mm average depth has been used (see Assumptions_Log.md, ASM-003).
- **[W-003]** Several items priced as ALLOWANCE under FALLBACK_POLICY = ALLOW_PARAMETRIC due to insufficient rate evidence for lump-sum activities.
