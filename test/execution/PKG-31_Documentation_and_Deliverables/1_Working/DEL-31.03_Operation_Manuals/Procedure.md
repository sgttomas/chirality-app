# Procedure: DEL-31.03 Operation Manuals

## Purpose

This procedure defines the process for producing and managing **Operation Manuals** within **PKG-31 Documentation & Deliverables**.

**Objective:**
To produce comprehensive, accurate, and user-friendly Operation Manuals that enable safe and effective operation of the Canola Oil Transload Facility Phase 1.

**Source:** Decomposition DEL-31.03 (line 688); _CONTEXT.md

**Deliverable type:** Manual
**Responsible party:** D&B Contractor

## Prerequisites

### Dependencies

**Dependency Tracking:**
- See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies coordinated externally

**Upstream Dependencies (logical workflow):**
- As-Built Drawings (DEL-31.02) — configuration baseline
- Commissioning Records (PKG-30) — validated operating parameters and procedures
- Control System Design (DEL-19.01) — control logic and HMI design
- Design specifications and calculations from discipline packages
- **Source:** **ASSUMPTION** based on logical workflow; Specification IR-01, IR-04, IR-06

**Downstream Uses:**
- Operations personnel — day-to-day facility operations
- Training programs — operator training and competency development
- Maintenance Manuals (DEL-31.04) — interface reference
- **Source:** **ASSUMPTION** based on operations lifecycle

### Reference Materials

**Required Inputs:**
- As-Built Drawings (DEL-31.02) — P&IDs, layouts, electrical one-lines, control diagrams
- Commissioning test procedures and results (PKG-30)
- Control system documentation (DEL-19.01, PKG-19) — control logic, HMI screens, alarm lists
- Vendor documentation (DEL-31.05) — equipment operation manuals
- Asset Hierarchy (DEL-31.06) — equipment tagging
- Design specifications from discipline packages (PKG-10 through PKG-26)
- Employer's Requirements — **TBD** — **location TBD**
- Applicable standards (ISO 9001, ISO 14001, ISO 45001, API, NFPA) — **TBD**
- **Source:** Specification (Interface Requirements section); **ASSUMPTION** per typical operation manual inputs

**Reference Materials Location:**
- See `_REFERENCES.md`
- See `0_References/` in package directory

### Personnel Requirements

**Roles:**
1. **Operations Manual Coordinator:** Overall responsibility for manual production
2. **Technical Writers / Documentation Specialists:** Manual development and writing
3. **Subject Matter Experts (SMEs):** Process engineers, discipline engineers, control systems engineers for technical content
4. **Operations Personnel / SMEs:** Operations review and field verification
5. **HSE Personnel:** Safety content review
6. **Approvers:** Project Manager, Chief Engineer, Operations Manager (as applicable)

**Source:** **ASSUMPTION** per typical manual development team; Specification QR-02

### Tools and Systems

- Word processing software (e.g., Microsoft Word, Adobe InDesign)
- Drawing/diagram tools for procedure flowcharts and system diagrams
- Access to As-Built Drawings and design documentation
- Access to control system for HMI screenshots
- Document management system
- **Source:** **ASSUMPTION** per documentation development IT requirements

## Steps

### Step 1: Planning and Scoping

**Objective:** Establish the operation manual scope, structure, and production plan.

**Activities:**

1.1. **Develop Operation Manual Outline:**
   - Identify all facility systems requiring operation manuals
   - Define manual structure (one comprehensive manual vs. multiple system manuals)
   - Create table of contents for each manual (system description, normal operations, emergency operations, troubleshooting, etc.)
   - **Source:** Specification FR-01; **ASSUMPTION** per documentation planning

1.2. **Coordinate with Stakeholders:**
   - Engage operations personnel (or operations SMEs) to understand operating philosophy and priorities
   - Coordinate with maintenance manual team (DEL-31.04) to define operations vs. maintenance scope boundaries
   - Coordinate with HSE for safety requirements and emergency procedures
   - **Source:** Specification IR-02, QR-02; **ASSUMPTION** per stakeholder coordination

1.3. **Develop Production Schedule:**
   - Align manual development with commissioning schedule (to enable field verification)
   - Allocate resources (technical writers, SMEs, reviewers)
   - Establish milestones (draft complete, review complete, field verification, final issuance)
   - **Source:** **ASSUMPTION** per project scheduling

**Deliverables:** Operation Manual Outline, Production Schedule

**Verification:** Outline approved by Operations Manual Coordinator and stakeholders

### Step 2: Gather Reference Information

