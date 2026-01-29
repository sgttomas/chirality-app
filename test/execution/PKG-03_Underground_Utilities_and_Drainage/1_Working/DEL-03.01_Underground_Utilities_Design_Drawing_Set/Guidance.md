# Guidance: DEL-03.01 Underground Utilities Design Drawing Set

## Purpose

**Primary Purpose:**
- Support the development of underground utilities design drawings that establish the arrangement, geometry, and installation details for PKG-03 storm drainage, oil-water separator (OWS), duct bank, and trenchless crossing infrastructure (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:188).
- Provide interpretive guidance that complements the Specification requirements and Procedure workflow by clarifying how drawing details tie to performance outcomes, environmental protection objectives, and constructability constraints (Specification §Scope defines what; this Guidance explains why and how).

**Secondary Purpose:**
- Help drawing originators make informed decisions about detailing level, annotation clarity, coordination priorities, and trade-offs during drawing production (supports Procedure §Steps workflow where originators refine schematic arrangements into detailed plans).
- Clarify the intent behind Specification requirements (especially FR-2 environmental protection, IF-1 coordination, and QR-3 drawing conventions) so reviewers can assess whether drawings meet project objectives beyond mere compliance checking.
- Provide context for construction teams and QA/QC personnel who will use these drawings for excavation planning, installation verification, and as-built records (Datasheet §Conditions operational context describes downstream users).

## Principles

**P-1: Hydraulic Conveyance and Containment Controls**
- The storm drainage and OWS systems documented in this drawing set must demonstrate clear hydraulic conveyance paths and spill containment controls that satisfy the Employer's Requirements for civil utilities and environmental protection (Source: test/Volume_2_Part_2_Employers_Requirements.pdf; Specification §PR-1 sets hydraulic and structural performance expectations).
- **Rationale**: Storm drainage plan-and-profile sheets must show not only pipe geometry but also hydraulic grade lines, flow directions, and tie-in elevations to existing systems, enabling construction teams to verify constructability and operations teams to understand drainage flow paths for future maintenance (Datasheet §Construction describes plan-and-profile content; Specification §FR-1 requires comprehensive arrangement).
- **Application**: When detailing storm drainage sheets, include annotations for:
  - Design storm event and hydraulic capacity (values from DEL-03.03 Design Calculations per Specification §PR-1)
  - Invert elevations, pipe slopes, and hydraulic grade lines at key points (manhole locations, tie-ins, outfalls)
  - Flow direction arrows and catchment area boundaries (supports constructability verification per Specification §FR-3)
  - OWS inlet/outlet connections with capacity annotations (supports environmental protection per Specification §FR-2)
- **Cross-reference**: Specification §PR-1 hydraulic and structural performance; Datasheet §Construction storm drainage content; Procedure §Steps environmental protection annotation requirement.

**P-2: Environmental Protection Clarity (OBJ-7)**
- This deliverable supports **OBJ-7 Environmental Protection**; drawings must clearly capture spill containment features, drainage controls, and OWS instrumentation/capacity to demonstrate compliance with environmental protection requirements and facilitate regulatory inspection (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; Specification §FR-2 environmental protection features requirement).
- **Rationale**: Environmental protection features (OWS location, containment volumes, emergency overflow routes, instrumentation points) are critical for permitting, regulatory compliance, and spill response planning. Drawing clarity directly affects:
  - Construction inspection outcomes (inspectors need to verify OWS capacity, containment sump volumes, drainage flow paths match approved design)
  - Operations and maintenance planning (operations teams need clear as-built records of OWS layout, instrumentation, and drainage system configuration)
  - Emergency response (spill response teams need to understand containment boundaries and flow paths)
(Datasheet §Conditions operational context describes these downstream uses; Specification §FR-2 requires clear annotation of environmental protection features.)
- **Application**: When detailing OWS layout sheet and storm drainage plans, emphasize:
  - Containment boundary delineation (show which areas drain to OWS vs. direct storm drainage)
  - OWS capacity and treatment flow rate annotations (values from DEL-03.02 Technical Specification and DEL-03.04 Data Sheet Package per Specification §IF-2)
  - Instrumentation symbols and callouts (level sensors, flow meters, alarm points) with tag numbers matching control system documentation
  - Emergency overflow routes and discharge points with annotations referencing permit conditions or regulatory requirements
  - Sump locations and volumes with calculation references (DEL-03.03 per Specification §PR-1)
