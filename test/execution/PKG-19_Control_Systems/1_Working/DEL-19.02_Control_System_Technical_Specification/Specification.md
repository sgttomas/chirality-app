# Specification: DEL-19.02 Control System Technical Specification

## Scope

This specification defines the requirements for **Control System Technical Specification** within **PKG-19 Control Systems**.

**Deliverable purpose:** Defines performance, materials, and workmanship requirements for control system per ER requirements.

**Source:** `_CONTEXT.md`

### Included in Scope

- DCS/PLC technical specification (performance, functional, and hardware requirements)
- HMI technical specification (operator interface requirements and hardware)
- Historian technical specification (data management and retention requirements)
- Control system performance criteria
- Materials and workmanship standards
- Interface requirements with other systems
- Testing and commissioning requirements
- Documentation and training requirements

**Source:** `_CONTEXT.md` anticipated artifacts; Decomposition PKG-19 scope

### Excluded from Scope

- Control system design drawings (see DEL-19.01 Control System Design Drawing Set)
- Equipment data sheets and vendor submittals (see DEL-19.03 Control System Data Sheet Package)
- Control system software programming and configuration (see DEL-19.04 Control System Software)
- Field instrumentation specifications (see PKG-20 Field Instrumentation deliverables)
- Electrical power distribution specifications (see PKG-17 Electrical Power Distribution)

**Source:** PKG-19 deliverable structure per Decomposition

## Requirements

### Functional Requirements

**FR-01: System Capacity**
- Control system shall support facility throughput capacity of 1,000,000 MT/annum (OBJ-2)
- System shall monitor and control 32 railcar unloading positions
- System shall monitor and control 3 × 15,000 MT storage tanks (45,000 MT total per OBJ-3)
- System shall control marine loading operations
- **Source:** OBJ-2, OBJ-3; Decomposition Section 1 (Project Overview)
- **Rationale:** Guidance.md §Principles; **Verification:** Procedure.md Steps 1–2, TC-01, TC-02

**FR-02: Operational Flexibility**
- Control system shall support both tank storage operations and direct rail-to-ship transfer modes (OBJ-4)
- Mode changes shall not require system reconfiguration or downtime
- **Source:** OBJ-4 Operational Flexibility
- **Rationale:** Guidance.md §Principles (Flexibility); **Verification:** Procedure.md Step 2, TC-02

**FR-03: Reliability and Availability**
- Control system shall support safe, efficient, reliable, and continuous operation (OBJ-1)
- System availability target: **TBD** — Employer's Requirements **location TBD** — **ASSUMPTION**: ≥99.5% typical for process control systems
- Redundancy shall be provided for critical control functions
- Fail-over time for redundant components: **TBD** — **ASSUMPTION**: ≤1 second bumpless transfer
- **Source:** OBJ-1 Safe & Reliable Operation
- **Rationale:** Guidance.md §Trade-offs TO-02; **Verification:** Procedure.md Step 2, TC-01, TC-02

**FR-04: Custody Transfer Integration**
- Control system shall interface with custody transfer metering systems (PKG-12) to support accuracy requirements (OBJ-10)
- System shall collect, record, and report custody transfer data
- Data integrity and audit trail requirements per **TBD** — Employer's Requirements **location TBD**
- **Source:** OBJ-10 Custody Transfer Accuracy
- **Rationale:** Guidance.md §Principles (Accuracy); **Verification:** Procedure.md Step 3, TC-03

**FR-05: Safety Integration**
- Control system shall interface with safety systems (PKG-23: Fire Protection)
- If Safety Instrumented System (SIS) is required, separation between BPCS (Basic Process Control System) and SIS per ISA 84 / IEC 61511
- **TBD** — Confirm SIS scope and Safety Integrity Level (SIL) requirements per Employer's Requirements **location TBD**
- **Source:** OBJ-1; ISA 84 / IEC 61511 standard
- **Rationale:** Guidance.md §Applicable Standards Context; **Verification:** Procedure.md Step 3, TC-03

**FR-06: Data Collection and Historian**
- Historian shall collect process data from DCS/PLC at defined sampling rates
- Data retention: Short-term (high-resolution) **TBD** duration; Long-term (compressed) **TBD** duration
- Historian shall support reporting, trending, and analytics functions
- **Source:** Typical control system historian requirements; specific requirements TBD
- **Rationale:** Guidance.md §Considerations (Data Management); **Verification:** Procedure.md Step 2, TC-02

