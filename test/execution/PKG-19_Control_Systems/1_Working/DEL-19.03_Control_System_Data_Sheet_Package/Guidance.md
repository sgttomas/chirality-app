# Guidance: DEL-19.03 Control System Data Sheet Package

## Purpose

This guidance supports the review and approval of **Control System Data Sheet Package** for **PKG-19 Control Systems**.

**Deliverable purpose:** Defines and substantiates control system in accordance with ER requirements.

**Source:** `_CONTEXT.md`

This deliverable consists of vendor-supplied equipment data sheets that demonstrate the proposed control system equipment meets the requirements of DEL-19.02 (Control System Technical Specification). The review and approval process ensures equipment is suitable before procurement and fabrication begins.

## Principles

### Submittal Review Philosophy

**Purpose of Data Sheet Review:**
The data sheet review is a critical control gate that verifies vendor-proposed equipment meets project requirements before significant procurement expenditures and fabrication lead times are committed. It prevents:
- Procurement of equipment that does not meet performance requirements
- Interface incompatibilities discovered late in construction
- Non-compliant equipment requiring replacement or rework
- Schedule delays due to unsuitable equipment

**Key Review Principles:**
- **Compliance-Based:** Equipment must demonstrate compliance with DEL-19.02 specification requirements
- **Performance-Focused:** Review performance data, not just feature lists
- **Interface-Critical:** Verify compatibility with field instrumentation (PKG-20), electrical (PKG-17), and other interfaces
- **Risk-Based:** Prioritize review of critical and long-lead equipment (controllers, servers)
- **Documented:** All review comments and approvals documented for traceability

**Source:** Standard EPC submittal review practice

### Role of Compliance Matrix

The compliance matrix is a key tool that systematically cross-references every requirement in DEL-19.02 to the proposed equipment specifications. It forces the vendor to demonstrate compliance and makes reviewer's job more efficient.

**Compliance Matrix Best Practices:**
- Require vendor to complete matrix (not Contractor)
- Matrix shall reference specific data sheet page numbers
- Deviations shall be clearly flagged in matrix
- Reviewer verifies matrix accuracy (do not trust without verification)

**Source:** Standard compliance verification practice

## Considerations

### Factors to Consider During Review

**1. Specification Compliance (Primary Focus)**
- Does equipment meet all functional requirements (FR-01 through FR-08 in DEL-19.02)?
- Does equipment meet all performance requirements (PR-01 through PR-04)?
- Are all interfaces compatible (IR-01 through IR-05)?
- Are environmental ratings adequate (MR-04)?

**2. Equivalency and Substitutions**
- If vendor proposes "equivalent" equipment (not specified brand/model), is it truly equivalent?
- Does equivalency create additional engineering or integration work?
- Is equivalency acceptable under project procurement rules?

**3. Long-Term Support and Obsolescence**
- Is equipment current production (not nearing end-of-life)?
- Is vendor committed to long-term support (warranty, software updates, spare parts)?
- Is equipment based on current technology platforms (not legacy/obsolete technology)?

**4. Integration and Compatibility**
- **I/O Compatibility (PKG-20):** Do I/O modules support required signal types (4-20mA, discrete, HART, Fieldbus)? Are I/O counts adequate with spare capacity?
- **Power Compatibility (PKG-17):** Do power requirements match available power supply? Is UPS capacity adequate?
- **Network Compatibility:** Are communication protocols compatible (EtherNet/IP, Modbus TCP, OPC UA, etc.)? Is network bandwidth adequate?
- **Software Compatibility:** Are HMI and historian compatible with DCS/PLC (OPC connectivity, drivers, etc.)?

**5. Cybersecurity (if DEL-19.02 specifies requirements)**
- Does equipment support required security features (authentication, access control, audit logging)?
- Does network equipment support required security protocols (firewall, VLAN, VPN)?

**6. Certifications and Standards**
- Are required certifications provided (UL, CSA, CE)?
- If hazardous area equipment (per PKG-30), are ATEX/IECEx certifications provided?
- Does vendor have ISO 9001 certification?

**Source:** Typical data sheet review considerations; DEL-19.02 requirements

## Trade-offs

### Competing Concerns to Evaluate

**Note:** These trade-offs relate to Specification.md review criteria (RAC-01 through RAC-05) and deviation handling (DH-01 through DH-03).

**TO-01: Strict Compliance vs. Flexibility for Equivalents**
- **Strict Compliance:**
  - *Advantages:* Ensures specification intent, reduces integration risk, simpler review
  - *Disadvantages:* May limit vendor options, potentially higher cost, less competitive
- **Flexibility (Accept Equivalents):**
  - *Advantages:* More vendor options, potentially lower cost, more competitive
  - *Disadvantages:* Additional engineering review, potential integration risks, deviations to track
