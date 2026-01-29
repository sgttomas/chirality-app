# Procedure: DEL-03.05 Underground Utilities Installation & Test Records

## Purpose

Define the step-by-step process for executing, capturing, verifying, and documenting installation and test records for PKG-03 Underground Utilities, ensuring that pressure testing, flow testing, CCTV inspection, as-built surveying, OWS performance verification, and commissioning documentation are completed consistently, reviewed rigorously, and delivered with complete quality documentation (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:202).

**Production purpose:** Enable QA/QC inspectors and test crews to execute installation verification and performance testing, capture test records that demonstrate conformance to design requirements, and compile commissioning documentation supporting operations handover.

**QA purpose:** Ensure installation and test records undergo self-check, interdisciplinary coordination check, and independent review per project Quality Management Plan requirements before archival, creating traceable QA record for regulatory compliance and commissioning acceptance.

## Prerequisites

**Dependencies (coordinated externally per `_DEPENDENCIES.md`):**
- **DEL-03.01 Drawing Set**: Equipment layouts, pipe routes, instrumentation locations (required for test planning, test section identification, as-built comparison; Specification §IF-1).
- **DEL-03.02 Technical Specification**: Installation requirements, material specifications, testing procedures, acceptance criteria (required for test protocols and conformance verification; Specification §IF-1).
- **DEL-03.03 Design Calculations**: Hydraulic calculations, pipe sizing, OWS capacity calculations (required for performance validation benchmarks; Specification §IF-1).
- **DEL-03.04 Data Sheet Package**: Equipment specifications and material properties (OWS equipment data, pipe material data, instrumentation data) (required for equipment performance testing parameters; Specification §IF-1).
- **DEL-03.06 CCTV Survey Report**: (Interface: DEL-03.06 uses DEL-03.05 CCTV inspection records as input for detailed analysis; coordination required for record format and defect coding system; Specification §IF-2).

**Reference materials:**
- **Employer's Requirements Volume 2 Part 2: Civil & Process Mechanical Works** — testing procedures, acceptance criteria, performance standards (Source: test/Volume_2_Part_2_Employers_Requirements.pdf; Specification §Standards).
- **Employer's Requirements Volume 2 Part 1: General Requirements** — Quality Management Plan, inspection and testing requirements, QA/QC procedures, record retention requirements (Source: test/Volume_2_Part_1_Employers_Requirements.pdf; Specification §QR-1).
- **Testing standards**: Pressure testing standards (ASTM hydrostatic testing, air testing), flow testing standards, CCTV inspection standards (PACP or equivalent), survey standards, OWS performance testing standards, calibration standards (TBD; Specification §Standards).
- **Project QA/QC standards**: Test record templates, inspection checklist templates, review procedures (TBD; Specification §Documentation).
- **Package-level references** in `execution/PKG-03_Underground_Utilities_and_Drainage/0_References/_REFERENCE_INDEX.md`.

**Test equipment and calibration requirements:**
- **Pressure testing equipment**: Pressure gauges (calibrated, certificate current), test pumps, isolation plugs/valves, pressure relief devices (Guidance §C-1 test equipment calibration consideration).
- **Flow measurement equipment**: Flow meters (calibrated, certificate current), weirs, flumes, velocity measurement devices (Guidance §C-1).
- **CCTV inspection equipment**: Pipeline camera systems, video recording equipment, lighting, defect measurement tools (Guidance §P-3 pipe condition verification).
- **Survey equipment**: Total station or GPS equipment (calibrated, certificate current), survey rods, level, survey control monuments (Guidance §C-3 as-built accuracy consideration).
- **OWS performance testing equipment**: Flow meters for inlet/outlet (calibrated), level measurement devices, oil concentration measurement equipment, water quality sampling equipment, laboratory analysis services (Guidance §P-2 environmental protection verification).
- **Instrumentation calibration equipment**: Calibration standards for level sensors, flow meters, oil layer thickness monitors (Guidance §C-1).
- **Calibration certificate verification**: Verify all test equipment calibration certificates are current before testing execution; plan retest schedule if calibration expires during testing program (Specification §QR-2).

