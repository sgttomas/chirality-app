# Procedure: DEL-28.03 Design Coordination Installation & Test Records

## Purpose

This procedure defines the process for producing and managing **Design Coordination Installation & Test Records** within **PKG-28 Design Verification**.

**Deliverable Purpose:** Provides evidence of completion, inspection, and testing for design coordination, supporting design quality, constructability, and **OBJ-6: Regulatory Compliance** — "The Works comply with all permits, codes, and authority requirements."

**Source:** _CONTEXT.md (DEL-28.03 description); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-6)

**Deliverable type:** Record
**Responsible party:** D&B Contractor (QA/QC)

**Source:** _CONTEXT.md (deliverable type, responsible party)

**Dual-Use Nature:** This procedure describes both:
1. How to **produce** design coordination records (the documentation process)
2. How to **conduct** design coordination (the coordination activity itself)

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

**Source:** _DEPENDENCIES.md (dependency tracking mode)

**Upstream deliverables and input data:**

Design coordination occurs throughout design development and requires ongoing input from all discipline design packages (PKG-01 through PKG-36).

**Coordination Prerequisites:**
- Project initiated and design teams mobilized
- Discipline design work underway or planned
- Coordination procedures and tools established (coordination meeting protocols, BIM coordination plan if applicable, RFI system)

**Source:** Specification.md (IR-1: coordination interfaces with all discipline packages); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4, Package Summary)

**TBD:** Specific coordination start timing and prerequisites per project schedule

### Reference Materials

**Required references:**
- See `_REFERENCES.md` for applicable reference documents
- See `0_References/` in package directory for reference materials
- BIM Execution Plan (BEP) — **TBD**: Project BIM requirements and coordination protocols (if BIM is used)
- Project Quality Management Plan (QMP) — **TBD**: QMP reference for coordination procedures
- Employer's Requirements — **TBD**: Specific ER sections governing design coordination requirements
- Design basis documents and design criteria per discipline
- Applicable codes and standards per discipline

**Source:** Specification.md (Standards section, IR-5, IR-6); Datasheet.md (References section)

### Personnel Requirements

**D&B Contractor Personnel:**

**Coordination Management Roles:**
- Design Coordination Lead — overall responsibility for coordination process, facilitates coordination meetings, manages coordination records
- BIM Coordinator (if BIM is used) — manages 3D models, performs clash detection, facilitates BIM coordination meetings
- RFI Coordinator — manages RFI process and tracking system
- QA/QC Manager — oversees coordination as part of quality management, ensures coordination records are maintained
- **ASSUMPTION**: Coordination management roles; **TBD**: Specific role assignments

**Discipline Design Lead Roles:**
- Discipline Design Leads (Civil, Structural, Marine, Mechanical, Process, Electrical, I&C, Fire Protection, Environmental, etc.) — represent their disciplines in coordination, participate in coordination meetings, resolve coordination issues, update designs to address coordination requirements
- Qualified professional engineers (P.Eng. in BC or equivalent) — **TBD**: Specific licensing requirements per discipline
- **Source:** Datasheet.md (coordination scope across disciplines); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4, Package Summary: multi-discipline project); **ASSUMPTION**: P.Eng. qualifications per professional practice standards

**TBD:** Specific personnel assignments, qualifications, and time allocation for coordination activities

### Tools and Systems

**Required Tools:**
- Meeting platform (in-person meeting rooms or virtual meeting software like Teams, Zoom) — **TBD**: Meeting platform specification
- BIM software (if BIM is used) — **TBD**: Specific BIM software (e.g., Revit, Navisworks for clash detection, etc.)
- RFI tracking system (spreadsheet, database, or project management software) — **TBD**: RFI tracking system specification
- Issue tracking system for coordination issues — **TBD**: Issue tracking system (may be same as RFI system or separate)
- Project document management system for filing coordination records
- Collaboration tools (shared file systems, cloud storage) for model sharing and document exchange
- **ASSUMPTION**: Electronic tools for efficiency and accessibility

**TBD:** Specific tool selections and configurations

## Steps

### Step 1: Establish Coordination Framework

**1.1 Develop Coordination Plan**
- Define coordination approach:
  - Coordination meeting frequency and schedule — **TBD**: Meeting schedule
  - BIM coordination requirements (if applicable) — **TBD**: BIM coordination plan
  - RFI process and protocols
  - Interface management approach
  - Issue tracking and escalation procedures
