# Specification: DEL-28.01 Independent Design Verification Reports

## Scope

This specification defines the requirements for **Independent Design Verification Reports** within **PKG-28 Design Verification**.

**Purpose:** Documents analysis and results for independent design verification reports required for design verification and approvals, supporting **OBJ-6: Regulatory Compliance** — "The Works comply with all permits, codes, and authority requirements."

**Source:** _CONTEXT.md (DEL-28.01 description); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-6; Section 6, Objective-to-Deliverable Mapping)

**Anticipated deliverable artifacts:**
- IDV reports (by discipline/submission stage)

**Scope Inclusions:**
- Independent verification of design calculations, drawings, and specifications across all disciplines
- Verification of compliance with applicable codes, standards, and Employer's Requirements
- Identification of non-compliances and design deficiencies
- Verification of resolution of identified issues
- IDV reports prepared at 30%, 60%, 90%, and IFC design submission stages — **ASSUMPTION**: Standard D&B milestone sequence

**Scope Exclusions:**
- Design work itself (performed under discipline packages PKG-01 through PKG-27, PKG-29 through PKG-36)
- VFPA IP Review process (covered under DEL-28.02)
- Inter-discipline coordination records (covered under DEL-28.03)
- Testing and commissioning verification (covered under PKG-29)

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (PKG-28 scope; Section 1.2: Scope Focus)

## Requirements

### Functional Requirements

| Req ID | Requirement | Guidance § | Procedure Step | Verification |
|--------|-------------|------------|----------------|--------------|
| FR-1 | IDV shall be performed by qualified third-party reviewers independent of the design team. Reviewers shall be licensed P.Eng. in applicable discipline and BC jurisdiction. | P-1, C-2 | Step 1.2 | V-5 |
| FR-2 | IDV reports shall be produced for each major design submission stage: 30%, 60%, 90%, IFC. Each stage shall verify all design documents issued at that stage. | P-3 | Step 7 | V-3 |
| FR-3 | IDV shall cover all applicable design disciplines: Civil, Structural, Marine, Mechanical, Process, Electrical, I&C, Fire Protection. | E-3 | Step 1.1 | V-5 |
| FR-4 | IDV shall verify compliance with applicable codes (BC Building Code, CSA, ASME, API), Employer's Requirements, design criteria, and regulatory requirements (VFPA, municipal, provincial). | P-4 | Step 3.1 | V-4 |
| FR-5 | Non-compliances shall be documented with finding number, description, affected documents, code reference, severity (Critical/Major/Minor), and recommended action. | C-4, E-2 | Step 3.2 | V-3 |
| FR-6 | IDV reports shall verify closure of findings from previous stages. Design revisions addressing findings shall be reviewed and confirmed compliant. | P-3 | Step 3.3 | V-3 |

**TBD Items:**
- FR-1: Specific licensing requirements per discipline
- FR-2: Specific document lists per stage and discipline
- FR-4: Complete code list per discipline; specific ER sections
- FR-5: Finding classification criteria

**Source:** ISO 9001 quality management principles; _CONTEXT.md (anticipated artifacts); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4, Package Summary; Section 2, OBJ-6)

### Performance Requirements

| Req ID | Requirement | Guidance § | Procedure Step | Verification |
|--------|-------------|------------|----------------|--------------|
| PR-1 | IDV shall review 100% of design documents within scope for each stage. | C-3 | Step 3.4 | V-2 |
| PR-2 | IDV reports shall be issued within **TBD** days of receipt of design submission. | C-1 | Step 2.2 | V-5 |
| PR-3 | Reviewers shall hold P.Eng. licenses in BC and have minimum **TBD** years of experience in applicable discipline. | C-2 | Step 1.2 | V-5 |

**TBD Items:**
- PR-1: Sampling approach for large drawing sets, if applicable
- PR-2: Review schedule duration
- PR-3: Experience requirements

**Source:** _CONTEXT.md (anticipated artifacts); ISO 9001 quality requirements

