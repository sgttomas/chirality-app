# Specification: DEL-14.01 Process Piping Design Drawing Set

## Scope

This specification defines the requirements for **Process Piping Design Drawing Set** within **PKG-14 Process Piping**.

**Description:** Defines the design arrangement and details for process piping per ER requirements (source: Decomposition DEL-14.01; rationale: Guidance.md Purpose section).

**Piping systems covered** (source: Decomposition PKG-14 Scope; attributes: Datasheet.md Attributes; system integration: Guidance.md Principles item 2):
- Railcar unloading headers
- Marine loading export lines
- Product recycle lines
- Nitrogen distribution piping
- Tank farm piping connections
- All associated pipe supports

**Drawing deliverables** (source: Decomposition DEL-14.01; attributes: Datasheet.md Attributes; production procedures: Procedure.md Steps 2-6):
- P&IDs (Process and Instrumentation Diagrams)
- Piping GAs (General Arrangement drawings)
- Piping isometrics
- Pipe support drawings
- Phase 2 connection details

**Exclusions:**
- Nitrogen skid internal piping (supplied by Employer per Decision DEC-07; Contractor scope limited to connection piping — interface requirements: IR-8; coordination: Procedure.md Step 1; considerations: Guidance.md Considerations item 1)
- Employer-responsible items except for interface connections (source: Decomposition Section 1.2)

## Requirements

### Functional Requirements

**Design intent** (source: Decomposition Section 2; rationale: Guidance.md Principles items 1-2; verification: Procedure.md Steps 1, 10):
- FR-1: Drawings shall define piping systems to support throughput capacity of 1,000,000 MT per annum (OBJ-2) (attributes: Datasheet.md Design Throughput; sizing: Procedure.md Step 1; rationale: Guidance.md Principles item 1)
- FR-2: Drawings shall support operational flexibility for both tank storage operations and direct rail-to-ship transfer (OBJ-4) (rationale: Guidance.md Principles item 2; P&ID development: Procedure.md Step 2)
- FR-3: Drawings shall include provisions for Phase 2 expansion connections with minimal disruption (OBJ-8) (details: Datasheet.md Phase 2 connection details; rationale: Guidance.md Principles item 5; procedure: Procedure.md Step 6)
- FR-4: Piping layout shall minimize disturbance to existing Terminal commercial activities during construction (OBJ-5) (considerations: Guidance.md Considerations item 4; routing: Procedure.md Step 3)

**Drawing content requirements** (detailed in: Guidance.md Considerations item 2; production: Procedure.md Steps 2-6):
- FR-5: P&IDs shall show all process piping, equipment connections, instrumentation, control schemes, and safety devices (description: Datasheet.md Construction - P&IDs; procedure: Procedure.md Step 2; rationale: Guidance.md Considerations item 2; **TBD** detail requirements — location TBD: ER Volume 2 Part 2)
- FR-6: Piping GAs shall show piping routing in plan and elevation with spatial coordination across disciplines (description: Datasheet.md Construction - Piping GAs; procedure: Procedure.md Step 3; coordination: IR-1, IR-2; rationale: Guidance.md Considerations item 2; **TBD** coordination requirements)
- FR-7: Piping isometrics shall provide fabrication-ready single-line drawings with dimensions, welds, fittings, and material callouts (description: Datasheet.md Construction - Piping isometrics; procedure: Procedure.md Step 4; rationale: Guidance.md Considerations item 2; **TBD** fabrication drawing standards)
- FR-8: Pipe support drawings shall define support locations, types, loads, and attachment details (description: Datasheet.md Construction - Pipe support drawings; procedure: Procedure.md Step 5; rationale: Guidance.md Principles item 4; load verification: QR-6; **TBD** support design requirements — location TBD: ER Volume 2 Part 2)
- FR-9: Phase 2 connection details shall show stub-outs, flanges, or capped connections for future expansion (description: Datasheet.md Construction - Phase 2 connection details; procedure: Procedure.md Step 6; rationale: Guidance.md Principles item 5; **TBD** expansion interface requirements)

### Performance Requirements

