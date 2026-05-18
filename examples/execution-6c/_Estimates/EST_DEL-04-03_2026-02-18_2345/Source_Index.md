# Source Index — EST_DEL-04-03_2026-02-18_2345

## Price Sources Used

| Source File | Source Type | Items Used | Supports |
|-------------|-----------|------------|----------|
| `_PriceSources/Professional_Staff_Rates.csv` | RATE_TABLE | R-02 (PM, $175/hr), R-15 (CM, $155/hr) | Hourly rates for DEL-04-03 line items |
| `_PriceSources/Level_of_Effort.csv` | RATE_TABLE (hours) | DEL-04-03/R-02 (6h), DEL-04-03/R-15 (4h) | Hour quantities for DEL-04-03 line items |
| `_PriceSources/Assumed_Project_Parameters.csv` | PARAMETERS | PP-04 (6-week proposal timeline) | Context for effort calibration; not directly priced |

## Decomposition Source

| Source File | Version | Items Used |
|-------------|---------|------------|
| `_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md` | v1.0 (2026-02-04) | DEL-04-03 definition (Section 8), PKG-06 definition (Section 7), SOW-021 mapping (Section 10) |

## Dependency Source

| Source File | Schema | Items Used |
|-------------|--------|------------|
| `DEL-04-03/Dependencies.csv` | v3.1 | 11 dependency rows (4 anchor, 4 upstream execution, 2 downstream, 1 handover) |

## BOE Source

| Source File | Section | Items Used |
|-------------|---------|------------|
| `_Estimates/BASIS_OF_ESTIMATE.md` | Section 4 PKG-06 | DEL-04-03 row: Tier T3, RATE_TABLE, STRICT, FALSE, Narrative substance |

## Sources NOT Used (provided but not applicable)

| Source File | Reason |
|-------------|--------|
| `_PriceSources/Assumed_Project_Parameters.csv` (most rows) | Parameters are construction/site-related; not directly applicable to DEL-04-03 production cost |

## Parsing Notes

- Professional_Staff_Rates.csv: 30 roles; 2 used for this deliverable (R-02, R-15)
- Level_of_Effort.csv: 67 rows total; 2 rows matched to DEL-04-03
- All source files parsed without errors
- All rates and hours are MEDIUM confidence (PARAMETRIC/MARKET basis)
