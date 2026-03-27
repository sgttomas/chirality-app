# Source Index -- EST_DEL-001-01_2026-03-26_1759

| Source File | Type | Rows Used | Supports | Parsing Notes |
|---|---|---|---|---|
| Professional_Staff_Rates.csv | Rate Table | R-01, R-08, R-11, R-12, R-13 | Staff hourly rates for all 5 line items | 25 roles; 5 used for this deliverable. All MEDIUM confidence, PARAMETRIC basis. |
| Level_of_Effort.csv | Rate Table (quantities) | DEL-001-01/R-01, R-08, R-11, R-12, R-13 | Base hours allocation per role | 5 rows for DEL-001-01. PARAMETRIC basis. Base hours adjusted per DEC-001. |
| Assumed_Project_Parameters.csv | Parameters | PP-10 (floor area), PP-17 (currency) | Cross-check parameters | 18 rows total; 2 referenced for context. |
| Professional_Design_Fees.csv | Parametric (cross-check) | DF-01 | Parametric cross-check of total vs fee percentage | Not used for pricing; used for reasonableness validation. |
| Parametric_Building_Rates.csv | Parametric (cross-check) | PB-01 | Construction value estimate for fee cross-check | Not used for pricing; used for reasonableness validation. |
| CBS_Taxonomy.csv | Taxonomy | CBS-01, CBS-02 | CBS code assignment | 29 L2 categories; 2 used for this deliverable. |

## Sources Not Used

| Source File | Reason |
|---|---|
| Fees_Permits_Insurance.csv | No permit/insurance items in DEL-001-01 scope |
| All other PriceSources files | Not applicable to professional design LOE costing |
