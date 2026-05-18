# Source Index -- EST_DEL-04-04_2026-02-18_1500

## Price Sources

| # | Source File | Source Type | Items Used | Supports | Parsing Notes |
|---|---|---|---|---|---|
| 1 | _PriceSources/Electrical_System_Rates.csv | Rate Table | ES-12 | Cold storage basic electrical (power + lighting) at $6/sf | 15 rows total; 1 row directly applicable (ES-12). ES-05 (lighting-only) was considered but not used to avoid double-counting with ES-12. |
| 2 | _PriceSources/Mechanical_System_Rates.csv | Rate Table | MS-13 | Cold storage ventilation (condensation prevention) at $3/sf | 14 rows total; 1 row directly applicable (MS-13). |
| 3 | _PriceSources/Construction_Labour_Rates.csv | Rate Table | (none directly) | Not directly used for line pricing; labour rates are embedded in the $/sf rates from ES-12 and MS-13. T-07 (Electrician $80/hr burdened) and T-05 (Plumber/Pipefitter $82/hr burdened) are the relevant trades. | Available for detailed build-up if needed in future iterations. |
| 4 | _PriceSources/Parametric_Building_Rates.csv | Parametric | PB-01, PB-02 (cross-check only) | Used for cross-check validation only (PB-02 turnkey $48/sf minus PB-01 shell $32/sf = $16/sf delta). Not used for line pricing. | 9 rows total; 2 rows used for cross-check. |
| 5 | _PriceSources/Assumed_Project_Parameters.csv | Parameters | PP-07, PP-14 | PP-07 = 6,000 sf cold storage area (confirmed, HIGH). PP-14 = 2 overhead doors (confirmed, HIGH). | 29 rows total; 2 rows directly applicable. |

## Decomposition Source

| Source File | Used For |
|---|---|
| _Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md | Package/deliverable IDs; scope item mapping (SOW-0300 MEP aspects); objective mapping (OBJ-004); scope boundary validation |

## Dependency Source

| Source File | Used For |
|---|---|
| DEL-04-04_Cold Storage - Electrical & Ventilation/Dependencies.csv | 9 dependency rows loaded. Used for blocker detection and readiness assessment. No unresolved blockers preventing estimating. |
