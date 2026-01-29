# Specification: DEL-24.02 Security System Technical Specification

## Scope

This specification defines the requirements for producing the **Security System Technical Specification** within **PKG-24 Security Systems** for the Canola Oil Transload Facility — Phase 1 at Fraser Surrey Terminal.

**Purpose:** Defines performance, materials, and workmanship requirements for security system per ER requirements.

*Source: `_CONTEXT.md`; Decomposition Section 5 — PKG-24 (line 567)*

### Inclusions

The technical specification document shall include:
- CCTV system performance and materials specification
- Access control system performance and materials specification
- Network infrastructure requirements for security systems
- Installation and workmanship standards
- Testing and acceptance criteria
- Integration requirements with Terminal security network per DEC-05
- Quality assurance and quality control requirements

*Source: `_CONTEXT.md` — Anticipated Artifacts; Decomposition Section 5 — PKG-24 scope; DEC-05 (Section 7)*

### Exclusions

The following are outside the scope of this technical specification:
- Design drawings and layouts (covered under DEL-24.01)
- Equipment datasheets and submittals (covered under DEL-24.03)
- Installation and test records (covered under DEL-24.04)
- Detailed installation procedures **ASSUMPTION** — may be included as an appendix or referenced separately
- Security operations procedures **ASSUMPTION** — Employer/Terminal responsibility
- Procurement specifications for individual equipment **ASSUMPTION** — derived from this technical specification for procurement packages

*Source: PKG-24 deliverable structure; standard technical specification scope boundaries*

### Interface Scope

**Critical interfaces:**
- Integration with Terminal security network per DEC-05 (CCTV, access control, communications as separate system interfaces)
- Coordination with PKG-17 (Electrical Power) for power supply requirements and specifications
- Coordination with PKG-23 (Fire Protection) for access control integration with fire alarm/life safety systems
- Coordination with PKG-25 (Communications & IT) for network infrastructure specifications
- Coordination with design drawings (DEL-24.01) — this specification supports the design intent defined in drawings

*Source: DEC-05 (Decomposition Section 7); package interdependencies*

## Requirements

### Functional Requirements

#### FR-1: Technical Specification Document Structure
- **FR-1.1**: The specification shall be structured per **TBD** — CSI MasterFormat divisions or narrative format
- **FR-1.2**: The specification shall include the following major sections (minimum):
  - Section 1: General Requirements (scope, references, submittals, quality assurance, delivery/storage/handling, warranties)
  - Section 2: Products (CCTV system, access control system, network infrastructure, materials)
  - Section 3: Execution (installation, testing, commissioning, closeout)
- **FR-1.3**: The specification shall be organized to support procurement and construction activities
- **FR-1.4**: The specification shall clearly define acceptance criteria for equipment and installation

*Source: Standard technical specification structure (CSI MasterFormat) **ASSUMPTION***

#### FR-2: CCTV System Performance Requirements
- **FR-2.1**: The specification shall define camera performance requirements:
  - Resolution, frame rate, compression codec
  - Low-light performance (minimum lux rating)
  - Field of view and lens specifications to support design (DEL-24.01)
  - Environmental ratings (IP, IK, operating temperature)
  - Power requirements (PoE class, voltage)

- **FR-2.2**: The specification shall define NVR/recording system requirements:
  - Recording capacity (channels, resolution, frame rate, retention period)
  - Storage architecture (RAID level, redundancy, hot-swap capability)
  - Network throughput and bandwidth
  - Failover and redundancy features **TBD**

- **FR-2.3**: The specification shall define VMS requirements:
  - Software functionality (live view, playback, export, alarm management, reporting)
  - User interface and multi-monitor support
  - ONVIF compliance for interoperability **ASSUMPTION**
  - Integration APIs and protocols **TBD**

*Source: Typical CCTV technical specification content; specifics TBD per ER and design (DEL-24.01)*

