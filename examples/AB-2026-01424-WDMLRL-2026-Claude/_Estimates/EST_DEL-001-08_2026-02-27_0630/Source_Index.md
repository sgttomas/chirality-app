# Source Index — EST_DEL-001-08_2026-02-27_0630

## Indexed Price Sources

| # | Source File | Source Type | What It Supports | Parsing Notes |
|---|---|---|---|---|
| 1 | PriceSources/Professional_Staff_Rates.csv | PARAMETRIC | Hourly rates for 25 professional roles (R-01 through R-25) in CAD. Used to price labour line items by role. | CSV; 27 rows incl. header; all rates marked PARAMETRIC with MEDIUM confidence. |
| 2 | PriceSources/Level_of_Effort.csv | PARAMETRIC | Estimated hours by role per deliverable. DEL-001-08 has 5 role assignments: R-01 (6 hr), R-08 (4 hr), R-11 (18 hr), R-12 (14 hr), R-13 (8 hr). Total 50 hrs. | CSV; rows filtered to DEL-001-08. All entries marked PARAMETRIC. |
| 3 | PriceSources/Assumed_Project_Parameters.csv | PARAMETRIC | 18 project parameters including facility area (~13,000 sq ft), ceiling height (35 ft), crane count (2), cistern volume (50,000 L), currency (CAD). Used for context validation; not directly used for pricing DEL-001-08. | CSV; 19 rows incl. header. |
| 4 | PriceSources/Professional_Design_Fees.csv | PARAMETRIC | Design fee percentages by discipline (Architecture 4.5%, Structural 1.8%, Mechanical 1.6%, Electrical 1.6%, Civil 1.0%). Not directly applied to DEL-001-08 — LOE-based pricing used instead. | CSV; 6 rows incl. header. Could serve as cross-check against total design package cost. |
| 5 | PriceSources/Parametric_Building_Rates.csv | PARAMETRIC | Building cost rates per sf (Industrial shop $285/sf recommended; Wash Bay increment $70/sf). Not directly applied to DEL-001-08 design cost — these are construction cost benchmarks. | CSV; 3 rows incl. header. Used for overall project cost context only. |

## Source Coverage for DEL-001-08

- **Primary pricing mechanism:** Level of Effort (hours by role) x Professional Staff Rates (hourly rate by role) = PARAMETRIC labour cost.
- **All 5 Detail.csv line items** are priced using Sources 1 and 2 (Staff Rates + LOE). 100% coverage.
- Sources 3, 4, and 5 provide project context but are not directly used for line-item pricing on this deliverable.
- No quotes, historical data, or allowance tables were needed for this scope.

## What Sources Cannot Support

- Material or product costs for finish materials (this deliverable is the design document, not the construction cost of installing finishes).
- Specialty consultant fees for code review or occupancy classification (not broken out in LOE; assumed included in Senior Architect hours).
- County aesthetic review meeting costs (assumed included in PM and Senior Architect LOE).
