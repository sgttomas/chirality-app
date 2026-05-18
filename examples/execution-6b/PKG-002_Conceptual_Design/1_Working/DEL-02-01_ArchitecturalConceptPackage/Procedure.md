# Architectural Concept Package — Procedure

**Document ID:** Procedure_DEL-02-01
**Deliverable ID:** DEL-02-01
**Version:** 3.0
**Date:** 2026-02-17
**Status:** DRAFT (Pass 3 — Semantic Lensing Enrichment)

---

## Purpose

This procedure describes the **workflow, coordination sequence, and verification checkpoints** for producing the Architectural Concept Package drawings. The drawings must demonstrate a functional, code-compliant building layout on the 12-acre developable site and explicitly incorporate all Addendum 03 requirements as required by RFP §7.1.1 and SOW-0009/SOW-0010.

The procedure is intended for the **Architect** (lead role for PKG-002 per Decomposition §8) and supporting discipline engineers (Structural, Mechanical, Electrical, Civil) during the **concept design phase** — typically a 2–4 week intensive period within the proposal preparation timeline.

---

## Prerequisites

### Required Information and Reference Materials

| Resource | Purpose | Source / Status |
|---|---|---|
| **RFP §7.1.1** | Defines required concept design content (floor plans, elevations, sections, massing, dimensioned size) | Provided; reviewed |
| **Appendix A (Owner Statement of Requirements — OSR)** | Detailed project requirements by space and discipline; operational context for each building zone; **bay count extraction required** (Lensing B-001) | RFP Appendix A; detailed text TBD — **must be extracted and validated before Step 2 begins** (see V-00 prerequisite checkpoint) |
| **Appendix B (Functional Program)** | Room-by-room program: space names, target areas (where not overridden by addenda), equipment, power/data needs, adjacency notes | RFP Appendix B; **must be extracted and validated before Step 2 begins** (full room list required for program analysis and AR-018 verification; see V-00 prerequisite checkpoint) |
| **Addendum 01 (Jul 11, 2024)** | Missing dimensions are intentional; designer proposes; spaces must at minimum meet building code | Incorporated |
| **Addendum 03 (Jul 31, 2024) — GOVERNS** | Room sizing ranges, 16 ft overhead doors, 40 bunker gear lockers, sumps, ventilation, fill stations, solar-capable roof, second-storey option, pickled sand storage exclusion | **Governs per Decomposition §2**; must be fully embedded in drawings (not just narratives) |
| **Site Plan Reference (Appendix E, F)** | 12-acre developable area boundary; existing site grading; flood fringe (8 acres excluded); utility context | Appendix E (grading), F (site/subdivision plan); flood zone mapping |
| **Geotechnical Investigation Report (2021, Appendix D)** | Foundation and slab design basis; no additional investigation planned per Decomposition DEL-02-03 definition | Appendix D; use 2021 report only — no additional geotech at concept phase |
| **Wetland Assessment and Environmental Assessment** | Site constraint mapping (wetland buffer, environmental protection zones) | Appendix D |
| **Decomposition v2.3 — DEL-02-01 to DEL-02-05 definitions** | Discipline deliverable scope, interface points, objective alignment | Confirmed |
| **CAD Platform and Drawing Standards** | File format (.dwg or .rvt), layer naming, title block template, scale conventions | ASSUMPTION: Design-Build firm standard; to be confirmed at Step 1 |

### Upstream Dependencies

Per _DEPENDENCIES.md: No formal upstream deliverables declared as blocking prerequisites. However, the following **concurrent coordination dependencies** must be managed actively:

| Concurrent Deliverable | Interface | Coordination Required |
|---|---|---|
| **DEL-02-02 (Civil Site Concept)** | 12-acre site boundary, building footprint placement, parking, access, utilities, Cold Storage placement | Building footprint must fit within 12-acre developable area; site plan must show fire apparatus access routes and civilian parking separately |
| **DEL-02-03 (Structural Concept)** | Structural system type, column grid, apparatus bay clear-span, floor-to-floor heights, slab sump integration | Column grid governs architectural floor plan layout; coordinate before finalizing bay dimensions |
| **DEL-02-04 (Mechanical Concept)** | Apparatus bay direct exhaust routing, bunker gear room ventilation, generator location, fill stations, sump pump strategy | Ductwork vertical rise zones and mechanical room sizing must be spatially reserved on floor plan |
| **DEL-02-05 (Electrical/IT Concept)** | Solar-capable roof orientation, electrical room location, generator connection, access control rough-in | Solar orientation must be confirmed before finalizing roof design on elevations |

### V-00: Prerequisite Validation Checkpoint (Lensing F-002)

Before beginning Step 2 (Program Analysis), the Architect must confirm that the following prerequisite extractions are complete. This checkpoint ensures that the foundational data required for program analysis and AR-018 verification is available before design work begins.

