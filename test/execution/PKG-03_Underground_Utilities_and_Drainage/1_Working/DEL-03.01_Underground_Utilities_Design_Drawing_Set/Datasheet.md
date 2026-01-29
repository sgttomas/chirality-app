# Datasheet: DEL-03.01 Underground Utilities Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-03.01 |
| Name | Underground Utilities Design Drawing Set |
| Package | PKG-03 Underground Utilities & Drainage |
| Discipline | Civil |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Drawing Number | To be issued per project numbering system (TBD – see Specification §FR-4 and §Documentation for metadata control requirements; Procedure §6 describes numbering assignment process) |
| Sheet Size | Per project drawing standards (TBD – typically ANSI D or ISO A1 for civil plan sheets) |
| Scale | Match feature size – typical 1:200 for site plans, 1:50 for details, 1:100 for profiles (TBD per project CAD standards; see Specification §QR-3) |
| CAD Standard | Project CAD convention (TBD – layer naming, line weights, annotation standards per Specification §Standards and §QR-3; Procedure §3.3 describes CAD standard alignment check; Guidance §P-3 explains consistent notation rationale) |
| Revision | 00 (initial issue for design development; see Procedure §6.2 for revision code setting) |
| Classification | Civil – Underground Utilities |
| Typical Sheet Types | Site plans, plan-and-profile sheets, detail sheets, OWS schematic, duct bank schedules (see Specification §Scope for anticipated artifact list; Procedure §3.2 describes drawing structure establishment) |
| Coordinate System | Project site coordinate system and vertical datum (TBD – to align with PKG-02 site grading deliverables per Specification §IF-1 and Procedure §2.1; Guidance §C-1 and §P-4 emphasize coordination importance) |

## Conditions

**Context & environmental expectations:**
- Defines the design arrangement and details for underground utilities that satisfy the Employer's Requirements in PKG-03, specifically storm drainage systems, oil-water separator (OWS) containment, electrical/communications duct banks, and trenchless utility crossings (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:188; Specification §Scope provides detailed artifact list).
- Designed to support storm drainage collection and conveyance, spill containment via OWS, and conduit routing within Fraser Surrey Terminal facility boundaries per Scope Focus (Contractor scope only, Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47; Specification §Scope exclusions clarifies what is NOT in drawing set).
- Deliverable supports **OBJ-7 Environmental Protection**; drawings must clearly capture spill containment features, drainage controls, and OWS instrumentation/capacity to demonstrate compliance with environmental protection requirements (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; elaborated in Guidance §P-2 environmental protection clarity principle; implemented via Procedure §5 environmental protection annotation step; verified via Specification §FR-2 requirement and Procedure §7.3.3 independent check).
- Design life, temperature range, seismic criteria, and hydraulic design storm event follow the civil design brief and Employer's Requirements civil standards; specific values remain TBD until Volume 2 Part 2 clauses are extracted (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD; see Specification §PR-3 design life and environmental conditions requirement; Procedure §Prerequisites lists civil design brief as required reference material; Guidance §C-2 addresses ER extraction consideration).
- Coordinate drawing metadata, revision process, and sheet organization with the Specification §FR-4 and §Documentation requirements to ensure drawing control aligns with project document management procedures (cross-reference: Specification §FR-4 drawing metadata requirement implemented via Procedure §6 metadata compilation and §8 issue into document control).

**Operational context:**
- Drawing set is used by construction teams for excavation planning, by QA/QC for installation verification (see Procedure §Verification and §7 for review workflow), and by operations for as-built records and maintenance planning (ASSUMPTION per typical civil drawing lifecycle; Guidance §C-5 construction use and as-built record intent consideration explains balancing constructability clarity with operations use).
- Environmental protection features (OWS location, drainage flow paths, containment volumes) are critical for permitting and regulatory compliance; drawing clarity directly affects construction inspection outcomes (rationale in Guidance §P-2 environmental protection clarity principle; Procedure §5 environmental protection annotation implements clear annotation requirements).

## Construction

