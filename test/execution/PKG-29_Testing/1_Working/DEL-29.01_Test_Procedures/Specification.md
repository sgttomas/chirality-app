# Specification: DEL-29.01 Test Procedures

## Scope

This specification defines the requirements for **Test Procedures** within **PKG-29 Testing**.

**Purpose:** Defines the execution method and controls for test to meet safety, quality, and operational requirements. **Source:** Decomposition line 646

**Deliverable Type:** Procedure
**Responsible Party:** D&B Contractor (QA/QC)
**Source:** _CONTEXT.md

### Inclusions

This deliverable encompasses procedures for:
1. **Hydrostatic test procedures** — Pressure testing of storage tanks, piping, and loading systems
2. **Electrical test procedures** — Testing of electrical power distribution, motors, and protection systems
3. **I&C test procedures** — Calibration, loop checks, and functional testing of instrumentation and control systems

**Source:** _CONTEXT.md Anticipated Artifacts, Decomposition line 646

### Exclusions

The following are excluded from this deliverable:
- Factory Acceptance Testing (FAT) procedures — covered by DEL-29.04
- Site Acceptance Testing (SAT) procedures — covered by DEL-29.05
- Commissioning procedures — covered by PKG-30 (Commissioning)
- Tank hydrotest water management procedures — covered by DEL-29.06
- Test records and documentation — covered by DEL-29.03 (Test Installation & Test Records)

**ASSUMPTION:** Exclusions based on PKG-29 deliverable scope boundaries per decomposition.

## Requirements

### Functional Requirements

**FR-1: Procedure Content Requirements**
- Each test procedure shall define:
  - Test objectives and acceptance criteria
  - Required equipment and instrumentation
  - Step-by-step test execution sequence
  - Safety precautions and hazard controls
  - Personnel qualifications and roles
  - Documentation and record-keeping requirements
  - Emergency response provisions

**Source:** ASME B31.3, API 650, IEC 62382 (general testing procedure requirements) **ASSUMPTION**

**FR-2: Test Coverage Requirements**
- Procedures shall cover all systems requiring verification prior to commissioning:
  - All pressure vessels and piping systems requiring Code compliance
  - All electrical equipment requiring energization testing
  - All instrumentation requiring calibration and loop verification
  - All safety systems requiring functional demonstration

**Source:** Project Objectives OBJ-1 (Safe & Reliable Operation), OBJ-10 (Custody Transfer Accuracy) — Decomposition Section 6

**FR-3: Hold and Witness Point Integration**
- Test procedures shall identify and integrate all hold points and witness points as defined in DEL-29.02 (Inspection and Test Plan With Hold/Witness Points)
- Procedures shall specify inspection requirements prior to and following each test

**Source:** Cross-reference to DEL-29.02, Decomposition line 647

### Performance Requirements

**PR-1: Hydrostatic Testing Requirements**
- Storage tank hydrostatic test pressure: **TBD** — **ASSUMPTION**: Per API 650 (typically 1.5× design pressure or per code)
- Piping hydrostatic test pressure: **TBD** — **ASSUMPTION**: Per ASME B31.3 (typically 1.5× design pressure)
- Test medium: Potable water unless otherwise specified **ASSUMPTION**
- Hold duration: **TBD** — Per applicable code requirements (typically 24 hours for tanks, 10 minutes minimum for piping)
- Acceptance criteria: No visible leakage, no pressure drop exceeding code limits **ASSUMPTION**

**Source:** API 650, ASME B31.3, CSA Z662 **location TBD**

**PR-2: Electrical Testing Requirements**
- Insulation resistance testing: **TBD** — **ASSUMPTION**: Minimum values per NFPA 70 and IEEE 43
- Continuity testing: Maximum resistance values **TBD**
- Protection relay settings: **TBD** — Per electrical design and coordination study
- Ground resistance: **TBD** — Per NFPA 70 and local electrical code

**Source:** NFPA 70, IEEE 43 **location TBD**

**PR-3: I&C Testing Requirements**
- Instrument calibration accuracy: **TBD** — Per instrument specification and process requirements
- Custody transfer metering accuracy: **TBD** — Per Employer's Requirements and regulatory requirements for fiscal metering
- Control loop response: **TBD** — Per control philosophy and process requirements
- Safety system proof test: **TBD** — Per safety integrity level (SIL) requirements

