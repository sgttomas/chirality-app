# Procedure: DEL-19.01 Control System Design Drawing Set

## Purpose

This procedure defines the process for **producing** the **Control System Design Drawing Set** within **PKG-19 Control Systems**.

**Deliverable purpose:** Defines the design arrangement and details for control system per ER requirements.

**Source:** `_CONTEXT.md`

**Deliverable type:** Drawing
**Responsible party:** D&B Contractor
**Discipline:** I&C

This procedure guides the I&C design team through the development, review, and approval of the control system design drawings, ensuring compliance with project requirements, applicable standards, and quality procedures.

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md` and `_DEPENDENCIES.md`)

**Upstream deliverables** (coordination required but not formally tracked):
- **DEL-00.xx (PKG-00):** Project design basis documents defining overall requirements
- **DEL-19.02:** Control System Technical Specification (requirements definition) — ideally developed in parallel or prior to detailed drawings
- **DEL-20.xx (PKG-20):** Field instrumentation design deliverables (I/O requirements)
- **DEL-17.xx (PKG-17):** Electrical power distribution deliverables (power requirements for control system)
- **DEL-30.xx (PKG-30):** Area classification deliverables (hazardous area boundaries affecting equipment ratings)
- **PKG-21/PKG-22:** Building design deliverables (control room layout, physical space allocation)
- **Process system deliverables (PKG-10 through PKG-16):** Process design information (P&IDs, equipment layouts) defining control requirements

**Source:** Typical I&C design workflow dependencies; specific sequencing TBD per project schedule

### Reference Materials

**Required reference documents:**
- Employer's Requirements (Volumes 2 Part 1, 2, 3) — **TBD** — **location TBD**
- Project CAD Standards — **TBD**
- Project Drawing Numbering and Revision Procedures — **TBD**
- Applicable codes and standards (see Specification.md):
  - ISA 5.1 (Instrumentation Symbols and Identification)
  - ISA 84 / IEC 61511 (if SIS scope)
  - CSA C22.1 (Canadian Electrical Code)
  - API 554 (Process Instrumentation and Control)
- Control system vendor technical documentation (if vendor selected) — **TBD**
- Site layout drawings and building design drawings — **TBD**

**Available reference materials:** See `_REFERENCES.md` and `0_References/` in package directory

### Personnel Requirements

**Qualified personnel:**
- **Originator:** I&C design engineer with experience in control system design for industrial facilities — **ASSUMPTION**: Per project staffing plan
- **Checker:** Independent checker with I&C discipline qualifications — **ASSUMPTION**: Per project quality procedures
- **Approver:** I&C discipline lead or authorized representative — **TBD**

**Competency requirements:**
- Familiarity with ISA 5.1 symbology
- CAD software proficiency (project-standard CAD platform)
- Understanding of DCS/PLC system architecture and industrial networks
- Knowledge of bulk liquid handling operations (preferred)

**Source:** **ASSUMPTION**: Standard project personnel competency requirements; specific qualifications TBD per project quality procedures

### Tools and Resources

- CAD software (project-standard platform) — **TBD**
- ISA 5.1 symbol libraries
- Project drawing templates and title blocks — **TBD**
- Access to project document management system — **TBD**

## Steps

### Step 1: Design Basis Review and Planning

**Objective:** Establish design basis and planning for drawing development

**Activities:**
1. Review Employer's Requirements for control system requirements
2. Review DEL-19.02 (Control System Technical Specification) for functional and performance requirements
3. Review project objectives (OBJ-1, OBJ-4, OBJ-10) and understand how control system supports each
4. Coordinate with process disciplines (PKG-10 through PKG-16) to understand process control requirements:
   - Railcar unloading control strategy (PKG-10)
   - Marine loading control strategy (PKG-11)
   - Custody transfer metering integration (PKG-12)
   - Storage tank monitoring and control (PKG-13)
   - Process piping control points (PKG-14)
   - Pump control (PKG-15)
5. Coordinate with electrical discipline (PKG-17) for power supply requirements
6. Coordinate with building design (PKG-21/PKG-22) for control room and cabinet space allocation
7. Identify drawing list and scope for each drawing (architecture, networks, cabinets, HMI)
8. Prepare drawing development schedule

**Outputs:**
- Design basis summary
- Drawing list and scope definition
- Coordination meeting minutes (if applicable)

**Verification:** Design basis review by discipline lead

**Source:** Typical I&C design initiation workflow; specific process TBD per project procedures

### Step 2: Control System Architecture Development

**Objective:** Define overall control system topology and functional architecture

**Activities:**
1. Define control system type (DCS vs. PLC) — coordinate with Employer if not already specified
2. Define system hierarchy (controllers, HMI, historian, I/O subsystems)
3. Define redundancy strategy for critical functions (supporting OBJ-1 reliability)
4. Define functional zones (unloading, storage, loading, utilities)
5. Assign controller responsibilities to functional zones
6. Define data flow (process data, alarms, historian)
7. Draft control system architecture drawing(s)

**Outputs:**
- Control system architecture drawing(s) (draft)

**Verification:** Self-check for completeness and consistency with requirements

**Source:** Design workflow per Specification.md functional requirements FR-01, FR-02, FR-06

### Step 3: Network Architecture Development

**Objective:** Define industrial network topology and communication infrastructure

**Activities:**
1. Define network segmentation (control network, safety network if applicable, business network)
2. Select communication protocols (EtherNet/IP, Modbus TCP, PROFINET, etc.) — coordinate with field device specifications (PKG-20)
3. Define network devices (switches, routers, firewalls) and locations
4. Define network backbone (fiber optic, copper) and routing
5. Identify cybersecurity zones and conduits (per ISA/IEC 62443 concepts if applicable)
6. Draft network drawing(s)

**Outputs:**
- Network topology drawing(s) (draft)

**Verification:** Self-check for network bandwidth, latency, and cybersecurity considerations

**Source:** Design workflow per Specification.md functional requirement FR-03

### Step 4: Cabinet Layout Development

**Objective:** Define physical arrangement of control system equipment in cabinets

**Activities:**
1. Define cabinet types and quantities (DCS/PLC cabinets, I/O cabinets, junction boxes)
2. Coordinate cabinet locations with building design (PKG-21/PKG-22) and area classification (PKG-30)
3. Develop cabinet elevations showing equipment mounting:
   - Controllers (DCS/PLC)
   - I/O modules
   - Power supplies
   - Network switches
   - Terminal blocks
   - Other equipment
4. Define cable entry/exit provisions
5. Define cooling and ventilation requirements (if required for design documentation)
6. Draft cabinet layout drawing(s)

**Outputs:**
- Cabinet layout drawing(s) (draft)

**Verification:** Self-check for dimensional accuracy and compliance with cabinet standards

**Source:** Design workflow per Specification.md; anticipated artifacts per `_CONTEXT.md`

### Step 5: HMI Arrangement Development

**Objective:** Define operator interface configuration and locations

**Activities:**
1. Define HMI workstation count and locations:
   - Control room workstations
   - Remote operator stations (railcar unloading area, marine loading area, etc.)
2. Define HMI hardware configuration (monitors, computers, input devices)
3. Define HMI connectivity to control system and historian
4. Coordinate HMI locations with building design (control room layout per PKG-21/PKG-22)
5. Consider operational flexibility requirements (OBJ-4) — support for tank storage and direct rail-to-ship modes
6. Draft HMI arrangement drawing(s)

**Outputs:**
- HMI arrangement drawing(s) (draft)

**Verification:** Self-check for operational requirements and ergonomic considerations

**Source:** Design workflow per Specification.md functional requirement FR-04; anticipated artifacts per `_CONTEXT.md`

### Step 6: Interdisciplinary Coordination

**Objective:** Verify interfaces with other disciplines and resolve conflicts

**Activities:**
1. Coordinate with field instrumentation (PKG-20):
   - Verify I/O count and signal types
   - Verify communication protocols for smart devices
2. Coordinate with electrical (PKG-17):
   - Verify power requirements for control system equipment
   - Verify UPS backup strategy
3. Coordinate with process disciplines (PKG-10 through PKG-16):
   - Verify control strategies align with process design
   - Verify interlock and shutdown logic
4. Coordinate with safety systems (PKG-23):
   - Verify fire protection and ESD interfaces
5. Coordinate with building design (PKG-21/PKG-22):
   - Verify control room layout and cabinet locations
   - Verify HVAC requirements for control room
6. Conduct interdisciplinary check (IDC) meeting(s)
7. Revise drawings to incorporate IDC comments

**Outputs:**
- IDC comment log
- Revised drawings addressing IDC comments

**Verification:** IDC sign-off by affected disciplines

**Source:** Specification.md interface requirements IR-01 through IR-05; typical engineering workflow **ASSUMPTION**

### Step 7: Independent Check

**Objective:** Perform independent technical review of drawings

**Activities:**
1. Submit drawings to independent checker (qualified I&C engineer, not the originator)
2. Checker reviews for:
   - Compliance with Employer's Requirements
   - Compliance with applicable standards (ISA 5.1, etc.)
   - Compliance with project CAD standards
   - Dimensional accuracy (cabinet layouts)
   - Consistency across drawings (architecture, networks, cabinets, HMI)
   - Interface consistency with other deliverables
   - Completeness (all required drawing types produced)
3. Checker prepares check report with comments
4. Originator addresses checker comments and revises drawings
5. Checker verifies comment closure

**Outputs:**
- Independent check report
- Revised drawings addressing check comments

**Verification:** Checker sign-off confirming technical adequacy

**Source:** Specification.md verification methods; typical engineering quality procedures **ASSUMPTION**

### Step 8: Drawing Finalization and Approval

**Objective:** Finalize drawings and obtain approval for issue

**Activities:**
1. Apply final revisions per independent check
2. Verify all title blocks, revision blocks, and drawing numbers correct per project standards
3. Verify all sheets signed by originator and checker
4. Submit drawings to discipline lead or approver
5. Approver reviews for:
   - Overall technical adequacy
   - Consistency with project strategy and objectives
   - Readiness for construction/procurement use
6. Approver signs drawings

**Outputs:**
- Approved drawing set (Control System Design Drawing Set)

**Verification:** Approver signature confirming approval for issue

**Source:** Specification.md verification methods; typical approval workflow **ASSUMPTION**

### Step 9: Document Issuance and Distribution

**Objective:** Issue drawings and distribute per project procedures

**Activities:**
1. Assign final drawing numbers and revision codes per project numbering system
2. Upload drawings to project document management system
3. Distribute drawings per project distribution matrix:
   - To procurement for control system equipment purchase
   - To construction for installation planning
   - To commissioning for planning and procedures development
   - To other disciplines for coordination
4. File issued drawings in `3_Issued/` folder (copy)
5. Update `_STATUS.md` to reflect issuance (when appropriate per lifecycle progression)

**Outputs:**
- Issued drawing set (final)
- Distribution records
- Updated `_STATUS.md` (when transitioned to ISSUED state)

**Verification:** Confirmation of distribution and document management system upload

**Source:** Specification.md documentation requirements; typical document issuance workflow **ASSUMPTION**

## Verification

### Verification Activities Summary

The following verification activities are performed during the procedure:

| Step | Verification Activity | Verifier |
|------|----------------------|----------|
| 1 | Design basis review | Discipline lead |
| 2-5 | Self-check during drafting | Originator |
| 6 | Interdisciplinary check (IDC) | Affected disciplines |
| 7 | Independent check | Independent checker |
| 8 | Approval review | Discipline lead / Approver |
| 9 | Distribution confirmation | Document control |

**Source:** Specification.md verification methods

### Acceptance Criteria (from Specification.md)

See `Specification.md` Verification section for full acceptance criteria (AC-01, AC-02, AC-03). Summary below:

**AC-01 — Completeness:**
- All required drawing types produced (architecture, networks, cabinet layouts, HMI arrangement)
- All sheets numbered, titled, and signed per project standards
- **TBD** — Specific completeness checklist per project procedures

**AC-02 — Accuracy:**
- No dimensional conflicts
- Equipment selections consistent with specifications (DEL-19.02) and data sheets (DEL-19.03)
- Interface points verified with adjacent disciplines
- **TBD** — Accuracy verification procedure

**AC-03 — Compliance:**
- ISA 5.1 symbology applied correctly per PR-03 (Specification.md)
- CAD standards complied with per PR-02 (Specification.md)
- Employer's Requirements satisfied
- **TBD** — Compliance checklist

### Sign-off Requirements

- Originator sign-off on each drawing sheet
- Checker sign-off on each drawing sheet
- Approver sign-off on each drawing sheet
- **TBD** — Specific sign-off authority matrix per project quality procedures

## Records

### Documentation Outputs (from Specification.md and `_CONTEXT.md`)

**Primary deliverable artifacts:**
1. Control system architecture drawing(s)
2. Network drawings
3. Cabinet layout drawings
4. HMI arrangement drawing(s)

**Supporting records:**
- Design basis summary
- Drawing list and scope definition
- Coordination meeting minutes
- IDC comment log and closure records
- Independent check report
- Distribution records

### Record Management

**Filing locations:**
- Working files: `1_Working/DEL-19.01_Control_System_Design_Drawing_Set/`
- Checking copies: `2_Checking/To/` (during review phase) → `2_Checking/From/` (returned with comments)
- Issued copies: `3_Issued/` (final approved drawings with issue date/revision in filename)

**Document management system:**
- All drawings uploaded to project DMS — **TBD** — DMS path and conventions
- Revision control per project procedures — **TBD**

**Retention requirements:**
- Retention per project records retention schedule — **TBD**
- **ASSUMPTION**: Electronic records retained for life of facility plus regulatory retention period

**Source:** Typical engineering records management practice; specific requirements TBD per project procedures

### Lifecycle State Management

**`_STATUS.md` transitions** (when appropriate per project lifecycle):
- `OPEN` → `INITIALIZED` (initial drafts generated)
- `INITIALIZED` → `IN_PROGRESS` (active design work underway)
- `IN_PROGRESS` → `CHECKING` (submitted for review)
- `CHECKING` → `IN_PROGRESS` (if comments require rework) or → `ISSUED` (if approved)
- `ISSUED` (final state for this phase)

**Note:** Status transitions are human-managed decisions; this procedure describes when transitions are typical, but does not automatically change status.

**Source:** Framework lifecycle model per `AGENTS.md`
