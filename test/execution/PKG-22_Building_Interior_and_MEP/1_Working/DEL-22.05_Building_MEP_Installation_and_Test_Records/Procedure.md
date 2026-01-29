# Procedure: DEL-22.05 Building MEP Installation and Test Records

## Purpose

This procedure defines the process for producing and managing **Building MEP Installation and Test Records** within **PKG-22 Building Interior & MEP**.

**Deliverable Purpose:** Provides evidence of completion, inspection, and testing for building MEP per Employer's Requirements.

**Source:** Decomposition REVISED_v2.md, DEL-22.05 entry; _CONTEXT.md

### Scope of This Procedure

This procedure covers:
- **Record identification**: Determining required test records
- **Testing coordination**: Coordinating testing activities with construction and commissioning
- **Data collection**: Conducting tests and recording results
- **Verification**: Reviewing and verifying test records
- **Submission**: Submitting records for acceptance and closeout

**Deliverable Classification:**
- **Type:** Record
- **Responsible Party:** D&B Contractor (QA/QC)

**Source:** _CONTEXT.md; standard test record workflow

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED — Dependencies are coordinated externally

**Upstream Requirements**:
1. **Construction Completion** — Systems substantially complete and ready for testing
2. **Design Documents** — DEL-22.01 drawings, DEL-22.02 specifications, DEL-22.03 calculations, DEL-22.04 data sheets available
3. **Utilities Connected** — Electrical power, water, controls operational
4. **Safety Systems** — Fire protection, emergency lighting, life safety systems operational
5. **Test Procedures** — Test procedures and protocols prepared (may be part of commissioning plan)

**Source:** Standard testing prerequisites

### Reference Materials

**Required References**:
- DEL-22.01, DEL-22.02, DEL-22.03, DEL-22.04 (design basis)
- NBC 2020, NFPA 13, ASHRAE Guideline 1.1, SMACNA TAB standards
- Project Quality Management Plan
- Project Commissioning Plan — **TBD** (location TBD)

**Source:** Specification.md Standards section

### Personnel Requirements

| Role | Qualification |
|------|--------------|
| QA/QC Manager | Responsible for test record management and acceptance |
| Commissioning Engineer | Develops test procedures, witnesses tests, reviews results (may be CxA or contractor) |
| TAB Contractor | Independent air and water balance testing (certified TAB technician) |
| Fire Protection Contractor | Fire sprinkler system testing per NFPA 13 (may require licensed technician) |
| AHJ Inspector | Fire Marshal and building inspector for code compliance acceptance |

**Source:** ASSUMPTION: standard testing personnel requirements

### Tools and Resources

- Test instruments (calibrated): manometers, flow meters, pressure gauges, thermometers
- Instrument calibration certificates (current within calibration period)
- Test forms and checklists per project QA/QC procedures
- Digital camera for photo documentation

**Source:** ASSUMPTION: standard testing tools

## Steps

### Step 1: Record Identification

**Objective**: Identify all required installation and test records per codes, specifications, and commissioning plan.

**Requirements Addressed**: Supports FR-01 (completeness), establishes scope for FR-02/03/04 (system-specific tests).

**Activities**:

1.1. **Review Design Documents**:
   - Identify all MEP systems and equipment from DEL-22.01 drawings
   - Review DEL-22.02 specifications for testing requirements
   - Review DEL-22.03 calculations for performance acceptance criteria

1.2. **Review Code Requirements**:
   - NBC 2020 — Required tests for building systems
   - NFPA 13 — Required acceptance tests for fire protection
   - ASHRAE Guideline 1.1 — Recommended commissioning tests

1.3. **Review Project Requirements**:
   - Project Quality Management Plan — Required quality records
   - Project Commissioning Plan — Commissioning test requirements (if CxA appointed)
   - Employer's Requirements — Any additional testing requirements

1.4. **Prepare Test Record Matrix**:
   - List all required tests by system (HVAC, plumbing, fire protection)
   - Identify acceptance criteria for each test
   - Identify required witnesses (contractor QA/QC, CxA, owner, AHJ)
   - Prepare test schedule coordinated with construction completion

**Verification**: Test record matrix reviewed and approved by QA/QC Manager and Lead Engineer.

**Source:** Specification.md FR-01; standard testing planning process

### Step 2: Data Collection

**Objective**: Conduct testing and collect test data per procedures and codes.

**Requirements Addressed**: Executes FR-02 (HVAC testing), FR-03 (plumbing testing), FR-04 (fire protection testing).

**Activities**:

2.1. **Verify Pre-Testing Readiness**:
   - Systems substantially complete with punch list items closed
   - Utilities connected and operational
   - Safety systems operational
   - Test instruments calibrated (verify calibration certificates)

2.2. **HVAC Testing** (per FR-02):
   - **Duct Pressure Test**: Test ductwork for leakage per SMACNA standards. Record test pressure, duration, leakage rate.
   - **Air Balance (TAB)**: Engage independent TAB contractor. Measure airflows at all outlets/inlets. Adjust dampers to achieve design airflows (±10% typical). Prepare TAB report with all measurements and adjustments.
   - **Equipment Functional Test**: Operate equipment through all modes (heating, cooling, ventilation). Verify capacities and control sequences. Record performance data.
   - **Control System Functional Test**: Test control sequences, interlocks, alarms, BAS integration (coordinate with PKG-19).

2.3. **Plumbing Testing** (per FR-03):
   - **Water Supply Pressure Test**: Pressurize water supply piping to 1.5× operating pressure (or per NBC 2020). Hold for 2 hours. Inspect for leaks. Record test pressure, duration, results.
   - **Drainage Test**: Conduct air or water test of drainage piping per NBC 2020. Record test pressure/head, duration, results.
   - **Backflow Preventer Test**: Test backflow preventers per manufacturer and CSA B64. Record differential pressures and flow. Provide certification.
   - **Hot Water Performance**: Measure hot water temperature, flow, and recovery rate. Verify meets design requirements.

2.4. **Fire Protection Testing** (per FR-04):
   - **Hydrostatic Test**: Pressurize sprinkler piping to 200 psi (or per NFPA 13). Hold for 2 hours. Inspect for leaks. Record test pressure, duration, results. Witness required.
   - **Main Drain Test**: Open main drain valve. Measure static pressure, residual pressure, and flow. Record results. Compare to design requirements and water supply curve.
   - **Trip Test**: Trip alarm valve. Verify water motor gong, bell, and supervisory signals activate. Verify fire alarm panel receives signal (coordinate with PKG-19). Record results.
   - **Fire Pump Test** (if applicable): Conduct capacity test per NFPA 20. Verify pump delivers rated flow at rated pressure. Conduct run test. Record pump curves and results.

2.5. **Photo Documentation**:
   - Photograph test setups, instrument readings, and any deficiencies
   - Include in test record package

**Verification**: Test data reviewed by Commissioning Engineer for accuracy and reasonableness.

**Source:** Specification.md FR-02/03/04; Guidance.md (system-specific testing requirements)

### Step 3: Verification

**Objective**: Verify test records are complete, accurate, and demonstrate acceptance.

**Requirements Addressed**: Addresses PR-01 (witness and sign-off), PR-02 (acceptance criteria), QR-01 (authenticity and traceability).

**Activities**:

3.1. **Self-Check** (by test performer):
   - Verify all required data recorded
   - Verify test meets acceptance criteria or corrective actions documented
   - Verify signatures and dates complete

3.2. **Technical Review** (by Commissioning Engineer):
   - Verify test procedures followed correctly
   - Verify test results reasonable and meet acceptance criteria
   - Verify performance meets DEL-22.03 design calculations and DEL-22.04 data sheet requirements
   - Identify any deficiencies requiring corrective action and retesting

3.3. **Witness Verification**:
   - Verify required witnesses present and signatures obtained
   - Commissioning Agent review (if CxA appointed)
   - Owner's representative review (if required)

3.4. **Corrective Actions** (if tests fail):
   - Document failure mode and root cause
   - Implement corrective actions
   - Retest after corrections
   - Document retesting results

**Verification**: All test records verified complete and acceptable by QA/QC Manager.

**Source:** Specification.md PR-01/02, QR-01; Procedure quality checkpoints

### Step 4: Compilation

**Objective**: Compile all test records into organized package for submission.

**Requirements Addressed**: Supports documentation requirements and prepares for submission (Step 5).

**Activities**:

4.1. **Organize Records**:
   - Organize by system (HVAC, plumbing, fire protection)
   - Organize by test type within each system
   - Create table of contents

4.2. **Attach Supporting Documentation**:
   - Instrument calibration certificates
   - Test procedures
   - Manufacturer startup reports
   - Photo documentation
   - Corrective action reports (if any)

4.3. **Prepare Summary Report**:
   - Summary of all tests conducted
   - Summary of results (pass/fail)
   - Summary of any outstanding issues or punch list items
   - Recommendation for system acceptance

