# Specification: DEL-25.01 Communications Design Drawing Set

## Scope

This specification defines the requirements for **Communications Design Drawing Set** within **PKG-25 Communications & IT**.

**Purpose:** Defines the design arrangement and details for communications per ER requirements.

**Source:** `_CONTEXT.md` Description; Decomposition Table PKG-25 DEL-25.01

**Anticipated deliverable artifacts:**
- Fiber network layout
- Communications distribution drawings
- Patch panel locations

**Source:** Decomposition Table PKG-25 DEL-25.01

**Package Scope Context:**

PKG-25 covers:
- Communications network
- Fiber infrastructure
- Patch panels
- Workstation connectivity

**Source:** Decomposition Section 5 PKG-25 (Scope)

**Interface Boundaries:**

Per DEC-05 (Decomposition Section 7): "Terminal network interfaces treated as multiple distinct systems — CCTV, access control, communications are separate systems with distinct interfaces."

**Inclusions:**
- Data network infrastructure for facility operations
- Voice communications infrastructure (if applicable)
- Fiber optic backbone network
- Structured cabling for workstations and control systems
- Patch panel and network equipment locations

**Exclusions:**
- CCTV network (see PKG-24 Security Systems)
- Access control network (see PKG-24 Security Systems)
- Control system networks/fieldbus (see PKG-19 Control Systems) — coordination required for integration points

**Source:** Decomposition Section 7 DEC-05; inference from PKG-25 scope and related packages

## Requirements

### Functional Requirements

**Drawing Content Requirements:**

1. **Fiber Network Layout:**
   - Show fiber optic cable routing throughout facility
   - Indicate fiber termination points
   - Show splice locations and fiber distribution frames
   - Identify fiber types (single-mode, multi-mode) and fiber counts
   - **TBD** — Specific routing corridors and pathways

2. **Communications Distribution Drawings:**
   - Show structured cabling distribution (horizontal and vertical)
   - Indicate telecommunications rooms (TRs) and equipment room (ER) locations
   - Show cable pathways (trays, conduits, sleeves)
   - Identify cable types and pathway fill capacities
   - **TBD** — Building-specific distribution details

3. **Patch Panel Locations:**
   - Show rack elevations with patch panel assignments
   - Indicate port assignments and labeling scheme
   - Show cable management details
   - **TBD** — Specific rack layouts per location

**Source:** Inference from anticipated artifacts (Decomposition Table PKG-25 DEL-25.01) and typical structured cabling design practice

**Drawing Set Organization:**

- Drawings shall be organized logically by area or system
- Index drawing required listing all drawings in set
- Key plans and legends required for multi-drawing sets
- **TBD** — Specific drawing numbering scheme per project standards

**Source:** **ASSUMPTION** — Standard engineering drawing set practice

### Performance Requirements

**Design Criteria:**

- Network topology: **TBD** — Star, ring, mesh, or hybrid per system requirements
- Cable performance ratings: Per DEL-25.02 specification
- Bandwidth/capacity requirements: **TBD** — Based on operational needs and future expandability (OBJ-8)
- Redundancy requirements: **TBD** — Based on reliability objectives (OBJ-1)
- Physical layer performance: **TBD** — Per TIA-568 or equivalent standards

**Source:** Cross-reference to DEL-25.02; **ASSUMPTION** of industry standards; Decomposition Section 2 (OBJ-1, OBJ-8)

**Pathway Capacity:**

- Cable tray/conduit fill: **TBD** — Per NEC/CSA requirements with future growth allowance
- Separation from power/EMI sources: **TBD** — Per TIA-569 and electrical code requirements
- Physical protection: **TBD** — Per exposure and hazard classification

**Source:** **ASSUMPTION** — Industry standard practice; **TBD** pending specific project requirements

### Interface Requirements

**Coordination Required With:**

- PKG-17 Electrical Power Distribution — Power supply to communications equipment
- PKG-18 Lighting — Shared cable pathways, coordination in equipment rooms
- PKG-19 Control Systems — Network integration points for SCADA/control data
- PKG-20 Field Instrumentation — Potential network-connected instruments
- PKG-21 Building Structures & Envelope — Penetrations, sleeves, pathway supports
- PKG-22 Building Interior & MEP — Equipment room layout, HVAC for equipment cooling
- PKG-24 Security Systems — Separation per DEC-05; potential shared infrastructure
- PKG-29 Testing — Network testing and acceptance criteria
- PKG-30 Commissioning — System integration and functional testing

