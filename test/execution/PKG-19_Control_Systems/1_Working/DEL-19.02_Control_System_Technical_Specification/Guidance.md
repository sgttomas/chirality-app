# Guidance: DEL-19.02 Control System Technical Specification

## Purpose

This guidance document supports the development of **Control System Technical Specification** for **PKG-19 Control Systems**.

**Deliverable purpose:** Defines performance, materials, and workmanship requirements for control system per ER requirements.

**Source:** `_CONTEXT.md`

**Deliverable classification:**
- Type: Specification (Technical Specification)
- Discipline: I&C
- Responsible: D&B Contractor

This deliverable provides the technical requirements that define WHAT the control system equipment must do and HOW it must perform. It forms the basis for vendor selection, procurement, and acceptance testing.

## Principles

### Engineering Rationale (I&C Discipline)

**Purpose of Technical Specification:** *(Supports Specification.md Scope, all FR/PR/IR/MR requirements)*
The technical specification translates project objectives and process requirements into actionable equipment requirements. It ensures:
- Equipment is fit for purpose (throughput, reliability, flexibility) — *Specification.md FR-01, FR-02, FR-03*
- Equipment meets applicable codes and standards — *Specification.md Standards section*
- Equipment is compatible with existing terminal infrastructure (where applicable) — *Considerations §4*
- Equipment can be maintained and supported over design life — *Specification.md QR-02*
- Vendor proposals are comparable and can be objectively evaluated — *Specification.md AC-03*

**Source:** Standard specification engineering practice

**Design Philosophy:** *(Supports Specification.md FR-01 through FR-08)*
- **Performance-Based:** Specify performance outcomes rather than prescribing specific products (unless pre-qualified by Employer) — *Trade-offs TO-04*
- **Reliability (OBJ-1):** Specify redundancy, MTBF, fail-over time based on criticality assessment — *Specification.md FR-03; Trade-offs TO-02*
- **Flexibility (OBJ-4):** Specify operational modes explicitly; avoid hard-coded limitations — *Specification.md FR-02*
- **Accuracy (OBJ-10):** Specify data integrity, audit trails, and custody transfer interfaces — *Specification.md FR-04*
- **Future Expansion (OBJ-8):** Specify spare capacity (I/O, controller memory, network bandwidth) for Phase 2 — *Considerations §3*
- **Lifecycle Cost (OBJ-9):** Balance capital cost with maintenance cost, spare parts availability, and support longevity — *Trade-offs TO-03*

**Source:** Project objectives OBJ-1, OBJ-4, OBJ-8, OBJ-9, OBJ-10 per Decomposition Section 2

### Applicable Standards Context

**IEC 61131-3 — Programmable Controllers Programming Languages:**
- Defines standard programming languages (ladder logic, function block, structured text, etc.)
- Ensures portability and maintainability of control logic
- Vendor shall support at least one IEC 61131-3 language

**ISA 84 / IEC 61511 — Safety Instrumented Systems:**
- If SIS is required, defines separation between BPCS and SIS
- Defines Safety Integrity Level (SIL) requirements and verification
- **TBD** — Confirm SIS scope per Employer's Requirements **location TBD**

**API 554 — Process Instrumentation and Control:**
- Industry best practices for bulk liquid handling facilities
- Guidance on alarm management, control strategies, and operator interfaces

**ISA/IEC 62443 — Cybersecurity for Industrial Automation:**
- **ASSUMPTION**: Applicable for network security architecture
- Defines security levels, zones, and conduits
- Specifies authentication, access control, and audit requirements

**ISA 18.2 — Management of Alarm Systems:**
- **ASSUMPTION**: Best practices for alarm management (alarm rationalization, alarm load targets)
- Helps prevent alarm flooding and operator overload

**Source:** Standards listed in Specification.md; rationale based on standard industry application

## Considerations

### Factors to Consider During Development

