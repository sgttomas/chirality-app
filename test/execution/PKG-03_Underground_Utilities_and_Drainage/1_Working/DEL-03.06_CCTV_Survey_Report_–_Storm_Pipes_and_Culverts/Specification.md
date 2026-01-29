# Specification: DEL-03.06 CCTV Survey Report – Storm Pipes & Culverts

## Scope

This specification governs the development of the **CCTV Survey Report – Storm Pipes & Culverts** for **PKG-03 Underground Utilities & Drainage**. The report documents analysis and results of CCTV surveys for storm pipes and culverts, providing detailed defect assessment, pipe condition evaluation, and remediation recommendations required for design verification, commissioning acceptance, and operations handover per the Employer's Requirements (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:203).

**Anticipated artifacts within this scope:**
- Executive summary (survey overview, key findings, overall condition assessment, recommendations summary)
- Pipe inventory (surveyed pipes with drawing references, material types, diameters, lengths, survey status, condition ratings)
- Defect analysis (comprehensive defect coding log, severity assessment, location referencing, defect descriptions, environmental/hydraulic impact assessment, defect photographs/video frame captures)
- Remediation recommendations (defect-by-defect recommendations, remediation methods, priority, cost implications, implementation timing)
- Video file index (video file names, pipe coverage, storage locations)
- Conclusions and sign-offs (overall pipe condition conclusions, limitations and assumptions, reviewer sign-offs)

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:203; elaborated in Datasheet §Construction for report organization)

**Exclusions:**
- Detailed remediation design and construction drawings are outside DEL-03.06 scope; report provides remediation recommendations only; detailed remediation design is separate deliverable if defects require repair/replacement.
- Process equipment inspection and above-ground structures are outside PKG-03 scope per Scope Focus (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47).

## Requirements

### Functional Requirements

**FR-1: Clear Summary Documentation**
- Provide executive summary documenting survey overview, key findings, overall pipe condition assessment, and recommendations summary to enable stakeholder understanding and decision-making (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:203).
- Executive summary shall include survey extent (number of pipes surveyed, total length surveyed), key findings (number of defects by severity, critical defects requiring immediate attention), overall condition assessment (percentage of pipes in good/fair/poor condition, condition rating system explanation), and high-priority recommendations to support project management and commissioning planning (ASSUMPTION per typical CCTV survey report executive summary; rationale in Guidance §Purpose).
- Verification: Procedure §Verification self-check confirms executive summary is complete and accurately reflects report content; interdisciplinary check verifies summary clarity for non-specialist stakeholders.

**FR-2: Environmental Protection Defect Identification**
- Identify and document defects that could impact containment integrity, environmental controls, or spill migration pathways to support **OBJ-7 Environmental Protection** objectives for PKG-03 (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786).
- Defect analysis shall include environmental impact flag for defects affecting containment (defects in pipes within containment areas, defects creating potential spill migration pathways, defects near sensitive receptors), with environmental impact assessment describing potential consequences and recommended mitigation actions to support environmental risk management (rationale in Guidance §P-2; operational context in Datasheet §Conditions).
- Verification: Procedure §Steps environmental impact assessment requirement; Procedure §Verification independent check confirms environmental protection defect identification supports OBJ-7.

**FR-3: Comprehensive Defect Documentation**
- Document all identified defects with comprehensive defect coding log including defect type, severity, location, description, environmental/hydraulic impact assessment, and photograph/video frame capture references to support remediation planning and asset management (Dependencies: uses DEL-03.05 CCTV Inspection Records as primary input; NOT_TRACKED per `_DEPENDENCIES.md`).
- Defect coding log shall use standard defect coding system (PACP or equivalent per project CCTV survey standards) with defect type coding, severity scoring (minor, moderate, severe, critical), location referencing (pipe ID, chainage, manholes), defect dimensions and orientation, and photograph/video references to enable consistent defect evaluation and remediation prioritization (Datasheet §Construction lists comprehensive defect coding log).
- Verification: Procedure §Verification interdisciplinary check includes defect coding consistency review and coordination with DEL-03.05 CCTV inspection records to confirm defect data accuracy.

**FR-4: Remediation Recommendations**
- Provide defect-by-defect remediation recommendations with remediation methods, priority, cost implications, and implementation timing to support remediation planning and budgeting (ASSUMPTION per typical CCTV survey report remediation recommendations; rationale in Guidance §Purpose supports remediation planning).
- Remediation recommendations shall include recommended action (monitor, repair, replace, clean, line), remediation method description (pipe repair methods, lining options, replacement approach), priority (immediate, near-term, long-term, monitor per Guidance §T-2 remediation priority trade-off), estimated cost implications (order of magnitude cost estimate for budgeting), and implementation timing recommendations (coordinate with construction schedule, operations access windows) to enable efficient remediation execution (Datasheet §Construction describes remediation recommendations content).
- Verification: Procedure §Verification self-check confirms remediation recommendations are constructable and cost-effective; interdisciplinary check verifies coordination with project schedule and operations access; independent check validates remediation priority and methods.

