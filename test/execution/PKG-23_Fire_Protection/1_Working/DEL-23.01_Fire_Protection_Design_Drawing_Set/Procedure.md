# Procedure: DEL-23.01 Fire Protection Design Drawing Set

## Purpose

This procedure defines the process for **producing** the **Fire Protection Design Drawing Set** within **PKG-23 Fire Protection** for the Canola Oil Transload Facility — Phase 1 Design & Build project.

**Scope of This Procedure:**

This procedure covers the production workflow for developing, checking, coordinating, and issuing the fire protection design drawings per project quality and document control requirements.

**Deliverable Information:**
- **Deliverable ID:** DEL-23.01
- **Deliverable Type:** Drawing
- **Responsible Party:** D&B Contractor
- **Discipline:** Specialty (Fire Protection)
- **Source:** Decomposition DEL-23.01 and `_CONTEXT.md`

**Related Procedures:**
- This procedure describes **production** of the drawing set
- Separate procedures exist for **using/operating** the fire protection systems depicted in the drawings (operations and maintenance manuals, emergency response procedures — outside scope of this deliverable)

## Prerequisites

### Dependencies

**Dependency Tracking Mode:**
- **Mode:** NOT_TRACKED
- **Source:** `_DEPENDENCIES.md`
- **Coordination:** Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

**Upstream Dependencies (inputs required before commencing):**

The following inputs are typically required before fire protection design drawings can be developed. Since dependencies are NOT_TRACKED, the timing and availability of these inputs are coordinated by humans externally:

| Input | Source | Purpose | Status |
|-------|--------|---------|--------|
| Site survey and base drawings | PKG-03 Civil | Base plan for fire water loop layout, hydrant locations | **TBD** — coordinate with civil lead |
| Site grading and drainage plan | PKG-03 Civil | Fire water loop burial depths, drainage coordination | **TBD** — coordinate with civil lead |
| Underground utilities plan | PKG-03 Civil | Avoid conflicts with fire water loop routing | **TBD** — coordinate with civil lead |
| Process P&ID | PKG-14 Process Piping | Foam system connections to tanks and marine loading | **TBD** — coordinate with process lead |
| Tank locations and sizes | PKG-13 Storage Tanks | Fire protection coverage, foam system design | **TBD** — coordinate with tank design lead |
| Electrical load list | PKG-17 Electrical | Fire pump power (if applicable), fire alarm panel power | **TBD** — coordinate with electrical lead |
| Control system architecture | PKG-19 Control Systems | Fire alarm/control system integration | **TBD** — coordinate with I&C lead |
| Building layouts | PKG-21, PKG-22 Buildings | Building fire alarm system coordination | **TBD** — coordinate with building design lead |
| Marine structures layout | PKG-08 Marine Structures | Marine fire main, wharf hydrant locations | **TBD** — coordinate with marine lead |
| Employer's Requirements | Employer | Project-specific fire protection requirements | **TBD** — to be provided by Employer |
| Fire water demand calculation | DEL-23.03 (this package) | Basis for fire water loop sizing | **TBD** — develop in parallel or prior |
| Fire protection equipment data sheets | DEL-23.04 (this package) | Equipment specifications for drawing callouts | **TBD** — develop in parallel or after preliminary design |
| Authority Having Jurisdiction (AHJ) input | Local fire marshal / AHJ | Jurisdiction-specific requirements | **TBD** — coordinate early in design |

**Source:** **ASSUMPTION** based on typical fire protection design workflow and interdisciplinary coordination requirements

### Reference Materials

**Required Reference Materials:**

The following reference materials must be available before commencing fire protection design drawings:

