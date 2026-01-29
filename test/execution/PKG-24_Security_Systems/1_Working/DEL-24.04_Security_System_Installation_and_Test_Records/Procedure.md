# Procedure: DEL-24.04 Security System Installation & Test Records

## Purpose

This procedure defines the process for **documenting installation and testing** of the security system and **compiling the Installation & Test Records package** within **PKG-24 Security Systems** for the Canola Oil Transload Facility.

**Deliverable objective:** Provides evidence of completion, inspection, and testing for security system, demonstrating compliance with design (DEL-24.01), specification (DEL-24.02), and approved equipment (DEL-24.03).

*Source: `_CONTEXT.md`; Decomposition Section 5 — PKG-24 (line 569)*

**Deliverable type:** Record (QA/QC Documentation)
**Responsible party:** D&B Contractor (QA/QC)
**Discipline:** Specialty (Security Systems)

**Procedure scope:** This procedure covers the workflow for documenting installation and testing activities throughout the security system installation and commissioning process, culminating in a complete record package for Employer acceptance and permanent facility documentation.

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

*Source: `_DEPENDENCIES.md`*

**Upstream deliverables required:**
- **DEL-24.01** — Security System Design Drawing Set (installation and coverage verification basis)
- **DEL-24.02** — Security System Technical Specification (testing requirements and acceptance criteria)
- **DEL-24.03** — Security System Data Sheet Package (approved equipment for installation verification)
- **PKG-29** — Testing procedures and SAT requirements
- **PKG-30** — Commissioning procedures

**Installation and testing prerequisites:**
- Security system installation complete or in progress
- Power and network infrastructure operational
- Installation inspection and testing personnel available
- Test equipment available and calibrated

*Source: Standard installation and testing prerequisites*

### Reference Materials

**Required references:**
- See `_REFERENCES.md` for applicable reference documents
- See `0_References/` in package directory for reference materials

**Expected reference materials:**
- DEL-24.01 (Security System Design Drawing Set) — installation and coverage verification basis
- DEL-24.02 (Security System Technical Specification) — testing requirements and acceptance criteria
- DEL-24.03 (Security System Data Sheet Package) — approved equipment specifications
- Manufacturer installation and testing instructions (from approved equipment)
- PKG-29 testing procedures **TBD**
- PKG-30 commissioning procedures **TBD**
- **TBD** — Project Quality Management Plan — inspection and testing procedures
- **TBD** — Project test forms and checklists

*Source: DEL-24.01, DEL-24.02, DEL-24.03; PKG-29, PKG-30*

### Personnel Requirements

**Qualifications:**
- **QA/QC Inspector:** Qualified inspector for installation verification and inspection
- **Test Technician:** Qualified security systems technician for functional testing (manufacturer-trained preferred)
- **Witness (SAT/Commissioning):** Designer and/or Employer representative for formal acceptance testing **TBD**

**Competency requirements:**
- Understanding of security system installation standards and best practices
- Ability to read and interpret design drawings (DEL-24.01), specifications (DEL-24.02), and equipment datasheets (DEL-24.03)
- Proficiency with test equipment (cable testers, multimeters, network diagnostic tools)
- Knowledge of applicable codes and standards (CEC, TIA-568, manufacturer requirements)
- **ASSUMPTION:** Personnel competency per project Quality Management Plan

*Source: Standard QA/QC and testing personnel requirements*

### Tools and Resources

**Test equipment:**
- Cable tester (for continuity, insulation resistance, data cable certification)
- Multimeter (for voltage, current, resistance measurements)
- Network diagnostic tools (for IP addressing, connectivity, bandwidth testing)
- Camera coverage verification tools (field-of-view measurement, screenshots/photos)
- Test laptops/workstations for VMS and access control software testing

**Test equipment calibration:**
- Test equipment requiring calibration shall have current calibration certificates **TBD**
- Calibration records available for inspection if required

**Documentation tools:**
- Test forms and checklists (from project quality plan or PKG-29) **TBD**
- Digital camera for installation photos
- Document compilation software (PDF compiler, indexing tools)
- Project document management system for record submission **TBD**

