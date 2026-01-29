# Specification: DEL-18.02 Lighting Technical Specification

## Scope

This specification defines the requirements for the **Lighting Technical Specification** deliverable within **PKG-18 Lighting** for the Canola Oil Transload Facility.

**Purpose:** Defines performance, materials, and workmanship requirements for lighting per ER requirements. *(Source: _CONTEXT.md, Decomposition DEL-18.02 description)*

**Package Scope:** Interior and exterior LED lighting, lighting controls, emergency lighting. *(Source: Decomposition PKG-18 scope)*

**Deliverable Artifacts:**
- LED lighting specification
- Lighting controls specification
- Emergency lighting specification

*(Source: _CONTEXT.md, Decomposition DEL-18.02 anticipated artifacts)*

**Inclusions:**
- Performance requirements for LED lighting fixtures (efficacy, lumen output, color rendering, lumen maintenance)
- Material requirements for fixtures, poles, and supports (corrosion resistance, IP ratings, finishes)
- Workmanship requirements for installation, wiring, and commissioning
- Lighting control equipment and systems specifications (sensors, switches, panels, integration)
- Emergency lighting and battery backup system specifications
- Testing and acceptance criteria
- Submittal requirements (product data, certifications, test reports, O&M manuals)
- Warranty requirements

**Exclusions:**
- Lighting design and calculations (see DEL-18.03)
- Lighting layout drawings (see DEL-18.01)
- Electrical power distribution specifications (see PKG-17)
- Control system logic and programming details (see PKG-19)
- Building structural supports (see PKG-21; lighting specifies interface requirements only)

## Requirements

### Functional Requirements

**FR-1: LED Lighting Equipment**
- Specification shall define performance and material requirements for all LED lighting fixtures shown on design drawings (DEL-18.01)
- Fixture types shall include (at minimum):
  - Exterior area lighting (pole-mounted and building-mounted) — **TBD** *(ER requirements location TBD)*
  - Interior high-bay or linear fixtures for process/warehouse areas — **TBD**
  - Interior fixtures for control rooms, offices, and utility areas — **TBD**
  - Emergency and egress lighting fixtures — **TBD**
- LED technology per PKG-18 scope *(Source: Decomposition PKG-18 scope)*

**FR-2: Lighting Controls Equipment**
- Specification shall define requirements for lighting control devices and systems per PKG-18 scope *(Source: Decomposition PKG-18 scope)*
- Control types may include:
  - Manual switches and contactors — **TBD**
  - Occupancy/vacancy sensors — **TBD**
  - Photocells and daylight harvesting sensors — **TBD**
  - Time-based scheduling controls — **TBD**
  - Integration with facility control system (PKG-19) — **TBD**

**FR-3: Emergency Lighting Equipment**
- Specification shall define requirements for emergency lighting per NFPA 101 and CSA C22.1 — **ASSUMPTION**
- Emergency power sources:
  - Battery backup (integral or remote) — **TBD**
  - Emergency generator or UPS supply — **TBD**
  - Duration: minimum 90 minutes per code — **TBD** *(Code requirements location TBD)*

**FR-4: Submittals and Documentation**
- Specification shall require contractors to submit:
  - Product data sheets showing compliance with specification — **ASSUMPTION**
  - Shop drawings for custom or integrated systems — **TBD**
  - Photometric test reports (IES files, laboratory test data) — **ASSUMPTION**
  - Certification of compliance with CSA C22.2 or UL standards — **ASSUMPTION**
  - Warranty documentation — **TBD**
  - Operation and maintenance manuals — **ASSUMPTION**

### Performance Requirements

**PR-1: LED Fixture Performance**
- **Efficacy:** Minimum lumens per watt — **TBD** *(ER or energy code requirements location TBD)* — **ASSUMPTION**: 100-120 lm/W minimum for area lighting
- **Lumen Output:** Per fixture type and application based on calculations (DEL-18.03) — **TBD**
- **Color Rendering Index (CRI):** Minimum values per area type — **TBD** — **ASSUMPTION**: CRI ≥ 70 exterior; CRI ≥ 80 interior task areas
- **Color Temperature:** Per area requirements — **TBD** — **ASSUMPTION**: 4000-5000K typical
- **Lumen Maintenance:** L70 ≥ 50,000 hours — **TBD** — **ASSUMPTION**: 70% lumen output after 50,000 hours minimum
- **Power Factor:** Minimum 0.90 for LED drivers — **TBD** — **ASSUMPTION**: Per energy efficiency standards
- **Harmonic Distortion:** THD < 20% — **TBD** — **ASSUMPTION**: Per CSA C22.2 or IEEE requirements

