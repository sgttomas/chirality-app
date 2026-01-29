# Datasheet: DEL-03.04 Underground Utilities Data Sheet Package

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-03.04 |
| Name | Underground Utilities Data Sheet Package |
| Package | PKG-03 Underground Utilities & Drainage |
| Discipline | Civil |
| Type | Data Sheet |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Document Number | To be issued per project numbering system (TBD – see Specification §FR-4 and §Documentation for metadata control requirements; Procedure §6 describes numbering assignment process) |
| Data Sheet Types | OWS equipment data sheet, pipe material data sheets (HDPE, concrete, PVC, steel casing), instrumentation data sheets, pump data sheets (if applicable) (see Specification §Scope for anticipated data sheet types; Procedure §3.2 describes data sheet package structure establishment) |
| Revision | 00 (initial issue for design development; see Procedure §6.2 for revision code setting) |
| Format | Tabulated data sheets with equipment specifications, material properties, performance parameters, testing requirements (typical format per project data sheet standards; Specification §Documentation describes format TBD) |
| Classification | Civil – Underground Utilities Equipment & Materials |
| Data Sheet Sections | OWS equipment data, pipe material specifications, instrumentation specifications, testing and inspection requirements (aligned with Specification §Scope anticipated artifacts; Procedure §3.2 establishes section structure) |
| Data Sources | Equipment manufacturer data sheets, material supplier specifications, DEL-03.03 Design Calculations results, DEL-03.02 Technical Specification requirements (see Specification §Standards for governing standards list; Procedure §2 input data collection) |

## Conditions

**Context & environmental expectations:**
- Defines equipment specifications and material properties for underground utilities described in PKG-03, covering oil-water separator (OWS) equipment data, pipe material specifications, instrumentation data, and testing requirements to substantiate design drawings (DEL-03.01) and technical specifications (DEL-03.02) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:211; Specification §Scope provides detailed data sheet coverage).
- Designed to support storm drainage collection and conveyance, spill containment via OWS, and conduit routing within Fraser Surrey Terminal facility boundaries per Scope Focus (Contractor scope only, Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47; Specification §Scope exclusions clarifies what is NOT in data sheet package).
- Deliverable supports **OBJ-7 Environmental Protection**; data sheets must capture OWS equipment specifications, treatment performance parameters, and discharge monitoring instrumentation to demonstrate compliance with environmental protection requirements (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; elaborated in Guidance §P-2 environmental protection equipment substantiation principle; implemented via Procedure §4.2 OWS equipment data sheet development; verified via Specification §FR-2 requirement and Procedure §7.3.3 independent check).
- Equipment performance specifications (OWS treatment capacity, retention volume, instrumentation ranges) and material properties (pipe strength, corrosion resistance, chemical compatibility) are sourced from manufacturer data sheets, validated against design calculations (DEL-03.03), and verified for compliance with Employer's Requirements (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD; see Specification §PR-3 design life and environmental conditions requirement; Procedure §Prerequisites lists manufacturer data and DEL-03.03 as required references; Guidance §C-2 addresses ER compliance verification consideration).
- Coordinate data sheet metadata, revision process, and content organization with the Specification §FR-4 and §Documentation requirements to ensure data sheet control aligns with project document management procedures (cross-reference: Specification §FR-4 document metadata requirement implemented via Procedure §6 metadata compilation and §8 issue into document control).

**Operational context:**
- Data sheet package is used by procurement teams for equipment and material ordering, by suppliers for submittal preparation, by construction contractors for installation verification, by QA/QC for conformance inspection (see Procedure §Verification and §7 for review workflow), and by operations for maintenance planning and spare parts identification (ASSUMPTION per typical data sheet lifecycle; Guidance §C-5 procurement use and operations reference consideration explains balancing specification detail with procurement flexibility).
- Environmental protection equipment data (OWS specifications, instrumentation, discharge monitoring) is critical for permitting and regulatory compliance; data sheet clarity and accuracy directly affect equipment procurement, installation acceptance, and environmental inspection outcomes (rationale in Guidance §P-2 environmental protection equipment substantiation principle; Procedure §4.2 OWS equipment data sheet development implements clear specification).

## Construction

