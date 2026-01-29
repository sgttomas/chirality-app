# Specification: DEL-24.01 Security System Design Drawing Set

## Scope

This specification defines the requirements for producing the **Security System Design Drawing Set** within **PKG-24 Security Systems** for the Canola Oil Transload Facility — Phase 1 at Fraser Surrey Terminal.

**Purpose:** Defines the design arrangement and details for security system per ER requirements.

*Source: `_CONTEXT.md`; Decomposition Section 5 — PKG-24*

### Inclusions

The drawing set shall include:
- CCTV layout showing camera locations and coverage zones
- Camera coverage drawings with field-of-view analysis
- Access control layout showing readers, controllers, and controlled doors/gates
- **ASSUMPTION**: System architecture diagram showing network topology and Terminal integration
- **ASSUMPTION**: Mounting and installation details for equipment

*Source: `_CONTEXT.md` — Anticipated Artifacts; typical security system drawing set content*

### Exclusions

The following are outside the scope of this drawing set:
- Security system equipment specifications (covered under DEL-24.02)
- Equipment datasheets and submittals (covered under DEL-24.03)
- Installation and test records (covered under DEL-24.04)
- Security operations procedures **ASSUMPTION** — operational procedures outside D&B scope
- Terminal-wide security master plan **ASSUMPTION** — Employer responsibility

*Source: Decomposition Section 1.2 — Contractor scope only; PKG-24 deliverable structure*

### Interface Scope

**Critical interfaces:**
- Integration with Terminal security network per DEC-05 (CCTV, access control, communications treated as separate systems with distinct interfaces)
- Coordination with PKG-03 (Underground Utilities) for conduit routing
- Coordination with PKG-17 (Electrical Power) for power supply points
- Coordination with PKG-25 (Communications & IT) for network infrastructure
- Coordination with PKG-21/PKG-22 (Buildings) for building-mounted equipment

*Source: DEC-05 (Decomposition Section 7); package interdependencies*

## Requirements

### Functional Requirements

#### FR-1: CCTV Coverage
- **FR-1.1**: Drawings shall define camera locations providing continuous coverage of:
  - **TBD** — All tank farm areas per ER requirements
  - **TBD** — Railcar unloading stations
  - **TBD** — Marine loading berth and loading arms
  - **TBD** — Site perimeter and access gates
  - **TBD** — Other critical areas per ER security requirements

- **FR-1.2**: Camera coverage drawings shall demonstrate:
  - **TBD** — Minimum pixel density for facial recognition at key points
  - **TBD** — Elimination of blind spots in critical areas
  - **TBD** — Adequate illumination levels (coordinate with PKG-18 Lighting)
  - **TBD** — Field-of-view calculations and verification

*Source: Typical CCTV system design requirements; specifics TBD per ER*

#### FR-2: Access Control Coverage
- **FR-2.1**: Drawings shall define access control points at:
  - **TBD** — Site entrance gates
  - **TBD** — Building access doors
  - **TBD** — Restricted area boundaries
  - **TBD** — Emergency egress points (with appropriate fail-safe/fail-secure designation)

- **FR-2.2**: Access control layout shall show:
  - Card reader locations and door hardware
  - Access control panel/controller locations
  - Integration points with door position switches, request-to-exit devices
  - Power and data connection points

*Source: Typical access control system design requirements; specifics TBD per ER*

#### FR-3: Terminal Integration
- **FR-3.1**: Drawings shall define integration architecture with existing DP World Fraser Surrey Terminal security systems per DEC-05
- **FR-3.2**: Network topology shall show:
  - **TBD** — Physical and logical network segregation
  - **TBD** — Firewall locations and security zones
  - **TBD** — Connection points to Terminal network
  - **TBD** — Monitoring/control data flow paths

*Source: DEC-05 (Decomposition Section 7) — Terminal network interfaces*

### Performance Requirements

#### PR-1: Drawing Quality and Accuracy
- **PR-1.1**: All drawings shall be dimensionally accurate and coordinated with civil/structural/architectural base drawings
- **PR-1.2**: Camera coverage analysis shall demonstrate **TBD** lux minimum illumination at night (coordinate with PKG-18)
- **PR-1.3**: Coverage calculations shall assume **TBD** camera specifications (resolution, lens, mounting height)

*Source: Standard drawing production requirements*

