# Source_Index — EST_DEL-001-11_2026-02-26_2245

## Indexed Price Sources

| Source File | Source Type | Parsing Notes | Supports | Does Not Support |
|---|---|---|---|---|
| `Professional_Staff_Rates.csv` | PARAMETRIC (rate table) | 25 rows; RoleID R-01 through R-25; hourly rates in CAD; all MEDIUM confidence | Hourly staff rates for all roles referenced in LOE | No lump-sum activity costs; no material costs |
| `Level_of_Effort.csv` | PARAMETRIC (effort model) | 577 rows total; 5 rows for DEL-001-11; maps DeliverableID x RoleID to EstimatedHours | Hour quantities for DEL-001-11: R-01 (6h), R-08 (4h), R-11 (27h), R-12 (21h), R-13 (12h) | No rates (must cross-reference with Staff Rates); no non-labour items |
| `Assumed_Project_Parameters.csv` | PARAMETRIC (parameters) | 18 rows; project identity, location, facility attributes, equipment, currency | Project context: 13,000 sqft addition, 35 ft ceiling, 2x5T cranes, CAD currency | No pricing rates; informational context only |
| `Professional_Design_Fees.csv` | PARAMETRIC (fee model) | 5 rows; discipline-level fee percentages as % of construction value | Alternative fee-based pricing method for architecture (DF-01: 3.0%-6.0%, recommended 4.5%) | Requires construction value input (not available for this deliverable-level estimate); not used as primary method |
| `Parametric_Building_Rates.csv` | PARAMETRIC (building rates) | 2 rows; PB-01 industrial building at $220-$360/sf (recommended $285/sf); PB-02 wash bay premium | Cross-check for overall building cost (not directly applicable to design specification deliverable) | Not applicable to design-phase professional services costing |

## Source-to-Item Mapping

| ItemID | Primary Source | Secondary Source | Notes |
|---|---|---|---|
| ITEM-001 | PS-LOE (R-01, 6h) + PS-STAFF (R-01, $165/hr) | -- | Direct LOE x Rate |
| ITEM-002 | PS-LOE (R-08, 4h) + PS-STAFF (R-08, $135/hr) | -- | Direct LOE x Rate |
| ITEM-003 | PS-LOE (R-11, 27h) + PS-STAFF (R-11, $180/hr) | -- | Direct LOE x Rate |
| ITEM-004 | PS-LOE (R-12, 21h) + PS-STAFF (R-12, $135/hr) | -- | Direct LOE x Rate |
| ITEM-005 | PS-LOE (R-13, 12h) + PS-STAFF (R-13, $95/hr) | -- | Direct LOE x Rate |
| ITEM-006 | None — no pricing source available | -- | Amount = TBD; existing conditions survey not priced in LOE for this deliverable |
| ITEM-007 | None — included in ITEM-003 Senior Architect hours | -- | Code review effort assumed embedded in Senior Architect LOE; no separate line priced |
| ITEM-008 | None — included in ITEM-004 Architect hours | -- | Coordination effort assumed embedded in Architect LOE; no separate line priced |
| ITEM-009 | None — included in ITEM-001 PM hours | -- | County coordination assumed embedded in PM LOE; no separate line priced |
| ITEM-010 | None — no pricing source for stamp fees | -- | Amount = TBD; professional stamp fees not in price sources |
| ITEM-011 | None — no pricing source for permit fees | -- | Amount = TBD; permit fees not in price sources; OI-003 open |