## Steps

### Step 1: Test Planning and Preparation

**Objective:** Plan and prepare for installation inspection and testing activities.

**Activities:**
1.1. Develop test schedule
   - Coordinate test schedule with construction/installation schedule
   - Identify test milestones (cable completion, equipment installation completion, system integration, SAT, commissioning)
   - Allow adequate time for deficiency resolution and re-testing
   - Coordinate witness availability for SAT and commissioning **TBD**

1.2. Prepare test procedures and forms
   - Obtain or develop test procedures per DEL-24.02 and PKG-29 requirements
   - Prepare test forms and checklists for each test type (cable testing, equipment functional testing, coverage verification, access control testing, integration testing, SAT)
   - Include acceptance criteria from DEL-24.02 in test procedures
   - Obtain approval of test procedures from designer/Employer if required **TBD**

1.3. Assemble test equipment and verify calibration
   - Identify required test equipment
   - Verify test equipment availability
   - Verify calibration current (obtain calibration certificates if required)
   - Obtain spare test forms, batteries, consumables

1.4. Conduct pre-test coordination meeting
   - Review test procedures with installation and testing team
   - Clarify roles and responsibilities
   - Review safety requirements (lockout/tagout, hot work permits for hazardous areas)
   - Confirm test schedule and logistics

**Outputs:**
- Test schedule with milestones
- Test procedures and forms ready
- Test equipment assembled and calibrated
- Team briefed and ready for testing

**Verification:** Test plan review with project team and designer/Employer (if required)

---

### Step 2: Pre-Installation Verification (Equipment Receiving Inspection)

**Objective:** Verify equipment is correct and undamaged before installation.

**Activities:**
2.1. Equipment receiving inspection (as equipment arrives on site)
   - Verify equipment matches approved DEL-24.03 submittals (manufacturer, model, quantity)
   - Verify equipment tag numbers (if pre-labeled) or prepare tags
   - Inspect for shipping damage (packaging, equipment condition)
   - Verify completeness (accessories, mounting hardware, documentation included)
   - Verify certifications and documentation included (datasheets, manuals, warranty)

2.2. Pre-installation functional testing (optional but recommended for critical equipment)
   - Power up equipment and verify basic function before installation
   - For cameras: Verify image quality, power-up, no dead pixels
   - For readers: Verify card read operation, LED/buzzer function
   - For controllers: Verify power-up, communication, basic operation
   - Identify any defective equipment before installation (reject and replace)

2.3. Document equipment receiving inspection
   - Complete equipment receiving inspection forms
   - Document any damage, defects, or discrepancies
   - Photograph equipment condition if issues found
   - Store equipment properly until installation

**Outputs:**
- Equipment receiving inspection records
- Pre-installation functional test records (if performed)
- Defective equipment identified and rejected (if any)

**Verification:** QA/QC sign-off on equipment receiving inspection

---

### Step 3: Installation Verification and Inspection

**Objective:** Verify equipment installed per design (DEL-24.01), specification (DEL-24.02), and manufacturer instructions.

**Activities:**
3.1. Installation inspection (as installation progresses)
   - Inspect equipment locations (verify against DEL-24.01 design drawings)
   - Inspect mounting (proper mounting hardware, secure, level/plumb, weatherproofing)
   - Inspect cable routing (proper support, protection, separation from power, labeling)
   - Inspect connections (proper termination, secure, no exposed conductors)
   - Inspect environmental protection (IP ratings maintained, cable entries sealed)
   - Identify installation deficiencies and document for correction

3.2. Installation photography
   - Overall installation views (context and location)
   - Detailed mounting and connection photos
   - Weatherproofing and cable entry details
   - Problem areas or field modifications (before and after correction)
   - Organize photos by equipment tag number or location

3.3. Complete installation checklists
   - Use standardized installation checklists for each equipment type
   - Include: tag number, location verification, equipment verification (matches DEL-24.03), mounting verification, cable verification, weatherproofing verification
   - Sign-off by installer and inspector

