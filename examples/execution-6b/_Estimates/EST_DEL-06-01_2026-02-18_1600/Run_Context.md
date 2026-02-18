# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-06-01_2026-02-18_1600 |
| **AsOf** | 2026-02-18T16:00:00 |
| **Scope** | DEL-06-01 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-06-01/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Scope Resolution

| DeliverableID | PackageID | Path | InScope |
|---|---|---|---|
| DEL-06-01 | PKG-006 | PKG-006_Delivery_Plan/1_Working/DEL-06-01_DesignMethodologyNarrative/ | TRUE |

## CBS Mapping Rule

CBS codes are derived deterministically from the `Category` column in `Professional_Staff_Rates.csv`:
- Category "Management" -> CBS = `MGMT`
- Category "Design" -> CBS = `DESIGN`
- Category "Production" -> CBS = `PROD`
- Category "Construction" -> CBS = `CONSTR`
- Category "Financial" -> CBS = `FIN`
- Category "Administrative" -> CBS = `ADMIN`
- Category "Legal" -> CBS = `LEGAL`
- Category "Specialty" -> CBS = `SPEC`
- Category "External" -> CBS = `EXT`

For DEL-06-01, both roles (R-03 Design Manager = Management, R-02 Project Manager = Management) map to CBS = `MGMT`.

## Pricing Method

Cost = Hours (from Level_of_Effort.csv) x HourlyRate_CAD (from Professional_Staff_Rates.csv), per role, per deliverable. This is a RATE_TABLE method: the rate table provides unit rates and the level-of-effort table provides quantities.
