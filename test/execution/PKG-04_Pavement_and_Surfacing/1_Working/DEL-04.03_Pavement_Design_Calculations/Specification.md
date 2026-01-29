# Specification: DEL-04.03 Pavement Design Calculations

## Scope

### Included
This specification defines the requirements for producing the Pavement Design Calculations (DEL-04.03), which provide the engineering basis and structural validation for pavement sections shown in DEL-04.01 and specified in DEL-04.02.

The calculations shall include:
- Pavement structural analysis and layer thickness determination
- Traffic loading analysis and load distribution
- Subgrade bearing capacity evaluation
- Material property selection and validation
- Structural capacity verification (stress, strain, deflection, fatigue analysis)
- Sensitivity analysis for design parameter variations
- OBJ-8 Phase 2 expansion corridor ultimate loading analysis
- Interface design validation for transitions to adjacent work packages

### Excluded
- Detailed pavement layout and grading design (covered by DEL-04.01)
- Material specifications and construction workmanship requirements (covered by DEL-04.02)
- Field testing and quality control procedures (covered by DEL-04.04)
- Pavement life cycle cost analysis (unless specifically required by ER)
- Pavement maintenance and rehabilitation design (future work)

## Requirements

### R1: Calculation Input Requirements

#### R1.1: Traffic Loading Data
**Requirement**: The calculations shall be based on documented traffic loading data including:
- Vehicle types and classifications (heavy trucks, railcar movers, light vehicles, construction equipment)
- Axle loads (single, tandem, tridem) in kN or equivalent
- Tire pressures in kPa
- Traffic volume (vehicles per day or annual repetitions)
- Traffic growth rate over design life (if applicable)
- Load distribution (directional, lane distribution, wander)
- Equivalent Single Axle Load (ESAL) computation or load spectra for mechanistic analysis

**Source**: Owner/ER traffic data (**TBD** – if not provided, document assumed loading based on facility operational requirements and flag as **ASSUMPTION**)
**Verification**: Traffic loading assumptions reviewed with Owner/Engineer and approved prior to final calculation issuance

#### R1.2: Geotechnical Parameters
**Requirement**: The calculations shall be based on documented geotechnical parameters including:
- Subgrade soil classification (USCS or AASHTO)
- Subgrade bearing capacity: California Bearing Ratio (CBR) or resilient modulus (Mr) in MPa
- Compaction requirements: Standard Proctor maximum dry density and optimum moisture content (ASTM D698)
- Frost depth and frost susceptibility
- Groundwater elevation and seasonal variation
- Soil strength variation (spatial variability for sensitivity analysis)

**Source**: Geotechnical investigation report (**TBD** – if not available, document assumed values based on regional soil data and flag as **ASSUMPTION**)
**Verification**: Geotechnical assumptions reviewed with geotechnical engineer and approved prior to final calculation issuance

#### R1.3: Material Properties
**Requirement**: The calculations shall use material properties consistent with DEL-04.02 specification:

**Asphalt Materials**:
- Asphalt binder grade (PG grading): Source from DEL-04.02 (reference Datasheet **ASSUMPTION**: PG 58-34)
- Asphalt mix dynamic modulus or resilient modulus at design temperature: Use laboratory test data or correlations from mix design
- Asphalt mix fatigue characteristics: Use laboratory test data or design manual relationships (TAC, AASHTO)
- Poisson's ratio: 0.35 typical (**ASSUMPTION**)

