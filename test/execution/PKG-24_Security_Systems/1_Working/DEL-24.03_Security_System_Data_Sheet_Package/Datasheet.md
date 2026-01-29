# Datasheet: DEL-24.03 Security System Data Sheet Package

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-24.03 |
| Name | Security System Data Sheet Package |
| Package | PKG-24 Security Systems |
| Discipline | Specialty |
| Type | Data Sheet |
| Responsible | D&B Contractor |
| Status | INITIALIZED |
| Project | Canola Oil Transload Facility — Phase 1 |
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC |

*Source: `_CONTEXT.md`; Decomposition Section 5 — PKG-24 (line 568)*

## Attributes

### Data Sheet Package Characteristics

| Attribute | Value |
|-----------|-------|
| Package Document Number | **TBD** — To be assigned per project numbering system |
| Package Type | Equipment Submittal Package **ASSUMPTION** |
| Submittal Format | **TBD** — PDF compilation or project-specified format |
| Total Equipment Count | **TBD** — Based on design (DEL-24.01) and procurement |
| Revision | **TBD** — Initial submittal for approval |
| Classification | For Construction / Procurement **ASSUMPTION** |
| Submittal Status | **TBD** — Awaiting approval, Approved, Approved as Noted, etc. |

*Source: Standard equipment submittal package characteristics*

### Equipment Data Sheet Scope

| Equipment Category | Data Sheets Included | Quantity (TBD) |
|--------------------|----------------------|----------------|
| **CCTV Cameras** | Fixed camera datasheets (multiple models possible) | **TBD** — per DEL-24.01 design |
| | PTZ camera datasheets | **TBD** |
| | Camera housings and mounts (if separate) | **TBD** |
| **Video Recording** | Network Video Recorder (NVR) datasheets | **TBD** — 1 or 2 (redundant) |
| | Storage subsystem (if separate from NVR) | **TBD** |
| **Video Management** | Video Management System (VMS) software datasheet/license | **TBD** |
| **Access Control Readers** | Card reader datasheets (multiple models/locations) | **TBD** — per DEL-24.01 design |
| | Biometric reader datasheets (if applicable) | **TBD** |
| **Access Control Controllers** | Access control panel/controller datasheets | **TBD** |
| | Access control software datasheet/license | **TBD** |
| **Door Hardware** | Electric strike datasheets | **TBD** |
| | Magnetic lock datasheets | **TBD** |
| | Crash bar / panic device datasheets | **TBD** |
| | Door position switch / REX device datasheets | **TBD** |
| **Network Infrastructure** | Network switch datasheets (PoE, managed) | **TBD** |
| | Fiber optic equipment datasheets | **TBD** |
| **Power & UPS** | UPS datasheets | **TBD** |
| | Power supply datasheets | **TBD** |
| **Accessories** | Cable, conduit, mounting hardware (as required by specification) | **TBD** |

*Source: `_CONTEXT.md` — Anticipated Artifacts; typical security system equipment list from DEL-24.01 and DEL-24.02*

## Conditions

### Submittal Purpose and Context

**Purpose:** Defines and substantiates security system in accordance with ER requirements by providing equipment datasheets demonstrating compliance with DEL-24.02 (Technical Specification).

*Source: `_CONTEXT.md`; DEL-24.02 as specification basis*

**Submittal workflow:**
1. Contractor selects equipment meeting DEL-24.02 specification requirements
2. Contractor assembles equipment datasheets and supporting documentation
3. Contractor submits data sheet package (DEL-24.03) for review and approval
4. Designer/Employer reviews for compliance with specification and design
5. Approval granted (or revise-and-resubmit if non-compliant)
6. Approved equipment procured and installed
7. Installation verified per DEL-24.04 (Installation & Test Records)

*Source: Standard equipment submittal and procurement workflow*

### Operational Context

**Facility Type:** Canola oil transload facility (CSD grade canola oil)
- Permitted throughput: 1,000,000 MT per annum
- Storage capacity: 45,000 MT (3 × 15,000 MT tanks)
- Railcar capacity: 32 unloading stations on 2 tracks

*Source: Decomposition Section 1.1 — Key Parameters*

**Security System Application:** CCTV surveillance and access control for industrial transload facility with Terminal security network integration per DEC-05

*Source: Decomposition Section 5 — PKG-24 scope; DEC-05 (Section 7)*

### Environmental Conditions for Equipment Selection

| Condition | Value | Impact on Equipment Selection |
|-----------|-------|-------------------------------|
| Location | Fraser Surrey Terminal, Surrey, BC (coastal marine) | Corrosion-resistant materials, marine-grade enclosures |
| Operating Temperature | Outdoor: -20°C to +40°C **ASSUMPTION**; Indoor: +15°C to +30°C | Wide temperature rating for outdoor equipment |
| Humidity | High humidity coastal environment | Conformal coating, sealed enclosures |
| Environmental Classification | Outdoor/Industrial/Marine | IP66/IP67 minimum outdoor, corrosion resistance |
| Hazardous Area Classification | **TBD** — Class I Div 2 likely near tank farm/unloading | Appropriate area classification ratings where required |
| Vandal Resistance | Public-facing and accessible locations | IK10 impact rating for accessible cameras/readers |
| Weather Exposure | Rain, snow, ice, salt spray, UV | Weatherproof ratings, UV-resistant materials |

