# Procedure: DEL-24.02 Security System Technical Specification

## Purpose

This procedure defines the process for **producing** the **Security System Technical Specification** within **PKG-24 Security Systems** for the Canola Oil Transload Facility.

**Deliverable objective:** Defines performance, materials, and workmanship requirements for security system per ER requirements.

*Source: `_CONTEXT.md`; Decomposition Section 5 — PKG-24 (line 567)*

**Deliverable type:** Specification
**Responsible party:** D&B Contractor
**Discipline:** Specialty (Security Systems)

**Procedure scope:** This procedure covers the workflow from design basis review through final specification issuance, including requirements development, specification writing, review, and approval.

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

*Source: `_DEPENDENCIES.md`*

**Upstream deliverables and information required:**
- **DEL-24.01** — Security System Design Drawing Set (design basis for specification requirements)
- **TBD** — Employer's Requirements (ER) Volume 2 — security system functional and performance requirements
- **TBD** — Hazardous area classification drawings
- **TBD** — Terminal security standards and integration requirements (from Employer/Terminal IT/security operations)
- **TBD** — Project quality management plan and specification standards

**Interface coordination required with:**
- PKG-17 (Electrical Power) — power supply requirements and specifications
- PKG-23 (Fire Protection) — access control integration with fire alarm/life safety
- PKG-25 (Communications & IT) — network infrastructure specifications

*Source: Standard interdisciplinary coordination for technical specification development*

### Reference Materials

**Required references:**
- See `_REFERENCES.md` for applicable reference documents (note: no specific references identified yet)
- See `0_References/` in package directory for reference materials

**Expected reference materials:**
- Employer's Requirements Volume 2 Parts 1-3 (location: **TBD**)
- DEL-24.01 (Security System Design Drawing Set) — design basis
- **TBD** — DP World Fraser Surrey Terminal security standards and specifications
- **TBD** — Project specification standards and templates (CSI MasterFormat or equivalent)
- **TBD** — Approved manufacturers and equipment standards

**Applicable codes and standards:**
- See `Specification.md` for complete list
- Key standards: **TBD** — IEC 62676, ONVIF, OSDP, NBC 2020, CEC (CSA C22.1)

*Source: Specification.md — Standards section; `_REFERENCES.md`*

### Personnel Requirements

**Qualifications:**
- **Lead specifier:** Security systems engineer or specialist with **TBD** years of experience in security system specification and procurement
- **Technical writer:** Proficiency in technical specification writing (CSI MasterFormat or equivalent)
- **Reviewer:** Independent qualified specialist, not involved in original specification development
- **Approver:** Discipline lead or designated authority

**Competency requirements:**
- Understanding of security system technologies (CCTV, access control, network infrastructure)
- Knowledge of applicable codes and standards
- Experience with procurement specifications and construction documents
- Familiarity with Terminal integration requirements
- **ASSUMPTION:** Personnel competency per project Quality Management Plan

*Source: Standard specification development competency requirements*

### Tools and Resources

**Software and tools:**
- **TBD** — Word processing or specification software (MS Word, SpecLink, MasterSpec)
- **TBD** — Project document management system for transmittals and reviews
- **TBD** — Requirements management tool or spreadsheet for ER compliance matrix

**Access and permissions:**
- Access to project document management system
- Access to DEL-24.01 design drawings and coverage analysis
- Access to Terminal security system documentation **TBD** — coordinate with Employer

## Steps

### Step 1: Design Basis Review and Requirements Extraction

**Objective:** Understand design intent and extract specification requirements from design drawings.

**Activities:**
1.1. Review DEL-24.01 (Security System Design Drawing Set)
   - CCTV layout: Camera locations, types (fixed/PTZ), mounting details
   - Camera coverage drawings: Coverage analysis, image quality requirements, field-of-view calculations
   - Access control layout: Reader locations, door hardware, access control panel locations
   - System architecture: Network topology, Terminal integration points

1.2. Extract equipment requirements from design:
   - Camera specifications (resolution, frame rate, lens, environmental ratings) to achieve coverage requirements
   - NVR/VMS requirements (capacity, storage, retention period)
   - Access control system requirements (technology, capacity, architecture)
   - Network infrastructure requirements (cabling, switches, bandwidth)
   - Power and UPS requirements

