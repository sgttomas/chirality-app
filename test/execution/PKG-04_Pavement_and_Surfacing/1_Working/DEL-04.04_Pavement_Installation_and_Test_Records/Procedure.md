# Procedure: DEL-04.04 Pavement Installation & Test Records

## Purpose

This procedure defines the workflow for planning, executing, documenting, reviewing, and delivering pavement installation and test records (DEL-04.04) to demonstrate construction conformance to DEL-04.01 (drawings), DEL-04.02 (specifications), and DEL-04.03 (calculations), while ensuring OBJ-8 Phase 2 expansion corridor enhanced documentation is complete.

## Prerequisites

### Dependencies
**Mode**: NOT_TRACKED (per `_DEPENDENCIES.md`)
**Note**: Dependencies are coordinated externally by humans. The following inputs are typically required:
- DEL-04.01 final drawing set (as-built design basis for field verification)
- DEL-04.02 final specification (acceptance criteria, testing frequencies, material requirements)
- DEL-04.03 final calculations (target values for thickness, density verification)
- Testing equipment (nuclear density gauge, coring equipment, survey instruments) with current calibration
- Accredited testing laboratory (ISO 17025 or equivalent)
- Qualified inspectors and technicians (ACI, NICET, or equivalent certifications)

### Reference Materials
- **Decomposition**: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- **Datasheet (DEL-04.04)**: Record Scope, Record Types, Acceptance Criteria, Assumptions & TBDs
- **Specification (DEL-04.04)**: Requirements R1.1–R4.2, Verification Methods, Standards
- **Guidance (DEL-04.04)**: Review Checklist, Principles, Trade-offs
- **DEL-04.01 final drawings, DEL-04.02 final specification, DEL-04.03 final calculations**
- **Testing standards**: ASTM D6938, D1556, D698, D2726, D2041, C39
- **Project quality plan** (**TBD** – confirm testing procedures, record formats, approval authorities)

### Personnel & Roles
- **Field Inspectors**: Perform daily inspections, witness testing, complete daily QC reports
- **Testing Technicians**: Perform field testing (compaction, coring), prepare test records
- **Laboratory Technicians**: Perform laboratory testing (core density, concrete strength), prepare laboratory reports
- **Contractor QA/QC Manager**: Review all records for completeness and compliance, compile final record package
- **Engineer**: Review and approve NCR corrective actions, review and accept final record package
- **Surveyor**: Perform as-built survey verification of pavement grades and profiles

### Tools & Systems
- **Testing equipment**: Nuclear density gauge (calibrated), sand cone equipment, coring equipment, survey instruments (GPS, total station, laser level)
- **Record forms**: Standardized test record forms per project quality plan (**TBD** – obtain templates or create based on Specification R1.1–R1.7)
- **Traceability matrix**: Spreadsheet linking test records to DEL-04.01/04.02/04.03 references
- **Document management system**: For record compilation, indexing, distribution (**TBD** – confirm system and procedures)

## Steps

### Step 1: Planning - Develop Testing Plan and Traceability Matrix

**Objective**: Plan testing activities and establish traceability framework before construction starts

**Tasks**:
1.1. **Review design documents**:
- Review DEL-04.01 final drawings to identify all pavement zones requiring testing (subgrade, base, subbase, asphalt pavement, concrete pavement, line marking)
- Review DEL-04.02 final specification to extract testing requirements (methods, frequencies, acceptance criteria)
- Review DEL-04.03 final calculations to extract target values (layer thicknesses, compaction densities)

1.2. **Identify OBJ-8 Phase 2 expansion corridor zones**:
- Review DEL-04.01 drawings and Decomposition OBJ-8 mapping to identify expansion corridor zones
- Confirm enhanced testing requirements for expansion corridors (reference Datasheet **ASSUMPTION**: 2x standard testing frequency)

1.3. **Create Testing Plan**:
- Calculate total number of tests required based on pavement areas and testing frequencies from DEL-04.02
  - Example: If total subgrade area is 10,000 m² and testing frequency is 1 per 500 m², plan 20 subgrade compaction tests (40 tests for expansion corridors if 2x frequency)
