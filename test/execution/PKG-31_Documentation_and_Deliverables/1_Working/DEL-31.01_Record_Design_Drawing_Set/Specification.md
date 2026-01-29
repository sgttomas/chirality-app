# Specification: DEL-31.01 Record Design Drawing Set

## Scope

This specification defines the requirements for **Record Design Drawing Set** within **PKG-31 Documentation & Deliverables**.

**Purpose:**
Defines and substantiates record design drawings in accordance with Employer's Requirements (ER) and VFPA standards.

**Source:** Decomposition DEL-31.01 (line 686)

**Scope Inclusions:**

The Record Design Drawing Set shall include:
- Final approved design drawings from all project disciplines (Civil, Structural, Mechanical, Process, Electrical, I&C, Marine, Buildings, Fire Protection)
- Drawing registers and indices
- Drawing transmittal documentation
- Revision control and tracking documentation

**Scope Exclusions:**

- As-Built drawings (covered under DEL-31.02)
- Construction working drawings and shop drawings (discipline-specific deliverables)
- Vendor drawings (covered under DEL-31.05)
- Temporary works drawings (not part of permanent facility documentation)

**Source:** **ASSUMPTION** based on distinction between Record (design intent) and As-Built (as-constructed) per industry practice

**Anticipated deliverable artifacts:**
- Record drawings (all disciplines) per VFPA standards

**Source:** _CONTEXT.md; Decomposition line 686

## Requirements

### Functional Requirements

**FR-01: Drawing Completeness**
- The Record Design Drawing Set shall include all final approved design drawings for the Canola Oil Transload Facility Phase 1 Works
- All disciplines identified in Section 4 of the Decomposition (Packages and Deliverables) shall be represented
- **Source:** Decomposition Section 4; **ASSUMPTION** based on project scope
- **Rationale:** See Guidance.md (Principle 2: Multi-Discipline Integration; Considerations: Scope and Completeness)
- **Verification:** See Procedure.md (Step 1.1: Develop Drawing Register; Step 3.4: Completeness Check)

**FR-02: Drawing Accuracy**
- All drawings shall accurately represent the approved design intent
- Drawings shall be based on final design calculations, specifications, and design verification outcomes
- **Source:** **ASSUMPTION** per engineering practice; cross-reference to DEL-28.01–DEL-28.03 (Design Verification)

**FR-03: VFPA Standards Compliance**
- All drawings shall comply with VFPA (Vancouver Fraser Port Authority) drawing standards and requirements
- **Source:** Decomposition DEL-31.01 (line 686); Employer's Requirements — **TBD** — **location TBD**
- **Rationale:** See Guidance.md (Principle 3: Standardization and Consistency; Considerations: VFPA Standards Compliance)
- **Verification:** See Procedure.md (Step 1.4: Obtain VFPA Standards; Step 3.3: VFPA Standards Compliance Check)

**FR-04: Multi-Discipline Coordination**
- Drawings shall demonstrate coordination between disciplines (e.g., structural/architectural coordination, mechanical/electrical clash resolution)
- **Source:** **ASSUMPTION** per project coordination requirements; reference Decomposition DEC-01 (line 799) — discipline-organized packages
- **Rationale:** See Guidance.md (Principle 2: Multi-Discipline Integration; Considerations: Coordination and Clash Resolution; Examples: Multi-Discipline Coordination Examples)
- **Verification:** See Procedure.md (Step 2.3: Discipline Coordination; Step 3.2: Interdisciplinary Check; Verification Method 4)

**FR-05: Revision Control**
- All drawings shall include revision tracking per project document control procedures
- Superseded revisions shall be clearly identified and archived
- **Source:** **ASSUMPTION** per document management best practice
- **Rationale:** See Guidance.md (Principle 4: Traceability and Configuration Control)
- **Verification:** See Procedure.md (Step 6: Configuration Management and Revisions)

### Performance Requirements

**PR-01: Drawing Quality**
- Drawings shall be legible, complete, and suitable for their intended use (construction reference, regulatory submittals, operations & maintenance)
- **Source:** **ASSUMPTION** per Employer's Requirements — **TBD** — **location TBD**

