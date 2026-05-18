# Source Index

## Pricing Sources Used

| # | Source Path | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | test/execution-6b/_PriceSources/Professional_Staff_Rates.csv | Rate Table | 30 roles with RoleID, Role, Category, HourlyRate_CAD; parsed as CSV with header row | Hourly rates for all professional staff roles; matched by RoleID |
| 2 | test/execution-6b/_PriceSources/Level_of_Effort.csv | Level of Effort (Hours) | 73 rows covering all 38 deliverables; filtered by Execution=6b and DeliverableID=DEL-08-02; parsed as CSV with header row | Estimated hours by role per deliverable; provides Qty for rate table pricing |
| 3 | test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv | Project Parameters | 29 parameters covering durations, areas, quantities, and financial estimates; parsed as CSV with header row | Contextual parameters only; no direct pricing used from this source for DEL-08-02 |

## Dependency Sources Used

| # | Source Path | Source Type | Notes |
|---|---|---|---|
| 1 | test/execution-6b/PKG-008_Commissioning_Closeout_and_Warranty/1_Working/DEL-08-02_DeficienciesManagementNarrative/Dependencies.csv | Dependency Register (v3.1) | 13 dependency rows; used for blocker/readiness analysis only; NOT used for pricing evidence |

## Decomposition Source

| # | Source Path | Version | Notes |
|---|---|---|---|
| 1 | test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md | v2.3 FINAL | Provides stable IDs (PKG-008, DEL-08-02), scope item mapping (SOW-0024), and deliverable description |

## Source Coverage for DEL-08-02

- **Hours evidence**: Level_of_Effort.csv provides 2 rows for DEL-08-02 (R-21: 6 hrs, R-02: 2 hrs). Coverage: COMPLETE.
- **Rate evidence**: Professional_Staff_Rates.csv provides rates for R-21 ($140/hr) and R-02 ($175/hr). Coverage: COMPLETE.
- **No gaps identified** for this deliverable.
