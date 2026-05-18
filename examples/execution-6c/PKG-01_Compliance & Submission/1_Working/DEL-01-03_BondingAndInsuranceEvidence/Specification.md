# Specification: DEL-01-03 Bonding and Insurance Evidence

## Scope

### Inclusions

This deliverable covers:

1. **Agreement to Bond (Proposal Stage)**
   - Surety commitment letter confirming capacity to bond the project if proposal is accepted
   - Issued by a licensed surety company or surety broker
   - **Source:** `_CONTEXT.md` (anticipated artifacts); decomposition document DEL-01-03 definition (lines 171-174)

2. **Bond Cost Inclusion Statement**
   - Explicit statement or table confirming that bond costs are included in the proposal pricing
   - Reconciliation with Appendix H Schedule A and Schedule B
   - **Source:** Decomposition document SOW-004 (line 277); scope ledger (line 314)

3. **Insurance Approach Summary (as required)**
   - Summary of insurance coverage approach for the project
   - **Source:** `_CONTEXT.md` (anticipated artifacts)

**Total Obligation Fulfillment Scope:** **TBD** — Confirm whether RFP §5.3.1 imposes obligations beyond bonding and insurance (e.g., parent company guarantee, letter of credit, other financial security instruments). Current scope assumes only bonding and insurance; confirmation needed that no obligations are missed. — *[F-003]*

### Exclusions

This deliverable does **not** cover:

- Final bond issuance (occurs post-award, during contract execution)
- Detailed insurance certificates (proposal stage only)
- Subcontractor bonding or insurance (addressed elsewhere)
- **ASSUMPTION:** Scope limited to prime Design-Builder commitments at proposal stage

### Interfaces

- **DEL-01-02 (Formal Submission Package):** This deliverable must be included in the final proposal PDF
- **DEL-05-01/02 (Appendix H Pricing):** Bond costs must be reflected in pricing documents
- **Source:** Decomposition document (deliverable definitions and scope ledger)

---

## Requirements

### REQ-01: Agreement to Bond Inclusion

**Requirement:** The proposal **shall** include an Agreement to Bond from a licensed surety.

- **Rationale:** Mandatory compliance requirement (OBJ-001)
- **Source:** RFP §5.3.1 (**location TBD**; referenced in `_REFERENCES.md` and decomposition scope ledger line 314)
- **Acceptance Criteria:** Agreement to Bond document present in submission package **AND** contains required content elements (surety name, project identification, bond types, capacity confirmation, validity period, authorized signature). Presence alone is insufficient for defensible compliance substantiation. — *[C-002]*
- **Conformance Threshold:** **TBD**: Define minimum bond value, minimum surety rating, or minimum validity period that constitutes pass/fail threshold — *[C-001]*
- **Source Reference:** Decomposition document (`_CONTEXT.md` acceptance criteria, line 13)
- **Note on Letter Issuer:** Datasheet permits letter from "surety company or broker"; this requirement specifies "from a licensed surety." **Conflict potential** — if RFP requires direct surety letter, a broker letter may not comply. RFP §5.3.1 to determine acceptability of broker-issued letters. — *[F-004]*

### REQ-02: Surety Licensing

**Requirement:** The surety **shall** be licensed to operate in Alberta.

- **Rationale:** Jurisdictional requirement for contract enforceability
- **Source:** **ASSUMPTION** (standard for Alberta public sector projects; requires confirmation from RFP §5.3.1 or Alberta legislation). If this is non-negotiable baseline, it needs authoritative sourcing; if assumption, requirement should be flagged as provisional. — *[F-001]*
- **Acceptance Criteria:** Surety company listed with Alberta regulatory authority
- **Regulatory Authority Name:** **TBD** — This document references "Financial Services Regulatory Authority of Alberta" but this name requires verification. All documents should align to a single canonical regulatory body name once confirmed. — *[A-004, C-004]*

### REQ-03: Bond Cost Inclusion

**Requirement:** Bond costs **shall** be included in the proposal price.

- **Rationale:** Mandatory for pricing completeness and competitiveness (OBJ-007)
- **Source:** Decomposition document SOW-004 (line 277); scope ledger notes (line 314: "Bond costs included in proposal price")
- **Acceptance Criteria:** Explicit statement in deliverable confirming inclusion; costs reflected in Appendix H Schedule B

### REQ-04: Bond Cost Documentation

**Requirement:** The bond cost inclusion statement **shall** identify the basis for bond cost estimation.

