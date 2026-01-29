# Procedure: DEL-10.01 Railcar Unloading Design Drawing Set

## Purpose

This procedure defines the process for **producing and managing** the **Railcar Unloading Design Drawing Set** within **PKG-10 Railcar Unloading System**.

**Scope of Procedure:**
- Production of design drawings for the railcar unloading system (32 stations)
- Internal verification and independent checking workflow
- Interdisciplinary coordination (IDC)
- Approval and issue process
- Document control and records management

**Deliverable Type:** Drawing
**Responsible Party:** D&B Contractor
**Discipline:** Process
**Status:** INITIALIZED

**Dual-Use Nature:**
- This procedure primarily describes how to **produce** the drawing deliverable (design drawings for the unloading system)
- The produced drawings themselves will be **used by** construction contractors (installation), operations personnel (system understanding), and maintenance staff (equipment access, troubleshooting)
- Separate operating procedures for the unloading system itself are outside the scope of this deliverable (may be covered in PKG-22 Operating Manuals if applicable)

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED — dependencies coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`)

**Upstream Inputs (typical sequence — coordinate via project schedule and stage gates):**

| Input | Source Deliverable | Status | Required Information | Use in This Procedure | Specification Link |
|-------|-------------------|--------|---------------------|----------------------|--------------------|
| Site survey and rail alignment | PKG-07 Rail Works deliverables (e.g., DEL-07.xx survey drawings, track layout) | **TBD** | Track centerline coordinates, elevations, curvature data, superelevation; 32 station positions coordinated with track geometry | Step 2 (design layout — station positions); Step 4 (IDC with PKG-07 — verify track alignment) | Specification.md IF-01 (track alignment coordination) |
| Structural support locations | PKG-05 Concrete Structures deliverables (e.g., DEL-05.xx foundation drawings) | **TBD** | Foundation locations (plan coordinates, elevations), foundation load capacities, seismic design criteria | Step 2 (design layout — foundation coordination); Step 4 (IDC with PKG-05 — verify support locations and loads) | Specification.md IF-02 (structural coordination including seismic) |
| Process design basis | DEL-10.02 Technical Specification | **TBD** | Performance requirements (unloading rates, simultaneous operations), operating parameters (temperature, pressure), equipment specifications (arm types, materials), containment requirements | Step 1 (scope confirmation — verify requirements); Step 2 (design development — per specifications) | Specification.md §Requirements (design basis requirements from DEL-10.02) |
| Equipment sizing calculations | DEL-10.03 Design Calculations | **TBD** | Header pipe sizing (pipe diameters, wall thickness), hydraulic profile (elevations, slopes, pressure drop), containment volume calculations (pan sizing, sump sizing), throughput analysis (verify 1,000,000 MT/annum) | Step 2 (header layout per calculated sizes, containment details per calculated volumes) | Specification.md PF-01, PF-03, PF-04 (performance requirements verified by calculations) |
| Equipment data sheets | DEL-10.04 Data Sheet Package | **TBD** | Unloading arm specifications (32 units — dimensions, reach envelopes, mounting details), quick-connect specifications, sump pump specifications (if included in PKG-10), equipment tags | Step 2 (arm arrangement drawings per data sheet dimensions and tags) | Specification.md FN-03 (arm requirements); Datasheet.md §Construction (equipment details from data sheets) |
| Hazardous area classification | **TBD** — PKG-17 deliverable or separate HAC study | **TBD** | Area classification boundaries (Class I Div 2 or Zone 2 extent), classification drawing (zones shown on plot plan) | Step 2 (show classification zones on GA for electrical/instrumentation interface coordination) | Specification.md IF-03 (electrical coordination including HAC); Datasheet.md §Conditions (HAC parameter **TBD**) |

**ASSUMPTION:** Dependencies managed through project schedule, stage gates (30% / 60% / 90% / IFC), and human coordination (project managers, discipline leads). Upstream deliverables to be available per project milestone plan. If upstream inputs not available at required stage, identify as TBD on drawings and issue with assumptions clearly marked; update in subsequent revisions when inputs available.

### Reference Materials

| Reference | Location | Purpose | Document Link | Specification Link |
|-----------|----------|---------|---------------|--------------------|
| Decomposition | `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | PKG-10 scope (§5); DEL-10.01 definition; objective mapping (§6: OBJ-1, OBJ-2, OBJ-4, OBJ-7) | Datasheet.md §References; Specification.md §Scope | Specification.md §Scope (scope definition); Guidance.md §Principles (objective alignment) |
| Employer's Requirements Vol 2 Pt 1 | `test/Volume_2_Part_1_Employers_Requirements.pdf` | Project requirements (clauses **TBD** — unloading system requirements, performance criteria, interface requirements) | Specification.md §Requirements; Datasheet.md §Conditions | Specification.md §Requirements (ER requirements drive specifications) |
| Employer's Requirements Vol 2 Pt 2 | `test/Volume_2_Part_2_Employers_Requirements.pdf` | Technical specifications, design criteria (clauses **TBD** — equipment specs, materials, standards) | Specification.md §Requirements; Datasheet.md §Conditions | Specification.md §Requirements, §Standards (ER technical specifications) |
| Employer's Requirements Vol 2 Pt 3 | `test/Volume_2_Part_3_Employers_Requirements.pdf` | Quality and documentation requirements (clauses **TBD** — CAD standard, document control, review/approval process) | Specification.md QA-xx; Datasheet.md §Attributes | Specification.md §Standards (CAD standard), QA-xx (quality requirements), §Documentation (document control) |
| Specification.md | This deliverable folder | Requirements to be satisfied by drawings (functional FN-xx, performance PF-xx, interface IF-xx, quality QA-xx) | All steps (design development and verification against requirements) | Bidirectional link (this procedure implements specification requirements) |
| Guidance.md | This deliverable folder | Design principles, considerations, trade-offs (gravity flow design, spill containment, operational access, etc.) | Step 2 (design development per principles and considerations) | Bidirectional link (this procedure applies guidance principles) |
| Datasheet.md | This deliverable folder | Drawing attributes, metadata, anticipated artifacts, interface elements | Steps 1 (drawing list per anticipated artifacts), 2 (metadata population), 3 (metadata check), 6 (finalize metadata) | Bidirectional link (this procedure produces drawings per datasheet specifications) |
| Applicable standards | **TBD** — per Specification.md §Standards | Code compliance: Project CAD standard (drawing production), ASME B31.3 (process piping), BC Building Code (structural/seismic), Environmental regulations (containment), HAC standard (area classification) | Step 2 (design per codes and standards); Step 5 (compliance check) | Specification.md §Standards (all applicable standards listed) |

### Personnel Requirements

| Role | Qualification | Responsibility | Verification | Specification Link |
|------|---------------|----------------|--------------|-------------------|
| Design Engineer | Process discipline; CAD proficiency; **TBD** years experience or professional registration (P.Eng. in BC for engineering deliverables) | Drawing production (Steps 1–3): design development, CAD production, self-check | Originator sign-off on drawings (title block or separate sign-off sheet) | Specification.md QA-02 (originator metadata requirement) |
| Checker | Process discipline; independent from originator; **TBD** years experience or professional registration | Independent drawing review (Step 5): technical adequacy, code compliance, dimensional accuracy, cross-references, constructability | Checker sign-off (title block or separate sign-off sheet); comment resolution record | Specification.md QA-03 (independent check requirement) |
| Discipline Lead | Process discipline; approval authority; **TBD** years experience and professional registration | Drawing approval (Step 5): technical adequacy, ER compliance, completeness, appropriateness for issue | Approval sign-off (title block or separate sign-off sheet) | Specification.md QA-05 (approval requirement) |
| IDC Coordinator | Multi-discipline coordination experience; understanding of all discipline scopes | Interface coordination (Step 4): organize IDC meetings, track interface issues, coordinate conflict resolution, obtain sign-offs | IDC sign-off sheet (all interface disciplines signed) | Specification.md QA-04 (IDC requirement); Specification.md IF-01 through IF-06 (all interfaces) |
| Document Controller | Document control procedures knowledge; project document management system familiarity | Issue and transmittal (Step 6): document numbering, transmittal preparation, distribution, document register updates | Transmittal record; document register entry | Specification.md §Documentation (document control requirements) |

**ASSUMPTION:** Personnel competency requirements per project quality procedures and professional registration requirements (e.g., P.Eng. in BC for engineering deliverables, or Engineer-in-Training under supervision of P.Eng.).