3.4. Document as-built conditions
   - Mark up DEL-24.01 design drawings with any field changes (red-line markups)
   - Document equipment location changes, cable routing changes, field modifications
   - Maintain as-built markup set for final record drawings

**Outputs:**
- Installation checklists (all equipment)
- Installation photos
- Installation inspection reports (with any deficiencies identified)
- As-built markups

**Verification:** QA/QC inspector sign-off on installation verification

---

### Step 4: Cable Testing

**Objective:** Verify cable installation quality and proper terminations.

**Activities:**
4.1. Data cable testing (Cat6A, fiber optic)
   - For each data cable:
     - Continuity test (all conductors/fibers continuous)
     - Termination verification (proper wiring scheme T568A/T568B, secure terminations)
     - Cable length measurement
     - For copper: Insulation resistance test (minimum 50 MOhm @ 500 VDC) **ASSUMPTION**
     - For copper: Data cable certification test (TIA-568 Category 6A compliance) if required **TBD**
     - For fiber: Optical loss test (dB loss within acceptable range per fiber type/length) **TBD**
   - Record results on cable test form (cable ID, test results, pass/fail)
   - Generate cable test reports from test equipment (if applicable)

4.2. Power cable testing
   - For each power cable circuit:
     - Continuity and polarity verification
     - Insulation resistance test
     - Voltage measurement at equipment termination (verify proper voltage)
     - Verify no shorts or ground faults
   - Record results on cable test form

4.3. Document and resolve cable testing deficiencies
   - If cable test fails: Identify problem (open, short, miswire, poor termination)
   - Correct problem (re-terminate, replace cable, troubleshoot)
   - Re-test and verify pass

**Outputs:**
- Cable test records (all data and power cables)
- Cable test reports from test equipment (if generated)
- Deficiency records and corrective actions (if any)

**Verification:** Cable test results reviewed and signed-off by test technician and QA/QC

---

### Step 5: Individual Equipment Functional Testing

**Objective:** Verify each equipment item functions correctly.

**Activities:**
5.1. Camera functional testing (each camera)
   - Power-up test (camera powers up, LED indicators correct)
   - Network connectivity (camera accessible on network, proper IP address)
   - Image quality test (clarity, color, exposure, no image defects)
   - PTZ operation test (pan, tilt, zoom, preset positions) for PTZ cameras
   - IR illumination test (IR LEDs operate in low light) for IR-equipped cameras
   - Record results on camera functional test form (camera tag, test results, screenshot)

5.2. NVR/VMS functional testing
   - NVR power-up and camera discovery (all cameras detected)
   - Recording operation test (verify recording to storage)
   - Playback operation test (playback recorded video, fast-forward/rewind, export)
   - Storage capacity verification (verify storage matches DEL-24.02 retention requirements)
   - VMS software operation test (live view, alarm management, user access, reporting)

5.3. Access control reader functional testing (each reader)
   - Reader power-up (LED indicator correct)
   - Card read test (present valid card, verify beep/LED response)
   - Communication with controller (verify reader communicates with assigned controller)
   - Read range test (verify read range meets specification) **TBD**
   - Tamper detection test (if equipped)

5.4. Door hardware functional testing (each door)
   - Electric strike or magnetic lock operation (verify unlock when energized)
   - Door position switch test (verify door open/closed status indication)
   - Request-to-exit (REX) device test (verify door unlock on exit request)
   - Crash bar/panic device test (verify free egress without credential)

5.5. Access control controller functional testing (each controller)
   - Controller power-up and reader communication (all assigned readers detected)
   - Door unlock command test (manual unlock via controller/software)
   - Input/output testing (alarm inputs, door position inputs, REX inputs, unlock outputs)
   - Battery backup test (verify operation on battery backup, verify backup duration) **TBD**

5.6. Network equipment functional testing
   - Switch power-up and port status (all connected devices detected)
   - PoE operation (PoE devices powered correctly, no PoE faults)
   - Network connectivity and bandwidth (verify network performance adequate)
   - VLAN configuration (verify proper VLAN segregation if implemented)

