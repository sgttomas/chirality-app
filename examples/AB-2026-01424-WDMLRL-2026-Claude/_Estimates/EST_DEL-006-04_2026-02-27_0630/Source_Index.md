# Source Index — EST_DEL-006-04_2026-02-27_0630

## Pricing Sources Indexed

### Source 1 — Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv |
| **Type** | PARAMETRIC (rate table) |
| **Format** | CSV with columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes |
| **Records** | 25 roles (R-01 through R-25) |
| **Supports** | Unit rates (CAD/hr) for all professional staff roles; used to price ITEM-001 through ITEM-004 |
| **Confidence** | MEDIUM (all rates) |
| **Parsing Notes** | Clean CSV; all rates are in CAD; basis is PARAMETRIC for all entries |

**Roles Used for DEL-006-04:**

| RoleID | Role | HourlyRate_CAD |
|---|---|---|
| R-01 | Project Manager | 165 |
| R-08 | Cost Estimator | 135 |
| R-13 | BIM Technician | 95 |
| R-18 | Plumbing Engineer | 160 |

### Source 2 — Level_of_Effort.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv |
| **Type** | PARAMETRIC (effort allocation model) |
| **Format** | CSV with columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes |
| **Records** | Multiple rows per deliverable; 4 rows for DEL-006-04 |
| **Supports** | Hour quantities for each role assigned to DEL-006-04 |
| **Confidence** | MEDIUM (basis = PARAMETRIC) |
| **Parsing Notes** | Filtered to DEL-006-04 rows: R-01 (6 hr), R-08 (4 hr), R-13 (21 hr), R-18 (49 hr) |

### Source 3 — Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv |
| **Type** | PARAMETRIC (parameter table) |
| **Format** | CSV with columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes |
| **Records** | 20 parameters (PP-01 through PP-20) |
| **Supports** | Project context parameters (cistern volume 50,000 L per PP-14; currency CAD per PP-17); not directly used for line-item pricing but confirms project context |
| **Confidence** | HIGH to MEDIUM depending on parameter |
| **Parsing Notes** | Key parameters: PP-14 (Cistern Volume = 50,000 L, CONFIRMED, HIGH); PP-17 (Currency = CAD, ASSUMPTION, MEDIUM) |

### Source 4 — Professional_Design_Fees.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv |
| **Type** | PARAMETRIC (fee percentage model) |
| **Format** | CSV with columns: ItemID, Discipline, Description, FeePercentMin, FeePercentMax, RecommendedPercent, FeeBase, Basis, Confidence, Notes |
| **Records** | 5 discipline fee entries (DF-01 through DF-05) |
| **Supports** | Alternative fee-based pricing approach; NOT used for this estimate (LOE-based approach preferred for DEL-006-04 as a single deliverable within a package) |
| **Confidence** | MEDIUM |
| **Parsing Notes** | Not applied. LOE (hours x rates) is the primary pricing method for this deliverable. Fee percentage model would require construction_value base which is outside the scope of a single design deliverable estimate. |

## Source Coverage Summary

| Item Category | Source Available | Pricing Method |
|---|---|---|
| Professional staff hours (ITEM-001 to ITEM-004) | Level_of_Effort.csv + Professional_Staff_Rates.csv | PARAMETRIC (hours x rate) |
| Drawing/design activities (ITEM-005 to ITEM-019) | Covered by staff-hour LOE (ITEM-001 to ITEM-004) | Not separately priced — these are deliverable sub-activities encompassed by the staff-hour allocation |

## Gaps

- Professional_Design_Fees.csv not used (alternative pricing method available but not applied; LOE approach is more granular for single-deliverable scope).
- No external printing, plotting, or reproduction costs in price sources.
- No travel/site visit costs in price sources (rural site near Ferintosh, Alberta).