**Materials & configuration focus:**
- Primary systems documented in the drawing set include:
  - **Storm drainage**: Pipe network plans showing alignment, sizing, invert elevations; plan-and-profile sheets with hydraulic grade lines (Specification §Scope lists "storm drainage plans and profiles"; Procedure §4.1 describes detailed storm drainage sheet development; Guidance §P-1 hydraulic conveyance principle and §Example 1 provide implementation guidance).
  - **Oil-Water Separator (OWS)**: Layout plan showing location, piping connections, sump details, instrumentation points; capacity and treatment flow requirements are specified in related deliverables (cross-reference: DEL-03.02 Technical Specification for OWS performance criteria per Specification §IF-2; DEL-03.04 Data Sheet Package for equipment specifications per Specification §PR-2; Procedure §4.2 describes OWS layout sheet development; Guidance §P-2 emphasizes environmental protection details for OBJ-7 compliance; Guidance §Example 2 provides OWS layout clarity guidance).
  - **Duct banks**: Plan views showing conduit routing, trench cross-sections, pull box locations, schedule tables listing conduit sizes/quantities; supports electrical and communications infrastructure (Specification §Scope lists "duct bank plans"; coordinate with PKG-17 Electrical per Specification §IF-1; Procedure §4.3 describes duct bank plan development including coordination with PKG-17; Guidance §T-4 duct bank schedule detail trade-off recommends detailed schedule on civil drawings; Guidance §Example 3 provides duct bank coordination guidance).
  - **Trenchless crossings**: Alignment drawings for bores/jacks beneath existing roads, rail tracks, or utilities; crossing details showing host pipe sizes, carrier pipe installations, annular space specifications (Specification §Scope lists "trenchless crossing drawings"; Procedure §4.4 describes trenchless crossing sheet development; Guidance §T-3 trenchless crossing representation detail trade-off recommends simplified alignment drawings + reference to boring specification; Guidance §Example 4 provides crossing alignment drawing guidance).
- Materials selection (pipe materials, backfill specifications, duct bank concrete encasement) is documented in DEL-03.02 Technical Specification and DEL-03.04 Data Sheet Package; this drawing set provides geometry and arrangement only (ASSUMPTION per typical drawing set / specification separation of concerns; see Specification §Scope exclusions and §IF-2 linkage to related deliverables; Procedure §2.2 describes collecting DEL-03.02 material specifications as design input).
- Trench details, bedding and backfill typical sections, and utility separation clearances are shown on detail sheets; these details implement the construction requirements from Employer's Requirements Volume 2 Part 2 civil standards (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, specific clauses TBD; see Procedure §Prerequisites which lists ER Volume 2 Part 2 as required reference material; Procedure §4.5 describes detail sheet development).

**Drawing organization (ASSUMPTION per typical civil drawing set structure; Guidance §C-3 emphasizes sheet structure to avoid scope creep):**
- Cover sheet: Drawing index, abbreviations, general notes, coordinate system / datum statement, applicable standards list (Procedure §3.2 establishes drawing structure; Procedure §2.4 describes documenting data sources in drawing general notes)
- Site utility plan: Overall layout showing all underground systems in plan view, tie-ins to existing infrastructure (Procedure §3.1 describes schematic site utility plan development)
- Storm drainage plan-and-profile sheets: One sheet per drainage branch or system segment, showing pipe alignment in plan and profile with invert elevations, slopes, hydraulic calculations reference (Procedure §4.1 describes detailed storm drainage plan-and-profile sheet development; Guidance §Example 1 provides sheet structure guidance)
- OWS layout sheet: Enlarged plan and sections showing separator location, inlet/outlet piping, access details, instrumentation (Procedure §4.2 describes OWS layout sheet development; Guidance §Example 2 provides layout clarity guidance)
- Duct bank plan and sections: Conduit routing in plan view, typical trench cross-sections, pull box details, conduit schedule table (Procedure §4.3 describes duct bank plan development; Guidance §Example 3 provides coordination emphasis guidance)
- Trenchless crossing sheets: Alignment plan and profile for each crossing, boring/jacking details, casing and carrier pipe specifications (Procedure §4.4 describes trenchless crossing sheet development; Guidance §Example 4 provides alignment drawing guidance)
- Detail sheets: Standard details for pipe connections, trench sections, manhole/catch basin installations, utility separations (Procedure §4.5 describes detail sheet development)

## References

- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:188 — scope, description, and anticipated artifacts for DEL-03.01.
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786 — OBJ-7 Environmental Protection mapping includes DEL-03.01 (storm drainage and OWS support environmental controls).
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47 — Scope Focus confirms contractor-only work scope, affects interface assumptions.
- test/Volume_2_Part_2_Employers_Requirements.pdf — Civil & Process Mechanical Works requirements for underground utilities, pipe materials, installation standards (details TBD, location references to be populated during design development; Specification §Standards lists this as governing standard; Procedure §Prerequisites lists as required reference material; Guidance §C-2 Employer's Requirements extraction consideration addresses extraction importance).
- test/Volume_2_Part_1_Employers_Requirements.pdf — General Requirements including Quality Management Plan, document control procedures, QA/QC requirements (Specification §QR-1 references for quality management compliance; Procedure §Prerequisites lists as required reference material).
- Specification.md — §Scope defines anticipated artifacts list; §FR-1 to §FR-4 functional requirements; §PR-1 to §PR-3 performance requirements; §IF-1 to §IF-2 interface requirements; §QR-1 to §QR-3 quality requirements; §Standards governing and supplementary standards; §Verification design review process; §Documentation drawing set organization and associated quality records.
- Guidance.md — §Purpose clarifies intent behind drawing set production; §P-1 to §P-4 principles (hydraulic conveyance, environmental protection clarity for OBJ-7, consistent notation, coordination-driven detailing); §C-1 to §C-5 considerations (upstream data availability, ER extraction, sheet structure and scope boundaries, QA sign-offs, construction use and as-built record intent); §T-1 to §T-4 trade-offs (detailing level, storm drainage capacity vs trench congestion, trenchless crossing representation, duct bank schedule detail); §Examples 1-4 (storm drainage plan-and-profile, OWS layout, duct bank plan with coordination, trenchless crossing alignment).
- Procedure.md — §Purpose production and QA purposes; §Prerequisites dependencies, reference materials, design intent understanding, personnel requirements; §Steps 1-8 (scope review, input data collection, schematic arrangements, detailed plans/profiles/sections, environmental protection annotation, metadata compilation, verification workflow, issue into document control); §Verification self-check, interdisciplinary check, independent check; §Records drawing deliverables and quality records.
- Package-level references in `execution/PKG-03_Underground_Utilities_and_Drainage/0_References/_REFERENCE_INDEX.md` (to be populated with project CAD standards, civil design criteria, applicable codes).
- DEL-03.02 Technical Specification — Material specifications, pipe performance requirements, OWS treatment criteria, boring specifications (referenced for materials per Specification §IF-2; Procedure §2.2 collects as design input).
- DEL-03.03 Design Calculations — Hydraulic calculations, pipe sizing, OWS capacity calculations, structural analysis (referenced for performance validation per Specification §PR-1 and §PR-2; Procedure §2.2 collects as design input; Procedure §7.3.2 validates performance against calculations).
- DEL-03.04 Data Sheet Package — Equipment data sheets for OWS, pumps, instrumentation (referenced for OWS capacity per Specification §PR-2; Procedure §4.2 OWS layout annotations reference data sheets).
- DEL-03.05 Installation and Test Records — Installation testing and commissioning (referenced for as-built records intent and QA verification per Specification §IF-2; Guidance §C-4 QA sign-offs support future installation records).

## Cross-Document Linkages

**Datasheet ↔ Specification:**
- Datasheet §Attributes "Drawing Number" TBD → Specification §FR-4 drawing metadata requirement → Specification §Documentation numbering format TBD
- Datasheet §Attributes "CAD Standard" TBD → Specification §QR-3 CAD standards and drawing conventions → Specification §Standards supplementary standards TBD
- Datasheet §Attributes "Typical Sheet Types" → Specification §Scope anticipated artifacts list (storm drainage, OWS, duct banks, trenchless crossings match exactly)
- Datasheet §Attributes "Coordinate System" TBD align with PKG-02 → Specification §IF-1 coordination with adjacent packages PKG-02 site grading coordination
- Datasheet §Construction storm drainage content → Specification §FR-1 comprehensive arrangement requirement → Specification §PR-1 hydraulic and structural performance requirement
- Datasheet §Construction OWS layout content → Specification §FR-2 environmental protection features requirement → Specification §PR-2 facility throughput and containment support
- Datasheet §Construction duct bank content → Specification §FR-3 coordination across underground networks requirement → Specification §IF-1 coordination with PKG-17 electrical
- Datasheet §Construction trenchless crossing content → Specification §Scope trenchless crossing drawings artifact → Specification §PR-1 structural performance for crossings
- Datasheet §Construction material systems → Specification §IF-2 linkage to DEL-03.02 Technical Specification and DEL-03.04 Data Sheet Package

**Datasheet ↔ Guidance:**
- Datasheet §Conditions OBJ-7 environmental protection emphasis → Guidance §P-2 environmental protection clarity principle (explains why OBJ-7 is critical for permitting and regulatory compliance)
- Datasheet §Construction OWS layout description → Guidance §P-2 environmental protection application guidance (containment boundaries, OWS capacity annotations, instrumentation, overflow routes) → Guidance §Example 2 OWS layout sheet clarity
- Datasheet §Construction drawing organization structure → Guidance §C-3 sheet structure and scope boundaries consideration (avoid scope creep, maintain traceability to decomposition)
- Datasheet §Conditions operational context (construction use, as-built records, operations maintenance) → Guidance §C-5 construction use and as-built record intent consideration (balance constructability clarity with operations use)
- Datasheet §Attributes "CAD Standard" → Guidance §P-3 consistent notation and layer structure principle (explains why consistency matters for construction use, coordination, as-built updates, QA efficiency)
- Datasheet §Construction storm drainage plan-and-profile content → Guidance §P-1 hydraulic conveyance and containment controls principle → Guidance §Example 1 storm drainage plan-and-profile sheet structure
- Datasheet §Construction duct bank schedule content → Guidance §P-4 coordination-driven detailing principle (duct banks support electrical infrastructure, coordination with PKG-17 is priority) → Guidance §T-4 duct bank schedule detail trade-off → Guidance §Example 3 duct bank plan with coordination emphasis
- Datasheet §Construction trenchless crossing details → Guidance §T-3 trenchless crossing representation detail trade-off → Guidance §Example 4 trenchless crossing alignment drawing

**Datasheet ↔ Procedure:**
- Datasheet §Attributes "Revision" 00 initial issue → Procedure §6.2 set initial revision code (describes revision code setting process)
- Datasheet §Attributes "Typical Sheet Types" → Procedure §3.2 establish drawing structure (describes how drawing structure is established matching anticipated artifacts)
- Datasheet §Attributes "Coordinate System" align with PKG-02 → Procedure §2.1 input data collection from PKG-02 site grading (describes collecting coordinate system definition and vertical datum from PKG-02)
- Datasheet §Construction storm drainage content → Procedure §4.1 develop detailed storm drainage plan-and-profile sheets (describes sheet development process with plan view, profile view, annotations)
- Datasheet §Construction OWS layout content → Procedure §4.2 develop detailed OWS layout sheet (describes plan view, section view, annotations including capacity and instrumentation)
- Datasheet §Construction duct bank content → Procedure §4.3 develop detailed duct bank plan and sections (describes plan view, cross-section, conduit schedule table, coordination notes with PKG-17)
- Datasheet §Construction trenchless crossing content → Procedure §4.4 develop detailed trenchless crossing sheets (describes plan view, profile view, detail callouts, general note for boring contractor submittals)
- Datasheet §Construction drawing organization structure → Procedure §3.2 drawing structure establishment matches Datasheet organization (cover sheet, site utility plan, plan-and-profiles, OWS sheet, duct bank sheets, crossing sheets, detail sheets)
- Datasheet §Conditions drawing control alignment → Procedure §6 metadata compilation + §8 issue into document control system (describes how drawing metadata is populated and drawings are issued per document control procedures)
- Datasheet §References lists quality records → Procedure §Records quality records section (self-check checklist, interdisciplinary review log, independent check review stamp, QA checklists, issue register entry, drawing review logs)

**Entity Coverage Check (all four documents):**
- Storm drainage plans/profiles: Datasheet §Construction ✓, Specification §Scope + §FR-1 + §PR-1 ✓, Guidance §P-1 + §Example 1 ✓, Procedure §4.1 + §Records ✓
- OWS layout: Datasheet §Construction ✓, Specification §Scope + §FR-2 + §PR-2 ✓, Guidance §P-2 + §Example 2 ✓, Procedure §4.2 + §Records ✓
- Duct bank plans: Datasheet §Construction ✓, Specification §Scope + §FR-3 + §IF-1 (PKG-17) ✓, Guidance §P-4 + §T-4 + §Example 3 ✓, Procedure §4.3 + §Records ✓
- Trenchless crossing drawings: Datasheet §Construction ✓, Specification §Scope + §PR-1 ✓, Guidance §T-3 + §Example 4 ✓, Procedure §4.4 + §Records ✓
- Environmental protection (OBJ-7): Datasheet §Conditions ✓, Specification §FR-2 + §PR-2 ✓, Guidance §P-2 ✓, Procedure §5 + §7.3.3 ✓
- Document metadata/numbering: Datasheet §Attributes ✓, Specification §FR-4 + §Documentation ✓, Guidance §P-3 (consistent notation) ✓, Procedure §6 + §7.1.5 ✓
- Coordination with adjacent packages (PKG-02, PKG-04, PKG-14, PKG-17): Datasheet §Attributes (PKG-02 coord system) ✓, Specification §FR-3 + §IF-1 ✓, Guidance §P-4 + §C-1 ✓, Procedure §2.1 + §7.2 ✓
- CAD standards: Datasheet §Attributes ✓, Specification §QR-3 ✓, Guidance §P-3 ✓, Procedure §3.3 + §7.1.4 ✓

**TBD Items Cross-Check:**
- Drawing numbering system: Datasheet §Attributes TBD → Specification §FR-4 TBD → Specification §Documentation TBD pending document control register → Procedure §6.1 obtain numbers from document control register
- Sheet size: Datasheet §Attributes TBD (typically ANSI D or ISO A1) → Specification §Documentation TBD per project drawing standards → Procedure §Prerequisites lists project CAD standards as required reference
- Scale: Datasheet §Attributes TBD (typical scales noted) → Specification §Documentation TBD per project drawing standards → Procedure §Prerequisites lists project CAD standards as required reference
- CAD Standard: Datasheet §Attributes TBD → Specification §QR-3 TBD → Specification §Standards supplementary standards TBD → Procedure §Prerequisites lists project CAD standards as required reference
- Coordinate System: Datasheet §Attributes TBD align with PKG-02 → Specification §IF-1 coordinate with PKG-02 → Procedure §2.1 collect from PKG-02 (upstream input dependency)
- Design parameters (design life, seismic, temperature, design storm): Datasheet §Conditions TBD from ER Volume 2 Part 2 → Specification §PR-3 TBD from ER and civil design brief → Procedure §Prerequisites lists ER Volume 2 Part 2 and civil design brief as required references → Guidance §C-2 ER extraction consideration addresses extraction importance

(All TBD items have clear path to resolution via Procedure prerequisites and input data collection; TBD status is consistent across documents.)

## Pass 3 Final Notes

**Pass 3 Reconciliation Completed:**
- All cross-document linkages verified bidirectional: Datasheet references to Specification/Guidance/Procedure have corresponding back-references in those documents.
- Entity coverage check confirms all major anticipated artifacts (storm drainage, OWS, duct banks, trenchless crossings) and themes (OBJ-7 environmental protection, coordination with adjacent packages, CAD standards, document metadata) appear consistently across all four documents.
- TBD items cross-check confirms all TBD items are consistent across documents and have clear resolution path via Procedure prerequisites or input data collection steps.
- Terminology consistency verified: "storm drainage", "OWS layout", "duct bank plans", "trenchless crossing drawings", "OBJ-7 Environmental Protection", "coordinate system alignment with PKG-02", "CAD standards", "interdisciplinary check", "independent check" used consistently across all four documents.
- No conflicts detected between documents; all requirements, rationale, and implementation steps align.

**Document Maturity:**
- This Datasheet, along with Specification, Guidance, and Procedure, has completed three enrichment passes (Pass 1 initial generation, Pass 2 cross-reference and detail enrichment, Pass 3 final reconciliation).
- Documents are ready for WORKING_ITEMS sessions where human engineer will refine, validate, and populate TBD items as design development proceeds.
- All four documents provide coherent, traceable, and consistent foundation for DEL-03.01 Underground Utilities Design Drawing Set production.
