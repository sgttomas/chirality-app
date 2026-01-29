# Datasheet: DEL-24.02 Security System Technical Specification

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-24.02 |
| Name | Security System Technical Specification |
| Package | PKG-24 Security Systems |
| Discipline | Specialty |
| Type | Specification |
| Responsible | D&B Contractor |
| Status | INITIALIZED |
| Project | Canola Oil Transload Facility — Phase 1 |
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC |

*Source: `_CONTEXT.md`; Decomposition Section 5 — PKG-24 (line 567)*

## Attributes

### Specification Document Characteristics

| Attribute | Value |
|-----------|-------|
| Document Number | **TBD** — To be assigned per project numbering system |
| Specification Type | Technical Specification — Performance and materials requirements **ASSUMPTION** |
| Specification Format | CSI MasterFormat or narrative format **TBD** |
| Revision | **TBD** — Initial issue for review |
| Page Count (Estimated) | **TBD** — Typical security system technical specifications: 30-80 pages **ASSUMPTION** |
| Classification | For Construction **ASSUMPTION** |
| Format | PDF and editable source (Word/InDesign) **ASSUMPTION** |

*Source: Standard industry practice for technical specification documents*

### Specification Scope

| Scope Element | Description |
|---------------|-------------|
| CCTV System Specification | Performance, materials, and workmanship for CCTV surveillance system |
| Access Control Specification | Performance, materials, and workmanship for access control system |
| Network Infrastructure | Data network requirements for security systems integration |
| Terminal Integration | Integration requirements with existing DP World Fraser Surrey Terminal security systems per DEC-05 |
| Installation Standards | Workmanship and installation quality requirements |
| Testing and Commissioning | Acceptance testing and commissioning requirements |

*Source: `_CONTEXT.md` — Anticipated Artifacts; Decomposition Section 5 — PKG-24 scope; DEC-05 (Section 7)*

### Technical Requirements Coverage

| System/Component | Specification Coverage |
|------------------|------------------------|
| **CCTV Cameras** | Camera types (fixed, PTZ), resolution, frame rate, low-light performance, environmental ratings (IP, IK), mounting hardware |
| **Video Recording** | NVR capacity, recording duration, storage architecture, redundancy, playback capability |
| **Video Management** | VMS software, user interface, alarm integration, reporting, remote access |
| **Access Control Readers** | Reader types (proximity, biometric), technology (RFID frequency, standards), environmental ratings |
| **Access Control Panels** | Controller architecture (distributed/centralized), capacity (doors/users), communication protocols, power backup |
| **Access Control Software** | User management, access level administration, audit trails, alarm handling, integration |
| **Door Hardware** | Electric strikes, magnetic locks, crash bars, door position switches, REX devices |
| **Network Infrastructure** | Cabling standards, switches, fiber backbone, VLANs, bandwidth requirements |
| **Power Supply** | UPS requirements, battery backup duration, power distribution |
| **Conduit and Wiring** | Conduit types, cable specifications, installation methods, hazardous area requirements |

*Source: Typical security system technical specification content; specifics TBD per ER*

## Conditions

### Operational Context

**Facility Type:** Canola oil transload facility (CSD grade canola oil)
- Permitted throughput: 1,000,000 MT per annum
- Storage capacity: 45,000 MT (3 × 15,000 MT tanks)
- Railcar capacity: 32 unloading stations on 2 tracks
- Marine loading: Berth 10 with loading arms

*Source: Decomposition Section 1.1 — Key Parameters*

**Security System Scope:** CCTV, access control, integration with Terminal security network

*Source: Decomposition Section 5 — PKG-24 scope*

**Operational Requirements (ASSUMPTION — typical for 24/7 industrial facility):**
- Continuous 24/7/365 operation
- High reliability and availability (target: 99.5%+ uptime) **TBD** — per ER
- Integration with Terminal security operations center
- Support for maintenance and system expansion

### Environmental Conditions

| Condition | Value |
|-----------|-------|
| Location | Fraser Surrey Terminal, Surrey, BC (coastal marine environment) |
| Climate Zone | Pacific Maritime — wet, mild winters, moderate summers **ASSUMPTION** |
| Operating Temperature Range | Outdoor: -20°C to +40°C **ASSUMPTION** typical for BC coastal; Indoor: +15°C to +30°C **ASSUMPTION** |
| Humidity | High humidity coastal environment — equipment shall be rated for marine/coastal installation **ASSUMPTION** |
| Environmental Classification | Outdoor/Industrial — corrosive marine environment **ASSUMPTION** |
| Hazardous Area Classification | **TBD** — Class I Div 2 likely near railcar unloading and tank farm areas **ASSUMPTION**; general industrial areas non-classified |
| Seismic Requirements | **TBD** — Per NBC 2020 for Surrey, BC location (high seismic zone) **ASSUMPTION** |
| Weather Protection | Equipment shall withstand rain, snow, ice, salt spray, and UV exposure **ASSUMPTION** |
| Vandal Resistance | IK10 impact resistance for accessible public-facing locations **ASSUMPTION** |

