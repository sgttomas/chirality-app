# Source Index — EST_DEL-02-01_2026-02-18_2100

## Revision Note

This source index extends the prior run (EST_DEL-02-01_2026-02-18_0800) by adding Interior_Architectural_Rates.csv (PS-27), which was not available during the prior run. This file resolves all 7 TBD items.

## Price Sources Loaded

| # | File | Rows | Supports | Status |
|---|---|---|---|---|
| 1 | Building_Envelope_Rates.csv | 15 | BE-11/12/13 (doors/hardware) | Unchanged from prior run |
| 2 | **Interior_Architectural_Rates.csv** (NEW) | 25 | IA-01/02/04 (partitions); IA-05 (ceiling); IA-08 (floor finish); IA-12/13 (paint); IA-15/16/17/18 (accessibility); IA-19/20/21 (signage) | **NEW — resolves all 7 prior TBD items** |
| 3 | Professional_Design_Fees.csv | 8 | DF-01 (architectural fee at 7%) | Now computable (construction subtotal available) |
| 4 | Construction_Labour_Rates.csv | 15 | Context only (T-02, T-12 not directly used as composite rates available in IA file) | Unchanged |
| 5 | Structural_Concrete_Rates.csv | 15 | Context only (slab is DEL-02-04) | Unchanged |
| 6 | Mechanical_System_Rates.csv | 14 | Not applicable to DEL-02-01 | Unchanged |
| 7 | Electrical_System_Rates.csv | 14 | Not applicable to DEL-02-01 | Unchanged |
| 8 | Equipment_Pricing.csv | 15 | Not applicable to DEL-02-01 | Unchanged |
| 9 | Assumed_Project_Parameters.csv | 29 | PP-05 (18,000 sf); PP-11/12 (bay counts) | Unchanged |

## Key Rate Table Entries Used (NEW)

### Interior Architectural Rates (from Interior_Architectural_Rates.csv)

| ItemID | Description | Unit | RecommendedRate | Used For |
|---|---|---|---|---|
| IA-01 | Steel stud + 2-layer drywall (fire-rated) | m2 | $112 | L-004 blended partition rate (20% weight) |
| IA-02 | Steel stud + 1-layer drywall (non-rated) | m2 | $82 | L-004 blended partition rate (70% weight) |
| IA-04 | Washroom/wet area partition | m2 | $132 | L-004 blended partition rate (10% weight) |
| IA-05 | Suspended acoustic tile ceiling | m2 | $68 | L-006 |
| IA-08 | Sealed concrete floor (densifier + sealer) | m2 | $35 | L-005 |
| IA-12 | Interior paint — standard latex | m2 | $13 | L-009 blended paint rate (85% weight) |
| IA-13 | Interior paint — epoxy/wet area | m2 | $20 | L-009 blended paint rate (15% weight) |
| IA-15 | Accessible door hardware upgrade | each | $325 | L-007 (6 upgrades) |
| IA-16 | Tactile walking surface indicator | m2 | $230 | L-007 (8 m2) |
| IA-17 | Grab bars + accessories (per accessible WC) | each | $1,100 | L-007 (2 washrooms) |
| IA-18 | Accessible signage package (per floor) | LS | $3,500 | L-007 (1 package) |
| IA-19 | Code-required exit signage (illuminated) | each | $450 | L-008 (14 signs) |
| IA-20 | Fire safety signage package | LS | $2,000 | L-008 (1 package) |
| IA-21 | Room identification signage | each | $115 | L-008 (28 signs) |

### Design Fees (from Professional_Design_Fees.csv)

| ItemID | Description | Rate | Basis |
|---|---|---|---|
| DF-01 | Architectural design fees | 7.0% | Construction cost of architectural scope ($157,317) |
