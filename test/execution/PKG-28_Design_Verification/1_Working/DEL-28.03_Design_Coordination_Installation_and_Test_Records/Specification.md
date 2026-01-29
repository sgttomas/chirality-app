# Specification: DEL-28.03 Design Coordination Installation & Test Records

## Scope

This specification defines the requirements for **Design Coordination Installation & Test Records** within **PKG-28 Design Verification**.

**Purpose:** Provides evidence of completion, inspection, and testing for design coordination, supporting design quality, constructability, and **OBJ-6: Regulatory Compliance** — "The Works comply with all permits, codes, and authority requirements."

**Source:** _CONTEXT.md (DEL-28.03 description); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-6; Section 6, Objective-to-Deliverable Mapping)

**Anticipated deliverable artifacts:**
- Inter-discipline coordination records
- Clash detection reports
- RFI logs

**Source:** _CONTEXT.md (anticipated artifacts)

**Scope Inclusions:**
- Documentation of inter-discipline design coordination activities throughout design development
- Coordination meeting minutes and action item tracking
- 3D model-based clash detection reports (if BIM is used)
- Request for Information (RFI) logs tracking design questions and resolutions
- Interface registers documenting interface agreements between disciplines
- Coordination issue logs tracking resolution of coordination issues
- Evidence that coordination was performed systematically and coordination issues were resolved

**Scope Exclusions:**
- Design work itself (performed under discipline packages PKG-01 through PKG-36)
- Independent Design Verification (covered under DEL-28.01)
- VFPA IP Review coordination (covered under DEL-28.02)
- Construction coordination (construction-phase coordination is separate from design coordination)
- Testing and commissioning records (covered under PKG-29 Testing and other discipline-specific packages)

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (PKG-28 scope: inter-discipline coordination; Section 1.2: Scope Focus); **ASSUMPTION**: Scope boundaries per deliverable type

## Requirements

### Functional Requirements

**FR-1: Coordination Meeting Documentation**
- All inter-discipline design coordination meetings shall be documented with meeting minutes
- Meeting minutes shall include:
  - Meeting date, time, location/format (in-person or virtual)
  - Attendees list (names, disciplines, companies)
  - Agenda items and discussion topics
  - Interface issues identified and discussed
  - Decisions made
  - Action items with responsible party and due date
  - Next meeting date (if scheduled)
- Meeting minutes shall be distributed to attendees and filed in project records
- **Source:** **ASSUMPTION**: Standard meeting documentation requirements; Datasheet.md (record type: coordination meeting minutes)

**FR-2: Coordination Meeting Frequency**
- Regular design coordination meetings shall be held throughout design development
- Minimum meeting frequency: **TBD** — **ASSUMPTION**: Weekly or bi-weekly during active design phases, monthly during less active phases
- Additional coordination meetings shall be held as needed to address specific interface issues or coordination needs
- Intensive coordination meetings shall be held prior to each major design submission (30%, 60%, 90%, IFC)
- **Source:** Datasheet.md (coordination frequency TBD); **ASSUMPTION**: Regular coordination typical for D&B projects

**FR-3: Clash Detection (BIM Coordination)**
- If BIM (Building Information Modeling) is used, regular 3D model clash detection shall be performed
- Clash detection shall be performed using appropriate BIM software (e.g., Navisworks, Revit, other) — **TBD**: BIM software specification
- Clash detection runs shall be performed:
  - Prior to each major design submission (30%, 60%, 90%, IFC) — minimum
  - **TBD**: Additional interim clash detection frequency during design development
- Clash detection reports shall be generated showing all detected clashes
- All clashes shall be reviewed, prioritized, and assigned for resolution
- Critical and major clashes shall be resolved prior to design submission
- **Source:** Datasheet.md (BIM/3D modeling requirement, clash detection reports); **ASSUMPTION**: BIM coordination if BIM is used per industry practice

**FR-4: Clash Classification and Resolution**
- Detected clashes shall be classified by severity:
  - **Critical**: Clashes affecting primary structure, safety systems, or code compliance — must be resolved before design submission
  - **Major**: Clashes affecting design functionality or constructability — should be resolved before design submission
  - **Minor**: Clashes with minimal design impact — resolve during design development or construction
