# Specification: DEL-29.04 FAT Installation & Test Records

## Scope

This specification defines requirements for **FAT Installation & Test Records** within **PKG-29 Testing**.

**Purpose:** Provides evidence of completion, inspection, and testing for FAT. **Source:** Decomposition line 649

**Deliverable Type:** Record | **Responsible:** D&B Contractor (QA/QC)

### Inclusions

FAT records for major equipment including:
- Mechanical equipment (pumps, loading arms, specialty valves)
- Electrical equipment (MCCs, switchgear, VFDs)
- I&C equipment (control panels, PLCs, metering systems)

### Exclusions

- Routine commercial equipment not requiring FAT
- Site acceptance tests (covered by DEL-29.05)
- Commissioning tests (covered by PKG-30)

## Requirements

### Functional Requirements

**FR-1: FAT Scope Definition**
- ITP (DEL-29.02) shall identify which equipment requires FAT
- Purchase orders shall specify FAT requirements
- FAT procedures shall be submitted by vendor for approval or provided by project

**FR-2: FAT Record Content**
Each FAT report shall include:
- Equipment identification and specification reference
- Pre-FAT inspection results (dimensional, material, workmanship)
- Performance test results with acceptance criteria
- Functional test results (controls, interlocks, safety features)
- Deficiencies and resolution
- Witness signatures per ITP requirements

**FR-3: Traceability**
- FAT records traceable to purchase orders and specifications
- FAT records traceable to ITP witness requirements
- Test instruments traceable to calibration standards

### Performance Requirements

**PR-1: Acceptance Criteria**
- Equipment performance shall meet or exceed purchase specification requirements
- All functional tests shall demonstrate correct operation
- Deficiencies shall be resolved before shipment or documented as punch list for site completion

**PR-2: Witness Requirements**
- Contractor QC shall witness all FATs per procurement plan
- Employer shall witness FATs designated in ITP as hold or witness points
- Adequate advance notice (typically 3-4 weeks) shall be provided for witnessed FATs

**TBD:** Specific notification periods per Employer's Requirements **location TBD**

### Interface Requirements

**IR-1: Vendor Coordination**
- Vendors shall provide FAT procedures for approval
- Vendors shall schedule FATs with adequate notice
- Vendors shall provide qualified test personnel and calibrated test equipment

**IR-2: Contractor Responsibilities**
- Review and approve vendor FAT procedures
- Witness FATs and document results
- Coordinate Employer and third-party witnesses
- Accept equipment contingent on satisfactory FAT

**IR-3: Documentation Flow**
- FAT reports from vendors reviewed by Contractor QC
- Approved FAT reports filed in project records (this deliverable)
- FAT records provided to commissioning team and O&M

### Quality Requirements

**QR-1: FAT Procedure Approval**
- Vendor FAT procedures shall be submitted for approval minimum 2 weeks before FAT **ASSUMPTION**
- Procedures shall be reviewed for adequacy (covers specification requirements, adequate acceptance criteria)

**QR-2: Deficiency Management**
- Deficiencies identified during FAT shall be documented
- Critical deficiencies shall be corrected before shipment
- Minor deficiencies may be added to punch list for site completion (with Employer concurrence)
- Re-tests conducted after corrections

**QR-3: Record Quality**
- FAT reports shall be complete, legible, and signed
- Test data shall be accurate and traceable
- Photographs shall document equipment condition and test setup

## Standards

**Quality Management:**
- ISO 9001: Quality Management Systems (supplier quality requirements)
- Project Quality Management Plan **location TBD**

**Equipment-Specific Standards:**
- API 610: Centrifugal Pumps (pump performance testing)
- NFPA 20: Stationary Pumps for Fire Protection (fire pump testing)
- IEC 61439: Low-Voltage Switchgear and Controlgear Assemblies (electrical panel testing)
- IEC 61511: Functional Safety - SIS (safety system testing)
- Measurement Canada: Weights and Measures Act (custody transfer metering) **ASSUMPTION**

## Verification

**VM-1: Completeness Check**
- Verify all equipment identified for FAT has FAT records

**VM-2: Content Verification**
- Verify FAT reports include all required elements
- Verify test results meet acceptance criteria
- Verify deficiencies resolved or documented

**VM-3: Signature Verification**
- Verify vendor, Contractor, and Employer witness signatures (per ITP requirements)

### Acceptance Criteria

**AC-1:** FAT conducted for all specified equipment
**AC-2:** All FAT reports complete with required content
**AC-3:** All equipment passed FAT or deficiencies resolved
**AC-4:** All required witness signatures obtained
**AC-5:** FAT records compiled and archived

## Documentation

**Required Outputs:**

**Factory Acceptance Test Reports (by equipment):**
- Pumps: FAT report per API 610 or vendor standard
- Loading arms: FAT report per manufacturer standard
- MCCs/Switchgear: FAT report per IEC or vendor standard
- Control panels/PLCs: FAT report including I/O verification and logic testing
- Metering systems: FAT report including calibration and proving

**Supporting Documentation:**
- Vendor FAT procedures (approved)
- Test data sheets
- Photographs
- Deficiency lists and resolutions
- Material certifications (verified during FAT)

**Compilation:**
- Organized by equipment tag or system
- Index provided
- Filed in project document management system (permanent records)
