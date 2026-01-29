# Specification: DEL-24.03 Security System Data Sheet Package

## Scope

This specification defines the requirements for assembling and submitting the **Security System Data Sheet Package** within **PKG-24 Security Systems** for the Canola Oil Transload Facility — Phase 1 at Fraser Surrey Terminal.

**Purpose:** Defines and substantiates security system in accordance with ER requirements by providing equipment datasheets that demonstrate compliance with DEL-24.02 (Technical Specification).

*Source: `_CONTEXT.md`; Decomposition Section 5 — PKG-24 (line 568)*

### Inclusions

The data sheet package shall include equipment datasheets and supporting documentation for:
- CCTV cameras (fixed and PTZ) with technical specifications and certifications
- Network video recorders (NVR) and storage systems
- Video management system (VMS) software and licensing
- Access control card readers and biometric devices
- Access control controllers/panels and software
- Door hardware (electric strikes, magnetic locks, crash bars, REX devices, door position switches)
- Network infrastructure (switches, fiber optic equipment, cabling)
- Power supplies and UPS systems
- Mounting hardware and accessories

*Source: `_CONTEXT.md` — Anticipated Artifacts; Datasheet.md — Equipment scope*

### Exclusions

The following are outside the scope of this data sheet package:
- Design drawings and layouts (covered under DEL-24.01)
- Technical specifications for procurement (covered under DEL-24.02)
- Installation procedures and test records (covered under DEL-24.04)
- Operations and maintenance manuals **ASSUMPTION** — provided separately or as part of closeout
- As-built documentation **ASSUMPTION** — developed post-installation

*Source: PKG-24 deliverable structure*

### Interface Scope

**Critical interfaces:**
- DEL-24.01 (Design Drawings) — Equipment locations, types, and quantities
- DEL-24.02 (Technical Specification) — Equipment performance requirements that datasheets must demonstrate compliance with
- DEL-24.04 (Installation & Test Records) — Installed equipment verification
- Terminal integration requirements per DEC-05 — Equipment compatibility with Terminal security systems

*Source: PKG-24 deliverable relationships; DEC-05 (Decomposition Section 7)*

## Requirements

### Functional Requirements

#### FR-1: Data Sheet Package Structure and Organization
- **FR-1.1**: The package shall be organized by equipment category:
  - Section 1: CCTV System (cameras, NVR, VMS)
  - Section 2: Access Control System (readers, controllers, software, door hardware)
  - Section 3: Network Infrastructure (switches, cabling, fiber equipment)
  - Section 4: Power and UPS
  - Section 5: Accessories and miscellaneous equipment

- **FR-1.2**: Each equipment category shall include:
  - Equipment schedule/list with quantities and tag numbers per DEL-24.01
  - Individual equipment datasheets
  - Compliance matrix showing how equipment meets DEL-24.02 requirements

- **FR-1.3**: Package shall include table of contents and equipment index for easy navigation

*Source: Standard equipment submittal package organization*

#### FR-2: Equipment Datasheet Content Requirements
- **FR-2.1**: Each equipment datasheet shall include:
  - Manufacturer and model identification
  - Equipment tag number per design (DEL-24.01)
  - Technical specifications (performance, physical, electrical, environmental)
  - Compliance certifications (UL, CSA, IP/IK ratings, etc.)
  - Installation instructions summary or reference
  - Warranty information

- **FR-2.2**: Datasheets shall clearly demonstrate compliance with DEL-24.02 specification requirements
  - Include compliance matrix or narrative for each equipment type
  - Highlight specifications that meet or exceed requirements
  - Provide justification for any deviations or "approved equivalent" claims

*Source: DEL-24.02 submittal requirements; standard equipment datasheet content*

#### FR-3: CCTV Equipment Data Sheet Requirements
- **FR-3.1**: Camera datasheets shall include:
  - Image sensor specifications (resolution, sensor size, sensitivity)
  - Lens specifications (focal length, field of view, aperture)
  - Performance specifications (frame rate, compression, low-light capability, WDR)
  - Environmental ratings (IP, IK, operating temperature range)
  - Power requirements (PoE class, voltage, current)
  - ONVIF compliance certification **ASSUMPTION**
  - Mounting options and accessories