### Tools and Resources

| Tool/Resource | Purpose | Specification Link | Use in Procedure |
|---------------|---------|-------------------|------------------|
| CAD software | Drawing production per project CAD standard (e.g., AutoCAD, MicroStation, or other per ER) | Specification.md QA-01 (CAD standard compliance) | Step 2 (drawing production) |
| Project CAD standard | Drawing format, symbols, layers, line weights, text styles, title block template | Specification.md QA-01; Datasheet.md §Attributes (CAD standard **TBD**) | Step 2 (CAD standard application), Step 5 (CAD compliance check) |
| Project document numbering system | Drawing number assignment (numbering format, number series allocation) | Datasheet.md §Attributes (drawing number series **TBD**) | Step 1 (assign drawing numbers) |
| Document management system | Drawing storage, revision control, transmittal, distribution, document register | Specification.md §Documentation (electronic format, retention) | Step 6 (issue and filing), all steps (version control) |
| Calculation software | **If needed** — hydraulic analysis (header sizing), containment sizing (typically performed in DEL-10.03; drawings verify against calculations rather than perform calculations) | DEL-10.03 (calculations reference) | Step 2 (verify design against DEL-10.03 calculations) |

## Steps

### Step 1: Confirm Scope and Define Drawing List

**Objective:** Establish the approved drawing list based on PKG-10 scope and anticipated artifacts, ensuring completeness and traceability to requirements.

**Actions:**

1. **Review Specification.md §Scope** for deliverable scope and exclusions:
   - Confirm PKG-10 scope elements to be depicted: (1) unloading arms, (2) quick-connects, (3) gravity flow header, (4) spill containment pans, (5) collection system, (6) atmospheric venting, (7) flow indicators (Specification.md FN-01)
   - Confirm anticipated drawing types: GA, Arm Arrangement, Header Layout, Containment Details (Specification.md FN-02; Datasheet.md §Construction)
   - Note exclusions: vendor fabrication drawings (DEL-10.04 scope), downstream piping (PKG-14 scope), electrical schematics (PKG-17 scope), instrumentation loop diagrams (PKG-20 scope), rail track design (PKG-07 scope), structural design (PKG-05/PKG-06 scope)

2. **Review Datasheet.md §Construction** for anticipated artifacts:
   - Unloading System GA (overall 32-station layout)
   - Unloading Arm Arrangement (arm positions for 32 stations)
   - Header Pipe Layout (gravity flow header routing, sizes, slopes)
   - Containment Details (spill pans, collection sumps, drains)

3. **Develop preliminary drawing list** with discipline lead (see Guidance.md §Examples for typical content of each drawing type):

   | Drawing No. | Drawing Title | Content Summary | Spec Req | Datasheet Link | Guidance Link |
   |-------------|---------------|-----------------|----------|----------------|---------------|
   | **TBD**-GA-001 | Railcar Unloading System - General Arrangement | Overall 32-station layout, header routing, containment areas, equipment locations, access routes, interface points | FN-01, FN-02, FN-03 | §Construction (GA content) | §Examples (GA typical content and scale 1:100 or 1:200) |
   | **TBD**-AR-001 to 00X | Railcar Unloading Arms - Arrangement | Arm positions (may require multiple sheets for 32 stations — e.g., 4 sheets × 8 stations, or typical detail + overall layout), quick-connect details, clearances, reach envelopes, access platforms | FN-01, FN-02, FN-03, IF-01 | §Construction (Arm Arrangement content) | §Examples (Arm Arrangement typical content and scale 1:50 or 1:25) |
   | **TBD**-PL-001 | Header Pipe Layout | Gravity flow header routing (plan and profile), pipe sizes per DEL-10.03, slopes marked (minimum 1:100), branch connections (32 stations), isolation valves, air release valves, pipe supports, discharge connection | FN-01, FN-02, FN-04, IF-05 | §Construction (Header Layout content) | §Examples (Header Layout typical content and scale 1:50 or 1:100) |
   | **TBD**-DT-001 to 00X | Containment Details | Spill containment pans (32 individual or combined per Guidance.md §Trade-offs decision), collection sumps, drain routing, sump pumps, containment volume reference to DEL-10.03 | FN-01, FN-02, FN-05, IF-03, IF-04 | §Construction (Containment Details content) | §Examples (Containment Details typical content and scale 1:20 or 1:50) |

   **Note:** Drawing number prefix (**TBD**) per project document numbering procedure (coordinate with document control). Actual sheet count to be determined during design development based on drawing complexity, clarity requirements (avoid clutter per Guidance.md §Principles — clarity principle), and CAD standard sheet size. For example, if 32 stations cannot be shown clearly on one arrangement sheet at readable scale, use multiple sheets (e.g., 4 sheets showing details for station groups, plus one overall layout sheet).

4. **Assign drawing numbers** per project document numbering procedure (**TBD**):
   - Confirm numbering format with document control (e.g., project code - discipline code - drawing type - sequence number)
   - Reserve number block for PKG-10 deliverables (coordinate with other PKG-10 deliverables: DEL-10.02 through DEL-10.05 may also have drawing components)
   - Update Datasheet.md §Attributes with assigned drawing number series
   - Document drawing number assignment in drawing list

5. **Obtain discipline lead sign-off** on approved drawing list:
   - Review drawing list with discipline lead for completeness (all scope elements covered per Specification.md FN-01)
   - Confirm drawing types align with project CAD standard and deliverable expectations
   - Obtain sign-off (written approval or email confirmation)

**Output:** Approved drawing list with assigned drawing numbers; filed in `1_Working/` deliverable folder.

**Verification:** Discipline lead sign-off on drawing list (paper or electronic sign-off record).

**Traceability to Specification:**
- Specification.md FN-02: Anticipated artifacts addressed in approved drawing list
- All 7 PKG-10 scope elements (Specification.md FN-01) covered across the 4 drawing types
- Exclusions per Specification.md §Scope confirmed (no drawings for excluded scope)

---

### Step 2: Develop Design and Produce Drawings

**Objective:** Produce drawings addressing all Specification.md requirements using upstream inputs and design principles from Guidance.md.

**Actions:**

1. **Obtain upstream inputs** (per §Prerequisites above):
   - Site survey and rail alignment (PKG-07) — for station positions and track geometry coordination
   - Structural support locations (PKG-05) — for foundation locations and loads
   - Process design basis (DEL-10.02) — for performance requirements and equipment specifications
   - Equipment sizing calculations (DEL-10.03) — for header sizes, containment volumes, throughput verification
   - Equipment data sheets (DEL-10.04) — for arm dimensions, reach envelopes, equipment tags
   - Hazardous area classification (**TBD**) — for classification zones on GA (if HAC study complete)

   **If upstream inputs not yet available:** Identify as **TBD** on drawings with assumptions clearly marked; proceed with design based on reasonable assumptions (document assumptions); update drawings in subsequent revisions when inputs become available.

2. **Develop design layout** for 32 unloading stations per Guidance.md principles:

   **a) Apply gravity flow design principle** (Guidance.md §Principles):
   - Determine header elevations and slopes (minimum 1:100 for drainage; verify with DEL-10.03 hydraulic analysis) to ensure gravity drainage from all 32 stations to discharge point
   - Show slopes clearly on Header Layout drawing (slope arrows and slope values marked)
   - Provide air release provisions at high points (automatic air release valves shown on drawing)
   - Verify no stagnant zones or vapor lock potential (profile view shows elevations)

   **b) Apply equipment spacing principle** (Guidance.md §Principles):
   - Arrange 32 stations per railcar spacing (typically 14–18m centers for North American railcars; verify with PKG-07 track geometry)
   - Account for track curvature effects (may require wider spacing on curves; coordinate with PKG-07)
   - Verify arm reach envelopes (per DEL-10.04 data sheets — typically 3–5m horizontal reach) accommodate railcar positioning tolerance (typically ±500mm)
   - Show clearances for safe operations (operator access, maintenance access, railcar clearances)

   **c) Apply operational access principle** (Guidance.md §Principles):
   - Show access routes on GA (walkways, platforms, access roads for maintenance vehicles)
   - Show operator access platforms on Arm Arrangement (if required for arm connection/disconnection; may be at grade or elevated depending on railcar height and arm mounting)
   - Provide clearances for equipment maintenance (sufficient space for equipment removal/replacement)
   - Consider operational safety (no confined spaces, fall protection where required, lighting — coordinate with PKG-17)

   **d) Apply spill containment principle** (Guidance.md §Principles):
   - Design containment pans per Guidance.md §Trade-offs decision (individual pans per station **PROPOSAL** or common containment system **TBD** — human ruling required)
   - Size containment per DEL-10.03 containment volume calculations (typically one railcar capacity ~100–150 m³ per station, or largest credible spill per regulatory requirements)
   - Show collection system (drain routing from pans to sumps, sump locations, sump sizing, sump pumps)
   - Demonstrate regulatory compliance (containment volume shown on drawing with reference to DEL-10.03; design per environmental regulations **TBD**)

   **e) Consider design factors** from Guidance.md §Considerations:
   - **32-station layout:** Verify against all design factors (railcar spacing, track curvature, arm reach, header routing, access)
   - **Gravity flow header:** Verify slopes, sizing (per DEL-10.03), air release, isolation valves (per OBJ-4 operational flexibility)
   - **Containment volume:** Verify pan sizing, collection capacity, regulatory compliance
   - **Product properties:** Consider canola oil viscosity and temperature effects (if heating required for winter operations **TBD**, show heat tracing on header layout)
   - **Site conditions:** Consider climate (winterization **TBD**), seismic (coordinate with PKG-05), environmental constraints, site access
   - **Railcar interface:** Verify connection type (quick-connect/dry-break) compatible with standard railcar bottom outlets
   - **Simultaneous operations:** Verify header sizing (per DEL-10.03) accommodates required simultaneous operations for 1,000,000 MT/annum throughput

