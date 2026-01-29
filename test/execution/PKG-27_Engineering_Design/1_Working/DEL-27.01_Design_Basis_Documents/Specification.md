# Specification: DEL-27.01 Design Basis Documents

## Scope

This specification defines the requirements for **Design Basis Documents** within **PKG-27 Engineering Design**.

**Purpose:** Documents analysis and results for design basis documents required for design verification and approvals (per _CONTEXT.md).

**Anticipated deliverable artifacts:**
1. Design Basis Memorandum (see Datasheet § Construction; Guidance § Examples §4; Procedure Step 3.1)
2. Design Criteria (see Datasheet § Construction; Guidance § Examples §1-3; Procedure Step 3.2)

**Scope Boundaries:**

**Included:**
- Establishment of design philosophy and technical approach for Phase 1 works (see Guidance § Principles §1)
- Definition of performance requirements, design parameters, and criteria (see Guidance § Principles §5)
- Identification of applicable codes, standards, and regulatory requirements (see Guidance § Principles §4)
- Documentation of key technical decisions and assumptions (see Guidance § Trade-offs)
- Phase 2 expansion interface requirements and considerations per OBJ-8 (see Guidance § Principles §7)
- Design verification and approval requirements (see Guidance § Considerations)

**Excluded:**
- Detailed discipline-specific design calculations (covered in respective package deliverables)
- Construction methodology and sequencing (covered in construction planning deliverables)
- Employer-responsible items except for interface requirements (per Decomposition Section 1.2)

**Source:** _CONTEXT.md; Decomposition DEL-27.01 entry, Section 1.2 (Scope Focus)

## Requirements

### Functional Requirements

**FR-1: Design Basis Establishment**
- The Design Basis Documents shall establish the foundation for all engineering design work for Phase 1 of the Canola Oil Transload Facility
- Design basis shall address all discipline areas: civil, structural, mechanical, electrical, control systems, and safety systems
- **Guidance §:** Principles §1, §3 (Foundation for Integrated Design, Multi-Discipline Integration)
- **Procedure Step:** Step 1.1, Step 2.2 (Requirements Review, Multi-Discipline Workshops)
- **Verification:** VM-1 (Technical Review), VM-2 (Multi-Discipline Review)
- **Source:** Decomposition Section 1.1; **ASSUMPTION**: Comprehensive multi-discipline coverage required for Design & Build contract

**FR-2: Objective Alignment**
- Design basis shall demonstrate compliance with Project Objectives OBJ-1 through OBJ-10, with particular emphasis on:
  - OBJ-1: Safe & Reliable Operation (see Guidance § Principles §8)
  - OBJ-2: Throughput Capacity (1,000,000 MT per annum) (see Guidance § Principles §5)
  - OBJ-6: Regulatory Compliance (see Guidance § Principles §4)
  - OBJ-8: Future Expandability (Phase 2) (see Guidance § Principles §7)
- **Guidance §:** Principles §2 (Objective-Driven Design)
- **Procedure Step:** Step 3.1 (Content development guidance)
- **Verification:** VM-1 (Review against project objectives)
- **Source:** Decomposition Section 2 (Project Objectives), Section 6 (Objective Mapping for PKG-27)

**FR-3: Design Criteria Definition**
- Design Criteria shall specify performance requirements, design loads, environmental conditions, and acceptance criteria for all major systems and components
- Criteria shall be traceable to Employer's Requirements and applicable codes/standards
- **Guidance §:** Principles §5, §6 (Performance-Based Criteria, Worst-Case Design Envelope)
- **Procedure Step:** Step 2.3, Step 3.2 (Design Criteria Calculations, Design Criteria Preparation)
- **Verification:** V-1 (Requirements Traceability), V-3 (Code/Standard Compliance)
- **Source:** **ASSUMPTION**: Standard Design & Build practice; Decomposition Section 3 (Reference Documents)