| Reference | Purpose | Location | Status |
|-----------|---------|----------|--------|
| Employer's Requirements Vol 2 Parts 1–3 | Project-specific fire protection requirements, design criteria, standards | `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_{1,2,3}_Employers_Requirements.pdf` | **TBD** — per INIT.md, do not attempt to read at this stage |
| NFPA 30 | Combustible liquid facility fire protection requirements | Package `0_References/` or standards library | **TBD** — obtain standard |
| NFPA 24 | Fire water loop design requirements | Package `0_References/` or standards library | **TBD** — obtain standard |
| NFPA 72 | Fire alarm system design requirements | Package `0_References/` or standards library | **TBD** — obtain standard |
| NFPA 20 | Fire pump installation requirements (if applicable) | Package `0_References/` or standards library | **TBD** — obtain standard if fire pump required |
| NBCC 2020 | Building code fire protection requirements | Package `0_References/` or standards library | **TBD** — obtain code |
| BCFC | British Columbia Fire Code | Package `0_References/` or standards library | **TBD** — obtain code |
| Project CAD Manual | Drawing standards, layering, symbology, title blocks | **TBD** | **TBD** — obtain project CAD standards |
| Project Quality Management Plan | Quality procedures, check requirements, sign-off protocols | **TBD** | **TBD** — obtain project QMP |
| Project Document Control Procedures | Drawing numbering, revision control, transmittal procedures | **TBD** | **TBD** — obtain project document control procedures |

**Source:** See `_REFERENCES.md` and Specification.md Section "Standards"

### Personnel Requirements

**Required Personnel and Qualifications:**

| Role | Qualifications | Responsibilities | Source |
|------|----------------|------------------|--------|
| Fire Protection Designer / Engineer | Professional Engineer (P.Eng.) licensed in BC or Canada, fire protection or mechanical discipline, experience with NFPA 30 and combustible liquid facilities | Lead fire protection design, prepare drawings, perform calculations | **ASSUMPTION**: Professional engineering requirement for BC |
| CAD Technician / Designer | Proficiency in AutoCAD or project CAD software, experience with industrial fire protection drawings | Prepare drawings under engineer direction, incorporate markups | **ASSUMPTION**: Standard design team composition |
| Checker / Reviewer | P.Eng. in fire protection or related discipline, independent from originator | Independent technical check of drawings for code compliance, accuracy, completeness | **ASSUMPTION**: Project quality procedures |
| Discipline Lead / Approver | Senior P.Eng. with fire protection or facility design experience | Final approval of drawings for issue, coordination with other disciplines | **ASSUMPTION**: Project quality procedures |
| Interdisciplinary Coordination Lead | Experience with multi-discipline project coordination | Facilitate IDC reviews, track and resolve interface comments | **ASSUMPTION**: Design-build coordination requirement |

**Source:** **ASSUMPTION** based on project quality procedures (**TBD** — to be confirmed per project organization and quality plan)

### Tools and Software

| Tool | Purpose | Source |
|------|---------|--------|
| AutoCAD (or equivalent CAD software) | Drawing preparation | **ASSUMPTION**: Standard industrial CAD software |
| Hydraulic analysis software (e.g., AFT Fathom, PIPE-FLO) | Fire water loop hydraulic analysis (supports DEL-23.03, informs drawing) | **ASSUMPTION**: Standard fire protection calculation tool |
| Fire alarm system design software (if applicable) | Fire alarm device layout, circuit calculations | **ASSUMPTION**: May be used for complex fire alarm systems |
| Project Document Management System | Drawing storage, revision control, transmittal | **TBD** — project-specific DMS |

## Steps

### Step 1: Design Initiation and Planning

**Step 1.1: Kickoff and Scope Review**
- Review deliverable scope, requirements, and objectives (see `_CONTEXT.md`, Specification.md, Guidance.md)
- Review Employer's Requirements for fire protection requirements
- Identify and obtain required reference materials (codes, standards, project procedures)
- **TBD** — specific kickoff meeting or review checklist per project procedures
- **Output:** Design basis understanding, reference materials collected
- **Source:** **ASSUMPTION**: Standard design workflow

**Step 1.2: Dependency and Interface Coordination**
- Identify upstream dependencies and coordinate timing with other disciplines
- Establish interdisciplinary coordination schedule (IDC meetings, drawing exchange milestones)
- Coordinate with AHJ for early input on jurisdiction-specific requirements
- **TBD** — coordination meeting schedule and communication plan
- **Output:** Coordination plan, interface agreement, dependency status
- **Source:** **ASSUMPTION**: Multi-discipline coordination requirement