3. **Produce drawings** per project CAD standard (Specification.md QA-01):

   **a) Unloading System GA** (refer to Guidance.md §Examples for typical content):
   - Show overall layout: 32 unloading station positions along rail track (plan view; show track centerline from PKG-07 for coordination)
   - Show gravity flow header routing from stations to discharge connection (interface with PKG-14 — show connection point location, size, elevation)
   - Show containment areas (individual pans or common system per design; indicate containment boundaries)
   - Show equipment locations: sump pumps (Containment Details reference), isolation valves (Header Layout reference), flow indicators (32 locations — one per station)
   - Show access routes and clearances (operational access, maintenance access, site access roads)
   - Show interface points with adjacent disciplines: Rail track (PKG-07 — track centerline), structural supports (PKG-05 — foundation locations marked "See PKG-05 for foundation details"), electrical connections (PKG-17 — connection points marked), instrumentation (PKG-20 — instrument locations), piping connection (PKG-14 — discharge connection marked "To PKG-14 piping")
   - Include north arrow, scale, key plan (if required for orientation on large site), legend (symbols used)
   - Apply title block with metadata per Datasheet.md §Attributes
   - **Typical scale:** 1:100 or 1:200 (entire 32-station layout visible on one or two sheets for orientation — Guidance.md §Examples)

   **b) Unloading Arm Arrangement** (refer to Guidance.md §Examples for typical content):
   - Show arm positions at each of 32 stations (plan and elevation views; may require multiple sheets for clarity — see Step 1 drawing list)
   - Show quick-connect details and railcar coupling interface (connection type, coupler detail, railcar outlet interface)
   - Show clearance envelopes and reach envelopes (per DEL-10.04 data sheets — show reach limits as dashed lines or shaded zones)
   - Show operator access platforms and railcar access points (if platforms required; show access routes)
   - Show flow indicator locations (one per station — coordinate with PKG-20 for instrument type and mounting)
   - Show atmospheric vent connections (vent connection points from railcars; vent routing — may be to atmosphere or to vapor recovery system **TBD**)
   - Coordinate arm positions with rail track centerline (interface PKG-07 — verify station locations match track geometry)
   - Coordinate arm foundations with structural supports (interface PKG-05 — show foundation locations; note loads for PKG-05 foundation design)
   - Apply equipment tags per DEL-10.04 data sheets (consistent tagging across all drawings and data sheets)
   - **Typical scale:** 1:50 or 1:25 (sufficient detail for arm positioning, clearances, and connection details — Guidance.md §Examples; multiple sheets may be required for 32 stations)

   **c) Header Pipe Layout** (refer to Guidance.md §Examples for typical content):
   - Show gravity flow header pipe routing (plan and profile views; profile essential to show elevations and slopes)
   - Show pipe sizes (per DEL-10.03 calculations — note pipe sizes on drawing with reference to DEL-10.03)
   - Show pipe slopes (minimum 1:100 for drainage; mark slopes on profile view with arrows and slope values, e.g., "1:100 ↓")
   - Show branch connections from each of 32 stations (show connection points, branch pipe sizes, connection details — swept vs. abrupt)
   - Show isolation valves (locations per Guidance.md OBJ-4 operational flexibility; valve types — manual or actuated **TBD**; valve tags)
   - Show air release valves at high points (automatic air release valve locations marked on profile view)
   - Show pipe supports (support locations — coordinate with PKG-05/PKG-06 for support design; note support types — e.g., guide, anchor, slide)
   - Show discharge connection to downstream piping (interface with PKG-14 — connection size, elevation, location clearly marked; isolate valve at connection point for responsibility boundary)
   - Include pipe schedule (list all pipe sizes, materials, wall thickness), valve list (valve tag, type, size, operator), material notes (e.g., "All piping SS316 for food-grade service unless noted")
   - **Typical scale:** 1:50 or 1:100 (system overview with sufficient detail for pipe routing, connections, and supports — Guidance.md §Examples)

   **d) Containment Details** (refer to Guidance.md §Examples for typical content):
   - Show spill containment pan arrangement (32 individual or combined system per Guidance.md §Trade-offs decision — human ruling required; show pan arrangement in plan view)
   - Show containment pan dimensions and volume (note volume on drawing, e.g., "Containment pan volume = XX m³ per DEL-10.03"; verify volume adequate for largest credible spill)
   - Show collection sumps and sump sizing (sump locations in plan and section views; sump dimensions, volume; sumps may be one per pan or combined depending on design)
   - Show drain routing from pans to sumps (drain pipe sizes, slopes for gravity drainage, connection points to pans and sumps)
   - Show sump pump locations and pump specifications (pump locations in plan view; pump tags; reference DEL-10.04 if pumps are included in data sheet package, or note pump specifications on drawing)
   - Show sump level switches (interface with PKG-20 — level switch locations for high level alarm and pump control)
   - Show electrical connections for sump pumps (interface with PKG-17 — power supply connection points; cable routing coordination)
   - Include containment volume calculations summary or reference to DEL-10.03 (note on drawing: "Containment volume per DEL-10.03 Calculation XX")
   - Show material notes (e.g., "Containment pans SS304 with welded joints for liquid-tight construction")
   - **Typical scale:** 1:20 or 1:50 (sufficient detail for containment construction, drainage connections, and sump details — Guidance.md §Examples)

4. **Apply Guidance.md considerations** (verify design addresses all considerations from Guidance.md §Considerations):
   - 32-station layout: verify railcar spacing, track curvature effects, arm reach envelopes, header routing, access routes
   - Gravity flow header: verify slopes (minimum 1:100), sizing (per DEL-10.03), air release provisions, isolation valves
   - Containment volume: verify pan sizing per largest credible spill scenario (typically one railcar capacity per station), collection capacity (sump sizing)
   - Product properties: consider canola oil viscosity (affects header sizing), temperature (winterization **TBD**), food-grade handling (material selection)
   - Site conditions: consider climate (outdoor installation, weather exposure), seismic (BC Building Code requirements — coordinate with PKG-05), environmental constraints
   - Railcar interface: verify quick-connect type compatible with standard railcar bottom outlets, positioning tolerance accommodated by arm reach
   - Simultaneous operations: verify header sizing (per DEL-10.03) accommodates required simultaneous operations for throughput capacity

5. **Populate drawing metadata** per Datasheet.md §Attributes:
   - Drawing number (from Step 1 approved drawing list)
   - Drawing title (descriptive title per drawing content)
   - Sheet size (per CAD standard — typically ANSI D or ISO A1 for GA/arrangements; ANSI C or ISO A3 for details)
   - Scale (per Step 3 typical scales; verify scale appropriate for content clarity)
   - Revision (initial issue: "0" or "A" per project convention **TBD**)
   - Date (drawing preparation date; updated on each revision)
   - Originator name (design engineer name)
   - Title block fields per CAD standard: project name ("Canola Oil Transload Facility"), location ("Fraser Surrey Terminal, Surrey, BC"), client ("DP World Fraser Surrey Inc."), contractor (D&B contractor name **TBD**), discipline ("Process"), other fields per CAD standard **TBD**

