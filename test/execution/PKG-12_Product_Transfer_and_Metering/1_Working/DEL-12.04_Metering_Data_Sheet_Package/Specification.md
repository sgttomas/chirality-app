# Specification: DEL-12.04 Metering Data Sheet Package

## Scope

### Deliverable Definition

This specification defines the requirements for the **Metering Data Sheet Package** deliverable within **PKG-12 Product Transfer & Metering**.

DEL-12.04 defines and substantiates metering in accordance with Employer's Requirements (Source: Decomposition:359).

### Package Scope Context

PKG-12 scope covers custody transfer flow meters (rail unloading and marine loading) and metering instrumentation (Source: Decomposition:350).

The facility transfers CSD (Crude Super Degummed) canola oil from rail tank cars to storage tanks (via rail unloading metering) and from storage tanks to liquid bulk carriers for export (via marine loading metering), with a permitted throughput of 1,000,000 MT per annum (Source: Decomposition:41, 43).

### Inclusions

The data sheet package shall include, at minimum:

| Artifact | Description | Source |
|----------|-------------|--------|
| Flow Meter Data Sheets (2) | Data sheets for custody transfer flow meters: (1) rail unloading service, (2) marine loading service | Decomposition:359 |
| Temperature/Pressure Transmitter Data Sheets | Data sheets for temperature transmitter(s) and pressure transmitter(s) (if applicable) for custody transfer compensation | Decomposition:359 |

**Note:** Decomposition specifies "flow meter data sheets (2)" indicating separate data sheets for rail unloading and marine loading services (Source: Decomposition:359).

### Exclusions

The following are outside the scope of DEL-12.04:

- General field instrumentation data sheets for non-metering instruments (covered in PKG-20 Field Instrumentation, except metering-specific instruments which are in this deliverable)
- Control system I/O lists and database (covered in PKG-19 Control Systems)
- Valve data sheets (covered in PKG-16 Valves, if separate valve package exists, or PKG-14 Process Piping)
- Pump data sheets for transfer pumps (covered in PKG-15 Pumps)

## Requirements

### Functional Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-01 | The data sheet package shall include all decomposition-listed artifacts: (1) flow meter data sheet for rail unloading, (2) flow meter data sheet for marine loading, (3) temperature transmitter data sheet(s), (4) pressure transmitter data sheet(s) if applicable | Decomposition:359 | Checklist review per Procedure.md Step 1.1 |
| REQ-02 | Data sheets shall identify service, tag number, and design conditions for each meter and instrument including: service description (rail unloading or marine loading custody transfer), tag number per project tag numbering system, P&ID reference, normal/design/min/max operating conditions | TBD; ER Vol 2 Part 2, location TBD; ASSUMPTION based on data sheet standards | Document review per Procedure.md Step 3 |
| REQ-03 | Data sheets shall capture interface requirements for installation including: process connections (size, rating, type), electrical power supply (voltage, frequency), signal outputs (type, protocol), communication interfaces, mounting and orientation requirements, straight-run requirements (for flow meters) | ASSUMPTION based on installation coordination needs | Document review per Procedure.md Step 3; IDC review per Procedure.md interface coordination |
| REQ-04 | Tag numbers on data sheets shall be consistent with P&IDs (PKG-14), metering specification (DEL-12.02), and drawings (DEL-12.01) | ASSUMPTION; cross-document consistency | Cross-reference check per Procedure.md Step 5.1 |

### Performance Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-05 | Data sheet performance fields shall be consistent with DEL-12.02 metering specification requirements: accuracy class, repeatability, turndown ratio, flow range, materials, proving requirements from specification shall be documented in data sheets | ASSUMPTION; cross-document consistency | Cross-reference review per Procedure.md Step 5.1 |
| REQ-06 | Data sheet parameters shall be consistent with DEL-12.03 calculation basis: flow ranges, meter sizes, accuracy/uncertainty values, proving criteria from calculations shall be documented in data sheets | ASSUMPTION; cross-document consistency | Cross-reference review per Procedure.md Step 5.2 |
| REQ-07 | Flow meter data sheets shall document accuracy class, repeatability, and expanded uncertainty per DEL-12.03 uncertainty budget to support OBJ-10 custody transfer accuracy | Decomposition:789; DEL-12.03 | Technical review; OBJ-10 alignment check |
| REQ-08 | Flow meter data sheets shall document flow ranges (normal, design, min, max) per DEL-12.03 sizing calculations to support OBJ-2 throughput capacity | Decomposition:781; DEL-12.03 | Technical review; OBJ-2 alignment check |
| REQ-09 | Performance values (accuracy, flow ranges, materials, electrical specifications) are TBD pending ER Vol 2 Part 2 extraction, DEL-12.02 specification finalization, and vendor data availability | TBD; ER Vol 2 Part 2, location TBD | Technical review; verify TBD items are flagged |

