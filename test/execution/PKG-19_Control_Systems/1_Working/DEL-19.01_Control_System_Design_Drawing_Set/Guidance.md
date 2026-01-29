# Guidance: DEL-19.01 Control System Design Drawing Set

## Purpose

This guidance document supports the development of **Control System Design Drawing Set** for **PKG-19 Control Systems**.

**Deliverable purpose:** Defines the design arrangement and details for control system per ER requirements.

**Source:** `_CONTEXT.md`

**Deliverable classification:**
- Type: Drawing
- Discipline: I&C (Instrumentation & Control)
- Responsible: D&B Contractor

This deliverable provides the graphical design documentation that defines how the control system is architected, networked, physically arranged, and interfaced with operators. It forms the basis for procurement, installation, and commissioning of the control system.

## Principles

### Engineering Rationale (I&C Discipline)

**Control System Role:**
The control system is the central nervous system of the canola oil transload facility, coordinating:
- Railcar unloading operations (32 positions)
- Storage tank operations (3 × 15,000 MT tanks)
- Marine loading operations
- Custody transfer metering
- Safety interlocks and alarms
- Process optimization

**Source:** Decomposition Project Overview and PKG-19 scope; facility capacity parameters from OBJ-2, OBJ-3

**Design Philosophy:**
- **Reliability (OBJ-1):** Control system architecture shall minimize single points of failure affecting safe and continuous operation. Redundancy strategy for critical functions.
- **Operational Flexibility (OBJ-4):** System shall support multiple operating modes (tank storage, direct rail-to-ship) without reconfiguration.
- **Accuracy (OBJ-10):** Integration with custody transfer metering systems to ensure measurement integrity.
- **Maintainability:** Modular design facilitating maintenance and future expansion (OBJ-8).

**Source:** Project objectives OBJ-1, OBJ-4, OBJ-8, OBJ-10 per Decomposition Section 2

### Applicable Standards Context

**ISA 5.1 — Instrumentation Symbols and Identification:**
- Provides standardized symbology for control system documentation
- Ensures consistency and clarity in drawing interpretation
- Facilitates communication across disciplines and project phases

**ISA 84 / IEC 61511 — Safety Instrumented Systems:**
- Governs design of safety functions if Safety Instrumented System (SIS) is in scope
- Defines separation between Basic Process Control System (BPCS) and SIS
- **TBD** — Confirm if SIS scope applies to this facility per Employer's Requirements **location TBD**

**CSA C22.1 — Canadian Electrical Code:**
- Governs electrical safety and installation requirements
- Applies to power distribution within control cabinets and to control equipment

**API 554 — Process Instrumentation and Control:**
- Provides industry best practices for process control system design in petroleum and chemical facilities
- Applicable to canola oil transload operations (bulk liquid handling)

**ISA/IEC 62443 — Cybersecurity for Industrial Automation:**
- **ASSUMPTION**: Likely applicable for network security architecture
- Defines security zones, conduits, and defense-in-depth strategies
- **TBD** — Confirm specific cybersecurity requirements per Employer's Requirements **location TBD**

**Source:** Standards listed in Datasheet.md and Specification.md; rationale based on standard industry application

## Considerations

### Factors to Consider During Development

**1. System Architecture:**
- **Centralized vs. Distributed Control:** Evaluate control system topology (single DCS vs. distributed PLCs) based on facility geography, reliability requirements, and operational preferences
- **Redundancy Strategy:** Determine level of redundancy (controller, power supplies, communications) required for OBJ-1 reliability
- **Scalability:** Consider future expansion to support Phase 2 (OBJ-8)

**2. Network Design:**
- **Network Segmentation:** Separate process control, safety (if SIS), and business networks to meet cybersecurity and reliability requirements
- **Communication Protocols:** Select industrial protocols (e.g., EtherNet/IP, Modbus TCP, PROFINET) compatible with field devices (PKG-20) and compatible with Employer's existing terminal infrastructure
- **Bandwidth and Latency:** Size network to support real-time control, historian data collection, and HMI responsiveness