6. **Apply cross-references** (ensure traceability per Guidance.md §Documentation Considerations):
   - Reference to Specification DEL-10.02 for equipment specifications (note on drawings: "Equipment specifications per DEL-10.02")
   - Reference to Calculations DEL-10.03 for sizing and analysis (note on drawings: "Header sizing per DEL-10.03 Calculation XX"; "Containment volume per DEL-10.03 Calculation YY")
   - Reference to Data Sheets DEL-10.04 for equipment details (note on drawings: "Unloading arm details per DEL-10.04 data sheets"; use consistent equipment tags)
   - Drawing-to-drawing cross-references (e.g., "See Dwg **TBD**-DT-001 for containment details"; "Refer to Dwg **TBD**-PL-001 for header routing")
   - Interface cross-references to other packages (e.g., "Interface with PKG-07 Rail Works — verify track alignment"; "Interface with PKG-14 Process Piping — coordinate connection details")

**Output:** Draft drawings ready for internal self-check (Step 3).

**Traceability to Specification (verify all requirements addressed):**

| Requirement | Drawing | Content Verification | Status after Step 2 |
|-------------|---------|---------------------|---------------------|
| FN-01: All PKG-10 scope elements (7 items) | All drawings | All 7 scope elements depicted: (1) unloading arms — Arm Arrangement, (2) quick-connects — Arm Arrangement, (3) gravity flow header — Header Layout, (4) spill containment pans — Containment Details, (5) collection system — Containment Details, (6) atmospheric venting — GA and Arm Arrangement, (7) flow indicators — GA and Arm Arrangement | ✓ Draft complete — all elements shown |
| FN-02: Anticipated artifacts (4 drawing types) | Drawing list | 4 drawing types produced per approved list: (1) GA, (2) Arm Arrangement, (3) Header Layout, (4) Containment Details | ✓ Draft complete — all drawing types produced |
| FN-03: 32 unloading positions with clearances | GA, Arrangement | 32 stations shown on GA (overall layout); Arm Arrangement shows individual station details with clearances and reach envelopes | ✓ Draft complete — 32 stations shown with clearances |
| FN-04: Gravity flow header with slopes, sizes, connections | Header Layout | Header routing shown with pipe sizes (per DEL-10.03), slopes marked (minimum 1:100), branch connections from 32 stations, isolation valves, air release valves | ✓ Draft complete — gravity flow header fully detailed |
| FN-05: Containment system with volume verification | Containment Details | Pans shown (32 individual or combined per decision), sumps, collection system, volume noted with reference to DEL-10.03 | ✓ Draft complete — containment system shown with calculations reference |
| PF-01: 1,000,000 MT/annum capacity | All drawings | 32-station layout supports throughput (verify with DEL-10.03 analysis) | Verify with DEL-10.03 — calculations confirm capacity |
| PF-04: Header sizing for performance | Header Layout | Pipe sizes per DEL-10.03 calculations (header sized for simultaneous operations) | Verify with DEL-10.03 — header sizing calculations |
| IF-01 to IF-06: Interfaces shown | All drawings | Interface points marked on drawings; prepare for IDC (Step 4) | ✓ Draft complete — interfaces marked; ready for IDC |

---

### Step 3: Internal Self-Check

**Objective:** Verify drawing completeness and accuracy before formal review (independent check Step 5 and IDC Step 4).

**Actions:**

1. **Check drawing completeness** against approved drawing list (Step 1):
   - Verify all drawings from approved list are produced (count sheets; verify drawing numbers match approved list)
   - Verify no drawings missing from approved list
   - Verify no extra drawings not on approved list (if additional drawings needed, update approved list with discipline lead sign-off)

2. **Verify all Specification.md requirements addressed** (use traceability table from Step 2 above):
   - **FN-01 through FN-06:** Functional requirements — verify all PKG-10 scope elements shown on appropriate drawings
   - **PF-01 through PF-04:** Performance requirements — verify design supports throughput (verify against DEL-10.03 calculations) and performance criteria
   - **IF-01 through IF-06:** Interface requirements — verify interface points identified and marked on drawings (ready for IDC Step 4)
   - **QA-01 through QA-06:** Quality requirements — verify CAD standard compliance (line weights, layers, symbols per standard), metadata complete (Datasheet.md §Attributes), drawings ready for independent check

3. **Check dimensional consistency and cross-references** between drawings:
   - **Dimensions:** Verify dimensions match across drawings (e.g., station spacing on GA matches Arm Arrangement; header pipe sizes on Header Layout match calculations DEL-10.03; containment pan dimensions on Containment Details match volume calculations)
   - **Equipment tags:** Verify equipment tags consistent across all drawings and data sheets (same tag for same equipment: unloading arm tags on GA, Arm Arrangement, and DEL-10.04 data sheets must match)
   - **Pipe sizes:** Verify pipe sizes consistent between Header Layout and any other drawings showing piping (sizes per DEL-10.03 calculations)
   - **Containment volumes:** Verify containment pan dimensions on Containment Details result in stated volume (or clearly reference DEL-10.03 for volume calculations)
   - **Cross-references:** Verify drawing cross-references are correct (e.g., "See Dwg X for detail" — verify Dwg X exists and shows the referenced detail; verify drawing number is correct)
   - **Interface points:** Verify interface points shown consistently on all relevant drawings (e.g., header discharge connection shown on Header Layout and marked on GA at same location; foundation locations shown on Arm Arrangement match structural drawings from PKG-05 if available)

4. **Verify drawing metadata** per Datasheet.md §Attributes:
   - **Drawing number:** Verify correct and per approved numbering system from Step 1
   - **Drawing title:** Verify accurate and descriptive of drawing content
   - **Sheet size:** Verify correct per CAD standard
   - **Scale:** Verify correct and appropriate for content (readable at stated scale; not too small causing clutter)
   - **Revision:** Verify correct for initial issue (0 or A per convention)
   - **Date:** Verify current (date of drawing completion or self-check completion)
   - **Originator name:** Verify complete (design engineer name)
   - **Title block:** Verify complete per CAD standard (all required fields populated: project, location, client, contractor, discipline, etc.)

5. **Identify interface points for IDC** (Step 4 preparation):
   - Mark interface points on drawings (or prepare interface list referencing drawing locations)
   - Example markings: "Interface with PKG-07 — verify track centerline coordinates"; "Interface with PKG-05 — confirm foundation locations and loads"; "Interface with PKG-14 — coordinate connection size and elevation"
   - Prepare interface coordination list for IDC Coordinator:
     - IF-01 (PKG-07 Rail Works): Drawings GA and Arm Arrangement — verify station positions, track geometry, clearances
     - IF-02 (PKG-05 Concrete Structures): All drawings — verify support locations and loads
     - IF-03 (PKG-17 Electrical): Containment Details and GA — verify electrical connections and HAC zones
     - IF-04 (PKG-20 Instrumentation): GA, Arm Arrangement, Containment Details — verify instrument locations
     - IF-05 (PKG-14 Process Piping): Header Layout — verify discharge connection details
     - IF-06 (Other **TBD**): Identify any other interfaces as needed
   - Identify disciplines to be involved in IDC (PKG-05, PKG-07, PKG-14, PKG-17, PKG-20, others as identified)

6. **Mark up any issues identified** and resolve before proceeding to Step 4:
   - **Errors:** Correct immediately (dimensional errors, calculation errors, tag errors, cross-reference errors)
   - **Omissions:** Add missing content (missing scope elements, missing interface points, missing metadata)
   - **Inconsistencies:** Reconcile and resolve (dimension mismatches, tag inconsistencies, cross-reference errors)
   - **Unclear content:** Clarify or add notes (add dimension if missing, add note if intent unclear, add cross-reference if needed)
   - Document issues found and resolved (self-check record or marked-up review copy)

**Output:** Self-checked drawings with all issues resolved; ready for IDC (Step 4) and independent check (Step 5).

**Verification:** Design engineer self-check completion record (checklist or sign-off indicating self-check performed and issues resolved); marked-up review copy filed in `1_Working/`.

---

### Step 4: Interdisciplinary Coordination (IDC)

**Objective:** Coordinate interfaces with adjacent disciplines per Specification.md IF-xx requirements to ensure design integration and resolve conflicts before independent check and approval.

**Actions:**

