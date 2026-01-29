# Procedure: DEL-04.03 Pavement Design Calculations

## Purpose

This procedure defines the workflow for producing, reviewing, coordinating, and issuing the Pavement Design Calculations (DEL-04.03) to ensure calculation inputs are properly sourced, methodology is appropriate, results validate DEL-04.01 drawings and DEL-04.02 specifications, and outputs support DEL-04.04 testing requirements, while tracking all assumptions for resolution.

## Prerequisites

### Dependencies
**Mode**: NOT_TRACKED (per `_DEPENDENCIES.md`)
**Note**: Dependencies are coordinated externally by humans. The following inputs are typically required:
- Traffic loading data from Owner/ER (**TBD** – if not provided, assumed values will be used)
- Geotechnical investigation report (**TBD** – site investigation required)
- DEL-04.01 preliminary drawing set (pavement layout and section arrangement to analyze)
- DEL-04.02 preliminary specification (material properties to use as calculation inputs)
- Employer's Requirements design criteria (**location TBD** – design methodology, performance requirements)
- Design standards (TAC, AASHTO, PCA manuals)
- Pavement analysis software (**TBD** – software selection and licensing)

### Reference Materials
- **Decomposition**: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- **Datasheet (DEL-04.03)**: Current version with Calculation Scope, Design Inputs, Assumptions & TBDs
- **Specification (DEL-04.03)**: Current version with Requirements R1.1–R5.2
- **Guidance (DEL-04.03)**: Current version with Review Checklist, Principles, Trade-offs
- **Design standards**: TAC Pavement Design Manual, AASHTO Guide, PCA manuals (obtain copies or confirm access)
- **Climate data**: Fraser Surrey, BC climate records (MAAT, freeze-thaw cycles, frost depth)

### Personnel & Roles
- **Calculation Engineer**: Responsible for calculation execution, input assembly, analysis, output documentation
- **Senior Engineer/Checker**: Performs independent check of calculation methodology, inputs, execution, outputs
- **Geotechnical Engineer**: Provides geotechnical parameters; reviews and approves geotechnical assumptions
- **DEL-04.01 Drafter**: Provides pavement layout and section arrangement; receives calculation outputs for drawing updates
- **DEL-04.02 Specification Author**: Provides material property specifications; receives calculation material property assumptions for specification validation
- **DEL-04.04 QA/QC Lead**: Receives calculation output summary as target values for field testing
- **QA Reviewer**: Performs cross-document coordination review, traceability audit, assumption log maintenance

### Tools & Systems
- **Pavement analysis software** (**TBD** – KENPAVE, CIRCLY, MEPDG, or equivalent)
- **Spreadsheet software**: For input assembly, hand calculations, sensitivity analysis, output summaries
- **Calculation documentation template**: Per project standards (**TBD** – obtain template or create based on project requirements)
- **Assumption tracking log**: Coordinated with DEL-04.01 and DEL-04.02 (spreadsheet or database)
- **Traceability matrix**: Linking calculation outputs to drawings, specifications, and test requirements (spreadsheet)

## Steps

### Step 1: Assemble Calculation Inputs and Document Sources

**Objective**: Gather all required design inputs and document sources; flag assumptions and TBDs

**Tasks**:
1.1. **Review scope**:
- Review Datasheet "Calculation Scope" to understand analysis extent (pavement zones, loading cases, OBJ-8 requirements)
- Review DEL-04.01 preliminary drawing set to identify pavement zones requiring analysis
- List all pavement sections/zones to be analyzed (create analysis matrix with zone ID, DEL-04.01 reference, traffic type, area)

1.2. **Assemble traffic loading data**:
- Request traffic loading data from Owner/ER (vehicle types, axle loads, repetitions, growth rate)
- If traffic data is provided: Document source, verify completeness, enter into input summary table
- If traffic data is NOT provided: Develop assumed loading based on facility operational requirements (e.g., typical truck traffic for transload facility, railcar mover loading); flag as **ASSUMPTION** and add to assumption tracking log with resolution path

