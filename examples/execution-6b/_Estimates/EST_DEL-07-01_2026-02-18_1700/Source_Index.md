# Source Index

## Price Sources Used

| # | Source File | Source Type | Parsing Notes | What It Supports |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | 30 roles; CSV with RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes | Hourly rates for all professional staff roles; provides UnitRate for RATE_TABLE method |
| 2 | `_PriceSources/Level_of_Effort.csv` | Rate Table (Hours) | 73 rows; CSV with Execution, DeliverableID, RoleID, Role, EstimatedHours, Basis, Notes | Hours by role by deliverable; provides Qty for each line item |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Reference / Parameters | 29 rows; CSV with ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes | Project-level assumptions (areas, durations, quantities); not directly used for pricing DEL-07-01 but provides context |

## Decomposition Source

| Source File | Version | Status | What It Provides |
|---|---|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | v2.3 FINAL | Accepted | Package IDs, Deliverable IDs, scope item mappings, objective mappings |

## Dependency Source

| Source File | Row Count | What It Provides |
|---|---|---|
| `DEL-07-01_ConstructionMethodologyNarrative/Dependencies.csv` | 15 rows | Upstream prerequisites (4 deliverables, 4 documents), downstream handovers (3 deliverables), anchors (3) |

## Source Limitations

- `Assumed_Project_Parameters.csv` was reviewed but does not contain parameters that directly drive DEL-07-01 pricing. It provides project context only.
- Rate table rates have `Confidence=MEDIUM` and `Basis=MARKET`. No firm-specific rate card was provided.
- Level of effort hours have `Basis=PARAMETRIC`, meaning they are parametric estimates of the hours to produce the deliverable, not time-tracked actuals.
