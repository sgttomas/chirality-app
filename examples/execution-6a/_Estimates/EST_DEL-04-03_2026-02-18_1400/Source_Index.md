# Source Index

## Price Sources

| # | Source File | Source Type | Items Used | Supports | Parsing Notes |
|---|---|---|---|---|---|
| 1 | Structural_Concrete_Rates.csv | Rate Table | SC-03, SC-07, SC-12, SC-13, SC-14, SC-15 | Foundation (screw piles, spread footings, strip footings); floor slab; reinforcing; anchor bolts | 16 items total; CSV with headers; rates in CAD; Confidence=MEDIUM |
| 2 | Building_Envelope_Rates.csv | Rate Table | (none used for DEL-04-03) | Not applicable -- building shell is DEL-04-01 scope | 15 items total; not relevant to foundation/floor |
| 3 | Mechanical_System_Rates.csv | Rate Table | (none used for DEL-04-03) | Not applicable -- mechanical is DEL-04-04 scope | 14 items total; not relevant to foundation/floor |
| 4 | Electrical_System_Rates.csv | Rate Table | (none used for DEL-04-03) | Not applicable -- electrical is DEL-04-04 scope | 14 items total; not relevant to foundation/floor |
| 5 | Parametric_Building_Rates.csv | Rate Table | (none used directly; PB-02 used as cross-check) | PB-02 provides a turnkey PEMB rate ($48/sf) that includes foundation + floor; used for validation only | 9 items total; parametric rates |
| 6 | Construction_Labour_Rates.csv | Rate Table | (none used directly; labour embedded in unit rates) | Labour rates are embedded in the unit rates from Structural_Concrete_Rates.csv | 15 items total; fully burdened rates in CAD |
| 7 | Assumed_Project_Parameters.csv | Parameters | PP-07, PP-14 | PP-07: Cold storage footprint = 6,000 sf (confirmed); PP-14: 2 overhead doors for cold storage (confirmed) | 29 items total; project parameters |

## Deliverable Sources (Read-Only)

| Source | Purpose | Key Data Extracted |
|---|---|---|
| DEL-04-03 Datasheet.md | Quantities, soil parameters, foundation options | Building dimensions (60'x100' = 6,000 sf = 557.4 m2); soil stratigraphy; frost depth 2.0 m; sulphate class S-2; 4 door openings |
| DEL-04-03 Specification.md | Requirements (REQ-01 through REQ-13) | Foundation selection criteria; floor system criteria; concrete mix requirements; subgrade preparation requirements |
| DEL-04-03 Guidance.md | Design trade-offs and option assessment | Screw piles described as "ideal"; foundation option assessment; floor option assessment |
| DEL-04-03 Dependencies.csv | Dependency evidence for blockers | 12 dependency rows; no blocking dependencies for estimating purposes |
| DEL-04-03 _CONTEXT.md | Deliverable identity and scope | SOW-0303, SOW-0304; DEC-002, DEC-003 |

## Decomposition Source

| Source | Data Used |
|---|---|
| Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md | DEL-04-03 identity; PKG-004 identity; scope items SOW-0303, SOW-0304; decisions DEC-002, DEC-003 |

## Sources NOT Used (and reason)

| Source | Reason |
|---|---|
| Building_Envelope_Rates.csv | Building shell/envelope is DEL-04-01 scope, not DEL-04-03 |
| Mechanical_System_Rates.csv | Mechanical/ventilation is DEL-04-04 scope, not DEL-04-03 |
| Electrical_System_Rates.csv | Electrical is DEL-04-04 scope, not DEL-04-03 |
| Construction_Labour_Rates.csv | Labour is embedded in unit rates from Structural_Concrete_Rates.csv; no separate labour line items needed |
