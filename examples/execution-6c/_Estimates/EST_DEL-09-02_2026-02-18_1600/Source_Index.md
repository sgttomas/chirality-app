# Source Index -- EST_DEL-09-02_2026-02-18_1600

## Indexed Price Sources

### PS-1: Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv |
| **Source Type** | Rate Table |
| **Items** | 30 roles (RoleID R-01 through R-30) |
| **Applicable to DEL-09-02** | R-02 (Project Manager, $175/hr), R-07 (Civil Engineer Senior, $155/hr), R-29 (Geotechnical Engineer, $155/hr) |
| **Parsing Notes** | CSV; clean parse; all rates in CAD; Confidence=MEDIUM for applicable roles |
| **Supports** | UnitRate derivation for all 3 line items |
| **Cannot Support** | N/A -- all required roles present |

### PS-2: Level_of_Effort.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv |
| **Source Type** | Rate Table (hours allocation) |
| **Items** | 65 rows total; 3 rows for DEL-09-02 |
| **Applicable to DEL-09-02** | R-02: 8h, R-07: 6h, R-29: 4h (total 18 hours) |
| **Parsing Notes** | CSV; clean parse; Execution=6c filter applied; Basis=PARAMETRIC for all applicable rows |
| **Supports** | Quantity (hours) derivation for all 3 line items |
| **Cannot Support** | N/A -- all required hours present |

### PS-3: Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv |
| **Source Type** | Parametric reference data |
| **Items** | 29 parameters (PP-01 through PP-29) |
| **Applicable to DEL-09-02** | Context only -- PP-09 (12-acre site), PP-10 (4.5-acre developed area) provide scope context but do not directly drive pricing for proposal production cost |
| **Parsing Notes** | CSV; clean parse |
| **Supports** | Contextual validation of scope parameters |
| **Cannot Support** | Direct pricing -- no unit rates or hours for DEL-09-02 in this file |

---

## Source Coverage Assessment

| Metric | Value |
|---|---|
| Line items requiring rate evidence | 3 |
| Line items with rate evidence found | 3 |
| Coverage | 100% |
| Sources with parsing issues | 0 |
