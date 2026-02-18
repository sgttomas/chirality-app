# Source Index: EST_DEL-05-01_2026-02-18_1400

## Source Files Used

| # | File | Path | Source Type | Items Used | Lines Referencing |
|---|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | _PriceSources/ | Rate Table | R-02 ($175/hr), R-18 ($145/hr), R-19 ($115/hr) | L-001, L-002, L-003 |
| 2 | Level_of_Effort.csv | _PriceSources/ | Hours Estimate | DEL-05-01 rows: R-18 (40h), R-19 (24h), R-02 (8h) | L-001, L-002, L-003 |
| 3 | Assumed_Project_Parameters.csv | _PriceSources/ | Parameters | PP-05 (18000 sf), PP-07 (6000 sf), PP-10 (4.5 ac), PP-11 through PP-20, PP-21 through PP-25 | L-010 through L-041 |
| 4 | Structural_Concrete_Rates.csv | _PriceSources/ | Construction Rates | SC-01 through SC-15 | L-011 |
| 5 | Building_Envelope_Rates.csv | _PriceSources/ | Construction Rates | BE-01 through BE-15 | L-012 |
| 6 | Interior_Architectural_Rates.csv | _PriceSources/ | Construction Rates | IA-01 through IA-25 | L-013 |
| 7 | Mechanical_System_Rates.csv | _PriceSources/ | Construction Rates | MS-01 through MS-14 | L-014 |
| 8 | Electrical_System_Rates.csv | _PriceSources/ | Construction Rates | ES-01 through ES-14 | L-015 |
| 9 | Earthwork_Civil_Rates.csv | _PriceSources/ | Construction Rates | EC-01 through EC-11 | L-016 |
| 10 | Paving_Surfacing_Rates.csv | _PriceSources/ | Construction Rates | PS-01 through PS-09 | L-016 |
| 11 | Underground_Utility_Rates.csv | _PriceSources/ | Construction Rates | UU-01 through UU-12 | L-017 |
| 12 | Equipment_Pricing.csv | _PriceSources/ | Equipment Pricing | EQ-01 through EQ-15 | L-018, L-019 |
| 13 | Optional_Items_Pricing.csv | _PriceSources/ | Optional Items | OPT-01 through OPT-18 | L-030 through L-035 |
| 14 | Parametric_Building_Rates.csv | _PriceSources/ | Parametric Cross-Check | PB-01 through PB-09 | L-018, Summary cross-check |
| 15 | Construction_Labour_Rates.csv | _PriceSources/ | Labour Rates | T-01 through T-15 | Not directly referenced (embedded in construction rates) |
| 16 | Professional_Design_Fees.csv | _PriceSources/ | Fee Percentages | DF-01 through DF-08 | L-020 |
| 17 | Fees_Permits_Insurance.csv | _PriceSources/ | Fees/Permits/Insurance | FP-01 through FP-19 | L-017, L-021, L-022 |

All files located under: `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/`

---

## Sources NOT Used (available but not applicable to DEL-05-01)

None. All 17 provided PRICE_SOURCES were used for either direct pricing or cross-checking.

---

## Source Quality Assessment

| Category | Basis | Confidence | Count of Lines |
|---|---|---|---|
| Production cost (staff rates + LOE) | RATE_TABLE (market-based hourly rates x parametric hours) | MEDIUM | 3 |
| Construction content (structure, envelope, MEP, site) | PARAMETRIC (unit rates x estimated quantities) | LOW-MEDIUM | 12 |
| Optional items | PARAMETRIC (equipment + system pricing) | LOW | 6 |
| FF&E allowance (OPT-18) | ALLOWANCE (fixed amount per OI-004) | HIGH | 1 |

---

## Key Source Dependencies and Limitations

1. **No vendor quotes**: All construction rates are parametric Alberta 2024 market estimates. No formal quotes from suppliers, subtrades, or specialty contractors have been obtained.
2. **Quantities are estimated**: Building areas, utility run lengths, and material quantities are planning estimates derived from the functional program and site parameters. Actual quantities will be determined during detailed design.
3. **Rate ranges available but midpoint used**: Most construction rate sources provide min/max/recommended. The recommended rate (typically near midpoint) is used throughout.
4. **Percentage-based items sensitive to base value**: General requirements (15%), design fees (9%), and bonds/insurance/permits are calculated as percentages of base construction value. Changes to base value cascade to these items.