- Document coordination plan in project Quality Management Plan or separate coordination plan document

**Source:** Specification.md (FR-2, FR-3, FR-5, IR-5, IR-6); Guidance.md (C-1: Coordination Approach and Tools)

**1.2 Assign Coordination Roles**
- Assign coordination roles and responsibilities per Personnel Requirements above
- Communicate roles and responsibilities to project team
- Establish authority levels for coordination decisions

**Source:** Guidance.md (C-2: Coordination Roles and Responsibilities)

**1.3 Set Up Coordination Tools**
- Set up BIM coordination environment (if BIM is used): model repository, clash detection software, model standards
- Set up RFI tracking system with RFI log template
- Set up coordination issue tracking system
- Set up coordination meeting schedule and calendar invites
- Provide training to project team on coordination tools and processes

**Source:** Specification.md (FR-3, FR-5, FR-7); Guidance.md (C-1: Coordination Approach and Tools, C-4: BIM Coordination Strategy, C-5: RFI Process)

**Verification:** Coordination framework established; roles assigned; tools set up and operational; team trained

### Step 2: Conduct Regular Coordination Meetings

**2.1 Schedule and Convene Coordination Meetings**
- Hold regular inter-discipline coordination meetings per established schedule (e.g., weekly or bi-weekly during active design)
- Distribute meeting agenda in advance (1-2 days prior) — **TBD**: Agenda distribution timing
- Ensure discipline design leads attend or send qualified delegates

**Source:** Specification.md (FR-1, FR-2); Guidance.md (C-3: Coordination Meeting Structure)

**2.2 Facilitate Coordination Discussion**
Typical coordination meeting agenda per Guidance.md (E-1):
1. Review action items from previous meeting
2. Design status update by discipline
3. Interface issues and coordination topics
4. Clash detection results review (if available)
5. RFI status and escalations
6. Assign new action items with responsible party and due date
7. Schedule next meeting

**Source:** Specification.md (FR-1); Guidance.md (C-3: Coordination Meeting Structure, E-1: Sample agenda)

**2.3 Document Meeting Minutes**
- Document coordination meeting minutes including:
  - Meeting date, time, location/format
  - Attendees list
  - Discussion topics and interface issues
  - Decisions made
  - Action items with responsible party and due date
  - Next meeting date
- Issue meeting minutes within **TBD** days of meeting (e.g., 2-5 days)
- Distribute meeting minutes to attendees and file in project document management system

**Source:** Specification.md (FR-1, PR-3, D-1); Datasheet.md (coordination meeting minutes format); Guidance.md (E-1: Sample minutes)

**Verification:** Coordination meetings held per schedule; meeting minutes documented and distributed; action items tracked

### Step 3: Perform BIM Clash Detection (if BIM is used)

**3.1 Federate Discipline Models**
- Collect current design models from all disciplines
- Federate (combine) discipline models in clash detection software (e.g., Navisworks)
- Verify models are current revisions and properly georeferenced

**Source:** Specification.md (FR-3); Guidance.md (C-4: BIM Coordination Strategy)

**3.2 Run Clash Detection**
- Perform clash detection analysis using BIM software
- Run clash detection per defined frequency:
  - **Minimum**: Prior to each major design submission (30%, 60%, 90%, IFC)
  - **TBD**: Additional interim clash detection frequency (e.g., weekly or bi-weekly during active design)
- Use clash detection rules and filters appropriate to design stage (filter out known acceptable "clashes" like bolt clearances, etc.)

**Source:** Specification.md (FR-3); **ASSUMPTION**: Clash detection frequency and rules

**3.3 Review and Classify Clashes**
- Review all detected clashes
- Classify clashes by severity:
  - **Critical**: Clashes affecting primary structure, safety systems, code compliance — must resolve before submission
  - **Major**: Clashes affecting functionality or constructability — should resolve before submission
  - **Minor**: Clashes with minimal impact — resolve during design development or construction
- Assign clashes to responsible disciplines for resolution

**Source:** Specification.md (FR-4); Datasheet.md (clash severity classification); Guidance.md (C-7: Coordination Issue Prioritization)

**3.4 Generate Clash Detection Report**
- Generate clash detection report from BIM software showing:
  - Clash detection run date and model revisions
  - Total clashes detected and breakdown by severity
  - Clashes by discipline pair
  - Individual clash details (location, disciplines involved, classification, responsible party, status)
