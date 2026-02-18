# Run Context

## Run Identity

| Field | Value |
|---|---|
| RunID | EST_DEL-01-06_2026-02-18_1030 |
| AsOf | 2026-02-18T10:30:00-07:00 |
| AgentType | ESTIMATING (Type 2 Task Agent) |

## Scope

| Field | Value |
|---|---|
| Scope (as provided) | DEL-01-06 |
| ScopeResolvedSummary | 1 deliverable in scope; 0 excluded; 0 blocked |
| DeliverableID | DEL-01-06 |
| DeliverableName | Site Supervision, Logistics & Housekeeping |
| PackageID | PKG-001 |
| PackageName | General Requirements & Delivery Controls |
| DeliverablePath | PKG-001_General Requirements & Delivery Controls/1_Working/DEL-01-06_Site Supervision, Logistics & Housekeeping |

## Configuration

| Parameter | Value |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| CURRENCY | CAD |
| FALLBACK_POLICY | STRICT |
| ALLOW_MIXED_METHODS | FALSE |
| UPDATE_LATEST_POINTER | FALSE |
| ROUNDING | DOLLAR |
| OUTPUT_LABEL | DEL-01-06 |

## Resolved Paths

| Input | Resolved Path |
|---|---|
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a |
| ESTIMATES_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Estimates/ |
| DECOMPOSITION_PATH | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| DEPENDENCY_SOURCES | AUTO (resolved to: DEL-01-06/Dependencies.csv -- 8 rows; 8 ACTIVE) |
| PRICE_SOURCE_1 | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Professional_Staff_Rates.csv |
| PRICE_SOURCE_2 | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Level_of_Effort.csv |
| PRICE_SOURCE_3 | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Assumed_Project_Parameters.csv |

## CBS Mapping Rule

CBS codes are assigned deterministically based on Package and deliverable substance:
- PKG-001 management deliverables -> CBS `01-MGMT` (General Requirements -- Management Labor)
- PKG-001 construction management labor -> CBS `01-CMGT` (General Requirements -- Construction Management)
- Non-labor site costs (temp facilities, fencing, cleaning) -> CBS `01-SITE` (General Requirements -- Site General Costs)

This rule is applied to DEL-01-06 line items as follows:
- Site Superintendent labor: CBS `01-CMGT` (primary on-site construction management)
- Construction Manager labor: CBS `01-CMGT` (periodic site oversight / construction management)
- Temporary facilities/fencing: CBS `01-SITE` (non-labor site general costs)
- Site cleaning: CBS `01-SITE` (non-labor site general costs)

## Warnings

- [WARNING] Non-labor cost drivers (temporary facilities/fencing, site cleaning) identified in brief but no rate table evidence exists in PRICE_SOURCES. Per FALLBACK_POLICY=STRICT, these are recorded as TBD amounts. Rerun with appropriate rate table or change FALLBACK_POLICY to resolve.