- **FR-3.2**: NVR datasheets shall include:
  - Recording capacity (channels, resolution, storage capacity, retention period calculations)
  - Storage architecture (RAID level, drive configuration, hot-swap capability)
  - Network specifications (throughput, bandwidth, network interfaces)
  - Redundancy features (if applicable) **TBD**
  - VMS compatibility

- **FR-3.3**: VMS datasheets shall include:
  - Software features and capabilities (live view, playback, alarm management, reporting)
  - Licensing model and quantities
  - System requirements (servers, workstations)
  - ONVIF compliance and integration APIs
  - Integration capability with Terminal systems per DEC-05 **TBD**

*Source: DEL-24.02 CCTV system requirements; typical CCTV equipment datasheet content*

#### FR-4: Access Control Equipment Data Sheet Requirements
- **FR-4.1**: Card reader datasheets shall include:
  - Technology (proximity, smart card, biometric) and frequency/standard
  - Read range and performance
  - Supported credential types
  - Communication protocol (OSDP, Wiegand) and wiring requirements
  - Environmental ratings (IP, IK, operating temperature)
  - Tamper detection features

- **FR-4.2**: Access control controller datasheets shall include:
  - System architecture (distributed/centralized)
  - Capacity (doors, credentials, events)
  - Communication specifications (TCP/IP, encryption)
  - Battery backup specifications (capacity, duration)
  - Input/output specifications (door position, REX, alarm inputs)
  - Fail-safe/fail-secure configuration capability

- **FR-4.3**: Door hardware datasheets shall include:
  - Electric strikes: Grade, holding force, voltage, fail-safe/fail-secure designation
  - Magnetic locks: Holding force, voltage, fail-safe operation
  - Crash bars/panic devices: Grade, fire rating, ADA compliance
  - Door position switches and REX devices: Type, specifications, mounting

- **FR-4.4**: Access control software datasheets shall include:
  - Software features (user management, access levels, audit trails, reporting)
  - System requirements (servers, workstations, database)
  - Licensing model
  - Integration capability with Terminal access control platform per DEC-05 **TBD**

*Source: DEL-24.02 access control system requirements; typical access control equipment datasheet content*

#### FR-5: Supporting Documentation Requirements
- **FR-5.1**: Compliance certifications shall be included:
  - UL/CSA listings for electrical safety
  - FCC compliance for RF devices
  - IP rating certifications (IEC 60529)
  - IK rating certifications (IEC 62262)
  - ONVIF certifications for IP cameras
  - Hazardous area certifications where required **TBD**

- **FR-5.2**: Factory Acceptance Testing (FAT) documentation (if required for major equipment) **TBD**:
  - FAT test procedures and acceptance criteria
  - FAT test results and certifications
  - Deficiency resolution documentation

- **FR-5.3**: Integration documentation for Terminal interface per DEC-05:
  - Protocol specifications and API documentation
  - Configuration guides for integration
  - Compatibility certification or test results

*Source: DEL-24.02 quality and integration requirements; DEC-05*

### Performance Requirements

#### PR-1: Compliance Demonstration
- **PR-1.1**: All equipment shall meet or exceed DEL-24.02 specification requirements
- **PR-1.2**: Compliance matrix shall clearly show requirement vs. equipment specification comparison
- **PR-1.3**: Any deviations or "approved equivalent" substitutions shall be clearly identified with technical justification

#### PR-2: Documentation Quality
- **PR-2.1**: Datasheets shall be current manufacturer literature (not obsolete or superseded products)
- **PR-2.2**: All datasheets shall be legible, complete, and in English (or bilingual English/French for Canadian standards)
- **PR-2.3**: Package shall be professionally compiled and indexed for easy review

#### PR-3: Environmental and Regulatory Compliance
- **PR-3.1**: Equipment shall meet environmental requirements for Fraser Surrey Terminal coastal marine environment:
  - Outdoor equipment: IP66/IP67 minimum, corrosion-resistant materials
  - Vandal-prone locations: IK10 impact resistance
  - Operating temperature: -20°C to +40°C for outdoor equipment **ASSUMPTION**

- **PR-3.2**: Equipment shall meet Canadian regulatory requirements:
  - CSA or UL listing for electrical safety
  - Canadian Electrical Code (CEC) compliance
  - NBC 2020 compliance for structural mounting
  - Hazardous area ratings where required **TBD**

*Source: Datasheet.md — Environmental conditions; DEL-24.02 environmental and regulatory requirements*

### Interface Requirements