- Export clash report to PDF and distribute to discipline design leads
- File clash report in project document management system

**Source:** Specification.md (FR-3, FR-4, D-2); Datasheet.md (clash detection report format); Guidance.md (E-2: Sample clash report)

**Verification:** Clash detection performed per schedule; clashes classified and assigned; clash report generated and distributed

### Step 4: Resolve Coordination Issues (Clashes, RFIs, Interface Questions)

**4.1 Clash Resolution**
For each clash assigned:
- Responsible discipline reviews clash and determines resolution approach (reroute pipe, adjust elevation, relocate equipment, etc.)
- Discipline updates design documents (drawings, models) to resolve clash
- Discipline updates clash status in clash tracking system or reports closure to BIM Coordinator
- BIM Coordinator verifies clash resolution in updated models

**Source:** Specification.md (FR-4); **ASSUMPTION**: Clash resolution workflow

**4.2 RFI Processing**
When design question or clarification is needed:
- Originating discipline submits RFI using RFI system
- RFI Coordinator logs RFI in RFI tracking system with unique RFI number
- RFI Coordinator routes RFI to addressee (discipline or party responsible for response)
- Addressee reviews RFI and prepares response
- Addressee submits response via RFI system
- RFI Coordinator updates RFI log with response and date
- Originating discipline confirms response resolves question and closes RFI
- **TBD**: RFI response timeframe requirement (e.g., respond within 5-10 business days)

**Source:** Specification.md (FR-5, PR-2); Datasheet.md (RFI log format); Guidance.md (C-5: RFI Process, E-3: Sample RFI log)

**4.3: Interface Coordination** (for critical interfaces)
For complex or critical interfaces:
- Affected disciplines coordinate interface requirements (elevations, locations, loads, connection details, responsibilities)
- Document interface agreement in interface register or coordination meeting minutes
- Verify interface agreement is reflected in design documents
- Update interface register status to "Agreed" and later "Verified"

**Source:** Specification.md (FR-6); Datasheet.md (interface registers); Guidance.md (C-6: Interface Documentation, E-4: Sample interface register)

**4.4 Escalation of Critical Issues**
For critical or high-priority coordination issues that are not being resolved:
- Design Coordination Lead escalates to project management
- Project management intervenes to facilitate resolution (additional meetings, resource allocation, decision authority)
- Critical issues tracked until resolved

**Source:** Specification.md (FR-7, PR-2); Guidance.md (P-6: Issue Tracking to Closure, C-7: Prioritization)

**Verification:** Coordination issues (clashes, RFIs, interface questions) tracked and resolved; critical issues escalated and resolved before design submissions

### Step 5: Pre-Submission Coordination Verification

Prior to each major design submission (30%, 60%, 90%, IFC):

**5.1 Coordination Status Review**
- Review coordination status:
  - All coordination meetings held and documented
  - Clash detection performed on current models
  - All critical and major clashes resolved (per specification PR-2)
  - All critical and high-priority coordination issues resolved
  - All overdue RFIs escalated and resolved or have approved action plans
  - Interface agreements documented and reflected in design
- Prepare coordination status summary

**Source:** Specification.md (IR-2, PR-2); Guidance.md (C-8: Coordination Status Tracking and Reporting)

**5.2 Final Clash Detection Run**
- Perform final clash detection run on design submission models
- Verify all critical and major clashes resolved
- Document any remaining minor clashes with justification for deferral (if applicable)
- Issue final clash detection report for design submission

**Source:** Specification.md (FR-3, FR-4, PR-2); **ASSUMPTION**: Final clash check before submission

**5.3 Coordination Sign-Off** (if required)
- Obtain coordination sign-off from discipline design leads confirming their designs are coordinated
- **TBD**: Coordination sign-off requirements and format
- **ASSUMPTION**: Sign-off may be informal (email confirmation) or formal (signed coordination certificate)

**Verification:** Coordination status verified; critical and major issues resolved; coordination readiness confirmed for design submission

### Step 6: Maintain Coordination Records

Throughout design development:

**6.1 File Coordination Meeting Minutes**
- File meeting minutes in project document management system within **TBD** days of meeting
- File in `1_Working/DEL-28.03_Design_Coordination_Installation_and_Test_Records/` folder or designated coordination records folder
- Maintain sequential filing (COORD-MTG-001, COORD-MTG-002, etc.)

