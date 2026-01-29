# Datasheet: DEL-04.03 Pavement Design Calculations

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-04.03 |
| Name | Pavement Design Calculations |
| Package | PKG-04 Pavement & Surfacing |
| Discipline | Civil |
| Type | Calculation |
| Responsible | D&B Contractor |
| Status | INITIALIZED |
| Objective | OBJ-8 Future Expandability (Phase 2) |

## Attributes

### Calculation Scope
This calculation package provides the engineering basis and verification for all pavement structural design shown in DEL-04.01 and specified in DEL-04.02, including:

- **Pavement layer thickness determination**: Asphalt wearing course, binder course, base course, subbase thicknesses based on traffic loading and subgrade conditions
- **Concrete pavement design**: Slab thickness, reinforcement requirements, joint spacing for concrete surfacing zones
- **Load analysis**: Vehicle loading spectra (heavy trucks, railcar movers, light vehicles), axle configurations, repetition counts, load distribution
- **Structural capacity verification**: Stress analysis, deflection analysis, fatigue life prediction under design loading
- **Subgrade bearing capacity evaluation**: CBR-based design or resilient modulus-based design with geotechnical parameters
- **Sensitivity analysis**: Parametric studies showing effect of varying geotechnical conditions, traffic loads, or material properties on pavement thickness
- **OBJ-8 future expansion analysis**: Design validation for Phase 2 expansion corridor pavement loaded to ultimate Phase 2 capacity
- **Interface design validation**: Pavement transitions at structure interfaces (PKG-05), utility crossings (PKG-03), rail embedments (PKG-07), wharf edges (PKG-08)

### Calculation Methodology

#### Design Approach (**ASSUMPTION** – pending ER confirmation)
- **Flexible pavement (asphalt)**: Layered elastic analysis or mechanistic-empirical pavement design per TAC Pavement Design Manual or AASHTO Pavement Design Guide (**TBD**: confirm design methodology from ER)
- **Rigid pavement (concrete)**: PCA method or AASHTO rigid pavement design method (**TBD**: confirm from ER)
- **Design life**: 25 years for initial Phase 1 construction; ultimate Phase 2 loading for expansion corridors (**ASSUMPTION**: 25-year life – confirm from ER)
- **Reliability level**: 90-95% reliability typical for industrial pavements (**ASSUMPTION** – to be confirmed from ER performance requirements)

#### Design Software/Tools (**TBD**)
- Pavement analysis software (e.g., KENPAVE, CIRCLY, MEPDG, or equivalent)
- Spreadsheet calculations for simple sections or verification checks
- Finite element analysis (if required for complex geometry or loading)

### Design Inputs

#### Traffic Loading Data (**TBD** – pending Owner/ER data)
- **Heavy trucks**: Axle loads (single, tandem, tridem), tire pressures, repetitions per day, growth factor
- **Railcar movers**: Axle loads, wheel configurations, operational patterns, repetitions
- **Light vehicles**: Car/pickup truck loading for parking areas and access roads
- **Construction equipment**: Temporary loading during construction phase (if critical)
- **Load spectra**: Distribution of load magnitudes over design life (ESAL equivalent or load spectra for mechanistic analysis)
- **Directional distribution**: Traffic channelization, wander (lane width effects on stress distribution)

#### Geotechnical Parameters (**TBD** – pending geotechnical investigation report)
- **Subgrade soil type**: Soil classification (USCS or AASHTO), plasticity index, moisture susceptibility
- **Subgrade bearing capacity**: CBR value (in-situ or laboratory) or resilient modulus (Mr) from laboratory testing
- **Frost susceptibility**: Frost depth, frost heave potential, thaw weakening effects (Fraser Surrey, BC climate)
- **Groundwater elevation**: Depth to groundwater, seasonal variation, effect on subgrade strength
- **Compaction characteristics**: Optimum moisture content, maximum dry density (Standard Proctor per ASTM D698)

#### Material Properties