#### PR-2: Design Standards Compliance
- **PR-2.1**: Drawings shall comply with:
  - **TBD** — Project CAD standards and layering conventions
  - **TBD** — DP World Fraser Surrey Terminal drawing standards (if applicable)
  - **TBD** — Applicable security industry standards (IEC 62676 series, ONVIF) **ASSUMPTION**

#### PR-3: Constructability
- **PR-3.1**: Drawings shall clearly define installation requirements and constraints
- **PR-3.2**: Cable routing shall consider:
  - **TBD** — Separation from power cables per electrical code
  - **TBD** — Hazardous area classification boundaries
  - **TBD** — Physical protection requirements in vehicle/equipment traffic areas

### Interface Requirements

#### IR-1: Interdisciplinary Coordination
- **IR-1.1**: CCTV camera locations shall be coordinated with:
  - Structural steel (PKG-06) and concrete structures (PKG-05) for mounting points
  - Lighting (PKG-18) for adequate illumination
  - Electrical power (PKG-17) for power supply routing

- **IR-1.2**: Underground conduit routing shall be coordinated with:
  - PKG-03 (Underground Utilities & Drainage) for trenching and conduit installation
  - PKG-04 (Pavement & Surfacing) for bore/trench restoration

- **IR-1.3**: Building-mounted equipment shall be coordinated with:
  - PKG-21 (Building Structures) for structural mounting provisions
  - PKG-22 (Building Interior & MEP) for interior equipment rooms and cable routing

*Source: Standard interdisciplinary coordination requirements; dependencies NOT_TRACKED per `_DEPENDENCIES.md`*

#### IR-2: Employer Interface
- **IR-2.1**: Integration approach and connection details shall be reviewed and accepted by Employer **TBD** — review milestone
- **IR-2.2**: Drawings shall accommodate existing Terminal security infrastructure constraints **TBD** — existing conditions survey required

### Quality Requirements

#### QR-1: Review and Approval Process
- **QR-1.1**: All drawings shall undergo:
  - Self-check by originator
  - Interdisciplinary check (IDC) with affected disciplines
  - Independent technical check by qualified checker
  - Approval by discipline lead or designated approver

*Source: Standard engineering deliverable quality process*

#### QR-2: Drawing Standards
- **QR-2.1**: All drawings shall comply with project Quality Management Plan
- **QR-2.2**: Drawing format, title blocks, and notation shall follow **TBD** — project CAD manual
- **QR-2.3**: Revisions shall be clearly identified per **TBD** — project revision control procedures

#### QR-3: Traceability
- **QR-3.1**: Design decisions shall be traceable to ER requirements **TBD** — ER section references
- **QR-3.2**: Coverage analysis assumptions and calculations shall be documented
- **QR-3.3**: Interface agreements with Terminal security systems shall be documented

### Safety and Regulatory Requirements

#### SR-1: Safe Design
- **SR-1.1**: Design shall support Safe & Reliable Operation (OBJ-1) by providing:
  - Continuous monitoring of hazardous process areas
  - Access control to restricted/hazardous zones
  - Integration with emergency response systems **TBD** — coordination with fire alarm (PKG-23)

*Source: OBJ-1 (Decomposition Section 2)*

#### SR-2: Regulatory Compliance (OBJ-6)
- **SR-2.1**: Design shall comply with:
  - **TBD** — Applicable provincial and federal security regulations
  - **TBD** — Port authority security requirements
  - **TBD** — Privacy legislation for video surveillance (PIPEDA) **ASSUMPTION**
  - National Building Code of Canada 2020 — for structural mounting **ASSUMPTION**

*Source: OBJ-6 (Decomposition Section 2) — Regulatory Compliance*

#### SR-3: Hazardous Area Compliance
- **SR-3.1**: Equipment locations and installation methods shall comply with hazardous area classification **TBD** — per facility area classification drawings
- **SR-3.2**: Cameras and equipment in classified areas shall be rated for appropriate Class/Division/Zone **TBD**

## Standards

### Governing Codes and Standards

**Canadian Codes:**
- National Building Code of Canada (NBC) 2020 **ASSUMPTION**
- Canadian Electrical Code (CSA C22.1) — for electrical installation **ASSUMPTION**
- British Columbia Building Code **ASSUMPTION**