**Source:** Specification.md (FR-1, PR-3, D-1, D-7); **ASSUMPTION**: Systematic filing

**6.2 Maintain RFI Log**
- Maintain RFI log in real-time as RFIs are submitted and responded to
- Keep RFI log accessible to project team (shared file location, project management system)
- Export RFI log snapshots to PDF at design milestones (30%, 60%, 90%, IFC) for archival
- File RFI log snapshots in coordination records folder

**Source:** Specification.md (FR-5, D-3, D-7); Guidance.md (C-9: Record Management)

**6.3 File Clash Detection Reports**
- File clash detection reports in coordination records folder after each clash detection run
- Maintain sequential filing by date and stage (CLASH-REPORT-2026-02-15-60PCT, etc.)

**Source:** Specification.md (D-2, D-7); **ASSUMPTION**: Systematic filing

**6.4 Maintain Coordination Issue Logs** (if used)
- Maintain coordination issue logs (if used) in real-time
- Export snapshots at design milestones for archival
- File in coordination records folder

**Source:** Specification.md (FR-7, D-5, D-7); **ASSUMPTION**: Living documents with milestone snapshots

**Verification:** Coordination records filed systematically and accessible; living documents (RFI logs, issue logs) current and accessible

### Step 7: Final Coordination Records Compilation

At project completion or final design submission (IFC):

**7.1 Compile Final Coordination Record Package**
- Compile final coordination record package including:
  - All coordination meeting minutes (full set from project start to completion)
  - All clash detection reports (full set from all design stages)
  - Final RFI log export (complete log showing all RFIs and resolutions)
  - Final interface registers (if used)
  - Final coordination issue logs (if used)
  - Coordination status summary for final submission
- Organize records in logical structure (by record type, by date, or by design stage)

**Source:** Specification.md (D-1 through D-5, D-7); **ASSUMPTION**: Final compilation at project completion

**7.2 Final QA/QC Review**
- Perform completeness check of coordination records per Specification.md (V-1)
- Verify all required records present
- Verify records accurately reflect coordination activities (data accuracy per Specification.md V-2)
- Obtain QA/QC approval

**Source:** Specification.md (V-1, V-2, V-4)

**7.3 File Final Coordination Records**
- File final coordination record package in `3_Issued/` folder
- Assign final document number and date — **TBD**: Document numbering for final record package
- File in project document management system with proper metadata for long-term retention
- Retain per record retention requirements (Specification.md QR-4)

**Source:** Specification.md (QR-3, QR-4, D-6, D-7); Datasheet.md (retention period TBD)

**Verification:** Final coordination records compiled, reviewed, and filed; records complete and accurate; retention requirements met

### Step 8: Submittal to Employer (if required)

**8.1 Prepare Coordination Records Submittal** (if required by Employer)
- Prepare coordination records for submittal to Employer per contract requirements
- **TBD**: Employer submittal requirements for coordination records (summary only, full records, or records upon request)
- Typical approach: Include coordination status summary in design submission packages; provide detailed records upon request

**Source:** Specification.md (D-8: Submittal to Employer); **ASSUMPTION**: Coordination summaries with submissions, detailed records available

**8.2 Submit to Employer**
- Submit coordination records to Employer per submittal protocol
- Log submittal in project correspondence system

**Verification:** Coordination records submitted to Employer per requirements (if required); submittal logged

## Verification

**Verification activities for Design Coordination Record deliverables:**

**V-1: Completeness Check**
- Verify all required coordination records present
- **Verification method:** Records checklist per Specification.md (V-1)
- **Acceptance criteria:** All coordination meetings documented; all clash detection runs documented; RFI log complete
- **Source:** Specification.md (V-1)

**V-2: Data Accuracy Verification**
- Verify coordination records accurately reflect coordination activities
- **Verification method:** Spot-check per Specification.md (V-2)
- **Acceptance criteria:** Records accurate and consistent with source data
- **Source:** Specification.md (V-2)

**V-3: Coordination Issue Closure Verification**
- Verify critical clashes and critical coordination issues resolved before design submissions
- **Verification method:** Issue status review per Specification.md (V-3)
- **Acceptance criteria:** Critical items resolved; major items substantially resolved or action plans in place
- **Source:** Specification.md (V-3)

