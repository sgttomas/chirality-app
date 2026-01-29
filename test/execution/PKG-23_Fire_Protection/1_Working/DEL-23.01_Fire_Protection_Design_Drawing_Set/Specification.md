# Specification: DEL-23.01 Fire Protection Design Drawing Set

## Scope

This specification defines the requirements for **Fire Protection Design Drawing Set** within **PKG-23 Fire Protection** for the Canola Oil Transload Facility — Phase 1 Design & Build project.

**Project Context:**
- Location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- Employer: DP World Fraser Surrey Inc.
- Contract Type: Design & Build
- Source: Decomposition document Section 1.1

**Deliverable Scope:**

This deliverable defines the design arrangement and details for fire protection systems per Employer's Requirements (ER), including:

**Anticipated deliverable artifacts:**
- Fire water loop layout (Source: Decomposition DEL-23.01 anticipated artifacts)
- Hydrant locations (Source: Decomposition DEL-23.01 anticipated artifacts)
- Fire alarm system drawings (Source: Decomposition DEL-23.01 anticipated artifacts)

**Additional drawings (typical for fire protection systems):**
- Fire water system schematic — **ASSUMPTION**
- Foam system layout and details — **ASSUMPTION**: Likely required for combustible liquid storage per NFPA 30
- Fire pump installation details (if applicable) — **ASSUMPTION**
- Fire protection details and standard details — **ASSUMPTION**
- Fire protection zone plan — **ASSUMPTION**

**Scope Boundaries:**

| Included | Excluded / Interface |
|----------|---------------------|
| Fire water distribution piping and loop | Fire water source/supply connection (interface with Employer or municipal supply — **TBD**) |
| Fire hydrants and hose stations | Fire department vehicle access (PKG-03 Civil scope) |
| Fire alarm detection and notification system | Fire alarm monitoring/dispatch connection (interface — **TBD**) |
| Foam suppression systems for tanks and marine loading | Building sprinkler systems (PKG-22 Building MEP scope — **ASSUMPTION**) |
| Fire pump (if within Contractor scope) | Fire pump electrical power supply (PKG-17 Electrical scope) |
| Fire protection control/monitoring interfaces | Control system integration (PKG-19 Control Systems scope) |

**Project Objectives Supported:**

This deliverable supports **OBJ-1: Safe & Reliable Operation** — "The facility is suitable for safe, efficient, reliable, and continuous use under actual operational conditions" (Source: Decomposition Section 2 and Section 6 Objective Mapping)

## Requirements

### Functional Requirements

**FR-1: Fire Water Distribution System**
- The fire water loop shall provide fire protection coverage to all facility areas including tank farm, marine loading, railcar unloading, pump house, and building areas
- Source: **ASSUMPTION**: Standard fire protection functional requirement for industrial facility
- Verification: Coverage analysis and compliance with NFPA 30 spacing requirements (see DEL-23.03)

**FR-2: Fire Hydrant System**
- Fire hydrants shall be located to provide coverage per NFPA 30 requirements for combustible liquid facilities
- Hydrant spacing shall not exceed code-required maximums — **TBD**: Specific spacing per NFPA 30 analysis
- Source: **ASSUMPTION**: NFPA 30 requirements (location TBD — requires access to NFPA 30)
- Verification: Hydrant coverage analysis (see DEL-23.03)

**FR-3: Fire Detection and Alarm System**
- Fire detection and alarm system shall provide early warning of fire conditions and activate suppression systems as required
- System shall include detection devices, notification appliances, and control panel(s)
- Source: **ASSUMPTION**: Standard fire alarm functional requirement per NFPA 72
- Verification: System functional testing (see DEL-23.05)

**FR-4: Foam Suppression Systems**
- Fixed foam suppression systems shall be provided for storage tanks and marine loading areas as required by NFPA 30 for combustible liquid facilities — **TBD**: Specific foam system requirements
- Source: **ASSUMPTION**: NFPA 30 requirements for Class IIIA combustible liquids (location TBD)
- Verification: System design calculations and testing (see DEL-23.03, DEL-23.05)

**FR-5: Fire Protection Coordination**
- Fire protection systems shall be coordinated with facility process, electrical, and control systems
- Source: **ASSUMPTION**: Standard coordination requirement
- Verification: Interdisciplinary checks and interface reviews

### Performance Requirements

