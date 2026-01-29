# Procedure: DEL-03.01 Underground Utilities Design Drawing Set

## Purpose

**Production Purpose:**
- Produce and control the civil drawing deliverable that establishes the underground utilities arrangement, geometry, and installation details for storm drainage infrastructure, oil-water separator (OWS) layout, duct banks, and trenchless crossings for PKG-03 (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:188).
- Implement the workflow that transforms design inputs (calculations from DEL-03.03, specifications from DEL-03.02, coordination data from adjacent packages) into verified, QA-approved drawing sheets ready for construction use (Specification §Scope defines what drawings contain; this Procedure defines how to produce them).

**Quality Assurance Purpose:**
- Execute QA/QC review process (self-check, interdisciplinary check, independent check) that verifies compliance with Specification requirements, validates coordination with adjacent disciplines, and confirms drawing set completeness before issue (Specification §Verification and §QR-1 require QA compliance; this Procedure implements review workflow).
- Generate quality records (drawing review logs, QA checklists, issue registers) that provide audit trail for contract compliance and support future installation verification (DEL-03.05) and operations use (Specification §Documentation lists associated quality records; this Procedure defines how records are created and retained).

## Prerequisites

**Dependencies:**
- Dependencies are coordinated externally by humans (see `_DEPENDENCIES.md`); confirm inputs from adjacent packages are approved for design release before starting detailed drawing production (Source: Specification §IF-1 coordination with adjacent packages; Guidance §C-1 upstream design data availability consideration).
- Required upstream inputs include:
  - **PKG-02 Site Grading**: Finished grade elevations, site grading plans, drainage flow directions, coordinate system and vertical datum definitions (Specification §IF-1 and Datasheet §Attributes coordinate system alignment requirement).
  - **PKG-04 Pavement and Surfacing**: Pavement sections, drainage inlet locations, trench restoration requirements (Specification §IF-1 coordination requirement).
  - **PKG-14 Process Piping**: Process piping alignments, crossing locations, utility separation requirements (Specification §IF-1 coordination requirement).
  - **PKG-17 Electrical Power Distribution**: Duct bank conduit routing, pull box locations, conduit sizes/quantities (Specification §IF-1 coordination requirement; Datasheet §Construction duct bank content supports electrical infrastructure).
  - **DEL-03.03 Design Calculations**: Hydraulic calculations, pipe sizing, OWS capacity calculations, structural analysis for trenchless crossings (Specification §PR-1 hydraulic and structural performance; Guidance §P-1 hydraulic conveyance principle).
  - **DEL-03.02 Technical Specification**: Material specifications, pipe performance requirements, OWS treatment criteria, boring specifications (Specification §IF-2 linkage to related deliverables; Datasheet §Construction notes materials are in Technical Specification).

**Reference Materials:**
- **Employer's Requirements Volume 2 Part 2 (Civil & Process Mechanical Works)**: Civil utility design criteria, pipe material standards, installation methods, environmental protection requirements (Source: Specification §Standards governing standards; Guidance §C-2 emphasizes ER extraction for drawing general notes).
- **Employer's Requirements Volume 2 Part 1 (General Requirements)**: Project Quality Management Plan, document control procedures, QA/QC requirements, drawing numbering scheme (Source: Specification §QR-1 quality management compliance; test/Volume_2_Part_1_Employers_Requirements.pdf).
- **Project CAD Standards**: Layer naming conventions, line weight standards, symbol libraries, text styles, annotation standards, title block template (Source: Specification §QR-3 CAD standards requirement; Datasheet §Attributes CAD Standard; Guidance §P-3 consistent notation principle).
- **Civil Design Brief**: Design life, seismic design category, temperature range, design storm event, other environmental design parameters (Source: Specification §PR-3 design life and environmental conditions; Datasheet §Conditions lists design parameters TBD from civil design brief).
- **Package-level reference index**: `execution/PKG-03_Underground_Utilities_and_Drainage/0_References/_REFERENCE_INDEX.md` (to be populated with project-specific codes, standards, and reference documents).

**Design Intent Understanding:**
- Review Specification requirements (§Scope, §Requirements, §Standards, §Verification) to understand functional, performance, interface, and quality expectations for the drawing set (Specification provides "what"; this Procedure provides "how").
- Review Guidance principles, considerations, and trade-offs (§Principles, §Considerations, §Trade-offs) to understand why requirements exist and how to make informed detailing decisions (Guidance §Purpose clarifies intent behind requirements; helps originator prioritize when making drawing production decisions).
- Understand downstream use: Construction teams will use drawings for excavation planning and installation; operations teams will use drawings for maintenance planning and as-built records; QA/QC will use drawings for inspection verification (Datasheet §Conditions operational context describes downstream users).

**Personnel Requirements:**
- **Originator**: Civil discipline designer with underground utilities design experience; responsible for producing drawings per this Procedure workflow (ASSUMPTION per typical QA process and Quality Management Plan in Volume 2 Part 1).
- **Checker**: Civil discipline senior engineer or lead; responsible for interdisciplinary coordination review and technical check before independent review.
- **Approver/Independent Reviewer**: Discipline lead or designated independent reviewer; responsible for final compliance check and approval signature before issue.
- **Adjacent Discipline Reviewers**: Representatives from PKG-02, PKG-04, PKG-14, PKG-17 for interdisciplinary coordination review (Specification §IF-1 coordination requirement; Verification section interdisciplinary check step).

## Steps

### Step 1: Scope and Objectives Review

**Objective**: Confirm drawing set scope, anticipated artifacts, and project objectives before starting production.

**Actions**:
1.1. Read decomposition entry for DEL-03.01 (test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:188) to confirm scope description and anticipated artifacts list (storm drainage plans/profiles, OWS layout, duct bank plans, trenchless crossing drawings).

1.2. Review Specification §Scope and §Requirements to confirm functional, performance, interface, and quality expectations (Specification §FR-1 to FR-4, §PR-1 to PR-3, §IF-1 to IF-2, §QR-1 to QR-3 define drawing set requirements; this step ensures originator understands what must be delivered).

1.3. Confirm **OBJ-7 Environmental Protection** objective emphasis: Storm drainage and OWS support environmental controls; drawings must clearly capture spill containment features, drainage flow paths, and OWS instrumentation (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; Specification §FR-2 environmental protection features requirement; Guidance §P-2 environmental protection clarity principle).

1.4. Identify scope exclusions: Materials specifications are in DEL-03.02, hydraulic calculations are in DEL-03.03, installation testing is in DEL-03.05, above-ground structures are outside PKG-03 scope (Specification §Scope exclusions; prevents scope creep per Guidance §C-3).

**Verification**: Scope review checklist confirms originator has read decomposition entry, Specification requirements, and Guidance principles; checklist signed before proceeding to Step 2.

