# Specification: DEL-19.03 Control System Data Sheet Package

## Scope

This specification defines the requirements for **Control System Data Sheet Package** within **PKG-19 Control Systems**.

**Deliverable purpose:** Defines and substantiates control system in accordance with ER requirements.

**Source:** `_CONTEXT.md`

### Included in Scope

- Review and approval of vendor-supplied data sheets for DCS/PLC equipment
- Review and approval of vendor-supplied data sheets for HMI equipment
- Review and approval of vendor-supplied data sheets for historian equipment
- Compliance verification against DEL-19.02 (Control System Technical Specification)
- Coordination with interfacing disciplines for compatibility verification
- Approval for procurement and fabrication

**Source:** `_CONTEXT.md` anticipated artifacts; DEL-19.02 equipment requirements

### Excluded from Scope

- Development of technical specification for equipment (see DEL-19.02 Control System Technical Specification)
- Vendor selection and contract award (procurement process managed separately)
- Control system design drawings (see DEL-19.01 Control System Design Drawing Set)
- Control system software development (see DEL-19.04 Control System Software)
- Equipment installation and testing (see DEL-19.05 Control System Installation & Test Records)
- Field instrumentation data sheets (see PKG-20 Field Instrumentation deliverables)

**Source:** PKG-19 deliverable structure per Decomposition

## Requirements

### Data Sheet Submittal Requirements

**DSR-01: Submittal Content and Format**
- Vendor shall submit complete equipment data sheets for all control system equipment specified in DEL-19.02
- Data sheets shall include: model/part numbers, technical specifications, performance data, environmental ratings, physical dimensions, certifications, documentation list
- Vendor shall provide compliance matrix cross-referencing DEL-19.02 specification requirements to proposed equipment specifications
- Deviations from DEL-19.02 specification shall be clearly identified and technically justified
- **Source:** Standard vendor submittal requirements; DEL-19.02 specification

**DSR-02: Submittal Schedule**
- Vendor shall submit data sheets per project submittal schedule
- Long-lead items (controllers, servers) shall be submitted early to avoid schedule delays
- **TBD** — Specific submittal schedule and lead times per project procedures

**DSR-03: Documentation Quality**
- Data sheets shall be legible, complete, and in English
- Data sheets shall be current (from current manufacturer catalogs or custom equipment specifications)
- Data sheets shall include revision/date to ensure currency
- **Source:** Standard documentation quality requirements

**DSR-04: Certifications and Approvals**
- Vendor shall provide copies of applicable certifications (UL, CSA, CE, ISO 9001, ATEX/IECEx for hazardous areas)
- Certifications shall be current and valid
- **Source:** DEL-19.02 quality requirements (MR-01, QR-01)

### Review and Approval Criteria

**RAC-01: Technical Compliance with DEL-19.02 Specification**
- Equipment shall meet or exceed all functional requirements (DEL-19.02 FR-01 through FR-08):
  - System capacity (FR-01): Support 1,000,000 MT/a throughput, 32 railcar positions, 3 storage tanks
  - Operational flexibility (FR-02): Support tank storage and direct rail-to-ship transfer modes
  - Reliability and availability (FR-03): Meet availability targets, redundancy provisions
  - Custody transfer integration (FR-04): Interface with metering systems per OBJ-10
  - Safety integration (FR-05): SIS separation if applicable
  - Data collection and historian (FR-06): Data retention and reporting capabilities
  - Alarm management (FR-07): Alarm management per ISA 18.2 principles
  - Cybersecurity (FR-08): Network segmentation, access control, authentication
- Equipment shall meet or exceed all performance requirements (DEL-19.02 PR-01 through PR-04):
  - DCS/PLC performance (PR-01): Scan time, I/O response time, accuracy, communication latency
  - HMI performance (PR-02): Screen update rate, alarm response time, concurrent operators
  - Historian performance (PR-03): Data collection rate, query response time, storage capacity
  - Network performance (PR-04): Bandwidth, availability
- **Source:** DEL-19.02 Specification.md functional and performance requirements

**RAC-02: Interface Compatibility**
- Equipment shall be compatible with all interface requirements (DEL-19.02 IR-01 through IR-05):
  - Field instrumentation (IR-01): I/O types, signal types, communication protocols compatible with PKG-20
  - Electrical power (IR-02): Power requirements compatible with PKG-17; UPS backup provisions
  - Safety systems (IR-03): Interface compatibility with PKG-23 fire protection and ESD
  - Process systems (IR-04): Control strategies compatible with PKG-10 through PKG-16 processes
  - Building systems (IR-05): HVAC and space requirements compatible with PKG-21/PKG-22
- **Source:** DEL-19.02 Specification.md interface requirements

**RAC-03: Materials and Environmental Compliance**
- Equipment shall meet all materials and environmental requirements (DEL-19.02 MR-01 through MR-05):
  - Equipment quality (MR-01): New, current manufacture, established manufacturers
  - Hardware standards (MR-02): Industrial-grade, modular, scalable
  - Software standards (MR-03): IEC 61131-3 programming, supported OS versions, licensing
  - Environmental ratings (MR-04): Temperature, humidity, vibration, EMI, hazardous area ratings per PKG-30
  - Cybersecurity (MR-05): Security features, firewall, VPN, audit logging
- **Source:** DEL-19.02 Specification.md materials and workmanship requirements