- **Cross-reference**: Specification §FR-2 environmental protection requirement; Datasheet §Conditions OBJ-7 environmental protection emphasis; Procedure §Steps environmental protection annotation requirement.

**P-3: Consistent Notation and Layer Structure**
- Maintain consistent notation (symbols, line types, text styles, annotation standards), layer structure (CAD layer naming, object organization), and metadata (title blocks, drawing numbers, revision codes) so the drawing set aligns with project CAD standards and document control practices (Specification §QR-3 CAD standards requirement; Datasheet §Attributes CAD Standard field).
- **Rationale**: Consistent notation and layer structure are essential for:
  - Constructability: Construction teams need to instantly recognize pipe types, utility types, crossing details without ambiguity.
  - Coordination: Adjacent disciplines (PKG-02 grading, PKG-04 paving, PKG-17 electrical) need to overlay drawings and identify conflicts; consistent layers enable automated clash detection.
  - As-built updates: Operations teams will mark up drawings during construction and create as-built records; consistent structure simplifies markup and reduces errors.
  - QA/QC efficiency: Reviewers can focus on design content rather than deciphering inconsistent notation (supports Procedure §Verification review workflow).
(Specification §QR-3 emphasizes consistency across sheets; Procedure §Steps includes CAD standard alignment check; Datasheet §Construction describes drawing organization requiring consistent structure.)
- **Application**: Before starting detailed drawing production:
  - Confirm project CAD standards are available (layer naming conventions, line weight standards, symbol libraries, text styles) – see Procedure §Prerequisites reference materials requirement.
  - Use standard symbol libraries for manholes, catch basins, valves, duct banks, pull boxes rather than creating custom symbols.
  - Apply consistent annotation styles: pipe size callouts in same format on all sheets, elevation callouts in consistent units and precision, leader line styles uniform across set.
  - Verify title block template matches project document control requirements (Specification §FR-4 drawing metadata requirement; Datasheet §Attributes metadata fields).
- **Cross-reference**: Specification §QR-3 CAD standards and drawing conventions; Datasheet §Attributes CAD Standard; Procedure §Steps CAD standard alignment check.

**P-4: Coordination-Driven Detailing**
- Prioritize coordination information (utility separations, crossing details, interface tie-ins with adjacent systems) in drawing details because underground utilities constructability depends on accurate coordination more than individual system performance (Specification §FR-3 coordination across underground networks; Specification §IF-1 coordination with adjacent packages).
- **Rationale**: Underground utilities construction involves multiple contractors, sequential installation, and limited rework opportunities once backfilled. Coordination failures (pipe conflicts, inadequate clearances, elevation mismatches) cause costly delays and rework. This drawing set must provide coordination information with sufficient clarity and precision for:
  - Excavation planning: Construction teams need to know where existing utilities are, where new utilities will be installed, and what clearances must be maintained.
  - Installation sequencing: Some utilities must be installed before others (e.g., duct banks before storm drainage in shared trenches); drawings should indicate sequencing constraints via notes or phasing annotations.
  - Clash avoidance: Reviewers from adjacent disciplines need to verify their systems don't conflict with PKG-03 utilities; consistent coordinate system and elevation datum are essential (Datasheet §Attributes specifies coordinate system alignment with PKG-02).
(Specification §IF-1 lists specific adjacent packages requiring coordination; Procedure §Verification interdisciplinary check implements coordination review.)
- **Application**: In plan views and cross-sections, show:
  - Utility separation dimensions (horizontal and vertical clearances) with code/standard references
  - Crossing details (over/under, casing pipes, protective slabs) with elevation callouts
  - Tie-in points to existing utilities or adjacent package systems with coordinate/elevation annotations
  - Trench shared by multiple utilities with installation sequence notes (e.g., "Install duct bank first, backfill to elevation X, then install storm drain")
  - Interface boundaries (e.g., "Coordinate tie-in elevation with PKG-02 site grading") to flag coordination dependencies
- **Cross-reference**: Specification §FR-3 coordination requirement; Specification §IF-1 adjacent package coordination; Datasheet §Attributes coordinate system alignment; Procedure §Verification interdisciplinary check.

## Considerations

