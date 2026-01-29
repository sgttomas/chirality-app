# Procedure: DEL-29.01 Test Procedures

## Purpose

This procedure defines the process for developing, reviewing, approving, and managing **Test Procedures** within **PKG-29 Testing**.

**Deliverable Purpose:** Defines the execution method and controls for test to meet safety, quality, and operational requirements. **Source:** Decomposition line 646

**Note on Dual-Use Nature:** This Procedure document describes the process for *producing* the test procedure deliverables. The test procedures themselves (Hydrostatic, Electrical, I&C) will contain their own procedural steps for *executing* tests. **ASSUMPTION**

**Deliverable Type:** Procedure
**Responsible Party:** D&B Contractor (QA/QC)
**Discipline:** T&C

**Source:** _CONTEXT.md

## Prerequisites

### Dependencies

**Dependency Tracking:** See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

**Upstream Deliverable Requirements:**

The following design deliverables should be at an appropriate maturity level before test procedures can be finalized:

- **PKG-13 (Storage Tanks):** Tank design drawings, specifications, and calculations provide basis for tank hydrostatic test requirements
- **PKG-14 (Process Piping):** Piping design drawings, specifications, and pressure class information provide basis for piping hydrostatic test requirements
- **PKG-17 (Electrical Power Distribution):** Electrical single-line diagrams, equipment specifications, protection coordination study provide basis for electrical test requirements
- **PKG-19 (Control Systems):** I&C drawings, loop diagrams, instrument specifications, control philosophy provide basis for I&C test requirements

**ASSUMPTION:** Typical EPC project sequencing where design precedes test procedure development

**Note:** Test procedures may be developed progressively as design matures. Early draft procedures can be prepared based on preliminary design and refined when final design is available.

### Reference Materials

**Required Inputs:**

From `_REFERENCES.md` and package `0_References/` folder:
- Employer's Requirements (Volume 2 Parts 1-3) **location TBD**
- Applicable codes and standards (see Specification.md for full list)
- Design drawings and specifications (as they become available)
- Equipment vendor manuals and test requirements
- Project Quality Management Plan **location TBD**
- Project HSE Management Plan **location TBD**
- Inspection and Test Plan (DEL-29.02) — for hold/witness point integration

**Industry Standards (for procedure format and content guidance):**
- ASME B31.3: Process Piping (Appendix K: Non-mandatory Rules for Hydrostatic Testing)
- API 650: Welded Tanks for Oil Storage (Section 7: Inspection and Testing)
- IEC 62382: Electrical and instrumentation loop check
- NFPA 70E: Standard for Electrical Safety in the Workplace **ASSUMPTION**

**Source:** Referenced standards in Datasheet.md and Specification.md

### Personnel Requirements

**Procedure Development Team:**
- Lead: QA/QC Manager or designated Test Engineer
- Technical Input: Discipline engineers (Process, Structural, Electrical, I&C) as applicable
- Review: HSE personnel, Operations representative (if available), Construction Manager
- Approval: D&B Contractor QA/QC Manager (or per project authority matrix) **TBD**

**Qualifications:**
- Test procedure authors should have relevant discipline expertise and prior testing experience **ASSUMPTION**
- Reviewers should have competency in their respective areas
- **TBD** — Specific qualification/certification requirements per project quality plan

### Tools and Resources

- Project document management system for procedure storage and revision control
- Procedure templates (if available from project or D&B Contractor standards)
- Access to design documentation (drawings, specifications, calculations)
- Access to codes and standards (printed or electronic)

**TBD** — Specific software tools for procedure authoring

## Steps

### Step 1: Identify Testing Requirements

**Objective:** Determine what tests are required for the project systems and equipment.

**Activities:**
1.1. Review design documentation to identify all pressure systems, electrical equipment, and instrumentation requiring testing

1.2. Review applicable codes and standards to identify mandatory test requirements:
   - Pressure systems: ASME B31.3, API 650, CSA Z662
   - Electrical systems: NFPA 70, IEEE standards
   - I&C systems: IEC 62382, manufacturer requirements

1.3. Review Employer's Requirements for project-specific test requirements **location TBD**

1.4. Review DEL-29.02 (Inspection and Test Plan) to identify testing scope and hold/witness points

1.5. Coordinate with discipline engineers to confirm test requirements and priorities

**Outputs:**
- Testing requirements list (by system or equipment)
- Identification of test types needed (hydrostatic, electrical, I&C)