#### FR-3: Access Control System Performance Requirements
- **FR-3.1**: The specification shall define card reader requirements:
  - Technology (proximity, smart card, biometric) and frequency/standard
  - Read range and performance
  - Environmental ratings and vandal resistance
  - Communication protocol (OSDP, Wiegand) **TBD**

- **FR-3.2**: The specification shall define access control panel/controller requirements:
  - System architecture (distributed/centralized)
  - Capacity (doors per panel, credentials per system)
  - Communication (TCP/IP, encryption)
  - Battery backup duration
  - Fail-safe/fail-secure configuration capability

- **FR-3.3**: The specification shall define door hardware requirements:
  - Electric strikes, magnetic locks specifications (grade, holding force, materials)
  - Crash bars and panic devices coordination with fire/life safety (PKG-23)
  - Door position switches and request-to-exit devices

- **FR-3.4**: The specification shall define access control software requirements:
  - User management and access level administration
  - Audit trail and reporting capability
  - Alarm handling and monitoring
  - Integration with Terminal access control system per DEC-05 **TBD**

*Source: Typical access control technical specification content; DEC-05 (Decomposition Section 7)*

#### FR-4: Network Infrastructure Requirements
- **FR-4.1**: The specification shall define cabling requirements:
  - Cable types (Cat6A, fiber optic) and performance specifications
  - Installation standards (TIA-568) **ASSUMPTION**
  - Environmental ratings (outdoor, plenum, hazardous area)

- **FR-4.2**: The specification shall define network equipment requirements:
  - PoE switch specifications (power budget, port count, PoE class support)
  - Managed switch features (VLAN, QoS, IGMP snooping, redundancy)
  - Fiber optic patch panels and termination equipment

- **FR-4.3**: The specification shall define network architecture requirements:
  - VLAN segregation for security systems
  - Bandwidth and throughput calculations
  - Firewall requirements for Terminal integration per DEC-05
  - Redundancy and failover topology **TBD**

*Source: Typical IP security system network specifications; DEC-05*

#### FR-5: Environmental and Durability Requirements
- **FR-5.1**: The specification shall define environmental ratings for equipment:
  - IP ratings (IP65/IP66/IP67 for outdoor equipment)
  - IK ratings (IK08/IK10 for vandal-prone locations)
  - Operating temperature range (-30°C to +60°C for outdoor) **ASSUMPTION**
  - Humidity, salt spray, UV resistance for marine/coastal environment

- **FR-5.2**: The specification shall define materials requirements:
  - Corrosion-resistant materials (stainless steel, powder-coated aluminum) for coastal environment
  - Marine-grade materials where exposed to salt spray
  - Suitable for industrial hazardous area classification **TBD**

*Source: Environmental conditions at Fraser Surrey Terminal (coastal marine environment); Datasheet.md*

#### FR-6: Integration and Interoperability Requirements
- **FR-6.1**: The specification shall define Terminal integration requirements per DEC-05:
  - CCTV integration: Protocol, data format, connection topology **TBD**
  - Access control integration: Credential synchronization, event logging **TBD**
  - Network integration: Security zones, firewall rules, VPN/secure tunnel **TBD**

- **FR-6.2**: The specification shall require open protocols and standards where possible:
  - ONVIF for CCTV interoperability **ASSUMPTION**
  - OSDP for access control communication **ASSUMPTION**
  - Standard TCP/IP networking

*Source: DEC-05 (Decomposition Section 7) — Terminal network interfaces as separate systems; industry best practice for open standards*

### Performance Requirements

#### PR-1: Reliability and Availability
- **PR-1.1**: Security systems shall support 24/7/365 continuous operation
- **PR-1.2**: Target system availability: **TBD** — 99.5%+ uptime (supports OBJ-1 Safe & Reliable Operation)
- **PR-1.3**: Equipment MTBF shall be specified per manufacturer data and verified during FAT **TBD**
- **PR-1.4**: Redundancy shall be provided for critical components **TBD** — NVR, network switches, power supplies

*Source: OBJ-1 (Decomposition Section 2) — Safe & Reliable Operation; typical industrial security system reliability requirements*