**Outputs:**
- Equipment functional test records (all cameras, NVR, VMS, readers, controllers, door hardware, network equipment)
- Test screenshots (cameras, VMS, access control software)
- Deficiency records and corrective actions (if any)

**Verification:** Test technician and QA/QC sign-off on equipment functional testing

---

### Step 6: System-Level Functional Testing

**Objective:** Verify system-level operation (CCTV system, access control system, integration).

**Activities:**
6.1. CCTV system testing
   - End-to-end CCTV system test (camera → network → NVR → VMS → recording → playback)
   - Verify continuous recording for all cameras (or motion-triggered per design)
   - Verify recording retention (storage capacity supports retention period per DEL-24.02)
   - Verify video export function (export video from VMS for incident investigation)
   - Verify alarm handling (camera tampering, video loss alarms)
   - Verify VMS user access control (different user roles and permissions)

6.2. CCTV coverage verification (critical test for acceptance)
   - For each camera: Verify field-of-view matches DEL-24.01 coverage drawings
   - Capture screenshots from each camera showing actual coverage
   - Verify coverage quality (image detail adequate for intended use: identification, recognition, detection)
   - Verify no critical blind spots or coverage gaps
   - Conduct daytime and nighttime coverage verification (coordinate with PKG-18 lighting)
   - Compare actual coverage to coverage analysis from DEL-24.01
   - Document any coverage deficiencies and corrective actions
   - Obtain designer/Employer sign-off on coverage verification

6.3. Access control system testing
   - End-to-end access control test (card read → controller → door unlock → audit log)
   - Access level verification (test different user access levels at different doors, verify grant/deny per design)
   - Time zone verification (if access schedule implemented, verify time-based restrictions)
   - Audit trail verification (verify all access events logged with timestamp, user, door, result)
   - Alarm testing (unauthorized access, door forced, door held open alarms)
   - Fail-safe/fail-secure verification (verify proper operation per DEL-24.02 and life safety requirements)
   - Fire alarm integration test (coordinate with PKG-23): Verify door unlock on fire alarm activation

6.4. Integration testing (CCTV + Access Control)
   - Event correlation test (access control event triggers CCTV recording/PTZ preset if designed)
   - Alarm integration test (access control alarms visible in VMS, CCTV alarms visible in access control software)
   - Audit trail correlation (verify events visible in both CCTV and access control audit trails)

**Outputs:**
- CCTV system test records
- CCTV coverage verification records with screenshots (critical acceptance documentation)
- Access control system test records
- Integration test records
- Deficiency records and corrective actions (if any)

**Verification:** System testing sign-off by test technician, QA/QC, and designer/Employer for coverage verification

---

### Step 7: Terminal Integration Testing (per DEC-05)

**Objective:** Verify integration with Terminal security systems.

**Activities:**
7.1. CCTV integration with Terminal VMS
   - Verify video streams accessible from Terminal VMS or monitoring station **TBD**
   - Verify video quality and latency acceptable for Terminal monitoring
   - Verify user access and permissions (Terminal operators can access Phase 1 cameras)
   - Coordinate with Terminal IT/security operations for integration testing

7.2. Access control integration with Terminal system
   - Verify credential synchronization (if Terminal manages credentials) **TBD**
   - Verify event reporting to Terminal system **TBD**
   - Verify audit trail integration or reporting
   - Coordinate with Terminal security operations for acceptance

7.3. Network integration
   - Verify network connectivity through firewall/gateway
   - Verify proper network security (VLANs, firewall rules, encryption)
   - Verify bandwidth adequate and no impact to Terminal network

7.4. Document Terminal integration and obtain acceptance
   - Document integration configuration and operation
   - Obtain Terminal IT/security operations acceptance of integration **TBD**

**Outputs:**
- Terminal integration test records
- Terminal acceptance sign-off **TBD**

**Verification:** Terminal IT/security operations acceptance

*Source: DEC-05 (Decomposition Section 7)*

---

### Step 8: Site Acceptance Testing (SAT)

**Objective:** Formal witnessed testing to verify system meets DEL-24.02 specification requirements.