| Prerequisite | Validation Criterion | Responsible | Status |
|---|---|---|---|
| **Appendix A (OSR) extraction** | Key operational requirements extracted: fire apparatus fleet composition and bay count, PW vehicle fleet and bay requirements, operational workflows, adjacency priorities | Architect | TBD |
| **Appendix B (Functional Program) extraction** | Complete room list extracted: room names, target areas, equipment requirements, power/data needs, adjacency notes; all rooms identified including those not covered by Addendum 03 sizing ranges | Architect | TBD |
| **Bay count determination** | Total number of fire apparatus bays and PW workshop bays confirmed from Appendix A/B (Lensing B-001); this datum is required before floor plan layout alternatives can be meaningfully compared | Architect | TBD |

> **Gate rule:** Do not proceed to Step 2 until all three prerequisite items are validated. If Appendix A or B cannot be fully extracted (e.g., source documents unavailable), document the gap and the assumptions being made in the Design Coordination Log; proceed with documented assumptions clearly labeled as **ASSUMPTION** on all affected drawings and documents.

(Source: Appendix A/B -- location TBD; Specification AR-018; Lensing items F-002, B-001, A-002.)

---

## Steps

### Step 1: Establish Design Team, Coordination Protocol, and Drawing Standards

**Responsible Party:** Architect (Lead)

**Actions:**
1. Confirm Architect as PKG-002 lead per Decomposition §8; assign single point of contact for each discipline (Structural, Mechanical, Electrical, Civil)
2. Establish a **weekly coordination meeting cadence** (e.g., every Monday) with all discipline leads; document meeting dates on project schedule
3. Agree on **shared CAD/BIM folder structure** and file naming convention:
   - Floor plan: `DEL-02-01_FLOORPLAN_vXX.dwg`
   - Elevations: `DEL-02-01_ELEVATIONS_vXX.dwg`
   - Sections: `DEL-02-01_SECTIONS_vXX.dwg`
4. Confirm **drawing standards**: scale conventions, layer naming, title block template (must include DEL-02-01 identifier, date, revision number)
5. Distribute Appendix B (Functional Program) and Addendum 03 to all discipline leads; confirm receipt

**Timeline:** Days 1–2 of concept phase

**Verification:** Distribution list confirmed; coordination schedule created; shared folder accessible to all disciplines

---

### Step 2: Program Analysis and Functional Adjacency Diagram

**Responsible Party:** Architect (Lead); all discipline leads review output

**Actions:**
1. **Extract full room list from Appendix B (Functional Program):**
   - Room name, target area (sf), equipment, power/data requirements, adjacency notes
   - Cross-reference with Addendum 03 §1.16 sizing ranges — addendum values govern where they differ
   - Produce **Room Schedule Spreadsheet** (see Records section for format); flag all rooms with Addendum 03 sizing constraints

2. **Identify and note all Addendum 03 special requirements** for each applicable space:
   - Apparatus bays: 2,000–2,200 sf, 16 ft doors, sumps, direct exhaust, fill station (fire bay)
   - PW bays: 2,000–2,200 sf, sumps, general ventilation, fill station (PW bay)
   - Bunker gear room: 200–350 sf, 40 lockers, room-level ventilation
   - Other rooms: sizes per §1.16 table

3. **Develop functional adjacency matrix and bubble diagram:**
   - Zone cluster identification (see Guidance EX-001):
     - **Fire Apparatus Zone:** fire bays, bay exit/entry
     - **Decontamination / Gear Zone:** decon room, decon showers (×2), bunker gear lockers, SCBA, compressor, duty gear, EMS storage, First Aid/PPE
     - **Public Works Zone:** PW bays, workshop access
     - **Administrative/Shared Zone:** offices, meeting room (ICP), kitchen, residential quarters, visitor entry
     - **Mechanical/Utility Zone:** HVAC equipment, sump pumps, electrical room, generator (if interior)
   - Matrix: which zones MUST be adjacent, SHOULD be adjacent, SHOULD NOT be adjacent
   - Hand-drawn or digital bubble diagram showing spatial relationships

4. **(Optional but recommended) Early validation with Owner's Project Committee:**
   - Send room schedule and bubble diagram to Pendergast (PM) and Kowalchuk (Operations Manager) per Decomposition §5 for feedback
   - Resolve any adjacency or program gaps before proceeding to sketch layouts
   - Document feedback in design coordination log

**Timeline:** Days 2–4

**Verification:** Room Schedule complete and signed off internally; bubble diagram drafted; no major program conflicts; all Addendum 03 rooms captured with sizing requirements flagged

---

### Step 3: Sketch Concept Floor Plan Layouts (2–3 Alternatives)

**Responsible Party:** Architect

**Actions:**
1. **Develop 2–3 alternative floor plan sketch layouts** (paper or digital sketch):
   - **Option A:** Single-storey; all operational and shared spaces at grade; offices/admin in separate wing or grouped with apparatus zone
   - **Option B:** Two-storey; apparatus and PW bays on ground floor; shared spaces (offices, kitchen, ICP meeting room, residential quarters) on second floor per Addendum 03 §1.17
   - **Option C (if applicable):** Alternative arrangement driven by site geometry from DEL-02-02 (e.g., L-shaped, separated wings)

2. **For each option, rough-place key zones:**
   - Apparatus bays: each ~40' × 50–55' based on 2,000–2,200 sf range
   - PW bays: same area range; separate access zone
   - Decon/gear cluster in proximity to apparatus bays
   - Bunker gear room: 200–350 sf with locker configuration (see Guidance EX-002)
   - Mechanical and electrical rooms: adjacent to served spaces
   - Generator: note exterior pad preference or interior room location (see Guidance C-004)

