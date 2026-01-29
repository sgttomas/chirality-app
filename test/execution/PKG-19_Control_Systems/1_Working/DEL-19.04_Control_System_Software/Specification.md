# Specification: DEL-19.04 Control System Software

## Scope

Defines requirements for PLC/DCS application software, HMI graphics, and historian configuration within PKG-19 Control Systems.

**Deliverable purpose:** Defines and substantiates control system software in accordance with ER requirements. **Source:** `_CONTEXT.md`

### Included
- PLC/DCS control logic (process control, interlocks, alarms per DEL-19.02 functional requirements)
- HMI graphics (operator screens, alarms, trends, reports)
- Historian configuration (tag database, data collection, retention, reporting)
- Software testing and commissioning support

### Excluded
- Control system hardware (see DEL-19.03)
- Field instrumentation programming (see PKG-20)
- Installation and field wiring (see DEL-19.05)

## Requirements

### Functional Requirements (FR)

**FR-01: Process Control Implementation**
- Implement all process control strategies per process design (P&IDs from PKG-10-16)
- Support facility throughput 1,000,000 MT/a (OBJ-2): railcar unloading (32 positions), storage (3 tanks), marine loading
- Support operational flexibility (OBJ-4): tank storage mode AND direct rail-to-ship transfer mode without reconfiguration
- **Source:** DEL-19.02 FR-01, FR-02, FR-04; OBJ-2, OBJ-4
- **Rationale:** Guidance.md §Principles (Operational Flexibility); **Verification:** Procedure.md Steps 1–3, 6–7

**FR-02: Safety Interlocks and Protection**
- Implement all safety interlocks per process safety requirements
- Fail-safe logic (safe state on loss of power, communication, or control)
- Emergency shutdown (ESD) logic coordinated with PKG-23 fire protection/safety systems
- If SIS (Safety Instrumented System) in scope: BPCS/SIS separation per IEC 61511
- **Source:** DEL-19.02 FR-05, FR-06; IEC 61511 (if SIS applicable)
- **Rationale:** Guidance.md §Principles (Reliability), §Considerations (Safety Interlocks); **Verification:** Procedure.md Steps 3, 6–7, 9

**FR-03: Alarm Management**
- Alarm management per ISA 18.2 alarm management principles
- Alarm prioritization: Critical, High, Medium, Low
- Alarm load target: ≤6 alarms per operator per 10 minutes (steady-state)
- **TBD** — Peak alarm load during upset conditions
- **Source:** DEL-19.02 FR-07; ISA 18.2
- **Rationale:** Guidance.md §Considerations (Alarm Rationalization), §Trade-offs TO-02; **Verification:** Procedure.md Steps 3, 6–7

**FR-04: Data Collection and Historian**
- Historian shall collect all process tags at defined sampling rates (fast ≤1 sec, normal 5-10 sec, slow 1 min)
- Data retention: Short-term **TBD** days (full resolution), Long-term **TBD** years (compressed)
- Custody transfer metering data: integrity, audit trails, tamper-proof totalization (OBJ-10)
- Reporting: shift reports, daily production, monthly summary, custody transfer reports
- **Source:** DEL-19.02 FR-04, FR-06; OBJ-10
- **Verification:** Procedure.md Step 5, 6–7

**FR-05: HMI Operator Interface**
- Intuitive operator interface with consistent graphics, navigation, and symbology
- Process overview screens, area screens, equipment detail screens
- Real-time trends, historical trends, alarm displays
- Operator control: start/stop equipment, setpoint adjustment, mode selection
- **Source:** DEL-19.02 FR-04; ISA 101 HMI design principles (if applicable)
- **Rationale:** Guidance.md §Considerations (HMI Design), §Trade-offs TO-03; **Verification:** Procedure.md Steps 4, 6–7, 9

### Performance Requirements (PR)

**PR-01: PLC/DCS Performance**
- Controller scan time per DEL-19.02 PR-01: **ASSUMPTION** ≤100 ms for critical control loops
- I/O response time (field device to controller to HMI): **ASSUMPTION** ≤1 second end-to-end
- Control loop performance: stable PID control, ≤2% overshoot, settling time **TBD**
- **Source:** DEL-19.02 PR-01