#### PR-2: Recording and Storage
- **PR-2.1**: Video recording retention period: **TBD** — typical 30-90 days
- **PR-2.2**: Recording shall be continuous 24/7 for all cameras (or motion-activated **TBD**)
- **PR-2.3**: Storage shall support specified resolution, frame rate, and retention without data loss
- **PR-2.4**: Video export capability for incident investigation **TBD** — formats, authentication

#### PR-3: Image Quality and Coverage
- **PR-3.1**: Image quality shall support operational requirements:
  - Identification level: Facial recognition at access control points **TBD** — minimum pixel density
  - Recognition level: Person identification in restricted areas **TBD**
  - Detection level: Activity detection at perimeter **TBD**
  - Monitoring level: General situational awareness **TBD**

- **PR-3.2**: Image quality shall be verified against design coverage analysis (DEL-24.01)

*Source: Typical CCTV performance requirements; coordinate with DEL-24.01 coverage design*

#### PR-4: Access Control Performance
- **PR-4.1**: Card reader read range: **TBD** — 2-10 cm typical depending on technology
- **PR-4.2**: Door unlock time: **TBD** — <2 seconds from card presentation to door unlock typical
- **PR-4.3**: Access decision processing: Real-time with **TBD** — <1 second latency
- **PR-4.4**: Audit trail logging: All access events, alarm events, system events logged with timestamp and user/location

### Interface Requirements

#### IR-1: Interdisciplinary Coordination
- **IR-1.1**: Electrical power requirements shall be coordinated with PKG-17:
  - Power supply locations and circuit requirements
  - UPS/battery backup sizing and locations
  - Grounding and surge protection

- **IR-1.2**: Fire/life safety integration shall be coordinated with PKG-23:
  - Access control fail-safe configuration for emergency egress
  - Integration with fire alarm system (door unlock on fire alarm)
  - Delayed egress where permitted by code

- **IR-1.3**: Network infrastructure shall be coordinated with PKG-25:
  - Backbone network capacity and routing
  - Switch locations and power requirements
  - Fiber optic termination points

*Source: Standard interdisciplinary coordination requirements; dependencies NOT_TRACKED per `_DEPENDENCIES.md`*

#### IR-2: Employer/Terminal Interface
- **IR-2.1**: Integration specifications shall be reviewed and accepted by Employer/Terminal IT and security operations **TBD** — review milestone
- **IR-2.2**: Equipment standards and approved manufacturers list **TBD** — from ER or Employer standards
- **IR-2.3**: Compatibility with existing Terminal security infrastructure shall be verified **TBD**

### Quality Requirements

#### QR-1: Specification Development and Review Process
- **QR-1.1**: Specification shall be developed from design basis (DEL-24.01) and ER requirements
- **QR-1.2**: Specification shall undergo:
  - Technical review by discipline lead
  - Interdisciplinary review for interface coordination
  - Employer review and acceptance **TBD** — at specified design milestone
  - Constructability review **TBD** — input from construction/installation team

#### QR-2: Equipment Quality and Testing
- **QR-2.1**: All equipment shall be new, current manufacturer model, approved for project use
- **QR-2.2**: Equipment shall be factory tested per manufacturer QC procedures
- **QR-2.3**: Major equipment shall undergo Factory Acceptance Testing (FAT) **TBD** — define scope
- **QR-2.4**: Equipment submittals (DEL-24.03) shall demonstrate compliance with technical specification

#### QR-3: Installation Quality
- **QR-3.1**: Installation shall be by qualified security systems integrator **TBD** — certification requirements
- **QR-3.2**: Installation shall follow manufacturer instructions and applicable codes
- **QR-3.3**: Workmanship shall meet industry standards and project quality plan
- **QR-3.4**: Installation shall be verified per testing procedures (PKG-29, DEL-24.04)

### Safety and Regulatory Requirements

