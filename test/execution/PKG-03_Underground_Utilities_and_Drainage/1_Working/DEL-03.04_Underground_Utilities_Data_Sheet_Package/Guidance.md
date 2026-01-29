# Guidance: DEL-03.04 Underground Utilities Data Sheet Package

## Purpose

Provide decision-making context and engineering rationale for developing the Underground Utilities Data Sheet Package for PKG-03, ensuring that OWS equipment data, pipe material specifications, and instrumentation data substantiate design deliverables and support procurement, installation, and operations.

**Why this deliverable matters:**
- Data sheets consolidate equipment specifications and material properties from multiple sources (manufacturer catalogs, calculations, specifications) into procurement-ready format; accurate data sheets prevent procurement delays and installation conflicts (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:211).
- Environmental protection equipment data (OWS specifications, discharge monitoring instrumentation) directly supports **OBJ-7 Environmental Protection** by documenting treatment capacity and performance verification methods (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; Specification §FR-2).
- Data sheets create permanent equipment and material record for operations maintenance, spare parts procurement, and future facility modifications (rationale for Specification §QR-2 data source traceability; supports Datasheet §Conditions operational context).

## Principles

**P-1: Equipment and Material Substantiation**
- Data sheets must provide complete equipment specifications and material properties sufficient for procurement, submittal preparation, installation verification, and operations maintenance; incomplete data causes procurement delays and field modifications.
- **Application:** Document equipment type/model, capacities, performance parameters, materials of construction, dimensions/weights, electrical requirements, testing requirements; for materials, document material type, sizes, properties, standards compliance, jointing methods, testing requirements.
- **Rationale:** Procurement teams need complete specifications to prepare purchase orders; suppliers need clear requirements for submittal preparation; QA/QC needs acceptance criteria for conformance inspection (supports Specification §FR-1).
- **Cross-reference:** Datasheet §Construction equipment and material data sheet content; Procedure §4 data sheet development; Specification §FR-1 and §PR-1.

**P-2: Environmental Protection Equipment Substantiation**
- OWS equipment data sheet must document treatment capacity, retention volume, treatment performance targets, and discharge monitoring instrumentation to demonstrate **OBJ-7 Environmental Protection** compliance and support permitting/regulatory approval.
- **Application:** Specify OWS design flow rate, peak flow capacity, separator volume components (oil/solids/water), retention time, treatment performance (oil removal efficiency), discharge water quality targets, instrumentation (level, flow, oil thickness, alarms).
- **Rationale:** Environmental permits specify treatment performance and discharge limits; OWS equipment specifications must demonstrate compliance; instrumentation enables continuous monitoring and compliance verification (supports Specification §FR-2 and §PR-2).
- **Cross-reference:** Datasheet §Construction OWS equipment data sheet; Procedure §4.2 OWS data sheet development; Specification §FR-2; Example 1 OWS data sheet structure.

**P-3: Data Source Traceability and Accuracy**
- All data sheet content must be traceable to source documents (manufacturer catalogs, supplier specifications, DEL-03.03 calculations, DEL-03.02 specification) with references and dates to support verification, procurement, and future equipment replacement.
- **Application:** Document data sources in data sheet notes or introduction; include manufacturer catalog numbers, supplier specification document IDs, calculation references, specification clause references; validate data accuracy against source documents before finalization.
- **Rationale:** Undocumented data creates verification difficulties; inaccurate data causes procurement errors, installation delays, equipment performance failures; clear data sources enable future equipment replacement with equivalent specifications (supports Specification §QR-2).
- **Cross-reference:** Datasheet §Attributes "Data Sources"; Procedure §2 input data collection and §7.1.2 data accuracy verification; Specification §QR-2.

**P-4: Coordination with Procurement and Installation**
- Data sheets must support procurement workflows (purchase order preparation, submittal review) and installation verification (conformance inspection, testing acceptance criteria) through clear organization and complete content.
- **Application:** Organize data sheets by equipment/material type for efficient procurement; include submittal data requirements; document testing requirements and acceptance criteria cross-referencing DEL-03.05 Installation and Test Records; use consistent format across all data sheets.
- **Rationale:** Data sheet organization affects procurement efficiency; incomplete testing requirements delay installation acceptance; consistent format improves review efficiency and reduces errors (supports Specification §IF-1 coordination with DEL-03.05 and §QR-1).
- **Cross-reference:** Datasheet §Conditions operational context (procurement, installation); Procedure §3.2 package structure; Specification §IF-1; Consideration C-4 QA coordination.

## Considerations

**C-1: Manufacturer Data Availability**
- Data sheets require manufacturer catalog data and supplier specifications; data availability varies depending on equipment selection and procurement phase; preliminary data sheets may use typical/generic specifications pending final equipment selection.
- **Impact:** Initial data sheets may use manufacturer catalog data for budget equipment selection; final data sheets require actual equipment submittals after procurement; data sheet revisions required when equipment selection changes.
- **Recommended approach:** Develop preliminary data sheets using manufacturer catalog data for representative equipment models; flag data requiring confirmation from actual equipment submittals; coordinate data sheet revision schedule with procurement milestones.
- **Cross-reference:** Specification §PR-1 equipment performance; Datasheet §Conditions TBD items; Procedure §2.2 manufacturer data collection.