**C-1: Upstream Design Data Availability**
- Confirm design data from adjacent disciplines (earthworks/grading from PKG-02, pavement sections from PKG-04, process piping tie-ins from PKG-14) are approved for design release before finalizing trench alignments, pipe invert elevations, and crossing details (Scope focus: contractor-only work, Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47; Specification §IF-1 coordination with adjacent packages; Procedure §Prerequisites and §Steps input data collection).
- **Impact**: If upstream data is not available or changes after drawing production, rework is required. Drawing production schedule must account for data availability dependencies (even though dependencies are tracked externally per `_DEPENDENCIES.md` NOT_TRACKED mode).
- **Mitigation**: Use placeholder annotations ("TBD – coordinate with PKG-02") and issue drawings for review/coordination before committing to final elevations; incorporate interdisciplinary review comments before finalizing (Procedure §Verification interdisciplinary check).

**C-2: Employer's Requirements Extraction**
- Incorporate regulatory requirements, design criteria, and material standards captured in Employer's Requirements Volume 2 Part 2 (Civil & Process Mechanical Works), particularly those affecting storm drainage design storm event, OWS discharge limits, pipe material selections, and trenchless crossing methods (Source: test/Volume_2_Part_2_Employers_Requirements.pdf; Specification §Standards governing standards; Specification §PR-1 and §PR-3 reference ER requirements).
- **Impact**: Drawing general notes, detail callouts, and material annotations must reference correct ER clauses to satisfy contract requirements and support QA/QC verification (Procedure §Verification independent check confirms compliance with ER).
- **Mitigation**: Extract relevant ER clauses early in design development (Procedure §Prerequisites lists ER as required reference material); compile list of applicable clauses and code sections for drawing general notes; include "See Employer's Requirements Volume 2 Part 2, Section X for [requirement]" annotations on detail sheets.

**C-3: Sheet Structure and Scope Boundaries**
- Structure sheets to clearly identify the anticipated artifacts listed in `_CONTEXT.md` (storm drainage plans/profiles, OWS layout, duct bank plans, trenchless crossings) to avoid scope creep, ensure Procedure verification steps capture each artifact, and maintain traceability to decomposition scope (Specification §Scope anticipated artifacts; Datasheet §Construction drawing organization; Procedure §Verification self-check confirms all anticipated artifacts present).
- **Impact**: If drawing set expands beyond anticipated artifacts (e.g., adding above-ground structures, buildings, process equipment details) without scope clarification, QA/QC review scope becomes unclear and deliverable acceptance criteria become ambiguous.
- **Mitigation**: Use cover sheet drawing index to explicitly list sheets and their correspondence to anticipated artifacts; include scope boundary notes (e.g., "Above-ground structures shown for reference only; see PKG-XX for detailed design"); confirm scope with discipline lead before adding non-standard sheets.

**C-4: Responsible Party and QA/QC Sign-offs**
- Highlight the designated responsible party (D&B Contractor per Datasheet §Identification) and the need for QA/QC sign-offs (self-check, interdisciplinary check, independent check per Specification §QR-1 and §QR-2) to support future installation and test records (DEL-03.05) and maintain contract accountability (Procedure §Verification describes review workflow; Specification §Verification details review activities).
- **Impact**: Missing or incomplete QA/QC sign-offs delay drawing issue, block downstream construction activities, and create audit trail gaps for contract compliance verification.
- **Mitigation**: Confirm project QA procedures early (Procedure §Prerequisites lists Quality Management Plan as required reference); populate title block review stamp blocks with clear originator/checker/approver roles; track review status via issue register (Specification §Documentation associated quality records).

**C-5: Construction Use and As-Built Record Intent**
- Drawing details must balance constructability clarity (dimensions, sections, connection details sufficient for construction teams) with as-built record intent (annotations and structure that support future markup and operations use) – see Datasheet §Conditions operational context for downstream users (Specification §FR-1 requires sufficient detail for construction teams; Datasheet §Construction describes drawing organization supporting operations use).
- **Impact**: Over-detailed drawings (every bolt, every weld) create clutter and slow construction use; under-detailed drawings leave ambiguities that cause RFIs and rework. As-built markup complexity increases if original drawing structure doesn't anticipate field changes (e.g., no space for as-built elevation annotations, no clear indication of which dimensions are critical vs. approximate).
- **Mitigation**: Use typical details for repetitive elements (standard pipe connections, standard trench sections) to reduce sheet clutter; show critical dimensions (invert elevations, tie-in coordinates, clearances) prominently; leave annotation space for as-built markups; include general note: "Contractor shall verify dimensions in field and provide as-built markup per DEL-03.05 requirements."

