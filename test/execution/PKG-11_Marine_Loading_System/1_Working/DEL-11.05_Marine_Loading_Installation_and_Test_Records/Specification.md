# Specification: DEL-11.05 Marine Loading Installation & Test Records

## Scope

This specification defines the requirements for **Marine Loading Installation & Test Records** within **PKG-11 Marine Loading System**.

**Purpose:** Provides evidence of completion, inspection, and testing for the marine loading system, demonstrating compliance with specification requirements and readiness for operation.

**Package scope (PKG-11):**
- Powered loading arm (articulated boom with powered slew/luff)
- Emergency release coupling (ERC)
- Double-walled export pipe
- Leak detection system
- Nitrogen supply provisions
- Operator shelter

**Anticipated deliverable artifacts:**
- FAT records
- Installation records
- Leak detection test records

**Objectives served (per decomposition Section 6):**
- OBJ-1 Safe & Reliable Operation
- OBJ-2 Throughput Capacity (1,000,000 MT/annum)
- OBJ-4 Operational Flexibility
- OBJ-7 Environmental Protection

## Related Deliverables (PKG-11)

| Deliverable | Relationship |
|-------------|--------------|
| DEL-11.01 Marine Loading Design Drawing Set | As-installed verification reference |
| DEL-11.02 Marine Loading Technical Specification | Acceptance criteria source (§9) |
| DEL-11.03 Marine Loading Design Calculations | Verification of calculated values |
| DEL-11.04 Marine Loading Data Sheet Package | Tag/duty reference |
| DEL-11.06 Marine Loading Arm OEM Qualification Package | FAT procedures and OEM documentation |

## Requirements

### General Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| ITR-001 | Provide a records index/register with IDs, equipment tags, dates, and status | Document review |
| ITR-002 | Each record shall be uniquely identified and revision controlled | Document review |
| ITR-003 | Records shall be traceable to test/inspection procedure or method statement | Traceability check |
| ITR-004 | Records shall reference acceptance criteria (ER clause, code, or specification) | Traceability check |
| ITR-005 | Records shall include equipment tag and location | Completeness check |
| ITR-006 | Records shall be legible with required signatures and dates | Signature check |
| ITR-007 | Records shall comply with project QA/QC procedures | QA audit |

### FAT Record Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| FAT-001 | Provide FAT records for loading arm (functional test, envelope verification) | Document review |
| FAT-002 | Provide FAT records for ERC (release force, valve closure, reset) | Document review |
| FAT-003 | Provide FAT records for leak detection sensors (calibration, response) | Document review |
| FAT-004 | Provide FAT records for sump pump (performance curve, motor test) | Document review |
| FAT-005 | FAT records shall include witness sign-off per project ITP | Signature check |
| FAT-006 | FAT records shall reference OEM test procedures | Traceability check |
| FAT-007 | FAT records shall include acceptance criteria and pass/fail status | Completeness check |

### Installation Record Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| INS-001 | Provide mechanical completion checklist for loading arm installation | Document review |
| INS-002 | Provide pipe installation checklist for double-walled pipe | Document review |
| INS-003 | Provide instrument installation checklist for leak detection devices | Document review |
| INS-004 | Provide as-installed verification against IFC drawings | Cross-reference check |
| INS-005 | Installation records shall include torque values, alignment data as applicable | Completeness check |
| INS-006 | Installation records shall include inspector sign-off | Signature check |

### Commissioning / Functional Test Record Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| COM-001 | Provide loading arm functional test record (slew/luff, position feedback, controls) | Document review |
| COM-002 | Provide ERC functional test record (manual activation, auto-release simulation) | Document review |
| COM-003 | Provide leak detection loop test record (simulated leak, alarm, ESD trip) | Document review |
| COM-004 | Provide sump pump functional test record (level control, run/stop) | Document review |
| COM-005 | Provide ESD integration test record (trip signals, interlocks) | Document review |
| COM-006 | Test records shall include test procedure reference | Traceability check |
| COM-007 | Test records shall include acceptance criteria and measured values | Completeness check |
| COM-008 | Test records shall include witness sign-off per project ITP | Signature check |

