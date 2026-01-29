# Specification: DEL-03.05 Underground Utilities Installation & Test Records

## Scope

This specification governs the capture, verification, and documentation of **Underground Utilities Installation & Test Records** for **PKG-03 Underground Utilities & Drainage**. The records provide evidence of completion, inspection, and testing for storm drainage, OWS, and duct bank systems to demonstrate compliance with design requirements and Employer's Requirements (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:202).

**Anticipated artifacts within this scope:**
- Pressure test records (hydrostatic testing, air testing, pre-test checklists, test execution logs, acceptance verification)
- Leak test records (leak detection, repair documentation, retest verification)
- Flow testing records (flow measurement, design flow comparison, acceptance verification)
- CCTV inspection records (video logs, defect coding, location referencing, remediation recommendations)
- As-built survey records (final locations and elevations, deviations documentation, survey accuracy verification)
- OWS performance verification records (flow testing, retention time verification, treatment efficiency testing, instrumentation calibration, commissioning sign-off)
- Containment integrity test records (visual inspection, hydrostatic/dye testing, leak detection, repair documentation)
- Commissioning records (system-level checklists, final acceptance sign-offs, punch list resolutions, handover documentation)

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:202; elaborated in Datasheet §Construction for record package organization)

**Exclusions:**
- Detailed remediation design for identified defects is outside DEL-03.05 scope; records document defects and recommendations only; remediation execution is separate activity (records provide inputs for remediation planning).
- Process equipment testing and commissioning are outside PKG-03 scope per Scope Focus (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47).

## Requirements

### Functional Requirements

**FR-1: Hydraulic Integrity Documentation**
- Document pressure testing, leak testing, and flow testing results for all underground utilities (storm drainage pipes, OWS piping connections, duct bank conduits) to demonstrate hydraulic integrity and leak-free installation per the decomposition scope (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:202).
- Pressure test records shall include pre-test checklist (visual inspection, joint completion, backfill status, isolation, gauge calibration), test execution log (initial pressure, duration, interval readings, leak observations), test results (pressure drop calculation, acceptance criteria comparison, pass/fail determination), and inspector signatures (ASSUMPTION per typical pressure testing protocol; rationale in Guidance §Purpose).
- Verification: Procedure §Verification self-check confirms all pressure test record sections are complete and acceptance criteria are correctly applied; interdisciplinary check verifies coordination with DEL-03.02 specification acceptance criteria.

**FR-2: Environmental Protection Documentation**
- Document OWS performance verification testing, containment integrity testing, and discharge monitoring instrumentation calibration to support **OBJ-7 Environmental Protection** objectives for PKG-03 (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786).
- OWS performance verification records shall document flow testing (design flow, peak flow), retention time verification, treatment performance testing (oil removal efficiency measurement, discharge water quality laboratory analysis results), instrumentation calibration (level sensors, flow meters, oil layer thickness monitors), and commissioning sign-off to demonstrate environmental compliance (rationale in Guidance §P-2; operational context in Datasheet §Conditions).
- Verification: Procedure §Steps OWS performance testing requirement; Procedure §Verification independent check confirms OWS performance verification records demonstrate environmental compliance per OBJ-7.

**FR-3: Pipe Condition Documentation**
- Document CCTV inspection results for storm pipes and culverts to identify defects, support remediation planning, and provide baseline condition for future maintenance (Dependencies: coordination with DEL-03.06 CCTV Survey Report which provides detailed analysis of CCTV findings; NOT_TRACKED per `_DEPENDENCIES.md`).
- CCTV inspection records shall include video file references, defect coding log (defect type, severity, location/chainage, description), location referencing (manholes, tie-in points), defect photographs, and remediation recommendations to support DEL-03.06 analysis (Datasheet §Construction lists CCTV inspection records).
- Verification: Procedure §Verification interdisciplinary check includes coordination review with DEL-03.06 development team to confirm CCTV record format supports detailed defect analysis.