**PR-2: Environmental and Durability Requirements**
- **Operating Temperature:** Fixtures rated for -20°C to +40°C minimum — **TBD** — **ASSUMPTION**: Per Surrey, BC climate
- **IP Rating:** Minimum IP65 for exterior; IP54 for indoor industrial; IP20 for interior office areas — **TBD** — **ASSUMPTION**: Per environment
- **Corrosion Resistance:** Marine-grade materials and finishes for outdoor fixtures — **ASSUMPTION**: Due to marine environment at Fraser Surrey Terminal
- **Impact Resistance:** IK ratings per application — **TBD** — **ASSUMPTION**: High-traffic or hazardous areas may require enhanced impact protection
- **UV Resistance:** Outdoor fixtures and enclosures UV-stabilized — **ASSUMPTION**

**PR-3: Seismic and Structural**
- Fixtures and poles designed for seismic loads per NBCC 2020 for Surrey, BC — **TBD** — **ASSUMPTION**
- Pole foundations coordinated with civil discipline (PKG-01, PKG-02, PKG-03) — **ASSUMPTION**
- Mounting details for building-mounted fixtures coordinated with structural/architectural (PKG-21, PKG-22) — **ASSUMPTION**

**PR-4: Electrical Performance**
- **Supply Voltage:** Fixtures compatible with facility electrical system voltage — **TBD** — **ASSUMPTION**: 120/208V or 347/600V per PKG-17
- **Voltage Range:** Fixtures operate across ±10% voltage variation — **TBD** — **ASSUMPTION**: Per CSA C22.1
- **Inrush Current:** Limited to prevent nuisance breaker tripping — **TBD**
- **Electromagnetic Compatibility (EMC):** Compliance with EMC standards — **TBD**

**PR-5: Control System Performance**
- Control devices compatible with facility control system architecture (PKG-19) — **TBD**
- Response time for occupancy sensors — **TBD** — **ASSUMPTION**: Typical 30-second delay adjustable
- Daylight sensor setpoints — **TBD**
- Communication protocols for networked controls — **TBD** — **ASSUMPTION**: BACnet, Modbus, or DALI typical

**PR-6: Emergency Lighting Performance**
- Emergency illumination levels per NFPA 101 — **TBD**: Minimum 10 lux (1 fc) average, 1 lux (0.1 fc) minimum at floor along egress paths — **ASSUMPTION**
- Emergency lighting duration: 90 minutes minimum — **TBD** — **ASSUMPTION**: Per NFPA 101 and CSA C22.1
- Battery backup system self-test capability — **TBD** — **ASSUMPTION**: Monthly and annual self-test per code

### Interface Requirements

**IR-1: Lighting Design Drawings (DEL-18.01)**
- Specification shall be coordinated with lighting design drawings — **ASSUMPTION**
- Fixture types, quantities, and performance in specification shall match those shown on drawings — **ASSUMPTION**

**IR-2: Lighting Design Calculations (DEL-18.03)**
- Performance requirements shall be based on calculation results — **ASSUMPTION**
- Illumination levels, uniformity, and fixture selections supported by photometric analysis — **ASSUMPTION**

**IR-3: Lighting Data Sheets (DEL-18.04)**
- Equipment data sheets shall demonstrate compliance with specification requirements — **ASSUMPTION**
- Manufacturer data sheets submitted per specification submittal requirements — **ASSUMPTION**

**IR-4: Electrical Power Distribution (PKG-17)**
- Electrical characteristics (voltage, current, power) coordinated with electrical power design — **ASSUMPTION**
- Circuit protection and wire sizing coordinated — **TBD**

**IR-5: Control Systems (PKG-19)**
- Lighting control interfaces and integration requirements coordinated with facility control system design — **TBD**
- Communication protocols, I/O points, and control logic defined — **TBD**

**IR-6: Hazardous Area Classification (PKG-17 or PKG-24)**
- Fixtures in hazardous areas meet classification requirements (Class I Division 1/2 or Zone 0/1/2) per CSA C22.1 — **TBD**
- Certification and labeling requirements for hazardous locations — **TBD**