**Guidance alignment:**
- Review Guidance.md §Purpose to understand why installation and test records matter for conformance verification, regulatory compliance, and operations handover.
- Review Guidance.md §Principles (P-1 hydraulic integrity verification, P-2 environmental protection verification for OBJ-7, P-3 pipe condition verification, P-4 installation traceability and acceptance) before testing execution.
- Review Guidance.md §Examples 1-4 for pressure test record structure, CCTV inspection record structure, OWS performance test record structure, and commissioning handover record structure.

**Personnel (ASSUMPTION per typical Quality Management Plan):**
- **Test crew/field inspector**: Executes tests (pressure testing, flow testing, CCTV inspection), captures field test data, performs self-check.
- **Survey crew**: Executes as-built surveys, captures survey field notes, processes survey data.
- **CCTV specialist surveyor**: Executes CCTV inspection, operates camera equipment, codes defects per standard system (Datasheet §Identification lists "D&B Contractor (Specialist Surveyor)" as responsible for related DEL-03.06).
- **Laboratory analyst**: Performs discharge water quality analysis for OWS performance verification (external service or in-house laboratory).
- **QA/QC checker**: Reviews test record completeness, verifies test results against acceptance criteria, confirms coordination with related deliverables.
- **Independent reviewer (approver)**: Validates compliance with Employer's Requirements, confirms test result validity, signs test records for archival.
- **QA coordinator**: Verifies QA documentation completeness, manages record management system archival.

## Steps

### 1. Review Scope and Confirm Testing Requirements

- Review decomposition entry test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:202 and `_CONTEXT.md` to confirm anticipated record types (pressure test, leak test, flow testing, CCTV inspection, as-built survey, OWS performance verification, containment integrity, commissioning).
- Review Specification.md §Scope for anticipated records, exclusions, scope boundaries (Guidance §C-4 record structure and scope boundaries).
- Identify interface testing requiring coordination with adjacent packages or DEL-03.06 CCTV Survey Report per Specification §IF-2.
- **Verification checkpoint:** Test crew lead confirms scope understanding and testing requirements with QA/QC Manager before proceeding.
- **Cross-reference:** Datasheet §Construction record types; Specification §Scope; Guidance §C-4.

### 2. Collect and Document Input Data

**2.1 Collect Design Inputs from Related Deliverables:**
- Obtain DEL-03.01 Drawing Set for equipment layouts, pipe routes, test section identification; document drawing revision (Specification §IF-1; Datasheet §References).
- Obtain DEL-03.02 Technical Specification for installation requirements, testing procedures, acceptance criteria; document specification revision (Specification §IF-1).
- Obtain DEL-03.03 Design Calculations for design flow rates, OWS capacity, performance validation benchmarks; document calculation revision (Specification §IF-1).
- Obtain DEL-03.04 Data Sheet Package for equipment specifications (OWS equipment data, pipe material data, instrumentation data) and testing requirements; document data sheet package revision (Specification §IF-1).

**2.2 Extract ER Testing Requirements and Acceptance Criteria:**
- Extract applicable testing procedures and acceptance criteria from Employer's Requirements Volume 2 Part 2; document ER clause references (Specification §Standards; Guidance §C-2 ER compliance demonstration).
- Review project Quality Management Plan for inspection and testing requirements, record retention requirements from Employer's Requirements Volume 2 Part 1 (Specification §QR-1).

**2.3 Verify Test Equipment Calibration:**
- Verify all test equipment calibration certificates are current; document calibration certificate references (pressure gauges, flow meters, survey equipment, instrumentation calibration standards) (Specification §QR-2; Guidance §C-1 test equipment calibration consideration).
- Plan calibration renewal or equipment replacement if calibration expires during testing program.

