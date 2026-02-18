# Source Index
## DEL-08-01: DetailedProjectSchedule

---

## Purpose

This index catalogues all source documents used to develop the estimate, organized by priority and type.

---

## Primary Sources (Scope Definition)

### 1. Deliverable Documents (Four Documents)

| Document | Path | Usage |
|----------|------|-------|
| **_CONTEXT.md** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-08_Schedule & Milestones/1_Working/DEL-08-01_DetailedProjectSchedule/_CONTEXT.md` | Deliverable ID, name, description, anticipated artifacts, acceptance criteria |
| **Datasheet.md** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-08_Schedule & Milestones/1_Working/DEL-08-01_DetailedProjectSchedule/Datasheet.md` | Schedule attributes, activity count (50-150), duration constraints, milestone list |
| **Specification.md** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-08_Schedule & Milestones/1_Working/DEL-08-01_DetailedProjectSchedule/Specification.md` | REQ-SCH-000 through REQ-SCH-012, verification methods, evaluation framework |
| **Guidance.md** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-08_Schedule & Milestones/1_Working/DEL-08-01_DetailedProjectSchedule/Guidance.md` | Duration benchmarks (18-24 months), long-lead items, commissioning duration, Alberta climate considerations |
| **Procedure.md** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-08_Schedule & Milestones/1_Working/DEL-08-01_DetailedProjectSchedule/Procedure.md` | 10-step production process, WBS structure, cross-deliverable coordination steps, QA requirements |

---

### 2. Project-Level Documents

| Document | Path | Usage |
|----------|------|-------|
| **Decomposition Document** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md` | Project scope, DEL-08-01 acceptance criteria, Addendum 03 impacts, OBJ-009 objectives |

---

## Pricing Sources

### 3. Rate Tables

| Source | Path | Status | Usage |
|--------|------|--------|-------|
| **Project Rate Tables** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Estimates/_RateTables/` | EMPTY | No rate data available; fallback to allowances |

### 4. Vendor Quotes

| Source | Status | Usage |
|--------|--------|-------|
| **Vendor Quotes** | NOT AVAILABLE | Professional services deliverable; no vendor quotes applicable |

### 5. Allowance Basis

| Source | Basis | Usage |
|--------|-------|-------|
| **Labour Rates** | Market assumptions for Alberta consulting rates | Scheduler $125/hr, Senior PM $150/hr, Technical Lead $140/hr |
| **Effort Estimates** | Parametric based on typical proposal development | Hours per activity type extrapolated from scope |

---

## Quantity Sources

### 6. Explicit Quantities Extracted

| Quantity | Value | Source Document | Section |
|----------|-------|-----------------|---------|
| Schedule Activities | 50-150 EA | Datasheet.md | Schedule Structure |
| Project Phases | 6 EA | Procedure.md | Step 3.1 |
| Key Milestones | 12-15 EA | Specification.md | C-006 |
| Specification Requirements | 13 EA | Specification.md | REQ-SCH-000 to REQ-SCH-012 |
| Cross-Deliverable Interfaces | 5 EA | Procedure.md | Step 6 |
| Project Duration Target | 18-24 months | Guidance.md | Trade-off 1 |
| Long-Lead Items | 5-10 EA | Guidance.md | Consideration 4 |
| Commissioning Duration | 10-12 weeks | Guidance.md | Consideration 5 |

---

## Referenced But Not Accessible

| Document | Reference | Impact |
|----------|-----------|--------|
| **RFP Section 7.1.9** | Multiple TBD references in four documents | Schedule format and software requirements unknown; inferred from decomposition |
| **Addendum 01** | Datasheet.md references | Timeline context not accessible; minimal impact |
| **Addendum 03** | Datasheet.md, Specification.md, Guidance.md, Procedure.md | Key impacts (survey post-award, pickled sand removal) documented in decomposition |
| **Historical Project Data** | Guidance.md, Procedure.md references | Duration benchmarking; assumed firm has comparable project records |

---

## Agent Instructions

| Document | Path | Usage |
|----------|------|-------|
| **AGENTS.md** | `/Users/ryan/ai-env/projects/chirality-app-test/AGENTS.md` | Framework context, agent index |
| **AGENT_ESTIMATING.md** | `/Users/ryan/ai-env/projects/chirality-app-test/agents/AGENT_ESTIMATING.md` | Estimating agent protocol, spec, structure |

---

## Source Priority Summary

| Priority | Source Type | Availability | Usage |
|----------|-------------|--------------|-------|
| 1 | Vendor Quotes | NOT AVAILABLE | - |
| 2 | Rate Tables | NOT AVAILABLE | - |
| 3 | Historical Data | ASSUMED AVAILABLE | Duration benchmarking (not directly accessed) |
| 4 | Deliverable Documents | AVAILABLE | Primary scope and quantity source |
| 5 | Allowances | APPLIED | All pricing |

---

## Document Control

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-08-01_2026-02-04_1323 |
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
