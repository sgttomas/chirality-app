# Procedure: DEL-28.01 Independent Design Verification Reports

## Purpose

This procedure defines the process for producing and managing **Independent Design Verification Reports** within **PKG-28 Design Verification**.

**Deliverable Purpose:** Documents analysis and results for independent design verification reports required for design verification and approvals, supporting **OBJ-6: Regulatory Compliance** — "The Works comply with all permits, codes, and authority requirements."

**Source:** _CONTEXT.md (DEL-28.01 description); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-6)

**Deliverable type:** Report
**Responsible party:** D&B Contractor

**Source:** _CONTEXT.md (deliverable type, responsible party)

**Dual-Use Nature:** This procedure describes both:
1. How to **produce** Independent Design Verification Reports (the report preparation process)
2. How to **conduct** independent design verification (the verification activity itself)

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

**Source:** _DEPENDENCIES.md (dependency tracking mode)

**Upstream deliverables and input data:**

**For each IDV review stage, the following must be available:**
- Completed design documents for the applicable stage (30%, 60%, 90%, or IFC) from discipline packages (PKG-01 through PKG-27, PKG-29 through PKG-36)
- Design submission package for the applicable stage (DEL-27.04) — **ASSUMPTION**: IDV reviews design documents included in submission packages
- Design basis documents and design criteria
- Applicable codes, standards, and Employer's Requirements
- Findings from previous IDV stage (for closure verification) — except for initial 30% review

**Source:** Specification.md (FR-2, IR-1); Datasheet.md (related deliverable: DEL-27.04); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4, Package Summary)

**TBD:** Specific design document lists per discipline and stage

### Reference Materials

**Required references:**
- See `_REFERENCES.md` for applicable reference documents
- See `0_References/` in package directory for reference materials
- Employer's Requirements — **TBD**: Specific ER sections governing IDV requirements and design criteria
- Applicable codes and standards — see Specification.md (Standards section) — **TBD**: Complete code list per discipline
- Project Quality Management Plan — **TBD**: QMP reference
- Project document control procedures — **TBD**: Document control system reference

**Source:** Specification.md (Standards section, IR-3); Datasheet.md (References section)

### Personnel Requirements

**IDV Reviewer Qualifications:**
- Professional Engineer (P.Eng.) licensed in British Columbia (or under EGBC mobility provisions)
- Minimum **TBD** years of experience in applicable discipline
- Demonstrated expertise in applicable codes and standards
- Independent of design team (separate company or separate business unit)
- No direct involvement in design work being reviewed

**Source:** Specification.md (FR-1, PR-3); Datasheet.md (review method: independent third-party); **ASSUMPTION**: BC professional licensing requirements and independence criteria

**IDV Review Team Roles:**
- Lead Reviewer (per discipline) — oversees review, prepares report, signs verification statement
- Checkers/Reviewers (as needed for large scope) — perform detailed review, document findings
- QA/QC Reviewer — reviews IDV report prior to issue

**ASSUMPTION:** Role structure typical for large D&B projects; **TBD**: Specific role requirements and qualifications

**D&B Contractor Coordination Roles:**
- IDV Coordinator — coordinates IDV process, manages schedule, tracks findings
- Discipline Design Leads — respond to findings, coordinate design revisions
- Project Quality Manager — approves IDV methodology and oversees IDV process

**ASSUMPTION:** Contractor coordination roles; **TBD**: Specific responsibilities

## Steps

### Step 1: IDV Planning and Setup

**1.1 Establish IDV Program**
- Define IDV scope for each discipline and design stage (30%, 60%, 90%, IFC)
- Identify applicable codes, standards, and regulatory requirements per discipline
- Develop IDV review checklists based on applicable codes and project requirements — **TBD**: Checklist templates
- Establish finding classification criteria (Critical, Major, Minor) — **TBD**: Classification criteria
- Define IDV schedule aligned with design submission schedule (DEL-27.04)

**Source:** Specification.md (FR-2, FR-3, FR-4, FR-5); Guidance.md (C-1, C-4)

**1.2 Select and Qualify IDV Reviewers**
- Identify and engage qualified IDV reviewers for each discipline
- Verify reviewer qualifications (P.Eng. license, experience, expertise)
- Confirm reviewer independence from design team
- Document reviewer qualifications and certifications