**IR-7: Building and Structural (PKG-21, PKG-22)**
- Fixture mounting requirements compatible with building construction and ceiling systems — **ASSUMPTION**
- Structural loads for building-mounted fixtures coordinated — **TBD**

**IR-8: Civil and Site (PKG-01, PKG-02, PKG-03)**
- Pole foundation loads and details coordinated with civil foundation design — **ASSUMPTION**
- Underground conduit and wiring compatible with site grading and utilities — **TBD**

### Quality Requirements

**QR-1: Manufacturing Quality**
- LED fixtures shall be manufactured by approved manufacturers — **TBD** *(Approved manufacturers list or performance-based specification)*
- Quality certifications: ISO 9001 or equivalent — **TBD** — **ASSUMPTION**
- Product testing and certification by recognized laboratory (CSA, UL, ETL, or equivalent) — **ASSUMPTION**

**QR-2: Installation Quality**
- Installation workmanship shall comply with:
  - Manufacturer's installation instructions — **ASSUMPTION**
  - CSA C22.1 (Canadian Electrical Code) — **ASSUMPTION**
  - Project Quality Management Plan — **TBD** *(QMP location TBD)*
- Installer qualifications — **TBD** — **ASSUMPTION**: Licensed electricians per provincial requirements

**QR-3: Testing and Commissioning**
- Illumination level testing per specification and DEL-18.03 calculations — **ASSUMPTION**
- Functional testing of controls and emergency systems — **ASSUMPTION**
- Testing requirements detailed in specification and executed per DEL-18.05 — **ASSUMPTION**

**QR-4: Documentation and Submittals**
- All submittals reviewed and approved prior to procurement and installation — **ASSUMPTION**
- As-installed documentation and O&M manuals provided — **TBD**
- Warranty documentation and spare parts lists — **TBD**

## Standards

**Applicable Codes and Standards (Electrical Discipline):**

**Primary Electrical Codes:**
- **CSA C22.1** (Canadian Electrical Code) — Governing electrical code for installations in Canada — **ASSUMPTION**
- **CSA C22.2** — Electrical equipment standards and certification — **ASSUMPTION**
- **NBCC 2020** (National Building Code of Canada) — Building code including emergency lighting, seismic requirements — **ASSUMPTION**

**Lighting Equipment Standards:**
- **CSA C22.2 No. 250.0** — LED equipment — **TBD** *(Specific part number to be confirmed)*
- **UL 1598** or **CSA equivalent** — Luminaires — **TBD**
- **UL 924** or **CSA equivalent** — Emergency lighting equipment — **TBD**
- **IEC 60529** — IP rating classification — **ASSUMPTION**
- **IEC 62262** or equivalent — IK impact rating — **TBD**

**Lighting Design and Performance Standards:**
- **IESNA Lighting Handbook** — Illumination design criteria — **TBD** *(Edition and location TBD)*
- **IES LM-79** — Approved method for photometric and electrical testing of SSL products — **TBD**
- **IES LM-80** — Approved method for lumen maintenance testing of LED light sources — **TBD**
- **IES TM-21** — Projecting long-term lumen maintenance of LED light sources — **TBD**

**Life Safety and Emergency Lighting:**
- **NFPA 101** (Life Safety Code) — Emergency egress lighting — **ASSUMPTION**
- **NFPA 70** (NEC) — May be referenced for certain equipment standards (CSA C22.1 is governing code in Canada) — **TBD**

**Environmental and Quality Standards:**
- **ISO 9001** — Quality management system for manufacturers — **TBD**
- **RoHS** (Restriction of Hazardous Substances) — Environmental compliance — **TBD**
- **Energy Star** or equivalent — Energy efficiency certification (if applicable) — **TBD**

**Control System Standards:**
- **BACnet** (ISO 16484-5) — Building automation and control networks (if applicable) — **TBD**
- **DALI** (IEC 62386) — Digital Addressable Lighting Interface (if applicable) — **TBD**
- **Modbus** — Communication protocol (if applicable) — **TBD**

**Project-Specific Standards:**
- **Employer's Requirements** — Project-specific standards and requirements — **TBD** *(Vol 2 Part 1, Part 2, Part 3 — location TBD)*

## Verification

**Verification Methods for Specification Deliverables:**

