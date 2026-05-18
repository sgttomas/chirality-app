# Source Index -- EST_DEL-01-06_2026-02-18_1030

## Price Sources

### Source 1: Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| Path | _PriceSources/Professional_Staff_Rates.csv |
| Type | Rate Table |
| Format | CSV (31 rows including header) |
| Content | Hourly rates (CAD) for 30 professional roles by RoleID |
| Basis | MARKET |
| Confidence | MEDIUM (all rows) |
| Used for DEL-01-06 | Yes -- R-16 Site Superintendent ($135/hr) and R-15 Construction Manager ($155/hr) |
| Parsing notes | Clean CSV; no parsing issues. Rate for R-30 (Surety Broker) is $0 (commission-based; not applicable here). |
| Limitations | Covers professional labor rates only. Does not include non-labor costs (equipment, materials, rentals, subcontracted services). |

### Source 2: Level_of_Effort.csv

| Field | Value |
|---|---|
| Path | _PriceSources/Level_of_Effort.csv |
| Type | Rate Table (quantity support -- estimated hours by deliverable and role) |
| Format | CSV (18 rows including header; filtered to Execution 6a) |
| Content | Estimated hours per RoleID per DeliverableID for all PKG-001 deliverables |
| Basis | PARAMETRIC (all rows) |
| Used for DEL-01-06 | Yes -- R-16 (1,440 hrs) and R-15 (60 hrs) |
| Parsing notes | Clean CSV. Hours are parametrically derived (noted in Basis column). |
| Limitations | Covers professional labor hours only. No line items for non-labor costs (temp facilities, fencing, cleaning subcontracts). |

### Source 3: Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| Path | _PriceSources/Assumed_Project_Parameters.csv |
| Type | Rate Table (project parameter support -- durations, areas, quantities, financial estimates) |
| Format | CSV (29 rows including header) |
| Content | Project parameters including durations, building areas, quantities, and rough financial estimates |
| Basis | Mixed (ASSUMPTION, CONFIRMED, DESIGN_BASIS, DERIVED, PARAMETRIC) |
| Used for DEL-01-06 | Indirectly -- PP-01 (18-month construction duration) underpins the 1,440 hr Site Superintendent estimate in Level_of_Effort.csv |
| Parsing notes | Clean CSV. Some rows are PARAMETRIC/LOW confidence financial estimates (PP-21 through PP-25) used for order-of-magnitude calculations only. |
| Limitations | Does not contain unit rates for pricing. Provides parameter context for hours/quantity derivation. |

## Non-Price Sources (read-only context)

### Decomposition

| Field | Value |
|---|---|
| Path | _Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| Used for | Stable IDs (PKG-001, DEL-01-06), scope item mappings (SOW-0010, SOW-0111, SOW-0112), CBS hint derivation |
| Status | Loaded successfully; DEL-01-06 confirmed in Phase 5 deliverable table |

### Dependency Register

| Field | Value |
|---|---|
| Path | DEL-01-06/Dependencies.csv |
| Used for | Blocker detection; readiness assessment |
| Status | Loaded successfully; 8 rows (4 ANCHOR, 4 EXECUTION); 0 estimate-blocking items |

### Deliverable Working Files (read-only)

| File | Used for |
|---|---|
| DEL-01-06/Datasheet.md | Scope confirmation, cost driver identification |
| DEL-01-06/_CONTEXT.md | Deliverable description and artifact list |
| DEL-01-06/_DEPENDENCIES.md | Dependency summary and extraction notes |

## Source Coverage Assessment

| Cost Driver (from brief) | Source Coverage | Status |
|---|---|---|
| Site superintendent salary | Fully covered by Professional_Staff_Rates.csv (R-16) + Level_of_Effort.csv | PRICED |
| Construction manager oversight | Fully covered by Professional_Staff_Rates.csv (R-15) + Level_of_Effort.csv | PRICED |
| Temp facilities/fencing/cleaning | No rate table evidence in any PRICE_SOURCE | TBD -- missing source |
