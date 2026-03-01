# Procedure — DEL-001-04 Building Sections

**Document Type:** Procedure (operational)
**Deliverable ID:** DEL-001-04
**Deliverable Name:** Building Sections
**Package:** PKG-001 Architectural Design
**Revision:** R1 — 2026-02-26 (4_DOCUMENTS Pass 3 — Semantic Lensing Enrichment)

---

## Purpose

This procedure describes the steps to produce the Building Sections drawing set (DEL-001-04) as part of the final architectural design for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. It covers the workflow from section cut selection through to IFC issue, including internal reviews and inter-discipline coordination checkpoints.

The building sections must be delivered at two stages: (1) Preliminary Design for County approval, and (2) IFC (Issued for Construction) with P.Eng. stamp. This procedure applies to both stages, with stage-specific verification steps noted.

**Source:** RFP §3.3.2; Decomposition OBJ-003.

---

## Prerequisites

### Upstream Information Required

| Item | Source | Status |
|---|---|---|
| Conceptual floor plan and building notes | App B (Shop) — accessible | Available |
| RFP Design Requirements | RFP §3.4 — accessible | Available |
| Confirmed plan dimensions (architectural) | DEL-001-02 Floor Plans | Must exist before sections are finalized |
| Structural system determination (concrete structure, column grid, wall thickness) | PKG-002 Structural Design — structural engineer | Required before IFC sections |
| Mezzanine framing elevation and depth | DEL-002-05 Mezzanine Framing Details | Required before mezzanine section is finalized |
| Service pit structural details (depth, walls) | DEL-002-06 Service Pit / Trench Structural Details | Required before pit section is finalized |
| Crane runway beam elevations | DEL-002-07 Crane Support Structure Details | Required before crane clearance sections are finalized. **(X-002):** Receipt must be verified before finalizing crane clearance sections — see Verification table. |
| Geotechnical report | Proponent-obtained (RFP §3.3.2) | Required before foundation/slab assumptions are made. **(F-002):** Receipt must be verified before proceeding with foundation/slab representations in sections — see Verification table. |

### Software and Tools

- Architectural CAD or BIM platform (TBD by Architect)
- Discipline coordination model / clash detection (TBD)

> **TBD (A-004):** Minimum CAD/BIM platform requirements or selection criteria should be specified rather than left entirely to "TBD by Architect." At minimum, the platform must support: (a) 2D section production at required scales (1:100 and 1:50), (b) grid line and level datum management, (c) export to formats accepted by structural/mechanical/electrical consultants for coordination. If BIM-based coordination is expected, the platform must support IFC export or a specified model exchange format. Proposed authority: Architect. (Source: Procedure > Prerequisites > Software and Tools.)

### Reference Documents

| Ref | Document |
|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf (§3.1, §3.3.2, §3.4) |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf (conceptual floor plan) |
| — | Alberta Building Code (applicable edition) — location TBD |
| — | CCDC 14-2013 — location TBD |
| DEL-001-02 | Architectural Floor Plans (section cut marks must match) |
| DEL-001-11 | Architectural Specification (assembly types referenced on sections) |

---

## Steps

### Phase A — Preliminary Design (for County Approval)

**Step A-1 — Establish Vertical Datum and Level Strategy**

1. Confirm the site benchmark and finished floor level (FFL) of the addition relative to existing grade. Coordinate with civil design (PKG-005) and geotechnical report.
2. Establish the primary datum: finished floor level = 0.00 m (or as set by project convention).
3. Set the 35' (10,668 mm) ceiling height as a target elevation above FFL.
4. Mark the datum and ceiling height on a working section diagram shared with the structural engineer.

**Source:** RFP §3.4; App B (Shop) notes; ASSUMPTION applied for datum convention.

---

**Step A-2 — Identify Section Cut Locations on Floor Plan**