- **TBD**: Specific clash classification criteria
- Clash resolution shall be documented including:
  - Clash description and location
  - Disciplines involved
  - Resolution approach (which discipline made changes, what changes were made)
  - Resolved status and date
- **Source:** Datasheet.md (clash severity classification); **ASSUMPTION**: Risk-based clash classification approach

**FR-5: RFI System**
- A formal Request for Information (RFI) system shall be established to track design questions and resolutions
- Each RFI shall be assigned a unique sequential number
- RFI log shall track:
  - RFI number
  - Originator (discipline raising question)
  - Addressee (discipline or party expected to respond)
  - RFI question/issue description
  - Date submitted
  - Response/resolution
  - Date responded
  - Status (Open, Responded, Closed)
  - Related drawing/document references
- RFIs shall be responded to in a timely manner — **TBD**: RFI response timeframe requirements
- All RFIs shall be tracked to closure
- **Source:** Datasheet.md (record type: RFI logs); **ASSUMPTION**: Standard RFI tracking system for D&B projects

**FR-6: Interface Documentation**
- Key inter-discipline interfaces shall be documented in interface registers or interface agreements
- Interface documentation shall include:
  - Discipline pair (e.g., Civil-Structural, Mechanical-Electrical)
  - Interface description (what is being coordinated)
  - Responsible discipline for each interface element
  - Interface criteria (elevations, locations, sizes, connection details, loads)
  - Agreement date
  - Status (TBD, Agreed, Verified in design documents)
- **ASSUMPTION**: Interface documentation for critical coordination points; **TBD**: Interface documentation format and requirements

**FR-7: Coordination Issue Tracking**
- Coordination issues identified during coordination meetings, clash detection, or RFI process shall be tracked in a coordination issue log
- Issue log shall include:
  - Issue number
  - Issue description
  - Discipline(s) affected
  - Priority (Critical, High, Medium, Low)
  - Responsible party for resolution
  - Target resolution date
  - Resolution description
  - Status (Open, In Progress, Resolved)
- Critical and high-priority issues shall be tracked and escalated until resolved
- **ASSUMPTION**: Issue tracking system for coordination management; **TBD**: Issue tracking system specification

### Performance Requirements

**PR-1: Coordination Record Completeness**
- 100% of coordination meetings shall be documented with meeting minutes
- 100% of clash detection runs shall be documented with clash detection reports
- 100% of RFIs shall be logged and tracked to closure
- **Source:** **ASSUMPTION**: Completeness requirement for quality records

**PR-2: Coordination Issue Resolution**
- All critical clashes and critical coordination issues shall be resolved prior to design submission
- **TBD**: % of major clashes and issues to be resolved prior to design submission (e.g., 90% or 100%)
- All RFIs shall be responded to within **TBD** days of submittal
- **Source:** **ASSUMPTION**: Performance criteria for effective coordination

**PR-3: Record Timeliness**
- Coordination meeting minutes shall be issued within **TBD** days of meeting (e.g., within 2-5 days)
- Clash detection reports shall be issued within **TBD** days of model coordination
- **ASSUMPTION**: Timeliness requirements for coordination effectiveness

### Interface Requirements

**IR-1: Discipline Design Packages**
- Design coordination records interface with all discipline design packages (PKG-01 through PKG-36)
- Coordination ensures consistency and compatibility across all discipline deliverables
- Coordination issues identified shall be resolved through revisions to discipline design documents
- **Source:** Datasheet.md (coordination scope across all disciplines); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4, Package Summary)

**IR-2: Design Submission Packages**
- Design coordination supports DEL-27.04 (Design Submission Packages: 30%, 60%, 90%, IFC)
- Intensive coordination occurs prior to each design submission to ensure coordinated, clash-free submissions
- Coordination status (clashes resolved, RFIs closed) reported as part of design submission readiness
- **Source:** Datasheet.md (coordination phases aligned with design submissions); **ASSUMPTION**: Coordination integrated with submission process

**IR-3: Independent Design Verification**
- Design coordination coordinates with DEL-28.01 (Independent Design Verification Reports)
- IDV may identify coordination issues requiring resolution
- Coordination records provide evidence to IDV reviewers that coordination was performed
- **Source:** Datasheet.md (related deliverable: DEL-28.01); **ASSUMPTION**: IDV and coordination coordination per DEL-28.01 references

