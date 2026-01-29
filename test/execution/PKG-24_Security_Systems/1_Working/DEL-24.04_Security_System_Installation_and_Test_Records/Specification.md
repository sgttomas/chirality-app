# Specification: DEL-24.04 Security System Installation & Test Records

## Scope

This specification defines the requirements for documenting and managing **Security System Installation & Test Records** within **PKG-24 Security Systems** for the Canola Oil Transload Facility — Phase 1 at Fraser Surrey Terminal.

**Purpose:** Provides evidence of completion, inspection, and testing for security system, demonstrating compliance with design (DEL-24.01), specification (DEL-24.02), and approved equipment (DEL-24.03).

*Source: `_CONTEXT.md`; Decomposition Section 5 — PKG-24 (line 569)*

### Inclusions

The installation and test record package shall include:
- Equipment receiving inspection records
- Installation checklists and verification records
- Installation photos (as-installed documentation)
- Cable testing records (continuity, insulation resistance, termination verification)
- Equipment functional test records (cameras, NVR, VMS, readers, controllers, door hardware, network equipment)
- CCTV coverage verification records (field-of-view verification, image quality assessment)
- Access control functional test records (card read, door operation, access levels, fail-safe/fail-secure)
- System integration test records (CCTV + access control + Terminal integration per DEC-05)
- Site Acceptance Testing (SAT) records (procedures, results, acceptance certificates)
- Commissioning records (integrated operation, performance verification, Terminal coordination)
- Deficiency lists and corrective action records
- Training records (reference PKG-35)
- As-built documentation (markups and final as-installed drawings)

*Source: `_CONTEXT.md` — Anticipated Artifacts; Datasheet.md — Record scope*

### Exclusions

The following are outside the scope of this record package:
- Design drawings (covered under DEL-24.01) — as-built markups are included
- Technical specifications (covered under DEL-24.02)
- Equipment submittals (covered under DEL-24.03)
- Operations and maintenance manuals **ASSUMPTION** — provided separately as part of closeout documentation
- Security operations procedures **ASSUMPTION** — Employer/Terminal responsibility

*Source: PKG-24 deliverable structure*

### Interface Scope

**Critical interfaces:**
- DEL-24.01 (Design Drawings) — Installation verification basis, coverage verification basis
- DEL-24.02 (Technical Specification) — Testing requirements and acceptance criteria basis
- DEL-24.03 (Equipment Submittals) — Installed equipment verification basis (equipment matches approved submittals)
- PKG-23 (Fire Protection) — Access control integration with fire alarm testing
- PKG-29 (Testing) — Testing procedures and SAT requirements
- PKG-30 (Commissioning) — Commissioning procedures and performance verification
- PKG-35 (Training & Handover) — Training records
- Terminal integration per DEC-05 — Integration testing and acceptance

*Source: PKG-24 deliverable relationships; DEC-05 (Decomposition Section 7)*

## Requirements

### Functional Requirements

#### FR-1: Record Package Organization and Completeness
- **FR-1.1**: Records shall be organized by installation and testing phase:
  - Section 1: Pre-Installation Verification (receiving inspection, pre-installation testing)
  - Section 2: Installation Records (installation checklists, photos, as-built markups)
  - Section 3: Installation Testing (cable testing, power-up testing, individual equipment functional testing)
  - Section 4: System Testing (CCTV coverage verification, access control functional testing, integration testing)
  - Section 5: Site Acceptance Testing (SAT procedures and results)
  - Section 6: Commissioning Records (performance verification, Terminal integration, operational handover)
  - Section 7: Deficiency Management (deficiency lists, corrective actions, closeout)
  - Section 8: Training and Handover (training records, final acceptance certificates)

- **FR-1.2**: Each test record shall include minimum information:
  - Equipment/system identification (tag number, location, description)
  - Test procedure reference or test steps performed
  - Test date, time, and personnel identification (tester, witness)
  - Test equipment used (calibration status where applicable)
  - Test results (pass/fail with measurements or observations)
  - Deficiencies identified and resolution status
  - Sign-offs (tester, inspector, witness as applicable)

