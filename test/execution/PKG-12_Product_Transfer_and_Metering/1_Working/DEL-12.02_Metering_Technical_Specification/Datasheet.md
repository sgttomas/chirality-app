# Datasheet: DEL-12.02 Metering Technical Specification

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-12.02 |
| Name | Metering Technical Specification |
| Package | PKG-12 Product Transfer & Metering |
| Discipline | Process |
| Type | Specification |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Document Number | To be issued per project numbering system (TBD; Source: ER Vol 2 Part 1, location TBD) |
| Specification Type | Technical Specification — Process Metering / Custody Transfer |
| Revision | 00 (initial issue) |
| Classification | Process — Custody Transfer Metering |
| Format | Text specification document (Word, PDF, or per project standards; TBD) |
| Estimated Length | 30-50 pages including requirements, installation details, testing procedures, and appendices (ASSUMPTION based on typical custody transfer metering specifications) |

## Conditions

### Design Context

| Condition | Value / Description | Source |
|-----------|---------------------|--------|
| Service Application | Custody transfer metering for CSD canola oil at rail unloading and marine loading transfer points | Decomposition:350 |
| Product | CSD (Crude Super Degummed) canola oil | Decomposition:43 |
| Design Throughput | 1,000,000 MT per annum (permitted) | Decomposition:41 |
| Metering Points | Two primary custody transfer locations: (1) Rail unloading — measuring product received from rail tank cars; (2) Marine loading — measuring product delivered to liquid bulk carriers for export | Decomposition:350 |
| Operating Temperature Range | TBD (Source: ER Vol 2 Part 2, location TBD) |
| Design Pressure | TBD (Source: ER Vol 2 Part 2, location TBD) |
| Fluid Properties | CSD canola oil; specific properties TBD: density at operating temperature, viscosity vs. temperature curve, vapor pressure, pour point, flash point (Source: ER Vol 2 Part 2, location TBD) |
| Viscosity Range | TBD — CSD canola oil viscosity at operating conditions affects meter technology selection and performance (Source: ER Vol 2 Part 2, location TBD) |
| Hazardous Area Classification | TBD; affects electrical equipment selection for metering system (Source: ER Vol 2 Part 2, location TBD) |
| Environmental Exposure | Outdoor installation at Fraser Surrey Terminal; Pacific Northwest climate (rain, temperature range, wind, seismic) (TBD; ER Vol 2 Part 1) |

### Objective Alignment

| Objective | Relevance to This Deliverable |
|-----------|-------------------------------|
| OBJ-2 Throughput Capacity (1,000,000 MT/a) | Specification must define metering performance (flow range, turndown, pressure drop) that does not constrain the 1,000,000 MT/a throughput; meter sizing must accommodate design flow rates for both rail unloading and marine loading services (Source: Decomposition:781; Specification.md REQ-08) |
| OBJ-10 Custody Transfer Accuracy | Specification must define accuracy class, repeatability, uncertainty budget, and proving requirements for custody transfer measurement; specification requirements drive DEL-12.01 drawings, DEL-12.03 calculations, and DEL-12.05 verification records (Source: Decomposition:789; Specification.md REQ-09) |
| OBJ-6 Regulatory Compliance | Specification must ensure compliance with Measurement Canada and applicable custody transfer regulations for commercial transactions (ASSUMPTION based on Canadian location; TBD verification from ER) |

## Construction

### Anticipated Specification Content

| Artifact | Description | Source |
|----------|-------------|--------|
| Custody Transfer Flow Meter Specification | Performance, materials, installation, and testing requirements for custody transfer flow meters serving rail unloading and marine loading; includes accuracy requirements, flow range, meter technology, materials of construction, installation requirements (straight-run, orientation, mounting), electrical/controls interfaces, proving requirements, and acceptance criteria | Decomposition:357; Specification.md REQ-02 |
| Metering System Specification | System-level requirements including metering instrumentation (temperature, pressure, density transmitters as applicable), proving system (in-line prover, portable prover, or master meter), integration with control system, data logging and totalizing, QA requirements (certificates, calibration traceability, FAT/SAT), and documentation submittals | Decomposition:357; Specification.md REQ-02 |

