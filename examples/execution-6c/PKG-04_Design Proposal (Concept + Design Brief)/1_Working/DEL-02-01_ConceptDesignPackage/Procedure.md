# Procedure: DEL-02-01 Concept Design Package

## Purpose

This procedure defines the process for **producing** the Concept Design Package deliverable (DEL-02-01) for the Penhold Public Services Building RFP proposal. It guides the Lead Architect / Designer and supporting team members through concept development, drawing production, and deliverable completion to meet acceptance criteria and support proposal evaluation.

**Scope:** This procedure addresses deliverable production (for the proposal team), not operation/use (as there is no operational "use" of a design package beyond review and evaluation).

**Source:** Protocol Step 4d (Procedure.md interpretation rule: production of deliverable artifact)

---

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED

**Note:** Dependencies are coordinated externally by humans (see `_DEPENDENCIES.md` and execution/_Coordination/_COORDINATION.md for schedule-first coordination approach).

**Expected Inputs (coordination responsibility):**
- Access to RFP and addenda (available in `_Sources/` directory)
- Access to site reference materials (geotechnical, wetland, flood zone, grading, subdivision context)
- Functional Program (Appendix B of RFP) — room list and program requirements
- Owner Statement of Requirements (Appendix A of RFP) — performance objectives and constraints
- Coordination with PKG-02 (Financial Proposal) team for cost implications and scope alignment
- Coordination with PKG-04 other deliverables (DEL-02-02 Design Brief, DEL-02-03 Sustainability Narrative) for narrative consistency

**Source:** _DEPENDENCIES.md (NOT_TRACKED mode); _REFERENCES.md (reference materials inventory)

---

### Reference Materials

The following reference materials must be accessible before beginning concept design work:

**Primary Sources:**
1. **RFP Document:** AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf
   - Location: /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Sources/
   - Required sections: Appendix A (OSR), Appendix B (Functional Program), Section 7.1 (design requirements)

2. **Addendum 01:** AB-2024-07156-Penhold_Public Services Building Addendum01.pdf
   - Location: /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Sources/
   - Key content: Room dimension flexibility clarification

3. **Addendum 03:** AB-2024-07156-Penhold_Public Services Building Addendum03.pdf
   - Location: /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Sources/
   - Key content: 12-acre developable site, pickled sand storage removal, technical requirements (doors, sumps, exhaust, generator, fill stations, solar)

**Site Context Sources:**
4. **Site Grading:** AB-2024-07156-Penhold PSB_Site grading.pdf
5. **Adjacent Subdivision Design:** AB-2024-07156-Penhold PSB_Adjacent Subdivision Design.pdf
6. **Flood Zone Mapping:** AB-2024-07156-Penhold PSB_parcel flood zone.pdf
7. **Geotechnical Investigation Report:** AB-2024-07156-Penhold PSB_Geotechnical Investigation Report.pdf
8. **Wetland Assessment:** AB-2024-07156-Penhold PSB_Wetland Assessment.pdf

**Project Context:**
9. **Decomposition Document:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md
10. **Deliverable Context File:** _CONTEXT.md (this deliverable folder)
11. **Four Documents (this set):** Datasheet.md, Specification.md, Guidance.md, Procedure.md (for cross-reference during production)

**Source:** _REFERENCES.md; Protocol Step 1 (Read Context)

---

### Tools and Resources

**Design Tools:**
- CAD software (AutoCAD, Revit, or equivalent) for plan, section, elevation production
- 3D modeling software (SketchUp, Rhino, Revit, or equivalent) for massing studies
- Graphics software (Adobe Illustrator, InDesign, or equivalent) for drawing composition and annotation
- PDF export tools for deliverable assembly

**Reference Tools:**
- Alberta Building Code 2019 (digital or print)
- National Building Code of Canada (NBC)
- National Fire Code of Canada (NFC)
- Accessibility standards (CSA B651 or ABC Part 3)

**Collaboration Tools:**
- Shared file repository for drawings and narratives (coordination with other PKG-04 deliverables)
- Review/markup tools for internal QA and cross-deliverable consistency checks

**[X-001 Enrichment — Resource Verification]** Before Step 1 begins, confirm tool availability: (1) CAD (AutoCAD/Revit), (2) 3D modeling (SketchUp/Rhino/Revit), (3) PDF export tools, (4) Shared file repository. If unavailable, escalate to Proposal Manager for procurement or approve alternate tool. Source: _SEMANTIC_LENSING.md Item X-001 (Matrix X: guiding:necessity).

**Source:** ASSUMPTION: Standard architectural design practice for proposal-stage concept development

---

### Team Roles and Responsibilities

