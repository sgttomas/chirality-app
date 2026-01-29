# Specification: DEL-03.01 Underground Utilities Design Drawing Set

## Scope

This specification governs the development of the **Underground Utilities Design Drawing Set** for **PKG-03 Underground Utilities & Drainage**. The set defines the design arrangement, geometry, and installation details for storm drainage, containment, duct banks, and trenchless crossings per the Employer's Requirements (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:188).

**Anticipated artifacts within this scope:**
- Storm drainage plans and profiles (plan-and-profile sheets showing pipe alignment, invert elevations, hydraulic grade lines)
- Oil-Water Separator (OWS) layout (plan and sections with piping connections, instrumentation, capacity details)
- Duct bank plans (conduit routing plans, trench cross-sections, pull box locations, conduit schedules)
- Trenchless crossing drawings (alignment plans/profiles, boring/jacking details, casing and carrier pipe specifications)

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:188; elaborated in Datasheet §Construction for drawing organization structure)

**Exclusions:**
- Material specifications, pipe performance requirements, and hydraulic calculations are documented in DEL-03.02 Technical Specification and DEL-03.03 Design Calculations (not in this drawing set).
- Construction procedures, installation testing, and commissioning are documented in DEL-03.05 Installation and Test Records (not in this drawing set).
- Above-ground structures, buildings, and process equipment are outside PKG-03 scope per Scope Focus (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47).

## Requirements

### Functional Requirements

**FR-1: Comprehensive Underground Utilities Arrangement**
- Provide complete plans, profiles, and details for storm drainage, OWS, duct bank routing, and trenchless crossings to demonstrate the underground utilities arrangement described in the decomposition (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:188).
- Drawing set shall include sufficient detail for construction teams to understand excavation limits, pipe alignments, connection points, and coordination with adjacent systems (ASSUMPTION per typical civil drawing set function; rationale in Guidance §Purpose).
- Verification: Procedure §Verification self-check confirms all anticipated artifacts are present; interdisciplinary check verifies coordination with adjacent disciplines.

**FR-2: Environmental Protection Features**
- Capture oil-water separator layout, containment sumps, drainage flow paths, and OWS instrumentation details to support **OBJ-7 Environmental Protection** objectives for PKG-03 (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786).
- Drawings shall clearly annotate environmental protection features (containment boundaries, OWS capacity, emergency overflow routes) to facilitate construction inspection and regulatory compliance verification (rationale in Guidance §Principles; operational context in Datasheet §Conditions).
- Verification: Procedure §Steps annotation requirement for environmental protection features; Procedure §Verification independent check confirms compliance with civil standards and Employer's Requirements.

**FR-3: Coordination Across Underground Networks**
- Represent coordination requirements (utility separations, crossing details, interface tie-ins) so civil disciplines, other packages (PKG-02 grading, PKG-04 paving, PKG-17 electrical), and QA/QC can verify constructability before installation begins (Dependencies: NOT_TRACKED per `_DEPENDENCIES.md`; coordination managed externally by humans).
- Drawings shall use consistent coordinate system and vertical datum matching PKG-02 site grading deliverables to ensure elevation ties are correct (Datasheet §Attributes "Coordinate System" specifies alignment with PKG-02).
- Verification: Procedure §Verification interdisciplinary check includes coordination review with earthworks, paving, process, and electrical disciplines.

**FR-4: Drawing Metadata and Document Control**
- Ensure drawing metadata (numbering, revision, title blocks, sheet sizes, scales) aligns with the Datasheet attributes and project document control expectations (Datasheet §Attributes lists metadata fields; this requirement ensures drawings implement those fields correctly).
- Drawing numbering scheme shall follow project document control procedures; initial issue revision is "00" per Datasheet §Attributes (TBD: specific numbering format pending project document control register definition per Procedure §Prerequisites).
- Verification: Procedure §Steps revision history compilation; Procedure §Verification QA review confirms metadata completeness before document control system release.

### Performance Requirements

