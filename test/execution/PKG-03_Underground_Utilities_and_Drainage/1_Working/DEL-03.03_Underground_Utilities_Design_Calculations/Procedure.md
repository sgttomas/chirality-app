# Procedure: DEL-03.03 Underground Utilities Design Calculations

## Purpose

Define the step-by-step process for developing, verifying, and documenting the Underground Utilities Design Calculations package for PKG-03, ensuring that storm drainage hydraulics, OWS sizing, duct bank capacity analysis, and trenchless crossing structural calculations are executed consistently, reviewed rigorously, and delivered with complete quality documentation (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:210).

**Production purpose:** Enable civil calculation engineer to produce calculation package that demonstrates hydraulic performance, environmental protection compliance (OBJ-7), and structural adequacy for underground utilities design, supporting DEL-03.01 Drawing Set and DEL-03.02 Technical Specification with quantitative engineering basis.

**QA purpose:** Ensure calculation package undergoes self-check, interdisciplinary coordination check, and independent review per project Quality Management Plan requirements before issue, creating traceable QA record for regulatory compliance verification and future design modifications.

## Prerequisites

**Dependencies (coordinated externally per `_DEPENDENCIES.md`):**
- **PKG-02 Site Grading**: Site grading plans, finished grade elevations, drainage flow directions, coordinate system definition (required for storm drainage hydraulic calculations and drainage area delineation; Specification §IF-2 coordination with PKG-02).
- **PKG-17 Electrical Power Distribution**: Cable schedules, cable sizes, electrical load information (required for duct bank capacity fill factor analysis; Specification §IF-2 coordination with PKG-17).
- **DEL-03.01 Drawing Set**: Pipe alignments, invert elevations, slopes, OWS location, duct bank routing, trenchless crossing alignments (required as geometric basis for calculations; Specification §IF-1 coordination with DEL-03.01).
- **DEL-03.02 Technical Specification**: Material properties, pipe performance requirements, OWS treatment criteria (required as design constraints and performance targets for calculations; Specification §IF-1 coordination with DEL-03.02).

**Reference materials (to be obtained before calculation begins):**
- **Employer's Requirements Volume 2 Part 2: Civil & Process Mechanical Works** — design criteria, storm drainage standards, OWS performance requirements, structural loading criteria (Source: test/Volume_2_Part_2_Employers_Requirements.pdf; Specification §Standards governing standard).
- **Employer's Requirements Volume 2 Part 1: General Requirements** — Quality Management Plan, document control procedures, QA/QC requirements, calculation standards (Source: test/Volume_2_Part_1_Employers_Requirements.pdf; Specification §QR-1).
- **Civil design brief** — design storm return period, runoff coefficients, design life, seismic design category, temperature range, hydraulic design criteria (TBD; Specification §PR-3 references; Guidance §C-1 design criteria availability).
- **Geotechnical report** — soil properties, bearing capacity, groundwater levels, seismic site class (TBD; Specification §PR-3 references; required for trenchless crossing structural analysis per Step 4.4).
- **Rainfall intensity-duration-frequency (IDF) curves** — design storm rainfall intensities for hydraulic calculations (TBD; to be sourced from local jurisdiction, Metro Vancouver, or civil design brief; required for storm drainage calculations per Step 4.1).
- **Project calculation standards** — calculation format template, preparer/checker/approver requirements, revision control procedures, approved calculation software list (TBD; Specification §FR-4 and §QR-1 reference).
- **Approved calculation software** — hydraulic modeling software (TBD: typical tools StormCAD, HydroCAD, HEC-RAS), software validation documentation (Specification §QR-3 software validation requirements).
- **Package-level references** in `execution/PKG-03_Underground_Utilities_and_Drainage/0_References/_REFERENCE_INDEX.md` — to be populated with project-specific standards and data sources.

**Guidance alignment:**
- Review Guidance.md §Purpose to understand why calculations matter for design validation and regulatory compliance.
- Review Guidance.md §Principles (P-1 hydraulic performance verification, P-2 environmental protection performance verification, P-3 calculation assumptions traceability, P-4 coordination with design deliverables) to understand engineering rationale before calculation development.
- Review Guidance.md §Considerations (C-1 design criteria availability, C-2 ER extraction, C-3 calculation structure and scope boundaries, C-4 QA coordination, C-5 engineering record) to understand practical considerations affecting calculation approach.
- Review Guidance.md §Examples 1-4 for calculation structure and methodology guidance specific to each calculation type.

**Personnel (ASSUMPTION per typical Quality Management Plan):**
- **Civil calculation engineer (preparer)**: Develops calculations, documents methodology and assumptions, performs self-check, responsible for calculation accuracy.
- **Discipline checker**: Reviews calculation logic, verifies results, confirms methodology appropriateness, performs spot-checks of critical calculations.
- **Independent reviewer (approver)**: Validates compliance with Employer's Requirements and civil standards, confirms design criteria application, signs calculation package for issue.
- **QA coordinator**: Verifies QA documentation completeness, confirms review checklist completion, manages document control system issue.

## Steps

### 1. Review Scope and Confirm Calculation Requirements

**Objective:** Understand calculation package scope, identify anticipated calculation types, confirm alignment with decomposition and Specification requirements before calculation development begins.

**Activities:**
- Review decomposition entry test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:210 to confirm DEL-03.03 scope and anticipated artifacts (storm drainage hydraulics, OWS sizing, duct bank capacity, trenchless crossing structural calculations).
- Review `_CONTEXT.md` anticipated artifacts list to confirm calculation types expected in package.
- Review Specification.md §Scope to understand anticipated calculation types, exclusions, and scope boundaries (Guidance §C-3 calculation structure and scope boundaries consideration emphasizes avoiding scope creep).
- Identify interface calculations requiring coordination with adjacent packages (duct bank capacity coordinates with PKG-17 electrical cable sizing; storm drainage coordinates with PKG-02 site grading) per Specification §IF-2.
- Document scope understanding and any scope clarifications required in calculation planning notes.

**Verification checkpoint:** Calculation engineer confirms understanding of scope and calculation types with discipline lead before proceeding; scope clarifications documented.

