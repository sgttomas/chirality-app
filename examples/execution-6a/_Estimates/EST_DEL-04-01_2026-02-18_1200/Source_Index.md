# Source Index — EST_DEL-04-01_2026-02-18_1200

## Price Sources

| # | SourceID | Path | Type | Parsing Notes | Supports | Does Not Support |
|---|---|---|---|---|---|---|
| 1 | PriceSrc-01 | _PriceSources/Parametric_Building_Rates.csv | PARAMETRIC | 11 rows parsed; CSV format; ItemID = PB-01 through PB-09 | PB-01: PEMB shell $28-35/sf (primary model for DEL-04-01); PB-02: PEMB turnkey $42-55/sf (cross-check only; includes items outside DEL-04-01 scope) | Detailed component-level pricing; does not break down framing vs. cladding vs. roof separately |
| 2 | PriceSrc-02 | _PriceSources/Structural_Concrete_Rates.csv | PARAMETRIC | 15 rows parsed; CSV format; ItemID = SC-01 through SC-15 | Concrete and structural steel rates; foundation components | Not directly used for DEL-04-01 (foundation/floor is DEL-04-03 scope) |
| 3 | PriceSrc-03 | _PriceSources/Building_Envelope_Rates.csv | PARAMETRIC | 15 rows parsed; CSV format; ItemID = BE-01 through BE-15 | Envelope component rates (wall panels, roof panels, flashing, sealant) | Available for cross-check of PB-01 shell rate; not used as primary basis since PB-01 parametric is the designated model |
| 4 | PriceSrc-04 | _PriceSources/Mechanical_System_Rates.csv | PARAMETRIC | 14 rows parsed; CSV format; ItemID = MS-01 through MS-14 | MS-13: cold storage ventilation $2-4/sf | Not used for DEL-04-01 (ventilation is DEL-04-04 scope) |
| 5 | PriceSrc-05 | _PriceSources/Electrical_System_Rates.csv | PARAMETRIC | 14 rows parsed; CSV format; ItemID = ES-01 through ES-14 | ES-05/ES-12: cold storage electrical/lighting rates | Not used for DEL-04-01 (electrical is DEL-04-04 scope) |
| 6 | PriceSrc-06 | _PriceSources/Construction_Labour_Rates.csv | RATE_TABLE | 15 rows parsed; CSV format; TradeID = T-01 through T-15 | Labour rates for cross-check | Not used as primary basis (PARAMETRIC model preferred) |
| 7 | PriceSrc-07 | _PriceSources/Assumed_Project_Parameters.csv | PARAMETRIC | 29 rows parsed; CSV format; ParameterID = PP-01 through PP-29 | PP-07: Cold storage 6,000 sf (CONFIRMED, HIGH confidence); PP-22: $290,000 rough parametric (PEMB turnkey at $48/sf) | PP-22 includes turnkey scope beyond DEL-04-01 shell-only boundary |

## Decomposition Source

| Field | Value |
|---|---|
| Path | _Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| Type | Decomposition (read-only) |
| Used for | Package IDs, Deliverable IDs, scope item traceability, CBS hints |

## Dependency Source

| Field | Value |
|---|---|
| Path | DEL-04-01 deliverable folder / Dependencies.csv |
| Type | Dependency register (read-only) |
| Used for | Blocker detection, upstream/downstream relationship mapping |
| Rows parsed | 14 |

## Deliverable Content Sources (read-only; not pricing evidence)

| File | Used for |
|---|---|
| DEL-04-01 / _CONTEXT.md | Deliverable identity confirmation |
| DEL-04-01 / Datasheet.md | Attributes, conditions, construction elements |
| DEL-04-01 / Specification.md | Requirements (REQ-04-01-001 through REQ-04-01-015), scope boundaries |
| DEL-04-01 / Procedure.md | Not read for pricing; available for context |
| DEL-04-01 / Guidance.md | Not read for pricing; available for context |