**Step 1.3: Drawing List and Numbering**
- Develop preliminary drawing list based on anticipated artifacts (see Specification.md Section "Documentation")
- Assign drawing numbers per project numbering system — **TBD**
- **Output:** Drawing list with assigned drawing numbers
- **Source:** **ASSUMPTION**: Project document control procedures

### Step 2: Preliminary Design (Conceptual)

**Step 2.1: Fire Protection Basis of Design**
- Develop fire protection basis of design (FPBOD) document or section (may be part of DEL-23.02 Technical Specification or separate)
- Define fire protection zones, system types, design criteria
- Perform preliminary fire water demand calculation (may be part of DEL-23.03 or preliminary estimate)
- **TBD** — FPBOD document format and approval process
- **Output:** Fire protection basis of design, preliminary fire water demand estimate
- **Source:** **ASSUMPTION**: Typical fire protection design workflow

**Step 2.2: Conceptual Layout Development**
- Develop conceptual fire water loop layout on site plan base drawing
- Identify preliminary hydrant locations based on NFPA 30 spacing requirements and coverage analysis
- Identify preliminary foam system locations (tank foam, marine loading arm foam)
- Identify preliminary fire alarm system architecture (panel locations, detection zones)
- **Output:** Conceptual layout sketches or preliminary drawings (for internal review)
- **Verification:** Self-check for code compliance, coverage, feasibility
- **Source:** **ASSUMPTION**: Conceptual design phase

**Step 2.3: Conceptual Design Review**
- Review conceptual design with Employer, AHJ, and internal team
- Review for constructability, operability, maintainability
- Resolve comments and feedback
- **TBD** — conceptual design review meeting and approval
- **Output:** Approved conceptual design, comment resolution log
- **Source:** **ASSUMPTION**: Design-build review gate

### Step 3: Detailed Design Development

**Step 3.1: Fire Water Loop Layout Drawing**
- Develop detailed fire water loop layout drawing on final site plan base drawing
- Show fire water main routing, pipe sizes (based on hydraulic analysis DEL-23.03), isolation valves, connections to source
- Show underground vs. above-ground pipe routing, pipe supports (if above-ground)
- Coordinate routing with civil (grading, utilities), process (connections), and other disciplines
- Add notes, legends, general notes, and details as required
- **Output:** Fire water loop layout drawing (draft)
- **Verification:** Self-check for completeness, accuracy, code compliance
- **Source:** Decomposition DEL-23.01 anticipated artifacts and **ASSUMPTION**

**Step 3.2: Hydrant Locations Drawing**
- Develop detailed hydrant locations drawing on site plan base drawing
- Show fire hydrant locations with coverage radii per NFPA 30, hose reach, access routes
- Show hydrant types, sizes, and model numbers (from DEL-23.04 data sheets)
- Coordinate hydrant locations with civil (grading, access roads) and operations (vehicle movements)
- Add notes, legends, and details (hydrant installation detail, valve pit detail)
- **Output:** Hydrant locations drawing (draft)
- **Verification:** Self-check for code-compliant spacing, coverage, accessibility
- **Source:** Decomposition DEL-23.01 anticipated artifacts and **ASSUMPTION**

**Step 3.3: Fire Alarm System Drawings**
- Develop fire alarm system layout drawing showing detection device locations, alarm notification device locations, fire alarm panel locations
- Show detection zones, device types, wiring/conduit routing (risers or detailed routing per project standards)
- Develop fire alarm single-line diagram showing system architecture, panel configuration, connections to facility control system
- Develop fire alarm panel schedules showing device lists, circuit information, I/O assignments
- Coordinate with electrical (power supply), I&C (control system integration), and buildings (building fire alarm)
- Add notes, legends, and details as required
- **Output:** Fire alarm system drawings (draft) — layout, single-line diagram, panel schedules
- **Verification:** Self-check for code compliance (NFPA 72), system completeness, interface coordination
- **Source:** Decomposition DEL-23.01 anticipated artifacts and **ASSUMPTION**