**Product handling** (source: Decomposition Section 1.1; attributes: Datasheet.md Conditions; rationale: Guidance.md Principles item 3):
- PR-1: Piping systems shall be suitable for CSD (Crude Super Degummed) canola oil service (product: Datasheet.md Attributes; material selection: Guidance.md Principles item 3, Trade-offs item 1; specifications: Standards section - Materials and corrosion)
- PR-2: Design shall accommodate operating temperature range (conditions: Datasheet.md Conditions; thermal expansion: PR-7; rationale: Guidance.md Trade-offs item 2; **TBD** — location TBD: ER Volume 2 Part 2)
- PR-3: Design shall accommodate operating pressure range (conditions: Datasheet.md Conditions; design code: Datasheet.md Design Code; verification: Procedure.md Step 10; **TBD** varies by system — location TBD: ER Volume 2 Part 2)
- PR-4: Piping sizing shall support flow rates required for 1,000,000 MT/annum throughput (conditions: Datasheet.md Flow rates; calculation: cross-reference DEL-14.03; procedure: Procedure.md Step 1; rationale: Guidance.md Principles item 1; **TBD** flow requirements to be confirmed per DEL-14.03 calculations)

**Design criteria** (rationale: Guidance.md Principles item 4; verification: Procedure.md Step 10):
- PR-5: Piping design shall comply with ASME B31.3 for process piping stress, supports, and flexibility (code: Datasheet.md Design Code; rationale: Guidance.md Principles item 1; analysis: QR-5; procedure: Procedure.md Step 10; **TBD** specific design conditions — location TBD: ER Volume 2 Part 2)
- PR-6: Piping supports shall be designed for seismic loads (conditions: Datasheet.md Seismic requirements; rationale: Guidance.md Principles item 4; verification: QR-6; procedure: Procedure.md Step 5, Step 10; **TBD** seismic design basis — **ASSUMPTION**: NBC 2020; location TBD: ER Volume 2 Part 1)
- PR-7: Piping layout shall accommodate thermal expansion and contraction (conditions: Datasheet.md Operating temperature range; rationale: Guidance.md Trade-offs item 2; analysis: cross-reference DEL-14.03; procedure: Procedure.md Step 3; **TBD** expansion loop or expansion joint requirements)

### Interface Requirements

**Interdisciplinary coordination** (rationale: Guidance.md Considerations item 1; procedure: Procedure.md Step 8):
- IR-1: Piping GAs shall be coordinated with structural steel, concrete structures, electrical raceways, and instrumentation cable trays (content requirement: FR-6; procedure: Procedure.md Step 3, Step 8; considerations: Guidance.md Trade-offs item 3; **TBD** coordination procedures)
- IR-2: Piping supports shall be coordinated with structural attachment points (performance requirement: PR-6; support procedure: Procedure.md Step 5, Step 8; rationale: Guidance.md Principles item 4; cross-reference DEL-06.01 Structural Steel Design Drawings and DEL-05.01 Concrete Structures Design Drawings)
- IR-3: P&IDs shall be coordinated with instrumentation and control system design (content requirement: FR-5; procedure: Procedure.md Step 2, Step 8; cross-reference PKG-19 Control Systems)

**Equipment interfaces** (coordination: Procedure.md Step 1, Step 8):
- IR-4: Piping connections to railcar unloading pumps shall match pump nozzle sizes and ratings (cross-reference DEL-15.01 Pump Design Drawings and DEL-15.04 Pump Data Sheets; procedure: Procedure.md Step 1, Step 4)
- IR-5: Piping connections to marine loading pumps shall match pump nozzle sizes and ratings (cross-reference DEL-15.01, DEL-15.04; procedure: Procedure.md Step 1, Step 4)
- IR-6: Piping connections to storage tanks shall match tank nozzle locations and sizes (systems: Datasheet.md Tank farm piping connections; cross-reference DEL-13.01 Storage Tank Design Drawings; procedure: Procedure.md Step 1, Step 4)
- IR-7: Piping connections to valves and specialty equipment shall match equipment ratings (material data: cross-reference DEL-14.04; cross-reference PKG-16 Valves & Specialty Equipment; procedure: Procedure.md Step 1, Step 4)
- IR-8: Nitrogen distribution piping shall connect to Employer-supplied nitrogen skid (systems: Datasheet.md Nitrogen distribution piping; considerations: Guidance.md Considerations item 1; interface details **TBD** per Decision DEC-07 — location TBD: ER or Employer interface drawings; procedure: Procedure.md Step 1)

**System interfaces** (systems: Datasheet.md Key piping systems; coordination: Procedure.md Step 1, Step 8):
- IR-9: Railcar unloading header design shall interface with railcar unloading system (cross-reference PKG-10 Railcar Unloading System; procedure: Procedure.md Step 1, Step 8)
- IR-10: Marine loading export line design shall interface with marine loading system (cross-reference PKG-11 Marine Loading System; procedure: Procedure.md Step 1, Step 8)
- IR-11: Metering connections shall be coordinated with product transfer and metering package (systems: Datasheet.md Metering connections; cross-reference PKG-12 Product Transfer & Metering; procedure: Procedure.md Step 1, Step 8)

