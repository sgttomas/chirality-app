# Datasheet: DEL-19.04 Control System Software

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-19.04 |
| Name | Control System Software |
| Package | PKG-19 Control Systems |
| Discipline | I&C |
| Type | Software |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md` and Decomposition Section PKG-19

## Attributes

### Software Package Components

| Component | Description |
|-----------|-------------|
| PLC/DCS Application Software | Control logic, interlocks, sequencing, regulatory control, alarm logic |
| HMI Graphics | Operator screens, faceplates, trends, alarms, reports |
| Historian Configuration | Tag database, data collection configuration, archiving rules, reporting |
| Software Development Basis | DEL-19.01 (architecture), DEL-19.02 (functional requirements), process design (PKG-10-16) |

**Source:** `_CONTEXT.md` anticipated artifacts; control system software typical scope

### Software Characteristics

| Attribute | Value |
|-----------|-------|
| Programming Languages | Per IEC 61131-3 — **TBD**: Ladder Logic, Function Block Diagram, Structured Text, or vendor-specific |
| DCS/PLC Platform | Per DEL-19.03 (selected vendor equipment) — **TBD** |
| HMI Platform | Per DEL-19.03 (selected vendor equipment) — **TBD** |
| Historian Platform | Per DEL-19.03 (selected vendor equipment) — **TBD** |
| Software Version | Current supported version at time of development — **TBD** |
| License Type | Per DEL-19.02 specification — **TBD**: Perpetual or subscription |

**Source:** DEL-19.02 specification; DEL-19.03 vendor equipment selection

### System Functional Scope

| Function | Software Scope |
|----------|----------------|
| Railcar Unloading Control | 32 railcar position control, valve sequencing, level monitoring, flow control |
| Storage Tank Control | 3 tanks (3 × 15,000 MT), level monitoring, temperature monitoring, tank selection logic |
| Marine Loading Control | Loading arm control, flow control, sequencing, ship-shore interface |
| Custody Transfer Metering | Metering system interface, data collection, totalizers, reporting (OBJ-10) |
| Process Interlocks | Safety interlocks, process protection, emergency shutdown logic |
| Alarms and Events | Alarm management per ISA 18.2 concepts, alarm prioritization, event logging |

**Source:** Facility operational scope per Decomposition Section 1; OBJ-2 (throughput 1,000,000 MT/a), OBJ-10 (custody transfer accuracy)

## Conditions

### Operational Requirements

| Requirement | Software Implementation |
|-------------|-------------------------|
| Reliability (OBJ-1) | Robust error handling, watchdog timers, fail-safe logic, redundancy management (if applicable) |
| Operational Flexibility (OBJ-4) | Mode selection (tank storage vs. direct rail-to-ship), no hard-coded limitations, configurable setpoints |
| Throughput Capacity (OBJ-2) | Control logic supports 1,000,000 MT/a facility capacity |
| Custody Transfer Accuracy (OBJ-10) | Metering data integrity, audit trails, tamper-proof totalization |

**Source:** OBJ-1, OBJ-2, OBJ-4, OBJ-10 per Decomposition Section 2

### Software Development Requirements

| Requirement | Details |
|-------------|---------|
| Programming Standards | IEC 61131-3 languages; vendor best practices; structured programming (modularization, commenting, naming conventions) |
| Version Control | Software version control system — **TBD** — **ASSUMPTION**: Git or vendor-provided version control |
| Documentation | Inline code comments, functional description documents, I/O assignment lists, alarm/interlock matrices |
| Testing | Software simulation testing (offline), Factory Acceptance Test (FAT), Site Acceptance Test (SAT) |
| Security | Access control (password-protected programming), audit trails, change control |

**Source:** DEL-19.02 specification software requirements; IEC 61131-3 standard; typical software development practice

### Performance Criteria

| Criterion | Target |
|-----------|--------|
| PLC/DCS Scan Time | Per DEL-19.02 PR-01 — **ASSUMPTION**: ≤100 ms for critical control loops |
| Alarm Response Time | Per DEL-19.02 PR-02 — **ASSUMPTION**: ≤3 seconds (field event to HMI alarm) |
| Data Logging Rate | Per DEL-19.02 PR-03 — historian sampling rates **TBD** based on tag types (fast: 1 second; normal: 5-10 seconds) |

**Source:** DEL-19.02 Specification.md performance requirements

## Construction

### PLC/DCS Application Software Structure

**Control Logic Organization (Typical):**
- **Main Control Program:** Scan management, mode control, global variables
- **Process Control Modules:** Railcar unloading, storage tanks, marine loading, metering
- **Regulatory Control:** PID loops (flow, level, temperature, pressure)
- **Sequential Control:** Batch sequences, startup/shutdown sequences, valve sequencing
- **Interlock Logic:** Safety interlocks, process protection, permissive logic
- **Alarm Logic:** Alarm generation, prioritization, acknowledgment handling
- **Communication Modules:** Field device communication (Modbus, EtherNet/IP, etc.), HMI communication, historian communication

**Programming Approach:**
- Modular design (reusable function blocks for pumps, valves, tanks, etc.)
- State machine logic for sequences
- Exception handling and fault management
- Online tuning capability for PID loops

**Source:** **ASSUMPTION**: Typical DCS/PLC software structure; specific architecture TBD per vendor platform and DEL-19.02 requirements

### HMI Graphics Structure

**Screen Hierarchy (Typical):**
- **Overview Screens:** Facility overview, process flow diagram (PFD)
- **Area Screens:** Railcar unloading area, storage tank area, marine loading area
- **Detail Screens:** Individual equipment (pumps, valves, tanks, meters)
- **Trend Screens:** Real-time and historical trends
- **Alarm Screens:** Active alarms, alarm history, alarm acknowledgment
- **Reports:** Shift reports, custody transfer reports, production summary

**Graphics Standards:**
- Consistent color scheme (per ISA 101 or project standard)
- Consistent symbology (pumps, valves, tanks, etc.)
- Consistent navigation (buttons, menus)
- Alarm prioritization (color-coded: critical, high, medium, low)

**Source:** **ASSUMPTION**: Typical HMI graphics structure and ISA 101 HMI design principles; specific standards TBD per DEL-19.02 and project HMI style guide

### Historian Configuration Structure

**Tag Database:**
- Process tags (AI, AO, DI, DO from DCS/PLC)
- Calculated tags (totals, averages, rates)
- **TBD** — Total tag count based on final I/O list (PKG-20)

**Data Collection:**
- Sampling rates (fast: 1 second; normal: 5-10 seconds; slow: 1 minute)
- Compression (deadband, deviation compression)
- Data retention (short-term: **TBD** days at full resolution; long-term: **TBD** years compressed)

**Reporting:**
- Shift reports, daily production, monthly summary
- Custody transfer reports (per OBJ-10)
- Alarm/event reports

**Source:** DEL-19.02 historian requirements; typical historian configuration

### Software Development and Quality Process

**Development Phases:**
1. **Requirements Analysis:** Review DEL-19.02, process design (P&IDs from PKG-14), control strategies
2. **Design:** Software architecture, module structure, I/O assignment, alarm/interlock matrices
3. **Programming:** Code development per IEC 61131-3 and vendor platform
4. **Simulation Testing:** Offline testing, loop testing, interlock testing
5. **FAT (Factory Acceptance Test):** Integrated testing with hardware at vendor facility
6. **SAT (Site Acceptance Test):** On-site testing with field devices
7. **Commissioning:** Final tuning, optimization, operator training

**Quality Controls:**
- Peer review of code
- Version control (all changes tracked)
- Change management (change requests, approval, testing, documentation)
- Software backups (multiple generations)

**Source:** Typical software development lifecycle for industrial control systems; DEL-19.02 testing requirements

## References

- **Decomposition:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — Section PKG-19, DEL-19.04
- **Context:** `_CONTEXT.md`
- **Dependencies:** `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)
- **Basis Documents:**
  - DEL-19.01 (Control System Design Drawing Set) — system architecture, network topology
  - DEL-19.02 (Control System Technical Specification) — functional and performance requirements
  - DEL-19.03 (Control System Data Sheet Package) — vendor platform and hardware
  - Process design deliverables (PKG-10-16) — P&IDs, control strategies, I/O requirements
  - Field instrumentation deliverables (PKG-20) — I/O lists, tag numbering, signal types
- **Applicable Standards:**
  - IEC 61131-3 (Programming Languages)
  - ISA 18.2 (Alarm Management)
  - ISA 101 (HMI Design) — **ASSUMPTION**: If applicable
  - ISA/IEC 62443 (Cybersecurity) — secure programming practices
- See `Specification.md`, `Guidance.md`, `Procedure.md` for software requirements, development philosophy, and development workflow
