# Specification: DEL-29.05 SAT Installation & Test Records

## Scope

Requirements for **SAT Installation & Test Records** within **PKG-29 Testing**.

**Purpose:** Provides evidence of completion, inspection, and testing for SAT. **Source:** Decomposition line 650

**Type:** Record | **Responsible:** D&B Contractor (QA/QC)

### Inclusions
SAT records for integrated systems: railcar unloading, transfer, storage, marine loading, electrical, control, fire protection

### Exclusions
- Individual equipment FATs (DEL-29.04)
- Commissioning performance tests (PKG-30)

## Requirements

### Functional Requirements

**FR-1: SAT Prerequisites**
- FATs complete for major equipment
- Installation complete and hydrostatic/electrical/I&C tests passed
- Pre-commissioning complete (cleaning, flushing, initial energization)

**FR-2: SAT Scope**
- Functional testing of all operating modes (normal, abnormal, emergency)
- Integration testing of system interfaces
- Safety system verification (ESD, alarms, interlocks)
- Performance verification (flows, pressures, metering accuracy)

**FR-3: SAT Documentation**
Each SAT report shall include: System ID, prerequisites verified, test procedures followed, test results, deficiencies and resolution, witness signatures

### Performance Requirements

**PR-1: Acceptance Criteria**
- Systems perform per design specifications
- All safety functions operate correctly
- Custody transfer metering within specified accuracy
- Deficiencies resolved or on documented punch list

**PR-2: Witness Requirements**
- Contractor test engineer and QC present
- Employer witness per ITP requirements
- Operations representatives participate for training

### Interface Requirements

**IR-1:** SATs demonstrate system-to-system interfaces function correctly
**IR-2:** SAT completion is prerequisite for commissioning (PKG-30)

### Quality Requirements

**QR-1:** SAT procedures approved before testing
**QR-2:** Deficiencies managed through NCR process
**QR-3:** SAT records permanent quality records

## Standards

- IEC 62382: Loop checking
- ISA-88: Batch control (if applicable)
- Project commissioning procedures
- Employer's Requirements **location TBD**

## Verification

**VM-1:** All systems have SAT reports
**VM-2:** All SATs passed or deficiencies resolved
**VM-3:** Required witness signatures obtained

### Acceptance Criteria
**AC-1:** SATs complete for all systems
**AC-2:** All SAT reports complete and signed
**AC-3:** Systems ready for commissioning

## Documentation

**Required Outputs:**
- Site Acceptance Test Reports (by system)
- Organized by system or package
- Index provided
- Permanent records in document management system
