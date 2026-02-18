# Source Index -- EST_DEL-08-01_2026-02-18_1400

## Price Sources

### PS-01: Professional_Staff_Rates.csv
- **Path:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv`
- **Type:** Rate table
- **Content:** 30 professional roles with hourly rates in CAD
- **Basis:** MARKET (Alberta 2024 market data)
- **Confidence:** MEDIUM
- **Parsing notes:** CSV with headers; RoleID, Role, Category, HourlyRate_CAD columns used for pricing
- **Supports:** Unit rates for all line items (R-17 Scheduler $130/hr, R-02 PM $175/hr, R-15 CM $155/hr)

### PS-02: Level_of_Effort.csv
- **Path:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv`
- **Type:** Rate table (effort quantities)
- **Content:** 65 rows mapping DeliverableID x RoleID to estimated hours
- **Basis:** PARAMETRIC (comparable proposal efforts for $15-20M municipal DB projects)
- **Confidence:** MEDIUM
- **Parsing notes:** CSV with headers; filtered to Execution=6c, DeliverableID=DEL-08-01; yields 3 rows
- **Supports:** Quantities (hours) for all line items (R-17: 20hr, R-02: 8hr, R-15: 4hr)

### PS-03: Assumed_Project_Parameters.csv
- **Path:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv`
- **Type:** Parameter table
- **Content:** 29 project-level parameters (durations, areas, quantities, financial estimates)
- **Basis:** Mixed (ASSUMPTION, DESIGN_BASIS, CONFIRMED, DERIVED, PARAMETRIC)
- **Confidence:** Mixed (LOW to HIGH)
- **Parsing notes:** CSV with headers; provides context parameters but no direct pricing inputs for DEL-08-01 line items
- **Supports:** Contextual validation only -- PP-01 through PP-04 confirm project duration assumptions that inform schedule scope

---

## Dependency Evidence (read-only, not used for pricing)

### Dependencies.csv (DEL-08-01)
- **Path:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-08_Schedule & Milestones/1_Working/DEL-08-01_DetailedProjectSchedule/Dependencies.csv`
- **Type:** Dependency register
- **Content:** 11 ACTIVE rows (3 ANCHOR, 8 EXECUTION)
- **Used for:** Blocker/readiness assessment only (not pricing evidence per invariant)

---

## Decomposition (read-only)

### Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md
- **Path:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md`
- **Type:** Decomposition output
- **Used for:** Stable IDs (PKG-08, DEL-08-01), deliverable name/definition, SOW/OBJ traceability
