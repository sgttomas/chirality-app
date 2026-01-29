# Procedure: DEL-28.03 Design Coordination Installation & Test Records

## Purpose

This procedure defines the process for producing and managing **Design Coordination Installation & Test Records** within **PKG-28 Design Verification**.

**Deliverable Purpose:** Provides evidence of completion, inspection, and testing for design coordination, supporting design quality, constructability, and **OBJ-6: Regulatory Compliance** — "The Works comply with all permits, codes, and authority requirements."

**Source:** _CONTEXT.md (DEL-28.03 description); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-6)

**Deliverable type:** Record
**Responsible party:** D&B Contractor (QA/QC)

**Dual-Use Nature:** This procedure describes both:
1. How to **produce** design coordination records (documentation process)
2. How to **conduct** design coordination (coordination activity itself)

**Cross-Document References:**
- Datasheet.md — Identification, Attributes, Conditions, Construction, References
- Specification.md — Requirements FR-1 through FR-7, PR-1 through PR-3, IR-1 through IR-6, QR-1 through QR-4
- Guidance.md — Principles P-1 through P-6, Considerations C-1 through C-9, Trade-offs T-1 through T-6

**Source:** _CONTEXT.md (deliverable type, responsible party)

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

**Source:** _DEPENDENCIES.md (dependency tracking mode)

**Upstream deliverables and input data:**

| Input | Source | Specification Req | Status |
|-------|--------|-------------------|--------|
| Design documents from all disciplines | PKG-01 through PKG-36 | IR-1 | Required (ongoing) |
| Coordination procedures and tools | Project setup | IR-5, IR-6 | Required |
| BIM Execution Plan (if BIM used) | Project setup | IR-5 | Required if BIM |
| Quality Management Plan | Project setup | IR-6 | Required |

**Coordination Prerequisites:**
- Project initiated and design teams mobilized
- Discipline design work underway or planned
- Coordination procedures and tools established

**Source:** Specification.md (IR-1, IR-5, IR-6); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4)

### Reference Materials

| Reference | Location | Status |
|-----------|----------|--------|
| Applicable reference documents | _REFERENCES.md | See file |
| Package reference materials | 0_References/ | See folder |
| BIM Execution Plan | — | **TBD**: If BIM used |
| Project Quality Management Plan | — | **TBD** |
| Employer's Requirements | — | **TBD**: Specific ER sections |

**Source:** Specification.md (Standards section, IR-5, IR-6); Datasheet.md (References section)

### Personnel Requirements

| Role | Responsibility | Qualifications | Specification Req |
|------|----------------|----------------|-------------------|
| Design Coordination Lead | Overall coordination, facilitates meetings, manages records | — | FR-1, FR-2 |
| BIM Coordinator (if BIM) | Manages models, performs clash detection | BIM software expertise | FR-3, FR-4 |
| RFI Coordinator | Manages RFI process and tracking | — | FR-5 |
| QA/QC Manager | Oversees coordination as quality management | — | QR-1, QR-2 |
| Discipline Design Leads | Represent disciplines, resolve coordination issues | P.Eng. (BC) — **TBD** | IR-1 |

**Source:** Datasheet.md (Conditions: Coordination Scope); Guidance.md (C-2)

## Steps

### Step Summary

| Step | Activity | Specification Req | Guidance § | Verification |
|------|----------|-------------------|------------|--------------|
| 1 | Establish Coordination Framework | FR-2, FR-3, FR-5, IR-5, IR-6, QR-1 | C-1, C-2, C-4, C-5 | — |
| 2 | Conduct Regular Coordination Meetings | FR-1, FR-2, PR-1, PR-3 | P-2, C-3, E-1 | V-1 |
| 3 | Perform BIM Clash Detection (if BIM) | FR-3, FR-4, PR-1, IR-5 | P-4, C-4, T-3, E-2 | V-1 |
| 4 | Resolve Coordination Issues | FR-4, FR-5, FR-6, FR-7, PR-2, IR-1 | P-6, C-5, C-6, C-7, E-3, E-4 | V-3 |
| 5 | Pre-Submission Coordination Verification | IR-2, PR-2 | P-2, C-8 | V-3 |
| 6 | Maintain Coordination Records | QR-3, D-1 through D-7 | C-9 | V-1 |
| 7 | Final Coordination Records Compilation | QR-3, QR-4, D-7 | C-9 | V-1, V-2, V-4, V-5 |
| 8 | Submittal to Employer (if required) | D-8 | — | — |

### Step 1: Establish Coordination Framework

**1.1 Develop Coordination Plan** — Specification.md FR-2, FR-3, FR-5, IR-5, IR-6, QR-1; Guidance.md C-1
- Define coordination approach:
  - Coordination meeting frequency and schedule — **TBD**
  - BIM coordination requirements (if applicable) — **TBD**: Per BEP
  - RFI process and protocols
  - Interface management approach
  - Issue tracking and escalation procedures
