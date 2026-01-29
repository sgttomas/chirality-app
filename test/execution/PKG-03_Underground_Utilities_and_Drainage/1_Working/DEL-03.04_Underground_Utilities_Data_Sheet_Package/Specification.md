# Specification: DEL-03.04 Underground Utilities Data Sheet Package

## Scope

This specification governs the development of the **Underground Utilities Data Sheet Package** for **PKG-03 Underground Utilities & Drainage**. The data sheets define equipment specifications and material properties for OWS, pipes, instrumentation, and pumps to substantiate design drawings and technical specifications per the Employer's Requirements (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:211).

**Anticipated artifacts within this scope:**
- OWS equipment data sheet (equipment type, treatment capacity, separator volume, retention time, performance parameters, instrumentation, testing requirements)
- Pipe material data sheets (HDPE, concrete, PVC, steel casing: material properties, sizes, jointing methods, chemical resistance, testing requirements)
- Instrumentation data sheets (level sensors, flow meters, oil layer thickness monitors: specifications, ranges, calibration requirements)
- Pump data sheets if applicable (capacity, head, motor power, materials, testing requirements)

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:211; elaborated in Datasheet §Construction for data sheet package organization)

**Exclusions:**
- Detailed installation procedures and testing protocols are documented in DEL-03.05 Installation and Test Records (not in this data sheet package; data sheets provide equipment/material specifications only).
- Process equipment and above-ground structures are outside PKG-03 scope per Scope Focus (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47).

## Requirements

### Functional Requirements

**FR-1: Comprehensive Equipment and Material Substantiation**
- Provide complete equipment specifications and material properties for OWS, pipes, instrumentation, and pumps to substantiate underground utilities design described in the decomposition (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:211).
- Data sheets shall include sufficient detail for procurement teams to prepare purchase orders, suppliers to prepare submittals, and QA/QC to verify conformance (ASSUMPTION per typical data sheet function; rationale in Guidance §Purpose).
- Verification: Procedure §Verification self-check confirms all data sheet sections are complete; interdisciplinary check verifies coordination with DEL-03.02 specification requirements.

**FR-2: Environmental Protection Equipment Substantiation**
- Document OWS equipment specifications, treatment performance parameters, and discharge monitoring instrumentation to support **OBJ-7 Environmental Protection** objectives for PKG-03 (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786).
- OWS data sheet shall specify treatment capacity, retention volume, treatment performance (oil removal efficiency), discharge water quality targets, and instrumentation (level sensors, flow meters, oil layer thickness monitors, alarms) to support environmental protection system adequacy (rationale in Guidance §P-2; operational context in Datasheet §Conditions).
- Verification: Procedure §Steps OWS data sheet development requirement; Procedure §Verification independent check confirms OWS equipment specifications meet environmental performance criteria.

**FR-3: Instrumentation Substantiation**
- Document instrumentation specifications for underground utilities monitoring and control to support operational and environmental protection requirements (Dependencies: coordination with PKG-18 I&C if detailed instrumentation specifications are in that package; NOT_TRACKED per `_DEPENDENCIES.md`).
- Data sheets shall specify instrument types, measurement ranges, accuracy, output signals, environmental ratings, calibration requirements to support procurement and installation (Datasheet §Construction lists instrumentation data sheets).
- Verification: Procedure §Verification interdisciplinary check includes coordination review with PKG-18 I&C if applicable to confirm instrumentation scope boundaries.

**FR-4: Document Metadata and Data Sheet Control**
- Ensure data sheet metadata (numbering, revision, preparer/checker/approver signatures, data sources identification) aligns with the Datasheet attributes and project document control expectations (Datasheet §Attributes lists metadata fields; this requirement ensures data sheets implement those fields correctly).
- Data sheet numbering scheme shall follow project document control procedures; initial issue revision is "00" per Datasheet §Attributes (TBD: specific numbering format pending project document control register definition per Procedure §Prerequisites).
- Verification: Procedure §Steps metadata compilation; Procedure §Verification QA review confirms metadata completeness before document control system release.

