# Datasheet: DEL-12.04 Metering Data Sheet Package

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-12.04 |
| Name | Metering Data Sheet Package |
| Package | PKG-12 Product Transfer & Metering |
| Discipline | Process |
| Type | Data Sheet |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Data Sheet Numbers | To be issued per project numbering system (TBD; Source: ER Vol 2 Part 1, location TBD) |
| Equipment Tags | TBD — per project tag numbering system (Source: ER Vol 2 Part 1, location TBD); tags shall be consistent with P&IDs (PKG-14) and DEL-12.01 drawings |
| Service Description | Custody transfer metering (rail unloading and marine loading) plus associated instrumentation (temperature, pressure, density transmitters as applicable) |
| Revision | 00 (initial issue) |
| Classification | Process — Custody Transfer Metering Data Sheets |
| Data Sheet Count | Minimum 4 data sheets: (1) flow meter for rail unloading, (2) flow meter for marine loading, (3) temperature transmitter(s), (4) pressure transmitter(s); additional data sheets if density transmitters or multiple transmitters per service (ASSUMPTION) |
| Format | Tabular data sheets (spreadsheet, database, or structured document format per project standards; TBD) |

## Conditions

### Design Context

| Condition | Value / Description | Source |
|-----------|---------------------|--------|
| Service Application | Custody transfer metering for CSD canola oil at rail unloading and marine loading transfer points | Decomposition:350 |
| Product | CSD (Crude Super Degummed) canola oil | Decomposition:43 |
| Design Throughput | 1,000,000 MT per annum (permitted) | Decomposition:41 |
| Metering Points | Two primary custody transfer locations: (1) Rail unloading — measuring product received from rail tank cars; (2) Marine loading — measuring product delivered to liquid bulk carriers for export | Decomposition:350 |

### Data Sheet Design Basis (TBD)

All design basis parameters TBD from ER Vol 2 Part 2, DEL-12.02 specification, DEL-12.03 calculations, or vendor data; data sheets shall document sources for all parameters per Specification.md REQ-09:

| Parameter Category | Parameters | Source |
|-------------------|------------|--------|
| **Product Properties** | CSD canola oil density at reference temperature (typical ~0.91-0.92 g/cm³ at 15°C; ASSUMPTION), density vs. temperature curve, viscosity at operating temperature (typical ~30-70 cP at 20°C; ASSUMPTION), viscosity vs. temperature curve, vapor pressure, pour point, flash point | ER Vol 2 Part 2, location TBD; or product specifications |
| **Operating Conditions** | Operating temperature range (product temperature and ambient temperature), operating pressure range (at meter inlet and outlet), environmental conditions (outdoor installation at Fraser Surrey Terminal) | ER Vol 2 Part 2, location TBD |
| **Rail Unloading Service** | Design flow rate, normal flow rate, minimum flow rate, maximum flow rate (TBD from ER or DEL-12.03; facility has 32 unloading stations per Decomposition:44) | ER Vol 2 Part 2, location TBD; or DEL-12.03 calculations |
| **Marine Loading Service** | Design flow rate, normal flow rate, minimum flow rate, maximum flow rate (TBD from ER or DEL-12.03) | ER Vol 2 Part 2, location TBD; or DEL-12.03 calculations |
| **Performance Requirements** | Accuracy class (e.g., ±0.15%, ±0.25%; TBD from ER or DEL-12.02), repeatability (e.g., ±0.05%, ±0.1%; TBD), turndown ratio (e.g., 10:1, 20:1; TBD), uncertainty budget (from DEL-12.03) | ER Vol 2 Part 2, location TBD; DEL-12.02 specification; DEL-12.03 calculations |
| **Proving Requirements** | Proving method (in-line prover, portable prover, master meter; TBD from DEL-12.02), proving frequency (quarterly, semi-annually, annually; TBD), meter factor acceptance criteria (e.g., ±0.05% drift; TBD from DEL-12.03) | DEL-12.02 specification; DEL-12.03 calculations |
| **Hazardous Area** | Area classification (Division 1, Division 2, non-classified; TBD), electrical certifications required (CSA, UL, ATEX, IECEx; TBD) | ER Vol 2 Part 2, location TBD |

### Objective Alignment

