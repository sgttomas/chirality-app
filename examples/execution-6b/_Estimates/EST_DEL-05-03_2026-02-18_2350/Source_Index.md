# Source Index

| # | Source File | Source Type | Parsing Notes | What It Supports |
|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | Rate Table | 30 role rows; CSV; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes | Provides hourly rate for R-11 (Mechanical Engineer Senior) = $160/hr CAD. MARKET basis, MEDIUM confidence. |
| 2 | Level_of_Effort.csv | Rate Table (Hours) | 73 rows across all deliverables; CSV; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes | Provides estimated hours for DEL-05-03: R-11 = 8 hours. PARAMETRIC basis. Single role assignment for this deliverable. |
| 3 | Assumed_Project_Parameters.csv | Parameter Table | 29 parameter rows; CSV; columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes | Reference context only. No parameters directly used for DEL-05-03 pricing. Provides project-level context (building areas, construction value estimates) but DEL-05-03 is a narrative deliverable priced by professional hours, not by construction parameters. |

## Source Coverage Assessment

- **DEL-05-03 pricing** is fully supported by sources 1 and 2.
- Source 1 provides the unit rate ($/hr).
- Source 2 provides the quantity (hours).
- Source 3 is informational context only -- no direct pricing contribution to DEL-05-03.
- No gaps requiring fallback or TBD amounts.