**Cross-reference:** Datasheet §Construction calculation package types; Specification §Scope anticipated calculation types and exclusions; Guidance §C-3 calculation structure and scope boundaries.

### 2. Collect and Document Input Data

**Objective:** Assemble all required design criteria, site data, reference documents, and upstream deliverable information needed for calculation development; document data sources to support traceability and independent verification.

**2.1 Collect Geometric and Design Inputs from Related Deliverables:**
- Obtain DEL-03.01 Drawing Set (approved for design or latest revision available) for pipe alignments, invert elevations, slopes, OWS location, duct bank routing, trenchless crossing alignments; document drawing revision and date obtained (Specification §IF-1 coordination with DEL-03.01; Datasheet §References notes drawings provide geometric basis).
- Obtain DEL-03.02 Technical Specification for material properties (pipe roughness coefficients, structural capacities), pipe performance requirements, OWS treatment criteria; document specification revision and date obtained (Specification §IF-1 coordination with DEL-03.02).
- Obtain DEL-03.04 Data Sheet Package (if available) for equipment performance parameters (OWS capacity, pump curves, instrumentation ranges); document data sheet revision if used in calculations (Specification §IF-1 coordination with DEL-03.04).
- Obtain PKG-02 site grading plans for finished grade elevations, drainage flow directions, site coordinate system definition, vertical datum; document package deliverable ID and revision (Specification §IF-2 coordination with PKG-02; required for storm drainage calculations per Guidance §Example 1).
- Obtain PKG-17 cable schedules for cable sizes, cable quantities, conduit assignments (required for duct bank capacity fill factor analysis per Specification §IF-2 and Guidance §T-4); document package deliverable ID, revision, and coordination date.

**2.2 Collect Design Criteria and Standards:**
- Extract applicable design criteria from Employer's Requirements Volume 2 Part 2: design storm return period, hydraulic capacity factors, OWS treatment efficiency targets, structural load factors, seismic design parameters; document ER clause references and data extraction date (Specification §Standards governing standard; Guidance §C-2 ER extraction and interpretation consideration).
- Obtain civil design brief for runoff coefficients, design life, temperature range, seismic design category, hydraulic design criteria; document civil design brief document ID and revision (Specification §PR-3 design life and environmental conditions; Guidance §C-1 design criteria availability consideration).
- Obtain geotechnical report for soil properties (unit weight, friction angle, cohesion), bearing capacity, groundwater levels, seismic site class; document geotechnical report document ID, revision, and boring locations relevant to trenchless crossings (Specification §PR-3; required for Step 4.4 trenchless crossing calculations).
- Obtain rainfall IDF curves for design storm rainfall intensities; document data source (local jurisdiction, Metro Vancouver, or civil design brief reference); verify design storm return period matches ER requirements (required for Step 4.1 storm drainage calculations per Guidance §Example 1).
- Identify applicable codes and standards (NBC, BCBC, CSA standards, electrical codes for duct bank fill factors); document code editions and applicable clauses (Specification §Standards applicable codes).

**2.3 Identify Conservative Assumptions for Missing Data:**
- For any design criteria not yet available (e.g., civil design brief pending, geotechnical investigation incomplete), identify conservative assumptions to enable calculation to proceed; document assumption justification and future validation requirements (Guidance §C-1 design criteria availability and data gaps consideration; Guidance §T-1 calculation detail vs conservative assumptions trade-off).
- Flag calculations requiring revision when specific data becomes available; coordinate with design team to prioritize data acquisition for critical design decisions.

**2.4 Document Data Sources in Calculation Input Summary:**
- Prepare calculation input data summary section documenting all data sources with document IDs, revision numbers, data extraction dates; list all assumptions with justification; reference applicable standards and codes (Specification §QR-2 calculation methodology documentation requirement; Guidance §P-3 calculation assumptions and data source traceability principle; Datasheet §Construction input data summary content).

**Verification checkpoint:** Discipline checker reviews input data summary to confirm all required data sources are identified and documented; verifies conservative assumptions are appropriate for missing data; confirms coordination with adjacent packages (PKG-02, PKG-17) is documented.

**Cross-reference:** Specification §IF-1 and §IF-2 coordination with related deliverables and adjacent packages; Guidance §C-1 design criteria availability, §C-2 ER extraction, §P-3 data source traceability; Datasheet §Attributes "Design Criteria Sources".

### 3. Establish Calculation Package Structure

**Objective:** Organize calculation package into sections matching Specification scope and anticipated calculation types to support scope control and enable efficient review.

**3.1 Define Calculation Package Organization:**
- Structure calculation package with sections matching Specification §Scope anticipated calculation types:
  - Cover page: Calculation title, project identification, preparer/checker/approver signature blocks, revision history table
  - Input data summary: Design criteria, site parameters, rainfall data, soil properties, applicable standards reference list (prepared in Step 2.4)
  - Storm drainage hydraulic calculations section
  - OWS sizing calculations section
  - Duct bank capacity calculations section
  - Trenchless crossing structural calculations section
  - Results summary and conclusions
  - Appendices: Software output files, manufacturer data sheets (from DEL-03.04), standard calculation references, drainage area sketches
- Organize sections in logical sequence supporting review workflow; use consistent numbering and formatting per project calculation standards (TBD; Specification §FR-4 calculation control).

**3.2 Establish Calculation Section Structure:**
- For each calculation section, establish subsection structure: introduction/objective, methodology description, input data, analysis/calculations, results, verification/checks (ASSUMPTION per typical calculation structure; Guidance §C-5 engineering record and future reference consideration emphasizes clear structure for future review).
- Include executive summary table at beginning of calculation package showing key results (pipe sizes, flows, capacities, margins) to enable quick review without detailed analysis review (Guidance §C-5 engineering record).

**Verification checkpoint:** Calculation engineer confirms calculation structure with discipline checker before detailed calculation development; structure alignment with Specification §Scope verified.

**Cross-reference:** Specification §Scope anticipated calculation types; Specification §Documentation calculation package organization; Datasheet §Construction calculation package organization structure; Guidance §C-3 calculation structure and scope boundaries.

### 4. Develop Detailed Calculations