### Performance Requirements

**PR-1: Equipment and Material Performance**
- Conform to the equipment performance, material properties, and design expectations described in the Employer's Requirements Volume 2 Part 2: Civil & Process Mechanical Works (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, specific clauses TBD).
- Equipment specifications (OWS capacity, pump performance, instrumentation ranges) shall support design calculations documented in DEL-03.03 Design Calculations; material properties (pipe strength, chemical resistance) shall support design requirements documented in DEL-03.02 Technical Specification (interface linkage to calculations and specification deliverables; Datasheet §Construction describes data sheet content).
- Verification: Data sheet specifications validated against DEL-03.03 calculation results and DEL-03.02 specification requirements; Procedure §Verification independent check confirms compliance with Employer's Requirements.

**PR-2: Facility Throughput and Containment Support**
- Ensure data sheets support the permitted throughput (1,000,000 MT/a canola oil), storage capacity (45,000 MT in three tanks), and containment expectations for Phase 1 as described in the decomposition's project overview parameters (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md, Project Overview section; Datasheet §Conditions references these parameters).
- OWS equipment data sheet shall specify treatment capacity and retention volume supporting anticipated runoff volumes and spill containment requirements from DEL-03.03 calculations (interface linkage; Datasheet §Construction notes OWS equipment data).
- Verification: Procedure §Steps OWS data sheet development validates equipment capacity against DEL-03.03 sizing calculations; Procedure §Verification interdisciplinary check includes process team review of containment adequacy.

