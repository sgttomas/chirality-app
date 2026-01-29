# Specification: DEL-03.02 Underground Utilities Technical Specification

## Scope

This specification governs the development of the **Underground Utilities Technical Specification** for **PKG-03 Underground Utilities & Drainage**. The specification defines performance, materials, and workmanship requirements for storm drainage, oil-water separator (OWS), duct banks, and trenchless crossings per the Employer's Requirements (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:199).

**Anticipated specification sections within this scope:**
- Storm drainage specification (pipe materials, installation requirements, manhole/catch basin construction, hydrostatic testing, CCTV inspection)
- Oil-Water Separator (OWS) specification (treatment performance criteria, materials of construction, instrumentation, discharge limits, performance testing)
- Duct bank specification (conduit materials, concrete encasement, pull box installation, separation requirements, continuity testing)
- Trenchless crossing specification (boring/jacking methods, casing and carrier pipe specifications, grouting requirements, installation testing)
- General requirements (scope, references, submittals, quality assurance, delivery/storage/handling, backfill and restoration)

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:199; elaborated in Datasheet §Construction for specification section organization structure)

**Exclusions:**
- Geometric layout, pipe alignments, elevations, and plan/profile details are documented in DEL-03.01 Drawing Set (not in this specification).
- Hydraulic calculations, pipe sizing analysis, OWS capacity calculations, and structural analysis are documented in DEL-03.03 Design Calculations (not in this specification).
- Equipment selection details, manufacturer data sheets, and performance curves are documented in DEL-03.04 Data Sheet Package (not in this specification).
- Installation records, test results, commissioning reports, and as-built documentation are captured in DEL-03.05 Installation and Test Records (not in this specification).
- Above-ground structures, buildings, and process equipment are outside PKG-03 scope per Scope Focus (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47).

## Requirements

### Functional Requirements

**FR-1: Comprehensive Performance and Materials Requirements**
- Provide complete performance criteria, material specifications, installation requirements, and testing protocols for storm drainage, OWS, duct banks, and trenchless crossings to enable material suppliers to prepare submittals and construction contractors to execute installations per the decomposition (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:199).
- Specification sections shall include sufficient detail for:
  - Material suppliers to identify compliant products and prepare technical submittals (material certifications, test reports, product data)
  - Construction contractors to understand installation tolerances, jointing procedures, backfill requirements, and testing protocols
  - QA/QC personnel to verify material compliance and installation workmanship before acceptance
(ASSUMPTION per typical specification function; rationale in Guidance §Purpose and §P-3 material and workmanship clarity principle).
- Verification: Procedure §Verification self-check confirms all anticipated specification sections are present and complete; interdisciplinary check verifies coordination with design drawings (DEL-03.01) and installation records (DEL-03.05).

**FR-2: Environmental Protection Performance Requirements**
- Capture oil-water separator treatment performance criteria, discharge limits, containment system requirements, and monitoring protocols to support **OBJ-7 Environmental Protection** objectives for PKG-03 (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786).
- Specification shall clearly define:
  - OWS treatment efficiency requirements (oil removal percentage, solids settling capacity, flow rate capacity)
  - Discharge limits (oil content, suspended solids, pH, other parameters per environmental permit conditions)
  - Instrumentation and monitoring requirements (level sensors, flow meters, alarm setpoints, data recording)
  - Performance testing and commissioning protocols to demonstrate compliance before facility operations commence
(rationale in Guidance §P-2 environmental protection performance principle; operational context in Datasheet §Conditions).
- Verification: Procedure §Steps environmental protection requirements definition captures performance criteria and discharge limits; Procedure §Verification independent check confirms compliance with environmental regulations and Employer's Requirements.