**PR-1: Fire Water Flow and Pressure**
- Fire water system shall deliver required flow and pressure per NFPA 30 and hydraulic analysis
- Minimum flow rate: **TBD** gpm (to be determined per DEL-23.03 Fire Protection Design Calculations)
- Minimum residual pressure: **TBD** psi at most remote hydrant (to be determined per DEL-23.03)
- Duration: **TBD** hours (typically 2–4 hours for combustible liquid facilities per NFPA 30 — **ASSUMPTION**)
- Source: NFPA 30 and hydraulic analysis (DEL-23.03)
- Verification: Hydraulic calculations (DEL-23.03) and flow testing (DEL-23.05)

**PR-2: Fire Alarm System Response Time**
- Fire detection devices shall activate alarm within response time limits per NFPA 72
- Source: **ASSUMPTION**: NFPA 72 requirements (location TBD)
- Verification: System commissioning tests (DEL-23.05)

**PR-3: Foam System Discharge Rate**
- Foam systems shall deliver foam solution at application rates per NFPA standards — **TBD**: Specific rates per tank size and product
- Source: **ASSUMPTION**: NFPA 11/16 requirements (location TBD)
- Verification: Foam system calculations (DEL-23.03) and discharge testing (DEL-23.05)

**PR-4: System Reliability**
- Fire protection systems shall meet reliability targets per OBJ-1 (Safe & Reliable Operation)
- Redundancy and backup provisions: **TBD**
- Source: Decomposition Section 2 (OBJ-1) and **ASSUMPTION**: Reliability requirements per Employer's Requirements
- Verification: Design review and reliability analysis (if required — **TBD**)

### Interface Requirements

**INT-1: Civil and Site Development (PKG-03, PKG-04)**
- Fire water loop routing coordinated with site grading, roads, and utilities
- Hydrant locations coordinated with vehicle access and turning radii
- Underground fire main coordination with other underground utilities
- Source: **ASSUMPTION**: Standard interface coordination
- Verification: Interdisciplinary checks (IDC)

**INT-2: Process Piping (PKG-14)**
- Foam system connections to storage tanks and marine loading arms
- Fire protection water supply for cooling systems (if required)
- Source: **ASSUMPTION**: Standard interface coordination
- Verification: Interdisciplinary checks (IDC)

**INT-3: Electrical Power Distribution (PKG-17)**
- Electrical power supply to fire pump (if required), fire alarm panel, and emergency lighting
- Emergency power/backup power provisions
- Source: **ASSUMPTION**: Standard interface coordination
- Verification: Interdisciplinary checks (IDC) and electrical load calculations

**INT-4: Control Systems (PKG-19)**
- Fire alarm system integration with facility SCADA/DCS
- Fire protection system status monitoring and alarms
- Source: **ASSUMPTION**: Standard interface coordination
- Verification: Control system integration testing (DEL-19.05)

**INT-5: Marine Structures (PKG-08)**
- Marine fire main and hydrant/monitor locations on wharf
- Foam system connections for marine loading arms
- Source: **ASSUMPTION**: Standard interface coordination for marine terminal
- Verification: Interdisciplinary checks (IDC)

**INT-6: Buildings (PKG-21, PKG-22)**
- Building fire alarm system integration
- Fire protection penetrations through building envelope
- Source: **ASSUMPTION**: Standard interface coordination
- Verification: Interdisciplinary checks (IDC)

**INT-7: Employer/Authority Interfaces**
- Connection to fire water supply source — **TBD**: Employer-supplied or municipal connection
- Fire department coordination — **TBD**: Access, pre-plans, training
- Fire marshal approval and inspections — **TBD**
- Source: **ASSUMPTION**: Typical authority having jurisdiction (AHJ) requirements

### Quality Requirements

**QR-1: Design Standards Compliance**
- All drawings shall comply with applicable NFPA codes and standards as listed in Section "Standards" below
- All drawings shall comply with National Building Code of Canada (NBCC) 2020 and British Columbia Fire Code (BCFC)
- Source: **ASSUMPTION**: Code compliance requirements for BC project
- Verification: Design review and AHJ approval

**QR-2: Drawing Standards**
- All drawings shall comply with project CAD standards — **TBD**: Project CAD manual reference
- Drawing format, title blocks, symbology, layering, and line types per project standards
- Source: **ASSUMPTION**: Project document control requirements
- Verification: CAD standards compliance check

**QR-3: Quality Management**
- All work shall comply with the project Quality Management Plan — **TBD**: QMP reference
- Source: Specification standard quality requirement
- Verification: Quality audits and reviews

**QR-4: Drawing Checking**
- All drawings subject to self-check, interdisciplinary check (IDC), and independent check per project quality procedures
- Source: **ASSUMPTION**: Project quality procedures
- Verification: Check records and sign-offs (see Procedure.md)

