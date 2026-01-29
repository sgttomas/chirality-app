# Procedure: DEL-21.01 Building Design Drawing Set

## Purpose

This procedure defines the process for **producing** the **Building Design Drawing Set** within **PKG-21 Building Structures & Envelope**.

**Deliverable Purpose:** Defines the design arrangement and details for building per ER requirements.

**Source:** Decomposition document line 513

**Deliverable Type:** Drawing
**Responsible Party:** D&B Contractor

**Procedure Scope:** This procedure describes the workflow for developing, coordinating, reviewing, and issuing the building design drawings. It covers the design drawing production process from initial concept through issued-for-construction (IFC) status.

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

**Source:** `_DEPENDENCIES.md`

**Typical Upstream Inputs (to be coordinated externally):**

1. **Employer's Requirements (ER)**
   - **TBD**: ER Volume 2 Part 3 (Building Works) — project-specific building functional requirements, performance criteria, materials/finishes
   - **Source:** Decomposition Section 3 (Reference Documents)

2. **Site Information**
   - **TBD**: Site survey and topographic information (elevations, existing conditions)
   - **TBD**: Geotechnical investigation report (soil conditions, bearing capacity, foundation recommendations)
   - **TBD**: Existing utilities survey (underground and overhead obstructions)
   - **TBD**: Site civil/grading design (finish grades, drainage, access roads)

3. **Equipment Information**
   - **TBD**: MCC electrical equipment layout and dimensional requirements (footprints, clearances, heat dissipation)
   - **TBD**: Equipment weights and anchorage requirements (for structural design)
   - **TBD**: Cable entry/exit requirements and routing

4. **Hazardous Area Classification**
   - **TBD**: Facility hazardous area classification study (determines building ventilation and electrical equipment requirements)

5. **Project Standards and Procedures**
   - **TBD**: Project CAD standards manual (layer conventions, line weights, text styles, title blocks)
   - **TBD**: Project drawing numbering system
   - **TBD**: Project document control procedures
   - **TBD**: Project Quality Management Plan (review and approval procedures)

6. **Design Criteria and Basis of Design**
   - **TBD**: Building design criteria document (loads, environmental conditions, performance targets)
   - **TBD**: Materials selection criteria (corrosion protection, durability, lifecycle cost considerations)

### Reference Materials

**Codes and Standards:**

Per Specification.md and Datasheet.md:
- NBC 2020 (National Building Code of Canada 2020)
- Provincial building code (BCBC 2018 or ABC 2019) — **TBD**: Confirm applicable code
- CSA A23.3 (Design of Concrete Structures)
- CSA S16 (Design of Steel Structures)
- ASHRAE 90.1 (Energy Standard for Buildings)
- CSA B651 (Accessible Design for the Built Environment)

**Project Reference Documents:**

- See `_REFERENCES.md` for additional reference materials
- See package `0_References/` folder for reference documents

### Personnel Requirements

**Design Team Roles:**

1. **Lead Building Designer (Architect or Structural Engineer with Building Design Experience)**
   - **TBD**: Professional designation requirements (P.Eng. or Architect registration in BC)
   - Responsible for overall building design coordination
   - Reviews and approves design drawings

2. **Building Designer / Drafter**
   - Develops building design concepts and produces CAD drawings
   - Performs self-check of drawings
   - **TBD**: Experience/qualification requirements per project quality procedures

3. **Structural Engineer**
   - Provides structural system design and sizing (coordinates with DEL-21.03: Building Design Calculations)
   - Reviews building design drawings for structural adequacy
   - **TBD**: P.Eng. registration in BC required

4. **Independent Checker**
   - Performs independent technical review of drawings
   - Checks design compliance with codes, standards, and ER requirements
   - Checks dimensional accuracy and drawing completeness
   - **TBD**: Qualification requirements (typically P.Eng. or senior designer/architect)

5. **Discipline Coordinator (for Interdisciplinary Checks)**
   - Coordinates building design with other disciplines (civil, MEP, process, electrical)
   - Facilitates IDC meetings and issue resolution
   - **TBD**: Role assignment and authority

**Source:** Typical engineering project organization; **TBD**: Project-specific roles and qualifications per Quality Management Plan

### Tools and Software