| Role | Responsibility | Availability Requirement |
|------|----------------|--------------------------|
| **Lead Architect / Designer** | Overall concept design leadership; drawing production; compliance oversight | Primary assignment for DEL-02-01 duration |
| **Site Planner / Civil Engineer** | Site concept plan; grading and drainage strategy; service routing | Coordination input as needed |
| **Structural Engineer** | Preliminary structural system recommendations; long-span bay structure; solar-ready roof provisions | Coordination input as needed |
| **Mechanical Engineer** | Space allocation for exhaust system; generator sizing estimate; HVAC strategy | Coordination input as needed |
| **Electrical Engineer** | Generator sizing and location; solar-ready electrical provisions | Coordination input as needed |
| **Code Consultant** | Building code review; occupancy classification; egress and accessibility compliance check | Coordination input as needed |
| **Proposal Manager** | Coordination with other packages; submission format compliance; schedule management | Oversight and coordination throughout |

**Source:** _CONTEXT.md (Responsible Party: Lead Architect / Designer); ASSUMPTION: Typical design team structure for integrated facility

---

## Steps

### Step 1: Review and Extract Requirements

**Objective:** Understand the full scope of requirements, constraints, and evaluation criteria before beginning design work.

**Actions:**

1.1. **Read the Four Documents (Datasheet, Specification, Guidance, Procedure)** in this deliverable folder to understand the compiled requirements, principles, and context.

1.2. **Review RFP Appendix A (Owner Statement of Requirements)** to extract:
   - Project objectives and owner priorities
   - Performance expectations (operational effectiveness, durability, maintainability)
   - Functional relationships and workflow requirements
   - Any explicit design constraints (height limits, setbacks, material preferences)

   **[B-004 Enrichment]** If RFP and Addenda conflict: Addendum 03 supersedes all; Addendum 02 supersedes Addendum 01; Addendum 01 supersedes base RFP (per Decomposition §2, Source Documents authority order). Document any conflicts on requirements checklist for Proposal Manager review. Source: _SEMANTIC_LENSING.md Item B-004 (Matrix B: knowledge:completeness).

1.3. **Review RFP Appendix B (Functional Program)** to extract:
   - Complete room list (Fire Hall spaces and Public Works spaces)
   - Room sizes (where specified) and Addendum 03 sample ranges (where provided)
   - Functional adjacency requirements (which spaces must be near each other)
   - Special room requirements (apparatus bays, ICP/meeting room, locker rooms, etc.)

1.4. **Review Addenda 01, 02, 03** to confirm all clarifications and amendments are captured:
   - Room dimension flexibility (Addendum 01)
   - 12-acre developable area; pickled sand storage removal (Addendum 03)
   - Technical requirements: 16 ft doors, bay sumps, exhaust, generator, fill stations, solar-ready roof (Addendum 03)

1.5. **Review site reference materials** (grading, flood zone, geotechnical, wetland, subdivision context) to identify:
   - Site boundary and developable area limits
   - Topography and drainage patterns
   - Soil conditions and foundation implications
   - Environmental constraints (wetlands, flood fringe)
   - Adjacent development context and access points

1.6. **Create a requirements checklist** (working document) to track compliance with:
   - Specification requirements R1–R15 (including R15 Regulatory Audit, R3-R8 System Integration)
   - Addendum 03 technical requirements (doors, sumps, exhaust, generator, fill stations, solar)
   - Acceptance criteria from _CONTEXT.md (program fit, pickled sand exclusion, Addendum 03 incorporation)

   **[X-002 Enrichment]** Checklist format: Spreadsheet with columns (Requirement ID | Statement | Verification Method | Status [Not Started / In Progress / Complete] | Notes). Checklist updated at end of each design step (Steps 2-8). Step 9 QA reviews checklist for completeness before delivery. Source: _SEMANTIC_LENSING.md Item X-002 (Matrix X: applying:sufficiency).

**Verification:** Requirements checklist complete and reviewed with Proposal Manager.

**Records:** Requirements checklist (working document, not a formal deliverable but retained for reference).

**[C-003 Enrichment — Error Handling]** If Step 1 prerequisite cannot be completed (e.g., RFP Appendix B missing, Town bylaws unavailable), escalate to Proposal Manager with: (1) missing information, (2) estimated impact on deliverable, (3) recommended path (proceed with assumption vs. defer). Proposal Manager rules on proceeding or halting work. Source: _SEMANTIC_LENSING.md Item C-003 (Matrix C: operative:completeness).

**Source:** Specification §Scope and §Requirements; Protocol Step 1 (Read Context)

---

### Step 2: Develop Site Concept

