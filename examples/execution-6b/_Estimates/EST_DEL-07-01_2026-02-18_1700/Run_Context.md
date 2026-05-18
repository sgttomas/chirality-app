# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-07-01_2026-02-18_1700 |
| **AsOf** | 2026-02-18T17:00:00-07:00 |
| **Scope** | DEL-07-01 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (resolved: DEL-07-01/Dependencies.csv found; 15 dependency rows loaded) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-07-01 | PKG-007 | PKG-007_Construction_Methodology_and_Administration/1_Working/DEL-07-01_ConstructionMethodologyNarrative/ | TRUE | Construction Methodology Narrative; SOW-0019; OBJ-002 |

## CBS Mapping Rule

CBS codes are assigned using a deterministic rule based on the rate table `Category` column in `Professional_Staff_Rates.csv`:
- `Management` category roles -> CBS `MGMT`
- `Construction` category roles -> CBS `CONST`
- All roles for this deliverable map to one of these two categories.

## Pricing Method

Cost = SUM(EstimatedHours per role x HourlyRate_CAD per role), sourced from:
- Hours: `Level_of_Effort.csv` (filtered to Execution=6b, DeliverableID=DEL-07-01)
- Rates: `Professional_Staff_Rates.csv` (matched by RoleID)

## Cost Ownership Boundary

Per brief instructions:
- DEL-07-01 covers construction methodology framework: H&S plan, staging, permits/inspections, budget control, schedule control, communications, QA/QC framework.
- Construction administration (supervision, documents) belongs to DEL-07-02 and is NOT included here.