**ASSUMPTION:** Requirements identification is an iterative process that refines as design matures.

### Step 2: Develop Test Procedure Content

**Objective:** Author detailed test procedures with all required elements.

**Activities:**

2.1. **For each test procedure, develop the following sections:**

   **A. Procedure Header:**
   - Procedure title and number
   - Revision and date
   - System or equipment identification
   - Applicable drawings and specifications
   - Approval signatures

   **B. Scope and Objectives:**
   - What is being tested
   - What the test is intended to verify
   - Applicable codes/standards

   **C. References:**
   - Design drawings
   - Specifications
   - Codes and standards
   - Related procedures

   **D. Equipment and Materials:**
   - Test equipment required (pumps, gages, meggers, calibrators, etc.)
   - Test medium (water, compressed air, etc.)
   - Instrumentation and calibration requirements
   - Support equipment (scaffolding, lighting, communication)

   **E. Personnel and Qualifications:**
   - Roles and responsibilities (test leader, technicians, QC inspector, witness)
   - Required qualifications/certifications
   - Minimum manning requirements

   **F. Safety Requirements:**
   - Hazard identification and risk assessment (or reference to JSA)
   - Required PPE
   - Isolation and lockout/tagout requirements
   - Emergency response and communication
   - Environmental controls (spill containment, water discharge)

   **G. Prerequisites:**
   - System completion requirements (punch list items that must be closed)
   - Prior inspections or tests that must be complete
   - Required permits or approvals
   - Weather/environmental conditions (if applicable)
   - Utility availability (water, power, compressed air)

   **H. Procedure Steps:**
   - Detailed step-by-step test execution sequence
   - Hold points and witness points (from DEL-29.02)
   - Inspection requirements during and after test
   - Data recording requirements
   - Clear pass/fail criteria for each step

   **I. Acceptance Criteria:**
   - Quantitative criteria (pressure drop limits, insulation resistance values, etc.)
   - Qualitative criteria (no visible leakage, no alarms, etc.)
   - Reference to code requirements or specifications

   **J. Records and Documentation:**
   - Test data sheets and forms (to be completed during test)
   - Photographic documentation requirements
   - Non-conformance reporting process
   - Test record filing (cross-reference to DEL-29.03)

2.2. Use procedure templates if available from project or D&B Contractor standards

2.3. Include all relevant forms, checklists, and data sheets as appendices

2.4. Ensure procedure language is clear, concise, and action-oriented (imperative voice)

**Outputs:**
- Draft test procedures (one for each test type or system)

**Source:** Procedure content requirements from Specification.md Section FR-1; typical EPC procedure structure **ASSUMPTION**

### Step 3: Integrate Hold and Witness Points

**Objective:** Ensure test procedures align with project Inspection and Test Plan.

**Activities:**

3.1. Review DEL-29.02 (Inspection and Test Plan With Hold/Witness Points) to identify all hold points and witness points applicable to testing activities

3.2. Incorporate hold points into test procedures:
   - Identify procedure step where hold point occurs
   - Specify who must release the hold (QC inspector, Engineer, Employer representative)
   - Provide sign-off block in procedure

3.3. Incorporate witness points into test procedures:
   - Identify procedure step where witness is required
   - Specify who may witness (Employer, third-party inspector, regulatory authority)
   - Provide advance notification requirements
   - Provide sign-off block in procedure

3.4. Coordinate with project QA/QC and Employer representative to confirm hold/witness point requirements

**Outputs:**
- Test procedures with integrated hold/witness points

**Source:** Cross-reference to DEL-29.02, Specification.md Section FR-3

### Step 4: Conduct Safety Review

**Objective:** Identify and mitigate hazards associated with test execution.

**Activities:**

4.1. Conduct hazard identification for each test procedure:
   - Pressure hazards (stored energy, release)
   - Electrical hazards (shock, arc flash)
   - Physical hazards (height, confined space, heavy equipment)
   - Environmental hazards (water discharge, chemical exposure)

4.2. Develop or reference Job Safety Analysis (JSA) for each test type

4.3. Incorporate safety controls into procedure:
   - Isolation and lockout/tagout steps
   - PPE requirements
   - Atmospheric monitoring (if applicable)
   - Emergency response provisions
   - Communication and coordination requirements

4.4. Review procedures with HSE personnel and obtain HSE concurrence

