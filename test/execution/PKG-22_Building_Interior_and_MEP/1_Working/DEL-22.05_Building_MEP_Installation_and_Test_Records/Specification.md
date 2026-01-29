# Specification: DEL-22.05 Building MEP Installation and Test Records

## Scope

This specification defines the requirements for **Building MEP Installation and Test Records** within **PKG-22 Building Interior & MEP**.

**Deliverable Description:** Provides evidence of completion, inspection, and testing for building MEP per Employer's Requirements.

**Source:** Decomposition REVISED_v2.md, DEL-22.05 entry; _CONTEXT.md

### Included

This record package shall include:

1. **HVAC test records** — Duct testing, air balance, equipment commissioning, functional performance testing
2. **Plumbing test records** — Pressure testing, leak testing, flow testing, backflow preventer certification
3. **Fire suppression test records** — Hydrostatic testing, main drain test, system acceptance testing per NFPA 13

**Source:** Decomposition REVISED_v2.md, DEL-22.05 anticipated artifacts

### Excluded

- Electrical testing records for main power distribution (covered by PKG-17)
- Control system commissioning records (covered by PKG-19, though MEP system functional testing interfaces shall be documented)
- Building structural inspections (covered by PKG-21)

**Source:** Package scope boundaries

### Relationship to Other Deliverables

These test records:
- **Verify installation per DEL-22.01** drawings
- **Demonstrate compliance with DEL-22.02** specifications
- **Validate performance per DEL-22.03** calculations
- **Confirm equipment meets DEL-22.04** data sheet requirements

**Source:** Standard EPC deliverable relationships

## Requirements

### Functional Requirements

#### FR-01: Record Completeness

All required installation and test records shall be documented per:
- NBC 2020 requirements for building systems
- NFPA 13 requirements for fire protection acceptance testing
- ASHRAE commissioning requirements for HVAC systems
- Project Quality Management Plan requirements

**Rationale**: See Guidance.md, Section "Purpose of Installation and Test Records"

**Verification**: See Procedure.md, Step 1 (record identification), Step 4 (completeness check)

**Source:** NBC 2020, NFPA 13, ASHRAE Guideline 1.1; project QA/QC requirements

#### FR-02: HVAC Testing Requirements

- **FR-02.1**: Duct pressure testing per SMACNA standards (leakage class verification)
- **FR-02.2**: Air and water balance (TAB) per ASHRAE/SMACNA to verify design airflows and water flows
- **FR-02.3**: Equipment functional performance testing (capacity, efficiency, control sequences)
- **FR-02.4**: Temperature control verification (setpoints, dead bands, reset schedules)

**Rationale**: See Guidance.md, Section "HVAC Testing and Commissioning Requirements"

**Verification**: See Procedure.md, Step 2 (data collection - HVAC testing)

**Source:** ASHRAE Guideline 1.1, SMACNA TAB standards

#### FR-03: Plumbing Testing Requirements

- **FR-03.1**: Water supply pressure testing per NBC 2020 / CSA B64 (hydrostatic test at 1.5× operating pressure for 2 hours typical)
- **FR-03.2**: Drainage leak testing (air or water test per NBC 2020)
- **FR-03.3**: Backflow preventer testing and annual certification
- **FR-03.4**: Hot water system performance (temperature, recovery rate, flow)

**Rationale**: See Guidance.md, Section "Plumbing Testing Requirements"

**Verification**: See Procedure.md, Step 2 (data collection - plumbing testing)

**Source:** NBC 2020, CSA B64 series

#### FR-04: Fire Suppression Testing Requirements

- **FR-04.1**: Hydrostatic testing per NFPA 13 (200 psi for 2 hours for steel pipe; verify per NFPA 13 for other materials)
- **FR-04.2**: Main drain test (flow and pressure at most remote drain to verify water supply adequacy)
- **FR-04.3**: System trip test (alarm valve actuation, water motor gong, supervisory signals)
- **FR-04.4**: Fire pump testing (if applicable): capacity test, run test, weekly/monthly tests
- **FR-04.5**: AHJ (Fire Marshal) final inspection and acceptance