**FR-07: Alarm Management**
- HMI shall provide alarm management per ISA 18.2 principles (if applicable)
- Alarm priorities, acknowledgment, and escalation procedures **TBD**
- Alarm load target: **TBD** — **ASSUMPTION**: ≤6 alarms per operator per 10 minutes (steady-state)
- **Source:** **ASSUMPTION**: ISA 18.2 alarm management best practices; specific requirements TBD
- **Rationale:** Guidance.md §Applicable Standards Context (ISA 18.2); **Verification:** Procedure.md Step 2, TC-02

**FR-08: Cybersecurity**
- Control system shall implement cybersecurity per **TBD** — Employer's Requirements **location TBD**
- **ASSUMPTION**: Network segmentation per ISA/IEC 62443 (Level 3 business, Level 2 supervisory, Level 1 control, Level 0 field)
- Firewall, access control, and authentication requirements **TBD**
- **Source:** **ASSUMPTION**: ISA/IEC 62443 concepts; specific requirements TBD
- **Rationale:** Guidance.md §Considerations (Cybersecurity Posture); **Verification:** Procedure.md Step 2, TC-01

### Performance Requirements

**PR-01: DCS/PLC Performance**
- Controller scan time: **TBD** — **ASSUMPTION**: ≤100 ms typical for process control loops
- I/O response time: **TBD** — **ASSUMPTION**: ≤1 second end-to-end
- Analog input accuracy: **TBD** — **ASSUMPTION**: 0.1% of span typical
- Communication latency (controller to HMI): **TBD** — **ASSUMPTION**: ≤500 ms
- **Source:** **ASSUMPTION**: Typical DCS/PLC performance criteria; specific requirements TBD per Employer's Requirements

**PR-02: HMI Performance**
- Screen update rate: **TBD** — **ASSUMPTION**: ≤2 seconds typical
- Alarm response time (field event to HMI alarm): **TBD** — **ASSUMPTION**: ≤3 seconds
- Concurrent operators: **TBD** — based on operational manning philosophy
- **Source:** **ASSUMPTION**: Typical HMI performance criteria; specific requirements TBD

**PR-03: Historian Performance**
- Data collection rate: **TBD** — based on number of tags and sampling rates
- Query response time: **TBD** — **ASSUMPTION**: ≤10 seconds for typical historical trend query
- Storage capacity: **TBD** — based on tag count, sampling rates, and retention period
- **Source:** **ASSUMPTION**: Typical historian performance criteria; specific requirements TBD

**PR-04: Network Performance**
- Industrial network bandwidth: **TBD** — based on I/O count and data rates
- Network availability: **TBD** — **ASSUMPTION**: ≥99.9% for control network
- **Source:** **ASSUMPTION**: Typical industrial network performance; specific requirements TBD

### Interface Requirements

**IR-01: Field Instrumentation (PKG-20)**
- Specify I/O types: Analog input (AI), Analog output (AO), Digital input (DI), Digital output (DO)
- Specify signal types: 4-20mA, 0-10V, discrete 24VDC, etc.
- Specify communication protocols: HART, Foundation Fieldbus, PROFIBUS, Modbus, EtherNet/IP, etc.
- I/O count and spare capacity: **TBD** — based on field instrumentation design (DEL-20.xx)
- **Source:** Deliverable structure per Decomposition; dependency mode NOT_TRACKED (coordinated externally)

**IR-02: Electrical Power (PKG-17)**
- Specify power requirements for control system equipment (DCS/PLC, HMI, network devices)
- Voltage: **TBD** — **ASSUMPTION**: 120VAC and/or 24VDC typical
- UPS backup: **TBD** — duration and capacity based on graceful shutdown requirements
- Grounding per CSA C22.1
- **Source:** CSA C22.1; coordination with DEL-17.xx

**IR-03: Safety Systems (PKG-23)**
- Specify interface to fire protection system (alarms, interlocks)
- Specify emergency shutdown (ESD) interfaces if applicable
- If SIS, specify BPCS/SIS communication and separation per IEC 61511
- **Source:** OBJ-1; IEC 61511 if SIS applicable

**IR-04: Process Systems (PKG-10 through PKG-16)**
- Railcar unloading control strategy (PKG-10)
- Marine loading control strategy (PKG-11)
- Custody transfer metering interface (PKG-12)
- Storage tank level/temperature monitoring and control (PKG-13)
- Process piping control (valves, flow control) (PKG-14)
- Pump control (start/stop, speed control, interlocks) (PKG-15)
- Valve control and position feedback (PKG-16)
- **Source:** Facility functional scope per Decomposition

