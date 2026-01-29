# Procedure: DEL-25.01 Communications Design Drawing Set

## Purpose

This procedure defines the process for producing and managing **Communications Design Drawing Set** within **PKG-25 Communications & IT**.

**Deliverable Purpose:** Defines the design arrangement and details for communications per ER requirements.

**Source:** `_CONTEXT.md` Description; Decomposition Table PKG-25 DEL-25.01

**Deliverable Context:**
- **Deliverable Type:** Drawing (design documentation)
- **Responsible Party:** D&B Contractor
- **Discipline:** Specialty (communications infrastructure)

**Source:** `_CONTEXT.md`; Decomposition Table PKG-25 DEL-25.01

**Procedure Scope:**

This procedure covers the production of the drawing set from initial design through approval and issuance. It addresses both the technical design process and the document management workflow.

The technical design shall be guided by:
- **Datasheet.md** — Defines the deliverable attributes, conditions, and construction details
- **Specification.md** — Defines the requirements, standards, and verification methods
- **Guidance.md** — Provides engineering principles, considerations, and trade-offs to inform design decisions

**Source:** Inference from deliverable type and typical engineering workflow; cross-reference to companion documents (Pass 2 enrichment)

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED

Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`).

**Source:** `_DEPENDENCIES.md`

**Upstream Deliverables and Input Data:**

The following inputs should be available or in progress before commencing design:

1. **Site and Facility Layout Information:**
   - Site plan and building floor plans (PKG-21, PKG-22)
   - Equipment room locations and dimensions
   - **TBD** — Architectural and civil drawing status

2. **User Requirements:**
   - Operational requirements for network connectivity
   - Workstation locations and density
   - Control system network integration requirements (coordinate with PKG-19)
   - **TBD** — Employer's communications requirements

3. **Technical Specifications and Criteria:**
   - DEL-25.02 Communications Technical Specification (may be developed in parallel)
   - Equipment selections (coordinate with DEL-25.03)
   - **TBD** — Project design basis and criteria documents

4. **Interface Information:**
   - Electrical power distribution plans (PKG-17) for equipment room power
   - Control system architecture (PKG-19) for integration points
   - Cable tray and conduit routing (PKG-17, PKG-19, PKG-20) for pathway coordination
   - Building penetrations and pathways (PKG-21, PKG-22)
   - **TBD** — Interface control documentation

5. **Standards and Reference Documents:**
   - Employer's Requirements: **TBD** — Communications-related sections
   - Project CAD manual and drawing standards: **TBD**
   - Project design criteria: **TBD**
   - Applicable codes and standards (see Specification.md Standards section)

**Source:** Specification.md Interface Requirements; Guidance.md Considerations; **TBD** for specific input status

### Reference Materials

- See `_REFERENCES.md` for applicable reference documents (currently no references identified; to be populated)
- See `0_References/` in package directory for reference materials
- Applicable codes and standards per Specification.md
- **TBD** — Employer's Requirements communications sections
- **TBD** — Project-specific design standards and criteria

**Source:** `_REFERENCES.md`; Specification.md Standards section

### Personnel Requirements

**Originator (Designer):**
- Qualified telecommunications or communications infrastructure engineer/designer
- Familiarity with TIA structured cabling standards
- Proficiency in CAD software per project standards
- **TBD** — Specific qualification or registration requirements

**Checker/Reviewer:**
- Independent qualified engineer/designer (not the originator)
- Experience with communications infrastructure design
- Authority to approve design for technical accuracy
- **TBD** — Checker qualification requirements per project quality procedures

**Approver (Discipline Lead):**
- Specialty discipline lead or communications lead engineer
- Authority to approve for issue
- **TBD** — Approval authority matrix

**Source:** **ASSUMPTION** — Standard engineering document workflow; **TBD** for project-specific requirements

### Tools and Resources

- CAD software: **TBD** — AutoCAD, MicroStation, or other per project standards
- Network design tools (optional): **TBD** — For pathway sizing, cable scheduling
- Document management system: **TBD** — For document control and distribution
- Design calculation tools (if needed): Spreadsheets or software for pathway fill calculations, cable pulling tension, etc.

**Source:** **ASSUMPTION** — Standard engineering tools; **TBD** for specific project tools

## Steps

### Step 1: Design Initiation and Planning

**Action:** Establish design basis and scope for the drawing set.

**Activities:**

1.1. Review inputs and prerequisites:
   - Confirm availability of required upstream information
   - Identify gaps and issue RFIs or information requests as needed
   - Review Employer's Requirements for communications-specific criteria

1.2. Establish design basis:
   - Determine network topology and architecture (star, ring, mesh)
   - Establish equipment room and TR locations
   - Define design standards and criteria to be applied
   - **TBD** — Design basis memorandum or design criteria document requirements

1.3. Plan drawing set organization:
   - Determine list of drawings to be produced
   - Assign drawing numbers per project numbering system
   - Create drawing index
   - **TBD** — Drawing numbering scheme

1.4. Coordinate with interfacing disciplines:
   - Schedule coordination meetings with PKG-17, PKG-19, PKG-21, PKG-22, PKG-24
   - Establish interface control points and responsibilities
   - **TBD** — Coordination meeting schedule

**Verification:** Design basis and drawing plan reviewed and approved by discipline lead.

**Source:** Guidance.md Considerations; **ASSUMPTION** — Standard design planning process

### Step 2: Design Development (Fiber Network Layout)

**Action:** Develop fiber optic backbone network design.

**Activities:**

2.1. Determine fiber requirements:
   - Identify endpoints requiring fiber connectivity
   - Determine fiber types (single-mode, multi-mode) and fiber counts
   - Establish redundancy requirements if applicable
   - **Reference:** Specification.md Performance Requirements; Guidance.md Principles (Redundancy)

2.2. Route fiber backbone:
   - Plan fiber routes between buildings and major areas
   - Select pathway types (direct burial, duct bank, overhead, building pathways)
   - Coordinate with civil and building packages for pathway installation
   - Identify splice locations and fiber distribution frame (FDF) locations

2.3. Develop fiber network layout drawing(s):
   - Show fiber routes on site plan and/or building floor plans
   - Indicate fiber types, counts, and termination points
   - Label per TIA-606 administration standard
   - Provide legends and notes

**Verification:** Fiber network layout reviewed for completeness, coordination with pathways, and technical adequacy.

**Source:** Datasheet.md Construction; Specification.md Requirements; Guidance.md Principles; **ASSUMPTION** — Fiber design workflow

### Step 3: Design Development (Communications Distribution)

**Action:** Develop structured cabling distribution design.

**Activities:**

3.1. Determine horizontal cabling requirements:
   - Identify all work areas and outlet locations
   - Determine outlet types and quantities (data, voice, etc.)
   - Establish cable types and performance categories (Cat 6, Cat 6A, etc.)
   - **Reference:** Specification.md Functional Requirements; DEL-25.02 for cable specifications

3.2. Design cable pathways:
   - Route cable trays, conduits, or other pathways from TRs to work areas
   - Size pathways per TIA-569 and code requirements with spare capacity
   - Coordinate pathway routing with other disciplines (electrical, I&C, architectural)
   - Identify penetrations and firestopping requirements
   - **Reference:** Guidance.md Considerations (Pathway Design); Specification.md Interface Requirements

3.3. Plan telecommunications rooms (TRs):
   - Locate TRs to meet distance limitations (~90m horizontal copper)
   - Size rooms per TIA-569 requirements
   - Plan rack layouts and equipment arrangements (coordinate with Step 4)
   - Coordinate with PKG-22 for HVAC and environmental controls

3.4. Develop communications distribution drawing(s):
   - Show cable pathways on building floor plans
   - Indicate outlet locations with symbols and labels
   - Show TR locations and cable entry points
   - Provide pathway sizing information and cable schedules
   - Include details for typical installations and special conditions

**Verification:** Distribution drawings reviewed for completeness, pathway coordination, compliance with TIA-569, and technical adequacy.

**Source:** Datasheet.md Construction; Specification.md Requirements; Guidance.md Considerations; **ASSUMPTION** — Structured cabling design workflow

### Step 4: Design Development (Patch Panel Locations)

**Action:** Develop equipment room and rack elevation designs.

**Activities:**

4.1. Design equipment room (ER) layout:
   - Plan rack locations, cable entry, and work clearances
   - Coordinate power distribution (PKG-17), grounding (TIA-607), and HVAC (PKG-22)
   - Plan cable management pathways (overhead ladder rack, underfloor, etc.)
   - **Reference:** Guidance.md Considerations (Equipment Room and TR Design)

4.2. Design rack elevations:
   - Allocate rack space for patch panels, network equipment, cable management
   - Coordinate equipment selections with DEL-25.03 data sheets
   - Plan port assignments and labeling scheme per TIA-606
   - Ensure adequate spacing for cables and airflow
   - **Reference:** DEL-25.03 for equipment dimensions and specifications

4.3. Develop patch panel location drawing(s):
   - Show equipment room floor plan(s) with rack locations
   - Provide rack elevation drawings showing panel-by-panel layout
   - Include cable entry details and grounding details
   - Provide labeling scheme and port assignment tables
   - **Reference:** Specification.md Functional Requirements (Patch Panel Locations)

**Verification:** Rack elevations reviewed for equipment fit, cable management adequacy, coordination with equipment data sheets (DEL-25.03), and compliance with TIA standards.

**Source:** Datasheet.md Construction; Specification.md Requirements; Guidance.md Considerations; **ASSUMPTION** — Equipment room design workflow

### Step 5: Drawing Production and Detailing

**Action:** Complete CAD production of all drawings in the set.

**Activities:**

5.1. Produce drawings per CAD standards:
   - Apply project CAD standards (layers, line weights, text styles, title blocks)
   - Ensure clarity and legibility per Specification.md Quality Requirements
   - Provide adequate details, sections, and enlarged views as needed
   - Cross-reference between drawings

5.2. Add legends, notes, and schedules:
   - Provide symbol legends on each drawing or on a legend sheet
   - Include general notes and drawing-specific notes
   - Provide cable schedules, pathway schedules, or equipment schedules as applicable
   - Reference applicable standards and specifications

5.3. Complete title blocks and drawing borders:
   - Drawing number, title, date, revision
   - Originator, checker, approver signature blocks
   - Project information and client information
   - **TBD** — Title block template and requirements

**Verification:** Drawings comply with project CAD standards per Specification.md Quality Requirements.

**Source:** Specification.md Quality Requirements; **ASSUMPTION** — CAD production standards

### Step 6: Self-Check

**Action:** Originator performs self-check of drawings before submittal for review.

**Activities:**

6.1. Technical accuracy check:
   - Verify all dimensions, cable types, and technical information
   - Check calculations (pathway fill, cable pulling tension, etc.) if applicable
   - Confirm compliance with standards and specifications

6.2. Completeness check:
   - Verify all required drawings are included per drawing index
   - Check that all areas and systems are covered
   - Ensure all details and sections are provided

6.3. Coordination check:
   - Verify consistency across drawings in the set
   - Check coordination with related deliverables (DEL-25.02, DEL-25.03)
   - Identify potential conflicts with other disciplines

6.4. CAD standards check:
   - Verify compliance with CAD manual
   - Check file naming, layer usage, and organization

**Verification:** Self-check complete; originator ready to submit for independent check.

**Source:** Specification.md Verification; **ASSUMPTION** — Standard self-check practice

### Step 7: Interdisciplinary Check (IDC)

**Action:** Coordinate drawings with interfacing disciplines to identify and resolve conflicts.

**Activities:**

7.1. Distribute drawings for IDC:
   - Issue drawings to interfacing disciplines per coordination plan
   - Typical recipients: PKG-17 Electrical, PKG-19 Control Systems, PKG-21/22 Buildings, PKG-24 Security
   - **TBD** — IDC distribution list and schedule

7.2. Conduct IDC review meeting (if applicable):
   - Present design and interface points
   - Discuss coordination issues and conflicts
   - Document action items and agreements

7.3. Resolve IDC comments:
   - Review comments from interfacing disciplines
   - Revise drawings as needed to resolve conflicts
   - Document resolutions and incorporate into drawings
   - **TBD** — Comment management system or process

**Verification:** All IDC comments addressed and resolved; interfacing disciplines concur with coordination.

**Source:** Specification.md Verification (Interdisciplinary Check); **ASSUMPTION** — Standard IDC process

### Step 8: Independent Check (Peer Review)

**Action:** Independent checker performs technical review of drawings.

**Activities:**

8.1. Assign checker:
   - Checker must be qualified and independent (not the originator)
   - **TBD** — Checker assignment per project procedures

8.2. Perform independent check:
   - Review for technical accuracy, completeness, and compliance
   - Verify calculations and design basis
   - Check coordination and interface points
   - Verify CAD standards compliance
   - **Reference:** Specification.md Verification methods

8.3. Document check comments:
   - Checker prepares comment list or marks up drawings
   - Comments categorized (mandatory corrections, suggestions, information)

8.4. Resolve check comments:
   - Originator addresses each comment
   - Revise drawings as needed
   - Document resolutions and obtain checker concurrence
   - **TBD** — Comment resolution workflow

**Verification:** All check comments resolved to checker's satisfaction; checker signs approval.

**Source:** Specification.md Verification (Design Review); **ASSUMPTION** — Standard checking process

### Step 9: Discipline Lead Approval

**Action:** Discipline lead reviews and approves drawings for issue.

**Activities:**

9.1. Final review by discipline lead:
   - Confirm technical adequacy and completeness
   - Verify all checking complete and comments resolved
   - Ensure compliance with project requirements and Employer's Requirements
   - **TBD** — Approval criteria and hold points

9.2. Approve for issue:
   - Discipline lead signs approval on drawings
   - Update drawing status and revision
   - **TBD** — Approval authority and delegation

**Verification:** Discipline lead approval signature on drawings.

**Source:** **ASSUMPTION** — Standard approval workflow

### Step 10: Submittal and Issuance

**Action:** Submit drawings per project document control procedures.

**Activities:**

10.1. Prepare submittal package:
   - Compile all drawings in the set
   - Prepare transmittal with drawing list
   - Include supporting documentation if required (design basis memo, calculations)
   - **TBD** — Submittal requirements and format

10.2. Submit to document control:
   - Upload to project document management system
   - Issue per project procedures
   - **TBD** — Document control procedures and EDMS

10.3. Distribute per distribution list:
   - Employer review (if required)
   - Construction team
   - Interfacing disciplines
   - **TBD** — Distribution list and review workflow

10.4. Track review and approval:
   - Monitor Employer review comments (if applicable)
   - Address and incorporate review comments
   - Re-issue as needed with updated revision
   - **TBD** — Review comment management

**Verification:** Drawings issued per document control procedures; submittal tracked and documented.

**Source:** Specification.md Documentation; **ASSUMPTION** — Standard document control practice

### Step 11: Revision Management (As Needed)

**Action:** Manage revisions during design development and post-issue.

**Activities:**

11.1. Initiate revision:
   - Determine need for revision (design changes, comment incorporation, errors)
   - Update revision designation per project system

11.2. Make revisions:
   - Update drawings with changes
   - Mark revision clouds and triangles per CAD standards
   - Update revision table in title block
   - Document reason for revision

11.3. Repeat verification steps:
   - Depending on extent of changes, may require re-check and re-approval
   - **TBD** — Revision checking requirements

11.4. Re-issue revised drawings:
   - Submit revised drawings per Step 10
   - Supersede previous revision in document management system

**Verification:** Revisions properly documented, checked, approved, and issued.

**Source:** **ASSUMPTION** — Standard revision management

## Verification

**Verification Activities Summary:**

Per Specification.md Verification section, the following verification methods apply:

1. **Design Review (Peer Check):** Independent review by qualified checker (Step 8)
   - Technical accuracy and completeness
   - Code and standards compliance
   - **Acceptance Criteria:** All comments resolved and closed

2. **Dimensional Verification:** Coordination with architectural and civil drawings (Steps 2-4, Step 7)
   - Location accuracy
   - Interference checking
   - **Acceptance Criteria:** No unresolved conflicts with interfacing disciplines

3. **Interdisciplinary Check (IDC):** Coordination review with interfacing disciplines (Step 7)
   - Interface point verification
   - Conflict resolution
   - **Acceptance Criteria:** All disciplines concur with design coordination

4. **CAD Standards Compliance Check:** Verification of CAD standards (Steps 5-6, Step 8)
   - Layer usage, line weights, text styles
   - Title block and drawing border compliance
   - File naming and organization
   - **Acceptance Criteria:** Full compliance with project CAD manual

**Source:** Specification.md Verification

**Sign-Off Requirements:**

- **Originator sign-off:** Self-check complete (Step 6)
- **Checker sign-off:** Independent check complete, all comments resolved (Step 8)
- **Approver sign-off:** Discipline lead approval for issue (Step 9)
- **TBD** — Signature protocol and delegation of authority per project quality procedures

**Source:** **ASSUMPTION** — Standard engineering sign-off protocol

**Verification Records:**

All verification activities shall be documented:
- Design review checklists
- IDC comment logs and resolutions
- Check comment logs and resolutions
- Approval signatures (in drawing title blocks or separate approval sheets)
- **TBD** — Records location and retention per project quality plan

**Source:** Specification.md Verification; **ASSUMPTION** — QA/QC record requirements

## Records

**Documentation Outputs:**

Per Decomposition Table PKG-25 DEL-25.01, the following artifacts are produced:
- **Fiber network layout**
- **Communications distribution drawings**
- **Patch panel locations**

Supporting documentation may include:
- Drawing index / list of drawings
- Design basis memorandum: **TBD**
- Calculation sheets (pathway fill, etc.): **TBD**
- **TBD** — As-built drawing requirements (post-construction, see DEL-25.04)

**Source:** Decomposition Table PKG-25 DEL-25.01; Specification.md Documentation

**Record Management:**

**Filing Locations:**
- Working files: `1_Working/DEL-25.01_Communications_Design_Drawing_Set/` (this folder)
- Review packages: `2_Checking/To/` (during review cycle)
- Issued documents: `3_Issued/` (upon approval and issuance)
- Electronic records: **TBD** — Project document management system (EDMS)

**Source:** Project folder structure convention; **ASSUMPTION** — Standard filing practice

**Retention Requirements:**
- **TBD** — Per project document control plan and contractual requirements
- Typically: Retain all revisions and native CAD files for contract duration plus warranty period

**Lifecycle Tracking:**
- Update `_STATUS.md` as deliverable progresses through lifecycle states
- Current state: INITIALIZED
- Target progression: INITIALIZED → IN_PROGRESS (when design work commences) → CHECKING (when submitted for review) → ISSUED (when approved)

**Source:** `_STATUS.md`; project lifecycle model per AGENTS.md

**Archival:**
- **ASSUMPTION**: Electronic records archived in project document management system
- Native CAD files archived with supporting reference files
- **TBD** — Archival format and media per project requirements

**Source:** **ASSUMPTION** — Standard electronic document archival practice

## Notes

**Process Customization:**

This procedure represents a general workflow for producing a communications design drawing set. Actual implementation may vary based on:
- Project-specific procedures and quality plans
- Employer's review and approval requirements
- Design stage (conceptual, 30%, 60%, 90%, IFC) and associated detail levels
- Contractual requirements

**TBD** — Project-specific procedure adaptations

**Source:** **ASSUMPTION** — Standard engineering workflow adapted to project specifics

**Coordination with Related Deliverables:**

This drawing set is closely coordinated with other PKG-25 deliverables:
- **DEL-25.02 Communications Technical Specification:** Provides performance and material requirements that inform drawing content
- **DEL-25.03 Communications Data Sheet Package:** Equipment specifications inform rack layouts and patch panel arrangements
- **DEL-25.04 Communications Installation & Test Records:** Test requirements may inform design details and acceptance criteria

Design decisions and information flow bi-directionally between these deliverables during design development.

**Source:** Logical relationship between PKG-25 deliverables; Specification.md cross-references

**Key Assumptions to Validate:**

- Project CAD standards and procedures
- Approval workflow and authority matrix
- Submittal requirements and schedule
- Interface control procedures
- Checking and review requirements
- Document control and EDMS procedures

These should be confirmed from project-specific quality and procedures documentation when available.

**Source:** **ASSUMPTION** — Standard practices pending project-specific procedures