- **CAD Software:** **TBD** — AutoCAD, Revit, or other project-standard software
- **Document Management System:** **TBD** — Project DMS for drawing storage, revision control, transmittal
- **Review/Markup Tools:** **TBD** — PDF markup software for review comments
- **Analysis Software (if required):** **TBD** — Structural analysis, energy modeling, daylighting analysis

### Project Readiness

- Project kick-off meeting completed
- Project CAD standards established and communicated to design team
- Document numbering system assigned for DEL-21.01 drawings
- Access to project DMS and reference materials established
- Design team roles and responsibilities assigned

## Steps

### Step 1: Design Initiation and Requirements Review

**Objective:** Establish design basis and understand project requirements.

**Activities:**

1.1 **Review Employer's Requirements**
   - Review ER Volume 2 Part 3 (Building Works) for:
     - Building functional requirements (MCC building, operator shelters)
     - Space programs and equipment clearances
     - Performance criteria (structural, envelope, fire, accessibility)
     - Materials and finishes requirements
     - Deliverable expectations and acceptance criteria
   - **TBD**: Document ER requirements in design basis document or requirements traceability matrix

1.2 **Review Project Objectives**
   - Understand project objectives relevant to building design (OBJ-1, OBJ-5, OBJ-6, OBJ-9 per decomposition Section 2)
   - Identify design priorities (safety, terminal continuity, regulatory compliance, lifecycle cost optimization)

1.3 **Review Site Conditions**
   - Review site survey (existing conditions, adjacent facilities, access constraints)
   - Review geotechnical investigation (soil conditions, foundation recommendations)
   - Site visit to observe existing terminal operations and site constraints (if feasible)
   - **TBD**: Coordinate with site civil design for building locations and elevations

1.4 **Review Equipment Requirements**
   - Obtain MCC electrical equipment dimensional data (footprints, heights, clearances)
   - Understand equipment heat dissipation and ventilation requirements
   - Coordinate with electrical discipline for equipment layout and cable routing
   - **TBD**: Equipment anchor bolt requirements and structural interface

1.5 **Review Codes and Standards**
   - Confirm applicable codes and standards (NBC 2020, provincial code, CSA standards)
   - Identify special requirements (seismic design, accessibility, energy performance)
   - **TBD**: Obtain code interpretations or rulings from authority having jurisdiction (if required)

1.6 **Establish Design Criteria**
   - Document design loads (dead, live, snow, wind, seismic) per NBC 2020 and site conditions
   - Document environmental design parameters (temperature, humidity, wind, precipitation)
   - Document performance targets (envelope thermal performance, fire ratings, accessibility provisions)
   - **TBD**: Prepare design criteria document or basis of design memorandum for review and approval

**Deliverables from Step 1:**
- Design basis document or requirements summary
- Design criteria (loads, environmental conditions, performance targets)
- Preliminary building program (space requirements, functional adjacencies)

**Source:** Typical design initiation activities; requirements review per Specification.md and Guidance.md

### Step 2: Concept Design Development

**Objective:** Develop building design concept and establish overall arrangement.

**Activities:**

2.1 **Building System Selection**
   - Evaluate building system alternatives (custom-designed vs. pre-engineered/modular) per Guidance.md Trade-off T1
   - Consider schedule, cost, constructability, and terminal continuity (OBJ-5)
   - **TBD**: Engage building system suppliers/manufacturers for design-assist input (if modular or PEMB approach)
   - Select building system approach and document rationale

2.2 **Develop Site Layout**
   - Establish building locations on site plan
   - Coordinate with site civil design (grading, drainage, access roads)
   - Consider construction access and laydown areas
   - Consider terminal operations continuity (avoid conflicts with existing operations per OBJ-5)
   - **TBD**: Develop site plan sketch showing building locations and site context

2.3 **Develop Building Layout**
   - Develop MCC building floor plan (equipment layout, access aisles, door locations)
   - Establish building dimensions (column grid, bay sizes)
   - Develop operator shelter layouts (size, door/window locations, number of shelters) per Guidance.md Trade-off T4
   - Coordinate with equipment requirements and operational flows
   - **TBD**: Develop concept floor plan sketches

2.4 **Develop Structural System Concept**
   - Select structural framing system (steel frame, pre-engineered, modular)
   - Establish column grid and member preliminary sizing
   - Select foundation type (shallow vs. deep foundations) per Guidance.md Trade-off T3 and geotechnical recommendations
   - Coordinate with structural engineer (DEL-21.03: Building Design Calculations)
   - **TBD**: Develop structural framing concept sketches