## Trade-offs

**T-1: Detailing Level – Constructability vs. Clarity**
- **Trade-off**: Balance detailing for constructability (detailed dimensions, sections, connection details) with clarity for future operations teams (simplified layouts, clear annotations, uncluttered sheets).
- **Competing Concerns**:
  - **More detail**: Construction teams need dimensions, materials, connection methods to install utilities correctly; insufficient detail causes RFIs, delays, and rework risk.
  - **Less detail**: Operations teams and future engineers need to understand system layout quickly; over-detailed drawings become difficult to interpret for maintenance planning or future modifications.
- **Decision Guidance**:
  - Use detail sheets for repetitive elements (standard pipe connections, standard trench sections, standard manhole installations) and reference them from plan sheets rather than duplicating details on every sheet.
  - Show critical dimensions and annotations on plan/profile sheets (invert elevations, pipe sizes, slopes, tie-in coordinates); relegate non-critical information (bolt sizes, gasket types, backfill lift thicknesses) to detail sheets or specification references (DEL-03.02).
  - Include simplified "key plan" or "overall layout" sheet showing entire underground utilities network without excessive detail to support operations use (Datasheet §Construction describes site utility plan as overall layout).
- **Status**: Decision TBD until design maturity; recommend balancing approach with detail sheets + simplified key plan (ASSUMPTION per typical civil drawing practice).
- **Cross-reference**: Datasheet §Conditions operational context; Specification §FR-1 sufficient detail requirement; Procedure §Steps schematic arrangements refinement.

**T-2: Storm Drainage Capacity vs. Trench Congestion**
- **Trade-off**: Evaluate storm drainage capacity (larger pipe sizes for hydraulic performance) versus pipeline routing efficiency and trench congestion (smaller pipes, shared trenches, utility coordination).
- **Competing Concerns**:
  - **Larger pipes**: Better hydraulic performance, more capacity margin for future expansion, reduced flood risk; but larger trenches, more excavation cost, more coordination conflicts with other utilities, longer construction duration.
  - **Smaller pipes**: Optimized hydraulic design with less excavation, easier coordination in shared trenches, lower material/installation cost; but less capacity margin, more sensitivity to design assumptions (design storm event, runoff coefficients), higher flood risk if assumptions are wrong.
- **Decision Guidance**:
  - Size pipes based on hydraulic calculations (DEL-03.03) using design storm event from Employer's Requirements (Specification §PR-1); avoid oversizing beyond reasonable margin (typically 10-20% capacity margin is sufficient).
  - Evaluate trench routing to minimize conflicts: route storm drainage in separate trenches from duct banks where feasible (duct banks typically shallower, can be installed first); coordinate crossing locations to minimize elevation conflicts.
  - Use trenchless crossings (jacking, boring) for road/rail/utility crossings to avoid excavation conflicts and traffic disruptions (Specification §Scope lists trenchless crossing drawings as anticipated artifact; Datasheet §Construction describes crossing details).
- **Status**: Decision deferred to hydraulic calculations (DEL-03.03) and coordination review (Procedure §Verification interdisciplinary check); drawing set documents selected pipe sizes and routing.
- **Cross-reference**: Specification §PR-1 hydraulic performance; P-4 coordination-driven detailing; Procedure §Verification interdisciplinary check.

**T-3: Trenchless Crossing Representation Detail**
- **Trade-off**: Choose between detailed trenchless crossing representation (boring profiles, casing details, annular space specifications, jacking forces, boring methods) and simpler alignment callouts (crossing location, casing size, carrier pipe size, reference to boring specification).
- **Competing Concerns**:
  - **More detail**: Boring contractors need detailed profiles, geotechnical conditions, casing specifications to bid and execute boring work; insufficient detail causes assumptions, contingencies, and claims risk.
  - **Less detail**: Avoids over-constraining boring contractor methods (allows contractor means-and-methods flexibility); reduces drawing complexity; defers detailed boring procedures to construction submittals.
