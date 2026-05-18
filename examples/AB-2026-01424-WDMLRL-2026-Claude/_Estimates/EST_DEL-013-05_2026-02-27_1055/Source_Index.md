# Source Index

## Price Sources Indexed

| Source File | Source Type | Parsing Notes | Supports | Limitations |
|---|---|---|---|---|
| Professional_Staff_Rates.csv | Rate Table (PARAMETRIC) | 25 roles with hourly CAD rates; all PARAMETRIC basis, MEDIUM confidence | Professional/management labour pricing for ITM-016 through ITM-021 | Rates are parametric estimates, not firm quotes |
| Level_of_Effort.csv | Parametric Model | 6 rows matched to DEL-013-05; provides hour allocations by role | Hour quantities for management/oversight roles allocated to this deliverable | Hours are parametric estimates; Notes column shows "PKG-013 TBD -- TBD" indicating some uncertainty |
| Assumed_Project_Parameters.csv | Parametric Model | 19 project parameters; key for DEL-013-05: PP-11 ceiling height 35ft, PP-10 floor area ~13,000 sqft | Building context parameters for system sizing context | Does not directly price mechanical systems |
| Mechanical_System_Rates.csv | Rate Table (ALLOWANCE) | 6 mechanical items; MS-05 directly applies to welding exhaust system; MS-06 for ductwork | MS-05: Welding station exhaust/vent system complete installed, RecommendedRate $8,000/EA (range $4,500-$12,000, ALLOWANCE, LOW confidence). MS-06: Ductwork installed at $60/m2 normalized per floor area | MS-05 is ALLOWANCE basis with LOW confidence; significant range uncertainty. MS-06 normalized per floor area not directly applicable to a single-station exhaust duct run |
| Construction_Labour_Rates.csv | Rate Table (PARAMETRIC) | 10 trades with hourly and fully burdened rates; T-06 HVAC Sheet Metal at $91.20/hr fully burdened | Installation labour pricing for mechanical trade work | Rates are parametric; labour hours for installation are estimated |
| Equipment_Pricing.csv | Rate Table (ALLOWANCE) | 3 equipment items (cranes, pressure washer, compressor) | No direct applicability to DEL-013-05 welding exhaust | Does not contain welding exhaust equipment pricing |

## Key Pricing Evidence Applied

- **MS-05** (Mechanical_System_Rates.csv): Welding station exhaust/vent system, $8,000 EA recommended. This is the primary parametric rate for the complete system equipment and materials (ITM-001 through ITM-009 bundled).
- **T-06** (Construction_Labour_Rates.csv): HVAC Sheet Metal worker at $91.20/hr fully burdened. Applied to installation labour estimate.
- **R-15** (Professional_Staff_Rates.csv): Mechanical Engineer at $165/hr. Applied to design engineering effort.
- **R-23** (Professional_Staff_Rates.csv): Commissioning Agent at $160/hr. Applied to testing and commissioning effort.
- **R-01, R-02, R-03, R-05, R-06, R-08** (Professional_Staff_Rates.csv + Level_of_Effort.csv): Management and oversight roles with allocated hours per Level_of_Effort.csv.
