# Datasheet: DEL-19.03 Control System Data Sheet Package

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-19.03 |
| Name | Control System Data Sheet Package |
| Package | PKG-19 Control Systems |
| Discipline | I&C |
| Type | Data Sheet |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md` and Decomposition Section PKG-19

## Attributes

### Data Sheet Package Characteristics

| Attribute | Value |
|-----------|-------|
| Package Type | Vendor equipment data sheets (submittal package) |
| Data Sheet Categories | PLC/DCS data sheets, HMI data sheets, Server data sheets (historian) |
| Purpose | Defines and substantiates control system equipment in accordance with ER requirements |
| Compliance Basis | DEL-19.02 (Control System Technical Specification) |
| Submittal Stage | Vendor submittals for review and approval prior to procurement |

**Source:** `_CONTEXT.md`; typical vendor submittal process for control system equipment

### Equipment Coverage

| Equipment Category | Data Sheets Required |
|--------------------|----------------------|
| DCS/PLC Controllers | Controller modules (CPU, memory), I/O modules (AI, AO, DI, DO), Communication modules, Power supplies, Racks/chassis |
| HMI Workstations | Computers/workstations, Monitors, Keyboards/mice/peripherals, HMI software platform, Licenses |
| Historian System | Server hardware, Database software, Historian application software, Licenses, Storage subsystems |
| Network Equipment | Industrial Ethernet switches, Routers, Firewalls (if applicable), Fiber optic equipment |
| Field Enclosures | Junction boxes, I/O cabinets (if pre-packaged by vendor), Environmental enclosures |

**Source:** Decomposition PKG-19 scope; typical control system equipment per DEL-19.01 architecture and DEL-19.02 specification

### System Context

| Parameter | Value |
|-----------|-------|
| Facility Capacity | 1,000,000 MT/annum canola oil throughput (OBJ-2) |
| Control Scope | 32 railcar unloading positions, 3 × 15,000 MT storage tanks, marine loading operations, custody transfer metering |
| Reliability Objective | Safe, efficient, reliable, continuous operation (OBJ-1) |
| Flexibility Objective | Support tank storage and direct rail-to-ship transfer modes (OBJ-4) |

**Source:** OBJ-1, OBJ-2, OBJ-4 per Decomposition Section 2

## Conditions

### Data Sheet Source and Process

| Condition | Value |
|-----------|-------|
| Data Sheet Provider | Control system vendor (selected based on DEL-19.02 specification procurement) |
| Submittal Trigger | After vendor contract award, per submittal schedule |
| Submittal Format | Vendor-standard data sheets + project-specific compliance matrix |
| Review Authority | D&B Contractor I&C discipline (technical review); Employer (if contractually required) |
| Approval Authority | I&C discipline lead or authorized representative |

**Source:** Standard D&B contract vendor submittal process

### Compliance Requirements

**Equipment shall demonstrate compliance with:**
- DEL-19.02 specification requirements (functional, performance, interface, environmental)
- Applicable codes and standards (IEC 61131-3, ISA 84, CSA C22.1, API 554, ISA/IEC 62443)
- Facility capacity requirements (1,000,000 MT/a throughput per OBJ-2)
- Reliability requirements (redundancy, MTBF, fail-over time per OBJ-1)
- Operational flexibility requirements (dual operating modes per OBJ-4)
- Environmental conditions (temperature, humidity, vibration, EMI, hazardous area classification per PKG-30)

**Source:** DEL-19.02 specification requirements; project objectives

### Quality and Certification Requirements

| Requirement | Details |
|-------------|---------|
| Equipment Quality | New, current manufacture, from established manufacturers with industrial control system track record |
| Certifications | UL, CSA, CE markings as applicable; vendor ISO 9001 certification (or equivalent) |
| Documentation | Installation manuals, operation manuals, maintenance manuals, spare parts lists |
| Warranty | Per DEL-19.02 specification — **TBD** — **ASSUMPTION**: Minimum 12 months from final acceptance |
| Support | Long-term support commitment, spare parts availability, software support per DEL-19.02 |

**Source:** DEL-19.02 quality and warranty requirements

## Construction

### Typical Data Sheet Content (by Equipment Type)

**PLC/DCS Controller Data Sheets:**
- Model/part numbers
- Processor specifications (speed, architecture, instruction set)
- Memory specifications (program memory, data memory, expandability)
- Scan time performance (typical and maximum)
- I/O capacity (total points, modules supported)
- Communication interfaces (protocols, data rates, ports)
- Power supply specifications (voltage, current, holdup time, redundancy)
- Environmental ratings (operating temperature, storage temperature, humidity, vibration, EMI immunity)
- Physical dimensions and mounting requirements
- Certifications (UL, CSA, CE, ATEX/IECEx for hazardous areas if applicable)
- MTBF (Mean Time Between Failures)

**HMI Workstation Data Sheets:**
- Computer/workstation specifications (processor, RAM, storage, OS version)
- Monitor specifications (size, resolution, touch capability, industrial vs. commercial grade)
- HMI software platform (version, features, tag capacity, licensing model)
- Graphics capabilities (screen layouts, trending, alarm management)
- Network interfaces (Ethernet ports, protocols supported)
- Redundancy provisions (if applicable)
- Environmental ratings (operating environment: control room climate-controlled)
- Physical dimensions and mounting
- Certifications

**Server Data Sheets (Historian):**
- Server hardware specifications (processor, RAM, storage capacity, RAID configuration)
- Operating system (version, licensing)
- Database software (type, version, capacity)
- Historian application software (version, features, tag capacity, data compression, retention capabilities)
- Network interfaces (Ethernet, protocols, redundancy)
- Data collection performance (tags per second, query response time)
- Backup and disaster recovery provisions
- Environmental ratings (server room environment)
- Physical dimensions (rack-mount standard)
- Certifications

**Network Equipment Data Sheets:**
- Industrial Ethernet switch specifications (ports, speed, managed/unmanaged, redundancy protocols like RSTP/MRP)
- Router specifications (if applicable)
- Firewall specifications (if applicable for cybersecurity zones per ISA/IEC 62443)
- Fiber optic media converters (if applicable)
- Environmental ratings (control room and/or field-rated)
- Certifications

**Source:** Typical vendor data sheet content for industrial control systems

### Review and Approval Workflow

**Step 1: Vendor Submittal**
- Vendor submits data sheets per project submittal schedule
- Submittal includes: equipment data sheets, compliance matrix (DEL-19.02 spec vs. proposed equipment), certifications, documentation list

**Step 2: Contractor Technical Review**
- I&C discipline reviews data sheets against DEL-19.02 specification requirements
- Verify compliance with functional requirements (FR-01 through FR-08 in DEL-19.02)
- Verify compliance with performance requirements (PR-01 through PR-04 in DEL-19.02)
- Verify interface compatibility (IR-01 through IR-05 in DEL-19.02)
- Verify environmental ratings and certifications (MR-01 through MR-05 in DEL-19.02)
- Identify deviations, deficiencies, or missing information
- Prepare review comments with status: Approve / Approve as Noted / Revise and Resubmit

**Step 3: Interdisciplinary Check**
- Coordinate with field instrumentation (PKG-20) for I/O compatibility and communication protocols
- Coordinate with electrical (PKG-17) for power requirements and compatibility
- Coordinate with safety systems (PKG-23) for safety interface compatibility

**Step 4: Employer Review (if required)**
- Submit data sheets to Employer for review (if contractually required)
- Consolidate Employer comments

**Step 5: Review Comment Issuance**
- Issue consolidated review comments to vendor
- Request resubmittal if revisions required

**Step 6: Resubmittal Review (if applicable)**
- Verify vendor addressed all review comments
- Approve if compliant

**Step 7: Final Approval**
- I&C discipline lead issues final approval
- Vendor authorized to proceed with procurement and fabrication

**Source:** Typical vendor submittal review and approval process for EPC projects

### Compliance Matrix (Example Structure)

| DEL-19.02 Requirement ID | Requirement Description | Proposed Equipment / Data Sheet Reference | Compliance Status | Comments |
|--------------------------|-------------------------|-------------------------------------------|-------------------|----------|
| FR-01 | System Capacity (1,000,000 MT/a support) | Controller: Model XYZ, I/O capacity 5000 points | Complies | Capacity exceeds requirement |
| PR-01 | Scan time ≤100 ms | Data sheet page 5: Typical scan time 50 ms | Complies | — |
| ... | ... | ... | ... | ... |

**Source:** Typical compliance matrix format for vendor submittals

## References

- **Decomposition:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — Section PKG-19, DEL-19.03
- **Context:** `_CONTEXT.md`
- **Dependencies:** `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally by humans)
- **Compliance Basis:** DEL-19.02 (Control System Technical Specification) — all requirements from DEL-19.02 apply to data sheet review
- **Coordination:** DEL-19.01 (Control System Design Drawing Set) — equipment arrangement and architecture context
- **Cross-references within DEL-19.03:**
  - See `Specification.md` for data sheet requirements (DSR-01 through DSR-04) and review criteria (RAC-01 through RAC-04)
  - See `Guidance.md` for review philosophy and trade-offs
  - See `Procedure.md` for submittal review workflow (Steps 1-8)
- **Related deliverables:**
  - DEL-19.04 (Control System Software) — software platform compatibility
  - DEL-19.05 (Control System Installation & Test Records) — equipment to be installed and tested
  - DEL-20.xx (Field Instrumentation) — I/O interface compatibility
  - DEL-17.xx (Electrical Power Distribution) — power supply compatibility
  - PKG-30 Area Classification — hazardous area equipment certification requirements
