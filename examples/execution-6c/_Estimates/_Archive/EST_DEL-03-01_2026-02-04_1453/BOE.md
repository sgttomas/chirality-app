# Basis of Estimate (BOE)

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-03-01_2026-02-04_1453 |
| **Estimate Label** | DEL-03-01 Design Methodology Narrative |
| **Pricing Date** | 2026-02 (dollars of February 2026) |
| **Currency** | CAD |
| **RUN_STATUS** | WARNINGS |

---

## Scope Definition

### Deliverable Being Estimated

- **Deliverable ID:** DEL-03-01
- **Name:** Design Methodology Narrative
- **Package:** PKG-05 Delivery Plan (Design Methodology + Docs Plan)
- **Discipline:** Design Management
- **Type:** Narrative Document
- **Responsible Party:** Design Manager / PM

### Scope Description

This deliverable involves producing a narrative document describing the Design-Builder's approach to:
- Design deliverables production
- Stakeholder and Project Team engagement
- Collaborative design process
- Design process sequencing
- Review and approval timelines
- Municipal permitting process
- Special considerations

The narrative is part of a Design-Build proposal response for the Town of Penhold Public Services Building (combined Fire Hall and Public Works facility).

---

## Scope Inclusions

1. **Engineering/Design Labor (E):**
   - Design Manager/PM time for authoring narrative
   - Lead Architect input on design process and professional seal requirements
   - Discipline leads (Civil/Structural/Mechanical/Electrical) input on coordination procedures
   - Construction Manager input on constructability integration
   - Scheduler input on milestone timing
   - Internal QC review labor

2. **Project Management (PM):**
   - Coordination with other deliverables (DEL-02-01, DEL-03-02, DEL-04-01, DEL-08-01)
   - Stakeholder review and approval cycles
   - Integration with proposal PDF

3. **Supporting Deliverables:**
   - Visual aids (flowcharts, timeline diagrams, coordination matrices)
   - Graphics production for design process flowchart, permitting sequence diagram

---

## Scope Exclusions

1. Actual design work (covered in DEL-02-01 Concept Design Package)
2. Construction methodology content (covered in DEL-04-01)
3. Detailed design and construction documents plan (covered in DEL-03-02)
4. Schedule development (covered in DEL-08-01)
5. Pricing or cost estimation methodology (covered in PKG-02)
6. Post-award execution of the methodology (proposal-stage document only)
7. External consultant fees (assumes in-house team)
8. Printing/reproduction costs

---

## Currency and Conversion

- **Primary Currency:** CAD (Canadian Dollars)
- **Conversion Assumptions:** None - all pricing in CAD
- **Evidence:** Instruction specified CAD; project is in Alberta, Canada (Town of Penhold)
- **Decision Reference:** D-001

---

## Contracting Assumptions

- **Delivery Model:** In-house proposal team labor
- **Location:** Alberta, Canada
- **Labor Basis:** Professional services (engineering/PM hourly rates)
- **Overhead:** Included in labor rates (fully burdened rates assumed)
- **No external procurement:** Document produced by internal team

---

## Pricing Sources Hierarchy

This estimate uses the following pricing priority:

1. **QUOTE:** Not available (no vendor quotes for proposal document production)
2. **RATE_TABLE:** Not available (no project rate tables found in `_Estimates/_RateTables/`)
3. **ALLOWANCE:** Primary basis - allowances based on typical effort for proposal narrative documents

**Decision Reference:** D-002 (Rate table fallback to allowances)

---

## Pricing Methodology

### Labor Estimation Approach

Effort estimated based on:
- Procedure.md 8-step process requiring multiple team members
- Specification.md 30 requirements to address
- Guidance.md 8 principles, 10 considerations, 6 trade-offs
- Typical complexity for design methodology narrative in Design-Build proposals

### Labor Rate Assumptions

All rates are **ALLOWANCES** based on typical Alberta professional services rates:

| Role | Assumed Hourly Rate (CAD) | Assumption ID |
|------|---------------------------|---------------|
| Design Manager/PM | $175/hr | A-001 |
| Lead Architect | $185/hr | A-002 |
| Discipline Lead (avg) | $165/hr | A-003 |
| Construction Manager | $160/hr | A-004 |
| Scheduler | $140/hr | A-005 |
| Graphics/CAD Technician | $95/hr | A-006 |
| Administrative/QC Support | $85/hr | A-007 |

---

## Indirects Model

**Factor-Based Model Applied:**

| Indirect Category | Factor | Basis | Decision Ref |
|-------------------|--------|-------|--------------|
| PM/Coordination Overhead | 15% | Applied to direct labor | D-003 |
| QA/QC Overhead | Explicit | Included in labor line items | N/A |

---

## Contingency Method

**Method:** PCT_BY_BUCKET (percentage by CBS bucket)

| CBS Bucket | Contingency % | Rationale |
|------------|---------------|-----------|
| Engineering (E) | 20% | High allowance reliance; narrative scope may vary |
| Project Management (PM) | 15% | Coordination complexity uncertain |

**Total Contingency:** Calculated as weighted average across buckets

**Decision Reference:** D-004

---

## Escalation

**Mode:** NONE (escalation not applied)

**Rationale:** Short-duration proposal effort; pricing date is current; no escalation adjustment required.

---

## Rounding Policy

- **Rounding:** Nearest $100 CAD for line items; nearest $1,000 CAD for totals
- **Precision:** Appropriate for allowance-based budget estimate

---

## Completeness Metrics

| Metric | Value |
|--------|-------|
| % Lines Priced by QUOTE | 0% |
| % Lines Priced by RATE_TABLE | 0% |
| % Lines Priced by ALLOWANCE | 100% |
| Deliverables with Explicit Quantities | 1 of 1 (100%) |
| Confidence Level | LOW-MEDIUM |

---

## Known Gaps

1. **No rate tables available:** All pricing based on assumed allowances
2. **Effort variability:** Actual effort highly dependent on proposal team experience, concurrent workload, and quality expectations
3. **Graphics scope undefined:** Number and complexity of visual aids not specified
4. **Cross-deliverable integration:** Effort for consistency with DEL-04-01, DEL-08-01 etc. may vary
5. **Review cycles:** Number of stakeholder review iterations assumed; actual may differ

---

## References

- **Decision Log:** `Decision_Log.md`
- **Assumptions Log:** `Assumptions_Log.md`
- **Risk Register:** `Risk_Register.md`
- **Source Index:** `Source_Index.md`
- **Detail.csv:** Line item details with full traceability

---

## Document Control

| Property | Value |
|----------|-------|
| **Generated** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
| **Source Deliverable** | DEL-03-01_DesignMethodologyNarrative |
| **Snapshot Path** | `_Estimates/EST_DEL-03-01_2026-02-04_1453/` |