**V-1: Technical Review Against Standards**
- Independent review of specification against CSA C22.1, CSA C22.2, IESNA, NFPA 101, NBCC — **ASSUMPTION**
- Verification that performance requirements are achievable and commercially available — **ASSUMPTION**

**V-2: Interdisciplinary Review**
- Coordination review with:
  - Electrical power distribution (PKG-17) — electrical compatibility
  - Control systems (PKG-19) — control interface compatibility
  - Architectural/structural (PKG-21, PKG-22) — mounting and integration
  - Civil (PKG-01, PKG-02, PKG-03) — foundation and site coordination
  - Fire protection (PKG-23) — emergency lighting coordination
- Review meeting or comment matrix per project procedures — **TBD**

**V-3: Employer Review and Comment**
- Specification submitted to Employer for review per contract requirements — **TBD**
- Employer comments addressed and specification updated — **ASSUMPTION**

**V-4: Compliance Matrix Verification**
- Compliance matrix showing specification sections vs. ER requirements — **TBD** — **ASSUMPTION**: Typical for contract deliverables
- Verification that all ER lighting requirements are addressed in specification — **TBD**

**V-5: Cross-Deliverable Consistency Check**
- Specification checked against:
  - Lighting Design Drawings (DEL-18.01) — fixture types and quantities consistent
  - Lighting Design Calculations (DEL-18.03) — performance requirements match calculated needs
  - Lighting Data Sheets (DEL-18.04) — specified products match data sheets
- Consistency verified before issue — **ASSUMPTION**

**V-6: Constructability Review**
- Review by construction or installation personnel for constructability and practicality — **TBD** — **ASSUMPTION**: Good practice
- Verification that specified products are commercially available and lead times are acceptable — **TBD**

**Acceptance Criteria:**
- All technical review comments closed — **ASSUMPTION**
- Interdisciplinary coordination issues resolved — **ASSUMPTION**
- Employer review complete and comments addressed — **TBD**
- Compliance matrix verified complete — **TBD**
- Cross-deliverable consistency confirmed — **ASSUMPTION**
- Specification approved by Electrical Discipline Lead and Project Engineering Manager — **TBD** *(Per approval matrix)*

## Documentation

**Required Documentation Outputs:**

Per decomposition and _CONTEXT.md:
1. **LED lighting specification** — Technical specification for LED fixtures, poles, and supports
2. **Lighting controls specification** — Technical specification for control devices and systems
3. **Emergency lighting specification** — Technical specification for emergency and egress lighting

**Specification Organization (typical CSI MasterFormat structure):**

**Part 1 — General:**
- Section 1.01: Summary and scope
- Section 1.02: References (codes and standards)
- Section 1.03: Submittals (product data, shop drawings, certifications, test reports)
- Section 1.04: Quality assurance (manufacturer qualifications, testing, certifications)
- Section 1.05: Delivery, storage, and handling
- Section 1.06: Project conditions and coordination
- Section 1.07: Warranty

**Part 2 — Products:**
- Section 2.01: Manufacturers (approved list or performance-based)
- Section 2.02: LED lighting fixtures (types, performance, materials)
- Section 2.03: LED drivers and power supplies
- Section 2.04: Lighting poles and supports
- Section 2.05: Lighting controls (sensors, switches, panels)
- Section 2.06: Emergency lighting and battery backup
- Section 2.07: Accessories and spare parts
- Section 2.08: Finishes

**Part 3 — Execution:**
- Section 3.01: Examination and preparation
- Section 3.02: Installation (general requirements)
- Section 3.03: Wiring and circuiting
- Section 3.04: Grounding and bonding
- Section 3.05: Field quality control and testing
- Section 3.06: Commissioning
- Section 3.07: Demonstration and training
- Section 3.08: Closeout submittals (as-builts, O&M manuals)

**Documentation Control:**
- Specification managed per project document control procedures — **TBD** *(Procedure location TBD)*
- Specification numbering per project numbering system — **TBD**
- Revision tracking and distribution per project procedures — **TBD**

**Issuance and Approval:**
- Draft specification to `2_Checking/To/` for review
- Approved specification to `3_Issued/` upon acceptance — **ASSUMPTION** *(Per project workflow)*
- Retention per project records management plan — **TBD**

**Electronic File Management:**
- Native format files (MS Word or similar) stored in project DMS — **TBD** *(System and location TBD)*
- PDF copies for distribution and record — **ASSUMPTION**
- Metadata and attributes per project requirements — **TBD**