**Source:** Specification.md (FR-1, PR-3); Guidance.md (C-2)

**1.3 Develop IDV Methodology**
- Prepare IDV methodology document describing review approach, criteria, and process
- Submit IDV methodology for approval — **TBD**: Approval authority (Project Quality Manager or Employer)
- Conduct kickoff meeting with IDV reviewers, design teams, and project management

**Source:** Specification.md (V-1); Guidance.md (C-7)

**Verification:** IDV methodology approved and documented; reviewers qualified and contracted; IDV schedule established

### Step 2: Design Document Submittal for IDV Review

**2.1 Prepare Design Submission**
- Design teams complete design deliverables for applicable stage (30%, 60%, 90%, or IFC)
- Compile design document list with revision numbers
- Assemble design submission package including drawings, specifications, calculations, datasheets, reports

**Source:** Specification.md (IR-1); Datasheet.md (related deliverable: DEL-27.04)

**2.2 Transmit to IDV Reviewers**
- Transmit design documents to IDV reviewers via project document management system or secure file transfer
- Provide design document list, design basis documents, and applicable codes/standards
- Provide findings from previous IDV stage (if applicable) for closure verification
- Confirm review scope and schedule with reviewers

**Source:** Specification.md (FR-6, PR-2); Guidance.md (C-1)

**Verification:** Design documents transmitted to IDV reviewers; document list complete; schedule confirmed

### Step 3: Conduct IDV Review

**3.1 Review Design Documents**
IDV reviewers perform independent technical review of design documents using the following approach:

**For each design document (drawing, specification, calculation, report):**
- Verify design basis and criteria are appropriate and consistent with project requirements
- Verify compliance with applicable codes and standards using review checklists
- Verify design assumptions are reasonable and documented
- Verify calculations are correct, complete, and properly documented
- Verify drawings are complete, accurate, and coordinated
- Verify specifications are clear, complete, and consistent with drawings and calculations
- Identify non-compliances, deficiencies, and areas requiring clarification

**Source:** Specification.md (FR-3, FR-4); Guidance.md (P-1, P-2, C-3)

