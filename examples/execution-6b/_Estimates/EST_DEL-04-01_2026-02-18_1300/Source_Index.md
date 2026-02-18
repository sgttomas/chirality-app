# Source Index

**RunID:** EST_DEL-04-01_2026-02-18_1300

## Pricing Sources

| # | Source Path | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | 30 roles (R-01 through R-30); CSV with headers: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes | Hourly rates (CAD) for all professional roles; used for UnitRate in Detail.csv |
| 2 | `_PriceSources/Level_of_Effort.csv` | Rate Table (hours) | 73 rows across all deliverables; filtered to 2 rows for DEL-04-01; CSV with headers: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes | Hour quantities per role per deliverable; used for Qty in Detail.csv |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Parametric (context only) | 29 parameters; not used directly for pricing DEL-04-01 | Context on project scale and quantities; not a pricing driver for this narrative deliverable |

## Decomposition Source

| Source Path | Version | Role |
|---|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | v2.3 FINAL | Package IDs, deliverable IDs, scope item mapping, deliverable descriptions, type classification |

## Dependency Source

| Source Path | Row Count | Role |
|---|---|---|
| `DEL-04-01_BuildingEnvelopeAndEnergyStrategy/Dependencies.csv` | 15 rows (v3.1 schema) | Blocker assessment; interface identification; readiness check |

## What Sources Cannot Support

- No construction material pricing (not applicable to this narrative deliverable).
- No escalation or contingency factors provided; estimate is base professional hours only.
- Rate confidence is MEDIUM (market basis); no firm-specific negotiated rates available.
- Hour estimates are PARAMETRIC basis per Level_of_Effort.csv; not based on historical actuals for this specific project type.