3. **Rough-dimension each option** to confirm program feasibility:
   - Does building footprint fit on the 12-acre site with parking, access, Cold Storage (60'×100'), and minimum setbacks?
   - Does the floor plate total align with program sum (sum of all rooms from Appendix B + Addendum 03)?
   - Is the apparatus bay clear-span structurally achievable in each option?

4. **Coordinate structurally** (first informal check with Structural Engineer):
   - Which option best supports apparatus bay clear-span without introducing excessive structural complexity?
   - Does the two-storey option introduce unacceptable structural complication for the column grid or gravity load path?

**Timeline:** Days 4–8

**Verification:** 2–3 alternative sketches produced; Structural Engineer informally reviews bay clear-span feasibility; total program area estimated and reasonable; site footprint confirmed to fit in 12-acre developable area

---

### Step 3A: Storey Decision Gate (Lensing A-005)

**Responsible Party:** Architect (decision); Structural Engineer and Civil Engineer (input)

**Purpose:** Before proceeding to multidiscipline input integration (Step 4) and CAD drafting (Step 5), the team must formally select and document the storey decision (single-storey vs. two-storey layout). This decision fundamentally affects structural system selection, egress design, HVAC routing, fire separation requirements (see Specification AR-C09), and site footprint. Proceeding to CAD without a documented storey decision risks costly rework.

**Actions:**
1. **Review 2-3 alternatives from Step 3** and evaluate each against:
   - Site footprint feasibility (does the single-storey option fit within 12-acre developable area with all required site elements? -- coordinate with Civil Engineer, DEL-02-02)
   - Structural complexity (two-storey adds fire-rated floor assembly, elevator/stair, increased foundation loads -- coordinate with Structural Engineer, DEL-02-03)
   - NBCC fire separation requirements for two-storey residential quarters (see Guidance C-005 and Specification AR-C09)
   - Scoring impact for OBJ-003 (see Guidance T-001 for trade-off analysis)
2. **Formally select preferred option** with documented rationale
3. **Record decision** in Design Coordination Log:
   - Selected option (single-storey / two-storey / hybrid)
   - Rationale for selection (site constraint, structural preference, program fit, scoring strategy)
   - Sign-off: Architect + at minimum Structural Engineer concurrence
   - Reference to Guidance CONF-G02 (storey decision conflict table entry)

**Timeline:** Day 8 (before Step 4 discipline input integration begins)

**Verification:** Storey decision documented in Design Coordination Log with rationale and sign-off; Structural Engineer has concurred on structural feasibility of selected option; Civil Engineer has confirmed site footprint feasibility

---

### Step 4: Multidiscipline Coordination and Input Integration

**Responsible Party:** Architect (facilitates); each discipline lead provides input

**Actions:**
1. **Structural Engineer (DEL-02-03 lead) provides:**
   - Proposed structural system (steel frame, post-and-beam, heavy timber?) that supports apparatus bay clear-spans
   - Column grid layout overlay on sketch floor plans
   - Confirmation of slab zones where sumps can be integrated (affects slab reinforcing design)
   - Floor-to-floor height assumptions (typically 16–18 ft for apparatus bays including mechanical ductwork space above)
   - Any structural assumptions from 2021 geotechnical report (bearing capacity, pile depth, frost protection depth)

2. **Mechanical Engineer (DEL-02-04 lead) provides:**
   - Apparatus bay direct exhaust ventilation strategy: where does exhaust duct rise vertically? Is there a roof-mounted unit or building-integrated ductwork?
   - Bunker gear room ventilation approach (dedicated exhaust fan? room-level air changes? placement of intake/exhaust openings on wall or roof?)
   - Generator location preference (exterior pad vs. interior equipment room) and fuel tank location
   - Water fill station preferred location (interior alcove vs. exterior pedestal; frost-protection approach)
   - Mechanical room size estimate and preferred location(s)
   - Sump drainage strategy (centralized vs. distributed per Guidance T-005)

3. **Electrical Engineer (DEL-02-05 lead) provides:**
   - Solar-capable roof orientation decision (flat? south/SW pitched?): this decision governs elevation design
   - Electrical room location and size requirement
   - Emergency generator electrical connection point and ATS (automatic transfer switch) location
   - Solar rough-in provisions (conduit pathways, junction boxes, roof penetration plan)
   - Access control and security device rough locations (if Additional Options 3-4 are being priced)

4. **Civil Engineer (DEL-02-02 lead) provides:**
   - Definitive 12-acre developable area boundary with flood fringe clearly distinguished
   - Recommended building footprint placement (considering access, parking, utilities, site grading)
   - Parking layout (staff, visitor, apparatus pre-positioning) in context with building footprint
   - Fire apparatus access routes (NBCC fire department access requirements)
   - Utility connection points (water, sewer, storm, electrical service entry)
   - Cold Storage (60'×100') placement relative to main building