### Data Quality Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-10 | Each data sheet shall include verification basis column or notes indicating source for critical fields: "ER Vol 2 Part 2 Clause X.X.X" for ER-derived requirements, "DEL-12.02 Specification Section Y" for specification requirements, "DEL-12.03 Calculation" for calculated values, "Vendor Certified Data" for manufacturer-certified parameters, "ASSUMPTION — rationale" for inferred values, "TBD — source needed" for unknown values | ASSUMPTION; traceability and auditability | Document review per Procedure.md Step 3.6; verification basis completeness check |
| REQ-11 | Data sheets shall include calibration and certification requirements enabling DEL-12.05 compliance verification: calibration range, calibration traceability (traceable to Measurement Canada, NIST, or equivalent), calibration interval, certificates required (calibration certificate, material certificates, Measurement Canada approval if applicable), proving requirements for flow meters | ASSUMPTION; ties to Decomposition:360 and DEL-12.05 | Document review per Procedure.md Step 3; verify calibration fields present |
| REQ-12 | Unknown data sheet fields shall be marked TBD with source needed; no fields shall be left blank without TBD or N/A designation | Epistemic rule | Document review; TBD/N/A completeness check |

### Interface Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-13 | Data sheets shall capture interface requirements for electrical/controls integration with PKG-17 (power supply), PKG-19 (signals, communications), and PKG-20 (transmitter integration): power supply voltage and frequency, signal output types (4-20 mA, HART, digital), communication protocols (Modbus, Profibus, Foundation Fieldbus, or other), area classification and certifications, cable and conduit requirements | ASSUMPTION based on interface coordination | IDC review per Procedure.md interface coordination; verify interface fields documented |
| REQ-14 | Interface coordination with adjacent packages (PKG-14 for P&IDs and tag numbers, PKG-17 for electrical, PKG-19 for controls, PKG-20 for instrumentation) is managed externally per dependency mode NOT_TRACKED | _DEPENDENCIES.md | Coordination meeting; verify coordination occurs |

### Quality Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-15 | Data sheets shall be independently reviewed for completeness, accuracy, and consistency before issue | ASSUMPTION; project quality procedures | Check record per Procedure.md Step 6 |
| REQ-16 | Data sheets shall include revision history documenting: revision number, date, description of changes, originator, checker, approver | ASSUMPTION; document control requirement | Revision history review |
| REQ-17 | All work shall comply with project Quality Management Plan | ASSUMPTION | QA/QC audit |

## Standards

### Governing References

| Standard/Reference | Applicability | Source |
|--------------------|---------------|--------|
| Employer's Requirements Vol 2 Part 1 | General requirements, document control, tag numbering system, data sheet format standards | TBD |
| Employer's Requirements Vol 2 Part 2 | Process mechanical requirements, metering requirements, operating conditions, fluid properties, accuracy requirements, proving requirements, hazardous area classification | TBD |
| Project Document Control Procedures | Data sheet numbering, revision control, approval requirements | TBD |
| Project Tag Numbering System | Instrument and equipment tag numbering conventions | TBD |

### Custody Transfer Metering Standards (TBD — ASSUMPTION)

The following standards may define required data sheet fields for custody transfer equipment:

| Standard | Potential Applicability |
|----------|------------------------|
| API MPMS (Manual of Petroleum Measurement Standards) | May specify data sheet requirements for custody transfer meters and proving equipment |
| OIML R117 (Dynamic Measuring Systems for Liquids Other Than Water) | May specify required data for custody transfer measuring systems |
| Measurement Canada | May specify required data sheet fields for meters requiring Canadian custody transfer approval |