### Interface Requirements

| Req ID | Requirement | Guidance § | Procedure Step | Verification |
|--------|-------------|------------|----------------|--------------|
| IR-1 | IDV reports interface with DEL-27.04 (Design Submission Packages). IDV review scope includes all design documents submitted at each stage. | P-5, E-4 | Step 2 | V-5 |
| IR-2 | IDV reports support regulatory submissions to VFPA and other authorities. Related to DEL-28.02 (VFPA IP Review Responses) and DEL-28.03 (Design Coordination Records). | P-4, C-5, C-6 | Step 5.1 | V-4 |
| IR-3 | IDV process shall comply with project Quality Management Plan. IDV findings shall be tracked in project quality/corrective action system. | C-7 | Step 6 | V-1 |
| IR-4 | IDV reviewers shall coordinate with discipline design leads to clarify findings and verify closures. | T-2 | Step 5.2 | V-3 |

**TBD Items:**
- IR-2: Specific regulatory submission requirements
- IR-3: QMP reference; tracking system specification

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (PKG-28 scope; DEL-27.04 description); _DEPENDENCIES.md (NOT_TRACKED mode)

### Quality Requirements

| Req ID | Requirement | Guidance § | Procedure Step | Verification |
|--------|-------------|------------|----------------|--------------|
| QR-1 | All IDV work shall comply with ISO 9001 Quality Management System requirements. | P-1, C-7 | Step 1.3 | V-1 |
| QR-2 | IDV reports shall be technically accurate, complete, and clearly written. Reports shall be checked and approved prior to issue. | — | Step 4.2 | V-2 |
| QR-3 | IDV reports shall be controlled per project document control procedures. Revisions shall be tracked and managed. | C-8 | Step 4.3 | V-2 |

**TBD Items:**
- QR-2: Specific QA/QC procedures
- QR-3: Document control system reference; revision control protocol

**Source:** Datasheet.md (applicable standards: ISO 9001)

## Standards

**Applicable codes and standards (Design discipline):**

| Standard | Applicability | Status |
|----------|---------------|--------|
| ISO 9001 | Quality Management Systems | Applicable |
| Employer's Requirements | IDV requirements | **TBD**: Specific ER sections |
| BC Building Code | Building and structural design | **TBD**: Specific sections |
| CSA Standards | Various discipline codes | **TBD**: Specific standards |
| ASME Standards | Mechanical equipment, piping | **TBD**: Specific standards |
| API Standards | Tank, petroleum equipment | **TBD**: Specific standards |
| IEEE Standards | Electrical systems | **TBD**: Specific standards |
| NFPA Standards | Fire protection | **TBD**: Specific standards |
| EGBC Practice Standards | Professional engineering practice in BC | Applicable |

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 1.1, Location: Fraser Surrey Terminal, Surrey, BC); Guidance.md (applicable standards context)

## Verification

**Verification methods for Report deliverables:**

| Verification ID | Method | Acceptance Criteria | Procedure Step |
|-----------------|--------|---------------------|----------------|
| V-1 | Technical review of IDV methodology | IDV methodology approved by Project Quality Manager | Step 1.3 |
| V-2 | IDV report QA/QC review | Report complete per D-1; QA/QC reviewer approval | Step 4.2 |
| V-3 | Finding tracking and closure verification | All Critical findings closed prior to IFC; Major/Minor findings closed or accepted | Step 6 |
| V-4 | Regulatory authority review (if required) | Authority acceptance per requirements | Step 5.1 |
| V-5 | Final IDV acceptance | IDV reports complete; findings closed; reviewers qualified; reports approved | Step 7 |

**Sign-off Requirements:**

| Role | Sign-off | Requirement Ref |
|------|----------|-----------------|
| Lead IDV Reviewer | Verification statement signature | FR-1 |
| QA/QC Reviewer | Report approval | QR-2 |
| D&B Contractor Approver | Issue approval | QR-3 |
| Project Quality Manager | IDV program acceptance | IR-3, QR-1 |