1.3. **Assemble geotechnical data**:
- Obtain geotechnical investigation report (if available)
- Extract subgrade soil classification, CBR or resilient modulus, compaction requirements, frost depth, groundwater elevation
- If geotechnical data is complete: Document source, verify applicability to pavement zones, enter into input summary table
- If geotechnical data is incomplete or not available: Develop assumed values based on regional soil data or conservative assumptions; flag as **ASSUMPTION** and add to assumption tracking log with resolution path (geotechnical engineer to confirm)

1.4. **Assemble material properties**:
- Review DEL-04.02 preliminary specification for asphalt, concrete, base/subbase material specifications
- Extract or correlate material properties (asphalt modulus, concrete strength, base modulus)
- If laboratory test data is available: Use test data and document source
- If laboratory test data is NOT available: Use design manual correlations or typical values; flag as **ASSUMPTION** and add to assumption tracking log

1.5. **Assemble environmental/climatic data**:
- Obtain climate data for Fraser Surrey, BC (mean annual air temperature, freeze-thaw cycles, frost depth)
- Document sources (climate records, geotechnical report, regional data)

1.6. **Create or update Assumption Tracking Log**:
- Use common format with DEL-04.01 and DEL-04.02 assumption logs (columns: ID, Description, Location, Category, Impacted deliverables, Resolution path, Status, Resolution notes)
- Log all **ASSUMPTION** and **TBD** items identified in Steps 1.2–1.5
- Assign responsibility for resolution (Owner for traffic data, geotechnical engineer for subgrade data, DEL-04.02 author for material properties, etc.)

1.7. **Create Input Summary Tables**:
- Traffic Loading Summary: Vehicle types, axle loads, repetitions, ESALs (or load spectra), growth rate, sources
- Geotechnical Parameter Summary: Subgrade soil type, CBR/Mr, compaction requirements, frost depth, groundwater, sources
- Material Property Summary: Asphalt modulus, concrete strength, base modulus, Poisson's ratios, sources
- Environmental Data Summary: MAAT, freeze-thaw cycles, frost depth, sources

**Verification**:
- All calculation inputs are documented in input summary tables with sources or **ASSUMPTION** flags
- Assumption Tracking Log is updated with all assumptions and TBDs
- Input summary reviewed with Senior Engineer and approved prior to analysis execution

**Records**:
- Input Summary Tables (part of calculation report)
- Updated Assumption Tracking Log

---

### Step 2: Perform Pavement Structural Analysis

**Objective**: Execute pavement design calculations using approved methodology and software

**Tasks**:
2.1. **Confirm design approach**:
- Confirm design methodology with Engineer (TAC vs. AASHTO vs. PCA)
- Confirm design life (25 years **ASSUMPTION** – to be confirmed from ER)
- Confirm reliability level (90% **ASSUMPTION** – to be confirmed from ER)
- Document approved design approach in calculation report