**Output**: Scope confirmation documented in project files; originator understands what drawings to produce and why.

---

### Step 2: Input Data Collection and Coordination

**Objective**: Collect design inputs from upstream packages and related deliverables; confirm data is approved for design release.

**Actions**:
2.1. Request and collect upstream design data:
- **PKG-02 Site Grading**: Site grading plans, finished grade elevations, drainage flow directions, coordinate system definition, vertical datum (Specification §IF-1 coordination with PKG-02; Datasheet §Attributes coordinate system alignment; Guidance §C-1 upstream data availability consideration).
- **PKG-04 Pavement**: Pavement sections, drainage inlet locations, trench restoration requirements (Specification §IF-1 coordination with PKG-04).
- **PKG-14 Process Piping**: Process piping alignments, crossing locations, utility separation requirements (Specification §IF-1 coordination with PKG-14).
- **PKG-17 Electrical**: Duct bank conduit routing, pull box locations, conduit sizes/quantities (Specification §IF-1 coordination with PKG-17; Datasheet §Construction duct bank schedule requires conduit quantities from electrical package).

2.2. Collect related PKG-03 deliverable outputs:
- **DEL-03.03 Design Calculations**: Hydraulic calculations for storm drainage (design storm event, pipe sizes, slopes, hydraulic grade lines), OWS capacity calculations, structural analysis for trenchless crossings (Specification §PR-1 hydraulic and structural performance; Guidance §P-1 hydraulic conveyance principle requires calculation references).
- **DEL-03.02 Technical Specification**: Material specifications (pipe materials, backfill specifications, concrete for duct bank encasement), OWS treatment criteria, boring specifications for trenchless crossings (Specification §IF-2 linkage to related deliverables; Datasheet §Construction notes materials are in Technical Specification).

2.3. Confirm data approval status: Verify that upstream package deliverables and related PKG-03 deliverables are approved for design release (typically "Issued for Design" or "Approved" status per project document control procedures; prevents rework if inputs change after drawing production per Guidance §C-1 mitigation).

2.4. Document data sources in drawing general notes and reference section: List calculation reports, specification documents, coordination drawings used as design basis (supports traceability per Specification §Verification dimensional and coordination verification; enables future reviewers to trace design decisions).

**Verification**: Input data collection checklist confirms all required inputs are collected and approved; checklist includes input document IDs, revision numbers, and approval status.

**Output**: Design input package assembled and documented; ready for drawing production.

---

### Step 3: Schematic Arrangements Development

**Objective**: Create initial schematic layouts for storm drainage, OWS, duct banks, and trenchless crossings; establish drawing structure and coordination approach.

**Actions**:
3.1. Develop schematic site utility plan (overall layout showing all underground systems):
- Plot storm drainage network alignment (pipe routes, manhole locations, catchment areas, outfall tie-ins) using hydraulic calculation results from DEL-03.03.
- Plot OWS location, inlet/outlet piping connections, access road, and containment boundary.
- Plot duct bank trench alignment, pull box locations, building entry points using electrical coordination data from PKG-17.
- Plot trenchless crossing locations (beneath roads, rail tracks, existing utilities) with entry/exit pit locations.
- Overlay existing utilities and site features (buildings, tank pads, paved areas) for coordination context.

3.2. Establish drawing structure per anticipated artifacts list (Specification §Scope; Datasheet §Construction drawing organization):
- Cover sheet: Drawing index, abbreviations, general notes, coordinate system/datum statement, applicable standards list
- Site utility plan: Overall layout sheet (schematic level, not detailed)
- Storm drainage plan-and-profile sheets: One sheet per drainage branch or system segment
- OWS layout sheet: Enlarged plan and sections
- Duct bank plan and sections: Conduit routing plans, trench cross-sections, conduit schedule table
- Trenchless crossing sheets: Alignment plans/profiles for each crossing
- Detail sheets: Standard details for pipe connections, trench sections, manhole/catch basin installations, utility separations

3.3. Align symbol usage, layering, and annotation conventions with project CAD standard:
- Use standard symbol libraries for manholes, catch basins, valves, duct banks, pull boxes (Specification §QR-3 CAD standards; Guidance §P-3 consistent notation principle; prevents custom symbols that cause confusion).
- Establish layer naming per project CAD conventions (e.g., "C-STRM-PIPE" for storm drainage pipes, "C-DUCT-BANK" for duct banks) to support coordination with adjacent disciplines and automated clash detection.
- Define annotation styles: Pipe size callouts format (e.g., "450mm Ø HDPE"), elevation callout format (e.g., "INV. EL. 10.25m"), leader line styles, text heights.

3.4. Conduct coordination schematic review with adjacent discipline leads (informal review at schematic stage to catch major conflicts early):
- Share schematic site utility plan with PKG-02 (grading), PKG-04 (paving), PKG-14 (process piping), PKG-17 (electrical) for preliminary coordination feedback.
- Identify and resolve major conflicts (pipe crossings, trench congestion, elevation mismatches) before proceeding to detailed design (Guidance §P-4 coordination-driven detailing emphasizes early coordination; prevents costly rework at detailed stage).

**Verification**: Schematic review meeting minutes document coordination feedback and resolution of major conflicts; discipline lead approves schematic arrangements before proceeding to Step 4.

**Output**: Schematic site utility plan and drawing structure established; CAD standards alignment confirmed; ready for detailed design.

---

### Step 4: Detailed Plans, Profiles, and Sections

**Objective**: Refine schematic arrangements into detailed plans, profiles, and sections with dimensions, elevations, annotations, and coordination details.

**Actions**:
4.1. Develop detailed storm drainage plan-and-profile sheets:
- **Plan view**: Pipe alignment with station numbers, manhole locations with IDs, catchment area boundaries, flow direction arrows, tie-in to existing drainage system, coordinate grid, utility crossing locations.
- **Profile view**: Ground surface profile, pipe invert elevations at manholes and key points, slopes (e.g., "S = 0.5%"), hydraulic grade line (from DEL-03.03 calculations), existing utility crossings with vertical clearances, geotechnical layer interfaces (if significant, e.g., rock depth).
- **Annotations**: Pipe size and material (e.g., "450mm Ø HDPE storm drain"), invert elevations (e.g., "INV. EL. 10.25m at MH-1"), hydraulic capacity reference (e.g., "See DEL-03.03 Calc Sheet X for design flow Q = 0.85 m³/s"), coordination notes (e.g., "Coordinate invert elevation with PKG-02 site grading at STA 0+120").
- **Cross-reference**: Guidance §Example 1 storm drainage plan-and-profile structure; Specification §FR-1 comprehensive arrangement and §PR-1 hydraulic performance; Datasheet §Construction storm drainage content.