- **FR-1.3**: Record package shall include table of contents and index for easy navigation

*Source: Standard installation and test record organization*

#### FR-2: Equipment Installation Verification Requirements
- **FR-2.1**: Installation checklists shall verify:
  - Equipment installed per DEL-24.01 design (correct location, proper mounting)
  - Equipment matches approved DEL-24.03 submittals (correct manufacturer and model)
  - Installation per DEL-24.02 requirements and manufacturer instructions
  - Proper weatherproofing and environmental protection (IP ratings maintained)
  - Proper cable routing, support, and protection
  - Cable labeling per project standards
  - Installation inspection and sign-off

- **FR-2.2**: Installation photos shall document:
  - Overall installation views showing context and location
  - Detailed mounting and connection photos
  - Weatherproofing and cable entry details
  - Problem areas, field modifications, or deviations from design (with explanation)

- **FR-2.3**: As-built markups shall document:
  - Any field changes to equipment locations or cable routing
  - Additional equipment or components not shown on original design
  - Final installed configuration for record drawings

*Source: DEL-24.01, DEL-24.02, DEL-24.03 as installation verification basis*

#### FR-3: Cable Testing Requirements
- **FR-3.1**: Data cable testing (Cat6A, fiber optic) shall verify:
  - Continuity test (all conductors/fibers)
  - Termination verification (proper wiring scheme, secure connections)
  - Cable length measurement
  - For copper: Insulation resistance test (minimum 50 Megaohms @ 500 VDC) **ASSUMPTION**
  - For fiber: Optical loss test (dB loss within acceptable range) **TBD**
  - Test results recorded per cable with pass/fail status

- **FR-3.2**: Power cable testing shall verify:
  - Continuity and proper polarity
  - Insulation resistance
  - Voltage at equipment termination (verify proper voltage)
  - No shorts or ground faults

*Source: TIA-568 cabling standards **ASSUMPTION**; DEL-24.02 installation requirements*

#### FR-4: CCTV Equipment and System Testing Requirements
- **FR-4.1**: Camera functional testing shall verify:
  - Camera powers up and communicates with NVR/VMS
  - Image quality (clarity, color accuracy, exposure)
  - PTZ operation (pan, tilt, zoom, preset positions) for PTZ cameras
  - Infrared (IR) illumination operation (if equipped)
  - Network connectivity and proper IP addressing
  - Test results recorded per camera with pass/fail and observations

- **FR-4.2**: NVR/VMS functional testing shall verify:
  - NVR powers up and all cameras detected
  - Recording operation (continuous and/or motion-triggered per design)
  - Storage capacity and retention period verification (per DEL-24.02)
  - Playback operation (all cameras, fast-forward/rewind, export)
  - VMS software operation (live view, alarm management, user access control)

- **FR-4.3**: CCTV coverage verification shall document:
  - Camera field-of-view verification (compare actual to DEL-24.01 coverage drawings)
  - Coverage quality verification (image detail, blind spots, lighting adequacy)
  - Screenshots or photos from each camera showing actual coverage
  - Comparison to coverage analysis and acceptance criteria from DEL-24.01/DEL-24.02
  - Coverage verification sign-off (designer/Employer acceptance)

*Source: DEL-24.02 CCTV testing requirements; DEL-24.01 coverage verification basis*

#### FR-5: Access Control Equipment and System Testing Requirements
- **FR-5.1**: Card reader functional testing shall verify:
  - Reader powers up and communicates with controller
  - Card read operation (test with valid credential)
  - Read range and response time (per DEL-24.02)
  - LED and buzzer indication (visual/audible feedback)
  - Tamper detection operation (if equipped)

