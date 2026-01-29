# Datasheet: DEL-04.01 Pavement Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-04.01 |
| Name | Pavement Design Drawing Set |
| Package | PKG-04 Pavement & Surfacing |
| Discipline | Civil |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |
| Objective | OBJ-8 Future Expandability (Phase 2) |

## Attributes

### Drawing Scope
- **Asphalt paving zones**: Roadways, hardstand areas, operational surfaces including future Phase 2 expansion corridors
- **Concrete surfacing**: Specialized areas subject to heavy/concentrated loads or chemical exposure
- **Curbs & gutters**: Perimeter containment, drainage conveyance, and delineation between paved zones
- **Sidewalks**: Personnel access routes with pedestrian safety features
- **Parking areas**: Vehicle parking layout with stall dimensions and circulation patterns
- **Line marking**: Traffic control, safety delineation, and operational guidance markings
- **Interface zones**: Transitions to rail works (PKG-07), marine structures (PKG-08), underground utilities (PKG-03), concrete structures (PKG-05)

### Drawing Set Composition
- **Plan views** (anticipated): Paving layout plans showing horizontal geometry, extents, and grade references
- **Section drawings**: Typical pavement sections showing layer thicknesses, materials, and subgrade preparation requirements
- **Detail sheets**: Curb profiles, joint details, drainage interfaces, expansion/contraction joint configurations
- **Line marking plans**: Traffic control striping, parking stall layouts, safety markings, reflectivity specifications
- **Notes sheets**: General notes, legend, material specifications references, installation sequence requirements

### Design Parameters (TBD pending DEL-04.03)
- **Design loads**: Vehicle loading classes, axle configurations, repetition counts
- **Pavement layer thicknesses**: Asphalt wearing course, binder course, base course, subbase (to be validated by DEL-04.03)
- **Concrete pavement**: Slab thickness, reinforcement requirements, joint spacing
- **Subgrade bearing capacity**: CBR values, compaction requirements (site-specific testing required)
- **Drainage slope requirements**: Minimum grades for surface drainage, tie-ins to PKG-03 storm system

### Conditions

#### Design Basis
- **Climate conditions**: Fraser Surrey, BC climate (freeze-thaw cycles, precipitation patterns)
- **Soil conditions**: **TBD** – geotechnical investigation results required from site survey
- **Groundwater levels**: **TBD** – to be established from geotechnical report
- **Service life**: Minimum 25-year design life per typical industrial pavement standards (**ASSUMPTION** – pending ER confirmation)

#### Operating Environment
- **Traffic types**: Heavy vehicles (trucks, railcar movers), light vehicles (personnel), rail-mounted equipment
- **Chemical exposure zones**: Areas subject to canola oil spillage or cleaning agent contact
- **Loading frequency**: Daily operations for transload facility (1,000,000 MT/a throughput capacity)

#### Interface Constraints
- **PKG-03 interfaces**: Surface drainage tie-ins to catch basins, manholes, culverts (coordinate elevations and slopes)
- **PKG-05 interfaces**: Pavement-to-structure transitions at building perimeters, retaining walls
- **PKG-07 interfaces**: Rail crossings, track embedment zones, clearance envelopes
- **PKG-08 interfaces**: Pavement termination at marine structure boundaries
- **Phase 2 expansion**: Reserved corridors and tie-in points per OBJ-8 (elevations and limits **ASSUMPTION** until Phase 2 design input received)

## Construction

### Material Requirements (Reference DEL-04.02)
- **Asphalt concrete**: Mix design specifications, aggregate gradation, binder grade (PG grading for BC climate)
- **Portland cement concrete**: Strength class, air entrainment, durability requirements
- **Aggregate base/subbase**: Gradation, plasticity index, soundness requirements
- **Line marking materials**: Paint vs. thermoplastic, color specifications, reflectivity standards

### Installation Requirements (Reference DEL-04.02 & Procedure)
- **Subgrade preparation**: Proof rolling, compaction testing, moisture conditioning
- **Layer placement sequence**: Base course, binder course, wearing surface (coordinate with DEL-04.04 testing)
- **Joint construction**: Construction joints, expansion joints, control joints (location and details on drawings)
- **Curing requirements**: Concrete curing duration and method, asphalt cooling period
- **Line marking application**: Surface preparation, ambient conditions, material application rates

## References

### Source Documents
- **Decomposition**: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section PKG-04, DEL-04.01
- **Employer's Requirements**: `test/Volume_2_Part_1_Employers_Requirements.pdf` (General requirements, drawing standards)
- **Employer's Requirements**: `test/Volume_2_Part_2_Employers_Requirements.pdf` (Civil & Process Mechanical Works, pavement requirements – **location TBD**)
- **Package Reference Index**: `test/execution/PKG-04_Pavement_and_Surfacing/0_References/_REFERENCE_INDEX.md`