**Rationale**: See Guidance.md, Section "Fire Protection Testing Requirements (NFPA 13)"

**Verification**: See Procedure.md, Step 2 (data collection - fire protection testing)

**Source:** NFPA 13 acceptance testing requirements

### Performance Requirements

#### PR-01: Testing Witness and Sign-Off

- All critical tests shall be witnessed by qualified personnel (contractor QA/QC, third-party commissioning agent, or owner's representative)
- Test records shall include signatures of tester, witness, and approver
- Failed tests shall be documented with corrective actions and retesting

**Rationale**: See Guidance.md, Section "Quality Assurance and Witness Requirements"

**Verification**: See Procedure.md, Step 3 (verification); witness signature requirements

**Source:** ASSUMPTION: standard QA/QC testing requirements

#### PR-02: Acceptance Criteria

All testing shall demonstrate:
- Systems installed per DEL-22.01 drawings and DEL-22.02 specifications
- Equipment performs per DEL-22.04 data sheet requirements
- System performance meets DEL-22.03 design calculations
- Code compliance demonstrated per NBC 2020, NFPA 13, and applicable standards

**Rationale**: See Guidance.md, Section "Acceptance Criteria and Performance Verification"

**Verification**: See Procedure.md, Step 3 (verification), Step 5 (submission and acceptance)

**Source:** Design deliverables cross-reference; code compliance requirements

#### PR-03: Commissioning Authority Acceptance

- **TBD** — Project may have commissioning authority (CxA) or third-party commissioning agent (location TBD)
- If commissioning authority appointed, all test records shall be reviewed and accepted by CxA
- Commissioning report summarizing testing results and system acceptance shall be prepared

**Rationale**: See Guidance.md, Section "Commissioning Process and Authority"

**Verification**: See Procedure.md, Step 5 (submission and acceptance)

**Source:** ASHRAE Guideline 0 commissioning process; project-specific commissioning requirements TBD

### Interface Requirements

#### IF-01: Coordination with Construction Contractor

Test records shall be coordinated with construction contractor:
- Construction completion and punch list closeout before testing
- Contractor QA/QC personnel shall witness or conduct testing
- Test records submitted as part of construction closeout package

**Rationale**: Testing cannot proceed until installation is substantially complete

**Verification**: See Procedure.md, Step 2 (data collection - construction readiness)

**Source:** Standard construction testing coordination

#### IF-02: Coordination with Commissioning Agent (if applicable)

If commissioning agent appointed:
- Test procedures and schedules coordinated with CxA
- CxA witnesses critical tests
- Test records submitted to CxA for review and acceptance

**Rationale**: See Guidance.md, Section "Commissioning Process and Authority"

**Verification**: See Procedure.md, Step 5 (CxA review)

**Source:** ASHRAE commissioning requirements; project commissioning plan TBD

#### IF-03: Authority Having Jurisdiction (AHJ) Inspections

Test records shall support AHJ inspections:
- Fire Marshal inspection and acceptance of fire protection system per NFPA 13
- Building inspector acceptance of plumbing and HVAC systems per NBC 2020
- AHJ sign-off required for building permit closeout

**Rationale**: See Guidance.md, Section "Regulatory Inspections and Code Compliance"

**Verification**: See Procedure.md, Step 5 (AHJ inspection coordination)

**Source:** NBC 2020, NFPA 13 inspection requirements; Surrey, BC permitting process

### Quality Requirements

#### QR-01: Record Authenticity and Traceability

- All test records shall be original signed documents (or controlled electronic records with audit trail)
- Test data shall be traceable to calibrated instruments (calibration certificates required)
- Any corrections or modifications shall be initialed and dated
- Records shall be legible and complete

**Rationale**: See Guidance.md, Section "Record Management and Quality Assurance"

**Verification**: See Procedure.md, Step 4 (verification - record quality check)

**Source:** ISO 9001 quality record requirements; project QA/QC procedures

#### QR-02: Record Retention

- Installation and test records shall be retained per project record retention requirements — **TBD** (location TBD)
- Minimum retention typically 7-10 years or per NBC 2020 / regulatory requirements
- Records form part of project closeout documentation delivered to owner

**Rationale**: Records required for warranty claims, regulatory compliance, future modifications

**Verification**: See Procedure.md, Step 5 (record archival)

**Source:** NBC 2020 requirements; ASSUMPTION: standard record retention practice

## Standards

### Applicable Codes and Standards

**Testing and Commissioning Standards:**

- **ASHRAE Guideline 0** — The Commissioning Process **TBD** (location TBD)
- **ASHRAE Guideline 1.1** — HVAC&R Technical Requirements for Commissioning **TBD** (location TBD)
- **NFPA 13** — Acceptance testing requirements **TBD** (location TBD)
- **SMACNA** — HVAC Systems Testing, Adjusting and Balancing **TBD** (location TBD)
- **NBC 2020** — Building systems testing requirements
- **CSA B64** series — Plumbing testing requirements **TBD** (location TBD)

**Source:** Applicable testing standards; specific editions TBD per Employer's Requirements

### Employer's Requirements

- **Employer's Requirements Volume 2** — **TBD** — Project-specific testing and commissioning requirements (location TBD)

## Verification

### Verification Methods

| Verification Activity | Description | Responsibility |
|----------------------|-------------|----------------|
| Completeness Check | Verify all required records per FR-01 are present | QA/QC Manager |
| Data Accuracy Verification | Verify test data is accurate and reasonable per FR-02/03/04 | Commissioning Engineer |
| Witness Signature Verification | Verify proper witnesses and sign-offs per PR-01 | QA/QC Manager |
| Acceptance Criteria Check | Verify test results meet acceptance criteria per PR-02 | Lead Engineer |
| Format Compliance | Verify records format per QR-01 | Document Control |
| AHJ Acceptance | Verify AHJ inspections and sign-offs per IF-03 | Project Manager |

**Source:** Requirements sections above; standard test record verification

### Acceptance Criteria

**Completeness:**
- [ ] All required HVAC test records present per FR-02
- [ ] All required plumbing test records present per FR-03
- [ ] All required fire protection test records present per FR-04
- [ ] All witness signatures and dates present per PR-01

**Performance:**
- [ ] All tests passed or corrective actions completed per PR-02
- [ ] Equipment performance meets DEL-22.04 requirements
- [ ] System performance meets DEL-22.03 design calculations
- [ ] Code compliance demonstrated per NBC 2020, NFPA 13

**Quality:**
- [ ] Records authentic and traceable per QR-01
- [ ] AHJ inspections and acceptance documented per IF-03
- [ ] Commissioning authority acceptance (if applicable) per PR-03

**Source:** Standard test record acceptance criteria

## Documentation

### Required Documentation Outputs

**Test Record Packages (per Decomposition DEL-22.05):**

1. **HVAC test records**
2. **Plumbing test records**
3. **Fire suppression test records**

**Supporting Documentation:**
- Test procedures and protocols
- Instrument calibration certificates
- Manufacturer startup reports
- AHJ inspection reports
- Commissioning report (if applicable)

**Source:** Decomposition REVISED_v2.md, DEL-22.05 anticipated artifacts

### Documentation Format and Control

- **Record format**: **TBD** — Standardized forms per project QA/QC procedures
- **Issued format**: PDF scans of original signed forms
- **Numbering**: **TBD** — Per project record numbering system
- **Retention**: Per project and regulatory requirements — **TBD**

**Filing and retention:**
- Working files: `1_Working/` (during testing)
- Issued: `3_Issued/` (final accepted records for owner turnover)

**Source:** ASSUMPTION: standard project document control per README.md Section 6