**IR-4: VFPA IP Review**
- Design coordination coordinates with DEL-28.02 (VFPA IP Review Responses)
- VFPA may identify inter-discipline coordination requirements
- Coordination process ensures VFPA requirements are addressed consistently across disciplines
- **Source:** Datasheet.md (related deliverable: DEL-28.02); DEL-28.02 Specification.md (IR-3)

**IR-5: BIM Execution Plan (if applicable)**
- If BIM is used, design coordination shall comply with project BIM Execution Plan (BEP)
- BEP defines BIM coordination requirements, model standards, clash detection protocols, coordination meeting requirements
- **TBD**: BIM Execution Plan reference and requirements
- **Source:** Datasheet.md (BIM/3D modeling requirement); **ASSUMPTION**: BEP if BIM is used

**IR-6: Quality Management System**
- Design coordination process shall comply with project Quality Management Plan (QMP)
- Coordination records are quality records demonstrating design quality management
- **TBD**: QMP reference
- **Source:** **ASSUMPTION**: QMS integration per ISO 9001

### Quality Requirements

**QR-1: ISO 9001 Compliance**
- All design coordination work shall comply with ISO 9001 Quality Management System requirements
- Coordination records are quality records demonstrating documented coordination process
- **Source:** Datasheet.md (applicable standards: ISO 9001)

**QR-2: Record Quality**
- Coordination records shall be accurate, complete, and clearly documented
- Meeting minutes shall be reviewed and approved by meeting chair or coordinator prior to distribution
- Clash detection reports shall be generated from current model revisions
- RFI log shall be maintained in real-time with current status
- **ASSUMPTION**: Quality requirements for records integrity

**QR-3: Document Control**
- All coordination records shall be controlled per project document control procedures
- Records shall be filed in project document management system with appropriate metadata
- Revisions shall be tracked and managed — **TBD**: Revision control protocol for records
- **ASSUMPTION**: Electronic document management system per project standards

**QR-4: Record Retention**
- Coordination records shall be retained per project record retention requirements
- Retention period: **TBD** — **ASSUMPTION**: Project lifetime plus 7-10 years per contract and professional liability requirements
- **Source:** Datasheet.md (retention period TBD)

## Standards

**Applicable codes and standards (Design discipline):**

- ISO 9001 — Quality Management Systems (quality records requirements)
- ISO 19650 — Organization and digitization of information about buildings and civil engineering works, including building information modeling (BIM) — **ASSUMPTION**: Applicable if BIM is used
- **TBD**: Project-specific BIM standards and protocols (if BIM is used)
- Employer's Requirements — **TBD**: Specific ER sections governing design coordination requirements
- Professional practice standards (EGBC) — **ASSUMPTION**: Coordination as part of professional design practice

**Source:** Datasheet.md (applicable standards: ISO 9001, ISO 19650); **ASSUMPTION**: BIM standards if BIM coordination is performed

## Verification

**Verification methods for Record deliverables:**

**V-1: Completeness Check**
- Verify all required records are present:
  - Coordination meeting minutes for all coordination meetings
  - Clash detection reports for all clash detection runs
  - RFI log with all RFIs tracked
  - Interface registers (if used)
  - Coordination issue logs (if used)
- **Verification method:** Records checklist review
- **Acceptance criteria:** All required records present and filed

**V-2: Data Accuracy Verification**
- Verify coordination records accurately reflect coordination activities
- Verify clash detection reports match model revisions analyzed
- Verify RFI log entries match RFI source documents
- **Verification method:** Spot-check verification against source data
- **Acceptance criteria:** Records accurate and consistent with source data

**V-3: Coordination Issue Closure Verification**
- Verify all critical clashes resolved prior to design submission
- Verify all critical and high-priority coordination issues resolved or have approved action plans
- Verify all RFIs responded to and closed (or have justified open status)
- **Verification method:** Issue status review in coordination logs
- **Acceptance criteria:** Critical items resolved; major items substantially resolved or action plans in place

**V-4: Witness Signature Verification (if applicable)**
- Verify meeting minutes signed or approved by meeting chair or coordinator
- Verify coordination records approved by responsible QA/QC personnel
- **Verification method:** Signature/approval check
- **Acceptance criteria:** Required approvals obtained
- **Source:** **ASSUMPTION**: Approval requirements for quality records