**RAC-04: Standards and Codes Compliance**
- Equipment shall comply with applicable codes and standards:
  - IEC 61131-3 (Programmable Controllers – Programming Languages)
  - ISA 84 / IEC 61511 (Safety Instrumented Systems, if SIS applicable)
  - CSA C22.1 (Canadian Electrical Code)
  - API 554 (Process Instrumentation and Control)
  - ISA 18.2 (Alarm Management)
  - ISA/IEC 62443 (Cybersecurity for Industrial Automation)
- Vendor shall reference applicable standards on data sheets and provide certification of compliance
- **Source:** DEL-19.02 Specification.md Standards section

**RAC-05: Lifecycle Support**
- Vendor shall demonstrate capability for long-term support:
  - Equipment warranty: **TBD** — **ASSUMPTION**: Minimum 12 months from final acceptance
  - Software support: **TBD** — **ASSUMPTION**: Minimum 5 years from final acceptance
  - Spare parts availability: **TBD** — **ASSUMPTION**: Minimum 10 years
  - Local support presence in BC/Canada (preferred)
- **Source:** DEL-19.02 Specification.md quality requirements (QR-02)

### Deviation Handling

**DH-01: Acceptable Deviations**
- Minor deviations that do not affect performance, interfaces, or standards compliance may be accepted with "Approve as Noted" status
- Examples: Alternate model numbers with equivalent or superior performance, minor dimensional variations that do not affect installation

**DH-02: Unacceptable Deviations**
- Deviations that affect system performance, reliability, safety, or interface compatibility shall require "Revise and Resubmit" status
- Examples: Insufficient I/O capacity, inadequate redundancy, incompatible communication protocols, missing certifications

**DH-03: Equivalency Evaluation**
- Vendor-proposed "equivalent" equipment (substitutes for specified equipment) shall be evaluated for:
  - Performance equivalency or superiority
  - Interface compatibility (no additional engineering or procurement required)
  - Standards and codes compliance
  - Lifecycle support equivalency
- Equivalents meeting all criteria may be approved; otherwise "Revise and Resubmit"

**Source:** Standard submittal review practice for deviations and equivalents

## Standards

All codes and standards from DEL-19.02 (Control System Technical Specification) apply to equipment data sheet review:
- IEC 61131-3 (Programmable Controllers)
- ISA 84 / IEC 61511 (Safety Instrumented Systems)
- CSA C22.1 (Canadian Electrical Code)
- API 554 (Process Instrumentation and Control)
- ISA 18.2 (Alarm Management)
- ISA/IEC 62443 (Cybersecurity)
- IEEE 802.3 (Ethernet)
- OPC Foundation Standards (OPC UA / OPC DA)

**Source:** DEL-19.02 Specification.md Standards section

## Verification

### Verification Methods

| Verification Activity | Method |
|-----------------------|--------|
| Technical compliance | Compliance matrix review (DEL-19.02 requirement vs. data sheet) |
| Performance adequacy | Review performance data against DEL-19.02 performance requirements (PR-01 through PR-04) |
| Interface compatibility | Interdisciplinary check (IDC) with PKG-20, PKG-17, PKG-23, process packages |
| Standards compliance | Verify certifications and standards references on data sheets |
| Lifecycle support | Review vendor warranty, support, and spare parts commitments |

**Source:** Standard vendor submittal verification practice

### Acceptance Criteria

**AC-01: Submittal Completeness**
- All required data sheets submitted (DCS/PLC, HMI, historian, network equipment)
- Compliance matrix complete and cross-referenced to DEL-19.02
- All certifications provided
- Documentation list provided

**AC-02: Technical Adequacy**
- Equipment meets or exceeds all DEL-19.02 functional and performance requirements
- No unacceptable deviations or unresolved deficiencies
- All review comments addressed (if resubmittal)

**AC-03: Approval for Procurement**
- I&C discipline lead approval issued
- Employer approval issued (if contractually required)
- Vendor authorized to proceed with equipment procurement and fabrication

**Source:** Standard submittal acceptance criteria

### Review Turnaround Time

- Contractor review turnaround: **TBD** — **ASSUMPTION**: 10-15 business days typical
- Employer review turnaround (if required): **TBD** per contract
- Vendor resubmittal turnaround: **TBD** — **ASSUMPTION**: 5-10 business days typical

**Source:** **ASSUMPTION**: Typical submittal review schedule; specific requirements TBD per project procedures

## Documentation

### Required Data Sheet Categories

**1. PLC/DCS Equipment Data Sheets:**
- Controller modules (CPUs)
- I/O modules (AI, AO, DI, DO)
- Communication modules
- Power supplies
- Racks/chassis

**2. HMI Equipment Data Sheets:**
- Workstation computers
- Monitors
- HMI software platform
- Peripheral devices

**3. Historian Equipment Data Sheets:**
- Server hardware
- Database software
- Historian application software
- Storage subsystems

**4. Network Equipment Data Sheets:**
- Industrial Ethernet switches
- Routers, firewalls (if applicable)
- Fiber optic equipment

**Source:** `_CONTEXT.md` anticipated artifacts; DEL-19.02 equipment scope

### Submittal Package Format

- Vendor cover letter with submittal summary
- Compliance matrix (DEL-19.02 requirement vs. proposed equipment)
- Equipment data sheets (manufacturer standard format acceptable)
- Certifications (copies)
- Documentation list (manuals, drawings, software)
- Deviations list (if any) with technical justification

**Source:** Standard vendor submittal package format

### Records and Filing

- Submittal log (tracking all submittals, review status, approval status)
- Review comment records
- Approved data sheets filed in `3_Issued/` folder
- Upload to project document management system
- Retention per project retention schedule — **TBD**

**Source:** Standard records management practice
