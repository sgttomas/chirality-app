# Source Index

## Price Sources

| # | Source Path | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `test/execution-6b/_PriceSources/Professional_Staff_Rates.csv` | Rate Table | CSV; 30 roles with RoleID, Role, Category, HourlyRate_CAD; all rates in CAD; Confidence = MEDIUM; Basis = MARKET | Unit rates ($/hr) for all professional staff roles. Used for DEL-08-03 roles R-02 and R-21. |
| 2 | `test/execution-6b/_PriceSources/Level_of_Effort.csv` | Rate Table (hours) | CSV; 73 rows across all deliverables; filtered to Execution=6b, DeliverableID=DEL-08-03 yields 2 rows (R-02 @ 4 hrs, R-21 @ 4 hrs); Basis = PARAMETRIC | Hour quantities per role per deliverable. Used to derive Qty for each Detail.csv line. |
| 3 | `test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv` | Project Parameters | CSV; 29 parameters covering duration, area, quantities, financial assumptions | Not directly used for DEL-08-03 pricing. Referenced for context only (no construction quantities apply to this narrative deliverable). |

## Dependency Source

| # | Source Path | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 4 | `test/execution-6b/PKG-008_.../DEL-08-03_.../Dependencies.csv` | Dependency Register | CSV; v3.1 schema; 10 dependency rows for DEL-08-03 | Blocker/readiness assessment only; NOT used for pricing evidence per invariant. |

## Decomposition Source

| # | Source Path | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 5 | `test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | Decomposition (v2.3 FINAL) | Markdown; 38 deliverables across 10 packages; DEL-08-03 confirmed in PKG-008 | Package/deliverable ID resolution; CBS hint (none explicit; deterministic rule applied). |