**2.4 Coordinate CCTV Record Format with DEL-03.06:**
- Coordinate CCTV inspection procedures, defect coding system, video file indexing, and location referencing methods with DEL-03.06 CCTV Survey Report development team to ensure record compatibility for detailed analysis (Specification §IF-2; Guidance §C-5 CCTV record coordination).

**Verification checkpoint:** QA/QC checker reviews input data completeness, test equipment calibration status, and DEL-03.06 coordination confirmation; confirms testing can proceed.

**Cross-reference:** Specification §IF-1, §IF-2, §QR-2; Guidance §C-1, §C-2, §C-5; Datasheet §Attributes "Data Sources".

### 3. Establish Record Package Structure

- Structure record package with sections matching Specification §Scope: Cover page, Introduction, Installation documentation, Pressure testing, Leak testing, Flow testing, CCTV inspection, As-built survey, OWS performance verification, Containment integrity testing, Commissioning records, Appendices.
- For pressure testing section, organize by pipe section or test package matching test execution sequence.
- For CCTV inspection section, organize by pipe run with video file index and defect coding logs.
- Use consistent tabular format for test records per project QA/QC standards (TBD; Specification §Documentation).
- **Verification checkpoint:** Test crew lead confirms record package structure with QA/QC checker before detailed testing execution.
- **Cross-reference:** Specification §Scope and §Documentation; Datasheet §Construction record package organization; Guidance §C-4.

### 4. Execute Pressure Testing and Capture Records

**4.1 Plan Pressure Test Sections:**
- Segment pressure testing by logical pipe sections (between manholes, by pipe material type) per DEL-03.02 specification requirements and Guidance §T-1 pressure testing detail trade-off.
- Identify test section boundaries, isolation points, pressure gauge locations; reference DEL-03.01 Drawing Set for test section identification.

**4.2 Execute Pressure Testing:**
- **Pre-test checklist**: Conduct visual inspection (joints complete, pipe clean, no visible damage), verify backfill status (partial backfill, full backfill per specification), install isolation (valves closed, plugs installed), verify pressure gauge calibration (gauge ID, calibration date, certificate reference).
- **Test execution**: Apply initial pressure (target pressure from DEL-03.02 specification or standard), record test duration (start time, end time, total duration per specification or standard requirement), record pressure readings (at 15-minute intervals or per specification), conduct leak detection observations (visual inspection, soap bubble testing, leak location identification).
- **Test results**: Record final pressure, calculate pressure drop (initial pressure - final pressure), compare to allowable pressure drop (from DEL-03.02 specification or standard), determine pass/fail.
- **Leak detection and repair** (if test fails): Document leak locations and repair methods; conduct retest after repairs; document retest results and final acceptance.
- **Inspector sign-off**: Inspector signature/date, supervisor signature/date on each pressure test record.
- **Supporting data**: Generate pressure-time graph (if required by specification or standard); capture photographs (test setup, leak locations if applicable); attach calibration certificate references.

**4.3 Capture Pressure Test Records:**
- Complete pressure test record for each test section using format per Guidance §Example 1 (test identification, pre-test checklist, test execution log, test results, reviewer signatures, supporting data).
- Organize pressure test records by pipe section in record package pressure testing section.

**4.4 Leak Test Records:**
- Document leak detection methods (visual observation, soap bubble testing, electronic leak detection), leak locations, repair documentation, retest verification after repairs.

**Verification checkpoint:** Self-check verifies pressure test records are complete, test execution procedures were followed, acceptance criteria are correctly applied, inspector sign-offs are present.

**Cross-reference:** Specification §FR-1, §PR-1; Guidance §P-1, §T-1, §Example 1; Datasheet §Construction pressure test records.

### 5. Execute Flow Testing and Capture Records

**5.1 Plan Flow Testing:**
- Identify flow test locations (storm drainage inlets, outlets, OWS inlet/outlet) referencing DEL-03.01 Drawing Set and DEL-03.03 Design Calculations for design flow rates.
- Verify flow measurement equipment calibration (flow meters, weirs, flumes); document calibration certificate references.

