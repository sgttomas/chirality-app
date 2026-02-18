# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-07-04_2026-02-18_2355 |
| **AsOf** | 2026-02-18T23:55:00-07:00 |
| **Scope** | DEL-07-04 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-07-04/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Scope Resolution

| DeliverableID | PackageID | Path | InScope |
|---|---|---|---|
| DEL-07-04 | PKG-007 | test/execution-6b/PKG-007_Construction_Methodology_and_Administration/1_Working/DEL-07-04_MeetingsAndReportingNarrative/ | TRUE |

## CBS Mapping Rule

No explicit CBSHint was provided in the decomposition for DEL-07-04. CBS is assigned as follows:
- Professional staff hours (PM, Construction Manager) -> `CBS-01-PROF` (Professional Services / Staff Time)

This mapping is deterministic: all Level_of_Effort line items for proposal-stage narrative deliverables are classified under professional services.

## Pricing Approach

- **Hours** sourced from `Level_of_Effort.csv` (rows filtered to `DeliverableID=DEL-07-04`)
- **Rates** sourced from `Professional_Staff_Rates.csv` (matched by `RoleID`)
- **Method** = RATE_TABLE (hours x rate)
- No parametric models, allowances, or quotes used
- No fallback was required (all line items priced from basis evidence)
