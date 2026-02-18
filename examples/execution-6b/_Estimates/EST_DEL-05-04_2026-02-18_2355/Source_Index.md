# Source Index

## Pricing Sources

| # | Source File | Source Type | Used For | Parsing Notes |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | Hourly rates by RoleID; R-13 = $155 CAD/hr | CSV with headers; 30 roles; all rates in CAD; Basis=MARKET; Confidence=MEDIUM |
| 2 | `_PriceSources/Level_of_Effort.csv` | Level of Effort (Hours) | Estimated hours by deliverable x role; DEL-05-04 has 1 row (R-13, 8 hrs) | CSV with headers; Execution=6b filter applied; Basis=PARAMETRIC for all rows |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Project Parameters | Not directly used for DEL-05-04 pricing; provides context (building areas, quantities) | CSV with headers; 29 parameters; used for cross-reference only |

## Decomposition Source

| Source File | Used For | Notes |
|---|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | Package/deliverable ID validation; scope item mapping; objective traceability | v2.3 FINAL; DEL-05-04 confirmed in PKG-005; covers SOW-0013; supports OBJ-005 |

## Dependency Source

| Source File | Used For | Notes |
|---|---|---|
| `DEL-05-04_ElectricalMaintainability/Dependencies.csv` | Blocker/readiness assessment | v3.1 schema; 9 rows; 3 prerequisites, 2 interfaces, 1 downstream handover, 2 anchors, 1 requirement trace |

## Source Limitations

- Level_of_Effort.csv provides hours with `Basis=PARAMETRIC` and no explicit confidence rating per row. Hours are treated as best available but carry inherent estimation uncertainty.
- Professional_Staff_Rates.csv rates are market-based at MEDIUM confidence. Actual negotiated rates may differ.
- No quote or historical data available for DEL-05-04. Under STRICT fallback policy, this is acceptable because RATE_TABLE basis is fully satisfied by the available sources.