**FR-5: Report Metadata and Traceability**
- Ensure CCTV survey report metadata (numbering, revision, surveyor/reviewer/approver signatures, survey dates, video file references, data source identification) supports traceability to DEL-03.05 CCTV inspection records, design deliverables, CCTV survey standards, and Quality Management Plan requirements (Datasheet §Attributes lists metadata fields; this requirement ensures report implements those fields correctly).
- Report numbering scheme shall follow project document control system; initial issue revision is "00" per Datasheet §Attributes (TBD: specific numbering format pending project document control system definition per Procedure §Prerequisites).
- Verification: Procedure §Steps metadata compilation; Procedure §Verification QA review confirms metadata completeness before document control system release.

### Performance Requirements

**PR-1: Defect Severity and Pipe Condition Assessment**
- Conform to the defect severity criteria, pipe condition assessment methods, and reporting expectations described in the Employer's Requirements Volume 2 Part 2: Civil & Process Mechanical Works and CCTV survey standards (PACP or equivalent) (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, specific clauses TBD; PACP or equivalent provides defect coding and severity scoring).
- Defect severity assessment shall consider defect dimensions, structural impact (pipe strength reduction, collapse risk), hydraulic impact (flow reduction, blockage risk, infiltration/exfiltration potential), environmental impact (containment breach risk, spill migration potential), defect frequency (isolated, widespread), and progression risk (stable, active, deteriorating) to support objective severity scoring (interface linkage to CCTV survey standards and engineering judgment; Datasheet §Construction describes defect severity assessment).
- Verification: Defect severity assessments validated against CCTV survey standards (PACP or equivalent severity scoring criteria) and Employer's Requirements acceptance criteria; Procedure §Verification independent check confirms defect severity assessment methodology and results compliance with standards.

### Interface Requirements

**IF-1: Coordination with Related PKG-03 Deliverables**
- Coordinate CCTV survey report content with related PKG-03 deliverables to ensure consistency and traceability:
  - **DEL-03.01 Drawing Set**: Ensure pipe inventory references design drawing pipe identification; defect locations reference drawing manholes and tie-in points; defect location referencing matches drawing nomenclature (Datasheet §References notes drawings provide pipe identification).
  - **DEL-03.02 Technical Specification**: Ensure defect severity criteria reference specification acceptance standards; remediation methods consider specification installation requirements (Datasheet §References notes specification provides defect severity criteria).
  - **DEL-03.03 Design Calculations**: Ensure hydraulic impact assessment references design flow rates and capacity calculations; defect flow reduction impact compared to design margins (Datasheet §References notes calculations provide hydraulic impact assessment benchmarks).
  - **DEL-03.04 Data Sheet Package**: Ensure pipe material properties from pipe material data sheets inform pipe condition assessment and remediation method selection (rationale in Guidance §C-4 pipe inventory coordination).
- Verification: Procedure §Verification interdisciplinary check confirms report content aligns with related deliverable content; Procedure §Steps input data collection ensures upstream deliverables are reviewed before defect analysis.

**IF-2: Coordination with DEL-03.05 Installation and Test Records**
- DEL-03.06 CCTV Survey Report uses DEL-03.05 CCTV Inspection Records as primary input; coordinate with DEL-03.05 to obtain raw CCTV video files, defect coding logs, and location referencing for detailed analysis (Dependencies: DEL-03.05 provides raw inspection data; NOT_TRACKED per `_DEPENDENCIES.md`).
- CCTV survey report shall reference DEL-03.05 CCTV inspection records with video file names, inspection dates, surveyor names to maintain traceability to field inspection; report builds upon DEL-03.05 field data with detailed defect analysis, condition assessment, and remediation recommendations (ASSUMPTION per typical CCTV survey workflow; Datasheet §References notes DEL-03.05 coordination).
- Verification: Procedure §Verification interdisciplinary check includes DEL-03.05 coordination confirmation to verify raw inspection data completeness and consistency; QA review verifies video file references are correct and defect locations match field inspection records.

### Quality Requirements

**QR-1: Compliance with Quality Management Plan**
- Deliverables shall comply with the project Quality Management Plan, document control expectations, and QA/QC requirements captured in Volume 2 Part 1: Employer's Requirements – General Requirements (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, details TBD).
- CCTV survey report production workflow shall follow quality procedures: specialist surveyor develops report, checker reviews defect analysis and remediation recommendations, approver signs before issue (ASSUMPTION per typical QA process; Procedure §Verification describes review steps).
- Verification: Procedure §Verification self-check, interdisciplinary check, and independent check are documented with review signatures; QA checklists are completed before issue (Procedure §Records lists QA checklists in records output).