- **FR-5.2**: Door hardware functional testing shall verify:
  - Electric strike or magnetic lock operation (door unlocks when energized)
  - Proper fail-safe or fail-secure operation per design
  - Door position switch operation (door open/closed status indication)
  - Request-to-exit (REX) device operation (door unlocks on exit request)
  - Crash bar/panic device operation (free egress maintained)

- **FR-5.3**: Access control system functional testing shall verify:
  - End-to-end access control operation (card presentation → door unlock → audit log)
  - Access level verification (test different user access levels grant/deny per design)
  - Time zone verification (access restricted per schedule if implemented)
  - Audit trail verification (all access events logged with timestamp, user, location)
  - Alarm handling (unauthorized access attempts, door held open, door forced open)

- **FR-5.4**: Fire alarm integration testing shall verify (coordinate with PKG-23):
  - Door unlock on fire alarm activation
  - Proper fail-safe operation during power loss or fire alarm condition
  - Emergency egress maintained per life safety codes

*Source: DEL-24.02 access control testing requirements; PKG-23 fire protection interface*

#### FR-6: Integration and System-Level Testing Requirements
- **FR-6.1**: CCTV + Access Control integration testing shall verify:
  - Access control events trigger CCTV recording or camera PTZ preset (if designed)
  - Alarm events generate alerts in VMS and access control software
  - Audit trail correlation (access events visible in both CCTV and access control logs)

- **FR-6.2**: Terminal integration testing shall verify per DEC-05:
  - CCTV integration: Video streams accessible from Terminal VMS or monitoring station **TBD**
  - Access control integration: Credential synchronization, event reporting to Terminal system **TBD**
  - Network integration: Proper network connectivity, security, and bandwidth
  - Integration testing coordinated with Terminal IT/security operations
  - Terminal acceptance of integration **TBD**

*Source: DEC-05 (Decomposition Section 7) — Terminal integration requirements*

### Performance Requirements

#### PR-1: Testing Completeness
- **PR-1.1**: 100% of installed equipment shall be tested and verified
- **PR-1.2**: All test records shall be complete (no missing information or unsigned records)
- **PR-1.3**: All deficiencies shall be resolved and closed before final acceptance

#### PR-2: Acceptance Criteria Compliance
- **PR-2.1**: All test results shall meet or exceed DEL-24.02 acceptance criteria
- **PR-2.2**: CCTV coverage shall meet design coverage requirements (DEL-24.01)
- **PR-2.3**: Access control system shall operate as designed with proper access control levels and fail-safe/fail-secure operation
- **PR-2.4**: Integration with Terminal systems shall be functional and accepted per DEC-05

*Source: DEL-24.02 acceptance criteria; DEC-05*

#### PR-3: Record Quality
- **PR-3.1**: Records shall be legible, complete, and professional
- **PR-3.2**: All records shall be dated and signed by responsible personnel
- **PR-3.3**: Records shall be organized and indexed for easy review and retrieval

### Interface Requirements

#### IR-1: Design Verification (DEL-24.01)
- **IR-1.1**: Installed equipment locations shall be verified against DEL-24.01 design drawings
- **IR-1.2**: CCTV coverage shall be verified against DEL-24.01 coverage analysis
- **IR-1.3**: As-built documentation shall reflect final installed configuration

*Source: DEL-24.01 as installation verification basis*

#### IR-2: Specification Compliance (DEL-24.02)
- **IR-2.1**: Installation shall be verified compliant with DEL-24.02 requirements
- **IR-2.2**: Testing shall be performed per DEL-24.02 testing requirements
- **IR-2.3**: Acceptance criteria from DEL-24.02 shall be met

*Source: DEL-24.02 as specification and testing basis*

#### IR-3: Equipment Verification (DEL-24.03)
- **IR-3.1**: Installed equipment shall be verified to match approved DEL-24.03 submittals
- **IR-3.2**: No unauthorized substitutions or deviations from approved equipment

*Source: DEL-24.03 as approved equipment basis*

