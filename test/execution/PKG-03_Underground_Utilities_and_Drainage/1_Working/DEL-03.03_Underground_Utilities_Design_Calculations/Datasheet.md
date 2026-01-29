# Datasheet: DEL-03.03 Underground Utilities Design Calculations

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-03.03 |
| Name | Underground Utilities Design Calculations |
| Package | PKG-03 Underground Utilities & Drainage |
| Discipline | Civil |
| Type | Calculation |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Document Number | To be issued per project numbering system (TBD – see Specification §FR-4 and §Documentation for metadata control requirements; Procedure §6 describes numbering assignment process) |
| Calculation Package Types | Storm drainage hydraulic calculations, OWS sizing and retention calculations, duct bank capacity and fill factor calculations, trenchless crossing structural calculations (see Specification §Scope for anticipated calculation types; Procedure §3.2 describes calculation package structure establishment) |
| Revision | 00 (initial issue for design development; see Procedure §6.2 for revision code setting) |
| Calculation Software | Hydraulic modeling software (TBD – typical tools: StormCAD, HydroCAD, HEC-RAS), spreadsheet calculations for OWS sizing and duct bank fill factors (TBD per project calculation standards; Specification §QR-3 software validation requirements; Procedure §Prerequisites lists approved calculation software as required reference) |
| Format | Calculation report with input summaries, assumptions, analysis methodology, results tables, validation checks, reviewer sign-offs (typical format per project calculation standards; Specification §Documentation describes format TBD) |
| Classification | Civil – Underground Utilities Engineering Analysis |
| Calculation Sections | Storm drainage hydraulics, OWS sizing, duct bank capacity analysis, trenchless crossing structural analysis (aligned with Specification §Scope anticipated artifacts; Procedure §3.2 establishes section structure) |
| Design Criteria Sources | Employer's Requirements Volume 2 Part 2: Civil & Process Mechanical Works (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, TBD); civil design brief (TBD); site survey and geotechnical data (TBD); see Specification §Standards for governing standards list |

## Conditions

**Context & environmental expectations:**
- Provides the engineering basis, sizing calculations, and performance verification for underground utilities described in PKG-03, covering storm drainage hydraulics, oil-water separator (OWS) sizing and retention, duct bank capacity analysis, and trenchless crossing structural calculations to substantiate design drawings (DEL-03.01) and specifications (DEL-03.02) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:210; Specification §Scope provides detailed calculation coverage).
- Designed to support storm drainage collection and conveyance, spill containment via OWS, and conduit routing within Fraser Surrey Terminal facility boundaries per Scope Focus (Contractor scope only, Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47; Specification §Scope exclusions clarifies what is NOT in calculation package).
- Deliverable supports **OBJ-7 Environmental Protection**; calculations must demonstrate containment system capacity, OWS treatment performance, and hydraulic conveyance adequacy to verify compliance with environmental protection requirements (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; elaborated in Guidance §P-2 environmental protection performance verification principle; implemented via Procedure §5 environmental protection calculations; verified via Specification §FR-2 requirement and Procedure §7.3.3 independent check).
- Design criteria (design storm return period, hydraulic capacity factors, structural loading, design life, temperature range, seismic criteria, OWS treatment efficiency targets) follow the civil design brief and Employer's Requirements civil standards; specific values remain TBD until Volume 2 Part 2 clauses are extracted (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD; see Specification §PR-3 design life and environmental conditions requirement; Procedure §Prerequisites lists civil design brief and ER Volume 2 Part 2 as required references; Guidance §C-2 addresses ER extraction consideration).
- Coordinate calculation metadata, revision process, and section organization with the Specification §FR-4 and §Documentation requirements to ensure calculation control aligns with project document management procedures (cross-reference: Specification §FR-4 document metadata requirement implemented via Procedure §6 metadata compilation and §8 issue into document control).

**Operational context:**
- Calculation package is used by design engineers to validate drawing dimensions and specification requirements, by checkers/reviewers for independent verification, by QA/QC for design compliance verification (see Procedure §Verification and §7 for review workflow), and as permanent record for operations and future modifications (ASSUMPTION per typical calculation lifecycle; Guidance §C-5 engineering record and future reference consideration explains balancing calculation detail with auditability).
- Environmental protection calculations (OWS sizing for peak runoff and spill volumes, retention time verification, discharge rate limits) are critical for permitting and regulatory compliance; calculation clarity and conservatism directly affect permit approval and environmental inspection outcomes (rationale in Guidance §P-2 environmental protection performance verification principle; Procedure §5 environmental protection calculations implements clear performance demonstration).

