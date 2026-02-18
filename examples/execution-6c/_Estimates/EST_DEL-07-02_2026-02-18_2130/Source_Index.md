# Source Index — EST_DEL-07-02_2026-02-18_2130

## Indexed Price Sources

### 1. Professional_Staff_Rates.csv

- **Path:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv`
- **Source type:** Rate table
- **Items:** 30 roles (R-01 through R-30)
- **Parsing notes:** CSV with columns RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes
- **Relevant rows for DEL-07-02:**
  - R-22 (Proposal Coordinator / Writer): $105/hr, Category=Administrative, Confidence=MEDIUM
  - R-26 (HR Coordinator): $85/hr, Category=Administrative, Confidence=MEDIUM
- **What it supports:** Hourly unit rates for all proposal production roles
- **What it cannot support:** Quantities/hours (those come from Level_of_Effort.csv)

### 2. Level_of_Effort.csv

- **Path:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv`
- **Source type:** Rate table (level-of-effort hours)
- **Items:** 65 rows across 21 deliverables
- **Parsing notes:** CSV with columns Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes
- **Relevant rows for DEL-07-02:**
  - DEL-07-02 / R-26 (HR Coordinator): 12 hours, Basis=PARAMETRIC
  - DEL-07-02 / R-22 (Proposal Coordinator / Writer): 8 hours, Basis=PARAMETRIC
- **What it supports:** Labour hour quantities per role per deliverable
- **What it cannot support:** Unit rates (those come from Professional_Staff_Rates.csv)

### 3. Assumed_Project_Parameters.csv

- **Path:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv`
- **Source type:** Parameter table (project assumptions)
- **Items:** 29 parameters (PP-01 through PP-29)
- **Parsing notes:** CSV with columns ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes
- **Relevant parameters for DEL-07-02:**
  - PP-04 (Proposal preparation duration): 6 weeks — contextual only; does not directly price line items
- **What it supports:** Context for proposal timeline and scope calibration
- **What it cannot support:** Direct pricing of DEL-07-02 line items (no resume-specific parameters)

---

## Dependency Sources (read-only, not pricing evidence)

- **Dependencies.csv:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-03_Team Qualifications (Appendix I + resumes)/1_Working/DEL-07-02_KeyTeamMembersAndResumes/Dependencies.csv`
- **Usage:** Blocker detection and readiness assessment only; not used as pricing evidence