**Objective:** Execute engineering calculations for each calculation type (storm drainage, OWS, duct banks, trenchless crossings) using appropriate methodologies, documenting assumptions and results to support design verification and independent review.

**4.1 Develop Storm Drainage Hydraulic Calculations:**
- **Drainage area delineation:** Identify contributing drainage areas for each inlet/catch basin using site grading plans from PKG-02 and facility layout; calculate drainage area sizes; determine flow paths and time of concentration; document drainage area assumptions and prepare drainage area sketches for calculation appendix (Guidance §Example 1 storm drainage calculation structure step 2).
- **Runoff calculation:** Apply rational method (Q = CiA) for drainage areas < 80 hectares or hydrograph analysis for larger areas per civil design brief requirements; calculate peak runoff for each inlet based on rainfall intensity (from IDF curves for time of concentration), runoff coefficient (from civil design standards), and drainage area; prepare runoff calculation table summarizing results for each inlet (Guidance §Example 1 step 3; Guidance §P-1 hydraulic performance and capacity verification principle).
- **Pipe sizing:** Size storm drain pipes for calculated flows using Manning equation or hydraulic modeling software; verify pipe velocities within acceptable range (minimum 0.6 m/s for self-cleaning, maximum 3-5 m/s to prevent erosion per civil design standards); document pipe size selection rationale.
- **Hydraulic grade line analysis:** Develop hydraulic grade line analysis using hydraulic modeling software (e.g., StormCAD) or step-backwater calculation method; verify hydraulic grade lines remain below inlet elevations and ground surface to prevent flooding; identify any capacity deficiencies requiring design revision (Guidance §Example 1 step 4).
- **Results summary:** Prepare results summary table listing pipe sizes, slopes, flows, velocities, hydraulic grade lines for each pipe segment; cross-reference DEL-03.01 Drawing Set sheet numbers for each pipe; flag any design revisions required (Guidance §Example 1 step 5).
- **Software output documentation:** Include hydraulic model setup description, model input file, model output report in calculation appendix; document software identification, version, validation status per Specification §QR-3 (Guidance §Example 1 step 6).

**Verification checkpoint:** Self-check verifies runoff calculations, pipe sizing logic, hydraulic grade line analysis; confirms results are reasonable and consistent with design criteria; validates software model setup.

**Cross-reference:** Specification §FR-1 comprehensive hydraulic analysis; Specification §PR-1 hydraulic performance; Datasheet §Construction storm drainage calculations content; Guidance §P-1 and §Example 1.

**4.2 Develop OWS Sizing Calculations:**
- **Contributing drainage area determination:** Identify paved areas and process areas draining to OWS using site layout and drainage flow paths; calculate contributing area size; determine runoff characteristics (runoff coefficient, time of concentration) (Guidance §Example 2 OWS sizing methodology step 1).
- **Peak runoff flow rate calculation:** Calculate peak runoff using rational method for design storm event (per ER requirements or environmental permit); consider both rainfall runoff and potential process spill scenarios (e.g., tank overfill, loading arm release); use conservative assumption for peak flow (maximum of storm runoff or spill release rate) (Guidance §Example 2 step 2; Guidance §P-2 environmental protection performance verification principle).
- **Separator volume sizing:** Apply empirical sizing equation (e.g., API separator sizing equation or manufacturer sizing guidelines from DEL-03.04) based on peak flow rate and target treatment performance; size separator for three volume components: oil storage volume, solids settling volume, water retention volume; document sizing equation source and assumptions (Guidance §Example 2 step 3; Guidance §T-2 OWS sizing methodology selection trade-off discusses methodology options).
- **Retention time verification:** Calculate retention time (separator volume / peak flow rate); verify retention time meets minimum duration for oil/water separation efficiency (typical minimum 10-20 minutes depending on oil characteristics and treatment target per ER or environmental permit); adjust separator volume if retention time is insufficient (Guidance §Example 2 step 4).
- **Discharge rate and quality limits confirmation:** Verify discharge rate complies with outfall capacity or environmental permit limits; confirm treatment performance (oil removal efficiency) meets discharge water quality limits (e.g., <15 mg/L oil & grease for typical environmental permits); document permit requirement references (Guidance §Example 2 step 5).
- **Results summary:** Prepare results summary table listing separator volume, retention time, treatment capacity, discharge rate/quality; cross-reference DEL-03.01 Drawing Set for OWS layout and DEL-03.04 Data Sheet Package for equipment specifications; note any conservative assumptions requiring validation (Guidance §Example 2 step 6).

**Verification checkpoint:** Self-check verifies contributing area determination, peak flow calculation logic, separator volume sizing methodology, retention time adequacy; confirms discharge compliance with environmental permit requirements.

**Cross-reference:** Specification §FR-2 environmental protection performance verification; Specification §PR-2 facility throughput and containment support; Datasheet §Construction OWS sizing content; Guidance §P-2 and §Example 2.

**4.3 Develop Duct Bank Capacity Calculations:**
- **Conduit schedule input:** Obtain cable schedule from PKG-17 showing cable sizes (conductor size, insulation type, overall diameter), cable quantities, and conduit assignments; document PKG-17 deliverable reference, revision, and coordination date (Guidance §Example 3 duct bank fill factor analysis step 1; Guidance §T-4 duct bank calculation coordination trade-off discusses coordination boundary).
- **Conduit fill area calculation:** For each conduit, calculate total cable cross-sectional area (sum of individual cable areas based on cable diameters from PKG-17 cable schedule or manufacturer data); calculate conduit internal area (based on conduit size from DEL-03.01 Drawing Set and conduit inside diameter from manufacturer data or DEL-03.02 specification) (Guidance §Example 3 step 2).
- **Fill factor verification:** Calculate fill factor (total cable area / conduit internal area); verify fill factor complies with electrical code limits (e.g., NEC/CEC Table 1 allows 40% fill for 3+ cables in conduit); identify any conduits exceeding fill limits requiring upsizing; prepare coordination note for PKG-17 if conduit changes affect electrical design (Guidance §Example 3 step 3).
- **Pull box spacing calculation:** Verify pull box spacing based on cable pulling tension limits (coordinate with PKG-17 for maximum pulling tension criteria per cable type); calculate cumulative pulling angles and straight lengths between pull boxes; verify pull box locations shown in DEL-03.01 Drawing Set comply with maximum spacing per electrical codes or cable manufacturer requirements (Guidance §Example 3 step 4).
- **Results summary:** Prepare results summary table listing conduit sizes, cable quantities, fill factors, pull box spacings; flag any fill factor exceedances or pull box spacing deficiencies; provide coordination notes for PKG-17 regarding any required changes (Guidance §Example 3 step 5).

