# Source Index

## Price Sources Used

### PS-01: Professional_Staff_Rates.csv

- **Path:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv`
- **Source Type:** Rate Table
- **Items:** 30 roles with hourly rates in CAD
- **Basis:** MARKET (Alberta 2024 market data)
- **Confidence:** MEDIUM (+/-20-30%)
- **Roles used for DEL-03-01:**
  - R-02 Project Manager: $175/hr
  - R-03 Design Manager: $165/hr
- **Parsing notes:** Standard CSV; clean parse; no issues
- **What it supports:** Hourly rates for all proposal production roles
- **What it cannot support:** Actual firm rates (parametric market proxies only)

### PS-02: Level_of_Effort.csv

- **Path:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv`
- **Source Type:** Rate Table (hours component)
- **Items:** 65 rows across 21 deliverables; 2 rows for DEL-03-01
- **Basis:** PARAMETRIC (planning estimates based on comparable $15-20M municipal DB proposals)
- **Confidence:** MEDIUM (+/-20-30%)
- **Rows used for DEL-03-01:**
  - DEL-03-01 / R-03 Design Manager: 10 hours
  - DEL-03-01 / R-02 Project Manager: 4 hours
- **Parsing notes:** Standard CSV; clean parse; no issues
- **What it supports:** Estimated hours per role per deliverable
- **What it cannot support:** Actual tracked effort; firm-specific productivity

### PS-03: Assumed_Project_Parameters.csv

- **Path:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv`
- **Source Type:** Reference Parameters
- **Items:** 29 parameters
- **Relevance to DEL-03-01:** PP-04 (proposal preparation duration: 6 weeks) provides context for total effort budget. No parameters directly price DEL-03-01 line items.
- **Parsing notes:** Standard CSV; clean parse; no issues

## Dependency Evidence (read-only, not pricing evidence)

- **Path:** `PKG-05_Delivery Plan (Design Methodology + Docs Plan)/1_Working/DEL-03-01_DesignMethodologyNarrative/Dependencies.csv`
- **Usage:** Blocker detection and readiness assessment only; not used for unit rates or quantities
- **Rows:** 10 ACTIVE (3 ANCHOR, 7 EXECUTION)
