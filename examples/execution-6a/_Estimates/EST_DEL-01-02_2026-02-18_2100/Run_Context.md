# Run Context

| Field | Value |
|---|---|
| RunID | EST_DEL-01-02_2026-02-18_2100 |
| AsOf | 2026-02-18T21:00:00-07:00 |
| PriorRunID | EST_DEL-01-02_2026-02-18_0900 |
| RevisionType | TBD resolution pass (ORCHESTRATOR-directed) |
| Scope | DEL-01-02 (Baseline Schedule, Updates & Reporting) |
| ScopeResolvedSummary | 1 deliverable in scope; 0 excluded; 0 blocked |
| BASIS_OF_ESTIMATE | RATE_TABLE |
| CURRENCY | CAD |
| PRICE_SOURCES | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| DECOMPOSITION_PATH | _Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| DEPENDENCY_SOURCES | AUTO (read DEL-01-02/Dependencies.csv) |
| FALLBACK_POLICY | STRICT (overridden to ALLOW_ALLOWANCE for TBD resolution per human authorization) |
| ALLOW_MIXED_METHODS | TRUE (RATE_TABLE + ALLOWANCE; authorized by human for TBD resolution) |
| UPDATE_LATEST_POINTER | FALSE |
| Rounding | DOLLAR |
| OUTPUT_LABEL | DEL-01-02 |

## Revision Notes

This snapshot revises EST_DEL-01-02_2026-02-18_0900 to resolve 1 TBD line item. The prior run applied STRICT fallback, leaving L-003 (scheduling software/tools) at TBD. The human authorized ORCHESTRATOR to resolve TBDs using parametric allowances where no rate table evidence exists.

**Changes from prior run:**
- L-003: TBD → $3,500 CAD (ALLOWANCE method; parametric estimate for scheduling software license)
- ALLOW_MIXED_METHODS changed from FALSE to TRUE (RATE_TABLE + ALLOWANCE now present)
- Total changed from $13,900 → $17,400

## Resolved Paths

| Input | Resolved Path |
|---|---|
| ESTIMATES_ROOT | {RUN_ROOT}/_Estimates/ |
| Decomposition | {RUN_ROOT}/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| Rate Table | {RUN_ROOT}/_PriceSources/Professional_Staff_Rates.csv |
| Level of Effort | {RUN_ROOT}/_PriceSources/Level_of_Effort.csv |
| Project Parameters | {RUN_ROOT}/_PriceSources/Assumed_Project_Parameters.csv |
| Dependencies | {RUN_ROOT}/PKG-001_.../DEL-01-02_.../Dependencies.csv |

## CBS Mapping Rule

Carried forward from prior run. CBS = `MGMT.PROJ_CONTROLS` for all lines.

## Method Reconciliation

L-001 and L-002 remain RATE_TABLE (LOE quantities × rate table unit rates). L-003 is now ALLOWANCE (parametric estimate, no rate table evidence). Mixed methods authorized by human for this TBD resolution pass.
