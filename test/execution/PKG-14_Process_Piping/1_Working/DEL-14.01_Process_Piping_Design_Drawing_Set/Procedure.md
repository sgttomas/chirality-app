# Procedure: DEL-14.01 Process Piping Design Drawing Set

## Purpose

This procedure defines the process for **producing** the **Process Piping Design Drawing Set** within **PKG-14 Process Piping**.

**Deliverable description** (source: Decomposition DEL-14.01; scope: Specification.md Scope; rationale: Guidance.md Purpose): Defines the design arrangement and details for process piping per ER requirements.

**Deliverable characteristics:**
- **Type:** Drawing (attributes: Datasheet.md Identification)
- **Discipline:** Mechanical (Process Piping)
- **Responsible:** D&B Contractor

**Drawing outputs** (source: Decomposition DEL-14.01; attributes: Datasheet.md Drawing Types; requirements: Specification.md Functional Requirements - Drawing content):
- P&IDs (Process and Instrumentation Diagrams) (requirements: Specification.md FR-5; description: Datasheet.md Construction - P&IDs; considerations: Guidance.md Considerations item 2)
- Piping GAs (General Arrangement drawings) (requirements: Specification.md FR-6; description: Datasheet.md Construction - Piping GAs; considerations: Guidance.md Considerations item 2)
- Piping isometrics (requirements: Specification.md FR-7; description: Datasheet.md Construction - Piping isometrics; considerations: Guidance.md Considerations item 2)
- Pipe support drawings (requirements: Specification.md FR-8; description: Datasheet.md Construction - Pipe support drawings; rationale: Guidance.md Principles item 4)
- Phase 2 connection details (requirements: Specification.md FR-9; description: Datasheet.md Construction - Phase 2 connection details; rationale: Guidance.md Principles item 5)

## Prerequisites

**Dependencies:**