**V-5: Archival Format Compliance**
- Verify records filed in appropriate format for long-term retention (typically PDF for issued records)
- Verify records filed in project document management system with proper metadata
- **Verification method:** Document management system compliance check
- **Acceptance criteria:** Records properly filed and retrievable
- **Source:** **ASSUMPTION**: Archival requirements for project records

**Acceptance criteria (overall):**
- All coordination records complete per specification
- Coordination meetings documented, clash detection performed, RFIs tracked
- Critical coordination issues resolved
- Records accurate and approved
- Records filed in document management system
- **Source:** _CONTEXT.md (responsible party: D&B Contractor QA/QC); **ASSUMPTION**: Acceptance criteria for record deliverables

## Documentation

**Required documentation outputs:**
- Inter-discipline coordination records (meeting minutes, action item logs)
- Clash detection reports (if BIM is used)
- RFI logs

**Source:** _CONTEXT.md (anticipated artifacts)

**Additional record types** — **ASSUMPTION**: Supporting coordination documentation:
- Interface registers or interface agreements
- Coordination issue logs
- Coordination status reports (summarizing coordination activities and status at design milestones)

**Documentation requirements:**

**D-1: Coordination Meeting Minutes**
Format and content per FR-1 (Coordination Meeting Documentation)
- **Document naming**: **TBD** — **ASSUMPTION**: Sequential numbering (e.g., COORD-MTG-001, COORD-MTG-002)
- **Format**: **TBD** — **ASSUMPTION**: PDF for issued minutes, editable format (Word, etc.) for drafts
- **Distribution**: All meeting attendees, project management, discipline leads

**D-2: Clash Detection Reports**
Format and content per FR-3, FR-4 (Clash Detection and Classification)
- **Report naming**: **TBD** — **ASSUMPTION**: By date and model stage (e.g., CLASH-REPORT-2026-01-15-60PCT, CLASH-REPORT-2026-03-20-90PCT)
- **Format**: **TBD** — **ASSUMPTION**: PDF export from BIM clash detection software with supporting model screenshots
- **Distribution**: All discipline design leads, BIM coordinator, project management

**D-3: RFI Log**
Format and content per FR-5 (RFI System)
- **Log format**: **TBD** — **ASSUMPTION**: Spreadsheet (Excel) or database system maintained in real-time
- **Export format**: **ASSUMPTION**: PDF snapshots for design milestones and final submittal
- **Distribution**: Project team access to live log; PDF exports to Employer with design submissions

**D-4: Interface Registers** (if used)
Format and content per FR-6 (Interface Documentation)
- **Register format**: **TBD** — **ASSUMPTION**: Spreadsheet or database
- **Export format**: PDF for design milestones
- **Distribution**: Affected disciplines, project management

**D-5: Coordination Issue Logs** (if used)
Format and content per FR-7 (Coordination Issue Tracking)
- **Log format**: **TBD** — **ASSUMPTION**: Spreadsheet or database maintained in real-time
- **Export format**: PDF snapshots for design milestones
- **Distribution**: Project team access to live log; summaries to project management

**D-6: Document Control**
- All coordination records shall comply with project document control procedures
- Document numbering: **TBD** — **ASSUMPTION**: Per project numbering system for records
- Revision control: **TBD** — **ASSUMPTION**: Version tracking for living documents (RFI logs, issue logs); revision tracking for issued documents (meeting minutes, clash reports)
- **Source:** Datasheet.md (record numbering TBD)

**D-7: Record Management**
- Coordination records shall be filed in project document management system
- Filing location: `1_Working/DEL-28.03_Design_Coordination_Installation_and_Test_Records/` (during design coordination) → `3_Issued/` (final compilation at project completion or design milestones)
- **ASSUMPTION**: Living documents (RFI logs, issue logs) maintained in working folder and exported to issued folder at milestones
- Retention: Per QR-4 (Record Retention)

**D-8: Submittal to Employer** (if required)
- Coordination records may be submitted to Employer as part of design submission packages or upon request
- **TBD**: Employer submittal requirements for coordination records
- **ASSUMPTION**: Coordination status summaries included in design submission packages; detailed records available upon request