**Source:** Inference from typical communications infrastructure dependencies; DEC-05 (Decomposition Section 7)

**Interface Documentation:**

- Interface points to be clearly identified on drawings
- Coordination drawings required where multiple disciplines converge
- **TBD** — Interface control documentation requirements

**Source:** **ASSUMPTION** — Standard engineering coordination practice

### Quality Requirements

**Drawing Quality Standards:**

- All drawings shall comply with project CAD standards: **TBD**
- Drawing accuracy: **TBD** — Tolerance requirements for location dimensions
- Clarity and legibility: Line weights, text sizes, and symbols per CAD manual
- Completeness: All required views, details, sections, and notes provided
- Drawing checking: See Procedure.md for checking and approval workflow

**Source:** **ASSUMPTION** — Standard engineering drawing requirements

**Documentation Quality:**

- All work shall comply with the project Quality Management Plan
- Drawing reviews shall be conducted per project quality procedures
- Comments and revisions shall be tracked and dispositioned
- **TBD** — Specific QA/QC hold points and approval authorities

**Source:** General project quality requirement; **TBD** for specific procedures

## Standards

**Applicable Codes and Standards:**

**Telecommunications Standards:**
- **ASSUMPTION**: TIA-568 (Commercial Building Telecommunications Cabling Standard)
- **ASSUMPTION**: TIA-569 (Telecommunications Pathways and Spaces)
- **ASSUMPTION**: TIA-606 (Administration Standard for Telecommunications Infrastructure)
- **ASSUMPTION**: TIA-607 (Generic Telecommunications Bonding and Grounding)
- **TBD** — ISO/IEC 11801 or other international standards if applicable

**Electrical and Safety Standards:**
- **ASSUMPTION**: CSA C22.1 (Canadian Electrical Code) or NEC Article 770 (Optical Fiber Cables and Raceways)
- **ASSUMPTION**: CSA C22.2 or UL listing for communications equipment
- Alberta OHS Code
- CSA Z462 (Electrical Safety in the Workplace)

**Building and Fire Protection:**
- **ASSUMPTION**: National Building Code of Canada (NBCC)
- **ASSUMPTION**: CAN/ULC-S102 (Plenum cable fire rating)
- **TBD** — Fire stopping and firestopping requirements for cable penetrations

**Project-Specific Requirements:**
- Employer's Requirements: **TBD** — Specific sections related to communications to be identified
- **TBD** — Project Design Criteria (if issued)
- **TBD** — Project CAD Manual and drawing standards

**Source:** **ASSUMPTION** for industry standards; **TBD** for project-specific documents not yet indexed

**Standard Application Notes:**

- Latest edition of standards in effect at time of design unless otherwise specified
- Where conflicts exist between standards, resolution required per project procedures
- Deviations from standards require engineering justification and approval

**Source:** **ASSUMPTION** — Standard engineering practice

## Verification

**Verification Methods for Drawing Deliverables:**

1. **Design Review (Peer Check):**
   - Independent review by qualified checker
   - Technical accuracy and completeness verification
   - Code and standards compliance check
   - **TBD** — Checker qualification requirements

2. **Dimensional Verification:**
   - Coordination with architectural and civil drawings for locations
   - Interference checking (clash detection if 3D model available)
   - **TBD** — Dimensional tolerance verification methods

3. **Interdisciplinary Check (IDC):**
   - Coordination review with interfacing disciplines
   - Interface point verification
   - **TBD** — IDC meeting schedule and participants

4. **CAD Standards Compliance Check:**
   - Layer usage, line weights, text styles
   - Title block and drawing border compliance
   - File naming and organization
   - **TBD** — CAD checking tools or procedures

**Source:** **ASSUMPTION** — Standard engineering drawing verification practice; See Procedure.md

**Acceptance Criteria:**

Per the verification workflow defined in Procedure.md Steps 6-9:
- All design review comments resolved and closed (Step 8)
- Drawings checked and approved by discipline lead (Step 9)
- No unresolved interdisciplinary conflicts (Step 7 IDC complete)
- Compliance with project CAD standards verified (Steps 5-6, 8)
- All verification records complete per Procedure.md Verification section
- **TBD** — Employer review and acceptance requirements (Step 10)
- **TBD** — Regulatory authority approvals (if required for drawings)