**Data sheet types & content focus:**
- Primary data sheets documented in the package include:
  - **OWS equipment data sheet**: Equipment type and model, treatment capacity (design flow rate, peak flow capacity), separator volume (oil storage, solids settling, water retention), retention time, treatment performance (oil removal efficiency, discharge water quality targets), materials of construction (internals, coatings, access hatches), dimensions and weights, instrumentation requirements (level sensors, flow meters, oil layer thickness monitors, alarms), electrical requirements, maintenance access provisions (Specification §Scope lists "OWS equipment data sheet"; Procedure §4.2 describes OWS data sheet development; Guidance §P-2 emphasizes environmental protection equipment substantiation for OBJ-7 compliance; Guidance §Example 1 provides OWS data sheet content guidance).
  - **Pipe material data sheets**: Pipe material type (HDPE, concrete, PVC, steel casing for trenchless crossings), pipe sizes and wall thicknesses, pipe class or stiffness ratings, material standards (ASTM, CSA, AWWA designations), pressure ratings, jointing methods (fusion, gasketed, welded), chemical resistance properties, corrosion protection (coatings, cathodic protection for steel), installation requirements (bedding, backfill, trench width), testing requirements (hydrostatic pressure testing, joint integrity testing) (cross-reference: DEL-03.01 Drawing Set for pipe layout geometry per Specification §IF-1; DEL-03.02 Technical Specification for pipe performance criteria per Specification §PR-1; DEL-03.03 Design Calculations for pipe sizing validation; Procedure §4.3 describes pipe material data sheet development; Guidance §T-3 pipe material data sheet detail trade-off recommends material property tables + reference to DEL-03.02 for installation requirements; Guidance §Example 2 provides pipe material data sheet structure guidance).
  - **Instrumentation data sheets** (if instrumentation is part of PKG-03 scope): Instrument type (level sensors, flow meters, oil layer thickness monitors for OWS), measurement range, accuracy, output signal, power requirements, materials of construction, environmental ratings (temperature, humidity, hazardous area classification if applicable), calibration requirements, testing requirements (Specification §Scope lists "instrumentation data sheets"; Procedure §4.4 describes instrumentation data sheet development if applicable; Guidance §T-4 instrumentation data sheet scope trade-off discusses coordination with PKG-18 I&C for detailed instrumentation specifications).
  - **Pump data sheets** (if pumps are part of PKG-03 scope, e.g., sump pumps in OWS): Pump type and model, capacity (design flow rate, total dynamic head), motor power and electrical requirements, materials of construction, curve data (flow vs head, efficiency, NPSH), dimensions and weights, installation requirements, testing requirements (Specification §Scope lists "pump data sheets" if applicable; Procedure §4.5 describes pump data sheet development if applicable; coordination with PKG-15 Pumps and Rotating Equipment may be required per Guidance §C-3 scope boundaries consideration).
- Data sheet content is sourced from equipment manufacturer data sheets, material supplier specifications, design calculation results (DEL-03.03), and technical specification requirements (DEL-03.02); data sheets consolidate information to support procurement and installation (ASSUMPTION per typical data sheet package purpose; see Specification §Scope data substantiation purpose and §IF-2 linkage to related deliverables; Procedure §2 describes collecting data from multiple sources).
- Testing and inspection requirements (hydrostatic pressure testing for pipes, OWS performance testing, instrumentation calibration, material conformance testing) are documented in data sheet sections to support quality assurance and commissioning (DEL-03.05 Installation and Test Records will reference data sheet testing requirements; see Specification §QR-3 testing and inspection requirements; Procedure §4.6 describes testing requirements documentation).

**Data sheet package organization (ASSUMPTION per typical data sheet package structure; Guidance §C-3 emphasizes data sheet structure to maintain traceability):**
- Cover page: Data sheet package title, project identification, revision history, table of contents
- Introduction: Scope, data sources, applicable standards, abbreviations and definitions
- OWS equipment data sheet: Equipment specifications, performance parameters, instrumentation, testing requirements
- Pipe material data sheets: Organized by pipe material type (HDPE, concrete, PVC, steel casing), material properties, jointing methods, testing requirements
- Instrumentation data sheets: Instrument specifications by type (level, flow, oil layer thickness), testing and calibration requirements
- Pump data sheets: Pump specifications, performance curves, testing requirements (if applicable)
- Testing and inspection requirements summary: Consolidated testing requirements cross-referencing individual data sheets
- Appendices: Manufacturer catalog data, material certificates, test reports, calculation references
(Procedure §3.2 establishes data sheet package structure; Procedure §2.4 describes documenting data sources and standards in introduction)