1. **Prepare for IDC:**
   - Issue drawings for IDC review (electronic copies via project document management system or printed copies per project convention)
   - Prepare interface coordination list identifying specific interface points on drawings (use interface list from Step 3, Item 5 above)
   - Schedule IDC meeting with affected disciplines (coordinate with IDC Coordinator; invite representatives from PKG-05, PKG-07, PKG-14, PKG-17, PKG-20, others as identified)
   - Distribute drawings and interface list in advance of IDC meeting (allow review time — typically 1–2 weeks before meeting)

2. **Conduct IDC review** for each interface (per Specification.md IF-01 through IF-06; refer to Guidance.md §Interface Considerations for coordination details):

   **IF-01: Rail track alignment (PKG-07 Rail Works)**
   - **Drawing Reference:** GA, Arm Arrangement
   - **Coordination Actions:**
     - Confirm station positions relative to track centerline (verify coordinates match PKG-07 track layout drawings; check for any discrepancies)
     - Verify clearances to track (maintain railway clearance envelope — verify no interference with track or railcar envelope)
     - Confirm track curvature effects on station spacing (if track is curved, verify station spacing adjusted appropriately; wider spacing may be required on curves)
     - Verify railcar positioning tolerance (confirm arm reach envelopes (per DEL-10.04) accommodate expected railcar positioning variation — typically ±500mm)
   - **Specification Requirement:** Specification.md IF-01
   - **Resolution:** Document agreements; update drawings if changes required; obtain PKG-07 sign-off on interface coordination

   **IF-02: Structural supports (PKG-05 Concrete Structures / PKG-06 Structural Steelwork)**
   - **Drawing Reference:** All drawings
   - **Coordination Actions:**
     - Confirm foundation locations and elevations for unloading arms (verify locations on Arm Arrangement match PKG-05 foundation plan; verify elevations consistent)
     - Confirm pipe support locations and loads for header piping (coordinate support locations on Header Layout with PKG-05/PKG-06; provide support loads for structural design)
     - Confirm containment structure supports (if containment pans require structural support, coordinate locations and loads with PKG-05)
     - Coordinate seismic design (verify seismic design criteria consistent between process and structural disciplines; BC Building Code requirements; site-specific seismic parameters per PKG-02 geotechnical study)
   - **Specification Requirement:** Specification.md IF-02
   - **Resolution:** Document support locations and loads; update drawings if changes required; obtain PKG-05/PKG-06 sign-off on interface coordination

   **IF-03: Electrical (PKG-17 Electrical)**
   - **Drawing Reference:** Containment Details, GA
   - **Coordination Actions:**
     - Confirm sump pump electrical connections (verify power supply locations on Containment Details; coordinate power requirements with PKG-17 — voltage, power, control)
     - Confirm area lighting requirements (coordinate lighting locations for nighttime operations; verify lighting levels adequate)
     - Confirm hazardous area classification boundaries (if HAC study complete, verify classification zones shown on GA match PKG-17 electrical design; coordinate electrical equipment selection per area classification)
   - **Specification Requirement:** Specification.md IF-03
   - **Resolution:** Document electrical connection points and requirements; update drawings if HAC zones to be shown; obtain PKG-17 sign-off on interface coordination

   **IF-04: Instrumentation (PKG-20 Field Instrumentation)**
   - **Drawing Reference:** GA, Arm Arrangement, Containment Details
   - **Coordination Actions:**
     - Confirm flow indicator locations and mounting at each of 32 stations (verify locations on GA and Arm Arrangement; coordinate instrument type, size, mounting details with PKG-20)
     - Confirm sump level switch locations (verify locations on Containment Details; coordinate level switch type, mounting, set points with PKG-20)
     - Confirm temperature element locations (**if required** for winterization or product quality monitoring; coordinate with PKG-20 if temperature measurement needed)
   - **Specification Requirement:** Specification.md IF-04
   - **Resolution:** Document instrument locations and types; update drawings if mounting details to be shown; obtain PKG-20 sign-off on interface coordination

   **IF-05: Process piping (PKG-14 Process Piping)**
   - **Drawing Reference:** Header Pipe Layout
   - **Coordination Actions:**
     - Confirm header discharge connection to downstream piping network (verify connection size, location, elevation on Header Layout matches PKG-14 piping layout; check for any conflicts)
     - Coordinate downstream piping layout (avoid conflicts between unloading area and downstream piping; verify routing compatible)
     - Coordinate isolation valve locations at responsibility boundary (confirm valve at connection point; clarify responsibility: PKG-10 installs isolation valve, PKG-14 takes over downstream of valve)
   - **Specification Requirement:** Specification.md IF-05
   - **Resolution:** Document connection details and responsibility boundary; update drawings if changes required; obtain PKG-14 sign-off on interface coordination

   **IF-06: Other interfaces (identify as applicable)**
   - **Example:** Control systems PKG-21 (if automated control), fire protection PKG-XX (if fire protection systems interface with unloading area), site utilities PKG-XX (if utility connections required)
   - **Coordination Actions:** Identify interface requirements; coordinate interface details; document agreements
   - **Specification Requirement:** Specification.md IF-06 (**TBD** — additional interface requirements per ER)
   - **Resolution:** Document interface coordination; update drawings if required; obtain sign-offs

3. **IDC meeting / comment resolution:**
   - Conduct IDC meeting (in-person, virtual, or distributed review per project convention)
   - Present drawings and interface points; discuss interfaces with each discipline
   - Document interface agreements and action items (IDC meeting minutes or interface coordination record)
   - Document conflicts requiring resolution (if interface conflicts identified, document conflict, affected disciplines, proposed resolution, responsible party for resolution)
   - Assign responsibilities for conflict resolution (typically discipline lead or design engineer; may require project management decision if conflict cannot be resolved at technical level)
   - Agree on schedule for conflict resolution and re-review (if changes required, agree on timeline for updates and re-submission for IDC review)

4. **Incorporate agreed changes:**
   - Update drawings per IDC agreements (incorporate agreed changes, clarifications, or additions from IDC review)
   - Resolve conflicts per agreed approach (if conflicts identified, implement agreed resolution; may require design changes, coordination with other disciplines, or escalation to project management)
   - Mark interface points as "coordinated" on drawings (or per project convention — e.g., add note "Interface coordinated with PKG-XX" or use coordination symbol)
   - Update cross-references if drawings from other disciplines are referenced (e.g., if PKG-05 foundation drawing number is known, add reference: "See PKG-05 Dwg YYY for foundation details")

5. **Obtain IDC sign-offs:**
   - Prepare IDC sign-off sheet listing all interface disciplines and their sign-off status (use table format with columns: Interface, Discipline/Package, Drawing Reference, Sign-off Status, Signature/Date)
   - Circulate IDC sign-off sheet to all affected disciplines (PKG-05, PKG-07, PKG-14, PKG-17, PKG-20, others as identified)
   - Obtain sign-offs from all interface disciplines (signatures or email confirmations indicating coordination complete and interface accepted)
   - File IDC sign-off sheet in `1_Working/` deliverable folder (retain as record of interface coordination per Specification.md QA-04)

**Output:** IDC-coordinated drawings with all interfaces resolved and signed off by all affected disciplines.

**Verification:** IDC sign-off sheet with signatures from all interface disciplines (Specification.md QA-04).

**Conflict Escalation:** If conflicts cannot be resolved at IDC level (technical disagreement, schedule conflict, cost impact requiring management decision), escalate to project management or technical authority for ruling per project procedures. Document conflict, positions of affected disciplines, and recommendation. Obtain ruling and incorporate into drawings. Re-circulate for IDC sign-off if ruling affects other disciplines.

---

### Step 5: Independent Check and Approval

**Objective:** Verify drawing quality, accuracy, and compliance through independent review and obtain discipline lead approval.

**Actions:**

1. **Issue drawings to independent checker:**
   - Assign checker (must be independent from originator per Specification.md QA-03 — different person than design engineer who produced drawings)
   - Provide checker with complete review package:
     - Drawings (all sheets in drawing set — GA, Arm Arrangement, Header Layout, Containment Details)
     - Specification.md (requirements to be verified against drawings)
     - Guidance.md (principles and considerations to be verified)
     - Datasheet.md (metadata and attributes to be verified)
     - DEL-10.03 (calculations for verification — header sizes, containment volumes, throughput)
     - IDC sign-off sheet (interface verification record)
     - Project CAD standard (for CAD compliance check)
     - Applicable codes and standards (per Specification.md §Standards — for code compliance check)