5. **Architect synthesizes all discipline inputs:**
   - Select preferred floor plan layout from 2–3 alternatives
   - Update sketch to incorporate structural column grid
   - Mark mechanical ductwork vertical rise zones and mechanical room location
   - Annotate electrical room and solar roof orientation
   - Overlay civil site context; confirm building footprint placement
   - Document unresolved issues in Design Coordination Log (see Records)

**Timeline:** Days 8–12 (concurrent with Step 3 refinement; discipline inputs gathered iteratively)

**Verification:** Design Coordination Log updated; all discipline inputs received or outstanding items flagged; preferred floor plan alternative selected; no critical coordination conflicts blocking CAD drafting

---

### Step 5: CAD Floor Plan Drafting (Preferred Layout)

**Responsible Party:** Architect

**Actions:**
1. **Set up CAD drawing file with layered structure:**
   - Base structural layer: column grid from Structural Engineer
   - Architectural layer: walls, doors, windows, room labels, dimensions, room sf annotations
   - Mechanical coordination layer: HVAC zone boundaries, ductwork vertical runs, exhaust shaft, mechanical room outline
   - Electrical coordination layer: electrical room, panel location, generator connection point, solar roof notation
   - Civil context layer: site boundary (12-acre), building footprint outline, parking context, Cold Storage outline (reference, not final)

2. **Draft each room with explicit annotations (required Addendum 03 callouts in CAPS):**
   - Apparatus Bay 1 and 2: dimension to confirm 2,000–2,200 sf; label "APPARATUS BAY #1 — XXXX SF"; mark "SUMP — TYP."; note "16 FT CLEAR OVERHEAD DOOR"; mark "2" MIN. WATER FILL STATION" (fire bay only); note "DIRECT EXHAUST VENTILATION — 2 APPARATUS — REFER DEL-02-04"
   - PW Workshop Bay 1 and 2: dimension to 2,000–2,200 sf; label "PW WORKSHOP BAY — XXXX SF"; mark "SUMP — TYP."; note "GENERAL VENTILATION"; mark "2" MIN. WATER FILL STATION" (PW bay)
   - Bunker Gear Room: dimension to 200–350 sf; show locker layout (40 units — schematic configuration per Guidance EX-002); label "40 BUNKER GEAR LOCKERS"; note "ROOM-LEVEL VENTILATION REQUIRED"
   - Decon Room, Decon Showers (×2), SCBA, Compressor, EMS Storage, Duty Gear, First Aid/PPE: each dimensioned to Addendum 03 sf range; labeled with room name and sf callout
   - Other rooms per Appendix B: labeled, dimensioned; sf callout
   - Mechanical Room, Electrical Room: located and dimensioned (size from discipline engineer input)
   - Accessible path: annotate "ACCESSIBLE PATH →" with arrow chain from main entry through key public spaces

3. **Overall building dimensions:**
   - Total building L × W callout on floor plan perimeter
   - Zone area sub-totals (Fire Apparatus Zone sf, PW Zone sf, Admin/Shared Zone sf, Mechanical/Utility sf)

4. **Structural overlay check:**
   - Confirm no column falls within apparatus or PW bay clear-span zone
   - Confirm sump zones are in valid slab locations (not coinciding with column footings)

**Timeline:** Days 12–16

**Verification:** CAD floor plan complete; all Addendum 03 rooms shown and annotated; sf callouts present; structural grid overlaid without clear-span conflicts; mechanical and electrical zones identified; accessible path traced; no critical drafting errors

---

### Step 6: Building Elevations (All Four Cardinal Directions)

**Responsible Party:** Architect

**Actions:**
1. **Develop four elevation drawings** (North, South, East, West) based on finalized floor plan:
   - **North Elevation:** Apparatus bay end-wall; 16 ft overhead door(s) shown with explicit height dimension "16'-0" CLEAR OPENING"; main entry (if north-facing); roof profile; mechanical/electrical penetrations
   - **South Elevation:** Solar-capable roof annotation; office/residential windows; secondary entry or PW bay end-wall (layout-dependent); note "FLAT ROOF — SOLAR-CAPABLE ORIENTATION PER ADDENDUM 03 §1.14" (or applicable roof type + orientation)
   - **East and West Elevations:** Side profiles of apparatus and PW bays; show 16 ft door height context; show second-storey profile if two-storey option used; ductwork chase expression if visible on exterior

2. **Annotate elevations with dimensions:**
   - Overall building height to roof eave; height to roof ridge/peak (if pitched)
   - Door heights: "16'-0" CLEAR" for overhead doors; "8'-0"" or code-minimum for personnel doors
   - Window sill/head heights at key facade zones
   - Floor-to-floor height (if two-storey): e.g., "FIRST FLOOR TO SECOND FLOOR: XX'-0""

3. **Material notation (descriptive, concept-level):**
   - Wall cladding: e.g., "Architectural masonry or fiber-cement siding — TBD by design team" (do not over-specify at concept phase)
   - Roofing: e.g., "Solar-capable flat roof — TPO or EPDM membrane over rigid insulation — REFER DEL-02-05 FOR SOLAR PROVISIONS"
   - Overhead doors: "Insulated sectional overhead doors with vision panels — 16 FT CLEAR"
   - Foundation/grade: "Refer DEL-02-03 Structural Concept for foundation design"