4.2. Develop detailed OWS layout sheet:
- **Plan view**: OWS location with coordinates, inlet piping from drainage collection system with pipe sizes and invert elevations, outlet piping to discharge point, access road, fence/enclosure, instrumentation points with tag numbers (coordinate with PKG-18 Instrumentation if applicable).
- **Section view**: OWS internal configuration (inlet chamber, oil separation chamber, outlet chamber), weir elevations, sludge storage volume annotation, instrumentation symbols (level sensors, flow meters, alarm points) with tag numbers, access hatches.
- **Annotations**: OWS capacity (e.g., "Treatment flow rate: 50 L/s, See DEL-03.04 OWS Data Sheet for equipment specifications"), containment volume (e.g., "Spill containment volume: 25 m³, See DEL-03.03 Calc Sheet Y for sizing basis"), inlet/outlet pipe sizes and invert elevations, instrumentation tag numbers matching control system documentation.
- **General note**: "OWS design and performance specifications per DEL-03.02 §[section]; OWS equipment data sheet per DEL-03.04; installation and commissioning per DEL-03.05." (Specification §IF-2 linkage to related deliverables; Guidance §Example 2 OWS layout clarity.)
- **Cross-reference**: Guidance §Example 2 OWS layout sheet; Specification §FR-2 environmental protection features and §PR-2 facility throughput and containment support; Datasheet §Construction OWS layout content; Guidance §P-2 environmental protection clarity (OBJ-7).

4.3. Develop detailed duct bank plan and sections:
- **Plan view**: Duct bank trench alignment with station numbers, pull box locations with IDs, conduit routing (show curved sections and transition points clearly), tie-in to building entry points, coordination with other utilities (storm drainage and process piping shown in dashed lines for reference with separation dimensions annotated).
- **Trench cross-section**: Trench width and depth dimensions, conduit arrangement (spacer pattern or configuration), concrete encasement dimensions and reinforcement (if applicable), backfill layers with material callouts, pavement restoration depth.
- **Conduit schedule table**: List conduit bank ID, conduit size, material (e.g., "4-inch PVC"), quantity, purpose (e.g., "600V power" or "communications"), reference to PKG-17 for cable specifications.
- **Coordination notes**: "Maintain 300mm minimum horizontal separation from storm drain per [code reference]"; "Install duct bank before paving per PKG-04 construction sequence"; "Coordinate pull box locations with PKG-17 Electrical to match equipment layout and cable routing."
- **Cross-reference**: Guidance §Example 3 duct bank plan with coordination emphasis; Specification §FR-3 coordination across underground networks and §IF-1 coordination with PKG-17; Datasheet §Construction duct bank content; Guidance §T-4 duct bank schedule detail trade-off (recommends detailed schedule on civil drawings + reference to PKG-17).

4.4. Develop detailed trenchless crossing sheets:
- **Plan view**: Crossing location (e.g., beneath existing road or rail track) with reference to site features, entry pit and exit pit locations with coordinates, boring path alignment (show as straight line unless curved bore required), existing surface features (road centerline, rail tracks, existing utilities shown for reference).
- **Profile view**: Ground surface profile, boring path profile with elevations and depths below surface, existing underground utilities to avoid (shown with vertical clearances annotated), geotechnical layer interfaces (rock depth, groundwater level if known from geotechnical report), casing pipe depth and length.
- **Detail callouts**: Casing pipe size and material (e.g., "300mm Ø steel casing pipe"), carrier pipe size and material (e.g., "150mm Ø HDPE storm drain inside casing"), annular space grouting requirement (reference to DEL-03.02 §[section] for grouting specification), entry/exit pit dimensions (plan and section views).
- **General note**: "Boring contractor shall submit detailed boring method, equipment specifications, jacking force calculations, and QA/QC procedures per DEL-03.02 for review before commencing work. Contractor shall verify locations of existing utilities via potholing before boring to avoid conflicts."
- **Cross-reference**: Guidance §Example 4 trenchless crossing alignment drawing; Specification §Scope trenchless crossing drawings; Datasheet §Construction trenchless crossing content; Guidance §T-3 trenchless crossing representation detail (recommends simplified alignment drawings + reference to boring specification).

4.5. Develop detail sheets:
- Standard pipe connection details (e.g., manhole-to-pipe connections, pipe-to-pipe joints, expansion joints)
- Standard trench sections (typical backfill, bedding, and compaction requirements by pipe type and depth)
- Manhole and catch basin installation details (base slab, wall construction, frame and cover, access ladder, benching)
- Utility separation details (horizontal and vertical clearance requirements with code references, protective slabs for crossing situations)
- Duct bank concrete encasement details (formwork, reinforcement, joint details, pull box connections)

**Verification**: Originator self-check (Step 5) confirms dimensions, elevations, annotations, and coordination details are complete and accurate before interdisciplinary review.

**Output**: Detailed drawing sheets ready for self-check and review workflow.

---

### Step 5: Environmental Protection Feature Annotation

**Objective**: Ensure environmental protection features (OWS, containment, drainage controls) are clearly annotated to support **OBJ-7 Environmental Protection** compliance and regulatory inspection.

**Actions**:
5.1. Annotate containment boundary delineation on site utility plan and storm drainage sheets:
- Show which areas drain to OWS (spill containment catchment) vs. direct storm drainage (clean runoff) using boundary lines, hatching patterns, or color coding.
- Label catchment areas with designations (e.g., "Zone A – Process area runoff to OWS", "Zone B – Roof runoff to storm drainage").

5.2. Annotate OWS capacity and treatment flow rate on OWS layout sheet:
- Include capacity annotation (e.g., "Treatment flow rate: 50 L/s") with reference to DEL-03.04 Data Sheet for equipment specifications.
- Include containment volume annotation (e.g., "Spill containment volume: 25 m³") with reference to DEL-03.03 Calculations for sizing basis.
- Show instrumentation with clear tag numbers matching control system documentation (coordinate with PKG-18 Instrumentation if applicable).

5.3. Annotate emergency overflow routes and discharge points:
- Show emergency overflow piping from OWS to storm drainage or other approved discharge point (per environmental permit conditions).
- Annotate discharge point location, elevation, and permit reference (e.g., "Discharge to municipal storm system per [permit ID]").

5.4. Annotate sump locations and volumes:
- Show sump locations on storm drainage plan with volume callouts (e.g., "Sump volume: 5 m³, See DEL-03.03 Calc Sheet Z").
- Reference calculation sheet that validates sump sizing for anticipated spill volumes or rainfall collection.

5.5. Include general note emphasizing environmental protection compliance:
- "Storm drainage and OWS systems designed to support environmental protection per OBJ-7 (test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786). Containment and treatment systems shall be installed and commissioned per DEL-03.05 before facility operations commence."

