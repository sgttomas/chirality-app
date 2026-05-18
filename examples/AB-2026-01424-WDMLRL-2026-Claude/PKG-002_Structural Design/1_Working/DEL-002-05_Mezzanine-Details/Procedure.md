# Procedure — DEL-002-05 Mezzanine Framing Details

**Document Type:** Procedure (Operational)
**Deliverable ID:** DEL-002-05
**Deliverable Name:** Mezzanine Framing Details
**Revision:** R1 — 2026-02-26 (Pass 3 enrichment)
**Status:** SEMANTIC_READY

---

## 1. Purpose

This procedure describes the steps to **produce** the Mezzanine Framing Details drawing set (DEL-002-05) — from initial information gathering through to Issued for Construction (IFC) release and building permit submission. It is written for the Structural Engineer of Record (or their team) responsible for PKG-002 Structural Design.

---

## 2. Prerequisites

### 2.1 Information Inputs Required Before Starting

| Input | Source / Owner | Status |
|---|---|---|
| Appendix B (Shop) conceptual floor plan | R-04 — accessible | Available |
| RFP §3.4 design requirements (mezzanine) | R-01 — accessible | Available |
| Decomposition entry for DEL-002-05 | WDMLRL_Decomposition_Claude.md | Available |
| Owner confirmation of mezzanine live load (oil tote count, equipment weights) | Owner / Camrose County | TBD — must be obtained |
| Confirmed mezzanine clear height under structure | Architect (PKG-001) / Owner | TBD — must be confirmed (see Guidance.md §3.2) |
| Mezzanine extent over wash bay — confirmed | Owner ruling on CF-DS-002 (see Guidance.md Conflict Table) | TBD — pending human ruling |
| Stair scope boundary — DEL-002-05 vs. DEL-002-09 | Human ruling on CF-DS-001 (see Guidance.md Conflict Table) | TBD — pending human ruling |
| Architectural floor plans (PKG-001) | Architect — DEL-001-02 | TBD — must be coordinated |
| Plumbing layout (cistern location confirmation) | Plumbing Engineer (PKG-006) | TBD |
| Mechanical layout (any penetrations through mezzanine) | Mechanical Engineer (PKG-003) | TBD |
| Electrical layout (mezzanine lighting, any penetrations) | Electrical Engineer (PKG-004) | TBD |
| Geotechnical report | Contractor/Geotech (SOW-0001) | TBD — pending field investigation |
| Building code edition applicable to permit | Camrose County permit authority | TBD — confirm before final design |

### 2.2 Required References

| Reference | Purpose |
|---|---|
| Alberta Building Code (ABC) — applicable edition | Governing structural loads, occupancy, stair/guardrail geometry |
| CSA S16 — Design of Steel Structures | Steel member and connection design (if steel framing selected) |
| CSA A23.3 — Design of Concrete Structures | Anchor and embed design into concrete structure |
| CSA W59 — Welded Steel Construction | Weld procedure and inspection (if welded connections) |
| DEL-002-03 Structural Framing Plans (when available) | Coordinate mezzanine columns and bearings with main building framing |
| DEL-002-10 Structural Calculation Package | Calculations to support this drawing set |
| DEL-002-12 Structural Specification | Material grades and workmanship requirements governing this work |

### 2.3 Declared Upstream Dependencies

Per _DEPENDENCIES.md: coordination is declared as NOT_TRACKED. Extracted dependency register has not been run. The following upstream items are inferred from context (ASSUMPTION — to be confirmed by human):

- DEL-002-03 Structural Framing Plans: mezzanine framing must align with overall building framing grid.
- DEL-001-02 Architectural Floor Plans: confirm room boundaries, clearances, and stair location.
- PKG-006 plumbing layout: confirm cistern and stair do not conflict.

---

## 3. Steps

### Step 1 — Resolve Pre-Design Decisions

**Purpose:** Obtain information and rulings needed before structural design can begin.

**Actions:**
1. Submit CF-DS-001 and CF-DS-002 from Guidance.md Conflict Table to ORCHESTRATOR / human for ruling. Do not proceed with mezzanine extent or stair scope until rulings are received.
2. Request from Owner / Camrose County:
   - Maximum number and type of oil totes to be stored on mezzanine simultaneously.
   - Any specific pumping equipment weights and footprints.
   - Desired clear height below mezzanine in each room (parts room, utility room, wash bay).
   - Confirmation of whether fork truck or telehandler access is required under the mezzanine.
3. Confirm applicable ABC code edition with Camrose County permit authority.
4. Coordinate with Architect (PKG-001) on:
   - Room boundary dimensions for parts room, utility room, wash bay.
   - Final stair location.
   - Mezzanine clear height requirement from architectural standpoint.