**Activities:**
8.1. SAT preparation
   - Complete all installation, equipment functional testing, and system testing
   - Resolve all critical and major deficiencies (minor deficiencies may be accepted "as noted")
   - Prepare SAT procedure (from PKG-29 or project-specific)
   - Schedule SAT with designer and Employer witnesses **TBD**
   - Prepare SAT test equipment and documentation

8.2. Conduct SAT per SAT procedure
   - Perform all SAT tests per procedure (typically abbreviated version of functional and system tests)
   - Verify performance meets DEL-24.02 acceptance criteria
   - Document test results in real-time (on SAT test forms)
   - Witness signs off each test section as completed

8.3. SAT deficiency management
   - If test fails or discrepancy found: Document deficiency, prioritize, develop corrective action plan
   - For critical deficiencies: Resolve and re-test before SAT completion
   - For minor deficiencies: May be accepted "as noted" with resolution plan and schedule
   - All deficiencies tracked in deficiency log

8.4. SAT completion and acceptance
   - All SAT tests passed or deficiencies accepted "as noted"
   - SAT completion certificate signed by contractor, designer, Employer witness
   - Deficiency resolution plan agreed (if any deficiencies accepted "as noted")

**Outputs:**
- SAT procedure
- SAT test results and records
- SAT deficiency list (if any)
- SAT completion certificate with sign-offs

**Verification:** SAT completion certificate signed by all parties

*Source: PKG-29 SAT requirements; DEL-24.02 acceptance criteria*

---

### Step 9: Commissioning and Operational Handover

**Objective:** Verify integrated system operation and readiness for operational handover.

**Activities:**
9.1. Commissioning per PKG-30 procedures
   - Integrated system operation testing (CCTV + access control + Terminal integration)
   - Performance verification under operational conditions
   - Operational readiness verification
   - Commissioning completion certificate

9.2. Training coordination (PKG-35)
   - Operations training for Terminal security staff
   - Maintenance training for Terminal maintenance staff
   - Training records and completion certificates

9.3. Documentation handover
   - Operations and maintenance manuals
   - As-built drawings (final)
   - Warranty documentation
   - Manufacturer support contacts

9.4. Final acceptance
   - Employer final acceptance inspection
   - All deficiencies resolved and closed
   - Final acceptance certificate issued

**Outputs:**
- Commissioning records and completion certificate
- Training records (from PKG-35)
- Documentation handover package
- Final acceptance certificate

**Verification:** Commissioning completion and Employer final acceptance

*Source: PKG-30 commissioning requirements; PKG-35 training requirements*

---

### Step 10: Record Package Compilation and Submission

**Objective:** Compile all installation and test records into organized package for Employer.

**Activities:**
10.1. Organize records by section (per Specification.md structure)
   - Section 1: Pre-Installation Verification
   - Section 2: Installation Records
   - Section 3: Installation Testing (cable testing, power-up testing)
   - Section 4: System Testing (coverage verification, access control testing, integration testing)
   - Section 5: Site Acceptance Testing
   - Section 6: Commissioning Records
   - Section 7: Deficiency Management
   - Section 8: Training and Handover

10.2. Prepare table of contents and index
   - Detailed table of contents with section numbers and page numbers
   - Equipment/test index (tag numbers cross-referenced to records)
   - Deficiency tracking summary (all deficiencies with closure status)

10.3. Quality check
   - Verify all records complete (no missing test records or unsigned forms)
   - Verify all deficiencies resolved and closed
   - Verify all required sign-offs obtained
   - Proofread for errors

10.4. Compile into PDF package
   - Combine all sections into organized PDF package
   - Add bookmarks for easy navigation
   - Ensure legibility and professional presentation

10.5. Submit to Employer
   - Transmit record package via project document management system **TBD**
   - Submit as permanent facility documentation
   - Retain copy for contractor records

10.6. File records
   - File final record package in project document management system
   - Archive in deliverable folder `3_Issued/DEL-24.04_YYYYMMDD_RevX/`
   - Permanent retention as facility documentation