| Objective | Relevance to This Deliverable |
|-----------|-------------------------------|
| OBJ-2 Throughput Capacity (1,000,000 MT/a) | Data sheets must specify equipment rated for design flow rates supporting 1,000,000 MT/a throughput; flow meter data sheets shall document flow ranges from DEL-12.03 calculations; transmitter data sheets shall document ranges adequate for operating conditions (Source: Decomposition:781; Specification.md REQ-04, REQ-05) |
| OBJ-10 Custody Transfer Accuracy | Data sheets must capture accuracy class, calibration requirements, proving requirements, and traceability fields for custody transfer compliance; accuracy class per DEL-12.02 specification; uncertainty budget per DEL-12.03; calibration traceability requirements per DEL-12.02 (Source: Decomposition:789; Specification.md REQ-04, REQ-05, REQ-10) |

## Construction

### Anticipated Data Sheet Content

| Data Sheet | Description | Source |
|------------|-------------|--------|
| Flow Meter Data Sheet — Rail Unloading | Custody transfer flow meter for rail unloading service; documents tag number, service description, process conditions (flow range, temperature, pressure, product), performance (accuracy class, repeatability, turndown, uncertainty), materials (wetted materials, housing, seals), electrical (power supply, signal outputs, communications), physical (size, connections, weight), calibration (calibration range, certificates required, proving requirements), vendor (manufacturer, model, certified data reference) | Decomposition:359; Specification.md REQ-01, REQ-02, REQ-03 |
| Flow Meter Data Sheet — Marine Loading | Custody transfer flow meter for marine loading service; same structure as rail unloading data sheet; service-specific conditions (higher flow rates for marine loading) | Decomposition:359; Specification.md REQ-01, REQ-02, REQ-03 |
| Temperature Transmitter Data Sheet(s) | Temperature measurement for custody transfer compensation; documents tag number(s), service description, measurement range (e.g., 0-100°C; TBD), accuracy (e.g., RTD Pt100 ±0.1°C; TBD from DEL-12.02), signal output (4-20 mA, HART, or other; TBD), calibration range and certificate requirements; separate data sheets for rail and marine services if transmitter specifications differ | Decomposition:359; Specification.md REQ-01, REQ-02, REQ-03 |
| Pressure Transmitter Data Sheet(s) | Pressure measurement for custody transfer compensation (if applicable; may not be required if canola oil compressibility is negligible); documents tag number(s), measurement range (e.g., 0-10 bar; TBD), accuracy (e.g., ±0.1% of span; TBD from DEL-12.02), signal output, calibration requirements; separate data sheets for rail and marine if specifications differ | Decomposition:359; Specification.md REQ-01, REQ-02, REQ-03 |

### Data Sheet Field Categories

Expected data sheet fields per Specification.md Documentation section (ASSUMPTION based on typical custody transfer metering data sheets; project standards may vary):

#### Flow Meter Data Sheet Fields