2. **Checker reviews drawings** against all requirements (refer to Specification.md §Verification for verification matrix):

   **a) Specification.md requirements:**
   - **FN-01 through FN-06:** Functional requirements
     - Verify all 7 PKG-10 scope elements depicted on appropriate drawings (unloading arms, quick-connects, gravity flow header, spill containment pans, collection system, atmospheric venting, flow indicators)
     - Verify all anticipated drawing types produced (GA, Arm Arrangement, Header Layout, Containment Details)
     - Verify 32 unloading positions shown with clearances and reach envelopes
     - Verify gravity flow header shown with sizes, slopes (minimum 1:100), connections, valves
     - Verify containment system shown with volume verification (reference to DEL-10.03)
   - **PF-01 through PF-04:** Performance requirements
     - Verify design supports 1,000,000 MT/annum throughput (cross-check with DEL-10.03 throughput analysis)
     - Verify header sizing supports required performance (cross-check header pipe sizes on drawings with DEL-10.03 calculations; verify sizes match)
     - Verify containment volume adequate (cross-check containment pan volumes on drawings with DEL-10.03 containment calculations; verify volumes adequate for largest credible spill)
   - **IF-01 through IF-06:** Interface requirements
     - Verify interfaces coordinated and marked on drawings (check IDC sign-off sheet; verify all interface disciplines signed off)
     - Verify interface points clearly marked on drawings (PKG-07 track alignment, PKG-05 supports, PKG-17 electrical, PKG-20 instrumentation, PKG-14 piping connection)
   - **QA-01 through QA-06:** Quality requirements
     - Verify CAD standard compliance (see item b below)
     - Verify drawing metadata complete (see item d below)
     - (QA-03 is this step — independent check)
     - Verify IDC performed and signed off (check IDC sign-off sheet)

   **b) Guidance.md principles:**
   - Verify **gravity flow design** principle applied: slopes shown (minimum 1:100), elevations ensure drainage, air release provisions at high points, no stagnant zones
   - Verify **spill containment** principle applied: all unloading areas have containment, pan arrangement shown, collection system shown, volume adequate
   - Verify **operational access** principle applied: access routes shown, clearances adequate, maintenance access provided
   - Verify **equipment spacing** principle applied: 32 stations arranged per railcar spacing, arm reach envelopes adequate, track curvature accounted for
   - Verify **atmospheric venting** principle applied: vent connections shown, vapor management addressed
   - Verify **flow indication** principle applied: flow indicators shown at each of 32 stations

   **c) CAD standard compliance:**
   - Verify line weights per standard (different line weights for object lines, dimension lines, centerlines, hidden lines per CAD standard)
   - Verify text styles per standard (text height readable at drawing scale, font per standard)
   - Verify layers per standard (correct layer usage for different drawing elements — e.g., equipment on equipment layer, piping on piping layer, dimensions on dimension layer)
   - Verify symbology per standard (standard symbols used for equipment, valves, instruments, etc.; symbols per CAD standard legend)
   - Verify title block format and content per standard (all required fields present, format matches CAD standard template)
   - Verify drawing sheet organization and layout (clear layout, not cluttered, logical organization, legend provided if symbols used)

   **d) Dimensional accuracy and cross-references:**
   - Verify dimensions are correct and consistent across drawings (station spacing, header pipe sizes, containment pan dimensions, clearances)
   - Verify cross-references point to correct drawings/sections (e.g., "See Dwg X" — verify Dwg X exists and shows referenced detail; verify drawing number correct)
   - Verify equipment tags match data sheets (check tags on drawings against DEL-10.04 data sheets; verify consistency)
   - Verify pipe sizes match calculations (check header pipe sizes on Header Layout against DEL-10.03 calculations; verify sizes consistent)
   - Verify containment volumes match calculations (check containment pan volumes on Containment Details against DEL-10.03 calculations; verify volumes adequate)
   - Verify elevations and slopes correct (check header profile elevations and slopes on Header Layout; verify slopes minimum 1:100 as required)

   **e) Constructability and clarity:**
   - Verify drawings are clear and unambiguous for construction use (contractor can build from these drawings without excessive RFIs)
   - Verify sufficient detail for construction without over-specification (focus on contractor-installed work; vendor details per DEL-10.04)
   - Verify no conflicts or contradictions within drawing set (no dimension conflicts, no contradictory notes, no conflicting details between drawings)
   - Verify notes and references are clear (notes are clear and unambiguous, references are correct and complete)

3. **Document checker comments:**
   - Checker marks up drawings with comments (electronic mark-ups or hardcopy redlines per project convention)
   - Checker prepares comment list or check sheet (list of all comments with comment number, drawing reference, comment description, severity — error/omission/clarification/suggestion)
   - Checker identifies comment severity:
     - **Errors:** Must correct before issue (dimensional errors, calculation errors, code violations, safety issues)
     - **Omissions:** Must add before issue (missing scope elements, missing interface points, missing metadata)
     - **Clarifications:** Should improve for clarity (unclear notes, missing dimensions where helpful, ambiguous references)
     - **Suggestions:** Optional improvements (alternative approaches, optimization suggestions, constructability improvements)

4. **Resolve checker comments:**
   - Design engineer reviews checker comments (review comment list and marked-up drawings)
   - Resolve all "errors" and "omissions" comments (correct errors, add missing content; these are mandatory before issue)
   - Address "clarifications" and "suggestions" as appropriate (improve clarity where checker identified ambiguity; consider suggestions if beneficial and within scope)
   - Update drawings with agreed changes (incorporate corrections, additions, clarifications)
   - Respond to checker on disposition of each comment (prepare comment response log: comment number, disposition — accepted/revised/rejected, explanation if rejected or revised differently than suggested)

5. **Obtain checker sign-off:**
   - Checker reviews comment dispositions and updated drawings (verify all critical issues resolved; verify updates address comments satisfactorily)
   - Checker confirms all critical issues resolved (errors and omissions corrected; clarifications addressed)
   - Checker signs off on drawings (sign-off on title block or separate sign-off sheet per project convention — Specification.md QA-03)
   - File checker sign-off record in `1_Working/` (checker signature/date, comment resolution record)

6. **Submit for discipline lead approval:**
   - Provide discipline lead with complete approval package:
     - Checked drawings (with checker sign-off on title block or separate sheet)
     - Specification.md (requirements verified by checker)
     - IDC sign-off sheet (interfaces coordinated)
     - Checker comment resolution record (all comments addressed)
     - DEL-10.03 calculations (support for design)
   - Discipline lead reviews for:
     - **Technical adequacy:** Design is technically sound, meets project objectives (OBJ-1, OBJ-2, OBJ-4, OBJ-7), complies with codes and standards
     - **Compliance with ER and project requirements:** Design meets Employer's Requirements (Specification.md requirements derived from ER)
     - **Completeness of drawing set:** All scope elements covered, all anticipated artifacts produced, no gaps in scope
     - **Appropriateness for issue:** Drawings ready for intended use (construction, coordination, regulatory approvals as applicable), quality adequate for project stage (30% / 60% / 90% / IFC)

7. **Obtain discipline lead approval sign-off:**
   - Discipline lead signs approval (sign-off on title block or separate sign-off sheet per project convention — Specification.md QA-05)
   - Approval sign-off confirms drawings approved for issue (technical adequacy confirmed, ER compliance confirmed, completeness confirmed)
   - File approval record in `1_Working/` (discipline lead signature/date)

**Output:** Approved drawings ready for issue with all sign-offs obtained (originator, checker, approver).

**Verification:**
- Checker sign-off (Specification.md QA-03) — confirming independent check performed and critical issues resolved
- Discipline lead approval sign-off (Specification.md QA-05) — confirming drawings approved for issue
- Comment resolution record filed (documenting checker comments and their resolution)

---

### Step 6: Issue and Transmittal

**Objective:** Issue drawings per project document control requirements and manage records.

**Actions:**

1. **Finalize drawing metadata** (Datasheet.md §Attributes — verify all metadata complete and current):
   - Verify drawing numbers correct (match approved drawing list from Step 1)
   - Set revision to initial issue (0 or A per project convention **TBD**)
   - Set issue date (current date — date of issue)
   - Verify all sign-offs present: originator (design engineer signature/date on title block), checker (checker signature/date on title block), approver (discipline lead signature/date on title block)
   - Verify title block complete per CAD standard (all required fields populated: project, location, client, contractor, discipline, drawing title, drawing number, scale, date, revision, signatures)
   - Set classification per project requirements (Datasheet.md §Attributes — classification **TBD**, e.g., Proprietary, For Internal Use, Unclassified)

