# Source Index

## Snapshot Identification

| Field | Value |
|-------|-------|
| **Snapshot ID** | EST_DEL-09-01_2026-02-04_1323 |
| **Deliverable** | DEL-09-01 Risk Register and Mitigation Plan |

---

## Source Discovery Summary

| Source Type | Count | Status |
|-------------|-------|--------|
| Explicit Pricing Sources (Quotes/Budgets) | 0 | Not available |
| Rate Tables | 0 | Not available |
| Quantity Sources (4 Documents) | 4 | Available - used |
| Fallback Model | 1 | Used for all pricing |

---

## Pricing Sources (Priority Order)

### Priority 1: Explicit Pricing Sources

| Source | Location | Status | Usage |
|--------|----------|--------|-------|
| Vendor quotes | N/A | NOT AVAILABLE | N/A |
| Budgetary quotes | N/A | NOT AVAILABLE | N/A |
| Proposals | N/A | NOT AVAILABLE | N/A |
| Budget sheets | N/A | NOT AVAILABLE | N/A |
| PO summaries | N/A | NOT AVAILABLE | N/A |

**Decision:** No explicit pricing sources available for professional services deliverable. Proceed with rate tables or allowances. (D-004)

### Priority 2: Rate Tables / Cost Libraries

| Source | Location | Status | Usage |
|--------|----------|--------|-------|
| Project rate tables | `_Estimates/_RateTables/` | NOT AVAILABLE | N/A |
| Historical rates | N/A | NOT AVAILABLE | N/A |

**Decision:** No rate tables available in _RateTables/ directory. Proceed with allowances. (D-004)

### Priority 3: Quantity Sources (Deliverable Documents)

| Source | Location | Status | Usage |
|--------|----------|--------|-------|
| Datasheet.md | DEL-09-01 folder | AVAILABLE | Risk categories, assessment framework, document structure |
| Specification.md | DEL-09-01 folder | AVAILABLE | Scope, requirements, verification methods |
| Guidance.md | DEL-09-01 folder | AVAILABLE | Principles, considerations, trade-offs |
| Procedure.md | DEL-09-01 folder | AVAILABLE | Steps, personnel, effort indicators |

**Usage:** Quantity sources provided scope definition and effort indicators (workshop duration, risk categories, QC areas). No explicit quantities or LOE provided.

### Priority 4: Fallback Typical Model

| Source | Status | Usage |
|--------|--------|-------|
| Professional judgment | USED | All line items priced using allowances based on scope complexity |
| Industry standard rates | USED | PM @ $200/hr, Technical Leads @ $150/hr (assumed) |

**Decision:** Fallback model used for all pricing due to absence of quotes and rate tables. Confidence rated LOW-MEDIUM. (D-004)

---

## Document Sources Indexed

### Deliverable Documents (Primary)

| Document | Path | Key Extractions |
|----------|------|-----------------|
| _CONTEXT.md | `PKG-09.../DEL-09-01_RiskRegisterAndMitigationPlan/` | Deliverable description, acceptance criteria, responsible parties |
| Datasheet.md | `PKG-09.../DEL-09-01_RiskRegisterAndMitigationPlan/` | 7 risk categories, assessment framework (P/I 1-5 scales), document structure |
| Specification.md | `PKG-09.../DEL-09-01_RiskRegisterAndMitigationPlan/` | Scope (7 categories + QMP), requirements (FR-01 to FR-07), verification methods |
| Guidance.md | `PKG-09.../DEL-09-01_RiskRegisterAndMitigationPlan/` | Risk management principles, QMP principles, 20 considerations, trade-offs |
| Procedure.md | `PKG-09.../DEL-09-01_RiskRegisterAndMitigationPlan/` | 7 steps, personnel roles, workshop guidance (2-4 hrs), QC checkpoint definitions |
| _REFERENCES.md | `PKG-09.../DEL-09-01_RiskRegisterAndMitigationPlan/` | 10 reference documents for risk identification |
| _DEPENDENCIES.md | `PKG-09.../DEL-09-01_RiskRegisterAndMitigationPlan/` | Tracking mode: NOT_TRACKED |