**Objective:** Establish building placement, site access, parking, and site improvements within the 12-acre developable area.

**Actions:**

2.1. **Prepare site base plan:**
   - Overlay site boundary (20-acre parcel) on CAD base
   - Delineate flood fringe area (8 acres for dog park/storm pond) using flood zone mapping
   - Delineate 12-acre developable area boundary (bold line)
   - Show existing site features: topography (contours or spot elevations), wetland areas, access points, adjacent streets/development

2.2. **Establish building orientation and placement:**
   - Position building within developable area
   - Orient apparatus bays for efficient emergency egress (typically toward primary street access)
   - Consider solar orientation for roof (south-facing preferred for solar readiness)
   - Maintain required setbacks from property lines (TBD: confirm from Town of Penhold bylaws)
   - Avoid wetland areas and minimize disturbance to environmentally sensitive zones

2.3. **Develop circulation and parking layout:**
   - Show primary access drive(s) from public street(s)
   - Design apparatus bay apron (clear egress path for fire apparatus; no obstructions)
   - Design public works equipment yard (vehicle circulation, equipment storage/parking)
   - Locate staff parking areas (Fire Hall and Public Works personnel; accessible parking spaces)
   - Show pedestrian access and accessible routes from parking to building entrances
   - Design service/delivery access (separate or shared with operational access)

2.4. **Locate site features and systems:**
   - Emergency generator location (fuel access, noise setback, maintenance clearance)
   - Fill station location(s) (accessible to fire apparatus and public works vehicles; circulation clearances)
   - Storm water management (direction of drainage; tie-in to storm pond in flood fringe area)
   - Site lighting (indicate schematically; detailed design TBD)
   - Fencing/gates for secure areas (if required for public works yard)

2.5. **Indicate site services routing (conceptual):**
   - Municipal water service entry point
   - Sanitary sewer service exit point
   - Storm sewer routing to pond
   - Electrical service entry (overhead or underground)
   - Natural gas service (if applicable)
   - Telecom/data service
   - Note: Detailed service design and tie-in costs addressed via allowance approach (per Addendum 03 clarification; see Specification R13)

2.6. **Annotate site concept plan:**
   - Label 12-acre developable area boundary and flood fringe area
   - Dimension key site features (building setbacks, parking spaces, drive aisles)
   - Provide site area summary (total site, developable area, building footprint, paved areas)
   - Add legend and north arrow

**Verification:** Site concept reviewed with Civil Engineer and Proposal Manager for constructability, cost implications, and compliance with site constraints.

**Records:** Site concept plan drawing (CAD file and PDF export).

**Source:** Specification R2 (site developable area), R6 (generator), R7 (fill stations), R13 (site services); Guidance §Considerations (Site Access and Circulation)

---

### Step 3: Develop Building Concept Plan

**Objective:** Layout all program spaces in a functional arrangement that demonstrates program fit, code compliance, and operational effectiveness.

**Actions:**

3.1. **Organize functional zones:**
   - Fire Hall zone: Apparatus bays, turnout gear storage, staff areas (offices, day room, kitchen, washrooms, sleeping quarters if applicable), meeting room (doubles as ICP)
   - Public Works zone: Vehicle/equipment bays, workshop, staff areas (offices, break room, washrooms, locker rooms), storage areas
   - Shared/core areas (if applicable): Mechanical/electrical rooms, entry/lobby, shared meeting spaces

3.2. **Layout apparatus bays (Fire Hall):**
   - Number of bays per Functional Program (Appendix B room list; TBD: requires PDF access)
   - Bay dimensions: width and depth to accommodate apparatus (typical: 14–16 ft wide x 50–70 ft deep per bay; confirm with OSR or fire apparatus specs)
   - Overhead door locations (16 ft clear height minimum per Addendum 03)
   - Indicate bay sump locations (floor drains for wash-down; per Addendum 03)
   - Show space allocation for fire apparatus exhaust system (ceiling-mounted or overhead; per Addendum 03)
   - Show personnel access doors from bays to staff areas (turnout gear storage immediately adjacent to bays)

3.3. **Layout public works vehicle/equipment areas:**
   - Vehicle/equipment bay(s): dimensions to accommodate trucks, loaders, graders, etc. (sizes TBD: confirm with Public Works vehicle inventory from OSR)
   - Workshop space: workbenches, tools, parts storage
   - Overhead door(s) for vehicle entry/exit (height TBD based on largest equipment; likely similar to fire apparatus: 14–16 ft)