**Asphalt Materials** (reference DEL-04.02 material specifications):
- **Asphalt binder**: Performance Grade (PG 58-34 **ASSUMPTION**), temperature-stiffness relationship
- **Asphalt mix modulus**: Dynamic modulus or resilient modulus at design temperature (typically 20°C for BC climate – **ASSUMPTION**)
- **Fatigue characteristics**: Asphalt mix fatigue life relationship (strain-based or stress-based)
- **Poisson's ratio**: Typically 0.35 for asphalt concrete (**ASSUMPTION** per industry standards)

**Concrete Materials** (reference DEL-04.02 material specifications):
- **28-day compressive strength**: 30-35 MPa (**ASSUMPTION** – to be confirmed from DEL-04.02)
- **Flexural strength (modulus of rupture)**: Typically 10-15% of compressive strength, or direct testing (**ASSUMPTION**)
- **Elastic modulus**: Approximately 4700√f'c MPa per ACI 318, where f'c is compressive strength in MPa (**ASSUMPTION**)
- **Poisson's ratio**: 0.15 for concrete (**ASSUMPTION** per industry standards)

**Base/Subbase Materials** (reference DEL-04.02 material specifications):
- **Resilient modulus**: Depends on material type and stress state; typically 150-300 MPa for granular base (**ASSUMPTION**)
- **Poisson's ratio**: 0.35-0.40 for granular materials (**ASSUMPTION**)

#### Environmental/Climatic Data
- **Design temperature**: Mean annual air temperature (MAAT) for Fraser Surrey, BC: approximately 10°C (**ASSUMPTION** – to be confirmed from climate data)
- **Freeze-thaw cycles**: Number of freeze-thaw cycles per year affecting pavement durability
- **Precipitation**: Drainage design affected by rainfall intensity (coordinates with PKG-03 drainage design)

### Calculation Outputs

#### Pavement Section Design Results
For each pavement zone shown in DEL-04.01:
- **Layer thicknesses** (mm): Wearing course, binder course, base course, subbase
- **Total pavement thickness** (mm): Sum of all layers
- **Cross-reference**: DEL-04.01 drawing sheet and section number where thickness is shown
- **Acceptance criteria**: Structural capacity (stress, strain, deflection) meets or exceeds design requirements with specified reliability

#### Structural Performance Verification
- **Critical stresses/strains**: Tensile strain at bottom of asphalt layer (fatigue criterion), compressive stress/strain on subgrade (rutting criterion)
- **Deflection**: Surface deflection under design load (optional check, not typically governing for new pavement design)
- **Safety factors**: Ratio of allowable to calculated stress/strain (typically ≥1.0 for limit state design, or per design methodology)
- **Fatigue life**: Predicted pavement life in equivalent single axle loads (ESALs) or years under traffic loading

#### Sensitivity Analysis Results
- **Subgrade sensitivity**: Effect of ±20% variation in CBR or Mr on required pavement thickness
- **Traffic sensitivity**: Effect of ±20% variation in traffic volume (ESALs) on pavement thickness
- **Material property sensitivity**: Effect of ±10% variation in asphalt modulus on critical strains
- **OBJ-8 expansion corridors**: Comparison of Phase 1 loading vs. ultimate Phase 2 loading on required thickness

#### Interface Design Validation
- **Transition zones**: Pavement thickness transitions at structure interfaces, calculated to minimize differential deflection
- **Utility crossings**: Pavement loading analysis over utility trenches (backfill compaction requirements validated)
- **Rail embedments**: Pavement structural adequacy adjacent to rail works (vibration and load transfer considerations)

### Conditions

#### Design Assumptions (**ASSUMPTION** unless otherwise noted)
1. Design methodology: TAC Pavement Design Manual or AASHTO Pavement Design Guide (mechanistic-empirical approach)
2. Design life: 25 years for Phase 1; ultimate loading for OBJ-8 Phase 2 expansion corridors
3. Reliability: 90% (typical for industrial pavement)
4. Traffic growth rate: 2% annual growth over design life (if traffic data provided; otherwise 0% growth – **TBD**)
5. Subgrade frost protection: Subbase thickness provides adequate frost protection (minimum 600 mm granular cover typical for BC frost depth – **ASSUMPTION**)
6. Drainage: Surface drainage per DEL-04.01; subdrainage provided if required by geotechnical conditions (**TBD**)

