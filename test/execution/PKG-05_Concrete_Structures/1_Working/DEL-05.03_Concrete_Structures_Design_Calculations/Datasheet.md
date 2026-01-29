# Datasheet: DEL-05.03 Concrete Structures Design Calculations

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-05.03 |
| Name | Concrete Structures Design Calculations |
| Package | PKG-05 Concrete Structures |
| Discipline | Structural |
| Type | Calculation |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Calculation Package | Foundations, containment walls, thrust blocks, equipment pads, seismic analysis |
| Document Number | TBD per project document control / numbering system |
| Revision | 00 (initial) — **ASSUMPTION** pending project revision scheme |
| Software / Tools | TBD per Contractor calculation standards (hand calcs, spreadsheets, FEM software) |
| Governing Design Basis | Employer's Requirements Volume 2 Part 2 + project design basis documents (**TBD** clause extraction) |
| Load Cases | Dead/live/equipment/thermal, soil/ground pressures, hydrostatic, seismic (**TBD** specific combinations) |
| Design Codes | Likely CSA A23.3 (concrete design), NBCC/BC Building Code (seismic, loads) — **ASSUMPTION** based on BC location |
| Issue Format | PDF and calculation files (spreadsheets/models) per project document control (**TBD**) |

## Conditions

**Project context:**
- Project: Canola Oil Transload Facility Phase 1, Fraser Surrey Terminal, Surrey, BC
- Design & Build contract
- Storage capacity: 45,000 MT (3 × 15,000 MT tanks)
- Permitted throughput: 1,000,000 MT per annum
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:10; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:44; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:41-42.)

**Design context:**
- Deliverable provides the **engineering basis and sizing/verification calculations** for concrete structures. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234.)
- Package scope includes foundations, containment walls, equipment pads, thrust blocks, ground liner system. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226.)
- PKG-05 deliverables support **OBJ-3 Storage Capacity (45,000 MT)** and **OBJ-7 Environmental Protection**; calculations should capture containment and durability implications. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:782; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786.)
- Contractor scope only; Employer-responsible items excluded except for interface connections. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49.)

**Design basis items to be confirmed (TBD until sourced from ERs / design basis):**
- Geotechnical parameters (bearing capacity, settlement tolerances, soil properties, groundwater levels)
- Design loads (dead, live, equipment, thermal, storage product loads for 45,000 MT capacity)
- Seismic design parameters (seismic zone, site class, importance factors, R values, drift limits)
- Material properties (concrete compressive strength, modulus of elasticity, unit weight, Poisson's ratio)
- Load combinations and load factors per design code
- Serviceability criteria (crack control for containment walls, settlement limits for foundations, deflection limits)
- Durability requirements affecting design (cover, exposure class impacts on section sizing)
(Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD; Datasheet DEL-05.01; Datasheet DEL-05.02.)

## Construction

**Calculation artifacts (anticipated):**

### 1. Foundation Calculations
**Content requirements:**
- Tank foundation calculations (3 × 15,000 MT tanks):
  - Bearing capacity verification
  - Settlement analysis (total and differential settlement)
  - Foundation sizing (diameter, thickness)
  - Reinforcement design
  - Seismic analysis if applicable
- Equipment pad foundation calculations:
  - Bearing capacity verification for equipment loads (pumps, meters, unloading equipment)
  - Settlement analysis
  - Pad sizing and reinforcement design
  - Anchor bolt design and pullout verification
  - Dynamic loading analysis if applicable (vibrating equipment)
- Building foundation calculations (control room, pump house if within PKG-05 scope — **TBD** scope boundary)
- Thrust block calculations:
  - Piping thrust load analysis
  - Passive soil resistance verification
  - Block sizing and reinforcement design
- Foundation design assumptions and input data register
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:41-42.)

### 2. Containment Wall Calculations
**Content requirements:**
- Containment wall structural design:
  - Earth pressure analysis (active/at-rest/passive as applicable)
  - Hydrostatic pressure analysis (product containment scenarios)
  - Wall sizing (height, thickness, base width if applicable)
  - Reinforcement design (vertical, horizontal, joint reinforcement)
  - Foundation bearing and sliding stability
  - Overturning stability