**PR-02: Drawing Format Standards**
- Drawing format, symbology, line weights, text sizes, and annotation standards shall comply with VFPA requirements
- **Source:** Decomposition DEL-31.01 (line 686); VFPA standards — **TBD** — **location TBD**

**PR-03: Coordinate System Accuracy**
- All drawings shall use a consistent project coordinate system
- Survey control points and benchmarks shall be clearly identified
- **Source:** **ASSUMPTION** per civil engineering practice; **TBD** — specific coordinate system per Employer's Requirements

**PR-04: Scale and Detail**
- Drawing scales shall be appropriate for the level of detail required
- **TBD** — Specific scale requirements per VFPA standards or Employer's Requirements

### Interface Requirements

**IR-01: Design Deliverable Integration**
- Record Design Drawings shall integrate outputs from all discipline-specific design drawing deliverables (DEL-04.01, DEL-05.01, DEL-06.01, DEL-07.01, DEL-08.01, DEL-09.01, DEL-10.01, DEL-11.01, DEL-12.01, DEL-13.01, DEL-14.01, DEL-15.01, DEL-16.01, DEL-17.01, DEL-18.01, DEL-19.01, DEL-20.01, DEL-23.01, DEL-24.01, DEL-25.01, DEL-26.01)
- **Source:** **ASSUMPTION** based on package structure; cross-reference to discipline drawing deliverables in Decomposition Section 4
- **Note:** See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)

**IR-02: Document Control Interface**
- Record Design Drawing Set shall interface with project document control system
- Drawing transmittals, registers, and approval records shall be maintained
- **Source:** **ASSUMPTION** per project management requirements

**IR-03: Regulatory Submittal Interface**
- Record Design Drawings shall be suitable for submission to regulatory authorities (VFPA, Transport Canada, Building Officials, etc.) as required
- **Source:** **ASSUMPTION** per regulatory compliance requirements; cross-reference to PKG-32 (Regulatory & Permits)

**IR-04: Operations & Maintenance Interface**
- Record Design Drawings shall serve as baseline reference for operation manuals (DEL-31.03) and maintenance manuals (DEL-31.04)
- **Source:** **ASSUMPTION** per OBJ-9 (Lifecycle Cost Optimization, Decomposition line 788)

### Quality Requirements

**QR-01: Quality Management System Compliance**
- All work shall comply with the project Quality Management Plan
- **Source:** **ASSUMPTION** per ISO 9001 requirements (Datasheet reference)

**QR-02: Drawing Checking and Review**
- All drawings shall undergo technical checking and independent review prior to approval
- Checker and reviewer qualifications shall meet project requirements
- **Source:** **ASSUMPTION** per engineering quality assurance practice

**QR-03: Drawing Approval Authority**
- Drawings shall be approved by authorized personnel per project procedures
- Approval signatures and dates shall be recorded on drawing title blocks
- **Source:** **ASSUMPTION** per document control practice

**QR-04: Audit Trail**
- Complete audit trail of drawing revisions, reviews, comments, and approvals shall be maintained
- **Source:** **ASSUMPTION** per quality management and traceability requirements

### Safety and Regulatory Requirements

**SR-01: Safe & Reliable Operation Support**
- Record Design Drawings shall support OBJ-1 (Safe & Reliable Operation) by accurately documenting design features related to safety systems, emergency response, and operational reliability
- **Source:** Decomposition Section 2, OBJ-1 (line 59); Objective Mapping (line 780)

**SR-02: Regulatory Compliance**
- Drawings shall comply with all applicable codes, standards, and regulatory requirements
- **Source:** OBJ-6 (Regulatory Compliance, Decomposition line 64); **TBD** — specific code/standard references per Employer's Requirements

**SR-03: Environmental Protection**
- Drawings shall document design features related to containment, spill prevention, and environmental controls per OBJ-7
- **Source:** OBJ-7 (Environmental Protection, Decomposition line 65)

### Lifecycle and Maintenance Requirements