**3. Physical Arrangement:**
- **Control Room Location:** Coordinate with building design (PKG-21/PKG-22) for optimal visibility, access, and environmental conditions
- **Cabinet Locations:** Balance accessibility for maintenance, proximity to field devices (cable length), and environmental protection (indoor vs. outdoor)
- **Hazardous Area Classification:** Equipment in or near hazardous areas (PKG-30) must meet area classification requirements

**4. Operator Interface:**
- **HMI Configuration:** Determine number and location of HMI workstations based on operational manning and operational modes (tank storage vs. direct transfer)
- **Remote Access:** Consider need for remote HMIs or mobile operator interfaces for field operations
- **Ergonomics and Human Factors:** HMI arrangement should support effective monitoring and control by operators

**5. Interfaces and Coordination:**
- **Field Instrumentation (PKG-20):** I/O count, signal types, and communication protocols must be coordinated
- **Electrical Power (PKG-17):** Power requirements, UPS backup, and emergency shutdown power must be defined
- **Process Systems (PKG-10 through PKG-16):** Control strategies and interlocks depend on process equipment design
- **Safety Systems (PKG-23):** Fire protection and emergency shutdown systems must interface with control system

**6. Regulatory and Environmental:**
- **Environmental Protection (OBJ-7):** Control system shall support leak detection, spill prevention, and environmental monitoring functions
- **Terminal Continuity (OBJ-5):** Installation and commissioning sequencing to minimize disruption to existing terminal operations

**Source:** Typical I&C design considerations; project-specific context from Decomposition objectives and scope

## Trade-offs

### Competing Concerns to Evaluate

**Note:** These trade-offs relate to Specification.md requirements FR-01 (System Topology), FR-02 (Control Architecture), and FR-06 (Reliability and Redundancy). Trade-off resolutions should be documented during design development and reflected in the drawing set.

**TO-01: DCS vs. PLC Architecture**
- **DCS (Distributed Control System):**
  - *Advantages:* Integrated platform, unified engineering environment, better suited for continuous process control
  - *Disadvantages:* Higher capital cost, potential vendor lock-in, single-source dependency
- **PLC (Programmable Logic Controller):**
  - *Advantages:* Lower cost, modular/scalable, multi-vendor options, rugged
  - *Disadvantages:* More complex system integration, potentially more engineering effort for HMI/historian integration
- **PROPOSAL:** Selection should consider Employer's existing terminal infrastructure, maintenance capabilities, and future expansion plans (OBJ-8)
- **TBD** — Employer preference per Employer's Requirements **location TBD**

**TO-02: Redundancy Level**
- **Full Redundancy (controllers, power, communications):**
  - *Advantages:* Maximum reliability (OBJ-1), no single point of failure
  - *Disadvantages:* Higher cost, increased complexity
- **Partial Redundancy (critical loops only):**
  - *Advantages:* Balanced cost/reliability, focused on high-risk areas
  - *Disadvantages:* Requires careful criticality assessment
- **Minimal Redundancy:**
  - *Advantages:* Lower cost, simpler design
  - *Disadvantages:* Increased risk of operational interruptions
- **PROPOSAL:** Redundancy strategy should be risk-based, considering consequence of control system failure on safety (OBJ-1), throughput (OBJ-2), and terminal operations (OBJ-5)
- **TBD** — Redundancy requirements per Employer's Requirements **location TBD**

**TO-03: Wired vs. Wireless Field Devices**
- **Wired I/O:**
  - *Advantages:* Proven reliability, deterministic communication, no battery maintenance
  - *Disadvantages:* Higher installation cost (cable and conduit), less flexible for future changes
- **Wireless I/O (where permitted):**
  - *Advantages:* Lower installation cost, easier to relocate, reduced cable runs
  - *Disadvantages:* Potential reliability concerns (signal interference, battery life), cybersecurity considerations
