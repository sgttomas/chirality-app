# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-08-01_2026-02-18_2359 |
| **AsOf** | 2026-02-18T23:59:00-07:00 |
| **Scope** | DEL-08-01 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | `test/execution-6b/_PriceSources/Professional_Staff_Rates.csv`, `test/execution-6b/_PriceSources/Level_of_Effort.csv`, `test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv` |
| **DECOMPOSITION_PATH** | `test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO -- read `DEL-08-01_CommissioningTrainingCloseoutNarrative/Dependencies.csv` (15 rows loaded) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **OUTPUT_LABEL** | DEL-08-01 |
| **Warnings** | None |

## Scope Resolution

| DeliverableID | PackageID | Path | InScope |
|---|---|---|---|
| DEL-08-01 | PKG-008 | `test/execution-6b/PKG-008_Commissioning_Closeout_and_Warranty/1_Working/DEL-08-01_CommissioningTrainingCloseoutNarrative/` | TRUE |

## CBS Mapping Rule

CBS codes are assigned deterministically based on the Professional_Staff_Rates.csv `Category` field:
- `Management` category roles -> CBS `MGMT` (management / coordination labor)
- `Construction` category roles -> CBS `CX` (commissioning labor)

This mapping is specific to DEL-08-01 where the cost drivers are commissioning lead hours and PM coordination hours.

## Pricing Approach

- **Hours** sourced from `Level_of_Effort.csv` (rows where `DeliverableID = DEL-08-01`)
- **Rates** sourced from `Professional_Staff_Rates.csv` (matched by `RoleID`)
- **Method** = `RATE_TABLE` for all line items (hours x hourly rate)
- **Rounding** = DOLLAR (amounts rounded to nearest whole dollar)