**QR-2: Defect Analysis Accuracy and Consistency**
- Defect coding, severity assessment, and location referencing shall be accurate and consistent using standard defect coding system (PACP or equivalent per project CCTV survey standards); defect analysis shall be validated against CCTV video files and field inspection records to support remediation planning credibility (ASSUMPTION per typical CCTV survey quality requirements; rationale in Guidance §P-3 defect coding and severity assessment principle).
- Defect analysis shall be reviewed for coding consistency (defect types coded per standard system), severity assessment accuracy (severity scoring consistent with defect dimensions and impact), location referencing accuracy (chainage measurements validated, manhole references correct), and photograph/video frame capture quality (images clearly show defects, annotations identify defect features) (Procedure §Steps defect analysis execution and review; Datasheet §Attributes "Data Sources" lists CCTV inspection records and CCTV survey standards).
- Verification: Procedure §Verification self-check confirms defect coding system is correctly applied and defect analysis is accurate; interdisciplinary check validates defect severity assessment consistency; independent check confirms defect analysis supports remediation recommendations.

**QR-3: Video File and Defect Documentation Traceability**
- All defect documentation (defect coding log entries, defect photographs, video frame captures) shall reference CCTV video files with video file names, chainage locations, and inspection dates to support traceability and future investigations; video files shall be archived and accessible for future reference (Datasheet §Construction describes video file index and defect photograph organization).
- Video file index shall document all CCTV video files with file names, pipe ID coverage, chainage coverage, inspection dates, video file formats, and storage locations (digital media, cloud storage, physical media) to enable efficient video file retrieval; video quality notes (lighting, clarity, camera issues) shall be documented to explain limitations (interface linkage to video file archival system).
- Verification: Procedure §Verification QA review confirms video file references are correct and video files are accessible; defect photographs cross-reference video files for traceability; video file index is complete and accurate.

## Standards

**Governing Standards:**
- **Employer's Requirements Volume 2 Part 2: Civil & Process Mechanical Works** is the authoritative source for applicable CCTV survey procedures, defect severity criteria, and pipe condition assessment standards; specific clauses will be extracted and referenced in report as survey execution proceeds (Source: test/Volume_2_Part_2_Employers_Requirements.pdf).
- **Employer's Requirements Volume 2 Part 1: General Requirements** governs project Quality Management Plan, document control procedures, QA/QC requirements, and report review procedures (Source: test/Volume_2_Part_1_Employers_Requirements.pdf).