2.5 **Develop Envelope System Concept**
   - Select envelope system (insulated metal panels, precast concrete, etc.)
   - Establish thermal performance targets per Guidance.md Trade-off T2 (code minimum vs. enhanced performance)
   - Select roofing system (standing seam metal, membrane, etc.)
   - Select doors and windows (types, sizes, performance requirements)
   - Consider corrosion protection and durability in coastal environment per Guidance.md Principle P3
   - **TBD**: Develop envelope system concept and material selections

2.6 **Code Compliance Review (Preliminary)**
   - Review concept design against NBC 2020 requirements:
     - Occupancy classification (Group F industrial typical)
     - Building height and area limits
     - Fire separation and egress requirements
     - Accessibility provisions
   - Identify code compliance issues and design adjustments required
   - **TBD**: Document preliminary code compliance analysis

2.7 **Concept Design Review**
   - Present concept design to project team and Employer (if required)
   - Obtain feedback and approval to proceed to detailed design
   - **TBD**: Document concept design decisions and approvals

**Deliverables from Step 2:**
- Concept site plan
- Concept floor plans
- Concept elevations (sketches)
- Structural system concept
- Envelope system concept
- Preliminary code compliance analysis
- Concept design review meeting minutes

**Source:** Typical building concept design process; coordination requirements per Guidance.md Principle P6

### Step 3: Detailed Design and CAD Drawing Production

**Objective:** Produce detailed building design drawings in CAD per project standards.

**Activities:**

3.1 **Set Up CAD Files**
   - Create drawing files per project CAD standards (layer conventions, line weights, text styles)
   - Set up drawing title blocks per project standards
   - Assign drawing numbers per project numbering system
   - Establish project coordinate system and units
   - **TBD**: Confirm CAD setup with project CAD manager or lead designer

3.2 **Develop Site Plan Drawing**
   - Show building locations with coordinates
   - Show site context (existing buildings, roads, property lines)
   - Show finish grades at building corners
   - Show access roads and paving limits
   - Include north arrow, scale, title block
   - **Drawing ID:** **TBD** (e.g., A-0.01 Site Plan)

3.3 **Develop Floor Plan Drawings**
   - Develop floor plans for MCC building and operator shelters
   - Show:
     - Column grid and dimensions
     - Walls and partitions (with wall type designations)
     - Doors and windows (with schedule references)
     - Equipment layout zones and clearances
     - Floor elevations and level changes
     - Accessibility features (accessible routes, door clearances)
     - Room/space identification
   - Include general notes, abbreviations, symbols legend
   - **Drawing ID:** **TBD** (e.g., A-1.01 MCC Building Floor Plan, A-1.02 Operator Shelter Plans)

3.4 **Develop Roof Plan Drawing**
   - Show roof layout and slopes
   - Show roof drainage (gutters, downspouts, roof drains)
   - Show rooftop equipment locations (HVAC units, if any)
   - Show roof access (hatches, ladders)
   - Include roof elevations and drainage patterns
   - **Drawing ID:** **TBD** (e.g., A-1.99 Roof Plan)

3.5 **Develop Elevation Drawings**
   - Develop exterior elevations for all building facades (North, South, East, West)
   - Show:
     - Building height and floor-to-floor dimensions
     - Window and door locations and elevations
     - Cladding materials and transitions
     - Finish grade and roof elevations
     - Material callouts and finishes
   - **Drawing ID:** **TBD** (e.g., A-2.01 North Elevation, A-2.02 South Elevation, etc.)

3.6 **Develop Section Drawings**
   - Develop building sections showing vertical coordination
   - Show:
     - Foundation to roof assembly
     - Floor-to-floor heights and interior clearances
     - Roof structure and drainage slopes
     - Envelope assembly thicknesses
     - Mechanical/electrical overhead coordination
   - **Drawing ID:** **TBD** (e.g., A-3.01 Building Section A-A, A-3.02 Building Section B-B)

3.7 **Develop Wall Section Drawings**
   - Develop typical wall sections showing envelope assemblies
   - Show:
     - Foundation/floor slab interface
     - Wall construction (framing, insulation, cladding)
     - Window/door jamb and sill details
     - Roof/wall interface
     - Material specifications and assembly notes
   - **Drawing ID:** **TBD** (e.g., A-4.01 Typical Wall Section)

