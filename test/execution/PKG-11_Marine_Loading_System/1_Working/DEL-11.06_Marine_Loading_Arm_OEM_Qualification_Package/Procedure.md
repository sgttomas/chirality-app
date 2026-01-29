# Procedure: DEL-11.06 Marine Loading Arm OEM Qualification Package

## Purpose

This procedure defines the process for producing and managing **Marine Loading Arm OEM Qualification Package** within **PKG-11 Marine Loading System**.

**Deliverable purpose:** Defines and substantiates marine loading arm OEM qualification in accordance with Employer's Requirements (ER), demonstrating OEM capability, product compliance, and suitability for the project prior to procurement commitment.

**Deliverable type:** Document Package
**Responsible party:** D&B Contractor (with OEM/Supplier)
**Discipline:** Process

## Prerequisites

### Dependencies
- See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)
- Upstream deliverables and input data to be confirmed prior to commencement

### Required Inputs

| Input | Source | Status |
|-------|--------|--------|
| Technical specification requirements | DEL-11.02 Technical Specification | **TBD** |
| ER qualification requirements | Employer's Requirements | **TBD** |
| Project design basis | PKG-00 / DEL-11.02 §3 | **TBD** |
| Hazardous area classification | PKG-27 | **TBD** |
| OEM contact / enquiry response | Procurement | **TBD** |
| Project QA/QC procedures | Project standards | **TBD** |

### Reference Materials
- `_REFERENCES.md` — applicable reference document list
- `0_References/` — package reference materials
- Employer's Requirements — **TBD** (specific clause references)
- Applicable codes and standards — **TBD** (confirm per ER and project code register)

### Personnel Requirements
- Process discipline engineer (technical review lead)
- Procurement specialist (OEM coordination)
- QA/QC representative (quality review)
- **ASSUMPTION:** Personnel competency per project quality procedures

## Steps

### Step 1: Confirm Qualification Requirements

**Action:** Identify ER clauses and project procurement requirements for OEM qualification.

| Task | Source | Output |
|------|--------|--------|
| Review ER for OEM qualification requirements | ER Vol 2 Parts 1–3 | Requirement list (**TBD**) |
| Review DEL-11.02 for technical requirements | Technical Specification | Technical criteria |
| Confirm hazardous area certification requirements | PKG-27 | Zone classification |
| Confirm project prequalification process | Project procedures | Process confirmation |

**Output:** Qualification requirements checklist.

### Step 2: Define Package Index

**Action:** Create contents list and agree submission structure.

| Task | Output |
|------|--------|
| Define required package sections | Package structure |
| Define required documents per section | Document checklist |
| Agree submission format with procurement | Format agreement |
| Create package index template | Index template |

**Required sections (from decomposition):**

| Section | Documents |
|---------|-----------|
| OEM Qualification Submission | Company profile, manufacturing capability, QA system |
| Comparable Project References | Reference list (minimum 3) |
| Compliance Statements | ER matrix, code compliance, deviation register |
| Supporting Documentation | Brochures, GA drawings, datasheets, certificates |

### Step 3: Issue Enquiry to OEM(s)

**Action:** Request qualification package from candidate OEM(s).

| Task | Responsibility | Output |
|------|----------------|--------|
| Prepare enquiry package | Procurement/Engineering | Enquiry documents |
| Include qualification requirements checklist | Engineering | Requirements attachment |
| Include preliminary DEL-11.02 requirements | Engineering | Technical attachment |
| Issue enquiry to OEM(s) | Procurement | Transmittal record |
| Track responses | Procurement | Response log |

### Step 4: Collect OEM Documents

**Action:** Obtain and organize OEM submission documents.

| Task | Responsibility | Output |
|------|----------------|--------|
| Receive OEM qualification package | Procurement | OEM submission |
| Log all documents with revision/date | QA | Document log |
| Verify completeness against checklist | Engineering | Completeness check |
| Request missing documents | Procurement | Follow-up log |

**OEM submission checklist:**
- [ ] Company profile and organizational chart
- [ ] Manufacturing facility information
- [ ] Quality management system certificate (ISO 9001)
- [ ] Design capability statement
- [ ] After-sales support information
- [ ] Comparable project references (minimum 3)
- [ ] Product brochure/catalog
- [ ] GA drawings with envelope data
- [ ] Standard product datasheets
- [ ] Hazardous area certificates
- [ ] FAT procedure outline
- [ ] Compliance statement (preliminary)

### Step 5: Develop Compliance Statements

**Action:** Prepare compliance matrix and deviation register.