4.5. Identify permit requirements (confined space entry, hot work, electrical work, etc.)

**Outputs:**
- Test procedures with safety requirements integrated
- JSA documents (or references to JSAs)
- HSE review and concurrence

**Source:** Specification.md Section QR-2; general EPC HSE practice **ASSUMPTION**

### Step 5: Conduct Technical Review

**Objective:** Verify test procedures are technically sound and constructible.

**Activities:**

5.1. Distribute draft procedures for multi-discipline review:
   - **Engineering review:** Verify procedures align with design intent and code requirements
   - **QA/QC review:** Verify procedures meet project quality standards
   - **Construction review:** Verify procedures are practical and executable in the field
   - **Operations review (if available):** Verify procedures consider operability and future maintenance

5.2. Consolidate review comments and conduct comment resolution meetings as needed

5.3. Revise procedures to address comments

5.4. Obtain reviewer sign-offs or concurrence

**Outputs:**
- Reviewed and revised test procedures
- Comment resolution record

**Source:** Specification.md Section VM-1

### Step 6: Conduct Procedure Walkthrough

**Objective:** Validate procedure adequacy through tabletop or field walkthrough.

**Activities:**

6.1. Schedule walkthrough session with procedure users (test crew, inspectors)

6.2. Conduct tabletop walkthrough:
   - Step through procedure sequentially
   - Identify unclear or ambiguous steps
   - Verify all required equipment and resources are identified
   - Verify data sheets and forms are adequate
   - Discuss potential issues or challenges

6.3. For complex or high-risk tests, conduct field walkthrough at actual test location:
   - Verify physical access to test points
   - Verify utility connections are adequate
   - Identify any site-specific safety concerns
   - Verify communication and emergency egress

6.4. Incorporate walkthrough findings into procedure revisions

**Outputs:**
- Validated test procedures
- Walkthrough findings and action items

**Source:** Specification.md Section VM-2; Guidance.md Best Practice 4

### Step 7: Obtain Procedure Approval

**Objective:** Obtain formal approval for test procedures.

**Activities:**

7.1. Prepare final procedure package:
   - Procedures with all revisions incorporated
   - Required appendices (forms, checklists, JSAs)
   - Review and concurrence records
   - Transmittal letter or cover sheet

7.2. Submit procedure package to approving authority (QA/QC Manager or per project authority matrix)

7.3. Obtain approval signatures

7.4. Enter approved procedures into project document control system

7.5. Distribute approved procedures to required personnel:
   - Construction/test execution team
   - QC inspectors
   - Engineering
   - HSE
   - Employer representative (per distribution matrix)

**Outputs:**
- Approved test procedures
- Documented distribution record

**Source:** Specification.md Sections QR-1, AC-3

### Step 8: Maintain and Revise Procedures

**Objective:** Keep procedures current and incorporate field feedback.

**Activities:**

8.1. Track field changes and deviations during test execution

8.2. Collect feedback from test crews on procedure adequacy

8.3. Document lessons learned from initial test executions

8.4. Revise procedures as needed to:
   - Correct errors or ambiguities
   - Incorporate approved field changes
   - Address changed conditions (design changes, equipment substitutions)

8.5. Process revisions through same review and approval cycle (Steps 5-7)

8.6. Supersede previous procedure revisions in document control system

8.7. Notify all holders of previous revisions

**Outputs:**
- Revised procedures (as needed)
- Revision history tracking

**Source:** Specification.md Section QR-3; general document control practice **ASSUMPTION**

## Verification

### Verification Activities

**V-1: Procedure Completeness Check**

- Verify all required procedure elements are present (per Step 2.1)
- Verify all required forms and appendices are included
- Verify all hold/witness points from DEL-29.02 are addressed
- Verify all safety requirements are addressed

**Responsibility:** QA/QC Lead or designee

**V-2: Technical Accuracy Check**

- Verify procedure steps are technically correct and align with design
- Verify acceptance criteria match code requirements and specifications
- Verify referenced drawings and specifications are correct and current
- Verify test equipment requirements are adequate

**Responsibility:** Discipline lead engineers (Process, Electrical, I&C as applicable)

**V-3: Safety Adequacy Check**

- Verify hazards are identified and controlled
- Verify JSAs are complete and approved
- Verify emergency response provisions are adequate
- Verify required permits are identified

**Responsibility:** HSE Manager or designee

**V-4: Constructability Check**