**Verification**: Environmental protection annotation checklist confirms all required features (containment boundaries, OWS capacity, instrumentation, overflow routes, sumps) are clearly shown and annotated; checklist reviewed during independent check (Step 7.3).

**Output**: Environmental protection features clearly annotated; drawings ready to support regulatory inspection and OBJ-7 compliance verification.

**Cross-reference**: Specification §FR-2 environmental protection features; Guidance §P-2 environmental protection clarity; Datasheet §Conditions OBJ-7 emphasis.

---

### Step 6: Metadata and Revision History Compilation

**Objective**: Populate drawing title blocks with metadata (drawing numbers, revisions, originator/checker/approver names, issue dates) and compile revision history per document control procedures.

**Actions**:
6.1. Assign drawing numbers per project numbering system:
- Obtain drawing numbers from project document control register or coordinator.
- Populate title block "Drawing Number" field (Datasheet §Attributes notes numbering system TBD; Specification §FR-4 drawing metadata requirement).

6.2. Set initial revision code:
- Initial issue revision is "00" per Datasheet §Attributes.
- Populate title block "Revision" field with "00" and issue description "Issued for Review" or "Issued for Construction" per project conventions (Specification §QR-2 drawing status codes).

6.3. Populate title block originator/checker/approver fields:
- Originator: Name and signature of civil designer who produced drawings
- Checker: Name and signature field (to be completed after interdisciplinary check, Step 7.2)
- Approver: Name and signature field (to be completed after independent check, Step 7.3)

6.4. Compile revision history:
- Populate title block revision history table with revision number, date, description, originator/checker/approver initials.
- Initial issue: "Rev 00, [Date], Issued for Review, [Initials]"
- Subsequent revisions (if issued after review comments): "Rev 01, [Date], Issued for Construction incorporating review comments, [Initials]"

6.5. Confirm title block template matches project document control requirements:
- Verify title block includes all required fields: Project name, deliverable ID (DEL-03.01), drawing title, drawing number, revision, issue date, originator, checker, approver, project location, coordinate system/datum statement, scale, sheet size.
- Verify title block format matches project template (Specification §QR-3 CAD standards; Guidance §P-3 consistent notation).

**Verification**: Metadata completeness checklist confirms all title block fields are populated (except checker/approver signatures pending review); checklist reviewed during self-check (Step 7.1) and QA review (Step 7.3).

**Output**: Drawing title blocks populated with metadata; ready for review workflow.

**Cross-reference**: Specification §FR-4 drawing metadata and document control; Specification §QR-2 drawing review and approval process; Datasheet §Attributes metadata fields.

---

### Step 7: Verification and QA/QC Review

**Objective**: Execute self-check, interdisciplinary check, and independent check to verify compliance with Specification requirements and validate drawing set completeness and accuracy.

#### Step 7.1: Self-Check (Originator Review)

**Actions**:
7.1.1. **Completeness check**: Confirm all anticipated artifacts (Specification §Scope list) are present:
- Storm drainage plans and profiles ✓
- OWS layout ✓
- Duct bank plans ✓
- Trenchless crossing drawings ✓
- Detail sheets ✓

7.1.2. **Dimensional accuracy check**: Verify dimensions, elevations, coordinates match design inputs:
- Storm drainage invert elevations match hydraulic calculations (DEL-03.03)
- OWS location coordinates match site plan
- Duct bank trench dimensions match cross-section details
- Trenchless crossing elevations match boring profile calculations
- Coordinate system and vertical datum match PKG-02 site grading (Specification §IF-1; Datasheet §Attributes coordinate system alignment)

7.1.3. **Annotation accuracy check**: Verify annotations, callouts, references are correct:
- Pipe sizes match hydraulic calculations (DEL-03.03)
- Material callouts reference DEL-03.02 Technical Specification correctly
- Calculation references (e.g., "See DEL-03.03 Calc Sheet X") point to correct calculation sheets
- Equipment data sheet references (e.g., "See DEL-03.04 OWS Data Sheet") are correct
- Coordination notes reference correct adjacent package deliverables (e.g., "Coordinate with PKG-02" cites correct PKG-02 deliverable)

7.1.4. **CAD standard compliance check**: Verify CAD standards alignment per Specification §QR-3 and Guidance §P-3:
- Layer naming matches project CAD conventions
- Line weights, text styles, annotation styles are consistent across sheets
- Symbol library usage is consistent (no custom symbols without justification)
- Title block format matches project template

7.1.5. **Metadata completeness check**: Verify title blocks are populated per Step 6 (drawing numbers, revisions, originator name, issue dates).

7.1.6. **Cross-document consistency check**: Verify drawing content aligns with Specification requirements, Datasheet attributes, and Guidance principles:
- Environmental protection features (OWS capacity, containment boundaries, instrumentation) are clearly annotated per Specification §FR-2 and Guidance §P-2
- Coordination details (utility separations, crossing clearances, interface tie-ins) are shown per Specification §FR-3 and Guidance §P-4
- Drawing organization matches Datasheet §Construction drawing structure

**Verification**: Self-check checklist completed and signed by originator; checklist documents all review items completed and any issues identified for correction before interdisciplinary check.

**Output**: Drawing set passes self-check; ready for interdisciplinary review.

---

#### Step 7.2: Interdisciplinary Check

**Actions**:
7.2.1. **Distribute drawings for interdisciplinary review**: Share drawing set (PDF or CAD files) with adjacent discipline leads:
- PKG-02 Site Grading: Review storm drainage tie-in elevations, finished grade coordination, drainage flow directions
- PKG-04 Pavement and Surfacing: Review trench restoration details, drainage inlet locations, pavement section coordination
- PKG-14 Process Piping: Review pipe crossing locations, utility separation clearances, trench congestion coordination
- PKG-17 Electrical Power Distribution: Review duct bank conduit routing, pull box locations, conduit schedule alignment with electrical design

7.2.2. **Coordination meeting**: Conduct interdisciplinary coordination meeting (or review workshop) to discuss comments:
- Review coordination comments from each discipline
- Identify and resolve conflicts (pipe crossing elevation conflicts, insufficient clearances, routing conflicts)
- Document agreed resolutions and action items

7.2.3. **Incorporate interdisciplinary review comments**: Update drawings to address coordination comments:
- Adjust pipe alignments, elevations, or routing to resolve conflicts
- Add coordination notes or clarifications requested by reviewers
- Update conduit schedule or crossing details to match adjacent discipline requirements
- Document changes in revision history (if issuing revised drawings for re-review)