### Related Deliverables (Cross-references)
- **DEL-04.02**: Pavement Technical Specification – material and workmanship requirements that govern drawing annotations
- **DEL-04.03**: Pavement Design Calculations – analytical basis for layer thicknesses, load capacity verification
- **DEL-04.04**: Pavement Installation & Test Records – field verification of as-built conformance to drawings
- **DEL-03.01–03.06**: Underground Utilities (PKG-03) – drainage system elevations and locations
- **DEL-05.01–05.04**: Concrete Structures (PKG-05) – structure-to-pavement interface elevations
- **DEL-07.01–07.04**: Rail Works (PKG-07) – track elevations, rail crossing details

### Standards & Codes (**ASSUMPTION** – pending ER confirmation and reference availability)
- **OPSS** (Ontario Provincial Standard Specifications) or equivalent BC MMCD (Master Municipal Construction Documents) – pavement construction standards
- **TAC** (Transportation Association of Canada) – Pavement Design and Rehabilitation Manual
- **CSA A23.1/A23.2** – Concrete materials and test methods (if applicable to concrete pavement zones)
- **ASTM D6433** – Pavement distress evaluation (for future maintenance planning)

## Assumptions & TBDs

### Assumptions Requiring Validation
1. **ASSUMPTION**: 25-year design life for industrial pavement – confirm with Employer's Requirements or project specification
2. **ASSUMPTION**: Phase 2 expansion corridors and tie-in elevations pending Phase 2 design input – coordinates and grades to be confirmed
3. **ASSUMPTION**: Applicable standards (OPSS/MMCD, TAC) – confirm governing jurisdiction requirements from ER
4. **ASSUMPTION**: Heavy vehicle loading class (e.g., AASHTO H-20 equivalent or industrial axle loads) – to be validated by DEL-04.03 design criteria

### TBDs Requiring Resolution
1. **TBD**: Site-specific geotechnical data (soil bearing capacity, CBR, groundwater elevation) – requires geotechnical investigation report
2. **TBD**: Employer's Requirements specific clause references for pavement design criteria – requires detailed ER review (Volume 2 Part 2)
3. **TBD**: Exact drawing sheet count and numbering system – to be established during drafting phase
4. **TBD**: CAD standards and title block requirements – confirm from project drawing management plan or ER general requirements
5. **TBD**: Line marking color and reflectivity standards – reference specific clauses in DEL-04.02 once specification is advanced

## Cross-document Coordination

### Linkages to Specification (DEL-04.01 Specification)

| Datasheet Section | Specification Reference | Alignment Requirement |
|-------------------|------------------------|----------------------|
| Attributes – Drawing Scope | Specification §R1.1 | Plan content requirements must cover all scope items |
| Attributes – Drawing Set Composition | Specification §R1.2, §R1.3, §R1.5 | Section, line marking, and document control requirements |
| Design Parameters | Specification §R2.2 | Calculation cross-references for layer thicknesses |
| Conditions – Interface Constraints | Specification §R1.4 | Interface annotation requirements |
| Construction – Material Requirements | Specification §R2.1 | Specification cross-reference requirements |
| Assumptions & TBDs | Specification §R3.2 | Assumption and TBD tracking requirements |

### Linkages to Guidance (DEL-04.01 Guidance)

| Datasheet Section | Guidance Reference | Verification Method |
|-------------------|-------------------|-------------------|
| Attributes – Drawing Scope | Guidance Step 1 checklist | Plan completeness verification |
| Attributes – Drawing Set Composition | Guidance Steps 2-3 checklists | Section and line marking verification |
| Conditions – Interface Constraints | Guidance Step 4 checklist | Interface and OBJ-8 callout verification |
| Conditions – Phase 2 expansion | Guidance Principle P3 | Future expandability review |
| Assumptions & TBDs | Guidance Principle P4 | Assumption tracking review |

### Linkages to Procedure (DEL-04.01 Procedure)

| Datasheet Section | Procedure Reference | Workflow Integration |
|-------------------|-------------------|---------------------|
| Attributes – Drawing Scope | Procedure Step 1 | Scope capture and initialization |
| Drawing Set Composition | Procedure Step 2 | Drawing drafting with traceability |
| Design Parameters (TBD) | Procedure Step 4 | DEL-04.03 coordination for resolution |
| Assumptions & TBDs | Procedure Steps 1, 3 | Assumption log creation and maintenance |
| Interface Constraints | Procedure Step 3.4 | Cross-package coordination actions |

### Linkages to Calculations (DEL-04.03)
- Drawing section thicknesses are outputs from DEL-04.03 pavement design calculations (coordinated via Procedure Step 4)
- Loading assumptions shown on drawings (vehicle types, axle loads) must match DEL-04.03 input parameters
- Any design iteration in DEL-04.03 triggers drawing update per Procedure Step 6 revision process

### Linkages to Test Records (DEL-04.04)
- Final issued drawing set (with revision number) becomes the basis for DEL-04.04 field verification (handoff per Procedure Step 5.5)
- Drawing section details and tolerances establish the acceptance criteria for compaction testing, thickness verification, and material sampling in DEL-04.04 (referenced per Specification §R2.3)
