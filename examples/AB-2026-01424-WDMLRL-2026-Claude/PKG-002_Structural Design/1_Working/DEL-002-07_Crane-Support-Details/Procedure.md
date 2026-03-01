# Procedure — DEL-002-07 Crane Support Structure Details

---

## Purpose

This procedure describes the steps to produce the Crane Support Structure Details drawing set (DEL-002-07) as an Issued for Construction (IFC) document package, signed and stamped by a P.Eng. licensed in Alberta. The procedure covers design inputs, engineering tasks, drawing production, coordination, and issuance.

---

## Prerequisites

### Upstream deliverables and inputs required before proceeding to IFC

| Prerequisite | Status Gate | Source |
|---|---|---|
| DEL-002-01 — Preliminary Structural Design | County approval of preliminary structural design must be obtained before final IFC drawings are issued | RFP §3.3.2; SOW-0010b |
| Geotechnical investigation report (PKG-008) | Required for crane column/foundation bearing capacity; must be available before foundation-level details are finalized | RFP §3.3.2; SOW-0001 |
| Crane supplier data sheet (PKG-016) | Required for: rated capacity, bridge end-truck wheel base, maximum wheel loads (static + dynamic impact), runway rail size and type requirements, minimum hook height, horizontal forces | ASSUMPTION (standard practice); SOW-0067 |
| DEL-002-03 — Structural Framing Plans | Column locations, bay widths, and building structural grid must be established. **[C-003]** Clarification needed: specify the minimum completion level of DEL-002-03 required before DEL-002-07 design can proceed (e.g., "column locations and bay widths confirmed on preliminary framing plan" vs. "DEL-002-03 IFC issued"). Premature design starts based on preliminary column locations risk rework if the framing plan changes. Proposed authority: Design Coordinator (PROPOSAL). | ASSUMPTION — coordinate with framing plan production |
| Applicable code editions confirmed | Structural Engineer of Record to confirm NBC, Alberta Building Code, CSA S16, CSA A23.3, and CMAA specification editions governing this project | ASSUMPTION |
| Building permit obtained or in process | All applicable Safety Code permits required | RFP §3.3.2; SOW-0006, SOW-0007 |

### Required references

