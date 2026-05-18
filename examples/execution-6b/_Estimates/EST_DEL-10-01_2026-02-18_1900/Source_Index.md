# Source Index

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | 30 roles; CSV with RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes | Hourly rates by role for all professional, management, construction, administrative, and specialty staff |
| 2 | `_PriceSources/Level_of_Effort.csv` | Rate Table (hours) | 73 rows; CSV with Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes | Hours by role per deliverable; 2 rows match DEL-10-01 (R-02: 10 hrs; R-15: 4 hrs) |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Parametric / Reference | 29 parameters; CSV with ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes | Project-level parameters (areas, quantities, durations, financial estimates); not directly used for DEL-10-01 pricing but provides context |

## Decomposition Source

| Source | Version | Status | Notes |
|---|---|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | v2.3 FINAL | Accepted | Provides DEL-10-01 definition, package assignment (PKG-010), scope item mapping (SOW-0028), and objective tracing (OBJ-008) |

## Dependency Source

| Source | Rows | Notes |
|---|---|---|
| `DEL-10-01/Dependencies.csv` | 12 rows | Schema v3.1; loaded via AUTO; provides upstream prerequisites and downstream interfaces |

## Sources NOT Used for Pricing

- `Assumed_Project_Parameters.csv`: Referenced for context (e.g., PP-24 total construction value for risk magnitude calibration) but no direct pricing derivation from this file for DEL-10-01.
- Dependency registers: Used for blocker/readiness analysis only (per invariant: "Dependencies are not pricing evidence").
