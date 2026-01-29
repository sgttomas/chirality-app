# Specification: DEL-19.01 Control System Design Drawing Set

## Scope

This specification defines the requirements for **Control System Design Drawing Set** within **PKG-19 Control Systems**.

**Deliverable purpose:** Defines the design arrangement and details for control system per ER requirements.

**Source:** `_CONTEXT.md`

### Included in Scope

- Control system architecture drawings showing DCS/PLC, HMI, historian, and network topology
- Network drawings showing industrial control networks, field device networks, and communication infrastructure
- Cabinet layout drawings showing physical arrangement of control equipment
- HMI arrangement drawings showing operator interface configuration

**Source:** `_CONTEXT.md` anticipated artifacts; Decomposition PKG-19 scope

### Excluded from Scope

- Detailed equipment specifications (see DEL-19.02 Control System Technical Specification)
- Equipment data sheets (see DEL-19.03 Control System Data Sheet Package)
- Control system software and programming (see DEL-19.04 Control System Software)
- Field instrumentation drawings (see PKG-20 Field Instrumentation deliverables)
- Electrical power distribution to control system (see PKG-17 Electrical Power Distribution)

**Source:** PKG-19 deliverable structure per Decomposition

## Requirements

### Functional Requirements

**FR-01: System Topology**
- Drawings shall define the overall control system topology including DCS/PLC controllers, HMI workstations, I/O racks, historian, and network infrastructure
- **Source:** Decomposition PKG-19 scope; **ASSUMPTION**: Typical control system drawing content
- **Rationale:** Guidance.md §Principles (Control System Role); **Verification:** Procedure.md Step 2

**FR-02: Control Architecture**
- Drawings shall show control system hierarchy and functional zones (process control, safety systems if applicable, monitoring systems)
- System shall support facility throughput of 1,000,000 MT/annum (OBJ-2)
- **Source:** OBJ-2 Throughput Capacity; **ASSUMPTION**: Control system sizing requirements TBD
- **Rationale:** Guidance.md §Principles (Design Philosophy); **Verification:** Procedure.md Step 2

**FR-03: Network Architecture**
- Drawings shall define industrial network architecture including control network, safety network (if applicable), and field device networks
- Network segmentation shall separate process control, safety, and business networks
- **Source:** **ASSUMPTION**: Typical industrial control system practice per ISA/IEC 62443 concepts; specific requirements TBD per Employer's Requirements **location TBD**
- **Rationale:** Guidance.md §Considerations (Network Design); **Verification:** Procedure.md Step 3

**FR-04: Operational Flexibility**
- Control system design shall support both tank storage operations and direct rail-to-ship transfer (OBJ-4)
- **Source:** OBJ-4 Operational Flexibility
- **Rationale:** Guidance.md §Principles (Operational Flexibility); **Verification:** Procedure.md Steps 2, 5

**FR-05: Custody Transfer Support**
- Control system shall integrate with custody transfer metering systems (PKG-12) to support accuracy requirements (OBJ-10)
- **Source:** OBJ-10 Custody Transfer Accuracy; interface with DEL-12.xx
- **Rationale:** Guidance.md §Principles (Accuracy); **Verification:** Procedure.md Step 6

**FR-06: Reliability and Redundancy**
- Control system architecture shall support safe, efficient, reliable, and continuous operation (OBJ-1)
- Redundancy strategy and fail-over architecture to be shown where required
- **Source:** OBJ-1 Safe & Reliable Operation; redundancy details **TBD** per Employer's Requirements **location TBD**
- **Rationale:** Guidance.md §Trade-offs TO-02; **Verification:** Procedure.md Step 2

### Performance Requirements

**PR-01: Drawing Quality**
- All drawings shall be legible, accurate, and suitable for construction and procurement purposes
- **Source:** Standard engineering drawing requirements; **ASSUMPTION**: Per project quality procedures

**PR-02: CAD Standards Compliance**
- All drawings shall comply with project CAD standards
- **TBD** — Project CAD standards document reference pending

**PR-03: Symbology and Notation**
- Instrumentation symbols and identification shall conform to ISA 5.1
- **Source:** Applicable standard ISA 5.1

**PR-04: Dimensional Accuracy**
- Cabinet layouts shall be dimensionally accurate and coordinated with physical space allocations
- **TBD** — Dimensional tolerance requirements

### Interface Requirements

**IR-01: Field Instrumentation (PKG-20)**
- Control system I/O requirements shall be coordinated with field instrumentation deliverables (DEL-20.xx)
- **Source:** Deliverable structure per Decomposition; dependency mode NOT_TRACKED (coordinated externally)
- **Verification:** Procedure.md Step 6 (Interdisciplinary Coordination)

**IR-02: Electrical Power (PKG-17)**
- Control system power requirements shall be coordinated with electrical power distribution deliverables (DEL-17.xx)
- **Source:** Deliverable structure per Decomposition
- **Verification:** Procedure.md Step 6 (Interdisciplinary Coordination)

**IR-03: Hazardous Area Classification (PKG-30)**
- Equipment locations and ratings shall be coordinated with area classification deliverables (DEL-30.xx)
- **Source:** Deliverable structure per Decomposition
- **Rationale:** Guidance.md §Considerations (Physical Arrangement); **Verification:** Procedure.md Step 6