**3.2 Document Findings**
For each finding identified:
- Assign unique finding number (e.g., IDV-[Discipline]-[Stage]-[###])
- Document finding description (clear statement of issue)
- Reference affected design document(s) with revision numbers
- Cite applicable code or standard section
- Classify finding severity (Critical, Major, Minor) per established criteria
- Provide recommended corrective action
- Record in finding tracking system or spreadsheet

**Source:** Specification.md (FR-5); Guidance.md (C-4, E-2)

**3.3 Verify Finding Closures (Stages after 30%)**
For design stages after 30% (i.e., 60%, 90%, IFC):
- Review findings from previous IDV stage
- Verify that design has been revised to address each finding
- Review design revisions for adequacy and code compliance
- Document closure verification for each finding (Closed, Partially Closed, Remain Open)
- Identify any new findings resulting from design revisions

**Source:** Specification.md (FR-6, V-3); Guidance.md (P-3)

**3.4 Complete Review Checklists**
- Complete code compliance checklists for each applicable code/standard section
- Document review coverage and any items not reviewed (with justification)

**Source:** Specification.md (FR-4, PR-1); **ASSUMPTION**: Checklist-based review for completeness verification

**Verification:** All design documents reviewed; findings documented; closure verification completed (if applicable); checklists completed

### Step 4: Prepare IDV Report

**4.1 Compile Report Content**
Prepare IDV report including the following sections (minimum):

1. **Executive Summary** — Key findings, overall compliance status, recommendations
2. **Introduction** — Review scope, objectives, methodology, review criteria
3. **Reviewer Qualifications** — Reviewer credentials, certifications, statement of independence
4. **Design Documents Reviewed** — Table listing all documents with revision numbers and review date
5. **Code and Standard Compliance Checklist** — Compliance verification by code/standard section
6. **Findings** — Detailed findings with severity classification, description, affected documents, code references, recommendations (organized by severity: Critical, Major, Minor)
7. **Closure Verification** (if applicable) — Status of findings from previous stage
8. **Conclusion and Verification Statement** — Overall compliance conclusion, verification statement signed by Lead Reviewer
9. **Appendices** (as needed) — Detailed checklists, supporting documentation

**Source:** Specification.md (D-1); Guidance.md (E-1); Datasheet.md (typical IDV report structure)

**4.2 Internal QA/QC Review**
- Submit draft IDV report for internal QA/QC review
- Address QA/QC comments and revise report
- Obtain QA/QC reviewer approval

**Source:** Specification.md (QR-2, V-2)

**4.3 Finalize and Approve Report**
- Incorporate QA/QC comments
- Obtain Lead Reviewer sign-off on verification statement
- Obtain approver sign-off (senior reviewer or principal) — **TBD**: Specific approval authority
- Assign document number and revision per project document control procedures — **TBD**: Document numbering system

**Source:** Specification.md (QR-3, D-2); **ASSUMPTION**: Standard engineering document approval process

**Verification:** IDV report complete per specification; QA/QC review completed; report approved and signed

### Step 5: Issue IDV Report

**5.1 Issue Report**
- Upload final IDV report to project document management system
- Transmit IDV report to D&B Contractor project management and discipline design leads
- Transmit IDV report to Employer (per submittal requirements) — **TBD**: Submittal protocol
- File issued report in `3_Issued/` folder with document number and date

**Source:** Specification.md (D-3, D-4); Procedure.md (Records section)

**5.2 Conduct Findings Review Meeting**
- Convene meeting with IDV reviewers, discipline design leads, and project management
- Review findings, discuss clarifications, and agree on closure approach
- Establish schedule for finding resolution and re-review (if needed)

**Source:** Specification.md (IR-4); Guidance.md (C-4, T-2)

**Verification:** IDV report issued and transmitted; findings review meeting conducted; closure plan established

### Step 6: Finding Resolution and Closure Tracking

**6.1 Track Findings to Closure**
- Discipline design teams address findings and revise design documents
- IDV Coordinator tracks finding status in finding tracking system
- Updated finding status reported in project status meetings
- Critical and Major findings escalated per project procedures — **TBD**: Escalation protocol

**Source:** Specification.md (V-3, IR-3); Guidance.md (C-4)

**6.2 Verify Finding Closures**
- For significant finding closures, IDV reviewers may perform interim re-review — **TBD**: Re-review criteria
- For all findings, closure verification is performed in next stage IDV review
- Document closure verification in subsequent IDV report

**Source:** Specification.md (FR-6, V-3); Guidance.md (P-3)

**Verification:** All findings tracked in tracking system; finding resolution progress monitored; closures verified

### Step 7: Repeat for Each Design Stage

**Repeat Steps 2-6 for each design submission stage:**
- **30% Design Stage** — Initial comprehensive review; establish baseline compliance
- **60% Design Stage** — Review design development; verify 30% finding closures; identify new findings
- **90% Design Stage** — Review design completion; verify 60% finding closures; identify final issues
- **IFC (Issue for Construction) Stage** — Final comprehensive review; verify all finding closures; confirm construction-ready compliance

**Source:** Specification.md (FR-2); Datasheet.md (review stages: 30%, 60%, 90%, IFC); Guidance.md (P-3, T-6)

**Verification:** IDV reports completed for all required design stages; all findings tracked to closure; final IFC review confirms compliance

## Verification

**Verification activities for IDV Report deliverables:**

**V-1: IDV Methodology Verification**
- IDV methodology reviewed and approved prior to commencement
- **Verification method:** Technical review of methodology
- **Acceptance criteria:** Methodology approved by Project Quality Manager (or designated authority)
- **Source:** Specification.md (V-1)

**V-2: IDV Report Quality Verification**
- Each IDV report subject to internal QA/QC review prior to issue
- **Verification method:** QA/QC review by qualified reviewer independent of report preparation
- **Acceptance criteria:** QA/QC reviewer approval; report complete per Specification.md (D-1)
- **Source:** Specification.md (QR-2, V-2)

**V-3: Finding Tracking and Closure Verification**
- All findings tracked in finding tracking system
- Finding closures verified in subsequent stage IDV reviews
- **Verification method:** Tracking system reports; closure verification documented in IDV reports
- **Acceptance criteria:** All Critical findings closed prior to IFC; Major and Minor findings closed or accepted by Employer
- **Source:** Specification.md (V-3); **ASSUMPTION**: Finding closure criteria

**V-4: Regulatory Acceptance (if required)**
- IDV reports may be submitted to regulatory authorities as part of permit applications
- **Verification method:** Regulatory authority review
- **Acceptance criteria:** Authority acceptance or approval per authority requirements — **TBD**: Specific requirements per authority
- **Source:** Specification.md (V-4)

**V-5: Final IDV Acceptance**
- Final IDV reports (IFC stage) reviewed and accepted by D&B Contractor project management
- **Verification method:** Management review and approval
- **Acceptance criteria:**
  - IDV reports complete and compliant with Specification.md
  - All Critical and Major findings closed or dispositioned
  - Reviewer qualifications verified
  - Reports approved per project procedures
- **Source:** Specification.md (Verification section, Acceptance criteria)

**Sign-off requirements:**

| Role | Sign-off Requirement | Document Location |
|------|---------------------|-------------------|
| Lead IDV Reviewer (per discipline) | Verification statement signature | IDV Report (Conclusion section) |
| QA/QC Reviewer | Approval of IDV report | Internal review record |
| D&B Contractor Approver | Approval for issue | Document control cover sheet or approval record — **TBD**: Specific approval documentation |
| Project Quality Manager | Acceptance of IDV program and findings closure | Project quality records — **TBD** |

**Source:** Specification.md (V-2, Acceptance criteria); **ASSUMPTION**: Sign-off roles and requirements typical for D&B projects

## Records

**Documentation outputs:**

**Primary Deliverables:**
- IDV reports (by discipline/submission stage): IDV-[Discipline]-[Stage]
  - Examples: IDV-CIVIL-30, IDV-STRUCT-60, IDV-MECH-90, IDV-ELEC-IFC
  - Typical count: 8 disciplines × 4 stages = 32 IDV reports (may vary based on project needs)

**Source:** _CONTEXT.md (anticipated artifacts); Specification.md (D-1); Datasheet.md (report series naming convention)

**Supporting Records:**
- IDV methodology document
- IDV reviewer qualifications and certifications
- IDV review checklists (by discipline and stage)
- Finding tracking system / finding log
- Finding closure verification records
- IDV review meeting minutes
- Internal QA/QC review records
- Approval and sign-off records

**Source:** Steps 1-7 above; Specification.md (V-1, V-2, V-3); **ASSUMPTION**: Supporting records typical for quality management

**Record management:**

**Filing and Storage:**
- **Working documents**: Stored in `1_Working/DEL-28.01_Independent_Design_Verification_Reports/` folder
- **Documents under review**: Copied to `2_Checking/To/` with document number and date
- **Issued reports**: Filed in `3_Issued/` with final document number, revision, and date
- **Electronic records**: Stored in project document management system with appropriate metadata and access controls

**Source:** Specification.md (D-3); **ASSUMPTION**: Standard project document management structure

**Retention requirements:**
- **TBD**: Project records retention per contract requirements (typically 7-10 years post-project completion for engineering records)
- **ASSUMPTION**: Long-term retention for regulatory compliance and professional liability

**Document Control:**
- Document numbering: **TBD** — **ASSUMPTION**: Per project numbering system (e.g., IDV-[Discipline]-[Stage]-[Rev])
- Revision control: **TBD** — **ASSUMPTION**: Revision tracking per document management system (e.g., Rev 0, Rev A, Rev B)
- Format: **TBD** — **ASSUMPTION**: PDF for issued reports, MS Word or similar for working drafts
- Access control: Project team access for working documents; controlled distribution for issued reports

**Source:** Specification.md (QR-3, D-2); Datasheet.md (report format TBD)

**Submittal to Employer:**
- IDV reports submitted to Employer as part of or alongside design submission packages (DEL-27.04)
- Submittal format and protocol: **TBD** — **ASSUMPTION**: Per project submittal procedures
- Submittal schedule: Aligned with design submission schedule (30%, 60%, 90%, IFC stages)

**Source:** Specification.md (D-4); Datasheet.md (related deliverable: DEL-27.04); Guidance.md (E-4)
