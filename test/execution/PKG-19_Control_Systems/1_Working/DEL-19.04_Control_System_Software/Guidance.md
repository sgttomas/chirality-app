# Guidance: DEL-19.04 Control System Software

## Purpose

Supports development of control system software for PKG-19 Control Systems.

**Deliverable purpose:** Defines and substantiates control system software in accordance with ER requirements. **Source:** `_CONTEXT.md`

Software implements process control strategies, safety interlocks, operator interface, and data management per DEL-19.02 functional requirements and process design (PKG-10-16).

## Principles

### Software Development Philosophy

**Reliability (OBJ-1):** *(Supports Specification.md FR-02, QR-01)*
- Fail-safe logic: safe state on faults (power loss, communication loss, sensor failure) — *Procedure.md Step 3 (Interlock Logic)*
- Robust error handling: exception handling, watchdog timers, fault detection — *Procedure.md Step 3*
- Redundancy management: if redundant controllers (per DEL-19.02 FR-06), software shall manage fail-over — *Procedure.md Step 3*
- **Source:** OBJ-1; typical industrial control system reliability practices

**Maintainability:** *(Supports Specification.md QR-01)*
- Modular design: reusable function blocks for common equipment (pumps, valves, tanks, PID loops) — *Trade-offs TO-01*
- Clear structure: organized programs (main, process control, interlocks, alarms, communications) — *Procedure.md Step 2*
- Comprehensive commenting: all functions and complex logic documented inline — *Procedure.md Step 3*
- Consistent naming: tag naming per ISA 5.1 conventions, variable naming per project standards — *Procedure.md Step 2*
- Version control: all changes tracked, change logs maintained — *Procedure.md Step 3*
- **Source:** IEC 61131-3 best practices; software maintainability principles

**Operational Flexibility (OBJ-4):** *(Supports Specification.md FR-01)*
- Configurable parameters: setpoints stored in data blocks (not hard-coded), adjustable by operators or engineers
- Mode selection: tank storage mode vs. direct rail-to-ship transfer mode selectable without software changes
- Online tuning: PID loop tuning parameters adjustable during operation — *Procedure.md Step 9 (Loop Tuning)*
- **Source:** OBJ-4; operational flexibility requirement

## Considerations

### Factors to Consider During Development

**1. Control Strategy Implementation:**
- Review P&IDs (PKG-14 process piping) for control loops, valve sequencing, interlocks
- Coordinate with process engineers for control philosophy (PID vs. on-off, cascade control, ratio control)
- Implement PID tuning: initial tuning parameters from process simulation or empirical rules; final tuning during commissioning
- **Source:** Process design coordination; typical control strategy implementation

**2. Alarm Rationalization (ISA 18.2):**
- Minimize nuisance alarms: alarm setpoints rationalized to avoid frequent alarms during normal operation
- Prioritize alarms by consequence: Critical (immediate action required), High (prompt action), Medium (awareness), Low (information)
- Alarm suppression: suppress alarms during startup/shutdown sequences when expected
- Target: ≤6 alarms per operator per 10 minutes steady-state (per ISA 18.2)
- **Source:** ISA 18.2 alarm management principles

**3. HMI Design (ISA 101 principles if applicable):**
- Operator-centric: design from operator's perspective (what do they need to see/do?)
- Minimize clicks: critical information accessible in ≤3 clicks
- Consistent graphics: same symbols for pumps, valves, tanks across all screens
- Situational awareness: overview screens show facility status at a glance
- **Source:** ISA 101 HMI design principles (if applicable); typical HMI design best practices

**4. Safety Interlocks:**
- Fail-safe: interlocks designed to failsafe on loss of signal or power
- Testable: interlock logic testable during commissioning without endangering equipment/personnel
- Documented: interlock matrices document all interlock conditions and actions
- **Source:** Process safety requirements; typical safety interlock design

**5. Cybersecurity (ISA/IEC 62443):**
- Access control: password-protected programming, role-based access (operator, engineer, administrator)
- Audit trails: log all software changes, operator actions, alarm events
- Secure communications: encrypted communication for remote access (if required per DEL-19.02 FR-08)
- **Source:** ISA/IEC 62443 cybersecurity principles; DEL-19.02 FR-08, MR-05

## Trade-offs

**TO-01: Custom Function Blocks vs. Standard Library Blocks**
- **Custom:** Optimized for specific process, flexible, more development and testing time
- **Standard:** Vendor-provided, proven, faster development, less optimization
- **PROPOSAL:** Use standard library blocks for common functions (PID, timers, counters); develop custom blocks for unique sequences or complex control strategies
- **Source:** Typical software development trade-off

**TO-02: Alarm Quantity (Information vs. Overload)**
- **Too Many Alarms:** Operator overload, alarm flooding, critical alarms missed
- **Too Few Alarms:** Inadequate information, abnormal conditions not detected
- **PROPOSAL:** Alarm rationalization per ISA 18.2 (consequence-based prioritization, target ≤6/operator/10 min)
- **Source:** ISA 18.2

**TO-03: HMI Complexity (Detail vs. Simplicity)**
- **Detailed HMI:** All information visible, many screens, complex navigation
- **Simple HMI:** Minimal information, fewer screens, risk of missing critical data
- **PROPOSAL:** Layered approach (overview → area → detail), show most critical information on overview
- **Source:** ISA 101 (if applicable)

## Examples

**Typical PLC/DCS Program Structure:**
```
Main Program
├── Scan Management (initialization, sequencing)
├── Process Control
│   ├── Railcar Unloading (32 positions)
│   ├── Storage Tanks (3 tanks)
│   ├── Marine Loading
│   └── Metering (custody transfer)
├── Regulatory Control (PID loops)
├── Sequential Control (startup, shutdown, batch sequences)
├── Safety Interlocks
├── Alarm Management
└── Communications (HMI, historian, field devices)
```

**Typical HMI Screen Hierarchy:**
- Level 1: Facility Overview (PFD showing all major areas)
- Level 2: Area Screens (Unloading, Storage, Loading)
- Level 3: Equipment Detail (Pump detail, Valve detail, Tank detail)
- Supporting Screens: Trends, Alarms, Reports

**Typical Function Block Library:**
- Pump control block (start/stop, run status, fault detection)
- Valve control block (open/close, position feedback)
- Tank monitoring block (level, temperature, high/low alarms)
- PID controller block (setpoint, process variable, output)
- Interlock block (permissives, trip logic, reset)

**Source:** **ASSUMPTION**: Typical industrial control software structure; specific implementation TBD per vendor platform and project requirements
