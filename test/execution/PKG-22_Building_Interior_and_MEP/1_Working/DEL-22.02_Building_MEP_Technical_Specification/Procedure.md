# Procedure: DEL-22.02 Building MEP Technical Specification

## Purpose

This procedure defines the process for producing and managing **Building MEP Technical Specification** within **PKG-22 Building Interior & MEP**.

**Deliverable Purpose:** Defines performance, materials, and workmanship requirements for building MEP per Employer's Requirements.

**Source:** Decomposition REVISED_v2.md, DEL-22.02 entry; _CONTEXT.md

This procedure covers the workflow to produce technical specifications that support DEL-22.01 drawings and define procurement, installation, and testing requirements for MEP systems.

**Deliverable Classification:**
- **Type:** Specification
- **Responsible Party:** D&B Contractor

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`)

**Source:** _DEPENDENCIES.md

**Required Inputs** (ASSUMPTION: typical specification inputs):

1. **DEL-22.01 Building MEP Design Drawing Set** — Drawings define what equipment and systems must be specified
2. **DEL-22.03 Building MEP Design Calculations** — Calculations provide equipment sizing and performance requirements
3. **Employer's Requirements** — **TBD** — Project-specific requirements and standards (location TBD)
4. **Applicable Codes and Standards** — NBC 2020, ASHRAE, NFPA 13, CSA B64, CEC, etc. (see Specification.md Standards section)
5. **Project Specification Standards** — **TBD** — Specification format template and writing standards (location TBD)

**Source:** Specification.md Interface Requirements; Datasheet.md applicable standards

### Reference Materials

- See `_REFERENCES.md` for applicable reference documents
- See `execution/PKG-22_Building_Interior_and_MEP/0_References/` for reference materials
- Employer's Requirements Volume 2 — **TBD** (location TBD)
- Code and standard documents listed in Datasheet.md References section

**Source:** _REFERENCES.md; Datasheet.md

### Personnel Requirements

**ASSUMPTION**: Typical specification writer qualifications:

| Role | Qualification |
|------|--------------|
| Lead Specification Writer | Professional Engineer (P.Eng.) or experienced specification professional; MEP experience |
| Technical Reviewers | Discipline engineers for each MEP system (HVAC, plumbing, fire protection, electrical) |
| Coordination Reviewer | IDC Coordinator experienced in multi-discipline coordination |

**Professional Seal**: Specification may require P.Eng. BC seal per contract or NBC 2020 requirements—**TBD**.

**Source:** Specification.md QR-02; ASSUMPTION: standard qualifications

### Tools and Software

**Required Software** (ASSUMPTION):
- Word processing software (MS Word or similar)
- Specification management software (if used by project)
- Document control system (for review and approval workflow)

**Source:** ASSUMPTION: standard specification writing tools

## Steps

### Step 1: Specification Planning and Format Selection

**Objective**: Establish specification structure before writing begins.

**Requirements Addressed**: Specification.md PR-01 (Specification Format and Organization)

**Activities**:

1.1. **Confirm Specification Format**:
   - Identify project specification format standard (CSI MasterFormat or alternative) — **TBD** (location TBD)
   - Obtain specification section templates per project standards
   - Confirm section numbering system

1.2. **Develop Specification Outline**:
   - List required specification sections for HVAC, Plumbing, Fire Suppression (and Electrical if required)
   - Example HVAC sections: 23 05 00 Common Work, 23 07 00 Insulation, 23 31 00 Ducts, 23 74 00 Rooftop Units, etc.
   - Cross-reference with DEL-22.01 drawings to ensure all equipment/systems are covered

1.3. **Identify Standards and References**:
   - Compile list of applicable codes and standards per Datasheet.md References section
   - Obtain copies of referenced standards for specification writing
   - Document standard editions to be referenced

**Verification**: Specification outline reviewed and approved by discipline lead.

**Source:** Specification.md PR-01, FR-02; Datasheet.md specification sections

### Step 2: Requirements Gathering and Coordination

**Objective**: Gather all technical requirements before writing specification text.

**Requirements Addressed**: Specification.md FR-02 (Standards Compliance), FR-03 (Performance Criteria), IF-01 through IF-05 (Interface Requirements)

**Activities**:

2.1. **Review Design Documents**:
   - Review DEL-22.01 drawings for equipment types, sizes, locations
   - Review DEL-22.03 calculations for equipment sizing basis and performance requirements
   - Identify equipment to be specified and performance criteria

2.2. **Review Employer's Requirements**:
   - Extract MEP-specific requirements from Employer's Requirements — **TBD** (location TBD)
   - Document project-specific material preferences or restrictions
   - Identify specified manufacturers or equipment standards

2.3. **Coordination Meetings**:
   - Meet with HVAC, plumbing, fire protection (and electrical) designers to confirm requirements
   - Coordinate with PKG-19 (Control Systems) for control interfaces
   - Coordinate with PKG-17 (Electrical Power) for electrical requirements
   - Coordinate with PKG-21 (Building Structures) for structural support requirements

2.4. **Manufacturer Research**:
   - Identify acceptable manufacturers for major equipment
   - Confirm product availability and lead times
   - Obtain representative product data for reference (preliminary DEL-22.04 information)

**Verification**: Requirements list and coordination notes documented and approved.

**Source:** Specification.md Requirements section; Guidance.md Considerations

### Step 3: Specification Writing (Draft Development)

**Objective**: Write specification text for all required sections.

**Requirements Addressed**: All Functional Requirements (FR-01 through FR-08) from Specification.md

**Activities**:

3.1. **Write General (Part 1) Sections**:
   - Section scope and description
   - Related sections (cross-references)
   - References (codes and standards)
   - Submittals (shop drawings per DEL-22.06, product data per DEL-22.04, test reports per DEL-22.05) — **FR-07**
   - Quality assurance (qualifications, testing requirements) — **FR-08**

3.2. **Write Products (Part 2) Sections**:
   - Materials specifications (types, standards, properties) — **FR-04**
   - Equipment specifications (performance, manufacturers, models) — **FR-05**
   - Fabrication requirements
   - Source quality control (factory testing)

3.3. **Write Execution (Part 3) Sections**:
   - Installation requirements and methods — **FR-06**
   - Field quality control (testing, inspections) — **FR-08**
   - Startup and commissioning — **FR-08**
   - Cleaning, protection, warranties

3.4. **Incorporate Performance Criteria**:
   - Equipment capacities per DEL-22.03 calculations — **FR-03**
   - Energy efficiency per ASHRAE 90.1 — **FR-03**
   - Fire suppression coverage and hydraulic performance per NFPA 13 — **FR-03**

3.5. **Define Interface Requirements**:
   - Controls interfaces to PKG-19 (BAS integration) — **IF-04**
   - Electrical power requirements to PKG-17 (voltage, amps, disconnects) — **IF-05**
   - Structural support requirements to PKG-21 — **FR-06**

**Verification**: Draft specifications complete for all required sections per outline from Step 1.

**Source:** Specification.md FR-01 through FR-08; Datasheet.md typical section structure

### Step 4: Review and Coordination

**Objective**: Review specifications for technical adequacy, coordination, and quality before issue.

**Requirements Addressed**: Specification.md QR-01 (Specification Review and Approval), IF-01 through IF-03 (coordination with related deliverables)

**Activities**:

4.1. **Internal Technical Review**:
   - Each MEP discipline (HVAC, plumbing, fire, electrical) reviews respective sections
   - Verify technical adequacy and code compliance — Specification.md FR-02
   - Verify specifications are constructible — Specification.md PR-02
   - Document review comments

4.2. **Coordination Checks**:
   - **Drawings Coordination (IF-01)**: Verify specifications match DEL-22.01 drawings (no contradictions, all equipment specified)
   - **Calculations Coordination (IF-02)**: Verify equipment sizing matches DEL-22.03 calculations
   - **Datasheets Coordination (IF-03)**: Verify equipment selections match DEL-22.04 datasheets (may be preliminary at this stage)
   - **Interdisciplinary Coordination**: IDC review across all MEP disciplines and with PKG-17, PKG-19, PKG-21

4.3. **Constructability Review**:
   - If construction team available, review for constructability
   - Verify installation methods are practical and safe
   - Verify material availability and lead times

4.4. **Format and Writing Quality Review**:
   - Verify specification format per project standards — Specification.md PR-01
   - Verify clear, imperative language ("shall") — Specification.md PR-02
   - Verify no internal contradictions — Specification.md PR-02
   - Verify consistent terminology across all sections

**Verification**: All review comments documented and addressed; approval signatures obtained.

**Source:** Specification.md QR-01, IF-01 through IF-03, PR-01, PR-02

### Step 5: Finalization and Issue

**Objective**: Finalize specifications for issue to construction.

**Requirements Addressed**: Specification.md QR-02 (Professional Responsibility)

**Activities**:

5.1. **Incorporate Review Comments**:
   - Revise specifications per review comments
   - Re-verify coordination items if significant changes made
   - Obtain re-approval if major revisions

5.2. **Professional Review and Seal (if required)**:
   - Submit to Professional Engineer (P.Eng. BC) for review if required — Specification.md QR-02
   - Engineer reviews for professional standard of care and code compliance
   - Engineer applies seal and signature if required by contract or NBC 2020

5.3. **Final Quality Check**:
   - Verify all sections complete per outline
   - Verify all cross-references correct
   - Verify document formatting and pagination correct
   - Verify revision status and document control information complete

5.4. **Issue Process**:
   - Export to PDF per project standards
   - Submit to project document control for distribution
   - File issued copy in `3_Issued/` folder
   - Update `_STATUS.md` to ISSUED with date and revision

**Verification**: Specifications issued with all required approvals and professional seal (if required).

**Source:** Specification.md QR-02; standard document issuance process

### Step 6: Construction Support and Updates

**Objective**: Support construction phase and maintain specifications current.

**Activities**:

6.1. **RFI Response**:
   - Respond to contractor Requests for Information regarding specification interpretation
   - Issue clarifications or revised specification sections if needed
   - Maintain revision control

6.2. **Substitution Requests**:
   - Review contractor-proposed substitutions for "or approved equal" items
   - Verify proposed products meet performance and quality requirements
   - Approve or reject with justification; issue addenda if approved

6.3. **Specification Revisions**:
   - Issue revised specifications for significant changes or clarifications
   - Coordinate revisions with DEL-22.01 drawings if affected
   - Maintain revision history

6.4. **Closeout Updates**:
   - Update specifications to reflect approved substitutions and field changes
   - Coordinate with DEL-22.05 installation records and DEL-22.06 shop drawings for as-built conditions
   - Issue final revised specifications for owner's record

**Verification**: All RFIs and substitutions addressed; final specifications issued for record.

**Source:** ASSUMPTION: standard construction support process

## Verification

### Quality Control Checkpoints

**Completeness (per FR-01)**:
- [ ] All equipment shown on DEL-22.01 drawings is specified
- [ ] All required specification sections per outline are present
- [ ] All submittals, testing, and warranty requirements defined

**Standards Compliance (per FR-02)**:
- [ ] All applicable codes and standards correctly referenced
- [ ] NBC 2020 requirements addressed
- [ ] ASHRAE 90.1, NFPA 13, CSA B64, CEC requirements addressed (as applicable)

**Performance Criteria (per FR-03)**:
- [ ] Equipment capacities match DEL-22.03 calculations
- [ ] Energy efficiency requirements per ASHRAE 90.1 included
- [ ] Fire suppression performance per NFPA 13 included

**Coordination (per IF-01 through IF-05)**:
- [ ] No contradictions with DEL-22.01 drawings
- [ ] Equipment sizing supported by DEL-22.03 calculations
- [ ] Equipment selections consistent with DEL-22.04 datasheets
- [ ] Controls interfaces coordinated with PKG-19
- [ ] Electrical requirements coordinated with PKG-17

**Quality (per PR-01, PR-02, QR-01, QR-02)**:
- [ ] Specification format per project standards
- [ ] Clear, imperative language used
- [ ] No internal contradictions
- [ ] All reviews completed and documented
- [ ] Professional seal applied (if required)

**Source:** Specification.md Requirements and Verification sections

## Records

### Documentation Outputs

**Primary Deliverable** (per Decomposition DEL-22.02):
- **HVAC specification**
- **Building plumbing specification**
- **Fire suppression specification**
- **Electrical building services specification** (if required) — **TBD**

**Source:** Decomposition REVISED_v2.md, DEL-22.02 anticipated artifacts

**Supporting Documentation**:
- Specification outline (section list)
- Requirements list and coordination notes
- Review comments and resolution log
- Professional seal documentation (if applicable)

**Source:** ASSUMPTION: standard specification development records

### Record Management

**File Storage Locations**:

| Stage | Location | Contents |
|-------|----------|----------|
| Working | `1_Working/` | Draft specifications, work-in-progress |
| Checking | `2_Checking/To/` | Copies submitted for review (with DEL-ID + date + rev) |
| Issued | `3_Issued/` | Issued-for-construction specifications (PDF) |

**Source:** README.md Section 6 (review and issue conventions)

**Version Control**:
- All revisions tracked in document control system
- Revision history maintained per project procedures
- Addenda and clarifications tracked

**Retention Requirements**:
- Working files: Retain through project closeout, archive per project procedures
- Issued specifications: Retain in project archives per company and regulatory requirements — **TBD** (retention period per project records management plan)

**Source:** ASSUMPTION: standard document control and records management