- Serviceability analysis (OBJ-7 Environmental Protection):
  - Crack control analysis (crack width limits for containment integrity)
  - Joint design (construction joints, control joints, expansion joints)
  - Waterproofing and liner interface considerations
  - Leakage pathway evaluation
- Seismic analysis:
  - Dynamic earth pressure (Mononobe-Okabe or equivalent)
  - Seismic overturning and sliding stability
  - Seismic reinforcement detailing requirements
- Containment volume verification (support OBJ-3 45,000 MT storage capacity)
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786.)

### 3. Seismic Analysis
**Content requirements:**
- Seismic design basis definition:
  - Seismic zone and site class
  - Spectral acceleration values
  - Importance factors
  - Ductility and overstrength factors (R values)
  - Drift limits and deformation criteria
- Seismic analysis methodology:
  - Equivalent static analysis or dynamic analysis (justify methodology selection)
  - Load combinations with seismic effects
  - Seismic detailing requirements
- Element-specific seismic analysis:
  - Tank foundations under seismic loads
  - Containment walls under seismic earth pressure
  - Equipment pads under seismic equipment loads
  - Thrust blocks under seismic piping loads
- Seismic performance verification:
  - Strength verification under seismic load combinations
  - Deformation/drift verification
  - Detailing requirements for ductile behavior
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234; Datasheet DEL-05.01: Conditions.)

**Supporting documentation (calculation package structure):**
- Calculation cover sheet and index
- Design basis and assumptions register
- Input data summary (loads, geotechnical properties, material properties, code parameters)
- Load combination summary
- Calculation methodology and software description
- Calculation results summary
- Recommendations and design verification statement
- Independent check sign-off
(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Specification.md: Documentation.)

## References

- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234 — DEL-05.03 description and anticipated artifacts.
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226 — PKG-05 scope (foundations/containment/pads/thrust blocks/liner).
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:782 and :786 — objective mappings (OBJ-3 Storage Capacity 45,000 MT, OBJ-7 Environmental Protection).
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:10 — project location (Surrey, BC).
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:44 — contract type (Design & Build).
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:41-42 — storage capacity parameters.
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49 — scope focus (contractor scope only).
- test/Volume_2_Part_2_Employers_Requirements.pdf — concrete/structural requirements and design basis (clause locations TBD).
- test/Volume_2_Part_1_Employers_Requirements.pdf — general requirements, QA/QC and document control for calculations (clause locations TBD).
- execution/PKG-05_Concrete_Structures/0_References/_REFERENCE_INDEX.md — baseline references for PKG-05.
- DEL-05.01 (Design Drawing Set) — drawings must reflect calculation results (element sizing, reinforcement).
- DEL-05.02 (Technical Specification) — material properties and design assumptions must align with specification values.
- DEL-02.04 (Geotechnical Reports) — geotechnical parameters input to foundation calculations.
- Specification.md — requirements for calculation content, quality, and documentation.
- Guidance.md — principles for calculation development, assumption handling, and containment sensitivity.
- Procedure.md — calculation development, checking, and issue workflow.

## Cross-Document Points

- **Specification → Requirements:** Each calculation artifact (foundations, containment walls, seismic) listed in Construction must be explicitly required in `Specification.md` with acceptance criteria and verification methods.
- **DEL-05.01 → Drawing Alignment:** Calculation results (element sizing, reinforcement quantities) must align with DEL-05.01 drawing dimensions and details.
- **DEL-05.02 → Material Properties:** Material properties assumed in calculations (concrete strength, modulus) must align with DEL-05.02 specification values.
- **Procedure → Verification:** `Procedure.md` defines the checking and verification workflow to ensure calculation quality and traceability.
- **Guidance → Containment Sensitivity:** Containment wall serviceability analysis (crack control, joint design) must reflect OBJ-7 Environmental Protection intent as described in `Guidance.md`.