**5.2 Execute Flow Testing:**
- Measure flow rates at key locations (inlet, outlet, branch connections) using calibrated flow measurement equipment.
- Compare measured flow rates to design flow rates from DEL-03.03 calculations; calculate deviation from design flow.
- Verify flow distribution (multiple outlets, drainage areas) matches design expectations.
- Compare test results to acceptance criteria (flow rate tolerance from DEL-03.02 specification or standard); determine pass/fail.

**5.3 Capture Flow Testing Records:**
- Complete flow testing record for each test location using tabular format (test identification, flow measurement equipment calibration reference, measured flow rates, design flow rates from DEL-03.03, deviation calculation, acceptance criteria comparison, pass/fail determination, inspector signature/date).
- Organize flow testing records by drainage area or system section in record package flow testing section per Guidance §T-2 flow testing detail trade-off.

**Verification checkpoint:** Self-check verifies flow testing records are complete, measured flows are compared to design flows, acceptance criteria are correctly applied.

**Cross-reference:** Specification §PR-1; Guidance §P-1, §T-2; Datasheet §Construction flow testing records.

### 6. Execute OWS Performance Verification Testing and Capture Records

**6.1 Pre-Operational Inspection:**
- Conduct visual inspection of OWS equipment (internals condition, coalescing plates installed correctly, access hatches secure).
- Verify instrumentation installation (level sensors, flow meters, oil layer thickness monitor installed and wired correctly).
- Verify electrical connections (power supply, control panel functional).
- Document pre-operational inspection checklist completion.

**6.2 OWS Flow Testing:**
- Measure design flow rate and peak flow capacity using calibrated flow meters at OWS inlet and outlet.
- Verify inlet/outlet flow balance; document flow meter calibration references.
- Compare measured flows to design flow rate from DEL-03.03 calculation and peak flow capacity from DEL-03.04 OWS data sheet.

**6.3 Retention Time Verification:**
- Calculate retention time from separator volume (from DEL-03.04 OWS data sheet) and measured flow rate.
- Compare calculated retention time to design retention time from DEL-03.03 calculation; verify retention time meets specification requirement from DEL-03.02.

**6.4 Treatment Performance Testing:**
- **Test procedure**: Reference manufacturer procedure or standard method for treatment performance testing.
- **Oil introduction**: Introduce test oil (document oil type, concentration) at OWS inlet; allow retention period per design retention time.
- **Discharge sampling**: Collect discharge water quality samples at OWS outlet (document sample location, sample time, sample handling per laboratory requirements).
- **Laboratory analysis**: Submit samples to laboratory for oil concentration analysis; obtain laboratory test reports documenting oil concentration in discharge.
- **Treatment efficiency calculation**: Calculate oil removal efficiency (% removal = (inlet concentration - outlet concentration) / inlet concentration × 100%).
- **Acceptance criteria comparison**: Compare oil removal efficiency to target efficiency from DEL-03.02 specification or DEL-03.04 OWS data sheet and regulatory discharge limits from environmental permits; determine pass/fail.

**6.5 Containment Integrity Testing:**
- Conduct visual inspection of containment areas for cracks, defects, or damage.
- Execute hydrostatic testing or dye testing for liner/sealant integrity per DEL-03.02 specification or standard procedure.
- Conduct leak detection; document any leaks identified.
- Document repairs if leaks detected; conduct retest verification after repairs.
- Document acceptance sign-off (no leaks detected, containment integrity confirmed).

**6.6 Instrumentation Calibration:**
- Calibrate level sensors, flow meters, oil layer thickness monitors using calibration standards and procedures.
- Document calibration procedures, calibration results, accuracy verification for each instrument.
- Attach instrumentation calibration certificates to record appendices.

**6.7 Commissioning Sign-Off:**
- Confirm OWS performance testing completion (flow testing, retention time verification, treatment performance testing, instrumentation calibration all passed).
- Document conformance statement (OWS performance meets specification requirements and supports OBJ-7 Environmental Protection).
- Obtain inspector signature/date, supervisor signature/date, Employer's Representative acceptance signature if required per contract.