5. Coordinate with Plumbing Engineer (PKG-006) on cistern footprint and maintenance access clearances in utility room.

**Output:** Pre-design decision record (may be captured in _MEMORY.md or a project decision log). Ruling on CF-DS-001 and CF-DS-002.

---

### Step 2 — Establish Design Parameters

**Purpose:** Set the structural design basis for the mezzanine.

> **HOLD POINT (C-003):** Before proceeding with Step 2 actions, the following gate condition must be satisfied:
>
> | Gate | Condition | Evidence Required |
> |---|---|---|
> | **G-001: Owner Load Confirmation** | Owner / Camrose County has provided documented confirmation of: (a) maximum oil tote count and arrangement, (b) equipment list with weights, and (c) desired mezzanine clear height. | Written Owner response (email, letter, or meeting minutes signed by Owner representative). Record in pre-design decision record. |
>
> **Do not proceed to Step 2 actions until G-001 is satisfied.** If Owner confirmation is delayed, escalate to Project Manager. Source: Procedure Step 1 action 2; this formalizes the prerequisite as a hold point per C-003.

> **Readiness Check (F-003):** Before establishing mezzanine column locations in Step 2 action 2, confirm that the building grid from DEL-002-03 (Structural Framing Plans) is available. If DEL-002-03 is not yet issued, coordinate with the Structural Engineer of Record to obtain the preliminary building grid. Do not finalize mezzanine column locations without this input. Source: Procedure §2.3 (upstream dependency on DEL-002-03); Step 2 action 2.

**Actions:**
1. Establish design live load:
   - Calculate load from oil totes (number x weight, divided by mezzanine area) -> distributed load in kPa.
   - Compare to ABC minimum storage live load -> use greater value.
   - Record design live load (kPa or psf) in calculation package (DEL-002-10).