#### IR-4: Testing and Commissioning Coordination
- **IR-4.1**: Testing shall be performed per PKG-29 testing procedures
- **IR-4.2**: Site Acceptance Testing (SAT) shall be coordinated with designer and Employer
- **IR-4.3**: Commissioning shall be performed per PKG-30 commissioning procedures
- **IR-4.4**: Training records shall be coordinated with PKG-35 training program

*Source: PKG-29, PKG-30, PKG-35 interfaces*

### Quality Requirements

#### QR-1: Inspection and Testing Personnel
- **QR-1.1**: Installation inspections shall be performed by qualified QA/QC personnel
- **QR-1.2**: Testing shall be performed by qualified technicians (manufacturer-trained preferred)
- **QR-1.3**: SAT and commissioning shall be witnessed by designer and/or Employer representative **TBD**

#### QR-2: Test Equipment Calibration
- **QR-2.1**: Test equipment used for measurements shall be calibrated (cable testers, multimeters, etc.)
- **QR-2.2**: Calibration records or certificates shall be available for inspection **TBD**

#### QR-3: Record Retention
- **QR-3.1**: Records shall be filed per project document control procedures
- **QR-3.2**: Final record package shall be submitted to Employer as permanent facility record
- **QR-3.3**: Retention period: Permanent for facility operations and maintenance **ASSUMPTION**

### Safety and Regulatory Requirements

#### SR-1: Safety During Testing
- **SR-1.1**: Testing shall be performed safely with proper hazard controls
- **SR-1.2**: Live electrical testing shall follow proper lockout/tagout (LOTO) procedures
- **SR-1.3**: Testing in hazardous areas shall follow proper hot work permits and procedures **TBD**

#### SR-2: Regulatory Compliance Verification
- **SR-2.1**: Installation shall be verified compliant with Canadian Electrical Code (CEC)
- **SR-2.2**: Fire/life safety integration shall be verified compliant with NFPA and life safety codes (coordinate with PKG-23)
- **SR-2.3**: Privacy compliance shall be verified (signage, data retention policies) **TBD**

*Source: Standard safety and regulatory requirements*

## Standards

### Governing Standards

**Installation and Testing Standards:**
- Canadian Electrical Code (CSA C22.1) — electrical installation verification
- National Building Code of Canada (NBC) 2020 — structural mounting and seismic verification
- TIA-568 — cabling installation and testing standards **ASSUMPTION**
- Manufacturer installation and testing instructions (from DEL-24.03 approved equipment)

**Quality Management:**
- Project Quality Management Plan **TBD** — inspection and testing procedures
- ISO 9001 quality management principles **ASSUMPTION**

**Project-Specific:**
- DEL-24.02 (Security System Technical Specification) — testing requirements and acceptance criteria
- PKG-29 (Testing) — testing procedures and SAT requirements
- PKG-30 (Commissioning) — commissioning procedures

## Verification

### Verification Methods

#### Installation Verification
- **Visual inspection:** Verify installation per design, proper mounting, weatherproofing, cable routing
- **As-installed verification:** Verify equipment locations and routing match design (or as-built markups)
- **Equipment verification:** Verify installed equipment matches approved DEL-24.03 submittals

#### Testing Verification
- **Test procedure review:** Verify testing performed per specified procedures
- **Test result review:** Verify all test results pass and meet acceptance criteria
- **Deficiency review:** Verify all deficiencies identified, resolved, and closed

#### SAT and Commissioning Verification
- **SAT witness:** Designer and/or Employer witness SAT and verify acceptance criteria met
- **Commissioning verification:** Verify integrated system operation and Terminal integration per DEC-05
- **Final acceptance:** Employer acceptance of completed and tested system

### Acceptance Criteria

**Installation Acceptance:**
- All equipment installed per design (DEL-24.01) or as-built approved deviations
- All equipment matches approved submittals (DEL-24.03)
- Installation complies with specification (DEL-24.02) and manufacturer instructions
- Installation inspection complete and signed off

