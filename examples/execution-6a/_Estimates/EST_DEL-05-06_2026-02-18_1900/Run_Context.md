# Run Context

## Run Identity

- **RunID:** EST_DEL-05-06_2026-02-18_1900
- **AsOf:** 2026-02-18T19:00:00-07:00
- **AgentType:** ESTIMATING (Type 2)

## Scope

- **Scope (as provided):** DEL-05-06 only (PKG-005)
- **ScopeResolvedSummary:** 1 deliverable in scope; 0 excluded; 0 blocked

## Configuration

| Parameter | Value |
|---|---|
| BASIS_OF_ESTIMATE | QUOTE |
| CURRENCY | CAD |
| FALLBACK_POLICY | STRICT |
| ALLOW_MIXED_METHODS | FALSE |
| UPDATE_LATEST_POINTER | FALSE |
| ROUNDING | DOLLAR |
| OUTPUT_LABEL | DEL-05-06 |

## Resolved Paths

| Input | Resolved Path |
|---|---|
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a |
| ESTIMATES_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Estimates/ |
| DECOMPOSITION_PATH | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| DEPENDENCY_SOURCES | AUTO (resolved: PKG-005/.../DEL-05-06_.../Dependencies.csv -- 10 rows) |

## PRICE_SOURCES (resolved)

1. `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Optional_Items_Pricing.csv` -- Appliance line items OPT-12 through OPT-17; labeled PARAMETRIC basis in source; treated as QUOTE per brief guidance (see Decision_Log.md DEC-EST-001).
2. `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Assumed_Project_Parameters.csv` -- Project parameters reference (not used for pricing; quantities confirmed only).

## CBS Mapping Rule

No explicit `CBSHint` was provided in the decomposition for DEL-05-06. CBS codes are assigned deterministically as follows:
- Equipment purchase line items: `CBS-EQP` (Equipment Purchase)
- Installation/connection line items: `CBS-INST` (Installation & Connection)

## Warnings

- None critical. See Decision_Log.md for method-classification decision (DEC-EST-001).