2. Establish mezzanine plan dimensions:
   - Confirm extent: over parts room (~400 sq ft), utility room, and wash bay (24' wide) per R-04, subject to CF-DS-002 ruling.
   - Confirm column grid locations in coordination with DEL-002-03 building grid (per readiness check F-003 above).
3. Confirm mezzanine system:
   - Select framing material (steel or concrete) per Guidance.md §3.1 and §4.
   - Select deck system (grating, concrete-on-composite deck, checker plate) — refer to Guidance.md §4.1 (Deck System Selection Criteria) for evaluation criteria.
   - Document selection rationale.
4. Establish mezzanine floor elevation based on:
   - Required clear height below (parts room, utility room, wash bay).
   - Available height within 35' building envelope.
   - Stair geometry requirements.

**Output:** Design parameters recorded in calculation package (DEL-002-10). Parameters shared with Architect for coordination.

---

### Step 3 — Structural Analysis and Member Sizing

**Purpose:** Perform structural calculations to size all mezzanine framing members and connections.

**Actions:**
1. Perform structural analysis for mezzanine framing under:
   - Dead load (self-weight of deck, framing, finishes).
   - Design live load (established in Step 2).
   - Snow load transfer (if applicable — verify if mezzanine is internal or if roof load path affects mezzanine columns; see REQ-DS-020).
   - Seismic load per ABC (determine applicability per REQ-DS-016; if applicable, include in analysis).
2. Size primary beams, secondary joists (or beams), and columns.
3. Design all connections:
   - Beam-to-column connections.
   - Beam-to-wall or beam-to-concrete connections (ledger, corbel, or bearing on concrete).
   - Column base plates and anchor bolts (or cast-in embeds) into concrete slab or foundation.
4. Design guardrail posts for horizontal load per ABC (refer to REQ-DS-010 for specific load value requirement).
5. Design stair stringers, treads, and landings (subject to CF-DS-001 ruling).
6. Design embed plates and anchor bolts for integration with concrete structure — coordinate timing with concrete pours (per REQ-DS-019, Structural Engineer approval required before pour).
7. Check deflection limits per ABC / CSA S16 for serviceability under live load (per REQ-DS-018, state limits on drawings).
8. Address fire protection applicability per ABC occupancy (per REQ-DS-017).
9. Document all calculations in DEL-002-10 Structural Calculation Package.

**Output:** Completed structural calculations (DEL-002-10 draft).

---

### Step 3A — Corrosion Protection Specification (A-004)

**Purpose:** Specify corrosion protection for steel framing members in the wash bay zone.

> This step applies only if the mezzanine extends over the wash bay (per CF-DS-002 ruling) and steel framing is selected (per Step 2 action 3).

**Actions:**
1. Identify all steel framing members within or above the wash bay zone (beams, columns, bracing, deck supports, and connections).
2. Select corrosion protection system appropriate for wash bay exposure:
   - Hot-dip galvanizing per CSA G189 or equivalent (ASSUMPTION: applicable standard — location TBD).
   - Alternatively, an industrial paint system rated for chemical and moisture exposure.
   - Document the selected system and its basis.
3. Specify corrosion protection on the mezzanine framing detail drawings for all wash bay zone members.
4. Coordinate with DEL-002-12 Structural Specification to confirm material and coating specifications are consistent.

**Output:** Corrosion protection specification noted on drawings and coordinated with DEL-002-12.

Source: Guidance.md §3.3 (wash bay corrosion environment); REQ-DS-015 (corrosion protection requirement). ASSUMPTION: CSA G189 or equivalent is applicable — confirm with Structural Engineer of Record.

---

### Step 4 — Produce Mezzanine Framing Details Drawing Set

**Purpose:** Translate structural calculations into IFC-quality drawings.

**Actions:**
1. Produce the following drawing sheets (minimum per REQ-DS-013):
   - Mezzanine Framing Plan: plan view with all beam/joist sizes, column locations, dimensions, and design live load noted.
   - Mezzanine Sections (minimum 2 — longitudinal and transverse): show framing depth, clearance dimensions, and connection to concrete structure.
   - Framing Connection Details: typical and special connections (beam-to-column, beam-to-wall, deck-to-beam).
   - Stair Framing Details (subject to CF-DS-001 ruling): stringers, treads, landings, handrail connections, rise/run dimensions.
   - Guardrail / Edge Protection Details: height, post spacing, infill, design loading noted (per REQ-DS-010 — state horizontal design load value).
   - Anchor / Embed Details: column base plates, embed plates, post-installed anchor details (if used).
   - General Notes sheet: design live load, dead load basis, material grades (steel grade, concrete strength for embeds), weld specifications, bolt grades, applicable codes (ABC edition, CSA S16 edition, CSA A23.3 edition), deflection limits (per REQ-DS-018), fire protection determination (per REQ-DS-017), seismic determination (per REQ-DS-016), corrosion protection for wash bay zone (per REQ-DS-015, if applicable).
2. Coordinate drawing content with:
   - DEL-002-03 Structural Framing Plans (column grid, beam grid consistency).
   - DEL-002-04 Structural Sections (avoid duplication; cross-reference where overlap occurs).
   - DEL-002-09 Stair Details (per CF-DS-001 ruling — either include or cross-reference).
   - Architectural drawings (PKG-001): room boundaries, stair location, mezzanine clear height.
3. Assign drawing numbers per project drawing register (see Datasheet §4.1, drawing numbering note E-001).

**Output:** Draft drawing set (internal review quality).

---

### Step 5 — Internal Review and Correction

**Purpose:** Ensure drawing set is complete, consistent, and code-compliant before Structural Engineer of Record stamps.

**Actions:**
1. Internal quality review by a senior structural engineer (not the author):
   - Check all member sizes against calculations.
   - Check all connection details against calculations.
   - Check code compliance: guardrail height and horizontal design load, stair geometry, live load notation, deflection limits, fire protection, seismic determination, corrosion protection.
   - Check cross-references to other drawing sets.
   - Check consistency with DEL-002-12 Structural Specification material requirements.
2. Incorporate corrections from internal review.
3. Confirm with multi-discipline team (Architect, Mechanical, Plumbing, Electrical) that no late coordination issues remain. Obtain signed coordination confirmation per REQ-DS-012 verification approach (F-002).

**Output:** Review-corrected drawing set ready for P.Eng. stamp.

---

### Step 6 — P.Eng. Stamp and IFC Release

**Purpose:** Formally issue the drawing set as Issued for Construction.

**Actions:**
1. Structural Engineer of Record reviews final drawings and confirms:
   - All calculations are complete and support the drawings.
   - All code requirements are satisfied.
   - All coordination issues are resolved.
2. Apply Alberta P.Eng. stamp and signature to all drawing sheets (REQ-DS-014).
3. Issue drawing set as IFC within the project drawing register.
4. Include stamped drawings in building permit submission package (SOW-0006).

**Output:** Stamped IFC drawing set (DEL-002-05 — Issued for Construction). Submitted to Camrose County permit authority as part of building permit application.

---

### Step 7 — Construction Support

**Purpose:** Support contractor during mezzanine framing construction to ensure conformance with IFC drawings.

**Actions:**
1. Review contractor's shop drawings for mezzanine steel framing (if applicable) and respond within agreed turnaround time. Record shop drawing review as a supporting document (per Specification §5.2, X-002).
2. Review contractor's embed installation plan and confirm timing relative to concrete pours. Confirm Structural Engineer of Record approval of embed/anchor bolt locations before each applicable concrete pour (per REQ-DS-019).
3. Conduct site reviews at key construction stages:
   - Inspect embed/anchor bolt installation before concrete pour.
   - Inspect mezzanine steel erection and connections before deck installation.
   - Inspect completed mezzanine framing, deck, guardrails, and stair before architectural/MEP trades begin work at mezzanine level.
4. **Welding inspection scope for mezzanine connections (D-002):**
   - Identify all welded connections in the mezzanine framing (beam-to-column, column base plate welds, bracing connections, guardrail post welds, stair stringer connections).
   - Specify welding inspection type per CSA W59 requirements (visual inspection at minimum; non-destructive testing for critical connections as determined by the Structural Engineer of Record).
   - Specify inspection frequency (e.g., 100% visual on all shop and field welds; NDE sampling rate for critical connections per CSA W59 — ASSUMPTION: specific rate TBD by Structural Engineer of Record).
   - Document CSA W59 compliance verification in field review reports.
   Source: Specification §3 Standards (CSA W59); Specification §4 Field Verification (welding inspection). ASSUMPTION: CSA W59 is applicable if welded connections are used — confirm edition per C-002.
5. Issue field review reports (confirm County rep is present for inspections per R-01 §3.3.2 — SOW-0084, SOW-0085). See Guidance.md §7 for terminology distinction between "field review report" and "inspection report."
6. Issue any Supplemental Instructions or Contemplated Change Notices through proper design-build change management process if site conditions require field modifications.

**Output:** Shop drawing review records, field review reports, as-built markup (fed into as-built survey SOW-0004).

---

## 4. Verification

| Check | Verification Method | Timing |
|---|---|---|
| Design live load sufficient for oil totes + equipment | Calculation review (DEL-002-10); load value stated on drawings | Pre-IFC |
| Mezzanine plan covers required rooms | Drawing review vs. App B floor plan | Pre-IFC |
| Stair access detailed and code-compliant | Drawing review: rise/run, handrail height per ABC | Pre-IFC |
| Guardrail height and loading per ABC | Drawing review: dimension and horizontal design load value noted (REQ-DS-010) | Pre-IFC |
| Deflection limits stated on drawings | Drawing review: limit values per REQ-DS-018 | Pre-IFC |
| Seismic design determined | Calculation review: determination per REQ-DS-016 | Pre-IFC |
| Fire protection determined | Drawing review: determination per REQ-DS-017 | Pre-IFC |
| Corrosion protection specified (wash bay) | Drawing review: specification per REQ-DS-015 (if applicable) | Pre-IFC |
| P.Eng. stamp on all sheets | Title block audit | At IFC issue |
| Owner load confirmation documented | G-001 gate evidence (Step 2) | Before analysis |
| DEL-002-03 grid available | F-003 readiness check (Step 2) | Before column layout |
| Column/embed locations coordinated with concrete pours | Construction meeting / embed inspection (REQ-DS-019) | During construction |
| Mezzanine framing erected to IFC | Site review and field review report | During construction |
| Guardrails and stair installed to IFC | Site review and field review report | During construction |
| Welding inspection completed | Field review reports per CSA W59 (D-002) | During construction |
| County inspector present at inspections | Attendance confirmation per SOW-0084 | During construction |
| All inspection reports provided to County | Document transmittal per SOW-0085 | During/after construction |
| As-built conforms to IFC | As-built survey verification (D-001) | Post-construction |

---

## 5. Records

| Record | Description | Responsible |
|---|---|---|
| Calculation Package (DEL-002-10) | Structural calculations supporting all mezzanine member and connection designs | Structural Engineer of Record |
| IFC Drawing Set (DEL-002-05) | Stamped, signed IFC drawings submitted for permit | Structural Engineer of Record |
| Building Permit (SOW-0006) | Issued by Camrose County permit authority | Contractor (Prime) |
| Shop Drawing Review Records | Reviewed and stamped/commented contractor shop drawings for mezzanine steel (X-002) | Structural Engineer of Record |
| Field Review Reports | Site review records at each construction inspection stage (see Guidance §7 for terminology) | Structural Engineer of Record |
| Inspection Reports (copies to County) | All Safety Code inspections per SOW-0085 (see Guidance §7 for terminology) | Contractor (Prime) |
| As-Built Markup | Marked-up drawings reflecting as-built conditions; input to as-built survey SOW-0004; verified against IFC per D-001 | Structural Engineer of Record / Contractor |
| Pre-Design Decision Record | Record of Owner confirmations (live load, clearances, mezzanine extent) from Step 1; includes G-001 gate evidence | Project Manager / Structural Engineer |
| Welding Inspection Records | CSA W59 compliance verification records for mezzanine connections (D-002) | Structural Engineer of Record / Welding Inspector |