| Field Category | Fields | Source / Notes |
|----------------|--------|----------------|
| **Identification** | Tag number (per project tag numbering system; coordinate with P&IDs), service description (e.g., "Rail Unloading Custody Transfer Metering"), P&ID reference (drawing number and sheet), location (e.g., "Rail Unloading Metering Skid"), equipment description (e.g., "Custody Transfer Coriolis Mass Flowmeter") | Tag number from project system; P&ID from PKG-14 |
| **Process Conditions** | Service (rail unloading or marine loading), product (CSD canola oil), normal flow rate (m³/h or kg/h; TBD from DEL-12.03), design flow rate (maximum for sizing; TBD), minimum flow rate (defines turndown; TBD), maximum flow rate (peak flow; TBD), operating temperature (normal and range; TBD from ER), operating pressure (normal and range; TBD from ER), product density (at reference temperature and vs. temperature; TBD), product viscosity (at operating temperature; TBD) | Flow rates from DEL-12.03; operating conditions from ER Vol 2 Part 2 or design basis |
| **Performance** | Meter type (Coriolis mass, ultrasonic, turbine, positive displacement; TBD from DEL-12.02), accuracy class (e.g., ±0.15%; TBD from DEL-12.02), repeatability (e.g., ±0.05%; TBD from DEL-12.02), turndown ratio (e.g., 20:1; TBD from DEL-12.03), expanded uncertainty (from DEL-12.03 uncertainty budget), flow range (minimum to maximum with accuracy maintained), pressure drop (at maximum flow; from DEL-12.03), response time (if relevant for control) | Performance from DEL-12.02 specification; calculated values from DEL-12.03 |
| **Materials** | Wetted materials (body material: SS316L, carbon steel, or other; internals material; seals and gaskets: Viton, PTFE, or other; TBD from DEL-12.02), housing material (cast iron, stainless steel, aluminum, or other), pressure rating (ANSI class, PN rating, or other; TBD), temperature rating (minimum and maximum; TBD) | Materials from DEL-12.02 specification; vendor data |
| **Electrical / Controls** | Power supply (voltage, frequency, power consumption; e.g., 120VAC 60Hz, 24VDC; TBD), signal outputs (flow: 4-20 mA, pulse, or digital; density if Coriolis: 4-20 mA or digital; temperature if integral: 4-20 mA or digital; totalizer: pulse output; TBD), communication protocol (Modbus RTU/TCP, HART, Profibus, Foundation Fieldbus, or other; TBD from PKG-19), area classification (Division 1, Division 2, non-classified; TBD from ER), electrical certification (CSA, UL, ATEX, IECEx; TBD), cable entries (number, size, type) | Electrical from DEL-12.02 specification; coordinate with PKG-17, PKG-19 |
| **Physical** | Meter size (line size; from DEL-12.03 sizing calculation), process connections (flange size, rating, facing; e.g., 6" 150# RF; TBD), meter length (face-to-face dimension; from vendor data), weight (empty and filled; from vendor data), mounting orientation (horizontal, vertical, inclined; per manufacturer and DEL-12.02), straight-run requirements (upstream and downstream; from DEL-12.02 or manufacturer; e.g., "10D upstream, 5D downstream") | Sizing from DEL-12.03; physical data from vendor; installation requirements from DEL-12.02 |
| **Calibration / Proving** | Calibration range (flow range over which meter is calibrated; typically same as specified flow range), calibration traceability (traceable to Measurement Canada, NIST, or equivalent national metrology institute), calibration interval (per Measurement Canada or DEL-12.02; e.g., "Prove quarterly or per Measurement Canada regulations"), proving method (in-line prover, portable prover, master meter; from DEL-12.02), meter factor range (acceptable range; e.g., 0.995-1.005; from DEL-12.03), meter factor drift limit (e.g., ±0.05%; from DEL-12.03), proving acceptance criteria (from DEL-12.03) | Calibration requirements from DEL-12.02; proving from DEL-12.03 |
| **Vendor** | Manufacturer (vendor name), model number (vendor model designation), vendor data sheet reference (manufacturer document number), certified data (indicate which fields are vendor-certified), serial number (for installed equipment; TBD until procurement), vendor certification (certificates provided: calibration certificate, material certificates, Measurement Canada approval if applicable) | Vendor data; certification requirements from DEL-12.02 |
| **Verification Basis** | For each critical field, indicate verification basis: "ER Vol 2 Part 2 Clause X.X.X", "DEL-12.02 Specification Section Y", "DEL-12.03 Calculation", "Vendor Certified Data", "ASSUMPTION — rationale", "TBD — source needed" | Traceability per Specification.md REQ-09 |

#### Temperature Transmitter Data Sheet Fields

| Field Category | Fields | Source / Notes |
|----------------|--------|----------------|
| **Identification** | Tag number, service description (e.g., "Rail Unloading Metering Temperature Compensation"), P&ID reference, location | Project tag system; P&IDs from PKG-14 |
| **Process Conditions** | Service, product (CSD canola oil), normal temperature, design temperature range, installation (immersion, surface-mounted, thermowell) | Operating conditions from ER Vol 2 Part 2 |
| **Performance** | Sensor type (RTD Pt100, RTD Pt1000, thermocouple Type J/K/T, or other; TBD from DEL-12.02), accuracy (e.g., Class A RTD ±(0.15 + 0.002×T)°C, or ±0.1°C; TBD), measurement range (e.g., 0-100°C, -20-80°C; TBD), response time (if critical for control), drift (long-term stability) | Sensor type and accuracy from DEL-12.02; range from operating conditions |
| **Electrical** | Power supply (if powered transmitter; 24VDC, 120VAC, or loop-powered from control system; TBD), signal output (4-20 mA, 4-20 mA with HART, digital; TBD from PKG-19), communication protocol if applicable, area classification, electrical certification | Electrical requirements from PKG-19, PKG-20; area classification from ER |
| **Physical** | Sensor length (immersion length if in thermowell), process connection (threaded, flanged, compression fitting; size and type), housing (field-mount, DIN rail, integral with meter), cable entries | Physical requirements coordinate with installation; vendor data |
| **Calibration** | Calibration range, calibration traceability (traceable to national standards), calibration interval (typical 12-24 months or per project QA plan) | Calibration requirements from DEL-12.02 or project QA plan |
| **Vendor** | Manufacturer, model, vendor data sheet reference, serial number (TBD until procurement) | Vendor data |

#### Pressure Transmitter Data Sheet Fields (if applicable)

| Field Category | Fields | Source / Notes |
|----------------|--------|----------------|
| **Identification** | Tag number, service description, P&ID reference, location | Project tag system; P&IDs from PKG-14 |
| **Process Conditions** | Service, product, normal pressure, design pressure range, pressure type (gauge, absolute, differential if used for differential pressure across meter) | Operating conditions from ER Vol 2 Part 2 |
| **Performance** | Measurement range (e.g., 0-10 bar, 0-150 psi; TBD), accuracy (e.g., ±0.1% of span, ±0.25% of span; TBD from DEL-12.02), turndown (rangeability of transmitter), overpressure rating, burst pressure | Range from operating conditions; accuracy from DEL-12.02 |
| **Electrical** | Power supply, signal output (4-20 mA, 4-20 mA with HART, digital), communication protocol, area classification, electrical certification | Electrical from PKG-19, PKG-20; area classification from ER |
| **Physical** | Process connection (threaded, flanged; size and type), housing, mounting (field-mount, panel-mount), cable entries, environmental rating (IP rating, NEMA rating) | Physical requirements from installation; vendor data |
| **Calibration** | Calibration range, calibration points (typically 0%, 25%, 50%, 75%, 100% of range), calibration traceability, calibration interval | Calibration requirements from DEL-12.02 or project QA plan |
| **Vendor** | Manufacturer, model, vendor data sheet reference, serial number (TBD until procurement) | Vendor data |

### Objective Alignment

| Objective | Relevance to This Deliverable |
|-----------|-------------------------------|
| OBJ-2 Throughput Capacity (1,000,000 MT/a) | Data sheets must specify equipment rated for design flow rates supporting 1,000,000 MT/a throughput; flow meter data sheets shall document flow ranges from DEL-12.03 calculations (rail unloading and marine loading design flow rates); transmitter data sheets shall document ranges adequate for operating conditions without constraining operations (Source: Decomposition:781; Specification.md REQ-04, REQ-05) |
| OBJ-10 Custody Transfer Accuracy | Data sheets must capture accuracy class, calibration requirements, proving requirements, and traceability fields for custody transfer compliance; flow meter data sheets document accuracy class per DEL-12.02, uncertainty budget per DEL-12.03, proving requirements; transmitter data sheets document measurement accuracy for compensation; calibration traceability documented for all instruments (Source: Decomposition:789; Specification.md REQ-04, REQ-05, REQ-10) |

## References

### Primary Sources

| Reference | Content | Location |
|-----------|---------|----------|
| Decomposition | PKG-12 scope definition, DEL-12.04 definition, objective mappings, facility parameters (throughput, unloading stations) | Lines 41, 44, 350, 359, 781, 789 |
| ER Vol 2 Part 1 | General requirements, document control, tag numbering system, data sheet standards | TBD |
| ER Vol 2 Part 2 | Process mechanical requirements, metering requirements, operating conditions, fluid properties (CSD canola oil), accuracy requirements, hazardous area classification | TBD |

### Related Deliverables (PKG-12)

| Deliverable | Relationship |
|-------------|--------------|
| DEL-12.01 Metering Design Drawing Set | Drawings show equipment arrangement and installation details; tag numbers on drawings shall match data sheet tag numbers (per Specification.md REQ-04); equipment shown in drawings shall match data sheet specifications (sizes, connections, orientations) |
| DEL-12.02 Metering Technical Specification | Specification provides performance requirements, materials, and workmanship standards; data sheets demonstrate equipment compliance with specification requirements (per Specification.md REQ-04); data sheet parameters shall align with specification requirements |
| DEL-12.03 Metering Design Calculations | Calculations provide sizing basis (flow ranges, meter sizes, accuracy/uncertainty, proving criteria); data sheets capture parameters validated by calculations (per Specification.md REQ-05); flow ranges, meter sizes, uncertainty values from calculations shall be documented in data sheets |
| DEL-12.05 Metering Installation & Test Records | Test records verify data sheet parameters; calibration certificates in DEL-12.05 verify calibration traceability documented in data sheets; FAT and SAT records verify performance per data sheet specifications (per Specification.md REQ-10) |

### Interface Packages (Coordinated Externally)

Dependencies coordinated externally per dependency mode NOT_TRACKED (see `_DEPENDENCIES.md`):

- PKG-14 Process Piping — P&IDs provide tag numbers and service references; piping provides process connection requirements
- PKG-17 Electrical Power Distribution — power supply requirements; area classification
- PKG-19 Control Systems — signal integration (signal types, communication protocols), HMI requirements, data logging
- PKG-20 Field Instrumentation — transmitter specifications (may be specified in PKG-20 or in this deliverable for metering-specific transmitters)

## Cross-Document Traceability

| Document | Section | Link Points |
|----------|---------|-------------|
| Specification.md | § Scope | Defines inclusions (flow meter data sheets ×2, temperature/pressure transmitter data sheets) and exclusions (general field instrumentation, control system I/O, valves, pumps) |
| Specification.md | § Requirements | REQ-01 through REQ-17: functional (REQ-01-04 artifact presence and identification), performance (REQ-05-09 specification/calculation consistency), data quality (REQ-10-12 verification basis), interface (REQ-13-14 electrical/controls coordination), quality (REQ-15-17 independent check) |
| Specification.md | § Standards | Governing references (ER Vol 2 Part 1/2); custody transfer standards (API MPMS, OIML R117, Measurement Canada) defining data sheet field requirements |
| Specification.md | § Verification | Verification methods (checklist, document review, cross-reference, vendor data, IDC, independent check, OBJ alignment) and acceptance criteria |
| Specification.md | § Documentation | Data sheet field requirements matching Construction section field categories |
| Guidance.md | § Purpose | Data sheets as structured source of truth for equipment parameters; downstream use (engineering, procurement, vendors, installation, testing, operations) |
| Guidance.md | § Principles | Development rationale (single source of truth, traceability REQ-10, consistency REQ-04/05/06, no invention REQ-12); custody transfer principles (accuracy capture REQ-07, calibration traceability REQ-11, proving fields REQ-11) |
| Guidance.md | § Considerations | Content considerations (service differentiation REQ-02, vendor data timing, interface fields REQ-13, calibration fields REQ-11); flow meter field guidance; transmitter field guidance; service-specific (rail batch vs. marine continuous); data sheet timing (inquiry/order/delivery stages) |
| Guidance.md | § Trade-offs | Standardization vs. optimization; accuracy vs. cost; vendor lock-in vs. flexibility; detail level based on available information |
| Procedure.md | § Step 1 | Identify required data sheets per REQ-01; assign tag numbers per REQ-02/04; create data sheet index |
| Procedure.md | § Step 2 | Establish data sheet template with field categories per Construction section |
| Procedure.md | § Step 3 | Populate design basis from ER, DEL-12.02, DEL-12.03 per REQ-05/06; document verification basis per REQ-10 |
| Procedure.md | § Step 4 | Obtain and incorporate vendor data per REQ-09; mark vendor-certified fields per REQ-10 |
| Procedure.md | § Step 5 | Cross-check consistency with DEL-12.01/02/03 per REQ-04/05/06; verify interfaces per REQ-13 |
| Procedure.md | § Step 6 | Independent check and issue per REQ-15/16/17 |
| DEL-12.01 | Drawings | Tag numbers, meter sizes, orientations, straight-run dimensions from data sheets per Conditions section |
| DEL-12.02 | Specification | Performance requirements (accuracy, repeatability, materials, proving) as data sheet inputs per Construction section Performance/Materials/Calibration fields |
| DEL-12.03 | Calculations | Sizing parameters (flow ranges, meter sizes, pressure drop, uncertainty) as data sheet inputs per Construction section Performance/Physical fields |
| DEL-12.05 | Test Records | Data sheet calibration and proving fields enable DEL-12.05 compliance verification per Construction section Calibration/Proving fields |
| PKG-14 | P&IDs | Tag numbers, P&ID references, line sizes, process connections per Construction section Identification/Physical fields |
| PKG-17 | Electrical | Power supply, area classification per Construction section Electrical/Controls fields |
| PKG-19 | Controls | Signal outputs, communication protocols per Construction section Electrical/Controls fields |
| PKG-20 | Instrumentation | Transmitter specifications coordination per Construction section transmitter fields