7.2.4. **Obtain interdisciplinary review sign-offs**: Collect sign-off confirmation from adjacent discipline leads:
- Sign-off indicates discipline has reviewed drawings and coordination conflicts are resolved
- Sign-offs may be email confirmations, review comment log closeout signatures, or formal review stamps on drawings (per project QA procedures)

**Verification**: Interdisciplinary review log documents comments received, resolutions, and sign-offs; checker signature on drawing title blocks confirms interdisciplinary coordination review completed.

**Output**: Drawing set passes interdisciplinary check; coordination with adjacent disciplines validated; ready for independent check.

**Cross-reference**: Specification §IF-1 coordination with adjacent packages; Specification §Verification interdisciplinary check; Guidance §P-4 coordination-driven detailing; Guidance §C-1 upstream design data availability.

---

#### Step 7.3: Independent Check

**Actions**:
7.3.1. **Compliance with civil standards check**: Independent reviewer verifies compliance with:
- Employer's Requirements Volume 2 Part 2 (Civil & Process Mechanical Works): Civil utility design criteria, pipe material standards, installation methods, environmental protection requirements (Specification §Standards governing standards)
- Applicable codes and regulations: NBC, BCBC, CSA standards, local municipal standards (Specification §Standards assumed applicable codes)
- Project civil design brief: Design life, seismic design category, design storm event, other design parameters (Specification §PR-3 design life and environmental conditions)

7.3.2. **Hydraulic and structural performance validation**: Independent reviewer validates performance against design inputs:
- Verify storm drainage pipe sizes, slopes, and hydraulic grade lines match hydraulic calculations (DEL-03.03) per Specification §PR-1
- Verify OWS capacity and containment volumes match sizing calculations (DEL-03.03) per Specification §PR-2
- Verify trenchless crossing casing sizes, depths, and structural details match structural analysis (DEL-03.03)
- Confirm design parameters (design storm event, seismic category, soil bearing capacity) match civil design brief per Specification §PR-3

7.3.3. **Environmental protection compliance check**: Independent reviewer confirms environmental protection features are clearly shown per Specification §FR-2 and Guidance §P-2 (OBJ-7):
- Containment boundaries are delineated (Step 5.1)
- OWS capacity and instrumentation are annotated (Step 5.2)
- Emergency overflow routes are shown (Step 5.3)
- Sump locations and volumes are annotated (Step 5.4)
- General note emphasizes environmental protection compliance (Step 5.5)

7.3.4. **Quality requirements compliance check**: Independent reviewer verifies QA compliance per Specification §QR-1, §QR-2, §QR-3:
- Drawing production followed QA procedures: originator prepared, checker reviewed, approver signs (Specification §QR-1)
- Review checkpoints completed: Self-check checklist ✓, interdisciplinary review log ✓, independent check in progress ✓ (Specification §QR-2)
- CAD standards compliance confirmed: Layer naming, line weights, text styles, symbol libraries (Specification §QR-3)

7.3.5. **Traceability verification**: Independent reviewer confirms drawing annotations reference related deliverables correctly per Specification §IF-2:
- Material callouts reference DEL-03.02 Technical Specification
- Calculation references cite DEL-03.03 Design Calculations with correct calculation sheet IDs
- Equipment data sheet references cite DEL-03.04 Data Sheet Package
- Installation and commissioning notes reference DEL-03.05 Installation and Test Records

7.3.6. **Record review results**: Independent reviewer documents findings in review stamp block on drawings:
- "Reviewed for compliance with civil standards and Employer's Requirements. Approved for issue." [Signature, Date]
- If issues are found: "Reviewed for compliance. Revise and resubmit per attached comment log." [Signature, Date]

**Verification**: Independent check review stamp on drawings confirms compliance verification completed; QA checklist documents all review items completed and any issues resolved before issue.

**Output**: Drawing set passes independent check; approved for issue into document control system.

**Cross-reference**: Specification §Verification independent check; Specification §QR-1 quality management compliance; Specification §QR-2 drawing review and approval process; Specification §PR-1, §PR-2, §PR-3 performance requirements.

---

### Step 8: Issue into Document Control System

**Objective**: Package drawing set for issue into project document control system; create issue register entry and distribute to construction teams and stakeholders.

**Actions**:
8.1. Finalize drawing set package:
- Ensure all drawings have complete title block signatures (originator, checker, approver)
- Ensure revision codes and issue descriptions are consistent across all sheets
- Compile drawing set into single PDF package (or multi-sheet CAD file per project conventions)
- Include cover letter or transmittal memo listing drawings in package, issue purpose (e.g., "Issued for Construction"), and distribution list

8.2. Submit to document control coordinator:
- Upload drawing package to project document management system (e.g., ProjectWise, SharePoint, or other system per project conventions)
- Complete document control submission form with drawing numbers, revisions, issue status, distribution list

8.3. Create issue register entry:
- Document control coordinator creates issue register entry with:
  - Drawing numbers and revisions issued
  - Issue date
  - Issue status (e.g., "Issued for Review", "Issued for Construction", "As-Built")
  - Distribution list (construction teams, adjacent disciplines, operations, regulatory agencies as applicable)
  - Transmittal number or reference

8.4. Distribute drawing package per distribution list:
- Document control coordinator distributes drawing package to construction teams, adjacent disciplines, and stakeholders
- Distribution may be via document management system notifications, email transmittals, or hard copy distribution per project procedures

