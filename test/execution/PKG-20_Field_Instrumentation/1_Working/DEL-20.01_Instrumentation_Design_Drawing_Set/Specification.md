# Specification: DEL-20.01 Instrumentation Design Drawing Set

## Scope

This specification defines the requirements for the **Instrumentation Design Drawing Set** within **PKG-20 Field Instrumentation** for the Canola Oil Transload Facility Phase 1 at Fraser Surrey Terminal, Surrey, BC.

**Deliverable Purpose:**

Defines the design arrangement and details for instrumentation per ER requirements.

**Source:** Decomposition document `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, DEL-20.01 description (line 496)

**Package Scope:**

PKG-20 Field Instrumentation includes field instruments, transmitters, switches, instrument cabling, and junction boxes.

**Source:** Decomposition document, PKG-20 Scope (line 490)

**Deliverable Artifacts:**

This drawing set shall include:
1. **Instrument location plans** — Spatial arrangement of field instruments on facility layout
2. **Instrument installation details** — Mounting, support, and connection details for field instruments
3. **Cable schedules** — Instrument cable routing, termination, and specifications

**Source:** Decomposition document, DEL-20.01 Anticipated Artifacts (line 496); `_CONTEXT.md`

**Inclusions:**
- Field instrument locations and elevations
- Instrument mounting and support details
- Instrument cable routing arrangements
- Junction box locations and schedules
- Instrument hook-up details (typical and specific)
- Cable schedule tables with termination information

**Exclusions:**
- Control system architecture (see PKG-22 Control Systems & SCADA)
- Electrical power distribution (see PKG-17 Electrical Power Distribution)
- Instrument procurement specifications (see DEL-20.02 Instrumentation Technical Specification)
- Instrument data sheets (see DEL-20.04 Instrumentation Data Sheet Package)

**Source:** **ASSUMPTION** based on deliverable type (Drawing) and typical EPC package boundaries

## Requirements

### Functional Requirements

**FR-1: Drawing Content**

The Instrumentation Design Drawing Set shall provide sufficient detail to support:
- Equipment procurement (instrument mounting requirements)
- Construction and installation (field installation guidance)
- Commissioning and testing (loop verification, as-built records)
- Operations and maintenance (instrument location reference)

**Source:** **ASSUMPTION** based on typical drawing deliverable purpose for design-build projects

**FR-2: Instrument Location Plans**

The drawing set shall include instrument location plans showing:
- All field instruments by tag number (per ISA 5.1 tagging convention — **TBD**: Project tagging standard)
- Instrument elevations and orientations
- Access requirements for installation and maintenance
- Coordination with structural, piping, and electrical disciplines

**Source:** Anticipated artifacts (line 496) and **ASSUMPTION** based on ISA 5.1 instrumentation practices

**FR-3: Installation Details**

The drawing set shall include installation details showing:
- Instrument mounting arrangements (pipe-mounted, vessel-mounted, structure-mounted)
- Support and bracket details
- Tubing and wiring connection details
- Weatherproofing and environmental protection
- Hazardous area seal and cable gland details (**TBD**: per facility hazardous area classification)

**Source:** Anticipated artifacts (line 496) and **ASSUMPTION** based on typical I&C installation requirements

**FR-4: Cable Schedules**

The drawing set shall include cable schedules showing:
- Cable identification and tagging
- Cable routing from field instruments to termination points
- Cable specifications (conductor size, insulation, shielding)
- Termination details (junction boxes, marshalling cabinets, control panels)

**Source:** Anticipated artifacts (line 496) and **ASSUMPTION** based on typical I&C cable documentation

**FR-5: Coordination with Process Design**

Instrument locations shall be coordinated with:
- P&IDs (process instrument tagging and loop identification)
- Piping arrangements (connection points, accessibility)
- Equipment layouts (vessel nozzles, tank penetrations)
- Structural design (platform access, cable tray routing)

**Source:** **ASSUMPTION** based on interdisciplinary coordination requirements for design-build projects

**FR-6: Project-Specific Requirements**

Drawings shall address project-specific facility context:
- Canola oil service (material compatibility, process conditions)
- Marine terminal environment (corrosion protection, weathering)
- Railcar unloading operations (32 stations, instrument coverage)
- Storage tank instrumentation (3 × 15,000 MT tanks, level/temperature monitoring)
- Custody transfer metering (accurate measurement for export loading)

**Source:** Decomposition Section 1.1 Project Overview (Key Parameters) and **ASSUMPTION** based on facility function

### Performance Requirements

**PR-1: Drawing Attributes and Standards**

All drawings shall comply with the following attributes (see Datasheet.md for detailed attribute specifications):

- **Drawing Scale:** **TBD** — **ASSUMPTION**: Typical scales 1:50, 1:100 for plans; NTS (not to scale) for details
- **Sheet Size:** **TBD** — **ASSUMPTION**: ISO A1 or ANSI D per project CAD standards
- **CAD Standard:** **TBD** — To be confirmed per project document management plan
- **Drawing Format:** **TBD** — **ASSUMPTION**: Electronic PDF/DWG per project requirements
- **Revision Control:** Per project document control procedures (see Procedure.md Step 6)
- **Classification:** **TBD** — **ASSUMPTION**: Contractor's Design Documents (for construction)

**PR-2: Symbology and Conventions**

- Instrumentation symbology shall comply with ISA 5.1
- Discipline drawing standards — **TBD**: I&C drawing conventions to be defined
- Project CAD standards — **TBD**: Layer naming, line weights, text styles per project standards

**PR-3: Information Completeness**

Drawings shall be sufficiently complete for:
- Construction bidding (if applicable)
- Field installation without additional engineering input
- Commissioning and loop checkout (tag identification, termination verification)

**Source:** **ASSUMPTION** based on design-build deliverable maturity expectations

**PR-3: Drawing Accuracy**

- Instrument locations shall be dimensioned and coordinated with as-designed piping and equipment arrangements
- Installation details shall reflect manufacturer requirements and site conditions
- Cable schedules shall match control system I/O allocation (**TBD**: coordinate with PKG-22 Control Systems)

**Source:** **ASSUMPTION** based on typical drawing accuracy requirements

### Interface Requirements

**INT-1: Interdisciplinary Coordination**

This deliverable interfaces with:
- **PKG-14 Process Piping** — Instrument connections to process piping
- **PKG-22 Control Systems & SCADA** — Control system I/O and network architecture
- **PKG-23 Electrical Infrastructure** — Power supply to instruments, cable routing infrastructure
- **PKG-13 Storage Tanks** — Tank instrumentation (level, temperature)
- **PKG-15 Pumps and Rotating Equipment** — Equipment instrumentation (pressure, flow, vibration)
- **PKG-12 Product Transfer and Metering** — Custody transfer instrumentation

**Source:** **ASSUMPTION** based on typical I&C interfaces and decomposition package structure

**INT-2: Deliverable Dependencies**

See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies coordinated externally by humans.

**Typical upstream inputs** (coordination required):
- P&IDs and instrument lists
- Equipment layouts and piping arrangements
- Hazardous area classification drawings
- Control system architecture and I/O requirements

**Typical downstream users:**
- Construction contractors (for field installation)
- Commissioning team (for loop verification)
- Operations (for as-built reference)

**Source:** **ASSUMPTION** based on typical EPC workflow

### Quality Requirements

**QR-1: Design Review**

All drawings shall undergo:
- Self-check by originator
- Interdisciplinary check (IDC) with affected disciplines
- Independent peer review by qualified I&C engineer
- Approval by discipline lead

**Source:** **ASSUMPTION** based on typical EPC quality procedures

**QR-2: Drawing Revision Control**

- All drawings shall be revision-controlled per project document control procedures — **TBD**: Project numbering and revision system
- Drawing changes shall be tracked and marked on revised drawings
- Superseded drawings shall be archived per project document management plan

**Source:** **ASSUMPTION** based on typical document control requirements

**QR-3: Compliance Verification**

Drawings shall be verified for compliance with:
- Project design basis and Employer's Requirements — **TBD**: Specific ER sections to be identified
- Applicable codes and standards (see Standards section below)
- Project quality management plan — **TBD**: Project QA/QC procedures

**Source:** **ASSUMPTION** based on typical quality assurance requirements

**QR-4: As-Built Documentation**

Drawing set shall be updated to reflect as-built conditions:
- Field modifications during construction
- Commissioning findings and adjustments
- Final instrument locations and cable routing

**Source:** **ASSUMPTION** based on typical design-build as-built requirements

## Standards

**I&C Discipline Standards (Applicable):**

- **ISA 5.1** — Instrumentation Symbols and Identification
  - **ASSUMPTION**: Governs instrument tagging, symbology, and drawing conventions
  - **TBD**: Specific clauses to be referenced pending access to standard

- **ISA 84 / IEC 61511** — Functional Safety of Safety Instrumented Systems
  - **ASSUMPTION**: Applicable if safety instrumented functions (SIF) are included in facility design
  - **TBD**: Applicability to be confirmed based on process safety requirements

- **API 554** — Process Instrumentation and Control
  - **ASSUMPTION**: Applicable for process industry instrumentation design practices
  - **TBD**: Specific sections relevant to drawing preparation

**Electrical and Hazardous Area Standards:**

- **CSA C22.1** — Canadian Electrical Code
  - **ASSUMPTION**: Governs hazardous area installation, wiring methods, and cable specifications for BC location
  - **TBD**: Specific requirements for instrumentation wiring in hazardous areas

- **CSA C22.2 No. 30** / **IEC 60079** — Explosive Atmospheres
  - **ASSUMPTION**: Applicable for hazardous area classification and instrument enclosure selection
  - **TBD**: Facility hazardous area classification to be confirmed

**Design and Construction Standards:**

- **NBC 2015** — National Building Code of Canada
  - **ASSUMPTION**: Governs structural loads, seismic design for instrument supports
  - **TBD**: Seismic design parameters for Surrey, BC location

- **CSA Z662** — Oil and Gas Pipeline Systems
  - **ASSUMPTION**: May be applicable for instrument connections to process piping
  - **TBD**: Applicability to be confirmed based on piping system classification

**Project-Specific Standards:**

- **Employer's Requirements** — Project-specific design criteria and performance standards
  - **TBD**: Specific sections to be identified from Volume 2 Parts 1-3
  - **Source:** Decomposition Section 3 Reference Documents (lines 75-79) — Employer's Requirements volumes listed

**Note:** Standards applicability and specific clause-level requirements **TBD** pending access to standard documents and Employer's Requirements. Current standard list is **ASSUMPTION** based on I&C discipline typical practice and Canadian regulatory context.

## Verification

**Verification Methods:**

| Requirement | Verification Method | Responsibility | Procedure Reference |
|-------------|---------------------|----------------|---------------------|
| Drawing content completeness | Design review checklist | I&C Lead Engineer | Procedure.md Steps 4.2, 4.3 |
| Instrument location coordination | Interdisciplinary check (IDC) | All affected disciplines | Procedure.md Step 4.4 |
| Installation detail accuracy | Manufacturer data review | I&C Engineer | Procedure.md Step 3.2 |
| Cable schedule consistency | Control system I/O cross-check | I&C + Electrical | Procedure.md Step 3.3 |
| Standards compliance | Code compliance review | I&C Lead + QA | Procedure.md Step 4.1 |
| CAD standards compliance | Drawing standards audit | CAD Manager | Procedure.md Step 4.1 |

**Implementation:** See Procedure.md Section "Verification" for detailed verification activities and acceptance criteria.

**Source:** **ASSUMPTION** based on typical EPC verification methods for drawing deliverables

**Acceptance Criteria:**

- All instruments from P&IDs are located and detailed on drawings
- All interdisciplinary coordination issues are resolved (no open IDC comments)
- Drawings are approved by discipline lead (signed and stamped per professional requirements)
- Drawings comply with project CAD standards and naming conventions — **TBD**: Project-specific criteria
- All hazardous area installations comply with electrical code requirements — **TBD**: Per hazardous area classification

**Source:** **ASSUMPTION** based on typical drawing deliverable acceptance criteria

**Hold Points:**

- **TBD** — Hold points for Employer review to be identified per project execution plan
- **ASSUMPTION**: Typical hold points may include 30%, 60%, 90% design reviews and IFC (Issued for Construction)

## Documentation

**Required Documentation Outputs:**

1. **Instrument Location Plans**
   - Format: **TBD** — **ASSUMPTION**: CAD drawings (PDF + native DWG/DGN)
   - Naming convention: **TBD** — Per project document numbering system
   - Revision control: Per project document control procedures

2. **Instrument Installation Details**
   - Format: **TBD** — **ASSUMPTION**: CAD drawings (PDF + native DWG/DGN)
   - Content: Typical and specific mounting details, connection diagrams
   - Coordination: Manufacturer installation manuals (from DEL-20.04 Data Sheet Package)

3. **Cable Schedules**
   - Format: **TBD** — **ASSUMPTION**: Tabular schedules embedded in drawings or separate database export
   - Content: Cable identification, routing, specifications, termination points
   - Coordination: Control system I/O database (from PKG-22 Control Systems)

**Source:** Decomposition DEL-20.01 Anticipated Artifacts (line 496)

**Documentation Management:**

- All documentation shall be managed per project document control procedures — **TBD**: Document management system and protocols
- Drawings shall be stored in project document repository with access control
- Revisions shall be tracked and distributed per project change management procedures
- Final issue shall be archived as as-built documentation per project closeout requirements

**Source:** **ASSUMPTION** based on typical EPC document management requirements

**Supporting Documentation:**

The following supporting documentation may be produced in conjunction with this deliverable:
- Design calculation records (see DEL-20.03 Instrumentation Design Calculations)
- Instrument data sheets (see DEL-20.04 Instrumentation Data Sheet Package)
- Installation test records (see DEL-20.05 Instrumentation Installation & Test Records)

**Source:** Cross-reference to related PKG-20 deliverables per decomposition (lines 497-500)

**Project Objective Alignment:**

This deliverable supports **OBJ-1: Safe & Reliable Operation** — ensuring field instrumentation is properly designed, located, and installed for safe and reliable facility operations.

**Source:** Decomposition Section 6 Objective-to-Deliverable Mapping (line 780)