**Security Industry Standards (ASSUMPTION — to be confirmed per ER):**
- **TBD** — IEC 62676 series (Video surveillance systems)
- **TBD** — ONVIF Profile S/T (network video device interoperability)
- **TBD** — OSDP (Open Supervised Device Protocol) for access control
- **TBD** — ASIS/SIA standards for physical security systems

**Project-Specific:**
- Employer's Requirements Volume 2 Parts 1-3 **TBD** — specific ER sections for security systems
- **TBD** — DP World Fraser Surrey Terminal security standards and procedures
- **TBD** — Project CAD Standards Manual

### Drawing Standards

- **TBD** — Project CAD layering and symbology standards
- **TBD** — ANSI Y14.5 or ISO 128 for dimensioning and tolerancing **ASSUMPTION**
- **TBD** — CSA drafting standards for Canadian engineering drawings **ASSUMPTION**

## Verification

### Verification Methods

#### Design Review
- **Peer check** by independent qualified engineer (not originator)
- **Interdisciplinary check (IDC)** with:
  - Civil/structural for mounting and routing
  - Electrical for power supply
  - Communications for network infrastructure
  - Fire protection for alarm integration **TBD**
- **Employer review** at **TBD** — design stage (30%/60%/90%/IFC)

#### Coverage Verification
- **Field-of-view calculations** for each camera location
- **Coverage gap analysis** using camera coverage software **TBD** — tool to be specified
- **Illumination coordination** with lighting design (PKG-18)
- **Mock-up or site walk** to verify mounting feasibility **TBD** — if required by Employer

#### CAD Standards Compliance
- **Automated CAD check** per project standards **TBD** — CAD QC tool
- **Drawing index verification** — completeness check against drawing list
- **Cross-reference verification** — ensure all referenced drawings exist and are current

### Acceptance Criteria

**Design Acceptance:**
- All ER requirements for security coverage are addressed **TBD** — ER requirements checklist
- Coverage analysis demonstrates no critical blind spots
- Integration approach accepted by Employer/Terminal security operations
- All IDC comments resolved and closed

**Drawing Acceptance:**
- All drawings checked and approved per quality procedures
- Drawing register complete and current
- CAD standards compliance verified
- All revisions properly tracked and documented

**Completion Criteria:**
- Drawing set issued for construction (IFC status)
- Employer acceptance obtained
- All review comments incorporated
- Drawing transmittal completed per document control procedures

## Documentation

### Required Documentation Outputs

**Primary Deliverables:**
1. **CCTV Layout Drawings**
   - Site-wide camera location plan
   - Coverage zone overlay drawings
   - Mounting height and orientation details

2. **Camera Coverage Drawings**
   - Field-of-view diagrams per zone
   - Coverage analysis calculations
   - Illumination coordination notes

3. **Access Control Layout Drawings**
   - Card reader and controller locations
   - Door hardware and devices schedule
   - Cable routing and connection diagrams

**Supporting Documents (ASSUMPTION):**
4. System architecture diagram
5. Integration interface drawing (Terminal security network)
6. Typical mounting and installation details

*Source: `_CONTEXT.md` — Anticipated Artifacts; typical drawing set structure*

### Documentation Requirements

**Format and Media:**
- **Drawing format:** **TBD** — DWG (native CAD) and PDF (sealed) **ASSUMPTION**
- **Sheet size:** **TBD** — ANSI D (24"×36") or as specified **ASSUMPTION**
- **Transmittal:** Via project document management system **TBD**

**Revision Control:**
- Drawing numbering per **TBD** — project numbering system
- Revision tracking per **TBD** — project revision control procedures
- All revisions clearly identified with revision clouds and delta notes

**Record Management:**
- Electronic files stored in project document management system **TBD**
- Record drawings updated per as-built markup process
- Retention per project records management plan **TBD**

### Supporting Documentation

- **Design calculations:** Coverage analysis and camera placement rationale
- **Interdisciplinary coordination log:** IDC meeting notes and resolution records
- **ER compliance matrix:** Traceability of design to ER requirements **TBD**
- **Interface agreements:** Documented agreements with Terminal security operations **TBD**

---

*Document status: Enriched draft — Pass 1*
*Enrichment date: 2026-01-28*
*Cross-references: Datasheet.md for system attributes; Procedure.md for production workflow*
