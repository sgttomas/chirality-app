# Source Index — EST_DEL-001-05_2026-02-27_0545

## Indexed Price Sources

| # | Source File | Source Type | What It Supports | Parsing Notes |
|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | Rate Table | Hourly rates by role (R-01 through R-25); used for unit rate pricing of labour line items | 25 roles; all CAD; PARAMETRIC basis; MEDIUM confidence |
| 2 | Level_of_Effort.csv | Parametric Model | Estimated hours per deliverable per role; DEL-001-05 rows provide hours for 5 roles (R-01, R-08, R-11, R-12, R-13) | 577 total rows; filtered to DEL-001-05 = 5 rows; PARAMETRIC basis |
| 3 | Assumed_Project_Parameters.csv | Parameter Table | Project identity, location, facility parameters, currency assumption | 18 parameters; used for context validation (currency = CAD, building area ~13,000 sqft) |
| 4 | Professional_Design_Fees.csv | Parametric Model | Alternative fee-based pricing method (% of construction value); not used as primary method for this run | 5 discipline fee entries; DF-01 Architecture = 4.5% recommended; available as cross-check only |
| 5 | Parametric_Building_Rates.csv | Parametric Model | Overall building cost cross-check rate ($/sqft); not directly applicable to design-only deliverable | 2 entries; PB-01 industrial $285/sf recommended; used only for cross-check commentary |

## Sources Not Used (available in PriceSources but not in PRICE_SOURCES list for this run)

| Source File | Reason Not Used |
|---|---|
| Interior_Architectural_Rates.csv | Contains construction material rates (partitions, finishes, ceilings, flooring, millwork); not applicable to design effort pricing for a drawing set deliverable |
| Building_Envelope_Rates.csv | Construction scope; not applicable to design deliverable |
| Construction_Labour_Rates.csv | Construction trade rates; not applicable to design deliverable |
| Earthwork_Civil_Rates.csv | Civil construction; not applicable |
| Electrical_System_Rates.csv | Electrical construction; not applicable |
| Equipment_Pricing.csv | Major equipment; not applicable |
| Fees_Permits_Insurance.csv | Bonding/permits; not applicable to individual drawing set |
| Mechanical_System_Rates.csv | Mechanical construction; not applicable |
| Optional_Items_Pricing.csv | Optional scope; not applicable |
| Paving_Surfacing_Rates.csv | Civil construction; not applicable |
| Structural_Concrete_Rates.csv | Structural construction; not applicable |
| Underground_Utility_Rates.csv | Civil construction; not applicable |

## Key Source Linkages

| Detail.csv LineID | Primary Source | Secondary Source |
|---|---|---|
| L-001 | Level_of_Effort.csv (DEL-001-05, R-11, 54 hrs) | Professional_Staff_Rates.csv (R-11, $180/hr) |
| L-002 | Level_of_Effort.csv (DEL-001-05, R-12, 42 hrs) | Professional_Staff_Rates.csv (R-12, $135/hr) |
| L-003 | Level_of_Effort.csv (DEL-001-05, R-13, 24 hrs) | Professional_Staff_Rates.csv (R-13, $95/hr) |
| L-004 | Level_of_Effort.csv (DEL-001-05, R-01, 6 hrs) | Professional_Staff_Rates.csv (R-01, $165/hr) |
| L-005 | Level_of_Effort.csv (DEL-001-05, R-08, 4 hrs) | Professional_Staff_Rates.csv (R-08, $135/hr) |
| L-006 | Level_of_Effort.csv (embedded in L-001 to L-005) | — |
| L-007 | Level_of_Effort.csv (embedded in L-004) | — |
| L-008 | Level_of_Effort.csv (embedded in L-001) | — |
| L-009 | Level_of_Effort.csv (embedded in L-001, L-002) | — |
| L-010 | No pricing basis available | Assumptions_Log.md ASM-004 |
