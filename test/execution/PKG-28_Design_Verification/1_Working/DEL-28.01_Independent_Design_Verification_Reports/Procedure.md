# Procedure: DEL-28.01 Independent Design Verification Reports

## Purpose

This procedure defines the process for producing and managing **Independent Design Verification Reports** within **PKG-28 Design Verification**.

**Deliverable Purpose:** Documents analysis and results for independent design verification reports required for design verification and approvals, supporting **OBJ-6: Regulatory Compliance** — "The Works comply with all permits, codes, and authority requirements."

**Source:** _CONTEXT.md (DEL-28.01 description); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-6)

**Deliverable type:** Report
**Responsible party:** D&B Contractor

**Dual-Use Nature:** This procedure describes both:
1. How to **produce** Independent Design Verification Reports (report preparation process)
2. How to **conduct** independent design verification (verification activity itself)

**Cross-Document References:**
- Datasheet.md — Identification, Attributes, Conditions, Construction, References
- Specification.md — Requirements FR-1 through FR-6, PR-1 through PR-3, IR-1 through IR-4, QR-1 through QR-3
- Guidance.md — Principles P-1 through P-5, Considerations C-1 through C-8, Trade-offs T-1 through T-6

**Source:** _CONTEXT.md (deliverable type, responsible party)

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

**Source:** _DEPENDENCIES.md (dependency tracking mode)

**Upstream deliverables and input data:**

| Input | Source | Specification Req | Status |
|-------|--------|-------------------|--------|
| Design documents for applicable stage | PKG-01 through PKG-27, PKG-29 through PKG-36 | FR-2, IR-1 | Required |
| Design submission package | DEL-27.04 | IR-1 | Required |
| Design basis documents and criteria | Various | FR-4 | Required |
| Applicable codes, standards, ERs | — | FR-4 | Required |
| Previous stage IDV findings | DEL-28.01 (prior stage) | FR-6 | Required (except 30%) |

**TBD:** Specific design document lists per discipline and stage

**Source:** Specification.md (FR-2, IR-1); Datasheet.md (Cross-Deliverable Coordination)

### Reference Materials

| Reference | Location | Status |
|-----------|----------|--------|
| Applicable reference documents | _REFERENCES.md | See file |
| Package reference materials | 0_References/ | See folder |
| Employer's Requirements | — | **TBD**: Specific ER sections |
| Applicable codes and standards | — | **TBD**: Per discipline |
| Project Quality Management Plan | — | **TBD**: QMP reference |
| Project document control procedures | — | **TBD**: Reference |

**Source:** Specification.md (Standards section, IR-3); Datasheet.md (References section)

### Personnel Requirements

**IDV Reviewer Qualifications** — See Specification.md FR-1, PR-3; Guidance.md C-2:

| Role | Qualifications | Independence Requirement |
|------|----------------|-------------------------|
| Lead Reviewer (per discipline) | P.Eng. (BC); **TBD** years experience; discipline expertise | Independent of design team |
| Checker/Reviewer | P.Eng. (BC) or EIT under supervision; discipline knowledge | Independent of design team |
| QA/QC Reviewer | Quality professional; IDV report review experience | Independent of report preparation |

**D&B Contractor Coordination Roles:**

| Role | Responsibility |
|------|----------------|
| IDV Coordinator | Coordinates IDV process, manages schedule, tracks findings |
| Discipline Design Leads | Respond to findings, coordinate design revisions |
| Project Quality Manager | Approves IDV methodology, oversees IDV process |

**Source:** Specification.md (FR-1, PR-3); Guidance.md (C-2); **ASSUMPTION**: Role structure typical for D&B projects

## Steps

### Step Summary

| Step | Activity | Specification Req | Guidance § | Verification |
|------|----------|-------------------|------------|--------------|
| 1 | IDV Planning and Setup | FR-1, FR-2, FR-3, FR-4, FR-5, IR-3 | C-1, C-2, C-4, C-7 | V-1 |
| 2 | Design Document Submittal for IDV Review | IR-1, PR-2 | C-1, P-5 | — |
| 3 | Conduct IDV Review | FR-3, FR-4, FR-5, FR-6, PR-1 | P-1, P-2, C-3, C-4 | V-3 |
| 4 | Prepare IDV Report | QR-2, QR-3, D-1 | E-1 | V-2 |
| 5 | Issue IDV Report | D-3, D-4, IR-4 | C-5, T-2 | — |
| 6 | Finding Resolution and Closure Tracking | FR-6, IR-3 | C-4, P-3 | V-3 |
| 7 | Repeat for Each Design Stage | FR-2 | P-3, T-6 | V-5 |