**LR-01: Lifecycle Cost Optimization**
- Record Design Drawings shall support OBJ-9 (Lifecycle Cost Optimization) by providing accurate baseline documentation for future operations, maintenance, modifications, and expansions
- **Source:** Decomposition Section 2, OBJ-9 (line 67); Objective Mapping (line 788)

**LR-02: Future Expandability Documentation**
- Drawings shall document provisions for Phase 2 expansion per OBJ-8
- **Source:** OBJ-8 (Future Expandability, Decomposition line 66)

## Standards

**Applicable codes and standards (Project Delivery discipline):**

- **VFPA (Vancouver Fraser Port Authority) Drawing Standards** — **TBD** — **location TBD**
- **ISO 9001:2015** — Quality Management Systems
- **ISO 14001** — Environmental Management Systems
- **ISO 45001** — Occupational Health and Safety Management Systems
- **CAD Standards** — **TBD** — Project-specific CAD standards and layer naming conventions
- **Employer's Requirements** — Volumes 2 Part 1, 2, 3 (project-specific requirements) — **TBD** — **location TBD**

**Source:** Datasheet References; **ASSUMPTION** per Project Delivery discipline context

**Additional applicable standards (discipline-specific):**
- Each discipline's drawings shall comply with discipline-specific codes and standards as identified in respective package specifications (PKG-04 through PKG-26)
- **Source:** **ASSUMPTION** based on multi-discipline project scope

## Verification

**Verification methods for Drawing Set deliverables:**

1. **Technical Accuracy Review**
   - Independent technical review by qualified checker
   - Verification of calculations, design assumptions, and technical content
   - **Source:** **ASSUMPTION** per engineering QA/QC practice

2. **Completeness Check**
   - Verification that all required drawings are included
   - Cross-check against drawing register and deliverable requirements
   - **Source:** **ASSUMPTION** per document control practice

3. **Format and Standards Compliance**
   - Review for compliance with VFPA drawing standards
   - Check symbology, annotations, title blocks, scales, coordinate systems
   - **Source:** Requirement FR-03, PR-02

4. **Multi-Discipline Coordination Review**
   - Clash detection and coordination verification
   - Interface point confirmation
   - **Source:** Requirement FR-04

5. **Stakeholder Review**
   - Internal design review (D&B Contractor team)
   - Employer review and approval (as required per contract)
   - Regulatory authority review (as required for permitting)
   - **Source:** **ASSUMPTION** per contract requirements — **TBD** — specific approval authorities per Employer's Requirements

**Acceptance criteria:**

- All technical review comments resolved and closed
- Checker and approver sign-offs obtained
- Drawings issued with "Approved for Construction" or equivalent status
- Compliance with VFPA standards confirmed
- Employer acceptance obtained (if required per contract)
- **Source:** **ASSUMPTION** per project quality procedures — **TBD** — specific acceptance criteria per Employer's Requirements

## Documentation

**Required documentation outputs:**

1. **Record Design Drawings:**
   - Electronic format (CAD native files and PDF)
   - Hard copy sets (if required)
   - **Source:** Decomposition DEL-31.01 (line 686); **ASSUMPTION** per standard practice

2. **Drawing Register:**
   - Comprehensive list of all drawings with drawing numbers, titles, revisions, dates
   - **Source:** **ASSUMPTION** per document control requirements

3. **Drawing Transmittals:**
   - Transmittal records for all drawing submissions and approvals
   - **Source:** **ASSUMPTION** per document control practice

4. **Revision History:**
   - Record of all drawing revisions with change descriptions
   - **Source:** Requirement FR-05

**Documentation requirements:**

- All documents shall comply with project document control procedures
- Revision control per project numbering system — **TBD**
- Format: **ASSUMPTION**: Per project document management requirements and VFPA standards
- Electronic records managed in project document management system — **TBD** — **location TBD**
- Retention requirements: **TBD** — Per Employer's Requirements and regulatory requirements

**Filing and Archiving:**
- Working documents in `1_Working/` folder
- Review packages in `2_Checking/To/` (during review)
- Issued documents in `3_Issued/` (upon approval)
- **Source:** README.md (Section: "How to use the framework")