3.8 **Develop Detail Drawings**
   - Develop connection details, flashing details, door/window details as required
   - Reference details from other drawings
   - **Drawing ID:** **TBD** (e.g., A-5.01 Details Sheet 1, A-5.02 Details Sheet 2, etc.)

3.9 **Develop Schedules**
   - Prepare door schedule (door types, sizes, hardware, fire ratings)
   - Prepare window schedule (window types, sizes, glazing specifications)
   - Prepare wall type schedule (wall construction assemblies)
   - **Drawing ID:** **TBD** (e.g., A-6.01 Schedules)

3.10 **Develop Drawing Index and Cover Sheet**
   - Prepare drawing index listing all drawings in set
   - Prepare cover sheet with project information, drawing index, abbreviations, symbols legend
   - **Drawing ID:** **TBD** (e.g., A-0.00 Cover Sheet)

**Deliverables from Step 3:**
- Complete building design drawing set in CAD (all sheets)
- Drawing index
- Door/window/wall type schedules

**Source:** Typical building drawing development; drawing content requirements per Specification.md and Datasheet.md

### Step 4: Self-Check and Quality Review

**Objective:** Designer performs self-check to identify and correct errors before formal review.

**Activities:**

4.1 **Dimensional Check**
   - Verify all dimensions for accuracy and consistency across drawings
   - Check column grid dimensions
   - Check floor-to-floor heights and clearances
   - Check door/window dimensions against schedules
   - Verify foundation/structural interface dimensions

4.2 **Consistency Check**
   - Verify consistency between plan, elevation, and section views
   - Verify material callouts match specifications (DEL-21.02)
   - Verify structural member sizes match calculations (DEL-21.03) — **TBD**: Coordination with structural engineer
   - Check schedule references (all doors/windows on plans appear in schedules)

4.3 **Completeness Check**
   - Verify all sheets have title blocks with correct project information
   - Verify all drawings have north arrow (site plan, floor plans)
   - Verify all drawings have scale notation
   - Verify all details are referenced from main drawings
   - Check for missing notes or incomplete specifications

4.4 **CAD Standards Check**
   - Verify drawing files comply with project CAD standards (layers, line weights, text styles)
   - Verify title blocks are correct and consistent
   - Verify drawing numbers are correct and sequential
   - **TBD**: Run automated CAD checking tools (if available)

4.5 **Code Compliance Check**
   - Review drawings against NBC 2020 requirements:
     - Egress routes and travel distances
     - Barrier-free design provisions (accessible entrances, routes, door clearances)
     - Fire-rated assemblies (if required)
   - Document code compliance or identify non-compliances for resolution

4.6 **Document Self-Check**
   - Designer signs and dates self-check completion
   - Record self-check findings and corrections in design file or quality record
   - **TBD**: Self-check documentation per project quality procedures

**Deliverables from Step 4:**
- Self-check completed and documented
- Drawing set ready for interdisciplinary check and independent review

**Source:** Specification.md Verification VM-02, VM-04, VM-05; typical engineering quality procedures

### Step 5: Interdisciplinary Coordination (IDC)

**Objective:** Coordinate building design with other disciplines to resolve interface conflicts.

**Activities:**

5.1 **Distribute Drawings for IDC**
   - Issue drawing set to affected disciplines for interdisciplinary check:
     - Civil/site (building locations, elevations, drainage)
     - Structural (foundation loads, structural interface)
     - MEP (PKG-22: space coordination, penetrations, roof equipment)
     - Electrical (MCC equipment layout, cable routing)
     - Process (operator shelter locations relative to railcar stations)
   - **TBD**: IDC distribution per project coordination procedures

5.2 **IDC Meeting**
   - Facilitate IDC meeting with discipline representatives
   - Review and discuss interface issues and comments
   - Capture IDC comments and action items
   - Assign responsibility for resolving each comment
   - **TBD**: IDC meeting schedule and format (in-person, online, asynchronous review)

5.3 **Resolve IDC Comments**
   - Address each IDC comment:
     - Update drawings if design changes required
     - Coordinate with other disciplines if interface adjustments needed
     - Document resolution rationale
   - Re-issue drawings if significant changes made (repeat IDC if necessary)

5.4 **Close Out IDC**
   - Verify all IDC comments resolved or dispositioned
   - Obtain IDC sign-off from discipline representatives
   - Document IDC completion in project coordination record
   - **TBD**: IDC close-out documentation per project procedures

