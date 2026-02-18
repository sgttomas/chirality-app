# Source Index
## DEL-04-02: Budget Control and Change Management Plan

---

## Source Classification

Sources are classified by priority per AGENT_ESTIMATING protocol:

1. **Explicit Pricing Sources** (highest priority): Vendor quotes, budgetary quotes, proposals
2. **Rate Tables / Cost Libraries**: Project rate tables in _RateTables/
3. **Quantity Sources**: Datasheets, specifications, procedures
4. **Embedded Fallback Model** (lowest priority): Allowances with assumptions

---

## Sources Discovered

### Explicit Pricing Sources

| Source | Type | Status | Notes |
|--------|------|--------|-------|
| Vendor quotes | Quote | NOT FOUND | No vendor quotes available for professional services |
| Budgetary quotes | Quote | NOT FOUND | N/A for plan document development |

---

### Rate Tables / Cost Libraries

| Source | Type | Status | Notes |
|--------|------|--------|-------|
| `_RateTables/` folder | Rate Table | NOT FOUND | Folder does not exist or is empty |
| Project rate tables | Rate Table | NOT FOUND | No project-specific rates available |

---

### Quantity Sources (Primary)

| Source | Path | Type | Content Used |
|--------|------|------|--------------|
| Datasheet.md | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-06_Construction Methodology + Administration/1_Working/DEL-04-02_BudgetControlAndChangeManagementPlan/Datasheet.md` | Quantity | Deliverable attributes, conditions, plan scope |
| Specification.md | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-06_Construction Methodology + Administration/1_Working/DEL-04-02_BudgetControlAndChangeManagementPlan/Specification.md` | Quantity | 12 requirements (REQ-1 through REQ-12); verification criteria |
| Guidance.md | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-06_Construction Methodology + Administration/1_Working/DEL-04-02_BudgetControlAndChangeManagementPlan/Guidance.md` | Quantity | Principles, considerations, trade-offs, examples |
| Procedure.md | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-06_Construction Methodology + Administration/1_Working/DEL-04-02_BudgetControlAndChangeManagementPlan/Procedure.md` | Quantity | 15 steps; plan structure (7 sections, 4 templates); verification checkpoints |
| _CONTEXT.md | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-06_Construction Methodology + Administration/1_Working/DEL-04-02_BudgetControlAndChangeManagementPlan/_CONTEXT.md` | Quantity | Deliverable identity, acceptance criteria, scope traceability |

---

### Fallback Model (Used)

| Source | Type | Content Used |
|--------|------|--------------|
| AGENT_ESTIMATING.md | Protocol | Default CBS categories, contingency method (PCT_BY_BUCKET), rounding policy |
| Professional rate assumptions | Allowance | $140/hr CM, $130/hr Commercial Lead, $150/hr PM, $100/hr Technical Staff |
| Effort assumptions | Allowance | Section drafting 4-8 hrs; template development 2-3 hrs; review cycles |

---

## Source-to-Line Item Mapping

### Quantity Extraction Summary

| Source | Section | Quantity Extracted | Line Items |
|--------|---------|-------------------|------------|
| Procedure.md | Step 3 | 7 plan sections | L-001 through L-007 |
| Procedure.md | Step 3 | 4 templates | L-008 through L-011 |
| Specification.md | REQ-5 | Pricing methodology support | L-012 |
| Specification.md | REQ-9 | Appendix H consistency verification | L-013 |
| Specification.md | REQ-10 | Addenda integration review | L-014 |
| Procedure.md | Step 9 | Internal review (3 reviewers) | L-016, L-017, L-018 |
| Procedure.md | Step 10 | Formatting and finalization | L-019 |
| Procedure.md | Step 12 | Validation walkthrough | L-020 |

### Pricing Source Summary

| Method | Source | Line Items | Amount |
|--------|--------|------------|--------|
| ALLOWANCE | A-001 (CM rate) | L-001 through L-007, L-014, L-016 | $6,160 |
| ALLOWANCE | A-002 (Commercial Lead rate) | L-008 through L-013, L-017 | $2,080 |
| ALLOWANCE | A-003 (PM rate) | L-015, L-018, L-020 | $1,200 |
| ALLOWANCE | A-011 (Technical Staff rate) | L-019 | $200 |
| ALLOWANCE | D-004 (Contingency) | L-021, L-022 | $1,247 |

---

## Sources Not Accessible

| Source | Status | Impact |
|--------|--------|--------|
| RFP Section 7 | PDF not accessible | Detailed requirements TBD; scope uncertainty |
| Addendum 03 | PDF not accessible | Detailed clarifications TBD |
| Rate tables | Not provided | All pricing by allowance |

---

## Pricing Basis Selection Decisions

| Decision | Selection | Rationale |
|----------|-----------|-----------|
| D-003 | CBS mapping to E + PM | Document type (Plan) maps to professional services categories |
| D-004 | 15% contingency | No rate tables; moderate uncertainty from RFP TBD items |

---

## Document Control

| Property | Value |
|----------|-------|
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
| **Sources Indexed** | 8 (5 quantity sources, 0 rate tables, 0 quotes, 3 fallback) |