### Quality Requirements

**Drawing standards** (procedure: Procedure.md Step 7, Step 11):
- QR-1: All drawings shall comply with project CAD standards (attributes: Datasheet.md CAD Standard, CAD Software; considerations: Guidance.md Considerations item 2; procedure: Procedure.md Prerequisites, Step 7; **TBD** CAD management plan — location TBD: project procedures)
- QR-2: Drawing format, title blocks, and revision control shall comply with project document control procedures (attributes: Datasheet.md Drawing Number Prefix, Revision Control; procedure: Procedure.md Step 7, Step 11; **TBD** — location TBD: project procedures)
- QR-3: Drawings shall undergo interdisciplinary check (IDC) prior to issue for construction (coordination: IR-1, IR-2, IR-3; procedure: Procedure.md Step 8; verification: Verification section - IDC; **TBD** IDC procedures)
- QR-4: All drawings shall be checked and approved per project quality procedures (procedure: Procedure.md Step 9, Step 11; verification: Verification section; **TBD** check/approval matrix)

**Design verification** (rationale: Guidance.md Principles item 1; procedure: Procedure.md Step 10):
- QR-5: Piping stress analysis shall be performed for critical lines (performance requirement: PR-5; cross-reference DEL-14.03; procedure: Procedure.md Step 10; **TBD** criticality criteria)
- QR-6: Pipe support loads shall be verified by calculation (performance requirement: PR-6; support drawings: FR-8; cross-reference DEL-14.03; procedure: Procedure.md Step 5, Step 10; **TBD** load confirmation requirements)
- QR-7: Transient analysis shall be performed for railcar unloading and marine loading lines (systems: Datasheet.md Railcar unloading headers, Marine loading export lines; cross-reference DEL-14.06 Transient Analysis - Railcar Unloading, DEL-14.07 Transient Analysis - Marine Loading; procedure: Procedure.md Step 10; valve timing: cross-reference DEL-14.08)

## Standards

**Applicable codes and standards (Mechanical discipline):**

**Process piping design:**
- ASME B31.3 — Process Piping (design, materials, fabrication, inspection, testing) (code: Datasheet.md Design Code; rationale: Guidance.md Principles item 1; requirements: PR-5; verification: Procedure.md Step 10)
- **TBD** — Piping material specifications per DEL-14.02 (location TBD: ER Volume 2 Part 2)
- **TBD** — Additional applicable standards to be identified during design development (location TBD: ER Volume 2 Part 2)

**Piping supports:**
- **TBD** — Pipe support design standards (rationale: Guidance.md Principles item 4; **ASSUMPTION**: MSS SP-58, MSS SP-69, or similar; location TBD: ER Volume 2 Part 2)
- NBC 2020 — National Building Code of Canada (seismic and structural loads) (requirements: PR-6; **ASSUMPTION**: confirm design basis; location TBD: ER Volume 2 Part 1)

**Drawing standards:**
- **TBD** — CAD standards and drawing conventions (requirements: QR-1; attributes: Datasheet.md CAD Standard; procedure: Procedure.md Prerequisites, Step 7; location TBD: project CAD management plan)
- **TBD** — Symbology standards for P&IDs (content: FR-5; procedure: Procedure.md Step 2; **ASSUMPTION**: ISA 5.1 or similar; location TBD: project standards)

**Materials and corrosion:**
- **TBD** — Material selection criteria (product: PR-1; materials: Datasheet.md Materials; rationale: Guidance.md Principles item 3, Trade-offs item 1; location TBD: ER Volume 2 Part 2 or DEL-14.02)
- **TBD** — Corrosion allowance and coating requirements (conditions: Datasheet.md Corrosion allowance; location TBD: ER Volume 2 Part 2)

**Project-specific requirements:**
- Employer's Requirements Volume 2 Part 1 — General Requirements (procedure: Procedure.md Prerequisites)
- Employer's Requirements Volume 2 Part 2 — Civil & Process Mechanical Works (procedure: Procedure.md Step 1)
- Project Quality Management Plan — **TBD** (requirements: QR-4; location TBD)

## Verification

**Verification methods for Drawing deliverables:**