- Document coordination plan in QMP or separate document

**1.2 Assign Coordination Roles** — Guidance.md C-2
- Assign roles per Personnel Requirements above
- Communicate roles to project team
- Establish authority levels for coordination decisions

**1.3 Set Up Coordination Tools** — Specification.md FR-3, FR-5, FR-7; Guidance.md C-1, C-4, C-5
- Set up BIM coordination environment (if BIM): model repository, clash software, standards
- Set up RFI tracking system with log template
- Set up coordination issue tracking system
- Set up meeting schedule
- Train project team on tools and processes

**Verification:** Framework established; roles assigned; tools operational; team trained

### Step 2: Conduct Regular Coordination Meetings

**2.1 Schedule and Convene Meetings** — Specification.md FR-1, FR-2; Guidance.md P-2, C-3
- Hold regular meetings per schedule (e.g., weekly/bi-weekly during active design)
- Distribute agenda in advance (1-2 days prior) — **TBD**
- Ensure discipline leads attend or send qualified delegates

**2.2 Facilitate Coordination Discussion** — Guidance.md E-1

Typical agenda:
1. Review action items from previous meeting
2. Design status update by discipline
3. Interface issues and coordination topics
4. Clash detection results review (if available)
5. RFI status and escalations
6. Assign new action items with responsibility and due date
7. Schedule next meeting

**2.3 Document Meeting Minutes** — Specification.md FR-1, PR-3, D-1; Datasheet.md Construction; Guidance.md E-1

Document minutes including:

| Element | Content |
|---------|---------|
| Meeting ID | Sequential (COORD-MTG-001, etc.) |
| Date/Time/Location | Meeting details |
| Attendees | Names, disciplines |
| Discussion Topics | Interface issues discussed |
| Decisions Made | Coordination decisions |
| Action Items | Responsible party, due date |
| Next Meeting | Scheduled date |

- Issue minutes within **TBD** days (e.g., 2-5 days)
- Distribute to attendees and file in document management system

**Verification:** Meetings held per schedule (V-1); minutes documented and distributed; action items tracked

### Step 3: Perform BIM Clash Detection (if BIM is used)

**3.1 Federate Discipline Models** — Specification.md FR-3; Guidance.md C-4
- Collect current models from all disciplines
- Federate in clash detection software (e.g., Navisworks)
- Verify models are current revisions and properly georeferenced

**3.2 Run Clash Detection** — Specification.md FR-3; Guidance.md T-3
- Perform clash detection per defined frequency:
  - **Minimum**: Prior to each design submission (30%, 60%, 90%, IFC)
  - **TBD**: Additional interim frequency (e.g., weekly/bi-weekly during active design)
- Use clash detection rules and filters appropriate to design stage

**3.3 Review and Classify Clashes** — Specification.md FR-4; Datasheet.md Construction; Guidance.md C-7

Classify by severity:

| Severity | Definition | Action |
|----------|------------|--------|
| Critical | Affects structure, safety, code compliance | Must resolve before submission |
| Major | Affects functionality or constructability | Should resolve before submission |
| Minor | Minimal impact | Resolve during design or construction |

Assign clashes to responsible disciplines for resolution

**3.4 Generate Clash Detection Report** — Specification.md FR-3, FR-4, D-2; Guidance.md E-2

Generate report showing:
- Clash detection run date and model revisions
- Total clashes and breakdown by severity
- Clashes by discipline pair
- Individual clash details (location, disciplines, classification, responsible, status)

Export to PDF and distribute to discipline leads; file in document management system

**Verification:** Clash detection performed per schedule (V-1); clashes classified and assigned; report generated and distributed

### Step 4: Resolve Coordination Issues (Clashes, RFIs, Interface Questions)

**4.1 Clash Resolution** — Specification.md FR-4; Guidance.md P-6
- Responsible discipline reviews clash and determines resolution approach
- Discipline updates design documents to resolve clash
- Discipline updates clash status in tracking system
- BIM Coordinator verifies resolution in updated models

**4.2 RFI Processing** — Specification.md FR-5, PR-2; Datasheet.md Construction; Guidance.md C-5, E-3

When design question/clarification needed:

| Step | Activity |
|------|----------|
| 1 | Originating discipline submits RFI |
| 2 | RFI Coordinator logs with unique number |
| 3 | RFI routed to addressee |
| 4 | Addressee prepares and submits response |
| 5 | RFI Coordinator updates log with response |
| 6 | Originating discipline confirms resolution and closes RFI |

**TBD**: RFI response timeframe (e.g., 5-10 business days)

**4.3 Interface Coordination** — Specification.md FR-6; Datasheet.md Construction; Guidance.md C-6, E-4

