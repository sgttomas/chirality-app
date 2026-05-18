# Source Index — EST_DEL-007-01_2026-02-27_0546

## Pricing Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|-----------|------------|--------------|----------|
| 1 | Professional_Staff_Rates.csv | Rate Table | 25 roles with RoleID, hourly rates in CAD, PARAMETRIC basis, MEDIUM confidence. Parsed successfully; all rows well-formed. | Hourly rate lookup for all professional staff roles. Directly supports unit rate pricing for labour items. |
| 2 | Level_of_Effort.csv | Parametric Model (hours allocation) | Multi-deliverable LOE table. 3 rows matched for DEL-007-01: R-01 (6 hr), R-08 (4 hr), R-19 (70 hr). PARAMETRIC basis. | Hour quantities for each role per deliverable. Primary quantity source for design/management labour items. |
| 3 | Assumed_Project_Parameters.csv | Parametric Context | 19 project parameters (identity, location, facility, schedule, equipment, currency). No direct pricing data; provides context parameters for parametric models. | Context only. Currency confirmed as CAD (PP-17). Building area ~13,000 sqft (PP-10). |
| 4 | Professional_Design_Fees.csv | Parametric Model (fee percentages) | 5 discipline fee ranges as percentages of construction value. Does NOT include a Landscape Architect line. Disciplines covered: Architecture, Structural, Mechanical, Electrical, Civil. | Not directly applicable to DEL-007-01. No Landscape Architect fee percentage available. Design effort priced via LOE + staff rates instead. |

## Source Coverage Assessment

- **DEL-007-01 is a design-phase deliverable** (Design Presentation type). All priceable work is professional labour.
- **Full coverage achieved** via Level_of_Effort.csv (quantities in hours) cross-referenced with Professional_Staff_Rates.csv (unit rates in CAD/hr).
- **Professional_Design_Fees.csv** is not applicable: no Landscape Architect fee line exists, and the fee-percentage method requires a construction value base which is not relevant for pricing a single preliminary design deliverable.
- **Assumed_Project_Parameters.csv** provides context but no direct pricing inputs for this deliverable.

## Source Gaps

None identified for DEL-007-01. All 3 labour line items have both quantity (from LOE) and rate (from staff rates) with full traceability.