**Source:** **ASSUMPTION** — Standard acceptance criteria; Cross-reference to Procedure.md workflow; **TBD** for project-specific approvals

**Verification Records:**

- Design review checklists completed
- Checker comments and resolutions documented
- Approval signatures per project procedures
- **TBD** — Records location and retention requirements

**Source:** **ASSUMPTION** — Standard QA/QC practice

## Documentation

**Required Documentation Outputs:**

Per Decomposition Table PKG-25 DEL-25.01:
- Fiber network layout
- Communications distribution drawings
- Patch panel locations

**Supporting Documentation:**

- Drawing index / list of drawings
- Legend and symbol sheets
- General notes sheets
- Design basis memorandum: **TBD** — Requirements for design rationale documentation
- Calculation sheets (if applicable): **TBD**
- **TBD** — As-built drawing requirements (post-construction)

**Source:** Decomposition Table PKG-25 DEL-25.01; **ASSUMPTION** for supporting documentation

**Documentation Requirements:**

**Format and Media:**
- Electronic format: **TBD** — PDF, DWG, or other formats per project EDMS requirements
- Plot size and scale: Per Datasheet.md attributes
- Revision control: Per project document numbering system — **TBD**
- **ASSUMPTION**: All documents submitted through project document management system

**Submittal Requirements:**
- **TBD** — Submittal schedule and milestones (30%, 60%, 90%, IFC, etc.)
- **TBD** — Number of copies and distribution list
- **TBD** — Review and approval workflow

**File Management:**
- CAD files: **TBD** — Native file format and version requirements
- Reference files and x-refs: **TBD** — File organization and management
- Archive and backup: **TBD** — Project archive requirements

**Source:** **ASSUMPTION** for standard practices; **TBD** for project-specific requirements

**Cross-Reference to Related Deliverables:**

- DEL-25.02 Communications Technical Specification — Performance and material requirements inform drawing content
- DEL-25.03 Communications Data Sheet Package — Equipment data informs patch panel layouts and equipment room arrangements
- DEL-25.04 Communications Installation & Test Records — Test requirements inform drawing details and acceptance criteria
- See Datasheet.md References section for additional cross-references

**Source:** Logical relationship between PKG-25 deliverables

---

## Cross-Document Consistency Check

**This section verifies alignment between the four documents for DEL-25.01:**

| Requirement/Entity | Datasheet | Specification | Guidance | Procedure |
|-------------------|-----------|---------------|----------|-----------|
| Fiber network layout | Construction | Functional Req. 1 | Examples | Step 2 |
| Communications distribution | Construction | Functional Req. 2 | Examples | Step 3 |
| Patch panel locations | Construction | Functional Req. 3 | Examples | Step 4 |
| TIA-568 standard | References | Standards | Principles, Examples | Prerequisites |
| TIA-569 standard | References | Standards | Principles, Considerations | Prerequisites |
| TIA-606 standard | References | Standards | Principles | Steps 2-4 |
| TIA-607 standard | References | Standards | Considerations | Step 4 |
| Equipment room (ER) | Conditions | Interface Req. | Considerations | Steps 1, 4 |
| Telecommunications rooms (TRs) | Conditions | Interface Req. | Considerations | Steps 3, 4 |
| Pathway design | Construction | Performance Req. | Considerations, Trade-offs | Step 3 |
| Redundancy | Conditions | Performance Req. | Principles, Trade-offs | Step 2 |
| Future expansion (OBJ-8) | References | Performance Req. | Principles, Trade-offs | Steps 1, 3 |
| DEC-05 (separation from PKG-24) | Conditions | Scope Exclusions | Considerations | Step 7 (IDC) |
| CAD standards | Attributes | Quality Req. | Considerations | Steps 5, 6, 8 |
| Verification methods | — | Verification | — | Steps 6-9 |
| Design review | — | Verification | — | Step 8 |
| IDC | — | Verification | Considerations | Step 7 |

**Consistency verification:** All key entities and requirements are addressed across all four documents where applicable.

**Source:** Cross-document consistency check (Pass 2 enrichment)