#### Limitations and Exclusions
- Dynamic loading analysis (impact, vibration) not included unless specifically required by ER (**ASSUMPTION** – static loading governs)
- Pavement life cycle cost analysis not included unless specifically required by ER (**ASSUMPTION**)
- Pavement maintenance planning and overlay design not included (future Phase work)
- Specialty pavements (permeable pavement, porous asphalt, etc.) not included unless shown in DEL-04.01

## Construction

### Calculation Deliverables
The calculation package shall include:

1. **Calculation Report**: Narrative describing design approach, inputs, methodology, results, conclusions
2. **Input Summary Tables**: Tabulated design inputs (traffic, geotechnical, material properties) with sources
3. **Analysis Worksheets**: Step-by-step calculations (hand calculations or software input/output sheets)
4. **Output Summary Tables**: Pavement section thicknesses, stresses/strains, safety factors, with cross-references to DEL-04.01 drawings
5. **Sensitivity Analysis Results**: Parametric study results showing effect of input variations
6. **OBJ-8 Phase 2 Analysis**: Ultimate loading case for expansion corridors
7. **References**: List of design standards, software manuals, material test reports, geotechnical reports

### Calculation Verification and Review
- **Self-check**: Calculation author performs self-check (arithmetic verification, unit consistency, reasonableness check)
- **Independent check**: Senior engineer or checker reviews calculation methodology, inputs, and results
- **Cross-document coordination check**: QA reviewer verifies calculation outputs match DEL-04.01 drawing sections and DEL-04.02 specification requirements

### Calculation Revision Control
- **Revision numbering**: Initial issue Rev 0; subsequent revisions Rev 1, Rev 2, etc.
- **Revision history**: Summary of changes, reason for revision (e.g., "Updated subgrade CBR from geotechnical report"), date, author/checker
- **Superseded calculations**: Previous calculation revisions retained for reference and traceability

## References

### Source Documents
- **Decomposition**: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section PKG-04, DEL-04.03, OBJ-8 mapping
- **Employer's Requirements Volume 2 Part 2**: Civil & Process Mechanical Works, pavement design requirements (**location TBD** – requires detailed review)
- **Package Reference Index**: `test/execution/PKG-04_Pavement_and_Surfacing/0_References/_REFERENCE_INDEX.md`
- **Geotechnical Investigation Report**: Site-specific soils data (**TBD** – not yet available)
- **Traffic Loading Data**: Owner-provided traffic loading spectra (**TBD** – not yet provided)

### Related Deliverables (Cross-references)
- **DEL-04.01**: Pavement Design Drawing Set – graphical representation of pavement sections validated by these calculations
- **DEL-04.02**: Pavement Technical Specification – material properties and construction requirements used as calculation inputs
- **DEL-04.04**: Pavement Installation & Test Records – field testing validates that as-built pavement conforms to calculated design
- **PKG-03 geotechnical deliverables** (if applicable): Geotechnical investigation report providing subgrade properties
- **PKG-05 structural deliverables**: Structure loading and elevations for pavement interface design
- **PKG-07 rail deliverables**: Track loading and vibration data for pavement design adjacent to rail works

### Design Standards & Codes (**ASSUMPTION** – pending ER confirmation)
- **TAC Pavement Design and Rehabilitation Manual**: Canadian pavement design methodology
- **AASHTO Guide for Design of Pavement Structures**: Alternate pavement design methodology (flexible and rigid pavements)
- **PCA**: Portland Cement Association concrete pavement design method (if rigid pavement zones exist)
- **ASTM D698**: Standard Proctor test for subgrade compaction correlation
- **CSA A23.1**: Concrete materials properties (if concrete pavement zones exist)

