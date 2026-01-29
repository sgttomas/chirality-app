# Specification: DEL-27.01 Design Basis Documents

## Scope

This specification defines the requirements for **Design Basis Documents** within **PKG-27 Engineering Design**.

**Purpose:** Documents analysis and results for design basis documents required for design verification and approvals (per _CONTEXT.md).

**Anticipated deliverable artifacts:**
1. Design Basis Memorandum
2. Design Criteria

**Scope Boundaries:**

**Included:**
- Establishment of design philosophy and technical approach for Phase 1 works
- Definition of performance requirements, design parameters, and criteria
- Identification of applicable codes, standards, and regulatory requirements
- Documentation of key technical decisions and assumptions
- Phase 2 expansion interface requirements and considerations (per OBJ-8)
- Design verification and approval requirements

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
- **Source:** Decomposition Section 1.1; **ASSUMPTION**: Comprehensive multi-discipline coverage required for Design & Build contract

**FR-2: Objective Alignment**
- Design basis shall demonstrate compliance with Project Objectives OBJ-1 through OBJ-10, with particular emphasis on:
  - OBJ-1: Safe & Reliable Operation
  - OBJ-2: Throughput Capacity (1,000,000 MT per annum)
  - OBJ-6: Regulatory Compliance
  - OBJ-8: Future Expandability (Phase 2)
- **Source:** Decomposition Section 2 (Project Objectives), Section 6 (Objective Mapping for PKG-27)

**FR-3: Design Criteria Definition**
- Design Criteria shall specify performance requirements, design loads, environmental conditions, and acceptance criteria for all major systems and components
- Criteria shall be traceable to Employer's Requirements and applicable codes/standards
- **Source:** **ASSUMPTION**: Standard Design & Build practice; Decomposition Section 3 (Reference Documents)

**FR-4: Phase 2 Expansion Provisions**
- Design basis shall identify Phase 2 expansion interfaces and ensure Phase 1 design accommodates future expansion with minimal disruption (per OBJ-8)
- **Source:** Decomposition Section 2 (OBJ-8), Section 6 (Objective Mapping); **ASSUMPTION**: Coordination with DEL-27.03

### Performance Requirements

**PR-1: Throughput Performance**
- Design basis shall establish criteria to achieve permitted capacity of 1,000,000 MT per annum (OBJ-2)
- **TBD** — Specific throughput rates, operating hours, availability requirements to be defined from Employer's Requirements
- **Source:** Decomposition Section 2 (OBJ-2)

**PR-2: Storage Performance**
- Design basis shall establish criteria for 45,000 MT storage capacity (3 × 15,000 MT tanks) (OBJ-3)
- **TBD** — Tank design parameters, inventory management requirements to be defined from Employer's Requirements
- **Source:** Decomposition Section 2 (OBJ-3), Section 1.1

**PR-3: Operational Flexibility**
- Design basis shall establish criteria to support both tank storage operations and direct rail-to-ship transfer (OBJ-4)
- **TBD** — Mode transition requirements, simultaneous operation capabilities to be defined
- **Source:** Decomposition Section 2 (OBJ-4)

**PR-4: Safety and Reliability**
- Design basis shall establish criteria for safe, efficient, reliable, and continuous operation (OBJ-1)
- Design shall incorporate hazard analysis results from DEL-27.02 (HAZOP Study Reports)
- **TBD** — Specific safety performance targets, reliability metrics to be defined from Employer's Requirements
- **Source:** Decomposition Section 2 (OBJ-1); **ASSUMPTION**: Coordination with DEL-27.02

### Interface Requirements

**IR-1: Multi-Discipline Coordination**
- Design basis shall define interface requirements between all disciplines (civil, structural, mechanical, electrical, controls, safety)
- **TBD** — Specific interface control requirements to be coordinated via project design coordination procedures
- **Source:** **ASSUMPTION**: Standard Design & Build coordination requirements; see `_DEPENDENCIES.md` (NOT_TRACKED)

**IR-2: Employer Interfaces**
- Design basis shall identify all interfaces with Employer-responsible items (permits, nitrogen skid supply, etc.)
- Interface requirements shall clearly delineate Contractor vs. Employer responsibilities per Decomposition Section 1.2
- **TBD** — Specific interface points to be defined from Employer's Requirements
- **Source:** Decomposition Section 1.2 (Scope Focus)

**IR-3: Existing Terminal Interfaces**
- Design basis shall address interfaces with existing Fraser Surrey Terminal facilities
- Design shall minimize disturbance to existing Terminal commercial activities (OBJ-5)
- **TBD** — Specific interface requirements to be coordinated with Terminal operations
- **Source:** Decomposition Section 2 (OBJ-5)

**IR-4: Phase 2 Expansion Interfaces**
- Design basis shall define Phase 2 expansion interfaces and design provisions
- Coordinate with DEL-27.03 (Phase 2 Expansion Documentation)
- **TBD** — Specific Phase 2 interface requirements to be defined
- **Source:** Decomposition Section 2 (OBJ-8); **ASSUMPTION**: Coordination with DEL-27.03

### Quality Requirements