**FR-4: Phase 2 Expansion Provisions**
- Design basis shall identify Phase 2 expansion interfaces and ensure Phase 1 design accommodates future expansion with minimal disruption per OBJ-8
- **Guidance §:** Principles §7 (Phase 2 Future-Proofing); Trade-offs §2
- **Procedure Step:** Step 2.2 (Workshop topics - Phase 2 provisions)
- **Verification:** VM-1, VM-2 (Review against Phase 2 requirements)
- **Cross-Reference:** Coordination with DEL-27.03
- **Source:** Decomposition Section 2 (OBJ-8), Section 6 (Objective Mapping); **ASSUMPTION**: Coordination with DEL-27.03

### Performance Requirements

**PR-1: Throughput Performance**
- Design basis shall establish criteria to achieve permitted capacity of 1,000,000 MT per annum (OBJ-2)
- **TBD** — Specific throughput rates, operating hours, availability requirements to be defined from Employer's Requirements
- **Datasheet §:** Conditions (Permitted Throughput)
- **Guidance §:** Principles §5; Considerations (Operational); Examples §1
- **Procedure Step:** Step 2.2 (Performance requirements workshop topic)
- **Verification:** V-1 (Requirements Traceability)
- **Source:** Decomposition Section 2 (OBJ-2)

**PR-2: Storage Performance**
- Design basis shall establish criteria for 45,000 MT storage capacity (3 × 15,000 MT tanks) (OBJ-3)
- **TBD** — Tank design parameters, inventory management requirements to be defined from Employer's Requirements
- **Datasheet §:** Conditions (Storage Capacity)
- **Guidance §:** Examples §1 (Tank Storage Design Criteria)
- **Procedure Step:** Step 2.2 (Workshop topics), Step 3.2 (Design Criteria)
- **Verification:** V-1, V-2 (Multi-Discipline Consistency)
- **Source:** Decomposition Section 2 (OBJ-3), Section 1.1

**PR-3: Operational Flexibility**
- Design basis shall establish criteria to support both tank storage operations and direct rail-to-ship transfer (OBJ-4)
- **TBD** — Mode transition requirements, simultaneous operation capabilities to be defined
- **Datasheet §:** Conditions (Railcar Capacity)
- **Guidance §:** Considerations (Operational)
- **Procedure Step:** Step 2.2 (Dual operating modes workshop topic)
- **Verification:** V-1
- **Source:** Decomposition Section 2 (OBJ-4)

**PR-4: Safety and Reliability**
- Design basis shall establish criteria for safe, efficient, reliable, and continuous operation (OBJ-1)
- Design shall incorporate hazard analysis results from DEL-27.02 (HAZOP Study Reports)
- **TBD** — Specific safety performance targets, reliability metrics to be defined from Employer's Requirements
- **Datasheet §:** Conditions (Hazardous area classification)
- **Guidance §:** Principles §8, §9 (Inherent Safety, Environmental Protection)
- **Procedure Step:** Step 2.2 (Safety requirements workshop topic)
- **Verification:** V-4 (IDV)
- **Cross-Reference:** DEL-27.02
- **Source:** Decomposition Section 2 (OBJ-1); **ASSUMPTION**: Coordination with DEL-27.02

### Interface Requirements

**IR-1: Multi-Discipline Coordination**
- Design basis shall define interface requirements between all disciplines (civil, structural, mechanical, electrical, controls, safety)
- **TBD** — Specific interface control requirements to be coordinated via project design coordination procedures
- **Guidance §:** Principles §3 (Multi-Discipline Integration); Considerations (Multi-Discipline Coordination)
- **Procedure Step:** Step 2.2 (Interface requirements matrix)
- **Verification:** V-2 (Multi-Discipline Consistency)
- **Source:** **ASSUMPTION**: Standard Design & Build coordination requirements; see `_DEPENDENCIES.md` (NOT_TRACKED)

**IR-2: Employer Interfaces**
- Design basis shall identify all interfaces with Employer-responsible items (permits, nitrogen skid supply, etc.)
- Interface requirements shall clearly delineate Contractor vs. Employer responsibilities per Decomposition Section 1.2
- **TBD** — Specific interface points to be defined from Employer's Requirements
- **Guidance §:** Considerations (Regulatory and Compliance - Permit Requirements)
- **Procedure Step:** Step 1.1 (Identify applicable regulations and permits)
- **Verification:** V-5 (Employer Review)
- **Source:** Decomposition Section 1.2 (Scope Focus)