#### SR-1: Safe Design and Installation (OBJ-1)
- **SR-1.1**: Equipment selection and installation shall support Safe & Reliable Operation (OBJ-1):
  - Hazardous area ratings where required **TBD**
  - Proper electrical grounding and bonding
  - Equipment protection from physical damage
  - Safe access for maintenance

*Source: OBJ-1 (Decomposition Section 2)*

#### SR-2: Regulatory Compliance (OBJ-6)
- **SR-2.1**: Equipment and installation shall comply with:
  - Canadian Electrical Code (CSA C22.1) — electrical safety, hazardous area installation
  - National Building Code of Canada (NBC) 2020 — structural mounting, seismic
  - **TBD** — Provincial and federal security/privacy regulations (PIPEDA) **ASSUMPTION**
  - **TBD** — Port authority requirements
  - **TBD** — Workplace safety regulations (WorkSafeBC)

*Source: OBJ-6 (Decomposition Section 2) — Regulatory Compliance*

#### SR-3: Life Safety Integration
- **SR-3.1**: Access control shall not impede emergency egress
- **SR-3.2**: Access control shall integrate with fire alarm per NFPA and life safety codes:
  - Automatic door unlock on fire alarm activation
  - Emergency egress hardware (crash bars, panic devices)
  - Delayed egress where permitted, with proper signage and alarms

*Source: Standard life safety requirements for access control systems*

## Standards

### Governing Codes and Standards

**Canadian Codes:**
- National Building Code of Canada (NBC) 2020
- Canadian Electrical Code (CSA C22.1) — electrical installation, hazardous area classification
- British Columbia Building Code **ASSUMPTION**

**Security Industry Standards (ASSUMPTION — to be confirmed per ER):**
- **TBD** — IEC 62676 series (Video surveillance systems for use in security applications)
- **TBD** — ONVIF Profile S/T/G (Network video device interoperability)
- **TBD** — OSDP v2 (Open Supervised Device Protocol) for access control
- **TBD** — ASIS/SIA standards for physical security systems

**Data/Communications Standards:**
- **TBD** — TIA-568 (Commercial Building Telecommunications Cabling Standard)
- **TBD** — TIA-942 (Data Center Standards) for equipment room design **ASSUMPTION**
- IEEE 802.3af/at/bt (Power over Ethernet) **ASSUMPTION**

**Environmental/Testing Standards:**
- IEC 60529 (IP ratings) — Ingress Protection for enclosures
- IEC 62262 (IK ratings) — Impact Protection for vandal resistance
- **TBD** — MIL-STD-810 (Environmental testing) for ruggedized equipment **ASSUMPTION**

**Project-Specific:**
- Employer's Requirements Volume 2 Parts 1-3 **TBD** — specific ER sections for security system specifications
- **TBD** — DP World Fraser Surrey Terminal security standards and specifications
- **TBD** — Project Quality Management Plan
- **TBD** — Project CAD and documentation standards (for specification format and structure)

### Specification Format Standards

- **TBD** — CSI MasterFormat (or equivalent) for specification structure **ASSUMPTION**
- **TBD** — Project specification template and format guidelines

## Verification

### Verification Methods

#### Document Review and Approval
- **Technical review** by discipline lead — verify specification meets design intent (DEL-24.01) and ER requirements
- **Interdisciplinary review** — coordinate with PKG-17, PKG-23, PKG-25 for interface requirements
- **Constructability review** — input from installation/construction team on practicality
- **Employer review** — acceptance at **TBD** — design stage (30%/60%/90%/IFC)

#### Compliance Verification
- **ER compliance matrix** — verify all ER requirements addressed in specification **TBD**
- **Standards compliance check** — verify all applicable codes and standards referenced and requirements included
- **Completeness check** — verify all sections complete, no TBD items remaining (or TBDs documented and scheduled for resolution)

#### Equipment Verification (via DEL-24.03 submittals)
- Equipment submittals (DEL-24.03) shall demonstrate compliance with this technical specification
- Factory Acceptance Testing (FAT) shall verify equipment performance per specification **TBD** — FAT scope and acceptance criteria
- Equipment certifications (UL, CSA, IP/IK ratings, etc.) shall be verified