**PR-1: Hydraulic and Structural Performance**
- Conform to the hydraulic capacity, structural load, drainage performance, and seismic design expectations described in the Employer's Requirements Volume 2 Part 2: Civil & Process Mechanical Works (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, specific clauses TBD).
- Storm drainage system design shall accommodate the design storm event (return period TBD from Employer's Requirements); pipe sizes and slopes shown on plan-and-profile sheets shall support calculated flows documented in DEL-03.03 Design Calculations (interface linkage to calculations deliverable; Datasheet §Construction describes plan-and-profile content).
- Verification: Design calculations (DEL-03.03) validate hydraulic performance; drawing annotations reference calculation results; Procedure §Verification independent check confirms compliance with civil standards.

**PR-2: Facility Throughput and Containment Support**
- Ensure drawings support the permitted throughput (1,000,000 MT/a canola oil), storage capacity (45,000 MT in three tanks), and containment expectations for Phase 1 as described in the decomposition's project overview parameters (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md, Project Overview section; Datasheet §Conditions references these parameters).
- OWS layout shall accommodate anticipated runoff volumes and spill containment requirements; capacity sizing documented in DEL-03.02 Technical Specification and verified via DEL-03.04 Data Sheet Package (interface linkage; Datasheet §Construction notes that materials/performance are in related deliverables).
- Verification: Procedure §Steps environmental protection annotation requirement ensures OWS capacity and containment volumes are clearly shown; Procedure §Verification interdisciplinary check includes process team review of containment adequacy.

**PR-3: Design Life and Environmental Conditions**
- Drawing details shall reflect design life, temperature range, seismic criteria, and other environmental design parameters from the civil design brief and Employer's Requirements (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD; Datasheet §Conditions lists these as TBD pending ER extraction).
- Pipe materials, trench details, and structural elements shown on drawings shall be compatible with site soil conditions, groundwater levels, and seismic design category (ASSUMPTION: typical civil design considerations; specific values TBD from geotechnical report and Employer's Requirements).
- Verification: Procedure §Verification independent check confirms design parameters match civil design brief; drawing general notes reference applicable design criteria documents.

### Interface Requirements

**IF-1: Coordination with Adjacent Packages**
- Coordinate layout information with adjacent packages to ensure interface consistency:
  - **PKG-02 Site Grading**: Coordinate site grading plans, finished grade elevations, drainage flow directions; ensure storm drainage invert elevations tie correctly to site grades (Datasheet §Attributes specifies coordinate system alignment with PKG-02).
  - **PKG-04 Pavement and Surfacing**: Coordinate pavement sections, drainage inlet locations, trench restoration details; ensure utility trenches do not compromise pavement structural design.
  - **PKG-17 Electrical Power Distribution**: Coordinate duct bank routing, separation clearances, pull box locations; ensure electrical conduit paths shown in PKG-17 match duct bank plans in this drawing set (Datasheet §Construction lists duct banks as supporting electrical and communications infrastructure).
  - **PKG-14 Process Piping**: Coordinate pipe crossing locations, utility separations, trench congestion in areas with both process piping and underground utilities.
- Coordination is managed through existing project coordination workflows per Scope Focus (Contractor scope only, Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47); dependencies are tracked externally (see `_DEPENDENCIES.md`).
- Verification: Procedure §Verification interdisciplinary check includes review by adjacent discipline leads; Procedure §Steps coordination data collection ensures upstream package deliverables are approved for design release before detailing.

**IF-2: Linkage to Related PKG-03 Deliverables**
- Drawing callouts, annotations, and detail references shall link to performance requirements and material specifications documented in:
  - **DEL-03.02 Technical Specification**: Material selections, pipe performance requirements, OWS treatment criteria (Datasheet §Construction notes materials are in Technical Specification).
  - **DEL-03.03 Design Calculations**: Hydraulic calculations, pipe sizing basis, structural analysis (PR-1 references calculation validation).
  - **DEL-03.04 Data Sheet Package**: Equipment data sheets for OWS, pumps, instrumentation (PR-2 references OWS capacity sizing in Data Sheet Package).
  - **DEL-03.05 Installation and Test Records**: Construction sequencing, QA/QC inspection points, as-built markup requirements (Procedure §Records cross-references installation records).
- Ensure drawing notes include "See DEL-03.0X for [performance/material/calculation] requirements" to maintain traceability across deliverables (ASSUMPTION per typical drawing set practice of referencing related documents; Guidance §Considerations emphasizes traceability for QA sign-offs).
- Verification: Procedure §Verification QA review confirms drawing annotations reference correct related deliverable IDs and sections.

### Quality Requirements

**QR-1: Compliance with Quality Management Plan**
- Deliverables shall comply with the project Quality Management Plan and document control expectations captured in Volume 2 Part 1: Employer's Requirements – General Requirements (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, details TBD).
- Drawing production workflow shall follow quality procedures: originator prepares, checker reviews, approver signs (ASSUMPTION per typical QA process; Procedure §Verification describes review steps).
- Verification: Procedure §Verification self-check, interdisciplinary check, and independent check are documented with review stamps/signatures; QA checklists are completed before issue (Procedure §Records lists QA checklists in records output).

**QR-2: Drawing Review and Approval Process**
- Drawings shall be internally reviewed by originators, checked by discipline checker, and approved by discipline lead per QA/QC processes before issue (ASSUMPTION per Procedure §Verification workflow).
- Review checkpoints include: dimensional accuracy, coordination with adjacent systems, compliance with civil standards, annotation completeness, metadata correctness (Procedure §Verification lists review activities).
- Drawing status codes (e.g., "For Review", "For Construction", "As-Built") shall be clearly marked on title blocks per project document control procedures (TBD: specific status code definitions pending project conventions; Datasheet §Attributes lists revision as "00" for initial issue).
- Verification: Procedure §Steps deliver drawing set into document control system; Procedure §Verification QA review confirms all review stamps and approval signatures are present before release.

**QR-3: CAD Standards and Drawing Conventions**
- Drawings shall conform to project CAD standards for layer naming, line weights, text styles, symbol libraries, and annotation standards (Datasheet §Attributes "CAD Standard" lists project CAD convention as TBD).
- Drawing organization, sheet layouts, and detail callout conventions shall be consistent across all sheets in the set to facilitate construction use and future as-built updates (Datasheet §Construction describes drawing organization structure; Guidance §Principles emphasizes consistent notation).
- Verification: Procedure §Steps CAD standard alignment check during schematic arrangements phase; Procedure §Verification self-check includes CAD standard compliance review.

## Standards

**Governing Standards:**
- **Employer's Requirements Volume 2 Part 2: Civil & Process Mechanical Works** is the authoritative source for applicable civil standards, pipe materials, installation methods, and product selections; specific clauses will be extracted and referenced in drawing general notes as design details mature (Source: test/Volume_2_Part_2_Employers_Requirements.pdf).
- **Employer's Requirements Volume 2 Part 1: General Requirements** governs project Quality Management Plan, document control procedures, and QA/QC requirements (Source: test/Volume_2_Part_1_Employers_Requirements.pdf).

**Supplementary Standards (TBD pending project definition):**
- CAD discipline standards: Layer naming conventions, line weight standards, symbol libraries, annotation standards (Datasheet §Attributes and QR-3 reference project CAD standards; to be documented in package `0_References/` per Procedure §Prerequisites).
- Civil design criteria: Design storm return periods, seismic design category, soil bearing capacity, groundwater design levels (PR-3 references civil design brief; specific values TBD from Employer's Requirements and geotechnical report).
- Drawing numbering and revision control: Project document control register, drawing numbering scheme, revision code definitions, title block template (FR-4 and QR-2 reference document control procedures; TBD pending project document management plan).

**Applicable Codes and Regulations (ASSUMPTION pending ER extraction):**
- National Building Code of Canada (NBC) – civil works provisions
- British Columbia Building Code (BCBC) – local amendments
- Canadian Standards Association (CSA) standards for pipe materials and installations
- Local municipal standards (City of Surrey, Metro Vancouver) for storm drainage tie-ins and environmental discharge permits
- Environmental regulations for oil-water separator design and discharge limits (supports OBJ-7 Environmental Protection per FR-2)

(Note: Specific code editions and applicable clauses to be extracted from Employer's Requirements Volume 2 Part 2 during design development; see Procedure §Prerequisites for reference material review requirement.)

## Verification

**Design Review Process:**
- **Self-check (originator review)**: Ensures annotations, dimensions, profiles, and details match design inputs from calculations (DEL-03.03) and specifications (DEL-03.02); verifies CAD standard compliance (QR-3); confirms all anticipated artifacts (Scope list) are present; checks metadata completeness (FR-4). (Source: Procedure §Verification self-check step; Datasheet §Cross-Document Linkages references Procedure verification process.)

- **Interdisciplinary check**: Verifies coordination with earthworks (PKG-02), paving (PKG-04), process (PKG-14), and electrical (PKG-17) disciplines per IF-1 requirements; confirms utility separations and crossing details are constructible; reviews environmental protection annotations (FR-2) with process team. (Source: Procedure §Verification interdisciplinary check step; ASSUMPTION per typical engineer-review process and Quality Management Plan per test/Volume_2_Part_1_Employers_Requirements.pdf.)

- **Independent check**: Confirms compliance with civil standards (Standards section) and Employer's Requirements (Volume 2 Part 2); validates hydraulic and structural performance (PR-1) against calculation results (DEL-03.03); ensures design parameters (PR-3) match civil design brief; records results in review stamp blocks on drawings. (Source: Procedure §Verification independent check step; reviews tie to Specification requirements to close verification loop.)

**Dimensional and Coordination Verification:**
- Scale, coordinates, and elevations checks confirm that plan-and-profile sheets align with site constraints from PKG-02 site grading and survey data (IF-1 coordination requirement; Datasheet §Attributes specifies coordinate system match).
- Utility separation clearances verified against applicable standards and constructability constraints (ASSUMPTION: typical civil coordination check).
- Results recorded in drawing review records and QA checklists per QR-1 (Procedure §Records lists drawing review logs and QA checklists).

**Traceability Verification:**
- Drawing annotations reference Data Sheet Package (DEL-03.04) and Technical Specification (DEL-03.02) for performance requirements per IF-2 linkage requirement.
- Drawing general notes reference applicable standards, design criteria documents, and calculation reports to maintain traceability (ASSUMPTION per typical drawing set practice).
- Procedure §Verification QA review confirms drawing callouts reference correct related deliverable IDs and sections per IF-2.

## Documentation

**Documented Artifacts:**
- Storm drainage plans and profiles (plan-and-profile sheets with pipe alignments, invert elevations, slopes, hydraulic grade lines)
- OWS layout (plan and sections showing separator location, piping, instrumentation, capacity annotations)
- Duct bank plans (conduit routing plans, trench cross-sections, pull box details, conduit schedule tables)
- Trenchless crossing drawings (alignment plans/profiles, boring/jacking details, casing and carrier pipe specifications)
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:188; detailed in Datasheet §Construction)

**Drawing Set Organization:**
- Cover sheet: Drawing index, abbreviations, general notes, coordinate system / datum statement, applicable standards list
- Site utility plan: Overall layout showing all underground systems, tie-ins to existing infrastructure
- Plan-and-profile sheets: Storm drainage system details (one sheet per branch or segment)
- OWS layout sheet: Enlarged plan and sections with piping and instrumentation details
- Duct bank plan and sections: Conduit routing, trench cross-sections, pull box details, conduit schedules
- Trenchless crossing sheets: Alignment and details for each crossing
- Detail sheets: Standard details for pipe connections, trench sections, manhole/catch basin installations, utility separations
(ASSUMPTION per typical civil drawing set structure; Datasheet §Construction describes drawing organization; Guidance §Considerations emphasizes sheet structure to avoid scope creep.)

**Format, Numbering, and Revision Control:**
- Format: Sheet size per project drawing standards (Datasheet §Attributes lists typical ANSI D or ISO A1 for civil plan sheets, TBD).
- Numbering: Drawing numbers to be issued per project numbering system (FR-4 requirement; Datasheet §Attributes notes numbering system TBD).
- Revision control: Initial issue revision "00" per Datasheet §Attributes; subsequent revisions follow project document control procedures (QR-2 requirement).
- Metadata: Title blocks include drawing number, title, revision, issue date, originator, checker, approver, project name, deliverable ID (FR-4 metadata requirement; Procedure §Steps includes revision history compilation).
- Details (e.g., numbering scheme format, revision code definitions, title block template) remain TBD until the project document control register is defined (Source: test/Volume_2_Part_1_Employers_Requirements.pdf per QR-1; Procedure §Prerequisites lists document control procedures as required reference material).

**Associated Quality Records:**
- Drawing review logs documenting self-check, interdisciplinary check, and independent check results (Verification section review process; Procedure §Records lists drawing review logs).
- QA checklists confirming CAD standard compliance, metadata completeness, coordination verification (QR-1 and QR-3 requirements; Procedure §Records lists QA checklists).
- Issue registers tracking drawing issue status, distribution, and revisions (QR-2 requirement; Procedure §Records lists issue registers).
- Discipline review records from adjacent packages (IF-1 coordination; Procedure §Records lists discipline review records).
(All records retained per project document control procedures per test/Volume_2_Part_1_Employers_Requirements.pdf.)

## Cross-Document Notes

**Specification → Datasheet:**
- Scope anticipated artifacts → Datasheet §Construction describes each artifact in detail with drawing content expectations
- FR-4 drawing metadata requirements → Datasheet §Attributes lists metadata fields to be implemented on drawings
- IF-1 coordinate system coordination with PKG-02 → Datasheet §Attributes "Coordinate System" specifies alignment requirement
- Standards section governing codes → Datasheet §Conditions references civil standards for design parameters

**Specification → Guidance:**
- FR-2 environmental protection features → Guidance §Principles elaborates OBJ-7 rationale and containment controls clarity
- PR-1 hydraulic and structural performance → Guidance §Principles explains hydraulic conveyance and drainage rationale
- IF-1 coordination requirements → Guidance §Considerations emphasizes coordination needs with adjacent disciplines
- QR-3 drawing conventions → Guidance §Principles emphasizes consistent notation and layer structure

**Specification → Procedure:**
- Verification section design review process → Procedure §Verification describes self-check, interdisciplinary check, independent check steps in detail
- FR-1 comprehensive arrangement requirement → Procedure §Steps schematic arrangements workflow produces drawings to meet this requirement
- QR-1 quality management compliance → Procedure §Verification implements QA/QC review per Quality Management Plan
- Documentation associated quality records → Procedure §Records lists all QA documentation outputs

**Requirement Traceability:**
- Each functional requirement (FR-1 to FR-4) has corresponding Procedure verification step
- Each performance requirement (PR-1 to PR-3) references design inputs (calculations, specifications) and has independent check verification
- Each interface requirement (IF-1 to IF-2) has interdisciplinary check or coordination verification
- Each quality requirement (QR-1 to QR-3) has QA review checkpoint in Procedure §Verification

## Pass 2 Enrichments

This Pass 2 revision adds:
1. Expanded Scope section with explicit exclusions clarifying what is NOT in this drawing set (materials/specs in DEL-03.02, installation in DEL-03.05).
2. Detailed functional requirements (FR-1 to FR-4) with explicit verification cross-references to Procedure sections.
3. Detailed performance requirements (PR-1 to PR-3) with interface linkages to related deliverables (DEL-03.02, DEL-03.03, DEL-03.04).
4. Detailed interface requirements (IF-1 to IF-2) listing specific adjacent packages and related PKG-03 deliverables with coordination expectations.
5. Enhanced quality requirements (QR-1 to QR-3) covering QA process, drawing review workflow, and CAD standards.
6. Expanded Standards section with governing standards, supplementary standards (TBD), and assumed applicable codes.
7. Detailed Verification section breaking down self-check, interdisciplinary check, and independent check activities with explicit ties to requirements.
8. Enhanced Documentation section describing drawing set organization structure and associated quality records.
9. Requirement traceability summary showing each requirement has corresponding verification in Procedure.

## Pass 3 Final Notes

**Pass 3 Reconciliation Completed:**
- All requirements (FR-1 to FR-4, PR-1 to PR-3, IF-1 to IF-2, QR-1 to QR-3) have corresponding verification in Procedure §Verification and implementation steps in Procedure §Steps.
- All requirements have rationale or context in Guidance (FR-2 → Guidance §P-2 environmental protection, FR-3 → Guidance §P-4 coordination-driven detailing, QR-3 → Guidance §P-3 consistent notation, etc.).
- All requirements reference Datasheet attributes or content (FR-4 → Datasheet §Attributes metadata, FR-1 → Datasheet §Construction comprehensive content, etc.).
- Requirement traceability summary (end of §Cross-Document Notes) confirms every requirement has verification checkpoint in Procedure.
- Entity coverage verified: All anticipated artifacts in §Scope (storm drainage, OWS, duct banks, trenchless crossings) appear in Datasheet §Construction, Guidance §Examples, and Procedure §Records.
- TBD items consistent with Datasheet: Drawing numbering system TBD (§FR-4, §Documentation), CAD standards TBD (§QR-3, §Standards), coordinate system TBD align with PKG-02 (§IF-1), design parameters TBD from ER and civil design brief (§PR-3).
- Terminology consistency verified: "storm drainage plans and profiles", "OWS layout", "duct bank plans", "trenchless crossing drawings", "OBJ-7 Environmental Protection", "interdisciplinary check", "independent check" used consistently with Datasheet, Guidance, and Procedure.

**Cross-Document Consistency Verification:**
- §Scope anticipated artifacts list matches Datasheet §Attributes "Typical Sheet Types" and Datasheet §Construction organization exactly.
- §FR-2 environmental protection features requirement implements OBJ-7 emphasis from Datasheet §Conditions, elaborated by Guidance §P-2, implemented via Procedure §5.
- §IF-1 coordination with adjacent packages (PKG-02, PKG-04, PKG-14, PKG-17) matches Datasheet §Attributes coordinate system alignment, Guidance §P-4 and §C-1, Procedure §2.1 and §7.2.
- §IF-2 linkage to related PKG-03 deliverables (DEL-03.02, DEL-03.03, DEL-03.04, DEL-03.05) matches Datasheet §Construction materials/performance references, Guidance examples references, Procedure §2.2 input data collection.
- §Verification design review process (self-check, interdisciplinary check, independent check) matches Procedure §7.1, §7.2, §7.3 exactly with detailed implementation steps.
- §Documentation drawing set organization matches Datasheet §Construction drawing organization structure and Procedure §3.2 drawing structure establishment.

**Document Maturity:**
- This Specification, along with Datasheet, Guidance, and Procedure, has completed three enrichment passes (Pass 1 initial generation, Pass 2 detailed requirements and verification enrichment, Pass 3 final reconciliation).
- All requirements are traceable to verification steps, implementation procedures, and design rationale.
- Document is ready for WORKING_ITEMS sessions where human engineer will validate requirements, populate TBD items from Employer's Requirements and design inputs, and refine performance criteria as design development proceeds.
- Specification provides complete, traceable, and enforceable requirements foundation for DEL-03.01 Underground Utilities Design Drawing Set production.
