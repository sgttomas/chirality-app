# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-09-01_2026-02-18_2200 |
| **AsOf** | 2026-02-18T22:00:00 |
| **Scope** | DEL-09-01 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-09-01/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Resolved Paths

- **ESTIMATES_ROOT:** `test/execution-6b/_Estimates/`
- **DELIVERABLE_PATH:** `test/execution-6b/PKG-009_Schedule_and_Milestones/1_Working/DEL-09-01_DetailedProjectSchedule/`
- **Professional_Staff_Rates.csv:** `test/execution-6b/_PriceSources/Professional_Staff_Rates.csv`
- **Level_of_Effort.csv:** `test/execution-6b/_PriceSources/Level_of_Effort.csv`
- **Assumed_Project_Parameters.csv:** `test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv`
- **Dependencies.csv:** `DEL-09-01_DetailedProjectSchedule/Dependencies.csv` (12 rows; 0 blocking)

## CBS Mapping Rule

CBS codes are assigned deterministically based on the role `Category` field from `Professional_Staff_Rates.csv`:
- `Administrative` category roles -> CBS = `LABOUR.ADMIN`
- `Management` category roles -> CBS = `LABOUR.MGMT`
- `Design` category roles -> CBS = `LABOUR.DESIGN`
- `Production` category roles -> CBS = `LABOUR.PROD`
- `Construction` category roles -> CBS = `LABOUR.CONST`
- `Financial` category roles -> CBS = `LABOUR.FIN`
- `Legal` category roles -> CBS = `LABOUR.LEGAL`
- `Specialty` category roles -> CBS = `LABOUR.SPEC`
- `External` category roles -> CBS = `LABOUR.EXT`

For DEL-09-01, the roles and mappings are:
- R-17 Scheduler (Category=Construction) -> CBS = `LABOUR.CONST`
- R-02 Project Manager (Category=Management) -> CBS = `LABOUR.MGMT`
- R-15 Construction Manager (Category=Construction) -> CBS = `LABOUR.CONST`

## BOE Context (from Brief)

- **Deliverable:** DEL-09-01 -- Detailed Project Schedule (T3, Schedule + Narrative)
- **Cost Drivers:** Scheduler/PM hours; Gantt chart production; critical path analysis; schedule assumptions; design-through-closeout timeline. Scheduling software costs if applicable (PS-10: embedded in hourly rate per INDEX.md).
- **Cost Ownership:** Gantt chart + critical path + assumptions -> DEL-09-01 (NOT in DEL-07-01 construction schedule control narrative which is separate). Schedule milestone dates -> DEL-09-01 (NOT in DEL-06-02 which defines design submission milestones; schedule PLACES them in time).
- **Pricing method:** Use Level_of_Effort.csv for hours, Professional_Staff_Rates.csv for rates.
