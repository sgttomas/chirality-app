# Source Index

## Indexed Price Sources

### Source 1: Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv |
| **Source Type** | Rate Table |
| **Items** | 30 roles (R-01 through R-30) |
| **Parsing Notes** | CSV with headers: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes |
| **Supports** | All professional staff hourly rates for proposal production costing |
| **Used for DEL-01-01** | R-22 (Proposal Coordinator / Writer) at $105/hr CAD; Category = Administrative; Confidence = MEDIUM; Basis = MARKET |

### Source 2: Level_of_Effort.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv |
| **Source Type** | Rate Table (hours per role per deliverable) |
| **Items** | 67 rows across 21 deliverables for execution 6c |
| **Parsing Notes** | CSV with headers: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes |
| **Supports** | Hour quantities for all proposal production deliverables |
| **Used for DEL-01-01** | 1 row: R-22 at 8 hours; Basis = PARAMETRIC; Notes = "Same scope as 6b DEL-01-01" |

### Source 3: Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv |
| **Source Type** | Parameters (project-level assumptions) |
| **Items** | 29 parameters (PP-01 through PP-29) |
| **Parsing Notes** | CSV with headers: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes |
| **Supports** | Project timeline, building areas, quantities, financial parameters for scope calibration |
| **Used for DEL-01-01** | PP-04 (Proposal preparation duration = 6 weeks) provides context for the LOE estimate. No direct pricing impact on this deliverable. |

---

## Source Coverage Assessment

| Deliverable | Sources Available | Pricing Completeness |
|---|---|---|
| DEL-01-01 | Professional_Staff_Rates.csv + Level_of_Effort.csv | 100% -- all line items have rate table evidence |