### Key Specification Topics

The specification must address the following topics (ASSUMPTION based on typical custody transfer metering specifications; specific requirements TBD from ER Vol 2 Part 2):

| Topic | Coverage | Specification.md Reference |
|-------|----------|---------------------------|
| Performance Requirements | Accuracy class (e.g., ±0.15%, ±0.25%, TBD), uncertainty budget, repeatability (e.g., ±0.05%, TBD), turndown ratio (flow range from minimum to maximum measurable flow), response time, linearity | REQ-05, REQ-06, REQ-07, REQ-09 |
| Flow Range | Design flow rate, normal flow rate, minimum flow rate, maximum flow rate for rail unloading service; design flow rate, normal flow rate, minimum flow rate, maximum flow rate for marine loading service; flow rates to be specified per DEL-12.03 calculations | REQ-08 |
| Meter Technology | Technology selection (Coriolis mass flowmeter, ultrasonic flowmeter, turbine flowmeter, positive displacement flowmeter, or other); technology drives accuracy, straight-run requirements, proving approach, pressure drop, and cost | Guidance.md Technology Selection Factors |
| Materials | Wetted parts materials compatible with CSD canola oil (stainless steel, carbon steel, or other; TBD); body material, internal components, seals and gaskets; corrosion resistance, cleanability, food-grade materials if required | REQ-03 |
| Installation Requirements | Straight-run requirements upstream and downstream (e.g., 10D upstream, 5D downstream; TBD per meter technology and manufacturer); orientation (horizontal, vertical, or inclined; TBD per meter type); mounting and support requirements; instrument tap locations for temperature, pressure, density measurement; access for proving and maintenance | Links to DEL-12.01 drawings |
| Proving Requirements | Proving method (in-line prover with sphere or piston, portable prover, master meter, or combination); proving frequency (e.g., quarterly, semi-annually, annually, or per operational schedule; TBD); acceptance criteria for proving (e.g., meter factor drift <±0.05%; TBD); proving connections and isolation | REQ-04; Specification.md REQ-09 |
| Instrumentation | Temperature measurement (transmitter type, range, accuracy; e.g., RTD Pt100, ±0.1°C; TBD); pressure measurement (transmitter type, range, accuracy; e.g., ±0.1% of span; TBD); density measurement if applicable (for mass flow compensation or direct mass measurement; TBD per meter technology) | REQ-03; Specification.md |
| Electrical/Controls | Power supply requirements (voltage, frequency, power consumption; TBD); signal outputs (4-20 mA, pulse, digital communication; TBD); communication protocols (Modbus, HART, Profibus, or other; TBD); integration with control system (PKG-19); area classification compliance (intrinsically safe, explosion-proof, or general purpose; TBD) | REQ-10 interface requirements |
| QA Requirements | Calibration certificates traceable to national standards (Measurement Canada, NIST, or equivalent); material certificates (MTRs) for wetted components; factory acceptance test (FAT) requirements and acceptance criteria; site acceptance test (SAT) requirements; inspection and test plan (ITP); as-built documentation | REQ-12, REQ-13; links to DEL-12.05 |

### Specification Structure (ASSUMPTION)

Typical section structure for custody transfer metering technical specification:

| Section | Content |
|---------|---------|
| 1. Scope and Service Description | Rail unloading and marine loading metering scope; CSD canola oil product; custody transfer application; system boundaries (included/excluded) |
| 2. Definitions and Abbreviations | Custody transfer terminology (accuracy, repeatability, proving, meter factor, uncertainty, turndown); abbreviations (FAT, SAT, MTR, ITP, etc.) |
| 3. Reference Documents and Standards | ER references, applicable custody transfer standards (API MPMS, OIML R117, Measurement Canada), codes and regulations |
| 4. Technical Requirements | Performance (accuracy, repeatability, uncertainty), flow range and sizing, materials of construction, environmental ratings, hazardous area classification |
| 5. Design and Installation | Meter selection and sizing basis (reference DEL-12.03 calculations), installation requirements (straight-run, orientation, mounting, supports), instrument tap locations, piping arrangement (bypass, isolation, proving connections) |
| 6. Proving Requirements | Proving method and equipment, proving frequency and procedures, acceptance criteria for proving, prover calibration and traceability |
| 7. Electrical and Controls | Power supply, signal outputs and protocols, integration with control system (PKG-19), data logging and totalizing, alarm and interlock functions |
| 8. Inspection, Testing, and Acceptance | Factory acceptance test (FAT) procedures and criteria, site acceptance test (SAT) procedures and criteria, calibration procedures, proving procedures, installation inspection |
| 9. Documentation and Submittals | Data sheets (reference DEL-12.04), drawings (reference DEL-12.01), calculations (reference DEL-12.03), certificates and test records (reference DEL-12.05), operation and maintenance manuals |
| 10. Quality Assurance | Quality plan and ITP, hold points and witness points, nonconformance handling, material traceability |
| 11. Appendices | Requirements traceability matrix (map clauses to ER references), flow diagrams, proving schematics, data sheets templates |

## References

### Primary Sources

| Reference | Content | Location |
|-----------|---------|----------|
| Decomposition | PKG-12 scope definition, DEL-12.02 definition, objective mappings | Lines 41, 43, 350, 357, 781, 789 |
| ER Vol 2 Part 1 | General requirements, document control, quality procedures | TBD |
| ER Vol 2 Part 2 | Process mechanical requirements, metering technical requirements, accuracy criteria, fluid properties, operating conditions, hazardous area classification | TBD |

### Related Deliverables (PKG-12)

| Deliverable | Relationship |
|-------------|--------------|
| DEL-12.01 Metering Design Drawing Set | Drawings implement metering arrangements per this specification; installation requirements in this specification drive drawing content (straight-run dimensions, orientation, instrument tap locations); tag numbers in drawings must match this specification |
| DEL-12.03 Metering Design Calculations | Calculations verify meter sizing and performance per this specification; flow rates, pressure drops, and straight-run requirements calculated in DEL-12.03 must align with specification requirements |
| DEL-12.04 Metering Data Sheet Package | Data sheets capture specific instrument parameters per this specification; data sheets document compliance with specification requirements (accuracy, flow range, materials, electrical) |
| DEL-12.05 Metering Installation & Test Records | Test records demonstrate compliance with this specification; FAT, SAT, calibration, and proving records per specification requirements (REQ-12, REQ-13) |

### Applicable Standards (TBD — ASSUMPTION)

The following custody transfer metering standards may be applicable; specific applicability to be confirmed from ER Vol 2 Part 2:

| Standard | Description | Potential Applicability |
|----------|-------------|------------------------|
| API MPMS (Manual of Petroleum Measurement Standards) | Comprehensive custody transfer measurement standards for petroleum products | May be applicable to vegetable oil custody transfer; commonly referenced even for non-petroleum liquids; specific chapters TBD (e.g., Chapter 4 Proving Systems, Chapter 5 Metering, Chapter 11 Physical Properties) |
| OIML R117 | International Recommendation: Dynamic measuring systems for liquids other than water | Likely applicable as primary standard for vegetable oil metering; covers accuracy classes, installation requirements, proving |
| Measurement Canada | Canadian custody transfer regulations and approval requirements | Applicable for custody transfer in Canada; meters may require Measurement Canada approval; specific requirements TBD |
| ISO 9001 | Quality management systems | General QMS requirements applicable to specification development and equipment procurement |
| IEC 60079 series | Electrical apparatus for explosive atmospheres | Applicable if metering is in hazardous area; governs electrical equipment selection |

**Note:** Standard applicability and specific clause requirements to be confirmed from ER Vol 2 Part 2 and project basis documents.

## Cross-Document Traceability

