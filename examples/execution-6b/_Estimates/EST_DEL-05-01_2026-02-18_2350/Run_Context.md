# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-05-01_2026-02-18_2350 |
| **AsOf** | 2026-02-18T23:50:00-07:00 |
| **Scope** | DEL-05-01 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-05-01/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Scope Resolution

| DeliverableID | PackageID | Path | InScope |
|---|---|---|---|
| DEL-05-01 | PKG-005 | PKG-005_Building_Durability_and_Maintenance/1_Working/DEL-05-01_ArchitecturalDurabilityAndMaintenance/ | TRUE |

## Pricing Method

Basis is RATE_TABLE. Hours are sourced from `Level_of_Effort.csv` (column `EstimatedHours`, filtered to `Execution=6b` and `DeliverableID=DEL-05-01`). Hourly rates are sourced from `Professional_Staff_Rates.csv` (column `HourlyRate_CAD`, joined on `RoleID`). Amount = Hours x Rate, rounded to nearest dollar per ROUNDING=DOLLAR.

## CBS Mapping Rule

No explicit `CBSHint` is present in the decomposition for DEL-05-01. CBS is assigned deterministically as follows:
- Professional services labour for narrative production -> `CBS-100` (Professional Fees / Design Services)

This mapping is recorded here as the authoritative rule for this run. If the project later defines a formal CBS dictionary, future runs should adopt it.