**Verification checkpoint:** Self-check verifies conduit fill calculations, fill factor compliance with electrical codes, pull box spacing adequacy; confirms coordination with PKG-17 cable schedule is documented.

**Cross-reference:** Specification §FR-3 coordination with electrical infrastructure; Specification §IF-2 coordination with PKG-17; Datasheet §Construction duct bank capacity content; Guidance §P-4, §T-4, and §Example 3.

**4.4 Develop Trenchless Crossing Structural Calculations:**
- **Input data collection:** Obtain geotechnical parameters (soil unit weight, internal friction angle, cohesion) from geotechnical report for crossing location; identify roadway surcharge load (vehicle load per highway design code or pavement weight); determine crossing depth and length from DEL-03.01 Drawing Set; identify casing pipe size, wall thickness, and material from DEL-03.02 Technical Specification (Guidance §Example 4 trenchless crossing structural analysis step 1).
- **Earth pressure calculation:** Calculate vertical earth pressure on casing pipe (overburden soil pressure = soil unit weight × depth); apply surcharge load (roadway live load or pavement dead load); select earth pressure coefficient (use at-rest coefficient or increased value to account for boring disturbance per Guidance §T-3 trenchless crossing calculation conservatism trade-off); document conservatism in assumptions (Guidance §Example 4 step 2).
- **Casing pipe structural analysis:** Model casing pipe as beam on elastic foundation or use ring deflection analysis method appropriate for pipe material and installation conditions; apply earth pressure and surcharge loads; calculate bending moments, deflections, and stresses; verify against allowable limits per pipe material standard (e.g., ASTM steel pipe allowable stresses, deflection limits per API or AWWA standards) (Guidance §Example 4 step 3).
- **Jacking force calculation:** Estimate jacking force based on pipe-soil friction (friction coefficient × normal force from earth pressure) and face resistance for boring method (auger boring, microtunneling, etc. per DEL-03.02 specification); verify jacking force within thrust capacity of typical jacking equipment and pipe crushing strength; note validation requirement with boring contractor based on selected equipment (Guidance §Example 4 step 4).
- **Settlement and differential movement analysis:** Estimate settlement potential from soil consolidation or boring disturbance using geotechnical parameters; verify carrier pipe support and annular space (per DEL-03.01 crossing details) accommodate anticipated settlements without pipe overstress; document monitoring requirements if settlement risk is significant (Guidance §Example 4 step 5).
- **Results summary:** Prepare results summary table listing loading conditions, structural capacities, utilization ratios (actual/allowable), safety factors; document conservatism in assumptions and note any validation requirements (e.g., "Verify jacking force with boring contractor") (Guidance §Example 4 step 6).

**Verification checkpoint:** Self-check verifies loading calculations, structural analysis methodology, capacity verification against allowable limits; confirms conservative assumptions are documented per Guidance §T-3.

**Cross-reference:** Specification §PR-1 structural performance (trenchless crossings); Datasheet §Construction trenchless crossing calculations content; Guidance §P-1 structural performance, §T-3, and §Example 4.

**4.5 Document Calculation Methodology:**
- For each calculation section, document methodology including governing equations, analysis methods (rational method, hydrograph analysis, API separator sizing, ring deflection analysis, etc.), software tools used, design standards applied, and all assumptions (Specification §QR-2 calculation methodology documentation requirement; Guidance §P-3 calculation assumptions and data source traceability principle).
- Include calculation flowchart or methodology overview for complex analyses (e.g., hydraulic model setup, structural analysis approach) to support independent verification (Guidance §C-5 engineering record and future reference consideration).
- Reference applicable code sections, standard equations, and manufacturer data sources for all methods and parameters used.
- Document software validation status: software identification, version number, validation procedure reference (for project-validated software), or validation calculation (for spreadsheets or in-house tools) per Specification §QR-3 software validation requirements.

**Verification checkpoint:** Self-check confirms methodology is clearly documented and assumptions are identified for all calculation sections; verifies software validation documentation is included.

**Cross-reference:** Specification §QR-2 calculation methodology documentation; Datasheet §Construction methodology documentation content; Guidance §P-3 and §C-5.

### 5. Develop Environmental Protection Calculations Summary

**Objective:** Consolidate environmental protection-related calculations (OWS sizing, drainage capacity, discharge limits) and demonstrate compliance with **OBJ-7 Environmental Protection** requirements to support permitting and regulatory approval.

**Activities:**
- Summarize OWS sizing results from Step 4.2: separator volume, retention time, treatment capacity, discharge rate/quality; confirm compliance with environmental permit requirements or Employer's Requirements environmental protection criteria (Specification §FR-2 environmental protection performance verification; Guidance §P-2 environmental protection performance verification principle).
- Summarize storm drainage capacity results from Step 4.1: peak runoff flows, drainage system capacity, outfall discharge rates; confirm containment and conveyance adequacy to prevent environmental contamination from runoff bypassing treatment systems.
- Identify any environmental protection margins or conservatism in calculations (e.g., OWS retention time safety factor, storm drainage capacity margin above design storm); document justification for conservatism.
- Cross-reference environmental protection features in DEL-03.01 Drawing Set (OWS layout, containment boundaries, drainage flow paths) and DEL-03.02 Technical Specification (OWS treatment criteria, discharge limits) to demonstrate calculation-design consistency.
- Prepare environmental protection calculations summary section or executive summary table for use in permitting documentation or regulatory compliance verification.

**Verification checkpoint:** Interdisciplinary check with process team or environmental specialist confirms environmental protection calculations demonstrate OBJ-7 compliance; independent check validates compliance with environmental permit requirements and ER environmental criteria.