*Source: Project location (Decomposition Section 1); standard security equipment environmental requirements*

### Design Life and Reliability

| Parameter | Value |
|-----------|-------|
| Design Life | **TBD** — Typical: 15-20 years for security infrastructure **ASSUMPTION** |
| Equipment MTBF | **TBD** — Mean Time Between Failures per manufacturer specifications |
| System Availability | **TBD** — 99.5%+ target uptime **ASSUMPTION** |
| Maintenance Intervals | **TBD** — Preventive maintenance schedule per manufacturer recommendations |
| Technology Refresh | **TBD** — Typical: 5-7 years for cameras/electronics, 10-15 years for infrastructure **ASSUMPTION** |
| Spare Parts Strategy | **TBD** — Critical spares inventory requirements |

*Source: Standard reliability requirements for industrial security systems*

## Construction

### CCTV System Components — Performance Requirements

**Cameras (specifications TBD per ER and coverage analysis):**
- Fixed cameras: **TBD** resolution (minimum 2MP typical for identification), frame rate, lens options
- PTZ cameras: **TBD** zoom range, pan/tilt speed, positioning accuracy, home position capability
- Low-light performance: **TBD** minimum illumination (0.01 lux typical for low-light cameras)
- Wide Dynamic Range (WDR): **TBD** for high-contrast scenes (backlight conditions)
- Environmental ratings: IP66/IP67 minimum for outdoor, IK10 for vandal-prone locations
- Operating temperature: -40°C to +60°C for outdoor cameras **ASSUMPTION**
- Corrosion resistance: Marine-grade materials for coastal environment (stainless steel, powder-coated aluminum)

**Network Video Recorder (NVR):**
- Recording capacity: **TBD** — channels, resolution, frame rate, retention period (30-90 days typical)
- Storage: **TBD** — RAID configuration for redundancy, hot-swappable drives
- Network throughput: **TBD** — bandwidth to support all camera streams simultaneously
- Redundancy: **TBD** — dual NVR for critical recording areas **ASSUMPTION**

**Video Management System (VMS):**
- Software platform: **TBD** — ONVIF-compliant for multi-vendor interoperability **ASSUMPTION**
- User licenses: **TBD** — concurrent users, operator workstations
- Features: Live view, playback, video export, alarm handling, audit logging, PTZ control
- Integration: API for integration with access control and Terminal systems **TBD**

*Source: Typical CCTV system technical specifications; specifics TBD per ER and design (DEL-24.01)*

### Access Control System Components — Performance Requirements

**Card Readers:**
- Technology: **TBD** — Proximity (125 kHz) or smart card (13.56 MHz HID, MIFARE) **ASSUMPTION**
- Read range: **TBD** — 2-10 cm typical depending on card type
- Environmental ratings: IP65 minimum for outdoor, IK08 for vandal resistance
- Operating temperature: -30°C to +60°C **ASSUMPTION**
- Protocol: OSDP (Open Supervised Device Protocol) or Wiegand **TBD**

**Access Control Panels/Controllers:**
- Architecture: **TBD** — Distributed intelligent controllers or centralized system
- Capacity: **TBD** — doors per panel, credentials per system
- Communication: TCP/IP network-based, encrypted **ASSUMPTION**
- Power backup: Battery backup for **TBD** hours (4-8 hours typical)
- Fail-safe/Fail-secure: Configurable per door per life safety requirements

**Door Hardware:**
- Electric strikes: **TBD** — Grade 1 commercial, stainless steel for durability
- Magnetic locks: **TBD** — holding force (600-1200 lbs typical), with door position switch and REX
- Crash bars/Panic devices: **TBD** — UL listed, coordinated with fire/life safety requirements (PKG-23)
- Door position switches: **TBD** — magnetic contacts or position sensors
- Request-to-exit (REX) devices: **TBD** — PIR motion sensors or push buttons

**Access Control Software:**
- Platform: **TBD** — Centralized management software with web interface **ASSUMPTION**
- Features: Cardholder management, access level administration, time zones, alarm monitoring, audit trails
- Reporting: Standard and custom reports, real-time dashboards
- Integration: Integration with Terminal access control platform per DEC-05 **TBD**

*Source: Typical access control technical specifications; specifics TBD per ER*

### Network Infrastructure — Performance Requirements

**Cabling:**
- Data cables: Cat6A minimum for IP cameras and access control panels **ASSUMPTION**
- Fiber optic: Single-mode fiber for backbone and long runs (>90m)
- Cable specifications: **TBD** — CSA-approved, plenum-rated where required, outdoor-rated for exterior runs
- Installation: Per TIA-568 standards **ASSUMPTION**