| Task | Responsibility | Output |
|------|----------------|--------|
| Map OEM capabilities to DEL-11.02 requirements | Engineering | Compliance matrix (draft) |
| Map OEM capabilities to ER requirements | Engineering | Compliance matrix (ER section) |
| Identify deviations/exceptions | Engineering | Deviation list |
| Document proposed disposition for each deviation | Engineering | Deviation register |
| Request OEM clarification on any gaps | Procurement | Clarification log |

**Compliance matrix format:**

| Req ID | Requirement | OEM Compliance | Evidence | Deviation? |
|--------|-------------|----------------|----------|------------|
| MLA-001 | Example | Compliant | GA drawing | No |
| MLA-002 | Example | Partial | Datasheet | Yes — see D-001 |

### Step 6: Reference Verification

**Action:** Verify comparable project references.

| Task | Responsibility | Output |
|------|----------------|--------|
| Review references for relevance | Engineering | Relevance assessment |
| Contact reference clients (if required/authorized) | Procurement | Reference feedback |
| Document reference evaluation | Engineering | Reference evaluation form |

**Reference evaluation criteria:**
- Product type: powered marine loading arm with ERC
- Service: vegetable oil or similar liquid bulk
- Environment: marine, coastal
- Age: within last 10 years preferred
- Performance: no significant issues reported

### Step 7: Internal Review

**Action:** Conduct technical and quality review of compiled package.

| Review Type | Participants | Focus |
|-------------|--------------|-------|
| Technical review | Process engineers | OEM capability, product suitability, deviations |
| QA review | QA representative | Document control, completeness, certification validity |
| Procurement review | Procurement specialist | Commercial acceptability, lead time |
| Interface review | Adjacent discipline leads | I&C, electrical, structural interfaces |

**Output:** Review comments log.

### Step 8: Resolve Comments and Deviations

**Action:** Address review comments and finalize deviation dispositions.

| Task | Responsibility | Output |
|------|----------------|--------|
| Respond to all review comments | Engineering | Comment response log |
| Finalize deviation dispositions | Engineering/Management | Approved deviation register |
| Obtain acceptance for critical deviations | Project management | Deviation approvals |
| Update compliance matrix | Engineering | Final compliance matrix |
| Update package index | QA | Final index |

### Step 9: Approve and Issue

**Action:** Obtain approvals and issue qualification package.

| Task | Responsibility | Output |
|------|----------------|--------|
| Engineering approval | Lead engineer | Approval signature |
| QA approval | QA manager | Approval signature |
| Management approval (for deviations) | Project manager | Deviation approvals |
| Document control registration | Document controller | Transmittal |
| Issue to Employer (if required) | Procurement | Transmittal record |

## Verification

**Verification activities (traceability to Specification.md):**

| Verification Method | Requirements Verified | Record |
|---------------------|----------------------|--------|
| Document review | OEM-001 to OEM-005 | Completeness form |
| Completeness check | QUAL, REF, DOC requirements | Checklist |
| Technical review | QUAL-006, INT requirements | Technical evaluation |
| Compliance review | COMP-001 to COMP-006 | Compliance matrix |
| Reference review | REF-001 to REF-006 | Reference evaluation |
| Deviation review | COMP-003, COMP-004 | Deviation register |
| Certificate review | QUAL-003, COMP-005, DOC-004 | Certificate log |

**Acceptance checklist (aligns to Datasheet.md and Specification.md):**

| Criterion | Check | Status |
|-----------|-------|--------|
| Package index present with document list and revisions | Document review | ☐ |
| OEM qualification submission complete | Completeness check | ☐ |
| Minimum 3 comparable project references provided | Reference count | ☐ |
| Compliance statements with ER traceability | Compliance review | ☐ |
| Deviations documented with approved disposition | Deviation review | ☐ |
| Supporting documentation complete and revision controlled | Document review | ☐ |
| Internal review completed and comments resolved | Review records | ☐ |

**Sign-off requirements:**

| Role | Responsibility | Signature Block |
|------|----------------|-----------------|
| Process Engineer | Technical review lead | **TBD** |
| QA Representative | Quality review | **TBD** |
| Lead Engineer | Discipline approval | **TBD** |
| Project Manager | Deviation approval (if required) | **TBD** |

**ASSUMPTION:** Sign-off protocol per project quality procedures.

## Records

**Documentation outputs:**
- OEM qualification submission
- Comparable project references list
- Compliance statements and matrix
- Deviation register (with approvals)
- Supporting documentation package
- Package index

**Record management:**

| Record | Location | Retention |
|--------|----------|-----------|
| Draft package (working) | `1_Working/` | Until superseded |
| Review packages | `2_Checking/To/` | Per project procedures |
| Issued package | `3_Issued/` | Project archive (**TBD**) |
| OEM correspondence | Document control system | Project archive (**TBD**) |
| Deviation approvals | Document control system | Project archive (**TBD**) |

**ASSUMPTION:** Electronic records in project document management system.