**Cross-reference:** Specification §FR-2 environmental protection performance verification; Specification §PR-2 facility throughput and containment support; Datasheet §Conditions OBJ-7 environmental protection emphasis; Guidance §P-2.

### 6. Compile Calculation Metadata and Prepare for Issue

**Objective:** Finalize calculation package with complete metadata, revision information, and signature blocks to support document control system issue and future traceability.

**6.1 Obtain Calculation Number from Document Control Register:**
- Request calculation document number from project document control system per project numbering procedures (TBD; Specification §FR-4 document metadata and calculation control requirement).
- Verify calculation number format matches project calculation numbering scheme; confirm number is unique and not previously issued.

**6.2 Set Initial Revision Code:**
- Set revision code to "00" for initial issue per Datasheet §Attributes (or per project revision code conventions if different; confirm with document control coordinator).
- Prepare revision history table on cover page showing Revision 00, issue date (TBD at time of issue), description "Initial issue for design development", preparer/checker/approver names.

**6.3 Complete Calculation Package Metadata:**
- Complete cover page with calculation title, project identification, calculation number, revision, issue date (TBD), preparer/checker/approver signature blocks.
- Verify all calculation sections are numbered consistently and cross-references between sections are correct.
- Verify all appendices are included and referenced in calculation body (software output files, manufacturer data sheets from DEL-03.04, drainage area sketches, standard calculation references).
- Prepare calculation results summary table (executive summary) showing key results for quick review.

**6.4 Compile Quality Records:**
- Prepare calculation review checklist for self-check documentation (verification activities listed in Step 7.1 below).
- Prepare interdisciplinary review log for coordination check documentation (verification activities listed in Step 7.2 below).
- Prepare independent check review form for approver signature and comments (verification activities listed in Step 7.3 below).
- Obtain QA checklists per project Quality Management Plan requirements (TBD; Specification §QR-1 compliance with Quality Management Plan).

**Verification checkpoint:** QA coordinator reviews calculation metadata completeness, verifies revision history is documented, confirms quality record templates are prepared before verification workflow begins.

**Cross-reference:** Specification §FR-4 document metadata and calculation control; Specification §Documentation calculation package organization; Datasheet §Attributes metadata fields; Guidance §C-5 engineering record.

### 7. Execute Verification Workflow

**Objective:** Ensure calculation package undergoes rigorous review per project Quality Management Plan requirements, creating traceable QA record for regulatory compliance and future reference.

**7.1 Self-Check (Preparer Review):**

Calculation engineer (preparer) performs self-check using calculation review checklist; documents review completion by signing/dating checklist and initialing calculation pages reviewed.

**Self-check activities:**
- **7.1.1 Calculation logic and methodology:** Review calculation approach for each section; verify methodology is appropriate for analysis type (rational method for small drainage areas, hydrograph for large areas; API sizing for OWS; fill factor analysis for duct banks; structural analysis for crossings); confirm governing equations and analysis methods are correct.
- **7.1.2 Input data verification:** Verify all input data sources are correctly referenced in input data summary; confirm data extraction is accurate (e.g., rainfall intensities match IDF curves, soil properties match geotechnical report); validate input data is reasonable for site conditions.
- **7.1.3 Units and conversions:** Check unit consistency throughout calculations; verify unit conversions are correct (e.g., mm to m, kPa to MPa, flow rate units); confirm results units match typical engineering practice and code requirements.
- **7.1.4 Methodology documentation:** Confirm calculation methodology is documented per Specification §QR-2 and Guidance §P-3 requirements; verify assumptions are identified and justified; check that conservative assumptions for missing data are flagged per Guidance §C-1.
- **7.1.5 Metadata completeness:** Verify calculation number, revision, preparer/checker/approver names, issue date (TBD) are correctly populated on cover page; check revision history table is complete; confirm all calculation pages are numbered and total page count is correct.
- **7.1.6 Software validation:** For software calculations, verify software identification, version, validation status are documented per Specification §QR-3; confirm software output files are included in appendix and correctly referenced in calculation body; perform spot-check of software results against hand calculation for representative case.
- **7.1.7 Cross-reference verification:** Check that cross-references to related deliverables (DEL-03.01 drawing sheet numbers, DEL-03.02 specification sections, DEL-03.04 data sheets, PKG-17 cable schedules) are correct and up-to-date.
- **7.1.8 Results reasonableness:** Review calculation results for reasonableness; verify pipe sizes, flows, capacities are typical for facility type and scale; identify any outliers or unexpected results requiring further validation.
- **7.1.9 Completeness check:** Confirm all anticipated calculation sections per Specification §Scope are included (storm drainage, OWS, duct banks, trenchless crossings); verify results summary table is complete; check all appendices are included.

**Self-check documentation:** Calculation engineer signs/dates self-check checklist, initials calculation pages, documents any corrections or clarifications made during self-check.

**Cross-reference:** Specification §Verification self-check description; Specification §QR-2 methodology documentation; Specification §QR-3 software validation; Guidance §P-3 data source traceability.

**7.2 Interdisciplinary Check (Coordination Review):**

Discipline checker or designated coordination reviewer performs interdisciplinary check focusing on coordination with related deliverables and adjacent packages; documents review completion using interdisciplinary review log.

