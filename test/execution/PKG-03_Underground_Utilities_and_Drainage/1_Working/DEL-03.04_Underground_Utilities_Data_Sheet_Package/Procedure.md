# Procedure: DEL-03.04 Underground Utilities Data Sheet Package

## Purpose

Define the step-by-step process for developing, verifying, and documenting the Underground Utilities Data Sheet Package for PKG-03, ensuring that OWS equipment data, pipe material specifications, instrumentation data, and pump data are assembled consistently, reviewed rigorously, and delivered with complete quality documentation (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:211).

**Production purpose:** Enable civil specifier/data sheet preparer to produce data sheet package that substantiates underground utilities equipment and materials, supporting procurement, installation verification, and operations maintenance.

**QA purpose:** Ensure data sheet package undergoes self-check, interdisciplinary coordination check, and independent review per project Quality Management Plan requirements before issue, creating traceable QA record for procurement and regulatory compliance.

## Prerequisites

**Dependencies (coordinated externally per `_DEPENDENCIES.md`):**
- **DEL-03.01 Drawing Set**: Equipment layouts, pipe routes, instrumentation locations (required for data sheet context; Specification §IF-1).
- **DEL-03.02 Technical Specification**: Material specifications, pipe performance requirements, OWS treatment criteria (required for data sheet content; Specification §IF-1).
- **DEL-03.03 Design Calculations**: Equipment sizing results, capacity validation (required for equipment data; Specification §IF-1).

**Reference materials:**
- **Employer's Requirements Volume 2 Part 2: Civil & Process Mechanical Works** — equipment specifications, material standards, testing requirements (Source: test/Volume_2_Part_2_Employers_Requirements.pdf; Specification §Standards).
- **Employer's Requirements Volume 2 Part 1: General Requirements** — Quality Management Plan, submittal procedures (Source: test/Volume_2_Part_1_Employers_Requirements.pdf; Specification §QR-1).
- **Equipment manufacturer catalogs**: OWS equipment data, pump data (TBD; Specification §PR-1; Guidance §C-1 manufacturer data availability).
- **Material supplier specifications**: Pipe material properties, jointing systems (TBD; Specification §PR-1).
- **Project data sheet standards**: Data sheet template, format requirements (TBD; Specification §FR-4).
- **Package-level references** in `execution/PKG-03_Underground_Utilities_and_Drainage/0_References/_REFERENCE_INDEX.md`.

**Guidance alignment:**
- Review Guidance.md §Purpose to understand why data sheets matter for procurement and operations.
- Review Guidance.md §Principles (P-1 equipment/material substantiation, P-2 environmental protection equipment, P-3 data source traceability, P-4 procurement/installation coordination) before data sheet development.
- Review Guidance.md §Examples 1-4 for data sheet structure and content guidance.

**Personnel (ASSUMPTION per typical Quality Management Plan):**
- **Civil specifier/data sheet preparer**: Assembles data sheets, documents data sources, performs self-check.
- **Discipline checker**: Reviews data sheet content, verifies data accuracy, confirms coordination with related deliverables.
- **Independent reviewer (approver)**: Validates compliance with Employer's Requirements, confirms data source accuracy, signs data sheet package for issue.
- **QA coordinator**: Verifies QA documentation completeness, manages document control system issue.

## Steps

### 1. Review Scope and Confirm Data Sheet Requirements
- Review decomposition entry test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:211 and `_CONTEXT.md` to confirm anticipated data sheet types (OWS equipment, pipe materials, instrumentation, pumps).
- Review Specification.md §Scope for anticipated data sheets, exclusions, scope boundaries (Guidance §C-3 scope boundaries).
- Identify interface data sheets requiring coordination with adjacent packages (instrumentation with PKG-18 I&C, pumps with PKG-15 if applicable) per Specification §IF-1.
- **Verification checkpoint:** Data sheet preparer confirms scope understanding with discipline lead before proceeding.
- **Cross-reference:** Datasheet §Construction data sheet types; Specification §Scope; Guidance §C-3.

### 2. Collect and Document Input Data

**2.1 Collect Design Inputs from Related Deliverables:**
- Obtain DEL-03.01 Drawing Set for equipment layouts, pipe routes, instrumentation locations; document drawing revision (Specification §IF-1; Datasheet §References).
- Obtain DEL-03.02 Technical Specification for material specifications, performance requirements; document specification revision (Specification §IF-1).
- Obtain DEL-03.03 Design Calculations for equipment sizing results (OWS capacity, pump sizing if applicable); document calculation revision (Specification §IF-1).

