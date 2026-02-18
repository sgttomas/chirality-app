# Source Index
## DEL-01-01: ComplianceMatrixAndChecklist Estimate

---

## Purpose

This index lists all sources used to develop the estimate, classified by type and priority.

---

## Source Hierarchy

Per AGENT_ESTIMATING protocol, sources are prioritized as follows:

1. **Explicit Pricing Sources** (quotes, budgets) - None available
2. **Rate Tables / Cost Libraries** - None available
3. **Quantity Sources** (documents with counts, sizes) - Available
4. **Fallback Model** (allowances) - Used for all pricing

---

## Pricing Sources

### Explicit Pricing Sources (Priority 1)

| Source | Type | Status | Notes |
|--------|------|--------|-------|
| Vendor quotes | N/A | NOT AVAILABLE | No vendor quotes for professional services |
| Budgetary proposals | N/A | NOT AVAILABLE | Not applicable |

### Rate Tables (Priority 2)

| Source | Location | Status | Notes |
|--------|----------|--------|-------|
| Project rate tables | `_Estimates/_RateTables/` | EMPTY | Folder exists but contains no rate tables |

### Quantity Sources (Priority 3)

| Source | Location | Used For | Priority |
|--------|----------|----------|----------|
| Datasheet.md | DEL-01-01 folder | Requirement counts, addenda counts, structure | PRIMARY |
| Specification.md | DEL-01-01 folder | Detailed requirement tables, scope definition | PRIMARY |
| Guidance.md | DEL-01-01 folder | Work approach, principles, considerations | SECONDARY |
| Procedure.md | DEL-01-01 folder | Task steps, effort drivers, verification points | PRIMARY |
| _CONTEXT.md | DEL-01-01 folder | Deliverable metadata, acceptance criteria | SECONDARY |

### Fallback Model (Priority 4)

| Source | Used For | Notes |
|--------|----------|-------|
| AGENT_ESTIMATING default model | Labour rates, contingency method | Used for all pricing |
| Industry typical ratios | Effort per requirement, maintenance factor | Parametric estimates |

---

## Quantity Sources - Detail

### Datasheet.md Extractions

| Data Point | Value | Used In |
|------------|-------|---------|
| RFP Sections covered | 4 (Sections 6, 7, 8, 9) | Scope definition |
| Section 6 requirements | 1 mandatory | Line L-001 qty basis |
| Section 7 subsections | 22 | Line L-001 qty basis |
| Section 8 evaluation criteria | 6 | Line L-001 qty basis |
| Section 9 subsections | 22 | Line L-001 qty basis |
| Total requirements | ~51 | Line L-001 qty basis |
| Addenda tracked | 3 (01, 02, 03) | Line L-002 scope |
| Addendum 01 items | 2 | Line L-002 qty basis |
| Addendum 02 items | 1 | Line L-002 qty basis |
| Addendum 03 items | 21 | Line L-002 qty basis |
| Total addendum items | 24 | Line L-002 qty basis |
| High-risk items | 8 | Line L-003 qty basis |
| Packages to coordinate | 9 | Line L-005 qty basis |

### Specification.md Extractions

| Data Point | Value | Used In |
|------------|-------|---------|
| REQ-01 through REQ-13 | 13 requirements | Scope confirmation |
| Pass/fail risk items table | 8 items | Line L-003 qty basis |
| Addenda integration detail | 24 items mapped | Line L-002 validation |
| Milestone reviews | 3 (50%, 90%, final) | Lines L-006 through L-008 |

### Procedure.md Extractions

| Data Point | Value | Used In |
|------------|-------|---------|
| Step count | 17 steps | Work scope confirmation |
| Extraction steps | 7 (Steps 1-7) | Line L-001, L-002 basis |
| Verification checkpoints | 5 | Line L-010 basis |
| Records required | 4 types | Line L-011 basis |

### Guidance.md Extractions

| Data Point | Value | Used In |
|------------|-------|---------|
| Living document principle | Updates at milestones | Line L-009 basis |
| Considerations | 7 trade-offs | Scope understanding |
| Review cadence | Weekly + milestones | Lines L-006-L-009 basis |

---

## Source File Paths

| Document | Absolute Path |
|----------|---------------|
| _CONTEXT.md | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-01_ComplianceMatrixAndChecklist/_CONTEXT.md` |
| Datasheet.md | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-01_ComplianceMatrixAndChecklist/Datasheet.md` |
| Specification.md | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-01_ComplianceMatrixAndChecklist/Specification.md` |
| Guidance.md | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-01_ComplianceMatrixAndChecklist/Guidance.md` |
| Procedure.md | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-01_ComplianceMatrixAndChecklist/Procedure.md` |

---

## References (External)

| Document | Purpose | Status |
|----------|---------|--------|
| AGENTS.md | Agent framework rules | Read |
| AGENT_ESTIMATING.md | Estimating protocol | Read |
| Decomposition document | Project structure | Referenced in documents |

---

## Source Quality Assessment

| Source Type | Availability | Quality | Impact on Estimate |
|-------------|--------------|---------|-------------------|
| Quotes | NOT AVAILABLE | N/A | Forces allowance method |
| Rate Tables | NOT AVAILABLE | N/A | Forces allowance method |
| Quantity Sources | AVAILABLE | HIGH | Good basis for scope |
| Fallback Model | USED | MEDIUM | All pricing by allowance |

---

## Document Control

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-01-01_2026-02-04_1322 |
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