**Interdisciplinary check activities:**
- **7.2.1 DEL-03.01 Drawing Set coordination:** Verify calculation geometric inputs (pipe alignments, invert elevations, slopes, OWS location, duct bank routing, crossing alignments) match DEL-03.01 Drawing Set; confirm calculation results (pipe sizes, slopes, hydraulic parameters) align with drawing annotations; identify any inconsistencies requiring drawing or calculation revision (Specification §IF-1 coordination with DEL-03.01; Guidance §P-4 coordination with design deliverables).
- **7.2.2 DEL-03.02 Technical Specification coordination:** Verify calculation material properties (pipe roughness coefficients, structural capacities) match DEL-03.02 Technical Specification; confirm calculation performance assumptions (OWS treatment criteria, discharge limits) align with specification requirements; check that calculation results validate specification performance claims (Specification §IF-1 coordination with DEL-03.02).
- **7.2.3 DEL-03.04 Data Sheet Package coordination:** Verify calculation equipment performance parameters (OWS capacity, pump curves if applicable, instrumentation ranges) match DEL-03.04 Data Sheet Package; confirm calculations validate equipment selection adequacy (Specification §IF-1 coordination with DEL-03.04).
- **7.2.4 PKG-02 site grading coordination:** Verify calculation drainage area delineation, finished grade elevations, drainage flow directions align with PKG-02 site grading plans; confirm site coordinate system and vertical datum match PKG-02 (Specification §IF-2 coordination with PKG-02).
- **7.2.5 PKG-17 electrical coordination:** Verify duct bank fill factor calculations use current PKG-17 cable schedules; confirm coordination notes address any conduit sizing or pull box spacing issues; check that calculation assumptions (cable sizes, quantities, pulling tensions) align with PKG-17 electrical design (Specification §IF-2 coordination with PKG-17; Guidance §T-4 duct bank calculation coordination).
- **7.2.6 Environmental protection calculations review:** Review OWS sizing calculations and storm drainage capacity results with process team or environmental specialist to confirm environmental protection adequacy for OBJ-7 compliance; verify environmental permit requirements are correctly interpreted and applied (Specification §FR-2 environmental protection performance verification; Step 5 environmental protection calculations summary).

**Interdisciplinary check documentation:** Discipline checker or coordination reviewer signs/dates interdisciplinary review log, documents coordination confirmation or identifies issues requiring resolution; reviews are tracked until closure.

**Cross-reference:** Specification §Verification interdisciplinary check description; Specification §IF-1 coordination with related deliverables; Specification §IF-2 coordination with adjacent packages; Guidance §P-4 and §C-4.

**7.3 Independent Check (Approver Review):**

Independent reviewer (approver, typically senior civil engineer) performs independent check focusing on compliance with Employer's Requirements, civil standards, and design criteria validation; documents review completion by signing calculation package for issue.

**Independent check activities:**
- **7.3.1 Standards compliance:** Verify calculations comply with Employer's Requirements Volume 2 Part 2 civil requirements; confirm applicable codes and standards (NBC, BCBC, CSA standards, electrical codes for duct banks) are correctly applied; validate code editions and clause references are current (Specification §Verification independent check; Specification §Standards governing standards and applicable codes).
- **7.3.2 Hydraulic performance validation:** Validate storm drainage hydraulic calculations demonstrate compliance with design storm event per ER requirements; verify hydraulic grade lines, pipe capacities, and outfall discharge rates meet hydraulic performance criteria; confirm calculation methodology is appropriate and results are reasonable (Specification §PR-1 hydraulic and structural performance; Guidance §P-1 hydraulic performance verification).
- **7.3.3 OWS compliance verification:** Validate OWS sizing calculations demonstrate adequate treatment capacity, retention time, and discharge compliance; verify OWS design supports OBJ-7 Environmental Protection objectives; confirm environmental permit requirements are satisfied (Specification §FR-2 environmental protection performance verification; Specification §PR-2 facility throughput and containment support; Guidance §P-2).
- **7.3.4 Design criteria validation:** Verify design criteria used in calculations (design storm return period, runoff coefficients, design life, seismic parameters, soil properties, structural load factors) match civil design brief and geotechnical report; confirm ER Volume 2 Part 2 requirements are correctly extracted and interpreted per Guidance §C-2; validate conservative assumptions for missing data are appropriate per Guidance §C-1 (Specification §PR-3 design life and environmental conditions).
- **7.3.5 Structural performance validation:** For trenchless crossing structural calculations, validate loading assumptions, structural analysis methodology, and capacity verification against allowable limits; confirm conservatism is appropriate for boring condition uncertainty per Guidance §T-3 (Specification §PR-1 structural performance).
- **7.3.6 Calculation spot-checks:** Perform independent spot-checks of critical calculations to verify accuracy; recalculate representative cases using different method or software to validate results; check order-of-magnitude reasonableness for key results (peak flows, separator volume, structural capacities).
- **7.3.7 QA documentation review:** Review self-check checklist and interdisciplinary review log to confirm all verification activities are completed and issues are resolved; verify calculation package metadata is complete; confirm quality records per Quality Management Plan are prepared (Specification §QR-1 compliance with Quality Management Plan).

**Independent check documentation:** Independent reviewer signs/dates independent check review form and calculation package cover page approver signature block; documents review comments and confirms all comments are resolved before issue; records results in reviewer signature blocks per project QA procedures.

**Cross-reference:** Specification §Verification independent check description; Specification §Standards; Specification §PR-1, §PR-2, §PR-3 performance requirements; Guidance §C-1, §C-2, §T-3 considerations.

**Verification completion:** All three verification steps (self-check, interdisciplinary check, independent check) must be completed and documented before calculation package issue; any review comments must be resolved and resolutions documented in review logs; preparer/checker/approver signatures on cover page confirm verification completion.

### 8. Issue Calculation Package into Document Control System

**Objective:** Deliver completed and verified calculation package into project document control system for distribution and archival, creating permanent engineering record.

**Activities:**
- Finalize calculation package issue date on cover page and revision history table (set to date of document control system submittal).
- Compile calculation package PDF: combine cover page, input summary, all calculation sections, results summary, appendices into single searchable PDF file per project document control requirements.
- Archive calculation source files (hydraulic model files, spreadsheet files, software output files) per document control procedures; ensure files are accessible for future validation or design modifications.
- Submit calculation package to document control system with document metadata (calculation number, revision, title, discipline, package, deliverable ID, preparer/checker/approver names, issue date) per project document control procedures (TBD; Specification §FR-4 document metadata).
- Obtain document control register confirmation of issue; verify calculation package is distributed to project team per distribution matrix.
- File quality records (self-check checklist, interdisciplinary review log, independent check review form, QA checklists) per Quality Management Plan archival requirements (Specification §QR-1; quality records listed in Records section below).

**Issue completion confirmation:** Document control coordinator confirms calculation package is issued into document control system; calculation register entry is created; distribution is complete.

**Cross-reference:** Specification §FR-4 document metadata and calculation control; Specification §Documentation calculation package deliverables; Datasheet §Conditions calculation control alignment; Guidance §C-5 engineering record preservation.