- **Decision Guidance**:
  - Show alignment plan and profile with entry/exit pit locations, boring path, depth, casing size, carrier pipe size on drawing sheets (supports Specification §Scope trenchless crossing drawings artifact).
  - Reference detailed boring methods, jacking forces, annular grouting procedures to boring specification (DEL-03.02 Technical Specification) rather than duplicating on drawings (Datasheet §Construction notes materials/methods are in Technical Specification).
  - Include general note: "Boring contractor shall submit detailed boring procedures, equipment specifications, and QA/QC plan per DEL-03.02 for review before commencing work."
  - Show critical constraints on drawings: existing utilities to avoid, elevation limits (above/below existing infrastructure), casing-to-obstacle clearances.
- **Status**: Recommend simplified alignment drawings + reference to boring specification (ASSUMPTION: balance drawing clarity with contractor flexibility); detailed boring procedures in construction submittals.
- **Cross-reference**: Specification §Scope trenchless crossing drawings; Datasheet §Construction crossing details; Specification §IF-2 linkage to DEL-03.02 Technical Specification.

**T-4: Duct Bank Schedule Detail**
- **Trade-off**: Lean toward clarity for duct bank schedule tables when multiple utilities converge (electrical, communications, instrumentation conduits share duct bank trench) versus simplified representation (show trench outline only, reference conduit details to electrical package).
- **Competing Concerns**:
  - **Detailed schedule**: Civil contractors need to know trench dimensions, conduit quantities, concrete encasement details to excavate and construct duct banks; electrical contractors need to confirm conduit sizes/quantities match their design.
  - **Simplified representation**: Avoids duplicating electrical package information; reduces coordination burden if electrical design changes; keeps civil drawings focused on civil scope (excavation, trench, concrete encasement).
- **Decision Guidance**:
  - Show duct bank trench location, cross-section geometry, concrete encasement dimensions on civil drawings (Specification §Scope lists duct bank plans as anticipated artifact; Datasheet §Construction describes duct bank content).
  - Include conduit schedule table on civil drawings listing conduit sizes, quantities, and purposes (e.g., "6 × 4-inch PVC conduits for 600V power, 4 × 2-inch PVC conduits for communications") to enable civil contractor trench sizing and electrical contractor verification (supports Specification §FR-3 coordination across underground networks).
  - Reference electrical package (PKG-17) for conduit routing details, pull box internal configurations, and cable specifications (Specification §IF-1 coordination with PKG-17; avoids scope duplication).
  - Include coordination note: "Verify conduit quantities and sizes with PKG-17 Electrical before finalizing duct bank construction."
- **Status**: Recommend detailed duct bank schedule on civil drawings + reference to PKG-17 for electrical details (ASSUMPTION: civil contractor needs schedule for trench sizing; electrical contractor verifies against their design).
- **Cross-reference**: Specification §Scope duct bank plans; Specification §IF-1 coordination with PKG-17; P-4 coordination-driven detailing; Procedure §Verification interdisciplinary check.

## Examples

**Example 1: Storm Drainage Plan-and-Profile Sheet Structure**
- **Plan view** (upper portion of sheet): Shows pipe alignment in plan, manhole locations with station numbers, catchment area boundaries, flow direction arrows, tie-in to existing drainage system, coordinate grid.
- **Profile view** (lower portion of sheet): Shows ground surface profile, pipe invert elevations, slopes, hydraulic grade line, manhole depths, existing utility crossings, geotechnical layer interfaces (if significant).
- **Annotations**: Pipe size and material (e.g., "450mm Ø HDPE storm drain"), invert elevations at key points (manholes, tie-ins, crossings), slopes (e.g., "S = 0.5%"), hydraulic capacity reference (e.g., "See DEL-03.03 Calc Sheet X for hydraulic analysis"), coordination notes (e.g., "Coordinate invert elevation with PKG-02 site grading at STA 0+120").
- **Cross-reference**: Datasheet §Construction storm drainage content; Specification §FR-1 comprehensive arrangement; P-1 hydraulic conveyance and containment controls.