- **Rationale:** Transparency and pricing defensibility
- **Source:** **ASSUMPTION** (derived from OBJ-007 pricing competitiveness objective; requires verification from RFP)
- **Acceptance Criteria:** Statement includes bond percentage or fixed cost; source basis (e.g., surety quote, industry rate)
- **Evidentiary Threshold:** **TBD** — Define whether a surety quote must be attached, or if proponent self-statement is sufficient for regulatory reviewer. Current acceptance criteria may be too permissive. — *[F-002]*

### REQ-05: Bond Types Coverage

**Requirement:** The Agreement to Bond **shall** confirm surety capacity to provide performance and labor and material payment bonds.

- **Rationale:** Standard Design-Build bonding protection for Owner (performance bond protects against contractor default; labor and material payment bond protects against non-payment of subcontractors/suppliers)
- **Source:** **ASSUMPTION** (typical for Design-Build contracts; specific types to be confirmed from RFP §5.3.1 **location TBD**)
- **Acceptance Criteria:** Agreement to Bond explicitly mentions bond types or references contract bond requirements

### REQ-06: Insurance Approach Summary (Conditional)

**Requirement:** If required by RFP §5.3.1, the deliverable **shall** include an insurance approach summary.

- **Rationale:** Compliance with "as required" scope per `_CONTEXT.md`
- **Source:** `_CONTEXT.md` anticipated artifacts (line 18); RFP §5.3.1 requirements **TBD** (not yet extracted)
- **Acceptance Criteria:** Insurance summary present if RFP mandates it at proposal stage
- **Status Note:** The condition ("If required by RFP §5.3.1") cannot be resolved until RFP §5.3.1 is extracted. This leaves the mandatory/optional status unresolved. — *[A-003]*
- **Normalization Note:** The "as required" qualifier appears in _CONTEXT.md, Datasheet, Specification, Guidance, and Procedure. Once RFP is read, this conditional must be resolved consistently across all documents. — *[E-003]*

### REQ-07: Consistency with Pricing Documents

**Requirement:** Bond costs stated in this deliverable **shall** reconcile with bond cost line items in Appendix H Schedule B.

- **Rationale:** Cross-document consistency (fundamental to proposal credibility)
- **Source:** Decomposition document (deliverable interfaces); agent protocol (cross-document consistency requirement)
- **Acceptance Criteria:** Bond cost figures match across DEL-01-03 and DEL-05-02

### REQ-08: Agreement to Bond Validity Period

**Requirement:** The Agreement to Bond **shall** include a validity period covering the proposal evaluation timeline (typically 60-90 days post-submission). — *[C-003]*

- **Rationale:** Comprehensive mandatory coverage — validity period is operationally referenced in Guidance and Procedure but was not previously a formal requirement.
- **Source:** Guidance Example 1; Procedure Step 2
- **Acceptance Criteria:** Validity period explicitly stated and extends beyond anticipated proposal evaluation period

### REQ-09: Addenda Integration Verification

**Requirement:** The deliverable production process **shall** verify that all addenda affecting bonding/insurance requirements have been integrated. — *[X-006]*

- **Rationale:** Total conformance adjudication — Guidance notes that addenda acknowledgment failure may disqualify the price proposal (Considerations > For the Team, item 3). This high-risk compliance gate requires a corresponding verification requirement.
- **Source:** Guidance.md (Considerations > For the Team); Decomposition hard constraints (C-07, line 49)
- **Acceptance Criteria:** Documentation that addenda were reviewed for bonding/insurance impacts; any changes integrated into deliverable

### REQ-10: Holistic Package Integrity

**Requirement:** Prior to submission, the complete deliverable package (Agreement to Bond + Bond Cost Statement + Insurance Summary) **shall** undergo a holistic integrity review as an integrated whole. — *[X-008]*

- **Rationale:** Full-scope integrity audit — verification table is requirement-by-requirement but no integrative check existed.
- **Source:** Semantic lensing (X:reviewing:completeness lens)
- **Acceptance Criteria:** Documented holistic review confirming coherence across all three components; no conflicting statements or orphaned references

---

## Standards

### Governing Codes and Standards

| Standard/Code | Applicability | Source |
|---------------|---------------|--------|
| **RFP §5.3.1** | Agreement to Bond and bond cost requirements | `_REFERENCES.md`; decomposition scope ledger (line 314) |
| **Governing Statute** | **TBD**: Identify upstream regulatory authority (e.g., Alberta Public Procurement Act, Municipal Government Act provisions on bonding) that anchors RFP bonding requirements | Proposal Manager to identify — *[A-002]* |
| **Alberta Surety Licensing Regulations** | Surety prequalification | **ASSUMPTION** (standard for Alberta public projects; requires confirmation) |
| **CCDC 222 (Guide to Calling Construction Performance Bonds)** | Industry best practice for bonding | **ASSUMPTION** (reference standard; not mandated by RFP) |