## Standards

**Governing Codes and Standards (Fire Protection):**

The following codes and standards are applicable to this deliverable:

| Code/Standard | Title | Application | Source |
|---------------|-------|-------------|--------|
| NFPA 30 | Flammable and Combustible Liquids Code | Primary standard for combustible liquid storage and handling | **ASSUMPTION**: Governing standard for canola oil (Class IIIA combustible liquid) |
| NFPA 24 | Installation of Private Fire Service Mains and Their Appurtenances | Fire water loop and underground piping design | **ASSUMPTION**: Applicable to fire water distribution |
| NFPA 20 | Installation of Stationary Pumps for Fire Protection | Fire pump installation (if applicable) | **ASSUMPTION**: If fire pump is part of Contractor scope |
| NFPA 13 | Installation of Sprinkler Systems | Building and process area sprinkler systems (if applicable) | **ASSUMPTION**: Coordination with building scope |
| NFPA 15 | Water Spray Fixed Systems for Fire Protection | Tank cooling/deluge systems (if applicable) | **ASSUMPTION**: May apply to storage tank protection |
| NFPA 16 | Installation of Foam-Water Sprinkler and Foam-Water Spray Systems | Tank and marine loading foam systems | **ASSUMPTION**: Likely applicable for combustible liquid protection |
| NFPA 11 | Low-, Medium-, and High-Expansion Foam | Foam system design | **ASSUMPTION**: Applicable if foam systems used |
| NFPA 72 | National Fire Alarm and Signaling Code | Fire alarm and detection system design | **ASSUMPTION**: Governs fire alarm design |
| NBCC 2020 | National Building Code of Canada 2020 Edition | Building code requirements | **ASSUMPTION**: Applicable building code for BC |
| BCFC | British Columbia Fire Code | Provincial fire code | **ASSUMPTION**: Provincial fire code requirements |
| Alberta OHS Code | Occupational Health and Safety Code | Worker safety requirements | Decomposition: applicable standard |
| CSA Z462 | Workplace Electrical Safety | Electrical safety in fire protection systems | Decomposition: applicable standard |

**Additional Standards and References:**

| Document | Application | Source |
|----------|-------------|--------|
| Employer's Requirements Volume 2 Parts 1–3 | Project-specific requirements | Decomposition Section 3 (Reference Documents) |
| Project CAD Manual | Drawing production standards | **TBD** |
| Project Quality Management Plan | Quality procedures | **TBD** |
| Project Document Control Procedures | Document management | **TBD** |

**Standards Availability:**

The specific clause-level requirements from the above codes and standards will be extracted and applied during design development. If a standard is cited but the relevant text is not available in accessible references (package `0_References/`), specific requirements will be marked **TBD** until the standard is obtained.

## Verification

**Verification Methods for Drawing Deliverables:**

The following verification methods shall be applied to ensure the fire protection design drawing set meets requirements:

**V-1: Design Self-Check**
- Originator reviews drawings for completeness, accuracy, and compliance with standards
- Verification record: Self-check sign-off on drawing or transmittal
- Source: **ASSUMPTION**: Project quality procedures

**V-2: Interdisciplinary Check (IDC)**
- Affected disciplines review drawings for interface coordination and conflicts
- IDC comments tracked and resolved prior to issue
- Verification record: IDC sign-off and comment resolution log
- Source: **ASSUMPTION**: Project quality procedures

**V-3: Independent Check (Peer Review)**
- Qualified checker (not the originator) reviews drawings for technical correctness, code compliance, and completeness
- Checker verifies calculations, assumptions, and references
- Verification record: Independent check sign-off on drawing or transmittal
- Source: **ASSUMPTION**: Project quality procedures

**V-4: Dimensional Verification**
- Key dimensions, coordinates, and elevations verified against survey control and other discipline drawings
- Verification record: Dimensional check record or markup
- Source: **ASSUMPTION**: Project quality procedures for coordination drawings

**V-5: CAD Standards Compliance Check**
- Drawings checked for compliance with project CAD standards (layering, line types, symbology, title block)
- Verification record: CAD QA/QC checklist
- Source: **ASSUMPTION**: Project CAD standards

**V-6: Code Compliance Review**
- Drawings reviewed for compliance with NFPA 30, NBCC, BCFC, and other applicable codes
- Verification record: Code compliance checklist or design review minutes
- Source: **ASSUMPTION**: Project quality procedures and AHJ requirements

**V-7: Constructability Review**
- Drawings reviewed for constructability, access, maintenance considerations
- Verification record: Constructability review comments and resolutions
- Source: **ASSUMPTION**: Design-build best practice