**FR-3: Coordination with Electrical Infrastructure**
- Define duct bank conduit materials, concrete encasement requirements, and separation criteria that enable coordination with electrical package (PKG-17) and support electrical/communications infrastructure installation (Dependencies: NOT_TRACKED per `_DEPENDENCIES.md`; coordination managed externally by humans).
- Specification shall reference PKG-17 electrical design for conduit sizes, quantities, and routing requirements while maintaining civil discipline ownership of trench construction, concrete encasement, and backfill specifications (Datasheet §Construction describes duct bank specification content supporting electrical infrastructure).
- Verification: Procedure §Verification interdisciplinary check includes review with PKG-17 Electrical to confirm conduit material specifications and encasement requirements align with electrical design assumptions.

**FR-4: Document Metadata and Document Control**
- Ensure specification metadata (document numbering, revision, author/checker/approver, issue date) aligns with the Datasheet attributes and project document control expectations (Datasheet §Attributes lists metadata fields; this requirement ensures specification implements those fields correctly).
- Specification numbering scheme shall follow project document control procedures; initial issue revision is "00" per Datasheet §Attributes (TBD: specific numbering format pending project document control register definition per Procedure §Prerequisites).
- Verification: Procedure §Steps metadata compilation; Procedure §Verification QA review confirms metadata completeness before document control system release.

### Performance Requirements

**PR-1: Hydraulic and Structural Performance**
- Conform to the hydraulic capacity, structural load, drainage performance, and seismic design expectations described in the Employer's Requirements Volume 2 Part 2: Civil & Process Mechanical Works (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, specific clauses TBD).
- Storm drainage system materials shall support:
  - Design storm event hydraulic capacity (flow rates from DEL-03.03 Design Calculations per Guidance §C-1 design calculation availability consideration)
  - Structural loading (burial depth, traffic loads, seismic loads per civil design brief)
  - Durability (chemical resistance to anticipated stormwater constituents, UV resistance if exposed, frost resistance, design life per §PR-3)
- Pipe material specifications (ring stiffness for flexible pipes, crushing strength for rigid pipes, jointing methods, bedding and backfill requirements) shall enable performance compliance (interface linkage to DEL-03.03 calculations for sizing basis; Datasheet §Construction describes storm drainage specification content).
- Verification: Design calculations (DEL-03.03) validate hydraulic and structural performance; specification material requirements support calculated performance; Procedure §Verification independent check confirms material specifications support performance requirements.

**PR-2: OWS Treatment Capacity and Containment Performance**
- Ensure specification supports the permitted throughput (1,000,000 MT/a canola oil), storage capacity (45,000 MT in three tanks), and containment expectations for Phase 1 as described in the decomposition's project overview parameters (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md, Project Overview section; Datasheet §Conditions references these parameters).
- OWS performance criteria shall accommodate:
  - Anticipated runoff volumes and spill containment requirements (sizing from DEL-03.03 Design Calculations)
  - Treatment flow rate capacity (L/s or m³/h) sufficient for design storm event plus potential spill scenarios
  - Oil removal efficiency (percentage removal of free oil and emulsified oil)
  - Solids settling capacity (removal of suspended solids to discharge limits)
  - Discharge quality limits (oil content ppm, suspended solids mg/L, pH range, other parameters per environmental permit)
- OWS materials of construction shall provide chemical resistance to canola oil, stormwater constituents, and cleaning chemicals; structural integrity for burial depth and traffic loads; and durability for design life (interface linkage to DEL-03.04 Data Sheet Package for equipment materials; Datasheet §Construction notes that equipment details are in Data Sheet Package).
- Verification: Procedure §Steps environmental protection requirements definition ensures OWS treatment performance and discharge limits are clearly specified; Procedure §Verification interdisciplinary check includes process team and environmental team review of treatment adequacy and discharge compliance.

**PR-3: Design Life and Environmental Conditions**
- Specification material requirements shall reflect design life, temperature range, seismic criteria, soil conditions, and other environmental design parameters from the civil design brief and Employer's Requirements (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD; Datasheet §Conditions lists these as TBD pending ER extraction).
- Material selections (pipe materials, coatings, concrete mix designs, geotextiles, backfill specifications) shall be compatible with:
  - Site soil conditions (soil type, bearing capacity, corrosivity, groundwater chemistry from geotechnical report)
  - Environmental conditions (temperature range, freeze-thaw cycles, UV exposure, seismic design category)
  - Design life expectations (typically 50+ years for civil infrastructure; TBD from civil design brief)