**C-2: ER Compliance Verification**
- Employer's Requirements Volume 2 Part 2 contains equipment and material standards; data sheets must demonstrate compliance; ER requirements affect equipment selection and material specifications.
- **Impact:** OWS performance requirements, pipe material standards, testing protocols are TBD pending ER extraction; data sheet content must address ER compliance verification needs.
- **Recommended approach:** Review ER Volume 2 Part 2 for applicable equipment/material requirements; document ER compliance in data sheet notes; cross-reference ER clauses for key specifications.
- **Cross-reference:** Specification §Standards governing standards (ER Volume 2 Part 2); Datasheet §Conditions and §Attributes TBD from ER; Principle P-3 data source traceability.

**C-3: Data Sheet Structure and Scope Boundaries**
- Data sheet package scope aligns with DEL-03.04 decomposition scope (OWS, pipes, instrumentation for PKG-03); avoid scope creep into adjacent package equipment data (e.g., process pumps in PKG-15, detailed I&C in PKG-18).
- **Impact:** Scope boundaries between civil underground utilities equipment and adjacent package equipment must be clearly defined; duct bank instrumentation may overlap with PKG-18 I&C scope.
- **Recommended approach:** Review decomposition scope during planning; organize data sheets by equipment/material type matching Specification §Scope; identify interface equipment requiring coordination; document scope boundaries in introduction.
- **Cross-reference:** Specification §Scope anticipated data sheets and exclusions; Datasheet §Construction package organization; Procedure §1 scope review; Trade-off T-4 instrumentation scope.

**C-4: QA Sign-offs and Coordination with Installation Records**
- Data sheet review and approval creates traceable QA record; data sheet testing requirements inform installation testing documented in DEL-03.05; coordination ensures test acceptance criteria align with equipment/material specifications.
- **Impact:** Data sheet signatures document that equipment/material specifications are verified before procurement; testing requirements provide basis for installation acceptance testing.
- **Recommended approach:** Follow data sheet review workflow per Procedure §Verification; coordinate with DEL-03.05 development team to ensure test procedures reference data sheet specifications; provide data sheet extracts for test procedure development.
- **Cross-reference:** Specification §Verification; Specification §IF-1 coordination with DEL-03.05; Principle P-4 coordination with installation; Procedure §7 verification and §Records QA documentation.

**C-5: Procurement Use and Operations Reference**
- Data sheets serve multiple uses: procurement purchase orders, supplier submittals, installation verification, operations maintenance, future equipment replacement; content must balance procurement detail with operations usability.
- **Impact:** Procurement needs complete specifications for competitive bidding; operations needs equipment identification for spare parts; excessive detail reduces clarity; insufficient detail causes procurement ambiguity.
- **Recommended approach:** Include core specifications in main data sheet tables; use appendices for supplemental data (manufacturer curves, detailed dimensions); focus on performance-based specifications allowing supplier flexibility where appropriate.
- **Cross-reference:** Datasheet §Conditions operational context; Principle P-4 procurement and installation coordination; Trade-off T-1 data sheet detail vs procurement flexibility.

## Trade-offs

**T-1: Data Sheet Detail vs Procurement Flexibility**
- **Trade-off:** Detailed equipment specifications (model numbers, specific features) ensure exact procurement but limit supplier competition; performance-based specifications allow supplier flexibility but require more submittal review.
- **Recommended approach:** Use performance-based specifications for equipment allowing multiple manufacturers (OWS treatment capacity targets vs specific model); use detailed specifications where standardization is required (pipe materials, instrumentation types); document basis of selection in data sheet notes.
- **Cross-reference:** Consideration C-5 procurement use; Principle P-1 equipment substantiation; Specification §PR-1 and §PR-2.

**T-2: OWS Equipment Specification Approach**
- **Trade-off:** Specify OWS by manufacturer model number vs performance requirements; model specification ensures known performance but limits competition; performance specification allows supplier innovation but increases submittal review effort.
- **Recommended approach:** Specify OWS by performance requirements (treatment capacity, retention volume, efficiency, discharge limits) allowing multiple manufacturers; include design basis from DEL-03.03 calculations; require submittal demonstration of compliance.
- **Cross-reference:** Principle P-2 environmental protection equipment; Example 1 OWS data sheet; Specification §FR-2 and §PR-2.

**T-3: Pipe Material Data Sheet Content**
- **Trade-off:** Include detailed pipe installation requirements in data sheets vs reference DEL-03.02 specification; detailed data sheets support standalone procurement but duplicate specification content; specification references reduce duplication but require coordination.
- **Recommended approach:** Include material properties, sizes, jointing methods in data sheets; reference DEL-03.02 for installation requirements (bedding, backfill, testing); use data sheet notes to cross-reference specification clauses.
- **Cross-reference:** Principle P-1 material substantiation; Example 2 pipe material data sheet; Specification §IF-1 coordination with DEL-03.02.