## Construction

**Calculation types & analysis focus:**
- Primary calculation packages documented in the design calculations include:
  - **Storm drainage hydraulic calculations**: Runoff calculation (rational method or hydrograph analysis), pipe sizing and slope verification, hydraulic grade line analysis, inlet and catch basin capacity, manhole sizing, outfall discharge rates (Specification §Scope lists "storm drainage hydraulic calculations"; Procedure §4.1 describes storm drainage calculation development; Guidance §P-1 hydraulic performance and capacity verification principle and §Example 1 provide implementation guidance).
  - **Oil-Water Separator (OWS) sizing calculations**: Contributing drainage area determination, peak runoff flow rate, treatment flow capacity, separator volume sizing (oil storage, solids settling, water retention), retention time verification, discharge rate and quality limits (cross-reference: DEL-03.01 Drawing Set for OWS layout geometry per Specification §IF-1; DEL-03.02 Technical Specification for OWS performance criteria per Specification §PR-2; DEL-03.04 Data Sheet Package for equipment specifications; Procedure §4.2 describes OWS sizing calculation development; Guidance §P-2 emphasizes environmental protection performance verification for OBJ-7 compliance; Guidance §Example 2 provides OWS sizing methodology guidance).
  - **Duct bank capacity calculations**: Conduit fill factor analysis (number of cables, cable sizes, allowable fill percentages per electrical codes), conduit spacing and trench width verification, pull box spacing calculations, coordination with electrical load calculations from PKG-17 (Specification §Scope lists "duct bank capacity calculations"; coordinate with PKG-17 Electrical per Specification §IF-1; Procedure §4.3 describes duct bank capacity calculation development including coordination with PKG-17 cable schedules; Guidance §T-4 duct bank calculation detail trade-off recommends simplified fill factor check + reference to PKG-17 for detailed cable analysis; Guidance §Example 3 provides duct bank capacity analysis guidance).
  - **Trenchless crossing structural calculations**: Earth pressure and surcharge loading on casing pipes, casing pipe structural analysis (bending, deflection, buckling), jacking forces and thrust capacity, carrier pipe support and annular space requirements, settlement and differential movement analysis (Specification §Scope lists "trenchless crossing structural calculations"; Procedure §4.4 describes trenchless crossing calculation development; Guidance §T-3 trenchless crossing calculation detail trade-off recommends conservative load factors given uncertainty in boring conditions; Guidance §Example 4 provides crossing structural analysis guidance).
- Input parameters (rainfall intensity-duration-frequency curves, runoff coefficients, soil properties, pipe roughness coefficients, seismic accelerations, design loads) are documented in calculation input summary sections and sourced from civil design brief, geotechnical report, and Employer's Requirements (ASSUMPTION per typical calculation structure; see Specification §Scope input data requirements and §IF-2 linkage to related documents; Procedure §2.2 describes collecting design criteria and input parameters).
- Calculation methodology (governing equations, analysis methods, software tools, design standards applied) is documented to support independent verification and future design modifications (ASSUMPTION per typical calculation documentation practice; see Specification §QR-2 calculation methodology documentation requirement; Procedure §4.5 describes methodology documentation).

**Calculation package organization (ASSUMPTION per typical civil calculation structure; Guidance §C-3 emphasizes calculation structure to avoid scope creep):**
- Cover page: Calculation title, project identification, preparer/checker/approver signatures, revision history
- Input data summary: Design criteria, site parameters, rainfall data, soil properties, applicable standards reference list
- Storm drainage calculations: Drainage area delineation, runoff calculations, pipe sizing, hydraulic grade line analysis, results summary table
- OWS sizing calculations: Contributing area, peak flow determination, separator volume sizing, retention time verification, discharge limit confirmation
- Duct bank capacity calculations: Conduit schedule, fill factor analysis, pull box spacing, coordination notes with PKG-17
- Trenchless crossing calculations: Loading analysis, structural capacity verification, jacking force calculations, settlement assessment
- Appendices: Software output files, manufacturer data sheets, standard calculation references
(Procedure §3.2 establishes calculation section structure; Procedure §2.4 describes documenting applicable standards and data sources in calculation input summary)

## References

- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:210 — scope, description, and anticipated artifacts for DEL-03.03.
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786 — OBJ-7 Environmental Protection mapping includes DEL-03.03 (OWS sizing and drainage calculations support environmental controls).
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47 — Scope Focus confirms contractor-only work scope, affects interface assumptions.
- test/Volume_2_Part_2_Employers_Requirements.pdf — Civil & Process Mechanical Works requirements for storm drainage design criteria, OWS performance requirements, structural loading standards (details TBD, location references to be populated during design development; Specification §Standards lists this as governing standard; Procedure §Prerequisites lists as required reference material; Guidance §C-2 Employer's Requirements extraction consideration addresses extraction importance).
- test/Volume_2_Part_1_Employers_Requirements.pdf — General Requirements including Quality Management Plan, document control procedures, QA/QC requirements, calculation standards (Specification §QR-1 references for quality management compliance; Procedure §Prerequisites lists as required reference material).
- Specification.md — §Scope defines anticipated calculation types; §FR-1 to §FR-4 functional requirements; §PR-1 to §PR-3 performance requirements; §IF-1 to §IF-2 interface requirements; §QR-1 to §QR-3 quality requirements; §Standards governing and supplementary standards; §Verification calculation review process; §Documentation calculation package organization and associated quality records.
- Guidance.md — §Purpose clarifies intent behind calculation production; §P-1 to §P-4 principles (hydraulic performance and capacity verification, environmental protection performance verification for OBJ-7, calculation assumptions and data source traceability, coordination with design drawings and specifications); §C-1 to §C-5 considerations (design criteria availability, ER extraction, calculation structure and scope boundaries, QA sign-offs, engineering record and future reference); §T-1 to §T-4 trade-offs (calculation detail vs conservative assumptions, OWS sizing methodology selection, trenchless crossing calculation conservatism, duct bank capacity analysis coordination with electrical); §Examples 1-4 (storm drainage hydraulic calculation structure, OWS sizing methodology, duct bank fill factor analysis, trenchless crossing structural analysis).
- Procedure.md — §Purpose calculation production and QA purposes; §Prerequisites dependencies, reference materials, design criteria inputs, personnel requirements; §Steps 1-8 (scope review, input data collection, calculation development for storm drainage/OWS/duct banks/trenchless crossings, environmental protection calculations, methodology documentation, metadata compilation, verification workflow, issue into document control); §Verification self-check, interdisciplinary check, independent check; §Records calculation deliverables and quality records.
- Package-level references in `execution/PKG-03_Underground_Utilities_and_Drainage/0_References/_REFERENCE_INDEX.md` (to be populated with civil design brief, rainfall IDF curves, geotechnical report, hydraulic modeling software validation).
- DEL-03.01 Drawing Set — Layout geometry and pipe alignments (pipe routes, invert elevations, OWS location, duct bank routing, crossing locations) provide geometric basis for calculations (referenced per Specification §IF-1; Procedure §2.1 collects as design input for calculation geometry).
- DEL-03.02 Technical Specification — Material specifications, pipe performance requirements, OWS treatment criteria provide design constraints and performance targets for calculations (referenced for performance criteria per Specification §PR-1 and §PR-2; Procedure §2.2 collects as design input; Procedure §7.3.2 validates calculation results support specification requirements).
- DEL-03.04 Data Sheet Package — Equipment data sheets for OWS, pumps, instrumentation provide equipment performance parameters for sizing calculations (referenced for equipment selection validation per Specification §PR-2; Procedure §4.2 OWS sizing calculations reference data sheets).
- DEL-03.05 Installation and Test Records — Installation procedures and testing protocols benefit from calculation margins and tolerances (referenced for installation guidance coordination per Specification §IF-2; Guidance §C-4 QA coordination with installation records).
- DEL-03.06 CCTV Survey Report — Post-installation inspection requirements (calculation performance assumptions may inform inspection acceptance criteria per Specification §QR-3).

## Cross-Document Linkages

**Datasheet ↔ Specification:**
- Datasheet §Attributes "Document Number" TBD → Specification §FR-4 document metadata requirement → Specification §Documentation numbering format TBD
- Datasheet §Attributes "Calculation Package Types" → Specification §Scope anticipated calculation types list (storm drainage hydraulics, OWS sizing, duct bank capacity, trenchless crossing structural match exactly)
- Datasheet §Attributes "Calculation Software" → Specification §QR-3 software validation and quality requirements → Specification §Standards supplementary standards TBD
- Datasheet §Attributes "Design Criteria Sources" → Specification §Standards governing standards list
- Datasheet §Construction storm drainage calculations content → Specification §FR-1 comprehensive hydraulic analysis requirement → Specification §PR-1 hydraulic and structural performance requirement
- Datasheet §Construction OWS sizing content → Specification §FR-2 environmental protection performance verification requirement → Specification §PR-2 treatment capacity and containment performance
- Datasheet §Construction duct bank capacity content → Specification §FR-3 coordination with electrical infrastructure requirement → Specification §IF-1 coordination with PKG-17 electrical
- Datasheet §Construction trenchless crossing calculations content → Specification §Scope trenchless crossing structural calculations → Specification §PR-1 structural performance for crossings
- Datasheet §Construction input parameters and methodology → Specification §QR-2 calculation methodology documentation requirement

**Datasheet ↔ Guidance:**
- Datasheet §Conditions OBJ-7 environmental protection emphasis → Guidance §P-2 environmental protection performance verification principle (explains why OBJ-7 is critical for OWS sizing calculations and discharge limits)
- Datasheet §Construction OWS sizing description → Guidance §P-2 environmental protection performance verification application guidance (peak flow determination, retention time verification, discharge limits) → Guidance §Example 2 OWS sizing methodology
- Datasheet §Construction calculation package organization structure → Guidance §C-3 calculation structure and scope boundaries consideration (avoid scope creep, maintain traceability to decomposition)
- Datasheet §Conditions operational context (design engineers, checkers, QA/QC, permanent record) → Guidance §C-5 engineering record and future reference consideration (balance calculation detail with auditability and future design modifications)
- Datasheet §Attributes "Design Criteria Sources" → Guidance §P-3 calculation assumptions and data source traceability principle (explains why input data documentation is essential for calculation verification and future updates)
- Datasheet §Construction storm drainage calculations content → Guidance §P-1 hydraulic performance and capacity verification principle → Guidance §Example 1 storm drainage hydraulic calculation structure
- Datasheet §Construction duct bank capacity content → Guidance §P-4 coordination with design drawings and specifications principle (duct banks support electrical infrastructure, calculations must enable DEL-03.01 drawing verification) → Guidance §T-4 duct bank capacity analysis coordination trade-off → Guidance §Example 3 duct bank fill factor analysis
- Datasheet §Construction trenchless crossing calculations → Guidance §T-3 trenchless crossing calculation conservatism trade-off → Guidance §Example 4 trenchless crossing structural analysis

**Datasheet ↔ Procedure:**
- Datasheet §Attributes "Revision" 00 initial issue → Procedure §6.2 set initial revision code (describes revision code setting process)
- Datasheet §Attributes "Calculation Package Types" → Procedure §3.2 establish calculation section structure (describes how section structure is established matching anticipated calculation types)
- Datasheet §Construction storm drainage calculations content → Procedure §4.1 develop storm drainage hydraulic calculations (describes runoff calculation, pipe sizing, hydraulic grade line analysis development process)
- Datasheet §Construction OWS sizing content → Procedure §4.2 develop OWS sizing calculations (describes contributing area, peak flow, separator volume, retention time calculations development)
- Datasheet §Construction duct bank capacity content → Procedure §4.3 develop duct bank capacity calculations (describes conduit fill factor, spacing, pull box calculations with PKG-17 coordination)
- Datasheet §Construction trenchless crossing calculations content → Procedure §4.4 develop trenchless crossing structural calculations (describes loading analysis, structural capacity, jacking forces calculations development)
- Datasheet §Construction calculation methodology documentation → Procedure §4.5 document calculation methodology (describes methodology documentation for independent verification)
- Datasheet §Construction calculation package organization structure → Procedure §3.2 calculation section structure establishment matches Datasheet organization (cover page, input summary, storm drainage, OWS, duct banks, trenchless crossings, appendices)
- Datasheet §Conditions calculation control alignment → Procedure §6 metadata compilation + §8 issue into document control system (describes how calculation metadata is populated and calculations are issued per document control procedures)
- Datasheet §References lists quality records → Procedure §Records quality records section (self-check checklist, interdisciplinary review log, independent check review, QA checklists, issue register entry, calculation review logs)

**Entity Coverage Check (all four documents):**
- Storm drainage hydraulic calculations: Datasheet §Construction ✓, Specification §Scope + §FR-1 + §PR-1 ✓, Guidance §P-1 + §Example 1 ✓, Procedure §4.1 + §Records ✓
- OWS sizing calculations: Datasheet §Construction ✓, Specification §Scope + §FR-2 + §PR-2 ✓, Guidance §P-2 + §Example 2 ✓, Procedure §4.2 + §Records ✓
- Duct bank capacity calculations: Datasheet §Construction ✓, Specification §Scope + §FR-3 + §IF-1 (PKG-17) ✓, Guidance §P-4 + §T-4 + §Example 3 ✓, Procedure §4.3 + §Records ✓
- Trenchless crossing structural calculations: Datasheet §Construction ✓, Specification §Scope + §PR-1 ✓, Guidance §T-3 + §Example 4 ✓, Procedure §4.4 + §Records ✓
- Environmental protection (OBJ-7): Datasheet §Conditions ✓, Specification §FR-2 + §PR-2 ✓, Guidance §P-2 ✓, Procedure §5 + §7.3.3 ✓
- Calculation methodology documentation: Datasheet §Construction ✓, Specification §QR-2 ✓, Guidance §P-3 (data source traceability) ✓, Procedure §4.5 + §7.3.4 ✓
- Document metadata/numbering: Datasheet §Attributes ✓, Specification §FR-4 + §Documentation ✓, Guidance §P-3 (traceability) ✓, Procedure §6 + §7.1.5 ✓
- Coordination with related deliverables (DEL-03.01, DEL-03.02, DEL-03.04, DEL-03.05): Datasheet §References ✓, Specification §IF-1 + §IF-2 ✓, Guidance §P-4 + §C-4 ✓, Procedure §2.1 + §2.2 + §7.2 ✓
- Standards compliance and software validation: Datasheet §Attributes ✓, Specification §Standards + §QR-3 ✓, Guidance §P-3 ✓, Procedure §Prerequisites + §7.3.1 ✓

**TBD Items Cross-Check:**
- Document numbering system: Datasheet §Attributes TBD → Specification §FR-4 TBD → Specification §Documentation TBD pending document control register → Procedure §6.1 obtain numbers from document control register
- Calculation software: Datasheet §Attributes TBD (typical tools noted) → Specification §QR-3 TBD software validation → Specification §Standards supplementary standards TBD → Procedure §Prerequisites lists approved calculation software as required reference
- Calculation format: Datasheet §Attributes TBD (typical format noted) → Specification §Documentation TBD per project calculation standards → Procedure §Prerequisites lists project calculation standards as required reference
- Design criteria values (design storm, hydraulic capacity factors, OWS treatment efficiency, design life, seismic, temperature, structural loading): Datasheet §Attributes and §Conditions TBD from ER Volume 2 Part 2 and civil design brief → Specification §PR-1, §PR-2, §PR-3 TBD from ER and design brief → Procedure §Prerequisites lists ER Volume 2 Part 2 and civil design brief as required references → Guidance §C-1 and §C-2 address design criteria availability and ER extraction considerations

(All TBD items have clear path to resolution via Procedure prerequisites and input data collection; TBD status is consistent across documents.)

## Pass 3 Final Notes

**Pass 3 Reconciliation Completed:**
- All cross-document linkages verified bidirectional: Datasheet references to Specification/Guidance/Procedure have corresponding back-references in those documents.
- Entity coverage check confirms all major anticipated calculation types (storm drainage hydraulics, OWS sizing, duct bank capacity, trenchless crossing structural) and themes (OBJ-7 environmental protection, coordination with related deliverables, standards compliance, calculation methodology documentation) appear consistently across all four documents.
- TBD items cross-check confirms all TBD items are consistent across documents and have clear resolution path via Procedure prerequisites or input data collection steps.
- Terminology consistency verified: "storm drainage hydraulic calculations", "OWS sizing calculations", "duct bank capacity calculations", "trenchless crossing structural calculations", "OBJ-7 Environmental Protection", "coordination with DEL-03.01/02/04/05", "standards compliance", "calculation methodology documentation", "interdisciplinary check", "independent check" used consistently across all four documents.
- No conflicts detected between documents; all requirements, rationale, and implementation steps align.

**Document Maturity:**
- This Datasheet, along with Specification, Guidance, and Procedure, has completed three enrichment passes (Pass 1 initial generation, Pass 2 cross-reference and detail enrichment, Pass 3 final reconciliation).
- Documents are ready for WORKING_ITEMS sessions where human engineer will refine, validate, and populate TBD items as design development proceeds and input data (civil design brief, geotechnical report, ER Volume 2 Part 2 extracts) becomes available.
- All four documents provide coherent, traceable, and consistent foundation for DEL-03.03 Underground Utilities Design Calculations production.