## References

- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:211 — scope, description, and anticipated artifacts for DEL-03.04.
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786 — OBJ-7 Environmental Protection mapping includes DEL-03.04 (OWS equipment data supports environmental controls).
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47 — Scope Focus confirms contractor-only work scope, affects interface assumptions.
- test/Volume_2_Part_2_Employers_Requirements.pdf — Civil & Process Mechanical Works requirements for equipment and material specifications, performance standards, testing requirements (details TBD, location references to be populated during design development; Specification §Standards lists this as governing standard; Procedure §Prerequisites lists as required reference material; Guidance §C-2 Employer's Requirements compliance verification consideration addresses ER compliance importance).
- test/Volume_2_Part_1_Employers_Requirements.pdf — General Requirements including Quality Management Plan, document control procedures, QA/QC requirements, submittal procedures (Specification §QR-1 references for quality management compliance; Procedure §Prerequisites lists as required reference material).
- Specification.md — §Scope defines anticipated data sheet types; §FR-1 to §FR-4 functional requirements; §PR-1 to §PR-3 performance requirements; §IF-1 to §IF-2 interface requirements; §QR-1 to §QR-3 quality requirements; §Standards governing and supplementary standards; §Verification data sheet review process; §Documentation data sheet package organization and associated quality records.
- Guidance.md — §Purpose clarifies intent behind data sheet package production; §P-1 to §P-4 principles (equipment and material substantiation, environmental protection equipment substantiation for OBJ-7, data source traceability and accuracy, coordination with procurement and installation); §C-1 to §C-5 considerations (manufacturer data availability, ER compliance verification, data sheet structure and scope boundaries, QA sign-offs, procurement use and operations reference); §T-1 to §T-4 trade-offs (data sheet detail vs procurement flexibility, OWS equipment specification approach, pipe material data sheet content, instrumentation data sheet scope); §Examples 1-4 (OWS equipment data sheet structure, pipe material data sheet organization, instrumentation data sheet content, testing requirements documentation).
- Procedure.md — §Purpose data sheet package production and QA purposes; §Prerequisites dependencies, reference materials, manufacturer data inputs, personnel requirements; §Steps 1-8 (scope review, input data collection, data sheet package structure establishment, OWS/pipe/instrumentation/pump data sheet development, testing requirements documentation, metadata compilation, verification workflow, issue into document control); §Verification self-check, interdisciplinary check, independent check; §Records data sheet deliverables and quality records.
- Package-level references in `execution/PKG-03_Underground_Utilities_and_Drainage/0_References/_REFERENCE_INDEX.md` (to be populated with equipment manufacturer catalogs, material supplier specifications, applicable material standards).
- DEL-03.01 Drawing Set — Layout geometry and equipment locations (OWS location, pipe routes, instrumentation locations) provide context for data sheets (referenced per Specification §IF-1; Procedure §2.1 collects as design input for data sheet context).
- DEL-03.02 Technical Specification — Material specifications, pipe performance requirements, OWS treatment criteria provide performance targets and constraints for data sheets (referenced for performance criteria per Specification §PR-1 and §PR-2; Procedure §2.2 collects as design input; Procedure §7.3.2 validates data sheet content against specification requirements).
- DEL-03.03 Design Calculations — Hydraulic calculations, pipe sizing, OWS capacity calculations provide sizing basis and performance validation for equipment and material selection (referenced for sizing validation per Specification §PR-1 and §PR-2; Procedure §2.2 collects calculation results as data sheet input).
- DEL-03.05 Installation and Test Records — Installation procedures and testing protocols reference data sheet specifications for acceptance criteria (referenced for installation guidance coordination per Specification §IF-2; Guidance §C-4 QA coordination with installation records).
- DEL-03.06 CCTV Survey Report — Post-installation inspection may reference pipe material data sheets for defect assessment criteria.

## Cross-Document Linkages

**Datasheet ↔ Specification:**
- Datasheet §Attributes "Document Number" TBD → Specification §FR-4 document metadata requirement → Specification §Documentation numbering format TBD
- Datasheet §Attributes "Data Sheet Types" → Specification §Scope anticipated data sheet types list (OWS equipment, pipe materials, instrumentation, pumps match exactly)
- Datasheet §Attributes "Data Sources" → Specification §Standards governing standards list + Specification §IF-1 linkage to related deliverables
- Datasheet §Construction OWS equipment data sheet content → Specification §FR-2 environmental protection equipment substantiation requirement → Specification §PR-2 treatment capacity and containment performance
- Datasheet §Construction pipe material data sheets content → Specification §FR-1 comprehensive material substantiation requirement → Specification §PR-1 hydraulic and structural performance
- Datasheet §Construction instrumentation data sheets content → Specification §FR-3 instrumentation substantiation requirement (if in scope) → Specification §IF-1 coordination with PKG-18 I&C
- Datasheet §Construction testing requirements → Specification §QR-3 testing and inspection requirements
- Datasheet §Construction data sheet package organization → Specification §Documentation data sheet package organization

**Datasheet ↔ Guidance:**
- Datasheet §Conditions OBJ-7 environmental protection emphasis → Guidance §P-2 environmental protection equipment substantiation principle (explains why OBJ-7 is critical for OWS equipment data and discharge monitoring instrumentation)
- Datasheet §Construction OWS equipment data sheet description → Guidance §P-2 environmental protection equipment substantiation application guidance (treatment capacity, retention volume, instrumentation, discharge monitoring) → Guidance §Example 1 OWS equipment data sheet structure
- Datasheet §Construction data sheet package organization structure → Guidance §C-3 data sheet structure and scope boundaries consideration (maintain traceability to decomposition, avoid scope creep into adjacent packages)
- Datasheet §Conditions operational context (procurement, suppliers, construction, QA/QC, operations) → Guidance §C-5 procurement use and operations reference consideration (balance specification detail with procurement flexibility and operations maintenance use)
- Datasheet §Attributes "Data Sources" → Guidance §P-3 data source traceability and accuracy principle (explains why data source documentation is essential for procurement verification and future equipment replacement)
- Datasheet §Construction pipe material data sheets content → Guidance §P-1 equipment and material substantiation principle → Guidance §T-3 pipe material data sheet detail trade-off → Guidance §Example 2 pipe material data sheet organization
- Datasheet §Construction instrumentation data sheets content → Guidance §T-4 instrumentation data sheet scope trade-off → Guidance §Example 3 instrumentation data sheet content
- Datasheet §Construction testing requirements → Guidance §Example 4 testing requirements documentation

**Datasheet ↔ Procedure:**
- Datasheet §Attributes "Revision" 00 initial issue → Procedure §6.2 set initial revision code (describes revision code setting process)
- Datasheet §Attributes "Data Sheet Types" → Procedure §3.2 establish data sheet package structure (describes how package structure is established matching anticipated data sheet types)
- Datasheet §Construction OWS equipment data sheet content → Procedure §4.2 develop OWS equipment data sheet (describes equipment specifications, performance parameters, instrumentation, testing requirements development)
- Datasheet §Construction pipe material data sheets content → Procedure §4.3 develop pipe material data sheets (describes material properties, jointing methods, testing requirements development by pipe material type)
- Datasheet §Construction instrumentation data sheets content → Procedure §4.4 develop instrumentation data sheets (describes instrument specifications, calibration requirements development if in scope)
- Datasheet §Construction pump data sheets content → Procedure §4.5 develop pump data sheets (describes pump specifications, performance curves development if applicable)
- Datasheet §Construction testing requirements → Procedure §4.6 document testing and inspection requirements (describes testing requirements documentation and cross-referencing)
- Datasheet §Construction data sheet package organization structure → Procedure §3.2 data sheet package structure establishment matches Datasheet organization (cover page, introduction, OWS, pipes, instrumentation, pumps, testing summary, appendices)
- Datasheet §Conditions data sheet control alignment → Procedure §6 metadata compilation + §8 issue into document control system (describes how data sheet metadata is populated and package is issued per document control procedures)
- Datasheet §References lists quality records → Procedure §Records quality records section (self-check checklist, interdisciplinary review log, independent check review, QA checklists, issue register entry, data sheet review logs)

**Entity Coverage Check (all four documents):**
- OWS equipment data sheet: Datasheet §Construction ✓, Specification §Scope + §FR-2 + §PR-2 ✓, Guidance §P-2 + §Example 1 ✓, Procedure §4.2 + §Records ✓
- Pipe material data sheets: Datasheet §Construction ✓, Specification §Scope + §FR-1 + §PR-1 ✓, Guidance §P-1 + §T-3 + §Example 2 ✓, Procedure §4.3 + §Records ✓
- Instrumentation data sheets: Datasheet §Construction ✓, Specification §Scope + §FR-3 (if in scope) ✓, Guidance §T-4 + §Example 3 ✓, Procedure §4.4 + §Records ✓
- Pump data sheets: Datasheet §Construction ✓, Specification §Scope (if applicable) ✓, Guidance §C-3 (scope boundaries) ✓, Procedure §4.5 + §Records ✓
- Environmental protection (OBJ-7): Datasheet §Conditions ✓, Specification §FR-2 + §PR-2 ✓, Guidance §P-2 ✓, Procedure §4.2 + §7.3.3 ✓
- Testing and inspection requirements: Datasheet §Construction ✓, Specification §QR-3 ✓, Guidance §Example 4 ✓, Procedure §4.6 + §7.3.4 ✓
- Document metadata/numbering: Datasheet §Attributes ✓, Specification §FR-4 + §Documentation ✓, Guidance §P-3 (data source traceability) ✓, Procedure §6 + §7.1.5 ✓
- Coordination with related deliverables (DEL-03.01, DEL-03.02, DEL-03.03, DEL-03.05): Datasheet §References ✓, Specification §IF-1 + §IF-2 ✓, Guidance §P-4 + §C-4 ✓, Procedure §2.1 + §2.2 + §7.2 ✓
- Data source traceability: Datasheet §Attributes ✓, Specification §Standards + §IF-1 ✓, Guidance §P-3 ✓, Procedure §2 + §7.1.2 ✓

**TBD Items Cross-Check:**
- Document numbering system: Datasheet §Attributes TBD → Specification §FR-4 TBD → Specification §Documentation TBD pending document control register → Procedure §6.1 obtain numbers from document control register
- Data sheet format: Datasheet §Attributes TBD (typical format noted) → Specification §Documentation TBD per project data sheet standards → Procedure §Prerequisites lists project data sheet standards as required reference
- Equipment performance specifications (OWS treatment capacity, retention volume, instrumentation ranges): Datasheet §Conditions TBD from manufacturer data and DEL-03.03 → Specification §PR-2 TBD from calculations and ER requirements → Procedure §Prerequisites lists DEL-03.03 and manufacturer data as required references → Guidance §C-1 manufacturer data availability consideration
- Material properties (pipe strength, corrosion resistance, chemical compatibility): Datasheet §Conditions TBD from material supplier specifications and ER Volume 2 Part 2 → Specification §PR-1 TBD from ER and material standards → Procedure §Prerequisites lists ER Volume 2 Part 2 and material supplier specifications as required references → Guidance §C-2 ER compliance verification consideration

(All TBD items have clear path to resolution via Procedure prerequisites and input data collection; TBD status is consistent across documents.)

## Pass 3 Final Notes

**Pass 3 Reconciliation Completed:**
- All cross-document linkages verified bidirectional: Datasheet references to Specification/Guidance/Procedure have corresponding back-references in those documents.
- Entity coverage check confirms all major anticipated data sheet types (OWS equipment, pipe materials, instrumentation, pumps, testing requirements) and themes (OBJ-7 environmental protection, coordination with related deliverables, data source traceability, document metadata) appear consistently across all four documents.
- TBD items cross-check confirms all TBD items are consistent across documents and have clear resolution path via Procedure prerequisites or input data collection steps.
- Terminology consistency verified: "OWS equipment data sheet", "pipe material data sheets", "instrumentation data sheets", "pump data sheets", "OBJ-7 Environmental Protection", "coordination with DEL-03.01/02/03/05", "data source traceability", "interdisciplinary check", "independent check" used consistently across all four documents.
- No conflicts detected between documents; all requirements, rationale, and implementation steps align.

**Document Maturity:**
- This Datasheet, along with Specification, Guidance, and Procedure, has completed three enrichment passes (Pass 1 initial generation, Pass 2 cross-reference and detail enrichment, Pass 3 final reconciliation).
- Documents are ready for WORKING_ITEMS sessions where human engineer will refine, validate, and populate TBD items as design development proceeds and equipment selection/material specifications mature.
- All four documents provide coherent, traceable, and consistent foundation for DEL-03.04 Underground Utilities Data Sheet Package production.
