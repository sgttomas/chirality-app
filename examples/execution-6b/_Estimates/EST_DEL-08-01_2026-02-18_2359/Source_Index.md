# Source Index

## Price Sources Used

| # | Source Path | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `test/execution-6b/_PriceSources/Professional_Staff_Rates.csv` | Rate Table | 30 roles with RoleID, Role, Category, HourlyRate_CAD; all rates basis=MARKET, confidence=MEDIUM | Hourly rates (UnitRate) for all professional staff roles; matched by RoleID |
| 2 | `test/execution-6b/_PriceSources/Level_of_Effort.csv` | Rate Table (hours component) | 73 rows; Execution=6b; keyed by DeliverableID + RoleID; EstimatedHours with basis=PARAMETRIC | Hours (Qty) per deliverable per role; 2 rows matched for DEL-08-01 |
| 3 | `test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv` | Parameters / Reference | 29 parameters across Duration, Area, Quantity, Financial categories | Context parameters only; no direct pricing use for DEL-08-01 (no quantity/area drivers for this narrative deliverable) |

## Decomposition Source

| Source Path | Version | Status | Used For |
|---|---|---|---|
| `test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | v2.3 FINAL | ACCEPTED | Package ID (PKG-008), Deliverable ID (DEL-08-01), scope item mapping (SOW-0023), objective mapping (OBJ-002) |

## Dependency Source

| Source Path | Row Count | Used For |
|---|---|---|
| `test/execution-6b/PKG-008_.../DEL-08-01_.../Dependencies.csv` | 15 rows (2 anchor + 11 execution + 1 document prerequisite) | Blocker/readiness assessment; interface identification |

## Sources NOT Used (in scope but not applicable)

- `Assumed_Project_Parameters.csv`: Reviewed but no parameters directly drive pricing for DEL-08-01. This deliverable is a narrative document; its cost is entirely labor-driven by hours and rates.