**Source:** Guidance.md (Principles P-1 through P-5); Procedure.md (Steps 1-7, Verification section)

## Documentation

**Required documentation outputs:**

| Document Type | Naming Convention | Count | Procedure Step |
|---------------|-------------------|-------|----------------|
| IDV Reports | IDV-[Discipline]-[Stage] (e.g., IDV-CIVIL-30) | ~32 (8 disciplines × 4 stages) | Step 4, Records |
| IDV Methodology | Per project numbering | 1 | Step 1.3 |
| Reviewer Qualifications | Per project numbering | Per reviewer | Step 1.2 |
| Review Checklists | Per project numbering | Per discipline/stage | Step 3.4 |
| Finding Tracking Log | Per project numbering | 1 (ongoing) | Step 6.1 |

**Source:** _CONTEXT.md (anticipated artifacts); Datasheet.md (report series naming convention)

**Documentation requirements:**

**D-1: Report Content**
Each IDV report shall include (minimum) — See Procedure.md Step 4.1:
1. Executive summary
2. Review scope and objectives
3. Methodology and review criteria
4. Design documents reviewed (list with revision numbers)
5. Reviewer qualifications and certifications
6. Code and standard compliance checklist
7. Findings (non-compliances and recommendations) — organized by severity
8. Closure verification (for findings from previous stages)
9. Verification statement and sign-off

**D-2: Document Control**
- Document numbering: **TBD** — Per project numbering system
- Revision control: **TBD** — Per document management system
- Format: **TBD** — PDF for issued; editable source for working

**D-3: Record Management**
- Working documents: `1_Working/DEL-28.01.../`
- Under review: `2_Checking/To/` with document number and date
- Issued: `3_Issued/` with final document number, revision, date
- Retention: **TBD** — Per contract requirements

**D-4: Submittal**
- IDV reports submitted alongside design submission packages (DEL-27.04)
- Submittal format and protocol: **TBD**

**Source:** Procedure.md (record management section); Datasheet.md (related deliverable: DEL-27.04)

## Cross-Document Traceability Matrix

| Specification Requirement | Datasheet Section | Guidance Section | Procedure Step |
|---------------------------|-------------------|------------------|----------------|
| FR-1 (Independent Review) | Attributes (Review Method) | P-1, C-2 | Step 1.2 |
| FR-2 (Stage Coverage) | Attributes (Review Stages) | P-3 | Step 7 |
| FR-3 (Discipline Coverage) | Attributes (Disciplines Covered), Construction | E-3 | Step 1.1 |
| FR-4 (Compliance Verification) | Attributes (Verification Scope), Conditions | P-4 | Step 3.1 |
| FR-5 (Finding Documentation) | Construction (Report Structure) | C-4, E-2 | Step 3.2 |
| FR-6 (Closure Verification) | Construction (Report Structure) | P-3 | Step 3.3, Step 6.2 |
| PR-1 (Review Completeness) | — | C-3 | Step 3.4 |
| PR-2 (Timeliness) | Conditions (Review Duration) | C-1 | Step 2.2 |
| PR-3 (Reviewer Qualifications) | Attributes (Review Method) | C-2 | Step 1.2 |
| IR-1 (Design Submissions) | Cross-Deliverable Coordination | P-5, E-4 | Step 2 |
| IR-2 (Regulatory Submissions) | Cross-Deliverable Coordination | C-5, C-6 | Step 5.1 |
| IR-3 (QMS Integration) | References | C-7 | Step 6 |
| IR-4 (Design Team Coordination) | — | T-2 | Step 5.2 |
| QR-1 (ISO 9001) | References | P-1, C-7 | Step 1.3 |
| QR-2 (Report Quality) | — | — | Step 4.2 |
| QR-3 (Document Control) | Attributes (Classification) | C-8 | Step 4.3, Step 5.1 |

**Source:** Cross-document consistency verification per AGENT_4_DOCUMENTS_REVISED_v3.md (Step 5)