4.4. **Quality Check**:
   - Verify all pages legible and complete
   - Verify all signatures present
   - Verify document control information (project name, date, revision, page numbers)

**Verification**: Compiled package reviewed by QA/QC Manager for completeness and quality.

**Source:** Standard test record compilation practice

### Step 5: Submission and Acceptance

**Objective**: Submit test records for acceptance by commissioning authority, owner, and AHJ.

**Requirements Addressed**: Addresses PR-03 (CxA acceptance), IF-02 (CxA coordination), IF-03 (AHJ inspections).

**Activities**:

5.1. **Submit to Commissioning Authority** (if CxA appointed):
   - Submit compiled test record package to CxA for review
   - Address any CxA comments or requests for additional testing
   - Obtain CxA acceptance sign-off
   - CxA prepares commissioning report summarizing testing and acceptance

5.2. **Coordinate AHJ Inspections**:
   - **Fire Marshal**: Schedule final fire protection system inspection. Provide test records for review. Address any deficiencies. Obtain fire protection system acceptance certificate.
   - **Building Inspector**: Schedule final MEP inspection. Provide test records for review. Address any deficiencies. Obtain building permit sign-off.

5.3. **Submit to Owner**:
   - Submit final test record package to owner as part of project closeout
   - Include all test records, commissioning report, AHJ acceptance certificates
   - Provide training to owner's operations staff on system operation and maintenance

5.4. **Archive Records**:
   - File final accepted test records in `3_Issued/` folder
   - Provide copies to owner for O&M documentation
   - Retain per project record retention requirements — **TBD** (location TBD)

**Verification**: All acceptance sign-offs obtained; records submitted to owner; project closeout complete.

**Source:** Specification.md PR-03, IF-02/03; standard commissioning and closeout process

## Verification

### Quality Control Checkpoints

**Test Performer Check**:
- [ ] All required tests conducted per procedures
- [ ] All data recorded accurately
- [ ] Test meets acceptance criteria or corrective actions documented
- [ ] Signatures and dates complete

**Commissioning Engineer Review**:
- [ ] Test procedures followed correctly
- [ ] Test results meet acceptance criteria per PR-02
- [ ] Performance meets design requirements (DEL-22.03, DEL-22.04)
- [ ] Any deficiencies documented with corrective actions

**QA/QC Manager Review**:
- [ ] All required tests present per FR-01
- [ ] Record quality meets standards per QR-01
- [ ] Witness signatures present per PR-01
- [ ] Compilation complete and organized

**CxA Review** (if applicable):
- [ ] Testing scope adequate per commissioning plan
- [ ] Test results demonstrate systems ready for occupancy
- [ ] Any issues resolved or documented
- [ ] Ready for CxA acceptance per PR-03

**AHJ Inspection**:
- [ ] Fire protection system acceptance by Fire Marshal per IF-03
- [ ] MEP systems acceptance by Building Inspector per IF-03
- [ ] Building permit closeout complete

**Source:** Specification.md Verification section; Procedure verification checkpoints

### Sign-Off Requirements

| Milestone | Required Sign-Offs |
|-----------|-------------------|
| Test Record Matrix | QA/QC Manager, Lead Engineer |
| Individual Test Records | Tester, Witness (as required) |
| Verification Complete | Commissioning Engineer, QA/QC Manager |
| Compilation Complete | QA/QC Manager |
| Commissioning Acceptance | Commissioning Authority (if applicable) |
| AHJ Acceptance | Fire Marshal, Building Inspector |
| Owner Acceptance | Owner's Representative, Project Manager |

**Source:** ASSUMPTION: standard test record sign-off protocol

## Records

### Documentation Outputs

**Primary Deliverables** (per Decomposition DEL-22.05):
- **HVAC test records**
- **Plumbing test records**
- **Fire suppression test records**

**Supporting Documentation**:
- Test procedures and protocols
- Instrument calibration certificates
- Manufacturer startup reports
- Photo documentation
- Commissioning report (if CxA appointed)
- AHJ inspection reports and acceptance certificates

**Source:** Decomposition REVISED_v2.md, DEL-22.05 anticipated artifacts; Specification.md

### Record Management

**File Storage Locations**:

| Stage | Location | Contents |
|-------|----------|----------|
| Working | `1_Working/` | Test records during testing phase |
| Issued | `3_Issued/` | Final accepted test records for owner turnover |

**Retention**: Per project and regulatory requirements — **TBD** — typically 7-10 years minimum

**Source:** README.md Section 6; Specification.md QR-02
