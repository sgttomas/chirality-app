# Specification: DEL-20.05 Instrumentation Installation & Test Records

## Scope

Defines requirements for **Instrumentation Installation & Test Records** within **PKG-20 Field Instrumentation** for the Canola Oil Transload Facility Phase 1.

**Deliverable Purpose:** Provides evidence of completion, inspection, and testing for instrumentation.

**Source:** Decomposition document, DEL-20.05 (line 500)

**Record Scope:** Quality assurance and commissioning test records for field instrumentation (level, pressure, temperature, flow instruments).

**Anticipated Artifacts:** Calibration certificates, loop check records, FAT records, installation inspection records, functional test records.

## Requirements

### Functional Requirements

**FR-1: Record Completeness**

Test records shall be provided for all field instruments requiring: factory calibration, field calibration, loop verification, installation inspection, or functional testing. Records demonstrate compliance with DEL-20.02 specifications and installation per DEL-20.01 drawings.

**FR-2: Calibration Records**

Calibration certificates (factory and field) shall include: instrument identification, calibration date, calibration equipment (traceable standards), calibration data (input/output, error), accuracy verification, technician sign-off.

**FR-3: Loop Check Records**

Loop check records shall verify end-to-end functionality: sensor to control system. Include: loop identification, component verification, signal integrity, alarm/trip verification, sign-offs (instrument technician, control systems, commissioning engineer).

**FR-4: Installation Inspection Records**

Installation inspection records shall verify: mounting, wiring, hazardous area compliance (CSA C22.1), material verification (nameplate vs. data sheets), inspector sign-off.

**FR-5: Functional Test Records**

Functional test records shall verify operational performance: alarm/interlock verification, control loop tuning, safety system verification (API 2350 overfill, ISA 84 SIS if applicable).

**Source:** **ASSUMPTION** based on typical commissioning test record requirements

### Performance Requirements

**PR-1: Calibration Accuracy**

Calibration equipment shall have accuracy superior to instrument being calibrated (typically 4:1 ratio minimum). Calibration equipment traceable to national standards (NIST, NRC Canada).

**PR-2: Test Completion Before Startup**

All required test records complete and approved before instrument or system placed in operational service. No deviations or punch list items outstanding that affect safety or operability.

**PR-3: Record Quality**

Test records legible, complete (no blank fields unless marked N/A), signed by qualified personnel, dated. Non-conformances documented with corrective actions.

**Source:** **ASSUMPTION** based on typical commissioning quality requirements

### Interface Requirements

**INT-1: Construction Interface**

Test records verify construction work (installation inspections). Deficiencies identified on punch lists for correction before final acceptance.

**INT-2: Operations Interface**

Test records establish operational baseline (as-commissioned calibration data, alarm setpoints, control loop tuning). Records provided to operations for maintenance planning (recalibration schedules).

**INT-3: Regulatory Interface**

Test records may be required for permitting and safety approvals (overfill protection verification per API 2350, SIS verification per ISA 84, hazardous area compliance per CSA C22.1).

**Source:** **ASSUMPTION** based on typical commissioning and regulatory interfaces

### Quality Requirements

**QR-1: Qualified Personnel**

Testing and inspection performed by qualified personnel: certified calibration technicians, experienced commissioning engineers, QA/QC inspectors.

**QR-2: Independent Verification**

Critical tests (safety systems, custody transfer) may require independent verification or witness by Owner/regulatory authority. **TBD**: Hold points and witness points per project QA plan.

**QR-3: Record Retention**

Test records retained as permanent facility records per contract requirements and regulatory obligations. **TBD**: Retention period and archival format.

**Source:** **ASSUMPTION** based on typical EPC quality and record retention requirements

## Standards

**Applicable Standards:**

- ISA 84 / IEC 61511 (SIS verification and testing)
- API 2350 (overfill protection testing)
- CSA C22.1 (hazardous area installation inspection)
- ISO/IEC 17025 (calibration laboratory accreditation)
- Project QA plan and commissioning procedures

**Note:** Specific standards **TBD** based on project QA/commissioning requirements.

## Verification

**Verification Methods:**

Test records reviewed and approved by: commissioning lead (technical review), QA/QC manager (compliance review), Owner representative (acceptance review if required).

**Acceptance Criteria:**

Records complete, accurate, signed by qualified personnel. All tests passed (or non-conformances resolved with corrective actions). Equipment calibrated within specification tolerances. Loops functional and alarm/interlock setpoints verified.

**Source:** **ASSUMPTION** based on typical commissioning acceptance criteria

## Documentation

**Required Outputs:**

- Calibration certificates (factory and field)
- Loop check records
- FAT records (if applicable)
- Installation inspection records
- Functional test records

**Organization:** **TBD** — By instrument tag, by system, by test type, or by date

**Format:** **TBD** — Paper forms, electronic records, or database format per project commissioning system

**Management:**

Test records compiled during commissioning. Final record package provided to Owner at facility turnover. Retained as permanent facility records.

**Project Objective Alignment:**

Supports **OBJ-1: Safe & Reliable Operation** — Test records demonstrate instrumentation is correctly installed, calibrated, and functional for safe operations.

**Source:** Decomposition Section 6 (line 780)

## Cross-Document Traceability

This Specification defines requirements for DEL-20.05. The following documents provide complementary information:

| Document | Purpose | Key Linkages |
|----------|---------|--------------|
| Datasheet.md | Factual identification, attributes, conditions, references | Attributes § defines record types; Construction § provides record content details |
| Guidance.md | Engineering rationale and decision context | Principles explain quality gate approach; Trade-off addresses calibration methods |
| Procedure.md | Production workflow and verification steps | Steps 1-6 implement FR-1 to FR-5; Verification implements QR-1 to QR-3 |

**Requirement-to-Procedure Mapping:**

| Requirement | Procedure Step | What Is Implemented |
|-------------|----------------|---------------------|
| FR-1 Completeness | Steps 1-5 | All instruments tested through commissioning lifecycle |
| FR-2 Calibration | Step 3 | Pre-commissioning calibration and certificates |
| FR-3 Loop Checks | Step 3 | Loop check verification |
| FR-4 Installation Inspection | Step 1 | Installation inspection records |
| FR-5 Functional Tests | Steps 4, 5 | Wet calibration, functional and performance testing |
| QR-1 to QR-3 | Step 6 | Record compilation and quality verification |
