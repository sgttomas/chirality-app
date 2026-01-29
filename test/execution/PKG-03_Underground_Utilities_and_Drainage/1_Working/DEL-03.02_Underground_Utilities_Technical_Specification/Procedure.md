# Procedure: DEL-03.02 Underground Utilities Technical Specification

## Purpose

**Production Purpose:**
- Produce and control the technical specification deliverable that establishes performance, materials, and workmanship requirements for storm drainage, oil-water separator (OWS), duct banks, and trenchless crossings for PKG-03 (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:199).
- Implement the workflow that transforms design inputs (calculations from DEL-03.03, geometry from DEL-03.01, Employer's Requirements from Volume 2 Part 2) into verified, QA-approved specification sections ready for material procurement and construction execution (Specification §Scope defines what specification contains; this Procedure defines how to produce it).

**Quality Assurance Purpose:**
- Execute QA/QC review process (self-check, interdisciplinary check, independent check) that verifies compliance with Specification requirements, validates coordination with design drawings and installation records, and confirms specification completeness and technical accuracy before issue (Specification §Verification and §QR-1 require QA compliance; this Procedure implements review workflow).
- Generate quality records (specification review logs, QA checklists, issue registers) that provide audit trail for contract compliance and support future material submittal review and installation verification (Specification §Documentation lists associated quality records; this Procedure defines how records are created and retained).

## Prerequisites

**Dependencies:**
- Dependencies are coordinated externally by humans (see `_DEPENDENCIES.md`); confirm inputs from design calculations (DEL-03.03), design drawings (DEL-03.01), and related deliverables are complete or have sufficient information before starting specification development (Source: Specification §IF-1 coordination with related deliverables; Guidance §C-1 design calculation availability consideration).
- Required inputs include:
  - **DEL-03.03 Design Calculations**: Hydraulic calculations (pipe sizes, design storm event, flow rates), OWS capacity calculations (treatment flow rate, retention time, sizing), structural analysis for trenchless crossings (jacking forces, casing pipe requirements), design parameters (design life, seismic category, loading conditions) (Specification §PR-1, §PR-2, §PR-3 performance requirements reference calculations; Guidance §C-1 emphasizes calculation availability before finalizing specification performance requirements).
  - **DEL-03.01 Drawing Set**: Pipe alignments, elevations, OWS layout, duct bank routing, trenchless crossing locations provide geometry context for specification (specification provides materials/performance; drawings provide geometry) (Specification §IF-1 coordination requirement).
  - **DEL-03.04 Data Sheet Package** (if available): OWS equipment data sheets, pump data sheets, instrumentation details provide equipment context for specification performance criteria (Specification §IF-1 coordination requirement; may not be available early in specification development; coordinate performance criteria to align with anticipated equipment selections).
  - **DEL-03.05 Installation and Test Records structure** (if available): Testing and inspection forms, QA checklists provide context for specification testing requirements; ensure specification testing requirements align with what will be documented in installation records (Specification §IF-1 and §QR-3 coordination requirement; Guidance §P-4 coordination with installation records principle).

**Reference Materials:**
- **Employer's Requirements Volume 2 Part 2 (Civil & Process Mechanical Works)**: Civil utility performance criteria, pipe material standards, installation methods, environmental protection criteria, OWS discharge limits (Source: Specification §Standards governing standards; Guidance §C-2 emphasizes ER extraction for specification requirements).
- **Employer's Requirements Volume 2 Part 1 (General Requirements)**: Project Quality Management Plan, submittal procedures, document control procedures, QA/QC requirements (Source: Specification §QR-1 quality management compliance; test/Volume_2_Part_1_Employers_Requirements.pdf).
- **Project Specification Standards**: Specification format (CSI MasterFormat or project-specific organization), specification numbering scheme, section templates (if available) (Source: Specification §Documentation format TBD; Datasheet §Attributes specification format).
- **CSA and ASTM Standards**: Pipe material standards (CSA B182.1, CSA A257, CSA B137, ASTM D3034), concrete standards (CSA A23.1, CSA A23.2), testing standards (ASTM F1417, ASTM C969, NASSCO PACP), other applicable standards (Source: Specification §Standards supplementary standards list; to be confirmed during specification development).
- **Civil Design Brief**: Design life, seismic design category, temperature range, design storm event, other environmental design parameters (Source: Specification §PR-3 design life and environmental conditions; Datasheet §Conditions lists design parameters TBD from civil design brief).
- **Geotechnical Report**: Soil conditions, bearing capacity, corrosivity, groundwater chemistry affecting material selections and installation requirements (Source: Specification §PR-3 environmental conditions; required for backfill specifications and pipe material selections).
- **Package-level reference index**: `execution/PKG-03_Underground_Utilities_and_Drainage/0_References/_REFERENCE_INDEX.md` (to be populated with project-specific codes, standards, and reference documents).

**Design Intent Understanding:**
- Review Specification requirements (§Scope, §Requirements, §Standards, §Verification) to understand functional, performance, interface, and quality expectations for the technical specification (Specification provides "what"; this Procedure provides "how").
- Review Guidance principles, considerations, and trade-offs (§Principles, §Considerations, §Trade-offs) to understand why requirements exist and how to make informed specification decisions (e.g., performance-based vs. prescriptive approaches, OWS technology selection, trenchless crossing specification detail) (Guidance §Purpose clarifies intent behind requirements; helps specification writer prioritize when making specification development decisions).
- Understand downstream use: Material suppliers will use specification for submittal preparation; construction contractors will use specification for installation execution; QA/QC will use specification for inspection verification; operations will use specification for maintenance planning (Datasheet §Conditions operational context describes downstream users).

**Personnel Requirements:**
- **Originator**: Civil discipline specification writer with underground utilities specification experience; responsible for producing specification per this Procedure workflow (ASSUMPTION per typical QA process and Quality Management Plan in Volume 2 Part 1).
- **Checker**: Civil discipline senior engineer or lead; responsible for technical accuracy review and coordination check before independent review.
- **Approver/Independent Reviewer**: Discipline lead or designated independent reviewer; responsible for final compliance check, standards verification, and approval signature before issue.
- **Adjacent Discipline Reviewers**: Representatives from PKG-02 (backfill coordination), PKG-04 (pavement restoration coordination), PKG-17 (duct bank coordination), design calculation lead (performance criteria alignment), installation records lead (testing requirements coordination) for interdisciplinary coordination review (Specification §IF-1 and §IF-2 coordination requirements; Verification section interdisciplinary check step).

## Steps

### Step 1: Scope and Objectives Review

**Objective**: Confirm specification scope, anticipated sections, and project objectives before starting specification development.

**Actions**:
1.1. Read decomposition entry for DEL-03.02 (test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:199) to confirm scope description and anticipated specification sections (storm drainage, OWS, duct banks, trenchless crossings, general requirements).

1.2. Review Specification §Scope and §Requirements to confirm functional, performance, interface, and quality expectations (Specification §FR-1 to FR-4, §PR-1 to PR-3, §IF-1 to IF-2, §QR-1 to QR-3 define specification requirements; this step ensures originator understands what must be delivered).

1.3. Confirm **OBJ-7 Environmental Protection** objective emphasis: OWS specification must clearly capture treatment performance criteria, discharge limits, and monitoring protocols to demonstrate environmental compliance (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; Specification §FR-2 environmental protection performance requirement; Guidance §P-2 environmental protection performance principle).

1.4. Identify scope exclusions: Geometry and elevations are in DEL-03.01 Drawing Set, hydraulic calculations are in DEL-03.03 Design Calculations, equipment details are in DEL-03.04 Data Sheet Package, installation records are in DEL-03.05, above-ground structures are outside PKG-03 scope (Specification §Scope exclusions; prevents scope creep per Guidance §C-3).

**Verification**: Scope review checklist confirms originator has read decomposition entry, Specification requirements, and Guidance principles; checklist signed before proceeding to Step 2.

**Output**: Scope confirmation documented in project files; originator understands what specification sections to produce and why.

---

### Step 2: Input Data Collection and Coordination

**Objective**: Collect design inputs from design calculations, design drawings, and related deliverables; confirm data availability and alignment.

**Actions**:
2.1. Request and collect design calculation outputs:
- **DEL-03.03 Design Calculations**: Hydraulic calculation results (pipe sizes, design storm event, flow rates, slopes, hydraulic grade lines), OWS capacity calculation results (treatment flow rate, retention time, separator sizing, removal efficiency basis), structural analysis for trenchless crossings (casing pipe sizes, wall thickness, jacking forces, settlement predictions), design parameters (design life, seismic category, loading conditions, temperature range) (Specification §PR-1, §PR-2, §PR-3 performance requirements reference these calculations; Guidance §C-1 design calculation availability consideration emphasizes importance of calculation availability before finalizing specification performance requirements).

2.2. Collect design drawing information:
- **DEL-03.01 Drawing Set**: Review storm drainage plan-and-profile sheets, OWS layout sheet, duct bank plans, trenchless crossing sheets to understand geometry context for specification (specification sections will reference drawing sheets for alignments, elevations, details) (Specification §IF-1 coordination with DEL-03.01).

2.3. Collect related deliverable information (if available):
- **DEL-03.04 Data Sheet Package**: OWS equipment data sheet (if available early in design development) provides equipment context for OWS specification performance criteria; coordinate specification treatment efficiency and discharge limits with anticipated equipment capabilities (Specification §IF-1 coordination; may not be available early; proceed with performance criteria from calculations and coordinate with equipment data sheet when available).
- **DEL-03.05 Installation and Test Records structure**: Review installation records structure (if available) to understand what testing and inspection will be documented; ensure specification testing requirements align with installation records documentation plan (Specification §IF-1 and §QR-3; Guidance §P-4 coordination with installation records).

2.4. Confirm data availability status: Verify that design calculations are complete or have sufficient information to define specification performance requirements (ideally calculations are approved for design release; if calculations are preliminary, proceed with draft specification and coordinate revisions when calculations finalize per Guidance §C-1 mitigation).

2.5. Document data sources in specification general requirements section: List design calculation reports, drawing sheets, standards, and codes used as specification basis (supports traceability per Specification §Verification traceability verification; enables future reviewers and users to trace specification requirements to design basis).

**Verification**: Input data collection checklist confirms required design calculation outputs are collected (hydraulic calculations, OWS sizing, structural analysis, design parameters); checklist includes input document IDs, revision numbers, and availability status.

**Output**: Design input package assembled and documented; ready for specification section development.

---

### Step 3: Specification Section Structure Establishment

**Objective**: Establish specification section structure matching anticipated sections and project specification standards.

**Actions**:
3.1. Confirm project specification format and organization:
- Determine if project uses CSI MasterFormat section numbering (e.g., Section 33 00 00 series for underground utilities) or project-specific numbering scheme (Datasheet §Attributes specification format TBD; confirm with project specification coordinator or document control).
- Obtain specification section templates (if project has standard templates for general requirements, submittals, quality assurance, materials, installation, testing).

3.2. Establish specification section structure per anticipated sections (Specification §Scope; Datasheet §Construction specification organization):
- **Section 1 – General Requirements**: Scope, references, definitions, submittals, quality assurance, delivery/storage/handling
- **Section 2 – Storm Drainage System**: Materials (pipe, manholes, catch basins, fittings, bedding, backfill), installation requirements, testing and inspection (hydrostatic testing, CCTV inspection)
- **Section 3 – Oil-Water Separator System**: Performance criteria (treatment efficiency, flow capacity, discharge limits), materials of construction, instrumentation, installation requirements, performance testing and commissioning
- **Section 4 – Duct Bank System**: Conduit materials, concrete encasement, pull boxes, installation requirements, testing (conduit continuity testing)
- **Section 5 – Trenchless Crossing System**: Boring methods (performance requirements), casing and carrier pipes, grouting, testing and inspection
- **Section 6 – Backfill and Restoration**: Trench backfill materials, compaction requirements, pavement restoration

3.3. Create specification table of contents:
- List all sections with section numbers and titles
- Include cross-references to related deliverables in table of contents or general requirements section (e.g., "See DEL-03.01 Drawing Set for pipe alignments and elevations; See DEL-03.03 Design Calculations for hydraulic performance basis")

**Verification**: Specification section structure review confirms section organization matches anticipated sections (Specification §Scope list); table of contents approved by discipline lead before proceeding to detailed section development.

**Output**: Specification section structure established; table of contents created; ready for detailed section content development.

---

### Step 4: Specification Section Development

**Objective**: Develop detailed specification section content for storm drainage, OWS, duct banks, and trenchless crossings with materials, installation, and testing requirements.

#### Step 4.1: Storm Drainage Specification Requirements

**Actions**:
4.1.1. **General requirements sub-section**:
- Scope: Storm drainage pipe, manholes, catch basins, fittings, bedding, backfill per DEL-03.01 Drawing Set
- References: Employer's Requirements Volume 2 Part 2, CSA B182.1 (plastic pipe), CSA A257 (concrete pipe and manholes), ASTM standards, DEL-03.03 Design Calculations, DEL-03.01 Drawing Set
- Submittals: Pipe manufacturer product data, test reports (ring stiffness, chemical resistance, joint watertightness), manhole shop drawings, installation procedures, test plans (hydrostatic testing, CCTV inspection per DEL-03.06)
- Quality assurance: Manufacturer qualifications, material certifications (CSA or ASTM certification), testing laboratory accreditation, inspection requirements

4.1.2. **Materials sub-section**:
- Pipe materials: Define pipe material options with performance requirements (HDPE per CSA B137 with ring stiffness requirements, PVC per ASTM D3034 or CSA B137.2, concrete per CSA A257 with crushing strength requirements); include jointing requirements (gasket joints per CSA standards, jointing method affecting watertightness performance)
- Pipe performance: Reference design performance from DEL-03.03 calculations (hydraulic capacity, structural loading, design life from civil design brief per Specification §PR-1 and §PR-3); specify material properties supporting performance (ring stiffness or crushing strength, chemical resistance to stormwater constituents, joint watertightness, UV resistance if exposed)
- Manholes and catch basins: Precast concrete per CSA A257 or ASTM C478, dimensions and configurations per DEL-03.01 Drawing Set, frame and cover specifications (traffic-rated heavy-duty cast iron or other approved material)
- Bedding and backfill: Bedding material (crushed stone or sand per ASTM D2487 gradation requirements, thickness per drawings or 150mm minimum), backfill material (granular material or native soil reuse criteria, compaction requirements per Section 6)
- Apply Guidance §P-1 hydraulic performance and durability principle: Material specifications shall support calculated performance from DEL-03.03; include clear material standards references (CSA, ASTM section numbers) per Guidance §P-3 material and workmanship clarity principle.

4.1.3. **Installation sub-section**:
- Pipe installation: Alignment and grade tolerances (±25mm horizontal, ±10mm vertical, or as specified in ER Volume 2 Part 2), slope requirements (minimum slope per DEL-03.01 Drawing Set or 0.5% minimum for gravity drainage), bedding placement and compaction, jointing procedures (clean joint surfaces, install gaskets per manufacturer instructions, verify watertightness), support at joints (prevent differential settlement)
- Manhole and catch basin installation: Excavation and base preparation, base slab installation (precast or cast-in-place), manhole section assembly and jointing, invert channel construction (half-pipe benching or formed channels per DEL-03.01 details), frame and cover installation (set to final grade, adjust with grade rings, seal to prevent infiltration)
- Backfill: Placement in lifts per Section 6 backfill requirements, compaction around pipe to prevent damage or displacement

4.1.4. **Testing and inspection sub-section**:
- Hydrostatic pressure testing: Test method per ASTM F1417 or other approved standard, test pressure (1.5 × design pressure or 35 kPa minimum, whichever is greater), test duration (minimum 2 hours or per ER Volume 2 Part 2), allowable leakage limits (50 mL per 100 joints per hour per ASTM F1417 or other criteria from ER), test procedure (fill system with water, allow stabilization, apply test pressure, monitor pressure and leakage, record results)
- CCTV inspection: Timing (after backfilling complete but before pavement restoration), inspection standard (NASSCO PACP or other standard from ER Volume 2 Part 2), equipment requirements (camera resolution, lighting, recording), defect classification and reporting per DEL-03.06 CCTV Survey Report, acceptance criteria (no defects affecting structural integrity or watertightness, no infiltration/exfiltration, no joint displacement or separation exceeding [TBD] mm)
- Manhole and catch basin inspection: Dimensional tolerances (invert elevation ±10mm, frame and cover grade ±5mm), joint sealing (visual inspection for watertightness), invert channel construction quality (smooth transitions, proper slopes)
- Coordinate testing requirements with DEL-03.05 Installation and Test Records and DEL-03.06 CCTV Survey Report per Specification §IF-1 and Guidance §P-4.

**Verification**: Storm drainage specification section draft reviewed for completeness (materials, installation, testing all addressed), technical accuracy (standards references correct, performance criteria match DEL-03.03 calculations), and clarity (submittal requirements clear, acceptance criteria objective).

**Output**: Storm drainage specification section drafted; ready for review.

**Cross-reference**: Guidance §P-1 hydraulic performance and durability; Guidance §Example 1 storm drainage specification structure; Specification §PR-1 hydraulic and structural performance; Datasheet §Construction storm drainage specification content.

---

#### Step 4.2: OWS Specification Requirements

**Actions**:
4.2.1. **Performance requirements sub-section**:
- Treatment flow rate capacity: Design flow rate from DEL-03.03 calculations (L/s or m³/h), peak flow rate capacity for storm events, statement that OWS shall handle design flow without bypass or overflow
- Oil removal efficiency: Minimum removal efficiency for free oil (typically 95% or outlet concentration limit), minimum removal efficiency for total petroleum hydrocarbons (TPH) (typically 80% or outlet concentration limit), basis for efficiency calculation (influent concentration, target effluent concentration from environmental permit conditions or ER Volume 2 Part 2)
- Solids settling capacity: Effluent suspended solids concentration limit (mg/L per environmental permit or ER), retention time requirement (typically 3-5 minutes for gravity separator at design flow rate, or as calculated in DEL-03.03)
- Discharge limits: Maximum allowable concentrations for discharge per environmental permit conditions or ER Volume 2 Part 2 (oil and grease ≤ [TBD] ppm, TPH ≤ [TBD] ppm, suspended solids ≤ [TBD] mg/L, pH range [TBD] to [TBD], other parameters as applicable)
- Apply Guidance §P-2 environmental protection performance (OBJ-7) principle: Performance criteria shall support environmental compliance and regulatory permitting; performance values from DEL-03.03 calculations and environmental permit conditions.

4.2.2. **Materials and construction sub-section**:
- Separator vessel: Construction type (fabricated steel or reinforced concrete, or other approved material), sizing per DEL-03.04 OWS Data Sheet and DEL-03.03 calculations
  - Steel vessels: Plate thickness (minimum 6mm or per structural design), welding per AWS D1.1, interior coating suitable for canola oil and stormwater contact (specify coating system or performance requirements: chemical resistance, abrasion resistance, design life)
  - Concrete vessels: Mix design per CSA A23.1 (minimum strength, maximum w/c ratio, other requirements), wall thickness (minimum 200mm or per structural design), waterproofing system (specify type or performance requirements)
- Internals: Inlet and outlet baffles, oil skimmer mechanism, sludge hopper, access hatches, other components per DEL-03.04 OWS Data Sheet; materials (stainless steel 316, other corrosion-resistant materials suitable for canola oil and stormwater environment)
- Chemical resistance: Materials shall resist degradation from canola oil, stormwater constituents (salts, de-icing chemicals if applicable), cleaning chemicals; design life per civil design brief (typically 25-50 years)

4.2.3. **Instrumentation and monitoring sub-section**:
- Level instrumentation: High level alarm (prevent overflow), oil layer thickness sensor, sludge level indicator; coordinate instrument specifications with PKG-18 Instrumentation (if applicable) or specify performance requirements (accuracy, output signal type, environmental rating)
- Flow measurement: Effluent discharge flow meter with totalizer, accuracy requirements (±2% of full scale or better), coordinate with PKG-18 Instrumentation
- Sampling ports: Influent and effluent sampling ports for discharge quality monitoring per environmental permit requirements; accessible for sample collection, equipped with sample taps or valves
- Data logging and alarms: Interface to facility control system (if applicable) for data logging, alarm annunciation, remote monitoring; coordinate with PKG-18 Instrumentation

4.2.4. **Installation requirements sub-section**:
- Location and access: Install per DEL-03.01 Drawing Set OWS layout; provide access for maintenance (sludge removal, oil skimming, inspection); access road or pathways per drawings
- Foundation: Prepare foundation per geotechnical recommendations and structural design; bearing capacity, settlement limits, frost protection if applicable
- Piping connections: Inlet and outlet piping per DEL-03.01 Drawing Set and process piping specifications; ensure proper invert elevations for gravity flow, provide isolation valves for maintenance
- Instrumentation installation: Install per manufacturer recommendations and PKG-18 specifications; calibrate before commissioning

4.2.5. **Performance testing and commissioning sub-section**:
- Pre-commissioning inspection: Verify construction per DEL-03.01 Drawing Set and this specification, verify instrumentation installation and calibration, verify piping connections and isolation valves, conduct functional test of control system (alarms, data logging)
- Flow rate verification testing: Introduce water at various flow rates, measure actual flow through OWS with flow meter, verify OWS can handle design flow rate without bypass or overflow, verify retention time at design flow rate (compare measured retention time to calculated retention time from DEL-03.03)
- Oil removal efficiency testing: Introduce known oil concentration in influent (use canola oil or substitute oil approved by Engineer), operate OWS at design flow rate, collect influent and effluent samples, analyze samples for oil content (laboratory analysis per approved methods), calculate removal efficiency, conduct minimum 3 test runs and calculate average efficiency
- Discharge quality verification: Collect effluent samples during efficiency testing, analyze for all discharge limit parameters (oil and grease, TPH, suspended solids, pH, other parameters), verify effluent quality meets discharge limits
- Acceptance criteria: Performance test results shall demonstrate OWS meets or exceeds specified treatment efficiency and discharge limits; if test results do not meet acceptance criteria, contractor shall investigate cause (inadequate retention time, improper internals installation, equipment deficiency), implement corrective actions, and re-test
- Documentation: Performance test results documented per DEL-03.05 Installation and Test Records, submitted to Engineer for review and approval before facility operations commence
- Coordinate testing requirements with DEL-03.05 Installation and Test Records per Specification §IF-1 and Guidance §P-4.

**Verification**: OWS specification section draft reviewed for completeness (performance criteria, materials, instrumentation, installation, testing all addressed), alignment with OBJ-7 environmental protection objective (treatment efficiency and discharge limits support environmental compliance), coordination with DEL-03.03 calculations and DEL-03.04 equipment data sheet.

**Output**: OWS specification section drafted; ready for review.

**Cross-reference**: Guidance §P-2 environmental protection performance (OBJ-7); Guidance §Example 2 OWS performance criteria specification; Specification §FR-2 environmental protection performance; Specification §PR-2 OWS treatment capacity and containment performance; Datasheet §Construction OWS specification content.

---

#### Step 4.3: Duct Bank Specification Requirements

**Actions**:
4.3.1. **Conduit materials sub-section**:
- PVC conduit: Conforming to CSA C22.10 and NEMA TC 2, Schedule 40 minimum wall thickness (or Schedule 80 for areas with heavy traffic loads if specified in ER or PKG-17), sizes and quantities per DEL-03.01 Drawing Set conduit schedule and PKG-17 Electrical specifications, jointing (integral bell-end with solvent-welded joints or elastomeric gasket joints per CSA C22.10)
- Alternative HDPE conduit: Conforming to CSA B137, DR 13.5 minimum, jointing (mechanical couplings or fusion-welded joints per CSA B137); HDPE conduit may be used in lieu of PVC subject to Engineer approval and coordination with PKG-17 Electrical for compatibility with cable installation
- Conduit accessories: Couplings, adapters, expansion fittings, end caps, other accessories compatible with conduit type and suitable for concrete encasement installation
- Coordinate conduit specifications with PKG-17 Electrical per Specification §IF-2 and Guidance §T-4 duct bank specification coordination trade-off.

4.3.2. **Concrete encasement sub-section**:
- Concrete mix design: Minimum 25 MPa compressive strength at 28 days, conforming to CSA A23.1, maximum aggregate size 20mm (small aggregate for placement around conduits), slump 80-100mm (workable for placement without segregation or vibration-induced damage to conduits)
- Encasement dimensions: Minimum 75mm concrete cover on all sides of conduit bank (top, bottom, sides) or as shown on DEL-03.01 Drawing Set duct bank cross-sections; encasement width and depth per drawings
- Reinforcement: If required for structural loading (heavy traffic areas), provide welded wire mesh or rebar per structural design and DEL-03.01 Drawing Set details
- Placement: Place concrete around conduits in single pour if possible to avoid cold joints; use internal vibration carefully to consolidate concrete without displacing conduits or damaging conduit joints; finish top surface smooth and sloped for drainage if encasement is near surface
- Curing: Moist cure for minimum 7 days per CSA A23.1 or use curing compound conforming to ASTM C309

4.3.3. **Pull boxes sub-section**:
- Materials: Precast reinforced concrete per CSA A257, cast-in-place concrete per CSA A23.1, or fiberglass/polymer concrete pull boxes; material selection subject to Engineer approval based on traffic loading and installation conditions
- Size and spacing: Per DEL-03.01 Drawing Set and PKG-17 Electrical requirements (pull box spacing typically limited by cable pulling tension, often 100-150m maximum for long straight runs, 30-50m for runs with bends); minimum size [TBD based on conduit quantity and configuration, typically 1200mm × 1200mm × 1200mm depth for multi-conduit duct banks]
- Installation: Install at elevations per DEL-03.01 Drawing Set, provide removable covers (reinforced concrete or heavy-duty polymer, traffic-rated if in paved areas with loading per traffic conditions), anchor conduits to pull box walls with grout or mechanical fasteners to prevent movement during cable installation, provide drainage (sump and drain connection if groundwater or surface water infiltration anticipated)

4.3.4. **Installation requirements sub-section**:
- Trench preparation: Excavate trench to dimensions per DEL-03.01 Drawing Set duct bank plans and cross-sections, compact trench bottom to 95% Standard Proctor density (ASTM D698) to provide uniform bearing for concrete encasement
- Conduit installation: Install conduits per DEL-03.01 Drawing Set conduit routing and conduit schedule, maintain separation between conduits per code requirements and PKG-17 requirements (typically 75mm minimum or 1 conduit diameter, whichever is greater), support conduits on chairs or spacers at maximum [TBD – typically 1.5-2.0m] intervals to maintain alignment, separation, and grade during concrete placement, verify conduits are clean internally (no debris, soil, water) before concrete placement
- Concrete placement: Place concrete encasement per sub-section above, vibrate carefully to consolidate around conduits without displacing conduits or damaging joints, finish top surface
- Backfill: After concrete curing complete (minimum 7 days or per curing requirements), backfill trench with granular material per Section 6 backfill requirements, compact to 95% Standard Proctor density
- Coordinate installation with PKG-17 Electrical to ensure duct bank construction meets electrical cable installation requirements.

4.3.5. **Testing requirements sub-section**:
- Conduit continuity testing: After concrete curing and backfilling complete, perform mandrel test or cable pull test
  - Mandrel test: Pull rigid mandrel with diameter equal to [TBD – typically 90-95%] of conduit internal diameter through each conduit from pull box to pull box; mandrel shall pass through conduit without obstruction; mandrel passage verifies conduit is clear, continuous, and undamaged (no crushing, no joint separation)
  - Alternative cable pull test: Pull test cable or rope through each conduit; test cable passage verifies conduit is clear and continuous
- Testing documentation: Document test results (conduit ID, test method, test date, pass/fail, observations) per DEL-03.05 Installation and Test Records
- Coordinate testing requirements with DEL-03.05 per Specification §IF-1 and Guidance §P-4.

**Verification**: Duct bank specification section draft reviewed for completeness (conduit materials, concrete encasement, pull boxes, installation, testing all addressed), coordination with PKG-17 Electrical (conduit specifications align with electrical design assumptions).

**Output**: Duct bank specification section drafted; ready for review.

**Cross-reference**: Guidance §T-4 duct bank specification coordination with electrical; Guidance §Example 3 duct bank material requirements; Specification §IF-2 coordination with PKG-17; Specification §FR-3 coordination with electrical infrastructure; Datasheet §Construction duct bank specification content.

---

#### Step 4.4: Trenchless Crossing Specification Requirements

**Actions**:
4.4.1. **Performance requirements sub-section**:
- Alignment tolerances: Horizontal deviation ±150mm from design alignment shown on DEL-03.01 Drawing Set, vertical deviation ±75mm (or tighter tolerances if required for critical crossings beneath roads, rail tracks, or existing utilities)
- Casing pipe: Steel casing pipe conforming to CSA G40.21 Grade 350W or ASTM A252 Grade 3, minimum wall thickness per DEL-03.03 structural calculations for jacking forces and external loading, casing diameter per DEL-03.01 Drawing Set
- Carrier pipe: Storm drainage pipe per Section 2 storm drainage specification materials, installed inside casing with annular space grouting
- Surface settlement limits: Ground surface settlement above boring shall not exceed [TBD – typically 25mm maximum for crossings beneath roads, 15mm maximum beneath rail tracks, or per geotechnical recommendations]; contractor shall monitor surface settlement during boring and implement corrective actions if settlement approaches limits
- Apply Guidance §T-3 trenchless crossing specification detail trade-off: Performance-based specification approach allows contractor to propose boring method meeting performance requirements.

4.4.2. **Boring methods sub-section**:
- Acceptable methods: Contractor may propose auger boring, microtunneling, horizontal directional drilling (HDD), pipe jacking, or other trenchless methods meeting performance requirements above; proposed method subject to Engineer approval based on site conditions (soil type, groundwater, existing utilities), crossing length, alignment requirements, surface settlement limits
- Method selection considerations: Auger boring suitable for straight alignments in stable soils; microtunneling suitable for longer crossings or difficult soil conditions (high groundwater, unstable soils); HDD suitable for longer crossings or curved alignments; pipe jacking suitable for larger diameter casings
- Prohibited methods: Open cut excavation is not permitted for crossings beneath [specify roads, rail tracks, or other features requiring trenchless crossing per DEL-03.01 Drawing Set]

4.4.3. **Casing pipe installation sub-section**:
- Pipe sections: Steel pipe sections per performance requirements above, section lengths suitable for proposed boring method (typically 3-6m lengths for auger boring or pipe jacking, full-length casing for HDD if feasible)
- Welding: Pipe sections welded per AWS D1.1, welding procedures qualified per AWS D1.1, welders certified per AWS D1.1 or equivalent
- Weld inspection: Visual inspection of all welds per AWS D1.1 (acceptance criteria: no cracks, no incomplete fusion, no undercut exceeding limits); ultrasonic or radiographic inspection of [TBD – typically 10-25%] of welds or as directed by Engineer (critical crossings may require 100% non-destructive testing)
- Corrosion protection: If casing will remain in ground permanently and corrosion is concern (corrosive soils, stray electrical currents), provide coating (fusion-bonded epoxy, coal tar enamel, or other approved coating system per AWWA C203 or equivalent) or cathodic protection (sacrificial anodes or impressed current system per NACE standards); corrosion protection requirement per geotechnical report recommendations and ER Volume 2 Part 2

4.4.4. **Carrier pipe and grouting sub-section**:
- Carrier pipe installation: Install carrier pipe (storm drainage pipe per Section 2 materials) inside casing after casing installation complete, support carrier pipe on spacers or supports at maximum [TBD – typically 3m] intervals to maintain alignment and prevent sagging, spacers shall be non-corrosive and allow grout flow around carrier pipe
- Annular space grouting: Grout annular space between carrier pipe and casing with non-shrink cementitious grout (conforming to ASTM C1107 or equivalent) or other approved grout material (flowable fill per ASTM D6103 may be acceptable if approved); grouting procedure: inject grout from entry pit, vent at exit pit, continue grouting until grout flows from vent (indicates annular space is filled), allow grout to cure before backfilling entry/exit pits
- Grouting verification: Confirm grout flows from exit pit vent during grouting operation; if directed by Engineer, core drill or probe grouted annular space at [TBD] locations to verify complete filling

4.4.5. **Submittals sub-section**:
- Boring plan: Contractor shall submit boring plan minimum [TBD – typically 30 days] before commencing boring work, including:
  - Proposed boring method and equipment specifications
  - Soil investigation results: Test pits or soil borings at entry and exit pit locations to confirm geotechnical conditions (soil type, groundwater level, rock depth if applicable)
  - Jacking force calculations (for auger boring or pipe jacking) or pullback force calculations (for HDD) demonstrating casing pipe and joints can withstand installation stresses without damage; calculations shall account for soil friction, soil type, alignment (horizontal or inclined), and safety factors
  - Settlement predictions: Estimated ground surface settlement during boring based on boring method, soil conditions, and experience from similar projects; settlement predictions shall demonstrate compliance with settlement limits
  - Existing utility locations: Existing utilities verified by potholing, non-destructive investigation (ground penetrating radar, utility locating), or review of existing utility records; boring alignment shall maintain required clearances from existing utilities
  - QA/QC procedures: Alignment monitoring and verification methods, weld inspection procedures and frequencies, grouting verification methods, settlement monitoring plan (monitoring points, monitoring frequency, settlement limits triggering corrective actions)
  - Contingency plans: Corrective actions if alignment deviates from tolerances, if settlement exceeds limits, if casing pipe or joints are damaged during installation, if existing utilities are encountered
- Submittal review: Engineer will review boring plan within [TBD – typically 15-20 working days] and provide comments or approval; Contractor shall not commence boring until boring plan is approved; if significant deviations from approved plan are required during execution, Contractor shall submit revised plan for approval before proceeding

4.4.6. **Testing and inspection sub-section**:
- Alignment verification: Survey casing pipe alignment at exit pit (measure horizontal and vertical position relative to design alignment from DEL-03.01 Drawing Set), confirm deviation is within specified tolerances, document survey results
- Weld inspection: Visual inspection and non-destructive testing per casing pipe installation sub-section above, document inspection results (weld location, inspection method, acceptance/rejection, repair if required)
- Settlement monitoring: Monitor ground surface settlement at monitoring points during boring, document settlement readings (date, time, settlement magnitude), compare to settlement limits, implement corrective actions if settlement approaches limits (slow advance rate, modify boring method, grout voids if settlement caused by soil loss)
- Carrier pipe testing: After carrier pipe installation and grouting complete, perform hydrostatic pressure test per Section 2 storm drainage testing requirements if carrier pipe is pressure pipe; perform CCTV inspection per DEL-03.06 if carrier pipe is gravity storm drainage pipe
- Documentation: Boring records (alignment surveys, boring logs, advance rate records, settlement monitoring records), weld inspection reports, grouting records (grout volume, grouting procedure, venting confirmation), test results (carrier pipe hydrostatic test or CCTV inspection) documented per DEL-03.05 Installation and Test Records
- Coordinate testing requirements with DEL-03.05 and DEL-03.06 per Specification §IF-1 and Guidance §P-4.

**Verification**: Trenchless crossing specification section draft reviewed for completeness (performance requirements, boring methods, casing installation, carrier pipe and grouting, submittals, testing all addressed), performance-based approach allows contractor flexibility while ensuring performance compliance.

**Output**: Trenchless crossing specification section drafted; ready for review.

**Cross-reference**: Guidance §T-3 trenchless crossing specification detail trade-off (performance-based with contractor-submitted boring plan approach); Guidance §Example 4 trenchless crossing performance-based specification; Specification §Scope trenchless crossing specification; Datasheet §Construction trenchless crossing specification content.

---

### Step 5: Environmental Protection Requirements Definition

**Objective**: Ensure OWS performance criteria, discharge limits, and monitoring protocols clearly support **OBJ-7 Environmental Protection** compliance and regulatory permitting.

**Actions**:
5.1. Review OWS specification section (developed in Step 4.2) for environmental protection emphasis:
- Treatment performance criteria (oil removal efficiency, solids settling capacity, flow rate capacity) are clearly defined with numerical values from DEL-03.03 calculations and environmental permit conditions (or ER Volume 2 Part 2 if permit not yet issued).
- Discharge limits (oil content, suspended solids, pH, other parameters) are clearly defined with numerical limits matching environmental permit conditions or ER Volume 2 Part 2 requirements.
- Instrumentation and monitoring requirements (level sensors, flow meters, sampling ports, data logging) support discharge compliance monitoring and regulatory reporting.
- Performance testing protocol provides objective verification that OWS meets treatment efficiency and discharge limits before facility operations commence.

5.2. Coordinate environmental protection requirements with environmental permit conditions:
- If environmental discharge permit is available, extract discharge limits from permit and incorporate into OWS specification discharge limits sub-section; include permit number and issuing agency reference.
- If permit is not yet issued, coordinate with environmental permitting team to confirm anticipated discharge limits; include statement in specification: "Discharge limits are preliminary pending environmental permit issuance; Contractor shall verify final discharge limits with Engineer before OWS equipment procurement."

5.3. Coordinate environmental protection requirements with Employer's Requirements Volume 2 Part 2:
- Extract environmental protection requirements from ER Volume 2 Part 2 (if available); incorporate into OWS specification performance criteria and discharge limits.
- If ER environmental requirements are not yet extracted, include placeholder: "Environmental protection requirements per Employer's Requirements Volume 2 Part 2 Section [TBD]; Contractor shall confirm requirements with Engineer before OWS equipment procurement."

5.4. Add general environmental protection statement to specification general requirements section:
- "Storm drainage and OWS systems are designed to support **OBJ-7 Environmental Protection** per project objectives (test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786). OWS treatment performance and discharge quality shall comply with environmental permit conditions [permit number TBD] and Employer's Requirements Volume 2 Part 2 environmental protection criteria. OWS performance testing and commissioning per Section 3 shall demonstrate compliance before facility operations commence."

**Verification**: Environmental protection requirements review confirms OWS performance criteria and discharge limits clearly support OBJ-7 compliance; environmental permit conditions (or anticipated limits) are incorporated; performance testing protocol provides objective verification.

**Output**: Environmental protection requirements clearly defined in specification; OBJ-7 emphasis documented.

**Cross-reference**: Specification §FR-2 environmental protection performance; Specification §PR-2 OWS treatment capacity and containment performance; Guidance §P-2 environmental protection performance (OBJ-7); Datasheet §Conditions OBJ-7 environmental protection emphasis.

---

### Step 6: Metadata and Revision History Compilation

**Objective**: Populate specification metadata (document number, revision, author/checker/approver, issue date) and compile revision history per document control procedures.

**Actions**:
6.1. Assign document number per project numbering system:
- Obtain document number from project document control register or coordinator.
- Populate specification cover page or header "Document Number" field (Datasheet §Attributes notes numbering system TBD; Specification §FR-4 document metadata requirement).

6.2. Set initial revision code:
- Initial issue revision is "00" per Datasheet §Attributes.
- Populate specification cover page "Revision" field with "00" and issue description "Issued for Review" or "Issued for Construction" per project conventions (Specification §QR-2 specification status codes).

6.3. Populate author/checker/approver fields:
- Author: Name and signature of specification writer who produced specification
- Checker: Name and signature field (to be completed after interdisciplinary check, Step 7.2)
- Approver: Name and signature field (to be completed after independent check, Step 7.3)

6.4. Compile revision history:
- Populate specification cover page or revision history section with revision number, date, description, author/checker/approver initials.
- Initial issue: "Rev 00, [Date], Issued for Review, [Initials]"
- Subsequent revisions (if issued after review comments): "Rev 01, [Date], Issued for Construction incorporating review comments, [Initials]"

6.5. Confirm cover page template matches project document control requirements:
- Verify cover page includes all required fields: Project name, deliverable ID (DEL-03.02), specification title, document number, revision, issue date, author, checker, approver, project location.

**Verification**: Metadata completeness checklist confirms all cover page fields are populated (except checker/approver signatures pending review); checklist reviewed during self-check (Step 7.1) and QA review (Step 7.3).

**Output**: Specification metadata populated; ready for review workflow.

**Cross-reference**: Specification §FR-4 document metadata and document control; Specification §QR-2 specification review and approval process; Datasheet §Attributes metadata fields.

---

### Step 7: Verification and QA/QC Review

**Objective**: Execute self-check, interdisciplinary check, and independent check to verify compliance with Specification requirements and validate specification completeness, technical accuracy, and coordination.

#### Step 7.1: Self-Check (Originator Review)

**Actions**:
7.1.1. **Completeness check**: Confirm all anticipated specification sections (Specification §Scope list) are present and complete:
- General requirements ✓
- Storm drainage system ✓
- OWS system ✓
- Duct bank system ✓
- Trenchless crossing system ✓
- Backfill and restoration ✓

7.1.2. **Technical accuracy check**: Verify material specifications, performance criteria, installation requirements are technically accurate:
- Material standard references correct (CSA, ASTM section numbers and titles verified against actual standards)
- Performance criteria (hydraulic capacity, OWS treatment efficiency, structural loading, design life) match DEL-03.03 Design Calculations results
- Installation requirements are constructible (tolerances achievable, procedures practical, equipment and methods available)
- Testing requirements align with industry standards (ASTM, CSA, NASSCO test methods referenced correctly)

7.1.3. **Coordination check**: Verify specification coordinates with related deliverables:
- References to DEL-03.01 Drawing Set are correct (drawing sheet numbers, detail callouts)
- References to DEL-03.03 Design Calculations are correct (calculation sheet numbers, calculated values)
- References to DEL-03.04 Data Sheet Package are appropriate (OWS equipment data sheet referenced in OWS section)
- References to DEL-03.05 Installation and Test Records are appropriate (testing and inspection documentation requirements)
- References to DEL-03.06 CCTV Survey Report are appropriate (CCTV inspection requirements in storm drainage section)

7.1.4. **Clarity check**: Verify specification language is clear and unambiguous per Guidance §P-3 material and workmanship clarity principle:
- Material specifications reference specific standards with section numbers (not vague descriptions)
- Installation requirements define objective tolerances and procedures (not subjective "satisfactory workmanship" language)
- Testing acceptance criteria are objective (numerical limits, pass/fail criteria)
- Submittal requirements are clear (what to submit, when to submit, what data to include)

7.1.5. **Metadata completeness check**: Verify cover page metadata is populated per Step 6 (document number, revision, author name, issue date).

7.1.6. **OBJ-7 environmental protection check**: Verify OWS performance criteria, discharge limits, and monitoring requirements clearly support environmental compliance per Step 5 environmental protection requirements definition.

**Verification**: Self-check checklist completed and signed by originator; checklist documents all review items completed and any issues identified for correction before interdisciplinary check.

**Output**: Specification passes self-check; ready for interdisciplinary review.

---

#### Step 7.2: Interdisciplinary Check

**Actions**:
7.2.1. **Distribute specification for interdisciplinary review**: Share specification (PDF or Word document) with adjacent discipline leads and related deliverable leads:
- PKG-02 Site Grading: Review backfill specifications, compaction requirements, coordination with site grading requirements
- PKG-04 Pavement and Surfacing: Review pavement restoration specifications (Section 6), coordination with pavement structural sections and warranty requirements
- PKG-17 Electrical Power Distribution: Review duct bank specifications (Section 4), conduit material specifications, concrete encasement requirements, coordination with electrical design assumptions
- PKG-14 Process Piping: Review utility separation requirements, crossing details coordination
- DEL-03.03 Design Calculations lead: Review performance criteria (hydraulic capacity, OWS treatment efficiency, structural loading) for alignment with calculation results
- DEL-03.01 Drawing Set lead: Review geometry references (drawing sheet callouts, detail references) for accuracy
- DEL-03.05 Installation and Test Records lead: Review testing and inspection requirements for coordination with installation records documentation plan

7.2.2. **Coordination meeting**: Conduct interdisciplinary coordination meeting (or review workshop) to discuss comments:
- Review coordination comments from each discipline
- Identify and resolve conflicts (specification requirements conflicting with adjacent discipline requirements or assumptions)
- Document agreed resolutions and action items

7.2.3. **Incorporate interdisciplinary review comments**: Update specification to address coordination comments:
- Revise material specifications, installation requirements, or testing requirements to resolve conflicts or incorporate coordination feedback
- Add coordination notes or clarifications requested by reviewers
- Update references to related deliverables if drawing numbers, calculation sheet numbers, or other references change
- Document changes in revision history (if issuing revised specification for re-review)

7.2.4. **Obtain interdisciplinary review sign-offs**: Collect sign-off confirmation from adjacent discipline leads and related deliverable leads:
- Sign-off indicates discipline has reviewed specification and coordination conflicts are resolved
- Sign-offs may be email confirmations, review comment log closeout signatures, or formal review stamps on specification cover page (per project QA procedures)

**Verification**: Interdisciplinary review log documents comments received, resolutions, and sign-offs; checker signature on specification cover page confirms interdisciplinary coordination review completed.

**Output**: Specification passes interdisciplinary check; coordination with adjacent disciplines and related deliverables validated; ready for independent check.

**Cross-reference**: Specification §IF-1 coordination with related deliverables; Specification §IF-2 coordination with adjacent packages; Guidance §P-4 coordination with installation records; Guidance §C-4 QA coordination and sign-offs.

---

#### Step 7.3: Independent Check

**Actions**:
7.3.1. **Compliance with standards check**: Independent reviewer verifies compliance with:
- Employer's Requirements Volume 2 Part 2 (Civil & Process Mechanical Works): Extract applicable clauses, verify specification requirements comply with ER (Specification §Standards governing standards)
- Applicable codes and regulations: NBC, BCBC, CSA standards, ASTM standards, local municipal standards, environmental regulations (Specification §Standards assumed applicable codes)
- Civil design brief: Design life, seismic design category, design storm event, other design parameters (Specification §PR-3 design life and environmental conditions)

7.3.2. **Performance validation**: Independent reviewer validates specification performance requirements against design inputs:
- Verify storm drainage material specifications support hydraulic capacity and structural loading from DEL-03.03 Design Calculations per Specification §PR-1
- Verify OWS performance criteria (treatment flow rate, removal efficiency, discharge limits) match DEL-03.03 calculations and environmental permit conditions (or ER Volume 2 Part 2) per Specification §PR-2
- Verify trenchless crossing casing specifications (material, wall thickness) support jacking forces and external loading from DEL-03.03 structural analysis
- Confirm specification material requirements (pipe materials, concrete, backfill) are compatible with design parameters (design life, environmental conditions) from civil design brief per Specification §PR-3

7.3.3. **Environmental protection compliance check**: Independent reviewer confirms environmental protection requirements support **OBJ-7 Environmental Protection** per Specification §FR-2 and Guidance §P-2:
- OWS treatment performance criteria clearly defined (Step 5.1)
- Discharge limits clearly defined and aligned with environmental permit or ER (Step 5.2 and 5.3)
- Instrumentation and monitoring requirements support discharge compliance monitoring (Step 5.1)
- Performance testing protocol provides objective verification (Step 5.1)
- Environmental protection general statement included in general requirements (Step 5.4)

7.3.4. **Quality requirements compliance check**: Independent reviewer verifies QA compliance per Specification §QR-1, §QR-2, §QR-3:
- Specification development followed QA procedures: originator prepared, checker reviewed, approver signs (Specification §QR-1)
- Submittal requirements section is complete and clear (material submittals, shop drawings, product data, test plans) per Specification §QR-1
- Review checkpoints completed: Self-check checklist ✓, interdisciplinary review log ✓, independent check in progress ✓ (Specification §QR-2)
- Testing and inspection requirements are complete with clear acceptance criteria per Specification §QR-3 (hydrostatic testing, CCTV inspection, OWS performance testing, duct bank continuity testing)

7.3.5. **Traceability verification**: Independent reviewer confirms specification references to related deliverables are correct per Specification §IF-1:
- References to DEL-03.01 Drawing Set cite correct drawing sheet numbers and detail callouts
- References to DEL-03.03 Design Calculations cite correct calculation sheet numbers and calculated values
- References to DEL-03.04 Data Sheet Package are appropriate (OWS equipment data sheet)
- References to DEL-03.05 Installation and Test Records are appropriate (testing documentation requirements)
- References to DEL-03.06 CCTV Survey Report are appropriate (CCTV inspection requirements)

7.3.6. **Record review results**: Independent reviewer documents findings in review signature block on specification cover page:
- "Reviewed for compliance with Employer's Requirements, civil standards, and design calculations. Approved for issue." [Signature, Date]
- If issues are found: "Reviewed for compliance. Revise and resubmit per attached comment log." [Signature, Date]

**Verification**: Independent check review signature on specification cover page confirms compliance verification completed; QA checklist documents all review items completed and any issues resolved before issue.

**Output**: Specification passes independent check; approved for issue into document control system.

**Cross-reference**: Specification §Verification independent check; Specification §QR-1 quality management compliance; Specification §QR-2 specification review and approval process; Specification §PR-1, §PR-2, §PR-3 performance requirements.

---

### Step 8: Issue into Document Control System

**Objective**: Package specification for issue into project document control system; create issue register entry and distribute to material suppliers, contractors, and stakeholders.

**Actions**:
8.1. Finalize specification package:
- Ensure specification cover page has complete signatures (author, checker, approver)
- Ensure revision code and issue description are correct
- Compile specification into single PDF document (or Word document per project conventions)
- Include cover letter or transmittal memo listing specification sections, issue purpose (e.g., "Issued for Review", "Issued for Construction"), and distribution list

8.2. Submit to document control coordinator:
- Upload specification to project document management system (e.g., ProjectWise, SharePoint, or other system per project conventions)
- Complete document control submission form with document number, revision, issue status, distribution list

8.3. Create issue register entry:
- Document control coordinator creates issue register entry with:
  - Document number and revision issued
  - Issue date
  - Issue status (e.g., "Issued for Review", "Issued for Construction")
  - Distribution list (material suppliers, construction contractors, adjacent disciplines, QA/QC team, operations as applicable)
  - Transmittal number or reference

8.4. Distribute specification per distribution list:
- Document control coordinator distributes specification to material suppliers (for submittal preparation), construction contractors (for installation execution), adjacent disciplines, and stakeholders
- Distribution may be via document management system notifications, email transmittals, or hard copy distribution per project procedures

8.5. Archive quality records:
- Retain specification review logs, QA checklists, interdisciplinary review comments and resolutions, independent check review signature in project files per Specification §Documentation associated quality records
- Archive records per project document retention policy (typically 7+ years for design-build contracts; per Employer's Requirements Volume 2 Part 1)

**Verification**: Issue register entry confirms specification is issued into document control system; distribution confirmation (read receipts, acknowledgment emails) confirms stakeholders received specification.

**Output**: Specification issued into document control system; available for material procurement and construction use.

**Cross-reference**: Specification §FR-4 document metadata and document control; Specification §QR-2 specification review and approval process; Specification §Documentation format, numbering, and revision control; Datasheet §Conditions specification control alignment.

---

## Verification

This section consolidates verification activities described in Steps 7.1, 7.2, 7.3 above. Each verification activity ties to specific Specification requirements.

**Self-Check (Originator Review) – Step 7.1:**
- **Purpose**: Ensures specification sections are complete, material specifications are technically accurate, performance criteria match design calculations, installation requirements are clear and constructible, testing requirements are defined with acceptance criteria, coordination references are correct, and metadata is complete.
- **Ties to requirements**: Specification §FR-1 comprehensive performance and materials, §FR-4 document metadata, §QR-2 specification clarity; Datasheet §Attributes metadata fields; Guidance §P-3 material and workmanship clarity.
- **Output**: Self-check checklist completed and signed by originator.

**Interdisciplinary Check – Step 7.2:**
- **Purpose**: Verifies coordination with design drawings (DEL-03.01), design calculations (DEL-03.03), equipment data sheets (DEL-03.04), installation records (DEL-03.05), CCTV survey report (DEL-03.06), and adjacent disciplines (PKG-02 backfill, PKG-04 pavement restoration, PKG-17 duct bank, PKG-14 utility separations) per IF-1 and IF-2 requirements.
- **Ties to requirements**: Specification §IF-1 coordination with related deliverables, §IF-2 coordination with adjacent packages; Guidance §P-4 coordination with installation records; Guidance §C-4 QA coordination.
- **Output**: Interdisciplinary review log with comments, resolutions, and sign-offs; checker signature on specification cover page confirms coordination review completed.

**Independent Check – Step 7.3:**
- **Purpose**: Confirms compliance with Employer's Requirements (Volume 2 Part 2) and applicable standards (Standards section); validates specification material requirements support performance requirements (PR-1, PR-2, PR-3) and design calculation results (DEL-03.03); ensures environmental protection requirements (FR-2, PR-2) support OBJ-7 objectives and regulatory compliance; confirms testing and inspection requirements (QR-3) are complete with clear acceptance criteria; verifies submittal requirements (QR-1) are clear; verifies traceability (IF-1) to related deliverables; records results in review signature block.
- **Ties to requirements**: Specification §PR-1 hydraulic and structural performance, §PR-2 OWS treatment capacity, §PR-3 design life and environmental conditions, §FR-2 environmental protection performance, §IF-1 linkage to related deliverables, §QR-1 quality management compliance, §QR-3 testing and inspection requirements; Guidance §P-2 environmental protection performance (OBJ-7).
- **Output**: Independent check review signature on specification cover page confirms compliance verification; QA checklist documents review completion.

**Technical Accuracy Verification:**
- Material specifications reviewed against manufacturer product data, industry standards (CSA, ASTM), and Employer's Requirements to confirm technical accuracy and product availability.
- Performance criteria (hydraulic capacity, OWS treatment efficiency, structural loading) verified against design calculation results (DEL-03.03) to ensure specification requirements align with design performance (interface linkage per IF-1).
- Installation requirements reviewed for constructibility and alignment with construction industry best practices.
- Results recorded in specification review records and QA checklists per QR-1.

**Traceability Verification:**
- Specification sections reference Drawing Set (DEL-03.01), Design Calculations (DEL-03.03), Data Sheet Package (DEL-03.04), Installation and Test Records (DEL-03.05), and CCTV Survey Report (DEL-03.06) for geometry, performance basis, equipment details, testing documentation, and inspection results per IF-1 linkage requirement (Step 7.1.3 and Step 7.3.5).
- Specification general requirements section references applicable Employer's Requirements clauses, standards, and codes to maintain traceability to governing documents.

**Requirement Traceability Summary:**
- Each Specification functional requirement (§FR-1 to §FR-4) has corresponding verification step in this Procedure (Steps 7.1 completeness and clarity checks, 7.3.3 environmental protection check, 7.2 coordination check, 7.1.5 metadata check).
- Each Specification performance requirement (§PR-1 to §PR-3) has independent check validation in Step 7.3.2.
- Each Specification interface requirement (§IF-1 to §IF-2) has interdisciplinary check or traceability verification in Steps 7.2 and 7.3.5.
- Each Specification quality requirement (§QR-1 to §QR-3) has QA review checkpoint in Steps 7.1.4, 7.2, 7.3.4.

---

## Records

**Specification Deliverables (Specification §Scope and §Documentation):**
- General requirements section (scope, references, definitions, submittals, quality assurance, delivery/storage/handling)
- Storm drainage system specification (materials, installation, testing and inspection)
- Oil-water separator system specification (performance criteria, materials, instrumentation, installation, performance testing)
- Duct bank system specification (conduit materials, concrete encasement, pull boxes, installation, testing)
- Trenchless crossing system specification (boring methods, casing and carrier pipes, grouting, testing)
- Backfill and restoration specification (backfill materials, compaction, pavement restoration)
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:199 anticipated specification sections; detailed in Specification §Scope and Datasheet §Construction.)

**Quality Records (Specification §Documentation associated quality records):**
- **Self-check checklist**: Documents originator review completion per Step 7.1; includes completeness, technical accuracy, coordination, clarity, metadata checks.
- **Interdisciplinary review log**: Documents coordination comments from related deliverables (DEL-03.01/03/04/05/06) and adjacent packages (PKG-02/04/14/17); resolutions; sign-offs per Step 7.2.
- **Independent check review signature**: Documents independent reviewer compliance verification per Step 7.3; includes review findings and approval signature on specification cover page.
- **QA checklists**: Documents QA compliance verification (QA procedures followed, review checkpoints completed, standards compliance met, testing requirements complete) per Specification §QR-1, §QR-2, §QR-3 and Step 7.3.4.
- **Issue register entry**: Documents specification issue into document control system per Step 8.3; includes document number, revision, issue date, issue status, distribution list.
- **Specification review logs**: Consolidated record of self-check, interdisciplinary check, and independent check activities; retained per project document retention policy.
(All records retained per project document control procedures per test/Volume_2_Part_1_Employers_Requirements.pdf and Specification §QR-1 quality management compliance.)

**Related Deliverable Cross-References:**
- DEL-03.01 Drawing Set: Pipe alignments, elevations, OWS layout, duct bank routing, crossing locations referenced for geometry context (Specification §IF-1; Step 2.2 input data collection).
- DEL-03.03 Design Calculations: Hydraulic calculations, OWS sizing, structural analysis provide performance basis for specification requirements (Specification §PR-1, §PR-2, §PR-3; Step 2.1 input data collection; Step 7.3.2 performance validation).
- DEL-03.04 Data Sheet Package: OWS equipment data sheet referenced in OWS specification performance criteria (Specification §PR-2; Step 2.3 coordination; Step 4.2 OWS specification development).
- DEL-03.05 Installation and Test Records: Testing and inspection documentation requirements referenced in specification testing sections (Specification §IF-1 and §QR-3; Step 2.3 coordination; Step 4 testing requirements development; Step 7.2 interdisciplinary check).
- DEL-03.06 CCTV Survey Report: CCTV inspection requirements specified in storm drainage testing section (Specification §IF-1; Step 4.1.4 storm drainage testing requirements).

---

## Cross-Document Notes

**Procedure → Specification:**
- Steps 1-8 implement Specification requirements: Step 1 implements §Scope, Steps 2-6 implement §Requirements, Step 7 implements §Verification, Step 8 implements §Documentation.
- Step 7.1 self-check implements Specification §Verification self-check; Step 7.2 interdisciplinary check implements Specification §Verification interdisciplinary check; Step 7.3 independent check implements Specification §Verification independent check.
- Prerequisites section lists reference materials required by Specification §Standards (Employer's Requirements, CSA/ASTM standards, civil design brief, geotechnical report).
- Step 5 environmental protection requirements definition implements Specification §FR-2 environmental protection performance requirement and §PR-2 OWS treatment capacity and containment performance.
- Step 7.2 interdisciplinary check implements Specification §IF-1 coordination with related deliverables and §IF-2 coordination with adjacent packages.
- Step 7.3.5 traceability verification implements Specification §IF-1 linkage to related deliverables.

**Procedure → Datasheet:**
- Steps 4.1-4.4 specification section development produce specification content described in Datasheet §Construction (storm drainage, OWS, duct banks, trenchless crossings specification sections).
- Step 6 metadata compilation populates specification cover page fields listed in Datasheet §Attributes (document number, revision, author, checker, approver).
- Step 8 issue into document control implements specification control alignment per Datasheet §Conditions operational context.

**Procedure → Guidance:**
- Steps 4.1-4.4 specification section development implement Guidance principles: Step 4.1 implements §P-1 hydraulic performance and durability, Step 4.2 and Step 5 implement §P-2 environmental protection performance, Step 4 implements §P-3 material and workmanship clarity, Steps 4 and Step 7.2 implement §P-4 coordination with installation records.
- Prerequisites section addresses Guidance considerations: Prerequisites design calculation inputs address §C-1 design calculation availability, Prerequisites ER Volume 2 Part 2 reference address §C-2 ER extraction, Step 1 scope review addresses §C-3 section structure and scope boundaries, Step 7 verification addresses §C-4 QA coordination and sign-offs, Steps 4 specification section development address §C-5 construction use and material flexibility.
- Steps 4.1-4.4 specification section development resolve or document Guidance trade-offs: Step 4 material and installation requirements resolve §T-1 performance vs prescriptive (hybrid approach), Step 4.2 OWS requirements resolve §T-2 OWS treatment technology selection (performance-based with pre-qualified manufacturers), Step 4.4 trenchless crossing requirements resolve §T-3 trenchless crossing specification detail (performance-based with contractor-submitted boring plan), Step 4.3 duct bank requirements resolve §T-4 duct bank specification coordination (civil spec for trench/concrete + reference to PKG-17 for conduit details).
- Steps 4.1-4.4 specification section development examples correspond to Guidance §Examples 1-4: Step 4.1 implements Example 1 storm drainage specification structure, Step 4.2 and Step 5 implement Example 2 OWS performance criteria specification, Step 4.3 implements Example 3 duct bank material requirements, Step 4.4 implements Example 4 trenchless crossing performance-based specification.

**Workflow Completeness Check:**
- Specification requirement → Procedure step → Verification checkpoint mapping ensures every requirement is implemented in workflow and verified before issue:
  - §FR-1 comprehensive performance and materials → Steps 4.1-4.4 specification section development → Step 7.1 completeness and technical accuracy check ✓
  - §FR-2 environmental protection performance → Step 5 environmental protection requirements definition → Step 7.3.3 environmental protection compliance check ✓
  - §FR-3 coordination with electrical infrastructure → Step 4.3 duct bank specification + Step 7.2 PKG-17 coordination review ✓
  - §FR-4 document metadata → Step 6 metadata compilation → Step 7.1.5 metadata completeness check ✓
  - §PR-1 hydraulic and structural performance → Steps 2.1, 4.1 design inputs and storm drainage specification → Step 7.3.2 performance validation ✓
  - §PR-2 OWS treatment capacity and containment → Steps 2.1, 4.2, 5 design inputs, OWS specification, environmental protection requirements → Step 7.3.2 performance validation ✓
  - §PR-3 design life and environmental conditions → Prerequisites civil design brief and geotechnical report, Steps 2.1, 4 design inputs and specification sections → Step 7.3.2 performance validation ✓
  - §IF-1 coordination with related deliverables → Prerequisites and Step 2 input data collection → Step 7.2 interdisciplinary check + Step 7.3.5 traceability verification ✓
  - §IF-2 coordination with adjacent packages → Step 2 coordination data collection → Step 7.2 interdisciplinary check ✓
  - §QR-1 quality management compliance → Steps 7-8 QA/QC review workflow → Step 7.3.4 quality requirements compliance check ✓
  - §QR-2 specification review and approval → Steps 7-8 review workflow and issue → Step 8 issue register entry ✓
  - §QR-3 testing and inspection requirements → Step 4 testing requirements development (Steps 4.1.4, 4.2.5, 4.3.5, 4.4.6) → Step 7.3.4 testing requirements completeness check ✓

---

## Pass 2 Enrichments

This Pass 2 revision adds:
1. Expanded Purpose section with production purpose and quality assurance purpose clarifying dual intent of procedure (produce specification + execute QA workflow).
2. Detailed Prerequisites section with dependencies, reference materials, design intent understanding, and personnel requirements clearly listing what must be available before starting work.
3. Detailed Steps (Steps 1-8) breaking down specification development workflow into discrete phases with clear objectives, actions, verification checkpoints, and outputs for each step.
4. Expanded specification section development steps (Steps 4.1-4.4) with detailed actions for storm drainage, OWS, duct banks, and trenchless crossings implementing Guidance principles and examples.
5. Dedicated environmental protection requirements definition step (Step 5) implementing Specification §FR-2 and Guidance §P-2 (OBJ-7) with specific actions for OWS performance criteria, discharge limits, instrumentation, and performance testing.
6. Detailed metadata and revision history compilation step (Step 6) implementing Specification §FR-4 and Datasheet §Attributes metadata requirements.
7. Comprehensive verification section (Step 7) with detailed self-check, interdisciplinary check, and independent check procedures showing exactly what reviewers must verify and how verification ties to Specification requirements.
8. Issue into document control step (Step 8) implementing Specification §Documentation and §QR-2 with clear actions for finalizing specification, submitting to document control, creating issue register entry, distributing specification, and archiving quality records.
9. Enhanced Records section listing all specification deliverables (sections), quality records, and related deliverable cross-references.
10. Comprehensive cross-document notes showing how Procedure steps implement Specification requirements, produce Datasheet content, and apply Guidance principles/considerations/trade-offs.
11. Workflow completeness check table confirming every Specification requirement has corresponding Procedure step and verification checkpoint (requirement → implementation → verification traceability).

## Pass 3 Final Notes

**Pass 3 Reconciliation Completed:**
- All Specification requirements have corresponding Procedure implementation steps and verification checkpoints (workflow completeness check at end of §Cross-Document Notes confirms requirement → implementation → verification traceability).
- All Guidance principles have corresponding Procedure implementation:
  - Guidance §P-1 hydraulic performance and durability → Procedure §4.1 storm drainage specification with performance basis and material requirements supporting calculated performance
  - Guidance §P-2 environmental protection performance (OBJ-7) → Procedure §5 environmental protection requirements definition + §4.2 OWS specification + §7.3.3 compliance check
  - Guidance §P-3 material and workmanship clarity → Procedure §4 specification sections with clear material standards references, objective installation tolerances, objective testing acceptance criteria + §7.1.4 clarity check
  - Guidance §P-4 coordination with installation records → Procedure §2.3 coordination with DEL-03.05 structure + §4 testing requirements development coordinated with DEL-03.05 + §7.2 interdisciplinary check includes DEL-03.05 review
- All Guidance considerations addressed in Procedure prerequisites or workflow:
  - Guidance §C-1 design calculation availability → Procedure §Prerequisites DEL-03.03 inputs + §2.1 collect design calculation outputs + §2.4 confirm data availability status
  - Guidance §C-2 ER extraction → Procedure §Prerequisites ER Volume 2 Part 2 as required reference + §2.5 document data sources including ER + §7.3.1 compliance check
  - Guidance §C-3 section structure and scope boundaries → Procedure §1 scope and objectives review + §3.2 specification section structure establishment
  - Guidance §C-4 QA coordination and sign-offs → Procedure §Prerequisites personnel requirements + §7 verification workflow with three review levels (self-check, interdisciplinary check, independent check) + sign-off collection
  - Guidance §C-5 construction use and material flexibility → Procedure §4 specification section development implements balanced approach (clear material standards + allow contractor alternatives meeting performance)
- All Guidance trade-offs have implementation decisions in Procedure workflow:
  - Guidance §T-1 performance vs prescriptive → Procedure §4 specification sections implement hybrid approach (performance requirements + acceptable materials list + "or equal" provisions per §T-1 decision guidance)
  - Guidance §T-2 OWS treatment technology selection → Procedure §4.2 and §5 OWS specification implements performance-based with pre-qualified manufacturers approach (performance criteria defined, allow equipment suppliers to propose technology, pre-qualify manufacturers with proven installations per §T-2 decision guidance)
  - Guidance §T-3 trenchless crossing specification detail → Procedure §4.4 trenchless crossing specification implements performance-based with contractor-submitted boring plan approach (performance requirements defined, contractor proposes boring method and procedures, submittal review and approval required per §T-3 decision guidance)
  - Guidance §T-4 duct bank specification coordination → Procedure §4.3 duct bank specification implements civil spec for trench/concrete + reference to PKG-17 for conduit details approach (clear scope interface, coordination notes, conduit schedule from PKG-17 incorporated for trench sizing per §T-4 decision guidance)
- All Guidance examples have corresponding Procedure detailed specification section development steps:
  - Guidance §Example 1 storm drainage → Procedure §4.1 develop storm drainage specification requirements (implements example section structure with general requirements, materials, installation, testing sub-sections)
  - Guidance §Example 2 OWS performance criteria → Procedure §4.2 develop OWS specification requirements + §5 environmental protection requirements definition (implements example performance requirements, materials, instrumentation, installation, performance testing sub-sections)
  - Guidance §Example 3 duct bank materials → Procedure §4.3 develop duct bank specification requirements (implements example conduit materials, concrete encasement, pull boxes, installation, testing sub-sections)
  - Guidance §Example 4 trenchless crossing performance-based → Procedure §4.4 develop trenchless crossing specification requirements (implements example performance requirements, boring methods, casing installation, carrier pipe and grouting, submittals, testing sub-sections)

**Workflow Integrity Verification:**
- Every Specification requirement (FR-1 to FR-4, PR-1 to PR-3, IF-1 to IF-2, QR-1 to QR-3) has:
  - Implementation step(s) in Procedure §Steps producing specification content that satisfies the requirement
  - Verification checkpoint in Procedure §Verification confirming requirement is met before issue
  - Cross-reference to Guidance rationale explaining why requirement exists
  - Cross-reference to Datasheet content that requirement applies to
- Prerequisites section completeness verified:
  - Dependencies clearly state NOT_TRACKED mode and list required inputs from DEL-03.01/03/04/05 and design calculations (DEL-03.03)
  - Reference materials list all governing documents (ER Volume 2 Part 1 & 2, CSA/ASTM standards, civil design brief, geotechnical report, project specification standards, package reference index)
  - Design intent understanding guides originator to review Specification, Guidance, and downstream use context before starting
  - Personnel requirements identify originator, checker, approver, and adjacent discipline reviewers roles
- Steps section workflow verified:
  - Step 1 scope review → confirms what to produce (anticipated specification sections) and why (OBJ-7, requirements, exclusions)
  - Step 2 input data collection → gathers design calculation outputs, design drawing information, related deliverable information, confirms data availability
  - Step 3 specification section structure establishment → establishes section organization matching anticipated sections, creates table of contents
  - Step 4 specification section development → produces detailed content for all anticipated specification sections (storm drainage, OWS, duct banks, trenchless crossings) with materials, installation, testing requirements
  - Step 5 environmental protection requirements definition → implements OBJ-7 emphasis with clear OWS performance criteria, discharge limits, instrumentation, monitoring, performance testing
  - Step 6 metadata compilation → populates specification cover page with document number, revision, author/checker/approver, issue date per document control procedures
  - Step 7 verification workflow → executes self-check (originator), interdisciplinary check (related deliverables and adjacent packages coordination), independent check (compliance with ER and standards, performance validation) with documented checklists and review logs
  - Step 8 issue into document control → packages specification, submits to document control, creates issue register entry, distributes to stakeholders, archives quality records
- Verification section completeness verified:
  - Self-check (§7.1) covers completeness, technical accuracy, coordination, clarity, metadata completeness, OBJ-7 environmental protection
  - Interdisciplinary check (§7.2) covers coordination with DEL-03.01/03/04/05/06 and PKG-02/04/14/17, conflict resolution, coordination meeting, review comment incorporation, sign-off collection
  - Independent check (§7.3) covers compliance with ER and standards, performance validation against DEL-03.03, environmental protection compliance, quality requirements compliance, traceability verification, review results documentation
  - Each verification activity ties to specific Specification requirements (verification traceability documented)
- Records section completeness verified:
  - Specification deliverables list matches Datasheet §Construction specification organization and Specification §Scope anticipated sections exactly
  - Quality records list includes all QA documentation (self-check checklist, interdisciplinary review log, independent check review signature, QA checklists, issue register entry, specification review logs) per Specification §Documentation
  - Related deliverable cross-references match Specification §IF-1 linkages (DEL-03.01, DEL-03.03, DEL-03.04, DEL-03.05, DEL-03.06)

**Entity Coverage Verification:**
- All anticipated specification sections (storm drainage, OWS, duct banks, trenchless crossings, general requirements, backfill/restoration) have production steps in Procedure §4 and documentation in Procedure §Records, matching Datasheet §Construction, Specification §Scope, and Guidance §Examples.
- OBJ-7 Environmental Protection theme implemented via Procedure §5 environmental protection requirements definition with four specific actions (OWS performance criteria, discharge limits coordination with permit, ER coordination, environmental protection general statement) + §4.2 OWS specification development, verified via Procedure §7.3.3, matching Datasheet §Conditions, Specification §FR-2 and §PR-2, Guidance §P-2.
- Coordination with related deliverables theme implemented via Procedure §2 input data collection (DEL-03.01, DEL-03.03, DEL-03.04, DEL-03.05 inputs) + §7.2 interdisciplinary check (related deliverables coordination review) + §7.3.5 traceability verification, matching Datasheet §References, Specification §IF-1, Guidance §P-4 and §C-4.
- Material and workmanship clarity theme implemented via Procedure §4 specification section development (clear material standards references, objective installation requirements, objective testing acceptance criteria) + §7.1.4 clarity check, matching Datasheet §Attributes applicable standards, Specification §QR-1 and §QR-2, Guidance §P-3.
- Terminology consistency verified with other documents: "storm drainage specification", "OWS specification", "duct bank specification", "trenchless crossing specification", "OBJ-7 Environmental Protection", "coordination with DEL-03.01/03/04/05/06", "self-check", "interdisciplinary check", "independent check", "issue register", "specification review logs" used consistently.

**Document Maturity:**
- This Procedure, along with Datasheet, Specification, and Guidance, has completed three enrichment passes (Pass 1 initial generation, Pass 2 detailed workflow steps and verification enrichment, Pass 3 final reconciliation).
- Procedure provides complete, actionable, and traceable workflow for producing DEL-03.02 Underground Utilities Technical Specification from prerequisites through input collection, specification section development, environmental protection requirements definition, verification, and issue into document control.
- All eight workflow steps are detailed with clear objectives, actions, verification checkpoints, and outputs; workflow integrity verified via requirement → implementation → verification traceability mapping.
- Verification section provides three-level review process (self-check, interdisciplinary check, independent check) with explicit ties to Specification requirements ensuring all requirements are verified before issue.
- Document is ready for WORKING_ITEMS sessions where human engineer will execute workflow, adapt steps to project-specific procedures, populate TBD values from design calculations (DEL-03.03) and Employer's Requirements, and document actual specification production process including design decisions, coordination outcomes, and QA verification results.
- Procedure provides coherent, traceable, and enforceable workflow foundation for DEL-03.02 Underground Utilities Technical Specification production with full requirement traceability and quality assurance integration.
