# Specification: DEL-20.02 Instrumentation Technical Specification

## Scope

This specification defines the requirements for the **Instrumentation Technical Specification** within **PKG-20 Field Instrumentation** for the Canola Oil Transload Facility Phase 1 at Fraser Surrey Terminal, Surrey, BC.

**Deliverable Purpose:**

Defines performance, materials, and workmanship requirements for instrumentation per ER requirements.

**Source:** Decomposition document `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, DEL-20.02 description (line 497)

**Package Scope:**

PKG-20 Field Instrumentation includes field instruments, transmitters, switches, instrument cabling, and junction boxes.

**Source:** Decomposition document, PKG-20 Scope (line 490)

**Specification Artifacts:**

This technical specification shall include:
1. **Level instrument specification** — Performance, materials, and workmanship for level measurement devices
2. **Pressure instrument specification** — Performance, materials, and workmanship for pressure measurement devices
3. **Temperature specification** — Performance, materials, and workmanship for temperature measurement devices

**Source:** Decomposition document, DEL-20.02 Anticipated Artifacts (line 497); `_CONTEXT.md`

**Specification Purpose:**

This technical specification establishes:
- **Performance requirements** — Accuracy, range, response time, environmental ratings
- **Material requirements** — Wetted materials, enclosure materials, corrosion resistance
- **Workmanship requirements** — Installation methods, quality standards, testing protocols
- **Procurement basis** — Requirements for equipment suppliers and manufacturers
- **Construction guidance** — Requirements for field installation contractors

**Source:** Deliverable description "performance, materials, and workmanship requirements" (line 497)

**Inclusions:**
- Field instrument performance criteria (ranges, accuracies, environmental ratings)
- Material specifications for instrument wetted parts, enclosures, accessories
- Workmanship standards for installation, calibration, testing
- Quality assurance and acceptance criteria
- Reference standards and codes
- Manufacturer qualification requirements (if applicable)

**Exclusions:**
- Instrument location and installation drawings (see DEL-20.01 Instrumentation Design Drawing Set)
- Instrument sizing calculations and verification (see DEL-20.03 Instrumentation Design Calculations)
- Equipment-specific data sheets (see DEL-20.04 Instrumentation Data Sheet Package)
- Installation and test records (see DEL-20.05 Instrumentation Installation & Test Records)
- Control system and SCADA requirements (see PKG-22 Control Systems & SCADA)
- Electrical power distribution (see PKG-17 Electrical Power Distribution)
- Custody transfer metering systems (primary scope in PKG-12 Product Transfer and Metering)

**Source:** **ASSUMPTION** based on deliverable type (Specification) and typical EPC package boundaries; cross-references per decomposition

## Requirements

### Functional Requirements

**FR-1: Measurement Performance**

Field instruments shall provide accurate, reliable measurement of process variables to support:
- **Process control:** Automated control loops for safe and efficient operations
- **Monitoring:** Operator visibility into process conditions (tank levels, pressures, temperatures)
- **Safety:** Alarm generation and interlock activation for abnormal conditions
- **Custody transfer:** Accurate measurement for commercial product accountability (coordinate with PKG-12)

**Source:** **ASSUMPTION** based on typical instrumentation functional requirements for bulk liquid terminal

**FR-2: Level Measurement Requirements**

Level instruments shall measure and indicate:
- **Storage tank levels** (3 × 15,000 MT tanks):
  - Continuous level measurement for inventory management
  - High and low level alarms
  - Independent overfill protection (per API 2350 — **TBD**: Specific requirements)
  - Tank gauging accuracy: **TBD** — Per Employer's Requirements and regulatory requirements (custody transfer if applicable)

- **Process vessel levels** (unloading pits, sumps, day tanks):
  - Continuous level measurement and control
  - High and low level alarms and interlocks
  - Range suitable for vessel geometry

- **Loading operation levels:**
  - Marine loading arm ullage monitoring
  - Coordination with ship tank measurements

**Measurement Technology Selection:**
- **TBD** — Specific technology (radar, guided wave, float) to be selected based on application requirements and DEL-20.03 calculations
- **Accuracy:** **TBD** — Per application (custody transfer vs. process control)
- **Repeatability:** **TBD**
- **Response time:** **TBD**

**Source:** Decomposition Key Parameters (storage capacity line 40, railcar capacity line 43); **ASSUMPTION** based on typical tank terminal level measurement requirements; API 2350 reference for overfill protection

**FR-3: Pressure Measurement Requirements**

Pressure instruments shall measure and indicate:
- **Pump performance monitoring:**
  - Suction and discharge pressure for each pump
  - Pressure drop across filters and strainers
  - Differential pressure for flow verification

- **Piping system monitoring:**
  - Line pressure for safe operating envelope verification
  - High and low pressure alarms and interlocks
  - Pressure transmitters for control loops (loading rate control, etc.)

**Measurement Requirements:**
- **Ranges:** **TBD** — Per piping system design (atmospheric to pump discharge pressures)
- **Accuracy:** **TBD** — **ASSUMPTION**: ±0.5% of span typical for process control; higher for safety-critical
- **Overpressure rating:** **TBD** — Per piping system maximum allowable working pressure (MAWP)
- **Material compatibility:** Wetted parts compatible with CSD canola oil

**Source:** **ASSUMPTION** based on typical pump and piping system instrumentation for liquid transfer operations

**FR-4: Temperature Measurement Requirements**

Temperature instruments shall measure and indicate:
- **Product temperature monitoring:**
  - Storage tank temperatures (multiple elevations for stratification monitoring)
  - Product temperature for viscosity correlation and quality control
  - Loading temperature for custody transfer correction (if applicable)

- **Equipment protection:**
  - Pump bearing temperatures (high temperature alarm)
  - Motor winding temperatures (thermal protection)
  - Ambient temperature monitoring for freeze protection and winterization

**Measurement Requirements:**
- **Ranges:** **TBD** — Per process conditions (ambient to maximum product temperature)
- **Accuracy:** **TBD** — **ASSUMPTION**: ±0.5°C for product quality monitoring; ±1-2°C for equipment protection
- **Element type:** **TBD** — RTD (Pt100/Pt1000) preferred for accuracy; thermocouple for high-temperature applications
- **Thermowell requirements:** **TBD** — Material, insertion length, pressure/temperature rating

**Source:** **ASSUMPTION** based on canola oil temperature sensitivity (viscosity) and typical process monitoring requirements

**FR-5: Instrument Accessories**

Supporting components shall be specified to ensure complete, functional installations:
- **Instrument valves:** Isolation, drain, vent, calibration connections (ball valves, needle valves per application)
- **Instrument tubing:** Stainless steel seamless tubing, pressure-rated per application
- **Impulse piping:** Slope, support, and winterization per ISA/API standards
- **Instrument enclosures:** Weatherproof, corrosion-resistant per environmental conditions
- **Junction boxes:** Properly sized, rated per hazardous area classification
- **Cable glands and seals:** Per CSA C22.1 hazardous area requirements
- **Mounting hardware:** Supports, brackets, platforms with seismic qualification

**Source:** **ASSUMPTION** based on typical instrument accessory requirements for complete installations

### Performance Requirements

**PR-1: Accuracy and Uncertainty**

Instrument accuracy shall be specified to support:
- **Process control:** Adequate accuracy for stable control loop performance
- **Safety systems:** Accuracy suitable for reliable alarm and interlock actuation
- **Custody transfer:** Accuracy meeting regulatory and commercial requirements (coordinate with PKG-12)

**Accuracy Specification Format:**
- **TBD** — Percent of span, percent of reading, or absolute units per instrument type
- **TBD** — Include statement of total loop uncertainty (sensor + transmitter + wiring)

**Source:** **ASSUMPTION** based on typical measurement system accuracy requirements; **TBD**: Specific accuracy values per application

**PR-2: Environmental Ratings**

All field instruments shall be rated for:
- **Ambient temperature:** **TBD** — **ASSUMPTION**: -40°C to +60°C (outdoor BC coastal climate)
- **Humidity:** 0-100% RH non-condensing (coastal marine environment)
- **Enclosure rating:** NEMA 4X / IP66 minimum (weatherproof, corrosion-resistant)
- **Corrosion resistance:** Marine-grade materials and coatings (salt air exposure)
- **UV resistance:** Outdoor-rated materials and coatings (sunlight exposure)

**Source:** Project location (Fraser Surrey Terminal, coastal BC) and **ASSUMPTION** based on typical marine terminal environmental conditions

**PR-3: Hazardous Area Compliance**

Instruments installed in hazardous areas shall comply with:
- **Electrical classification:** Per facility hazardous area classification drawing — **TBD**
  - **ASSUMPTION**: Class I, Division 2 / Zone 2 areas likely for canola oil vapor release areas
- **Protection method:** Intrinsically safe (IS), explosion-proof (XP), or non-incendive (NI) per CSA C22.1
- **Certification:** CSA or equivalent North American certification for hazardous area equipment
- **Temperature class:** **TBD** — Per canola oil ignition temperature (T3 or T4 typical — **ASSUMPTION**)

**Source:** CSA C22.1 reference; **ASSUMPTION** based on canola oil combustibility; **TBD**: Facility hazardous area classification

**PR-4: Seismic Qualification**

Instrument mounting, supports, and in-line instruments shall be seismically qualified per:
- **NBC 2015** (National Building Code of Canada) seismic design requirements for Surrey, BC location
- **Seismic zone:** **TBD** — Per geotechnical and structural design basis
- **Mounting design:** Instrument supports and brackets designed to withstand seismic loads
- **In-line instruments:** Large in-line instruments (flow meters) may require seismic restraints

**Source:** **ASSUMPTION** based on Canadian building code requirements for BC jurisdiction; seismic active region

**PR-5: Design Life and Reliability**

Instruments shall be selected and specified for:
- **Design life:** **TBD** — **ASSUMPTION**: 25 years minimum facility design life
- **Maintenance intervals:** **TBD** — Calibration intervals, wear part replacement, overhaul schedules
- **Redundancy:** **TBD** — Critical instruments may require redundancy for high availability (supports OBJ-1: Safe & Reliable Operation)
- **Lifecycle cost:** Consider initial cost vs. maintenance cost (supports OBJ-9: Lifecycle Cost Optimization)

**Source:** **ASSUMPTION** based on typical industrial facility design life; OBJ-1 (line 58) and OBJ-9 (line 66) references

### Interface Requirements

**INT-1: Interdisciplinary Coordination**

This specification interfaces with:
- **PKG-12 Product Transfer and Metering** — Custody transfer metering requirements and accuracy
- **PKG-13 Storage Tanks** — Tank instrumentation (level, temperature), nozzle sizes and locations
- **PKG-14 Process Piping** — Instrument connections, taps, isolation valves, piping design pressures
- **PKG-15 Pumps and Rotating Equipment** — Equipment instrumentation (pressure, temperature, flow)
- **PKG-17 Electrical Power Distribution** — Instrument power supply requirements
- **PKG-22 Control Systems & SCADA** — Signal types (4-20 mA, HART, digital), I/O requirements, communication protocols
- **PKG-23 Electrical Infrastructure** — Cable routing infrastructure, junction boxes, power panels

**Source:** **ASSUMPTION** based on typical I&C interfaces and decomposition package structure

**INT-2: Related Deliverable Coordination**

This specification is coordinated with other PKG-20 deliverables:
- **DEL-20.01 (Drawing Set):** Drawings implement specification requirements for installation
- **DEL-20.03 (Calculations):** Calculations verify specification requirements and support instrument sizing
- **DEL-20.04 (Data Sheets):** Data sheets demonstrate equipment compliance with specification
- **DEL-20.05 (Test Records):** Test records verify specification compliance during commissioning

**Source:** Decomposition PKG-20 deliverables (lines 496-500); typical deliverable coordination in EPC workflow

**INT-3: Procurement Interface**

This specification serves as:
- **Procurement basis** for instrument equipment procurement packages
- **Bid evaluation criteria** for vendor quotations
- **Quality basis** for equipment receiving inspection and acceptance

**Procurement process (typical):**
1. Specification issued to vendors with data sheet templates (from DEL-20.04)
2. Vendor proposals evaluated against specification requirements
3. Vendor data sheets reviewed for compliance
4. Equipment received and inspected per specification

**Source:** **ASSUMPTION** based on typical EPC procurement workflow

**INT-4: Construction Interface**

This specification provides:
- **Installation requirements** for construction contractors
- **Quality standards** for field workmanship verification
- **Acceptance criteria** for construction inspection and quality assurance

**Construction use (typical):**
- Field installation per specification workmanship requirements
- Calibration and testing per specification and manufacturer requirements
- As-built documentation updated per specification (DEL-20.05 records)

**Source:** **ASSUMPTION** based on typical EPC construction workflow

### Quality Requirements

**QR-1: Specification Development and Review**

Specification development shall include:
- **Requirements capture:** Extract requirements from Employer's Requirements, applicable codes/standards, and project design basis
- **Technical review:** Discipline engineer review for technical accuracy and completeness
- **Interdisciplinary review:** Coordination with affected disciplines (process, piping, electrical, control systems)
- **Independent check:** Peer review by qualified I&C engineer
- **Approval:** I&C Lead Engineer approval for issuance

**Source:** **ASSUMPTION** based on typical EPC quality procedures for specification development

**QR-2: Compliance Verification**

Specification compliance shall be verified through:
- **Design calculations:** DEL-20.03 calculations verify instrument sizing and performance per specification
- **Equipment data sheets:** DEL-20.04 data sheets demonstrate vendor equipment meets specification
- **Factory acceptance testing (FAT):** Vendor testing per specification requirements (if applicable)
- **Site acceptance testing (SAT):** Field calibration and testing per DEL-20.05 procedures

**Source:** Cross-reference to other PKG-20 deliverables (lines 498-500); **ASSUMPTION** based on typical verification workflow

**QR-3: Manufacturer Qualification**

**TBD** — Manufacturer qualification requirements to be defined:
- Approved manufacturer list (AML) — if applicable per Employer's Requirements
- Manufacturer quality certifications (ISO 9001, API, etc.)
- Manufacturer experience with similar applications
- Warranty and after-sales support requirements

**Source:** **ASSUMPTION** — Typical EPC projects may have manufacturer qualification requirements

**QR-4: Material Certification and Traceability**

Material certifications shall be provided:
- **Wetted materials:** Material test reports (MTRs) for stainless steel components
- **Hazardous area certification:** CSA/UL certification documents for electrical equipment
- **Traceability:** Equipment nameplates and serial numbers for traceability

**Retention:** Certificates retained per project quality plan and turned over to Owner at project completion.

**Source:** **ASSUMPTION** based on typical EPC quality and closeout requirements

## Standards

**I&C Discipline Standards (Applicable):**

- **ISA 5.1** — Instrumentation Symbols and Identification
  - **Application:** Instrument tagging and identification conventions
  - **TBD:** Specific clauses to be referenced

- **ISA 12.27 / IEC 60079** — Hazardous Area Instrumentation
  - **Application:** Electrical equipment for explosive atmospheres
  - **TBD:** Specific requirements per facility hazardous area classification

- **ISA 84 / IEC 61511** — Functional Safety of Safety Instrumented Systems
  - **Application:** If safety instrumented functions (SIF) are required (overfill protection, emergency shutdown)
  - **TBD:** Safety integrity level (SIL) requirements per process safety analysis

- **API 554** — Process Instrumentation and Control
  - **Application:** Industry good practice for instrument selection, installation, calibration
  - **TBD:** Specific sections relevant to level, pressure, temperature instruments

**Instrument Type-Specific Standards:**

- **API 2350** — Overfill Protection for Storage Tanks
  - **Application:** Tank overfill prevention systems (3 × 15,000 MT tanks)
  - **TBD:** Independent overfill protection requirements per Employer's Requirements

- **API MPMS Chapter 3** — Tank Gauging
  - **Application:** Custody transfer tank gauging (if applicable)
  - **TBD:** Applicability and accuracy requirements (coordinate with PKG-12)

- **ASME B40.100** — Pressure Gauges and Gauge Attachments
  - **Application:** Pressure gauge specification and installation
  - **TBD:** Accuracy grades per application

**Electrical and Hazardous Area Standards:**

- **CSA C22.1** — Canadian Electrical Code
  - **Application:** Hazardous area classification, wiring methods, equipment selection for BC location
  - **TBD:** Specific Section 18 requirements for explosive atmospheres

- **CSA C22.2 No. 60079** (IEC 60079 series) — Explosive Atmospheres
  - **Application:** Equipment design, certification, and installation in hazardous areas
  - **TBD:** Specific parts applicable to instrumentation (intrinsic safety, explosion-proof enclosures)

**Material and Construction Standards:**

- **ASTM A312/A213** — Stainless Steel Pipe and Tubing
  - **Application:** Instrument tubing material specifications (316/316L stainless steel)

- **ASME B1.20.1** — Pipe Threads
  - **Application:** Threaded instrument connections

**Quality and Testing Standards:**

- **ISO 9001** — Quality Management Systems
  - **Application:** Manufacturer quality system requirements (if applicable)

- **ASME B31.3** — Process Piping
  - **Application:** Instrument tubing and piping installation (if applicable per project piping code)
  - **TBD:** Applicability to instrument impulse piping

**Project-Specific Standards:**

- **Employer's Requirements** — Project-specific design criteria and performance standards
  - **TBD:** Specific sections to be identified from Volume 2 Parts 1-3

**Source:** Decomposition Section 3 Reference Documents (lines 75-79) — Employer's Requirements volumes listed

**Note:** Standards applicability and specific clause-level requirements **TBD** pending access to standard documents and Employer's Requirements. Current standard list is **ASSUMPTION** based on I&C discipline typical practice and Canadian regulatory context.

## Verification

**Verification Methods:**

| Requirement Type | Verification Method | Timing | Responsibility | Records |
|------------------|---------------------|--------|----------------|---------|
| Functional requirements | Design review, calculations | During design | I&C Engineer | DEL-20.03 calculations |
| Performance requirements | Vendor data review, FAT | Procurement/fabrication | I&C + Procurement | DEL-20.04 data sheets |
| Material requirements | Material certifications (MTRs) | Equipment receiving | QA/QC | Vendor certificates |
| Workmanship requirements | Site inspection, SAT | Installation/commissioning | QA/QC + Commissioning | DEL-20.05 test records |
| Hazardous area compliance | Certification review, installation inspection | Procurement + installation | I&C + Electrical + QA | Certification docs + inspection records |
| Standards compliance | Compliance matrix review | Design + procurement | I&C Lead + QA | Compliance checklist |

**Implementation:** See Procedure.md for detailed verification steps and acceptance criteria.

**Source:** **ASSUMPTION** based on typical EPC verification methods; cross-references to other PKG-20 deliverables

**Acceptance Criteria:**

The specification is acceptable for issuance and use when:
- All requirements are defined or marked **TBD** with explicit follow-up plan
- All applicable codes and standards are identified
- Interdisciplinary coordination is complete (no open IDC comments)
- Independent check is complete with sign-off
- I&C Lead Engineer has approved
- Equipment procured per specification meets all specified requirements (verified via data sheets and testing)

**Source:** **ASSUMPTION** based on typical specification deliverable acceptance criteria

**Hold Points:**

- **TBD** — Hold points for Employer review to be identified per project execution plan
- **ASSUMPTION**: Typical hold points may include specification issue for Employer review/approval before equipment procurement

## Documentation

**Required Documentation Outputs:**

1. **Level Instrument Specification**
   - Scope and applicability (tank level, process level, loading level)
   - Performance requirements (accuracy, range, response time)
   - Technology requirements (radar, guided wave, float, switches)
   - Material requirements (wetted parts, enclosures, accessories)
   - Installation and calibration requirements
   - Testing and acceptance criteria
   - **Format:** **TBD** — Specification document format per project standards

2. **Pressure Instrument Specification**
   - Scope and applicability (pump monitoring, piping pressure, differential pressure)
   - Performance requirements (accuracy, range, overpressure rating)
   - Technology requirements (transmitters, gauges, switches)
   - Material requirements (wetted parts, enclosures, connections)
   - Installation and calibration requirements
   - Testing and acceptance criteria
   - **Format:** **TBD** — Specification document format per project standards

3. **Temperature Specification**
   - Scope and applicability (product temperature, equipment protection, ambient)
   - Performance requirements (accuracy, range, response time)
   - Technology requirements (RTDs, thermocouples, switches, thermowells)
   - Material requirements (element materials, thermowell materials, connections)
   - Installation and calibration requirements
   - Testing and acceptance criteria
   - **Format:** **TBD** — Specification document format per project standards

**Source:** Decomposition DEL-20.02 Anticipated Artifacts (line 497)

**Specification Organization (Typical):**

Each specification section (level, pressure, temperature) may be organized as:
1. **Scope** — Applicability and coverage
2. **References** — Applicable codes, standards, and related documents
3. **Definitions** — Terms and abbreviations
4. **Performance Requirements** — Measurement ranges, accuracies, environmental ratings
5. **Material Requirements** — Wetted materials, enclosures, accessories
6. **Design Requirements** — Configuration, features, options
7. **Workmanship Requirements** — Installation methods, calibration, testing
8. **Quality Assurance** — Certifications, testing, documentation
9. **Submittals** — Vendor data requirements (coordinate with DEL-20.04)

**Source:** **ASSUMPTION** based on typical technical specification format (CSI MasterFormat or discipline-specific)

**Documentation Management:**

- All specifications shall be managed per project document control procedures — **TBD**: Document management system
- Specifications shall be revision-controlled and distributed per project change management procedures
- Final issue shall be part of project closeout documentation (operations and maintenance manuals)

**Source:** **ASSUMPTION** based on typical EPC document management

**Supporting Documentation:**

- Design calculations (DEL-20.03) support specification requirements
- Equipment data sheets (DEL-20.04) demonstrate specification compliance
- Installation drawings (DEL-20.01) implement specification requirements
- Test records (DEL-20.05) verify specification compliance

**Source:** Cross-reference to related PKG-20 deliverables per decomposition (lines 496-500)

**Project Objective Alignment:**

This deliverable supports **OBJ-1: Safe & Reliable Operation** — Proper specification of instrument performance, materials, and workmanship ensures field instruments are fit for purpose and support safe, reliable facility operations.

**Source:** Decomposition Section 6 Objective-to-Deliverable Mapping (line 780)

## Cross-Document Traceability

This Specification defines the requirements for DEL-20.02. The following documents provide complementary information:

| Document | Purpose | Key Linkages |
|----------|---------|--------------|
| Datasheet.md | Factual identification, attributes, conditions, references | Conditions § provides operating context for FR-2 to FR-5; Construction § defines instrument types and technologies |
| Guidance.md | Engineering rationale and decision context | Principles explain "why" behind requirements; Trade-offs address design options; Examples illustrate application |
| Procedure.md | Production workflow and verification steps | Steps 1-5 implement requirements; Verification section implements QR-1 to QR-4 |

**Requirement-to-Guidance Mapping:**

| Requirement | Guidance Section | Rationale Summary |
|-------------|------------------|-------------------|
| FR-1 Measurement Performance | Principle 2 | Right instrument for application ensures measurement integrity |
| FR-2 Level Measurement | Level Instruments, Trade-off 1 | Technology selection and accuracy considerations |
| FR-3 Pressure Measurement | Pressure Instruments | Technology selection and range considerations |
| FR-4 Temperature Measurement | Temperature Instruments | Technology selection and thermowell considerations |
| FR-5 Accessories | Coordination Considerations | Complete installations require accessories |
| PR-2 Environmental Ratings | Principle 3 | Marine environment drives material and protection requirements |
| PR-3 Hazardous Area | Principle 4 | Canola oil combustibility requires electrical safety |
| PR-5 Design Life | Principle 5 | Lifecycle cost vs. capital cost balance |