**2.2 Collect Manufacturer and Supplier Data:**
- Obtain equipment manufacturer catalog data for OWS, pumps (if applicable), instrumentation; document manufacturer/catalog references (Specification §IF-2; Guidance §C-1 manufacturer data availability).
- Obtain material supplier specifications for pipes (HDPE, concrete, PVC, steel casing); document supplier/specification references (Specification §PR-1).
- For preliminary data sheets (budget phase), use representative manufacturer data; flag data requiring confirmation from actual equipment submittals (Guidance §C-1).

**2.3 Extract ER Requirements:**
- Extract applicable equipment/material requirements from Employer's Requirements Volume 2 Part 2; document ER clause references (Specification §Standards; Guidance §C-2 ER compliance verification).

**2.4 Document Data Sources in Introduction:**
- Prepare data sheet package introduction documenting all data sources with document IDs, revision numbers, data extraction dates; list any assumptions or preliminary data requiring confirmation (Specification §QR-2; Guidance §P-3 data source traceability).

**Verification checkpoint:** Discipline checker reviews input data completeness and data source documentation; confirms coordination with related deliverables.

**Cross-reference:** Specification §IF-1, §IF-2, §QR-2; Guidance §P-3, §C-1, §C-2; Datasheet §Attributes "Data Sources".

### 3. Establish Data Sheet Package Structure
- Structure data sheet package with sections matching Specification §Scope: Cover page, Introduction, OWS equipment data sheet, Pipe material data sheets (by type), Instrumentation data sheets, Pump data sheets (if applicable), Testing requirements summary, Appendices.
- For pipe material data sheets, organize by material type (HDPE, concrete, PVC, steel casing) per Guidance §Example 2.
- Use consistent tabular format per project data sheet template (TBD; Specification §FR-4).
- **Verification checkpoint:** Data sheet preparer confirms package structure with discipline checker before detailed data sheet development.
- **Cross-reference:** Specification §Scope and §Documentation; Datasheet §Construction package organization; Guidance §C-3, §Example 2.

### 4. Develop Detailed Data Sheets

**4.1 Scope Review** (covered in Step 1)

**4.2 Develop OWS Equipment Data Sheet:**
- Document equipment identification: Type, manufacturer/model (or "TBD - performance-based"), design basis reference (DEL-03.03 calculation).
- Document performance parameters: Design flow rate, peak flow capacity, separator volume (oil/solids/water), retention time, oil removal efficiency target, discharge water quality target (from DEL-03.03 and DEL-03.02).
- Document physical specifications: Dimensions, weight, materials of construction, access provisions (from manufacturer catalog).
- Document instrumentation: Level sensors, flow meters, oil layer thickness monitor, alarms with specifications (type, range, accuracy, output signal).
- Document electrical requirements: Power supply, connected load.
- Document testing requirements: Factory performance testing, field commissioning testing, reference to DEL-03.05 test procedures.
- Document data sources: DEL-03.03 calculation reference, manufacturer catalog reference, ER compliance clause references.
- **Verification checkpoint:** Self-check verifies OWS data completeness, validates capacity against DEL-03.03 calculations, confirms environmental protection specifications support OBJ-7 (Specification §FR-2; Guidance §P-2, §Example 1).
- **Cross-reference:** Specification §FR-2, §PR-2; Guidance §P-2, §Example 1; Datasheet §Construction OWS data sheet.

**4.3 Develop Pipe Material Data Sheets:**
- For each pipe material type (HDPE, concrete, PVC, steel casing), document:
  - Material standard (ASTM, CSA, AWWA)
  - Pipe sizes (diameter range), wall thicknesses (SDR ratings, classes)
  - Pressure ratings or stiffness ratings
  - Jointing methods (fusion welding, gaskets, solvent cement, welding)
  - Chemical resistance properties
  - Corrosion protection (coatings, cathodic protection for steel)
  - Installation requirements reference (cross-reference to DEL-03.02 per Guidance §T-3)
  - Testing requirements (hydrostatic pressure testing, joint integrity testing)
  - Data sources (material supplier specification references)
- **Verification checkpoint:** Self-check verifies material properties match DEL-03.02 specification requirements and material supplier data; confirms testing requirements are documented.
- **Cross-reference:** Specification §FR-1, §PR-1; Guidance §P-1, §T-3, §Example 2; Datasheet §Construction pipe material data sheets.

**4.4 Develop Instrumentation Data Sheets (if in scope):**
- For each instrument type (level sensors, flow meters, oil layer thickness monitors), document:
  - Sensor/meter type
  - Measurement range, accuracy
  - Output signal (4-20mA, digital, etc.)
  - Materials of construction, environmental rating
  - Calibration requirements
  - Data sources (manufacturer catalog references)
