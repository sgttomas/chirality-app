# Source Index: EST_DEL-02-02_2026-02-18_1036

## Price Sources Indexed

| # | Source File | Source Type | Usable for DEL-02-02 | Parsing Notes |
|---|---|---|---|---|
| 1 | Structural_Concrete_Rates.csv | RATE_TABLE | YES -- SC-03, SC-04 (slab-on-grade rates for bay floor finishing); SC-07 (rebar); SC-08 (misc steel) | 15 rows; ItemID SC-01 through SC-15; Unit rates in CAD |
| 2 | Building_Envelope_Rates.csv | RATE_TABLE | LIMITED -- BE-11 (hollow metal door), BE-13 (hardware) for fire support room doors | 15 rows; ItemID BE-01 through BE-15 |
| 3 | Interior_Architectural_Rates.csv | RATE_TABLE | YES -- IA-04 (wet area partitions), IA-07 (exposed ceiling paint), IA-08 (sealed concrete), IA-10 (ceramic tile), IA-12/IA-13 (paint), IA-24 (washroom accessories), IA-25 (toilet partitions) | 25 rows; ItemID IA-01 through IA-25 |
| 4 | Mechanical_System_Rates.csv | RATE_TABLE | YES -- MS-08 (breathing air compressor), MS-09 (water fill station concept), MS-10 (bay sump) | 14 rows; ItemID MS-01 through MS-14. Note: MS-06 (exhaust extraction) belongs to DEL-02-05 per ownership rules. |
| 5 | Electrical_System_Rates.csv | RATE_TABLE | NO -- Electrical scope belongs to DEL-02-06. Not used for DEL-02-02 pricing. | 14 rows; noted for reference only |
| 6 | Equipment_Pricing.csv | RATE_TABLE | YES -- EQ-06 (bunker gear lockers, 40 units), EQ-08 (breathing air compressor system) | 15 rows; ItemID EQ-01 through EQ-15. EQ-06 and EQ-08 are primary equipment for DEL-02-02. |
| 7 | Professional_Design_Fees.csv | RATE_TABLE | NO -- Design fees are project-level; not allocated to DEL-02-02 construction estimate. | 8 rows; noted for reference only |
| 8 | Construction_Labour_Rates.csv | RATE_TABLE | INDIRECT -- Labour rates embedded in composite unit rates from other tables; used for validation only. | 15 rows; TradeID T-01 through T-15 |
| 9 | Assumed_Project_Parameters.csv | PARAMETERS | YES -- PP-05 (main PSB 18,000 sf), PP-11 (4 fire bays), PP-15 (40 bunker gear lockers), PP-18 (8 bay sumps total, 4 fire). Provides quantity basis. | 29 rows; ParameterID PP-01 through PP-29 |

## Source Coverage Assessment

| DEL-02-02 Cost Element | Primary Source(s) | Coverage |
|---|---|---|
| Bunker gear lockers (40 units) | EQ-06 | FULL -- quantity confirmed (PP-15), unit rate available |
| Breathing air compressor system | EQ-08 / MS-08 | FULL -- system price available; both sources consistent ($45k-65k range) |
| Compressed air distribution piping | No direct rate table entry | PARTIAL -- priced as ALLOWANCE based on EQ-08 Notes + industry scope |
| Bay sump assemblies (4 fire bays) | MS-10 / EQ-10 | FULL -- unit rate available; quantity from PP-18 (4 fire) |
| Decon area fit-up (tile, partitions, fixtures) | IA-04, IA-10, IA-24, IA-25 | FULL -- composite from rate table entries |
| Support room fit-up (SCBA, compressor, gear storage, EMS) | IA-01 through IA-13 (various) | FULL -- rates available for partitions, finishes, paint |
| Bay floor finishing (sealed concrete) | IA-08 | FULL -- unit rate available |
| Bay exposed ceiling paint | IA-07 | FULL -- unit rate available |
| Support room doors (hollow metal) | BE-11, BE-13 | FULL -- unit rate available |

## Sources NOT Used (and why)

- **Electrical_System_Rates.csv**: Electrical scope (power, lighting, displays, PA) belongs to DEL-02-06 per cost ownership rules.
- **Professional_Design_Fees.csv**: Design fees are project-level overhead, not allocated to individual deliverable construction estimates.
- **Building_Envelope_Rates.csv** (most items): Envelope scope belongs to DEL-02-04. Only BE-11/BE-13 used for interior support room doors.