3.4. **Layout staff areas (Fire Hall):**
   - Offices (Fire Chief, officers, admin)
   - Day room / kitchen (firefighter common area)
   - Washrooms and showers (gender-neutral or separated; confirm with OSR)
   - Locker rooms (turnout gear storage + personal lockers)
   - Sleeping quarters (if 24/7 staffing; confirm with OSR)
   - Meeting room (doubles as Incident Command Post; generator must support ICP per Addendum 03)

3.5. **Layout staff areas (Public Works):**
   - Offices (Public Works director, supervisors, admin)
   - Break room / lunchroom
   - Washrooms and showers (for staff returning from field work)
   - Locker rooms (work gear, personal storage)
   - Storage (parts, supplies, seasonal equipment)

3.6. **Layout building support spaces:**
   - Mechanical room(s) (HVAC equipment, boiler/furnace, air handling units)
   - Electrical room(s) (panels, emergency generator connection, future solar PV interconnection provisions)
   - IT/telecom room (servers, network equipment)
   - Janitorial closets
   - Storage rooms (general, seasonal)

3.7. **Design circulation and egress:**
   - Primary entry/exit for each functional zone (Fire Hall entry, Public Works entry; may be shared or separate)
   - Accessible routes from entry to all public and staff areas
   - Egress paths meeting building code requirements (exit travel distances, exit widths, exit signage)
   - Fire separations (if required between Fire Hall and Public Works occupancies; TBD: requires code analysis)

3.8. **Verify program fit:**
   - Cross-check floor plan against Functional Program (Appendix B) room list
   - Confirm all required spaces are included and dimensioned reasonably
   - Compare room sizes to Addendum 03 sample ranges (where provided)
   - **[F-002 Enrichment]** For rooms with Addendum 03 sample ranges, verify sizing compliance. For rooms without sample ranges, verify compliance with Alberta Building Code space requirements (minimum dimensions for egress, clearances, accessibility) using code reference (e.g., ABC §3.3.1). Document sizing basis on floor plan legend. Source: _SEMANTIC_LENSING.md Item F-002 (Matrix F: normative:sufficiency).
   - Confirm no pickled sand storage building is shown (excluded scope per Addendum 03)

3.9. **Annotate floor plan:**
   - Label all rooms (function and approximate dimensions)
   - Show door swings and locations
   - Indicate accessible routes (accessible parking to accessible entrance to key spaces)
   - Dimension key spaces (apparatus bays, major rooms)
   - Add legend, north arrow, and scale

**Verification:** Concept plan reviewed with Code Consultant for egress and accessibility compliance; reviewed with Fire Chief (or OSR representative, if available) for operational workflow.

**Records:** Concept floor plan(s) drawing (CAD file and PDF export).

**Source:** Specification R1 (program fit), R3 (door height), R4 (bay sumps), R5 (exhaust system), R6 (generator supports ICP), R10 (room flexibility), R11 (code compliance), R12 (accessibility); Guidance §Principles (Functional Clarity)

---

### Step 4: Develop Building Massing and Roof Concept

**Objective:** Show building form, scale, and roof design to support solar readiness and architectural character.

**Actions:**

4.1. **Create 3D massing model:**
   - Model building footprint and height based on concept floor plan
   - Show single-story vs. two-story zones (if applicable; typically fire halls and public works are single-story for operational efficiency)
   - Model roof form: flat, gable, hip, or hybrid (consider solar orientation, drainage, and aesthetic character)

4.2. **Design roof for solar readiness:**
   - If sloped roof: Orient primary roof planes toward south for optimal solar access
   - If flat roof: Indicate structural provisions for tilted PV array racks
   - Note roof structure must support future PV panel loads (snow, wind, dead load; per Addendum 03)
   - Show roof area available for PV (estimate in square feet or percentage of roof area)

4.3. **Develop massing views:**
   - Produce 3D perspective views (eye-level and aerial) showing building form and context
   - Show building in site context (adjacent development, street frontage)
   - Indicate general material character (e.g., "Exterior: masonry and metal siding" — detailed materials in Design Brief DEL-02-02)

4.4. **Document massing study:**
   - Export massing views as images
   - Annotate with key dimensions (building length, width, height)
   - Add brief description of form rationale (e.g., "Building form provides functional separation of Fire Hall and Public Works zones while sharing central mechanical/electrical core")

**Verification:** Massing reviewed with Proposal Manager and Structural Engineer for feasibility and cost implications.

**Records:** Building massing study (3D model file and exported images with annotations).

**Source:** Specification R8 (solar-ready roof); Guidance §Considerations (Solar-Ready Roof Orientation); Guidance §Trade-offs (Roof Form)

---

### Step 5: Develop Key Sections

**Objective:** Show vertical relationships and critical dimensions, particularly apparatus bay overhead door height.

**Actions:**

