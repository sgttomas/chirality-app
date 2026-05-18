# Source Index

**RunID:** EST_DEL-01-09_2026-02-18_1500

## Price Sources

| # | Source File | Source Type | What It Supports | Parsing Notes |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | Hourly rates (CAD) by RoleID for 30 roles | CSV; 31 rows (header + 30 data); columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. All rates at MEDIUM confidence, MARKET basis. |
| 2 | `_PriceSources/Level_of_Effort.csv` | Rate Table (hours) | Estimated hours by DeliverableID and RoleID | CSV; 73 rows (header + 72 data); columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. DEL-01-09 has 2 rows (R-02: 8 hrs, R-24: 4 hrs). |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Parameters | Project-level assumptions (areas, quantities, financials) | CSV; 29 rows (header + 28 data). Not directly used for DEL-01-09 pricing but informs project context. |

## Decomposition Source

| Source File | Role | Notes |
|---|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | Scope IDs, package mapping, deliverable attributes | v2.3 FINAL; confirmed DEL-01-09 in PKG-001; covers SOW-0007; supports OBJ-006 |

## Dependency Source

| Source File | Role | Notes |
|---|---|---|
| `DEL-01-09_.../Dependencies.csv` | Execution dependencies, requirement traces | v3.1 schema; 11 dependency rows; 2 upstream prerequisites (DEL-01-07, DEL-01-08); 1 downstream handover (DEL-01-02); 1 downstream interface (DEL-07-03) |

## Source Coverage Assessment

All line items in Detail.csv have complete provenance:
- L-01: Hours from Level_of_Effort.csv (R-02 row), rate from Professional_Staff_Rates.csv (R-02 row)
- L-02: Hours from Level_of_Effort.csv (R-24 row), rate from Professional_Staff_Rates.csv (R-24 row)

No TBD source references exist.