**Objective:** Collect all reference materials needed for manual development.

**Activities:**

2.1. **Obtain Design Documentation:**
   - Obtain design specifications, calculations, and design basis documents from discipline packages
   - **Source:** **ASSUMPTION** per documentation collection

2.2. **Obtain As-Built Drawings:**
   - Obtain As-Built Drawings (DEL-31.02) — P&IDs, layouts, control diagrams
   - **Source:** Specification IR-01; cross-reference DEL-31.02

2.3. **Coordinate with Maintenance Manuals:**
   - Review maintenance manual scope (DEL-31.04) to clarify operations vs. maintenance boundaries
   - **Source:** Specification IR-02; cross-reference DEL-31.04

2.4. **Obtain Vendor Documentation:**
   - Obtain vendor operation manuals (DEL-31.05) for equipment-specific information
   - **Source:** Specification IR-03; cross-reference DEL-31.05

2.5. **Obtain Control System Documentation:**
   - Obtain control system documentation (DEL-19.01, PKG-19) — control logic, HMI screens, alarm lists
   - Arrange access to control system for HMI screenshots
   - **Source:** Specification IR-04; cross-reference DEL-19.01, PKG-19

2.6. **Obtain Commissioning Records:**
   - Obtain commissioning test procedures and results (PKG-30) — validated operating parameters, setpoints, procedures
   - **Source:** Specification IR-06; cross-reference PKG-30

2.7. **Review Asset Hierarchy:**
   - Obtain Asset Hierarchy (DEL-31.06) for equipment tagging and nomenclature
   - **Source:** Specification IR-05; cross-reference DEL-31.06

**Deliverables:** Reference materials compiled and organized

**Verification:** All required reference materials obtained

### Step 3: Develop Manual Content

**Objective:** Write operation manual content (system descriptions, procedures, safety information, troubleshooting).

**Activities:**

3.1. **Operating Procedures Development:**
   - Write normal operating procedures (start-up, steady-state operation, shutdown) for each system
   - Write emergency operating procedures (ESD, spill response, fire response, equipment failure)
   - Write mode transition procedures (rail-to-tank, tank-to-ship, direct rail-to-ship)
   - Include prerequisites, initial conditions, step-by-step instructions, expected outcomes
   - **Source:** Specification FR-01, FR-05, SR-03; **ASSUMPTION** per procedure development

3.2. **Safety Content Review:**
   - Identify hazards for each system and procedure (process hazards, physical hazards, environmental hazards)
   - Integrate risk mitigation steps into procedures
   - Add prominent cautions and warnings
   - Develop emergency procedure quick-reference sections
   - **Source:** Specification FR-04, SR-01, SR-03

3.3. **Procedure Quality Check:**
   - Verify procedures are complete, accurate, and step-by-step
   - Verify critical steps and cautions are clearly identified
   - Verify prerequisites and expected outcomes are stated
   - **Source:** Specification PR-01

3.4. **Format and Usability Check:**
   - Apply consistent formatting, numbering, and structure
   - Add visual aids (P&IDs, flowcharts, photographs, diagrams) where beneficial
   - Ensure clear, concise language appropriate for operations personnel
   - **Source:** Specification FR-03, PR-02

**Deliverables:** Draft Operation Manuals (all systems)

**Verification:** Draft manuals complete per outline; formatting and usability checked

### Step 4: Field Verification and Validation

**Objective:** Verify procedures against actual facility conditions and commissioning results.

**Activities:**

4.1. **Drawing References Check:**
   - Cross-check system descriptions and procedures against As-Built Drawings (DEL-31.02)
   - Verify P&ID references, valve numbers, equipment tags
   - **Source:** Specification IR-01

4.2. **Field Verification:**
   - Walk down procedures during commissioning or initial operations to verify accuracy
   - Verify operating parameters, setpoints, and control sequences against commissioning results (PKG-30)
   - Verify HMI operation and alarm responses
   - Document any discrepancies for correction
   - **Source:** Specification FR-02, IR-06; Verification method 6

4.3. **Asset Tag Verification:**
   - Verify equipment tags and identifiers align with Asset Hierarchy (DEL-31.06)
   - **Source:** Specification IR-05

4.4. **Update Manuals Based on Field Verification:**
   - Incorporate field verification findings and corrections
   - **Source:** **ASSUMPTION** per field verification process

**Deliverables:** Field-verified Operation Manuals

**Verification:** Field verification completed and sign-offs obtained; discrepancies corrected

### Step 5: Technical Review and Validation

**Objective:** Conduct technical, HSE, and operations personnel review of operation manuals.

