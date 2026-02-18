# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-05-03_2026-02-18_2350 |
| **AsOf** | 2026-02-18T23:50:00-07:00 |
| **Scope** | DEL-05-03 |
| **ScopeResolvedSummary** | 1 deliverable in scope (DEL-05-03 Mechanical Maintainability, PKG-005) |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-05-03/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Resolved Paths

- **ESTIMATES_ROOT:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Estimates/
- **Deliverable Path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-005_Building_Durability_and_Maintenance/1_Working/DEL-05-03_MechanicalMaintainability/
- **Decomposition:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md
- **Rate Table:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_PriceSources/Professional_Staff_Rates.csv
- **Level of Effort:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_PriceSources/Level_of_Effort.csv
- **Project Parameters:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv

## CBS Mapping Rule

CBS for DEL-05-03 is assigned as **PROFESSIONAL_SERVICES > MECHANICAL_ENGINEERING**. This deliverable is a T2 Narrative (no construction materials or equipment procurement); the cost driver is professional staff hours for producing a mechanical maintainability narrative for the proposal. CBS assigned deterministically based on the primary role (R-11, Mechanical Engineer Senior) and deliverable type (Narrative).

## Scope Resolution

DEL-05-03 is explicitly identified in the decomposition (Section 9, PKG-005) as "Mechanical Maintainability" -- a Durability/Narrative deliverable covering SOW-0013 and supporting OBJ-005 (15 evaluation points for Building Durability and Ease of Maintenance). The responsible party is the Mechanical Engineer.
