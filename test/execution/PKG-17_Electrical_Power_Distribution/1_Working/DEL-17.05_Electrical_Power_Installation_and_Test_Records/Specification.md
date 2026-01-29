# Specification: DEL-17.05 Electrical Power Installation & Test Records

## Scope

This specification defines the requirements for **Electrical Power Installation & Test Records** within **PKG-17 Electrical Power Distribution**.

**Purpose** (Source: Decomposition DEL-17.05 entry): Provides evidence of completion, inspection, and testing for electrical power.

**Anticipated deliverable artifacts** (Source: _CONTEXT.md): FAT records, insulation test records, protection relay test records

## Requirements

### Functional Requirements

**FR-1: Comprehensive Test Record Documentation**
- Test records shall document all factory and field tests performed on electrical power distribution equipment
- Record types: FAT records (transformers, switchgear, MCCs), insulation resistance tests (Megger), Hi-Pot tests (MV cables/equipment), protection relay tests, circuit breaker operation tests, ground resistance tests, load/energization tests
- **Source**: CEC, IEEE testing standards; project commissioning requirements
- **Rationale**: Complete test records provide evidence of code compliance, support warranty claims, enable future troubleshooting. See Guidance.md — Principle 4 (Document Everything).
- **Procedure**: See Procedure.md — Steps 1-4 (Testing Steps), Step 5 (Test Record Compilation).

**FR-2: Test Results and Acceptance Criteria**
- All test records shall include: Equipment identification, test method/standard, acceptance criteria, actual test results, pass/fail determination
- Failed tests shall be documented with corrective action and retest results
- **Source**: Quality assurance and regulatory compliance requirements
- **Rationale**: See Guidance.md — Principle 1 (Testing as Verification), Consideration 4 (Test Failures and Retesting).
- **Procedure**: See Procedure.md — Steps 2-4 (Testing Steps with acceptance criteria).

**FR-3: Test Equipment Calibration**
- Test records shall identify test equipment used (make, model, serial number, calibration date)
- Test equipment shall have valid calibration (within calibration interval)
- **Source**: Quality assurance requirements; ISO 17025 (testing laboratory standards)
- **Rationale**: See Guidance.md — Principle 3 (Test Equipment Calibration).
- **Procedure**: See Procedure.md — Step 5b (Test Record Review — verify calibration valid).

### Performance Requirements

**PR-1: Test Timing and Sequencing**
- Factory tests (FAT) performed before equipment shipment
- Field insulation tests (Megger, Hi-Pot) performed before energization
- Protection relay tests and breaker operation tests performed during commissioning
- Load tests and system energization performed per commissioning plan sequence
- **Source**: Safe and logical testing sequence; industry best practices

**PR-2: BC Safety Authority Compliance**
- Test records shall satisfy BC Safety Authority inspection requirements for electrical permit closeout
- Electrical inspector may witness critical tests (energization, final system tests)
- **Source**: BC Electrical Safety Regulation; OBJ-6 (Regulatory Compliance)

### Quality Requirements

**QR-1: Test Performer Qualifications**
- Factory tests performed by manufacturer qualified personnel
- Field tests performed by qualified electrical technicians or engineers (certified electricians, P.Eng., or C.E.T.)
- Protection relay testing performed by qualified relay technicians (manufacturer-certified or equivalent)
- **Source**: Professional competency requirements; test standard requirements

**QR-2: Test Record Sign-Off and Approval**
- All test records signed by test performer
- Critical tests (FAT, relay tests, energization) reviewed and approved by electrical engineer (P.Eng.)
- Commissioning test summary approved by discipline lead and Employer (for system turnover)
- **Source**: Quality assurance and project closeout requirements

**QR-3: As-Built Record Retention**
- Test records shall be retained permanently (life of facility) as part of project as-built documentation
- Records filed in 3_Issued/ folder and delivered to Owner
- **Source**: Record retention requirements; operations and maintenance needs

## Standards

**Primary Test Standards**:
- CEC (CSA C22.1) — Installation and testing requirements
- CSA C88, C802 — Transformer factory tests
- CSA C22.2 No. 31, No. 254 — Switchgear and MCC factory tests
- IEEE C37.09, C37.50, C37.90 — Circuit breaker and relay testing
- IEEE Std 43 — Insulation resistance testing
- IEEE Std 81 — Ground resistance testing
- IEEE Std 400 — MV cable testing

## Verification

**Verification Methods**:
- Test record review (verify completeness, acceptance criteria met, test equipment calibration valid)
- Witness testing (for critical tests)
- Electrical inspector approval (BC Safety Authority)

**Acceptance Criteria**:
- All required tests performed and documented
- All test results meet acceptance criteria (pass)
- Failed tests corrected and retested successfully
- Test records signed and approved

## Documentation

**Required Outputs** (Source: _CONTEXT.md):
- FAT records (transformers, switchgear, MCCs)
- Insulation test records (Megger, Hi-Pot)
- Protection relay test records
- Circuit breaker operation test records
- Ground resistance test records
- Load test / energization records
- Commissioning test summary

**Cross-References**:
- **Datasheet.md**: Test record types, content, and acceptance criteria
- **Guidance.md**: Testing principles, best practices, and common issues
- **Procedure.md**: Step-by-step testing procedures and sign-off process
- **DEL-17.02**: Specifications defining test requirements
- **DEL-17.03**: Protection coordination settings for relay tests
- **DEL-17.04**: FAT records from manufacturer data sheets

---
**Cross-Document Alignment Verified (Pass 3):** All functional requirements (FR-1 through FR-3), performance requirements (PR-1, PR-2), and quality requirements (QR-1 through QR-3) are traceable to Datasheet.md test record types, Guidance.md principles/considerations, and Procedure.md steps. No conflicts identified.