**IR-05: Building Systems (PKG-21/PKG-22)**
- HVAC requirements for control room (temperature, humidity control)
- Control room space and layout coordination
- Cable routing and tray coordination
- **Source:** Building design coordination

### Materials and Workmanship Requirements

**MR-01: Equipment Quality**
- All control system equipment shall be new, of current manufacture, and suitable for the intended service
- Equipment shall be from established manufacturers with proven track record in industrial control systems
- **Source:** Standard specification language; **ASSUMPTION**: Typical project quality requirements

**MR-02: Hardware Standards**
- DCS/PLC controllers: Industrial-grade, modular, scalable architecture
- HMI workstations: Industrial or commercial-grade per installation environment
- Network equipment: Industrial Ethernet switches, managed, with redundancy protocols (e.g., RSTP, MRP)
- **TBD** — Specific manufacturer approvals or pre-qualified equipment list per Employer's Requirements **location TBD**
- **Source:** **ASSUMPTION**: Typical industrial control system hardware standards

**MR-03: Software Standards**
- Programming languages per IEC 61131-3 (ladder logic, function block diagram, structured text, etc.)
- Operating systems: Current, supported versions with long-term support (LTS) commitment
- Licensing: Perpetual licenses or long-term subscription; unlimited runtime licenses
- **TBD** — Software version control and configuration management requirements
- **Source:** IEC 61131-3; **ASSUMPTION**: Typical software requirements

**MR-04: Environmental Ratings**
- Control room equipment: Indoor, climate-controlled environment
- Field equipment: NEMA 4X or IP66 minimum (outdoor, marine environment)
- Hazardous area equipment: Ratings per PKG-30 Area Classification — **TBD**
- Temperature rating: **TBD** — based on installation location
- **Source:** **ASSUMPTION**: Typical environmental ratings; specific requirements TBD

**MR-05: Cybersecurity Requirements**
- Equipment shall support security features: user authentication, access control, audit logging
- Network equipment shall support firewall, VLAN, and intrusion detection capabilities (if required)
- Software shall support secure remote access (VPN, encrypted communication)
- **TBD** — Specific cybersecurity compliance requirements per Employer's Requirements **location TBD**
- **Source:** **ASSUMPTION**: ISA/IEC 62443 concepts; specific requirements TBD

### Testing and Commissioning Requirements

**TC-01: Factory Acceptance Test (FAT)**
- FAT shall be performed at vendor's facility prior to shipment
- FAT scope: Hardware inspection, software functional testing, simulated I/O testing, communication testing
- FAT documentation: Test procedures, test results, punch list
- **TBD** — FAT attendance requirements (Owner, Contractor, Third-Party)
- **Source:** Standard control system FAT requirements; specific requirements TBD

**TC-02: Site Acceptance Test (SAT)**
- SAT shall be performed after installation and integration with field devices
- SAT scope: I/O checkout, control loop tuning, alarm testing, HMI functionality, historian data collection
- SAT documentation: Test procedures, test results, as-built documentation
- **TBD** — SAT acceptance criteria and sign-off requirements
- **Source:** Standard control system SAT requirements; specific requirements TBD

**TC-03: Integration Testing**
- Integration testing with process systems (unloading, storage, loading, metering)
- Integration testing with safety systems (fire protection, ESD)
- Performance testing under simulated load
- **TBD** — Integration test scope and acceptance criteria
- **Source:** **ASSUMPTION**: Typical system integration testing; specific requirements TBD

### Documentation and Training Requirements

**DR-01: Vendor Documentation**
- Hardware manuals (installation, operation, maintenance)
- Software manuals (programming, configuration, troubleshooting)
- Wiring diagrams and loop drawings
- Software backups and version control records
- Spare parts list and recommended inventory
- **Source:** Standard vendor documentation requirements

**DR-02: Training Requirements**
- Operator training (HMI operation, alarm response, normal/abnormal procedures)
- Maintenance training (hardware troubleshooting, software backup/restore, spare parts replacement)
- Engineering training (programming, configuration, advanced troubleshooting)
- **TBD** — Training duration, location, and number of attendees
- **Source:** Standard training requirements; specific requirements TBD

### Quality Requirements

**QR-01: Quality Management**
- All work shall comply with project Quality Management Plan
- Vendor shall have ISO 9001 certification (or equivalent)
- **TBD** — Specific quality procedures and hold points
- **Source:** Standard project quality requirements

