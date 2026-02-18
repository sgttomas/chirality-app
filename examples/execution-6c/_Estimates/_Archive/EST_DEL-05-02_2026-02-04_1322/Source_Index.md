# Source Index

## Snapshot Information

| Field | Value |
|-------|-------|
| **Snapshot ID** | EST_DEL-05-02_2026-02-04_1322 |
| **Deliverable** | DEL-05-02 AppendixH ScheduleB CostBreakdown |

---

## Source Documents (Pricing/Quantity Basis)

### Priority 1: Explicit Pricing Sources

| Source ID | Type | Location | Status | Usage |
|-----------|------|----------|--------|-------|
| (none) | Vendor Quotes | N/A | Not Available | No vendor quotes available for this estimate |

### Priority 2: Rate Tables / Cost Libraries

| Source ID | Type | Location | Status | Usage |
|-----------|------|----------|--------|-------|
| (none) | Rate Tables | _Estimates/_RateTables/ | Not Available | Directory does not exist; no rate tables provided |

### Priority 3: Quantity Sources (Deliverable Documents)

| Source ID | Type | Location | Sections Used | Usage |
|-----------|------|----------|---------------|-------|
| SRC-001 | Datasheet | DEL-05-02/Datasheet.md | Cost Categories, Additional Options, Conditions | Cost category structure; option definitions; scope constraints |
| SRC-002 | Specification | DEL-05-02/Specification.md | Requirements R-001 to R-010; Scope In/Out | Compliance requirements; scope boundaries |
| SRC-003 | Guidance | DEL-05-02/Guidance.md | Principles 1-5; Cost Allocation Considerations; Trade-offs | Cost allocation rationale; GR percentages; contingency approach |
| SRC-004 | Procedure | DEL-05-02/Procedure.md | Prerequisites; Steps 1-6 | Verification requirements; workflow dependencies |
| SRC-005 | Context | DEL-05-02/_CONTEXT.md | Description; Acceptance Criteria; Scope Traceability | Deliverable definition; pass criteria |

### Priority 4: Project Documentation

| Source ID | Type | Location | Sections Used | Usage |
|-----------|------|----------|---------------|-------|
| SRC-006 | Decomposition | _Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md | Section 4 (Addendum 03); Section 5 (Vocabulary); Section 8 (Deliverables); Section 12 (Open Issues); Section 15 (Evaluation) | Scope definition; addenda impacts; evaluation criteria |

### Priority 5: Fallback Model (Parametric)

| Source ID | Type | Basis | Usage |
|-----------|------|-------|-------|
| SRC-FALLBACK | Parametric Assumptions | Alberta municipal facility benchmarks (ASSUMPTION) | 100% of cost estimates; building $/SF; sitework $/SF; option allowances |

---

## Source Summary by Pricing Method

| Method | % of Estimate | Source IDs |
|--------|---------------|------------|
| QUOTE | 0% | None |
| RATE_TABLE | 0% | None |
| HISTORICAL | 0% | None |
| ALLOWANCE/PARAMETRIC | 100% | SRC-FALLBACK |

---

## Document Extraction Summary

### From Datasheet.md (SRC-001)
- Cost category structure: General Requirements, Building, Sitework
- Additional Options 1-6 definitions with operating cost notes
- Addendum 03 technical items requiring costing
- Scope constraints: pickled sand exclusion, 12-acre site

### From Specification.md (SRC-002)
- R-001: Template compliance (Appendix H Schedule B)
- R-004: Monitoring fee separation for Option 4
- R-005: Schedule A/B reconciliation requirement
- R-007: Scope exclusion (pickled sand storage)
- R-008: Site scope constraint (12-acre)

### From Guidance.md (SRC-003)
- General Requirements typical allocation: 8-12% of construction
- Building typical allocation: 60-70% of total cost
- Sitework typical allocation: 15-25% of total cost
- Contingency approach guidance (Principle 5)
- Trade-off analysis for granularity and contingency visibility

### From Procedure.md (SRC-004)
- Prerequisite dependencies (DEL-02-01 Concept Design)
- Verification checkpoints for estimate validation

### From _CONTEXT.md (SRC-005)
- Acceptance criteria: completeness, monitoring fee separation, Schedule A/B match

### From Decomposition (SRC-006)
- Addendum 03 scope changes (pickled sand removed, 12-acre site)
- Service tie-in allowance approach permitted
- Evaluation criteria: 35 points for Proposal Price
- Open issues: OI-003 (service tie-ins), OI-004 (FF&E treatment)

---

## Missing Sources (Gaps)

| Gap ID | Source Type | Expected Location | Impact | Resolution |
|--------|-------------|-------------------|--------|------------|
| G-001 | Appendix H Template | _Sources/ | Cannot confirm line item structure | Obtain from Proposal Manager |
| G-002 | Concept Design | DEL-02-01 | Building area/scope unknown | Complete DEL-02-01 |
| G-003 | Vendor Quotes | N/A | No firm pricing basis | Obtain budgetary quotes |
| G-004 | Rate Tables | _Estimates/_RateTables/ | 100% allowance-based | Provide firm rate tables |
| G-005 | Geotechnical Report | _Sources/ | Site conditions unknown | Obtain reference reports |
| G-006 | Addendum 03 PDF | _Sources/ | Referenced but location TBD | Confirm file location |

---

## Document Information

| Field | Value |
|-------|-------|
| Created | 2026-02-04 |
| Sources Indexed | 6 primary + 1 fallback |