Per `_DEPENDENCIES.md`: **NOT_TRACKED** — Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`).

**Upstream inputs required** (typical for process piping design; rationale: Guidance.md Principles item 2 - System integration):
- Process Flow Diagrams (PFDs) or preliminary process design — **TBD** source (requirements: Specification.md FR-1, FR-2)
- Equipment layout and nozzle data (requirements: Specification.md IR-4 through IR-11; systems: Datasheet.md Key piping systems) — cross-reference PKG-10 (Railcar Unloading), PKG-11 (Marine Loading), PKG-13 (Storage Tanks), PKG-15 (Pumps), PKG-16 (Valves)
- Design basis data (flow rates, temperatures, pressures, product properties) (requirements: Specification.md PR-2, PR-3, PR-4; conditions: Datasheet.md Conditions; **TBD** — location TBD: ER Volume 2 Part 2 or process design basis memo)
- Site survey and existing conditions information — **TBD** (considerations: Guidance.md Considerations item 4)
- Structural design information (steel framing, concrete foundations) (requirements: Specification.md IR-2; coordination: Guidance.md Considerations item 1) — cross-reference PKG-05 (Concrete Structures), PKG-06 (Structural Steelwork)
- Hazardous area classification study (conditions: Datasheet.md Hazardous area classification; considerations: Guidance.md Considerations item 6; **TBD** — location TBD: ER Volume 2 Part 2)

**Reference materials:**

Per `_REFERENCES.md`:
- Employer's Requirements Volume 2 Part 1 — General Requirements (location: test/Volume_2_Part_1_Employers_Requirements.pdf; requirements: Specification.md Standards - Project-specific requirements; examples: Guidance.md Examples item 1)
- Employer's Requirements Volume 2 Part 2 — Civil & Process Mechanical Works (location: test/Volume_2_Part_2_Employers_Requirements.pdf; requirements: Specification.md Standards - Project-specific requirements; examples: Guidance.md Examples item 1)
- Decomposition file (location: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md)

**Applicable codes and standards:**
- ASME B31.3 — Process Piping (code: Datasheet.md Design Code; requirements: Specification.md PR-5, Standards - Process piping design; rationale: Guidance.md Principles item 1; examples: Guidance.md Examples item 5)
- **TBD** — Additional codes per Specification.md Standards section and ER Volume 2 Part 2
- **TBD** — Project CAD standards and drawing conventions (requirements: Specification.md QR-1; attributes: Datasheet.md CAD Standard; considerations: Guidance.md Considerations item 2; location TBD: project CAD management plan)
- **TBD** — Project quality procedures (requirements: Specification.md QR-4; examples: Guidance.md Examples item 1; location TBD: project Quality Management Plan)

**Personnel requirements:**
- **Lead Designer:** Professional Engineer (P.Eng.) or Mechanical Engineer with process piping design experience — **TBD** specific qualifications (requirements: Specification.md QR-4)
- **CAD Technician/Designer:** Proficient in project CAD platform (e.g., AutoCAD Plant 3D, PDMS, or equivalent) (attributes: Datasheet.md CAD Software; requirements: Specification.md QR-1; considerations: Guidance.md Considerations item 2; **TBD** software platform)
- **Checker:** Independent checker qualified in process piping design (P.Eng. or equivalent) (requirements: Specification.md QR-4; verification: Specification.md Verification - Independent check; **TBD** checker qualifications)
- **Approver:** Discipline Lead or Project Engineer (requirements: Specification.md QR-4; **TBD** approval authority matrix)
- **ASSUMPTION**: Personnel competency requirements per project quality procedures

**Tools and software:**
- CAD software (attributes: Datasheet.md CAD Software; requirements: Specification.md QR-1; considerations: Guidance.md Considerations item 2; **TBD** — location TBD: project CAD management plan) — **ASSUMPTION**: AutoCAD Plant 3D, PDMS, SmartPlant, or similar 3D piping design platform
- Piping stress analysis software (e.g., CAESAR II, AutoPIPE) — for flexibility analysis per ASME B31.3 (requirements: Specification.md PR-5, QR-5; rationale: Guidance.md Principles item 1; cross-reference DEL-14.03)
- **TBD** — Clash detection software for interdisciplinary coordination (requirements: Specification.md IR-1, QR-3; trade-offs: Guidance.md Trade-offs item 3)
- **TBD** — Document management system for revision control and issuance (attributes: Datasheet.md Revision Control; requirements: Specification.md QR-2)

## Steps

### Step 1: Design Basis and Input Data Collection

**Objective:** Establish design basis and collect required input data (requirements: Specification.md FR-1, PR-4; rationale: Guidance.md Principles item 1; verification: Specification.md Verification - Design review).

**Actions:**
1. Review Employer's Requirements Volume 2 Part 2 for process piping design requirements (location: test/Volume_2_Part_2_Employers_Requirements.pdf; requirements: Specification.md Standards - Project-specific requirements; examples: Guidance.md Examples item 1; **TBD** extract relevant clauses)
2. Review decomposition and project objectives (OBJ-2 Throughput, OBJ-4 Flexibility, OBJ-8 Expandability) (requirements: Specification.md FR-1, FR-2, FR-3; rationale: Guidance.md Purpose - Project context)
3. Obtain or develop process design basis:
   - Flow rates for railcar unloading, marine loading, recycle, nitrogen distribution (requirements: Specification.md PR-4; conditions: Datasheet.md Flow rates; systems: Datasheet.md Key piping systems; **TBD** source)
   - Operating temperatures and pressures (requirements: Specification.md PR-2, PR-3; conditions: Datasheet.md Conditions; **TBD** source)
   - Product properties (density, viscosity, vapor pressure) for CSD canola oil (requirements: Specification.md PR-1; product: Datasheet.md Product Handled; rationale: Guidance.md Principles item 3; **TBD** source)
4. Collect equipment data:
   - Pump nozzle sizes, ratings, orientations (PKG-15) (requirements: Specification.md IR-4, IR-5; examples: Guidance.md Examples item 4; **TBD** timing)
   - Tank nozzle locations and sizes (PKG-13) (requirements: Specification.md IR-6; systems: Datasheet.md Tank farm piping connections; examples: Guidance.md Examples item 4; **TBD** timing)
   - Railcar unloading system interface data (PKG-10) (requirements: Specification.md IR-9; systems: Datasheet.md Railcar unloading headers; examples: Guidance.md Examples item 4; **TBD** timing)
   - Marine loading system interface data (PKG-11) (requirements: Specification.md IR-10; systems: Datasheet.md Marine loading export lines; examples: Guidance.md Examples item 4; **TBD** timing)
   - Valve and specialty equipment data (PKG-16) (requirements: Specification.md IR-7; **TBD** timing)
5. Obtain site information:
   - Site survey (elevations, existing utilities, obstructions) (considerations: Guidance.md Considerations item 4; **TBD**)
   - Structural design (steel framing, concrete foundations) (requirements: Specification.md IR-2; rationale: Guidance.md Principles item 4) — cross-reference PKG-05, PKG-06
6. Review nitrogen skid interface requirements (Employer-supplied; Contractor connects per Decision DEC-07) (requirements: Specification.md IR-8; systems: Datasheet.md Nitrogen distribution piping; considerations: Guidance.md Considerations item 1; **TBD** Employer interface drawing or data)

**Verification:** Design basis memo or input data register reviewed and approved (verification: Specification.md Verification - Design review; **TBD**).

---

### Step 2: P&ID Development

**Objective:** Develop Process and Instrumentation Diagrams (P&IDs) (requirements: Specification.md FR-5; description: Datasheet.md Construction - P&IDs; considerations: Guidance.md Considerations item 2 - P&IDs).

**Actions:**
1. Establish P&ID symbology standard (requirements: Specification.md Standards - Drawing standards; considerations: Guidance.md Considerations item 2 - P&IDs; **TBD** — location TBD: project CAD standards) — **ASSUMPTION**: ISA 5.1 or equivalent
2. Develop preliminary P&IDs showing:
   - Process flow from railcar unloading through storage to marine loading (requirements: Specification.md FR-1, FR-2; systems: Datasheet.md Key piping systems; rationale: Guidance.md Principles item 2)
   - Equipment (pumps, tanks, valves, specialty equipment) (requirements: Specification.md IR-4 through IR-7)
   - Piping (headers, export lines, recycle lines, nitrogen distribution) (scope: Specification.md Scope; systems: Datasheet.md Key piping systems)
   - Instrumentation (flow, pressure, temperature, level) (requirements: Specification.md FR-5, IR-3)
   - Control logic and safety systems (requirements: Specification.md FR-5)
   - Phase 2 expansion connection points (requirements: Specification.md FR-3, FR-9; rationale: Guidance.md Principles item 5)
3. Coordinate P&IDs with control system design (PKG-19) (requirements: Specification.md IR-3; considerations: Guidance.md Considerations item 1; **TBD** coordination procedure)
4. Conduct P&ID review with process, mechanical, instrumentation, and operations disciplines (verification: Specification.md Verification - Design review; **TBD** review meeting)
5. Incorporate review comments and issue P&IDs for design development

**Verification:**
- P&IDs reviewed by process engineer, mechanical lead, instrumentation lead (verification: Specification.md Verification - Design review; **TBD** sign-off)
- P&IDs checked for consistency with design basis and equipment data (verification: Specification.md Verification - Technical verification)

---

### Step 3: Piping General Arrangement (GA) Development

**Objective:** Develop piping routing and spatial arrangement in 3D (requirements: Specification.md FR-6; description: Datasheet.md Construction - Piping GAs; considerations: Guidance.md Considerations item 2 - Piping GAs).

**Actions:**
1. Set up 3D CAD model with:
   - Site boundaries and existing conditions (data from Step 1)
   - Structural steel and concrete foundations (requirements: Specification.md IR-2; rationale: Guidance.md Principles item 4) — coordinate with PKG-05, PKG-06
   - Equipment models (pumps, tanks, valves) from vendor data or preliminary layouts (requirements: Specification.md IR-4 through IR-7)
   - Electrical raceways and instrumentation cable trays (requirements: Specification.md IR-1) — coordinate with PKG-17, PKG-18, PKG-19
2. Route process piping in 3D model:
   - Follow P&IDs for connectivity and flow paths (from Step 2)
   - Apply piping design standards (minimum slope for drainage, maximum spans per ASME B31.3, clearances for maintenance) (code: Datasheet.md Design Code; requirements: Specification.md PR-5; rationale: Guidance.md Principles item 1; constraints: Datasheet.md Construction constraints - Access for maintenance)
   - Consider thermal expansion requirements (loops, expansion joints, or flexibility per DEL-14.03 analysis) (requirements: Specification.md PR-7; conditions: Datasheet.md Operating temperature range; rationale: Guidance.md Principles item 4; trade-offs: Guidance.md Trade-offs item 2)
   - Locate isolation valves, drain valves, vent valves per operational philosophy (rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations item 5)
3. Conduct 3D coordination (clash detection) with structural, electrical, instrumentation disciplines (requirements: Specification.md IR-1, QR-3; considerations: Guidance.md Considerations item 2; trade-offs: Guidance.md Trade-offs item 3; **TBD** coordination procedure and software)
4. Resolve clashes and optimize piping routing for constructability and maintainability (requirements: Specification.md FR-4; considerations: Guidance.md Considerations item 4, item 5; constraints: Datasheet.md Construction constraints)
5. Generate piping GA drawings (plan and elevation views) from 3D model (attributes: Datasheet.md Drawing Types, Scale)
6. Add dimensions, annotations, references to isometrics, and Phase 2 connection callouts (requirements: Specification.md FR-9; rationale: Guidance.md Principles item 5)

**Verification:**
- 3D model reviewed for clashes (target: zero unresolved clashes at time of GA issuance) (requirements: Specification.md QR-3; verification: Specification.md Verification - Technical verification)
- GAs checked for dimensional accuracy and consistency with 3D model (verification: Specification.md Verification - Technical verification)
- Interdisciplinary check (IDC) completed with affected disciplines (requirements: Specification.md QR-3; verification: Specification.md Verification - IDC; **TBD** IDC sign-off)

---

### Step 4: Piping Isometric Development

**Objective:** Develop fabrication-ready piping isometric drawings (requirements: Specification.md FR-7; description: Datasheet.md Construction - Piping isometrics; considerations: Guidance.md Considerations item 2 - Piping isometrics).

**Actions:**
1. Extract piping isometrics from 3D model (or develop manually if 3D model not used) (from Step 3 GA development)
2. Add fabrication information to each isometric:
   - Pipe size, schedule, material specification (materials: Datasheet.md Piping sizes, Materials; requirements: Specification.md Standards - Materials and corrosion; cross-reference DEL-14.04 line list)
   - Weld locations and weld symbols (requirements: Specification.md FR-7)
   - Fitting types (elbows, tees, reducers, flanges) (requirements: Specification.md FR-7)
   - Valve types and tag numbers (requirements: Specification.md IR-7)
   - Support locations and tag numbers (requirements: Specification.md FR-8; rationale: Guidance.md Principles item 4) — cross-reference pipe support drawings (Step 5)
   - Dimensions (spool lengths, overall dimensions, critical field dimensions) (attributes: Datasheet.md Scale; requirements: Specification.md FR-7)
   - Bill of materials (BOM) for each isometric (requirements: Specification.md FR-7)
3. Assign isometric drawing numbers per project numbering system (attributes: Datasheet.md Drawing Number Prefix; requirements: Specification.md QR-2; **TBD**)
4. Review isometrics for fabrication clarity and completeness (verification: Specification.md Verification - Technical verification)
5. Issue isometrics for fabrication and installation (documentation: Specification.md Documentation - Drawing types)

**Verification:**
- Isometrics checked for dimensional accuracy and material callouts (verification: Specification.md Verification - Technical verification)
- Isometrics verified against 3D model and piping GAs (verification: Specification.md Verification - Technical verification)
- Fabrication review (if applicable) (verification: Specification.md Verification - Design review; **TBD**)

---

### Step 5: Pipe Support Drawing Development

**Objective:** Develop pipe support detail drawings and schedules (requirements: Specification.md FR-8; description: Datasheet.md Construction - Pipe support drawings; rationale: Guidance.md Principles item 4; considerations: Guidance.md Considerations item 2 - Pipe support drawings).

**Actions:**
1. Identify support locations from 3D model or piping stress analysis (DEL-14.03) (from Step 3; requirements: Specification.md QR-6; cross-reference DEL-14.03)
2. Determine support types:
   - Rigid supports (hangers, shoes, saddles) (rationale: Guidance.md Principles item 4)
   - Spring hangers (for thermal expansion accommodation) (requirements: Specification.md PR-7; conditions: Datasheet.md Operating temperature range; rationale: Guidance.md Principles item 4; trade-offs: Guidance.md Trade-offs item 2)
   - Anchors, guides, restraints (for seismic and operational loads) (requirements: Specification.md PR-6; conditions: Datasheet.md Seismic requirements; rationale: Guidance.md Principles item 4)
3. Design support details:
   - Support configuration and dimensions (requirements: Specification.md FR-8)
   - Structural attachment details (embed plates, beam clamps, etc.) (requirements: Specification.md IR-2)
   - Support loads (vertical, lateral, seismic) from stress analysis (DEL-14.03) (requirements: Specification.md QR-6; cross-reference DEL-14.03)
4. Coordinate support attachment points with structural discipline (PKG-05, PKG-06) (requirements: Specification.md IR-2; rationale: Guidance.md Principles item 4; considerations: Guidance.md Considerations item 1)
5. Develop standard support details and project-specific details as required (requirements: Specification.md Standards - Piping supports; considerations: Guidance.md Considerations item 2 - Pipe support drawings; **TBD** standardization)
6. Create pipe support schedule listing all supports with type, location, loads, and drawing references (requirements: Specification.md FR-8; documentation: Specification.md Documentation - Pipe support drawings)

**Verification:**
- Support loads verified by piping stress analysis (DEL-14.03) (requirements: Specification.md QR-6; verification: Specification.md Verification - Support load verification)
- Support attachment points coordinated and approved by structural discipline (requirements: Specification.md IR-2; verification: Specification.md Verification - IDC)
- Support details checked for constructability and code compliance (code: Datasheet.md Design Code; requirements: Specification.md PR-6; verification: Specification.md Verification - Standards compliance)

---

### Step 6: Phase 2 Connection Details

**Objective:** Define interface provisions for future Phase 2 expansion (requirements: Specification.md FR-3, FR-9; description: Datasheet.md Construction - Phase 2 connection details; rationale: Guidance.md Principles item 5; considerations: Guidance.md Considerations item 2 - Phase 2 connection details).

**Actions:**
1. Review Phase 2 expansion requirements (source: OBJ-8; requirements: Specification.md FR-3; considerations: Guidance.md Considerations item 2 - Phase 2 connection details; **TBD** — location TBD: ER Volume 2 Part 2)
2. Identify Phase 2 connection points on P&IDs and piping GAs (from Step 2 and Step 3; requirements: Specification.md FR-9)
3. Develop connection details:
   - Stub-outs with capped or flanged ends (requirements: Specification.md FR-9; rationale: Guidance.md Principles item 5)
   - Oversized headers with future tie-in points (requirements: Specification.md FR-3; rationale: Guidance.md Principles item 5)
   - Flanged connections for future equipment (requirements: Specification.md FR-9)
4. Label Phase 2 connections clearly on all drawings (P&IDs, GAs, isometrics) (requirements: Specification.md FR-9; documentation: Specification.md Documentation - Phase 2 connection details)
5. Document Phase 2 interface requirements in design basis memo or separate interface control document (documentation: Specification.md Documentation - Supporting documentation; **TBD**)

**Verification:**
- Phase 2 connection details reviewed for adequacy and flexibility (requirements: Specification.md FR-3; verification: Specification.md Verification - Design review)
- Phase 2 provisions coordinated with related disciplines (structural for future loads, electrical for future power, etc.) (requirements: Specification.md IR-1, IR-2; verification: Specification.md Verification - IDC)

---

### Step 7: Design Self-Check

**Objective:** Originator reviews drawings for completeness and accuracy (requirements: Specification.md QR-4; verification: Specification.md Verification - Design self-check).

**Actions:**
1. Check all drawings for:
   - Completeness (all required views, details, dimensions, notes) (requirements: Specification.md FR-5 through FR-9)
   - Accuracy (dimensions, material callouts, references) (verification: Specification.md Verification - Dimensional verification)
   - Consistency (P&IDs ↔ GAs ↔ isometrics ↔ support drawings) (scope: Specification.md Scope; outputs from Steps 2-6)
   - Code compliance (ASME B31.3 requirements) (code: Datasheet.md Design Code; requirements: Specification.md PR-5; verification: Specification.md Verification - Standards compliance)
   - ER compliance (Employer's Requirements) (requirements: Specification.md Standards - Project-specific requirements; from Step 1)
2. Verify cross-references between drawings and related deliverables (DEL-14.02, DEL-14.03, DEL-14.04) (cross-references: Datasheet.md References; requirements: Specification.md Standards section; examples: Guidance.md Examples item 4)
3. Check drawing format, title blocks, revision control per project standards (attributes: Datasheet.md Drawing Number Prefix, Revision Control, Sheet Size, Scale; requirements: Specification.md QR-1, QR-2; verification: Specification.md Verification - Standards compliance; **TBD**)
4. Resolve self-check findings and update drawings

**Verification:**
- Originator sign-off on self-check completion (requirements: Specification.md QR-4; verification: Specification.md Verification - Design self-check; **TBD** sign-off procedure)

---

### Step 8: Interdisciplinary Check (IDC)

**Objective:** Coordinate piping design with affected disciplines and resolve conflicts (requirements: Specification.md QR-3, IR-1, IR-2, IR-3; verification: Specification.md Verification - IDC; considerations: Guidance.md Considerations item 1; trade-offs: Guidance.md Trade-offs item 3).

**Actions:**
1. Distribute drawings to affected disciplines:
   - Structural (PKG-05, PKG-06) — for pipe support loads and attachment points (requirements: Specification.md IR-2; from Step 5)
   - Electrical (PKG-17, PKG-18) — for spatial coordination of raceways and piping (requirements: Specification.md IR-1; from Step 3)
   - Instrumentation & Control (PKG-19) — for instrument locations and cable routing (requirements: Specification.md IR-3; from Step 2)
   - Process/Equipment packages (PKG-10, PKG-11, PKG-12, PKG-13, PKG-15, PKG-16) — for interface verification (requirements: Specification.md IR-4 through IR-11; systems: Datasheet.md Key piping systems)
2. Conduct IDC review meeting or distribute for written comments (requirements: Specification.md QR-3; **TBD** IDC procedure)
3. Collect IDC comments and categorize (conflicts, suggestions, information)
4. Resolve conflicts through coordination and model updates (from Step 3)
5. Incorporate valid comments and update drawings (update Steps 2-6 outputs as needed)
6. Issue IDC closeout report confirming all comments addressed (verification: Specification.md Verification - IDC)

**Verification:**
- IDC sign-off from all affected disciplines (requirements: Specification.md QR-3; verification: Specification.md Verification - IDC; **TBD** sign-off matrix)
- All conflicts resolved or escalated to project management for ruling (verification: Specification.md Verification - Acceptance criteria)

---

### Step 9: Independent Check

**Objective:** Peer review by qualified independent checker (requirements: Specification.md QR-4; verification: Specification.md Verification - Independent check).

**Actions:**
1. Assign independent checker (qualified in process piping design, not involved in original design) (personnel requirements: Prerequisites section; **TBD** checker assignment)
2. Checker reviews drawings for:
   - Technical correctness (design calculations, code compliance) (code: Datasheet.md Design Code; requirements: Specification.md PR-5; rationale: Guidance.md Principles item 1)
   - Completeness (all required information present) (requirements: Specification.md FR-5 through FR-9)
   - Constructability (can be built as shown) (requirements: Specification.md FR-4; considerations: Guidance.md Considerations item 4; constraints: Datasheet.md Construction constraints)
   - Consistency (internal consistency and consistency with other deliverables) (cross-references: Datasheet.md References; examples: Guidance.md Examples item 4)
   - ER compliance (requirements: Specification.md Standards - Project-specific requirements; from Step 1)
3. Checker issues check comments (typically in red markup or comment log)
4. Originator reviews check comments, resolves issues, updates drawings
5. Checker verifies comment resolution and signs off (requirements: Specification.md QR-4)

**Verification:**
- Checker sign-off confirming review complete and comments resolved (verification: Specification.md Verification - Independent check; **TBD** sign-off procedure)

---

### Step 10: Design Verification (Calculations)

**Objective:** Verify piping design by calculations (requirements: Specification.md QR-5, QR-6, QR-7; verification: Specification.md Verification - Technical verification; rationale: Guidance.md Principles item 1, item 4).

**Actions:**
1. Perform piping stress analysis (flexibility analysis) for critical lines per ASME B31.3 (code: Datasheet.md Design Code; requirements: Specification.md PR-5, QR-5; rationale: Guidance.md Principles item 1; trade-offs: Guidance.md Trade-offs item 2; examples: Guidance.md Examples item 5) — cross-reference DEL-14.03 (Process Piping Design Calculations)
2. Verify pipe support loads and spacing (requirements: Specification.md PR-6, QR-6; rationale: Guidance.md Principles item 4; from Step 5) — cross-reference DEL-14.03
3. Perform transient analysis (surge analysis) for railcar unloading and marine loading lines (requirements: Specification.md QR-7; systems: Datasheet.md Railcar unloading headers, Marine loading export lines; trade-offs: Guidance.md Trade-offs item 5; examples: Guidance.md Examples item 4) — cross-reference DEL-14.06 (Transient Analysis — Railcar Unloading), DEL-14.07 (Transient Analysis — Marine Loading)
4. Verify valve closing times per surge mitigation requirements (requirements: Specification.md QR-7) — cross-reference DEL-14.08 (Valve Closing Time Verification)
5. Update drawings to reflect calculation results (support locations, expansion loops, surge mitigation devices) (update Steps 3, 4, 5 outputs as needed)
6. Obtain calculation approval prior to final drawing approval (verification: Specification.md Verification - Acceptance criteria)

**Verification:**
- All required calculations (stress, support, transient) completed and approved (requirements: Specification.md QR-5, QR-6, QR-7; verification: Specification.md Verification - Acceptance criteria)
- Drawings consistent with calculation results (verification: Specification.md Verification - Technical verification)

---

### Step 11: Approval and Issuance

**Objective:** Discipline lead approves drawings for issue (requirements: Specification.md QR-4; documentation: Specification.md Documentation section; trade-offs: Guidance.md Trade-offs item 6).

**Actions:**
1. Compile drawing package:
   - P&IDs (from Step 2)
   - Piping GAs (from Step 3)
   - Piping isometrics (from Step 4)
   - Pipe support drawings (from Step 5)
   - Phase 2 connection details (from Step 6)
   - Drawing index (list of all drawings) (documentation: Specification.md Documentation - Drawing index)
   - Supporting calculations (or reference to DEL-14.03, DEL-14.06, DEL-14.07, DEL-14.08) (documentation: Specification.md Documentation - Design basis memo)
2. Discipline lead reviews package for overall consistency and completeness (requirements: Specification.md QR-4; verification: Specification.md Verification - Acceptance criteria)
3. Approver signs title blocks (or electronic approval per project procedures) (personnel requirements: Prerequisites section; requirements: Specification.md QR-4; attributes: Datasheet.md Revision Control; **TBD** approval workflow)
4. Issue drawings per project document control procedures:
   - For internal review (e.g., "IFR" — Issued for Review) (documentation: Specification.md Documentation - Storage location; **TBD** issuance code)
   - For Employer review (e.g., "IFA" — Issued for Approval) (documentation: Specification.md Documentation - Submittal requirements; **TBD** issuance code and submittal procedure)
   - For construction (e.g., "IFC" — Issued for Construction) (attributes: Datasheet.md Classification; **TBD** issuance code)
5. Place issued copies in `3_Issued/` folder with revision control (documentation: Specification.md Documentation - Storage location; attributes: Datasheet.md Revision Control)
6. Update drawing register and transmittal log (requirements: Specification.md QR-2; **TBD** project document control system)

**Verification:**
- Approver sign-off confirming package ready for issue (verification: Specification.md Verification - Acceptance criteria; **TBD** sign-off)
- Issuance code and revision control correct per project procedures (requirements: Specification.md QR-2; attributes: Datasheet.md Revision Control)

---

### Step 12: As-Built Documentation (Post-Construction)

**Objective:** Update drawings to reflect as-built conditions (documentation: Specification.md Documentation - As-built documentation).

**Actions:**
1. Collect as-built markup during construction (field changes, RFIs, change orders) (documentation: Specification.md Documentation - As-built documentation; **TBD** as-built markup procedure)
2. Incorporate as-built changes into drawings (red-line or model updates) (from Step 3 3D model)
3. Issue final as-built drawings (e.g., "ABD" — As-Built Drawing) (documentation: Specification.md Documentation - As-built documentation; **TBD** issuance code)
4. Archive as-built drawings and deliver to Employer per contract requirements (documentation: Specification.md Documentation - As-built documentation; **TBD** deliverable requirements — location TBD: ER Volume 2 Part 1)

**Verification:**
- As-built drawings verified against field conditions (site walk-down or photo verification) (verification: Specification.md Verification - Acceptance criteria)
- As-built package reviewed and approved prior to final delivery (requirements: Specification.md QR-4)

---

## Verification

**Verification activities summary:**

| Step | Verification Method | Acceptance Criteria |
|------|---------------------|---------------------|
| 1. Design Basis | Review and approval of design basis memo | All input data confirmed and approved (requirements: Specification.md FR-1, PR-4) |
| 2. P&ID Development | Multi-discipline review | P&IDs complete, consistent, and approved by process/mechanical/instrumentation leads (requirements: Specification.md FR-5; verification: Specification.md Verification - Design review) |
| 3. Piping GA Development | 3D clash detection, IDC | Zero unresolved clashes; IDC sign-off from all disciplines (requirements: Specification.md QR-3; verification: Specification.md Verification - IDC) |
| 4. Piping Isometric Development | Dimensional check, material verification | Isometrics match 3D model and GAs; material callouts correct (requirements: Specification.md FR-7; verification: Specification.md Verification - Technical verification) |
| 5. Pipe Support Development | Load verification (DEL-14.03), structural coordination | Support loads confirmed by stress analysis; attachment points approved by structural (requirements: Specification.md QR-6, IR-2; verification: Specification.md Verification - Support load verification) |
| 6. Phase 2 Connection Details | Interface review | Phase 2 provisions adequate for anticipated expansion (requirements: Specification.md FR-9; verification: Specification.md Verification - Design review) |
| 7. Design Self-Check | Originator review | Self-check complete; no outstanding issues (requirements: Specification.md QR-4; verification: Specification.md Verification - Design self-check) |
| 8. Interdisciplinary Check (IDC) | Multi-discipline review | All IDC comments addressed and closed (requirements: Specification.md QR-3; verification: Specification.md Verification - IDC) |
| 9. Independent Check | Peer review by qualified checker | Checker sign-off; all check comments resolved (requirements: Specification.md QR-4; verification: Specification.md Verification - Independent check) |
| 10. Design Verification (Calculations) | Stress analysis, transient analysis | Calculations approved; drawings consistent with results (requirements: Specification.md QR-5, QR-6, QR-7; verification: Specification.md Verification - Technical verification) |
| 11. Approval and Issuance | Discipline lead approval | Package complete and approved for issue (requirements: Specification.md QR-4; verification: Specification.md Verification - Acceptance criteria) |
| 12. As-Built Documentation | Field verification | As-built drawings match field conditions (documentation: Specification.md Documentation - As-built documentation) |

**Overall acceptance criteria:**
- All drawings reviewed, checked, and approved with no outstanding comments or holds (requirements: Specification.md QR-4; verification: Specification.md Verification - Acceptance criteria)
- All interdisciplinary coordination issues resolved (requirements: Specification.md QR-3; verification: Specification.md Verification - IDC)
- All calculations (stress, support, transient) completed and approved (requirements: Specification.md QR-5, QR-6, QR-7; verification: Specification.md Verification - Acceptance criteria)
- Drawings comply with ASME B31.3, project standards, and Employer's Requirements (code: Datasheet.md Design Code; requirements: Specification.md PR-5, Standards section; verification: Specification.md Verification - Standards compliance)
- **TBD** — Additional acceptance criteria per project quality procedures (location TBD; requirements: Specification.md QR-4)

---

## Records

**Documentation outputs** (source: Decomposition DEL-14.01; scope: Specification.md Scope; documentation: Specification.md Documentation section):

**Drawing types:**
- P&IDs (Process and Instrumentation Diagrams) (requirements: Specification.md FR-5; description: Datasheet.md Construction - P&IDs; Step 2)
- Piping GAs (General Arrangement drawings — plan and elevation views) (requirements: Specification.md FR-6; description: Datasheet.md Construction - Piping GAs; Step 3)
- Piping isometrics (fabrication drawings) (requirements: Specification.md FR-7; description: Datasheet.md Construction - Piping isometrics; Step 4)
- Pipe support drawings (support details and schedules) (requirements: Specification.md FR-8; description: Datasheet.md Construction - Pipe support drawings; Step 5)
- Phase 2 connection details (expansion interface drawings) (requirements: Specification.md FR-9; description: Datasheet.md Construction - Phase 2 connection details; Step 6)

**Supporting records:**
- Drawing index (list of all drawings in the set) (documentation: Specification.md Documentation - Drawing index; Step 11)
- Design basis memo or input data register (documentation: Specification.md Documentation - Design basis memo; Step 1; Verification table)
- Interdisciplinary check (IDC) records (comments, responses, sign-offs) (requirements: Specification.md QR-3; documentation: Specification.md Documentation - IDC records; Step 8; Verification table)
- Design review records (self-check, independent check, approval) (requirements: Specification.md QR-4; documentation: Specification.md Documentation - Design review records; Steps 7, 9, 11; Verification table)
- Comment resolution log (documentation: Specification.md Documentation - Comment resolution log; Steps 7, 8, 9)
- Drawing revision history (attributes: Datasheet.md Revision Control; requirements: Specification.md QR-2; Step 11)
- Calculation summary or references to DEL-14.03, DEL-14.06, DEL-14.07, DEL-14.08 (documentation: Specification.md Documentation - Design basis memo; Step 10; Verification table)
- As-built markup and final as-built drawings (post-construction) (documentation: Specification.md Documentation - As-built documentation; Step 12)

**Record management:**

**Storage locations:**
- Working files: `1_Working/DEL-14.01_Process_Piping_Design_Drawing_Set/` (working CAD files and drafts) (documentation: Specification.md Documentation - Storage location)
- Review copies: `2_Checking/To/` (drawings issued for review) (documentation: Specification.md Documentation - Storage location)
- Issued copies: `3_Issued/` (approved drawings with revision control) (documentation: Specification.md Documentation - Storage location; attributes: Datasheet.md Revision Control)

**Electronic format:**
- **TBD** — Native CAD format (e.g., .dwg, .dgn) for working files (attributes: Datasheet.md CAD Software; requirements: Specification.md QR-1; location TBD: project CAD management plan)
- **ASSUMPTION**: PDF for issued drawings and submittals (documentation: Specification.md Documentation - Electronic format)
- **TBD** — Document management system (DMS) for controlled issuance and revision tracking (attributes: Datasheet.md Revision Control; requirements: Specification.md QR-2)

**Retention requirements:**
- **TBD** — Drawing retention period per contract or regulatory requirements (location TBD: ER Volume 2 Part 1; documentation: Specification.md Documentation - Submittal requirements)
- **ASSUMPTION**: Permanent retention for as-built drawings (project record)

**Submittal and delivery:**
- **TBD** — Submittal schedule and approval workflow (location TBD: ER Volume 2 Part 1; documentation: Specification.md Documentation - Submittal requirements; Step 11)
- **TBD** — Final deliverable format and quantity (hard copy, electronic, both) (location TBD: ER Volume 2 Part 1; documentation: Specification.md Documentation - Electronic format)
- **TBD** — Delivery to Employer document control system or archive (Step 12)