*Source: Fraser Surrey Terminal coastal location; typical industrial security equipment environmental requirements*

## Construction

### Data Sheet Content Requirements

**Each equipment datasheet shall include (typical):**

**1. Equipment Identification:**
- Manufacturer name and contact information
- Model number and product name
- Equipment tag number per design (DEL-24.01) **TBD**
- Quantity and location

**2. Technical Specifications:**
- Performance specifications (resolution, capacity, power, etc.)
- Physical specifications (dimensions, weight, mounting)
- Electrical specifications (voltage, current, power consumption, PoE class)
- Environmental ratings (IP, IK, operating temperature, humidity)
- Compliance certifications (UL, CSA, CE, FCC, etc.)

**3. Compliance Documentation:**
- Demonstration of compliance with DEL-24.02 specification requirements
- Compliance matrix or narrative showing how equipment meets each applicable requirement
- Manufacturer certifications and test reports

**4. Supporting Documentation:**
- Installation instructions and mounting details
- Wiring diagrams and connection schematics
- Operation and maintenance manuals (or reference to where they will be provided)
- Warranty information

**5. Integration Documentation (for systems requiring integration):**
- Integration protocols and APIs (for Terminal integration per DEC-05)
- Compatibility with specified systems (e.g., ONVIF compliance for cameras)
- Configuration and setup requirements

*Source: Standard equipment submittal content requirements; DEL-24.02 submittal requirements*

### Specific Equipment Data Sheet Requirements

**CCTV Camera Data Sheets:**
- Camera type (fixed, PTZ, box, bullet, dome)
- Image sensor specifications (resolution, sensor size, pixel size)
- Lens specifications (focal length, field of view, aperture)
- Frame rate, compression codec (H.264, H.265)
- Low-light performance (minimum lux rating, WDR capability)
- Environmental ratings (IP, IK, operating temperature)
- Power requirements (PoE class, voltage, current)
- Mounting options and brackets
- ONVIF Profile compliance **ASSUMPTION**

**NVR Data Sheets:**
- Recording capacity (channels, maximum resolution per channel)
- Storage capacity (drive bays, maximum storage, RAID support)
- Network throughput (Mbps incoming/outgoing)
- Recording modes (continuous, motion, alarm-triggered)
- Playback capabilities (simultaneous playback streams)
- Redundancy features (dual power supply, RAID, failover) **TBD**
- Operating system and VMS compatibility

**Access Control Reader Data Sheets:**
- Technology (125 kHz proximity, 13.56 MHz smart card, biometric)
- Read range and performance
- Supported credential types (HID, MIFARE, etc.)
- Communication protocol (OSDP, Wiegand)
- Environmental ratings (IP, IK, operating temperature)
- Power requirements
- Vandal resistance and tamper detection

**Access Control Controller Data Sheets:**
- System architecture (intelligent distributed, network-based)
- Capacity (doors per controller, credentials, events)
- Communication (TCP/IP, RS-485)
- Battery backup (capacity, duration)
- Inputs/outputs (door position, REX, alarm inputs)
- Fail-safe/fail-secure configuration per door
- Integration with Terminal access control system per DEC-05 **TBD**

*Source: Typical security equipment datasheet requirements; DEL-24.02 specification requirements*

### Factory Acceptance Testing (FAT) Documentation

**For major equipment requiring FAT (TBD):**
- FAT test procedure and acceptance criteria
- FAT test results and certifications
- Witnessed testing by designer/Employer representative **TBD**
- Deficiency resolution and re-test results
- FAT completion certificate

*Source: DEL-24.02 — Equipment quality and testing requirements; typical FAT documentation*

## References

### Primary References

- Decomposition document: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — Sections 1, 2, 5 (PKG-24), 7 (DEC-05)
- `_CONTEXT.md` — Deliverable identity and anticipated artifacts
- `_REFERENCES.md` — No specific references identified yet
- **DEL-24.01** — Security System Design Drawing Set (equipment locations and quantities)
- **DEL-24.02** — Security System Technical Specification (equipment requirements basis for submittals)

### Submittal Review Standards

- Employer's Requirements Volume 2 **TBD** — Equipment standards and approved manufacturers
- **TBD** — Project submittal procedures and approval process
- **TBD** — DP World Fraser Surrey Terminal equipment standards

### Equipment Certifications and Standards

**Required certifications (typical — TBD per DEL-24.02):**
- UL or CSA listing for electrical safety (North American market)
- FCC compliance for RF devices (card readers, wireless equipment)
- CE marking for European-manufactured equipment
- IP rating certification (IEC 60529)
- IK rating certification (IEC 62262)
- ONVIF certification for IP cameras (interoperability)
- OSDP certification for access control readers (if required)
- Hazardous area certifications (Class I Div 2) where applicable **TBD**

### Cross-References

- See `_DEPENDENCIES.md` — NOT_TRACKED (dependencies coordinated externally)
- DEL-24.01 — Design basis for equipment selection and locations
- DEL-24.02 — Technical specification requirements that equipment must meet
- DEL-24.04 — Installation & Test Records (verification of installed equipment performance)
- PKG-29 (Testing) — Equipment testing procedures
- PKG-30 (Commissioning) — System commissioning and performance verification

---

*Document status: Enriched draft — Pass 1*
*Enrichment date: 2026-01-28*
*Next review: WORKING_ITEMS session for equipment-specific datasheet compilation*
