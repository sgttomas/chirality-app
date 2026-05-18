# Run Context

| Field | Value |
|---|---|
| RunID | EST_DEL-01-02_2026-02-18_0900 |
| AsOf | 2026-02-18T09:00:00-07:00 |
| Scope | DEL-01-02 (Baseline Schedule, Updates & Reporting) |
| ScopeResolvedSummary | 1 deliverable in scope; 0 excluded; 0 blocked |
| BASIS_OF_ESTIMATE | RATE_TABLE |
| CURRENCY | CAD |
| PRICE_SOURCES | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| DECOMPOSITION_PATH | _Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| DEPENDENCY_SOURCES | AUTO (read DEL-01-02/Dependencies.csv) |
| FALLBACK_POLICY | STRICT |
| ALLOW_MIXED_METHODS | FALSE |
| UPDATE_LATEST_POINTER | FALSE |
| Rounding | DOLLAR |
| OUTPUT_LABEL | DEL-01-02 |
| Warnings | [WARNING] Software/tools cost driver identified in brief but no pricing source available; line item set to TBD per STRICT fallback. |

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

No explicit CBSHint was provided in the decomposition. The following deterministic rule is applied:

- Deliverable substance = "Management" (from brief)
- Deliverable discipline = "Project controls" (from Datasheet.md)
- CBS assigned = `MGMT.PROJ_CONTROLS`

This rule is documented here for reproducibility. If a project-wide CBS taxonomy is established, this mapping should be revisited.

## Method Reconciliation

The `Level_of_Effort.csv` source declares its quantities with `Basis=PARAMETRIC`. However, the quantities (hours) are used here as **input quantities** to a rate-table calculation (Qty x UnitRate from `Professional_Staff_Rates.csv`). The pricing method is therefore `RATE_TABLE`, consistent with `BASIS_OF_ESTIMATE`. See Decision_Log.md DEC-EST-001.