| Document | Section | Link Points |
|----------|---------|-------------|
| Specification.md | § Scope | Defines inclusions (custody transfer flow meter specification, metering system specification) and exclusions (control system architecture PKG-19, field instrumentation PKG-20, process piping PKG-14, electrical distribution PKG-17) |
| Specification.md | § Requirements | REQ-01 through REQ-24 define what this specification deliverable must contain: functional requirements (REQ-01 through REQ-05), performance requirements (REQ-06 through REQ-10), material requirements (REQ-11, REQ-12), installation requirements (REQ-13, REQ-14), interface requirements (REQ-15, REQ-16), proving requirements (REQ-17, REQ-18, REQ-19), quality requirements (REQ-20, REQ-21, REQ-22), documentation requirements (REQ-23, REQ-24) |
| Specification.md | § Standards | Identifies governing references (ER Vol 2 Part 1/2) and custody transfer standards (API MPMS, OIML R117, Measurement Canada, ISO 5024, IEC 60079) |
| Specification.md | § Verification | Defines review methods (document review, technical review, cross-document check, IDC review, traceability matrix review) and acceptance criteria (artifact completeness, service coverage, traceability, testability, interface coverage) |
| Guidance.md | § Purpose | Explains that this specification drives DEL-12.01 drawings, DEL-12.03 calculations, DEL-12.04 data sheets, procurement, and DEL-12.05 QA records |
| Guidance.md | § Principles | Explains specification development rationale (contract alignment per REQ-24, objective support per REQ-09/REQ-10, testability per REQ-21, traceability, technology neutrality) and custody transfer metering principles (accuracy/uncertainty per REQ-06, repeatability per REQ-08, proving per REQ-04/REQ-17-19, compensation per REQ-03) |
| Guidance.md | § Considerations | Technology selection factors (Coriolis, ultrasonic, turbine, positive displacement per REQ-05), product properties (CSD canola oil viscosity, density, temperature per REQ-11), flow range (rail vs. marine per REQ-07/REQ-09), proving method (in-line, portable, master meter per REQ-17); service-specific (rail unloading 32 stations, marine loading high flow per REQ-01); interface (PKG-14/17/19/20 per REQ-15/REQ-16) |
| Guidance.md | § Trade-offs | Competing factors: accuracy vs. cost, accuracy vs. pressure drop, standardization vs. optimization, robustness vs. sensitivity, proving frequency vs. operational impact, in-line vs. portable prover |
| Procedure.md | § Step 1 | Gather basis from ER Vol 2 Part 2, applicable standards (API MPMS, OIML R117, Measurement Canada), design basis, objectives |
| Procedure.md | § Step 2 | Define scope for rail unloading and marine loading services; system boundaries |
| Procedure.md | § Step 3 | Draft requirements: 3.1 Performance (REQ-05 through REQ-10), 3.2 Materials (REQ-11, REQ-12), 3.3 Installation (REQ-13, REQ-14), 3.4 Proving (REQ-04, REQ-17-19), 3.5 Instrumentation (REQ-03), 3.6 Electrical/Controls (REQ-15), 3.7 QA (REQ-20-22), 3.8 Documentation (REQ-23, REQ-24) |
| Procedure.md | § Step 4 | Add verification hooks per REQ-21; traceability matrix per REQ-24 |
| Procedure.md | § Step 5 | Discipline check for completeness, consistency, testability, objective alignment, standard compliance |
| Procedure.md | § Step 6 | IDC with PKG-14, PKG-17, PKG-19, PKG-20 per REQ-16 |
| Procedure.md | § Step 7 | Issue per document control procedures |
| DEL-12.01 | Drawings | Drawings implement installation requirements per § Specification Structure Section 5; tag numbers, straight-run dimensions per this specification |
| DEL-12.03 | Calculations | Calculations verify meter sizing, flow rates per § Specification Structure Section 4 and REQ-09 |
| DEL-12.04 | Data Sheets | Data sheets document equipment parameters per § Specification Structure Section 9 and REQ-23 |
| DEL-12.05 | Test Records | Test records demonstrate compliance per § Specification Structure Section 8 and REQ-20, REQ-21