**V-4: Record Approval Verification**
- Verify coordination records approved by responsible QA/QC personnel
- **Verification method:** Approval check per Specification.md (V-4)
- **Acceptance criteria:** Required approvals obtained
- **Source:** Specification.md (V-4)

**V-5: Archival Format Compliance**
- Verify records filed in proper format and document management system
- **Verification method:** Filing compliance check per Specification.md (V-5)
- **Acceptance criteria:** Records properly filed and retrievable
- **Source:** Specification.md (V-5)

**Sign-off requirements:**

| Role | Sign-off Requirement | Document Location |
|------|---------------------|-------------------|
| Meeting Chair / Design Coordination Lead | Approval of coordination meeting minutes | Meeting minutes (signature or approval record) |
| BIM Coordinator (if applicable) | Approval of clash detection reports | Clash detection report (signature or approval record) |
| RFI Coordinator | Approval of RFI log compilations | RFI log export (cover sheet or approval record) |
| D&B Contractor QA/QC Manager | Final approval of coordination record package | Final coordination record package (cover sheet or approval record) — **TBD**: Specific approval format |

**Source:** Specification.md (V-4, Acceptance criteria); **ASSUMPTION**: Sign-off roles and requirements for quality records

## Records

**Documentation outputs:**

**Primary Deliverables:**
- Inter-discipline coordination records (coordination meeting minutes from all coordination meetings throughout design)
- Clash detection reports (reports from all clash detection runs throughout design, if BIM is used)
- RFI logs (complete RFI log showing all RFIs and resolutions throughout design)

**Source:** _CONTEXT.md (anticipated artifacts); Specification.md (D-1, D-2, D-3)

**Supporting Records:** — **ASSUMPTION**: Additional coordination documentation
- Interface registers or interface agreements (if used)
- Coordination issue logs (if used)
- Coordination status summaries (at design milestones)
- BIM Execution Plan (if BIM is used)
- Coordination procedures and protocols

**Source:** Specification.md (D-4, D-5); Guidance.md (supporting coordination documentation)

**Record management:**

**Filing and Storage:**
- **Working documents**: Stored in `1_Working/DEL-28.03_Design_Coordination_Installation_and_Test_Records/` folder throughout design
- **Living documents** (RFI logs, issue logs): Maintained in working folder; snapshots exported to issued folder at milestones
- **Issued records**: Final coordination record package filed in `3_Issued/` at project completion or final design submission
- **Electronic records**: Stored in project document management system with appropriate metadata and access controls

**Source:** Specification.md (D-7: Record Management); **ASSUMPTION**: Living documents in working folder, final package in issued folder

**Retention requirements:**
- **TBD**: Project records retention per contract requirements (typically 7-10 years post-project completion for quality records and professional liability)
- **ASSUMPTION**: Long-term retention for quality management and professional liability

**Source:** Specification.md (QR-4: Record Retention); Datasheet.md (retention period TBD)

**Document Control:**
- Meeting minutes numbering: **TBD** — **ASSUMPTION**: Sequential (COORD-MTG-001, COORD-MTG-002, etc.)
- Clash report numbering: **TBD** — **ASSUMPTION**: By date and stage (CLASH-REPORT-YYYY-MM-DD-STAGE)
- RFI log numbering: **TBD** — **ASSUMPTION**: Log filename with date/revision; individual RFIs numbered sequentially (RFI-001, RFI-002, etc.)
- Final record package numbering: **TBD** — **ASSUMPTION**: Package number assigned at final compilation
- Format: **TBD** — **ASSUMPTION**: PDF for issued records and reports, spreadsheet/database format for living logs, editable format (Word, etc.) for draft minutes

**Source:** Specification.md (D-6: Document Control); Datasheet.md (record numbering TBD)

**Interface with Other Deliverables:**
- Coordination records support design submissions (DEL-27.04) — coordination status included in submission readiness
- Coordination records interface with IDV reports (DEL-28.01) — coordination provides evidence to IDV reviewers
- Coordination records interface with VFPA IP Review responses (DEL-28.02) — coordination ensures consistent approach to VFPA requirements
- Coordination records support all discipline design packages (PKG-01 through PKG-36) — coordination ensures cross-discipline consistency

**Source:** Specification.md (IR-1, IR-2, IR-3, IR-4); Datasheet.md (related deliverables)