**Acceptance Criteria:**

Drawings are acceptable for issue when:
- All self-checks, IDCs, and independent checks completed with sign-offs
- All review comments resolved or dispositioned
- CAD standards compliance verified
- Code compliance verified
- Drawing revision status and metadata correct
- Source: **ASSUMPTION**: Project quality procedures — specific acceptance criteria **TBD**

**Hold Points / Witness Points:**

| Hold/Witness Point | Description | Party | Source |
|--------------------|-------------|-------|--------|
| Design review milestone | Fire protection design review at 30%/60%/90% (or per project schedule) | Employer review — **TBD** | **ASSUMPTION**: Typical design-build review gates |
| AHJ review | Fire marshal or authority having jurisdiction review/approval | Fire marshal / AHJ | **ASSUMPTION**: Required for fire protection systems |
| Interdisciplinary coordination | IDC completion prior to issue | All affected disciplines | **ASSUMPTION**: Standard coordination hold point |

Specific hold points and witness points to be confirmed per project quality plan and contract requirements — **TBD**

## Documentation

**Required Documentation Outputs:**

The fire protection design drawing set shall include (minimum):

| Drawing | Content | Source |
|---------|---------|--------|
| Fire water loop layout | Site plan showing fire water piping layout, loop configuration, isolation valves, connections to source | Decomposition: DEL-23.01 anticipated artifacts |
| Hydrant locations | Site plan showing fire hydrant locations, coverage radii (per NFPA 30), hose reach, access routes | Decomposition: DEL-23.01 anticipated artifacts |
| Fire alarm system drawings | Fire detection/alarm device locations, wiring/conduit routing, panel locations, single-line diagrams, panel schedules | Decomposition: DEL-23.01 anticipated artifacts |

**Additional Documentation (typical):**

| Drawing | Content | Source |
|---------|---------|--------|
| Fire water system schematic | Single-line diagram showing fire water system configuration, connections, control valves, pump (if applicable), isolation valves | **ASSUMPTION**: Typical drawing set component |
| Foam system layout | Foam concentrate storage tank, proportioning systems, foam piping, discharge devices for tank and marine loading areas | **ASSUMPTION**: Required for combustible liquid facility per NFPA 30 |
| Fire pump details | Fire pump room layout, pump installation details, piping connections (if fire pump in Contractor scope) | **ASSUMPTION**: If applicable |
| Fire protection details | Standard details for hydrant installation, valve pit details, pipe supports, sleeve/penetration details, fire main tie-in details | **ASSUMPTION**: Typical detail drawings |
| Fire protection zone plan | Fire protection zone boundaries, equipment tagging/numbering, system shutdown boundaries | **ASSUMPTION**: Facilitates operations and maintenance |

**Documentation Format and Control:**

| Requirement | Description | Source |
|-------------|-------------|--------|
| Format | Electronic CAD files (DWG or equivalent) and PDF plot files | **ASSUMPTION**: Standard project deliverable format |
| Sheet size | ANSI D (24" × 36") standard, ANSI E (34" × 44") for large site plans if needed | **ASSUMPTION**: Typical industrial drawing size |
| Revision control | Per project drawing numbering and revision system — **TBD** | **ASSUMPTION**: Project document control procedures |
| Drawing numbers | Per project numbering system with PKG-23 identifier — **TBD** | **ASSUMPTION**: Project document control procedures |
| Title block | Per project drawing standards — **TBD** | **ASSUMPTION**: Project drawing standards |
| Metadata | Drawing title, number, revision, date, originator, checker, approver, project name/number | **ASSUMPTION**: Standard drawing metadata |
| Transmittal | Drawings issued via formal transmittal per project document control procedures — **TBD** | **ASSUMPTION**: Project document control procedures |
| Storage location | Project document management system — **TBD** | **ASSUMPTION**: Electronic document management |
| Retention | Per project record retention requirements — **TBD** | **ASSUMPTION**: Project document control procedures |

**Document Management:**

- All drawings shall be managed per project document control procedures
- Drawings progress through review states: For Information → For Review → For Construction → As-Built (or per project conventions — **TBD**)
- Source: **ASSUMPTION**: Typical design-build document management workflow

**Deliverable Status and Location:**

- Working files: `1_Working/DEL-23.01_Fire_Protection_Design_Drawing_Set/`
- Review copies: `2_Checking/` (during CHECKING state)
- Issued copies: `3_Issued/` (upon ISSUED state)
- Lifecycle state tracked in `_STATUS.md`
- Source: README.md and framework conventions