**Outputs:**
- Complete installation and test record package
- Record package submittal to Employer
- Final project closeout documentation

**Verification:** Employer acceptance of record package

---

## Verification

### Verification Activities Summary

| Verification Activity | Responsible Party | Acceptance Criteria |
|-----------------------|-------------------|---------------------|
| **Equipment receiving inspection** | QA/QC Inspector | Equipment matches DEL-24.03, no damage, complete |
| **Installation inspection** | QA/QC Inspector | Installation per DEL-24.01 design and DEL-24.02 requirements |
| **Cable testing** | Test Technician | All cables pass continuity, insulation, termination tests |
| **Equipment functional testing** | Test Technician | All equipment functional and performs per specifications |
| **Coverage verification** | Designer / Employer | Coverage meets DEL-24.01 design and DEL-24.02 requirements |
| **Access control testing** | Test Technician + PKG-23 | Access control operates correctly, fire alarm integration functional |
| **Terminal integration testing** | Terminal IT / Security Ops | Integration functional and acceptable per DEC-05 |
| **SAT** | Contractor + Designer + Employer Witness | All SAT tests pass per DEL-24.02 acceptance criteria |
| **Commissioning** | Contractor + Employer | System operational and ready for handover |
| **Record package review** | Employer | Records complete, accurate, and acceptable |

*Source: Specification.md — Verification section*

### Completion Criteria

Installation and test records are complete when:
- ✓ All equipment installed and verified per DEL-24.01, DEL-24.02, DEL-24.03
- ✓ All cable testing complete and passed
- ✓ All equipment functional testing complete and passed
- ✓ CCTV coverage verification complete and accepted by designer/Employer
- ✓ Access control functional testing complete and passed
- ✓ Terminal integration testing complete and accepted per DEC-05
- ✓ SAT completed successfully with Employer witness sign-off
- ✓ Commissioning completed per PKG-30
- ✓ Training completed per PKG-35
- ✓ All deficiencies resolved and closed
- ✓ Record package complete, organized, and professional
- ✓ Record package submitted to Employer and accepted
- ✓ Final acceptance certificate issued
- ✓ Records filed as permanent facility documentation in `3_Issued/`

*Source: Specification.md — Acceptance criteria and completion criteria*

## Records

### Documentation Outputs

**Primary deliverable:**
- **Security System Installation & Test Records Package** — comprehensive QA/QC record package documenting installation, testing, and acceptance

*Source: `_CONTEXT.md` — Anticipated Artifacts*

**Record categories included:**
- Equipment receiving inspection records
- Installation checklists and photos
- Cable test records
- Equipment functional test records
- CCTV coverage verification records
- Access control test records
- Integration test records
- SAT procedures and results
- Commissioning records
- Deficiency management records
- Training records
- As-built documentation
- Final acceptance certificates

### Record Management

**Filing locations:**
- **Working files (during installation/testing):** `1_Working/DEL-24.04_Security_System_Installation_and_Test_Records/`
- **Final record package (upon completion):** `3_Issued/DEL-24.04_YYYYMMDD_Final/`
- **Employer facility records:** Permanent facility documentation

**File formats:**
- Record package: PDF
- Test forms: Scanned or electronic forms compiled into PDF
- Photos: Digital photos embedded in PDF or provided as organized file collection
- As-built drawings: CAD files (DWG) and PDF

**Retention requirements:**
- Permanent retention as facility documentation **ASSUMPTION**
- Retained by Employer for operations, maintenance, future modifications
- Contractor retains copy for warranty and project closeout purposes

**Document control:**
- Records are final upon Employer acceptance (not typically revised)
- Additional testing or corrective action may be appended if needed
- Superseded records (if any) clearly marked

*Source: Standard project record management practices*

---

*Document status: Enriched draft — Pass 1*
*Enrichment date: 2026-01-28*
*Cross-references: Specification.md for testing requirements; Guidance.md for testing principles; Datasheet.md for record scope*

---

**PKG-24 Security Systems — Complete**

All 4 deliverables with all 4 documents (16 documents total) have been enriched and are ready for WORKING_ITEMS sessions.