### Interface Record Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| INT-001 | Capture electrical energization sign-off (PKG-20 interface) | Interface check |
| INT-002 | Capture I&C loop check records (PKG-19 interface) | Interface check |
| INT-003 | Capture ESD integration verification (PKG-29 interface) | Interface check |
| INT-004 | Capture drainage system completion sign-off (PKG-03 interface) | Interface check |

**Note:** Dependency tracking is NOT_TRACKED; interfaces are coordinated externally per `_DEPENDENCIES.md`.

### Quality Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| QA-001 | Test instrument calibration certificates shall be included and current | Calibration check |
| QA-002 | Nonconformances shall be documented on NCR and dispositioned | NCR review |
| QA-003 | Punch list items shall be documented and tracked to closure | Punch list review |
| QA-004 | MDR completeness check required prior to turnover submission | MDR review |

## Standards

| Standard | Applicability | Status |
|----------|---------------|--------|
| Employer's Requirements (ER) | Witness/hold points, acceptance criteria | Clause references **TBD** |
| Project ITP | Inspection and test plan | **TBD** |
| Project QA/QC procedures | Record format and control | **TBD** |
| IEC 61511 | SIS testing requirements (leak detection/ESD) | **TBD** |

## Verification

**Verification methods for Record deliverables:**

| Method | Description | Applies To |
|--------|-------------|------------|
| Completeness check | All required records present per index | ITR-001 to ITR-007 |
| Traceability check | Acceptance criteria referenced | ITR-003, ITR-004 |
| Signature check | Required signatures and witness present | FAT-005, INS-006, COM-008 |
| Cross-reference check | As-installed matches IFC drawings | INS-004 |
| Calibration check | Test instrument calibrations current | QA-001 |
| NCR review | NCRs documented and closed | QA-002 |

**Acceptance criteria:**
- Records index complete with all required records
- Each record traceable to acceptance criteria
- Required signatures and witness obtained
- Calibration certificates current
- NCRs documented and dispositioned
- Punch list items closed or formally accepted

## Documentation

**Required documentation outputs:**
- FAT records package
- Installation records package
- Leak detection test records
- Commissioning test records
- Records index/register

**Documentation requirements:**
- All documents shall comply with project document control procedures
- Revision control per project numbering system — **TBD**
- Format: **TBD** (project document management requirements)
- Archival format: **TBD** (electronic/physical per project requirements)

---

**Pass 3 Enrichment Notes (Final Quality Check):**
- Verified all 36 requirements have unique IDs: ITR-001 to ITR-007 (7), FAT-001 to FAT-007 (7), INS-001 to INS-006 (6), COM-001 to COM-008 (8), INT-001 to INT-004 (4), QA-001 to QA-004 (4)
- Verified all requirements include verification method column
- Verified 3 record categories (FAT, installation, commissioning) align with Datasheet §Construction and Procedure §Steps 3-5
- Verified FAT requirements (7) trace to DEL-11.06 OEM data and DEL-11.02 §9
- Verified INS requirements (6) trace to DEL-11.01 IFC drawings and project ITP
- Verified COM requirements (8) trace to DEL-11.02 §6 (leak detection) and §9 (commissioning)
- Verified INT requirements (4) cover PKG-20, PKG-19, PKG-29, PKG-03 interfaces
- Verified Related Deliverables table (5 deliverables) consistent with Datasheet §Cross-Document Links
- Verified Standards table (4 standards) and Verification methods (6 methods)
- Verified acceptance criteria (6 items) align with Datasheet §Deliverable Acceptance (6 criteria)
- Confirmed terminology consistent with DEL-11.02: FAT, SAT, loop test, ESD integration, NCR
- All TBDs and ASSUMPTIONs retained with proper labeling
- Pass 3 complete — document ready for WORKING_ITEMS session