**6.8 Capture OWS Performance Verification Records:**
- Complete OWS performance verification record using format per Guidance §Example 3 (equipment identification, pre-operational inspection checklist, flow testing, retention time verification, treatment performance testing, instrumentation calibration, commissioning sign-off, supporting data references).
- Attach supporting data (laboratory test reports for discharge water quality, instrumentation calibration certificates, photographs of OWS installation and test setup) to record appendices.
- Organize OWS performance verification records in record package OWS performance verification section.

**Verification checkpoint:** Self-check verifies OWS performance verification record is complete, treatment performance testing demonstrates OBJ-7 compliance, instrumentation calibration is documented, commissioning sign-off is obtained.

**Cross-reference:** Specification §FR-2, §PR-2; Guidance §P-2, §Example 3; Datasheet §Construction OWS performance verification records and containment integrity test records.

### 7. Execute CCTV Inspection, As-Built Survey, and Capture Records

**7.1 Execute CCTV Inspection and Capture Records:**

**7.1.1 Plan CCTV Inspection:**
- Identify pipe sections for CCTV inspection (all storm pipes and culverts per DEL-03.06 scope) referencing DEL-03.01 Drawing Set for pipe identification.
- Coordinate CCTV inspection schedule with DEL-03.06 CCTV Survey Report development team per Step 2.4.

**7.1.2 Execute CCTV Inspection:**
- Conduct CCTV inspection using pipeline camera system with video recording, lighting, and defect measurement tools.
- Document inspection parameters (pipe section ID, pipe material, pipe diameter, inspection date, inspection crew, inspection direction, camera type, inspection conditions, video file reference).
- Record video files with consistent file naming and indexing per Step 2.4 coordination.
- Code defects using standard defect coding system (PACP or equivalent per Step 2.4 coordination): defect type, severity, location/chainage, description.
- Reference defect locations to manholes, tie-in points, or continuous chainage measurement.
- Capture defect photographs for significant defects.
- Develop remediation recommendations for identified defects (monitor, repair, replace) with priority (immediate, near-term, long-term) per Guidance §T-3 CCTV inspection detail trade-off.

**7.1.3 Capture CCTV Inspection Records:**
- Complete CCTV inspection record for each pipe section using format per Guidance §Example 2 (inspection identification, inspection parameters, defect coding log in tabulated format, location referencing, remediation recommendations, video file index).
- Organize CCTV inspection records by pipe run in record package CCTV inspection section.
- Provide CCTV inspection records (video files, defect coding logs) to DEL-03.06 development team for detailed analysis per Specification §IF-2.

**Verification checkpoint:** Self-check verifies CCTV inspection records are complete, defect coding is consistent, location referencing is accurate, video files are indexed correctly; interdisciplinary check includes DEL-03.06 coordination confirmation.

**Cross-reference:** Specification §FR-3, §IF-2; Guidance §P-3, §C-5, §T-3, §Example 2; Datasheet §Construction CCTV inspection records.

**7.2 Execute As-Built Survey and Capture Records:**

**7.2.1 Plan As-Built Survey:**
- Identify survey control monuments and tie-in points for as-built survey referencing project survey control network.
- Verify survey equipment calibration (total station, GPS equipment, level); document calibration certificate references.

**7.2.2 Execute As-Built Survey:**
- Measure final locations and elevations of installed underground utilities (pipe inverts at manholes and tie-in points, rim elevations, OWS location, duct bank routes) using calibrated survey equipment.
- Tie as-built measurements to survey control monuments per survey control network.
- Compare as-built locations to design locations from DEL-03.01 Drawing Set; document deviations from design.
- Obtain approval for deviations from design per project change management procedures if deviations exceed tolerance.
- Document survey field notes and reduced survey data.
- Verify survey accuracy per survey accuracy standards from Employer's Requirements or project survey standards (Guidance §C-3 as-built accuracy consideration).

