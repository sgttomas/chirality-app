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

---

## Cross-Document Linkage

| Document | Key Sections | Relationship |
|----------|--------------|--------------|
| Datasheet.md | §Attributes, §Construction, §References | Captures SAT system types, content structure, and cross-references |
| Guidance.md | §Principles, §Considerations, §Trade-offs, §Examples | Provides rationale and examples for implementing requirements |
| Procedure.md | §Steps 1-6, §Verification | Defines process for implementing these requirements |

**Requirement-to-Guidance Traceability:**
- FR-1 (Prerequisites) → Guidance §Principles (SAT vs. Commissioning), §Considerations Item 1 (Timing)
- FR-2 (SAT Scope) → Guidance §Principles (System Integration, Fail-safe Testing)
- FR-3 (Documentation) → Guidance §Examples (SAT Report)
- PR-1 (Acceptance) → Guidance §Trade-offs Item 1 (Comprehensive vs. Schedule)
- PR-2 (Witness) → Guidance §Considerations Item 4 (Operations Training)

**Requirement-to-Procedure Traceability:**
- FR-1 (Prerequisites) → Procedure Step 1 (Verify Prerequisites)
- FR-2 (Scope) → Procedure Step 2 (Develop Procedures), Step 4 (Conduct SATs)
- FR-3 (Documentation) → Procedure Steps 4, 6 (Document, Compile)
- PR-2 (Witness) → Procedure Step 3 (Schedule/Coordinate)
- QR-2 (Deficiencies) → Procedure Step 5