**FR-4: As-Built Documentation**
- Document final locations and elevations of installed underground utilities to provide as-built reference for operations, maintenance, and future modifications (ASSUMPTION per typical as-built documentation requirements; rationale in Guidance §Purpose supports operations handover).
- As-built survey records shall include survey control tie-ins, final utility locations/elevations (pipe inverts, rim elevations, OWS location, duct bank routes), deviations from design documented and approved, survey field notes and reduced data, and survey accuracy verification (Datasheet §Construction describes as-built survey records).
- Verification: Procedure §Verification self-check confirms as-built survey data is complete and deviations are documented; interdisciplinary check verifies as-built locations match DEL-03.01 design intent within tolerance.

**FR-5: Record Metadata and Traceability**
- Ensure installation and test record metadata (numbering, revision, inspector/reviewer signatures, test dates, equipment calibration references, data source identification) supports traceability to design deliverables, test standards, and Quality Management Plan requirements (Datasheet §Attributes lists metadata fields; this requirement ensures records implement those fields correctly).
- Record numbering scheme shall follow project record management system; initial issue revision is "00" per Datasheet §Attributes (TBD: specific numbering format pending project record management system definition per Procedure §Prerequisites).
- Verification: Procedure §Steps metadata compilation; Procedure §Verification QA review confirms metadata completeness before record management system archival.

### Performance Requirements

**PR-1: Hydraulic Performance Verification**
- Conform to the hydraulic performance, pressure testing, and flow testing expectations described in the Employer's Requirements Volume 2 Part 2: Civil & Process Mechanical Works and DEL-03.02 Technical Specification (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, specific clauses TBD; DEL-03.02 provides acceptance criteria).
- Pressure test results shall demonstrate leak-free installation within acceptance criteria (allowable pressure drop over test duration); flow test results shall demonstrate measured flow rates match design flow rates from DEL-03.03 calculations within tolerance (interface linkage to calculations and specification deliverables; Datasheet §Construction describes pressure and flow testing records).
- Verification: Pressure and flow test results validated against DEL-03.02 specification acceptance criteria and DEL-03.03 calculation design flows; Procedure §Verification independent check confirms test results meet hydraulic performance requirements.