**Example 2: OWS Layout Sheet Clarity**
- **Plan view**: Shows OWS location relative to site features (buildings, tank pads, paved areas), inlet piping from drainage collection system, outlet piping to discharge point, access road, fence/enclosure, instrumentation points with tag numbers.
- **Section view**: Shows OWS internal configuration (inlet chamber, oil separation chamber, outlet chamber), weir elevations, sludge storage volume, instrumentation (level sensors, flow meters, alarm points), access hatches.
- **Annotations**: OWS capacity (e.g., "Treatment flow rate: 50 L/s, See DEL-03.04 OWS Data Sheet"), containment volume (e.g., "Spill containment volume: 25 m³, See DEL-03.03 Calc Sheet Y"), inlet/outlet pipe sizes and invert elevations, instrumentation tag numbers matching control system documentation (coordinate with PKG-18 Instrumentation per Specification §IF-1).
- **General note**: "OWS design and performance specifications per DEL-03.02 Technical Specification; OWS equipment data sheet per DEL-03.04 Data Sheet Package; installation and commissioning per DEL-03.05 Installation and Test Records."
- **Cross-reference**: Datasheet §Construction OWS layout content; Specification §FR-2 environmental protection features; P-2 environmental protection clarity (OBJ-7); Specification §IF-2 linkage to related PKG-03 deliverables.

**Example 3: Duct Bank Plan with Coordination Emphasis**
- **Plan view**: Shows duct bank trench alignment, pull box locations with ID numbers, conduit routing (curved sections, transition points), tie-in to building entry points, coordination with other utilities (storm drainage, process piping shown in dashed lines for reference).
- **Trench cross-section**: Shows trench width and depth, conduit arrangement (spacer pattern), concrete encasement dimensions, backfill layers, pavement restoration depth.
- **Conduit schedule table**: Lists conduit ID, size, material, quantity, purpose (e.g., "Conduit bank A: 6 × 4-inch PVC for 600V power, see PKG-17 for cable specifications").
- **Coordination notes**: "Maintain 300mm minimum horizontal separation from storm drain per [code reference]"; "Install duct bank before paving per PKG-04 construction sequence"; "Coordinate pull box locations with PKG-17 Electrical to match equipment layout."
- **Cross-reference**: Datasheet §Construction duct bank content; Specification §FR-3 coordination across underground networks; P-4 coordination-driven detailing; T-4 duct bank schedule detail.

**Example 4: Trenchless Crossing Alignment Drawing**
- **Plan view**: Shows crossing location (e.g., beneath existing road or rail track), entry pit and exit pit locations, boring path alignment (typically straight line, curved if required), existing surface features (road centerline, rail tracks, existing utilities).
- **Profile view**: Shows ground surface profile, boring path profile with elevations, depth below surface, existing underground utilities to avoid (shown with vertical clearances), geotechnical layer interfaces (rock, groundwater level), casing pipe depth and length.
- **Detail callouts**: Casing pipe size and material (e.g., "300mm Ø steel casing pipe"), carrier pipe size and material (e.g., "150mm Ø HDPE storm drain inside casing"), annular space grouting requirement (reference to DEL-03.02 Technical Specification), entry/exit pit dimensions.
- **General note**: "Boring contractor shall submit boring method, equipment specifications, jacking force calculations, and QA/QC procedures per DEL-03.02 for review before commencing work. Contractor shall verify locations of existing utilities via potholing before boring."
- **Cross-reference**: Datasheet §Construction trenchless crossing content; Specification §Scope trenchless crossing drawings; T-3 trenchless crossing representation detail; P-4 coordination-driven detailing.

## Cross-Document Notes

**Guidance → Specification:**
- P-1 hydraulic conveyance rationale → Specification §PR-1 hydraulic and structural performance requirement (explains why requirement exists and how to implement)
- P-2 environmental protection clarity → Specification §FR-2 environmental protection features requirement (elaborates OBJ-7 objective and drawing annotation expectations)
- P-3 consistent notation rationale → Specification §QR-3 CAD standards and drawing conventions requirement (explains why consistency matters for construction use and QA efficiency)
- P-4 coordination-driven detailing → Specification §FR-3 coordination across underground networks and §IF-1 coordination with adjacent packages (explains why coordination information is priority)
- T-1 to T-4 trade-offs → Specification requirements provide boundaries for trade-off decisions (e.g., T-1 detailing level supports §FR-1 sufficient detail requirement)