- **PROPOSAL:** Accept equivalents if performance and interfaces are met; reject if deviations affect system reliability, performance, or integration effort
- **Source:** Standard procurement trade-off; balance cost vs. technical risk

**TO-02: Detailed Review vs. Schedule Pressure**
- **Detailed Review:**
  - *Advantages:* Thorough verification, fewer issues during installation/commissioning
  - *Disadvantages:* Longer review time, potential schedule delays
- **Fast-Track Review:**
  - *Advantages:* Maintain schedule, vendor can proceed quickly
  - *Disadvantages:* Risk of overlooking issues, potential rework later
- **PROPOSAL:** Detailed review for critical equipment (controllers, redundancy, safety interfaces); streamlined review for standard/non-critical items
- **Source:** Risk-based review approach

**TO-03: Technical Perfection vs. Practicality**
- Some deviations may be acceptable if they do not materially affect project objectives (OBJ-1 through OBJ-10)
- **PROPOSAL:** Focus on deviations that affect reliability (OBJ-1), capacity (OBJ-2), flexibility (OBJ-4), or safety; accept minor deviations that do not affect these objectives
- **Source:** Practical engineering judgment

## Examples

### Typical Data Sheet Review Checklist

**DCS/PLC Controller Review:**
- [ ] Processor speed and memory meet or exceed specification
- [ ] Scan time meets performance requirement (≤100 ms typical)
- [ ] I/O capacity adequate for field instrumentation count (PKG-20) plus spare capacity
- [ ] Communication protocols compatible (EtherNet/IP, Modbus TCP, etc.)
- [ ] Redundancy provisions meet specification (if specified)
- [ ] Environmental rating suitable for installation location (control room: climate-controlled; field: outdoor/industrial)
- [ ] Certifications provided (UL, CSA, CE; ATEX/IECEx if hazardous area)
- [ ] Programming per IEC 61131-3 languages supported
- [ ] MTBF data provided and acceptable

**HMI Workstation Review:**
- [ ] Computer specifications adequate (processor, RAM, storage)
- [ ] Monitor specifications suitable (size, resolution, touch capability)
- [ ] HMI software platform meets specification (version, features, tag capacity)
- [ ] Network interface compatible with control network
- [ ] Operating system current and supported (LTS version preferred)
- [ ] Licensing model acceptable (perpetual or long-term subscription)
- [ ] Environmental rating suitable (control room: commercial-grade acceptable)

**Historian Server Review:**
- [ ] Server hardware adequate (processor, RAM, storage capacity for retention period)
- [ ] RAID configuration for data protection
- [ ] Database software meets specification (type, version, capacity)
- [ ] Historian software meets specification (version, features, tag capacity, data compression)
- [ ] Data collection rate adequate (tags per second)
- [ ] Query response time acceptable
- [ ] Backup and disaster recovery provisions
- [ ] Network interface compatible
- [ ] Licensing model acceptable

**Source:** **ASSUMPTION**: Typical data sheet review checklist; specific checklist TBD per DEL-19.02 requirements

### Common Review Comments (Examples)

**Approve:**
- "Equipment meets all specification requirements. Approved for procurement."

**Approve as Noted:**
- "Approved with following notes: (1) Vendor to confirm spare I/O module availability; (2) Vendor to provide software licensing details prior to shipment."

**Revise and Resubmit:**
- "Controller scan time 150 ms exceeds specification requirement of ≤100 ms. Vendor to propose alternate controller meeting specification or justify deviation."
- "Missing CSA certification for control room equipment. Vendor to provide CSA-certified equipment or submit for CSA approval."
- "I/O capacity 3,000 points insufficient for project requirement of 4,500 points (per PKG-20 I/O list). Vendor to propose expanded I/O configuration."

**Source:** **ASSUMPTION**: Typical review comment language

### Deviation Documentation Example

| Deviation ID | DEL-19.02 Requirement | Vendor Proposal | Impact | Justification | Review Recommendation |
|--------------|----------------------|-----------------|--------|---------------|----------------------|
| DEV-001 | Controller scan time ≤100 ms | Proposed controller: 120 ms typical | Moderate | Vendor states 120 ms adequate for process control (not fast discrete control) | Revise and Resubmit — Vendor to propose compliant controller or provide detailed technical justification with example scan time calculations |
| DEV-002 | HMI software version 12.x | Proposed: Version 11.5 | Minor | Version 11.5 fully supported until 2028, all required features present | Approve as Noted — Vendor to confirm version 11.5 support commitment and upgrade path to version 12.x |

**Source:** **ASSUMPTION**: Typical deviation tracking format

## Conflict Table (for human ruling)

No conflicts identified at this enrichment stage. If conflicts arise during data sheet review (e.g., conflicting requirements between DEL-19.02 and vendor equipment capabilities), they will be recorded here with source citations and proposed resolutions.

**Format for future conflicts:**

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| (none) | (none) | (none) | (none) | (none) | (none) | (none) |
