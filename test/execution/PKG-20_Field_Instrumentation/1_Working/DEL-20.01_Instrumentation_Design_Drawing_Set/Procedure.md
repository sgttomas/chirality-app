# Procedure: DEL-20.01 Instrumentation Design Drawing Set

## Purpose

This procedure defines the process for **producing** the Instrumentation Design Drawing Set within **PKG-20 Field Instrumentation** for the Canola Oil Transload Facility Phase 1 project.

**Deliverable Scope:**

Defines the design arrangement and details for instrumentation per ER requirements.

**Source:** Decomposition document `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, DEL-20.01 (line 496)

**Deliverable Type:** Drawing
**Discipline:** I&C
**Responsible Party:** D&B Contractor

**Source:** `_CONTEXT.md`

**Procedure Application:**

This procedure addresses the **production workflow** for creating the drawing set, from initial design through to final issuance for construction. It covers:
- Design development steps
- Interdisciplinary coordination
- Review and verification activities
- Drawing issuance and revision control

**Note:** For **operational use** of the drawings (i.e., how construction personnel use these drawings for field installation), refer to construction work packages and installation procedures developed by the construction team.

## Prerequisites

### Dependencies

**Dependency Coordination:**

See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies are coordinated externally by humans per project coordination plan (`execution/_Coordination/_COORDINATION.md`).

**Source:** `_DEPENDENCIES.md` file content

**Typical Upstream Inputs Required (Coordination):**

The following inputs are typically required before instrumentation design drawings can be developed:

1. **Process Engineering Deliverables:**
   - P&IDs (Piping & Instrumentation Diagrams) with instrument tag list
   - Process flow diagrams (PFDs) and heat & material balances
   - Instrument index and control philosophy
   - **TBD**: Specific deliverable references from process engineering package

2. **Layout and Equipment Deliverables:**
   - Plot plan and equipment layout drawings
   - Piping arrangements and isometrics (for instrument connection points)
   - Structural platform and access arrangements (for instrument mounting and cable routing)
   - **TBD**: Coordinate with PKG-14 (Process Piping), structural packages, layout deliverables

3. **Electrical and Control System Deliverables:**
   - Hazardous area classification drawings
   - Control system architecture and I/O allocation
   - Cable tray and duct bank routing plans
   - **TBD**: Coordinate with PKG-17 (Electrical Power Distribution), PKG-22 (Control Systems & SCADA), PKG-23 (Electrical Infrastructure)

4. **Specification and Data Deliverables:**
   - DEL-20.02 (Instrumentation Technical Specification) — performance and material requirements
   - DEL-20.03 (Instrumentation Design Calculations) — sizing and verification basis
   - DEL-20.04 (Instrumentation Data Sheet Package) — equipment data sheets and vendor information
   - **TBD**: Sequencing and availability of parallel PKG-20 deliverables

5. **Project Basis Documents:**
   - Employer's Requirements (Volume 2 Parts 1-3) — **TBD**: Specific sections applicable to instrumentation design
   - Project design basis and standards list
   - Project CAD standards and drawing conventions
   - Project quality procedures and design review protocols

**Source:** **ASSUMPTION** based on typical EPC workflow dependencies for instrumentation drawing development; cross-references to other packages per decomposition structure

### Reference Materials

**Required References:**

- Decomposition document (project scope and deliverable definition)
- `_REFERENCES.md` (deliverable-specific reference list) — **Currently empty**: References to be populated as design progresses
- Package `0_References/` directory (reference materials repository) — **TBD**: Reference materials to be provided
- Employer's Requirements — **TBD**: Access to Volume 2 Parts 1-3

**Source:** `_REFERENCES.md` content; Decomposition Section 3 (lines 75-79)

**Applicable Standards and Codes:**

- ISA 5.1 (Instrumentation Symbols and Identification)
- ISA 84 / IEC 61511 (Functional Safety) — if applicable
- CSA C22.1 (Canadian Electrical Code)
- API 554 (Process Instrumentation and Control)
- **TBD**: Additional standards per project specification

**Source:** Datasheet.md References section; **ASSUMPTION** based on I&C discipline typical applicable standards

**Manufacturer Documentation:**

- Instrument manufacturer installation manuals and drawings (from vendors per DEL-20.04)
- Mounting hardware and accessories data
- Cable and termination specifications

**Source:** **ASSUMPTION** based on typical instrumentation drawing detail requirements

### Personnel Requirements

**Design Team Roles:**

| Role | Qualification | Responsibility |
|------|---------------|----------------|
| I&C Lead Engineer | P.Eng. (Electrical/Control Systems) | Overall deliverable responsibility, approval authority |
| I&C Design Engineer | Engineering degree + I&C experience | Design development, drawing production |
| CAD Technician/Designer | CAD certification + I&C drawing experience | Drafting, CAD standards compliance |
| I&C Checker | P.Eng. or senior engineer (independent) | Peer review, independent verification |
| Interdisciplinary Coordinator | Engineering background | IDC coordination, comment resolution |

**Source:** **ASSUMPTION** based on typical EPC engineering team structure and professional practice requirements (P.Eng. for BC jurisdiction)

**Competency Requirements:**
- I&C discipline knowledge (instrumentation types, installation practices, standards)
- Project CAD software proficiency — **TBD**: CAD platform (AutoCAD, MicroStation, etc.)
- Familiarity with oil/gas or bulk liquid terminal operations — **ASSUMPTION**: Relevant to canola oil transload facility
- Hazardous area classification knowledge (CSA C22.1 Section 18)

**Source:** **ASSUMPTION** based on deliverable technical requirements and project context

### Tools and Resources

**Software/Systems:**
- CAD software — **TBD**: Specific platform and version per project standards
- Project document management system — **TBD**: System and access protocols
- Instrument database or management system — **TBD**: If applicable for tag management and cable schedule generation

**Physical Resources:**
- Site access for field verification (as-built conditions, constructibility review)
- Access to reference standards and codes (library or online subscriptions)

**Source:** **ASSUMPTION** based on typical engineering work environment requirements

## Steps

### Overview: Requirements Implementation

This procedure implements the requirements defined in Specification.md and produces the deliverable artifacts documented in Datasheet.md. Guidance.md provides the engineering rationale and decision-making context for the steps below.

**Key Requirement Mappings:**
- Step 2 implements Specification FR-2 (Instrument Location Plans) and FR-5 (Coordination with Process Design)
- Step 3 implements Specification FR-3 (Installation Details) and FR-4 (Cable Schedules)
- Step 4 implements Specification QR-1 (Design Review), PR-3 (Drawing Accuracy), and INT-1 (Interdisciplinary Coordination)
- Step 5 implements Specification QR-2 (Drawing Revision Control) and Documentation section
- Step 6 implements Specification QR-4 (As-Built Documentation)

### Step 1: Design Initiation and Planning

**Objective:** Establish design basis, scope, and work plan.

**Implements:** Specification Scope section and FR-1 (Drawing Content)

**Activities:**

1.1. **Review Design Basis**
   - Review Employer's Requirements for instrumentation design criteria — **TBD**: Specific ER sections
   - Review P&IDs and instrument list for scope definition
   - Review process conditions and equipment specifications
   - Identify critical instrumentation (safety, custody transfer, regulatory compliance)

1.2. **Define Drawing List**
   - Develop preliminary drawing list (by area, system, or drawing type)
   - Assign drawing numbers per project numbering convention — **TBD**: Project drawing numbering system
   - Establish drawing release schedule aligned with construction needs

1.3. **Establish Design Criteria**
   - Confirm environmental conditions (temperature, hazardous area classification, seismic)
   - Confirm applicable standards and code requirements
   - Confirm CAD standards and drawing conventions
   - Identify any project-specific requirements or deviations

**Deliverable:** Design initiation package (design basis summary, drawing list, schedule)

**Verification:** I&C Lead Engineer review and approval

**Source:** **ASSUMPTION** based on typical EPC design initiation process

### Step 2: Design Development (Concept Phase)

**Objective:** Develop preliminary instrument locations and routing concepts.

**Activities:**

2.1. **Develop Instrument Location Concepts**
   - Locate instruments on equipment layout and piping arrangement drawings
   - Consider process requirements (measurement point locations per P&IDs)
   - Consider installation and maintenance access requirements
   - Consider hazardous area boundaries and electrical protection requirements
   - Identify mounting requirements (pipe-mounted, vessel-mounted, structure-mounted)

2.2. **Develop Cable Routing Concepts**
   - Identify cable tray and duct bank routing from instrument locations to termination points
   - Identify junction box locations (grouping by area, minimizing cable lengths)
   - Consider segregation requirements (IS barriers, power vs. signal)
   - Coordinate with electrical infrastructure design (PKG-23)

2.3. **Develop Installation Detail Concepts**
   - Identify typical vs. specific detail requirements
   - Review manufacturer installation recommendations
   - Develop standard details for common installations (instrument supports, cable glands, etc.)

2.4. **30% Design Review** (**ASSUMPTION**)
   - Issue concept drawings for internal review and interdisciplinary coordination
   - Resolve major conflicts and confirm design approach
   - Obtain approval to proceed to detailed design

**Deliverable:** Concept drawings (30% completeness) — **TBD**: Project-specific design review stages

**Verification:** Design review meeting, IDC coordination, I&C Lead approval

**Source:** **ASSUMPTION** based on typical EPC phased design approach (30/60/90/IFC)

### Step 3: Detailed Design Development

**Objective:** Develop detailed drawings suitable for construction and procurement.

**Activities:**

3.1. **Produce Detailed Instrument Location Plans**
   - Finalize instrument locations with dimensions and elevations
   - Add instrument tag numbers, service descriptions, and notes
   - Coordinate with piping isometrics for exact connection points
   - Coordinate with structural drawings for platform access and support locations

3.2. **Produce Detailed Installation Details**
   - Develop detailed mounting arrangements and connection diagrams
   - Reference manufacturer installation drawings where applicable
   - Include hazardous area sealing details per CSA C22.1
   - Include material specifications and bill of materials

3.3. **Produce Cable Schedules**
   - Develop comprehensive cable schedule with:
     - Cable tag numbers
     - From/To termination points
     - Cable specifications (type, size, conductor count, shielding)
     - Cable lengths and routing references
     - Termination details (junction box numbers, terminal strips)
   - Coordinate with control system I/O allocation (PKG-22)
   - Verify cable types and routing comply with hazardous area requirements

3.4. **60% Design Review** (**ASSUMPTION**)
   - Issue detailed drawings for formal review
   - Conduct interdisciplinary check (IDC) with all affected disciplines
   - Resolve comments and incorporate feedback

**Deliverable:** Detailed drawings (60% completeness) — **TBD**: Project-specific design review stages

**Verification:** IDC sign-off, design review approval, comment resolution

**Source:** **ASSUMPTION** based on typical EPC detailed design process

### Step 4: Final Design and Verification

**Objective:** Finalize drawings for construction issuance.

**Activities:**

4.1. **Complete Drawing Finalization**
   - Incorporate all review comments from 60% review
   - Add final details, notes, and specifications
   - Verify all cross-references and drawing coordination
   - Complete title blocks, revision blocks, and drawing stamps

4.2. **Self-Check**
   - Design engineer performs self-check using project checklist:
     - Completeness (all instruments from P&IDs are located and detailed)
     - Accuracy (dimensions, elevations, tag numbers verified)
     - Coordination (no conflicts with other disciplines)
     - Standards compliance (CAD standards, code requirements)
     - Clarity (drawings are clear and suitable for construction use)

4.3. **Independent Check**
   - Independent checker (qualified I&C engineer, not the originator) performs peer review:
     - Verify design compliance with Employer's Requirements and standards
     - Verify calculations and sizing (cross-check with DEL-20.03)
     - Verify equipment data (cross-check with DEL-20.04)
     - Identify errors, omissions, or improvement opportunities
     - Document review findings on check sheets

4.4. **Interdisciplinary Check (IDC)**
   - Issue drawings to affected disciplines for final coordination:
     - Process/Piping: Instrument connections, line numbers, operating conditions
     - Structural: Mounting supports, platform access, seismic bracing
     - Electrical: Power supply, cable routing, hazardous area compliance
     - Control Systems: I/O allocation, signal types, network architecture
   - Resolve all IDC comments and obtain discipline sign-offs

4.5. **90% Design Review** (**ASSUMPTION**)
   - Formal design review meeting with project team
   - Confirm readiness for IFC (Issued for Construction)
   - Obtain approval for final issuance

**Deliverable:** Final drawings (90% completeness, ready for IFC)

**Verification:** Self-check sign-off, independent check sign-off, IDC sign-offs, design review approval

**Source:** **ASSUMPTION** based on typical EPC verification process and quality assurance requirements

### Step 5: Drawing Approval and Issuance

**Objective:** Issue approved drawings for construction use.

**Activities:**

5.1. **Drawing Approval**
   - I&C Lead Engineer reviews and approves drawings
   - Professional Engineer stamp and signature (per provincial requirements for BC) — **TBD**: P.Eng. seal requirements
   - Document Control reviews for completeness and compliance with document control procedures

5.2. **Issued for Construction (IFC)**
   - Issue drawings with IFC status and revision identifier
   - Distribute per project distribution matrix:
     - Construction team (for field installation)
     - Procurement team (for equipment purchasing, if applicable)
     - Quality assurance (for inspection planning)
     - Commissioning team (for system checkout planning)
     - **TBD**: Project-specific distribution requirements

5.3. **Drawing Registration**
   - Register drawings in project document management system
   - Create as-built placeholder records (to be updated during construction)
   - Archive superseded revisions per document retention requirements

**Deliverable:** IFC drawings, distribution records

**Verification:** Document control approval, distribution confirmation

**Source:** **ASSUMPTION** based on typical EPC drawing issuance process and document control requirements

### Step 6: Drawing Maintenance and Revision

**Objective:** Manage drawing changes and maintain as-built documentation.

**Activities:**

6.1. **Change Management**
   - Process field change requests and RFIs (Requests for Information)
   - Evaluate impact of changes on design and downstream work
   - Issue revised drawings with revision identifier and revision description
   - Maintain revision history and change log

6.2. **As-Built Updates**
   - Incorporate field modifications and deviations during construction
   - Incorporate commissioning findings and adjustments
   - Coordinate as-built updates with construction site team (red-line markups)
   - Issue final as-built drawings upon project completion

6.3. **Lessons Learned Capture**
   - Document design issues, construction challenges, and improvement opportunities
   - Feed lessons learned into future project design standards and typical details
   - Contribute to continuous improvement of drawing production process

**Deliverable:** Revised drawings, as-built drawings, lessons learned documentation

**Verification:** Revision approval per same process as Step 5, as-built verification by construction team

**Source:** **ASSUMPTION** based on typical EPC change management and as-built documentation process

## Verification

### Design Verification Activities

**Verification Matrix:**

| Verification Type | Method | Performer | Timing | Documentation |
|-------------------|--------|-----------|--------|---------------|
| Self-check | Checklist review | Design engineer | After drawing completion | Check sheet (originator signature) |
| Independent check | Peer review | Independent I&C engineer | After self-check | Check sheet (checker signature) |
| Interdisciplinary check | Coordination review | All affected disciplines | At design milestones (30/60/90%) | IDC comments and sign-offs |
| Design review | Formal review meeting | Project team | At design milestones | Design review minutes, action log |
| Standards compliance | Code compliance check | QA or Lead Engineer | Before IFC issuance | Compliance checklist |
| CAD standards audit | Drawing standards check | CAD Manager or QA | Before IFC issuance | CAD standards checklist |

**Source:** **ASSUMPTION** based on typical EPC verification requirements and quality assurance practices

### Acceptance Criteria

**Drawing Acceptance Criteria:**

The drawing set is acceptable for issuance when:

1. **Completeness:**
   - All instruments from P&IDs are located and detailed
   - All anticipated artifacts are produced (location plans, installation details, cable schedules)
   - All drawing sheets are complete with no TBD placeholders (or TBDs explicitly approved by Lead Engineer)

2. **Accuracy:**
   - Instrument tag numbers match P&IDs and instrument index
   - Instrument locations are dimensioned and coordinated with piping/equipment arrangements
   - Installation details reflect manufacturer requirements and code compliance
   - Cable schedules match control system I/O allocation

3. **Coordination:**
   - All interdisciplinary check (IDC) comments are resolved and disciplines have signed off
   - No open conflicts with other discipline drawings
   - Hazardous area classifications are correctly reflected and compliant with CSA C22.1

4. **Standards Compliance:**
   - Drawings comply with project CAD standards (symbology, layering, title blocks, revision control)
   - Instrumentation symbology complies with ISA 5.1
   - Installation details comply with applicable codes (CSA C22.1, manufacturer requirements)

5. **Approval:**
   - Self-check and independent check are complete with sign-offs
   - I&C Lead Engineer has approved drawings
   - Professional Engineer seal applied (if required per provincial regulations)
   - Document control has confirmed compliance with document control procedures

**Source:** **ASSUMPTION** based on typical EPC drawing acceptance criteria and quality gate requirements

### Hold Points and Witness Points

**Potential Hold Points (TBD):**
- **TBD** — Hold points for Employer review to be identified per project execution plan and Employer's Requirements
- **ASSUMPTION**: Typical hold points may include:
  - 30% design review (concept approval)
  - 90% design review (pre-IFC approval)
  - IFC issuance (Employer acceptance before construction use)

**Witness Points (if applicable):**
- **TBD** — Witness points for Employer or third-party verification (e.g., regulatory authority review for safety-critical instrumentation)

**Source:** **ASSUMPTION** based on typical EPC quality plan structure; specific hold/witness points to be confirmed per project quality procedures and Employer's Requirements

## Records

### Documentation Outputs

**Primary Deliverable Outputs:**

1. **Instrument Location Plans**
   - Format: CAD drawings (PDF + native DWG/DGN) — **TBD**: Project CAD platform
   - Naming convention: **TBD** — Per project drawing numbering system
   - Storage location: Project document management system

2. **Instrument Installation Details**
   - Format: CAD drawings (PDF + native DWG/DGN)
   - Content: Typical and specific mounting/connection details
   - Storage location: Project document management system

3. **Cable Schedules**
   - Format: Tabular schedules (embedded in drawings or separate database export) — **TBD**: Project preference
   - Content: Cable identification, routing, specifications, terminations
   - Storage location: Project document management system

**Source:** Decomposition DEL-20.01 Anticipated Artifacts (line 496)

### Supporting Records

**Design and Verification Records:**

- Design calculations and analysis (cross-reference to DEL-20.03)
- Equipment data sheets and vendor information (cross-reference to DEL-20.04)
- Design review minutes and action logs
- Self-check and independent check sheets (signed)
- Interdisciplinary check comment logs and sign-offs
- Code compliance checklists
- CAD standards audit records

**Source:** **ASSUMPTION** based on typical EPC quality record requirements

**Change Management Records:**
- Field change requests and RFIs
- Revision logs and change descriptions
- As-built markup drawings (red-lines from construction)
- Lessons learned documentation

**Source:** **ASSUMPTION** based on typical EPC change control and as-built documentation process

### Record Management

**Filing and Storage:**

- Working files: Stored in deliverable folder `1_Working/` during design development
- Checking files: Copies placed in `2_Checking/To/` for formal review, returned in `2_Checking/From/` with comments
- Issued files: Final approved drawings placed in `3_Issued/` with revision identifier and issuance date
- Archive: Superseded revisions archived per project document retention plan

**Source:** README.md description of lifecycle folder structure (lines 115-124)

**Retention Requirements:**

- **TBD** — Retention period per project contract requirements and regulatory obligations
- **ASSUMPTION**: Typical retention includes:
  - Design records: Duration of design warranty period
  - As-built drawings: Facility lifecycle (permanent record)
  - Quality records: Per quality management plan and regulatory requirements (e.g., 7 years for professional practice records)

**Access Control:**
- Electronic records managed per project document management system access controls
- Distribution controlled per project distribution matrix
- Confidentiality and security per project contract terms

**Source:** **ASSUMPTION** based on typical EPC document management and professional practice requirements

### Integration with Other Deliverables

**Cross-References:**

This deliverable's records integrate with:
- **DEL-20.02 (Instrumentation Technical Specification)** — Drawings implement specification requirements
- **DEL-20.03 (Instrumentation Design Calculations)** — Drawings reflect calculation results (sizing, verification)
- **DEL-20.04 (Instrumentation Data Sheet Package)** — Drawings reference equipment data sheet information
- **DEL-20.05 (Instrumentation Installation & Test Records)** — Drawings support commissioning and testing activities

**Source:** Decomposition PKG-20 deliverables (lines 496-500); deliverable cross-reference relationships

### Handover to Operations

**Facility Turnover:**

Upon project completion, the following documentation shall be provided to the facility operations team:
- Final as-built drawings (all revisions)
- Electronic files (CAD native files for future modifications)
- Instrument location reference for maintenance planning
- Integration with facility asset management system — **TBD**: System and data format requirements

**Source:** **ASSUMPTION** based on typical facility turnover requirements and OBJ-9 (Lifecycle Cost Optimization) objective supporting maintainability

**Source (OBJ-9):** Decomposition Section 2 Project Objectives (line 66)

## Project Objective Alignment

This procedure supports the following project objectives:

**OBJ-1: Safe & Reliable Operation**
- Rigorous design and verification process ensures instrumentation is properly designed and installed
- Quality checks reduce errors and improve system reliability
- Clear documentation supports safe construction and commissioning

**Source:** Decomposition Section 6 Objective-to-Deliverable Mapping — PKG-20 supports OBJ-1 (line 780)

**Secondary Objective Support:**

- **OBJ-6: Regulatory Compliance** — Procedure ensures compliance with electrical code (CSA C22.1) and professional practice requirements (P.Eng. review)
- **OBJ-9: Lifecycle Cost Optimization** — Quality design reduces construction rework and supports efficient operations/maintenance
- **OBJ-5: Terminal Continuity** — Phased drawing release (if applicable) can support construction schedule and minimize terminal disruption

**Source:** **ASSUMPTION** based on procedure's role in quality assurance, compliance, and efficient project execution