**Supplementary Standards (TBD pending project definition):**
- CCTV survey standards: Pipeline Assessment and Certification Program (PACP) or equivalent defect coding system, video quality standards, inspection procedures (QR-2 references CCTV survey standards; specific standard TBD from Employer's Requirements and project CCTV survey standards).
- Pipe condition assessment guidelines: Pipe condition rating systems, defect severity scoring methods, remaining useful life estimation methods (PR-1 references pipe condition assessment guidelines; TBD from industry standards and engineering judgment).
- Defect remediation methods references: Pipe repair methods, pipe lining methods, pipe replacement methods, cleaning methods (FR-4 references remediation methods; TBD from industry standards and manufacturer recommendations).

**Applicable CCTV Survey Standards (ASSUMPTION pending ER extraction):**
- PACP (Pipeline Assessment and Certification Program) or equivalent defect coding system for consistent defect type and severity coding
- Video quality standards for lighting, camera resolution, inspection speed
- Defect measurement methods for defect dimensions, joint offsets, deformations
- Pipe condition rating systems for overall pipe condition assessment (good/fair/poor or numerical rating)
- Defect severity scoring criteria based on defect type, dimensions, frequency, structural/hydraulic/environmental impact

(Note: Specific standard editions and applicable clauses to be extracted from Employer's Requirements Volume 2 Part 2 and project CCTV survey standards during survey execution; see Procedure §Prerequisites for reference material review requirement.)

## Verification

**Report Review Process:**
- **Self-check (specialist surveyor review)**: Ensures report content is complete, defect analysis is accurate, defect coding system is correctly applied, remediation recommendations are constructable; verifies all anticipated report sections (Scope list) are included; checks metadata completeness (FR-5). (Source: Procedure §Verification self-check step; Datasheet §Cross-Document Linkages references Procedure verification process.)

- **Interdisciplinary check**: Verifies coordination with related deliverables (DEL-03.01 drawings for pipe identification, DEL-03.02 specification for defect severity criteria, DEL-03.03 calculations for hydraulic impact assessment, DEL-03.04 data sheets for material properties, DEL-03.05 CCTV inspection records for raw data traceability) per IF-1 and IF-2; confirms defect severity assessment consistency; reviews environmental protection defect identification (FR-2) with environmental specialist. (Source: Procedure §Verification interdisciplinary check step; ASSUMPTION per typical CCTV survey report review process and Quality Management Plan per test/Volume_2_Part_1_Employers_Requirements.pdf.)

- **Independent check**: Confirms compliance with Employer's Requirements (Volume 2 Part 2) CCTV survey procedures and defect severity criteria; validates defect analysis accuracy and remediation recommendations appropriateness; ensures environmental protection defect identification supports OBJ-7; records results in reviewer signature blocks. (Source: Procedure §Verification independent check step; reviews tie to Specification requirements to close verification loop.)

**Defect Analysis Validation:**
- Defect coding validated against CCTV survey standards (PACP or equivalent defect coding system) for consistency and completeness (FR-3 and PR-1 requirements; Procedure §Steps defect analysis execution).
- Defect severity assessment validated against CCTV survey standards severity scoring criteria and Employer's Requirements acceptance standards (PR-1 requirement).
- Defect locations validated against DEL-03.01 drawings and DEL-03.05 CCTV inspection records for accuracy (IF-1 and IF-2 requirements).
- Hydraulic impact assessment validated against DEL-03.03 calculations for flow reduction and capacity margin evaluation (IF-1 requirement).
- Environmental impact assessment validated for containment defects and spill migration risk identification supporting OBJ-7 (FR-2 requirement).
- Results recorded in report review records and QA checklists per QR-1 (Procedure §Records lists review logs and QA checklists).

**Traceability Verification:**
- CCTV survey report references DEL-03.05 CCTV inspection records (video file names, inspection dates, surveyor names), design deliverables (DEL-03.01 drawings, DEL-03.02 specification, DEL-03.03 calculations, DEL-03.04 data sheets), and CCTV survey standards (PACP or equivalent) with document IDs and survey dates (QR-3 video file and defect documentation traceability requirement; Datasheet §Attributes "Data Sources" lists data source types).
- Video file index cross-references all video files with pipe ID coverage and storage locations to maintain traceability (QR-3 video file traceability requirement).
- Procedure §Verification QA review confirms data source references are correct and document linkages are maintained per IF-1, IF-2, and QR-3.

## Documentation

**Documented Artifacts:**
- Executive summary (survey overview, key findings, overall condition assessment, recommendations summary)
- Pipe inventory (surveyed pipes with drawing references, material types, survey status, condition ratings)
- Defect analysis (comprehensive defect coding log, severity assessment, environmental/hydraulic impact, defect photographs/video frame captures)
- Remediation recommendations (defect-by-defect recommendations, remediation methods, priority, cost implications)
- Video file index (video file names, pipe coverage, storage locations)
- Conclusions and sign-offs (overall pipe condition conclusions, limitations and assumptions, reviewer sign-offs)
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:203; detailed in Datasheet §Construction)

**Report Organization:**
- Cover page: Report title, project identification, revision history, table of contents
- Executive summary: Survey overview, key findings, overall condition assessment, recommendations summary
- Introduction: Scope, survey extent, survey methodology, applicable standards and defect coding system, abbreviations, report organization
- Pipe inventory: Tabulated list of all surveyed pipes with identification, location, survey status, condition rating
- Defect analysis: Comprehensive defect coding log with defect type, severity, location, description, environmental/hydraulic impact, photograph references
- Remediation recommendations: Defect-by-defect recommendations with remediation method, priority, cost implications, implementation timing
- Defect photographs and video frame captures: Annotated images organized by pipe ID and chainage
- Video file index: Tabulated list of all video files with file names, pipe coverage, storage locations
- Conclusions: Overall pipe condition conclusions, limitations and assumptions, reviewer sign-offs, distribution list
- Appendices: CCTV survey standards references (PACP or equivalent), defect coding legend, pipe condition rating system, surveyor qualifications, video file storage media
(Datasheet §Construction describes report organization; Procedure §Steps establishes report structure)

**Associated Quality Records:**
- Report review checklist (self-check, interdisciplinary check, independent check per Verification section)
- Specialist surveyor/checker/approver signatures
- QA checklists per Quality Management Plan requirements (QR-1)
- Report register entry documenting issue status and distribution
- Report review logs tracking review comments and resolutions
- Video file archival records (video file storage media, cloud storage access, archival duration per QR-3)
(Source: Procedure §Records quality records section; supports QR-1 compliance with Quality Management Plan)

## Pass 3 Final Notes

**Pass 3 Reconciliation Completed:**
- All cross-document linkages verified bidirectional; entity coverage confirmed; terminology consistent.
- Requirements traceability: All Specification requirements map to Procedure implementation steps and verification activities.
- TBD items align with Datasheet and have clear resolution path via Procedure prerequisites.
- Documents ready for WORKING_ITEMS sessions.