**PR-02: HMI and Alarm Performance**
- HMI screen update rate per DEL-19.02 PR-02: **ASSUMPTION** ≤2 seconds
- Alarm response time (field event to HMI alarm annunciation): **ASSUMPTION** ≤3 seconds
- **Source:** DEL-19.02 PR-02

**PR-03: Historian Performance**
- Data collection rate adequate for tag count and sampling rates (per DEL-19.02 PR-03)
- Query response time for historical trends: **ASSUMPTION** ≤10 seconds
- **Source:** DEL-19.02 PR-03

### Quality Requirements (QR)

**QR-01: Programming Standards**
- Programming per IEC 61131-3 languages (Ladder Logic, Function Block Diagram, Structured Text, or vendor-specific if compliant)
- Structured programming: modular design, reusable function blocks, clear naming conventions
- Code commenting: all functions, function blocks, and complex logic sections commented
- Version control: all software changes tracked, versioned, and backed up
- **Source:** IEC 61131-3; DEL-19.02 MR-03 (software standards)

**QR-02: Testing and Validation**
- Simulation testing (offline, no hardware): verify control logic, interlocks, alarms
- Factory Acceptance Test (FAT): integrated testing with hardware at vendor facility per DEL-19.02 TC-01
- Site Acceptance Test (SAT): testing with field devices on-site per DEL-19.02 TC-02
- Operator acceptance: operator training and acceptance sign-off
- **Source:** DEL-19.02 TC-01, TC-02 (testing and commissioning requirements)

**QR-03: Cybersecurity**
- Password-protected programming access (role-based access control)
- Audit trails for all software changes (who, what, when)
- Secure remote access provisions (VPN, encrypted communication) if required per DEL-19.02 FR-08
- **Source:** DEL-19.02 FR-08, MR-05 (cybersecurity requirements); ISA/IEC 62443

## Standards

- **IEC 61131-3:** Programmable Controllers – Programming Languages
- **ISA 18.2:** Management of Alarm Systems for the Process Industries
- **ISA 101:** Human Machine Interfaces for Process Automation Systems (if applicable)
- **ISA/IEC 62443:** Security for Industrial Automation and Control Systems (cybersecurity)
- **IEC 61511:** Safety Instrumented Systems (if SIS scope applicable)

**Source:** DEL-19.02 Standards section; typical software development standards

## Verification

**Verification Methods:**
| Verification Activity | Method |
|-----------------------|--------|
| Code quality | Code review (peer review), compliance with IEC 61131-3 and programming standards |
| Functional correctness | Simulation testing, FAT functional testing, SAT functional testing |
| Performance | Scan time measurement, alarm response time measurement, historian data collection rate testing |
| Safety interlocks | Interlock testing (FAT and SAT), safe state verification |
| Operator acceptance | Operator training, user acceptance testing (UAT) |

**Acceptance Criteria:**
- All simulation tests pass
- All FAT tests pass (punch list resolved)
- All SAT tests pass
- Operator acceptance sign-off
- Software documentation complete

## Documentation

**Required Software Deliverables:**
1. **PLC/DCS Application Software:**
   - Source code (IEC 61131-3 programs, function blocks, data blocks)
   - Compiled/downloaded software (runtime)
   - Software backups (multiple generations)

2. **HMI Graphics:**
   - HMI project files (source)
   - HMI runtime files
   - Screen captures/documentation

3. **Historian Configuration:**
   - Tag database configuration
   - Report templates
   - Data collection configuration
   - Retention policies

**Software Documentation:**
- Functional description documents (what the software does)
- I/O assignment lists (tag database)
- Interlock matrices (interlock logic documentation)
- Alarm lists (alarm tags, priorities, setpoints, descriptions)
- Software version records (revision history)
- Test records (simulation, FAT, SAT)
- As-built documentation
- Operator manuals

**Source:** DEL-19.02 DR-01 (vendor documentation requirements); typical software deliverables