**Guidance → Datasheet:**
- P-1 hydraulic conveyance application → Datasheet §Construction storm drainage content (principles inform what content to include in drawings)
- P-2 environmental protection application → Datasheet §Conditions OBJ-7 emphasis and §Construction OWS layout content (principles explain why OWS details are critical)
- P-3 consistent notation application → Datasheet §Attributes CAD Standard and §Construction drawing organization (principles support metadata and structure requirements)
- Examples 1-4 → Datasheet §Construction describes drawing types that examples illustrate (examples provide concrete implementation of datasheet descriptions)

**Guidance → Procedure:**
- P-1 hydraulic conveyance application → Procedure §Steps environmental protection annotation requirement (principles guide what originators should annotate during drawing production)
- P-2 environmental protection clarity → Procedure §Steps environmental protection callouts and §Verification independent check (principles inform verification focus areas)
- P-3 consistent notation application → Procedure §Steps CAD standard alignment check and §Verification self-check CAD standard compliance (principles explain why CAD check is prerequisite step)
- C-1 to C-5 considerations → Procedure §Prerequisites and §Steps (considerations identify what inputs and workflow decisions are needed; Procedure implements workflow)
- T-1 to T-4 trade-offs → Procedure §Verification interdisciplinary check and independent check (trade-off decisions feed into review checkpoints where trade-offs are validated)

**Cross-Document Consistency Check:**
- All four anticipated artifacts (storm drainage, OWS layout, duct banks, trenchless crossings) have:
  - Datasheet §Construction description ✓
  - Specification §Scope listing ✓
  - Guidance examples (Examples 1-4) ✓
  - Procedure §Records documentation ✓
- Environmental protection (OBJ-7) emphasis appears in:
  - Guidance P-2 principle ✓
  - Specification §FR-2 requirement ✓
  - Datasheet §Conditions OBJ-7 reference ✓
  - Procedure §Steps environmental protection annotation ✓
- Coordination across disciplines appears in:
  - Guidance P-4 principle and C-1 consideration ✓
  - Specification §FR-3 and §IF-1 requirements ✓
  - Datasheet §Attributes coordinate system alignment ✓
  - Procedure §Verification interdisciplinary check ✓

## Pass 2 Enrichments

This Pass 2 revision adds:
1. Expanded Purpose section with primary and secondary purposes clarifying guidance intent and downstream users.
2. Detailed principles (P-1 to P-4) with rationale, application guidance, and cross-references to specific Specification requirements and Procedure steps.
3. Enhanced considerations (C-1 to C-5) identifying key decision points and impact/mitigation guidance.
4. Detailed trade-offs (T-1 to T-4) with competing concerns, decision guidance, and status/recommendations.
5. Concrete examples (Examples 1-4) illustrating how principles and considerations apply to each major anticipated artifact (storm drainage, OWS, duct banks, trenchless crossings).
6. Cross-document consistency check table confirming major themes (anticipated artifacts, OBJ-7, coordination) appear across all four documents.
7. Enhanced cross-document notes showing how Guidance principles/considerations/trade-offs inform Specification requirements, Datasheet content, and Procedure workflow.

## Pass 3 Final Notes

**Pass 3 Reconciliation Completed:**
- All principles (P-1 to P-4) have corresponding Specification requirements and Procedure implementation steps:
  - P-1 hydraulic conveyance → Specification §PR-1 + Procedure §4.1 storm drainage detailing
  - P-2 environmental protection (OBJ-7) → Specification §FR-2 + Procedure §5 environmental protection annotation
  - P-3 consistent notation → Specification §QR-3 + Procedure §3.3 CAD standard alignment + Procedure §7.1.4 CAD compliance check
  - P-4 coordination-driven detailing → Specification §FR-3 + §IF-1 + Procedure §2.1 input data collection + Procedure §7.2 interdisciplinary check
- All considerations (C-1 to C-5) have corresponding Procedure prerequisites or workflow steps:
  - C-1 upstream design data availability → Procedure §Prerequisites dependencies + Procedure §2.1 input data collection
  - C-2 Employer's Requirements extraction → Procedure §Prerequisites reference materials (ER Volume 2 Part 2) + Procedure §7.3.1 compliance check
  - C-3 sheet structure and scope boundaries → Procedure §1 scope review + Procedure §3.2 drawing structure establishment
  - C-4 responsible party and QA/QC sign-offs → Procedure §Prerequisites personnel requirements + Procedure §7 verification workflow
  - C-5 construction use and as-built record intent → Procedure §4 detailed design (balance detailing level) + Datasheet §Conditions operational context
