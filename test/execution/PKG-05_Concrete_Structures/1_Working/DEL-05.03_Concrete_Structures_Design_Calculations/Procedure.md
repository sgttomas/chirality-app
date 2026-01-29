# Procedure: DEL-05.03 Concrete Structures Design Calculations

## Purpose

Develop, check, and document the calculation package that underpins PKG-05 concrete structures, ensuring calculations:
- Provide engineering basis for foundations, containment walls, and seismic design
- Support DEL-05.01 (drawings) and DEL-05.02 (specifications) with verified design results
- Meet project quality, traceability, and document control requirements
- Support project objectives (OBJ-3 Storage Capacity, OBJ-7 Environmental Protection)
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234; Specification.md: Scope.)

## Prerequisites

### P-01: Dependencies (Coordinated Externally — NOT_TRACKED Mode)

Dependencies are coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`). Confirm inputs before starting calculations to minimize iterations:

**Geotechnical inputs (from PKG-02 DEL-02.04):**
- Bearing capacity parameters (allowable bearing pressure, ultimate bearing capacity factors)
- Settlement parameters (compression indices, consolidation parameters)
- Soil properties (unit weight, friction angle, cohesion, earth pressure coefficients)
- Groundwater levels and seasonal variations
- Soil-structure interaction parameters (subgrade modulus)
- Seismic site class determination

**Equipment loads (from PKG-10, PKG-11, PKG-13, PKG-15):**
- Equipment weights and dimensions (dead loads)
- Operating loads (product weight for 45,000 MT storage, dynamic loads, vibration)
- Thermal loads (temperature differentials)
- Anchor bolt requirements (tension, shear, combined loading)
- Seismic equipment response factors

**Piping loads (from PKG-14):**
- Pipe support loads (dead, operating, thermal, seismic)
- Thrust loads for thrust block design (pressure thrust, thermal thrust, seismic thrust)
- Anchor loads and moments

**Design basis documents:**
- Employer's Requirements (Volume 2 Part 1 and Part 2 — clause locations TBD)
- Seismic design parameters (spectral accelerations, site class, importance factors, R values)
- Load combinations and load factors
- Material properties and design strengths
- Serviceability limits (crack widths, settlement tolerances, deflection limits)

**Coordination approach:**
- Request inputs early via coordination process (NOT_TRACKED mode)
- Document assumptions for missing inputs and flag as TBD in assumptions register
- Identify hold points where calculations cannot proceed without critical inputs
- Update calculations when inputs are confirmed

(Source: `_DEPENDENCIES.md`; test/execution/_Coordination/_COORDINATION.md; Specification.md: FR-02; Specification.md: IR-01; Guidance.md: C-01; Guidance.md: C-05.)

### P-02: Reference Materials

**Employer's Requirements (clause locations TBD):**
- Volume 2 Part 1: General Requirements (document control, QA/QC requirements, quality management)
- Volume 2 Part 2: Civil & Process Mechanical Works (concrete/structural requirements, design criteria, serviceability limits)
(Source: execution/PKG-05_Concrete_Structures/0_References/_REFERENCE_INDEX.md; test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD.)

**Applicable codes and standards (TBD extraction from ERs):**
- Concrete design code (likely CSA A23.3)
- Building code (likely BC Building Code / NBCC)
- Foundation design standards
- Geotechnical design guidelines
- Seismic design standards
(Source: Specification.md: Standards; Datasheet.md: Attributes.)

**Related deliverables (as they mature):**
- DEL-05.01: Design drawings (coordinate element sizing and reinforcement)
- DEL-05.02: Technical specification (coordinate material properties)
- DEL-02.04: Geotechnical reports (input to foundation calculations)
(Source: Specification.md: IR-01; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:233.)

### P-03: Scope Baseline

Confirm PKG-05 scope and anticipated calculation artifacts:
- **Package scope:** Foundations, containment walls, equipment pads, thrust blocks, ground liner system
- **Anticipated artifacts:** Foundation calculations, containment wall calculations, seismic analysis
- **Project objectives:** OBJ-3 (Storage Capacity 45,000 MT), OBJ-7 (Environmental Protection)
- **Project context:** Canola Oil Transload Facility Phase 1, Fraser Surrey Terminal, Surrey, BC
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:782; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; Datasheet.md: Conditions.)

### P-04: Tools and Software

Calculation tools and software (TBD per Contractor standards):
- Hand calculation formats and templates
- Spreadsheet calculation templates
- Finite element analysis software (if required for complex elements)
- Software validation and verification requirements per project QA
(Source: Datasheet.md: Attributes; Guidance.md: C-04.)

### P-05: Document Control Conventions

Project document control requirements (TBD until conventions are established):
- Calculation numbering system
- Revision tracking and approval workflow
- Calculation format standards (cover sheet, index, design basis, calculations, results summary)
- Electronic file storage and backup requirements
(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Datasheet.md: Attributes; Specification.md: QR-01.)

## Steps

### Step 1: Define Calculation Scope and Create Calculation List

**Actions:**
1. Review decomposition entry for PKG-05 (foundations, containment walls, equipment pads, thrust blocks, ground liner system).
2. Review anticipated calculation artifacts (foundation calculations, containment wall calculations, seismic analysis).
3. Create detailed calculation list organized by element type:
   - Tank foundations (3 × 15,000 MT tanks — 3 calculation sets)
   - Equipment pad foundations (by equipment type or grouped if similar)
   - Building foundations (if within PKG-05 scope — **TBD** scope boundary)
   - Thrust blocks (by location or grouped if similar)
   - Containment walls (by wall section or zone)
   - Seismic analysis (design basis + element-specific analysis)
4. Assign calculation numbers per project document control system (**TBD**).
5. Identify dependencies between calculations (e.g., seismic analysis feeds into foundation calcs).
6. Create calculation package index.

**Outputs:**
- Calculation list with calculation numbers and scope descriptions
- Calculation package index
- Calculation development schedule (sequence and dependencies)

**Verification:**
- Calculation list covers all Specification requirements FR-01, FR-03, FR-04, FR-05
- Calculation list addresses all Datasheet Construction artifacts
- Calculation sequence respects dependencies

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234; Specification.md: FR-01; Datasheet.md: Construction.)

### Step 2: Assemble Design Basis and Input Data

**Actions:**
1. Extract design criteria from Employer's Requirements Volume 2 Part 2:
   - Concrete strength requirements
   - Durability/exposure requirements
   - Serviceability limits (crack widths, settlement tolerances, deflection limits)
   - Load factors and load combinations
   - Seismic design parameters
2. Collect geotechnical parameters from DEL-02.04 (geotechnical reports):
   - Bearing capacity
   - Settlement parameters
   - Soil properties (unit weight, friction angle, cohesion)
   - Groundwater levels
   - Seismic site class
3. Collect equipment loads from equipment packages (PKG-10, PKG-11, PKG-13, PKG-15):
   - Equipment weights and operating loads
   - Anchor bolt requirements
   - Dynamic loads and vibration if applicable
4. Collect piping loads from PKG-14:
   - Pipe support loads
   - Thrust loads for thrust blocks
5. Create input data register documenting all inputs with sources.
6. Create assumptions register for missing/provisional inputs, flagged as TBD.
7. Identify code requirements and governing clauses (extract from Employer's Requirements or flag as TBD).
8. Apply Guidance Principles P-01 (Traceability) and P-03 (Evidence-Based Code Application).
9. Apply Guidance Consideration C-05 (Assumption Management).

**Outputs:**
- Design basis statement
- Input data register (loads, geotech, materials, code parameters) with source citations
- Assumptions register (provisional parameters, TBD items) with impact assessment
- Code requirements summary with clause references
- Load combination summary

**Verification:**
- All inputs have source citations per Guidance P-01
- Assumptions are clearly identified and flagged as TBD per Guidance C-05
- Code references cite specific clauses (or flagged as TBD) per Guidance P-03
- Input data aligns with DEL-05.02 specification values per Specification IR-01

(Source: Specification.md: FR-02; test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD; Guidance.md: P-01; Guidance.md: P-03; Guidance.md: C-01; Guidance.md: C-05.)

### Step 3: Select Calculation Methodology

**Actions:**
1. Select calculation methodology for each element type based on complexity and criticality:
   - **Hand calculations:** Simple elements (small equipment pads, thrust blocks, preliminary sizing)
   - **Spreadsheets:** Repetitive calculations (multiple equipment pads, parametric studies)
   - **Finite element analysis (FEM):** Complex elements (large tank foundations, containment walls with complex loading, soil-structure interaction)
2. Document methodology selection with justification for each calculation.
3. If using software:
   - Identify software name and version
   - Verify software is validated for intended application
   - Document software capabilities and limitations
   - Define verification approach (hand check key results, comparison to simple models)
4. Apply Guidance Consideration C-04 (Methodology Selection).
5. Consider Guidance Trade-off T-02 (Modeling Detail vs Schedule).

**Outputs:**
- Methodology selection summary (element type → methodology + justification)
- Software description and validation statement (if applicable)
- Verification approach for software calculations

**Verification:**
- Methodology is appropriate to element complexity and criticality per Guidance C-04
- Software use is justified and validated per project QA requirements
- Verification approach is defined for software calculations

(Source: Specification.md: FR-06; Datasheet.md: Attributes; Guidance.md: C-04; Guidance.md: T-02.)

### Step 4: Execute Calculations

**Actions:**
1. **Foundation calculations:** Execute foundation design for each element type per Specification FR-03:
   - Bearing capacity verification
   - Settlement analysis
   - Foundation sizing
   - Reinforcement design
   - Seismic analysis (overturning, sliding, bearing pressure)
   - Document load cases, governing combinations, demand/capacity ratios

2. **Containment wall calculations:** Execute containment wall design per Specification FR-04:
   - Structural design (earth pressure, hydrostatic pressure, wall sizing, reinforcement)
   - Serviceability analysis (crack control, joint design, leakage evaluation) — Apply Guidance P-02 (Containment Sensitivity)
   - Seismic analysis (dynamic earth pressure, stability)
   - Document design checks and verification

3. **Seismic analysis:** Execute seismic design basis and element-specific analysis per Specification FR-05:
   - Define seismic design basis (zone, site class, spectral values, importance factors)
   - Document seismic methodology
   - Perform element-specific seismic analysis (foundations, walls, pads, thrust blocks)
   - Verify seismic performance (strength, deformation, detailing requirements)

4. Document all calculation steps per Guidance P-01 (Traceability):
   - Show all inputs with sources
   - Show all assumptions
   - Show all calculation steps (or retain software input/output files)
   - Summarize results in tables

5. Apply Guidance P-02 (Containment Sensitivity) for containment wall serviceability.
6. Apply Guidance P-04 (Design Optimization Balance) to optimize element sizing.
7. Apply Guidance P-05 (Consistency) to coordinate with DEL-05.01 and DEL-05.02.

**Outputs:**
- Foundation calculations (tank foundations, equipment pads, building foundations, thrust blocks)
- Containment wall calculations (structural, serviceability, seismic)
- Seismic analysis (design basis, methodology, element-specific)
- Calculation results summary tables
- Governing load cases identification

**Verification:**
- All calculation artifacts per Specification FR-01 are complete
- Calculations address strength and serviceability per Specification PR-01
- Seismic performance is verified per Specification PR-02
- Containment wall serviceability supports OBJ-7 per Specification PR-03
- Results are traceable and reproducible per Guidance P-01

(Source: Specification.md: FR-03; Specification.md: FR-04; Specification.md: FR-05; Specification.md: FR-06; Specification.md: PR-01; Specification.md: PR-02; Specification.md: PR-03; Guidance.md: P-01; Guidance.md: P-02; Guidance.md: P-04; Guidance.md: P-05.)

### Step 5: Prepare Calculation Package Documentation

**Actions:**
1. Prepare calculation package cover sheet and index.
2. Prepare design basis section:
   - Design basis statement
   - Input data register
   - Assumptions register
   - Load combination summary
   - Code requirements summary
3. Organize calculations by element type per calculation list (Step 1).
4. Prepare calculation results summary:
   - Summary tables (element sizes, reinforcement quantities, demand/capacity ratios)
   - Governing load cases by element
   - Design verification statement (confirm adequacy per code requirements)
5. Prepare recommendations section:
   - Recommendations for DEL-05.01 drawings (element sizes, reinforcement details, construction notes)
   - Recommendations for DEL-05.02 specifications (material requirements, quality control)
   - Outstanding TBD items requiring resolution
6. Apply Specification FR-06 (Calculation Results and Verification).
7. Apply Specification Documentation requirements.

**Outputs:**
- Complete calculation package with cover, index, design basis, calculations, results summary, recommendations
- Calculation package formatted per project standards (TBD)

**Verification:**
- Calculation package includes all required sections per Specification Documentation
- Results summary is clear and complete per Specification FR-06
- Recommendations support DEL-05.01 and DEL-05.02 development per Specification IR-01

(Source: Specification.md: FR-06; Specification.md: Documentation; Datasheet.md: Construction.)

### Step 6: Conduct Independent Check

**Actions:**
1. **Assign independent checker:** Identify qualified checker (not the calculation originator).
2. **Define check scope:** Independent checker reviews:
   - Calculation logic and methodology
   - Units and dimensional consistency
   - Load case application and load combinations
   - Code compliance and clause citations
   - Arithmetic verification (spot checks or full verification as appropriate)
   - Results reasonableness (compare to engineering judgment, simple estimates, similar projects)
   - Assumption reasonableness and impact
   - Traceability and reproducibility
3. **Independent checker review:** Checker performs review and documents findings in check comments.
4. **Address check comments:**
   - Review all check comments with originator
   - Resolve comments (accept, reject with justification, or modify calculations)
   - Document comment resolution
   - Update calculations as needed
5. **Checker sign-off:** Checker reviews resolutions and signs off on calculation package.
6. Apply Specification QR-02 (Independent Check).
7. Apply Guidance P-01 (Traceability — checker must be able to reproduce results).

**Outputs:**
- Independent check comments and findings
- Comment resolution log
- Updated calculations incorporating accepted check comments
- Checker sign-off on calculation package

**Verification:**
- Independent check covers all Specification QR-02 requirements
- All check comments are addressed and documented
- Checker sign-off confirms calculations are adequate
- Calculations are traceable and reproducible per Guidance P-01

(Source: Specification.md: QR-02; test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Guidance.md: P-01; Procedure.md: Verification.)

### Step 7: Finalize and Issue Calculation Package

**Actions:**
1. Finalize calculation package and update revision status per project document control.
2. Apply document control metadata (calculation number, revision, approval signatures, issue date).
3. Generate issue copies per project requirements (PDF, calculation files).
4. Assemble issue package:
   - Calculation package document (cover, index, design basis, calculations, results, recommendations)
   - Calculation files (spreadsheets, FEM models, hand calculations)
   - Check records (check comments, resolutions, sign-off)
5. Update Datasheet metadata (document number, revision, status).
6. Submit issue package per project document control process (electronic submission requirements **TBD**).
7. Update `_STATUS.md` to next lifecycle state per project process (e.g., IN_PROGRESS → CHECKING → ISSUED).
8. Coordinate calculation results with DEL-05.01 (drawings) and DEL-05.02 (specifications) development.

**Outputs:**
- Issued calculation package (PDF and calculation files)
- Check records
- Updated Datasheet and `_STATUS.md`

**Verification:**
- Calculation package is complete and includes all required content
- Document control metadata is complete and consistent with Datasheet per Specification QR-01
- All required records are assembled and complete
- Issue package meets project document control requirements
- `_STATUS.md` lifecycle state is updated appropriately
- Calculation results are coordinated with DEL-05.01 and DEL-05.02 per Specification IR-01

(Source: Specification.md: QR-01; Specification.md: IR-01; Specification.md: Documentation; Datasheet.md: Attributes; test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD.)

## Verification

### Completeness Verification (Maps to Specification Verification)

**Calculation artifacts present and complete:**
- Foundation calculations (tank foundations, equipment pads, building foundations, thrust blocks) — Specification FR-03
- Containment wall calculations (structural, serviceability, seismic) — Specification FR-04
- Seismic analysis (design basis, methodology, element-specific) — Specification FR-05
- Design basis and assumptions documentation — Specification FR-02
- Calculation results summary and recommendations — Specification FR-06

**Verification method:** Review calculation package content against Specification FR-01 and Datasheet Construction artifacts. Confirm each anticipated artifact is present and complete. (Source: Specification.md: FR-01; Datasheet.md: Construction; Procedure Step 1.)

### Alignment Verification (Maps to Specification Verification)

**Cross-deliverable consistency:**
- Calculation results (element sizing, reinforcement) align with DEL-05.01 drawing dimensions and details — Specification IR-01
- Material properties (concrete strength, modulus) align with DEL-05.02 specification values — Specification IR-01
- Geotechnical inputs align with DEL-02.04 geotechnical reports — Specification IR-01
- Load inputs align with equipment/piping data from source packages — Specification IR-01

**Verification method:** Conduct coordination review (implicitly during Step 4 and Step 7) to confirm alignment with DEL-05.01, DEL-05.02, and input sources. Document alignment in assumptions register and recommendations section. (Source: Specification.md: IR-01; Guidance.md: P-05; Procedure Steps 4 and 7.)

### Performance Verification (Maps to Specification Verification)

**Design adequacy:**
- Strength verification under factored loads per code requirements — Specification PR-01
- Serviceability verification (crack control, settlement, deflection) per design criteria — Specification PR-01
- Seismic performance verification per seismic design basis — Specification PR-02
- Containment wall crack control supports OBJ-7 Environmental Protection — Specification PR-03
- Foundation settlement within allowable limits — Specification PR-01

**Verification method:** Independent check (Step 6) verifies design adequacy and code compliance. Checker reviews strength/serviceability verification and seismic performance. (Source: Specification.md: PR-01; Specification.md: PR-02; Specification.md: PR-03; Procedure Step 6.)

### Quality Verification (Maps to Specification Verification)

**Traceability and quality:**
- Calculations are traceable and reproducible (inputs, assumptions, steps documented) — Specification QR-03
- Independent check is complete with findings addressed — Specification QR-02
- Document control metadata matches Datasheet — Specification QR-01
- Assumptions are identified and tracked per assumptions register — Specification FR-02

**Verification method:** Independent check (Step 6) verifies traceability per Guidance P-01. Document control verification (Step 7) confirms metadata consistency. (Source: Specification.md: QR-01; Specification.md: QR-02; Specification.md: QR-03; Guidance.md: P-01; Procedure Steps 6 and 7.)

## Records

**Calculation package deliverables:**
- Foundation calculations (tank foundations, equipment pads, building foundations, thrust blocks)
- Containment wall calculations (structural, serviceability, seismic)
- Seismic analysis (design basis, methodology, element-specific)
- Design basis and assumptions documentation
- Calculation results summary and recommendations
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234; Datasheet.md: Construction; Specification.md: Documentation.)

**Supporting documentation:**
- Calculation package cover sheet and index
- Input data register with source citations
- Assumptions register with TBD tracking
- Load combination summary
- Calculation methodology description

**QA/QC records:**
- Independent check comments and findings
- Comment resolution log
- Checker sign-off and approval records
- Calculation files (spreadsheets, FEM models, hand calculations)
- Revision history per project document control (**TBD**)
(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Specification.md: Documentation; Procedure Step 6.)

**Project records:**
- Issued calculation package files (PDF and calculation files)
- Document transmittal and submission records
- Updated Datasheet metadata
- Updated `_STATUS.md` lifecycle state
(Source: Specification.md: Documentation; Procedure Step 7.)

## Procedure Steps Traceability

| Procedure Step | Specification Requirements Verified | Guidance Principles/Considerations Applied | Datasheet Sections Addressed |
|----------------|-------------------------------------|-------------------------------------------|------------------------------|
| Step 1: Define Scope and Create List | FR-01 Artifact Coverage | E-01 Organization | Construction (all artifacts) |
| Step 2: Assemble Design Basis and Input Data | FR-02 Design Basis, IR-01, IR-02 | P-01 Traceability, P-03 Evidence-Based, C-01, C-05 | Conditions (TBD items), Construction: Supporting Docs |
| Step 3: Select Calculation Methodology | FR-06, Standards | C-04 Methodology, T-02 Modeling Detail | Attributes (Software/Tools) |
| Step 4: Execute Calculations | FR-03, FR-04, FR-05, PR-01, PR-02, PR-03 | P-01, P-02, P-04, P-05, C-02, C-03 | Construction (all calculation sets) |
| Step 5: Prepare Documentation | FR-06, Documentation | P-01 Traceability, E-01 Organization | Construction: Supporting Docs |
| Step 6: Conduct Independent Check | QR-02, QR-03 | P-01 Traceability | — (verification) |
| Step 7: Finalize and Issue | QR-01, IR-01 | P-05 Consistency | Attributes (Document Number, Revision) |

## Cross-Document Notes

- **Specification:** This Procedure's steps (Steps 1-7) and verifications demonstrate compliance with all `Specification.md` requirements (§FR-01 through §QR-03). The Procedure Steps Traceability table above maps each step to the Specification requirements it addresses. (Source: Specification.md: Requirements; Specification.md: Requirements Traceability Matrix; Specification.md: Verification.)
- **Guidance:** Use `Guidance.md` Principles (§P-01 through §P-05), Considerations (§C-01 through §C-05), Trade-offs (§T-01 through §T-04), and Examples (§E-01 through §E-03) to inform how calculations are developed. The Procedure Steps Traceability table above maps each step to the Guidance sections that inform execution. (Source: Guidance.md: Principles; Guidance.md: Considerations; Guidance.md: Trade-offs; Guidance.md: Examples; Guidance.md: Guidance-to-Specification Traceability.)
- **Datasheet:** `Datasheet.md` §Construction lists the calculation artifacts that Steps 1, 4, and 5 must produce. §Attributes define the metadata requirements that Steps 5 and 7 must implement. §Cross-Document Traceability identifies the linkages this Procedure must maintain. (Source: Datasheet.md: Construction; Datasheet.md: Attributes; Datasheet.md: Cross-Document Traceability.)