**PR-2: Environmental Performance Verification**
- Ensure OWS performance verification records demonstrate treatment capacity, retention volume, oil removal efficiency, and discharge water quality meet environmental protection requirements for Phase 1 supporting **OBJ-7 Environmental Protection** as described in the decomposition (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; Datasheet §Conditions references OBJ-7).
- OWS performance testing shall validate treatment performance (measured oil removal efficiency vs target efficiency from DEL-03.04 OWS data sheet), discharge water quality (laboratory analysis results vs regulatory limits from Employer's Requirements), and retention time (measured vs design from DEL-03.03 calculations) to support environmental permit compliance and regulatory approval (interface linkage; Datasheet §Construction notes OWS performance verification records).
- Verification: Procedure §Steps OWS performance testing validates equipment performance against DEL-03.04 OWS data sheet specifications and DEL-03.03 capacity calculations; Procedure §Verification independent check confirms environmental performance compliance per OBJ-7 and regulatory requirements.

### Interface Requirements

**IF-1: Coordination with Related PKG-03 Deliverables**
- Coordinate installation and test records with related PKG-03 deliverables to ensure consistency and traceability:
  - **DEL-03.01 Drawing Set**: Ensure as-built survey data references design drawing locations; CCTV inspection records reference pipe identification from drawings; test section identification matches drawing nomenclature (Datasheet §References notes drawings provide design basis).
  - **DEL-03.02 Technical Specification**: Ensure test procedures and acceptance criteria in records match specification requirements; validation testing demonstrates specification compliance (Datasheet §References notes specification provides performance targets and test protocols).
  - **DEL-03.03 Design Calculations**: Ensure flow test results and OWS performance testing validate design flow rates and capacity calculations; test results demonstrate calculation assumptions (Datasheet §References notes calculations provide sizing basis and performance validation).
  - **DEL-03.04 Data Sheet Package**: Ensure OWS performance testing references equipment specifications from OWS data sheet; pressure testing references pipe material specifications; instrumentation calibration references instrument data sheets (rationale in Guidance §C-5 CCTV record coordination).
- Verification: Procedure §Verification interdisciplinary check confirms record content aligns with related deliverable content; Procedure §Steps input data collection ensures upstream deliverables are reviewed before testing execution.

**IF-2: Coordination with DEL-03.06 CCTV Survey Report**
- CCTV inspection records captured in DEL-03.05 provide raw data (video files, defect coding logs, location referencing) for detailed analysis in DEL-03.06 CCTV Survey Report; coordinate record format and defect coding system to support DEL-03.06 analysis (Dependencies: DEL-03.06 uses DEL-03.05 CCTV inspection records as input; NOT_TRACKED per `_DEPENDENCIES.md`).
- CCTV inspection records shall use consistent defect coding system, location referencing methods, and video file indexing to enable efficient DEL-03.06 report development and defect remediation planning (ASSUMPTION per typical CCTV inspection workflow; Datasheet §References notes DEL-03.06 coordination).
- Verification: Procedure §Verification interdisciplinary check includes coordination review with DEL-03.06 development team to confirm CCTV record format compatibility; QA review verifies defect coding consistency.

### Quality Requirements

**QR-1: Compliance with Quality Management Plan**
- Deliverables shall comply with the project Quality Management Plan, inspection and testing requirements, and record retention expectations captured in Volume 2 Part 1: Employer's Requirements – General Requirements (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, details TBD).
- Installation and test record capture workflow shall follow quality procedures: field inspector executes tests and captures records, QA/QC checker reviews record completeness and test results, approver signs before archival (ASSUMPTION per typical QA process; Procedure §Verification describes review steps).
- Verification: Procedure §Verification self-check, interdisciplinary check, and independent check are documented with review signatures; QA checklists are completed before archival (Procedure §Records lists QA checklists in records output).

**QR-2: Test Equipment Calibration and Data Accuracy**
- All test equipment (pressure gauges, flow meters, survey equipment, instrumentation) shall be calibrated to traceable standards; calibration certificates shall be included in record appendices to support test result validity (ASSUMPTION per typical testing requirements; rationale in Guidance §C-1 test equipment calibration consideration).
- Test execution data (pressure readings, flow measurements, survey data, laboratory analysis results) shall be recorded accurately in field and validated during record review; any anomalies or retests shall be documented (Procedure §Steps testing execution and record capture; Datasheet §Attributes "Data Sources" lists field test execution records and calibration certificates).
- Verification: Procedure §Verification self-check confirms test equipment calibration certificates are current and test data is accurately recorded; independent check validates test results against acceptance criteria.

**QR-3: Testing Acceptance Criteria Documentation**
- Installation and test records shall document testing acceptance criteria for each test type (pressure test allowable pressure drop and duration, flow test tolerance, CCTV defect severity limits, OWS performance targets, survey accuracy standards) to support conformance verification (Datasheet §Construction describes testing acceptance criteria documentation).
- Acceptance criteria shall reference applicable standards, Employer's Requirements clauses, and DEL-03.02 Technical Specification requirements; test results shall be compared to acceptance criteria with pass/fail determination documented (interface linkage to testing standards and specification).
- Verification: Procedure §Verification QA review confirms acceptance criteria are correctly documented and test results are properly evaluated; independent check validates acceptance criteria compliance with standards and Employer's Requirements.

## Standards

**Governing Standards:**
- **Employer's Requirements Volume 2 Part 2: Civil & Process Mechanical Works** is the authoritative source for applicable testing procedures, acceptance criteria, and performance standards; specific clauses will be extracted and referenced in test records as testing execution proceeds (Source: test/Volume_2_Part_2_Employers_Requirements.pdf).
- **Employer's Requirements Volume 2 Part 1: General Requirements** governs project Quality Management Plan, inspection and testing requirements, QA/QC procedures, and record retention requirements (Source: test/Volume_2_Part_1_Employers_Requirements.pdf).

**Supplementary Standards (TBD pending project definition):**
- Pressure testing standards: ASTM standards for hydrostatic testing, air testing procedures, acceptance criteria (QR-3 references testing standards; specific standards TBD from Employer's Requirements and DEL-03.02 Technical Specification).
- Flow testing standards: Flow measurement procedures, instrumentation requirements, accuracy standards (PR-1 references flow testing standards; TBD from Employer's Requirements).
- CCTV inspection standards: Pipeline Assessment and Certification Program (PACP) or equivalent defect coding system, video quality standards, inspection procedures (FR-3 references CCTV standards; TBD from Employer's Requirements and coordination with DEL-03.06).
- Survey standards: Land surveying accuracy standards, survey control requirements, as-built documentation procedures (FR-4 references survey standards; TBD from Employer's Requirements).
- OWS performance testing standards: Treatment performance testing procedures, discharge water quality sampling and analysis methods, instrumentation calibration procedures (PR-2 references OWS testing standards; TBD from Employer's Requirements and environmental permits).
- Calibration standards: Test equipment calibration procedures, traceability requirements, calibration certificate formats (QR-2 references calibration standards; TBD from project Quality Management Plan).

**Applicable Test Procedures (ASSUMPTION pending ER extraction):**
- Hydrostatic pressure testing for pipes (test duration, allowable pressure drop, acceptance criteria)
- Air testing for duct banks and sealed systems
- Flow testing for storm drainage (measurement methods, design flow comparison, acceptance tolerance)
- CCTV inspection for pipes and culverts (video quality, defect coding, location referencing)
- As-built surveying (survey control, accuracy requirements, deviation documentation)
- OWS performance testing (flow capacity testing, retention time measurement, treatment efficiency testing, discharge water quality sampling)
- Containment integrity testing (visual inspection, hydrostatic or dye testing, leak detection)
- Instrumentation calibration (calibration procedures for level sensors, flow meters, oil layer thickness monitors)

(Note: Specific test procedure details and acceptance criteria to be extracted from Employer's Requirements Volume 2 Part 2 and DEL-03.02 Technical Specification during testing execution; see Procedure §Prerequisites for reference material review requirement.)

## Verification

**Inspection and Testing Review Process:**
- **Self-check (inspector/preparer review)**: Ensures test records are complete, test execution procedures were followed, test results are accurately recorded, acceptance criteria are correctly applied, calibration certificates are current; verifies all anticipated record types (Scope list) are included; checks metadata completeness (FR-5). (Source: Procedure §Verification self-check step; Datasheet §Cross-Document Linkages references Procedure verification process.)

- **Interdisciplinary check**: Verifies coordination with related deliverables (DEL-03.01 drawings for as-built comparison, DEL-03.02 specification for acceptance criteria, DEL-03.03 calculations for performance validation, DEL-03.04 data sheets for equipment specifications, DEL-03.06 CCTV survey report for defect analysis) per IF-1 and IF-2; confirms test results demonstrate design requirements; reviews OWS performance verification records (FR-2) with environmental specialist. (Source: Procedure §Verification interdisciplinary check step; ASSUMPTION per typical installation record review process and Quality Management Plan per test/Volume_2_Part_1_Employers_Requirements.pdf.)

- **Independent check**: Confirms compliance with Employer's Requirements (Volume 2 Part 2) testing procedures and acceptance criteria; validates test results against performance requirements (PR-1 hydraulic performance, PR-2 environmental performance); ensures OWS performance verification and containment integrity testing support OBJ-7 Environmental Protection; records results in reviewer signature blocks. (Source: Procedure §Verification independent check step; reviews tie to Specification requirements to close verification loop.)

**Test Result Validation:**
- Pressure test results (pressure drop calculations, pass/fail determination) validated against acceptance criteria from DEL-03.02 specification and Employer's Requirements (FR-1 and PR-1 requirements; Procedure §Steps pressure testing execution and acceptance verification).
- Flow test results (measured flow rates vs design flow rates) validated against DEL-03.03 calculation design flows and acceptance tolerance (PR-1 requirement).
- OWS performance test results (treatment efficiency, discharge water quality, retention time) validated against DEL-03.04 OWS data sheet specifications and regulatory limits (FR-2 and PR-2 requirements).
- CCTV inspection defect coding validated for consistency and completeness to support DEL-03.06 analysis (FR-3 requirement).
- As-built survey data validated for accuracy and deviations documented and approved (FR-4 requirement).
- Results recorded in test review records and QA checklists per QR-1 (Procedure §Records lists test witness logs, inspection checklists, review logs, QA checklists).

**Traceability Verification:**
- Installation and test records reference design deliverables (DEL-03.01 drawings, DEL-03.02 specification, DEL-03.03 calculations, DEL-03.04 data sheets), test equipment calibration certificates, laboratory test reports, and applicable standards with document IDs and test dates (QR-2 test equipment calibration and data accuracy requirement; Datasheet §Attributes "Data Sources" lists data source types).
- Test acceptance criteria cross-reference Employer's Requirements clauses and DEL-03.02 specification requirements to maintain traceability (QR-3 acceptance criteria documentation requirement).
- Procedure §Verification QA review confirms data source references are correct and document linkages are maintained per IF-1, IF-2, and QR-2.

## Documentation

**Documented Artifacts:**
- Pressure test records (pre-test checklists, test execution logs, pressure-time graphs, acceptance verification, inspector signatures)
- Leak test records (leak detection records, repair documentation, retest verification)
- Flow testing records (flow measurement equipment calibration, flow test results, acceptance verification)
- CCTV inspection records (video file index, defect coding logs, defect photographs, remediation recommendations)
- As-built survey records (survey control data, final utility locations/elevations, deviation documentation, survey accuracy verification)
- OWS performance verification records (pre-operational inspection, flow testing, retention time verification, treatment performance testing, instrumentation calibration, commissioning sign-off)
- Containment integrity test records (visual inspection records, hydrostatic/dye test records, leak detection, repairs, retest verification)
- Commissioning records (system-level checklists, final acceptance sign-offs, punch list resolutions, handover documentation)
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:202; detailed in Datasheet §Construction)

**Record Package Organization:**
- Cover page: Package title, project identification, revision history, table of contents
- Introduction: Scope, data sources, applicable standards and test procedures, abbreviations, record organization
- Installation documentation section: Material delivery logs, installation progress logs, dimensional verification records
- Pressure testing section: Organized by pipe section or test package, includes pre-test checklists, test execution logs, pressure-time graphs, acceptance verification, inspector signatures
- Leak testing section: Leak detection records, repair documentation, retest verification
- Flow testing section: Flow measurement equipment calibration, flow test results by drainage area or system section, acceptance verification
- CCTV inspection section: Organized by pipe run, includes video file index, defect coding logs, defect photographs, remediation recommendations
- As-built survey section: Survey control data, final utility locations/elevations, deviation documentation, survey accuracy verification
- OWS performance verification section: Pre-operational inspection, flow testing, retention time verification, treatment performance testing, instrumentation calibration, commissioning sign-off
- Containment integrity testing section: Visual inspection records, hydrostatic/dye test records, leak detection, repairs, retest verification
- Commissioning records section: System-level checklists, final acceptance sign-offs, punch list resolutions, handover documentation
- Appendices: Calibration certificates, laboratory test reports, CCTV video files (digital media references), test equipment specifications, inspector qualifications
(Datasheet §Construction describes record package organization; Procedure §Steps establishes package structure)

**Associated Quality Records:**
- Inspection checklists (pre-test checklists, pre-operational inspection checklists per Verification section)
- Test witness logs (documenting inspector presence during testing, test conditions, test results)
- Review logs (self-check, interdisciplinary check, independent check per Verification section)
- Inspector/reviewer/approver signatures
- QA checklists per Quality Management Plan requirements (QR-1)
- Record register entry documenting archival status and distribution
- Calibration certificates for test equipment (pressure gauges, flow meters, survey equipment, instrumentation per QR-2)
- Laboratory test reports (discharge water quality analysis for OWS performance verification)
(Source: Procedure §Records quality records section; supports QR-1 compliance with Quality Management Plan)

## Pass 3 Final Notes

**Pass 3 Reconciliation Completed:**
- All cross-document linkages verified bidirectional; entity coverage confirmed; terminology consistent.
- Requirements traceability: All Specification requirements map to Procedure implementation steps and verification activities.
- TBD items align with Datasheet and have clear resolution path via Procedure prerequisites.
- Documents ready for WORKING_ITEMS sessions.