**Testing Acceptance:**
- All equipment and systems tested per DEL-24.02 and PKG-29 requirements
- All test results pass and meet acceptance criteria
- CCTV coverage verified and acceptable
- Access control operation verified and acceptable
- Integration with Terminal systems verified and acceptable per DEC-05
- All deficiencies resolved and closed

**Final Acceptance:**
- SAT completed successfully with Employer witness sign-off
- Commissioning completed and system operational
- Training completed (PKG-35)
- All records complete, signed, and submitted to Employer
- Final acceptance certificate issued

**Completion Criteria:**
- Installation and test record package complete and submitted to Employer
- Employer final acceptance obtained
- Records filed as permanent facility documentation
- Package archived in deliverable folder `3_Issued/`

## Documentation

### Required Documentation Outputs

**Primary Deliverable:**
- **Security System Installation & Test Records Package** — comprehensive record package including:
  - Section 1: Pre-Installation Verification
  - Section 2: Installation Records
  - Section 3: Installation Testing
  - Section 4: System Testing (CCTV coverage verification, access control testing)
  - Section 5: Site Acceptance Testing
  - Section 6: Commissioning Records
  - Section 7: Deficiency Management
  - Section 8: Training and Handover

**Anticipated Test Records:**
1. Equipment receiving inspection records
2. Installation checklists (all equipment)
3. Installation photos
4. Cable test records (all data and power cables)
5. Camera functional test records
6. NVR/VMS functional test records
7. CCTV coverage verification records (field-of-view verification, screenshots)
8. Access control reader functional test records
9. Door hardware functional test records
10. Access control system functional test records
11. Integration test records (CCTV + access control + Terminal)
12. SAT procedures and test results
13. Commissioning procedures and performance verification
14. Deficiency lists and corrective action records
15. Training records
16. As-built documentation (markups and final drawings)
17. Final acceptance certificates

*Source: `_CONTEXT.md` — Anticipated Artifacts; Datasheet.md*

### Documentation Requirements

**Format and Media:**
- **Package format:** PDF compilation with table of contents and index **ASSUMPTION**
- **Test forms:** Standardized test forms or project-specified templates **TBD**
- **Photos:** Digital photos embedded in records or provided as separate file **TBD**
- **Transmittal:** Via project document management system **TBD**

**Organization:**
- Clear table of contents with section numbers and page numbers
- Equipment/test index cross-referencing tag numbers to test records
- Deficiency tracking with closure verification
- Final acceptance certificates and sign-offs

**Revision Control:**
- Package document number per **TBD** — project numbering system
- Records are typically final (not revised), but additional testing or corrective action may be appended
- Final submitted package is permanent facility record

**Record Management:**
- Electronic files stored in project document management system **TBD**
- Final record package submitted to Employer as permanent facility documentation
- Retention: Permanent for facility operations and maintenance **ASSUMPTION**

### Supporting Documentation

- **Test procedures:** Detailed test procedures for each test type (from PKG-29 or project-specific)
- **Acceptance criteria:** Defined acceptance criteria for each test (from DEL-24.02)
- **Deficiency management:** Deficiency tracking log with status and closure verification
- **As-built drawings:** Final as-installed drawings reflecting field changes

**Cross-References to Related Deliverables:**
- DEL-24.01 — Design basis for installation and coverage verification
- DEL-24.02 — Specification basis for testing requirements and acceptance criteria
- DEL-24.03 — Approved equipment basis for equipment verification
- PKG-29 (Testing), PKG-30 (Commissioning), PKG-35 (Training) — Testing, commissioning, and training procedures

---

*Document status: Enriched draft — Pass 1*
*Enrichment date: 2026-01-28*
*Cross-references: Datasheet.md for record scope; Guidance.md for testing principles; Procedure.md for record compilation workflow*