5.1. **Identify section cut locations:**
   - Section through apparatus bays (to show 16 ft clear door height and roof structure)
   - Section through staff areas (to show ceiling heights and any multi-story zones)
   - Section through site (if significant grade change)

5.2. **Draw building sections:**
   - Show floor-to-floor heights (slab to underside of structure)
   - Show apparatus bay overhead door (dimension 16 ft clear height prominently)
   - Show roof structure and form
   - Show foundation (schematic; detailed foundation design TBD pending geotechnical recommendations)
   - Indicate space for exhaust system above apparatus bays (if ceiling-mounted)

5.3. **Annotate sections:**
   - Dimension key heights (floor level, door height, eave/parapet height)
   - Label major spaces
   - Add scale and section cut reference

**Verification:** Sections reviewed with Structural Engineer for constructability and proportionality.

**Records:** Key section drawings (CAD file and PDF export).

**Source:** Specification R3 (16 ft overhead door height); Specification R5 (exhaust system space)

---

### Step 6: Develop Key Elevations

**Objective:** Show external appearance and material character for all building facades.

**Actions:**

6.1. **Draw building elevations (all four sides recommended):**
   - Front elevation (primary public-facing facade; typically apparatus bay side for fire hall)
   - Rear elevation
   - Left and right side elevations

6.2. **Indicate key features:**
   - Overhead doors (apparatus bays, public works bays)
   - Personnel entry doors
   - Windows (sizes and locations; daylighting and views)
   - Roof form and parapets
   - Material transitions (e.g., masonry base, metal siding upper walls; detailed in Design Brief DEL-02-02)

6.3. **Annotate elevations:**
   - Label key features (e.g., "Apparatus Bay Overhead Door (16 ft clear)")
   - Indicate approximate floor and roof heights (datum elevation or height above grade)
   - Add scale and north arrow reference

**Verification:** Elevations reviewed with Proposal Manager for alignment with Design Brief material and aesthetic narrative (DEL-02-02).

**Records:** Key elevation drawings (CAD file and PDF export).

**Source:** _CONTEXT.md (Anticipated Artifacts: elevations); Guidance §Principles (Functional Clarity Over Aesthetic Refinement)

---

### Step 7: Prepare Concept Design Narrative

**Objective:** Provide written context and rationale to accompany concept drawings, addressing compliance and technical requirements.

**Actions:**

7.1. **Draft narrative sections:**

   **Section A: Introduction and Design Intent**
   - Brief project overview (integrated Fire Hall + Public Works facility for Town of Penhold)
   - Design intent statement (functional efficiency, operational effectiveness, community identity)

   **Section B: Program Fit and Functional Organization**
   - Summary of program spaces (Fire Hall zone, Public Works zone, shared/core areas)
   - Functional adjacencies and circulation rationale (e.g., "Apparatus bays open directly to turnout gear storage for rapid emergency response")
   - Confirmation that all Functional Program (Appendix B) spaces are accommodated

   **Section C: Site Concept and Constraints**
   - 12-acre developable area compliance (building and site improvements within boundary)
   - Flood fringe area acknowledgment (8 acres designated for dog park and storm pond; not in building scope)
   - Site access and circulation strategy (emergency apparatus egress, public works yard operations, staff parking)
   - Response to site conditions (geotechnical, wetland, grading)

   **Section D: Addendum 03 Technical Requirements**
   - 16 ft overhead door height: "Apparatus bay overhead doors provide 16 ft clear height to accommodate current and future fire apparatus."
   - Bay sumps: "Floor drainage sumps are provided in all apparatus bays for vehicle wash-down and fluid containment."
   - Fire apparatus exhaust: "Space is allocated for a ceiling-mounted fire apparatus exhaust capture system in apparatus bays."
   - Generator: "Emergency generator is located [site location] and sized to support the Incident Command Post (meeting room) and critical building systems (detailed load analysis TBD)."
   - Fill stations: "Vehicle fill station(s) are located [site location] with access for both fire apparatus and public works equipment."
   - Solar-ready roof: "Roof is designed with [south-facing slopes / flat roof with structural capacity] to accommodate future photovoltaic (PV) panel installation."

   **Section E: Code Compliance Approach**
   - Building code compliance strategy (Alberta Building Code 2019; occupancy classifications TBD)
   - Egress and life safety (exit paths, travel distances, fire separations as required)
   - Accessibility (accessible parking, routes, entrances, washrooms; universal design principles)

   **Section F: Exclusions and Assumptions**
   - Pickled Sand Storage Building excluded (per Addendum 03)
   - Concept-level detail (detailed engineering and code analysis to follow post-award)
   - Room dimensions are approximate and subject to refinement during detailed design

