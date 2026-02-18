# Source Index

## Price Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `test/execution-6b/_PriceSources/Professional_Staff_Rates.csv` | Rate Table | 30 roles with RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence. All rates in CAD. Basis = MARKET for all professional roles. | Unit rates for all staff roles. Used R-23 ($130/hr) and R-02 ($175/hr) for DEL-07-05. |
| 2 | `test/execution-6b/_PriceSources/Level_of_Effort.csv` | Rate Table (hours) | 73 rows covering all 38 deliverables in execution-6b. Each row = (Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes). Basis = PARAMETRIC for all rows. | Hour quantities per role per deliverable. Used 2 rows for DEL-07-05: R-23 (8 hr), R-02 (4 hr). |
| 3 | `test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv` | Reference Parameters | 29 parameters covering duration, area, quantity, and financial assumptions. Not directly used for DEL-07-05 pricing but provides project context. | Background reference only for DEL-07-05. Not used for line item pricing. |

## Dependency Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 4 | `DEL-07-05/Dependencies.csv` | Dependency Register (v3.1) | 13 ACTIVE rows (3 ANCHOR, 10 EXECUTION). All SatisfactionStatus = TBD. | Blocker/readiness assessment. No estimate-blocking dependencies identified. |

## Sources NOT Used for Pricing

- `Assumed_Project_Parameters.csv`: provides project-level context (construction duration, building areas, financial estimates) but no data directly applicable to DEL-07-05 line item pricing.
- `Dependencies.csv`: used for blocker assessment only; not pricing evidence per AGENT_ESTIMATING invariant.