### Analysis Software/Tools (**TBD**)
- Pavement analysis software name and version (e.g., KENPAVE 1.0, CIRCLY 6.0, AASHTOWare Pavement ME Design 2.6)
- Software validation/verification documentation (required for QA purposes)

## Assumptions & TBDs

### Assumptions Requiring Validation
1. **ASSUMPTION**: Design methodology TAC Pavement Design Manual or AASHTO Guide – confirm from ER design requirements
2. **ASSUMPTION**: Design life 25 years – confirm from ER or project requirements
3. **ASSUMPTION**: Reliability 90% – confirm from ER performance requirements
4. **ASSUMPTION**: Traffic growth rate 2% annual – confirm from Owner traffic projections or use 0% if not provided
5. **ASSUMPTION**: Asphalt mix modulus and fatigue properties typical for BC dense-graded HMA – laboratory testing recommended for final design
6. **ASSUMPTION**: Concrete flexural strength 10-15% of compressive strength – laboratory testing recommended if concrete pavement zones are extensive
7. **ASSUMPTION**: Subbase provides adequate frost protection (600 mm minimum) – verify from BC frost depth data and geotechnical recommendations
8. **ASSUMPTION**: Static loading governs (no dynamic analysis required) – confirm from ER or loading characteristics

### TBDs Requiring Resolution
1. **TBD**: Employer's Requirements specific design requirements (design methodology, reliability, performance criteria) – requires detailed ER review
2. **TBD**: Traffic loading data (axle loads, repetitions, load spectra) – requires Owner/ER data or traffic study
3. **TBD**: Geotechnical investigation report (subgrade CBR, resilient modulus, frost depth, groundwater elevation) – site investigation required
4. **TBD**: Pavement analysis software selection and version – confirm from project engineering standards or ER requirements
5. **TBD**: Concrete pavement reinforcement (welded wire mesh vs. fiber reinforcement) – determine from DEL-04.02 specification or structural requirements
6. **TBD**: Subdrainage requirements – determine from geotechnical report recommendations and DEL-04.01 grading design
7. **TBD**: Construction equipment temporary loading – determine if temporary loading during construction is more critical than operational loading
8. **TBD**: Traffic directional distribution and wander – determine from operational layout and traffic patterns

## Cross-document Coordination

### Linkages to Drawings (DEL-04.01)
- Every pavement section thickness calculated herein must match the corresponding section detail in DEL-04.01 drawings
- Calculation output summary table shall reference DEL-04.01 drawing sheet and section/detail numbers
- When DEL-04.01 drawings are revised (layout changes, new pavement zones), calculations must be updated to cover revised scope
- Interface transition designs calculated herein are shown graphically in DEL-04.01 interface details

### Linkages to Specification (DEL-04.02)
- Material properties used as calculation inputs (asphalt modulus, concrete strength, base modulus) must match DEL-04.02 specified materials
- Calculation design assumptions (reliability, design life, loading) must be consistent with DEL-04.02 performance requirements
- When DEL-04.02 specification is revised (material changes, different performance criteria), calculations must be re-run to validate new requirements

### Linkages to Guidance (DEL-04.03 Guidance)
- Guidance provides review checklist to verify calculation completeness, input traceability, and output consistency with DEL-04.01/DEL-04.02
- Guidance ensures all calculation assumptions are flagged and logged in assumption tracking system
- Guidance review process validates calculation methodology and results prior to issuance

### Linkages to Procedure (DEL-04.03 Procedure)
- Procedure defines workflow for obtaining inputs, performing calculations, coordinating with DEL-04.01/DEL-04.02, and issuing results
- Procedure maintains assumption tracking log and calculation traceability matrix
- Procedure revision control ensures calculation updates are traced back to input changes or drawing/specification revisions

### Linkages to Test Records (DEL-04.04)
- Calculation output summary provides target values for DEL-04.04 field testing (pavement layer thicknesses, compaction densities)
- Calculation acceptance criteria define pass/fail limits for DEL-04.04 test results evaluation
- Calculation sensitivity analysis informs DEL-04.04 testing frequency and critical test locations (e.g., higher frequency in areas sensitive to subgrade variability)
