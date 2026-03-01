# Source Index — EST_DEL-001-09_2026-02-27_0546

## Price Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `Professional_Staff_Rates.csv` | Rate Table | 25 rows; RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes | Hourly rates for all professional staff roles (R-01 through R-25). Used to price ITEM-001 through ITEM-005. |
| 2 | `Level_of_Effort.csv` | Parametric Model | Multi-deliverable LOE table; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. Filtered to DEL-001-09 rows. | Hour allocations per role per deliverable. DEL-001-09 has 5 role assignments (R-01, R-08, R-11, R-12, R-13) totalling 130 hours. |
| 3 | `Assumed_Project_Parameters.csv` | Parametric Model | 19 rows; project identity, location, schedule, facility, equipment, currency parameters | Context parameters (project identity, currency=CAD, facility type, schedule). Not directly used for line-item pricing but confirms currency and project identity. |
| 4 | `Professional_Design_Fees.csv` | Parametric Model | 5 rows; fee-percentage ranges by discipline against construction_value | Architectural design fee range: 3.0%–6.0% of construction value (recommended 4.5%). Not used for this estimate — LOE-based pricing is preferred for individual deliverable estimates. Available as cross-check if construction value is known. |
| 5 | `Parametric_Building_Rates.csv` | Parametric Model | 2 rows; building-level parametric rates ($/sf) | Industrial maintenance shop rate: $220–$360/sf (recommended $285/sf). Not applicable to this deliverable (design drawing set, not construction). Retained for cross-reference only. |

## Sources Not Used (with rationale)

| Source | Reason Not Used |
|---|---|
| `Building_Envelope_Rates.csv` | Construction rates — not applicable to design deliverable |
| `Construction_Labour_Rates.csv` | Construction rates — not applicable to design deliverable |
| `Earthwork_Civil_Rates.csv` | Construction rates — not applicable to design deliverable |
| `Electrical_System_Rates.csv` | Construction rates — not applicable to design deliverable |
| `Equipment_Pricing.csv` | Equipment supply — not applicable to design deliverable |
| `Fees_Permits_Insurance.csv` | Not in specified PRICE_SOURCES list |
| `Interior_Architectural_Rates.csv` | Construction rates — not applicable to design deliverable |
| `Mechanical_System_Rates.csv` | Construction rates — not applicable to design deliverable |
| `Optional_Items_Pricing.csv` | Not in specified PRICE_SOURCES list |
| `Paving_Surfacing_Rates.csv` | Construction rates — not applicable to design deliverable |
| `Structural_Concrete_Rates.csv` | Construction rates — not applicable to design deliverable |
| `Underground_Utility_Rates.csv` | Construction rates — not applicable to design deliverable |