For complex/critical interfaces:
- Affected disciplines coordinate interface requirements
- Document agreement in interface register or meeting minutes
- Verify agreement reflected in design documents
- Update register status: TBD → Agreed → Verified

**4.4 Escalation of Critical Issues** — Specification.md FR-7, PR-2; Guidance.md P-6, C-7

For critical/high-priority issues not being resolved:
- Coordination Lead escalates to project management
- Project management intervenes to facilitate resolution
- Critical issues tracked until resolved

**Verification:** Issues tracked and resolved (V-3); critical issues escalated; RFIs responded

### Step 5: Pre-Submission Coordination Verification

Prior to each major design submission (30%, 60%, 90%, IFC):

**5.1 Coordination Status Review** — Specification.md IR-2, PR-2; Guidance.md P-2, C-8

Review status:
- All coordination meetings held and documented
- Clash detection performed on current models
- All critical and major clashes resolved
- All critical and high-priority issues resolved
- All overdue RFIs resolved or have approved action plans
- Interface agreements documented and reflected in design

Prepare coordination status summary

**5.2 Final Clash Detection Run** — Specification.md FR-3, FR-4, PR-2
- Perform final clash detection on submission models
- Verify all critical and major clashes resolved
- Document any remaining minor clashes with justification for deferral
- Issue final clash detection report for submission

**5.3 Coordination Sign-Off** (if required)
- Obtain coordination sign-off from discipline leads confirming designs are coordinated
- **TBD**: Sign-off requirements and format

**Verification:** Status verified (V-3); critical and major issues resolved; coordination readiness confirmed

### Step 6: Maintain Coordination Records

Throughout design development:

**6.1 File Coordination Meeting Minutes** — Specification.md FR-1, PR-3, D-1, D-7; Guidance.md C-9
- File minutes in document management system within **TBD** days
- File in `1_Working/DEL-28.03.../` or designated folder
- Maintain sequential filing (COORD-MTG-001, COORD-MTG-002, etc.)

**6.2 Maintain RFI Log** — Specification.md FR-5, D-3, D-7
- Maintain log in real-time as RFIs submitted and responded
- Keep log accessible to project team
- Export snapshots at milestones (30%, 60%, 90%, IFC)
- File snapshots in coordination records folder

**6.3 File Clash Detection Reports** — Specification.md D-2, D-7
- File reports after each clash run
- Sequential filing by date and stage (CLASH-REPORT-2026-02-15-60PCT, etc.)

**6.4 Maintain Coordination Issue Logs** (if used) — Specification.md FR-7, D-5, D-7
- Maintain logs in real-time
- Export snapshots at milestones
- File in coordination records folder

**Verification:** Records filed systematically (V-1); living documents current and accessible

### Step 7: Final Coordination Records Compilation

At project completion or final design submission (IFC):

**7.1 Compile Final Coordination Record Package** — Specification.md D-1 through D-5, D-7
Compile final package including:
- All coordination meeting minutes
- All clash detection reports
- Final RFI log export
- Final interface registers (if used)
- Final coordination issue logs (if used)
- Coordination status summary

Organize in logical structure

**7.2 Final QA/QC Review** — Specification.md V-1, V-2, V-4; Guidance.md C-9
- Perform completeness check (V-1)
- Verify data accuracy (V-2)
- Obtain QA/QC approval (V-4)

**7.3 File Final Coordination Records** — Specification.md QR-3, QR-4, D-6, D-7
- File in `3_Issued/`
- Assign final document number and date — **TBD**
- File in document management system with proper metadata
- Retain per record retention requirements (V-5)

**Verification:** Records compiled, reviewed, filed; complete and accurate (V-1, V-2, V-4, V-5)

### Step 8: Submittal to Employer (if required)

**8.1 Prepare Coordination Records Submittal** — Specification.md D-8
- Prepare records per contract requirements — **TBD**
- Typical: Status summaries with submissions; detailed records upon request

**8.2 Submit to Employer**
- Submit per submittal protocol
- Log submittal in correspondence system

**Verification:** Records submitted per requirements (if required); logged

## Verification

**Verification activities for Design Coordination Record deliverables:**

| Verification ID | Method | Acceptance Criteria | Procedure Step |
|-----------------|--------|---------------------|----------------|
| V-1 | Records completeness check | All meetings documented; all clash runs documented; RFI log complete | Step 6, Step 7.2 |
| V-2 | Data accuracy verification | Records accurate and consistent with source data | Step 7.2 |
| V-3 | Coordination issue closure | Critical clashes/issues resolved; major items resolved or action plans in place | Step 5 |
| V-4 | Record approval verification | Required approvals obtained | Step 7.2 |
| V-5 | Archival format compliance | Records properly filed and retrievable | Step 7.3 |

**Sign-off Requirements:**