**IR-04: Building Design (PKG-21/PKG-22)**
- Control room layout and equipment locations shall be coordinated with building structure and MEP deliverables
- **Source:** Deliverable structure per Decomposition
- **Rationale:** Guidance.md §Considerations (Physical Arrangement); **Verification:** Procedure.md Step 6

**IR-05: Process Systems (PKG-10, PKG-11, PKG-12, PKG-13, PKG-14, PKG-15)**
- Control system shall interface with railcar unloading (PKG-10), marine loading (PKG-11), metering (PKG-12), storage tanks (PKG-13), process piping (PKG-14), and pumps (PKG-15)
- **Source:** Facility functional scope per Decomposition
- **Rationale:** Guidance.md §Considerations (Interfaces and Coordination); **Verification:** Procedure.md Step 6

### Quality Requirements

**QR-01: Design Review**
- All drawings shall undergo self-check, interdisciplinary check, and independent check per project quality procedures
- **TBD** — Project quality procedure reference

**QR-02: Revision Control**
- All drawings shall be subject to revision control per project document control procedures
- **TBD** — Document control procedure reference

**QR-03: As-Built Updates**
- Drawings shall be updated to reflect as-built conditions during construction
- **TBD** — As-built update requirements per project procedures

## Standards

### Primary Codes and Standards

| Code/Standard | Title/Application |
|---------------|-------------------|
| ISA 5.1 | Instrumentation Symbols and Identification |
| ISA 84 / IEC 61511 | Safety Instrumented Systems (if SIS scope included) |
| CSA C22.1 | Canadian Electrical Code |
| API 554 | Process Instrumentation and Control |

**Source:** Typical I&C discipline standards; ISA 5.1 explicit for symbology; others **ASSUMPTION** pending Employer's Requirements

### Additional Standards (if applicable)

| Code/Standard | Title/Application |
|---------------|-------------------|
| IEC 61131 | Programmable controllers (programming architecture) |
| ISA/IEC 62443 | Cybersecurity for industrial automation and control systems |
| NFPA 70 | National Electrical Code (reference for electrical interfaces) |

**Source:** **ASSUMPTION**: Typical standards for industrial control systems; applicability TBD per Employer's Requirements **location TBD**

### Project Standards

- Employer's Requirements — **TBD** — **location TBD**
- Project CAD Standards — **TBD**
- Project Drawing Numbering System — **TBD**
- Project Document Control Procedures — **TBD**

## Verification

### Verification Methods

| Requirement Type | Verification Method |
|------------------|---------------------|
| Functional Requirements | Design review, functional verification against process requirements |
| Performance Requirements | CAD standards check, dimensional verification, legibility check |
| Interface Requirements | Interdisciplinary check (IDC) with affected packages |
| Quality Requirements | Quality assurance review per project QA/QC procedures |

**Source:** Standard engineering verification practice; **ASSUMPTION**: Per project quality procedures TBD

### Acceptance Criteria

**AC-01: Completeness**
- All required drawing types produced (architecture, networks, cabinet layouts, HMI arrangement)
- All sheets numbered, titled, and signed per project standards
- **TBD** — Specific completeness checklist per project procedures

**AC-02: Accuracy**
- No dimensional conflicts
- Equipment selections consistent with specifications (DEL-19.02) and data sheets (DEL-19.03)
- Interface points verified with adjacent disciplines
- **TBD** — Accuracy verification procedure

**AC-03: Compliance**
- ISA 5.1 symbology applied correctly
- CAD standards complied with
- Employer's Requirements satisfied
- **TBD** — Compliance checklist

### Review and Approval

- Self-check by originator
- Interdisciplinary check coordinated with affected packages
- Independent check by qualified checker
- Approval by discipline lead or authorized representative
- **TBD** — Sign-off authority matrix

## Documentation

### Required Drawing Types

1. **Control System Architecture**
   - System topology and hierarchy
   - Controller assignments (DCS/PLC)
   - HMI and historian configuration
   - Network infrastructure overview

2. **Network Drawings**
   - Industrial network topology
   - Network device locations
   - Communication protocols
   - Network segmentation and security zones

3. **Cabinet Layouts**
   - Cabinet elevations and sections
   - Equipment mounting arrangements
   - Cable entry/exit details
   - Cooling and power provisions

4. **HMI Arrangement**
   - HMI workstation locations
   - Hardware configuration
   - Remote HMI provisions
   - Connection diagrams

**Source:** `_CONTEXT.md` anticipated artifacts

**Note:** See `Datasheet.md` Construction section for additional detail on drawing set content. See `Procedure.md` Steps 2-5 for drawing production workflow.

### Drawing Format Requirements

- Sheet size: **TBD** — Per project CAD standards
- Title block: **TBD** — Per project template
- Revision block: **TBD** — Per project standards
- Scale: As appropriate (NTS for schematics, to-scale for physical layouts)
- Format: Native CAD + PDF **ASSUMPTION**

### Document Control

- Drawing numbers: Per project numbering system — **TBD**
- Revision control: Per project revision procedure — **TBD**
- Distribution: Per project distribution matrix — **TBD**
- Storage: Project document management system — **TBD**
- Retention: Per project retention schedule — **TBD**