1.3. Review Employer's Requirements (ER) **TBD** — specific ER sections
   - Functional requirements (what the system must do)
   - Performance requirements (how well it must perform)
   - Quality and reliability requirements
   - Integration requirements per DEC-05
   - Testing and acceptance criteria

1.4. Create ER compliance matrix
   - Map each ER requirement to specification section where it will be addressed
   - Identify any ER requirements not covered by design — flag for resolution
   - Document traceability from ER to specification

**Outputs:**
- Equipment requirements list extracted from DEL-24.01
- ER compliance matrix (requirements vs. specification sections)
- Design basis summary

**Verification:** Design basis review meeting with design team (DEL-24.01 designers)

*Source: DEL-24.01 as design basis; ER as requirements source*

---

### Step 2: Specification Structure and Outline Development

**Objective:** Establish specification document structure and section outline.

**Activities:**
2.1. Select specification format **TBD**
   - CSI MasterFormat (Division 28 — Electronic Safety and Security) **ASSUMPTION**
   - Or narrative/performance specification format
   - Or project-specific format per Employer requirements

2.2. Develop specification outline:
   - **Part 1 — General:** Scope, references, submittals, quality assurance, delivery/storage, warranties
   - **Part 2 — Products:** CCTV system (cameras, NVR, VMS), access control system (readers, controllers, software, door hardware), network infrastructure, materials
   - **Part 3 — Execution:** Installation requirements, testing and acceptance, commissioning, training, closeout

2.3. Allocate requirements to sections:
   - Map functional requirements to Product sections (Section 2)
   - Map installation and quality requirements to Execution sections (Section 3)
   - Map submittals and documentation requirements to General sections (Section 1)

2.4. Identify sub-specifications or appendices:
   - CCTV system specification
   - Access control system specification
   - Network infrastructure specification
   - Testing and acceptance procedures (or reference to PKG-29)

**Outputs:**
- Specification outline with section structure
- Requirements allocation matrix (requirements vs. sections)

**Verification:** Outline review with discipline lead and project team

*Source: Guidance.md — specification structure examples; CSI MasterFormat *

---

### Step 3: Specification Writing — Part 1 (General Requirements)

**Objective:** Write Part 1 sections defining general project requirements.

**Activities:**
3.1. Section 1.1 — Summary
   - Scope of work (CCTV, access control, integration per DEC-05)
   - Related sections and disciplines (PKG-17, PKG-23, PKG-25)
   - Work included and excluded

3.2. Section 1.2 — References
   - List all applicable codes and standards (NBC, CEC, IEC 62676, ONVIF, OSDP, etc.)
   - Reference DEL-24.01 design drawings

3.3. Section 1.3 — Submittals
   - Product data and equipment specifications (DEL-24.03)
   - Shop drawings and integration drawings
   - Test procedures and acceptance criteria
   - Operation and maintenance manuals
   - Warranties and certifications
   - Define submittal review and approval process

3.4. Section 1.4 — Quality Assurance
   - Equipment manufacturer qualifications
   - Installer qualifications and certifications **TBD**
   - Quality control procedures
   - Factory Acceptance Testing (FAT) requirements **TBD**

3.5. Section 1.5 — Delivery, Storage, and Handling
   - Protection and storage requirements for equipment
   - Handling procedures to prevent damage

3.6. Section 1.6 — Project Conditions
   - Environmental conditions (marine/coastal environment, temperature, humidity, hazardous areas)
   - Coordination with ongoing Terminal operations (OBJ-5)
   - Site access and security requirements

3.7. Section 1.7 — Warranty
   - Equipment warranty requirements (duration, coverage)
   - System warranty and support requirements

**Outputs:**
- Part 1 (General) sections drafted

**Verification:** Self-check for completeness and clarity

*Source: Specification.md — Requirements sections; Guidance.md — specification structure*

---

### Step 4: Specification Writing — Part 2 (Products)

**Objective:** Write Part 2 sections defining equipment and materials requirements.

**Activities:**
4.1. Section 2.1 — System Description
   - Overall CCTV and access control system architecture
   - Performance requirements (reliability, availability, image quality, access control response time)
   - Integration requirements with Terminal systems per DEC-05 **TBD**

