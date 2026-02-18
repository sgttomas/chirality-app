# Source Index -- EST_DEL-01-07_2026-02-18_1830

## Price Sources

### Source 1: Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| Path | _PriceSources/Professional_Staff_Rates.csv |
| Type | Rate Table |
| Format | CSV (31 data rows + header) |
| Content | Hourly rates (CAD) for 31 professional roles by RoleID |
| Basis | MARKET |
| Confidence | MEDIUM |
| Supports | Unit rate lookup for all labor line items |
| Limitations | Rates are market estimates, not contractual; no escalation or locality factors applied |
| Rows used for DEL-01-07 | R-02 (Project Manager, $175/hr), R-21 (Commissioning Lead, $140/hr), R-24 (Administrative / Document Control, $80/hr) |

### Source 2: Level_of_Effort.csv

| Field | Value |
|---|---|
| Path | _PriceSources/Level_of_Effort.csv |
| Type | Rate Table (hours component) |
| Format | CSV (18 data rows + header) |
| Content | Estimated hours by DeliverableID and RoleID for execution 6a |
| Basis | PARAMETRIC |
| Confidence | MEDIUM |
| Supports | Quantity (hours) for all labor line items |
| Limitations | Hours are parametric estimates based on assumed project duration and scope; not validated against historical projects |
| Rows used for DEL-01-07 | DEL-01-07/R-21 (120h), DEL-01-07/R-02 (30h), DEL-01-07/R-24 (20h) |

### Source 3: Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| Path | _PriceSources/Assumed_Project_Parameters.csv |
| Type | Parameter Table |
| Format | CSV (29 data rows + header) |
| Content | Project-level assumptions (durations, areas, quantities, financial estimates) |
| Basis | Mixed (ASSUMPTION, CONFIRMED, DESIGN_BASIS, DERIVED, PARAMETRIC) |
| Confidence | Mixed (LOW to HIGH) |
| Supports | Context for hour estimates (PP-01 construction duration 18 months; PP-03 total project duration 22 months) |
| Limitations | Parameters are assumptions, not confirmed quantities; not directly used for pricing but inform reasonableness of hour allocations |
| Rows referenced for DEL-01-07 | PP-01 (18 months construction duration -- anchors warranty period and Cx timeline) |

## Dependency Sources

### Dependencies.csv (DEL-01-07)

| Field | Value |
|---|---|
| Path | DEL-01-07 working folder / Dependencies.csv |
| Type | Dependency Register |
| Format | CSV (14 data rows + header; schema v3.1) |
| Content | Anchor edges (6) and execution edges (8) for DEL-01-07 |
| Used for | Blocker identification and readiness assessment (NOT used for pricing) |
| Limitations | All SatisfactionStatus=TBD (initial extraction; no closure assessment performed) |

## Decomposition

| Field | Value |
|---|---|
| Path | _Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| Version | FINAL v1.0 (Phase 7) |
| Used for | Package/deliverable ID validation; scope item mapping; CBS hint derivation |