### Reference Documents (Secondary)

| Document | Location | Relevance to Estimate |
|----------|----------|----------------------|
| RFP | _Sources/ | Risk themes; QC/inspection requirements |
| Addendum 01-03 | _Sources/ | Scope changes affecting risk scope |
| Geotechnical Report | _Sources/ | Referenced in risk identification effort |
| Wetland Assessment | _Sources/ | Referenced in risk identification effort |
| Environmental Assessment | _Sources/ | Referenced in risk identification effort |
| Site Grading | _Sources/ | Referenced in risk identification effort |
| Flood Zone Mapping | _Sources/ | Referenced in risk identification effort |
| Adjacent Subdivision Design | _Sources/ | Referenced in risk identification effort |

---

## Cost Driver Extraction Summary

### From Datasheet.md

| Cost Driver | Extraction | Line Item(s) |
|-------------|------------|--------------|
| 7 risk categories | Design, Site, Cost, Schedule, Procurement, Environmental, Permitting | L-001 to L-006 |
| Risk assessment framework | P/I scoring (1-5 scales), Score = P x I | L-004 |
| Document structure | Risk register + Mitigation plans + QMP | L-011, L-012 |
| 4 QC areas | Design, Construction, Commissioning, Documentation | L-007 to L-010 |

### From Specification.md

| Cost Driver | Extraction | Line Item(s) |
|-------------|------------|--------------|
| ~20 risks expected | Minimum risk count for project of this complexity | L-004 to L-006 |
| High-priority threshold | Score >=15 requires detailed mitigation | L-005 |
| 4 QMP areas required | Design QC, Construction QC, Commissioning QC, Documentation QC | L-007 to L-010 |
| Cross-deliverable consistency | Verify with DEL-09-02, DEL-05-03, DEL-08-01, DEL-06-01 | L-014 |

### From Guidance.md

| Cost Driver | Extraction | Line Item(s) |
|-------------|------------|--------------|
| 20 considerations listed | Site/Design/Cost/Schedule/Procurement/Compliance factors | L-001 to L-006 |
| Risk-to-QC mapping | Control procedures linked to risk categories | L-007 to L-010 |
| Mitigation decision matrix | Strategy varies by risk score | L-005, L-006 |

### From Procedure.md

| Cost Driver | Extraction | Line Item(s) |
|-------------|------------|--------------|
| Workshop duration | 2-4 hours recommended (used 4 hours) | L-001, L-002 |
| Personnel roles | PM + 6 Technical Leads | L-001 to L-003 |
| 7 procedure steps | Prep, Identify, Assess, Mitigate, QMP, Document, Review | All lines |
| 5 Design QC checkpoints | Concept, Schematic, DD, 90% CD, 100% CD | L-007 |
| 4 Construction QC points | Foundation, Structure, MEP, Finishes | L-008 |
| 3 Commissioning QC points | Functional test, Training, Documentation | L-009 |
| 4 Documentation QC points | Drawing, Spec, As-built, Closeout | L-010 |

---

## Source Selection Rationale

**Primary Pricing Basis Decision (D-004):**

Given the absence of:
- Vendor quotes for professional services
- Project rate tables for PM/Technical Lead labor
- Historical cost data for similar deliverables

The estimate uses ALLOWANCE method for all line items with the following basis:
- PM hourly rate: $200/hr (assumed typical D-B proposal PM rate)
- Technical Lead hourly rate: $150/hr average (assumed typical discipline lead rate)
- Effort hours derived from scope complexity analysis of deliverable documents

**Confidence:** LOW-MEDIUM due to 100% ALLOWANCE basis.

---

**Generated:** 2026-02-04 13:23
**Agent:** ESTIMATING (Type 2)