**IR-3: Existing Terminal Interfaces**
- Design basis shall address interfaces with existing Fraser Surrey Terminal facilities
- Design shall minimize disturbance to existing Terminal commercial activities (OBJ-5)
- **TBD** — Specific interface requirements to be coordinated with Terminal operations
- **Guidance §:** Considerations (Location-Specific - Existing terminal operations)
- **Procedure Step:** Step 2.1 (Existing Terminal as-built documentation)
- **Verification:** V-2, V-5
- **Source:** Decomposition Section 2 (OBJ-5)

**IR-4: Phase 2 Expansion Interfaces**
- Design basis shall define Phase 2 expansion interfaces and design provisions
- **TBD** — Specific Phase 2 interface requirements to be defined
- **Guidance §:** Principles §7; Trade-offs §2 (Phase 2 Provisions)
- **Procedure Step:** Step 2.2 (Phase 2 expansion provisions workshop topic)
- **Verification:** VM-1, V-2
- **Cross-Reference:** Coordinate with DEL-27.03 (Phase 2 Expansion Documentation)
- **Source:** Decomposition Section 2 (OBJ-8); **ASSUMPTION**: Coordination with DEL-27.03

### Quality Requirements

**QR-1: Quality Management**
- All design basis documents shall comply with ISO 9001 and project Quality Management Plan
- Document control, revision management, and approval workflows per project procedures
- **TBD** — Specific project quality procedures to be referenced
- **Datasheet §:** Attributes (Revision Control)
- **Guidance §:** Considerations (Lessons Learned §2, §3)
- **Procedure Step:** Step 4.3 (Quality check), Step 5.1 (Internal approval)
- **Verification:** V-4, V-5 (Quality sign-offs)
- **Source:** Datasheet.md; **ASSUMPTION**: ISO 9001 compliance required for Design & Build

**QR-2: Design Verification**
- Design basis shall be subject to independent design verification per DEL-28.01
- Verification scope and criteria to be defined in coordination with verification requirements
- **TBD** — Specific verification requirements to be coordinated with DEL-28.01
- **Datasheet §:** References (Cross-References)
- **Guidance §:** Considerations (IDV)
- **Procedure Step:** Verification § V-4 (IDV)
- **Verification:** V-4
- **Cross-Reference:** DEL-28.01 (Independent Design Verification Reports)
- **Source:** **ASSUMPTION**: Coordination with DEL-28.01

**QR-3: Submission Requirements**
- Design basis shall be submitted at 30%, 60%, 90%, and IFC stages per DEL-27.04
- Submission format and content requirements per project design submission procedures
- **TBD** — Specific submission requirements to be coordinated with DEL-27.04
- **Datasheet §:** Attributes (Submission Stages)
- **Guidance §:** Considerations (Design Submission)
- **Procedure Step:** Step 5.2 (Submission to Employer)
- **Verification:** V-5 (Employer Review)
- **Cross-Reference:** DEL-27.04
- **Source:** Datasheet.md; **ASSUMPTION**: Standard Design & Build submission stages

### Regulatory and Code Compliance

**RC-1: Regulatory Compliance**
- Design basis shall ensure compliance with all applicable permits, codes, and authority requirements (OBJ-6)
- **TBD** — Specific regulatory requirements to be identified from Employer's Requirements and permit conditions
- **Guidance §:** Principles §4; Considerations (Authority Having Jurisdiction)
- **Procedure Step:** Step 1.1 (Identify regulations and permits)
- **Verification:** V-3, V-5
- **Source:** Decomposition Section 2 (OBJ-6)

**RC-2: Environmental Compliance**
- Design basis shall establish criteria for adequate containment, spill prevention, and environmental controls (OBJ-7)
- **TBD** — Specific environmental requirements to be defined from permits and regulations
- **Guidance §:** Principles §9; Trade-offs §6 (Environmental Protection Level)
- **Procedure Step:** Step 2.2 (Environmental conditions workshop topic)
- **Verification:** V-3
- **Source:** Decomposition Section 2 (OBJ-7)

