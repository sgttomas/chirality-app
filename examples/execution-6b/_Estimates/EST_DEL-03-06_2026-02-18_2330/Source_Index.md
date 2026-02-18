# Source Index

**RunID:** EST_DEL-03-06_2026-02-18_2330

---

## Price Sources

| # | Source Path | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `/test/execution-6b/_PriceSources/Professional_Staff_Rates.csv` | Rate Table | CSV with 30 roles; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes | Hourly rates for all professional staff roles; MARKET basis; MEDIUM confidence |
| 2 | `/test/execution-6b/_PriceSources/Level_of_Effort.csv` | Rate Table (hours) | CSV with 73 rows across all deliverables; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes | Estimated hours by deliverable and role; PARAMETRIC basis; used as quantity input |
| 3 | `/test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv` | Parameters | CSV with 29 parameters; columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes | Project-level assumptions (areas, quantities, durations, financial estimates); not directly used for DEL-03-06 pricing but available for context |

## Scope Sources

| # | Source Path | Source Type | Notes |
|---|---|---|---|
| 4 | `/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | Decomposition | v2.3 FINAL; provides Package IDs, Deliverable IDs, scope item mappings, and deliverable descriptions |
| 5 | `/test/execution-6b/PKG-003_Design_Brief/1_Working/DEL-03-06_AccessibilityAndAdaptabilityNarrative/Dependencies.csv` | Dependency Register | v3.1 schema; 19 dependency rows for DEL-03-06; used for blocker/readiness analysis only |

## What Sources Can and Cannot Support

- **Professional_Staff_Rates.csv** provides unit rates for all roles. It cannot confirm whether hours are correctly allocated across roles.
- **Level_of_Effort.csv** provides hours by deliverable and role. Its basis is PARAMETRIC (estimated, not measured). It cannot provide rates.
- **Assumed_Project_Parameters.csv** provides project-level context (areas, quantities). It does not directly price DEL-03-06 line items but informs reasonableness checks.
- **Dependencies.csv** identifies upstream blockers and interfaces. It is not used for pricing evidence per invariant rules.