- Coordinate with PKG-18 I&C for instrumentation integration requirements per Guidance §T-4.
- **Verification checkpoint:** Self-check verifies instrumentation specifications match OWS requirements; confirms coordination with PKG-18 is documented if applicable.
- **Cross-reference:** Specification §FR-3; Guidance §T-4, §Example 3; Datasheet §Construction instrumentation data sheets.

**4.5 Develop Pump Data Sheets (if applicable):**
- If pumps are in PKG-03 scope (e.g., OWS sump pumps), document pump type/model, capacity (flow rate, head), motor power, materials, curve data, dimensions/weights, installation requirements, testing requirements, data sources.
- Coordinate with PKG-15 if detailed pump specifications are in that package per Guidance §C-3.
- **Verification checkpoint:** Self-check verifies pump specifications match design requirements; confirms scope coordination with PKG-15 if applicable.
- **Cross-reference:** Specification §Scope (pumps if applicable); Guidance §C-3 scope boundaries; Datasheet §Construction pump data sheets.

**4.6 Document Testing and Inspection Requirements:**
- Prepare testing requirements summary consolidating all testing requirements from individual data sheets.
- Include testing requirements table with columns: Equipment/Material, Test Type, Standard, Acceptance Criteria, DEL-03.05 Reference (per Guidance §Example 4).
- Cross-reference DEL-03.05 Installation and Test Records test procedures.
- **Verification checkpoint:** Self-check confirms all testing requirements are documented and cross-referenced; validates acceptance criteria against standards and ER requirements.
- **Cross-reference:** Specification §QR-3; Guidance §Example 4, §C-4; Datasheet §Construction testing requirements.

### 5. Compile Data Sheet Metadata and Prepare for Issue
- Request data sheet package document number from project document control system (TBD; Specification §FR-4).
- Set revision code to "00" for initial issue per Datasheet §Attributes.
- Complete cover page with package title, project identification, document number, revision, issue date (TBD), preparer/checker/approver signature blocks.
- Verify all data sheets are numbered consistently and cross-references are correct.
- Verify appendices are included (manufacturer catalog data, material certificates, calculation references).
- Prepare quality records templates (review checklists, review logs).
- **Verification checkpoint:** QA coordinator reviews metadata completeness before verification workflow begins.
- **Cross-reference:** Specification §FR-4, §Documentation; Datasheet §Attributes metadata fields; Guidance §C-5 operations reference.

### 6. Execute Verification Workflow

**6.1 Self-Check (Preparer Review):**
- Review data sheet content completeness for all equipment/material types per Specification §Scope.
- **6.1.1 Data completeness:** Verify all required data fields are populated (equipment specs, material properties, performance parameters, testing requirements).
- **6.1.2 Data accuracy verification:** Validate data against source documents (manufacturer catalogs, supplier specifications, DEL-03.03 calculations, DEL-03.02 specification); confirm data extraction is accurate.
- **6.1.3 Data source documentation:** Verify all data sources are correctly referenced with document IDs, catalog numbers, revision numbers per Specification §QR-2 and Guidance §P-3.
- **6.1.4 Metadata completeness:** Confirm document number, revision, preparer/checker/approver names, data sources list are correctly populated.
- **6.1.5 Cross-reference verification:** Check cross-references to related deliverables (DEL-03.01/02/03/05) are correct.
- **6.1.6 Testing requirements:** Confirm testing requirements are documented for all equipment/materials and cross-referenced to DEL-03.05.
- **Self-check documentation:** Data sheet preparer signs/dates self-check checklist, documents any corrections made.
- **Cross-reference:** Specification §Verification self-check; Specification §QR-2; Guidance §P-3.

**6.2 Interdisciplinary Check (Coordination Review):**
- **6.2.1 DEL-03.01 Drawing Set coordination:** Verify equipment sizes/locations match drawings (Specification §IF-1).
- **6.2.2 DEL-03.02 Technical Specification coordination:** Verify material properties and performance parameters match specification requirements (Specification §IF-1).
- **6.2.3 DEL-03.03 Design Calculations coordination:** Verify equipment capacities and sizing parameters match calculation results (Specification §IF-1).
- **6.2.4 DEL-03.05 Installation and Test Records coordination:** Verify testing requirements support installation test procedures (Specification §IF-1; Guidance §C-4).
- **6.2.5 PKG-18 I&C coordination:** Verify instrumentation scope boundaries and coordination requirements if applicable (Guidance §T-4).
- **6.2.6 Environmental protection review:** Review OWS equipment data sheet with process team or environmental specialist to confirm OBJ-7 compliance (Specification §FR-2).
- **Interdisciplinary check documentation:** Discipline checker signs/dates interdisciplinary review log, documents coordination confirmation or issues.
- **Cross-reference:** Specification §Verification interdisciplinary check; Specification §IF-1; Guidance §P-4, §C-4.