4.2. Section 2.2 — CCTV System Components
   - **Cameras:** Fixed and PTZ specifications (resolution, frame rate, low-light performance, environmental ratings, power requirements, mounting)
   - **NVR:** Recording capacity, storage architecture, redundancy, network throughput
   - **VMS:** Software features, licensing, ONVIF compliance, integration APIs
   - Specify performance requirements to achieve design (DEL-24.01) coverage objectives
   - Approved manufacturers list **TBD** — or "or approved equivalent" language

4.3. Section 2.3 — Access Control System Components
   - **Card readers:** Technology (proximity/smart card/biometric), read range, environmental ratings, protocol (OSDP/Wiegand)
   - **Controllers:** Architecture (distributed/centralized), capacity, communication, battery backup, fail-safe/fail-secure capability
   - **Door hardware:** Electric strikes, magnetic locks, crash bars, door position switches, REX devices
   - **Software:** User management, access levels, audit trails, alarm handling, Terminal integration **TBD**
   - Approved manufacturers list **TBD**

4.4. Section 2.4 — Network Infrastructure
   - **Cabling:** Cat6A, fiber optic, specifications, environmental ratings
   - **Network switches:** PoE specifications, managed features (VLAN, QoS), redundancy
   - **Network architecture:** VLANs, bandwidth, firewall, security

4.5. Section 2.5 — Materials
   - Conduit and cable tray (types, ratings, hazardous area compliance)
   - Mounting hardware (marine-grade stainless steel for coastal environment)
   - Power supplies and UPS (specifications, battery backup duration)
   - Cable entry and sealing (IP ratings, hazardous area sealing)

**Outputs:**
- Part 2 (Products) sections drafted

**Verification:** Self-check for completeness; verify specifications support design (DEL-24.01)

*Source: Datasheet.md — system components; Specification.md — functional requirements; DEL-24.01 design basis*

---

### Step 5: Specification Writing — Part 3 (Execution)

**Objective:** Write Part 3 sections defining installation, testing, and closeout requirements.

**Activities:**
5.1. Section 3.1 — Installation
   - General installation requirements (follow manufacturer instructions, applicable codes)
   - Mounting and support requirements (coordinate with structural disciplines)
   - Cable routing and termination (neat, accessible, labeled)
   - Conduit installation (underground/overhead coordination with PKG-03, PKG-17)
   - Hazardous area installation (conduit sealing, equipment ratings)
   - Phased installation to minimize Terminal disruption (OBJ-5)

5.2. Section 3.2 — Testing and Acceptance
   - Pre-installation testing (verify equipment before installation)
   - Installation testing (verify proper installation)
   - System functional testing (individual system operation)
   - Integration testing (CCTV and access control with Terminal systems per DEC-05)
   - Site Acceptance Testing (SAT) procedures and acceptance criteria
   - Reference PKG-29 (Testing) for detailed test procedures
   - Deficiency management and resolution

5.3. Section 3.3 — Commissioning
   - System commissioning per PKG-30 procedures
   - Performance verification (verify system meets specification requirements)
   - Integration verification with Terminal security operations
   - Operational demonstration

5.4. Section 3.4 — Training
   - Operations training for Terminal security staff
   - Maintenance training for Terminal maintenance staff
   - Training materials and documentation
   - Reference PKG-35 (Training & Handover) for training program

5.5. Section 3.5 — Closeout
   - As-built documentation (updated drawings, equipment lists)
   - Operations and maintenance manuals
   - Warranty documentation
   - Final acceptance and project closeout
   - Installation and test records (DEL-24.04)

**Outputs:**
- Part 3 (Execution) sections drafted

**Verification:** Self-check for completeness; verify testing requirements are testable

*Source: Specification.md — verification requirements; PKG-29, PKG-30, PKG-35 cross-references*

---

### Step 6: Technical Review and Revision

**Objective:** Internal technical review to verify specification quality and completeness.

**Activities:**
6.1. Self-review by specification writer
   - Verify all ER requirements addressed (check ER compliance matrix)
   - Verify all design requirements from DEL-24.01 addressed
   - Check for internal consistency (no conflicting requirements)
   - Verify all codes and standards referenced correctly
   - Check for completeness (no missing sections, no unresolved TBDs)

6.2. Discipline lead technical review
   - Review for technical accuracy and appropriateness
   - Verify requirements are clear, verifiable, and enforceable
   - Check for constructability and procurement practicality
   - Verify coordination with other specifications (PKG-17, PKG-23, PKG-25)