| Role | Sign-off Requirement | Document Location | Specification Req |
|------|---------------------|-------------------|-------------------|
| Meeting Chair / Coordination Lead | Meeting minutes approval | Minutes (signature or approval record) | FR-1, QR-2 |
| BIM Coordinator (if BIM) | Clash detection report approval | Report (signature or approval record) | FR-3 |
| RFI Coordinator | RFI log compilation approval | Log export (cover sheet or approval record) | FR-5 |
| D&B Contractor QA/QC Manager | Final record package approval | Final package (cover sheet or approval record) | QR-1, QR-2 |

**Source:** Specification.md (Verification section); Guidance.md (P-5)

## Records

**Documentation outputs:**

**Primary Deliverables:**

| Document Type | Naming Convention | Frequency | Source |
|---------------|-------------------|-----------|--------|
| Coordination Meeting Minutes | COORD-MTG-[###] | Per meeting | Specification.md D-1 |
| Clash Detection Reports | CLASH-REPORT-[Date]-[Stage] | Per clash run | Specification.md D-2 |
| RFI Logs | RFI-LOG-[Date/Rev] | Ongoing; snapshots at milestones | Specification.md D-3 |

**Source:** _CONTEXT.md (anticipated artifacts); Datasheet.md (Attributes: Record Types)

**Supporting Records:**

| Record Type | Purpose |
|-------------|---------|
| Interface registers | Interface agreement documentation |
| Coordination issue logs | Issue tracking |
| Coordination status summaries | Milestone status |
| BIM Execution Plan (if BIM) | BIM coordination requirements |
| Coordination procedures | Process documentation |

**Source:** Specification.md (D-4, D-5); Guidance.md

**Record Management:**

| Location | Purpose | Documents |
|----------|---------|-----------|
| `1_Working/DEL-28.03.../` | Working documents | Drafts, living documents |
| `1_Working/...` | Living documents | RFI logs, issue logs (with milestone exports) |
| `3_Issued/` | Final package | Complete coordination records at project completion |
| Project DMS | Electronic records | All records with metadata |

**Source:** Specification.md (D-7)

**Document Control:**
- Meeting minutes numbering: Sequential (COORD-MTG-001, etc.)
- Clash report numbering: By date and stage (CLASH-REPORT-YYYY-MM-DD-STAGE)
- RFI log numbering: Log filename with date/revision; RFIs numbered sequentially (RFI-001, etc.)
- Final package numbering: **TBD**
- Format: PDF for issued; spreadsheet/database for living logs; editable for drafts
- Retention: **TBD** — 7-10 years per contract requirements

**Source:** Specification.md (D-6); Datasheet.md (Attributes: Retention Period)

**Interface with Other Deliverables:**

| Deliverable | Relationship | Specification § |
|-------------|--------------|-----------------|
| DEL-27.04 Design Submission Packages | Coordination status supports submission readiness | IR-2 |
| DEL-28.01 Independent Design Verification | Coordination provides evidence to IDV reviewers | IR-3 |
| DEL-28.02 VFPA IP Review Responses | Coordination ensures consistent approach to VFPA requirements | IR-4 |
| PKG-01 through PKG-36 | Coordination ensures cross-discipline consistency | IR-1 |

**Source:** Specification.md (IR-1 through IR-4); Datasheet.md (Cross-Deliverable Coordination)

## Cross-Document Consistency Notes

This procedure has been verified for consistency with:
- **Datasheet.md**: All procedure steps reference appropriate Datasheet sections
- **Specification.md**: All steps implement specific requirements (FR, PR, IR, QR)
- **Guidance.md**: Steps informed by principles (P) and considerations (C)

**Step-to-Requirement Traceability:**

| Procedure Step | Specification Requirements | Guidance Sections |
|----------------|---------------------------|-------------------|
| Step 1 | FR-2, FR-3, FR-5, IR-5, IR-6, QR-1 | C-1, C-2, C-4, C-5 |
| Step 2 | FR-1, FR-2, PR-1, PR-3, D-1 | P-2, C-3, E-1 |
| Step 3 | FR-3, FR-4, PR-1, IR-5, D-2 | P-4, C-4, C-7, T-3, E-2 |
| Step 4 | FR-4, FR-5, FR-6, FR-7, PR-2, IR-1, D-3, D-4, D-5 | P-6, C-5, C-6, C-7, E-3, E-4 |
| Step 5 | IR-2, PR-2 | P-2, C-8 |
| Step 6 | QR-3, D-1, D-2, D-3, D-5, D-7 | C-9 |
| Step 7 | QR-3, QR-4, D-6, D-7, V-1, V-2, V-4, V-5 | C-9 |
| Step 8 | D-8 | — |

**Verification performed per:** AGENT_4_DOCUMENTS_REVISED_v3.md (Step 5, Cross-Reference and Iterate)