#### Installation and Performance Verification (via PKG-29, DEL-24.04)
- Installation inspection and testing per PKG-29 (Testing) procedures
- Site Acceptance Testing (SAT) shall verify installed system performance per specification
- Commissioning per PKG-30 shall verify integrated system operation
- Installation and test records (DEL-24.04) document verification results

*Source: Standard technical specification verification process; cross-references to related deliverables*

### Acceptance Criteria

**Specification Document Acceptance:**
- All ER requirements addressed (or documented as TBD with resolution plan)
- All applicable codes and standards identified and requirements incorporated
- Interface requirements coordinated with affected disciplines
- Employer review comments resolved and acceptance obtained
- Specification suitable for procurement and construction use

**System Performance Acceptance:**
- Equipment meets specified performance requirements (verified via FAT, SAT, commissioning)
- Installation meets workmanship and quality standards
- System integration with Terminal security network successful (per DEC-05)
- All testing and commissioning acceptance criteria met (per PKG-29, PKG-30)

**Completion Criteria:**
- Technical specification issued for construction (IFC status)
- Employer acceptance obtained at specified design milestone
- Specification suitable as basis for procurement and construction activities
- Specification filed in project document management system and deliverable folder `3_Issued/`

## Documentation

### Required Documentation Outputs

**Primary Deliverable:**
- **Security System Technical Specification** — comprehensive document including:
  - Section 1: General Requirements (scope, references, submittals, quality assurance, warranties)
  - Section 2: Products (CCTV, access control, network, materials specifications)
  - Section 3: Execution (installation, testing, commissioning requirements)

**Anticipated Sub-Specifications (within main document or as separate volumes):**
1. **CCTV System Specification** — cameras, NVR, VMS, installation, testing
2. **Access Control System Specification** — readers, controllers, door hardware, software, installation, testing

*Source: `_CONTEXT.md` — Anticipated Artifacts*

### Documentation Requirements

**Format and Media:**
- **Document format:** **TBD** — PDF for distribution, editable source (Word/InDesign) for revisions **ASSUMPTION**
- **Specification structure:** **TBD** — CSI MasterFormat divisions or narrative format
- **Page count (estimated):** 30-80 pages typical for security system technical specifications **ASSUMPTION**
- **Transmittal:** Via project document management system **TBD**

**Revision Control:**
- Document numbering per **TBD** — project numbering system
- Revision tracking per **TBD** — project revision control procedures
- All revisions clearly identified with revision summary table

**Record Management:**
- Electronic files stored in project document management system **TBD**
- Issued specification archived in deliverable folder `3_Issued/`
- As-built updates incorporated post-construction **TBD** — as-built process
- Retention per project records management plan **TBD**

### Supporting Documentation

- **Design basis:** DEL-24.01 (Security System Design Drawing Set) — drawings that this specification supports
- **ER compliance matrix:** Requirements traceability from ER to specification sections **TBD**
- **Standards reference list:** Complete list of codes and standards cited in specification
- **Interdisciplinary coordination log:** Interface requirements coordination with PKG-17, PKG-23, PKG-25
- **Employer review comments and responses:** Documentation of review process and resolutions

**Cross-References to Related Deliverables:**
- DEL-24.01 — Security System Design Drawing Set (design basis for specification)
- DEL-24.03 — Security System Data Sheet Package (equipment submittals demonstrating compliance)
- DEL-24.04 — Security System Installation & Test Records (verification of specification compliance)
- PKG-17, PKG-23, PKG-25 — Interface discipline specifications
- PKG-29 (Testing), PKG-30 (Commissioning) — Verification procedures

---

*Document status: Enriched draft — Pass 1*
*Enrichment date: 2026-01-28*
*Cross-references: Datasheet.md for system attributes; Guidance.md for specification development principles; Procedure.md for production workflow*