(ASSUMPTION: typical civil design considerations; specific values TBD from geotechnical report and Employer's Requirements; Guidance §C-2 addresses ER extraction importance).
- Verification: Procedure §Verification independent check confirms material selections and specifications align with civil design brief and geotechnical report; specification general requirements section references applicable design criteria documents.

### Interface Requirements

**IF-1: Coordination with Related PKG-03 Deliverables**
- Specification sections shall reference and coordinate with related PKG-03 deliverables to maintain consistency and traceability:
  - **DEL-03.01 Drawing Set**: Reference drawing sheets for pipe alignments, elevations, OWS layout, duct bank routing, crossing locations (specification provides materials/performance; drawings provide geometry).
  - **DEL-03.03 Design Calculations**: Reference calculation reports for performance basis (hydraulic capacity, structural loading, OWS sizing, trenchless crossing analysis); ensure specification material requirements support calculated performance.
  - **DEL-03.04 Data Sheet Package**: Reference equipment data sheets for OWS equipment specifications, pump specifications, instrumentation details (specification provides performance criteria; data sheets provide equipment selection).
  - **DEL-03.05 Installation and Test Records**: Specify testing and inspection requirements that will be documented in installation records (hydrostatic pressure testing, CCTV inspection, OWS performance testing, duct bank continuity testing); align installation procedures with specification installation requirements.
  - **DEL-03.06 CCTV Survey Report**: Specify CCTV inspection requirements for storm drainage pipes (inspection timing, acceptance criteria, defect reporting) that will be documented in CCTV survey report.
(Datasheet §Construction notes materials/methods coordination across deliverables; Guidance §P-4 coordination with installation records principle emphasizes this linkage.)
- Ensure specification sections include "See DEL-03.0X for [geometry/performance/equipment/testing] details" to maintain traceability across deliverables (ASSUMPTION per typical specification practice of referencing related documents; Guidance §C-4 QA coordination consideration emphasizes traceability for QA sign-offs).
- Verification: Procedure §Verification QA review confirms specification references cite correct related deliverable IDs and sections; interdisciplinary check confirms coordination with design drawings and installation records.

**IF-2: Coordination with Adjacent Packages**
- Coordinate material and installation requirements with adjacent packages to ensure interface consistency and constructability:
  - **PKG-02 Site Grading**: Coordinate trench backfill specifications, compaction requirements, and surface restoration with site grading requirements; ensure backfill materials and compaction align with pavement structural sections.
  - **PKG-04 Pavement and Surfacing**: Coordinate pavement restoration specifications (pavement section, base course, asphalt or concrete surface course) for utility trench cuts; ensure restoration meets pavement structural design and warranty requirements.
  - **PKG-17 Electrical Power Distribution**: Coordinate duct bank conduit material specifications (conduit type, size, material, separation requirements) with electrical design assumptions; ensure concrete encasement and pull box specifications support electrical cable installation and future maintenance.
  - **PKG-14 Process Piping**: Coordinate utility separation requirements and crossing details where underground utilities and process piping share trench corridors or cross paths.
- Coordination is managed through existing project coordination workflows per Scope Focus (Contractor scope only, Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47); dependencies are tracked externally (see `_DEPENDENCIES.md`).
- Verification: Procedure §Verification interdisciplinary check includes review by adjacent discipline leads (PKG-02, PKG-04, PKG-14, PKG-17); Procedure §Steps coordination data collection ensures upstream package material specifications are reviewed before finalizing specification requirements.

### Quality Requirements

**QR-1: Compliance with Quality Management Plan**
- Specification development and approval shall comply with the project Quality Management Plan and document control expectations captured in Volume 2 Part 1: Employer's Requirements – General Requirements (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, details TBD).
- Specification production workflow shall follow quality procedures: originator prepares specification sections, checker reviews for technical accuracy and completeness, approver signs for issue (ASSUMPTION per typical QA process; Procedure §Verification describes review steps).
- Submittal requirements section in specification shall define:
  - Material submittal procedures (timing, format, required data, approval process)
  - Shop drawing submittal requirements (for fabricated items like OWS, manholes, pull boxes)
  - Product data submittal requirements (manufacturer product data, test reports, certifications)
  - Submittal review and approval process (review periods, approval codes, resubmittal procedures)
- Verification: Procedure §Verification self-check, interdisciplinary check, and independent check are documented with review signatures; QA checklists are completed before issue (Procedure §Records lists QA checklists in records output).

**QR-2: Specification Review and Approval Process**
- Specification shall be internally reviewed by originator, checked by discipline checker, and approved by discipline lead per QA/QC processes before issue (ASSUMPTION per Procedure §Verification workflow).
- Review checkpoints include: technical accuracy of material specifications, completeness of performance requirements, coordination with design calculations and drawings, compliance with Employer's Requirements and standards, clarity of installation and testing requirements (Procedure §Verification lists review activities).
- Specification status codes (e.g., "For Review", "For Construction", "For Record") shall be clearly marked on cover page or document metadata per project document control procedures (TBD: specific status code definitions pending project conventions; Datasheet §Attributes lists revision as "00" for initial issue).
- Verification: Procedure §Steps deliver specification into document control system; Procedure §Verification QA review confirms all review signatures and approval stamps are present before release.

**QR-3: Testing and Inspection Requirements**
- Specification shall define clear testing and inspection requirements with acceptance criteria for each underground utility system to support QA/QC verification and commissioning (Datasheet §Construction describes testing requirements as specification content; Guidance §P-4 coordination with installation records emphasizes testing protocol clarity).
- Storm drainage testing and inspection requirements:
  - Hydrostatic pressure testing (test pressure, test duration, allowable leakage rates, test procedures per ASTM or other standards)
  - CCTV inspection of pipe interiors (inspection timing, equipment requirements, defect classification, acceptance criteria, reporting format per DEL-03.06)
  - Manhole and catch basin installation inspection (dimensional tolerances, joint sealing, frame and cover installation, invert channel construction)
- OWS performance testing requirements:
  - Pre-commissioning inspection (verification of construction per drawings and specifications, instrumentation calibration, control system functional testing)
  - Performance testing (flow rate verification, oil removal efficiency testing, discharge quality sampling and analysis)
  - Acceptance criteria (performance test results shall meet or exceed specified treatment efficiency and discharge limits)
- Duct bank testing requirements:
  - Conduit continuity testing (mandrel test or other method to verify conduit is clear and continuous from pull box to pull box)
  - Concrete encasement inspection (concrete mix design verification, curing procedures, dimensional tolerances)
- Trenchless crossing testing requirements:
  - Casing pipe inspection (weld inspection per AWS or other welding standards, coating inspection, cathodic protection testing if applicable)
  - Carrier pipe installation verification (alignment, support spacing, annular space grouting verification)
  - Hydrostatic testing of carrier pipe inside casing (if applicable for pressure piping)
- Verification: Procedure §Steps testing requirements development ensures all systems have clear testing and inspection protocols; Procedure §Verification independent check confirms testing requirements align with industry standards and Employer's Requirements; testing results documented in DEL-03.05 Installation and Test Records.

## Standards

**Governing Standards:**
- **Employer's Requirements Volume 2 Part 2: Civil & Process Mechanical Works** is the authoritative source for applicable civil standards, pipe material specifications, installation methods, environmental protection criteria, and product selections; specific clauses will be extracted and referenced in specification general requirements as design details mature (Source: test/Volume_2_Part_2_Employers_Requirements.pdf).
- **Employer's Requirements Volume 2 Part 1: General Requirements** governs project Quality Management Plan, submittal procedures, document control procedures, and QA/QC requirements (Source: test/Volume_2_Part_1_Employers_Requirements.pdf).

**Supplementary Standards (TBD pending ER extraction and design development):**
- **Pipe materials and installation:**
  - CSA B182.1 – Plastic Drain, Storm, and Sewer Pipe and Fittings
  - CSA A257 – Circular Concrete Culvert, Storm Drain, Sewer Pipe and Fittings
  - CSA B137 – Polyethylene Piping Systems (for HDPE pipes)
  - ASTM D2321 – Standard Practice for Underground Installation of Thermoplastic Pipe for Sewers and Other Gravity-Flow Applications
  - ASTM D3034 – Type PSM Poly(Vinyl Chloride) (PVC) Sewer Pipe and Fittings
- **Manholes and catch basins:**
  - CSA A257 – Circular Precast Reinforced Concrete Manhole Sections, Catch Basins and Fittings
  - ASTM C478 – Standard Specification for Precast Reinforced Concrete Manhole Sections
- **Concrete and backfill:**
  - CSA A23.1 – Concrete Materials and Methods of Concrete Construction
  - CSA A23.2 – Methods of Test and Standard Practices for Concrete
  - ASTM D2487 – Standard Practice for Classification of Soils for Engineering Purposes (for backfill material classification)
- **Testing and inspection:**
  - ASTM F1417 – Standard Test Method for Installation Acceptance of Plastic Gravity Sewer Lines Using Low-Pressure Air
  - ASTM C969 – Standard Practice for Infiltration and Exfiltration Acceptance Testing of Installed Precast Concrete Pipe Sewer Lines
  - NASSCO PACP (Pipeline Assessment Certification Program) – CCTV inspection standards (for DEL-03.06 CCTV Survey Report)
- **OWS and environmental:**
  - API (American Petroleum Institute) standards for oil-water separators (if applicable)
  - Local environmental discharge regulations (Metro Vancouver, BC Ministry of Environment)
  - Manufacturer's standards for OWS equipment (referenced in DEL-03.04 Data Sheet Package)
- **Electrical duct banks:**
  - CSA C22.10 – Safety Standard for Electrical Conduit Systems (for PVC conduit)
  - NEMA TC 2 – Electrical Polyvinyl Chloride (PVC) Conduit
  - CSA A23.1 – Concrete Materials and Methods (for concrete encasement)
- **Trenchless construction:**
  - ASTM F1962 – Standard Guide for Use of Maxi-Horizontal Directional Drilling for Placement of Polyethylene Pipe or Conduit Under Obstacles
  - ASTM F1541 – Standard Test Method for Establishing Performance of Materials for Guided Boring
  - Industry standards for auger boring, microtunneling (NASTT, ISTT publications)

**Applicable Codes and Regulations (ASSUMPTION pending ER extraction):**
- National Building Code of Canada (NBC) – civil works provisions
- British Columbia Building Code (BCBC) – local amendments
- Canadian Standards Association (CSA) standards for pipe materials and installations (listed above)
- Local municipal standards:
  - City of Surrey – Storm Drainage Design Criteria, Road Crossing Standards
  - Metro Vancouver – Stormwater Source Control Design Guidelines
  - Fraser Surrey Docks – Facility-specific requirements (if applicable)
- Environmental regulations:
  - Fisheries Act (Canada) – protection of fish habitat
  - Environmental Management Act (BC) – stormwater discharge permits
  - Metro Vancouver Sewer Use Bylaw – discharge limits (for OWS discharge if tied to sanitary sewer)
  - Stormwater discharge permit conditions (specific to facility; supports OBJ-7 Environmental Protection per FR-2)

(Note: Specific code editions, standard versions, and applicable clauses to be extracted from Employer's Requirements Volume 2 Part 2 during design development; see Procedure §Prerequisites for reference material review requirement and Guidance §C-2 for ER extraction importance.)

## Verification

**Specification Review Process:**
- **Self-check (originator review)**: Ensures specification sections are complete (all anticipated sections present), material specifications are technically accurate and support performance requirements (PR-1, PR-2, PR-3), installation requirements are clear and constructible, testing and inspection requirements are defined with acceptance criteria (QR-3), references to related deliverables are correct (IF-1), and metadata is complete (FR-4). (Source: Procedure §Verification self-check step; Datasheet §Cross-Document Linkages references Procedure verification process.)

- **Interdisciplinary check**: Verifies coordination with design drawings (DEL-03.01) to ensure material specifications support drawn configurations, with design calculations (DEL-03.03) to ensure material specifications support calculated performance, with equipment data sheets (DEL-03.04) to ensure OWS performance criteria align with equipment selections, with installation records (DEL-03.05) to ensure testing and inspection requirements are clear and complete, and with adjacent disciplines (PKG-02 backfill, PKG-04 pavement restoration, PKG-17 duct bank coordination, PKG-14 utility separations) per IF-2 requirements. (Source: Procedure §Verification interdisciplinary check step; ASSUMPTION per typical engineer-review process and Quality Management Plan per test/Volume_2_Part_1_Employers_Requirements.pdf.)

- **Independent check**: Confirms compliance with Employer's Requirements (Volume 2 Part 2) and applicable standards (Standards section); validates material specifications support performance requirements (PR-1, PR-2, PR-3) and design calculation results (DEL-03.03); ensures environmental protection requirements (FR-2, PR-2) support OBJ-7 objectives and regulatory compliance; confirms testing and inspection requirements (QR-3) align with industry standards and Quality Management Plan; verifies submittal requirements (QR-1) are complete and align with project procedures; records results in review signature block on specification cover page. (Source: Procedure §Verification independent check step; reviews tie to Specification requirements to close verification loop.)

**Technical Accuracy Verification:**
- Material specifications reviewed against manufacturer product data, industry standards (CSA, ASTM), and Employer's Requirements to confirm technical accuracy and product availability (ASSUMPTION: typical specification verification check).
- Performance criteria (hydraulic capacity, OWS treatment efficiency, structural loading) verified against design calculation results (DEL-03.03) to ensure specification requirements align with design performance (interface linkage per IF-1).
- Installation requirements reviewed for constructability and alignment with construction industry best practices (ASSUMPTION: typical specification verification check to avoid specifying impractical or uncommon installation methods).
- Results recorded in specification review records and QA checklists per QR-1 (Procedure §Records lists specification review logs and QA checklists).

**Traceability Verification:**
- Specification sections reference Drawing Set (DEL-03.01), Design Calculations (DEL-03.03), Data Sheet Package (DEL-03.04), and Installation and Test Records (DEL-03.05) for geometry, performance basis, equipment details, and testing documentation per IF-1 linkage requirement.
- Specification general requirements section references applicable Employer's Requirements clauses, standards, and codes to maintain traceability to governing documents (ASSUMPTION per typical specification practice).
- Procedure §Verification QA review confirms specification references cite correct deliverable IDs, calculation sheet numbers, drawing sheet numbers, and standard versions per IF-1.

## Documentation

**Documented Specification Sections:**
- General requirements: Scope, references, definitions, submittals, quality assurance, delivery/storage/handling
- Storm drainage system: Materials (pipe, manholes, catch basins, fittings), installation requirements (bedding, backfill, jointing), testing and inspection (hydrostatic testing, CCTV inspection per DEL-03.06)
- Oil-water separator system: Performance criteria (treatment efficiency, flow capacity, discharge limits), materials of construction (separator internals, coatings, access hatches), instrumentation (level sensors, flow meters, alarms), installation requirements, performance testing and commissioning
- Duct bank system: Conduit materials (PVC, HDPE conduit specifications), concrete encasement (mix design, placement, curing), pull boxes (materials, installation), installation requirements (trench dimensions, separation from other utilities, backfill), testing (conduit continuity testing)
- Trenchless crossing system: Boring methods (auger boring, microtunneling, HDD performance requirements), casing pipe (material, welding, coating, cathodic protection if applicable), carrier pipe (installation inside casing, support spacing, annular space grouting), testing and inspection
- Backfill and restoration: Trench backfill materials (granular materials, native soil reuse criteria), compaction requirements (lift thickness, compaction density, testing frequency), pavement restoration (pavement section matching existing or PKG-04 requirements, surface course)
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:199; detailed in Datasheet §Construction)

**Format, Numbering, and Revision Control:**
- Format: Text document organized in specification sections (Datasheet §Attributes notes typical CSI MasterFormat structure or project-specific organization, TBD).
- Numbering: Document number to be issued per project numbering system (FR-4 requirement; Datasheet §Attributes notes numbering system TBD).
- Revision control: Initial issue revision "00" per Datasheet §Attributes; subsequent revisions follow project document control procedures (QR-2 requirement).
- Metadata: Cover page or header includes document number, title, revision, issue date, originator, checker, approver, project name, deliverable ID (FR-4 metadata requirement; Procedure §Steps includes metadata compilation).
- Details (e.g., numbering scheme format, revision code definitions, cover page template) remain TBD until the project document control register is defined (Source: test/Volume_2_Part_1_Employers_Requirements.pdf per QR-1; Procedure §Prerequisites lists document control procedures as required reference material).

**Associated Quality Records:**
- Specification review logs documenting self-check, interdisciplinary check, and independent check results (Verification section review process; Procedure §Records lists specification review logs).
- QA checklists confirming technical accuracy, completeness, coordination with related deliverables, standards compliance (QR-1 and QR-2 requirements; Procedure §Records lists QA checklists).
- Issue registers tracking specification issue status, distribution, and revisions (QR-2 requirement; Procedure §Records lists issue registers).
- Discipline review records from adjacent packages (IF-2 coordination; Procedure §Records lists discipline review records).
- Material submittal review logs (future use during construction; specification submittal requirements section defines submittal procedures per QR-1).
(All records retained per project document control procedures per test/Volume_2_Part_1_Employers_Requirements.pdf.)

## Cross-Document Notes

**Specification → Datasheet:**
- Scope anticipated sections → Datasheet §Construction describes each section in detail with specification content expectations
- FR-4 document metadata requirements → Datasheet §Attributes lists metadata fields to be implemented in specification
- IF-1 coordination with related deliverables → Datasheet §References lists related PKG-03 deliverables
- Standards section governing codes → Datasheet §Conditions references Employer's Requirements and standards for performance criteria

**Specification → Guidance:**
- FR-2 environmental protection performance → Guidance §P-2 environmental protection performance principle elaborates OBJ-7 rationale and treatment performance criteria clarity
- PR-1 hydraulic and structural performance → Guidance §P-1 hydraulic performance and durability principle explains performance criteria importance
- IF-1 coordination with related deliverables → Guidance §P-4 coordination with installation records principle emphasizes linkage to DEL-03.05
- QR-3 testing and inspection requirements → Guidance §P-4 emphasizes testing protocol clarity for QA verification

**Specification → Procedure:**
- Verification section specification review process → Procedure §Verification describes self-check, interdisciplinary check, independent check steps in detail
- FR-1 comprehensive performance and materials requirement → Procedure §Steps specification section development workflow produces specification to meet this requirement
- QR-1 quality management compliance → Procedure §Verification implements QA/QC review per Quality Management Plan
- Documentation associated quality records → Procedure §Records lists all QA documentation outputs

**Requirement Traceability:**
- Each functional requirement (FR-1 to FR-4) has corresponding Procedure verification step
- Each performance requirement (PR-1 to PR-3) references design inputs (calculations, civil design brief, geotechnical report) and has independent check verification
- Each interface requirement (IF-1 to IF-2) has interdisciplinary check or coordination verification
- Each quality requirement (QR-1 to QR-3) has QA review checkpoint in Procedure §Verification

## Pass 2 Enrichments

This Pass 2 revision adds:
1. Expanded Scope section with explicit exclusions clarifying what is NOT in this specification (geometry in DEL-03.01, calculations in DEL-03.03, equipment details in DEL-03.04, installation records in DEL-03.05).
2. Detailed functional requirements (FR-1 to FR-4) with explicit verification cross-references to Procedure sections.
3. Detailed performance requirements (PR-1 to PR-3) with interface linkages to design calculations (DEL-03.03), equipment data sheets (DEL-03.04), and civil design brief.
4. Detailed interface requirements (IF-1 to IF-2) listing specific related PKG-03 deliverables and adjacent packages with coordination expectations.
5. Enhanced quality requirements (QR-1 to QR-3) covering QA process, specification review workflow, submittal requirements, and testing/inspection requirements.
6. Expanded Standards section with governing standards, supplementary standards (pipe materials, concrete, testing, OWS, duct banks, trenchless), and assumed applicable codes and regulations.
7. Detailed Verification section breaking down self-check, interdisciplinary check, and independent check activities with explicit ties to requirements.
8. Enhanced Documentation section describing specification section organization structure and associated quality records.
9. Requirement traceability summary showing each requirement has corresponding verification in Procedure.

## Pass 3 Final Notes

**Pass 3 Reconciliation Completed:**
- All requirements (FR-1 to FR-4, PR-1 to PR-3, IF-1 to IF-2, QR-1 to QR-3) have corresponding verification in Procedure §Verification and implementation steps in Procedure §Steps.
- All requirements have rationale or context in Guidance (FR-2 → Guidance §P-2 environmental protection performance, FR-3 → Guidance §P-4 coordination with installation records, QR-3 → Guidance §P-4 testing protocol clarity, etc.).
- All requirements reference Datasheet attributes or content (FR-4 → Datasheet §Attributes metadata, FR-1 → Datasheet §Construction comprehensive specification content, etc.).
- Requirement traceability summary (end of §Cross-Document Notes) confirms every requirement has verification checkpoint in Procedure.
- Entity coverage verified: All anticipated specification sections in §Scope (storm drainage, OWS, duct banks, trenchless crossings, general requirements) appear in Datasheet §Construction, Guidance §Examples, and Procedure §Records.
- TBD items consistent with Datasheet: Document numbering system TBD (§FR-4, §Documentation), specification format TBD (§Documentation), applicable standards TBD (§Standards), performance criteria values TBD from ER and DEL-03.03 (§PR-1, §PR-2, §PR-3).
- Terminology consistency verified: "storm drainage specification", "OWS specification", "duct bank specification", "trenchless crossing specification", "OBJ-7 Environmental Protection", "interdisciplinary check", "independent check" used consistently with Datasheet, Guidance, and Procedure.

**Cross-Document Consistency Verification:**
- §Scope anticipated sections list matches Datasheet §Attributes "Specification Sections" and Datasheet §Construction organization exactly.
- §FR-2 environmental protection performance requirement implements OBJ-7 emphasis from Datasheet §Conditions, elaborated by Guidance §P-2, implemented via Procedure §5.
- §IF-1 coordination with related PKG-03 deliverables (DEL-03.01, DEL-03.03, DEL-03.04, DEL-03.05, DEL-03.06) matches Datasheet §References, Guidance §P-4 and §C-4, Procedure §2.1 and §2.2.
- §IF-2 coordination with adjacent packages (PKG-02, PKG-04, PKG-14, PKG-17) matches Datasheet §Construction coordination notes, Guidance considerations, Procedure §7.2 interdisciplinary check.
- §Verification specification review process (self-check, interdisciplinary check, independent check) matches Procedure §7.1, §7.2, §7.3 exactly with detailed implementation steps.
- §Documentation specification section organization matches Datasheet §Construction specification organization structure and Procedure §3.2 section structure establishment.

**Document Maturity:**
- This Specification, along with Datasheet, Guidance, and Procedure, has completed three enrichment passes (Pass 1 initial generation, Pass 2 detailed requirements and verification enrichment, Pass 3 final reconciliation).
- All requirements are traceable to verification steps, implementation procedures, and design rationale.
- Document is ready for WORKING_ITEMS sessions where human engineer will validate requirements, populate TBD items from Employer's Requirements and design calculations (DEL-03.03), and refine performance criteria as design development proceeds.
- Specification provides complete, traceable, and enforceable requirements foundation for DEL-03.02 Underground Utilities Technical Specification production.