## Verification

**Verification workflow summary:**

This procedure implements three-level verification workflow per project Quality Management Plan to ensure calculation accuracy, coordination, and compliance before issue:

1. **Self-check (preparer review):** Calculation engineer verifies calculation logic, input data, units, methodology documentation, software validation, cross-references, results reasonableness, and completeness per Step 7.1 activities; documents review using self-check checklist.

2. **Interdisciplinary check (coordination review):** Discipline checker or coordination reviewer verifies coordination with related deliverables (DEL-03.01/02/04) and adjacent packages (PKG-02, PKG-17), and reviews environmental protection calculations adequacy per Step 7.2 activities; documents review using interdisciplinary review log.

3. **Independent check (approver review):** Independent reviewer validates compliance with Employer's Requirements and civil standards, confirms design criteria application, performs calculation spot-checks, and reviews QA documentation per Step 7.3 activities; documents review by signing calculation package for issue.

**Verification traceability:** All verification activities documented in quality records (checklists, review logs, signature blocks); verification links calculation package to Specification requirements, ensuring requirements traceability per Specification §Verification description.

**Cross-reference:** Specification §Verification describes three-level review process; Specification §QR-1 compliance with Quality Management Plan QA procedures; Guidance §C-4 QA sign-offs and coordination; Datasheet §Cross-Document Linkages references Procedure verification process.

## Records

**Calculation deliverables (primary outputs):**
- **Calculation package PDF**: Storm drainage hydraulic calculations, OWS sizing calculations, duct bank capacity calculations, trenchless crossing structural calculations, organized per Step 3 structure with cover page, input summary, calculation sections, results summary, appendices (Source: Specification §Documentation calculation package organization; Datasheet §Construction calculation package organization).
- **Calculation source files**: Hydraulic model files (e.g., StormCAD .stsw files), spreadsheet files (.xlsx), software output files archived per document control procedures for future validation or design modifications (Specification §QR-2 methodology documentation; Guidance §C-5 engineering record preservation).
- **Environmental protection calculations summary**: Consolidated summary of OWS sizing and drainage capacity results demonstrating OBJ-7 Environmental Protection compliance for permitting documentation (developed per Step 5).

**Quality records (supporting documentation):**
- **Self-check checklist**: Documents preparer review completion per Step 7.1 self-check activities; includes preparer signature/date, calculation pages initialed, corrections documented (Specification §Verification self-check documentation).
- **Interdisciplinary review log**: Documents coordination check completion per Step 7.2 activities; includes discipline checker or coordination reviewer signature/date, coordination confirmations or issues identified, issue resolutions tracked (Specification §Verification interdisciplinary check documentation).
- **Independent check review form**: Documents approver review completion per Step 7.3 activities; includes independent reviewer signature/date, review comments, comment resolutions; filed with calculation package (Specification §Verification independent check documentation).
- **QA checklists**: Per project Quality Management Plan requirements (TBD; specific checklist format per project QA procedures) documenting calculation package compliance with quality requirements (Specification §QR-1).
- **Calculation register entry**: Document control system record showing calculation number, revision, issue date, distribution, archived file location (Specification §FR-4 document metadata; Step 8 issue into document control).
- **Calculation review logs**: Tracks review comments from self-check, interdisciplinary check, independent check and documents comment resolutions; maintains traceability of calculation revisions during review process.
- **Software validation documentation**: Software identification, version, validation procedure reference or validation calculation confirming software accuracy per Step 4.5 methodology documentation (Specification §QR-3 software validation).

**Records retention:** All calculation deliverables and quality records archived per project document control and Quality Management Plan requirements for design life of facility plus regulatory retention period (ASSUMPTION per typical project archival requirements).

**Cross-reference:** Specification §Documentation associated quality records; Specification §QR-1 compliance with Quality Management Plan; Datasheet §Cross-Document Linkages references Procedure quality records section; Guidance §C-4 QA documentation; Guidance §C-5 engineering record preservation.

## Cross-Document Linkages

**Procedure ↔ Datasheet:**
- Procedure §Purpose production and QA purposes → Datasheet §Conditions operational context (calculations validate design, support regulatory approval, create permanent record)
- Procedure §Prerequisites lists reference materials → Datasheet §Attributes "Design Criteria Sources" + Datasheet §References
- Procedure §Steps 3.2 calculation section structure → Datasheet §Construction calculation package organization structure
- Procedure §Steps 4.1 storm drainage calculations → Datasheet §Construction storm drainage calculations content
- Procedure §Steps 4.2 OWS sizing calculations → Datasheet §Construction OWS sizing content
- Procedure §Steps 4.3 duct bank capacity calculations → Datasheet §Construction duct bank capacity content
- Procedure §Steps 4.4 trenchless crossing calculations → Datasheet §Construction trenchless crossing calculations content
- Procedure §Steps 4.5 methodology documentation → Datasheet §Construction methodology documentation content
- Procedure §Steps 6.2 set initial revision code → Datasheet §Attributes "Revision" 00
- Procedure §Records calculation deliverables and quality records → Datasheet §References lists quality records

**Procedure ↔ Specification:**
- Procedure §Purpose → Specification §Scope calculation production purpose
- Procedure §Prerequisites reference materials → Specification §Standards governing standards list
- Procedure §Steps 1 scope review → Specification §Scope anticipated calculation types and exclusions
- Procedure §Steps 2.1 input data collection from related deliverables → Specification §IF-1 coordination with DEL-03.01/02/04
- Procedure §Steps 2.1 input data collection from adjacent packages → Specification §IF-2 coordination with PKG-02/17
- Procedure §Steps 2.2 collect design criteria → Specification §PR-3 design life and environmental conditions
- Procedure §Steps 2.4 document data sources → Specification §QR-2 calculation methodology documentation
- Procedure §Steps 3.2 establish calculation section structure → Specification §Scope anticipated calculation types
- Procedure §Steps 4.1 storm drainage calculations → Specification §FR-1 comprehensive hydraulic analysis + §PR-1 hydraulic performance
- Procedure §Steps 4.2 OWS sizing calculations → Specification §FR-2 environmental protection performance verification + §PR-2 facility throughput and containment
- Procedure §Steps 4.3 duct bank capacity calculations → Specification §FR-3 coordination with electrical infrastructure + §IF-2 PKG-17 coordination
- Procedure §Steps 4.4 trenchless crossing calculations → Specification §PR-1 structural performance
- Procedure §Steps 4.5 methodology documentation → Specification §QR-2 calculation methodology documentation
- Procedure §Steps 5 environmental protection calculations → Specification §FR-2 environmental protection performance verification
- Procedure §Steps 6 metadata compilation → Specification §FR-4 document metadata and calculation control
- Procedure §Steps 7.1 self-check → Specification §Verification self-check description
- Procedure §Steps 7.2 interdisciplinary check → Specification §Verification interdisciplinary check description
- Procedure §Steps 7.3 independent check → Specification §Verification independent check description
- Procedure §Steps 8 issue into document control → Specification §Documentation calculation package deliverables
- Procedure §Records quality records → Specification §Documentation associated quality records

