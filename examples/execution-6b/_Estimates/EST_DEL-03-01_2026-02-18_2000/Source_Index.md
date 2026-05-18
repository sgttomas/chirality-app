# Source Index

**Snapshot:** EST_DEL-03-01_2026-02-18_2000

## Indexed Price Sources

| # | Source File | Source Type | What It Supports | Parsing Notes |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | Hourly rates by role (30 roles, CAD, MARKET basis) | CSV with header row; RoleID is key; HourlyRate_CAD is the pricing column. Used R-04 ($145/hr) for this estimate. |
| 2 | `_PriceSources/Level_of_Effort.csv` | Level of Effort (hours by role per deliverable) | Hour quantities by DeliverableID + RoleID | CSV with header row; filtered to Execution=6b, DeliverableID=DEL-03-01. Found 1 row: R-04 at 12 hrs. PARAMETRIC basis. |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Project Parameters | Building areas, quantities, financial parameters | CSV with header row; 29 parameters. Not directly used for DEL-03-01 pricing (no area-based or quantity-based cost drivers for a narrative deliverable). Retained in index for completeness. |

## Sources NOT Used (and Why)

- `Assumed_Project_Parameters.csv` -- Not applicable to DEL-03-01. This deliverable is priced purely on professional hours (no material quantities, no area-based parametrics). Parameters would be relevant for construction-scope deliverables.

## Dependency Evidence (Non-Pricing)

| Source | Type | Use |
|---|---|---|
| `DEL-03-01_ArchitecturalDesignBrief/Dependencies.csv` | Dependency Register | Blocker/readiness assessment only; 17 rows loaded. Not used for pricing. |
