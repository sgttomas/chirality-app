# Procedure: DEL-05.01 Concrete Structures Design Drawing Set

## Purpose

Produce and control the structural **Concrete Structures Design Drawing Set** for PKG-05, ensuring the drawings:
- Define the design arrangement and details for concrete structures per Employer's Requirements
- Support construction, fabrication, and QA/QC verification
- Maintain consistency with design calculations, specifications, and project objectives
- Meet project quality, document control, and coordination requirements
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232; Specification.md: Scope.)

## Prerequisites

### P-01: Dependencies (Coordinated Externally — NOT_TRACKED Mode)

Dependencies are coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`). Confirm required inputs before freezing layouts to minimize revisions and rework:

**Geotechnical inputs (from PKG-02):**
- Bearing capacity and settlement tolerances
- Soil properties and groundwater levels
- Ground improvement requirements if applicable
- Foundation recommendations from geotechnical investigation

**Equipment inputs (from PKG-10, PKG-11, PKG-13, PKG-15):**
- Equipment loads (dead, live, operating, seismic)
- Anchor bolt layouts and embedment requirements
- Equipment mounting elevations and tolerances
- Vibration isolation requirements if applicable
- Equipment vendor general arrangement (GA) drawings

**Tank inputs (from PKG-13):**
- Tank nozzle loads and anchor bolt loads
- Tank foundation settlement tolerances
- Tank foundation interface requirements
- Ground liner system coordination

**Piping inputs (from PKG-14):**
- Pipe support locations and loads
- Thrust block requirements and sizing
- Penetration locations through containment walls

**Utilities inputs (from PKG-03):**
- Underground drainage and duct bank locations
- Clash avoidance requirements
- Sump and drainage penetration requirements

**Building inputs (from PKG-21/PKG-22):**
- Control room and pump house foundation interfaces
- Building column loads and foundation requirements

**Coordination approach:**
- Hold layout freeze points until critical inputs are received
- Document assumptions clearly when inputs are not yet available
- Maintain assumption register and update drawings when inputs are confirmed
- Conduct interdisciplinary checks (IDC) before major milestones

(Source: `_DEPENDENCIES.md`; test/execution/_Coordination/_COORDINATION.md; Guidance.md: C-01.)

### P-02: Reference Materials

**Employer's Requirements (clause locations TBD):**
- Volume 2 Part 1: General Requirements (document control, QA/QC requirements)
- Volume 2 Part 2: Civil & Process Mechanical Works (concrete requirements, structural requirements)
- Volume 2 Part 3: Building Works (if applicable to PKG-05 scope)
(Source: execution/PKG-05_Concrete_Structures/0_References/_REFERENCE_INDEX.md; test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD.)

**Project design basis documents (TBD):**
- Design basis memorandum
- Geotechnical investigation report (from PKG-02)
- Seismic design parameters
- Environmental exposure classifications
- Load combinations and load factors

**Related deliverables (as they mature):**
- DEL-05.02: Concrete Structures Technical Specification (material requirements, quality standards)
- DEL-05.03: Concrete Structures Design Calculations (foundation sizing, wall design, seismic analysis)
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:233; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234; Specification.md: QR-03.)

### P-03: Scope Baseline

Confirm anticipated artifacts and PKG-05 scope for drawing coverage:
- **Package scope:** Foundations, containment walls, equipment pads, thrust blocks, ground liner system
- **Anticipated artifacts:** Foundation plans, containment wall plans, equipment pad details, reinforcement drawings
- **Project objectives:** OBJ-3 (Storage Capacity 45,000 MT), OBJ-7 (Environmental Protection)
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:782; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; Datasheet.md: Construction.)

### P-04: Document Controls

Project document control conventions (TBD until requirements are extracted):
- Drawing numbering system
- Revision tracking and issue status management
- Title block conventions
- CAD standards (layering, symbology, file formats)
- Issue formats (PDF and native CAD files)
- Electronic submission requirements
(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Datasheet.md: Attributes; Specification.md: QR-01.)

## Steps

### Step 1: Confirm Scope and Create Drawing List

**Actions:**
1. Review decomposition scope for PKG-05 (foundations, containment walls, equipment pads, thrust blocks, ground liner system).
2. Review anticipated artifacts (foundation plans, containment wall plans, equipment pad details, reinforcement drawings).
3. Create preliminary drawing list covering all anticipated artifacts and typical details.
4. Organize drawing list by sheet type (general, foundations, containment, reinforcement, typical details).
5. Assign drawing numbers per project document control system (**TBD**).
6. Identify coordination requirements with adjacent disciplines.

**Outputs:**
- Preliminary drawing list with sheet descriptions and drawing numbers
- Coordination matrix identifying required interdisciplinary inputs

**Verification:**
- Drawing list covers all Specification requirements FR-01 through FR-06
- Drawing list addresses all Datasheet Construction artifacts
- Coordination requirements identified for all interfaces

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232; Specification.md: FR-01; Datasheet.md: Construction; Guidance.md: E-01.)

### Step 2: Collect Design Inputs and Document Assumptions

**Actions:**
1. Request geotechnical parameters from PKG-02 (bearing capacity, settlement, soil properties).
2. Request equipment loads and anchor bolt layouts from equipment packages (PKG-10, PKG-11, PKG-13, PKG-15).
3. Request tank interface requirements from PKG-13 (nozzle loads, settlement tolerances).
4. Request piping support loads and thrust block requirements from PKG-14.
5. Request underground utility clash avoidance information from PKG-03.
6. Request building foundation interface requirements from PKG-21/PKG-22 if applicable.
7. Document assumptions where inputs are not yet available (maintain assumption register).
8. Identify hold points where layout freeze depends on receiving critical inputs.

**Outputs:**
- Design input register with received/pending status
- Assumption register with source and impact assessment
- Hold point list identifying layout freeze dependencies

**Verification:**
- All Prerequisite P-01 inputs are requested or assumptions documented
- Assumption register identifies impact on drawings and mitigation approach
- Hold points align with project schedule and coordination plan

(Source: `_DEPENDENCIES.md`; test/execution/_Coordination/_COORDINATION.md; Guidance.md: C-01; Specification.md: IR-01.)

### Step 3: Develop Structural Arrangements (Layout and Sections)

**Actions:**
1. Develop tank foundation layouts (3 × 15,000 MT tanks) showing dimensions, elevations, anchor bolt circles.
2. Develop equipment pad foundation layouts showing pad locations, dimensions, anchor bolt patterns.
3. Develop building foundation layouts if within PKG-05 scope (**TBD** scope boundary).
4. Develop thrust block layouts for underground piping systems (coordinate with PKG-14).
5. Develop containment wall layouts showing wall extents, heights, joint locations.
6. Develop foundation sections showing thickness, reinforcement zones, bearing surface details.
7. Develop containment wall sections showing wall thickness, joint details, liner interfaces.
8. Apply Specification requirements FR-02 (Foundation Details) and FR-03 (Containment Wall Details).
9. Apply Guidance Principles P-01 (Scope Fidelity), P-02 (Containment Clarity), P-05 (Interface Visibility).
10. Coordinate layouts with underground utilities (PKG-03) to avoid clashes.

**Outputs:**
- Foundation layout drawings (plans and sections)
- Containment wall layout drawings (plans and sections)
- Equipment pad layout drawings
- Thrust block layout drawings
- Section drawings showing key dimensions and reinforcement zones

**Verification:**
- Layouts cover all required foundation types (tanks, equipment, buildings, thrust blocks)
- Containment walls provide secondary containment for tank farm (OBJ-7 Environmental Protection)
- Dimensions, elevations, and sections are sufficient for construction and QA/QC
- No clashes with underground utilities (coordinate with PKG-03)
- Interface points with other disciplines are identified

(Source: Specification.md: FR-02; Specification.md: FR-03; Guidance.md: P-01; Guidance.md: P-02; Guidance.md: P-05; Guidance.md: C-01.)

### Step 4: Detail Reinforcement and Critical Elements

**Actions:**
1. Develop reinforcement plans for foundations showing bar marks, spacing, laps, cover requirements.
2. Develop reinforcement plans for containment walls showing vertical/horizontal reinforcement, joint reinforcement.
3. Prepare bar bending schedules with bar marks, quantities, dimensions, bend details.
4. Detail construction joints, control joints, and expansion joints (locations, shear keys, dowels, waterstops).
5. Detail waterstop installations at containment wall joints (coordinate with ground liner system).
6. Detail penetrations through containment walls (sleeves, sealing, waterproofing).
7. Detail embedments (anchor bolts, plates, sleeves, blockouts) for other disciplines.
8. Detail equipment mounting provisions (anchor bolts, grout pockets, shim details).
9. Apply Specification requirements FR-04 (Equipment Pad Details), FR-05 (Reinforcement Presentation), FR-06 (Typical Details).
10. Apply Guidance Principles P-02 (Containment Clarity), P-03 (Traceability), P-05 (Interface Visibility).
11. Apply Guidance Considerations C-02 (Constructability), C-03 (Durability and Exposure).

**Outputs:**
- Reinforcement plans (foundations, containment walls, equipment pads)
- Bar bending schedules with bar marks and quantities
- Joint details (construction, control, expansion) with waterstops
- Penetration and embedment details
- Equipment mounting details
- Typical details for repetitive elements

**Verification:**
- Reinforcement is detailed for fabrication and installation (bar marks, schedules, laps, cover)
- Reinforcement congestion is minimized through detailing and sequencing (constructability)
- Clear cover meets durability requirements by exposure zone (**TBD** from ERs)
- Containment joints are detailed to prevent leakage (waterstops, sealants)
- Embedments and penetrations are clearly identified for interdisciplinary coordination
- Typical details reduce repetition and improve construction quality

(Source: Specification.md: FR-04; Specification.md: FR-05; Specification.md: FR-06; Guidance.md: P-02; Guidance.md: P-03; Guidance.md: P-05; Guidance.md: C-02; Guidance.md: C-03.)

### Step 5: Draft to Project Standards and Apply General Notes

**Actions:**
1. Apply project CAD standards (layering, symbology, line weights, text styles) (**TBD**).
2. Apply project title block conventions (drawing number, title, revision, status, approvals) (**TBD**).
3. Ensure drawing metadata matches Datasheet attributes (drawing number, revision, classification).
4. Prepare general notes covering:
   - Concrete strength and exposure class by element type
   - Cover requirements by exposure zone
   - Reinforcement specifications (grade, type, lap/coupler requirements)
   - Construction joint and waterstop requirements
   - Curing requirements and quality control
   - Interface notes and hold points for other disciplines
   - Code references (when confirmed from ERs)
5. Prepare drawing legend with symbols and abbreviations.
6. Prepare drawing list / sheet index.
7. Apply Specification requirements QR-01 (Document Control) and QR-03 (Technical Consistency).
8. Apply Guidance Principle P-03 (Traceability) and P-04 (Evidence-Based Code Reference).

**Outputs:**
- Drawings formatted per project CAD and title block standards
- General notes sheet with comprehensive notes
- Legend sheet with symbols and abbreviations
- Drawing list / sheet index

**Verification:**
- CAD standards are applied consistently across all drawings
- Title blocks match Datasheet metadata (drawing number, revision, status)
- General notes cover all critical requirements (strength, cover, reinforcement, joints, curing)
- Drawing list is complete and accurate
- Code references are sourced from ERs (or flagged as TBD)

(Source: Datasheet.md: Attributes; Specification.md: QR-01; Specification.md: QR-03; Guidance.md: P-03; Guidance.md: P-04.)

### Step 6: Conduct Checks and Incorporate Comments

**Actions:**
1. **Originator self-check:** Review drawings for completeness, accuracy, consistency, and compliance with Specification requirements.
   - Verify all anticipated artifacts are present (Specification FR-01)
   - Verify dimensions, elevations, and notes are accurate and consistent
   - Verify reinforcement schedules match plans
   - Verify general notes are complete and correct
   - Verify interfaces are identified and coordinated

2. **Independent/peer check:** Technical review by independent checker (not the originator).
   - Review structural adequacy and code compliance
   - Review constructability and practical detailing
   - Review consistency with DEL-05.02 (Technical Specification) and DEL-05.03 (Design Calculations)
   - Review for errors, omissions, and inconsistencies
   - Document check comments and required actions

3. **Interdisciplinary check (IDC):** Coordinate with adjacent disciplines to verify interfaces.
   - Electrical (PKG-17): Conduit sleeves and embedments
   - Piping (PKG-14): Pipe sleeves, thrust blocks, penetrations
   - Instrumentation (PKG-20): Instrument penetrations and mounting
   - Equipment (PKG-10, PKG-11, PKG-13, PKG-15): Anchor bolts, equipment interfaces
   - Drainage (PKG-03): Drainage penetrations, sumps, clash avoidance
   - Marine (PKG-08): Interface with marine structures if applicable
   - Buildings (PKG-21/PKG-22): Building foundation interfaces if applicable
   - Document IDC comments and required actions

4. **Incorporate comments:** Address all check and IDC comments.
   - Update drawings to incorporate accepted comments
   - Document comment resolution (accept, reject with justification, or carry forward as assumption/TBD)
   - Re-check drawings if significant changes are made

5. Apply Specification requirements QR-02 (Checking Process) and IR-02 (Interface Identification).
6. Apply Guidance Principle P-05 (Interface Visibility) and Considerations C-04 (Interface Identification).

**Outputs:**
- Originator check report with findings and resolutions
- Independent check report with comments and resolutions
- IDC comment log with actions and closures
- Updated drawings incorporating check comments
- Check evidence per project QA/QC requirements

**Verification:**
- All Specification requirements (FR-01 through QR-03) are verified by checks
- All interfaces identified in Guidance C-04 are coordinated via IDC
- All check comments are addressed and documented
- Drawings are consistent with DEL-05.02 and DEL-05.03 (as available)
- Check evidence is retained per QA/QC requirements

(Source: Specification.md: QR-02; Specification.md: IR-02; Guidance.md: P-05; Guidance.md: C-04; test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD.)

### Step 7: Assemble Issue Package and Submit

**Actions:**
1. Finalize drawings and update revision status per project document control.
2. Generate PDF issue copies and prepare native CAD files per project requirements.
3. Assemble issue package:
   - Drawing set (all sheets in drawing list)
   - Drawing list / sheet index
   - General notes and legend
   - Typical details index if applicable
4. Assemble QA/QC records:
   - Originator check records
   - Independent check records
   - IDC records and comment log
   - Review comment/response tracking
   - Check evidence per project QA/QC requirements (**TBD** specific forms)
5. Update Datasheet status and revision metadata.
6. Submit issue package per project document control process (electronic submission requirements **TBD**).
7. Update `_STATUS.md` to next lifecycle state per project process (e.g., IN_PROGRESS → CHECKING → ISSUED).
8. Apply Specification Documentation requirements.

**Outputs:**
- Issued drawing set (PDF and native CAD files)
- Drawing list / sheet index
- General notes and legend
- QA/QC records package
- Updated Datasheet and `_STATUS.md`

**Verification:**
- All drawings in drawing list are included in issue package
- Drawing revisions and statuses are consistent across title blocks, drawing list, and Datasheet
- All required QA/QC records are assembled and complete
- Issue package meets project document control and submission requirements
- `_STATUS.md` lifecycle state is updated appropriately

(Source: Specification.md: Documentation; Datasheet.md: Attributes; test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD.)

## Verification

### Completeness Verification (Maps to Specification Verification)

**Anticipated artifacts present and complete:**
- Foundation plans (tank foundations, equipment pads, building foundations, thrust blocks) — Specification FR-02
- Containment wall plans (secondary containment layouts, sections, details) — Specification FR-03
- Equipment pad details (anchor bolt layouts, grout pockets, mounting details) — Specification FR-04
- Reinforcement drawings (plans, sections, schedules, bar bending details) — Specification FR-05
- Typical details (joints, embedments, standard reinforcement) — Specification FR-06
- Drawing list / sheet index, general notes, legend — Specification Documentation

**Verification method:** Review drawing list against Specification FR-01 and Datasheet Construction artifacts. Confirm each anticipated artifact is present and internally consistent. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232; Specification.md: FR-01; Datasheet.md: Construction; Procedure Step 1.)

### Consistency Verification (Maps to Specification Verification)

**Internal consistency:**
- Dimensions and elevations are consistent across plans, sections, and details
- Reinforcement schedules match reinforcement plans (bar marks, quantities, locations)
- General notes do not contradict detail drawings
- Section cut references are correct and complete
- Interface notes are consistent across related drawings

**Cross-deliverable consistency:**
- Drawing notes/details align with DEL-05.02 (Technical Specification) — Specification QR-03
- Drawing dimensions/loads align with DEL-05.03 (Design Calculations) — Specification QR-03
- Drawing metadata matches Datasheet (drawing number, revision, status, classification) — Specification QR-01

**Verification method:** Originator check (Step 6.1), independent check (Step 6.2), cross-reference to DEL-05.02 and DEL-05.03 as available. (Source: Specification.md: QR-01; Specification.md: QR-03; Datasheet.md: Attributes; Procedure Steps 5 and 6.)

### Design Basis Verification (Maps to Specification Verification)

**Design basis alignment:**
- Concrete strengths and exposure classes match design basis (**TBD** from ERs) — Specification PR-01
- Cover requirements match durability requirements by exposure zone — Specification PR-01
- Seismic detailing meets seismic design parameters — Specification PR-01
- Foundation sizing and reinforcement align with DEL-05.03 calculations — Specification QR-03
- Containment details support OBJ-7 Environmental Protection intent — Specification PR-02

**Verification method:** Independent check (Step 6.2) reviews technical adequacy and code compliance; cross-reference to DEL-05.03 Design Calculations when available. (Source: Specification.md: PR-01; Specification.md: PR-02; Guidance.md: P-02; Procedure Step 6.2.)

### Interface Verification (Maps to Specification Verification)

**Interface identification and coordination:**
- Embedded items, hold points, and interface elevations are clearly noted — Specification IR-02
- Interfaces with other disciplines are identified and coordinated via IDC — Specification IR-01, QR-02
- IDC comments are addressed and documented — Specification QR-02
- Coordination notes reference correct discipline drawings — Specification IR-02

**Verification method:** IDC process (Step 6.3) confirms interfaces with PKG-03, PKG-08, PKG-10, PKG-11, PKG-13, PKG-14, PKG-15, PKG-17, PKG-20, PKG-21/PKG-22 as applicable. (Source: Specification.md: IR-01; Specification.md: IR-02; Guidance.md: C-04; Procedure Step 6.3.)

### Requirement Coverage Verification (Maps to Specification Verification)

**Each Specification requirement has corresponding drawing content:**
- FR-01 through FR-06: Functional requirements → Drawing artifacts (verified in Step 1 and Step 6.1)
- PR-01 through PR-03: Performance requirements → Design basis notes and details (verified in Step 5 and Step 6.2)
- IR-01 through IR-02: Interface requirements → Interface notes and IDC (verified in Step 6.3)
- QR-01 through QR-03: Quality requirements → Document control, checks, consistency (verified in Steps 5, 6, 7)

**Each Specification requirement has corresponding Procedure step:**
- All requirements traced through Steps 1-7 and verification checks

**Verification method:** Requirement traceability matrix (implicit in Procedure steps); review drawing content against Specification requirements; review Procedure steps against Specification requirements. (Source: Specification.md: Requirements; Specification.md: Verification; Procedure Steps 1-7.)

### QA/QC Evidence Verification (Maps to Specification Verification)

**QA/QC records complete and retained:**
- Originator check records — Step 6.1
- Independent check records — Step 6.2
- IDC records and comment log — Step 6.3
- Review comment/response tracking — Step 6.4
- Check evidence per project QA/QC requirements (**TBD** specific forms)

**Verification method:** Review assembled QA/QC records package (Step 7) against project QA/QC and document control requirements. (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Specification.md: QR-02; Procedure Step 7.)

## Records

**Drawing set deliverables:**
- Foundation plans (tank foundations, equipment pads, building foundations, thrust blocks)
- Containment wall plans (secondary containment layouts, sections, details)
- Equipment pad details (anchor bolt layouts, grout pockets, mounting details)
- Reinforcement drawings (plans, sections, schedules, bar bending details)
- Typical details (joints, embedments, standard reinforcement)
- Drawing list / sheet index
- General notes and legend
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232; Specification.md: Documentation; Datasheet.md: Construction.)

**QA/QC records:**
- Originator check records (checklist, findings, resolutions)
- Independent check records (reviewer name, date, comments, resolutions)
- IDC records (disciplines coordinated, comments, closures)
- Review comment/response log
- Check evidence per project QA/QC requirements (**TBD** specific forms/checklists)
(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Specification.md: Documentation.)

**Coordination records:**
- Design input register (requested inputs, received status, assumptions)
- Assumption register (source, impact, mitigation, resolution)
- Hold point list (layout freeze dependencies, resolution)
- IDC comment log (discipline, comment, action, closure)
(Source: Procedure Steps 2 and 6.)

**Project records:**
- Issued drawing set files (PDF and native CAD)
- Drawing transmittal and submission records
- Updated Datasheet metadata
- Updated `_STATUS.md` lifecycle state
(Source: Specification.md: Documentation; Procedure Step 7.)

## Procedure Steps Traceability

| Procedure Step | Specification Requirements Verified | Guidance Principles/Considerations Applied | Datasheet Sections Addressed |
|----------------|-------------------------------------|-------------------------------------------|------------------------------|
| Step 1: Confirm Scope and Create Drawing List | FR-01 Artifact Coverage | P-01 Scope Fidelity, E-01 Sheet Grouping | Construction (all artifacts) |
| Step 2: Collect Design Inputs | IR-01 Dependency Coordination, PR-01 Design Basis Alignment | C-01 Required Inputs, C-03 Durability, C-05 Seismic | Conditions (TBD inputs) |
| Step 3: Develop Structural Arrangements | FR-02 Foundation Details, FR-03 Containment Wall Details | P-01, P-02 Containment Clarity, P-05 Interface Visibility | Construction: Foundations, Containment Walls |
| Step 4: Detail Reinforcement and Critical Elements | FR-04 Equipment Pad Details, FR-05 Reinforcement, FR-06 Typical Details, PR-02 Containment Performance | P-02, P-03, P-05, C-02 Constructability, C-04 Interface ID | Construction: Equipment Pads, Reinforcement, Typical Details |
| Step 5: Draft to Project Standards | QR-01 Document Control, QR-03 Technical Consistency | P-03 Traceability, P-04 Evidence-Based Code Reference | Attributes (all) |
| Step 6: Conduct Checks | QR-02 Checking Process, IR-02 Interface Identification | P-05 Interface Visibility, C-04 Interface ID | — (verification) |
| Step 7: Assemble Issue Package | Documentation requirements | — | Attributes (Issue Format) |

## Cross-Document Notes

- **Specification:** This Procedure's steps (Steps 1-7) and verifications demonstrate compliance with all `Specification.md` requirements (§FR-01 through §QR-03). The Procedure Steps Traceability table above maps each step to the Specification requirements it addresses. (Source: Specification.md: Requirements; Specification.md: Requirements Traceability Matrix; Specification.md: Verification.)
- **Guidance:** Use `Guidance.md` Principles (§P-01 through §P-05), Considerations (§C-01 through §C-05), and Examples (§E-01 through §E-03) to ensure containment/environmental intent is visible in details and notes, constructability is considered, and interfaces are clearly identified. The Procedure Steps Traceability table above maps each step to the Guidance sections that inform execution. (Source: Guidance.md: Principles; Guidance.md: Considerations; Guidance.md: Examples; Guidance.md: Guidance-to-Specification Traceability.)
- **Datasheet:** `Datasheet.md` §Construction lists the anticipated artifacts that Steps 1, 3, and 4 must produce. §Attributes define the metadata requirements that Step 5 must implement. §Cross-Document Traceability identifies the linkages this Procedure must maintain. (Source: Datasheet.md: Construction; Datasheet.md: Attributes; Datasheet.md: Cross-Document Traceability.)