- Plan test locations (random pattern for statistical sampling, plus targeted locations at critical areas/interfaces)
- Plan coring locations (coordinate with compaction testing to avoid conflict)
- Plan survey verification (100% coverage for grade, targeted profiles)
- Schedule testing activities relative to construction schedule (ensure testing doesn't delay construction)

1.4. **Create Traceability Matrix** (spreadsheet):
- Columns: Test ID, Test Type, Location (station/offset or coordinates), Date, DEL-04.01 Reference (sheet, section), DEL-04.02 Reference (clause), DEL-04.03 Reference (calculation sheet), Target Value, Acceptance Criterion, Test Result, Pass/Fail, NCR (if failed)
- Pre-populate planned test locations and references (to be filled in as tests are performed)

1.5. **Obtain testing resources**:
- Verify testing equipment is available and calibrated (calibration certificates current)
- Verify testing laboratory is accredited (ISO 17025 or equivalent) and has capacity for project
- Verify field inspectors and testing technicians are qualified and certified
- Obtain or create standardized test record forms per Specification R1.1–R1.7

**Verification**:
- Testing Plan covers all pavement zones per DEL-04.01
- Testing Plan meets or exceeds DEL-04.02 frequency requirements
- OBJ-8 expansion corridor zones have enhanced testing frequency
- Traceability Matrix template is created
- Testing resources (equipment, lab, personnel) are confirmed available

**Records**:
- Testing Plan (document or spreadsheet with planned test locations, quantities, schedule)
- Traceability Matrix template
- Equipment calibration certificates
- Laboratory accreditation certificate
- Inspector/technician qualification certificates

---

### Step 2: Execution - Perform Field Testing and Record Results

**Objective**: Execute testing per Testing Plan and document results in real time

**Tasks**:
2.1. **Daily pre-construction coordination**:
- Review construction schedule for day (what areas will be paved, what layers will be placed)
- Identify test locations for day based on Testing Plan
- Brief field inspectors and testing technicians on day's testing requirements

2.2. **Perform compaction testing** (per Specification R1.1):
- Test each layer (subgrade, base, subbase, asphalt binder, asphalt wearing) at planned locations
- Use ASTM D6938 (nuclear density) or ASTM D1556 (sand cone) method per DEL-04.02
- Record all required data on compaction test form: location, date, layer, depth, densities, moisture, percent compaction, pass/fail, cross-references
- If test fails (compaction < acceptance criterion): Stop work, initiate NCR, perform corrective action (additional compaction, rework), re-test
- Update Traceability Matrix with test results same day

2.3. **Perform pavement coring** (per Specification R1.2):
- Extract cores at planned locations after pavement has cured (minimum 24 hours for asphalt, 7 days for concrete)
- Measure layer thicknesses with ruler or caliper, record on core sample form
- Photograph cores (both ends, full length)
- Send cores to accredited laboratory for testing (asphalt: bulk density, TMD, air voids per ASTM D2726, D2041; concrete: 28-day compressive strength per ASTM C39)
- Receive laboratory test report, record results on core sample form
- Compare measured thicknesses and material properties to DEL-04.03 target values and DEL-04.02 acceptance criteria
- If core fails: Initiate NCR, evaluate corrective action (overlay, remove and replace, engineering evaluation, acceptance with reduced payment)
- Update Traceability Matrix with core results

2.4. **Perform survey verification** (per Specification R1.3):
- Survey as-built pavement surface elevations at planned locations using GPS, total station, or laser level
- Compare as-built elevations to DEL-04.01 design elevations, calculate deviations
- Evaluate deviations against DEL-04.02 grade tolerance
- Prepare profile charts showing longitudinal and cross-sectional profiles vs. design
- If deviations exceed tolerance: Initiate NCR, evaluate corrective action (grinding, overlay, acceptance with engineering evaluation)
- Update Traceability Matrix with survey results

2.5. **Collect material certifications** (per Specification R1.4):
- Collect asphalt mix design approval, binder certifications, aggregate test results, daily batch plant QC reports
- Collect concrete mix design approval, cement certifications, batch tickets (if applicable)
- Collect base/subbase material test results
- Collect line marking material certifications
- Verify all certifications are dated and correspond to construction period
- File certifications in record package

2.6. **Complete daily QC reports** (per Specification R1.5):
- Complete daily QC report each construction day: date, weather, work performed, quantities, test summary (number of tests, pass/fail counts), observations, issues
- File daily reports in chronological order

2.7. **Initiate NCRs for non-conformances** (per Specification R1.6):
- When test failure or observed non-conformance occurs: Initiate NCR immediately
- Complete NCR form: NCR number, date, location, description, affected DEL-04.01/04.02/04.03 references, root cause
- Propose corrective action
- Submit NCR to Engineer for review and approval
- Track NCR status in NCR log

**Verification**:
- All planned tests are performed per Testing Plan
- Test results are recorded same day on standardized forms
- Failed tests have NCRs initiated
- Traceability Matrix is updated daily
- Material certifications are collected and filed

**Records**:
- Compaction test records (one form per test)
- Core sample records (one form per core with laboratory reports)
- Survey verification reports with profile charts
- Material certification records
- Daily QC reports
- NCR forms (for failed tests or non-conformances)
- Updated Traceability Matrix

---

### Step 3: NCR Management - Track and Close Non-Conformances

**Objective**: Ensure all NCRs are resolved with approved corrective actions and closed

**Tasks**:
3.1. **NCR submittal to Engineer**:
- Submit NCR to Engineer with proposed corrective action
- Provide supporting information (test results, photographs, affected requirements from DEL-04.01/04.02/04.03)

3.2. **Engineer review and approval**:
- Engineer reviews proposed corrective action
- Engineer approves, modifies, or rejects proposed corrective action
- Document Engineer approval on NCR form

3.3. **Implement corrective action**:
- Contractor implements approved corrective action (rework, overlay, remove and replace, etc.)
- Document implementation (date, description, contractor signoff)
- Photograph corrective action (before and after)

3.4. **Verification testing**:
- Perform verification testing after corrective action to demonstrate conformance
- Record verification test results on NCR form
- If verification test passes: Proceed to NCR closure
- If verification test fails: Revise corrective action and repeat

3.5. **NCR closure**:
- Submit NCR with verification test results to Engineer for closure approval
- Engineer reviews and approves NCR closure
- Update NCR log with closure date
- File closed NCR in record package

3.6. **NCR tracking**:
- Maintain NCR log (spreadsheet) with columns: NCR Number, Date, Location, Description, Status (Open, Engineer Review, Corrective Action, Verification, Closed), Responsible Party, Target Closure Date
- Review NCR log weekly to ensure NCRs are progressing and not stagnating

**Verification**:
- All NCRs have Engineer-approved corrective actions
- All corrective actions are implemented and documented
- All NCRs have verification testing showing conformance
- All NCRs are closed with Engineer approval, or have approved action plan and schedule
- No NCRs remain open without resolution path at final acceptance

**Records**:
- NCR forms (complete with all sections filled: description, root cause, corrective action, approvals, verification, closure)
- NCR log (tracking spreadsheet)
- Photographs of non-conformances and corrective actions
- Verification test results

---

### Step 4: OBJ-8 Documentation - Compile Enhanced Records for Phase 2 Expansion Corridors

**Objective**: Ensure Phase 2 expansion corridor zones have enhanced documentation per OBJ-8 requirements

**Tasks**:
4.1. **Verify enhanced testing coverage**:
- Review Traceability Matrix to confirm expansion corridor zones have enhanced testing frequency (e.g., 2x standard)
- Identify any gaps in testing coverage and perform additional tests if needed

4.2. **Create detailed test location plans**:
- Prepare plan drawing showing all compaction test locations and core locations in expansion corridors
- Include survey coordinates for each test location
- Annotate plan with test results (pass/fail) and any NCRs
- This plan will be used as reference during Phase 2 design

4.3. **Compile enhanced material records**:
- Collect complete set of material records for expansion corridors: mix designs, material test reports, batch tickets
- Ensure records are more comprehensive than standard areas (e.g., every batch ticket, not just sample)
- Archive records separately for easy retrieval during Phase 2

4.4. **Compile photographic documentation**:
- Collect photographs of critical construction stages in expansion corridors:
  - Subgrade preparation (proof rolling, compaction)
  - Each layer placement (base, binder, wearing course)
  - Construction joints at Phase 2 tie-in locations (sawcut joints, joint protection)
- Annotate photographs with location, date, description

4.5. **Document Phase 2 tie-in joints**:
- Survey Phase 2 tie-in joint locations (coordinates, elevations)
- Photograph joints from multiple angles showing joint details
- Document joint protection measures per DEL-04.02
- Provide joint documentation package for Phase 2 design reference

4.6. **Create separate OBJ-8 record section**:
- Organize all OBJ-8 expansion corridor records in separate section of final record package (Section 8 per Datasheet recommended structure)
- Create index for OBJ-8 section for easy retrieval

**Verification**:
- Expansion corridor testing frequency is enhanced per requirements
- Test location plans with coordinates are complete
- Enhanced material records are complete and archived
- Photographic documentation covers all critical stages
- Phase 2 tie-in joints are surveyed and documented
- OBJ-8 record section is organized and indexed

**Records**:
- Enhanced test coverage documentation (Traceability Matrix showing expansion corridor tests)
- Detailed test location plans with coordinates
- Complete material certification records for expansion corridors
- Photographic documentation (organized by location and stage)
- Phase 2 tie-in joint documentation package (survey data, photographs, joint details)
- OBJ-8 record section index

---

### Step 5: Record Compilation - Assemble Final Record Package

**Objective**: Compile all records into organized final package ready for review and acceptance

**Tasks**:
5.1. **Collect all record types**:
- Compaction test records (all layers, all locations)
- Core sample records (all cores with laboratory reports)
- Survey verification reports
- Material certification records
- Daily QC reports
- NCR records (all NCRs, all closed or with approved action plans)
- OBJ-8 enhanced documentation
- Verify no records are missing using Traceability Matrix as checklist

5.2. **Organize records per recommended structure** (Datasheet Section "Record Organization and Format"):
- Section 1: Cover page and index
- Section 2: Material certifications
- Section 3: Mix design approvals
- Section 4: Compaction test records (organized by layer, then location)
- Section 5: Core sample records (organized by location)
- Section 6: Survey and profile verification
- Section 7: Daily QC reports (chronological)
- Section 8: Non-conformance reports
- Section 9: OBJ-8 Phase 2 expansion documentation
- Section 10: Final acceptance documentation
- Section 11: Appendices (photographs, calibration certificates, inspector certifications)

5.3. **Create cover page and index**:
- Cover page: Project name, deliverable identification (DEL-04.04), contractor name, submittal date, revision number
- Index/table of contents: List all sections with page numbers (or file names for digital records)

5.4. **Perform final QA review** (per Guidance Review Checklist Steps 1-10):
- Compaction test record review (completeness, coverage, OBJ-8, pass/fail, failures with NCRs, traceability, calibration)
- Core sample record review (completeness, coverage, OBJ-8, thickness comparison, material properties, failures with NCRs, photographs, lab certificates, traceability)
- Survey verification review (coverage, method, deviations, profile charts, failures with NCRs, surveyor credentials, traceability)
- Material certification review (asphalt, concrete, base/subbase, line marking, currency, conformance)
- Daily QC report review (completeness, content, consistency, issues documented, NCRs referenced)
- NCR review (all NCRs, completeness, approvals, verification, closure, no open NCRs)
- OBJ-8 documentation review (zones identified, enhanced testing, test location plans, material records, photographs, joint documentation, separate indexing)
- Record legibility and completeness (legibility, no blank fields, signatures, dates)
- Data accuracy and consistency (arithmetic, units, cross-record consistency, traceability to originals)
- Overall package organization (cover page, index, dividers, page numbering, revision control)

5.5. **Address QA review findings**:
- Correct any deficiencies identified in QA review
- Obtain missing records or information
- Clarify illegible entries
- Complete any blank fields
- Obtain missing signatures

5.6. **Contractor QA/QC Manager review and signoff** (per Specification R4.1):
- Contractor QA/QC Manager performs final review of complete record package
- Sign off on cover page or transmittal letter

**Verification**:
- All record types per Specification R1.1–R1.7 are included
- Records are organized per recommended structure
- Cover page and index are complete
- Guidance Review Checklist Steps 1-10 all pass (or deficiencies are addressed)
- Contractor QA/QC Manager signoff obtained

**Records**:
- Complete final record package (organized per recommended structure)
- QA review checklist (completed)
- Contractor QA/QC Manager signoff (on cover page or transmittal)

---

### Step 6: Submittal and Engineer Acceptance

**Objective**: Submit final record package to Engineer for review and acceptance

**Tasks**:
6.1. **Prepare submittal**:
- Prepare transmittal letter requesting Engineer review and acceptance of final record package
- Include Contractor QA/QC Manager signoff in transmittal or on cover page
- Provide record package in format specified by contract (paper, digital, or both)

6.2. **Submit to Engineer**:
- Submit final record package with transmittal letter to Engineer
- Retain copy of submittal for Contractor records

6.3. **Engineer review** (per Specification R4.2):
- Engineer reviews final record package for:
  - Completeness (all required record types included)
  - Compliance (construction conformed to DEL-04.01/04.02/04.03 or approved deviations documented)
  - NCR closure (all NCRs closed or approved disposition)
  - OBJ-8 documentation (Phase 2 enhanced records complete)
- Engineer may request clarifications or additional information

6.4. **Address Engineer review comments**:
- If Engineer identifies deficiencies: Address deficiencies and resubmit
- If Engineer requests clarifications: Provide clarifications
- Revise record package as needed

6.5. **Engineer acceptance**:
- Engineer issues acceptance certificate or acceptance letter for final record package
- Acceptance certificate included in final record package

6.6. **Final distribution**:
- Distribute accepted final record package per project distribution matrix (Owner, Engineer, Contractor, Package Coordinators)
- Provide digital backup if paper records are provided, or vice versa

6.7. **Archival**:
- Archive final accepted record package per contract record retention requirements (reference Datasheet **ASSUMPTION**: 25 years or design life, whichever is longer)
- Store in secure location with backup copies (for digital records: backup on separate server or cloud storage)
- Maintain index for easy retrieval

**Verification**:
- Final record package submitted to Engineer with Contractor QA/QC Manager signoff
- Engineer review complete
- Engineer review comments addressed
- Engineer acceptance certificate issued
- Final distribution complete per distribution matrix
- Records archived per retention requirements

**Records**:
- Submittal transmittal letter
- Engineer acceptance certificate or letter
- Final accepted record package (distributed per distribution matrix)
- Archival storage confirmation

---

## Verification

### Verification Checkpoints

| Checkpoint | Verification Method | Acceptance Criteria |
|------------|-------------------|---------------------|
| Step 1 complete | Review Testing Plan and Traceability Matrix | Plan covers all zones; meets DEL-04.02 frequencies; OBJ-8 enhanced; resources confirmed |
| Step 2 complete | Review daily updated Traceability Matrix and test records | All planned tests performed; results recorded; NCRs initiated for failures; matrix updated daily |
| Step 3 complete | Review NCR log | All NCRs have approved corrective actions; verification testing complete; all closed or action plans in place |
| Step 4 complete | Review OBJ-8 record section | Enhanced testing complete; test location plans with coordinates; enhanced material records; photographs; joint documentation; separate indexing |
| Step 5 complete | Review final record package and QA checklist | All record types included; organized per structure; Guidance checklist passes; Contractor QA/QC signoff |
| Step 6 complete | Review Engineer acceptance certificate | Engineer acceptance issued; final distribution complete; archival confirmed |

### Overall Acceptance Criteria
- Testing Plan covered all pavement zones per DEL-04.01
- All tests met or exceeded DEL-04.02 frequency requirements
- All test results met acceptance criteria or had approved NCRs
- All NCRs are closed or have approved disposition
- OBJ-8 Phase 2 expansion corridor enhanced documentation is complete
- Final record package is complete per Specification R1.1–R1.7
- Guidance Review Checklist Steps 1-10 all pass
- Contractor QA/QC Manager signoff obtained
- Engineer acceptance certificate issued

## Records

### Deliverable Records
1. **Testing Plan**: Planned test locations, quantities, schedule
2. **Traceability Matrix**: Complete matrix linking all tests to DEL-04.01/04.02/04.03
3. **Compaction Test Records**: All test forms
4. **Core Sample Records**: All core forms with lab reports
5. **Survey Verification Reports**: Survey data, profile charts
6. **Material Certification Records**: All material certificates
7. **Daily QC Reports**: All daily reports
8. **NCR Records**: All NCR forms with closures
9. **NCR Log**: Tracking spreadsheet
10. **OBJ-8 Enhanced Documentation**: Test location plans, enhanced material records, photographs, joint documentation
11. **Final Record Package**: Complete organized package per recommended structure
12. **QA Review Checklist**: Completed Guidance checklist
13. **Contractor QA/QC Manager Signoff**: Cover page or transmittal signoff
14. **Engineer Acceptance Certificate**: Final acceptance
15. **Archival Storage Confirmation**: Proof of archival per retention requirements

### File Naming Conventions (**TBD** – pending project document management plan)
- Final record package: `DEL-04.04_Pavement_Installation_Test_Records_R[Rev].pdf` (paper or digital)
- Traceability matrix: `DEL-04.04_Traceability_Matrix.xlsx`
- Testing plan: `DEL-04.04_Testing_Plan.pdf`
- NCR log: `DEL-04.04_NCR_Log.xlsx`

### Storage Locations
- **Working files**: `test/execution/PKG-04_Pavement_and_Surfacing/1_Working/DEL-04.04_Pavement_Installation_and_Test_Records/`
- **Issued files**: `test/execution/PKG-04_Pavement_and_Surfacing/3_Issued/`
- **Archival storage**: Per contract requirements (Owner document management system, secure offsite storage, or as specified)

## References

### Source Documents
- **Decomposition**: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section PKG-04, DEL-04.04, OBJ-8
- **Datasheet, Specification, Guidance (DEL-04.04)**
- **DEL-04.01 final drawings, DEL-04.02 final specification, DEL-04.03 final calculations**
- **Employer's Requirements Volume 2 Part 1 & 2**: QA/QC requirements (**location TBD**)

### Related Deliverables
- **DEL-04.01**: Design basis
- **DEL-04.02**: Acceptance criteria
- **DEL-04.03**: Target values