**Source:** IEC 62382, Employer's Requirements **location TBD**; Project Objective OBJ-10 (Custody Transfer Accuracy)

### Interface Requirements

**IR-1: Upstream Deliverable Interfaces**
- Test procedures shall be based on final design documentation:
  - Storage tank design (DEL-13.01-13.06)
  - Piping design (DEL-14.01-14.08)
  - Electrical design (DEL-17.01-17.05)
  - Control system design (DEL-19.01-19.05)
- **TBD** — Specific interface requirements to be defined when design progresses

**Source:** Cross-package dependencies, Decomposition Sections for PKG-13, 14, 17, 19 **ASSUMPTION**

**IR-2: Downstream Deliverable Interfaces**
- Test procedures shall enable production of:
  - Test records per DEL-29.03
  - FAT records per DEL-29.04
  - SAT records per DEL-29.05
- Procedures shall align with commissioning procedures (PKG-30)

**Source:** Decomposition lines 648-650, PKG-30 context

**IR-3: Water Management Interface**
- Hydrostatic test procedures shall reference water management requirements from DEL-29.06 (Tank Hydrotest Water Management Plan)
- Procedures shall specify water quality requirements, sampling, treatment, and disposal protocols

**Source:** Cross-reference to DEL-29.06, Decomposition line 651

### Quality Requirements

**QR-1: Procedure Development and Approval**
- All test procedures shall be developed by qualified personnel with relevant discipline expertise
- Procedures shall undergo multi-discipline review (Engineering, QA/QC, HSE, Operations) **ASSUMPTION**
- Procedures shall be approved by D&B Contractor QA/QC Manager prior to use
- Approval authority: **TBD**

**Source:** Project Quality Management Plan **location TBD**

**QR-2: Safety Review Requirements**
- All test procedures shall undergo hazard identification and risk assessment
- Job Safety Analysis (JSA) or equivalent shall be prepared for each test type **ASSUMPTION**
- Procedures shall identify required PPE, permit requirements, and emergency response measures

**Source:** General EPC best practice **ASSUMPTION**

**QR-3: Revision Control**
- Procedures shall be maintained under project document control
- Revisions shall be tracked and approved per project procedures
- Field changes shall be documented and incorporated into controlled revisions

**Source:** Project Document Control Procedures **location TBD**

## Standards

### Applicable Codes and Standards

**Hydrostatic Testing:**
- ASME B31.3: Process Piping (pressure testing requirements)
- API 650: Welded Tanks for Oil Storage (tank hydrostatic testing)
- API 653: Tank Inspection, Repair, Alteration, and Reconstruction
- CSA Z662: Oil and Gas Pipeline Systems (pressure testing)
- ASME PCC-1: Guidelines for Pressure Boundary Bolted Flange Joint Assembly

**Electrical Testing:**
- NFPA 70: National Electrical Code (testing and commissioning)
- IEEE 43: Recommended Practice for Testing Insulation Resistance of Rotating Machinery
- IEEE 141: Recommended Practice for Electric Power Distribution for Industrial Plants (Red Book)
- CSA C22.1: Canadian Electrical Code **ASSUMPTION**

**I&C Testing:**
- IEC 62382: Electrical and instrumentation loop check
- ISA-5.1: Instrumentation Symbols and Identification
- IEC 61511: Functional safety - Safety instrumented systems for the process industry sector

**General QA/QC:**
- ISO 9001: Quality Management Systems **ASSUMPTION**
- Employer's Requirements: **location TBD**

**Note:** Specific clause references shall be identified during procedure development when design details are finalized.

## Verification

### Verification Methods

**VM-1: Procedure Review and Approval**
- Technical review by discipline lead engineers
- Safety review by HSE personnel
- QA/QC review for compliance with quality procedures
- Operations review for constructability and operability **ASSUMPTION**

**VM-2: Procedure Walkthrough**
- Tabletop walkthrough of test procedures with execution team
- Field walkthrough where practical prior to first use
- Identification and resolution of procedural gaps or conflicts