**QR-02: Warranty and Support**
- Equipment warranty: **TBD** — **ASSUMPTION**: Minimum 12 months from final acceptance
- Software support: **TBD** — **ASSUMPTION**: Minimum 5 years from final acceptance
- Spare parts availability: **TBD** — **ASSUMPTION**: Minimum 10 years
- **Source:** **ASSUMPTION**: Typical warranty and support requirements; specific requirements TBD per Employer's Requirements

## Standards

### Primary Codes and Standards

| Code/Standard | Title/Application |
|---------------|-------------------|
| ISA 5.1 | Instrumentation Symbols and Identification |
| ISA 84 / IEC 61511 | Safety Instrumented Systems (if SIS scope included) |
| IEC 61131-3 | Programmable Controllers – Programming Languages |
| CSA C22.1 | Canadian Electrical Code |
| API 554 | Process Instrumentation and Control |

**Source:** Typical I&C discipline standards; ISA 5.1, IEC 61131-3, CSA C22.1 explicit; others **ASSUMPTION** pending Employer's Requirements

### Additional Standards (if applicable)

| Code/Standard | Title/Application |
|---------------|-------------------|
| ISA 18.2 | Management of Alarm Systems for the Process Industries |
| ISA/IEC 62443 | Security for Industrial Automation and Control Systems |
| IEEE 802.3 | Ethernet Standards |
| OPC Foundation Standards | OPC UA / OPC DA (interoperability) |

**Source:** **ASSUMPTION**: Typical standards for industrial control systems; applicability TBD per Employer's Requirements **location TBD**

### Project Standards

- Employer's Requirements — **TBD** — **location TBD**
- Project Quality Management Plan — **TBD**
- Project Document Control Procedures — **TBD**
- Project Cybersecurity Policy — **TBD**

## Verification

### Verification Methods

| Requirement Type | Verification Method |
|------------------|---------------------|
| Functional Requirements | Design review, FAT functional testing, SAT functional testing |
| Performance Requirements | Performance testing (scan time, response time, network latency), SAT performance verification |
| Interface Requirements | Interdisciplinary check (IDC), integration testing |
| Materials and Workmanship | Vendor qualifications review, equipment inspection, FAT |
| Testing and Commissioning | Witness FAT and SAT, review test documentation |
| Documentation and Training | Documentation review, training completion records |
| Quality Requirements | Vendor ISO 9001 certification, quality audit |

**Source:** Standard engineering verification practice; **ASSUMPTION**: Per project quality procedures TBD

### Acceptance Criteria

**AC-01: Specification Completeness**
- All sections complete (DCS/PLC, HMI, historian specifications)
- All requirements clearly stated and verifiable
- All interfaces identified and coordinated
- **TBD** — Specific completeness checklist per project procedures

**AC-02: Technical Adequacy**
- Requirements consistent with Employer's Requirements
- Requirements consistent with applicable codes and standards
- Requirements achievable with current technology
- **TBD** — Technical review and approval procedures

**AC-03: Vendor Compliance**
- Vendor proposals demonstrate compliance with specification requirements
- Deviations clearly identified and justified
- **TBD** — Compliance matrix and evaluation criteria

### Review and Approval

- Technical review by I&C discipline lead
- Interdisciplinary check with affected packages (PKG-20, PKG-17, PKG-23, process packages)
- Employer review and comment
- Approval by I&C discipline lead or authorized representative
- **TBD** — Sign-off authority matrix

## Documentation

### Required Specification Documents

1. **DCS/PLC Technical Specification**
   - General requirements
   - System architecture
   - Hardware requirements
   - Software requirements
   - Performance requirements
   - Interface requirements
   - Testing requirements
   - Documentation requirements

2. **HMI Technical Specification**
   - General requirements
   - Platform requirements
   - Hardware requirements
   - Operator interface requirements
   - Performance requirements
   - Interface requirements
   - Testing requirements
   - Training requirements

3. **Historian Technical Specification**
   - General requirements
   - Platform requirements
   - Hardware requirements
   - Data collection requirements
   - Data retention requirements
   - Reporting requirements
   - Interface requirements
   - Testing requirements

**Source:** `_CONTEXT.md` anticipated artifacts

### Document Format Requirements

- Format: **TBD** — **ASSUMPTION**: MS Word or equivalent + PDF
- Template: **TBD** — Per project specification template
- Numbering: Per project document numbering system — **TBD**
- Revision control: Per project revision procedure — **TBD**

### Document Control

- Document numbers: Per project numbering system — **TBD**
- Revision control: Per project revision procedure — **TBD**
- Distribution: Per project distribution matrix — **TBD**
- Storage: Project document management system — **TBD**
- Retention: Per project retention schedule — **TBD**
