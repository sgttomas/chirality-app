# Source Index — EST_DEL-006-05_2026-02-27_0546

## Price Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | Professional_Staff_Rates.csv | Rate Table (parametric) | 25 roles with hourly rates in CAD; Basis = PARAMETRIC; Confidence = MEDIUM for all entries | Hourly rates for all professional staff roles; directly supports unit rate pricing for design labour |
| PS-02 | Level_of_Effort.csv | Parametric Model (LOE) | Deliverable-level labour hours by role; 4 rows matched for DEL-006-05 (R-01: 6 hr, R-08: 4 hr, R-13: 21 hr, R-18: 49 hr); Basis = PARAMETRIC | Estimated hours per role per deliverable; primary quantity source for design effort items |
| PS-03 | Assumed_Project_Parameters.csv | Parametric Context | 19 parameters covering identity, location, contract, schedule, facility, equipment, plumbing, currency, economics; Confidence varies HIGH to MEDIUM | Context parameters for parametric pricing (e.g., PP-15 confirms 2,000 US gal septic tank; PP-17 confirms CAD currency) |
| PS-04 | Professional_Design_Fees.csv | Parametric Model (fee %) | 5 discipline-level fee percentages as % of construction value; no plumbing-specific row | Not directly applicable to DEL-006-05 (no plumbing-specific design fee row; no construction value basis available for this deliverable). Not used for pricing in this run. |

## Coverage Assessment

- **DEL-006-05** is a **Drawing Set** deliverable (Plumbing Engineer design output). The priceable scope is professional design labour.
- **PS-01 (Staff Rates)** and **PS-02 (Level of Effort)** together provide complete coverage for pricing the 4 identified labour line items.
- **PS-03 (Project Parameters)** confirms scope parameters (tank capacity, currency) but does not directly price items.
- **PS-04 (Design Fees)** does not include a plumbing-specific row and is not used. The Level_of_Effort approach (hours x rate) is the primary pricing method per the PARAMETRIC basis.

## Sources NOT Used

| Source | Reason |
|---|---|
| Professional_Design_Fees.csv | No plumbing-specific fee row; LOE-based pricing is more precise for this deliverable |