7.2. **Cross-reference narrative to drawings:**
   - Ensure narrative descriptions match drawing content (e.g., if narrative says "Generator located on west side of building," confirm this is shown on site plan)
   - Reference drawing numbers/titles in narrative where applicable

**Verification:** Narrative reviewed with Proposal Manager for consistency with Design Brief (DEL-02-02) and Sustainability Narrative (DEL-02-03).

**Records:** Concept Design Narrative (Word or PDF document).

**Source:** Specification §Documentation (Concept Design Narrative); Guidance §Principles (Compliance Transparency, Integration of Addendum 03 Technical Requirements)

---

### Step 8: Assemble Deliverable Package

**Objective:** Compile all drawings and narrative into a cohesive deliverable package suitable for inclusion in the proposal PDF.

**Actions:**

8.1. **Prepare drawing set:**
   - Arrange drawings in logical order:
     1. Site concept plan
     2. Concept floor plan(s)
     3. Building massing study (3D views)
     4. Key sections
     5. Key elevations
   - Apply consistent title blocks, scales, and annotation styles
   - Add drawing list/index if needed

8.2. **Export drawings to PDF:**
   - Export each drawing as a high-resolution PDF (suitable for proposal PDF assembly)
   - Confirm all text is legible and dimensions are clear
   - Optimize file sizes (balance quality with proposal 15 MB size limit)

8.3. **Finalize narrative document:**
   - Format narrative for proposal consistency (fonts, headings, page layout)
   - Include drawing references or thumbnails if helpful
   - Export narrative to PDF

8.4. **Create deliverable cover/summary:**
   - Title page: "DEL-02-01 Concept Design Package — Penhold Public Services Building"
   - Table of contents (if deliverable is multi-page)
   - Deliverable summary (1-paragraph overview of concept design approach)

8.5. **Package files:**
   - Combine all PDFs into a single DEL-02-01 package (or keep as separate files for proposal assembly team; coordinate with Proposal Manager)
   - Archive source CAD files and 3D models for future reference and post-award detailed design

**Verification:** Deliverable package reviewed against Acceptance Criteria (_CONTEXT.md):
   - Program fit demonstrated? (Yes/No)
   - Excludes removed pickled sand storage? (Yes/No)
   - Incorporates Addendum 03 requirements? (Yes/No — checklist verification)

**Records:** Deliverable package (PDF set + source files archive).

**Source:** Decomposition §3 (C-01: proposal PDF size limit); _CONTEXT.md (Acceptance Criteria)

---

### Step 9: Internal QA and Cross-Deliverable Consistency Check

**Objective:** Verify deliverable completeness, accuracy, and consistency with related deliverables before final submission to Proposal Manager.

**Actions:**

9.1. **Self-review checklist:**
   - All drawings complete and annotated? (site plan, floor plan, massing, sections, elevations)
   - All Addendum 03 technical requirements addressed? (16 ft doors, sumps, exhaust, generator, fill stations, solar)
   - Pickled sand storage building excluded? (confirm no mention or depiction)
   - Room list matches Functional Program (Appendix B)? (TBD: requires PDF access for full verification)
   - Code compliance approach documented? (egress, accessibility, occupancy)
   - Site within 12-acre developable area? (dimension check)

9.2. **Cross-check with related deliverables:**
   - **DEL-02-02 (Design Brief Narrative):** Ensure concept aligns with durability/maintenance strategy and material approach described in Design Brief (coordination meeting with Design Brief author recommended)
   - **DEL-02-03 (Sustainability & Energy Narrative):** Ensure solar-ready provisions and energy efficiency claims in Sustainability Narrative are supported by concept design (roof form, orientation, building envelope)
   - **PKG-02 (Financial Proposal):** Confirm concept scope matches estimating assumptions (building area, structural system, site development extent; coordination meeting with Estimator recommended)
   - **[X-003 Enrichment]** Step 9.2 cross-deliverable consistency check requires draft sections of DEL-02-02 and DEL-02-03 be available. If either is incomplete, Proposal Manager provides available drafts, or consistency check deferred to PKG-01 final proposal assembly QA stage. Source: _SEMANTIC_LENSING.md Item X-003 (Matrix X: judging:completeness).
   - **R3-R8 System Integration Check:** Verify mechanical/electrical/civil systems work together without conflicts per Specification R3-R8 System Integration requirement. Source: _SEMANTIC_LENSING.md Item F-003.