**Note:** Standard applicability to be confirmed from ER Vol 2 Part 2 and DEL-12.02 specification.

## Verification

### Verification Methods

| Method | Description | Applicable Requirements |
|--------|-------------|------------------------|
| Checklist Review | Verify presence of all decomposition-listed data sheets (flow meters ×2, temperature transmitters, pressure transmitters) | REQ-01 |
| Document Review | Review data sheets for completeness: verify all required field categories populated or marked TBD; verify verification basis documented | REQ-02, REQ-03, REQ-09, REQ-10, REQ-11, REQ-12 |
| Cross-Reference Review | Verify consistency with DEL-12.01 (tag numbers), DEL-12.02 (performance requirements), and DEL-12.03 (calculated parameters) | REQ-04, REQ-05, REQ-06 |
| Vendor Data Verification | Verify vendor-certified values are documented and vendor data sheets are referenced | REQ-09, vendor data incorporation |
| IDC Review | Review interface fields with impacted disciplines (PKG-14, PKG-17, PKG-19, PKG-20) to verify interface parameters are correct | REQ-13, REQ-14 |
| Independent Check | Independent reviewer verifies data sheet completeness, accuracy, and consistency | REQ-15 |
| OBJ Alignment Review | Verify data sheets support OBJ-2 (throughput: flow ranges adequate) and OBJ-10 (accuracy: accuracy class, calibration, proving documented) | REQ-07, REQ-08 |

### Acceptance Criteria

| Criterion | Description | Source |
|-----------|-------------|--------|
| Artifact Completeness | All data sheets present: (1) flow meter rail unloading, (2) flow meter marine loading, (3) temperature transmitter(s), (4) pressure transmitter(s) if applicable | Decomposition:359; REQ-01 |
| Field Completeness | All required field categories populated or marked TBD with source needed; no blank fields without TBD or N/A | REQ-02, REQ-03, REQ-12 |
| Tag Consistency | Tag numbers consistent with P&IDs (PKG-14), DEL-12.01 drawings, and DEL-12.02 specification | REQ-04 |
| Specification Consistency | Data sheet parameters consistent with DEL-12.02 specification requirements (accuracy, repeatability, materials, proving) | REQ-05 |
| Calculation Consistency | Data sheet parameters consistent with DEL-12.03 calculations (flow ranges, meter sizes, uncertainty, proving criteria) | REQ-06 |
| Vendor Data Documented | Vendor-certified values identified and referenced to vendor data sheets | REQ-09 |
| Verification Basis | Verification basis documented for critical fields (ER clause, specification section, calculation, vendor data, assumption, or TBD) | REQ-10 |
| Calibration Fields | Calibration requirements documented enabling DEL-12.05 compliance verification (calibration range, traceability, interval, certificates required, proving requirements for flow meters) | REQ-11 |
| Interface Coverage | Interface fields documented for electrical/controls integration (power supply, signals, communications) | REQ-13 |
| Check Complete | Independent check record complete with reviewer signature | REQ-15 |

## Documentation

### Required Documentation Outputs

| Output | Description | Source |
|--------|-------------|--------|
| Flow Meter Data Sheet — Rail Unloading | Custody transfer flow meter data sheet for rail unloading service with all field categories per Datasheet.md Construction section | Decomposition:359; REQ-01, REQ-02, REQ-03, REQ-07, REQ-08 |
| Flow Meter Data Sheet — Marine Loading | Custody transfer flow meter data sheet for marine loading service with all field categories per Datasheet.md Construction section | Decomposition:359; REQ-01, REQ-02, REQ-03, REQ-07, REQ-08 |
| Temperature Transmitter Data Sheet(s) | Temperature measurement data sheet(s) for custody transfer compensation; separate data sheets for rail and marine if transmitter specifications differ, or combined data sheet if identical transmitters | Decomposition:359; REQ-01, REQ-02, REQ-03 |
| Pressure Transmitter Data Sheet(s) | Pressure measurement data sheet(s) for custody transfer compensation if applicable (may not be required if canola oil compressibility is negligible; TBD from DEL-12.03); separate data sheets for rail and marine if specifications differ | Decomposition:359; REQ-01, REQ-02, REQ-03 |
| Data Sheet Index | Index listing all data sheets with tag numbers, equipment descriptions, data sheet numbers, and revisions | ASSUMPTION; Procedure.md Step 1.4 |

