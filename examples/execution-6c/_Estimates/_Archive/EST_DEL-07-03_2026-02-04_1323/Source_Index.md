# Source Index

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-07-03_2026-02-04_1323 |
| **Deliverable** | DEL-07-03 Appendix I - Subtrade and Consultant List |

---

## Source Discovery Summary

| Source Category | Available | Used | Notes |
|-----------------|-----------|------|-------|
| Vendor Quotes | No | No | No quotes for proposal preparation services |
| Rate Tables | No | No | `_Estimates/_RateTables/` directory empty |
| Deliverable Documents | Yes | Yes | Primary source for scope and requirements |
| Decomposition | Yes | Yes | Project context and scope items |
| Historical Data | No | No | No prior estimate snapshots available |

---

## Source Priority (Applied)

| Priority | Source Type | Status | Application |
|----------|-------------|--------|-------------|
| 1 | Vendor Quotes / Budgetary Quotes | NOT AVAILABLE | Would provide actual pricing for proposal preparation services |
| 2 | Project Rate Tables | NOT AVAILABLE | Would provide standard labor rates |
| 3 | Deliverable Documents (Qty sources) | USED | Scope definition from 4 documents |
| 4 | Fallback Model (Allowances) | USED | All line items priced via allowances |

---

## Primary Pricing Sources

### Source 1: Deliverable Documents (Scope Definition)

| Document | Location | Relevance | Used For |
|----------|----------|-----------|----------|
| _CONTEXT.md | DEL-07-03 folder | Deliverable definition, acceptance criteria | Scope boundaries |
| Datasheet.md | DEL-07-03 folder | Attributes, conditions, format requirements | Scope complexity |
| Specification.md | DEL-07-03 folder | Requirements REQ-01 through REQ-08 | Work scope definition |
| Guidance.md | DEL-07-03 folder | Purpose, principles, considerations | Qualitative scope |
| Procedure.md | DEL-07-03 folder | 10-step production process | Activity breakdown for line items |

### Source 2: Decomposition Document

| Document | Location | Relevance | Used For |
|----------|----------|-----------|----------|
| Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md | _Decomposition/ | Project context, SOW-007, OBJ-006, Addendum 03 impacts | Project scope context |

### Source 3: Allowance Basis (Fallback)

| Allowance Basis | Description | Confidence |
|-----------------|-------------|------------|
| Labor Rate Assumptions | PM @ CAD 150/hr, Admin @ CAD 85/hr | LOW |
| Effort Estimates | Per-step effort based on procedure complexity | LOW |
| Team Size Assumption | 25-30 firms to document | MEDIUM |

---

## Quantity Sources

| Quantity Type | Source | Evidence | Confidence |
|---------------|--------|----------|------------|
| Number of Procedure Steps | Procedure.md | 10 steps documented | HIGH |
| Number of Disciplines | Specification.md REQ-02 | 12+ major disciplines | HIGH |
| Number of Specialty Systems | Specification.md REQ-02, Decomposition Section 4 | 6 specialty systems per Addendum 03 | HIGH |
| Assumed Team Size | Guidance.md Example 1 | 25-30 firms inferred | MEDIUM |
| Labor Hours | ASSUMPTION | Based on procedure complexity | LOW |

---

## Sources NOT Available

| Source Type | Expected Location | Impact | Resolution |
|-------------|-------------------|--------|------------|
| Vendor Quotes | N/A | Cannot validate pricing | Track actuals for future calibration |
| Rate Tables | `_Estimates/_RateTables/` | Must use assumed rates | Provide rate tables for future runs |
| Historical Data | `_Estimates/_Archive/` | Cannot benchmark effort | Build history from this estimate |
| RFP Appendix I Template | _Sources/ (in RFP PDF) | Template effort uncertain | Extract template to confirm format |

---

## Source-to-Line Item Mapping

| Line ID | Primary Source | SourceRef |
|---------|----------------|-----------|
| L-001 | Procedure.md Step 1 | A-006 |
| L-002 | Procedure.md Step 2 | A-007 |
| L-003 | Procedure.md Step 3, Spec REQ-02 | A-008 |
| L-004 | Procedure.md Step 3, Guidance Principle 4 | A-009 |
| L-005 | Procedure.md Step 3, Decomposition Section 4 | A-010 |
| L-006 | Procedure.md Step 3, Spec REQ-05 | A-011 |
| L-007 | Procedure.md Step 4 | A-012 |
| L-008 | Procedure.md Step 5, Decomposition Section 4 | A-013 |
| L-009 | Procedure.md Step 6, Spec REQ-08 | A-014 |
| L-010 | Procedure.md Step 7 | A-015 |
| L-011 | Procedure.md Step 8, Spec REQ-07 | A-016 |
| L-012 | Procedure.md Step 9 | A-017 |
| L-013 | Procedure.md Step 10 | A-018 |

---

## Recommendations for Source Improvement

| Priority | Recommendation | Expected Impact |
|----------|----------------|-----------------|
| 1 | Provide labor rate tables to `_RateTables/` | Replace A-001, A-002 with actual rates |
| 2 | Track actual hours on this deliverable | Calibrate effort estimates for future |
| 3 | Obtain proposal preparation quotes if outsourcing | Replace allowances with quotes |
| 4 | Archive this estimate for future benchmarking | Build historical database |