6.3. Incorporate review comments and revise specification
   - Address all technical review comments
   - Update ER compliance matrix if requirements change
   - Update specification document

**Outputs:**
- Reviewed and revised specification
- Technical review comment log with resolutions

**Verification:** Discipline lead sign-off on technical review

---

### Step 7: Interdisciplinary Review

**Objective:** Coordinate specification requirements with interface disciplines.

**Activities:**
7.1. Issue specification for interdisciplinary review
   - Distribute to PKG-17 (Electrical Power), PKG-23 (Fire Protection), PKG-25 (Communications & IT)
   - Request review of interface requirements (power, fire alarm integration, network)
   - Allow **TBD** — review period (typically 2 weeks)

7.2. Attend interdisciplinary coordination meetings
   - Discuss interface requirements and coordination needs
   - Resolve conflicts or inconsistencies
   - Document agreed coordination actions

7.3. Track and resolve interdisciplinary comments
   - Log all comments in coordination tracking log
   - Update specification to address comments
   - Obtain sign-off from commenting disciplines

**Outputs:**
- Interdisciplinary comment log with resolutions
- Updated specification incorporating coordination

**Verification:** Sign-offs from interface disciplines (PKG-17, PKG-23, PKG-25)

---

### Step 8: Constructability Review

**Objective:** Verify specification is practical and constructible.

**Activities:**
8.1. Construction/installation team review **TBD** — if applicable
   - Review for installation practicality and feasibility
   - Identify potential construction issues or conflicts
   - Provide input on installation methods and sequencing

8.2. Procurement review **TBD** — if applicable
   - Verify equipment is commercially available
   - Check lead times and delivery requirements
   - Identify potential procurement challenges

8.3. Incorporate constructability comments
   - Update specification to address practical installation concerns
   - Revise requirements if needed for constructability

**Outputs:**
- Constructability review comments and resolutions
- Updated specification

**Verification:** Constructability review sign-off

---

### Step 9: Employer Review and Acceptance

**Objective:** Obtain Employer review and acceptance of specification.

**Activities:**
9.1. Prepare specification for Employer review
   - Finalize specification document
   - Prepare transmittal package with ER compliance matrix and supporting documentation
   - Issue specification to Employer at **TBD** — design milestone (30%/60%/90%/IFC)

9.2. Employer review
   - Employer reviews specification for compliance with ER requirements
   - Employer provides comments and requests revisions
   - Coordination with Terminal IT/security operations for integration requirements **TBD**

9.3. Respond to Employer comments
   - Address all Employer comments with written responses
   - Revise specification as required
   - Resubmit for Employer acceptance if major changes

9.4. Obtain Employer acceptance
   - Employer provides formal acceptance of specification
   - Document acceptance in project records

**Outputs:**
- Employer-accepted specification
- Employer review comment log and responses
- Employer acceptance letter or sign-off

**Verification:** Employer acceptance obtained

---

### Step 10: Final Approval and Issuance

**Objective:** Final approval and issuance of specification for procurement and construction.

**Activities:**
10.1. Final specification review by discipline lead/approver
   - Verify all review comments addressed and closed
   - Verify Employer acceptance obtained
   - Verify specification is complete and ready for procurement/construction use
   - Approve specification for final issuance

10.2. Prepare specification for issuance
   - Generate final PDF and editable source file
   - Apply issue stamp and revision identifier per project standards **TBD**
   - Update document control records and specification register

10.3. Issue specification for construction (IFC)
   - Transmit specification to Employer and project team
   - Distribute to procurement and construction teams
   - File in project document management system
   - Archive in deliverable folder `3_Issued/DEL-24.02_YYYYMMDD_RevX/`

**Outputs:**
- Issued specification (PDF and source)
- Specification transmittal record
- Updated document control records

**Verification:**
- Discipline lead/approver sign-off obtained
- Employer acceptance on file
- Specification issued for construction (IFC status)

---

### Step 11: Revision Management (as required during project)

**Objective:** Manage specification revisions during procurement and construction.

**Activities:**
11.1. Receive revision request
   - Review change request or design change notice
   - Assess impact on specification requirements

