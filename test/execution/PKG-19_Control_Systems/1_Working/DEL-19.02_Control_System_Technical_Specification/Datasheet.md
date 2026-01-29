# Datasheet: DEL-19.02 Control System Technical Specification

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-19.02 |
| Name | Control System Technical Specification |
| Package | PKG-19 Control Systems |
| Discipline | I&C |
| Type | Specification |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md` and Decomposition Section PKG-19

## Attributes

### Specification Characteristics

| Attribute | Value |
|-----------|-------|
| Document Number | **TBD** — Per project document numbering system |
| Specification Type | Technical Specification (equipment performance, materials, workmanship) |
| Revision | **TBD** — Per project revision procedure |
| Format | **TBD** — **ASSUMPTION**: Text document (MS Word or equivalent) + PDF |
| Classification | **TBD** — Per project document classification system |

**Source:** Standard specification document attributes; project-specific values TBD

### Specification Scope Components

| Component | Description | Specification § | Guidance § |
|-----------|-------------|-----------------|------------|
| DCS/PLC Specification | Performance, functional, and technical requirements for distributed control system or programmable logic controller | FR-01 to FR-08, PR-01, MR-02, MR-03 | Trade-offs TO-01, TO-02 |
| HMI Specification | Performance, functional, and technical requirements for human-machine interface workstations and software | FR-02, FR-07, PR-02 | Considerations §4, §5 |
| Historian Specification | Performance, functional, and technical requirements for data historian system | FR-06, PR-03 | Considerations §6 |

**Source:** `_CONTEXT.md` anticipated artifacts; Decomposition PKG-19 scope

### System Context

| Parameter | Value | Specification § | Related Objective |
|-----------|-------|-----------------|-------------------|
| Facility Throughput | 1,000,000 MT/annum canola oil | FR-01 | OBJ-2 |
| Storage Capacity | 45,000 MT (3 × 15,000 MT tanks) | FR-01 | OBJ-3 |
| Unloading Capacity | 32 railcar positions | FR-01, IR-04 | OBJ-2 |
| Loading Operations | Marine loading via loading arms | FR-01, IR-04 | OBJ-2, OBJ-4 |
| Metering | Custody transfer metering (accuracy per OBJ-10) | FR-04, IR-04 | OBJ-10 |
| Operational Modes | Tank storage operations AND direct rail-to-ship transfer (OBJ-4 flexibility) | FR-02 | OBJ-4 |

**Source:** Decomposition Section 1 (Project Overview); OBJ-2, OBJ-3, OBJ-4, OBJ-10

## Conditions

### Operational Requirements

| Requirement | Specification Basis | Specification § | Guidance § |
|-------------|---------------------|-----------------|------------|
| Reliability | Safe, efficient, reliable, and continuous operation (OBJ-1) | FR-03, FR-05 | Principles, Trade-offs TO-02 |
| Operational Flexibility | Support both tank storage and direct rail-to-ship transfer modes without reconfiguration (OBJ-4) | FR-02 | Principles, Trade-offs TO-04 |
| Custody Transfer Integration | Interface with custody transfer metering systems per OBJ-10 | FR-04 | Principles |
| Throughput Support | Control system capacity to support 1,000,000 MT/annum facility throughput (OBJ-2) | FR-01 | Principles |

**Source:** Decomposition Section 2 (Project Objectives); OBJ-1, OBJ-2, OBJ-4, OBJ-10

### Environmental Context

| Condition | Value |
|-----------|-------|
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC |
| Operating Temperature | **TBD** — Employer's Requirements **location TBD** — **ASSUMPTION**: Indoor control building environment (HVAC controlled) for DCS/PLC and HMI; outdoor-rated equipment for field installations |
| Environmental Classification | **TBD** — **ASSUMPTION**: Control room (indoor/climate-controlled); field equipment (outdoor/industrial with marine exposure) |
| Hazardous Area Classification | **TBD** — Per facility hazardous area study (see PKG-30 Area Classification deliverables) — affects equipment rating requirements |
| Seismic Requirements | **TBD** — Employer's Requirements **location TBD** — **ASSUMPTION**: NBC seismic zone per BC location |
| Design Life | **TBD** — Employer's Requirements **location TBD** — **ASSUMPTION**: 20-25 years typical for industrial control systems |

**Source:** Decomposition Section 1; environmental requirements TBD

### Quality and Compliance Context

| Aspect | Requirement |
|--------|-------------|
| Applicable Standards | ISA 5.1, ISA 84 / IEC 61511 (if SIS), CSA C22.1, API 554, IEC 61131 (programming), ISA/IEC 62443 (cybersecurity) |
| Quality Management | Per project Quality Management Plan |
| Regulatory Compliance | OBJ-6 (Regulatory Compliance) — specific requirements **TBD** |
| Environmental Protection | OBJ-7 (Environmental Protection) — control system support for leak detection, spill prevention **TBD** |

**Source:** Typical I&C standards; OBJ-6, OBJ-7 per Decomposition Section 2

## Construction

### Specification Structure (Anticipated)

**DCS/PLC Specification:**
- General requirements (scope, definitions, abbreviations)
- System architecture and configuration
- Controller hardware requirements (processor, memory, redundancy, I/O capacity)
- Communication requirements (protocols, network interfaces, bandwidth)
- Software requirements (programming languages per IEC 61131, licensing, version control)
- Performance requirements (scan time, response time, determinism)
- Reliability requirements (MTBF, redundancy, fail-over)
- Environmental requirements (temperature, humidity, vibration, EMI immunity)
- Power supply requirements (voltage, UPS backup)
- Expansion capability (spare I/O, future capacity per OBJ-8)
- Cybersecurity requirements (per ISA/IEC 62443 concepts if applicable)
- Testing and commissioning requirements (FAT, SAT)
- Documentation requirements (manuals, drawings, software backups)
- Warranty and support requirements

**HMI Specification:**
- General requirements
- HMI platform requirements (software, operating system, licensing)
- Hardware requirements (workstation specifications, monitors, peripherals)
- Operator interface requirements (screen layouts, alarm management, trending)
- Graphics standards and style guide
- User management and security (access levels, authentication)
- Performance requirements (screen update rate, responsiveness)
- Network interface requirements (connection to DCS/PLC and historian)
- Redundancy and backup provisions
- Expansion capability
- Testing and commissioning requirements
- Documentation requirements
- Training requirements

**Historian Specification:**
- General requirements
- Historian platform requirements (software, database, licensing)
- Hardware requirements (server specifications, storage capacity)
- Data collection requirements (data sources, sampling rates, compression)
- Data retention requirements (short-term vs. long-term storage)
- Reporting and analytics requirements
- Network interface requirements
- Redundancy and backup provisions
- Cybersecurity requirements
- Performance requirements (data throughput, query response time)
- Expansion capability
- Testing and commissioning requirements
- Documentation requirements

**Source:** **ASSUMPTION**: Typical control system technical specification content; specific requirements TBD per Employer's Requirements

### Interface Requirements

| Interface | Specification Requirement |
|-----------|---------------------------|
| Field Instrumentation (PKG-20) | I/O requirements, signal types, communication protocols (analog 4-20mA, digital, HART, Fieldbus, etc.) |
| Electrical Power (PKG-17) | Power requirements, UPS backup, grounding |
| Safety Systems (PKG-23) | Interface to fire protection, ESD systems; SIS separation if applicable |
| Process Systems (PKG-10-16) | Control strategies for unloading, loading, storage, piping, pumps, valves |
| Building Systems (PKG-21/PKG-22) | HVAC for control room, space allocation |
| Area Classification (PKG-30) | Equipment ratings for hazardous areas |

**Source:** Deliverable structure per Decomposition; typical I&C interfaces

### Standards and Codes

| Standard/Code | Application |
|---------------|-------------|
| ISA 5.1 | Instrumentation symbols and identification (coordination with DEL-19.01 drawings) |
| ISA 84 / IEC 61511 | Safety instrumented systems (if SIS in scope) — **TBD** |
| IEC 61131 | Programmable controller programming languages (ladder logic, function block, structured text, etc.) |
| CSA C22.1 | Canadian Electrical Code (electrical safety) |
| API 554 | Process instrumentation and control (bulk liquid handling best practices) |
| ISA/IEC 62443 | Cybersecurity for industrial automation — **ASSUMPTION**: Applicable for network security; requirements **TBD** |
| IEEE 802.3 | Ethernet standards (industrial network physical layer) |
| OPC UA / OPC DA | Open Platform Communications (HMI/historian connectivity to DCS/PLC) — **ASSUMPTION** |

**Source:** Typical I&C standards for control system specifications; specific applicability TBD per Employer's Requirements

## References

- **Decomposition:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — Section PKG-19, DEL-19.02
- **Context:** `_CONTEXT.md`
- **Dependencies:** `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally by humans)
- **Reference materials:** See `_REFERENCES.md` and `0_References/` in package directory
- **Cross-references within DEL-19.02:**
  - See `Specification.md` for detailed requirements (FR-01 through FR-08, PR-01 through PR-04, IR-01 through IR-05, MR-01 through MR-05)
  - See `Guidance.md` for design philosophy, trade-offs (TO-01 through TO-04), and specification structure example
  - See `Procedure.md` for specification development workflow (Steps 1-7)
- **Related deliverables:**
  - DEL-19.01 (Control System Design Drawing Set) — graphical design coordination
  - DEL-19.03 (Control System Data Sheet Package) — vendor equipment data
  - DEL-19.04 (Control System Software) — software implementation
  - DEL-20.xx (Field Instrumentation) — I/O and field device specifications
  - DEL-17.xx (Electrical Power Distribution) — power supply specifications
  - PKG-30 Area Classification — hazardous area equipment rating basis