**QR-1: Quality Management**
- All design basis documents shall comply with ISO 9001 and project Quality Management Plan
- Document control, revision management, and approval workflows per project procedures
- **TBD** — Specific project quality procedures to be referenced
- **Source:** Datasheet.md; **ASSUMPTION**: ISO 9001 compliance required for Design & Build

**QR-2: Design Verification**
- Design basis shall be subject to independent design verification per DEL-28.01
- Verification scope and criteria to be defined in coordination with verification requirements
- **TBD** — Specific verification requirements to be coordinated with DEL-28.01
- **Source:** **ASSUMPTION**: Coordination with DEL-28.01 (Independent Design Verification Reports)

**QR-3: Submission Requirements**
- Design basis shall be submitted at 30%, 60%, 90%, and IFC stages per DEL-27.04
- Submission format and content requirements per project design submission procedures
- **TBD** — Specific submission requirements to be coordinated with DEL-27.04
- **Source:** Datasheet.md; **ASSUMPTION**: Standard Design & Build submission stages

### Regulatory and Code Compliance

**RC-1: Regulatory Compliance**
- Design basis shall ensure compliance with all applicable permits, codes, and authority requirements (OBJ-6)
- **TBD** — Specific regulatory requirements to be identified from Employer's Requirements and permit conditions
- **Source:** Decomposition Section 2 (OBJ-6)

**RC-2: Environmental Compliance**
- Design basis shall establish criteria for adequate containment, spill prevention, and environmental controls (OBJ-7)
- **TBD** — Specific environmental requirements to be defined from permits and regulations
- **Source:** Decomposition Section 2 (OBJ-7)

**RC-3: Code and Standard Application**
- Design basis shall identify and apply all applicable Canadian codes and standards, including but not limited to:
  - National Building Code of Canada (NBC/NBCC)
  - CSA standards (discipline-specific)
  - **TBD** — Additional applicable codes/standards to be identified
- **Source:** Datasheet.md; **ASSUMPTION**: Canadian codes apply for BC location

## Standards

**Applicable codes and standards:**

**General:**
- ISO 9001: Quality Management Systems
- Employer's Requirements (project-specific requirements)

**Building and Structural:**
- National Building Code of Canada (NBC/NBCC) — **location TBD**
- CSA S16: Design of Steel Structures — **location TBD**
- CSA A23.3: Design of Concrete Structures — **location TBD**
- **TBD** — Additional structural codes as applicable

**Civil and Site:**
- **TBD** — Canadian civil engineering standards as applicable

**Mechanical and Process:**
- **TBD** — CSA mechanical and pressure equipment standards as applicable

**Electrical:**
- Canadian Electrical Code (CEC) — **location TBD**
- **TBD** — Additional electrical codes as applicable

**Safety:**
- **TBD** — Applicable safety codes and standards (to be informed by DEL-27.02 HAZOP results)

**Source:** Datasheet.md; **ASSUMPTION**: Standard Canadian codes apply; **location TBD** for all reference standards

## Verification

**Verification methods for Design Basis Documents:**

**VM-1: Technical Review**
- Design basis methodology and approach shall be reviewed for technical adequacy
- Review shall verify alignment with project objectives and Employer's Requirements
- **TBD** — Specific review procedures and checklist

**VM-2: Multi-Discipline Review**
- Design criteria shall be reviewed by all applicable discipline leads
- Review shall verify completeness, consistency, and adequacy of criteria
- **TBD** — Discipline review requirements and sign-off protocol

**VM-3: Independent Design Verification**
- Design basis shall undergo independent design verification per DEL-28.01
- Verification shall be performed by qualified personnel independent of design team
- **TBD** — Specific IDV procedures to be coordinated with DEL-28.01

**VM-4: Employer Review and Approval**
- Design basis shall be submitted to Employer at required submission stages (30%, 60%, 90%, IFC)
- Employer comments shall be addressed and incorporated
- **TBD** — Employer review and approval procedures

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
1. **Design Basis Memorandum**
2. **Design Criteria**

**Documentation structure and content:**

**Design Basis Memorandum (typical sections):**
- Executive summary
- Project overview and scope
- Design philosophy and technical approach
- Key technical decisions and rationale
- Code and standard selection
- Interface requirements (internal and external)
- Phase 2 expansion considerations
- Assumptions and exclusions
- Glossary and definitions
- **TBD** — Detailed table of contents to be developed per project template

**Design Criteria (typical sections):**
- Introduction and scope
- Performance requirements
- Design loads and environmental conditions
- Material specifications and standards
- Structural design criteria
- Mechanical and process design criteria
- Electrical and controls design criteria
- Safety and fire protection criteria
- Quality assurance requirements
- Code and standard references
- **TBD** — Detailed table of contents to be developed per project template

**Documentation requirements:**
- Format: **TBD** — PDF and native format per project document standards
- Revision control per project document numbering system — **TBD**
- All documents shall include:
  - Title page with project identification
  - Revision history and approval signatures
  - Table of contents
  - Page numbers and document control information
- Document management per project document control procedures
- Submission at 30%, 60%, 90%, IFC stages per DEL-27.04
- Filing: Working versions in `1_Working/`, review copies in `2_Checking/`, issued versions in `3_Issued/`

**Source:** _CONTEXT.md; **ASSUMPTION**: Standard Design & Build documentation requirements