8.5. Archive quality records:
- Retain drawing review logs, QA checklists, interdisciplinary review comments and resolutions, independent check review stamps in project files per Specification §Documentation associated quality records
- Archive records per project document retention policy (typically 7+ years for design-build contracts; per Employer's Requirements Volume 2 Part 1)

**Verification**: Issue register entry confirms drawing package is issued into document control system; distribution confirmation (read receipts, acknowledgment emails) confirms stakeholders received drawings.

**Output**: Drawing set issued into document control system; available for construction use and stakeholder review.

**Cross-reference**: Specification §FR-4 drawing metadata and document control; Specification §QR-2 drawing review and approval process; Specification §Documentation format, numbering, and revision control; Datasheet §Conditions drawing control alignment.

---

## Verification

This section consolidates verification activities described in Steps 7.1, 7.2, 7.3 above. Each verification activity ties to specific Specification requirements.

**Self-Check (Originator Review) – Step 7.1:**
- **Purpose**: Ensures annotations, dimensions, profiles, and details match design inputs; verifies CAD standard compliance; confirms anticipated artifacts are present; checks metadata completeness.
- **Ties to requirements**: Specification §FR-1 comprehensive arrangement, §FR-4 drawing metadata, §QR-3 CAD standards; Datasheet §Attributes metadata fields; Guidance §P-3 consistent notation.
- **Output**: Self-check checklist completed and signed by originator.

**Interdisciplinary Check – Step 7.2:**
- **Purpose**: Verifies coordination with earthworks (PKG-02), paving (PKG-04), process (PKG-14), and electrical (PKG-17) disciplines; confirms utility separations and crossing details are constructible; reviews environmental protection annotations with process team.
- **Ties to requirements**: Specification §FR-3 coordination across underground networks, §IF-1 coordination with adjacent packages; Guidance §P-4 coordination-driven detailing; Guidance §C-1 upstream design data availability.
- **Output**: Interdisciplinary review log with comments, resolutions, and sign-offs; checker signature on drawings confirms coordination review completed.

**Independent Check – Step 7.3:**
- **Purpose**: Confirms compliance with civil standards (Specification §Standards) and Employer's Requirements (Volume 2 Part 2); validates hydraulic and structural performance (Specification §PR-1) against calculation results (DEL-03.03); ensures design parameters (Specification §PR-3) match civil design brief; verifies environmental protection features (Specification §FR-2) are clearly shown; confirms traceability (Specification §IF-2) to related deliverables.
- **Ties to requirements**: Specification §PR-1 hydraulic and structural performance, §PR-2 facility throughput and containment support, §PR-3 design life and environmental conditions, §FR-2 environmental protection features, §IF-2 linkage to related deliverables, §QR-1 quality management compliance; Guidance §P-2 environmental protection clarity (OBJ-7).
- **Output**: Independent check review stamp on drawings confirms compliance verification; QA checklist documents review completion.

**Dimensional and Coordination Verification:**
- Scale, coordinates, and elevations checks confirm that plan-and-profile sheets align with site constraints from PKG-02 site grading and survey data (Specification §IF-1 coordination requirement; Datasheet §Attributes coordinate system match).
- Utility separation clearances verified against applicable standards and constructability constraints (Step 7.2 interdisciplinary check and Step 7.3 independent check).
- Results recorded in drawing review logs and QA checklists per Specification §QR-1 (Specification §Documentation associated quality records).

**Traceability Verification:**
- Drawing annotations reference Data Sheet Package (DEL-03.04) and Technical Specification (DEL-03.02) for performance requirements per Specification §IF-2 linkage requirement (Step 7.3.5).
- Drawing general notes reference applicable standards, design criteria documents, and calculation reports to maintain traceability (Step 2.4 and Step 7.3.1).

**Requirement Traceability Summary:**
- Each Specification functional requirement (§FR-1 to §FR-4) has corresponding verification step in this Procedure (Steps 7.1 completeness check, 7.3.3 environmental protection check, 7.2 coordination check, 7.1.5 metadata check).
- Each Specification performance requirement (§PR-1 to §PR-3) has independent check validation in Step 7.3.2.
- Each Specification interface requirement (§IF-1 to §IF-2) has interdisciplinary check or traceability verification in Steps 7.2 and 7.3.5.
- Each Specification quality requirement (§QR-1 to §QR-3) has QA review checkpoint in Steps 7.1.4, 7.2, 7.3.4.

---

## Records

**Drawing Deliverables (Specification §Scope and §Documentation):**
- Storm drainage plans and profiles (plan-and-profile sheets with pipe alignments, invert elevations, slopes, hydraulic grade lines)
- OWS layout (plan and sections showing separator location, piping, instrumentation, capacity annotations)
- Duct bank plans (conduit routing plans, trench cross-sections, pull box details, conduit schedule tables)
- Trenchless crossing drawings (alignment plans/profiles, boring/jacking details, casing and carrier pipe specifications)
- Detail sheets (pipe connections, trench sections, manhole/catch basin installations, utility separations)
- Cover sheet (drawing index, abbreviations, general notes, coordinate system/datum statement, applicable standards list)

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:188 anticipated artifacts; detailed in Specification §Scope and Datasheet §Construction.)

**Quality Records (Specification §Documentation associated quality records):**
- **Self-check checklist**: Documents originator review completion per Step 7.1; includes completeness, dimensional accuracy, annotation accuracy, CAD standard compliance, metadata completeness checks.
- **Interdisciplinary review log**: Documents coordination comments from PKG-02, PKG-04, PKG-14, PKG-17; resolutions; sign-offs per Step 7.2.
- **Independent check review stamp**: Documents independent reviewer compliance verification per Step 7.3; includes review findings and approval signature on drawing title blocks.
- **QA checklists**: Documents QA compliance verification (QA procedures followed, review checkpoints completed, CAD standards met) per Specification §QR-1 and Step 7.3.4.
- **Issue register entry**: Documents drawing package issue into document control system per Step 8.3; includes drawing numbers, revisions, issue date, issue status, distribution list.
- **Drawing review logs**: Consolidated record of self-check, interdisciplinary check, and independent check activities; retained per project document retention policy.

(All records retained per project document control procedures per test/Volume_2_Part_1_Employers_Requirements.pdf and Specification §QR-1 quality management compliance.)

**Related Deliverable Cross-References:**
- DEL-03.02 Technical Specification: Material specifications referenced in drawing annotations (Specification §IF-2; Step 2.2 input data collection).
- DEL-03.03 Design Calculations: Hydraulic calculations, OWS sizing, structural analysis referenced in drawing annotations (Specification §PR-1, §PR-2; Step 2.2 input data collection; Step 7.3.2 performance validation).
- DEL-03.04 Data Sheet Package: Equipment data sheets referenced in OWS layout annotations (Specification §PR-2; Step 4.2 OWS layout development; Step 7.3.5 traceability verification).
- DEL-03.05 Installation and Test Records: Installation and commissioning requirements referenced in drawing general notes (Specification §IF-2; Step 5.5 environmental protection general note).

---

## Cross-Document Notes

