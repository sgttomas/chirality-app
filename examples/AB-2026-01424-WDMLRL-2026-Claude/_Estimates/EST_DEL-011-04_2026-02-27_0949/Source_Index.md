# Source Index — EST_DEL-011-04_2026-02-27_0949

## Price Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | Professional_Staff_Rates.csv | Rate Table | 25 roles with RoleID, HourlyRate_CAD, Category. All rates PARAMETRIC basis. | Professional staff hourly rates for LOE pricing (L-013) |
| PS-02 | Level_of_Effort.csv | Parametric Model | Multi-deliverable LOE table. 6 rows matched for DEL-011-04: R-01 (6h), R-02 (8h), R-03 (10h), R-05 (4h), R-06 (6h), R-08 (4h). Total 38 hrs. | Professional staff hours for DEL-011-04 (L-013) |
| PS-03 | Assumed_Project_Parameters.csv | Parametric Parameters | 18 parameters. Key for this deliverable: PP-10 (Floor area ~13,000 sqft), PP-11 (Ceiling height 35 ft), PP-17 (Currency CAD). | Context parameters for quantity assumptions |
| PS-04 | Structural_Concrete_Rates.csv | Rate Table | 8 items. No direct applicability to doors/entrances. | Not used for this deliverable |
| PS-05 | Building_Envelope_Rates.csv | Rate Table | 6 items. BE-04 (Man door, insulated steel, $1,300/EA) directly applicable. BE-05 (Flashing/trim/sealants) provides context. | Door supply pricing (L-001); hardware context |
| PS-06 | Construction_Labour_Rates.csv | Rate Table | 10 trades with fully burdened rates. T-01 Carpenter ($80.60/hr FB) is primary trade for door installation. | Labour pricing for installation activities (L-004 through L-012) |
| PS-07 | Equipment_Pricing.csv | Rate Table | 3 items (cranes, wash bay, compressor). No direct applicability to doors/entrances. | Not used for this deliverable |

## Source Coverage Assessment

- **Directly supported:** Door unit supply rate (BE-04), construction labour rates (T-01), professional staff rates and hours (LOE + staff rates)
- **Parametrically derived:** Hardware set pricing, accessibility upgrade, caulking materials, temporary protection materials, fire-rated door allowance
- **Not supported by sources:** Exact door quantity (TBD in Datasheet), specific hardware pricing, fire-rating cost, installation productivity rates (assumed parametrically)