11.2. Incorporate revisions
   - Update specification sections as required
   - Update ER compliance matrix if requirements change
   - Mark revisions clearly in document (revision bars, revision summary)

11.3. Repeat review and approval process (Steps 6-10) as appropriate
   - Scope of re-review depends on magnitude of change **TBD**
   - Minor changes: Technical review and discipline lead approval
   - Major changes: Full review cycle including Employer review

11.4. Issue revised specification
   - Follow Step 10 (Issuance) process
   - Clearly identify revision in transmittal (revision number/letter, description of changes)
   - Supersede previous version in document control system

**Outputs:**
- Revised specification
- Revision transmittal

**Verification:**
- Appropriate level of review completed
- Revisions properly documented and tracked

---

## Verification

### Verification Activities Summary

| Verification Activity | Responsible Party | Acceptance Criteria |
|-----------------------|-------------------|---------------------|
| **Design basis review** | Specifier + Design Team | Design requirements extracted from DEL-24.01 |
| **ER compliance verification** | Specifier + Discipline Lead | ER compliance matrix shows all requirements addressed |
| **Technical review** | Discipline Lead | Specification technically accurate, complete, and enforceable |
| **Interdisciplinary review** | Interface Disciplines | Interface requirements coordinated, sign-offs obtained |
| **Constructability review** | Construction/Procurement Team (TBD) | Specification practical and constructible |
| **Employer review** | Employer | Specification meets ER requirements, acceptance obtained |
| **Final approval** | Discipline Lead / Approver | Specification ready for procurement and construction use |

*Source: Specification.md — Verification section*

### Sign-off Requirements

**Specification sign-offs (typical format — TBD per project):**
- **Prepared by:** [Name], [Date] — Specification writer
- **Reviewed by:** [Name], [Date] — Discipline lead technical review
- **Approved by:** [Name], [Date] — Discipline lead or designated approver
- **Employer acceptance:** [Name], [Date] — Employer representative

**ASSUMPTION:** Sign-off protocol per project Quality Management Plan

### Completion Criteria

Specification is complete and ready for procurement/construction use when:
- ✓ All ER requirements addressed per compliance matrix
- ✓ All design requirements from DEL-24.01 incorporated
- ✓ All applicable codes and standards referenced and requirements incorporated
- ✓ Interdisciplinary coordination completed and signed off
- ✓ Constructability review completed (if applicable)
- ✓ Employer review and acceptance obtained
- ✓ Final approval obtained from discipline lead/approver
- ✓ Specification issued for construction (IFC status)
- ✓ Specification filed in project document management system and deliverable folder `3_Issued/`

*Source: Specification.md — Verification and Documentation sections*

## Records

### Documentation Outputs

**Primary deliverable:**
- **Security System Technical Specification** — comprehensive document (estimated 30-80 pages)
  - Part 1: General Requirements
  - Part 2: Products (CCTV specification, access control specification, network infrastructure)
  - Part 3: Execution (installation, testing, commissioning)

*Source: `_CONTEXT.md` — Anticipated Artifacts; Datasheet.md*

**Supporting documentation:**
- ER compliance matrix — requirements traceability
- Equipment requirements list extracted from DEL-24.01
- Interdisciplinary coordination log
- Review comment logs (technical, interdisciplinary, constructability, Employer)
- Employer acceptance letter or sign-off

### Record Management

**Filing locations:**
- **Working files (during development):** `1_Working/DEL-24.02_Security_System_Technical_Specification/`
- **Review files (during review):** `2_Checking/To/` → `2_Checking/From/`
- **Issued files (upon approval):** `3_Issued/DEL-24.02_YYYYMMDD_RevX/`

**File formats:**
- Source file: **TBD** — MS Word, SpecLink, or project-specified format
- Distribution file: PDF
- Compliance matrix: Excel or equivalent

**Retention requirements:**
- **TBD** — Per project records management plan
- **ASSUMPTION:** Electronic records in project document management system for project duration + **TBD** years post-completion

**Document control:**
- All transactions tracked in project document management system **TBD**
- Specification register maintained and current
- Superseded revisions archived and marked as superseded

*Source: Standard project document control and records management practices*

---

*Document status: Enriched draft — Pass 1*
*Enrichment date: 2026-01-28*
*Cross-references: Specification.md for requirements; Guidance.md for specification development principles; Datasheet.md for system attributes*
