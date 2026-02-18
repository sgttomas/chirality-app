# Source Index: EST_DEL-03-02_2026-02-18_1430

## Price Sources Used

| # | Source File | Path | Source Type | What It Supports | Parsing Notes |
|---|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv | Rate Table | Hourly rates (CAD 2024) for 30 roles; MEDIUM confidence market rates | CSV; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes |
| 2 | Level_of_Effort.csv | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv | Level of Effort (hours) | Estimated hours per deliverable per role; PARAMETRIC basis | CSV; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes |
| 3 | Assumed_Project_Parameters.csv | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv | Project Parameters | Duration, area, quantity, and financial assumptions; not directly used for DEL-03-02 pricing but provides context | CSV; 29 parameters across Duration, Area, Quantity, Financial categories |

## Specific Source References in Detail.csv

| LineID | SourceRef | Source File(s) | Row(s) / Key(s) |
|---|---|---|---|
| L-01 | Professional_Staff_Rates.csv R-03 + Level_of_Effort.csv row DEL-03-02/R-03 | Professional_Staff_Rates.csv, Level_of_Effort.csv | R-03 (Design Manager, $165/hr); DEL-03-02/R-03 (10 hours) |
| L-02 | Professional_Staff_Rates.csv R-02 + Level_of_Effort.csv row DEL-03-02/R-02 | Professional_Staff_Rates.csv, Level_of_Effort.csv | R-02 (Project Manager, $175/hr); DEL-03-02/R-02 (4 hours) |

## Sources Not Used (available but not applicable)

- Assumed_Project_Parameters.csv: Provides project-level context (durations, areas, quantities, financial parameters) but DEL-03-02 is a narrative deliverable priced purely on professional hours. No parametric scaling applied.

## Dependency Evidence Sources

| Source | Path | Purpose |
|---|---|---|
| Dependencies.csv | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-05_Delivery Plan (Design Methodology + Docs Plan)/1_Working/DEL-03-02_DetailedDesignAndConstructionDocsPlan/Dependencies.csv | Dependency register (12 ACTIVE rows); used for blocker detection and readiness assessment |
| _DEPENDENCIES.md | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-05_Delivery Plan (Design Methodology + Docs Plan)/1_Working/DEL-03-02_DetailedDesignAndConstructionDocsPlan/_DEPENDENCIES.md | Dependency summary with downstream handoff notes and consumer context for TASK_ESTIMATING |

## Decomposition Source

| Source | Path | Purpose |
|---|---|---|
| Decomposition | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md | Package/deliverable ID validation; scope ledger traceability |