**Note:** Specific RFP bond percentage, insurance coverage minimums, and certificate format requirements are **TBD** (RFP §5.3.1 **location TBD**).

### Compliance Framework Overview

**TBD**: Once RFP §5.3.1 is extracted, create a traceable compliance framework that maps each RFP obligation to a specific requirement and verification method. Current structure has requirements and verification but source obligation linkage is incomplete. — *[X-002]*

---

## Verification

### Verification Methods

| Requirement | Verification Method | Responsible Party |
|-------------|---------------------|-------------------|
| REQ-01: Agreement to Bond Inclusion | Document inspection (proposal package checklist) + content element verification | Proposal Manager |
| REQ-02: Surety Licensing | Surety company verification (Alberta regulatory database — **specific database TBD** per A-004) | Proposal Manager or Estimator |
| REQ-03: Bond Cost Inclusion | Statement review; pricing document cross-check with documented evidence of cross-check execution — *[X-003]* | Proposal Manager + Estimator |
| REQ-04: Bond Cost Documentation | Narrative review for basis and source | Estimator |
| REQ-05: Bond Types Coverage | Agreement to Bond content review with specified pass/fail criteria for adequate coverage — *[D-001]* | Proposal Manager |
| REQ-06: Insurance Approach Summary | RFP requirement verification (**suspended until RFP TBD resolved** per E-002); document inspection | Proposal Manager |
| REQ-07: Consistency with Pricing Documents | Cross-document reconciliation (DEL-01-03 vs. DEL-05-02) | Proposal Manager + Estimator |
| REQ-08: Validity Period | Agreement to Bond content review for validity date | Proposal Manager |
| REQ-09: Addenda Integration | Documentation review of addenda impact assessment | Proposal Manager |
| REQ-10: Holistic Package Integrity | Integrative review of all three components as a unified package | Proposal Manager |

### Acceptance Gate

- **Gate:** Compliance review (pre-submission)
- **Criteria:** All requirements verified; no discrepancies with Appendix H pricing
- **Discrepancy Definition:** **TBD** — Define what constitutes a "discrepancy" (e.g., is a rounding difference a discrepancy? Is a different line-item allocation but same total a discrepancy?). Definitive compliance boundary requires clear pass/fail threshold. — *[D-002]*
- **Authority:** Proposal Manager
- **Escalation Path:** **TBD** — Define escalation path for cases where Proposal Manager cannot resolve a deficiency (e.g., surety refuses to issue letter, bond costs cannot be reconciled). Single-authority model may be insufficient for complex failure scenarios. — *[X-005]*
- **Source:** Decomposition document (DEL-01-03 acceptance criteria, line 174)

---

## Documentation

### Required Documentation Outputs

1. **Agreement to Bond** (letter from surety or broker)
   - Format: PDF or scanned letter on letterhead
   - Content: Surety commitment, bond types, project identification
   - **Source:** Decomposition document (anticipated artifacts, `_CONTEXT.md` line 16)

2. **Bond Cost Inclusion Statement**
   - Format: Narrative text or table within this deliverable or integrated into pricing narrative (DEL-05-03)
   - Content: Bond percentage or cost, confirmation of inclusion in pricing, reconciliation reference to Appendix H
   - **Source:** Decomposition document (anticipated artifacts, `_CONTEXT.md` line 17)

3. **Insurance Approach Summary** (if required)
   - Format: Brief narrative (1-2 paragraphs)
   - Content: Insurance types, coverage approach, timing (proposal vs. contract stage)
   - **Source:** Decomposition document (anticipated artifacts, `_CONTEXT.md` line 18)

### Records and Traceability

- Agreement to Bond filed in formal submission package (DEL-01-02)
- Bond cost inclusion statement referenced in compliance matrix (DEL-01-01)
- Cross-reference to pricing documents maintained in final proposal assembly
- **Source:** **ASSUMPTION** (derived from proposal management best practices and decomposition structure)

---

## Notes

- **Missing Information:** RFP §5.3.1 details (bond percentages, insurance requirements, format specifications) are **TBD** due to PDF access failure. Requirements REQ-02, REQ-04, REQ-05, and REQ-06 include assumptions that require verification when RFP becomes accessible.
- **High Compliance Risk:** This deliverable is flagged as a high compliance risk item (decomposition Section 11, line 348); failure to meet requirements may disqualify the proposal.
- **Cross-Document Dependency:** REQ-07 creates a hard consistency requirement with pricing deliverables (DEL-05-02); changes to bond costs must propagate across documents.