**Step 3.4: Additional Drawings (as applicable)**
- Develop fire water system schematic (single-line diagram) showing system configuration, control valves, pump (if applicable)
- Develop foam system layout and details showing foam concentrate storage, proportioning equipment, foam piping, discharge devices for tanks and marine loading
- Develop fire pump details (if fire pump in Contractor scope) showing pump room layout, pump installation, piping connections
- Develop fire protection details (standard details for hydrants, valve pits, pipe supports, penetrations)
- Develop fire protection zone plan showing zone boundaries, equipment tagging/numbering
- **Output:** Additional drawings (drafts) as required
- **Verification:** Self-check for completeness and coordination
- **Source:** **ASSUMPTION** based on typical fire protection drawing set

**Step 3.5: Drawing Annotation and Finalization**
- Add all required annotations, dimensions, notes, legends, symbols per project CAD standards
- Complete title blocks with drawing title, number, revision, date, originator, checker, approver (sign-off blocks per project standards — **TBD**)
- Verify drawing complies with project CAD standards (layering, line types, symbology)
- Perform final self-check for completeness and accuracy
- **Output:** Completed draft drawings ready for checking
- **Verification:** Self-check checklist (if project provides checklist — **TBD**)
- **Source:** **ASSUMPTION**: Project CAD standards and quality procedures

### Step 4: Interdisciplinary Check (IDC)

**Step 4.1: Issue Drawings for IDC**
- Issue draft drawings to affected disciplines for interdisciplinary check (IDC)
- Disciplines to review: Civil (PKG-03), Process Piping (PKG-14), Electrical (PKG-17), I&C (PKG-19), Marine Structures (PKG-08), Buildings (PKG-21, PKG-22), and others as applicable
- **TBD** — IDC distribution list and review duration per project coordination procedures
- **Output:** IDC transmittal
- **Source:** **ASSUMPTION**: Interdisciplinary coordination requirement

**Step 4.2: Receive and Review IDC Comments**
- Collect IDC comments from reviewing disciplines
- Review comments for validity and impact on design
- Coordinate with commenting disciplines to clarify comments or discuss resolutions
- **Output:** IDC comment log
- **Source:** **ASSUMPTION**: IDC workflow

**Step 4.3: Resolve IDC Comments and Update Drawings**
- Incorporate valid IDC comments into drawings (revise layout, add notes, coordinate interfaces)
- Document comment resolutions in IDC comment log
- Obtain agreement from commenting disciplines on resolutions
- Update drawings to reflect IDC comment resolutions
- **Output:** Revised drawings with IDC comments resolved, IDC comment resolution log
- **Verification:** Verify all IDC comments addressed and resolved
- **Source:** **ASSUMPTION**: IDC workflow

### Step 5: Independent Check (Peer Review)

**Step 5.1: Issue Drawings for Independent Check**
- Issue drawings to qualified independent checker (not the originator)
- Provide checker with design basis, calculations (DEL-23.03), data sheets (DEL-23.04), and applicable codes/standards for reference
- **TBD** — check duration and checker assignment per project quality procedures
- **Output:** Independent check transmittal
- **Source:** **ASSUMPTION**: Project quality procedures

**Step 5.2: Checker Review**
- Checker performs technical review of drawings for:
  - Code compliance (NFPA 30, NFPA 24, NFPA 72, NBCC, BCFC)
  - Technical accuracy and correctness
  - Completeness (all required information shown)
  - Consistency with calculations (DEL-23.03) and data sheets (DEL-23.04)
  - Constructability and practicality
  - CAD standards compliance
- Checker documents review comments and issues check comments to originator
- **Output:** Independent check comments
- **Source:** **ASSUMPTION**: Independent check scope per project quality procedures

**Step 5.3: Resolve Check Comments and Update Drawings**
- Originator reviews check comments and incorporates corrections/clarifications into drawings
- Originator coordinates with checker to resolve any disagreements or clarifications
- Update drawings to reflect check comment resolutions
- **Output:** Revised drawings with check comments resolved
- **Verification:** Originator verifies all check comments addressed
- **Source:** **ASSUMPTION**: Check comment resolution workflow