4. **Cross-references on each elevation:**
   - "Structural system: see DEL-02-03"
   - "Mechanical penetrations: see DEL-02-04"
   - "Solar provisions: see DEL-02-05"
   - "Site context: see DEL-02-02"

**Timeline:** Days 16–18

**Verification:** All four cardinal elevation drawings completed; 16 ft overhead door height explicitly dimensioned on applicable elevations; solar roof orientation annotated on South/applicable elevation; building height callouts consistent with floor plan room heights; no conflicts between elevation and floor plan door/window locations

---

### Step 7: Building Sections (Minimum 2, Recommended 2–4)

**Responsible Party:** Architect

**Actions:**
1. **Identify section cut locations** on floor plan with section markers (A–A, B–B, etc.):
   - **Section A–A (Required):** Longitudinal cut through fire apparatus bay(s); must show 16 ft overhead door clear opening height profile, bay slab with sump detail location, structural truss/frame above bay, ductwork zone above bay ceiling, roof profile and solar aspect
   - **Section B–B (Required):** Transverse cut through building at mixed-use zone or second-floor interface; must show floor-to-floor heights, structural slab separation, administrative/apparatus zone height difference
   - **Section C–C (Optional):** Cut through mechanical/utility zone if complex equipment arrangement is worth clarifying (e.g., mechanical room stack height, generator room with louvers)

2. **Section drawing content (by cut):**
   - Grade line and foundation depth indication (reference: 2021 geotech report, Appendix D)
   - Slab levels and structural element centerlines
   - Clear heights at apparatus bay: "16'-0" CLEAR OPENING" measured from finished floor to underside of door header
   - Structural depth above bay clear height (truss or beam depth zone)
   - Ductwork zone above structural depth: "DIRECT EXHAUST DUCT — REFER DEL-02-04"
   - Roof profile and solar-ready annotations
   - Adjacent room heights (e.g., office corridor at 9 ft clear minimum NBCC)
   - Floor-to-floor heights for two-storey sections

3. **Annotation on sections:**
   - All clear height dimensions in imperial and/or metric as appropriate
   - Structural system type noted (e.g., "STEEL FRAME — REFER DEL-02-03 STRUCTURAL CONCEPT")
   - Slab detail cross-reference: "REFER DEL-02-03 FOR SLAB DETAIL AT SUMP LOCATION"
   - HVAC routing note: "APPARATUS BAY DIRECT EXHAUST DUCTWORK — REFER DEL-02-04"

4. **Cross-reference section cut lines on floor plan:**
   - All section markers (arrows and cut line) clearly labeled and visible on floor plan
   - Direction of view indicated (arrow pointing in direction of projected view)

**Timeline:** Days 18–20

**Verification:** Minimum 2 sections present (A–A through apparatus bay; B–B through mixed-use zone); section cut lines legible on floor plan; 16 ft apparatus bay clear opening confirmed on section; floor-to-floor heights consistent with floor plan and elevation callouts; no conflicts with structural or mechanical discipline inputs

---

### Step 8: Optional 3D Rendering or Massing Diagram

**Responsible Party:** Architect (and/or rendering vendor if engaged)

**Decision Point:** This decision must be made by **Day 5 of concept phase (end of Week 1)**. See Guidance T-003 for trade-off analysis. (Lensing D-002: terminology standardized across all documents.)

**Actions (if 3D rendering / massing diagram is pursued):**
1. Build 3D model in SketchUp, Revit, or equivalent (for massing) or commission professional rendering vendor (for photorealistic)
2. Produce 2–4 perspective views:
   - **Aerial perspective:** Shows building footprint on 12-acre site with parking, access routes, Cold Storage, site context
   - **Street-level entry view:** Shows main public entry, administrative facade, architectural character
   - **Apparatus bay view:** Shows overhead door(s), 16 ft clear height context, operational approach zone
   - **Complementary view (SW, SE, or NE):** Shows solar-capable roof and overall building massing

3. Apply concept-level material representation (do not over-detail; consistent with elevation notation)
4. Include landscaping, parking, basic site context from DEL-02-02 (civil site plan)
5. Verify 3D model is geometrically consistent with floor plan and elevations before exporting images

**Timeline:** Days 18–22 (concurrent with Sections; start earlier if rendering vendor is engaged)

**Verification:** 3D model cross-checked against floor plan and elevations for geometric accuracy; perspectives legible and reflect building massing correctly; materials/colors consistent with elevation notation; site context included; ready for PDF export

---

### Step 9: Addendum 03 Compliance Cross-Check and Coordination Verification

**Responsible Party:** Architect (self-check); Discipline Engineers (coordination confirmation)

