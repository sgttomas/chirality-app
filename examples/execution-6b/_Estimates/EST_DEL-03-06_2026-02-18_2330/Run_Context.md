# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-03-06_2026-02-18_2330 |
| **AsOf** | 2026-02-18T23:30:00 |
| **Scope** | DEL-03-06 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | /test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-03-06/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Resolved Paths

- **Rate table:** `/test/execution-6b/_PriceSources/Professional_Staff_Rates.csv`
- **Level of effort:** `/test/execution-6b/_PriceSources/Level_of_Effort.csv`
- **Project parameters:** `/test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv`
- **Decomposition:** `/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md`
- **Dependencies:** `/test/execution-6b/PKG-003_Design_Brief/1_Working/DEL-03-06_AccessibilityAndAdaptabilityNarrative/Dependencies.csv`

## CBS Mapping Rule

No explicit `CBSHint` is present in the decomposition for DEL-03-06. CBS is assigned deterministically based on deliverable type:

- Deliverable Type = "Design Brief / Narrative" --> CBS = `DESIGN_BRIEF`

This rule is applied consistently across all Design Brief package deliverables in execution-6b.

## Pricing Method

`BASIS_OF_ESTIMATE = RATE_TABLE`. Hours are sourced from `Level_of_Effort.csv` (column `EstimatedHours`), rates from `Professional_Staff_Rates.csv` (column `HourlyRate_CAD`). Each line item computes `Amount = Qty (hours) x UnitRate ($/hr)`, rounded to the nearest whole dollar per `ROUNDING = DOLLAR`.
