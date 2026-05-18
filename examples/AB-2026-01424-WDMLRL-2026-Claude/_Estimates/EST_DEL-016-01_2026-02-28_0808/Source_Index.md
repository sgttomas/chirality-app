# Source Index — EST_DEL-016-01_2026-02-28_0808

## Indexed Price Sources

### Source 1: Professional_Staff_Rates.csv

| Field | Value |
|-------|-------|
| **Path** | .../PriceSources/Professional_Staff_Rates.csv |
| **Type** | Rate table (PARAMETRIC) |
| **Parsing Notes** | CSV with 25 rows; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes |
| **Supports** | Professional staff cost line items (PM, CPM, Site Superintendent, QA/QC Lead, HSE Manager, Cost Estimator) |
| **Cannot Support** | Equipment procurement pricing, construction trade labour, material costs |

### Source 2: Level_of_Effort.csv

| Field | Value |
|-------|-------|
| **Path** | .../PriceSources/Level_of_Effort.csv |
| **Type** | Parametric model (estimated hours by deliverable + role) |
| **Parsing Notes** | CSV; filtered to DEL-016-01 rows: 6 rows covering R-01 (PM, 6 hr), R-02 (CPM, 8 hr), R-03 (Site Super, 10 hr), R-05 (HSE, 4 hr), R-06 (QA/QC, 6 hr), R-08 (Cost Estimator, 4 hr) |
| **Supports** | Professional staff hour estimates for DEL-016-01 |
| **Cannot Support** | Equipment pricing, construction trade labour hours, material costs |

### Source 3: Assumed_Project_Parameters.csv

| Field | Value |
|-------|-------|
| **Path** | .../PriceSources/Assumed_Project_Parameters.csv |
| **Type** | Parametric model (project parameters) |
| **Parsing Notes** | CSV with 19 rows; key parameters for this deliverable: PP-12 (2 cranes), PP-13 (5 ton capacity), PP-11 (35 ft ceiling) |
| **Supports** | Confirms crane quantity and capacity for pricing |
| **Cannot Support** | Direct pricing; provides parameters only |

### Source 4: Equipment_Pricing.csv

| Field | Value |
|-------|-------|
| **Path** | .../PriceSources/Equipment_Pricing.csv |
| **Type** | Allowance table |
| **Parsing Notes** | CSV with 4 rows; EQ-01: "Overhead crane, 5 ton class (supply + install)" — PriceMin $120,000, PriceMax $280,000, RecommendedPrice $190,000, Quantity_Assumed 2, Basis ALLOWANCE, Confidence LOW; EQ-04: "Anti-collision system for 2 overhead cranes (shared runway)" — PriceMin $15,000, PriceMax $35,000, RecommendedPrice $25,000, Quantity_Assumed 1, Basis ALLOWANCE, Confidence LOW |
| **Supports** | Crane equipment supply and install pricing (EQ-01); anti-collision system pricing (EQ-04) |
| **Cannot Support** | Breakdown of supply vs. install; commissioning costs; professional staff costs |
| **Note** | EQ-01 is marked as supply + install combined. EQ-04 is conditional on shared runway configuration. Both are LOW confidence. |

### Source 5: Construction_Labour_Rates.csv

| Field | Value |
|-------|-------|
| **Path** | .../PriceSources/Construction_Labour_Rates.csv |
| **Type** | Rate table (PARAMETRIC) |
| **Parsing Notes** | CSV with 10 rows; relevant trades: T-03 (Ironworker, $92.80/hr fully burdened), T-04 (Electrician, $96.00/hr fully burdened), T-08 (Labourer, $65.10/hr fully burdened) |
| **Supports** | Construction trade labour rates for installation activities |
| **Cannot Support** | Equipment procurement pricing, professional staff costs, trade labour hours (hours must be estimated parametrically) |