**7.2.3 Capture As-Built Survey Records:**
- Complete as-built survey record in tabular format (utility identification, survey control reference, final location coordinates, final elevations, design location reference from DEL-03.01, deviation from design, deviation approval reference, survey accuracy verification).
- Attach survey field notes and reduced survey data to record appendices.
- Organize as-built survey records in record package as-built survey section.

**Verification checkpoint:** Self-check verifies as-built survey data is complete, survey accuracy is verified, deviations are documented and approved; interdisciplinary check verifies as-built locations match DEL-03.01 design intent within tolerance.

**Cross-reference:** Specification §FR-4; Guidance §C-3; Datasheet §Construction as-built survey records.

### 8. Compile Commissioning Documentation and Handover Records

**8.1 Compile System-Level Commissioning Checklist:**
- Integrate all installation and test records into system-level commissioning checklist using format per Guidance §Example 4.
- Commissioning checklist sections:
  - Installation complete: Material delivery records reviewed, installation logs reviewed, dimensional verification records reviewed.
  - Pressure testing complete: All pipe sections pressure tested and passed, leak repairs completed and retested.
  - Flow testing complete: Design flows verified, system capacity confirmed.
  - CCTV inspection complete: All pipes inspected, defects identified and evaluated (reference DEL-03.06 for detailed analysis), remediation plan developed for critical defects.
  - As-built survey complete: Final utility locations surveyed, deviations documented and approved, as-built drawings updated.
  - OWS performance verification complete: Flow testing passed, retention time verified, treatment performance passed, instrumentation calibrated.
  - Containment integrity testing complete: Visual inspection passed, hydrostatic/dye testing passed, no leaks detected.

**8.2 Document Punch List Items:**
- Identify outstanding items (minor defects, documentation completion, training requirements).
- Document responsible party, target completion date for each punch list item.
- Track punch list item resolutions; document completion confirmation.

**8.3 Obtain Final Acceptance Sign-Offs:**
- Obtain D&B Contractor QA/QC Manager signature/date on commissioning checklist.
- Obtain Employer's Representative signature/date if required per contract.
- Obtain regulatory agency acceptance signature if required for environmental permits (OWS performance verification, discharge monitoring).

**8.4 Compile Handover Documentation:**
- Prepare record package delivery confirmation documenting installation and test records, as-built drawings, O&M manuals, training completion records.
- Obtain operations team acknowledgment of handover documentation receipt.
- Document handover date and handover sign-offs per Guidance §C-6 operations handover consideration.