- All trade-offs (T-1 to T-4) have decision guidance and status recommendations with corresponding Specification requirements boundaries:
  - T-1 detailing level → Specification §FR-1 sufficient detail requirement sets lower bound; Procedure §4 detailed design implements balance
  - T-2 storm drainage capacity vs trench congestion → Specification §PR-1 hydraulic performance requires sizing from calculations (DEL-03.03); Procedure §7.2 interdisciplinary check validates coordination
  - T-3 trenchless crossing representation → Specification §Scope requires trenchless crossing drawings; Specification §IF-2 links boring methods to DEL-03.02; Procedure §4.4 implements simplified alignment drawings + specification reference approach
  - T-4 duct bank schedule detail → Specification §FR-3 coordination requirement needs schedule for civil/electrical coordination; Specification §IF-1 requires PKG-17 coordination; Procedure §4.3 implements detailed schedule on civil drawings approach
- All examples (Examples 1-4) have corresponding Datasheet §Construction descriptions and Procedure §4 detailed design steps:
  - Example 1 storm drainage → Datasheet §Construction storm drainage content + Procedure §4.1
  - Example 2 OWS layout → Datasheet §Construction OWS layout content + Procedure §4.2
  - Example 3 duct bank plan → Datasheet §Construction duct bank content + Procedure §4.3
  - Example 4 trenchless crossing → Datasheet §Construction trenchless crossing content + Procedure §4.4

**Cross-Document Consistency Verification:**
- All four anticipated artifacts (storm drainage, OWS, duct banks, trenchless crossings) have principle/consideration/example coverage in Guidance, requirements coverage in Specification, description in Datasheet §Construction, and production steps in Procedure §4.
- OBJ-7 Environmental Protection theme appears consistently: Guidance §P-2 provides rationale → Specification §FR-2 requires clear annotation → Datasheet §Conditions emphasizes OBJ-7 mapping → Procedure §5 implements annotation requirements → Procedure §7.3.3 verifies compliance.
- Coordination with adjacent packages theme appears consistently: Guidance §P-4 and §C-1 explain why coordination is priority → Specification §IF-1 requires coordination with PKG-02/04/14/17 → Datasheet §Attributes specifies coordinate system alignment → Procedure §2.1 collects upstream data → Procedure §7.2 executes interdisciplinary check.
- CAD standards theme appears consistently: Guidance §P-3 explains why consistency matters → Specification §QR-3 requires compliance → Datasheet §Attributes lists CAD Standard field → Procedure §3.3 aligns with CAD standards → Procedure §7.1.4 checks compliance.
- Terminology consistency verified with other documents: "storm drainage plans and profiles", "OWS layout", "duct bank plans", "trenchless crossing drawings", "OBJ-7 Environmental Protection", "coordinate system alignment with PKG-02", "interdisciplinary check", "independent check" used consistently.

**Guidance Completeness Check:**
- Purpose section clarifies primary and secondary purposes (why this guidance exists and who uses it).
- Principles section (P-1 to P-4) provides rationale, application guidance, and cross-references for each major theme.
- Considerations section (C-1 to C-5) identifies key decision points with impact/mitigation guidance.
- Trade-offs section (T-1 to T-4) presents competing concerns, decision guidance, and recommended approach for each major design decision.
- Examples section (Examples 1-4) provides concrete implementation guidance for each anticipated artifact.
- Cross-document notes confirm how Guidance informs Specification requirements, Datasheet content, and Procedure workflow.

**Document Maturity:**
- This Guidance, along with Datasheet, Specification, and Procedure, has completed three enrichment passes (Pass 1 initial generation, Pass 2 detailed principles/considerations/trade-offs/examples enrichment, Pass 3 final reconciliation).
- Guidance provides complete interpretive context for Specification requirements, explains design intent, clarifies trade-off decisions, and provides concrete examples for each major anticipated artifact.
- Document is ready for WORKING_ITEMS sessions where human engineer will refine principles based on actual design decisions, validate trade-off recommendations against project constraints, and adapt examples to project-specific conventions.
- Guidance provides coherent, traceable, and practical decision support foundation for DEL-03.01 Underground Utilities Design Drawing Set production.