**Deliverables from Step 5:**
- IDC comments log with resolutions
- Updated drawings (if changes made)
- IDC sign-off / completion record

**Source:** Specification.md Verification VM-03; Guidance.md Principle P6 (coordination and interface management)

### Step 6: Independent Check

**Objective:** Independent checker performs technical review of drawings for accuracy, completeness, and compliance.

**Activities:**

6.1 **Assign Independent Checker**
   - Assign qualified independent checker (typically P.Eng. or senior designer/architect)
   - Checker must be independent of design origination (not the designer)
   - **TBD**: Checker assignment per project quality procedures

6.2 **Independent Check Review**
   - Checker reviews drawings for:
     - **Design compliance:** Design meets ER requirements, codes, and standards
     - **Technical accuracy:** Dimensions, calculations, member sizes correct
     - **Completeness:** All required sheets, schedules, details present
     - **Consistency:** Plans, elevations, sections consistent; no conflicts
     - **Constructability:** Design is buildable with reasonable means and methods
   - Checker uses review checklist — **TBD**: Project-specific review checklist
   - Checker documents review comments and findings

6.3 **Address Check Comments**
   - Designer reviews check comments
   - Update drawings to address comments (or provide justification if comment not accepted)
   - Re-submit to checker if significant changes made

6.4 **Checker Approval**
   - Checker verifies all comments resolved satisfactorily
   - Checker signs and dates drawings (approval signature/stamp)
   - **TBD**: Checker approval documentation per project quality procedures

**Deliverables from Step 6:**
- Independent check comments log with resolutions
- Checker approval signature/stamp on drawings
- Updated drawings (if changes made)

**Source:** Specification.md Verification VM-01; typical engineering independent check procedures

### Step 7: Approval and Issue

**Objective:** Obtain final approval and issue drawings for construction or next phase.

**Activities:**

7.1 **Design Lead Review and Approval**
   - Lead building designer (or discipline manager) reviews complete drawing set
   - Verifies all reviews completed (self-check, IDC, independent check)
   - Verifies drawing set is complete and ready for issue
   - Signs and dates drawings (approval signature/stamp)
   - **TBD**: Approval authority and signature requirements per project procedures

7.2 **Professional Seal (if required)**
   - Professional engineer (P.Eng.) or architect seals drawings per regulatory requirements
   - **TBD**: Seal requirements for building design drawings in British Columbia (typically P.Eng. required for structural elements; architect seal may be required depending on building classification and AHJ)

7.3 **Prepare Issue Package**
   - Generate PDF set from CAD files
   - Verify PDF quality (readability, plot scale, no missing information)
   - Prepare transmittal letter or cover sheet
   - Assign revision number and issue date
   - Update drawing index with revision information

7.4 **Issue Drawings**
   - Upload drawing set to project document management system (DMS)
   - Transmit drawings per project distribution list (Employer, construction team, authorities having jurisdiction)
   - Record issue in document control log
   - Update `_STATUS.md` to reflect issue status (IN_PROGRESS → CHECKING → ISSUED per deliverable lifecycle)
   - Place issued copies in `3_Issued/` folder per deliverable folder structure

7.5 **Building Permit Submission (if required)**
   - Submit drawings to authority having jurisdiction for building permit review
   - Respond to building department review comments
   - Obtain building permit approval
   - **TBD**: Building permit submission requirements and timeline

**Deliverables from Step 7:**
- Issued drawing set (PDF and CAD files)
- Transmittal record
- Professional seal and approval signatures (if required)
- Building permit application and approval (if required)

**Source:** Specification.md Documentation section; README.md deliverable lifecycle; typical drawing issue procedures

### Step 8: Post-Issue Management

**Objective:** Manage drawing revisions and respond to construction issues.

**Activities:**

8.1 **Respond to Requests for Information (RFIs)**
   - Review RFIs from construction team related to building design drawings
   - Provide clarifications or issue supplemental sketches/details
   - **TBD**: Issue revised drawings if significant changes required (follow revision control process)

8.2 **Issue Drawing Revisions**
   - If design changes required during construction:
     - Update CAD files with changes
     - Mark revisions on drawings (cloud and triangle per drafting standards)
     - Update revision block in title block
     - Repeat review and approval process (Steps 4-7) for revised drawings
     - Issue revised drawing set with incremented revision number