2. **Convert to issue format** per project requirements:
   - **TBD** — Determine issue format per ER or project document control procedure: PDF (typical for transmittal and distribution), native CAD files (typical for contractor use in construction), or both
   - **TBD** — File naming convention per project document control procedure (typically: Project Code - Discipline - Drawing Number - Revision.extension, e.g., "COTF-PR-10-GA-001-0.pdf")
   - Apply document watermark or issue stamp (if required per project — e.g., "ISSUED FOR CONSTRUCTION" stamp; watermark with issue date)
   - Lock or protect issued files per document control procedure (prevent editing of issued files; maintain version control)

3. **Prepare transmittal** per project document control procedure:
   - **TBD** — Transmittal form or cover letter format per project (may be standard form or letter template)
   - List all drawings being issued in transmittal (table format with columns: Drawing Number, Drawing Title, Revision, Date)
   - Identify recipient(s): Employer (DP World Fraser Surrey Inc.), construction contractor (**TBD** if separate from D&B contractor), other disciplines for coordination (PKG-05, PKG-07, PKG-14, PKG-17, PKG-20), document control (for distribution per project distribution matrix)
   - Include transmittal purpose (e.g., "Issued for Construction" at IFC stage, "Issued for Review" at 30% or 60% stage, "Issued for Information" if for coordination only)
   - Obtain document controller sign-off on transmittal (document control verifies transmittal complete and distribution appropriate)

4. **Issue drawings:**
   - Submit drawings and transmittal to document control for distribution (per project document control procedure)
   - Document control distributes per project distribution matrix (Employer, contractor, disciplines, regulatory authorities as applicable, project files)
   - Document control updates document register (record drawing numbers, titles, revisions, issue date, distribution, transmittal number)

5. **File records** per §Records below:
   - **Working records** in `1_Working/` deliverable folder:
     - Approved drawing list (from Step 1)
     - IDC sign-off sheet (from Step 4)
     - Checker comments and resolution record (from Step 5)
     - Approval records (checker sign-off, discipline lead sign-off from Step 5)
     - Transmittal record (copy of transmittal from Step 6)
     - Self-check record (from Step 3)
   - **Review package** in `2_Checking/To/` (if required per project convention for formal reviews at stage gates):
     - Review copies of drawings (may be intermediate versions submitted for review at 30%, 60%, 90% stages)
     - Review comments and responses (if formal review process with Employer review comments)
   - **Issued drawings** in `3_Issued/` folder:
     - Final issued drawings (PDF or native CAD per project requirements)
     - Organized by revision (subdirectories for Revision 0, Revision A, etc., if multiple issues)
     - Transmittal record with issued drawings

6. **Update deliverable status:**
   - **Note:** Status updates are human-managed per project workflow and lifecycle (see `_STATUS.md`)
   - This procedure does not automatically update status
   - **Typical status progression:** OPEN → INITIALIZED (after Pass 1 draft generation by 4_DOCUMENTS agent) → IN_PROGRESS (during Steps 1–5 of this procedure) → CHECKING (during review at Step 5) → ISSUED (after Step 6 completion)
   - Update `_STATUS.md` per project convention and human decision (typically updated by discipline lead or project manager at appropriate milestones)

**Output:** Issued drawings with transmittal record; records filed per document control requirements; document register updated.

**Verification:**
- Document controller confirmation of issue (transmittal acknowledgment, distribution confirmation)
- Transmittal record (documents what was issued, when, to whom, for what purpose)
- Updated document register (confirms drawings registered in project document management system)

**Note for Subsequent Revisions:**
- Subsequent revisions follow similar process (Steps 2–6) with revision control per project procedures:
  - Mark revisions with revision clouds (highlight changes from previous revision)
  - Update revision history in title block (revision number, date, description of change, originator of change)
  - Maintain previous revision files per document control (do not delete or overwrite previous revisions; archive for traceability)
  - Update drawing number suffix for revision (e.g., Revision 0 → Revision 1, or Revision A → Revision B, per project convention)

---

## Verification

**Verification Summary:**

| Step | Verification Activity | Responsible | Record | Specification Link | Datasheet Link |
|------|----------------------|-------------|--------|--------------------|--------------------|
| 1 | Drawing list approval | Discipline lead | Approved drawing list with sign-off | Specification.md FN-02 (anticipated artifacts requirement) | Datasheet.md §Construction (anticipated artifacts) |
| 2 | Draft drawings completion | Design engineer | Draft drawings (all sheets) | Specification.md FN-01 through FN-05 (functional requirements), PF-01 through PF-04 (performance requirements) | Datasheet.md §Construction (drawing content requirements) |
| 3 | Self-check completion | Design engineer | Self-check record (checklist or marked-up review copy) | Specification.md QA-02 (metadata complete) | Datasheet.md §Attributes (metadata requirements) |
| 4 | IDC coordination | IDC coordinator / multi-discipline team | IDC sign-off sheet (all interface disciplines signed) | Specification.md IF-01 through IF-06 (all interface requirements); QA-04 (IDC sign-off required) | Datasheet.md §Construction (interface elements) |
| 5 | Independent check | Checker (independent from originator) | Checker sign-off (title block or separate sheet); comment resolution record | Specification.md QA-03 (independent check requirement) | — |
| 5 | Discipline lead approval | Discipline lead | Approval sign-off (title block or separate sheet) | Specification.md QA-05 (approval requirement) | — |
| 6 | Issue confirmation | Document controller | Transmittal record; document register entry | Specification.md §Documentation (document control requirements) | Datasheet.md §Attributes (issue metadata) |

**Requirement Verification Matrix (Traceability to Specification.md — comprehensive verification):**

| Req ID | Requirement Summary | Verification Step(s) | Verification Method | Record | Guidance Link | Datasheet Link |
|--------|---------------------|---------------------|---------------------|--------|---------------|----------------|
| FN-01 | All PKG-10 scope elements depicted (7 elements) | 2, 3, 5 | Design review; document check; independent check | Drawings showing all elements; checker sign-off | Guidance.md §Principles (all elements addressed) | Datasheet.md §Conditions (all elements listed) |
| FN-02 | Anticipated artifacts included (4 drawing types) | 1, 3 | Document check against approved list | Drawing list; drawings produced; self-check record | Guidance.md §Examples (4 drawing types) | Datasheet.md §Construction (4 drawing types) |
| FN-03 | 32 unloading positions shown with clearances | 2, 3, 5 | Design review; dimensional check; independent check | GA and Arm Arrangement drawings; checker sign-off | Guidance.md §Considerations (32-station layout) | Datasheet.md §Conditions (32 arms) |
| FN-04 | Gravity flow header shown (sizes, slopes, connections) | 2, 3, 5 | Design review; calculation check (DEL-10.03); independent check | Header Layout drawing; DEL-10.03 calculations; checker sign-off | Guidance.md §Principles (gravity flow design) | Datasheet.md §Construction (Header Layout content) |
| FN-05 | Containment system shown with volume verification | 2, 5 | Design review; calculation check (DEL-10.03); independent check | Containment Details drawing; DEL-10.03 calculations; checker sign-off | Guidance.md §Principles (spill containment) | Datasheet.md §Construction (Containment Details content) |
| FN-06 | Additional ER requirements | **TBD** | **TBD** — per ER clauses | **TBD** | **TBD** | — |
| PF-01 | 1,000,000 MT/annum capacity supported | 2, 3, 5 | Design review; throughput analysis (DEL-10.03); independent check | All drawings (32-station layout); DEL-10.03 throughput analysis; checker sign-off | Guidance.md §Principles (OBJ-2) | Datasheet.md §Conditions (throughput parameter) |
| PF-02 | Unloading rate requirements | **TBD** | **TBD** — per ER clauses | **TBD** | Guidance.md §Considerations (performance factors) | — |
| PF-03 | Containment volume requirements met | 2, 5 | Calculation verification (DEL-10.03); independent check | Containment Details drawing; DEL-10.03 containment calculations; checker sign-off | Guidance.md §Principles (OBJ-7) | Datasheet.md §Construction (Containment Details) |
| PF-04 | Header sizing and performance adequate | 2, 5 | Calculation verification (DEL-10.03 — header sizing, hydraulic analysis); independent check | Header Layout drawing; DEL-10.03 header calculations; checker sign-off | Guidance.md §Principles (gravity flow); Guidance.md §Considerations (header design) | Datasheet.md §Construction (Header Layout) |
| IF-01 | Rail track alignment interface coordinated | 4 | IDC review with PKG-07 | IDC sign-off sheet (PKG-07 signed); GA and Arm Arrangement drawings showing interface | Guidance.md §Interface Considerations (PKG-07) | Datasheet.md §Construction (interface table) |
| IF-02 | Structural supports interface coordinated | 4 | IDC review with PKG-05/PKG-06 | IDC sign-off sheet (PKG-05/PKG-06 signed); all drawings showing support locations | Guidance.md §Interface Considerations (PKG-05) | Datasheet.md §Construction (interface table) |
| IF-03 | Electrical interface coordinated | 4 | IDC review with PKG-17 | IDC sign-off sheet (PKG-17 signed); Containment Details and GA showing electrical connections | Guidance.md §Interface Considerations (PKG-17) | Datasheet.md §Construction (interface table) |
| IF-04 | Instrumentation interface coordinated | 4 | IDC review with PKG-20 | IDC sign-off sheet (PKG-20 signed); GA, Arm Arrangement, Containment Details showing instruments | Guidance.md §Interface Considerations (PKG-20) | Datasheet.md §Construction (interface table) |
| IF-05 | Process piping interface coordinated | 4 | IDC review with PKG-14 | IDC sign-off sheet (PKG-14 signed); Header Layout showing piping connection | Guidance.md §Interface Considerations (PKG-14) | Datasheet.md §Construction (interface table) |
| IF-06 | Other interfaces coordinated | 4 | IDC review as identified | IDC sign-off sheet (other disciplines as applicable) | — | — |
| QA-01 | CAD standard compliance | 5 | Independent check (CAD compliance check) | Checker sign-off (CAD standard verified) | Guidance.md §Principles (clarity) | Datasheet.md §Attributes (CAD standard) |
| QA-02 | Drawing metadata complete | 3, 6 | Self-check; document control check | Self-check record; finalized title blocks; transmittal | Guidance.md §Documentation Considerations (metadata) | Datasheet.md §Attributes (all metadata fields) |
| QA-03 | Independent check performed | 5 | Checker review and sign-off | Checker sign-off; comment resolution record | Guidance.md §Principles (completeness, consistency) | — |
| QA-04 | IDC sign-off obtained | 4 | IDC coordination | IDC sign-off sheet (all interface disciplines signed) | Guidance.md §Principles (coordination) | Datasheet.md §Construction (interfaces) |
| QA-05 | Discipline lead approval obtained | 5 | Approval review and sign-off | Approval sign-off | Guidance.md §Principles (completeness) | — |
| QA-06 | Additional ER quality requirements | **TBD** | **TBD** — per ER clauses | **TBD** | — | — |