### Data Sheet Field Requirements

Data sheets shall include the following field categories per Datasheet.md Construction section (ASSUMPTION based on typical custody transfer metering data sheets; specific fields may vary per project standards):

#### Flow Meter Data Sheet Fields (required fields for each flow meter data sheet)

| Field Category | Required Fields | Source |
|----------------|-----------------|--------|
| Identification | Tag number, service description, P&ID reference, location, equipment description | REQ-02; Datasheet.md |
| Process Conditions | Service (rail unloading or marine loading), product (CSD canola oil), normal flow rate, design flow rate, minimum flow rate, maximum flow rate, operating temperature (normal and range), operating pressure (normal and range), product density, product viscosity | REQ-02; operating conditions from ER Vol 2 Part 2 (TBD) |
| Performance | Meter type, accuracy class, repeatability, turndown ratio, expanded uncertainty, flow range (min to max with accuracy), pressure drop (at max flow), response time (if control-relevant) | REQ-07, REQ-08; performance from DEL-12.02 and DEL-12.03 |
| Materials | Wetted materials (body, internals, seals/gaskets), housing material, pressure rating, temperature rating | REQ-05; materials from DEL-12.02 |
| Electrical / Controls | Power supply (voltage, frequency, power consumption), signal outputs (flow, density if Coriolis, temperature if integral, totalizer pulse), communication protocol, area classification, electrical certification, cable entries | REQ-03, REQ-13; electrical from DEL-12.02; coordinate with PKG-17, PKG-19 |
| Physical | Meter size (line size), process connections (size, rating, facing), meter length (face-to-face), weight (empty, filled), mounting orientation, straight-run requirements | REQ-03, REQ-06; sizing from DEL-12.03; physical from vendor data |
| Calibration / Proving | Calibration range, calibration traceability, calibration interval, proving method, meter factor range, meter factor drift limit, proving acceptance criteria, proving frequency | REQ-11; calibration and proving from DEL-12.02 and DEL-12.03 |
| Vendor | Manufacturer, model number, vendor data sheet reference, serial number (TBD until procurement), vendor certifications (calibration certificate, material certificates, Measurement Canada approval if applicable) | REQ-10; vendor data |
| Verification Basis | For each critical field, indicate verification basis (ER clause, specification section, calculation, vendor certified, assumption, or TBD) | REQ-10; traceability |

#### Temperature Transmitter Data Sheet Fields

| Field Category | Required Fields | Source |
|----------------|-----------------|--------|
| Identification | Tag number, service description, P&ID reference, location | REQ-02 |
| Process Conditions | Service, product, normal temperature, design temperature range, installation type | REQ-02; from ER Vol 2 Part 2 (TBD) |
| Performance | Sensor type (RTD Pt100/Pt1000, thermocouple), accuracy, measurement range, response time, drift | REQ-03, REQ-05; from DEL-12.02 |
| Electrical | Power supply, signal output, communication protocol, area classification, electrical certification | REQ-03, REQ-13; from PKG-19, PKG-20 |
| Physical | Sensor length, process connection, housing, cable entries, environmental rating | REQ-03; from vendor data |
| Calibration | Calibration range, calibration traceability, calibration interval | REQ-11; from DEL-12.02 |
| Vendor | Manufacturer, model, vendor data sheet reference, serial number (TBD) | Vendor data |
| Verification Basis | Source for each critical field | REQ-10 |

#### Pressure Transmitter Data Sheet Fields (if applicable)

| Field Category | Required Fields | Source |
|----------------|-----------------|--------|
| Identification | Tag number, service description, P&ID reference, location | REQ-02 |
| Process Conditions | Service, product, normal pressure, design pressure range, pressure type (gauge, absolute, differential) | REQ-02; from ER Vol 2 Part 2 (TBD) |
| Performance | Measurement range, accuracy, turndown, overpressure rating, burst pressure | REQ-03, REQ-05; from DEL-12.02 |
| Electrical | Power supply, signal output, communication protocol, area classification, electrical certification | REQ-03, REQ-13; from PKG-19, PKG-20 |
| Physical | Process connection, housing, mounting, cable entries, environmental rating | REQ-03; from vendor data |
| Calibration | Calibration range, calibration points, calibration traceability, calibration interval | REQ-11; from DEL-12.02 |
| Vendor | Manufacturer, model, vendor data sheet reference, serial number (TBD) | Vendor data |
| Verification Basis | Source for each critical field | REQ-10 |