**Step 5.4: Checker Sign-off**
- Checker reviews updated drawings and verifies check comments resolved satisfactorily
- Checker signs drawing or transmittal to indicate independent check complete and satisfactory
- **Output:** Checker sign-off (on drawing title block or separate check record — **TBD** per project)
- **Source:** **ASSUMPTION**: Project quality procedures

### Step 6: Design Review and Approval

**Step 6.1: Design Review (if required)**
- Conduct formal design review at specified milestone (e.g., 30%, 60%, 90%, IFC) if required by project
- Design review attendees: Employer representative, discipline lead, checker, other stakeholders
- Present design, discuss design basis, resolve review comments
- **TBD** — design review schedule and format per project or contract requirements
- **Output:** Design review meeting minutes, action items
- **Source:** **ASSUMPTION**: Design-build review gates (may not apply if Employer not requiring formal reviews)

**Step 6.2: Discipline Lead Approval**
- Discipline lead reviews drawings for overall design adequacy, consistency with project requirements, constructability
- Discipline lead approves drawings for issue by signing drawing or transmittal
- **Output:** Discipline lead sign-off (on drawing title block or separate approval record — **TBD** per project)
- **Source:** **ASSUMPTION**: Project quality procedures

**Step 6.3: AHJ Submittal (if required)**
- Submit drawings to AHJ (fire marshal, building official) for review and approval if required by jurisdiction or project
- Address AHJ comments and revise drawings as required
- Obtain AHJ approval or permit
- **TBD** — AHJ submittal requirements and timing per project permit schedule
- **Output:** AHJ-approved drawings (or permit)
- **Source:** **ASSUMPTION**: Typical AHJ approval requirement for fire protection systems

### Step 7: Drawing Issue

**Step 7.1: Prepare Drawing Issue Package**
- Finalize drawings with all sign-offs (originator, checker, approver)
- Assign final revision number per project revision scheme (e.g., Rev 0 for initial issue, Rev A/B/C for subsequent revisions — **TBD**)
- Generate PDF plot files from CAD files
- Prepare transmittal letter or form per project document control procedures
- **Output:** Drawing issue package (CAD files, PDFs, transmittal)
- **Source:** **ASSUMPTION**: Project document control procedures

**Step 7.2: Issue Drawings**
- Issue drawings via project document management system or per project transmittal procedures
- Issue to: Employer, construction team, subcontractors, other disciplines as required
- Update drawing register or log with issue information (drawing numbers, revision, date, issue purpose)
- **TBD** — drawing distribution list and issue procedures per project document control
- **Output:** Issued drawings, transmittal record, updated drawing register
- **Source:** **ASSUMPTION**: Project document control procedures

**Step 7.3: Update Deliverable Status**
- Update `_STATUS.md` to reflect deliverable lifecycle state:
  - INITIALIZED → IN_PROGRESS (when design work commences)
  - IN_PROGRESS → CHECKING (when drawings issued for formal review/check)
  - CHECKING → ISSUED (when drawings formally issued for construction or other purpose)
- Copy issued drawings to `3_Issued/` folder per framework conventions (see README.md)
- **Output:** Updated `_STATUS.md`, issued drawings archived in `3_Issued/`
- **Source:** Framework conventions per AGENTS.md and README.md

### Step 8: Revision and As-Built

**Step 8.1: Drawing Revisions (during design/construction)**
- If changes required during design or construction, revise drawings following steps 3–7 above (design development, IDC, check, approval, issue)
- Increment revision number per project revision scheme
- Document revision description in drawing revision block or revision log
- **TBD** — revision approval authority and process per project change control procedures
- **Output:** Revised drawings
- **Source:** **ASSUMPTION**: Standard drawing revision workflow

**Step 8.2: As-Built Drawings (post-construction)**
- Collect as-built markups from construction team showing field changes and actual installed conditions
- Incorporate as-built markups into drawings (may be separate "As-Built" revision or final "Record" revision)
- Verify as-built information against installation and test records (DEL-23.05)
- Issue as-built drawings as final record drawings
- **TBD** — as-built drawing procedures per project document control
- **Output:** As-built / record drawings
- **Source:** **ASSUMPTION**: Design-build as-built drawing requirement

