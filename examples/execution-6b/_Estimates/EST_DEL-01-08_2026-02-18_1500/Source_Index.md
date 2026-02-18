# Source Index

## Pricing Sources

| # | Source File | Source Type | What It Supports | Parsing Notes |
|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | RATE_TABLE | Hourly rates by role (31 roles); columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes | Clean CSV; all rates in CAD; Basis = MARKET; Confidence = MEDIUM for all staff roles |
| 2 | Level_of_Effort.csv | RATE_TABLE (hours) | Estimated hours by deliverable and role; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes | Clean CSV; filtered to Execution=6b; Basis = PARAMETRIC for all rows; 2 rows match DEL-01-08 |
| 3 | Assumed_Project_Parameters.csv | REFERENCE | Project-level parameters (areas, quantities, durations, financial estimates); not directly used for DEL-01-08 pricing but reviewed for context | Clean CSV; 29 parameters; provides context on project scale but no direct pricing input for this deliverable |

## Decomposition Source

| Source | Version | Status | Usage |
|---|---|---|---|
| Penhold_PSB_Project_Decomposition_v2.md | v2.3 FINAL | ACCEPTED | Package/deliverable ID validation; scope item mapping (SOW-0017); objective mapping (OBJ-006) |

## Dependency Source

| Source | Schema | Rows | Usage |
|---|---|---|---|
| DEL-01-08/Dependencies.csv | v3.1 | 8 dependencies | Blocker/readiness assessment; upstream prerequisites (DEL-01-07, DEL-01-09); downstream handover (DEL-01-02); interface dependency (DEL-01-09) |

## Sources NOT Used

- No quotes, historical datasets, parametric models, or allowance tables were provided or needed for this deliverable.
- Assumed_Project_Parameters.csv was reviewed but contains no direct pricing inputs for DEL-01-08.