**T-4: Instrumentation Data Sheet Scope**
- **Trade-off:** Include detailed instrumentation specifications in PKG-03 data sheets vs coordinate with PKG-18 I&C; PKG-03 data sheets support civil procurement but may duplicate PKG-18 content; PKG-18 coordination reduces duplication but requires interface management.
- **Recommended approach:** Include instrumentation directly associated with civil underground utilities (OWS level/flow/oil thickness sensors) in PKG-03 data sheets; coordinate with PKG-18 for detailed I&C specifications and integration requirements; document coordination boundary in data sheet introduction.
- **Cross-reference:** Specification §FR-3 instrumentation substantiation; Specification §IF-1 coordination note; Consideration C-3 scope boundaries.

## Examples

**Example 1: OWS Equipment Data Sheet Structure**

**Recommended content:**
1. Equipment identification: Type (gravity separator, coalescing plate separator, etc.), manufacturer/model (or "TBD - performance-based specification"), design basis reference (DEL-03.03 calculation number)
2. Performance parameters: Design flow rate, peak flow capacity, separator volume (oil/solids/water compartments), retention time, oil removal efficiency target, discharge water quality target
3. Physical specifications: Dimensions (length/width/height), weight (empty/operating), materials of construction (internals, coatings), access provisions
4. Instrumentation: Level sensors (type, range), flow meters (type, range), oil layer thickness monitor, alarms (high level, high oil layer)
5. Electrical requirements: Power supply voltage/phase, connected load
6. Testing requirements: Factory performance testing, field commissioning testing, reference to DEL-03.05 test procedures
7. Data sources: DEL-03.03 calculation reference, manufacturer catalog reference, ER compliance clause references

**Application to DEL-03.04:** This structure demonstrates environmental protection equipment substantiation (Principle P-2) with complete procurement specifications and clear testing requirements supporting OBJ-7 compliance.

**Cross-reference:** Datasheet §Construction OWS data sheet content; Specification §FR-2; Procedure §4.2.

**Example 2: Pipe Material Data Sheet Organization**

**Recommended organization (separate data sheet for each material type):**
- HDPE pipe data sheet: Material standard (ASTM, CSA), pipe sizes (diameter range), wall thickness (SDR ratings), pressure class, jointing method (fusion welding), chemical resistance, testing (hydrostatic pressure, joint integrity)
- Concrete pipe data sheet: Material standard, pipe sizes, strength class, jointing method (gasket, mortar), bedding requirements reference, testing (three-edge bearing test, joint watertightness)
- PVC pipe data sheet: Material standard, pipe sizes, pressure class, jointing method (solvent cement, gaskets), chemical resistance, testing
- Steel casing pipe data sheet: Material standard (API, ASTM), pipe sizes, wall thickness, welding requirements, corrosion protection (coatings, cathodic protection if required), testing (hydrostatic, NDT)

**Application to DEL-03.04:** Organizing by material type supports efficient procurement and installation verification; cross-referencing DEL-03.02 for installation requirements avoids duplication (Trade-off T-3).

**Cross-reference:** Datasheet §Construction pipe material data sheets; Specification §FR-1; Procedure §4.3.

**Example 3: Instrumentation Data Sheet Content**

**Recommended content (for each instrument type):**
- Level sensors (OWS): Sensor type (ultrasonic, float, etc.), measurement range, accuracy, output signal (4-20mA, etc.), materials, environmental rating, calibration requirements
- Flow meters (OWS inlet/outlet): Meter type, flow range, accuracy, output signal, materials, installation requirements, calibration
- Oil layer thickness monitor (OWS): Sensor type, measurement range, accuracy, output signal, materials, calibration

**Application to DEL-03.04:** Instrument data sheets support civil procurement while coordinating with PKG-18 for integration (Trade-off T-4).

**Cross-reference:** Datasheet §Construction instrumentation data sheets; Specification §FR-3; Procedure §4.4.

**Example 4: Testing Requirements Documentation**

**Recommended approach:**
- Include testing requirements in each equipment/material data sheet section
- Provide testing requirements summary consolidating all requirements with cross-references to DEL-03.05 test procedures
- Document acceptance criteria from ER, standards, or manufacturer recommendations
- Example testing requirements table:
  | Equipment/Material | Test Type | Standard | Acceptance Criteria | DEL-03.05 Reference |
  |------|------|------|------|------|
  | HDPE pipe | Hydrostatic pressure | ASTM D2924 | 1.5x rated pressure | Test Proc TP-03.XX |
  | OWS | Performance test | Manufacturer procedure | >95% oil removal | Test Proc TP-03.YY |

**Application to DEL-03.04:** Clear testing requirements documentation supports QA coordination with DEL-03.05 (Consideration C-4).

**Cross-reference:** Datasheet §Construction testing requirements; Specification §QR-3; Procedure §4.6.

## Pass 3 Final Notes

**Pass 3 Reconciliation Completed:**
- All cross-document linkages verified; principles linked to requirements and procedures; entity coverage confirmed; terminology consistent.
- Documents ready for WORKING_ITEMS sessions.
