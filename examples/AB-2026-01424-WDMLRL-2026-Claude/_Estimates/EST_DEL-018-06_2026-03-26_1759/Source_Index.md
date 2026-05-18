# Source Index -- EST_DEL-018-06_2026-03-26_1759

| Source File | Type | Rows Used | Supports | Parsing Notes |
|---|---|---|---|---|
| Professional_Staff_Rates.csv | Rate Table | R-01, R-02, R-03, R-05, R-06, R-08 | Staff hourly rates for 6 professional services line items | 25 roles; 6 used for this deliverable. All MEDIUM confidence. |
| Level_of_Effort.csv | Rate Table (quantities) | DEL-018-06/R-01, R-02, R-03, R-05, R-06, R-08 | Base hours allocation per role | 6 rows for DEL-018-06. Base hours adjusted per DEC-002 for SOW-0122. |
| Construction_Labour_Rates.csv | Rate Table | T-04, T-05, T-07, T-08 | Trade labour fully-burdened rates for 6 construction labour line items | 10 trades; 4 used. All MEDIUM confidence. |
| Earthwork_Civil_Rates.csv | Rate Table | EC-01, EC-02 | Excavation and backfill rates | 4 rows; 2 used. MEDIUM confidence. |
| Underground_Utility_Rates.csv | Rate Table | UU-01, UU-03 | Underground conduit and piping installed rates | 5 rows; 2 used. UU-01 used as proxy for gas piping (LOW confidence for that application). |
| Electrical_System_Rates.csv | Rate Table | (not directly used for line items) | Referenced for context on electrical service scope | ES-03 referenced for service allowance range validation. |
| Fees_Permits_Insurance.csv | Rate Table | (not directly used) | Referenced for permit fee context | FP-05, FP-10 referenced for reasonableness checks. |
| CBS_Taxonomy.csv | Taxonomy | CBS-02, CBS-05, CBS-17, CBS-22, CBS-23, CBS-24, CBS-25, CBS-28, CBS-29 | CBS code assignment | 29 L2 categories; 9 used for this deliverable. |
| Assumed_Project_Parameters.csv | Parameters | PP-17 (currency) | Currency confirmation | CAD confirmed. |

## Sources Not Used

| Source File | Reason |
|---|---|
| Professional_Design_Fees.csv | No design fee items in DEL-018-06 scope |
| Parametric_Building_Rates.csv | Not applicable to utility tie-in costing |
| Building_Envelope_Rates.csv | Not applicable |
| Structural_Concrete_Rates.csv | Not applicable |
| Interior_Architectural_Rates.csv | Not applicable |
| Mechanical_System_Rates.csv | Not applicable |
| Equipment_Pricing.csv | Not applicable |
| Geotechnical_Investigation_Rates.csv | Not applicable |
| Paving_Surfacing_Rates.csv | Not applicable |
| Optional_Items_Pricing.csv | Not applicable |
