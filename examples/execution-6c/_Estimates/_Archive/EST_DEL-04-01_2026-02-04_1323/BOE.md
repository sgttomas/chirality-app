# Basis of Estimate (BOE)
## DEL-04-01 Construction Methodology Narrative

---

## Snapshot Identification

| Field | Value |
|-------|-------|
| **Snapshot ID** | EST_DEL-04-01_2026-02-04_1323 |
| **Estimate Label** | DEL-04-01_ConstructionMethodologyNarrative |
| **Pricing Date** | 2026-02 (dollars of February 2026) |
| **Currency** | CAD |
| **Run Status** | OK |
| **Prepared By** | ESTIMATING Agent (Type 2) |
| **Date Prepared** | 2026-02-04 |

---

## Scope Definition

### Deliverable Description
Construction Methodology Narrative for the Public Services Building Design-Build proposal. This deliverable covers:
- Staging of work (phasing strategy, sequencing, mobilization/demobilization)
- Logistics (site access, laydown areas, material storage, equipment deployment)
- Site safety (safety management framework, hazard identification, emergency response)
- Construction administration (cleaning, transportation/storage, site services/utilities)

**Source:** `_CONTEXT.md`, Decomposition document SOW-019, SOW-020

### WBS Reference
- **Package ID:** PKG-06 (Construction Methodology + Administration)
- **Deliverable ID:** DEL-04-01
- **Deliverable Type:** Narrative Document
- **Discipline:** Construction Management
- **Responsible Party:** Construction Manager

### Scope Inclusions
1. **Engineering/Authoring Labor:** Drafting of construction methodology narrative
2. **Technical Review Labor:** Internal review by PM, Estimator, Safety Lead, Lead Architect, Scheduler
3. **Cross-Deliverable Coordination:** Alignment with DEL-02-01 (Concept Design), DEL-08-01 (Schedule), DEL-09-02 (Site Conditions), DEL-05-03 (Pricing)
4. **Reference Document Review:** Review of geotechnical, wetland, environmental, flood, and grading reports
5. **RFP Compliance Review:** Verification against RFP Section 7.2 and 7.3.1-7.3.3 requirements
6. **QA and Proposal Assembly Integration:** Final QA, formatting, delivery to Proposal Manager
7. **Senior Reviewer Assessment:** Credibility and persuasiveness review

### Scope Exclusions
- Physical construction work (this is a proposal narrative, not construction execution)
- Detailed construction execution plans (developed post-award)
- Budget control and change management (covered in DEL-04-02)
- Communications and reporting (covered in DEL-04-03)
- Commissioning and closeout (covered in DEL-06-01)
- Detailed project schedule (covered in DEL-08-01)
- Risk register (covered in DEL-09-01)
- Site conditions due diligence summary (covered in DEL-09-02)

**Decision:** D-001 (Scope exclusions established per decomposition document package boundaries)

---

## Currency and Conversion

| Item | Value |
|------|-------|
| **Estimate Currency** | CAD |
| **Conversion Assumptions** | None (single currency estimate) |
| **Evidence** | User instruction specified CAD; project is in Alberta, Canada |

**Decision:** D-002 (Currency set to CAD per user instruction)

---

## Contracting Assumptions

| Assumption | Value | Source |
|------------|-------|--------|
| **Contract Type** | Design-Build (integrated design and construction) | Decomposition document Section 1 |
| **Delivery Model** | Proposal production phase (pre-award) | _CONTEXT.md |
| **Labor Source** | Internal proposal team (CM, PM, technical leads) | Procedure.md (Roles and Responsibilities) |
| **Labor Rates** | Allowance-based (no rate tables available) | D-003 |

**Decision:** D-003 (Labor rates estimated as allowances; no project rate tables available)

---

## Location and Productivity Assumptions

| Assumption | Value | Source |
|------------|-------|--------|
| **Project Location** | Town of Penhold, Alberta | Datasheet.md |
| **Work Type** | Professional services (narrative document production) | _CONTEXT.md |
| **Productivity Basis** | Standard professional services productivity | A-001 |

**Assumption:** A-001 (Productivity assumed at standard professional services rates for proposal development work in Alberta)

---

## Pricing Sources Hierarchy

| Priority | Source Type | Status | Usage |
|----------|-------------|--------|-------|
| 1 | Vendor Quotes | Not available | N/A |
| 2 | Project Rate Tables | Not available (empty `_RateTables/` directory) | N/A |
| 3 | Allowances | Used | All line items |

**Decision:** D-004 (All line items priced using allowances due to absence of rate tables and quotes)

---

## Indirects Model

| Category | Treatment | Rationale |
|----------|-----------|-----------|
| **Project Management** | Included in cross-deliverable coordination line item | PM time for coordination is explicit |
| **QA/QC** | Included in QA and review line items | Review labor is explicit |
| **Overhead** | Not separately broken out | Proposal production is internal team effort; OH embedded in allowance rates |

**Decision:** D-005 (Indirects embedded in allowance rates; not separately broken out for proposal production work)

---

## Contingency Method and Rationale

| Item | Value |
|------|-------|
| **Method** | PCT_BY_BUCKET (default) |
| **Engineering/Authoring** | 10% contingency |
| **Review/Coordination** | 10% contingency |
| **Rationale** | Standard contingency for professional services with defined scope |

**Decision:** D-006 (Contingency at 10% applied to base estimate; low-risk professional services work)

---

## Escalation Method and Rationale

| Item | Value |
|------|-------|
| **Escalation Mode** | NONE (default) |
| **Rationale** | Short-duration proposal work; pricing date contemporaneous with execution |

**Decision:** D-007 (Escalation not applied; work expected to be completed within pricing period)

---

## Rounding Policy

| Item | Value |
|------|-------|
| **Rounding** | Nearest $100 (for professional services line items) |
| **Summary Totals** | Nearest $100 |

---

## Completeness Metrics Summary

| Metric | Value |
|--------|-------|
| **% Lines Priced by QUOTE** | 0% |
| **% Lines Priced by RATE_TABLE** | 0% |
| **% Lines Priced by ALLOWANCE** | 100% |
| **% Deliverables with Explicit Quantities** | 100% (effort-hours estimated) |
| **Confidence Level** | MEDIUM |

---

## Known Gaps

1. **Rate Tables Not Available:** All pricing based on allowances; recommend providing professional services rate tables for future runs
2. **Site Reference Documents Not Accessed:** Detailed geotechnical, wetland, environmental reports not read in detail; effort estimates assume moderate complexity
3. **RFP Section 7.2 Details:** Specific RFP requirements inferred from decomposition document; actual RFP content may reveal additional requirements

**Assumption:** A-002 (Effort estimates assume moderate document complexity based on available information)

---

## References

- **Decision Log:** `Decision_Log.md`
- **Assumptions Log:** `Assumptions_Log.md`
- **Source Index:** `Source_Index.md`
- **Detail Line Items:** `Detail.csv`
- **Summary:** `Summary.md`
- **Risk Register:** `Risk_Register.md`
- **QA Report:** `QA_Report.md`

---

**End of Basis of Estimate**
