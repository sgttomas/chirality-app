# Source Index

## Price Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | Rate Table | 30 roles; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes | Unit rates ($/hr) for all staff roles; Basis = MARKET; Confidence = MEDIUM for all priced roles |
| 2 | Level_of_Effort.csv | Rate Table (hours) | 73 rows across all deliverables; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes | Hour quantities per role per deliverable; Basis = PARAMETRIC for all rows |
| 3 | Assumed_Project_Parameters.csv | Parametric Parameters | 29 parameters; columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes | Project-level assumptions (areas, quantities, durations, financial estimates); NOT directly used for DEL-01-07 pricing but provides context |

## Decomposition Source

| Source File | Version | Status | Used For |
|---|---|---|---|
| Penhold_PSB_Project_Decomposition_v2.md | v2.3 FINAL | FINAL ACCEPTED | Package IDs, deliverable IDs, scope item mappings, objective traceability |

## Dependency Source

| Source File | Used For |
|---|---|
| DEL-01-07_DesignBuildFirmExperienceProfile/Dependencies.csv | Blocker/readiness assessment; 11 dependency rows; 2 PENDING external prerequisites identified |

## Source Limitations

- Professional_Staff_Rates.csv rates are marked MARKET / MEDIUM confidence -- not firm-specific contracted rates.
- Level_of_Effort.csv hours are marked PARAMETRIC basis -- professional judgment estimates, not historical actuals.
- Assumed_Project_Parameters.csv was not directly used for DEL-01-07 line-item pricing (no direct cost driver from project parameters applies to this qualifications narrative deliverable).