### Step 1: IDV Planning and Setup

**1.1 Establish IDV Program** — Specification.md FR-2, FR-3, FR-4, FR-5; Guidance.md C-1, C-4
- Define IDV scope for each discipline and design stage (30%, 60%, 90%, IFC)
- Identify applicable codes, standards, and regulatory requirements per discipline — See Datasheet.md (Construction: Review Coverage by Discipline)
- Develop IDV review checklists based on applicable codes and project requirements — **TBD**: Checklist templates
- Establish finding classification criteria (Critical, Major, Minor) — **TBD**: Classification criteria
- Define IDV schedule aligned with design submission schedule (DEL-27.04)

**1.2 Select and Qualify IDV Reviewers** — Specification.md FR-1, PR-3; Guidance.md C-2
- Identify and engage qualified IDV reviewers for each discipline
- Verify reviewer qualifications (P.Eng. license, experience, expertise)
- Confirm reviewer independence from design team
- Document reviewer qualifications and certifications

**1.3 Develop IDV Methodology** — Specification.md QR-1, V-1; Guidance.md C-7
- Prepare IDV methodology document describing review approach, criteria, and process
- Submit IDV methodology for approval — **TBD**: Approval authority (Project Quality Manager or Employer)
- Conduct kickoff meeting with IDV reviewers, design teams, and project management

**Verification:** IDV methodology approved (V-1); reviewers qualified; IDV schedule established

### Step 2: Design Document Submittal for IDV Review

**2.1 Prepare Design Submission** — Specification.md IR-1; Guidance.md P-5
- Design teams complete design deliverables for applicable stage (30%, 60%, 90%, or IFC)
- Compile design document list with revision numbers
- Assemble design submission package including drawings, specifications, calculations, datasheets, reports

**2.2 Transmit to IDV Reviewers** — Specification.md IR-1, PR-2; Guidance.md C-1
- Transmit design documents to IDV reviewers via project document management system
- Provide design document list, design basis documents, and applicable codes/standards
- Provide findings from previous IDV stage (if applicable) for closure verification
- Confirm review scope and schedule with reviewers

**Verification:** Design documents transmitted; document list complete; schedule confirmed

### Step 3: Conduct IDV Review

**3.1 Review Design Documents** — Specification.md FR-3, FR-4; Guidance.md P-1, P-2, C-3

IDV reviewers perform independent technical review of design documents:

| Review Activity | Verification Focus | Code Reference |
|-----------------|-------------------|----------------|
| Design basis verification | Criteria appropriate and consistent | Project design basis |
| Code compliance | Compliance with applicable codes/standards | Per discipline codes |
| Assumption review | Assumptions reasonable and documented | Design documentation |
| Calculation verification | Correct, complete, properly documented | Per discipline standards |
| Drawing verification | Complete, accurate, coordinated | Project standards |
| Specification verification | Clear, complete, consistent | Project standards |
| Non-compliance identification | Issues requiring correction | Applicable codes |

**3.2 Document Findings** — Specification.md FR-5; Guidance.md C-4, E-2

For each finding identified:

| Field | Content | Example |
|-------|---------|---------|
| Finding Number | IDV-[Discipline]-[Stage]-[###] | IDV-CIVIL-30-001 |
| Description | Clear statement of issue | Foundation design missing seismic load case |
| Affected Documents | Document numbers with revisions | Drawing C-101 Rev A |
| Code Reference | Applicable code/standard section | NBC 2020 Section 4.1.8 |
| Severity | Critical / Major / Minor | Critical |
| Recommendation | Corrective action required | Revise design to include seismic loads |

**3.3 Verify Finding Closures** — Specification.md FR-6; Guidance.md P-3

For design stages after 30% (60%, 90%, IFC):
- Review findings from previous IDV stage
- Verify that design has been revised to address each finding
- Review design revisions for adequacy and code compliance
- Document closure verification: Closed / Partially Closed / Remain Open
- Identify any new findings resulting from design revisions

**3.4 Complete Review Checklists** — Specification.md PR-1; Guidance.md C-3
- Complete code compliance checklists for each applicable code/standard section
- Document review coverage and any items not reviewed (with justification)

**Verification:** All documents reviewed; findings documented (V-3); closures verified; checklists completed

### Step 4: Prepare IDV Report

**4.1 Compile Report Content** — Specification.md D-1; Guidance.md E-1; Datasheet.md Construction

Prepare IDV report including the following sections (minimum):

| Section | Content | Datasheet Ref |
|---------|---------|---------------|
| 1. Executive Summary | Key findings, overall compliance status, recommendations | Construction (Report Structure) |
| 2. Introduction | Review scope, objectives, methodology, review criteria | Construction (Report Structure) |
| 3. Reviewer Qualifications | Credentials, certifications, statement of independence | Construction (Report Structure) |
| 4. Design Documents Reviewed | Table listing documents with revision numbers and date | Construction (Report Structure) |
| 5. Compliance Checklist | Verification by code/standard section | Construction (Report Structure) |
| 6. Findings | Detailed findings by severity (Critical, Major, Minor) | Construction (Report Structure) |
| 7. Closure Verification | Status of previous stage findings (if applicable) | Construction (Report Structure) |
| 8. Conclusion and Verification Statement | Compliance conclusion, Lead Reviewer signature | Construction (Report Structure) |
| 9. Appendices | Detailed checklists, supporting documentation | Construction (Report Structure) |

**4.2 Internal QA/QC Review** — Specification.md QR-2, V-2
- Submit draft IDV report for internal QA/QC review
- Address QA/QC comments and revise report
- Obtain QA/QC reviewer approval

**4.3 Finalize and Approve Report** — Specification.md QR-3, D-2
- Incorporate QA/QC comments
- Obtain Lead Reviewer sign-off on verification statement
- Obtain approver sign-off — **TBD**: Specific approval authority
- Assign document number and revision per project document control procedures — **TBD**: Numbering system

**Verification:** Report complete per D-1 (V-2); QA/QC review completed; report approved and signed

### Step 5: Issue IDV Report

**5.1 Issue Report** — Specification.md D-3, D-4; Guidance.md C-5, C-6
- Upload final IDV report to project document management system
- Transmit IDV report to D&B Contractor project management and discipline design leads
- Transmit IDV report to Employer (per submittal requirements) — **TBD**: Submittal protocol
- File issued report in `3_Issued/` folder with document number and date

**5.2 Conduct Findings Review Meeting** — Specification.md IR-4; Guidance.md T-2
- Convene meeting with IDV reviewers, discipline design leads, and project management
- Review findings, discuss clarifications, and agree on closure approach
- Establish schedule for finding resolution and re-review (if needed)

**Verification:** IDV report issued and transmitted; findings review meeting conducted; closure plan established

### Step 6: Finding Resolution and Closure Tracking

**6.1 Track Findings to Closure** — Specification.md FR-6, IR-3; Guidance.md C-4
- Discipline design teams address findings and revise design documents
- IDV Coordinator tracks finding status in finding tracking system
- Updated finding status reported in project status meetings
- Critical and Major findings escalated per project procedures — **TBD**: Escalation protocol

**6.2 Verify Finding Closures** — Specification.md FR-6, V-3; Guidance.md P-3
- For significant finding closures, IDV reviewers may perform interim re-review — **TBD**: Re-review criteria
- For all findings, closure verification is performed in next stage IDV review
- Document closure verification in subsequent IDV report

**Verification:** All findings tracked (V-3); resolution progress monitored; closures verified

### Step 7: Repeat for Each Design Stage

**Repeat Steps 2-6 for each design submission stage** — Specification.md FR-2; Guidance.md P-3, T-6:

| Stage | Focus | Finding Closure Verification |
|-------|-------|------------------------------|
| 30% Design | Initial comprehensive review; establish baseline compliance | N/A (first review) |
| 60% Design | Review design development; verify 30% finding closures | 30% findings |
| 90% Design | Review design completion; verify 60% finding closures | 60% findings |
| IFC (Issue for Construction) | Final comprehensive review; confirm construction-ready compliance | All prior findings |

**Verification:** IDV reports completed for all required stages (V-5); all findings tracked to closure; final IFC review confirms compliance

## Verification

**Verification activities for IDV Report deliverables:**

| Verification ID | Method | Acceptance Criteria | Procedure Step |
|-----------------|--------|---------------------|----------------|
| V-1 | Technical review of IDV methodology | Methodology approved by Project Quality Manager | Step 1.3 |
| V-2 | QA/QC review of IDV report | Report complete per Specification.md D-1; QA/QC approval | Step 4.2 |
| V-3 | Finding tracking and closure verification | All Critical findings closed prior to IFC; Major/Minor closed or accepted | Step 6 |
| V-4 | Regulatory authority review (if required) | Authority acceptance per requirements | Step 5.1 |
| V-5 | Final IDV acceptance | Reports complete; findings closed; reviewers qualified; approved | Step 7 |

**Sign-off Requirements:**

| Role | Sign-off Requirement | Document Location | Specification Req |
|------|---------------------|-------------------|-------------------|
| Lead IDV Reviewer (per discipline) | Verification statement signature | IDV Report Section 8 | FR-1 |
| QA/QC Reviewer | Approval of IDV report | Internal review record | QR-2 |
| D&B Contractor Approver | Approval for issue | Document control cover sheet | QR-3 |
| Project Quality Manager | IDV program and findings closure acceptance | Project quality records | IR-3, QR-1 |

**Source:** Specification.md (Verification section); Guidance.md (Principles P-1 through P-5)

## Records

**Documentation outputs:**

**Primary Deliverables:**

| Document Type | Naming Convention | Typical Count | Source |
|---------------|-------------------|---------------|--------|
| IDV Reports | IDV-[Discipline]-[Stage] | ~32 (8 disciplines × 4 stages) | Specification.md D-1 |

Examples: IDV-CIVIL-30, IDV-STRUCT-60, IDV-MECH-90, IDV-ELEC-IFC

**Source:** _CONTEXT.md (anticipated artifacts); Datasheet.md (Attributes: Report Series)

**Supporting Records:**

| Record Type | Purpose | Retention |
|-------------|---------|-----------|
| IDV methodology document | Documents review approach | Project duration |
| Reviewer qualifications and certifications | Demonstrates competency | Project duration |
| IDV review checklists | Documents review coverage | Per discipline/stage |
| Finding tracking log | Tracks finding status | Project duration |
| Finding closure verification records | Documents closure | Project duration |
| IDV review meeting minutes | Documents discussions | Project duration |
| Internal QA/QC review records | Documents quality review | Project duration |
| Approval and sign-off records | Documents authorizations | Project duration |

**Source:** Steps 1-7 above; Specification.md (V-1, V-2, V-3)

**Record Management:**

| Location | Purpose | Documents |
|----------|---------|-----------|
| `1_Working/DEL-28.01.../` | Working documents | Drafts, working files |
| `2_Checking/To/` | Documents under review | Draft reports with date |
| `3_Issued/` | Issued reports | Final reports with number, revision, date |
| Project DMS | Electronic records | All records with metadata |

**Source:** Specification.md (D-3)

**Document Control:**
- Document numbering: **TBD** — Per project numbering system
- Revision control: **TBD** — Per document management system (e.g., Rev 0, Rev A, Rev B)
- Format: **TBD** — PDF for issued; MS Word or similar for drafts
- Access control: Project team access for working; controlled distribution for issued
- Retention: **TBD** — Per contract requirements (typically 7-10 years post-project)

**Source:** Specification.md (QR-3, D-2); Datasheet.md (Attributes: Report Format)

**Submittal to Employer:**
- IDV reports submitted alongside design submission packages (DEL-27.04)
- Submittal format and protocol: **TBD** — Per project submittal procedures
- Submittal schedule: Aligned with design submission schedule (30%, 60%, 90%, IFC)

**Source:** Specification.md (D-4); Datasheet.md (Cross-Deliverable Coordination)

## Cross-Document Consistency Notes

This procedure has been verified for consistency with:
- **Datasheet.md**: All procedure steps reference appropriate Datasheet sections
- **Specification.md**: All steps implement specific requirements (FR, PR, IR, QR)
- **Guidance.md**: Steps are informed by principles (P) and considerations (C)

**Step-to-Requirement Traceability:**

| Procedure Step | Specification Requirements | Guidance Sections |
|----------------|---------------------------|-------------------|
| Step 1 | FR-1, FR-2, FR-3, FR-4, FR-5, IR-3, QR-1, V-1 | C-1, C-2, C-4, C-7, P-1 |
| Step 2 | IR-1, PR-2 | C-1, P-5 |
| Step 3 | FR-3, FR-4, FR-5, FR-6, PR-1 | P-1, P-2, C-3, C-4, E-2 |
| Step 4 | QR-2, QR-3, D-1, D-2, V-2 | E-1, C-8 |
| Step 5 | D-3, D-4, IR-4 | C-5, C-6, T-2 |
| Step 6 | FR-6, IR-3, V-3 | C-4, P-3 |
| Step 7 | FR-2 | P-3, T-6 |

**Verification performed per:** AGENT_4_DOCUMENTS_REVISED_v3.md (Step 5, Cross-Reference and Iterate)