#### IR-1: Design Coordination
- **IR-1.1**: Equipment selections shall align with design (DEL-24.01):
  - Quantities match equipment schedules from design drawings
  - Equipment types match design intent (fixed vs. PTZ cameras, reader technology, etc.)
  - Mounting methods compatible with design details

- **IR-1.2**: Equipment specifications shall achieve design performance objectives:
  - Camera specifications support coverage analysis requirements
  - NVR capacity supports retention period requirements
  - Access control capacity supports facility access level structure

*Source: DEL-24.01 as design basis*

#### IR-2: Specification Compliance
- **IR-2.1**: All equipment shall comply with DEL-24.02 Technical Specification requirements
- **IR-2.2**: Any proposed substitutions or "approved equivalents" shall be submitted for approval with technical justification
- **IR-2.3**: Approved manufacturers list (if specified in DEL-24.02) shall be followed **TBD**

*Source: DEL-24.02 as specification basis*

#### IR-3: Terminal Integration Compatibility
- **IR-3.1**: Equipment proposed for Terminal integration shall be verified compatible with existing Terminal systems per DEC-05:
  - CCTV equipment compatible with Terminal VMS platform **TBD**
  - Access control equipment compatible with Terminal access control platform **TBD**
  - Network equipment compatible with Terminal network architecture **TBD**

*Source: DEC-05 (Decomposition Section 7)*

### Quality Requirements

#### QR-1: Submittal Review Process
- **QR-1.1**: Data sheet package shall be submitted for review and approval per project submittal procedures **TBD**
- **QR-1.2**: Submittal shall be reviewed by:
  - Designer for compliance with DEL-24.01 design and DEL-24.02 specification
  - Employer for acceptance and Terminal integration compatibility **TBD**

- **QR-1.3**: Submittal status shall be clearly marked:
  - Submitted for Approval
  - Approved (no exceptions)
  - Approved as Noted (minor comments, proceed with noted corrections)
  - Revise and Resubmit (significant issues, resubmittal required)
  - Rejected (not acceptable, major non-compliance)

#### QR-2: Resubmittal Requirements
- **QR-2.1**: If resubmittal required, contractor shall:
  - Address all review comments
  - Provide written responses to each comment
  - Clearly identify changes in resubmitted datasheets
  - Resubmit within required timeframe **TBD**

#### QR-3: Approved Equipment Record
- **QR-3.1**: Approved data sheet package becomes contract document for equipment procurement
- **QR-3.2**: No substitutions allowed after approval without formal change process
- **QR-3.3**: Installed equipment shall match approved datasheets (verified during installation and testing per DEL-24.04)

### Safety and Regulatory Requirements

#### SR-1: Electrical Safety
- **SR-1.1**: All equipment shall be approved for Canadian market:
  - CSA certification preferred, UL certification acceptable **ASSUMPTION**
  - Equipment shall comply with Canadian Electrical Code (CEC / CSA C22.1)

#### SR-2: Hazardous Area Compliance
- **SR-2.1**: Equipment for hazardous area installation shall have appropriate area classification ratings **TBD**
- **SR-2.2**: Installation methods shall comply with CEC hazardous area requirements

#### SR-3: Life Safety Integration
- **SR-3.1**: Access control equipment shall be compatible with fire/life safety requirements:
  - Fail-safe operation where required for emergency egress
  - Integration with fire alarm system (coordinate with PKG-23)

*Source: DEL-24.02 safety and regulatory requirements; PKG-23 interface*

## Standards

### Governing Standards

**Equipment Certification Standards:**
- UL/CSA standards for electrical safety
- IEC 60529 (IP ratings) for ingress protection
- IEC 62262 (IK ratings) for impact resistance
- FCC Part 15 for RF devices
- ONVIF profiles for IP camera interoperability **ASSUMPTION**
- OSDP for access control communication **ASSUMPTION**

**Canadian Regulatory Standards:**
- Canadian Electrical Code (CSA C22.1)
- National Building Code of Canada (NBC) 2020
- Privacy legislation (PIPEDA) for video surveillance **ASSUMPTION**

**Project-Specific:**
- Employer's Requirements Volume 2 Parts 1-3 **TBD**
- DEL-24.02 (Security System Technical Specification) — governing specification for equipment requirements
- **TBD** — DP World Fraser Surrey Terminal equipment standards

## Verification

### Verification Methods