1. Working from the coordinated floor plan (DEL-001-02), identify section cut locations that expose the following conditions:
   - Full longitudinal section (primary) through main shop bays
   - Transverse section through repair bays (including 24' bay widths and overhead door openings)
   - Transverse section through wash bay (including overhead door and mud sump reference)
   - Section through mezzanine zone (parts room, utility room, wash bay — mezzanine above)
   - Section through service pit / trench
2. Mark section cut arrows and identifiers on the floor plan drawing.
3. Confirm no two section cuts overlap with the same building conditions without documentation purpose.

**Source:** RFP §3.1, §3.4; App B (Shop) floor plan; Specification REQ-001; ASSUMPTION applied for minimum cut list.

---

**Step A-3 — Draft Preliminary Section Views**

For each section cut identified in Step A-2:

1. Draw the section to a working scale (1:100 minimum for overview; 1:50 for pit and mezzanine).
2. Show the following elements at preliminary stage:
   - Exterior wall outline and roof profile
   - Interior floor level (FFL) and ceiling height (35' datum)
   - Mezzanine floor level (use assumed elevation; note as ASSUMPTION until structural confirms)
   - Service pit indication (depth TBD — note as TBD)
   - Overhead crane indication (runway beam elevation TBD — note as TBD)
   - Overhead door openings (height TBD — note as TBD)
   - Space labels (Main Shop, Wash Bay, Parts Room, Utility Room, Office, Mezzanine, Service Pit)
3. Do not detail assemblies at preliminary stage — use generic wall/roof symbols.
4. Include grid reference lines coordinated with structural column grid (TBD from structural engineer).

**Source:** RFP §3.3.2; Decomposition OBJ-003; ASSUMPTION applied for preliminary drawing content.

---

**Step A-4 — Internal Architectural Review**

1. Architect reviews section drawings for:
   - Correct 35' ceiling height shown
   - All required space types represented in at least one section
   - Section cut marks match those shown on DEL-001-02 Floor Plans
   - No spatial conflicts visible (e.g., mezzanine blocking crane clearance — flag as conflict if present)
2. Record and resolve any internal conflicts before issuing for structural coordination.

---

**Step A-5 — Issue for Structural Coordination**

1. Issue preliminary sections to structural engineer with the following coordination requests:
   - Confirm structural system (wall thickness, column size) for incorporation into sections
   - Provide mezzanine framing depth and confirmed floor elevation
   - Provide service pit dimensions (depth, wall construction) for pit section
   - Provide crane runway beam elevation and clearance dimensions
2. Record the date of issue and the structural engineer's acknowledgment.

**Source:** Decomposition OBJ-003; ASSUMPTION applied for coordination protocol.

---

**Step A-6 — Submit Preliminary Design to County**

1. Incorporate any structural coordination responses received prior to preliminary submission (update TBD items where information is available).
2. Compile preliminary drawing set for County approval per RFP §3.3.2.
3. Submit to County project manager.
4. Record County approval date; note any County comments requiring revision.

**Source:** RFP §3.3.2.

---

### Phase B — Final Design / IFC

> **Gate Condition (E-002):** Before proceeding to Phase B, confirm that County approval of the Preliminary Design submission (Step A-6) has been received and that any County comments have been addressed or dispositioned. Record the County approval date and comment resolution status. If County approval has not been received, do not proceed to Phase B. (Source: Procedure Step A-6; Procedure Verification table.)

**Step B-1 — Incorporate Structural Coordination Responses**

1. Receive confirmed structural information from PKG-002 (column grid, slab thickness, mezzanine framing, pit walls, crane runways, roof structure).
2. Update all section drawings to reflect confirmed structural dimensions and elevations.
3. Replace all ASSUMPTION notes with confirmed values, or maintain as TBD if information is still outstanding (flag to Architect-of-Record).

**Source:** Decomposition OBJ-003; ASSUMPTION applied for coordination sequence.

---

**Step B-2 — Add Assembly and Material Annotations**

1. Add wall assembly callout references consistent with DEL-001-11 Architectural Specification.
2. Add roof assembly callout references.
3. Add floor assembly annotations (slab thickness, steel plate locations per App B and structural drawings).
4. Add insulation and vapour barrier indication per assembly types.
5. Confirm all annotations are consistent with other PKG-001 drawings (no conflicting assembly references).

**Source:** RFP §3.3.2; App B (Shop); Decomposition SOW-0024; ASSUMPTION applied for assembly annotation content.

---

**Step B-3 — Verify Code Compliance Items in Sections**

1. Confirm mezzanine stair geometry complies with Alberta Building Code (tread, riser, landing, handrail — specific clause TBD).
2. Confirm minimum headroom clearances in occupied spaces below mezzanine (clause TBD — Alberta Building Code).
3. Confirm service pit ventilation note/coordination is present.
4. Confirm overhead door clear heights are shown and adequate for intended equipment (motor scraper for wash bay — specific height TBD).
5. Document any code items that require Architect or Engineer judgment and flag for review.

**Source:** RFP §3.3.2; Alberta Building Code (location TBD); Alberta Safety Codes Act (location TBD).

---

**Step B-4 — Inter-Discipline Coordination Review**

1. Conduct a coordination review with:
   - Structural engineer (PKG-002): confirm all structural elements shown in sections match structural drawings
   - Mechanical engineer (PKG-003): confirm duct routing and equipment clearances do not conflict with section geometry
   - Electrical engineer (PKG-004): confirm high bay light mounting heights and crane power routing fit within ceiling envelope
2. Document any clashes found and resolve before IFC issue.
3. Record the names of reviewers and dates of review.
4. Use the following minimum-content checklist for the coordination review record **(A-005)**:

**Inter-Discipline Coordination Review Record — Minimum Content (ASSUMPTION):**

| Field | Content |
|---|---|
| Review date | Date of coordination review session |
| Participants | Names and disciplines of all reviewers |
| Drawings reviewed | List of section drawing sheet numbers reviewed |
| Clashes identified | For each clash: location, type (hard / clearance / workflow), severity, affected disciplines |
| Resolutions | For each clash: agreed resolution, responsible party, target date |
| Unresolved items | Any clashes remaining open, with justification and resolution path |
| Sign-off | Reviewer acknowledgment (name, date, discipline) |

> **TBD (A-005):** The review record template above is ASSUMPTION-based. The Architect should confirm or revise the minimum content and provide a project-standard template if one exists. Proposed authority: Architect. (Source: Procedure Step B-4; Specification REQ-010 Verification.)

**Source:** RFP §1.0; Decomposition OBJ-003.

---

**Step B-5 — Final Drawing Check and P.Eng. Stamp**

1. Architect-of-Record conducts final drawing review:
   - All section cuts from Step A-2 are present and complete
   - All TBD items resolved or documented with justification
   - Section cut identifiers match floor plan (DEL-001-02)
   - Drawing title block complete (project name, drawing number, revision, date, scale)
2. P.Eng. licensed in Alberta reviews and stamps IFC drawings.
3. Issue IFC drawing set.

**Source:** RFP §3.3.2; Decomposition OBJ-003.

---

**Step B-6 — Issue IFC Drawing Set**

1. Issue signed and stamped IFC Building Sections drawing set.
2. Distribute to: County project manager, structural engineer, mechanical engineer, electrical engineer, civil engineer, construction team.
3. Record issue date and distribution list.

---

## Verification

| Check | Verification Method | Timing |
|---|---|---|
| 35' ceiling height shown on drawings | Dimension annotation review | After Step A-3; After Step B-1 |
| All section cut locations match floor plan | Cross-reference DEL-001-02 | After Step A-2; Before IFC issue |
| Mezzanine elevation confirmed by structural | Structural engineer sign-off or coordination memo | Before Step B-2 |
| Service pit depth confirmed | Structural engineer input; shown on pit section | Before IFC issue |
| Crane clearance dimensions shown or referenced | Drawing review vs. crane and structural data | Before IFC issue |
| Code compliance items verified | Architect internal checklist; P.Eng. review | Step B-3; Step B-5 |
| No outstanding TBD items at IFC | Drawing QA sweep | Step B-5 |
| P.Eng. stamp present on IFC drawings | Visual confirmation on issued set | Step B-5 |
| Preliminary design approved by County | County written approval record; confirmed as gate condition before Phase B **(E-002)** | After Step A-6; before Phase B |
| Geotechnical report received **(F-002)** | Geotechnical report receipt confirmed; content reviewed for foundation/slab assumptions | Before foundation/slab representations are finalized |
| Crane runway beam elevation received **(X-002)** | Crane runway beam elevation data confirmed from structural engineer (DEL-002-07) | Before crane clearance sections are finalized |
| Section-drawing QA checklist completed **(E-003)** | QA checklist artifact completed covering: dimension chain closure, annotation completeness, grid line consistency, scale block accuracy, section cut identifier match to floor plan | Step B-5 (final drawing review) |

---

## Records

| Record | Description | Produced At |
|---|---|---|
| Preliminary section drawings | Drawing set issued to County for approval | Step A-6 |
| County approval record | Written approval or comments from County | After Step A-6 |
| Structural coordination memo / RFI responses | Record of confirmed structural dimensions | Step B-1 |
| Inter-discipline coordination review record | Clash log and resolution record | Step B-4 |
| IFC Building Sections drawing set | Final stamped drawings | Step B-6 |
| Drawing issue register / transmittal | Record of distribution at each issue | Steps A-6, B-6 |
| Section-drawing QA checklist **(E-003)** | Completed checklist artifact documenting: dimension chain closure, annotation completeness, grid line consistency, scale block accuracy, section identifier consistency with floor plan. ASSUMPTION: checklist format TBD by Architect. | Step B-5 |
