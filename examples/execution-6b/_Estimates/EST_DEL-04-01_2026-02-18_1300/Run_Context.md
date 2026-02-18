# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-04-01_2026-02-18_1300 |
| **AsOf** | 2026-02-18T13:00:00-07:00 |
| **Scope** | DEL-04-01 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-04-01/Dependencies.csv; 15 rows loaded) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |

## Resolved Paths

- **ESTIMATES_ROOT:** `test/execution-6b/_Estimates/`
- **Deliverable path:** `test/execution-6b/PKG-004_Sustainability_and_Energy/1_Working/DEL-04-01_BuildingEnvelopeAndEnergyStrategy/`
- **Rate table:** `test/execution-6b/_PriceSources/Professional_Staff_Rates.csv` (30 roles; R-01 through R-30)
- **Level of effort:** `test/execution-6b/_PriceSources/Level_of_Effort.csv` (73 rows total; 2 rows for DEL-04-01)
- **Project parameters:** `test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv` (29 parameters; used for context only)

## CBS Mapping Rule

No explicit `CBSHint` found in decomposition for DEL-04-01. CBS assigned as `PROF_SERVICES` using the following deterministic rule: all deliverables of Type "Sustainability / Narrative" under PKG-004 whose cost is composed entirely of professional consulting hours are mapped to CBS = `PROF_SERVICES`.

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-04-01 | PKG-004 | PKG-004_Sustainability_and_Energy/1_Working/DEL-04-01_BuildingEnvelopeAndEnergyStrategy/ | TRUE | Building Envelope & Energy Strategy (T2, Narrative) |

## Warnings

None.