**8.5 Prepare Record Package Introduction:**
- Document record package scope, data sources (field test execution records, calibration certificates, CCTV video files, survey field notes, DEL-03.01/02/03/04 design deliverable references), applicable standards and test procedures (from Employer's Requirements and DEL-03.02), abbreviations and definitions, record organization.
- Provide executive summary of commissioning results (all systems tested and accepted, punch list items identified and resolved, handover complete).

**Verification checkpoint:** QA/QC checker reviews commissioning checklist completeness, punch list item resolutions, final acceptance sign-offs, handover documentation.

**Cross-reference:** Specification §FR-5; Guidance §P-4, §C-6, §Example 4; Datasheet §Construction commissioning records.

### 9. Execute Verification Workflow

**9.1 Self-Check (Inspector/Preparer Review):**
- Review installation and test record package completeness for all record types per Specification §Scope.
- **9.1.1 Record completeness**: Verify all required record sections are populated (installation documentation, pressure testing, leak testing, flow testing, CCTV inspection, as-built survey, OWS performance verification, containment integrity, commissioning records).
- **9.1.2 Test execution verification**: Confirm test execution procedures were followed per Employer's Requirements and DEL-03.02 specification; verify test equipment calibration certificates are current and referenced.
- **9.1.3 Test result accuracy**: Validate test results are accurately recorded (pressure readings, flow measurements, survey data, laboratory analysis results); verify calculations are correct (pressure drop, retention time, treatment efficiency).
- **9.1.4 Acceptance criteria application**: Confirm acceptance criteria are correctly applied and test results are properly evaluated (pass/fail determination documented with supporting rationale).
- **9.1.5 Metadata completeness**: Confirm record package metadata (numbering, revision, inspector/reviewer names, test dates, equipment calibration references) are correctly populated per Specification §FR-5.
- **9.1.6 Cross-reference verification**: Check cross-references to related deliverables (DEL-03.01/02/03/04/06) are correct and data sources are documented.
- **9.1.7 Inspector sign-offs**: Verify inspector signatures/dates are present on all test records.
- **Self-check documentation**: Inspector/preparer signs/dates self-check checklist, documents any corrections made.
- **Cross-reference:** Specification §Verification self-check; Specification §QR-2, §FR-5; Guidance §C-1, §C-2.

**9.2 Interdisciplinary Check (Coordination Review):**
- **9.2.1 DEL-03.01 Drawing Set coordination**: Verify test section identification, as-built survey location referencing, CCTV inspection pipe identification match drawings (Specification §IF-1).
- **9.2.2 DEL-03.02 Technical Specification coordination**: Verify test procedures and acceptance criteria match specification requirements; confirm test results demonstrate specification compliance (Specification §IF-1).
- **9.2.3 DEL-03.03 Design Calculations coordination**: Verify flow test results and OWS performance testing validate design flow rates and capacity calculations (Specification §IF-1).
- **9.2.4 DEL-03.04 Data Sheet Package coordination**: Verify OWS performance testing references equipment specifications from OWS data sheet; confirm pressure testing references pipe material specifications (Specification §IF-1).
- **9.2.5 DEL-03.06 CCTV Survey Report coordination**: Verify CCTV inspection record format, defect coding system, video file indexing support DEL-03.06 analysis; confirm CCTV records provided to DEL-03.06 team (Specification §IF-2; Guidance §C-5).
- **9.2.6 Environmental protection review**: Review OWS performance verification records with environmental specialist to confirm OBJ-7 Environmental Protection compliance (Specification §FR-2; Guidance §P-2).
- **Interdisciplinary check documentation**: QA/QC checker signs/dates interdisciplinary review log, documents coordination confirmation or issues.
- **Cross-reference:** Specification §Verification interdisciplinary check; Specification §IF-1, §IF-2; Guidance §P-2, §C-5.

**9.3 Independent Check (Approver Review):**
- **9.3.1 ER compliance**: Verify installation and test records comply with Employer's Requirements Volume 2 Part 2 testing procedures and acceptance criteria (Specification §Verification; Guidance §C-2).
- **9.3.2 Test result validation**: Validate pressure test results, flow test results, OWS performance test results against performance requirements (Specification §PR-1 hydraulic performance, Specification §PR-2 environmental performance); confirm test equipment calibration and test result accuracy (Specification §QR-2).
- **9.3.3 Environmental protection validation**: Validate OWS performance verification records and containment integrity testing support OBJ-7 Environmental Protection; confirm treatment efficiency and discharge water quality meet regulatory limits and environmental permit requirements (Specification §FR-2, §PR-2; Guidance §P-2).
- **9.3.4 Commissioning documentation review**: Review commissioning checklist, punch list resolutions, final acceptance sign-offs, handover documentation; confirm commissioning is complete and operations handover is ready (Specification §FR-5; Guidance §C-6).
- **9.3.5 QA documentation review**: Review self-check checklist and interdisciplinary review log to confirm all verification activities are completed (Specification §QR-1).
- **Independent check documentation**: Independent reviewer signs/dates independent check review form and record package cover page approver signature block; documents review comments and confirms resolutions.
- **Cross-reference:** Specification §Verification independent check; Specification §Standards, §PR-2, §QR-3; Guidance §C-2, §P-2.

### 10. Archive Record Package into Record Management System

- Finalize record package issue date on cover page; set revision code to "00" for initial issue per Datasheet §Attributes.
- Compile record package PDF (cover page, introduction, all test records, commissioning documentation, appendices) or organize physical record package per project requirements.
- Submit record package to record management system with metadata (document number, revision, title, discipline, package, deliverable ID, inspector/reviewer/approver names, issue date).
- Obtain record management system confirmation of archival; verify distribution per distribution matrix (commissioning team, operations team, regulatory agencies if required).
- File quality records (inspection checklists, test witness logs, self-check checklist, interdisciplinary review log, independent check review form, QA checklists) per Quality Management Plan archival requirements.
- **Archival completion confirmation**: QA coordinator confirms record package is archived into record management system and distribution is complete.
- **Cross-reference:** Specification §FR-5, §Documentation; Datasheet §Conditions record control; Guidance §C-6 operations handover and maintenance reference.

## Verification

**Verification workflow summary:**
1. **Self-check (inspector/preparer review)**: Inspector/preparer verifies record completeness, test execution procedures followed, test results accurately recorded, acceptance criteria correctly applied, metadata complete, cross-references correct, inspector sign-offs present per Step 9.1 activities; documents review using self-check checklist.
2. **Interdisciplinary check (coordination review)**: QA/QC checker verifies coordination with related deliverables (DEL-03.01/02/03/04/06), reviews environmental protection record adequacy, and confirms commissioning documentation completeness per Step 9.2 activities; documents review using interdisciplinary review log.
3. **Independent check (approver review)**: Independent reviewer validates compliance with Employer's Requirements, confirms test result validity and performance requirements met, reviews environmental protection compliance, validates commissioning documentation, and reviews QA documentation per Step 9.3 activities; documents review by signing record package for archival.

**Verification traceability:** All verification activities documented in quality records; verification links installation and test record package to Specification requirements and design deliverables.

**Cross-reference:** Specification §Verification; Specification §QR-1; Guidance §P-4, §C-5; Datasheet §Cross-Document Linkages.

## Records

**Installation and test record deliverables (primary outputs):**
- **Record package PDF or physical package**: Pressure test records, leak test records, flow testing records, CCTV inspection records, as-built survey records, OWS performance verification records, containment integrity test records, commissioning records, organized per Step 3 structure (Source: Specification §Documentation; Datasheet §Construction).
- **Appendices**: Calibration certificates (pressure gauges, flow meters, survey equipment, instrumentation), laboratory test reports (discharge water quality), CCTV video files (digital media references or physical media), test equipment specifications, inspector qualifications, archived with record package.

**Quality records (supporting documentation):**
- **Inspection checklists**: Pre-test checklists (pressure testing), pre-operational inspection checklists (OWS performance verification) per Steps 4.2, 6.1 (Specification §Verification).
- **Test witness logs**: Documenting inspector presence during testing, test conditions, test results per testing execution steps.
- **Self-check checklist**: Documents inspector/preparer review completion per Step 9.1 (Specification §Verification).
- **Interdisciplinary review log**: Documents coordination check completion per Step 9.2 (Specification §Verification).
- **Independent check review form**: Documents approver review completion per Step 9.3 (Specification §Verification).
- **QA checklists**: Per Quality Management Plan requirements (Specification §QR-1).
- **Record register entry**: Record management system record (Specification §FR-5).
- **Calibration certificates**: For all test equipment (Specification §QR-2; documented in Steps 2.3, 4.2, 5.1, 6.6, 7.2.1).
- **Laboratory test reports**: Discharge water quality analysis for OWS performance verification (documented in Step 6.4).

**Records retention:** All installation and test record deliverables and quality records archived per project record management system and Quality Management Plan requirements.

**Cross-reference:** Specification §Documentation quality records; Specification §QR-1, §QR-2; Datasheet §References quality records; Guidance §C-6 operations handover.

## Pass 3 Final Notes

**Pass 3 Reconciliation Completed:**
- All cross-document linkages verified; steps linked to requirements; entity coverage confirmed; terminology consistent.
- Documents ready for WORKING_ITEMS sessions.