8.3 **Maintain Drawing Records**
   - Maintain current drawing set in project DMS
   - Archive superseded revisions per project document retention policy
   - **TBD**: Record drawing retention requirements and archive procedures

8.4 **Support Construction and Commissioning**
   - Provide design support during construction (site visits, reviews of submittals)
   - Review shop drawings (DEL-21.06) for conformance with design intent
   - Support building commissioning and inspection activities (DEL-21.05)
   - **TBD**: Design support scope and responsibilities during construction

**Deliverables from Step 8:**
- RFI responses
- Revised drawings (if changes made)
- Design support documentation (site visit reports, submittal reviews, etc.)

**Source:** Typical post-issue design management; coordination with DEL-21.05 and DEL-21.06

## Verification

**Verification Activities Throughout Procedure:**

Per Specification.md, verification methods include:

**V1: Design Review (Peer Check)** — Step 6 (Independent Check)
- Independent technical review by qualified checker
- Review against requirements, codes, and standards
- Documented check comments and resolutions

**V2: Dimensional Verification** — Step 4 (Self-Check) and Step 6 (Independent Check)
- Dimensions verified for accuracy and consistency across drawings
- Column grid, floor heights, clearances checked

**V3: Interdisciplinary Check (IDC)** — Step 5 (IDC)
- Coordination with civil, structural, MEP, electrical, process disciplines
- Interface conflicts identified and resolved

**V4: CAD Standards Compliance Check** — Step 4 (Self-Check)
- Layer usage, line weights, text styles verified
- Title blocks and revision tracking verified

**V5: Code Compliance Review** — Step 1 (Requirements Review), Step 2 (Concept Design), Step 4 (Self-Check)
- Design compliance with NBC 2020 verified throughout design process
- Egress, accessibility, fire ratings checked

**Acceptance Criteria:**

Per Specification.md:
- All reviews completed (self-check, IDC, independent check) — **Sign-off required**
- No unresolved IDC comments or conflicts — **IDC close-out record**
- Design complies with applicable codes and standards — **Code compliance documented**
- Drawing set is complete (no missing sheets or details) — **Completeness check passed**
- Employer review and acceptance — **TBD**: Employer approval process
- Authority having jurisdiction acceptance (building permit approval) — **TBD**: If required

**Source:** Specification.md Verification section

## Records

**Documentation Outputs:**

Per Specification.md and Datasheet.md:

**Primary Deliverables (Drawing Set):**
1. MCC Building General Arrangements (GAs)
2. Floor Plans
3. Elevations
4. Sections
5. Operator Shelter Drawings

**Supporting Documentation:**
- Drawing index
- Door/window/wall type schedules
- General notes and abbreviations
- Detail sheets

**Quality Records:**
- Design criteria document or basis of design memorandum
- Concept design review meeting minutes
- Self-check documentation
- IDC comments log and close-out record
- Independent check comments log and approval
- Design lead approval record
- Professional seal (if required)
- Transmittal records and issue log

**Coordination Records:**
- Requirements traceability (ER to design)
- Code compliance analysis/documentation
- Interface coordination records (with civil, structural, MEP, electrical)

**Record Management:**

Per Specification.md Documentation section and README.md:

- **Working location:** `1_Working/DEL-21.01_Building_Design_Drawing_Set/`
- **Review/checking location:** `2_Checking/` (when deliverable in CHECKING status)
- **Issued location:** `3_Issued/` (when deliverable issued)
- **Electronic records:** Project document management system (DMS) — **TBD**: DMS location and access
- **Retention:** **TBD**: Retention period per project and regulatory requirements
- **Archive:** **TBD**: Archive procedures for design documentation

**Revision Control:**

- Drawing revision numbers tracked in title block
- Revision clouds and triangles mark changes on drawings
- Revision history recorded in title block revision block
- Superseded revisions archived per document retention policy

**Source:** Specification.md Documentation section; README.md deliverable folder structure and lifecycle

---

**Procedure Revision History:**

| Date | Revision | Description | Author |
|------|----------|-------------|--------|
| 2026-01-28 | 0 | Initial procedure draft (4_DOCUMENTS enrichment) | 4_DOCUMENTS Agent |

**Note:** This procedure is based on typical building design drawing production workflow and project framework requirements. Specific project procedures, approvals, and documentation requirements should be confirmed with the project Quality Management Plan and Employer's Requirements.
