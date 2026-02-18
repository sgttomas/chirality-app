# Run Context

## Run Identity

| Field | Value |
|---|---|
| RunID | EST_DEL-01-05_2026-02-18_0000 |
| AsOf | 2026-02-18T00:00:00-07:00 |
| Agent | ESTIMATING (Type 2) |

## Scope

| Field | Value |
|---|---|
| Scope (as provided) | DEL-01-05 |
| ScopeResolvedSummary | 1 deliverable in scope; 0 excluded; 0 blocked |
| Deliverable | DEL-01-05 Meetings, Documentation & Change Control |
| Package | PKG-001 General Requirements & Delivery Controls |
| Tier | T0 (no upstream cost dependencies) |
| Substance | Management |

## Basis and Controls

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| CURRENCY | CAD |
| FALLBACK_POLICY | STRICT |
| ALLOW_MIXED_METHODS | FALSE |
| UPDATE_LATEST_POINTER | FALSE |
| ROUNDING | DOLLAR |
| OUTPUT_LABEL | DEL-01-05 |

## Resolved Paths

| Input | Resolved Path |
|---|---|
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a |
| ESTIMATES_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Estimates/ |
| DECOMPOSITION_PATH | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| DEPENDENCY_SOURCES | AUTO (resolved to: DEL-01-05 Dependencies.csv, 11 rows) |
| PRICE_SOURCES[1] | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Professional_Staff_Rates.csv |
| PRICE_SOURCES[2] | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Level_of_Effort.csv |
| PRICE_SOURCES[3] | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Assumed_Project_Parameters.csv |

## EXCLUSIONS (not ingested as pricing sources)

- `_Estimates/**`
- `_Aggregation/**`
- `_Reconciliation/**`
- `_Archive/**`

## CBS Mapping Rule

CBS codes are assigned deterministically based on the role Category field from Professional_Staff_Rates.csv:

| Role Category | CBS Code |
|---|---|
| Management | PM (Project Management) |
| Administrative | ADMIN (Administrative / Document Control) |

This rule is documented here and applied consistently in Detail.csv.

## Warnings

- None.
