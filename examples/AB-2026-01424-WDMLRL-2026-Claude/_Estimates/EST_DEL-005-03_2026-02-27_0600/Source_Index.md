# Source Index — EST_DEL-005-03_2026-02-27_0600

## Indexed Price Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-1 | Professional_Staff_Rates.csv | PARAMETRIC (rate table) | 25 roles with hourly rates in CAD; all PARAMETRIC basis; MEDIUM confidence | Unit rates for professional staff hours — Civil Engineer (R-17 $160/hr); BIM Technician (R-13 $95/hr); Project Manager (R-01 $165/hr); Cost Estimator (R-08 $135/hr) |
| PS-2 | Level_of_Effort.csv | PARAMETRIC (hours model) | LOE estimates by deliverable and role; DEL-005-03 has 4 rows: R-01 (6 hr), R-08 (4 hr), R-13 (36 hr), R-17 (84 hr) | Hours allocation for DEL-005-03 — total 130 hours across 4 roles |
| PS-3 | Assumed_Project_Parameters.csv | PARAMETRIC (context parameters) | 18 project parameters; establishes project identity; facility size (~13,000 sqft); currency CAD | Context for parametric model; does not directly provide unit rates |
| PS-4 | Professional_Design_Fees.csv | PARAMETRIC (fee percentages) | 5 discipline fee ranges as % of construction value; Civil (DF-05): 0.6%–1.5% recommended 1.0% | Alternative fee-based pricing method; not used as primary method for this run because LOE-based pricing is more granular for a single deliverable |

## Source Coverage Assessment

| Item Category | Primary Source | Coverage |
|---|---|---|
| Civil Engineer design hours | PS-2 (LOE) + PS-1 (rates) | FULL — 84 hours at $160/hr |
| BIM Technician drawing production hours | PS-2 (LOE) + PS-1 (rates) | FULL — 36 hours at $95/hr |
| Project Manager coordination hours | PS-2 (LOE) + PS-1 (rates) | FULL — 6 hours at $165/hr |
| Cost Estimator support hours | PS-2 (LOE) + PS-1 (rates) | FULL — 4 hours at $135/hr |
| Material/equipment costs | None | NOT APPLICABLE — DEL-005-03 is a design deliverable (drawing set); no material procurement |
| Construction costs | None | NOT APPLICABLE — construction is PKG-018 scope |
| Subconsultant fees | None | NOT COVERED — if any subconsultant engagement is needed (e.g., environmental assessment for landfill-adjacent stormwater), it is not priced here |

## Notes

- The parametric LOE model (PS-2) provides the primary hours basis for DEL-005-03. Combined with hourly rates from PS-1, this yields a fully priced estimate for professional design effort.
- Professional_Design_Fees.csv (PS-4) provides a cross-check: Civil discipline fee at 1.0% of construction value. This is noted for context but not used as the primary pricing method for this deliverable-level estimate (LOE is more granular).
- No construction material or equipment costs apply to this deliverable — DEL-005-03 is a design output (drawing set).