**Activities:**

5.1. **Technical Review:**
   - Technical review by qualified engineers and SMEs (process, mechanical, electrical, control systems)
   - Verify technical accuracy, completeness, and procedure correctness
   - Review comments documented and tracked
   - **Source:** Specification QR-02; Verification method 2

5.2. **HSE Review:**
   - HSE review of hazard identification, safety precautions, and emergency procedures
   - Verify safety content adequacy and regulatory compliance
   - **Source:** Specification QR-02, SR-01, SR-02; Verification method 3

5.3. **Operations Personnel Review:**
   - Review by operations personnel (or operations SMEs) for usability, practicality, and completeness
   - Operations personnel confirm manuals are understandable and usable
   - **Source:** Specification QR-02, LR-01; Verification method 4

5.4. **Comment Resolution:**
   - Address all review comments
   - Comments closed out when resolution confirmed
   - Manuals revised as needed
   - **Source:** **ASSUMPTION** per review cycle management

5.5. **Final Approval:**
   - Authorized approver (e.g., Operations Manager, Project Manager) provides final approval sign-off
   - Approval recorded per document control procedures
   - **Source:** Specification QR-03

**Deliverables:** Reviewed and approved Operation Manuals; comment tracking log

**Verification:** All reviewers sign off; all comments resolved; approver sign-off obtained

### Step 6: Completeness Review

**Objective:** Verify operation manual set is complete and ready for issuance.

**Activities:**

6.1. **Completeness Verification:**
   - Verify all facility systems covered per manual outline
   - Verify all required procedures included (normal, emergency, troubleshooting)
   - Cross-check against As-Built Drawings and system list
   - **Source:** Specification FR-01; Verification method 1

6.2. **Employer Acceptance (if required):**
   - Submit operation manuals to Employer for review and acceptance per contract requirements
   - Address Employer comments if any
   - **Source:** Specification QR-03; **TBD** — Employer review requirements per contract

6.3. **Final QA Check:**
   - Final quality assurance check for formatting, consistency, completeness
   - **Source:** **ASSUMPTION** per QA final checks

**Deliverables:** Complete Operation Manual Set (verified for completeness)

**Verification:** Completeness confirmed; Employer acceptance obtained (if required)

### Step 7: Issuance and Handover

**Objective:** Issue operation manuals and handover to operations personnel.

**Activities:**

7.1. **Prepare Deliverables:**
   - Prepare electronic format (PDF, searchable)
   - Prepare hard copy sets (printed manuals, binders) as required
   - Prepare operation manual master index and procedures index
   - **Source:** Specification (Documentation section)

7.2. **Distribution:**
   - Distribute operation manuals to control room, operations offices, training department
   - Upload to project document management system
   - Transmit to Employer per contract requirements
   - **Source:** Specification PR-03

7.3. **Configuration Management:**
   - Place issued manuals in `3_Issued/` folder
   - Establish change management process for future updates
   - Assign responsibility for manual maintenance and updates during operations
   - **Source:** Specification QR-04; README.md

7.4. **Training Support:**
   - Coordinate with training department to incorporate operation manuals into operator training programs
   - **Source:** Specification LR-02

**Deliverables:** Issued Operation Manuals; distribution confirmed

**Verification:** Distribution complete; document management system updated; handover to operations complete

## Verification

**Verification methods applied throughout procedure:**

1. **Completeness Review** (Step 6.1) — All systems and procedures covered
2. **Technical Review** (Step 5.1) — Technical accuracy verified
3. **HSE Review** (Step 5.2) — Safety content approved
4. **Operations Personnel Review** (Step 5.3) — Usability confirmed
5. **Format and Standards Compliance** (Step 3.4) — Standards verified
6. **Field Verification** (Step 4.2) — Procedures verified against facility conditions

**Overall Acceptance Criteria:**
- All facility systems covered
- Technical accuracy verified
- Safety content approved
- Operations personnel confirm usability
- Standards compliance confirmed
- Employer acceptance obtained (if required)

**Source:** Specification (Verification section)

## Records

**Documentation outputs:**

1. **System Operation Manuals** (electronic and hard copy)
2. **Operation Manual Master Index**
3. **Operations Procedures Index**
4. **Review and Approval Records** (technical, HSE, operations, approver sign-offs)
5. **Field Verification Records**

**Record management:**

- Working documents in `1_Working/`
- Review packages in `2_Checking/To/`
- Issued manuals in `3_Issued/`
- Copies in control room, operations offices, document management system
- Retention: For facility operational life

**Source:** README.md; Specification (Documentation section)