| Reference | Purpose |
|---|---|
| AB-2026-01424-WDMLRL RFP.pdf §3.4 | Crane design requirements (two 5-tonne cranes, 35' ceiling) |
| AB-2026-01424-Appendix B (Shop).pdf | Conceptual floor plan — crane positions, building dimensions |
| Crane supplier data sheet | Crane wheel loads, geometry, rail requirements |
| CSA S16 (current edition) | Runway beam and connection design (ASSUMPTION) |
| CSA A23.3 (current edition) | Concrete corbel/column design (ASSUMPTION) |
| CMAA Spec 70 or 74 (as applicable) | Crane service class, runway tolerances (ASSUMPTION) |
| NBC / Alberta Building Code | Load combinations, seismic, wind, snow (ASSUMPTION) |

---

## Steps

### Step 1 — Confirm Crane System Configuration

1.1 Obtain or confirm crane supplier data sheet (from PKG-016 procurement process). **[F-003]** Upon receipt, formally log the data sheet: record the document title, revision, date received, and source. Verify completeness by checking that all data fields listed in Step 1.2 below are present and populated. If any required fields are missing or marked TBD by the supplier, flag the specific gaps for resolution before proceeding. The crane supplier data sheet is the single most critical design input; its formal receipt and completeness verification should be a logged gate. Proposed authority: Structural Engineer (PROPOSAL).

1.2 Confirm the following from the data sheet and project requirements:
   - Crane type (top-running single-girder or double-girder bridge)
   - CMAA service class
   - Bridge end-truck wheel base and wheel spacing
   - Maximum static wheel load (at rated capacity + bridge self-weight)
   - Dynamic impact factor per governing standard
   - Horizontal lateral and longitudinal forces
   - Minimum runway rail size required by crane manufacturer
   - Minimum hook height under load
   - Required runway clearances (horizontal and vertical)

1.3 Confirm crane arrangement: two bridges on a shared runway pair, or two independent parallel runways. Coordinate with App B floor plan layout and building structural grid (DEL-002-03).

1.4 If crane supplier data is not yet available: document assumed conservative wheel loads in the calculation package (DEL-002-10), noting that final values must be confirmed. Flag for human review. (See Guidance.md — Trade-offs)

**Record:** Design input log entry noting crane data source, date received, and governing values used.

---

### Step 2 — Establish Structural Design Loads

2.1 Determine governing load combinations per NBC / Alberta Building Code (dead load, crane live load, impact, lateral forces, wind on crane, seismic).

2.2 Calculate maximum runway beam end reactions (vertical and horizontal) for:
   - One crane at maximum rated load, worst-case position on runway
   - Two cranes at maximum rated load, worst-case simultaneous position (if shared runway)

2.3 Apply appropriate impact factor to vertical wheel loads per governing standard (CMAA / NBC — ASSUMPTION).

2.4 Determine longitudinal and lateral crane braking forces for runway beam and support anchorage design.

2.5 Confirm that the 35' ceiling height provides adequate clearance above the crane hook at rated lift position. (RFP §3.4; ASSUMPTION that clearance check is required)

**Record:** Load summary table — to appear on IFC drawings.

---

### Step 3 — Design Runway Beam Support Structure

3.1 Select support configuration (corbels on concrete building columns, or dedicated crane columns) in coordination with DEL-002-03 column layout.

3.2 Design runway beam:
   - Select section (e.g., wide-flange steel beam) based on span, wheel loads, and deflection limits
   - Check bending, shear, and web local yielding/crippling
   - Check deflection limits (vertical and horizontal) per CMAA and CSA S16 requirements
   - Design runway rail attachment (bolted rail clips preferred to allow future replacement)

3.3 Design runway beam supports:
   - Design concrete corbels or crane column brackets per CSA A23.3 (corbels) or CSA S16 (steel brackets)
   - Check bearing, shear-friction, and tension requirements
   - Design anchor bolts or embedded plates at concrete interface

3.4 Design end stops at each runway termination:
   - Select end stop bumper type (spring, rubber, or hydraulic — ASSUMPTION based on crane speed and mass)
   - Design end stop connection to runway beam or building structure

3.5 Detail runway rail:
   - Select rail type and size per crane manufacturer requirements
   - Detail rail-to-beam connection (rail clips, bolted)
   - Note joint requirements at runway beam splices

**Record:** Structural calculation package entries (DEL-002-10).

---

### Step 4 — Produce IFC Drawing Set

4.1 Prepare the following drawing sheets (anticipated — final sheet list per structural engineer):

   a. **Crane Runway Framing Plan**
      - Plan view at runway beam elevation
      - Runway beam layout, support locations, bay widths
      - Crane travel limits, end stop locations
      - Grid and column references
      - Key dimensions (runway length, bay width, wheel gauge)

   b. **Runway Beam Sections and Elevation**
      - Beam size, material, orientation
      - Rail attachment detail reference
      - Elevation at top of rail
      - Splice location (if any)

   c. **Support Structure Details**
      - Concrete corbel reinforcing and geometry (if corbel type)
      - Steel bracket/plate details (if bracket type)
      - Anchor bolt or embedded plate schedule and layout
      - Concrete column section at support elevation (coordinate with DEL-002-03)

   d. **Connection Details**
      - Beam-to-corbel/bracket bearing details
      - Lateral restraint connection
      - End stop connection to beam or structure

   e. **Rail and End Stop Details**
      - Rail size and type
      - Rail clip spacing and installation
      - End stop type, bumper capacity, installation detail

   f. **Design Notes and Load Table**
      - Governing design standards (code editions)
      - Material specifications (steel grade, concrete class)
      - Maximum wheel load per crane (static + impact)
      - Runway deflection limits
      - Special inspection requirements (if any)

4.2 Apply title block, revision table, and drawing number per project document control convention.

4.3 Cross-check all dimensions against DEL-002-03 (Framing Plans) and DEL-002-04 (Structural Sections).

4.4 Add electrical coordination note: identify conductor bar/festoon mounting zone, minimum clearance envelope, and contact electrical engineer for confirmation. (SOW-0059; ASSUMPTION)

**Record:** Issued drawing set with revision index.

---

### Step 5 — Internal Review and Coordination

5.1 Structural engineer performs independent internal check of calculations and drawings.

5.2 Coordinate with:
   - **Architectural** (DEL-001): confirm clearances do not conflict with interior layout
   - **Electrical** (DEL-004): confirm crane power routing and conductor bar zone
   - **PKG-016** (Crane & Lifting Equipment): confirm runway geometry matches crane manufacturer requirements
   - **DEL-002-10** (Calculation Package): ensure calculations cover all elements of DEL-002-07

5.3 Resolve any coordination conflicts. If conflicts cannot be resolved from available information, flag in Guidance.md Conflict Table.

---

### Step 6 — Preliminary Design Review (if not already complete)

6.1 If the crane support approach was not explicitly covered in DEL-002-01 (Preliminary Structural Design), prepare a supplementary preliminary drawing for County review.

6.2 Obtain written County approval or confirmation before proceeding to IFC stamp.

**Source:** RFP §3.3.2 — County approval of preliminary design required before proceeding to final.

---

### Step 6A — Inspection Hold Point Identification
**[C-002]**

6A.1 Identify inspection hold points required under the Alberta Safety Codes Act building permit for the crane support structure construction sequence. Typical hold points may include:
   - Structural concrete pour inspection for crane column corbels or dedicated crane column foundations
   - Crane runway beam installation inspection (beam placement, alignment, and connection verification)
   - Rail installation inspection (rail alignment, clip tightness)
   - Crane runway load test (if required by AHJ)

6A.2 Document the identified hold points on the IFC drawing set or in the design notes, referencing the applicable Safety Code requirements.

6A.3 Coordinate hold point timing with the construction schedule and building permit authority.

**Source:** Guidance Consideration 4 (inspection hold points should be identified in the construction sequence); RFP §3.3.2 (all inspections coordinated); ASSUMPTION for specific hold point identification. Proposed authority: Structural Engineer + Authority Having Jurisdiction (PROPOSAL).

**Record:** Inspection hold point schedule or note on IFC drawings.

---

### Step 6B — Building Permit Verification Gate
**[C-001]**

6B.1 Before the P.Eng. stamp is applied and IFC drawings are issued (Step 7), verify that the building permit status satisfies the prerequisite: "Building permit obtained or in process."

6B.2 Record the building permit status (permit number, date, or in-process status confirmation) in the project records.

6B.3 If the building permit is not yet obtained or in process, do not proceed to IFC stamp. Flag for Project Manager resolution.

**Source:** Prerequisites table (building permit row); RFP §3.3.2 (all applicable Safety Code permits required). Proposed authority: Project Manager (PROPOSAL).

**Record:** Building permit status verification log entry.

---

### Step 7 — P.Eng. Stamp and IFC Issue

7.1 Structural Engineer of Record performs final review of the complete drawing set and calculation backup.

7.2 Apply professional engineer stamp and wet or digital signature to each IFC drawing sheet.

7.3 Issue drawing set as IFC (Issued for Construction).

7.4 Distribute to:
   - Project Manager (record set)
   - Building permit authority (as required)
   - Contractor / Construction team (PKG-011 — Building Structure & Envelope)
   - Crane supplier / installer (PKG-016)
   - Electrical Engineer (DEL-004 coordination)

**Record:** Drawing issue record with recipients, revision status, and date.

---

## Verification

| Check | Method | Pass Criterion |
|---|---|---|
| All required drawing sheets produced | Drawing register check | All anticipated sheets present per Step 4 sheet list |
| Load table present on drawings | Visual check of drawing notes | Maximum wheel load, impact factor, and deflection limits stated |
| Crane supplier data incorporated | Check calculation package (DEL-002-10) | Wheel loads traceable to crane supplier data sheet or documented assumed loads |
| P.Eng. stamp applied | Visual inspection of each issued sheet | Stamp and signature present on every IFC sheet |
| Cross-document consistency | Compare DEL-002-07 dimensions vs DEL-002-03 and DEL-002-04 | No dimensional conflicts |
| County preliminary approval obtained | Review project records | Written approval on file before IFC issued |
| Electrical coordination note present | Visual check of drawing notes | Conductor bar/festoon zone identified or note referencing electrical engineer |
| End stops detailed | Check drawing sheets | End stop details present at each runway termination |
| Building permit status verified **[C-001]** | Check project records per Step 6B | Building permit obtained or in-process confirmed before IFC stamp |
| Inspection hold points identified **[C-002]** | Check IFC drawings or design notes per Step 6A | Inspection hold points documented on drawings or in construction notes |
| Crane data sheet formally received **[F-003]** | Check design input log per Step 1.1 | Data sheet logged with all Step 1.2 fields confirmed present |
| Distribution completeness **[X-003]** | Transmittal log check after Step 7.4 | All distribution recipients listed in Step 7.4 have confirmed receipt of the issued drawing set |

---

## Records

| Record | Format | Retained by |
|---|---|---|
| IFC Drawing Set — DEL-002-07 | Drawing files (PDF and native CAD/BIM) | Structural Engineer; Project Manager |
| Structural Calculation Package (DEL-002-10) — crane support section | Calculation binder or digital file | Structural Engineer |
| Crane supplier data sheet | PDF or manufacturer document | Project Manager; Structural Engineer |
| County preliminary design approval | Email confirmation or meeting minutes | Project Manager |
| Inspection reports (building authority) | Official inspection records | Project Manager; provided to County per RFP §3.3.2 |
| Drawing issue record | Transmittal log | Project Manager |
| Internal design review record | Review checklist or marked-up drawings | Structural Engineer |