**1. Vendor Selection Strategy:** *(Supports Specification.md MR-01, MR-02, QR-01)*
- **Open Specification vs. Sole Source:** Balance standardization (Employer's existing systems) with competition — *see Trade-offs TO-04*
- **Pre-Qualified Vendors:** Determine if Employer has pre-qualified control system vendors
- **Local Support:** Consider vendor's local presence and support capabilities in BC/Canada — *Specification.md QR-02*

**2. System Architecture Trade-offs:** *(Supports Specification.md FR-01, FR-03; Procedure.md Step 2)*
- DCS vs. PLC — *see Trade-offs TO-01*
- Redundancy level — *see Trade-offs TO-02*
- Network architecture — *Specification.md FR-08*

**3. Expansion and Scalability (OBJ-8):** *(Supports Specification.md PR-01, PR-03, PR-04; Procedure.md Step 2)*
- Specify spare I/O capacity: **ASSUMPTION**: 25-30% spare typical — *Specification.md IR-01*
- Specify controller memory and processing margin — *Specification.md PR-01*
- Specify network bandwidth margin — *Specification.md PR-04*
- Consider Phase 2 expansion requirements per Employer's Requirements **TBD**

**4. Integration with Existing Terminal:** *(Supports Specification.md IR-04, IR-05; Procedure.md Step 3)*
- **Terminal Continuity (OBJ-5):** Minimize disruption during installation and commissioning
- Determine if control system must interface with existing terminal systems (SCADA, historian, network infrastructure)
- **TBD** — Employer's existing control system infrastructure per Employer's Requirements **location TBD**

**5. Operator Manning and Philosophy:** *(Supports Specification.md FR-02, FR-07, PR-02; Procedure.md Step 2)*
- Determine operational manning (24/7 vs. daytime only, number of operators)
- Determine control philosophy (centralized vs. distributed, automatic vs. manual)
- HMI workstation count and locations driven by operational philosophy
- **TBD** — Operational philosophy per Employer's Requirements **location TBD**

**6. Data Management and Historian:** *(Supports Specification.md FR-06, PR-03; Procedure.md Step 2)*
- Retention period (regulatory, commercial, operational requirements) — *Specification.md FR-06*
- Reporting requirements (daily, weekly, monthly reports) — *Specification.md FR-06*
- Integration with Employer's enterprise systems (if applicable)

**7. Cybersecurity Posture:** *(Supports Specification.md FR-08, MR-05; Procedure.md Step 2)*
- Determine cybersecurity requirements based on threat assessment and Employer's IT/OT policies
- Network segmentation, firewall rules, remote access policies — *Specification.md FR-08*
- **TBD** — Cybersecurity requirements per Employer's Requirements **location TBD**

**8. Testing and Commissioning Strategy:** *(Supports Specification.md TC-01, TC-02, TC-03; Procedure.md Steps 4–5)*
- FAT location, scope, and attendance — *Specification.md TC-01*
- SAT sequencing and acceptance criteria — *Specification.md TC-02*
- Integration testing with existing terminal operations — *Specification.md TC-03*

**Source:** Typical I&C specification development considerations; project-specific context from Decomposition objectives

## Trade-offs

### Competing Concerns to Evaluate

**Note:** These trade-offs relate to Specification.md requirements FR-01 through FR-08, PR-01 through PR-04, and MR-01 through MR-05. Trade-off resolutions should be documented in the specification and coordinated with Employer.

**TO-01: DCS vs. PLC**
- **DCS:**
  - *Advantages:* Integrated platform, advanced process control, unified engineering/HMI environment
  - *Disadvantages:* Higher cost, vendor lock-in, may be over-spec for discrete/batch operations
- **PLC:**
  - *Advantages:* Lower cost, robust for discrete control, multi-vendor ecosystem
  - *Disadvantages:* More engineering effort for HMI/historian integration, less suited for complex continuous control
- **PROPOSAL:** For canola oil transload (continuous liquid handling), DCS or high-end PLC with integrated HMI/historian is appropriate
- **TBD** — Employer preference per Employer's Requirements **location TBD**

**TO-02: Redundancy Level**
- **Full Redundancy:**
  - *Advantages:* Maximum availability (OBJ-1), no single point of failure
  - *Disadvantages:* ~2x cost, more complex
- **Partial Redundancy:**
  - *Advantages:* Balanced cost/risk, focus on critical functions
  - *Disadvantages:* Requires criticality assessment
- **Minimal Redundancy:**
  - *Advantages:* Lowest cost
  - *Disadvantages:* Higher risk of production loss
- **PROPOSAL:** Partial redundancy for critical control/safety functions; full redundancy if high availability target (e.g., >99.5%)
- **TBD** — Availability target and redundancy requirements per Employer's Requirements **location TBD**

**TO-03: Performance vs. Cost**
- Higher performance (faster scan times, more I/O capacity, larger historian) costs more but provides operational margin
- **PROPOSAL:** Specify minimum performance requirements plus margin (e.g., 25-30% spare capacity) for future growth
- **TBD** — Performance targets and spare capacity per Employer's Requirements

**TO-04: Open Standards vs. Proprietary**
- **Open Standards (OPC UA, IEC 61131-3, etc.):**
  - *Advantages:* Interoperability, reduced vendor lock-in, future flexibility
  - *Disadvantages:* May limit vendor-specific advanced features
- **Proprietary:**
  - *Advantages:* Optimized performance, vendor support
  - *Disadvantages:* Lock-in, harder to integrate
- **PROPOSAL:** Prefer open standards where possible; allow proprietary for vendor-specific optimization
- **TBD** — Employer's standards policy

**Source:** Typical I&C specification trade-offs; project context from Decomposition objectives

## Examples

### Reference Examples and Precedents

**Typical Technical Specification Structure for Industrial Control Systems:**
- Section 1: General (scope, definitions, abbreviations, references)
- Section 2: System Architecture (topology, redundancy, network)
- Section 3: Hardware Requirements (controllers, I/O, network devices)
- Section 4: Software Requirements (programming, licensing, HMI, historian)
- Section 5: Performance Requirements (scan time, response time, availability)
- Section 6: Interface Requirements (field devices, electrical, safety, enterprise)
- Section 7: Environmental and Installation Requirements
- Section 8: Testing and Commissioning (FAT, SAT, integration)
- Section 9: Documentation and Training
- Section 10: Warranty and Support

**Source:** **ASSUMPTION**: Typical specification structure; specific template TBD per project standards

**Example Performance Requirements:**
- Controller scan time: ≤100 ms for critical control loops
- I/O response time: ≤1 second end-to-end (field device to HMI)
- Alarm response time: ≤3 seconds (field event to HMI alarm annunciation)
- HMI screen update rate: ≤2 seconds
- Network availability: ≥99.9% for control network
- System availability: ≥99.5% (with redundancy)

**Source:** **ASSUMPTION**: Typical performance targets for process control systems; specific requirements TBD

**Example Spare Capacity Requirements:**
- I/O: 25-30% spare capacity (or per Phase 2 expansion requirements)
- Controller memory: 30-50% free after full programming
- Network bandwidth: 50% maximum utilization under normal conditions

**Source:** **ASSUMPTION**: Typical spare capacity provisions; specific requirements TBD

### Anticipated Artifacts Detail

**DCS/PLC Specification Sections:**
- Controller specifications (processor, memory, I/O capacity, redundancy)
- Communication specifications (protocols, network interfaces)
- Programming requirements (IEC 61131-3 languages, version control)
- Expansion provisions (spare I/O, future capacity)

**HMI Specification Sections:**
- HMI platform and software specifications
- Workstation hardware specifications (monitors, computers, peripherals)
- Operator interface requirements (screen layouts, alarm management, trending)
- Graphics standards and style guide

**Historian Specification Sections:**
- Historian platform and database specifications
- Server hardware specifications
- Data collection requirements (tags, sampling rates, compression)
- Data retention requirements (short-term, long-term)
- Reporting and analytics requirements

**Source:** `_CONTEXT.md` anticipated artifacts; typical specification content **ASSUMPTION**

## Conflict Table (for human ruling)

No conflicts identified at this enrichment stage. If conflicts arise during specification development, they will be recorded here with source citations and proposed resolutions.

**Format for future conflicts:**

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| (none) | (none) | (none) | (none) | (none) | (none) | (none) |