**6.3 Independent Check (Approver Review):**
- **6.3.1 ER compliance:** Verify data sheets comply with Employer's Requirements Volume 2 Part 2 equipment/material requirements (Specification §Verification; Guidance §C-2).
- **6.3.2 Data source validation:** Validate equipment specifications and material properties against manufacturer/supplier sources; confirm data accuracy (Specification §QR-2).
- **6.3.3 Environmental protection validation:** Validate OWS equipment specifications support OBJ-7 Environmental Protection; confirm treatment capacity and discharge compliance (Specification §FR-2, §PR-2).
- **6.3.4 Testing requirements validation:** Verify testing requirements comply with applicable standards and ER requirements (Specification §QR-3).
- **6.3.5 QA documentation review:** Review self-check checklist and interdisciplinary review log to confirm all verification activities are completed (Specification §QR-1).
- **Independent check documentation:** Independent reviewer signs/dates independent check review form and data sheet package cover page approver signature block; documents review comments and confirms resolutions.
- **Cross-reference:** Specification §Verification independent check; Specification §Standards, §PR-2, §QR-3; Guidance §C-2.

### 7. Issue Data Sheet Package into Document Control System
- Finalize data sheet package issue date on cover page.
- Compile data sheet package PDF (cover page, introduction, all data sheets, testing summary, appendices).
- Submit data sheet package to document control system with metadata (document number, revision, title, discipline, package, deliverable ID, preparer/checker/approver names, issue date).
- Obtain document control register confirmation of issue; verify distribution per distribution matrix.
- File quality records (self-check checklist, interdisciplinary review log, independent check review form, QA checklists) per Quality Management Plan archival requirements.
- **Issue completion confirmation:** Document control coordinator confirms data sheet package is issued into document control system.
- **Cross-reference:** Specification §FR-4, §Documentation; Datasheet §Conditions data sheet control; Guidance §C-5 procurement use and operations reference.

## Verification

**Verification workflow summary:**
1. **Self-check (preparer review):** Data sheet preparer verifies data completeness, data accuracy, data source documentation, metadata completeness, cross-references, testing requirements per Step 6.1 activities; documents review using self-check checklist.
2. **Interdisciplinary check (coordination review):** Discipline checker verifies coordination with related deliverables (DEL-03.01/02/03/05) and adjacent packages (PKG-18), and reviews environmental protection data sheet adequacy per Step 6.2 activities; documents review using interdisciplinary review log.
3. **Independent check (approver review):** Independent reviewer validates compliance with Employer's Requirements, confirms data source accuracy, reviews environmental protection specifications, validates testing requirements, and reviews QA documentation per Step 6.3 activities; documents review by signing data sheet package for issue.

**Verification traceability:** All verification activities documented in quality records; verification links data sheet package to Specification requirements.

**Cross-reference:** Specification §Verification; Specification §QR-1; Guidance §C-4; Datasheet §Cross-Document Linkages.

## Records

**Data sheet deliverables (primary outputs):**
- **Data sheet package PDF**: OWS equipment data sheet, pipe material data sheets, instrumentation data sheets, pump data sheets (if applicable), testing requirements summary, organized per Step 3 structure (Source: Specification §Documentation; Datasheet §Construction).
- **Appendices**: Manufacturer catalog data, material certificates, calculation references archived with data sheet package.

**Quality records (supporting documentation):**
- **Self-check checklist**: Documents preparer review completion per Step 6.1 (Specification §Verification).
- **Interdisciplinary review log**: Documents coordination check completion per Step 6.2 (Specification §Verification).
- **Independent check review form**: Documents approver review completion per Step 6.3 (Specification §Verification).
- **QA checklists**: Per Quality Management Plan requirements (Specification §QR-1).
- **Data sheet register entry**: Document control system record (Specification §FR-4).
- **Data sheet review logs**: Tracks review comments and resolutions.
- **Data source verification records**: Manufacturer catalog references, supplier specification confirmations (Specification §QR-2).

**Records retention:** All data sheet deliverables and quality records archived per project document control and Quality Management Plan requirements.

**Cross-reference:** Specification §Documentation quality records; Specification §QR-1; Datasheet §References quality records; Guidance §C-4, §C-5.

## Pass 3 Final Notes

**Pass 3 Reconciliation Completed:**
- All cross-document linkages verified; steps linked to requirements; entity coverage confirmed; terminology consistent.
- Documents ready for WORKING_ITEMS sessions.