**VM-3: Trial Runs (where applicable)**
- Trial execution on non-critical systems to validate procedure adequacy **ASSUMPTION**
- Incorporation of lessons learned into final procedures

**VM-4: Competency Verification**
- Verification that test execution personnel are qualified per procedure requirements
- Training records and certifications confirmed prior to test execution

**Source:** IEC 62382, General EPC practice **ASSUMPTION**

### Acceptance Criteria

**AC-1: Procedure Completeness**
- All required procedure elements present (scope, objectives, steps, safety, acceptance criteria, records)
- All hold/witness points identified and integrated with DEL-29.02
- All required forms, checklists, and data sheets included

**AC-2: Procedure Adequacy**
- Procedures are technically sound and consistent with design documentation
- Safety hazards identified and mitigated
- Procedures are clear, unambiguous, and executable by qualified personnel

**AC-3: Approval Status**
- All required reviews completed
- All review comments closed or dispositioned
- Approved signatures obtained per project authority matrix **TBD**

## Documentation

### Required Deliverable Outputs

1. **Hydrostatic Test Procedures**
   - Tank hydrostatic test procedure (per API 650)
   - Piping hydrostatic test procedures (per ASME B31.3/CSA Z662)
   - Loading arm hydrostatic test procedure
   - Pressure vessel test procedures (if applicable)

2. **Electrical Test Procedures**
   - Electrical equipment energization procedure
   - Motor insulation resistance and continuity testing procedure
   - Switchgear and MCC testing procedure
   - Protection relay testing procedure
   - Grounding system verification procedure
   - Lighting system testing procedure

3. **I&C Test Procedures**
   - Instrument calibration procedure (by instrument type)
   - Control loop checkout procedure
   - Interlock functional test procedure
   - Metering system calibration and accuracy verification procedure (custody transfer)
   - Safety instrumented system proof test procedure
   - Control system communications testing procedure

**Source:** _CONTEXT.md Anticipated Artifacts, Decomposition line 646; cross-package scope review **ASSUMPTION**

### Documentation Format and Control

- Document format: **TBD** — **ASSUMPTION**: Per project procedure template and document management system
- Document numbering: **TBD** — Per project numbering system
- Revision control: Per project document control procedures **location TBD**
- Distribution: **TBD** — **ASSUMPTION**: To QA/QC, Construction, Engineering, Commissioning, HSE, Employer
- Retention: **TBD** — Per project records retention schedule

### Supporting Documentation

Each test procedure shall reference or include:
- Applicable design drawings and specifications
- Required test equipment and calibration requirements
- Data sheets and test record forms (cross-reference DEL-29.03)
- Safety documentation (JSA, permits, emergency response)
- Inspection and Test Plan hold/witness points (cross-reference DEL-29.02)

**ASSUMPTION:** Supporting documentation requirements based on typical EPC project practice.

---

## Cross-Document Linkage

| Document | Key Sections | Relationship |
|----------|--------------|--------------|
| Datasheet.md | §Attributes, §Construction | Captures test types, applicable systems, and procedure format requirements |
| Guidance.md | §Principles, §Considerations, §Trade-offs, §Examples | Provides engineering rationale and practical examples for implementing requirements |
| Procedure.md | §Steps 1-8, §Verification | Defines process for developing procedures that satisfy these requirements |

**Requirement-to-Guidance Traceability:**
- FR-1 (Procedure Content) → Guidance §Principles (Testing Philosophy), Procedure Step 2
- FR-2 (Test Coverage) → Guidance §Project-Specific Context (Objectives Alignment)
- FR-3 (Hold/Witness Points) → Guidance §Considerations Item 4, Procedure Step 3
- PR-1 to PR-3 → Guidance §Discipline-Specific Principles, §Examples
- IR-1 to IR-3 → Guidance §Considerations Items 1, 5
- QR-1 to QR-3 → Procedure Steps 4-7, §Verification

**Requirement-to-Procedure Traceability:**
- FR-1 verification → Procedure V-1 (Completeness Check)
- PR-1 to PR-3 verification → Procedure V-2 (Technical Accuracy Check)
- QR-2 verification → Procedure V-3 (Safety Adequacy Check)
- QR-1 verification → Procedure Steps 5-7 (Review/Approval)
