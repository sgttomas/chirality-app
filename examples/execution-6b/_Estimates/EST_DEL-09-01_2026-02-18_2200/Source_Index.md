# Source Index

## Pricing Sources

| # | Source Path | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | `test/execution-6b/_PriceSources/Professional_Staff_Rates.csv` | Rate Table | 30 roles with RoleID, Role, Category, HourlyRate_CAD; all Basis=MARKET, Confidence=MEDIUM | Provides hourly rates (CAD) for all labour line items; rate lookup by RoleID |
| PS-02 | `test/execution-6b/_PriceSources/Level_of_Effort.csv` | Rate Table (hours) | 73 rows mapping Execution=6b deliverables to RoleID + EstimatedHours; Basis=PARAMETRIC | Provides estimated hours per role per deliverable; DEL-09-01 has 3 rows (R-17: 20h, R-02: 8h, R-15: 4h) |
| PS-03 | `test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv` | Parametric Parameters | 29 parameters covering duration, area, quantity, and financial estimates; mixed confidence | Context for schedule duration assumptions (PP-01: 18 months construction, PP-02: 4 months design, PP-03: 22 months total); not directly used for pricing |

## Dependency Sources

| # | Source Path | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| DS-01 | `test/execution-6b/PKG-009_Schedule_and_Milestones/1_Working/DEL-09-01_DetailedProjectSchedule/Dependencies.csv` | Dependency Register v3.1 | 12 rows; 2 ANCHOR + 7 EXECUTION dependencies; Schema v3.1 | Blocker/readiness analysis; no pricing evidence |

## Decomposition Source

| # | Source Path | Notes |
|---|---|---|
| DC-01 | `test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | v2.3 FINAL; provides DEL-09-01 definition under PKG-009 (Section 9); SOW-0025 mapping; OBJ-009 alignment |