#### Submittal Review
- **Designer review:** Verify compliance with DEL-24.01 design and DEL-24.02 specification
- **Compliance matrix review:** Verify all specification requirements addressed
- **Certification review:** Verify all required certifications included and valid
- **Integration review:** Verify Terminal compatibility per DEC-05 (coordinate with Employer/Terminal IT)

#### Technical Evaluation
- **Performance verification:** Compare equipment specifications to design requirements (coverage analysis, capacity, etc.)
- **Environmental suitability:** Verify equipment ratings appropriate for Fraser Surrey Terminal coastal marine environment
- **Compatibility verification:** Verify equipment interoperability (cameras with NVR/VMS, readers with controllers, etc.)

#### Employer Acceptance
- **Employer review:** Review for acceptability and Terminal integration approval
- **Terminal operations review:** Verify compatibility with existing Terminal security systems and procedures

### Acceptance Criteria

**Data Sheet Package Acceptance:**
- All equipment datasheets complete and current
- Compliance matrix demonstrates compliance with DEL-24.02 for all equipment
- Required certifications included and valid
- Integration documentation acceptable for Terminal interface per DEC-05
- Designer review comments resolved
- Employer acceptance obtained

**Equipment Approval:**
- Equipment meets or exceeds DEL-24.02 specification requirements
- Environmental ratings appropriate for application
- Required certifications valid
- Terminal integration verified (where applicable)
- Substitutions (if any) justified and accepted

**Completion Criteria:**
- Data sheet package approved (or approved as noted)
- Approved equipment becomes contract document
- Procurement may proceed based on approved equipment
- Package filed in project document management system and deliverable folder `3_Issued/`

## Documentation

### Required Documentation Outputs

**Primary Deliverable:**
- **Security System Data Sheet Package** — organized equipment submittal package including:
  - Section 1: CCTV System equipment datasheets
  - Section 2: Access Control System equipment datasheets
  - Section 3: Network Infrastructure equipment datasheets
  - Section 4: Power and UPS equipment datasheets
  - Section 5: Accessories and miscellaneous equipment
  - Appendices: Certifications, FAT documentation (if applicable), integration documentation

**Anticipated Equipment Datasheets:**
1. Camera datasheets (multiple models/types) — per DEL-24.01 design quantities
2. NVR datasheet(s)
3. VMS software datasheet and licensing
4. Card reader datasheets (multiple locations)
5. Access control controller datasheets
6. Access control software datasheet and licensing
7. Door hardware datasheets (electric strikes, magnetic locks, crash bars, REX, door position switches)
8. Network switch datasheets
9. Fiber optic equipment datasheets
10. UPS and power supply datasheets
11. Mounting hardware and accessories (as required)

*Source: `_CONTEXT.md` — Anticipated Artifacts; Datasheet.md*

### Documentation Requirements

**Format and Media:**
- **Package format:** PDF compilation with table of contents and index **ASSUMPTION**
- **Individual datasheets:** Manufacturer original PDFs or literature
- **Transmittal:** Via project document management system **TBD**

**Organization:**
- Clear table of contents with section numbers and page numbers
- Equipment index with tag numbers cross-referenced to datasheets
- Compliance matrices at section level or equipment level
- Certifications in appendices

**Revision Control:**
- Package document number per **TBD** — project numbering system
- Revision tracking per **TBD** — project revision control procedures
- Resubmittals clearly identified with revision summary

**Record Management:**
- Electronic files stored in project document management system **TBD**
- Approved package archived in deliverable folder `3_Issued/`
- Approved datasheets referenced during procurement and installation
- Retention per project records management plan **TBD**

### Supporting Documentation

- **Compliance matrices:** Requirement-by-requirement comparison (DEL-24.02 vs. equipment specifications)
- **Equipment schedules:** List of all equipment with tag numbers, quantities, locations (from DEL-24.01)
- **Substitution requests:** Documentation of any proposed substitutions with technical justification
- **Review comment responses:** Written responses to designer and Employer review comments

**Cross-References to Related Deliverables:**
- DEL-24.01 — Design basis for equipment locations and quantities
- DEL-24.02 — Specification basis for equipment requirements
- DEL-24.04 — Installation and test records (verification that installed equipment matches approved submittals)

---

*Document status: Enriched draft — Pass 1*
*Enrichment date: 2026-01-28*
*Cross-references: Datasheet.md for equipment scope; Guidance.md for submittal development principles; Procedure.md for submittal workflow*