**Procedure → Specification:**
- Steps 1-8 implement Specification requirements: Step 1 implements §Scope, Steps 2-6 implement §Requirements, Step 7 implements §Verification, Step 8 implements §Documentation.
- Step 7.1 self-check implements Specification §Verification self-check; Step 7.2 interdisciplinary check implements Specification §Verification interdisciplinary check; Step 7.3 independent check implements Specification §Verification independent check.
- Prerequisites section lists reference materials required by Specification §Standards (Employer's Requirements, project CAD standards, civil design brief).
- Step 5 environmental protection annotation implements Specification §FR-2 environmental protection features requirement and §PR-2 facility throughput and containment support.
- Step 7.2 interdisciplinary check implements Specification §IF-1 coordination with adjacent packages.
- Step 7.3.5 traceability verification implements Specification §IF-2 linkage to related deliverables.

**Procedure → Datasheet:**
- Steps 4.1-4.4 detailed plans/profiles/sections produce drawing content described in Datasheet §Construction (storm drainage, OWS layout, duct banks, trenchless crossings).
- Step 6 metadata compilation populates title block fields listed in Datasheet §Attributes (drawing number, revision, originator, checker, approver, coordinate system).
- Step 2 input data collection confirms coordinate system alignment with PKG-02 per Datasheet §Attributes coordinate system requirement.
- Step 8 issue into document control implements drawing control alignment per Datasheet §Conditions operational context.

**Procedure → Guidance:**
- Steps 3-4 schematic arrangements and detailed design implement Guidance principles: Step 4.1 implements §P-1 hydraulic conveyance, Step 5 implements §P-2 environmental protection clarity, Step 3.3 implements §P-3 consistent notation, Steps 4.1-4.4 implement §P-4 coordination-driven detailing.
- Prerequisites section addresses Guidance considerations: Prerequisites dependencies address §C-1 upstream design data availability, Prerequisites reference materials address §C-2 Employer's Requirements extraction, Step 1 scope review addresses §C-3 sheet structure and scope boundaries, Step 7 verification addresses §C-4 QA/QC sign-offs, Steps 4-5 detailed design address §C-5 construction use and as-built record intent.
- Steps 4.1-4.4 detailed design resolve or document Guidance trade-offs: Step 4 detailing level resolves §T-1, Step 4.1 pipe sizing resolves §T-2, Step 4.4 trenchless crossing detail resolves §T-3, Step 4.3 duct bank schedule resolves §T-4.
- Steps 4.1-4.4 detailed design examples correspond to Guidance §Examples 1-4: Step 4.1 implements Example 1 storm drainage, Step 4.2 implements Example 2 OWS layout, Step 4.3 implements Example 3 duct bank, Step 4.4 implements Example 4 trenchless crossing.

**Workflow Completeness Check:**
- Specification requirement → Procedure step → Verification checkpoint mapping ensures every requirement is implemented in workflow and verified before issue:
  - §FR-1 comprehensive arrangement → Steps 3-4 schematic and detailed design → Step 7.1 completeness check ✓
  - §FR-2 environmental protection features → Step 5 environmental protection annotation → Step 7.3.3 environmental protection compliance check ✓
  - §FR-3 coordination across underground networks → Steps 2, 3, 4 coordination → Step 7.2 interdisciplinary check ✓
  - §FR-4 drawing metadata → Step 6 metadata compilation → Step 7.1.5 metadata completeness check ✓
  - §PR-1 hydraulic and structural performance → Steps 2, 4 design inputs and detailed design → Step 7.3.2 performance validation ✓
  - §PR-2 facility throughput and containment → Steps 2, 4, 5 design inputs and OWS detailing → Step 7.3.2 performance validation ✓
  - §PR-3 design life and environmental conditions → Prerequisites civil design brief, Steps 2, 4 design inputs and detailed design → Step 7.3.2 performance validation ✓
  - §IF-1 coordination with adjacent packages → Prerequisites and Step 2 input data collection → Step 7.2 interdisciplinary check ✓
  - §IF-2 linkage to related deliverables → Steps 2, 4 reference annotations → Step 7.3.5 traceability verification ✓
  - §QR-1 quality management compliance → Steps 7-8 QA/QC review workflow → Step 7.3.4 quality requirements compliance check ✓
  - §QR-2 drawing review and approval → Steps 7-8 review workflow and issue → Step 8 issue register entry ✓
  - §QR-3 CAD standards → Step 3.3 CAD standard alignment, Step 4 detailed design → Step 7.1.4 CAD standard compliance check ✓

---

## Pass 2 Enrichments

This Pass 2 revision adds:
1. Expanded Purpose section with production purpose and quality assurance purpose clarifying dual intent of procedure (produce drawings + execute QA workflow).
2. Detailed Prerequisites section with dependencies, reference materials, design intent understanding, and personnel requirements clearly listing what must be available before starting work.
3. Detailed Steps (Steps 1-8) breaking down drawing production workflow into discrete phases with clear objectives, actions, verification checkpoints, and outputs for each step.
4. Expanded environmental protection annotation step (Step 5) implementing Specification §FR-2 and Guidance §P-2 (OBJ-7) with specific annotation requirements for containment boundaries, OWS capacity, instrumentation, overflow routes, and sumps.
5. Detailed metadata and revision history compilation step (Step 6) implementing Specification §FR-4 and Datasheet §Attributes metadata requirements.
6. Comprehensive verification section (Step 7) with detailed self-check, interdisciplinary check, and independent check procedures showing exactly what reviewers must verify and how verification ties to Specification requirements.
7. Issue into document control step (Step 8) implementing Specification §Documentation and §QR-2 with clear actions for finalizing drawing package, submitting to document control, creating issue register entry, distributing drawings, and archiving quality records.
8. Enhanced Records section listing all drawing deliverables, quality records, and related deliverable cross-references.
9. Comprehensive cross-document notes showing how Procedure steps implement Specification requirements, produce Datasheet content, and apply Guidance principles/considerations/trade-offs.
10. Workflow completeness check table confirming every Specification requirement has corresponding Procedure step and verification checkpoint (requirement → implementation → verification traceability).

## Pass 3 Final Notes

**Pass 3 Reconciliation Completed:**
- All Specification requirements have corresponding Procedure implementation steps and verification checkpoints (workflow completeness check at end of §Cross-Document Notes confirms requirement → implementation → verification traceability).
- All Guidance principles have corresponding Procedure implementation:
  - Guidance §P-1 hydraulic conveyance → Procedure §4.1 storm drainage detailing with hydraulic annotations
  - Guidance §P-2 environmental protection (OBJ-7) → Procedure §5 environmental protection annotation + §7.3.3 compliance check
  - Guidance §P-3 consistent notation → Procedure §3.3 CAD standard alignment + §7.1.4 CAD compliance check
  - Guidance §P-4 coordination-driven detailing → Procedure §2.1 input data collection + §3.4 coordination schematic review + §7.2 interdisciplinary check
- All Guidance considerations addressed in Procedure prerequisites or workflow:
  - Guidance §C-1 upstream design data availability → Procedure §Prerequisites dependencies + §2 input data collection + §2.3 data approval status confirmation
  - Guidance §C-2 ER extraction → Procedure §Prerequisites ER Volume 2 Part 2 as required reference + §7.3.1 compliance check
  - Guidance §C-3 sheet structure and scope boundaries → Procedure §1 scope and objectives review + §3.2 drawing structure establishment
  - Guidance §C-4 QA/QC sign-offs → Procedure §Prerequisites personnel requirements + §7 verification workflow with three review levels
  - Guidance §C-5 construction use and as-built record intent → Procedure §4 detailed design (balance detailing level) + §4 detail sheets for repetitive elements
- All Guidance trade-offs have implementation decisions in Procedure workflow:
  - Guidance §T-1 detailing level → Procedure §4 detailed plans/profiles/sections + §4.5 detail sheets for repetitive elements (implements balance approach)
  - Guidance §T-2 storm drainage capacity vs trench congestion → Procedure §2.2 collect DEL-03.03 hydraulic calculations (sizing from calculations) + §7.2 interdisciplinary check (coordination validation)
  - Guidance §T-3 trenchless crossing representation → Procedure §4.4 simplified alignment drawings + general note referencing DEL-03.02 for boring methods (implements recommended approach)
  - Guidance §T-4 duct bank schedule detail → Procedure §4.3 detailed duct bank schedule table + coordination notes with PKG-17 (implements recommended approach)
- All Guidance examples have corresponding Procedure detailed design steps:
  - Guidance §Example 1 storm drainage → Procedure §4.1 develop detailed storm drainage plan-and-profile sheets (implements example structure)
  - Guidance §Example 2 OWS layout → Procedure §4.2 develop detailed OWS layout sheet (implements example clarity guidance)
  - Guidance §Example 3 duct bank plan → Procedure §4.3 develop detailed duct bank plan and sections (implements example coordination emphasis)
  - Guidance §Example 4 trenchless crossing → Procedure §4.4 develop detailed trenchless crossing sheets (implements example alignment drawing guidance)

**Workflow Integrity Verification:**
- Every Specification requirement (FR-1 to FR-4, PR-1 to PR-3, IF-1 to IF-2, QR-1 to QR-3) has:
  - Implementation step(s) in Procedure §Steps producing deliverable content that satisfies the requirement
  - Verification checkpoint in Procedure §Verification confirming requirement is met before issue
  - Cross-reference to Guidance rationale explaining why requirement exists
  - Cross-reference to Datasheet content that requirement applies to
- Prerequisites section completeness verified:
  - Dependencies clearly state NOT_TRACKED mode and list required upstream inputs from PKG-02/04/14/17 and DEL-03.02/03/04
  - Reference materials list all governing documents (ER Volume 2 Part 1 & 2, project CAD standards, civil design brief, package reference index)
  - Design intent understanding guides originator to review Specification, Guidance, and downstream use context before starting
  - Personnel requirements identify originator, checker, approver, and adjacent discipline reviewers roles
- Steps section workflow verified:
  - Step 1 scope review → confirms what to produce (anticipated artifacts) and why (OBJ-7, requirements, exclusions)
  - Step 2 input data collection → gathers design inputs from upstream packages and related deliverables, confirms approval status
  - Step 3 schematic arrangements → establishes drawing structure, coordinates with adjacent disciplines at schematic stage
  - Step 4 detailed plans/profiles/sections → produces detailed content for all four anticipated artifacts with cross-references to calculations and specifications
  - Step 5 environmental protection annotation → implements OBJ-7 emphasis with clear containment boundaries, OWS capacity, instrumentation, overflow routes, sumps annotations
  - Step 6 metadata compilation → populates title blocks with drawing numbers, revisions, originator/checker/approver, issue dates per document control procedures
  - Step 7 verification workflow → executes self-check (originator), interdisciplinary check (adjacent disciplines), independent check (compliance with standards) with documented checklists and review logs
  - Step 8 issue into document control → packages drawing set, submits to document control, creates issue register entry, distributes to stakeholders, archives quality records
- Verification section completeness verified:
  - Self-check (§7.1) covers completeness, dimensional accuracy, annotation accuracy, CAD compliance, metadata completeness, cross-document consistency
  - Interdisciplinary check (§7.2) covers coordination with PKG-02/04/14/17, conflict resolution, coordination meeting, review comment incorporation, sign-off collection
  - Independent check (§7.3) covers compliance with civil standards and ER, hydraulic/structural performance validation, environmental protection compliance, quality requirements compliance, traceability verification, review results documentation
  - Each verification activity ties to specific Specification requirements (verification traceability documented)
- Records section completeness verified:
  - Drawing deliverables list matches Datasheet §Construction drawing organization and Specification §Scope anticipated artifacts exactly
  - Quality records list includes all QA documentation (self-check checklist, interdisciplinary review log, independent check review stamp, QA checklists, issue register entry, drawing review logs) per Specification §Documentation
  - Related deliverable cross-references match Specification §IF-2 linkages (DEL-03.02, DEL-03.03, DEL-03.04, DEL-03.05)

**Entity Coverage Verification:**
- All four anticipated artifacts (storm drainage, OWS, duct banks, trenchless crossings) have production steps in Procedure §4 and documentation in Procedure §Records, matching Datasheet §Construction, Specification §Scope, and Guidance §Examples.
- OBJ-7 Environmental Protection theme implemented via Procedure §5 environmental protection annotation with five specific annotation requirements (containment boundaries, OWS capacity, overflow routes, sumps, general note), verified via Procedure §7.3.3, matching Datasheet §Conditions, Specification §FR-2, Guidance §P-2.
- Coordination with adjacent packages theme implemented via Procedure §2.1 input data collection + §3.4 coordination schematic review + §7.2 interdisciplinary check, matching Datasheet §Attributes coordinate system alignment, Specification §IF-1, Guidance §P-4 and §C-1.
- CAD standards theme implemented via Procedure §3.3 CAD standard alignment + §7.1.4 CAD compliance check, matching Datasheet §Attributes, Specification §QR-3, Guidance §P-3.
- Terminology consistency verified with other documents: "storm drainage plans and profiles", "OWS layout", "duct bank plans", "trenchless crossing drawings", "OBJ-7 Environmental Protection", "coordinate system alignment with PKG-02", "self-check", "interdisciplinary check", "independent check", "issue register", "drawing review logs" used consistently.

**Document Maturity:**
- This Procedure, along with Datasheet, Specification, and Guidance, has completed three enrichment passes (Pass 1 initial generation, Pass 2 detailed workflow steps and verification enrichment, Pass 3 final reconciliation).
- Procedure provides complete, actionable, and traceable workflow for producing DEL-03.01 Underground Utilities Design Drawing Set from prerequisites through input collection, design development, annotation, verification, and issue into document control.
- All eight workflow steps are detailed with clear objectives, actions, verification checkpoints, and outputs; workflow integrity verified via requirement → implementation → verification traceability mapping.
- Verification section provides three-level review process (self-check, interdisciplinary check, independent check) with explicit ties to Specification requirements ensuring all requirements are verified before issue.
- Document is ready for WORKING_ITEMS sessions where human engineer will execute workflow, adapt steps to project-specific procedures, and document actual production process including design decisions, coordination outcomes, and QA verification results.
- Procedure provides coherent, traceable, and enforceable workflow foundation for DEL-03.01 Underground Utilities Design Drawing Set production with full requirement traceability and quality assurance integration.