## Verification

**Verification Activities at Each Step:**

The following verification activities are performed to ensure drawing quality and compliance:

| Verification Activity | When Performed | Performed By | Acceptance Criteria | Source |
|----------------------|----------------|--------------|---------------------|--------|
| **Self-Check** | After completing each drawing (Step 3) | Originator | Drawings complete, accurate, comply with codes and project standards, no obvious errors | **ASSUMPTION**: Project quality procedures |
| **Interdisciplinary Check (IDC)** | After self-check, before independent check (Step 4) | Affected disciplines | Interface coordination verified, no conflicts with other disciplines, IDC comments resolved | **ASSUMPTION**: Project coordination procedures |
| **Independent Check** | After IDC resolution (Step 5) | Qualified checker (independent from originator) | Technical correctness verified, code compliance verified, completeness verified, checker sign-off obtained | **ASSUMPTION**: Project quality procedures |
| **Dimensional Verification** | During independent check or as separate activity | Checker or survey coordinator | Key dimensions, coordinates, elevations verified against survey control and coordination drawings | **ASSUMPTION**: Project quality procedures |
| **CAD Standards Compliance Check** | During self-check and/or independent check | Originator and/or CAD QA/QC coordinator | Drawings comply with project CAD standards (layering, line types, symbology, title block format) | **ASSUMPTION**: Project CAD standards |
| **Code Compliance Review** | During independent check and/or formal design review | Checker and/or AHJ | Drawings comply with NFPA 30, NFPA 24, NFPA 72, NBCC, BCFC, and other applicable codes | **ASSUMPTION**: Code compliance requirement |
| **Constructability Review** | During design review or separate constructability review session | Construction team or experienced constructor | Drawings buildable, access adequate, construction sequencing feasible, no major constructability issues | **ASSUMPTION**: Design-build constructability review |
| **Design Review** | At design milestones (30%/60%/90%/IFC) if required by project | Employer, design team, checker, stakeholders | Design meets requirements, design basis sound, review comments resolved | **ASSUMPTION**: Design-build review gates (if applicable) |
| **AHJ Review** | Prior to construction (Step 6.3) | Fire marshal or authority having jurisdiction | Drawings comply with local jurisdiction requirements, permit issued or approval obtained | **ASSUMPTION**: AHJ approval requirement |

**Sign-off Requirements:**

The following sign-offs are required per project quality procedures (**TBD** — specific sign-off protocol to be confirmed):

| Sign-off | Role | Meaning | Location | Source |
|----------|------|---------|----------|--------|
| Originator Sign-off | Fire protection designer/engineer | Originator certifies drawing complete and accurate to best of their knowledge | Drawing title block or transmittal | **ASSUMPTION**: Project quality procedures |
| Checker Sign-off | Independent checker (P.Eng.) | Checker certifies independent check performed and drawing satisfactory | Drawing title block or separate check record | **ASSUMPTION**: Project quality procedures |
| Approver Sign-off | Discipline lead or designated approver (P.Eng.) | Approver authorizes drawing for issue | Drawing title block or transmittal | **ASSUMPTION**: Project quality procedures |
| AHJ Approval | Fire marshal or building official (if required) | AHJ approves drawing for construction or issues permit | Permit or approval stamp/letter | **ASSUMPTION**: AHJ approval requirement |

## Records

**Documentation Outputs from This Procedure:**

