# Source Index — EST_DEL-02-02_2026-02-18_2024

**Snapshot:** EST_DEL-02-02_2026-02-18_2024
**Date:** 2026-02-18

---

## Price Sources Used

### PS-01: Professional_Staff_Rates.csv

| Field | Value |
|-------|-------|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv |
| **Source Type** | Rate Table |
| **Items** | 30 roles with hourly rates in CAD |
| **Roles matched to DEL-02-02** | 8 of 30 (R-02, R-04, R-05, R-07, R-09, R-11, R-13, R-27) |
| **Rate Basis** | MARKET (Alberta 2024 parametric market rates) |
| **Confidence** | MEDIUM (all matched roles) |
| **Parsing Notes** | CSV with header row; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes |
| **Supports** | UnitRate for all 8 Detail.csv line items |
| **Cannot Support** | N/A — all required roles present |

### PS-02: Level_of_Effort.csv

| Field | Value |
|-------|-------|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv |
| **Source Type** | Rate Table (quantity dimension — hours per role per deliverable) |
| **Items** | 65 rows total (21 deliverables x applicable roles) |
| **Rows matched to DEL-02-02** | 8 rows (rows 20-27 in file, where Execution=6c and DeliverableID=DEL-02-02) |
| **LOE Basis** | PARAMETRIC (planning estimates based on comparable proposal efforts) |
| **Confidence** | MEDIUM (all matched rows; +/-20-30% accuracy per INDEX.md) |
| **Parsing Notes** | CSV with header row; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes |
| **Supports** | Qty (hours) for all 8 Detail.csv line items |
| **Cannot Support** | N/A — all required rows present |

### PS-03: Assumed_Project_Parameters.csv

| Field | Value |
|-------|-------|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv |
| **Source Type** | Parameters (project-level assumptions) |
| **Items** | 29 parameters |
| **Used for DEL-02-02** | Context only — PP-04 (proposal preparation duration: 6 weeks) confirms timeframe; PP-05 through PP-08 (building areas) confirm scope calibration context for design brief content |
| **Confidence** | MEDIUM (project parameters) |
| **Parsing Notes** | CSV with header row; columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes |
| **Supports** | Scope calibration context (no direct line item pricing) |
| **Cannot Support** | Direct unit rates or quantities (not its purpose) |

---

## Dependency Sources Used (non-pricing; readiness/blockers only)

### DEP-01: Dependencies.csv (DEL-02-02)

| Field | Value |
|-------|-------|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-04_Design Proposal (Concept + Design Brief)/1_Working/DEL-02-02_DesignBriefNarrative/Dependencies.csv |
| **Items** | 19 ACTIVE rows (7 ANCHOR + 12 EXECUTION) |
| **Used for** | Blocker identification and readiness assessment |
| **Key findings** | No estimate-blocking dependencies identified; upstream prerequisites are document inputs (RFP, addenda, geotech report) and DEL-02-01 concept development — these affect production sequencing, not pricing evidence |

### DEP-02: _DEPENDENCIES.md (DEL-02-02)

| Field | Value |
|-------|-------|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-04_Design Proposal (Concept + Design Brief)/1_Working/DEL-02-02_DesignBriefNarrative/_DEPENDENCIES.md |
| **Used for** | Narrative summary of dependency register; cross-check of Dependencies.csv |

---

## Decomposition Source

| Field | Value |
|-------|-------|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md |
| **Version** | v1.0 (Phase 7 Publish) |
| **DEL-02-02 entry** | Section 8 — PKG-04, Output: Design Brief narrative, Acceptance: addresses 7.1.2 requirements |
| **SOW mapping** | SOW-010, SOW-011, SOW-013, SOW-014, SOW-015 (from Scope Ledger Section 10) |

---

## Source Coverage Summary

| Detail.csv Column | Source File | Coverage |
|--------------------|------------|----------|
| UnitRate | Professional_Staff_Rates.csv | 8/8 lines (100%) |
| Qty (hours) | Level_of_Effort.csv | 8/8 lines (100%) |
| WBS_PackageID | Decomposition | 8/8 lines (100%) |
| WBS_DeliverableID | Decomposition | 8/8 lines (100%) |
| CBS | Deterministic mapping from rates Category | 8/8 lines (100%) |
| SourceRef | Dual-source reference (rates + LOE) | 8/8 lines (100%) |