**RC-3: Code and Standard Application**
- Design basis shall identify and apply all applicable Canadian codes and standards, including but not limited to:
  - National Building Code of Canada (NBC/NBCC)
  - CSA standards (discipline-specific)
  - **TBD** — Additional applicable codes/standards to be identified
- **Datasheet §:** References (Applicable Standards)
- **Guidance §:** Principles §4; Trade-offs §3, §4 (Code Selection/Application)
- **Procedure Step:** Step 2.2 (Code selection workshop topic)
- **Verification:** V-3 (Code and Standard Compliance)
- **Source:** Datasheet.md; **ASSUMPTION**: Canadian codes apply for BC location

## Standards

**Applicable codes and standards:**

**General:**

| Standard | Description | Status | Requirement § |
|----------|-------------|--------|---------------|
| ISO 9001 | Quality Management Systems | Applicable | QR-1 |
| Employer's Requirements | Project-specific requirements | **location TBD** | All |

**Building and Structural:**

| Standard | Description | Status | Requirement § |
|----------|-------------|--------|---------------|
| NBC/NBCC | National Building Code of Canada | **location TBD** | RC-3 |
| CSA S16 | Design of Steel Structures | **location TBD** | RC-3 |
| CSA A23.3 | Design of Concrete Structures | **location TBD** | RC-3 |
| **TBD** | Additional structural codes as applicable | To be identified | RC-3 |

**Civil and Site:**

| Standard | Description | Status | Requirement § |
|----------|-------------|--------|---------------|
| **TBD** | Canadian civil engineering standards as applicable | To be identified | RC-3 |

**Mechanical and Process:**

| Standard | Description | Status | Requirement § |
|----------|-------------|--------|---------------|
| **TBD** | CSA mechanical and pressure equipment standards as applicable | To be identified | RC-3 |
| API 650 | Welded Tanks for Oil Storage (or equivalent) | **location TBD** | PR-2 |

**Electrical:**

| Standard | Description | Status | Requirement § |
|----------|-------------|--------|---------------|
| CEC | Canadian Electrical Code | **location TBD** | RC-3 |
| **TBD** | Additional electrical codes as applicable | To be identified | RC-3 |

**Safety:**

| Standard | Description | Status | Requirement § |
|----------|-------------|--------|---------------|
| **TBD** | Applicable safety codes and standards | To be informed by DEL-27.02 HAZOP results | PR-4, RC-1 |

**Source:** Datasheet.md; **ASSUMPTION**: Standard Canadian codes apply; **location TBD** for all reference standards

## Verification

**Verification methods for Design Basis Documents:**

| Verification ID | Method | Requirements Verified | Procedure Step | Acceptance Criteria |
|-----------------|--------|----------------------|----------------|---------------------|
| VM-1 | Technical Review | FR-1, FR-2, FR-3, FR-4 | Step 3.3, Step 4.1 | Technical adequacy, alignment with objectives |
| VM-2 | Multi-Discipline Review | FR-1, IR-1, PR-2, PR-3 | Step 3.3 | Completeness, consistency across disciplines |
| VM-3 | Independent Design Verification | All requirements | Step 5 (via V-4) | Per DEL-28.01 criteria |
| VM-4 | Employer Review and Approval | All requirements | Step 5.2, Step 5.3 | Employer acceptance |

**VM-1: Technical Review**
- Design basis methodology and approach shall be reviewed for technical adequacy
- Review shall verify alignment with project objectives and Employer's Requirements
- **TBD** — Specific review procedures and checklist
- **Guidance §:** Considerations (Lessons Learned §1 - Early Stakeholder Alignment)
- **Procedure Step:** Step 3.3 (Internal Technical Review)

**VM-2: Multi-Discipline Review**
- Design criteria shall be reviewed by all applicable discipline leads
- Review shall verify completeness, consistency, and adequacy of criteria
- **TBD** — Discipline review requirements and sign-off protocol
- **Guidance §:** Principles §3; Considerations (Multi-Discipline Coordination)
- **Procedure Step:** Step 3.3 (Review checklist)

