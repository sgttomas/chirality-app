# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-02-03_2026-02-18_2100 |
| **AsOf** | 2026-02-18T21:00:00-07:00 |
| **Scope** | DEL-02-03 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-02-03/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Pricing Logic

Estimate is derived by joining two price source files:

1. **Level_of_Effort.csv** provides `DeliverableID`, `RoleID`, and `EstimatedHours` for each role contributing to DEL-02-03.
2. **Professional_Staff_Rates.csv** provides `RoleID` and `HourlyRate_CAD` for each role.

The join key is `RoleID`. For each line item:
- `Qty` = EstimatedHours from Level_of_Effort.csv
- `Unit` = HR
- `UnitRate` = HourlyRate_CAD from Professional_Staff_Rates.csv
- `Amount` = Qty x UnitRate, rounded per ROUNDING=DOLLAR

This constitutes a RATE_TABLE basis: hours are a level-of-effort estimate, rates are from a market-based rate table.

## CBS Mapping Rule

No explicit `CBSHint` was found in the decomposition for DEL-02-03. CBS is assigned as:
- `PROF-STRUCT` for structural engineering professional services hours

This is a deterministic mapping: structural engineer roles (R-09, R-10) map to CBS code `PROF-STRUCT` (professional services -- structural discipline).

## Dependency Summary

16 dependency rows loaded from DEL-02-03/Dependencies.csv. Key execution dependencies:
- **DEP-02-03-E001**: Prerequisite on DEL-02-01 (Architectural Concept Package) -- required for floor plans, clear spans, building heights
- **DEP-02-03-E002**: Prerequisite on DEL-02-02 (Civil Site Concept Plan) -- required for site placement, grading, foundation context
- **DEP-02-03-E003**: Prerequisite on Appendix D (2021 Geotechnical Report) -- required for bearing capacity, groundwater, frost depth
- **DEP-02-03-E007**: Constraint DEC-013 -- no additional geotechnical investigation

No blockers prevent estimating; all dependencies relate to production readiness, not pricing evidence.