**PR-3: Design Life and Environmental Conditions**
- Data sheet specifications shall reflect design life, temperature range, chemical exposure, corrosion environment, and other environmental design parameters from the civil design brief and Employer's Requirements (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD; Datasheet §Conditions lists these as TBD pending ER extraction).
- Material properties (pipe chemical resistance, coating systems, corrosion protection) shall be compatible with site environmental conditions and service requirements (ASSUMPTION: typical civil material selection considerations; specific values TBD from Employer's Requirements and DEL-03.02).
- Verification: Procedure §Verification independent check confirms material properties match environmental design parameters from civil design brief and Employer's Requirements.

### Interface Requirements

**IF-1: Coordination with Related PKG-03 Deliverables**
- Coordinate data sheet content with related PKG-03 deliverables to ensure consistency:
  - **DEL-03.01 Drawing Set**: Ensure equipment sizes, locations, and configurations in data sheets match drawing layouts (Datasheet §References notes drawings provide context).
  - **DEL-03.02 Technical Specification**: Ensure material properties and performance parameters in data sheets match specification requirements; data sheets provide detailed substantiation for specification claims (Datasheet §References notes specification provides performance targets).
  - **DEL-03.03 Design Calculations**: Ensure equipment capacities and sizing parameters in data sheets match calculation results and validate equipment selection adequacy (Datasheet §References notes calculations provide sizing basis).
  - **DEL-03.05 Installation and Test Records**: Provide testing requirements and acceptance criteria in data sheets to support installation testing protocols (rationale in Guidance §C-4 QA coordination with installation records).
- Verification: Procedure §Verification interdisciplinary check confirms data sheet content aligns with related deliverable content; Procedure §Steps input data collection ensures upstream deliverables are reviewed before data sheet development.

**IF-2: Coordination with Suppliers and Manufacturers**
- Data sheets shall be based on manufacturer catalog data and supplier specifications; coordinate with equipment suppliers and material manufacturers to obtain accurate data and confirm product availability (Dependencies: supplier coordination managed through procurement workflows; NOT_TRACKED per `_DEPENDENCIES.md`).
- Data sheet format shall support submittal preparation by suppliers; include clear identification of required submittal data (manufacturer data sheets, test reports, certificates) (ASSUMPTION per typical data sheet package use for procurement and submittals).
- Verification: Procedure §Verification self-check confirms data sources (manufacturer catalogs, supplier specifications) are correctly referenced; QA review verifies supplier data accuracy before data sheet finalization.

### Quality Requirements

**QR-1: Compliance with Quality Management Plan**
- Deliverables shall comply with the project Quality Management Plan and document control expectations captured in Volume 2 Part 1: Employer's Requirements – General Requirements (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, details TBD).
- Data sheet production workflow shall follow quality procedures: preparer develops data sheets, checker reviews content and data sources, approver signs before issue (ASSUMPTION per typical QA process; Procedure §Verification describes review steps).
- Verification: Procedure §Verification self-check, interdisciplinary check, and independent check are documented with review signatures; QA checklists are completed before issue (Procedure §Records lists QA checklists in records output).

**QR-2: Data Source Traceability and Accuracy**
- Data sheets shall document all data sources (equipment manufacturer catalogs, material supplier specifications, DEL-03.03 calculation results, DEL-03.02 specification requirements) with document references and data extraction dates to support independent verification and future procurement (ASSUMPTION per typical data sheet documentation requirements; rationale in Guidance §P-3 data source traceability principle).
- Material property data and equipment performance parameters shall be verified against manufacturer catalog data or material standards; any deviations or assumptions shall be documented (Procedure §Steps input data collection and verification; Datasheet §Attributes "Data Sources" lists data source types).
- Verification: Procedure §Verification self-check confirms data sources are documented and data accuracy is verified; independent check validates data against manufacturer/supplier sources.

**QR-3: Testing and Inspection Requirements Documentation**
- Data sheets shall document testing and inspection requirements for equipment and materials (hydrostatic pressure testing for pipes, OWS performance testing, instrumentation calibration, material conformance testing) to support quality assurance and commissioning (Datasheet §Construction describes testing requirements documentation).
- Testing requirements shall reference applicable standards and acceptance criteria from Employer's Requirements Volume 2 Part 2 and DEL-03.02 Technical Specification (interface linkage to testing standards).
- Verification: Procedure §Verification QA review confirms testing requirements are documented and cross-referenced to DEL-03.05 Installation and Test Records; independent check validates testing requirements compliance with standards.

## Standards

**Governing Standards:**
- **Employer's Requirements Volume 2 Part 2: Civil & Process Mechanical Works** is the authoritative source for applicable equipment specifications, material standards, and testing requirements; specific clauses will be extracted and referenced in data sheets as design details mature (Source: test/Volume_2_Part_2_Employers_Requirements.pdf).
- **Employer's Requirements Volume 2 Part 1: General Requirements** governs project Quality Management Plan, document control procedures, QA/QC requirements, and submittal procedures (Source: test/Volume_2_Part_1_Employers_Requirements.pdf).

**Supplementary Standards (TBD pending project definition):**
- Equipment manufacturer catalogs and specifications: OWS equipment data, pump data, instrumentation specifications (PR-1 references manufacturer data; to be obtained from equipment suppliers per Procedure §Prerequisites).
- Material supplier specifications: Pipe material properties, jointing systems, coating specifications (PR-1 references material data; to be obtained from material suppliers).
- Material standards: ASTM, CSA, AWWA standards for pipe materials, pressure ratings, jointing methods (QR-2 references material standards; specific standards TBD from DEL-03.02 Technical Specification).
- Data sheet format template: Project data sheet template, metadata requirements, content organization (FR-4 references data sheet format; TBD pending project data sheet standards).

**Applicable Codes and Standards (ASSUMPTION pending ER extraction):**
- ASTM standards for pipe materials (HDPE, PVC, concrete pipe, steel pipe)
- CSA standards for pipe installations and jointing
- AWWA standards for water/wastewater equipment
- Environmental regulations for oil-water separator performance and discharge water quality (supports OBJ-7 Environmental Protection per FR-2)
- Electrical codes for instrumentation and pump electrical requirements

(Note: Specific standard editions and applicable clauses to be extracted from Employer's Requirements Volume 2 Part 2 during design development; see Procedure §Prerequisites for reference material review requirement.)

## Verification

**Design Review Process:**
- **Self-check (preparer review)**: Ensures data sheet content is complete, data sources are documented, equipment/material specifications match design requirements; verifies all anticipated data sheet types (Scope list) are included; checks metadata completeness (FR-4). (Source: Procedure §Verification self-check step; Datasheet §Cross-Document Linkages references Procedure verification process.)

- **Interdisciplinary check**: Verifies coordination with related deliverables (DEL-03.01 drawings, DEL-03.02 specification, DEL-03.03 calculations) per IF-1; confirms data sheet content supports procurement and installation; reviews OWS equipment data sheet (FR-2) with process team. (Source: Procedure §Verification interdisciplinary check step; ASSUMPTION per typical data sheet review process and Quality Management Plan per test/Volume_2_Part_1_Employers_Requirements.pdf.)

- **Independent check**: Confirms compliance with Employer's Requirements (Volume 2 Part 2); validates equipment specifications and material properties against manufacturer/supplier data; ensures environmental design parameters (PR-3) match Employer's Requirements; records results in reviewer signature blocks. (Source: Procedure §Verification independent check step; reviews tie to Specification requirements to close verification loop.)

**Data Accuracy Verification:**
- Equipment performance data (OWS capacity, pump curves, instrumentation ranges) validated against manufacturer catalog data and DEL-03.03 calculation results (FR-2 and PR-1 requirements; Procedure §Steps data verification).
- Material property data (pipe strength, chemical resistance, pressure ratings) validated against material supplier specifications and material standards (PR-1 and QR-2 requirements).
- Testing requirements validated against applicable standards and DEL-03.02 specification requirements (QR-3 requirement).
- Results recorded in data sheet review records and QA checklists per QR-1 (Procedure §Records lists data sheet review logs and QA checklists).

**Traceability Verification:**
- Data sheets reference manufacturer catalogs, supplier specifications, DEL-03.03 calculations, DEL-03.02 specification with document IDs and data extraction dates (QR-2 data source traceability requirement; Datasheet §Attributes "Data Sources" lists data source types).
- Data sheet testing requirements cross-reference DEL-03.05 Installation and Test Records to maintain traceability (IF-1 coordination with related deliverables).
- Procedure §Verification QA review confirms data source references are correct and document linkages are maintained per IF-1 and QR-2.

## Documentation

**Documented Artifacts:**
- OWS equipment data sheet (equipment specifications, treatment performance, instrumentation, testing requirements)
- Pipe material data sheets (HDPE, concrete, PVC, steel casing: material properties, jointing methods, testing requirements)
- Instrumentation data sheets (level sensors, flow meters, specifications, calibration requirements)
- Pump data sheets if applicable (capacity, performance curves, testing requirements)
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:211; detailed in Datasheet §Construction)

**Data Sheet Package Organization:**
- Cover page: Package title, project identification, revision history, table of contents
- Introduction: Scope, data sources, applicable standards, abbreviations
- OWS equipment data sheet section
- Pipe material data sheets section (organized by material type)
- Instrumentation data sheets section
- Pump data sheets section (if applicable)
- Testing and inspection requirements summary
- Appendices: Manufacturer catalog data, material certificates, calculation references
(Datasheet §Construction describes data sheet package organization; Procedure §Steps establishes package structure)

**Associated Quality Records:**
- Data sheet review checklist (self-check, interdisciplinary check, independent check per Verification section)
- Preparer/checker/approver signatures
- QA checklists per Quality Management Plan requirements (QR-1)
- Data sheet register entry documenting issue status and distribution
- Data sheet review logs tracking review comments and resolutions
- Data source verification records (manufacturer catalog references, supplier specification confirmations per QR-2)
(Source: Procedure §Records quality records section; supports QR-1 compliance with Quality Management Plan)

## Pass 3 Final Notes

**Pass 3 Reconciliation Completed:**
- All cross-document linkages verified bidirectional; entity coverage confirmed; terminology consistent.
- Requirements traceability: All Specification requirements map to Procedure implementation steps and verification activities.
- TBD items align with Datasheet and have clear resolution path via Procedure prerequisites.
- Documents ready for WORKING_ITEMS sessions.