**VM-3: Independent Design Verification**
- Design basis shall undergo independent design verification per DEL-28.01
- Verification shall be performed by qualified personnel independent of design team
- **TBD** — Specific IDV procedures to be coordinated with DEL-28.01
- **Guidance §:** Considerations (IDV)
- **Procedure Step:** Verification § V-4

**VM-4: Employer Review and Approval**
- Design basis shall be submitted to Employer at required submission stages (30%, 60%, 90%, IFC)
- Employer comments shall be addressed and incorporated
- **TBD** — Employer review and approval procedures
- **Guidance §:** Considerations (Comment Resolution)
- **Procedure Step:** Step 5.2, Step 5.3

**Acceptance criteria:**
- Design basis demonstrates compliance with all Project Objectives (OBJ-1 through OBJ-10)
- Design criteria are complete, consistent, and traceable to requirements
- All applicable codes and standards are identified and properly applied
- All discipline interfaces are identified and addressed
- Phase 2 expansion provisions are adequately documented
- All Employer comments are satisfactorily addressed
- Independent design verification findings are resolved
- **TBD** — Additional project-specific acceptance criteria from quality procedures

**Source:** **ASSUMPTION**: Standard Design & Build verification approach; Datasheet.md (submission stages)

## Documentation

**Required documentation outputs:**

Per _CONTEXT.md and Decomposition DEL-27.01:
1. **Design Basis Memorandum** (see Datasheet § Construction; Guidance § Examples §4; Procedure Step 3.1)
2. **Design Criteria** (see Datasheet § Construction; Guidance § Examples §1-3; Procedure Step 3.2)

**Documentation structure and content:**

**Design Basis Memorandum (typical sections):**
- Executive summary
- Project overview and scope (see Scope section above)
- Design philosophy and technical approach (see Guidance § Principles)
- Key technical decisions and rationale (see Guidance § Trade-offs)
- Code and standard selection (see Standards section above)
- Interface requirements (see IR-1 through IR-4 above)
- Phase 2 expansion considerations (see FR-4, IR-4 above; Guidance § Principles §7)
- Assumptions and exclusions (see Guidance § Considerations)
- Glossary and definitions
- **TBD** — Detailed table of contents to be developed per project template

**Design Criteria (typical sections):**
- Introduction and scope
- Performance requirements (see PR-1 through PR-4 above)
- Design loads and environmental conditions (see Guidance § Examples §3)
- Material specifications and standards (see Standards above)
- Structural design criteria (see Guidance § Considerations)
- Mechanical and process design criteria (see Guidance § Examples §1, §2)
- Electrical and controls design criteria
- Safety and fire protection criteria (see PR-4; Guidance § Principles §8)
- Quality assurance requirements (see QR-1 through QR-3)
- Code and standard references (see Standards above)
- **TBD** — Detailed table of contents to be developed per project template

**Documentation requirements:**
- Format: **TBD** — PDF and native format per project document standards
- Revision control per project document numbering system — **TBD**
- All documents shall include:
  - Title page with project identification
  - Revision history and approval signatures (see Procedure Step 4.3)
  - Table of contents
  - Page numbers and document control information
- Document management per project document control procedures (see Procedure § Records)
- Submission at 30%, 60%, 90%, IFC stages per DEL-27.04 (see Procedure Step 5.2)
- Filing: Working versions in `1_Working/`, review copies in `2_Checking/`, issued versions in `3_Issued/` (see Procedure § Records)

**Source:** _CONTEXT.md; **ASSUMPTION**: Standard Design & Build documentation requirements

---

**Cross-Document Verification (Pass 3):**
- All requirements linked to Guidance § for rationale
- All requirements linked to Procedure Step for verification method
- All requirements linked to Datasheet § where applicable
- Terminology verified consistent with Datasheet.md, Guidance.md, Procedure.md
- Project parameters verified consistent: 1,000,000 MT/annum (OBJ-2), 45,000 MT storage (OBJ-3), 32 railcar stations
- Cross-references to DEL-27.02, DEL-27.03, DEL-27.04, DEL-28.01 verified consistent across all documents