| Record | Content | Purpose | Location / Storage | Source |
|--------|---------|---------|-------------------|--------|
| **Fire Protection Design Drawings** | Fire water loop layout, hydrant locations, fire alarm system drawings, foam system drawings, fire protection details, etc. (see Specification.md Section "Documentation") | Primary deliverable artifacts for construction, permitting, coordination | Working: `1_Working/DEL-23.01/` <br> Review: `2_Checking/` (during CHECKING state) <br> Issued: `3_Issued/` (upon ISSUED state) | Framework conventions |
| **Drawing Register / Log** | List of all drawings in deliverable with drawing numbers, revisions, issue dates, issue purpose | Tracking and document control | Project document management system — **TBD** | **ASSUMPTION**: Project document control |
| **Transmittal Records** | Transmittal letters/forms for drawing issues and revisions | Document distribution and receipt record | Project document management system — **TBD** | **ASSUMPTION**: Project document control |
| **IDC Comment Log** | Interdisciplinary check comments and resolutions | Coordination record, demonstrate interface issues resolved | `1_Working/DEL-23.01/` or project coordination folder — **TBD** | **ASSUMPTION**: Project coordination procedures |
| **Independent Check Records** | Check comments, resolutions, checker sign-off | Quality record, demonstrate independent verification performed | `1_Working/DEL-23.01/` or project quality folder — **TBD** | **ASSUMPTION**: Project quality procedures |
| **Design Review Minutes** | Design review meeting minutes, action items, comment resolutions | Record design review completion and approvals | Project coordination or quality folder — **TBD** | **ASSUMPTION**: Project review procedures |
| **AHJ Approval / Permit** | Fire marshal approval letter, building permit, or permit drawings with approval stamp | Regulatory compliance record | Project permitting folder — **TBD** | **ASSUMPTION**: Permitting requirement |
| **Revision Log** | Record of all drawing revisions with revision number, date, description of changes | Revision history and change tracking | Drawing revision block or separate revision log | **ASSUMPTION**: Drawing revision control |
| **As-Built Markups** | Field markups showing as-built conditions and changes | Basis for as-built drawings | Construction team records → transferred to design team for incorporation | **ASSUMPTION**: As-built drawing process |
| **As-Built / Record Drawings** | Final drawings reflecting as-constructed conditions | Permanent facility record for operations and maintenance | `3_Issued/` and project records archive | **ASSUMPTION**: Design-build as-built requirement |

**Record Management:**

- All records shall be managed per project document control procedures — **TBD**
- Electronic records stored in project document management system — **TBD**
- CAD files version-controlled per project CAD management procedures — **TBD**
- Record retention per project retention schedule — **TBD** (typically 25+ years for facility record drawings)
- **Source:** **ASSUMPTION**: Project document control and record management procedures

**Deliverable Lifecycle and Folder Structure:**

Per framework conventions (README.md, AGENTS.md):

| Lifecycle State | Folder Location | Purpose | Source |
|----------------|-----------------|---------|--------|
| INITIALIZED, IN_PROGRESS | `1_Working/DEL-23.01/` | Active working location for deliverable development | Framework conventions |
| CHECKING | `2_Checking/To/` (copy for review) | Review package location during formal review state; working files remain in `1_Working/` | Framework conventions (recommended convention) |
| ISSUED | `3_Issued/` (copy of issued drawings) | Issued drawing archive; working files remain in `1_Working/` for potential future revisions | Framework conventions (recommended convention) |

- `_STATUS.md` in `1_Working/DEL-23.01/` is the authoritative lifecycle state indicator
- Source: Framework conventions per README.md Section "How to use the framework"

**Related Records from Other Deliverables:**

The following related records from other PKG-23 deliverables support and verify the fire protection design drawings:

| Deliverable | Related Records | Relationship | Source |
|-------------|----------------|--------------|--------|
| DEL-23.02 | Fire Protection Technical Specification | Defines performance, materials, and workmanship requirements that inform drawing specifications | Decomposition PKG-23 |
| DEL-23.03 | Fire Protection Design Calculations (fire water demand, hydraulic calculations) | Provides sizing basis for fire water loop, pipe sizes, pump sizing (if applicable) | Decomposition PKG-23 |
| DEL-23.04 | Fire Protection Data Sheet Package (hydrant data sheets, fire alarm panel data sheet) | Provides equipment specifications that appear on drawings as callouts and equipment tags | Decomposition PKG-23 |
| DEL-23.05 | Fire Protection Installation & Test Records (hydrostatic test, flow test, fire alarm test records) | Verifies installed systems match design drawings; provides as-built verification | Decomposition PKG-23 |
