# Specification: DEL-29.03 Test Installation & Test Records

## Scope

This specification defines the requirements for **Test Installation & Test Records** within **PKG-29 Testing**.

**Purpose:** Provides evidence of completion, inspection, and testing for test. **Source:** Decomposition line 648

**Deliverable Type:** Record
**Responsible Party:** D&B Contractor (QA/QC)

### Inclusions

Test records generated from:
1. **Hydrostatic test records** — Pressure testing of tanks, piping, loading systems
2. **Electrical test records** — Insulation, continuity, protection, energization testing
3. **Instrument calibration records** — Calibration certificates for all field instruments

**Source:** _CONTEXT.md, Decomposition line 648

### Exclusions

- FAT records (covered by DEL-29.04)
- SAT records (covered by DEL-29.05)
- Commissioning records (covered by PKG-30)
- Hydrotest water management records (covered by DEL-29.06-29.08)

## Requirements

### Functional Requirements

**FR-1: Record Completeness**
- All tests performed per DEL-29.01 procedures shall have corresponding test records
- All ITP (DEL-29.02) activities marked as completed shall have supporting records
- Records shall include all required data fields per test procedure

**Source:** ISO 9001 (record requirements), DEL-29.01, DEL-29.02 cross-reference

**FR-2: Record Content**
Each test record shall include:
- System/equipment identification
- Test procedure reference
- Test date and personnel
- Test data (measured values)
- Acceptance criteria and results (pass/fail)
- ITP activity number and hold/witness signatures (if applicable)
- Non-conformance references (if test failed)
- Approvals and certifications

**Source:** Typical EPC test record requirements **ASSUMPTION**

**FR-3: Traceability**
- Records shall be traceable to ITP activity numbers (DEL-29.02)
- Records shall be traceable to test procedures (DEL-29.01)
- Records shall be traceable to design documents (drawings, specifications)
- Calibration records shall be traceable to calibration standards (with NIST or equivalent traceability)

**Source:** ISO 9001, ISO 17025 (calibration traceability) **ASSUMPTION**

### Performance Requirements

**PR-1: Data Accuracy**
- Test data shall be recorded accurately and legibly
- Instrument readings shall be recorded to appropriate precision per instrument accuracy
- Calculations (if any) shall be verified
- Data alterations shall be crossed out (not erased) and initialed

**Source:** Good laboratory practice, ISO 9001 **ASSUMPTION**

**PR-2: Timeliness**
- Test records shall be completed and signed on the day of test (or immediately following)
- Records shall be submitted for review within **TBD** days of test completion
- Complete record package shall be compiled and issued within **TBD** days of project testing completion

**TBD:** Specific timing requirements per project quality plan **location TBD**

### Interface Requirements

**IR-1: Upstream Interface**
- Test records implement procedures from DEL-29.01
- Test records document ITP activities from DEL-29.02
- Test records reference design basis from design deliverables (all packages)

**IR-2: Downstream Interface**
- Test records support commissioning activities (PKG-30)
- Test records provide baseline for O&M documentation
- Test records submitted to authorities for operating permits

### Quality Requirements

**QR-1: Record Review and Approval**
- Test records shall be reviewed by QC inspector or Engineer
- Failed tests shall be documented via non-conformance process
- Re-tests (after repair) shall be recorded and cross-referenced to original test and NCR
- Final record package shall be approved by QA/QC Manager

**QR-2: Record Retention**
- Test records are permanent quality records retained for facility lifetime **ASSUMPTION**
- Records shall be maintained in controlled storage (electronic and/or hardcopy)
- Access to records shall be controlled per document management procedures

**Source:** ISO 9001, typical facility asset management requirements **ASSUMPTION**

## Standards

**Quality Management:**
- ISO 9001: Quality Management Systems (record requirements)
- ISO 17025: Testing and Calibration Laboratories (calibration record requirements) **ASSUMPTION**

**Testing and Inspection:**
- ASME B31.3: Process Piping (test documentation requirements)
- API 650: Welded Tanks for Oil Storage (test record requirements)
- NFPA 70: National Electrical Code (electrical test documentation)
- IEC 62382: Electrical and instrumentation loop check (calibration documentation)
- Project Quality Management Plan: **location TBD**

## Verification

**VM-1: Completeness Check**
- Verify all required tests have corresponding records (cross-check against ITP and test log)
- Verify all required data fields are populated

**VM-2: Data Verification**
- Verify test results meet acceptance criteria
- Verify calculations are correct (if applicable)
- Verify calibration standards have valid certifications

**VM-3: Signature Verification**
- Verify required signatures present (tester, QC, Engineer, Employer witness)
- Verify signatories are qualified/authorized

**VM-4: Archival Compliance**
- Verify records are in specified format (electronic PDF, scanned hardcopy, etc.)
- Verify legibility and reproducibility

### Acceptance Criteria

**AC-1:** All required test records present (100% of tests performed)
**AC-2:** All test records complete (all data fields populated)
**AC-3:** All tests passed or NCRs closed for failed tests
**AC-4:** All required reviews and approvals obtained
**AC-5:** Records archived in specified format and location

## Documentation

**Required Outputs:**

1. **Hydrostatic Test Records** — One record per test (tanks, piping systems, equipment)
2. **Electrical Test Records** — Records by equipment or system tested
3. **Instrument Calibration Records** — One record per instrument calibrated

**Format:**
- Completed test data sheets (from DEL-29.01 procedures)
- Test reports (narrative + data)
- Certifications and certificates (calibration certs, QC sign-offs)
- Photographs (test setup, results, defects if any)
- Supporting data (pressure charts, waveforms, etc.)

**Compilation:**
- Records compiled into binders or electronic folders by system or test type
- Index or table of contents provided
- Cross-reference to ITP activity numbers

**Retention:**
- Permanent facility records
- Electronic archive in project document management system
- Hardcopy archive per project records management plan **location TBD**
