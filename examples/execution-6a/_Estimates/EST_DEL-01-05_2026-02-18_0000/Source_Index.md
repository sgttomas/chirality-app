# Source Index

## Pricing Sources

| # | Source Path | Source Type | Description | Supports |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | Hourly rates (CAD) for 30 professional roles by RoleID; includes Category, Basis, and Confidence fields | Unit rate lookup for all labour line items; provides $/hr by RoleID |
| 2 | `_PriceSources/Level_of_Effort.csv` | Rate Table (hours) | Estimated hours by DeliverableID and RoleID for execution 6a; includes Basis and Notes fields | Quantity (hours) for each labour line item; scoped to DEL-01-05 rows |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Parameters / Assumptions | Project-level parameters (durations, areas, quantities, financial estimates) with Source and Confidence | Context for hour estimates (e.g., PP-01 construction duration 18 months used as basis for LOE hours); not used directly for unit rates |

## Decomposition Source

| Source Path | Description |
|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` | Stable decomposition providing Package IDs, Deliverable IDs, scope item mappings, and objective linkages |

## Dependency Source

| Source Path | Description |
|---|---|
| `PKG-001_.../DEL-01-05_.../Dependencies.csv` | Extracted dependency register (v3.1, 11 rows) for DEL-01-05; used for blocker/readiness analysis only (not pricing evidence) |

## Parsing Notes

- **Professional_Staff_Rates.csv:** 31 data rows (R-01 through R-30 plus header). All rates in CAD. Confidence is MEDIUM for all active roles. R-30 (Surety Broker) has rate $0 and is not applicable to DEL-01-05.
- **Level_of_Effort.csv:** 18 data rows covering all PKG-001 deliverables. DEL-01-05 has 2 rows: R-02 (90 hrs) and R-24 (50 hrs). Basis is PARAMETRIC for all rows.
- **Assumed_Project_Parameters.csv:** 29 parameters. PP-01 (18-month construction duration) is the primary driver for DEL-01-05 hour estimates per LOE notes.
- **Dependencies.csv (DEL-01-05):** 11 rows (4 ANCHOR, 7 EXECUTION). No estimate-blocking dependencies identified; all upstream dependencies are contract-level prerequisites (not cost-information blockers).

## What These Sources Cannot Support

- No material/equipment costs are included (DEL-01-05 is a management/controls deliverable; cost drivers are labour hours only).
- No subcontractor quotes are included.
- No escalation or inflation factors are provided.
- No overhead/markup/profit percentages are provided in these sources; amounts are bare labour cost only.
