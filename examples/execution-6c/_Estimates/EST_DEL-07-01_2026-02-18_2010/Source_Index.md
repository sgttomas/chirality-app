# Source Index — EST_DEL-07-01_2026-02-18_2010

## Indexed Price Sources

### PS-01: Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv |
| **Source Type** | Rate Table |
| **Items** | 30 roles (R-01 through R-30) |
| **Relevant Rows** | R-02 (Project Manager, $175/hr), R-22 (Proposal Coordinator / Writer, $105/hr) |
| **Parsing Notes** | CSV with header row; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes |
| **Supports** | Hourly rate lookup for all proposal production roles |
| **Cannot Support** | Quantities (hours); those come from Level_of_Effort.csv |

### PS-02: Level_of_Effort.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv |
| **Source Type** | Rate Table (effort quantities) |
| **Items** | 65 rows across 21 deliverables |
| **Relevant Rows** | Row 52: DEL-07-01 / R-22 / 16 hrs; Row 53: DEL-07-01 / R-02 / 4 hrs |
| **Parsing Notes** | CSV with header row; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes |
| **Supports** | Hour quantities per role per deliverable |
| **Cannot Support** | Rates (those come from Professional_Staff_Rates.csv) |

### PS-03: Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv |
| **Source Type** | Reference Parameters |
| **Items** | 29 parameters (PP-01 through PP-29) |
| **Relevant Rows** | PP-04 (proposal preparation duration: 6 weeks) -- context only |
| **Parsing Notes** | CSV with header row; columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes |
| **Supports** | Context for effort calibration; not directly used for pricing DEL-07-01 |
| **Cannot Support** | Direct pricing; no rates or quantities for DEL-07-01 |

---

## Dependency Sources (Read-Only, Not Pricing Evidence)

| Source | Path | Use |
|---|---|---|
| Dependencies.csv | {RUN_ROOT}/Dependencies.csv | Blocker/readiness detection only; 10 ACTIVE rows for DEL-07-01 |
| _DEPENDENCIES.md | {RUN_ROOT}/_DEPENDENCIES.md | Narrative dependency summary; confirms declared upstream/downstream |

---

## Sources Not Used

The following PRICE_SOURCES files exist in the _PriceSources/ directory but are not relevant to DEL-07-01 (a pure proposal production deliverable with no construction pricing content):

- Fees_Permits_Insurance.csv
- Structural_Concrete_Rates.csv
- Building_Envelope_Rates.csv
- Interior_Architectural_Rates.csv
- Mechanical_System_Rates.csv
- Electrical_System_Rates.csv
- Earthwork_Civil_Rates.csv
- Paving_Surfacing_Rates.csv
- Underground_Utility_Rates.csv
- Equipment_Pricing.csv
- Optional_Items_Pricing.csv
- Parametric_Building_Rates.csv
- Construction_Labour_Rates.csv
- Professional_Design_Fees.csv