**Design review** (procedure: Procedure.md Step 7, Step 9):
- Design self-check by originator (procedure: Procedure.md Step 7)
- Independent check by qualified checker (peer review) (requirements: QR-4; procedure: Procedure.md Step 9)
- Interdisciplinary check (IDC) with affected disciplines (requirements: QR-3; coordination: IR-1, IR-2, IR-3; procedure: Procedure.md Step 8)
- Design review against ER requirements (procedure: Procedure.md Step 1, Step 7)

**Technical verification** (requirements: QR-5, QR-6, QR-7; procedure: Procedure.md Step 10):
- Dimensional verification and spatial coordination check (coordination: IR-1; procedure: Procedure.md Step 3)
- Interface verification with equipment data sheets and vendor drawings (interfaces: IR-4 through IR-11; procedure: Procedure.md Step 1, Step 4)
- Stress analysis verification per ASME B31.3 (requirements: QR-5; performance: PR-5; cross-reference DEL-14.03; procedure: Procedure.md Step 10)
- Support load verification (requirements: QR-6; performance: PR-6; cross-reference DEL-14.03; procedure: Procedure.md Step 5, Step 10)
- Transient analysis verification (requirements: QR-7; cross-reference DEL-14.06 Railcar Unloading, DEL-14.07 Marine Loading, DEL-14.08 Valve Timing; procedure: Procedure.md Step 10)

**Standards compliance** (requirements: QR-1, QR-2; procedure: Procedure.md Step 7):
- CAD standards compliance check (requirements: QR-1; procedure: Procedure.md Step 7)
- Drawing format and title block verification (requirements: QR-2; procedure: Procedure.md Step 7, Step 11)
- P&ID symbology verification against project standards (content: FR-5; procedure: Procedure.md Step 2, Step 7)

**Acceptance criteria:**
- All drawings reviewed and approved with no outstanding comments or holds (procedure: Procedure.md Step 11)
- Interdisciplinary check complete with all coordination issues resolved (requirements: QR-3; procedure: Procedure.md Step 8)
- All calculations (stress, support, transient) reviewed and approved (requirements: QR-5, QR-6, QR-7; procedure: Procedure.md Step 10)
- **TBD** — Additional acceptance criteria per project quality procedures (location TBD)

## Documentation

**Required documentation outputs:**

**Drawing types** (source: Decomposition DEL-14.01; attributes: Datasheet.md Drawing Types; production: Procedure.md Steps 2-6):
- P&IDs (Process and Instrumentation Diagrams) (content: FR-5; procedure: Procedure.md Step 2)
- Piping GAs (General Arrangement drawings — plan and elevation views) (content: FR-6; procedure: Procedure.md Step 3)
- Piping isometrics (fabrication drawings) (content: FR-7; procedure: Procedure.md Step 4)
- Pipe support drawings (support details and schedules) (content: FR-8; procedure: Procedure.md Step 5)
- Phase 2 connection details (expansion interface drawings) (content: FR-9; procedure: Procedure.md Step 6)

**Supporting documentation** (procedure: Procedure.md Steps 7-10; records: Procedure.md Records section):
- Drawing index (list of all drawings in the set) (procedure: Procedure.md Step 11)
- Design basis memo or calculation summary (cross-reference DEL-14.03; procedure: Procedure.md Step 1, Step 10)
- Interdisciplinary check (IDC) records (requirements: QR-3; procedure: Procedure.md Step 8)
- Design review records and comment resolution log (requirements: QR-4; procedure: Procedure.md Step 7, Step 9)

**Documentation requirements:**
- All documents shall comply with project document control procedures (requirements: QR-2; procedure: Procedure.md Step 11)
- Revision control per project numbering system (attributes: Datasheet.md Revision Control; requirements: QR-2; procedure: Procedure.md Step 11; **TBD** — location TBD: project procedures)
- Electronic format (attributes: Datasheet.md Sheet Size, CAD Software; procedure: Procedure.md Records - Electronic format; **TBD** — **ASSUMPTION**: PDF for issued drawings, native CAD files for working copies — location TBD: project CAD management plan)
- Storage location: `2_Checking/` (during review) → `3_Issued/` (upon approval) (procedure: Procedure.md Records - Storage locations)
- Submittal requirements (procedure: Procedure.md Step 11; **TBD** — submittal schedule and approval workflow; location TBD: ER Volume 2 Part 1)
- As-built documentation (procedure: Procedure.md Step 12; **TBD** — requirements for as-built markup and final record drawings; location TBD: ER Volume 2 Part 1)