**Procedure ↔ Guidance:**
- Procedure §Purpose → Guidance §Purpose "why this deliverable matters"
- Procedure §Prerequisites "Guidance alignment" → Guidance §Purpose, §Principles, §Considerations, §Examples referenced
- Procedure §Steps 1 scope review → Guidance §C-3 calculation structure and scope boundaries
- Procedure §Steps 2.2 collect design criteria → Guidance §C-1 design criteria availability + §C-2 ER extraction
- Procedure §Steps 2.3 conservative assumptions → Guidance §C-1 data gaps + §T-1 conservative assumptions trade-off
- Procedure §Steps 2.4 document data sources → Guidance §P-3 calculation assumptions and data source traceability
- Procedure §Steps 3.1 calculation package organization → Guidance §C-5 engineering record and future reference
- Procedure §Steps 4.1 storm drainage calculations → Guidance §P-1 hydraulic performance verification + §Example 1 calculation structure
- Procedure §Steps 4.2 OWS sizing calculations → Guidance §P-2 environmental protection performance verification + §Example 2 sizing methodology + §T-2 sizing methodology selection
- Procedure §Steps 4.3 duct bank capacity calculations → Guidance §P-4 coordination with design deliverables + §T-4 duct bank coordination + §Example 3 fill factor analysis
- Procedure §Steps 4.4 trenchless crossing calculations → Guidance §T-3 calculation conservatism + §Example 4 structural analysis
- Procedure §Steps 4.5 methodology documentation → Guidance §P-3 data source traceability + §C-5 engineering record
- Procedure §Steps 5 environmental protection calculations → Guidance §P-2 environmental protection performance verification
- Procedure §Steps 7.2 interdisciplinary check coordination activities → Guidance §P-4 coordination with design deliverables + §C-4 QA coordination
- Procedure §Steps 7.3 independent check design criteria validation → Guidance §C-1 design criteria availability + §C-2 ER extraction
- Procedure §Records calculation deliverables preservation → Guidance §C-5 engineering record and future reference

**Steps Linked to Requirements (Procedure Implementation → Specification Requirements):**
- Step 1 scope review → FR-4 document metadata (confirms calculation scope aligns with Specification)
- Steps 2.1-2.4 input data collection → IF-1 coordination with related deliverables + IF-2 coordination with adjacent packages
- Step 3 calculation structure → Scope anticipated calculation types
- Step 4.1 storm drainage calculations → FR-1 comprehensive hydraulic analysis + PR-1 hydraulic performance
- Step 4.2 OWS sizing calculations → FR-2 environmental protection performance verification + PR-2 facility throughput and containment
- Step 4.3 duct bank capacity calculations → FR-3 coordination with electrical infrastructure
- Step 4.4 trenchless crossing calculations → PR-1 structural performance (crossings)
- Step 4.5 methodology documentation → QR-2 calculation methodology documentation
- Step 5 environmental protection calculations → FR-2 environmental protection performance verification
- Step 6 metadata compilation → FR-4 document metadata and calculation control
- Step 7.1 self-check → QR-1 compliance with Quality Management Plan + QR-2 methodology documentation + QR-3 software validation
- Step 7.2 interdisciplinary check → IF-1 coordination with related deliverables + IF-2 coordination with adjacent packages + FR-2 environmental protection (process team review)
- Step 7.3 independent check → PR-1 hydraulic and structural performance + PR-2 facility throughput and containment + PR-3 design life and environmental conditions + QR-1 compliance with Quality Management Plan
- Step 8 issue into document control → FR-4 document metadata + Documentation calculation package deliverables

(All Procedure steps have clear linkages to Specification requirements, ensuring requirements implementation traceability.)

## Pass 3 Final Notes

**Pass 3 Reconciliation Completed:**
- All cross-document linkages verified bidirectional: Procedure steps reference Datasheet attributes/construction/references, Specification requirements, and Guidance principles/considerations/examples; corresponding back-references confirmed in those documents.
- Steps linked to requirements: All Procedure steps map to Specification requirements; implementation traceability matrix documented above.
- Entity coverage check: All major calculation types and themes appear consistently across all four documents (see Datasheet §Cross-Document Linkages entity coverage check).
- Terminology consistency verified: Key terms used consistently across all four documents (see Specification §Cross-Document Linkages terminology consistency check).
- Verification workflow described: Three-level verification (self-check, interdisciplinary check, independent check) implements Specification §Verification requirements and creates QA record per Quality Management Plan.
- TBD items cross-check: All TBD items in Procedure align with Datasheet and Specification TBD items; clear resolution path via Prerequisites identifies required reference materials.
- No conflicts detected between documents; all requirements, rationale, and implementation steps align.

**Document Maturity:**
- This Procedure, along with Datasheet, Specification, and Guidance, has completed three enrichment passes (Pass 1 initial generation, Pass 2 cross-reference and detail enrichment, Pass 3 final reconciliation).
- Documents are ready for WORKING_ITEMS sessions where human engineer will refine, validate, and populate TBD items as design development proceeds.
- All four documents provide coherent, traceable, and consistent foundation for DEL-03.03 Underground Utilities Design Calculations production.
