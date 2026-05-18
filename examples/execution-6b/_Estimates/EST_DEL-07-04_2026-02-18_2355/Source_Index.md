# Source Index

## Price Sources Used

| # | Source File | Source Type | What It Supports | Parsing Notes |
|---|---|---|---|---|
| 1 | `test/execution-6b/_PriceSources/Professional_Staff_Rates.csv` | Rate Table | Hourly rates by RoleID (CAD); 30 roles defined | CSV with headers; RoleID is the join key to Level_of_Effort.csv |
| 2 | `test/execution-6b/_PriceSources/Level_of_Effort.csv` | Rate Table (hours) | Estimated hours by DeliverableID + RoleID; 73 rows across all deliverables | CSV with headers; filtered to Execution=6b, DeliverableID=DEL-07-04 yielding 1 row |
| 3 | `test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv` | Parameters | Project-level parameters (durations, areas, quantities, financial estimates) | CSV with headers; 29 parameters; not directly used for DEL-07-04 pricing but provides context |

## Decomposition Source

| Source File | Role |
|---|---|
| `test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | Stable IDs (PKG-007, DEL-07-04), scope mapping (SOW-0022), objective alignment (OBJ-002), responsible party identification |

## Dependency Source

| Source File | Role |
|---|---|
| `test/execution-6b/PKG-007_Construction_Methodology_and_Administration/1_Working/DEL-07-04_MeetingsAndReportingNarrative/Dependencies.csv` | 9 dependency rows; used for blocker analysis and interface identification; not used for pricing |

## Source Limitations

- Level_of_Effort.csv assigns only 1 role (R-02 Project Manager) to DEL-07-04; the decomposition lists "PM / Construction Manager" as responsible parties, suggesting potential undercount.
- Assumed_Project_Parameters.csv provides no parameters directly driving DEL-07-04 scope (meeting frequency is not parameterized).