9.3. **Peer review:**
   - Distribute deliverable package to Code Consultant for regulatory compliance spot-check
   - **[A-004 Enrichment — Compliance Decision Gate]** Code Consultant issues compliance finding (Compliant / Conditional Compliant / Non-Compliant). If Non-Compliant, Proposal Manager decides: remediate, request variance, or accept risk. Document ruling in QA checklist. Source: _SEMANTIC_LENSING.md Item A-004 (Matrix A: normative:judging).
   - Distribute to Structural Engineer for constructability and feasibility review
   - Distribute to Proposal Manager for proposal integration and evaluation criteria alignment

9.4. **Incorporate review feedback:**
   - Address reviewer comments and revisions
   - Update drawings and narrative as needed
   - Document any assumptions or TBDs that cannot be resolved at concept stage (for post-award follow-up)

**[D-002 Enrichment — QA Decision Gate]** QA Review Results Classification:
- **(1) Blocking Issues** = must resolve before delivery (code non-compliance, missing Addendum 03 requirements, program fit gaps)
- **(2) Important Issues** = resolve if time permits (minor code clarifications, cost optimization)
- **(3) Nice-to-have** = post-award refinement
Lead Architect resolves Blocking + Important issues. Unresolved Blocking issues trigger escalation to Proposal Manager before delivery approval. Source: _SEMANTIC_LENSING.md Item D-002 (Matrix D: operative:judging).

**Verification:** QA checklist complete; all review comments addressed or documented as TBD.

**Records:** QA checklist (working document); review comment log with resolutions.

**Source:** Protocol Step 5 (Cross-Reference Consistency Check); Specification §Verification (Verification Methods table)

---

### Step 10: Deliver to Proposal Manager

**Objective:** Transfer completed deliverable package to Proposal Manager for integration into proposal PDF and submission.

**Actions:**

10.1. **Confirm deliverable completeness:**
   - All drawings produced and exported to PDF
   - Narrative document finalized and exported to PDF
   - Source files archived for post-award use
   - Deliverable meets Acceptance Criteria (_CONTEXT.md)

10.2. **Submit deliverable:**
   - Transfer DEL-02-01 package to Proposal Manager via agreed file-sharing method
   - Provide file inventory (list of PDFs and source files)
   - Confirm any special instructions for proposal PDF assembly (e.g., drawing order, page numbering)

10.3. **Coordinate final proposal assembly:**
   - Attend proposal assembly coordination meeting (if scheduled)
   - Be available for last-minute edits or clarifications during proposal finalization
   - Confirm final proposal PDF includes DEL-02-01 content correctly

**Verification:** Proposal Manager confirms receipt and integration of DEL-02-01 into proposal PDF.

**Records:** Deliverable transmittal record (email or file transfer log); proposal assembly coordination notes.

**Source:** Decomposition §7 (PKG-01 Compliance & Submission); Protocol Step 7 (Update Status after deliverable completion)

---

### Step 11: Post-Delivery Support

**[D-003 Enrichment]**

**Objective:** Maintain design authority and support proposal assembly after deliverable completion.

**Actions:**

11.1. **Remain available for consultation:**
   - After DEL-02-01 delivery, Lead Architect remains available for consultation during proposal assembly
   - If conflicts discovered (cost overrun, schedule misalignment, cross-package inconsistency), Proposal Manager alerts Lead Architect

11.2. **Handle post-delivery revisions:**
   - Minor revisions (drawing clarifications, labeling updates) approved by Lead Architect
   - Major changes (scope redesign, requirement reinterpretation) require Proposal Manager approval
   - Last revision deadline: 48 hours before proposal submission
   - All revisions tracked with revision number in document control

11.3. **Governance continuity:**
   - DEL-02-01 Concept Design Package establishes design foundation for proposal evaluation
   - If proposal is awarded, detailed design phase shall use this concept as baseline, maintaining all requirement compliance (R1-R15, Addendum 03 technical requirements, site constraints)
   - Lead Architect or designated Design Lead retains design authority for interpretation of concept intent
   - Changes to concept scope during detailed design require Owner/Project Manager approval

**Verification:** Post-delivery support activities documented in revision log.

**Records:** Revision log; post-delivery consultation notes.

**Source:** _SEMANTIC_LENSING.md Items D-003 (Matrix D: evaluative:reviewing) and X-004 (Matrix X: reviewing:consistency). Enduring governance reaffirmation requires post-delivery responsibility chain.

---

## Verification

### Deliverable Acceptance Checklist

The deliverable is complete and ready for proposal submission when all of the following are confirmed:

| Acceptance Criterion | Verification Method | Status |
|----------------------|---------------------|--------|
| **Program fit demonstrated** | Floor plan cross-checked against Functional Program (Appendix B); all required spaces included | [ ] Complete |
| **Excludes removed pickled sand storage** | Visual review of all drawings and narrative; no pickled sand building depicted or referenced | [ ] Complete |
| **Incorporates Addendum 03 requirements** | Checklist verification: 16 ft doors (shown on sections), bay sumps (shown on plan), exhaust (space allocated on plan), generator (shown on site plan), fill stations (shown on site plan), solar-ready roof (shown on massing/elevations and described in narrative) | [ ] Complete |
| **Site within 12-acre developable area** | Site plan dimensioned; building footprint and improvements within boundary | [ ] Complete |
| **Code compliance approach documented** | Narrative includes code compliance section; accessible routes shown on plan | [ ] Complete |
| **Drawings suitable for proposal PDF** | All drawings exported to PDF; legible at proposal scale; file sizes optimized | [ ] Complete |
| **Narrative complete and consistent** | Narrative addresses all required sections (program fit, site concept, Addendum 03 requirements, code compliance); cross-references drawings | [ ] Complete |
| **Cross-deliverable consistency** | Coordination confirmed with DEL-02-02 (Design Brief), DEL-02-03 (Sustainability), PKG-02 (Financial Proposal) | [ ] Complete |

**Source:** _CONTEXT.md (Acceptance Criteria); Specification §Verification (Acceptance Criteria)

---

### Quality Control Checkpoints

| Checkpoint | Responsible Party | Timing |
|------------|-------------------|--------|
| Requirements checklist complete | Lead Architect | Before beginning design work (Step 1) |
| Site concept feasibility review | Civil Engineer | After Step 2 (Site Concept) |
| Floor plan program fit verification | Lead Architect + Proposal Manager | After Step 3 (Concept Plan) |
| Code compliance spot-check | Code Consultant | After Step 3 (Concept Plan) |
| Structural feasibility review | Structural Engineer | After Step 4 (Massing) and Step 5 (Sections) |
| Cross-deliverable consistency check | Proposal Manager | After Step 8 (Deliverable Assembly) |
| Final QA review | Proposal Manager + Lead Architect | Before Step 10 (Delivery) |

**Source:** Protocol operating rules (source fidelity, cross-document consistency); Specification §Verification (Verification Methods)

---

## Records

The following records shall be produced and retained during deliverable production:

### Deliverable Artifacts (formal outputs)

1. **Site Concept Plan** (PDF + CAD source file)
2. **Concept Floor Plan(s)** (PDF + CAD source file)
3. **Building Massing Study** (PDF images + 3D model source file)
4. **Key Sections** (PDF + CAD source file)
5. **Key Elevations** (PDF + CAD source file)
6. **Concept Design Narrative** (PDF + Word source file)

### Working Documents (for internal use and post-award reference)

7. **Requirements Checklist** (spreadsheet or document tracking compliance with Specification R1–R15, Addendum 03 requirements, and Acceptance Criteria)
8. **QA Checklist** (deliverable acceptance checklist with sign-offs)
9. **Review Comment Log** (peer review feedback and resolutions)
10. **Deliverable Transmittal Record** (confirmation of delivery to Proposal Manager)

### Archive Files

11. **Source CAD Files** (floor plans, site plans, sections, elevations)
12. **3D Model Files** (massing study and any rendered views)
13. **Reference Materials** (marked-up copies of RFP appendices, addenda, site reports used during design)

**Storage Location:** Project file repository (coordinate with Proposal Manager for file structure and retention policy).

**Source:** Protocol (document control and traceability); Specification §Documentation (Deliverable Artifacts)

---

## Document Control

| Property | Value |
|----------|-------|
| **Created** | 2026-02-04 |
| **Author** | 4_DOCUMENTS Agent (Type 2 Specialist) |
| **Pass** | Pass 3 (Semantic Lensing + Final Reconcile) |
| **Next Action** | Ready for WORKING_ITEMS sessions |
| **Pass 2 Summary** | All Specification requirements (R1-R14) have verification steps in procedure Steps 1-9. Deliverable Acceptance Checklist aligns with Acceptance Criteria from _CONTEXT.md. Prerequisites reference Dependencies mode (NOT_TRACKED). Records section complete. |
| **Pass 3 Summary** | Semantic lensing enrichment complete. Incorporated items: B-004 (document precedence rule), X-002 (checklist format), C-003 (error handling), X-001 (resource verification), F-002 (room sizing standard), X-003 (cross-deliverable timing), A-004 (compliance decision gate), D-002 (QA decision gate), D-003/X-004 (Step 11 Post-Delivery Support). 10 warranted items incorporated from _SEMANTIC_LENSING.md. Procedure expanded from 10 to 11 steps. Final consistency sweep completed. |

---

**END OF PROCEDURE**