### Documentation Requirements

| Requirement | Description | Source |
|-------------|-------------|--------|
| Vendor Certification | Vendor-certified data clearly marked in verification basis column or notes | REQ-10 |
| TBD Fields | Unknown fields marked TBD with source needed; no blank fields without TBD or N/A designation | REQ-12; epistemic rule |
| Cross-Reference | Data sheets reference related deliverables: DEL-12.01 for installation details, DEL-12.02 for specification requirements, DEL-12.03 for calculated parameters | REQ-04, REQ-05, REQ-06 |
| Revision Control | Per project document control procedures; revision history documented per REQ-16 | TBD; ER Vol 2 Part 1 |

## Cross-Document Traceability

| Document | Section | Traceability Points |
|----------|---------|---------------------|
| Datasheet.md | § Identification | DEL-12.04 identity, discipline (Process), type (Data Sheet), responsible party (D&B Contractor) |
| Datasheet.md | § Attributes | Data sheet attributes (numbers TBD, equipment tags TBD, service description, revision, classification, count, format) |
| Datasheet.md | § Conditions | Design context (service application, product CSD canola oil, throughput 1M MT/a, metering points); design basis parameters (all TBD) per REQ-09; objective alignment (OBJ-2 per REQ-08, OBJ-10 per REQ-07) |
| Datasheet.md | § Construction | Anticipated data sheet content (flow meters ×2 per REQ-01, temperature transmitters, pressure transmitters); data sheet field categories (Identification per REQ-02, Process Conditions per REQ-02, Performance per REQ-07/08, Materials per REQ-05, Electrical/Controls per REQ-03/13, Physical per REQ-03, Calibration/Proving per REQ-11, Vendor per REQ-09, Verification Basis per REQ-10) matching field requirements |
| Guidance.md | § Purpose | Data sheets as structured, auditable single source of truth for equipment parameters; lifecycle use (design, procurement, installation, testing, operations); links specification (DEL-12.02) and calculations (DEL-12.03) to physical equipment per REQ-05/06 |
| Guidance.md | § Principles | Development rationale: single source of truth (REQ-05/06), traceability (REQ-10), consistency (REQ-04/05/06), no invention (REQ-12); custody transfer principles: accuracy capture (REQ-07), calibration traceability (REQ-11), proving fields (REQ-11) |
| Guidance.md | § Considerations | Content: service differentiation (REQ-02), vendor data timing, interface fields (REQ-03/13), calibration fields (REQ-11); flow meter fields (flow range REQ-08, accuracy REQ-07, materials REQ-05, connections REQ-03, electrical REQ-13, proving REQ-11); transmitter fields (range REQ-02, accuracy REQ-05, signal REQ-13, calibration REQ-11); service-specific (rail batch, marine continuous); data sheet timing (inquiry/order/delivery) |
| Guidance.md | § Trade-offs | Standardization vs. optimization, accuracy vs. cost, vendor lock-in vs. flexibility, detail level |
| Procedure.md | § Step 1 | Identify data sheets per REQ-01; assign tag numbers per REQ-02/04; create index |
| Procedure.md | § Step 2 | Establish template with field categories per field requirements |
| Procedure.md | § Step 3 | Populate design basis from ER, DEL-12.02, DEL-12.03 per REQ-05/06; document verification basis per REQ-10; mark TBD per REQ-09/12 |
| Procedure.md | § Step 4 | Obtain vendor data; incorporate per REQ-09; mark vendor-certified per REQ-10 |
| Procedure.md | § Step 5 | Cross-check: DEL-12.02 per REQ-05, DEL-12.03 per REQ-06, DEL-12.01 per REQ-04, interfaces per REQ-13/14 |
| Procedure.md | § Step 6 | Independent check per REQ-15; issue per REQ-16/17 |
| Procedure.md | § Verification | Verification activities mapped to requirements; acceptance criteria per Acceptance Criteria section |
| Procedure.md | § Records | Data sheet outputs matching Documentation section; independent check record per REQ-15