- Verify procedure is practical and can be executed with available resources
- Verify access and logistical considerations are addressed
- Verify schedule allows adequate time for procedure execution

**Responsibility:** Construction Manager or Test Superintendent

**Source:** Specification.md Section VM-1, Verification Methods

### Acceptance Criteria

**Test procedures are acceptable when:**

**AC-1:** All required procedure elements are present and complete (per Specification.md Section AC-1)

**AC-2:** All review comments have been addressed or dispositioned

**AC-3:** All required reviewer concurrences have been obtained

**AC-4:** HSE has concurred that safety requirements are adequate

**AC-5:** Required approvals have been obtained per project authority matrix

**AC-6:** Procedures have been entered into document control system and distributed

**Source:** Specification.md Sections AC-1, AC-2, AC-3

### Sign-off Requirements

| Role | Responsibility | Signature/Date |
|------|---------------|----------------|
| Procedure Author | Development | **TBD** |
| Discipline Engineer(s) | Technical Review | **TBD** |
| HSE Representative | Safety Review | **TBD** |
| QA/QC Manager | Approval | **TBD** |
| Construction Manager | Concurrence | **TBD** |
| Employer Representative (if required) | Acceptance | **TBD** |

**Note:** Specific sign-off requirements and authority levels per project authority matrix **location TBD**

## Records

### Documentation Outputs

**Primary Deliverables (per _CONTEXT.md):**

1. **Hydrostatic Test Procedures:**
   - Tank hydrostatic test procedure(s) — one per tank or tank type
   - Piping hydrostatic test procedures — organized by test section or system
   - Loading arm hydrostatic test procedure
   - Other pressure equipment test procedures as applicable

2. **Electrical Test Procedures:**
   - Electrical equipment energization procedure (general)
   - Motor and equipment testing procedure
   - Switchgear and MCC testing procedure
   - Protection relay testing procedure
   - Grounding system verification procedure
   - Lighting system testing procedure
   - Other electrical test procedures as applicable

3. **I&C Test Procedures:**
   - Instrument calibration procedures (by instrument type: pressure, temperature, level, flow, etc.)
   - Control loop checkout procedure
   - Interlock functional test procedure
   - Metering system calibration and verification procedure (custody transfer)
   - Safety instrumented system proof test procedure
   - Control system communications testing procedure
   - Other I&C test procedures as applicable

**Source:** _CONTEXT.md Anticipated Artifacts, Specification.md Documentation Section

### Supporting Documentation

**For each test procedure, maintain:**
- Procedure development record (drafts, review comments, comment resolution)
- Walkthrough notes and findings
- Approval and distribution records
- Revision history

**Test Execution Records (separate deliverable):**
- Completed test data sheets and forms — filed per DEL-29.03 (Test Installation & Test Records)
- Test photographs — filed per DEL-29.03
- Non-conformance reports — filed per project NCR system and referenced in DEL-29.03

**Source:** Cross-reference to DEL-29.03, general project records management **ASSUMPTION**

### Record Management

**Filing Location:**
- Working drafts: `1_Working/DEL-29.01_Test_Procedures/` (current location)
- Procedures under review: `2_Checking/To/` (when submitted for approval)
- Approved procedures: `3_Issued/` (upon approval)
- Project document management system (per project document control procedures)

**Retention Requirements:**
- Test procedures are project records retained for facility life **ASSUMPTION**
- Retention schedule per project records retention plan **location TBD**

**Electronic Records:**
- Native format files (Word, PDF, etc.) per project standards
- Version control and revision tracking per document management system

**Source:** General EPC document control practice **ASSUMPTION**

### Deliverable Status Tracking

**Current Status:** See `_STATUS.md` in this deliverable folder

**Lifecycle States:**
- OPEN: Deliverable scope defined, not yet started
- INITIALIZED: Initial documents (Datasheet, Specification, Guidance, Procedure) generated
- IN_PROGRESS: Test procedure development underway
- CHECKING: Procedures submitted for review and approval
- ISSUED: Procedures approved and released for use

**Status Updates:** Per project working-items lifecycle (see `execution/_Coordination/_COORDINATION.md`)

---

**Document Control:**
- This Procedure.md document is part of the deliverable scaffolding and describes the process for producing test procedures.
- The test procedures themselves (Hydrostatic, Electrical, I&C) will be developed following this process and stored per the filing locations above.
- For questions on test procedure development process, consult D&B Contractor QA/QC Manager.