**Network Switches:**
- PoE switches: **TBD** — 802.3af/at/bt for camera and reader power
- Managed switches: **TBD** — VLAN support, QoS, IGMP snooping for multicast
- Redundancy: **TBD** — dual homing, ring topology, or stacking for critical paths

**Network Architecture:**
- VLANs: Separate VLANs for CCTV, access control, management traffic **ASSUMPTION**
- Bandwidth: **TBD** — Calculated based on camera count, resolution, frame rate, compression
- Security: Firewall between security systems and Terminal network per DEC-05 **TBD**

*Source: DEC-05 (Decomposition Section 7); typical IP security system network requirements*

### Materials and Workmanship Standards

| Material/Component | Standard/Requirement |
|--------------------|----------------------|
| Outdoor cameras and housings | Corrosion-resistant materials (marine-grade stainless steel, powder-coated aluminum) **ASSUMPTION** |
| Mounting hardware | Stainless steel fasteners and brackets for coastal environment **ASSUMPTION** |
| Conduit | PVC Schedule 40 for underground, rigid steel or aluminum for exposed areas **ASSUMPTION** |
| Hazardous area equipment | **TBD** — Class I Div 2 rated where required, proper conduit sealing |
| Cable entry seals | **TBD** — Watertight seals, cable glands per IP rating |
| UPS/Battery backup | **TBD** — Sealed lead-acid or lithium-ion, capacity for specified backup duration |

**Workmanship standards:**
- Installation per manufacturer instructions and applicable codes
- Cable management: Neat, accessible, labeled per project standards **TBD**
- Terminations: Professional, tested, documented
- Conduit and cable routing: Coordinated with other disciplines, proper support and protection

*Source: Standard materials and workmanship requirements for industrial security systems*

### Installation and Commissioning Requirements

**Installation:**
- Contractor shall provide qualified security systems installers **TBD** — certification requirements
- Coordination with other trades per IDC process
- Phased installation to minimize Terminal disruption (OBJ-5)
- Protection of equipment during construction

**Testing:**
- Factory acceptance testing (FAT) for major equipment **TBD** — per equipment procurement specification (DEL-24.03)
- Site acceptance testing (SAT) per testing procedures (PKG-29)
- Integration testing with Terminal systems **TBD**

**Commissioning:**
- System commissioning per commissioning procedures (PKG-30)
- Training for Terminal security operations staff (PKG-35)
- Documentation turnover: as-built drawings, manuals, test records

*Source: OBJ-5 (Decomposition Section 2); standard commissioning requirements; PKG-29, PKG-30, PKG-35*

## References

### Primary References

- Decomposition document: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — Sections 1, 2, 5 (PKG-24), 7 (DEC-05)
- `_CONTEXT.md` — Deliverable identity and anticipated artifacts
- `_REFERENCES.md` — No specific references identified yet; ER volumes expected
- DEL-24.01 (Security System Design Drawing Set) — Design basis for technical specification requirements

### Applicable Standards (ASSUMPTION — to be confirmed per ER)

**Security Industry Standards:**
- **TBD** — IEC 62676 series (Video surveillance systems for use in security applications)
- **TBD** — ONVIF Profile S/T/G (Network video device interoperability)
- **TBD** — OSDP (Open Supervised Device Protocol) for access control
- **TBD** — TIA-568 (Commercial Building Telecommunications Cabling Standard)

**Canadian Codes:**
- National Building Code of Canada (NBC) 2020 — seismic, structural requirements
- Canadian Electrical Code (CSA C22.1) — electrical installation, hazardous area classification
- **TBD** — CSA standards for security systems in Canada

**Environmental and Quality:**
- IEC 60529 (IP ratings) — Ingress Protection for enclosures
- IEC 62262 (IK ratings) — Impact Protection
- ISO 9001 — Quality management for equipment manufacturing **ASSUMPTION**

**Project-Specific:**
- Employer's Requirements Volume 2 Parts 1-3 **TBD** — specific ER sections for security system performance requirements
- **TBD** — DP World Fraser Surrey Terminal security standards and specifications
- **TBD** — Project Quality Management Plan

### Cross-References

- See `_DEPENDENCIES.md` — NOT_TRACKED (dependencies coordinated externally)
- DEL-24.01 — Security System Design Drawing Set (design basis)
- DEL-24.03 — Security System Data Sheet Package (equipment submittals)
- DEL-24.04 — Security System Installation & Test Records (verification and commissioning)
- PKG-17 (Electrical Power Distribution) — Power supply for security equipment
- PKG-23 (Fire Protection) — Integration with fire alarm/life safety
- PKG-25 (Communications & IT) — Network infrastructure
- PKG-29 (Testing) — Site acceptance testing
- PKG-30 (Commissioning) — System commissioning and integration
- PKG-35 (Training & Handover) — Operations training and documentation

---

*Document status: Enriched draft — Pass 1*
*Enrichment date: 2026-01-28*
*Next review: WORKING_ITEMS session for detailed requirements development from ER*
