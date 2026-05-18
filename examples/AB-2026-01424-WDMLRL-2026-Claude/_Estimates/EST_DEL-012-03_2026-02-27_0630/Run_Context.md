# Run Context — EST_DEL-012-03_2026-02-27_0630

## Run Identity

| Field | Value |
|---|---|
| RunID | EST_DEL-012-03_2026-02-27_0630 |
| AsOf | 2026-02-27T06:30:00-07:00 |
| Scope | DEL-012-03 |
| ScopeResolvedSummary | 1 deliverable (DEL-012-03 Office Space) in PKG-012 Interior Construction & Fit-Out |
| BASIS_OF_ESTIMATE | PARAMETRIC |
| CURRENCY | CAD |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| UPDATE_LATEST_POINTER | FALSE |
| Rounding | NONE (default) |
| OUTPUT_LABEL | DEL-012-03 |

## Price Sources (Resolved)

| # | Path | Type | Notes |
|---|---|---|---|
| 1 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | Rate Table (parametric) | 25 professional roles with hourly CAD rates |
| 2 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | Parametric LOE model | Estimated hours by role per deliverable; 6 rows for DEL-012-03 |
| 3 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` | Parametric parameters | 19 project parameters (facility area, ceiling height, equipment, etc.) |
| 4 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Interior_Architectural_Rates.csv` | Rate Table (parametric) | 5 interior fit-out unit rates (partitions, paint, ceilings, flooring, millwork) |
| 5 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Construction_Labour_Rates.csv` | Rate Table (parametric) | 10 construction trade fully-burdened hourly rates |

## Decomposition Path

`_Decomposition/WDMLRL_Decomposition_Claude.md` — used for WBS traceability (PKG-012, DEL-012-03, SOW-0031)

## Deliverable Path

`PKG-012_Interior Construction & Fit-Out/1_Working/DEL-012-03_Office/`

## Documents Read

| Document | Status |
|---|---|
| _CONTEXT.md | Read |
| Datasheet.md | Read (R2 — SEMANTIC_READY) |
| Specification.md | Read (R2 — SEMANTIC_READY) |
| Guidance.md | Read (R2 — SEMANTIC_READY) |
| Procedure.md | Read (R2 — SEMANTIC_READY) |

## Warnings

- Office floor area is TBD (not dimensioned on conceptual drawings). Parametric area-based items use an assumed 25 m2 (~269 sq ft) office footprint derived from building context (see Assumptions_Log.md ASM-001).
- Scope boundary between PKG-012 and PKG-015 for electrical rough-in / device installation is unresolved (CONF-001). Items related to electrical device installation are included here as PKG-012 scope per _CONTEXT.md but flagged.
- Multiple finish specifications (flooring type, ceiling type, drywall finish level) are TBD pending IFC design.
- Door quantity and type TBD pending IFC door/window schedule; assumed 1 EA standard interior door per conceptual plan.