2.2. **Set up pavement analysis software**:
- Install and validate pavement analysis software (**TBD** – KENPAVE, CIRCLY, MEPDG, or equivalent)
- Document software name, version, developer, validation documentation
- Create software input files for each pavement zone:
  - Layer thicknesses (initial trial values based on experience or design charts)
  - Material properties (moduli, Poisson's ratios) from Step 1 input summary
  - Loading configuration (axle loads, tire pressures, contact areas) from Step 1 traffic summary
  - Critical loading positions (worst-case stress/strain locations)

2.3. **Execute layered elastic analysis**:
- Run software for each pavement zone and loading case
- Extract critical response parameters:
  - Tensile strain at bottom of asphalt layer (fatigue criterion)
  - Compressive stress/strain on subgrade (rutting criterion)
  - Surface deflection (optional verification check)
- Compare critical responses to allowable limits (per design methodology)
- Adjust layer thicknesses iteratively until critical responses meet acceptance criteria

2.4. **Perform hand calculation verification**:
- Select at least one critical pavement zone
- Perform simplified hand calculation or use design charts to verify software results
- Document hand calculation steps and comparison to software results
- If significant discrepancy (>10%), investigate cause (software error, input error, methodology difference) and resolve

2.5. **Document analysis process**:
- Include software input files (or screenshots) in calculation report appendix
- Include software output files (or summary tables) in calculation report
- Document layer thickness iterations and convergence to final design
- Explain any deviations from standard methodology or unusual results

**Verification**:
- Software inputs match documented inputs from Step 1
- Critical response parameters (strain, stress, deflection) are within allowable limits
- Hand calculation verification confirms software results are reasonable
- Senior Engineer reviews analysis methodology and software use

**Records**:
- Analysis Worksheets (software inputs, outputs, hand calculations)
- Pavement layer thickness design results for each zone

---

### Step 3: Perform Sensitivity and OBJ-8 Expansion Analysis

**Objective**: Evaluate design robustness to input parameter variations and validate OBJ-8 expansion corridor capacity

**Tasks**:
3.1. **Subgrade sensitivity analysis**:
- Vary subgrade CBR or Mr by ±20% from baseline value
- Re-run analysis for critical pavement zones
- Tabulate effect on required pavement thickness (baseline thickness, thickness at -20% subgrade, thickness at +20% subgrade)
- Document sensitivity (e.g., "±20% subgrade variation causes ±15 mm thickness variation")

3.2. **Traffic sensitivity analysis**:
- Vary traffic volume (ESALs) by ±20% from baseline value
- Re-run analysis for critical pavement zones
- Tabulate effect on required pavement thickness
- Document sensitivity

3.3. **Material property sensitivity analysis** (if material properties are uncertain):
- Vary asphalt modulus by ±10% from baseline value
- Re-run analysis for critical pavement zones
- Tabulate effect on critical strain and required thickness
- Document sensitivity

3.4. **OBJ-8 Phase 2 expansion analysis**:
- Identify pavement zones designated as Phase 2 expansion corridors (per DEL-04.01 and OBJ-8 objectives)
- Obtain or assume ultimate Phase 2 traffic loading (heavier vehicles or increased volume – **TBD** from Owner)
- Run analysis for Phase 2 loading case (use same pavement section as Phase 1, but increase traffic loading)
- Compare Phase 1 loading case results with Phase 2 loading case results
- Document whether Phase 1 pavement design is adequate for Phase 2 loading, or whether additional thickness is required
- If Phase 1 design is adequate for Phase 2: Document capacity reserve (safety factor or remaining fatigue life) available during Phase 1 operations

3.5. **Document sensitivity and OBJ-8 analysis**:
- Create sensitivity analysis summary tables showing parameter variations and thickness effects
- Create OBJ-8 analysis summary comparing Phase 1 vs. Phase 2 loading and required thicknesses
- Provide recommendations (e.g., "Design Phase 1 pavement for ultimate Phase 2 loading to avoid future reconstruction")

**Verification**:
- Sensitivity analysis covers critical parameters (subgrade, traffic, material properties)
- OBJ-8 analysis validates expansion corridor capacity for ultimate Phase 2 loading
- Sensitivity and OBJ-8 results are reasonable and properly documented

**Records**:
- Sensitivity Analysis Results (summary tables)
- OBJ-8 Phase 2 Analysis Results (summary tables, recommendations)

---

### Step 4: Prepare Calculation Output Summary and Traceability Matrix

**Objective**: Summarize calculation results with full traceability to DEL-04.01, DEL-04.02, DEL-04.04

**Tasks**:
4.1. **Create Calculation Output Summary Table**:
- Create table with columns: Pavement Zone ID, DEL-04.01 Reference (sheet, section), Traffic Loading (ESALs), Subgrade (CBR/Mr), Layer Thicknesses (wearing, binder, base, subbase), Total Thickness, Critical Strain/Stress, Safety Factor, DEL-04.02 Reference (material clauses), DEL-04.04 Reference (test requirements)
- Populate table with final design results from Step 2 analysis
- Ensure every pavement zone shown in DEL-04.01 has a corresponding calculation entry

4.2. **Create or update Traceability Matrix**:
- Link each calculation output (pavement thickness) to DEL-04.01 drawing section/detail where it is shown
- Link each material property input to DEL-04.02 specification clause
- Link each acceptance criterion to DEL-04.04 test procedure and acceptance form
- Identify any discrepancies between calculation outputs and DEL-04.01 drawings (flag for resolution)

4.3. **Cross-check with DEL-04.01 drawings**:
- Compare calculated thicknesses to DEL-04.01 drawing section details
- If thicknesses match: Document confirmation in traceability matrix
- If thicknesses do NOT match: Identify discrepancy, determine cause (calculation revision needed, or drawing revision needed), coordinate with DEL-04.01 drafter for resolution

4.4. **Cross-check with DEL-04.02 specifications**:
- Compare material properties used in calculation to DEL-04.02 specification requirements
- If material properties match: Document confirmation in traceability matrix
- If material properties do NOT match: Identify discrepancy, coordinate with DEL-04.02 author for resolution (either calculation revision or specification revision)

**Verification**:
- Output summary table is complete for all pavement zones
- Traceability matrix demonstrates complete linkage to DEL-04.01, DEL-04.02, DEL-04.04
- Cross-checks identify and document any discrepancies requiring resolution

**Records**:
- Calculation Output Summary Table
- Traceability Matrix (updated)
- Discrepancy log (if discrepancies exist)

---

### Step 5: Perform Calculation Review and Obtain Approvals

**Objective**: Verify calculation quality through self-check, independent check, and coordination review

**Tasks**:
5.1. **Self-check** (by Calculation Engineer):
- Arithmetic verification: Re-calculate or use alternate method for critical calculations
- Unit consistency: Verify all inputs and outputs have correct units; verify unit conversions are correct
- Reasonableness check: Compare results to similar projects, design manual charts, or simplified methods
- Input traceability: Verify all inputs have documented sources or **ASSUMPTION** flags
- Document self-check findings and sign off

5.2. **Independent check** (by Senior Engineer/Checker):
- Methodology review: Verify design approach (TAC, AASHTO, PCA) is appropriate for project conditions
- Input review: Verify inputs are reasonable, properly sourced, and assumptions are flagged
- Execution review: Verify calculation steps are correct (formulas, software inputs, logic)
- Output review: Verify results are reasonable and consistent with DEL-04.01/DEL-04.02
- Sensitivity review: Verify sensitivity analysis is adequate and properly interpreted
- Document independent check findings and sign off

5.3. **Cross-document coordination review** (by QA Reviewer):
- Execute Guidance Review Checklist (Steps 1-7)
- Verify calculated thicknesses match DEL-04.01 drawings (or discrepancies are identified)
- Verify material properties match DEL-04.02 specifications (or discrepancies are identified)
- Verify output summary provides target values for DEL-04.04 testing
- Verify assumptions are logged in coordinated assumption tracking system
- Document coordination review findings and sign off

5.4. **Resolve review comments**:
- Address all self-check, independent check, and coordination review findings
- Update calculation report, analysis worksheets, output summary, or traceability matrix as needed
- Re-check affected sections after revisions
- Obtain re-approval from reviewers after revisions

5.5. **Obtain final approvals**:
- Calculation Engineer signs calculation report (author signoff)
- Senior Engineer/Checker signs calculation report (checker signoff)
- QA Reviewer signs off on coordination review (QA signoff)
- Update calculation revision history with approval dates and signoffs

**Verification**:
- Self-check, independent check, and coordination review are complete with signoffs
- All review findings are addressed and resolved
- Calculation report is approved for issuance

**Records**:
- Self-check signoff (in calculation report or separate checklist)
- Independent check signoff (in calculation report or separate checklist)
- Coordination review signoff (in calculation report or separate checklist)
- Review comment log (if comments were issued)

---

### Step 6: Issue Calculation Package and Coordinate Handoffs

**Objective**: Issue calculation package and provide outputs to DEL-04.01, DEL-04.02, DEL-04.04 teams

**Tasks**:
6.1. **Assemble final calculation package**:
- Calculation Report (narrative)
- Input Summary Tables
- Analysis Worksheets (software inputs/outputs, hand calculations)
- Output Summary Table
- Sensitivity Analysis Results
- OBJ-8 Phase 2 Analysis Results
- Traceability Matrix
- Assumption Tracking Log
- References (design standards, geotechnical reports, material test data)
- Revision History
- Approval Signoffs

6.2. **Update revision status**:
- Update calculation report cover page and revision history (e.g., "Rev 0, [Date], Issued for Design")
- Update document management system with issued calculation package

6.3. **Handoff to DEL-04.01**:
- Provide Output Summary Table with pavement thicknesses to DEL-04.01 drafter
- Identify any discrepancies between calculated thicknesses and current drawing sections (flag for drawing revision)
- Schedule coordination meeting to review results and resolve any issues

6.4. **Handoff to DEL-04.02**:
- Provide material property inputs to DEL-04.02 specification author for validation
- Identify any material properties that differ from current specification (flag for specification revision or calculation revision)
- Notify DEL-04.02 author of any assumptions requiring specification clarification

6.5. **Handoff to DEL-04.04**:
- Provide Output Summary Table to DEL-04.04 QA/QC lead as target values for field testing
- Provide sensitivity analysis results to inform testing frequency and critical test locations
- Provide acceptance criteria (thickness tolerances, compaction density targets) for test evaluation

6.6. **Distribution**:
- Distribute calculation package per project distribution matrix (Owner, Engineer, Contractor, Package Coordinators, DEL-04.01/04.02/04.04 leads)

**Verification**:
- Calculation package is complete and approved
- Handoffs to DEL-04.01, DEL-04.02, DEL-04.04 are completed
- Distribution is complete per distribution matrix

**Records**:
- Final issued calculation package (PDF)
- Handoff meeting minutes (DEL-04.01, DEL-04.02, DEL-04.04)
- Distribution records

---

### Step 7: Manage Calculation Revisions (Post-Issuance)

**Objective**: Control calculation revisions to maintain traceability and consistency

**Tasks**:
7.1. **Revision triggers**:
- New geotechnical data available (updated CBR, soil properties)
- Traffic loading data updated or refined
- DEL-04.01 drawings revised (new pavement zones, layout changes)
- DEL-04.02 specifications revised (material property changes)
- Employer's Requirements clarified or revised
- Calculation errors or omissions identified

7.2. **Revision process**:
- Update affected calculation sections (inputs, analysis, outputs)
- Update revision history (new revision number, date, author/checker, summary of changes)
- Re-run affected analyses with updated inputs
- Update Output Summary Table and Traceability Matrix as needed
- Update Assumption Tracking Log if **ASSUMPTION**/**TBD** items are resolved or new items added
- Re-perform self-check, independent check, coordination review for affected sections
- Obtain re-approvals (author, checker, QA reviewer)

7.3. **Coordinate revised outputs**:
- Notify DEL-04.01 drafter if calculated thicknesses change (may require drawing revision)
- Notify DEL-04.02 author if material properties change (may require specification revision)
- Notify DEL-04.04 QA/QC lead if target values or acceptance criteria change

7.4. **Issue revised calculation**:
- Update calculation package with revised content and revision history
- Issue revised calculation per project distribution matrix
- Clearly mark superseded calculation revision and retain for traceability

**Verification**:
- Revised calculation includes updated revision history
- Affected sections are re-checked and re-approved
- Stakeholders (DEL-04.01/04.02/04.04) are notified of changes
- Distribution is complete

**Records**:
- Revised calculation package (PDF, with revision marks or revision history)
- Updated Traceability Matrix (if applicable)
- Updated Assumption Tracking Log (if applicable)
- Approval records for revised calculation
- Stakeholder notification records

---

## Verification

### Verification Checkpoints

| Checkpoint | Specification § | Guidance Step | Verification Method | Acceptance Criteria |
|------------|----------------|---------------|-------------------|---------------------|
| Step 1 complete | §R1.1–R1.4 | Step 1 | Review Input Summary Tables and Assumption Log | All inputs documented with sources or **ASSUMPTION** flags; assumption log updated |
| Step 2 complete | §R2.1–R2.3 | Steps 2–3 | Review Analysis Worksheets and Output Summary | Analysis complete for all pavement zones; software and hand calculations consistent; Senior Engineer approval |
| Step 3 complete | §R2.4–R2.5 | Step 2 | Review Sensitivity and OBJ-8 Analysis Results | Sensitivity analysis complete for critical parameters; OBJ-8 analysis validates expansion corridor capacity |
| Step 4 complete | §R3.1–R3.2 | Steps 4–5 | Review Output Summary Table and Traceability Matrix | Output summary complete; traceability matrix links to DEL-04.01/04.02/04.04; discrepancies identified |
| Step 5 complete | §R4.1–R4.3 | Step 7 | Review approval signoffs | Self-check, independent check, coordination review complete with signoffs |
| Step 6 complete | §R3.2 | Step 5 | Review handoff records and distribution confirmation | Handoffs to DEL-04.01/04.02/04.04 complete; distribution complete |
| Step 7 (revisions) | §R5.1–R5.2 | — | Review revision history and re-approvals | Revised calculation correct; re-approvals obtained; stakeholders notified |

### Overall Acceptance Criteria
- All calculation inputs documented with sources or **ASSUMPTION** flags with resolution paths
- Design methodology follows approved standard (TAC, AASHTO, PCA)
- Analysis complete for all pavement zones shown in DEL-04.01
- Sensitivity analysis demonstrates design robustness
- OBJ-8 Phase 2 analysis validates expansion corridor capacity
- Output summary table complete with traceability to DEL-04.01, DEL-04.02, DEL-04.04
- Self-check, independent check, coordination review signoffs obtained
- Handoffs to DEL-04.01, DEL-04.02, DEL-04.04 complete

## Records

### Deliverable Records
1. **Calculation Report**: Complete report with all sections per Specification R3
2. **Input Summary Tables**: Traffic, geotechnical, material properties, environmental data
3. **Analysis Worksheets**: Software inputs/outputs, hand calculations
4. **Output Summary Table**: Pavement thicknesses, stresses/strains, safety factors, with cross-references
5. **Sensitivity Analysis Results**: Parameter variation study results
6. **OBJ-8 Phase 2 Analysis Results**: Ultimate loading case results
7. **Traceability Matrix**: Cross-references to DEL-04.01, DEL-04.02, DEL-04.04
8. **Assumption Tracking Log**: Coordinated with DEL-04.01 and DEL-04.02
9. **Approval Signoffs**: Self-check, independent check, coordination review

### File Naming Conventions (**TBD** – pending project document management plan)
- Calculation Report: `DEL-04.03_Pavement_Design_Calculations_R[Rev].pdf`
- Traceability Matrix: `DEL-04.03_Traceability_Matrix.xlsx`
- Assumption Log: `PKG-04_Assumption_Log.xlsx` (coordinated across DEL-04.01/04.02/04.03)

### Storage Locations
- **Working files**: `test/execution/PKG-04_Pavement_and_Surfacing/1_Working/DEL-04.03_Pavement_Design_Calculations/`
- **Issued files**: `test/execution/PKG-04_Pavement_and_Surfacing/3_Issued/`
- **Reference files**: `test/execution/PKG-04_Pavement_and_Surfacing/0_References/` (geotechnical reports, traffic data, standards)

## References

### Source Documents
- **Decomposition**: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section PKG-04, DEL-04.03, OBJ-8
- **Datasheet (DEL-04.03)**: Calculation Scope, Design Inputs, Calculation Outputs, Assumptions & TBDs, Cross-document Coordination
- **Specification (DEL-04.03)**: Requirements R1.1–R5.2, Verification Methods, Standards
- **Guidance (DEL-04.03)**: Review Checklist, Principles, Considerations, Trade-offs, Coordination Guidance
- **Employer's Requirements Volume 2 Part 2**: Pavement design criteria (**location TBD**)

### Related Deliverables
- **DEL-04.01**: Pavement Design Drawing Set (pavement sections validated by these calculations)
- **DEL-04.02**: Pavement Technical Specification (material properties used as calculation inputs)
- **DEL-04.04**: Pavement Installation & Test Records (target values provided by these calculations)