---

## Records

**Documentation Outputs (Deliverable Artifacts — the drawings produced by this procedure):**

| Record | Description | Filing Location | Specification Link | Datasheet Link | Guidance Link |
|--------|-------------|-----------------|--------------------|--------------------|---------------|
| Unloading System GA | Overall layout drawing(s) showing 32-station layout, header routing, containment, equipment | `3_Issued/` (issued drawings); `1_Working/` (working copies) | Specification.md §Documentation (GA listed) | Datasheet.md §Construction (GA content) | Guidance.md §Examples (GA typical content) |
| Unloading Arm Arrangement | Arm position drawings (multiple sheets for 32 stations) showing arms, clearances, connections | `3_Issued/` (issued drawings); `1_Working/` (working copies) | Specification.md §Documentation (Arm Arrangement listed) | Datasheet.md §Construction (Arm Arrangement content) | Guidance.md §Examples (Arm Arrangement typical content) |
| Header Pipe Layout | Header routing drawing(s) showing piping, sizes, slopes, connections, valves | `3_Issued/` (issued drawings); `1_Working/` (working copies) | Specification.md §Documentation (Header Layout listed) | Datasheet.md §Construction (Header Layout content) | Guidance.md §Examples (Header Layout typical content) |
| Containment Details | Containment system drawings showing pans, sumps, drainage, pumps | `3_Issued/` (issued drawings); `1_Working/` (working copies) | Specification.md §Documentation (Containment Details listed) | Datasheet.md §Construction (Containment Details content) | Guidance.md §Examples (Containment Details typical content) |

**Production Records (Supporting Documentation — records of the drawing production process):**

| Record | Description | Filing Location | Purpose | Specification Link |
|--------|-------------|-----------------|---------|-------------------|
| Approved drawing list | Drawing list with assigned numbers and discipline lead sign-off | `1_Working/` | Step 1 output; traceability to scope; completeness verification | Specification.md FN-02 (drawing list requirement) |
| IDC sign-off sheet | Interface coordination record with signatures from all interface disciplines (PKG-05, PKG-07, PKG-14, PKG-17, PKG-20, others) | `1_Working/` | Step 4 output; interface verification (Specification.md QA-04) | Specification.md QA-04 (IDC requirement); IF-01 through IF-06 (all interfaces) |
| Checker comments and resolution | Checker mark-ups and comment resolution record (comment list, disposition, responses) | `1_Working/` | Step 5 output; quality verification (Specification.md QA-03); demonstrates independent check performed and issues resolved | Specification.md QA-03 (independent check requirement) |
| Checker sign-off | Independent check sign-off (may be on drawing title block or separate sheet) | `1_Working/` or on issued drawings (title block) | Step 5 output; quality verification; confirms independent check complete and drawings approved by checker | Specification.md QA-03 (checker sign-off requirement) |
| Approval sign-off | Discipline lead approval sign-off (may be on drawing title block or separate sheet) | `1_Working/` or on issued drawings (title block) | Step 5 output; approval verification; confirms drawings approved for issue by discipline lead | Specification.md QA-05 (approval requirement) |
| Transmittal record | Issue transmittal form/letter with distribution record and acknowledgments | `1_Working/` or per document control procedures | Step 6 output; issue verification; documents what was issued, when, to whom | Specification.md §Documentation (transmittal requirement) |
| Self-check record | Design engineer self-check completion record or checklist | `1_Working/` | Step 3 output; internal quality check; demonstrates self-check performed | Specification.md QA-02 (completeness check) |

**Record Management:**

| Location | Purpose | Contents | Access |
|----------|---------|----------|--------|
| `1_Working/` | Active working location for deliverable; all production records; working copies | All production records listed above; working copies of drawings (may be multiple iterations); supporting calculations references (DEL-10.03); data sheets references (DEL-10.04); correspondence related to deliverable | Discipline team access (design engineer, checker, discipline lead, IDC coordinator) |
| `2_Checking/To/` | Review packages during formal review cycles (if required per project convention) | Review copies of drawings submitted for formal reviews at stage gates (30%, 60%, 90%); review comments from Employer; review responses | Review team access (Employer, contractor review team, discipline leads) |
| `3_Issued/` | Issued drawings (final approved versions) | Final issued drawings (PDF or native CAD per project requirements); organized by revision (subdirectories for Rev 0, Rev 1, etc., or Rev A, Rev B, etc.); transmittal records with issued drawings | Project-wide access (all disciplines, contractor, Employer, construction team, operations team) |

**Retention Requirements:**
- **TBD** — per project document control procedure and regulatory requirements
- **ASSUMPTION:** Electronic records maintained in project document management system with backup and archival per IT procedures (daily backup, offsite archival)
- **ASSUMPTION:** Minimum retention period aligned with project design life (25–30 years typical per Datasheet.md §Conditions design life **TBD**) and regulatory requirements (building code, environmental regulations may require specific retention periods)
- **ASSUMPTION:** Issued drawings retained permanently for as-built record; working records retained for duration of design and construction phase minimum (may be archived after project completion)

**Traceability:**
- All records linked to deliverable ID (DEL-10.01) per Datasheet.md §Identification
- Drawing numbers traceable to approved drawing list (Step 1)
- Revisions traceable through revision history in title block and document register (each revision documented with number, date, description, originator)
- Interfaces traceable through IDC sign-off sheet linking to other package deliverables (PKG-05, PKG-07, PKG-14, PKG-17, PKG-20)
- Requirements traceable through verification matrix (each requirement linked to verification step, method, record)

**Pass 3 Final Verification:** All procedure steps aligned with Specification requirements, Guidance principles, and Datasheet attributes; all cross-references bidirectional and verified; all TBDs and ASSUMPTIONs properly marked and sourced; terminology consistent across all four documents (Datasheet, Specification, Guidance, Procedure).
