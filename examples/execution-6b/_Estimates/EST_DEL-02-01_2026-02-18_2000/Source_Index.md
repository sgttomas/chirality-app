# Source Index

## Pricing Sources Used

| # | Source File | Source Type | Role in Estimate | Parsing Notes |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | Provides hourly rates (CAD) by RoleID; Basis = MARKET; Confidence = MEDIUM for all roles used | 30 roles defined; 4 roles used for DEL-02-01 (R-02, R-04, R-05, R-06) |
| 2 | `_PriceSources/Level_of_Effort.csv` | Level of Effort (hours by deliverable and role) | Provides estimated hours per role per deliverable; Basis = PARAMETRIC; filtered to Execution=6b, DeliverableID=DEL-02-01 | 73 total rows; 4 rows match DEL-02-01 |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Project Parameters | Context only (building areas, quantities, durations); not directly used for pricing line items | 29 parameters; provides context for reasonableness checks |

## Decomposition Source

| Source File | Role | Version |
|---|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | Provides Package ID, Deliverable ID, scope item mapping, and deliverable description | v2.3 FINAL (2026-02-17) |

## Dependency Source

| Source File | Role | Row Count |
|---|---|---|
| `PKG-002_Conceptual_Design/1_Working/DEL-02-01_ArchitecturalConceptPackage/Dependencies.csv` | Provides upstream/downstream dependency evidence for blocker analysis | 16 dependency rows (4 anchors, 7 execution upstream, 4 execution downstream, 1 constraint) |

## What Sources Cannot Support

- No materials, equipment, or subcontractor pricing is required for DEL-02-01 (proposal production cost only).
- Rates are MARKET-basis with MEDIUM confidence; no firm-specific rate agreements were provided.
- Hours are PARAMETRIC-basis (from Level_of_Effort.csv); these are modeled estimates, not historical actuals.