- **PROPOSAL:** Wired for critical control loops and custody transfer; wireless may be considered for non-critical monitoring
- **TBD** — Wireless device policy per Employer's Requirements **location TBD**

**TO-04: Centralized Control Room vs. Distributed Operator Stations**
- **Centralized:**
  - *Advantages:* Consolidated operator presence, easier supervision, unified view of facility
  - *Disadvantages:* Operators farther from field equipment, longer response time for field issues
- **Distributed:**
  - *Advantages:* Operators closer to processes, faster local response
  - *Disadvantages:* More complex communication, potential for inconsistent situational awareness
- **PROPOSAL:** Hybrid approach with central control room plus remote HMIs at key field locations (railcar unloading, marine loading) may optimize operational flexibility (OBJ-4)
- **TBD** — Operational philosophy per Employer's Requirements **location TBD**

**Source:** Typical I&C design trade-offs; project context from Decomposition objectives; specific decisions TBD

## Examples

### Reference Examples and Precedents

**Typical Control System Architecture for Bulk Liquid Terminals:**
- Central DCS or PLC system located in control building
- Distributed I/O at process areas (unloading, storage, loading)
- Redundant controllers and power supplies for critical functions
- Separate BPCS and SIS (if required)
- Industrial Ethernet backbone with fiber optic runs to remote I/O
- HMI workstations in control room plus remote operator stations

**Source:** **ASSUMPTION**: Industry standard practice for similar facilities; specific precedents TBD

**Network Architecture Example:**
- **Level 3 (Business Network):** Historian, engineering workstations, enterprise connectivity
- **Level 2 (Supervisory Network):** HMI workstations, OPC servers, reporting systems
- **Level 1 (Control Network):** DCS/PLC controllers, I/O subsystems
- **Level 0 (Field Network):** Smart field devices, remote I/O

**Source:** **ASSUMPTION**: Purdue Reference Model for industrial control systems; specific architecture TBD per Employer's Requirements

**Cabinet Layout Considerations:**
- Standard cabinet widths (e.g., 600mm, 800mm) for modularity
- Top-mounted cable entry for indoor cabinets, bottom entry for outdoor to prevent water ingress
- Adequate clearance for door swing and maintenance access
- Separation of power and signal wiring to minimize EMI

**Source:** **ASSUMPTION**: Standard electrical cabinet design practice; specific requirements TBD per project standards

**HMI Arrangement Best Practices:**
- Dual monitors per operator workstation for process overview and detail views
- Ergonomic workstation design (adjustable chairs, proper lighting, line of sight to process windows if applicable)
- Backup HMI capability in case of primary workstation failure
- Consistent HMI graphics standards for ease of operation

**Source:** **ASSUMPTION**: Human factors best practices; specific configuration TBD per Employer's Requirements and DEL-19.04

### Anticipated Artifacts Detail

**Control System Architecture Drawing(s):**
- Single-line diagram showing all controllers, HMIs, historian, and network connections
- Functional zones (unloading, storage, loading, utilities)
- Redundancy configuration

**Network Drawings:**
- Network topology showing switches, routers, firewalls
- IP addressing scheme (if required for design documentation)
- Cable routing and backbone infrastructure

**Cabinet Layout Drawings:**
- Elevation and plan views of each cabinet type
- Equipment mounting locations and labels
- Terminal strip assignments (if required)
- Cable entry/exit details

**HMI Arrangement Drawings:**
- Control room layout with workstation locations
- Remote HMI locations (field operator stations)
- HMI hardware and connectivity

**Source:** `_CONTEXT.md` anticipated artifacts; typical drawing content **ASSUMPTION**

## Conflict Table (for human ruling)

No conflicts identified at this enrichment stage. If conflicts arise during detailed design, they will be recorded here with source citations and proposed resolutions.

**Format for future conflicts:**

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| (none) | (none) | (none) | (none) | (none) | (none) | (none) |