**Actions:**
1. **Architect self-check against Specification requirements (AR-001 to AR-021 and AR-C01 to AR-C09):**

   | Item | Check |
   |---|---|
   | AR-001, AR-003: Apparatus and PW bay areas 2,000–2,200 sf | sf callouts on floor plan; within range |
   | AR-002: 16 ft clear overhead doors | Labeled on floor plan door symbols, elevation dimensions, and section clear opening |
   | AR-004: 40 bunker gear lockers, 200–350 sf room | Locker count labeled; room area within range |
   | AR-005: Bunker gear room ventilation | "ROOM-LEVEL VENTILATION REQUIRED" noted on floor plan |
   | AR-006 to AR-012: All specified rooms present | Each room visible on floor plan with sf callout in range |
   | AR-013: Bay sumps | "SUMP TYP." labeled in all apparatus and PW bays |
   | AR-014, AR-015: Water fill stations (×2, 2" min) | Both fill stations located on floor plan; "2" MIN." noted |
   | AR-016: Second-storey (if used) | Upper floor plan present; floor-to-floor heights on elevation and section |
   | AR-017: Solar-capable roof orientation | Annotated on all four elevations |
   | AR-018: Full Functional Program compliance | All rooms from Appendix B present on floor plan; **prerequisite:** Appendix B room list extracted and signed off (see V-00 and Specification F-001) |
   | AR-019: Pickled sand storage excluded | No such notation on any drawing |
   | AR-020: Dimensioned building envelope | L × W on floor plan; H on elevation and section |
   | AR-021: Non-Addendum 03 rooms (Lensing A-001) | All non-Addendum 03 rooms (offices, kitchen, ICP, residential quarters, washrooms, mechanical, electrical) present on floor plan with sf callout; each meets building code minimum |
   | AR-C01: All four elevations | 4 elevations labeled N, S, E, W present |
   | AR-C04: Accessible path feasible | Path traced on floor plan |
   | AR-C09: Fire separation (two-storey, Lensing E-001) | If two-storey: fire separation requirement noted on section drawing or coordination notes; spatial feasibility of fire-rated floor assembly confirmed |

2. **Final discipline coordination confirmations (written or email):**
   - **Structural:** Column grid compatible with floor plan layout; slab sump zones structurally feasible; floor-to-floor heights achievable
   - **Mechanical:** Apparatus exhaust ductwork routing viable; bunker gear ventilation provisions shown; generator location feasible; fill station connections feasible
   - **Electrical:** Solar roof orientation confirmed; electrical distribution feasible; generator connection point identified
   - **Civil:** Building footprint within 12-acre developable area; parking/access/utilities shown; Cold Storage placement compatible

3. **Update Design Coordination Log** with all outstanding items:
   - Classify each as Critical (must resolve before PDF export) or Minor (can carry to detailed design)
   - Resolve all Critical items; document resolution

4. **Late-Arriving Discipline Input Change Management (Lensing X-002):**

   If a discipline engineer provides revised input that affects completed CAD drawings after Step 5 drafting is substantially complete, the following revalidation protocol applies:

   | Trigger | Action | Authorization | Tracking |
   |---|---|---|---|
   | **Structural change** (column grid revision, floor-to-floor height change, slab redesign affecting sumps) | Re-evaluate apparatus bay layout; redraft affected floor plan zones; update sections and elevations for height changes | Architect approval; Structural Engineer concurrence | Log as "Change Event" in Design Coordination Log with date, source, impact assessment, and resolution |
   | **Mechanical change** (exhaust routing revision, generator relocation, mechanical room resizing) | Update floor plan mechanical coordination layer; revise spatial reservations; confirm section ductwork zones | Architect approval; Mechanical Engineer concurrence | Same as above |
   | **Electrical change** (solar orientation change, electrical room relocation) | Update elevations for roof annotation; update floor plan electrical coordination layer | Architect approval; Electrical Engineer concurrence | Same as above |
   | **Civil change** (building footprint relocation, parking reconfiguration) | Update site context plan coordination; confirm building footprint still within 12-acre boundary | Architect approval; Civil Engineer concurrence | Same as above |

   > **Rule:** Any change event that affects 2 or more drawings triggers a mini re-run of Step 9 compliance cross-check (items 1-2 above) for the affected requirement IDs. The Architect decides whether a full re-check or targeted re-check is appropriate based on change scope. All change events must be recorded in the Design Coordination Log before PDF assembly (Step 10).

**Timeline:** Days 20–22

**Verification:** Specification requirements AR-001 through AR-C08 and AR-C09 confirmed on drawings; Design Coordination Log updated; no Critical issues outstanding; all four disciplines have confirmed coordination adequacy; any late-arriving changes processed through revalidation protocol and documented

---

### Step 10: PDF Drawing Set Assembly and Proposal Integration

**Responsible Party:** Architect + Proposal Manager

**Actions:**
1. **Export all drawings to PDF:**
   - Set print/plot area, scale bar, and page size (11×17 or letter; confirm with Proposal Manager based on total PDF budget)
   - Verify all drawing text and dimensions are legible at 100% zoom on screen and at print scale
   - Title blocks include DEL-02-01, date, revision number ("REV 2 — Concept Design, [Date]"), scale, north arrow

2. **Assemble drawing package in logical order:**
   - Cover/index page: "Section 7.1.1 — Proposed Conceptual Design — DEL-02-01 Architectural Concept Package"
   - Sheet 1: Floor plan(s)
   - Sheet 2: Building elevations (all four cardinal directions; combine on one sheet if space allows)
   - Sheet 3: Building sections (A–A, B–B, additional as required)
   - Sheet 4+: 3D rendering / massing diagram (optional; 1–4 perspectives)
   - Final sheet: Site context plan (from DEL-02-02 Civil Site Concept)

3. **Supplementary design coordination notes (1–2 pages, optional):**
   - Brief narrative: how floor plan accommodates Addendum 03 requirements, structural/mechanical/electrical integration strategy, site context approach
   - May be integrated into DEL-03-01 (Architectural Design Brief) if preferred to minimize PDF page count

4. **File size check:**
   - Confirm total proposal PDF ≤15 MB (RFP §4.2, Decomposition §3 Hard Constraint C-01)
   - Compress drawing PDF layers if needed to reduce file size without sacrificing legibility
   - Coordinate with Proposal Manager (DEL-01-02 assembly) to confirm this deliverable's contribution to total PDF size

5. **Internal QA before submission:**
   - Print drawings (letter or 11×17); verify dimensions are readable, callouts are unambiguous
   - Cross-reference callouts to DEL-02-03, DEL-02-04, DEL-02-05 are present on drawings
   - Proposal Manager final review: confirm content order per RFP §4.3 section order; confirm pickled sand storage absent; confirm addenda acknowledgement (Proposal Manager DEL-01-01 compliance matrix)

**Timeline:** Days 22–23 (final 1–2 days before proposal assembly)

**Verification:** PDF complete and legible; file size confirmed within 15 MB contribution; all required sheets present; cross-references to discipline deliverables present; approved by Proposal Manager for inclusion in proposal

---

## Verification

### QA/QC Checkpoint Summary

| Checkpoint | Step | Responsible | Pass Criteria |
|---|---|---|---|
| **V-01: Program Analysis Complete** | End Step 2 | Architect | Room Schedule complete; all Appendix B rooms captured with Addendum 03 sizing applied; bubble diagram drafted |
| **V-02: Site Feasibility Confirmed** | End Step 3 | Architect + Civil Eng | 2–3 sketch alternatives exist; at least one fits within 12-acre developable area with parking, Cold Storage, access routes |
| **V-03: Structural Coordination** | End Step 4 | Structural Engineer | Column grid provided; apparatus bay clear-span confirmed; slab sump zones identified; floor-to-floor heights set |
| **V-04: Mechanical Coordination** | End Step 4 | Mechanical Engineer | Exhaust duct routing identified; bunker gear ventilation strategy confirmed; generator location feasible; fill station locations feasible |
| **V-05: Electrical Coordination** | End Step 4 | Electrical Engineer | Solar roof orientation confirmed; electrical distribution feasible; generator connection point identified |
| **V-06: Civil Coordination** | End Step 4 | Civil Engineer | Building footprint placement within 12-acre confirmed; parking/access/utilities integrated; Cold Storage compatible |
| **V-07: CAD Floor Plan Draft** | End Step 5 | Architect | All rooms dimensioned; all Addendum 03 callouts present; column grid overlaid; accessible path traced; sf callouts within ranges |
| **V-08: Elevations Complete** | End Step 6 | Architect | 4 elevations (N, S, E, W) drafted; 16 ft overhead doors dimensioned; solar roof orientation annotated; no floor plan conflicts |
| **V-09: Sections Complete** | End Step 7 | Architect | Minimum 2 sections (A–A apparatus bay, B–B mixed-use); 16 ft clear opening shown on apparatus bay section; floor-to-floor heights consistent |
| **V-10: Rendering (if pursued)** | End Step 8 | Architect | 3D model geometrically accurate; perspectives legible; site context included; materials consistent with elevations |
| **V-00: Prerequisite Validation (Lensing F-002)** | Before Step 2 | Architect | Appendix A and Appendix B extractions complete; bay count determined; all prerequisites documented and validated (see Prerequisite Validation Checkpoint above) |
| **V-02A: Storey Decision Gate (Lensing A-005)** | End Step 3A | Architect + Structural Eng | Storey decision formally selected with documented rationale and sign-off; Structural and Civil Engineers concur on feasibility |
| **V-11: Addendum 03 Compliance Check** | End Step 9 | Architect | All AR-001 to AR-021 and AR-C01 to AR-C09 requirements confirmed present; Design Coordination Log complete; no Critical issues outstanding; any late-arriving changes processed per revalidation protocol (Lensing X-002) |
| **V-12: PDF Assembly and Proposal Ready** | End Step 10 | Proposal Manager | PDF complete and legible; file size within 15 MB budget; section order per RFP §4.3; cross-references to DEL-02-03/04/05 present; approved for submission |

---

## Records

### Documentation to Produce and Retain

| Record | Format | Owner | Retention |
|---|---|---|---|
| **CAD Source Files** | .dwg (AutoCAD) or .rvt (Revit) | Architect / BIM Repository | Project completion + 7 years (per CCDC 14) |
| **PDF Exported Drawing Set** | .pdf | Architect / Proposal archive | Project completion + 7 years |
| **Room Schedule Spreadsheet** | .xlsx | Architect | Through detailed design; handed off to DD phase |
| **Functional Adjacency / Bubble Diagram** | .pdf or scanned image | Architect | Through detailed design |
| **Sketch Alternatives (Options A, B, C)** | .pdf or scanned image | Architect | Through detailed design (reference and audit trail) |
| **Design Coordination Log** | .xlsx or equivalent | Architect (shared with all disciplines) | Through detailed design; Critical items formally closed; document carries to DD phase |
| **Discipline Coordination Confirmations** | Email or meeting minutes | Architect | Through detailed design |
| **3D Rendering / Massing Files** | .skp, .3ds, .psd, or vendor source | Architect / Rendering vendor | Proposal submission + 1 year |
| **Owner Review Feedback Notes** | .txt or .pdf summary | Architect / Proposal Manager | Through detailed design |

### Handoff to Downstream Deliverables

Upon completion of DEL-02-01 Concept Package, the following are handed off to downstream work:

| Downstream Deliverable | Handoff Content | When |
|---|---|---|
| **DEL-03-01 (Architectural Design Brief)** | Approved concept floor plan + elevations as basis for design intent narrative; adjacency rationale and code compliance approach | Immediately after concept drawings finalized |
| **DEL-03-06 (Accessibility & Adaptability)** | Accessible path identified on concept floor plan; first-floor layout showing accessible entry and path; second-storey option (if used) with lift/elevator provisions | Simultaneously with DEL-03-01 |
| **PKG-006 DEL-06-02 (Detailed Design and Construction Docs Plan)** | Approved concept drawings as baseline for detailed design submission milestones; Room Schedule; Design Coordination Log (outstanding items) | After proposal award and design-build contract execution |
| **DEL-01-02 (Formal Submission Package)** | PDF drawing set for inclusion in proposal PDF (Proposal Manager assembles overall package) | Per proposal assembly schedule (3+ days before email submission) |

---

## Notes

### Key Authoring Guidance

1. **Do not leave Addendum 03 requirements implicit** — every required Addendum 03 element must be explicitly labeled on the drawing in which it is shown. Evaluators will check drawings against the addendum; if they cannot find the label, the requirement may be scored as absent.

2. **The floor plan is the anchor drawing.** All other drawings (elevations, sections) derive from and must be geometrically consistent with the floor plan. Finalize the floor plan before drafting elevations or sections.

3. **Coordinate first, draft second.** Structural column grid, mechanical ductwork zones, and solar roof orientation must be confirmed with discipline engineers (Step 4) before committing to CAD drafting (Step 5). Retrofitting structural or mechanical constraints into a fully-drafted floor plan is costly.

4. **Track the Design Coordination Log from Day 1.** Every unresolved issue between disciplines belongs in the log. The log is the team's single source of truth for what is open, who owns it, and when it must be resolved.

5. **File size discipline matters.** The 15 MB PDF limit (RFP §4.2) is a hard constraint. Drawings must be exported at the minimum resolution needed for legibility, not the maximum. Check file size at end of Step 10; adjust if needed. Coordinate with Proposal Manager early to understand the page budget allocation for this deliverable.

6. **Rendering decision is time-critical.** If 3D rendering or massing diagram is pursued, the decision must be made by **Day 5 of concept phase (end of Week 1)**. Later decisions compress production time and risk poor quality output for the highest-scored technical criterion (20 pts). (Lensing D-002: terminology standardized across all documents.)

### Common Pitfalls to Avoid

1. **Omitting Addendum 03 annotated callouts.** A room drawn at the right size but not annotated "40 BUNKER GEAR LOCKERS" or "ROOM-LEVEL VENTILATION REQUIRED" will not clearly demonstrate compliance to evaluators.

2. **Missing all four cardinal elevations.** RFP §7.1.1 is explicit. Three elevations with the north end omitted (even if unremarkable) will be a non-compliance. All four must be present.

3. **Showing pickled sand storage on any drawing.** This is an explicit exclusion (Addendum 03 §1.2). Including it — even as a reference or future option — signals non-compliance with addenda.

4. **Overcrowding the drawing package to avoid 3D.** If every inch of available PDF page real-estate is consumed by floor plan and elevations with no rendering or massing, the proposal may score lower on the 20-pt criterion than if a modest massing diagram is included on one sheet.

5. **Deferring structural coordination.** Starting CAD drafting before structural column grid is confirmed results in a floor plan that may require complete redraft if the column grid conflicts with apparatus bay clear-span requirements. The coordination is cheap at Step 4 and expensive at Step 5+.

---

## Status Notes

- **Pass 3 Status (v3.0):** Semantic Lensing Enrichment — 4 lensing items applied:
  - V-00 prerequisite validation checkpoint added (F-002) — formalizes Appendix A/B extraction as gate before Step 2
  - Step 3A storey decision gate added (A-005) — requires documented storey selection with rationale and sign-off before proceeding to CAD
  - Rendering deadline terminology standardized to "Day 5 of concept phase (end of Week 1)" across Step 8 and Key Authoring Guidance note 6 (D-002)
  - Late-arriving discipline input change management protocol added to Step 9 (X-002) — defines triggers, actions, authorization, and tracking for post-CAD changes
  - Step 9 compliance checklist updated to include AR-021 (non-Addendum 03 rooms) and AR-C09 (fire separation for two-storey option)
  - QA/QC checkpoint table updated with V-00 and V-02A entries; V-11 scope expanded to AR-021 and AR-C09

---

**End of Procedure**
