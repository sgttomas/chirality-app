# Procedure: DEL-20.02 Instrumentation Technical Specification

## Purpose

This procedure defines the process for **producing** the Instrumentation Technical Specification within **PKG-20 Field Instrumentation** for the Canola Oil Transload Facility Phase 1 project.

**Deliverable Scope:**

Defines performance, materials, and workmanship requirements for instrumentation per ER requirements.

**Source:** Decomposition document `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, DEL-20.02 (line 497)

**Deliverable Type:** Specification
**Discipline:** I&C
**Responsible Party:** D&B Contractor

**Procedure Application:**

This procedure addresses the **production workflow** for creating the technical specification, from requirements gathering through to final issuance. The specification will be used for equipment procurement, construction execution, and quality verification.

## Prerequisites

### Dependencies

**Dependency Coordination:**

See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies coordinated externally by humans per project coordination plan.

**Typical Upstream Inputs Required (Coordination):**

1. **Process Engineering Deliverables:**
   - P&IDs with instrument list and service descriptions
   - Process data sheets (operating pressures, temperatures, flow rates)
   - Control philosophy and alarm/interlock schedule
   - **TBD**: Specific process engineering deliverable references

2. **Project Basis Documents:**
   - Employer's Requirements (Volume 2 Parts 1-3) — **TBD**: Specific sections for instrumentation requirements
   - Project design basis and standards list
   - Hazardous area classification drawings
   - Environmental design criteria (temperature, seismic, marine exposure)

3. **Related PKG-20 Deliverables (Coordination):**
   - DEL-20.03 (Instrumentation Design Calculations) — sizing/verification basis
   - DEL-20.04 (Instrumentation Data Sheet Package) — data sheet templates must match specification requirements
   - Sequencing: Specification typically precedes data sheets (specification defines requirements, data sheets demonstrate compliance)

**Source:** **ASSUMPTION** based on typical EPC workflow for specification development; cross-references per decomposition

### Reference Materials

**Required References:**

- Decomposition document (project scope and deliverable definition)
- `_REFERENCES.md` (deliverable-specific reference list) — **Currently empty**: References to be populated
- Package `0_References/` directory — **TBD**: Reference materials to be provided
- Employer's Requirements — **TBD**: Access to Volume 2 Parts 1-3

**Applicable Standards and Codes:**

- ISA 5.1, ISA 84, API 554, API 2350 (instrumentation and safety)
- CSA C22.1 (electrical and hazardous area)
- ASTM, ASME material and construction standards
- **TBD**: Additional standards per project requirements

**Industry References:**

- Vendor catalogs and technical literature (for technology capabilities and typical specifications)
- Previous project specifications for similar facilities (precedent references)

**Source:** Specification.md Standards section; **ASSUMPTION** based on typical specification development inputs

### Personnel Requirements

| Role | Qualification | Responsibility |
|------|---------------|----------------|
| I&C Lead Engineer | P.Eng. (Electrical/Control Systems) | Overall deliverable responsibility, approval authority |
| I&C Specification Engineer | Engineering degree + I&C experience | Specification development, requirements definition |
| I&C Checker | P.Eng. or senior engineer (independent) | Peer review, independent verification |
| Procurement Coordinator | Engineering or procurement background | Procurement interface, vendor coordination |

**Source:** **ASSUMPTION** based on typical EPC engineering team structure

### Tools and Resources

- Word processing / specification software — **TBD**: Platform per project standards
- Project document management system — **TBD**: System and access protocols
- Access to codes and standards (library or online subscriptions)
- Industry technical references and vendor literature

**Source:** **ASSUMPTION** based on typical specification development work environment

## Steps

### Overview: Requirements Implementation

This procedure implements the requirements defined in Specification.md and produces the specification artifacts documented in Datasheet.md. Guidance.md provides the engineering rationale and decision-making context for the steps below.

**Key Requirement Mappings:**
- Step 1 implements Specification Scope (requirements capture)
- Step 2 implements Specification FR-1 to FR-5 (functional requirements definition)
- Step 3 implements Specification PR-1 to PR-5 (performance requirements definition)
- Step 4 implements Specification INT-1 to INT-4, QR-1 to QR-4 (coordination and quality)
- Step 5 implements Specification Documentation section (issuance and management)

### Step 1: Requirements Gathering and Basis Development

**Objective:** Establish specification basis and capture requirements from source documents.

**Implements:** Specification Scope section

**Activities:**

1.1. **Review Employer's Requirements**
   - Extract instrumentation performance requirements — **TBD**: Specific ER sections
   - Identify regulatory and code compliance requirements
   - Identify project-specific preferences (approved vendor lists, standardization requirements)

1.2. **Review Process Design Basis**
   - Review P&IDs for instrument applications (level, pressure, temperature, flow)
   - Review process data sheets for operating conditions (ranges, design pressures/temperatures)
   - Review control philosophy for accuracy and response time requirements
   - Identify safety instrumented functions (SIF) requiring ISA 84 / IEC 61511 compliance

1.3. **Review Environmental and Site Conditions**
   - Operating temperature range (outdoor BC coastal climate)
   - Hazardous area classification (canola oil combustibility)
   - Seismic requirements (Surrey, BC location)
   - Corrosion environment (marine terminal)

1.4. **Establish Specification Structure**
   - Decide on organization: Single comprehensive specification vs. separate specs by instrument type (level, pressure, temperature)
   - Establish section structure (see Specification.md Documentation section for typical organization)
   - Assign section responsibilities (if multiple engineers)

**Deliverable:** Requirements register, specification outline

**Verification:** I&C Lead Engineer review and approval of approach

**Source:** **ASSUMPTION** based on typical EPC specification initiation process; Specification Scope and Requirements sections

### Step 2: Draft Functional Requirements

**Objective:** Define what instruments must accomplish (measurement functions).

**Implements:** Specification FR-1 to FR-5

**Activities:**

2.1. **Level Measurement Requirements**
   - Storage tank level measurement (3 × 15,000 MT tanks):
     - Continuous level for inventory and control
     - High/low level alarms
     - Independent overfill protection per API 2350
   - Process vessel level measurement (pits, sumps, day tanks)
   - Marine loading level monitoring
   - Technology selection guidance (radar, guided wave, float, switches)

2.2. **Pressure Measurement Requirements**
   - Pump performance monitoring (suction/discharge pressure)
   - Piping system pressure monitoring and control
   - Loading operations pressure control
   - Safety alarms and interlocks
   - Technology selection (transmitters, gauges, switches)

2.3. **Temperature Measurement Requirements**
   - Product temperature monitoring (storage tanks, transfer lines)
   - Equipment protection (pump bearings, motor windings)
   - Ambient temperature monitoring
   - Technology selection (RTDs, thermocouples, switches, thermowells)

2.4. **Instrument Accessories Requirements**
   - Instrument valves, tubing, fittings
   - Enclosures and junction boxes
   - Cable glands and sealing
   - Mounting hardware

**Deliverable:** Functional requirements section (draft)

**Verification:** Review against P&IDs and process design basis; cross-check with DEL-20.03 calculations (if available)

**Source:** Specification FR-1 to FR-5; **ASSUMPTION** based on typical functional requirements for bulk liquid terminal instrumentation

### Step 3: Draft Performance, Material, and Workmanship Requirements

**Objective:** Define how well instruments must perform and what they must be made of.

**Implements:** Specification PR-1 to PR-5

**Activities:**

3.1. **Performance Requirements**
   - Accuracy and uncertainty (fit-for-purpose per application)
   - Measurement ranges (based on process design)
   - Response time and update rate
   - Environmental ratings (temperature, humidity, enclosure ingress protection)
   - Hazardous area compliance (CSA/UL certification, protection method)
   - Seismic qualification

3.2. **Material Requirements**
   - Wetted materials (316/316L stainless steel for canola oil service)
   - Enclosure materials (stainless steel or marine aluminum, NEMA 4X rating)
   - Instrument tubing and fittings (stainless steel, pressure-rated)
   - Gaskets and seals (food-grade, compatible with canola oil)
   - Coatings and finishes (marine-grade, corrosion-resistant)

3.3. **Workmanship Requirements**
   - Installation methods (per manufacturer instructions, ISA/API standards)
   - Welding and threaded connections (per applicable codes)
   - Impulse piping slope and support requirements
   - Hazardous area installation requirements (conduit sealing, cable glands per CSA C22.1)
   - Calibration requirements (initial and periodic)
   - Testing requirements (see DEL-20.05 for detailed test procedures)

**Deliverable:** Performance, material, and workmanship requirements sections (draft)

**Verification:** Cross-check with environmental design basis, hazardous area classification, and material compatibility requirements

**Source:** Specification PR-1 to PR-5; **ASSUMPTION** based on typical performance/material/workmanship requirements

### Step 4: Coordination, Review, and Finalization

**Objective:** Coordinate with stakeholders, resolve comments, finalize specification.

**Implements:** Specification INT-1 to INT-4, QR-1 to QR-4

**Activities:**

4.1. **Interdisciplinary Coordination**
   - Coordinate with Process (P&ID alignment, process conditions)
   - Coordinate with Piping (instrument connections, taps, valves)
   - Coordinate with Electrical (power supply, hazardous area classification, cable routing)
   - Coordinate with Control Systems (signal types, I/O requirements, communication protocols)
   - Coordinate with Procurement (vendor evaluation criteria, data sheet requirements)

4.2. **Internal Technical Review**
   - Specification engineer self-check (completeness, accuracy, clarity)
   - Independent peer review by qualified I&C engineer
   - Review against applicable codes and standards (compliance verification)
   - Review against Employer's Requirements

4.3. **Interdisciplinary Review (IDC)**
   - Issue specification for formal IDC review
   - Collect comments from all affected disciplines
   - Resolve comments (revise specification or provide technical response)
   - Obtain IDC sign-offs

4.4. **Finalization**
   - Incorporate all review comments
   - Complete all specification sections (no TBD placeholders unless explicitly approved)
   - Add references, definitions, and supporting information
   - Format and proofread per project document standards

**Deliverable:** Final specification (ready for approval and issuance)

**Verification:** All review comments resolved, all IDC sign-offs obtained, independent check complete

**Source:** Specification INT-1 to INT-4, QR-1; **ASSUMPTION** based on typical EPC review and coordination process

### Step 5: Approval, Issuance, and Maintenance

**Objective:** Approve specification and issue for use in procurement and construction.

**Implements:** Specification Documentation section

**Activities:**

5.1. **Approval**
   - I&C Lead Engineer review and approval
   - Professional Engineer stamp and signature (if required per provincial regulations) — **TBD**: P.Eng. seal requirements for BC
   - Document Control review for compliance with document control procedures

5.2. **Issuance**
   - Issue specification with appropriate status (IFP = Issued for Procurement, IFC = Issued for Construction)
   - Distribute per project distribution matrix:
     - Procurement team (for equipment RFQs and bid packages)
     - Construction team (for installation workmanship)
     - Quality assurance (for inspection and testing criteria)
     - Vendors (with RFQ packages)
     - **TBD**: Project-specific distribution requirements

5.3. **Document Registration**
   - Register specification in project document management system
   - Link to related documents (DEL-20.01, DEL-20.03, DEL-20.04, DEL-20.05)
   - Archive superseded revisions per document retention requirements

5.4. **Procurement Support**
   - Participate in vendor RFQ preparation (specification is basis of RFQ)
   - Support bid evaluation (review vendor quotations and data sheets against specification)
   - Participate in vendor clarification meetings
   - Review and approve vendor data sheets (DEL-20.04 coordination)

5.5. **Construction Support**
   - Respond to RFIs (Requests for Information) from construction contractors
   - Review field change requests affecting specification compliance
   - Support quality assurance inspections (interpretation of specification requirements)

5.6. **Specification Maintenance**
   - Issue revisions as needed (design changes, vendor equipment changes)
   - Maintain revision log and change descriptions
   - Update as-installed documentation if specification changes during construction
   - Contribute lessons learned to future specification standards

**Deliverable:** Issued specification, distribution records, procurement/construction support

**Verification:** Approval sign-offs, distribution confirmation, successful procurement and construction use

**Source:** Specification Documentation section; **ASSUMPTION** based on typical EPC specification issuance and lifecycle management

## Verification

### Specification Verification Activities

| Verification Type | Method | Performer | Timing | Documentation |
|-------------------|--------|-----------|--------|---------------|
| Requirements completeness | Requirements checklist | Specification engineer | After Step 1 | Requirements register |
| Technical accuracy | Peer review | Independent I&C engineer | After Step 3 | Independent check sheet |
| Interdisciplinary coordination | IDC review | All affected disciplines | After Step 3 | IDC comments and sign-offs |
| Standards compliance | Compliance review | I&C Lead + QA | After Step 4 | Compliance checklist |
| Employer's Requirements compliance | ER compliance review | I&C Lead | After Step 4 | ER compliance matrix |
| Procurement readiness | Procurement review | Procurement team | Before Step 5 issuance | Procurement feedback |

**Source:** **ASSUMPTION** based on typical EPC verification methods for specification deliverables

### Acceptance Criteria

The specification is acceptable for issuance and use when:

1. **Completeness:**
   - All functional requirements are defined for level, pressure, temperature instruments
   - All performance requirements (accuracy, range, environmental, hazardous area) are specified
   - All material requirements (wetted parts, enclosures, accessories) are specified
   - All workmanship requirements (installation, calibration, testing) are specified
   - All applicable codes and standards are referenced

2. **Accuracy:**
   - Requirements align with process design basis (P&IDs, process data sheets)
   - Ranges and accuracies verified by DEL-20.03 calculations (if available)
   - Hazardous area requirements align with hazardous area classification drawings
   - Environmental requirements align with project environmental design basis

3. **Coordination:**
   - All IDC comments resolved and disciplines have signed off
   - Specification requirements are consistent with related deliverables (DEL-20.01, DEL-20.03, DEL-20.04)
   - Procurement team confirms specification is suitable for vendor RFQs
   - Construction team confirms workmanship requirements are constructible

4. **Quality:**
   - Independent check complete with sign-off
   - I&C Lead Engineer has approved
   - Compliance with applicable codes and standards verified
   - Document control has confirmed compliance with project document control procedures

5. **Usability:**
   - Specification is clear and unambiguous (vendors and contractors can interpret and comply)
   - Data sheet templates (DEL-20.04) match specification requirements (vendor submittals will address all requirements)
   - Acceptance criteria are verifiable (inspection and testing can confirm compliance)

**Source:** **ASSUMPTION** based on typical specification deliverable acceptance criteria

### Hold Points and Witness Points

**Potential Hold Points (TBD):**
- **TBD** — Hold points for Employer review to be identified per project execution plan
- **ASSUMPTION**: Typical hold points may include specification issue for Employer approval before equipment procurement

**Source:** **ASSUMPTION** based on typical EPC quality plan structure

## Records

### Documentation Outputs

**Primary Deliverable Outputs:**

1. **Level Instrument Specification**
   - Format: **TBD** — Technical specification document (Word, PDF, or specification software format)
   - Content: Performance, materials, workmanship for level instruments
   - Storage: Project document management system

2. **Pressure Instrument Specification**
   - Format: **TBD** — Technical specification document
   - Content: Performance, materials, workmanship for pressure instruments
   - Storage: Project document management system

3. **Temperature Specification**
   - Format: **TBD** — Technical specification document
   - Content: Performance, materials, workmanship for temperature instruments
   - Storage: Project document management system

**Source:** Decomposition DEL-20.02 Anticipated Artifacts (line 497)

**Note:** Specifications may be combined into a single comprehensive document or issued as separate specifications per instrument type — **TBD**: Organization per project preference.

### Supporting Records

**Development Records:**
- Requirements register and source document references
- Design review minutes and action logs
- Independent check sheets (signed)
- Interdisciplinary check comment logs and sign-offs
- Standards compliance checklists
- Employer's Requirements compliance matrix

**Procurement and Construction Support Records:**
- RFI responses (specification clarifications)
- Field change requests affecting specification
- Lessons learned documentation

**Source:** **ASSUMPTION** based on typical EPC quality record requirements

### Record Management

**Filing and Storage:**

- Working files: Stored in deliverable folder `1_Working/` during specification development
- Checking files: Copies placed in `2_Checking/To/` for formal review
- Issued files: Final approved specifications placed in `3_Issued/` with revision identifier
- Archive: Superseded revisions archived per project document retention plan

**Retention Requirements:**

- **TBD** — Retention period per project contract requirements
- **ASSUMPTION**: Typical retention includes design records during warranty period; final specifications as permanent facility records

**Access Control:**
- Electronic records managed per project document management system access controls
- Distribution controlled per project distribution matrix

**Source:** README.md description of lifecycle folder structure (lines 115-124); **ASSUMPTION** on retention and access control

### Integration with Other Deliverables

**Cross-References:**

This deliverable's records integrate with:
- **DEL-20.01 (Drawing Set):** Drawings implement specification requirements
- **DEL-20.03 (Calculations):** Calculations verify specification requirements
- **DEL-20.04 (Data Sheets):** Data sheets demonstrate specification compliance
- **DEL-20.05 (Test Records):** Test records verify specification compliance during commissioning

**Source:** Decomposition PKG-20 deliverables (lines 496-500); deliverable cross-reference relationships

### Handover to Operations

**Facility Turnover:**

Upon project completion, specifications shall be provided to facility operations team:
- Final as-issued specifications (all revisions)
- Inclusion in operations and maintenance (O&M) manuals
- Reference for future procurement (replacement instruments, spare parts)
- Reference for maintenance procedures (calibration, testing requirements)

**Source:** **ASSUMPTION** based on typical facility turnover requirements and OBJ-9 (Lifecycle Cost Optimization) supporting maintainability

## Project Objective Alignment

This procedure supports the following project objectives:

**OBJ-1: Safe & Reliable Operation**

Rigorous specification development process ensures:
- Instruments are fit-for-purpose for measurement and safety functions
- Quality checks reduce specification errors that could compromise safety/reliability
- Clear requirements support proper procurement and installation

**Source:** Decomposition Section 6 Objective-to-Deliverable Mapping — PKG-20 supports OBJ-1 (line 780)

**Secondary Objective Support:**

- **OBJ-6: Regulatory Compliance** — Procedure ensures compliance with electrical code (CSA C22.1), safety standards (API 2350), and professional practice
- **OBJ-9: Lifecycle Cost Optimization** — Fit-for-purpose specifications balance capital cost with maintenance cost and reliability
- **OBJ-10: Custody Transfer Accuracy** — Specifications support accurate product metering (coordinate with PKG-12)

**Source:** **ASSUMPTION** based on procedure's role in quality assurance, compliance, and efficient project execution

## Cross-Document Traceability

This Procedure defines the production workflow for DEL-20.02. The following documents provide complementary information:

| Document | Purpose | Key Linkages |
|----------|---------|--------------|
| Datasheet.md | Factual identification, attributes, conditions, references | Identification § provides deliverable identity; Conditions § provides project context; Construction § defines instrument types |
| Specification.md | Requirements and verification criteria | FR-1 to FR-5 define what to specify; QR-1 to QR-4 define quality requirements; INT-1 to INT-4 define interfaces |
| Guidance.md | Engineering rationale and decision context | Principles explain design approach; Trade-offs inform technology selection; Technical Considerations guide requirements definition |

**Procedure-to-Specification Mapping:**

| Procedure Step | Specification Requirement | What Is Implemented |
|----------------|--------------------------|---------------------|
| Step 1.1 | Scope, Standards | Requirements from Employer's Requirements |
| Step 1.2 | FR-1 to FR-5 | Process design basis requirements |
| Step 1.3 | PR-2 to PR-4 | Environmental and site conditions |
| Step 2.1 | FR-2 | Level measurement functional requirements |
| Step 2.2 | FR-3 | Pressure measurement functional requirements |
| Step 2.3 | FR-4 | Temperature measurement functional requirements |
| Step 2.4 | FR-5 | Instrument accessories functional requirements |
| Step 3.1 | PR-1 to PR-5 | Performance requirements |
| Step 3.2 | PR-2 | Material requirements |
| Step 3.3 | QR-4 | Workmanship requirements |
| Step 4.1 | INT-1 to INT-4 | Interdisciplinary coordination |
| Step 4.2-4.4 | QR-1 | Review and finalization |
| Step 5.1-5.6 | Documentation | Approval, issuance, maintenance |
