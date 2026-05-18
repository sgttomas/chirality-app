# Source_Index — EST_DEL-001-11_2026-02-28_0803

## Indexed Price Sources

| Source File | Source Type | Parsing Notes | Supports | Does Not Support |
|---|---|---|---|---|
| `Professional_Staff_Rates.csv` | PARAMETRIC (rate table) | 25 rows; RoleID R-01 through R-25; hourly rates in CAD; all MEDIUM confidence | Hourly staff rates for all roles referenced in LOE | No lump-sum activity costs; no material costs |
| `Level_of_Effort.csv` | PARAMETRIC (effort model) | 583 rows total; 6 rows for DEL-001-11; maps DeliverableID x RoleID to EstimatedHours | Hour quantities for DEL-001-11: R-01 (6h), R-08 (4h), R-11 (27h), R-12 (21h), R-13 (12h), R-21 (16h) | No rates (must cross-reference with Staff Rates); no non-labour items |
| `Assumed_Project_Parameters.csv` | PARAMETRIC (parameters) | 18 rows; project identity, location, facility attributes, equipment, currency | Project context: 13,000 sqft addition, 35 ft ceiling, 2x5T cranes, CAD currency | No pricing rates; informational context only |
| `Professional_Design_Fees.csv` | PARAMETRIC (fee model) | 5 rows; discipline-level fee percentages as % of construction value | Alternative fee-based pricing method for architecture (DF-01: 3.0%-6.0%, recommended 4.5%) | Requires construction value input (not available for this deliverable-level estimate); not used as primary method |
| `Parametric_Building_Rates.csv` | PARAMETRIC (building rates) | 2 rows; PB-01 industrial building at $220-$360/sf (recommended $285/sf); PB-02 wash bay premium | Cross-check for overall building cost (not directly applicable to design specification deliverable) | Not applicable to design-phase professional services costing |
| `Fees_Permits_Insurance.csv` | PARAMETRIC (fees/permits) | 12 rows; FP-01 through FP-12; bonding, insurance, permits, inspection, regulatory fees | FP-11: P.Eng. stamp/AAAL review ($1,500-$4,000, recommended $2,500); FP-12: Building permit Camrose County ($5,000-$15,000, recommended $10,000) | Many items not applicable to this deliverable (bonding, construction insurance, crane inspection) |

## Source-to-Item Mapping

| ItemID | Primary Source | Secondary Source | Notes |
|---|---|---|---|
| ITEM-001 | PS-LOE (R-01, 6h) + PS-STAFF (R-01, $165/hr) | -- | Direct LOE x Rate |
| ITEM-002 | PS-LOE (R-08, 4h) + PS-STAFF (R-08, $135/hr) | -- | Direct LOE x Rate |
| ITEM-003 | PS-LOE (R-11, 27h) + PS-STAFF (R-11, $180/hr) | -- | Direct LOE x Rate |
| ITEM-004 | PS-LOE (R-12, 21h) + PS-STAFF (R-12, $135/hr) | -- | Direct LOE x Rate |
| ITEM-005 | PS-LOE (R-13, 12h) + PS-STAFF (R-13, $95/hr) | -- | Direct LOE x Rate |
| ITEM-006 | PS-LOE (R-21, 16h) + PS-STAFF (R-21, $140/hr) | -- | Direct LOE x Rate; survey effort split: 8h field + 8h data processing |
| ITEM-007 | None -- included in ITEM-003 Senior Architect hours | -- | Code review effort assumed embedded in Senior Architect LOE; no separate line priced |
| ITEM-008 | None -- included in ITEM-004 Architect hours | -- | Coordination effort assumed embedded in Architect LOE; no separate line priced |
| ITEM-009 | None -- included in ITEM-001 PM hours | -- | County coordination assumed embedded in PM LOE; no separate line priced |
| ITEM-010 | Fees_Permits_Insurance.csv FP-11 ($2,500 recommended) | -- | P.Eng. stamp and AAAL review fee per issuance cycle |
| ITEM-011 | Fees_Permits_Insurance.csv FP-12 ($10,000 recommended) | -- | Building permit -- Camrose County (13,000 sqft commercial) |