**Concrete Materials** (if concrete pavement zones exist):
- 28-day compressive strength: Source from DEL-04.02 (reference Datasheet **ASSUMPTION**: 30-35 MPa)
- Flexural strength (modulus of rupture): Use laboratory test data or correlation (e.g., 0.6√f'c MPa per ACI 318)
- Elastic modulus: Use laboratory test data or correlation (e.g., 4700√f'c MPa per ACI 318)
- Poisson's ratio: 0.15 typical (**ASSUMPTION**)

**Base/Subbase Materials**:
- Resilient modulus: Use laboratory test data or correlations based on material type and stress state
- Poisson's ratio: 0.35-0.40 typical (**ASSUMPTION**)

**Source**: DEL-04.02 material specifications; laboratory test data; design manual correlations
**Verification**: Material properties reviewed with DEL-04.02 specification author for consistency

#### R1.4: Environmental and Climatic Data
**Requirement**: The calculations shall consider environmental factors:
- Design temperature: Mean annual air temperature (MAAT) for pavement modulus adjustment
- Freeze-thaw cycles: Number per year affecting pavement durability
- Frost depth: For frost protection thickness determination
- Drainage conditions: Surface drainage per DEL-04.01; subdrainage if required

**Source**: Climate data for Fraser Surrey, BC; geotechnical report recommendations
**Verification**: Environmental assumptions reviewed and documented

### R2: Calculation Methodology Requirements

#### R2.1: Design Approach and Standards
**Requirement**: The calculations shall follow a recognized pavement design methodology:
- **Flexible pavement (asphalt)**: TAC Pavement Design Manual mechanistic-empirical method OR AASHTO Guide for Design of Pavement Structures (**TBD** – confirm from ER requirements)
- **Rigid pavement (concrete)**: PCA method OR AASHTO rigid pavement design method (**TBD** – confirm from ER)
- **Design life**: 25 years minimum (reference Datasheet **ASSUMPTION** – confirm from ER)
- **Reliability level**: 90% minimum (reference Datasheet **ASSUMPTION** – confirm from ER performance requirements)

**Source**: Employer's Requirements design criteria (**location TBD**); TAC or AASHTO design manuals
**Verification**: Design methodology reviewed and approved by Engineer prior to calculation execution

#### R2.2: Structural Analysis Method
**Requirement**: Pavement structural analysis shall use:
- **Layered elastic analysis**: Multi-layer elastic theory (Burmister theory or equivalent) for stress/strain computation
- **Software**: Recognized pavement analysis software (e.g., KENPAVE, CIRCLY, MEPDG) with documented validation (**TBD** – specify software and version)
- **Critical response parameters**:
  - Tensile strain at bottom of asphalt layer (fatigue criterion)
  - Compressive stress/strain on subgrade (rutting criterion)
  - Surface deflection (optional verification check)

**Source**: Pavement design manual methodology; software user manuals
**Verification**: Software validation documentation provided; calculation methodology peer-reviewed

#### R2.3: Load Distribution and Analysis
**Requirement**: Traffic loading shall be analyzed considering:
- **Load configuration**: Single, tandem, or tridem axles per actual vehicle configurations
- **Tire contact area**: Circular or equivalent rectangular contact area based on tire pressure
- **Load distribution**: Elastic layer theory distribution through pavement structure
- **Critical loading position**: Positioned to produce maximum critical stress/strain
- **Cumulative damage**: Fatigue damage accumulation over design life (Miner's rule or equivalent)

**Source**: TAC or AASHTO load analysis procedures
**Verification**: Load distribution assumptions and critical loading positions documented and reviewed

#### R2.4: Sensitivity Analysis
**Requirement**: Sensitivity analysis shall be performed to evaluate effect of input parameter variations:
- **Subgrade sensitivity**: ±20% variation in CBR or resilient modulus
- **Traffic sensitivity**: ±20% variation in traffic volume (ESALs)
- **Material property sensitivity**: ±10% variation in asphalt modulus
- **Results presentation**: Tabulate effect of each parameter variation on required pavement thickness

**Source**: Standard sensitivity analysis practice
**Verification**: Sensitivity analysis results reviewed and documented

#### R2.5: OBJ-8 Phase 2 Expansion Analysis
**Requirement**: For pavement zones designated as Phase 2 expansion corridors per OBJ-8:
- Analyze pavement structural adequacy under ultimate Phase 2 loading (increased traffic volume and/or heavier vehicles – **TBD** from Owner Phase 2 requirements)
- Compare Phase 1 loading case with ultimate Phase 2 loading case
- Document required pavement thickness for ultimate loading
- If Phase 1 pavement is designed for ultimate loading, document capacity reserve available during Phase 1 operations

**Source**: OBJ-8 objectives (Decomposition Section 6); Owner Phase 2 requirements (**TBD**)
**Verification**: OBJ-8 analysis reviewed and approved by Engineer

### R3: Calculation Output Requirements

#### R3.1: Output Summary Table
**Requirement**: Calculation outputs shall be summarized in tabular format including:
- Pavement zone description (reference DEL-04.01 plan sheet and section number)
- Design traffic loading (ESALs or load spectrum)
- Subgrade bearing capacity (CBR or Mr)
- Layer thicknesses: wearing course, binder course, base course, subbase (in mm)
- Total pavement thickness (mm)
- Critical stresses/strains and safety factors
- Cross-reference to DEL-04.01 drawing section and DEL-04.02 specification clause

**Source**: Calculation analysis results
**Verification**: Output summary reviewed for consistency with DEL-04.01 drawings and DEL-04.02 specifications

#### R3.2: Traceability to Drawings and Specifications
**Requirement**: Each calculated pavement thickness shall be cross-referenced to:
- DEL-04.01 drawing sheet number and section/detail number where thickness is shown
- DEL-04.02 specification clause number governing materials and construction
- DEL-04.04 test record requirement for thickness verification

**Source**: Traceability matrix per Procedure
**Verification**: Cross-references audited by QA reviewer

#### R3.3: Assumption and Limitation Documentation
**Requirement**: All calculation assumptions and limitations shall be documented including:
- Traffic loading assumptions (if Owner data not provided)
- Geotechnical assumptions (if investigation data not available)
- Material property assumptions (if laboratory test data not available)
- Design methodology limitations (applicable range, exclusions)
- Each assumption flagged as **ASSUMPTION** with reference to assumption tracking log

**Source**: Calculation inputs and design approach
**Verification**: Assumptions reviewed and logged per Procedure; resolution paths identified

### R4: Calculation Verification and Review Requirements

#### R4.1: Self-Check
**Requirement**: Calculation author shall perform self-check including:
- Arithmetic verification (recalculate or use alternate method)
- Unit consistency check (all inputs and outputs have correct units)
- Reasonableness check (results are within expected range for similar projects)
- Input traceability check (all inputs have documented sources)

**Source**: Calculation quality assurance procedures
**Verification**: Self-check signoff by calculation author

#### R4.2: Independent Check
**Requirement**: Senior engineer or independent checker shall review:
- Design methodology appropriate for project conditions
- Input data sources and assumptions reasonable and documented
- Calculation execution correct (software inputs, formulas, logic)
- Output results reasonable and consistent with DEL-04.01/DEL-04.02
- Sensitivity analysis adequate and properly interpreted

**Source**: Calculation quality assurance procedures
**Verification**: Independent check signoff by checker

#### R4.3: Cross-Document Coordination Review
**Requirement**: QA reviewer shall verify:
- Calculated thicknesses match DEL-04.01 drawing sections (or identify discrepancies)
- Material properties match DEL-04.02 specifications (or identify discrepancies)
- Calculation outputs provide target values for DEL-04.04 testing
- Assumptions logged in coordinated assumption tracking system

**Source**: Guidance review checklist; Procedure coordination requirements
**Verification**: Cross-document coordination review signoff by QA reviewer

### R5: Calculation Revision Requirements

#### R5.1: Revision Triggers
**Requirement**: Calculations shall be revised when:
- DEL-04.01 drawings are revised (new pavement zones, layout changes, revised elevations)
- DEL-04.02 specifications are revised (material changes requiring property updates)
- New geotechnical data becomes available (updated CBR, soil properties)
- Traffic loading data is updated or refined
- Employer's Requirements are clarified or revised
- Calculation errors or omissions are identified

**Source**: Configuration management procedures
**Verification**: Revision triggers documented in calculation revision history

#### R5.2: Revision Documentation
**Requirement**: Each calculation revision shall include:
- Updated revision number (Rev 1, Rev 2, etc.)
- Revision date and author/checker
- Summary of changes (what was revised and why)
- Superseded calculation clearly marked and retained for traceability
- Re-check per R4.1, R4.2, R4.3 requirements

**Source**: Calculation quality assurance procedures
**Verification**: Revision history complete and approved

## Standards

### Design Standards and Codes
- **TAC Pavement Design and Rehabilitation Manual** (latest edition): Canadian pavement design methodology (**ASSUMPTION** – confirm from ER)
- **AASHTO Guide for Design of Pavement Structures** (1993 with supplements, or latest edition): Alternative pavement design methodology (**ASSUMPTION** – confirm from ER)
- **PCA Thickness Design for Concrete Highway and Street Pavements**: Concrete pavement design method (if applicable)
- **ASTM D698**: Standard Proctor compaction test (for subgrade correlation)
- **CSA A23.1**: Concrete materials properties (if concrete pavement)

### Analysis Software Standards (**TBD**)
- Software name, version, and validation documentation
- Software developer and technical support contact
- Applicable standards or manuals governing software use

## Verification

### Verification Methods

| Requirement | Verification Method | Responsible Party | Timing |
|-------------|-------------------|-------------------|--------|
| R1.1: Traffic loading | Review traffic data sources; approve assumptions | Engineer + Owner | Before analysis |
| R1.2: Geotechnical | Review geotechnical report; approve assumptions | Geotechnical engineer | Before analysis |
| R1.3: Material properties | Cross-check vs. DEL-04.02 specifications | DEL-04.02 author | During analysis |
| R1.4: Environmental data | Review climate data sources | Engineer | Before analysis |
| R2.1: Design approach | Review and approve methodology | Engineer | Before analysis |
| R2.2: Structural analysis | Review software validation; peer review | Senior engineer | During analysis |
| R2.3: Load distribution | Review load configurations and positions | Checker | During analysis |
| R2.4: Sensitivity analysis | Review parameter variations and results | Checker | During analysis |
| R2.5: OBJ-8 analysis | Review Phase 2 loading assumptions | Engineer + Owner | During analysis |
| R3.1: Output summary | Review summary table completeness | QA reviewer | After analysis |
| R3.2: Traceability | Audit cross-references via traceability matrix | QA reviewer | After analysis |
| R3.3: Assumptions | Review assumption log and resolution paths | QA reviewer | Each review cycle |
| R4.1: Self-check | Signoff by calculation author | Calculation author | After analysis |
| R4.2: Independent check | Signoff by checker | Senior engineer | After analysis |
| R4.3: Coordination review | Signoff by QA reviewer | QA reviewer | Before issuance |
| R5.1: Revision triggers | Document trigger in revision history | Calculation author | Each revision |
| R5.2: Revision documentation | Review revision history completeness | Checker | Each revision |

### Acceptance Criteria
- All calculation inputs (traffic, geotechnical, material properties, environmental) are documented with sources or flagged as **ASSUMPTION** with resolution paths
- Design methodology follows recognized standard (TAC, AASHTO, PCA) and is approved by Engineer
- Structural analysis software is validated and documented
- Sensitivity analysis demonstrates design robustness to parameter variations
- OBJ-8 Phase 2 analysis validates expansion corridor capacity
- Output summary table is complete with cross-references to DEL-04.01, DEL-04.02, DEL-04.04
- Traceability matrix demonstrates complete linkage to drawings and specifications
- Self-check, independent check, and coordination review signoffs obtained
- All **ASSUMPTION** items are logged with resolution paths

## Documentation

### Required Documentation Outputs
1. **Calculation Report**: Narrative describing design basis, inputs, methodology, analysis, results, conclusions
2. **Input Summary Tables**: Tabulated inputs (traffic, geotechnical, material properties) with sources
3. **Analysis Worksheets**: Calculation steps (hand calculations or software input/output sheets)
4. **Output Summary Table**: Pavement thicknesses, stresses/strains, safety factors, with cross-references per R3.1
5. **Sensitivity Analysis Results**: Parameter variation study results per R2.4
6. **OBJ-8 Phase 2 Analysis**: Ultimate loading case results per R2.5
7. **Traceability Matrix**: Cross-references to DEL-04.01, DEL-04.02, DEL-04.04 per R3.2
8. **Assumption Tracking Log**: **ASSUMPTION** and **TBD** items with resolution paths per R3.3
9. **References**: List of design standards, software manuals, geotechnical reports, test data
10. **Revision History**: Summary of calculation revisions per R5.2
11. **Approval Signoffs**: Self-check, independent check, coordination review signoffs per R4.1–R4.3

### Document Handoff Requirements
- **To DEL-04.01**: Provide pavement thickness outputs for drawing section details; notify of any discrepancies requiring drawing revision
- **To DEL-04.02**: Provide material property assumptions for specification validation; notify of any material changes requiring specification revision
- **To DEL-04.04**: Provide output summary table with target thicknesses and acceptance criteria for field testing; provide sensitivity analysis results to inform testing frequency and locations

## References

### Source Documents
- **Decomposition**: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section PKG-04, DEL-04.03, OBJ-8 mapping
- **Datasheet (DEL-04.03)**: Calculation Scope, Design Inputs, Calculation Outputs, Assumptions & TBDs, Cross-document Coordination
- **Guidance (DEL-04.03)**: Review Checklist
- **Procedure (DEL-04.03)**: Workflow Steps, Controls, traceability matrix and assumption log
- **Employer's Requirements Volume 2 Part 2**: Civil & Process Mechanical Works, pavement design criteria (**location TBD**)

### Related Deliverables
- **DEL-04.01**: Pavement Design Drawing Set (graphical representation of calculated pavement sections)
- **DEL-04.02**: Pavement Technical Specification (material properties and construction requirements used as calculation inputs)
- **DEL-04.04**: Pavement Installation & Test Records (field verification of calculated design)
