# Procedure: DEL-02-02 — Firehall Apparatus Bays & Support Spaces

**Enrichment Status:** Pass 3 semantic lensing complete (2026-02-17). Pre-design readiness checklist, Owner operational review step, formal code-compliance review checklist, and construction hold/witness points protocol added.

---

## Purpose

This procedure describes the steps to **produce** the DEL-02-02 deliverable artifacts during the proposal and subsequent detailed design phases, and the steps to **verify** that the completed design satisfies the requirements of this deliverable.

The deliverable has two phases of production:
- **Phase A: Proposal-stage** — produce the conceptual layouts, services concept, and coordination narrative for submission with the RFP response.
- **Phase B: Detailed design** — elaborate the proposal artifacts into construction documents through the design milestone submission sequence.

---

## Prerequisites

### Upstream Dependencies

No upstream dependencies are formally declared in _DEPENDENCIES.md. The following inputs are required before this deliverable can be fully completed:

| Input | Source | Status |
|---|---|---|
| RFP 2024_004 + Appendices (OSR, Functional Program) | _Sources/ | Available |
| Addendum 03 (July 31, 2024) | _Sources/ | Available |
| Decomposition FINAL v1.0 PHASE7 | _Decomposition/ | Available |
| Site Grading drawings (preferred building orientation) | Addendum 03 §1.20; Appendix E | Available (provided post-award per §1.20) |
| DEL-02-01 (Architectural Program) | PKG-002/1_Working/DEL-02-01 | Required to confirm overall floor plan zone allocation for firehall wing |
| DEL-02-04 (Envelope/Doors) | PKG-002/1_Working/DEL-02-04 | Required for overhead door specifications and structural bay clearances |
| DEL-02-05 (Mechanical) | PKG-002/1_Working/DEL-02-05 | Required for exhaust system design coordination and plumbing (sumps, fill station, decon showers) |
| DEL-02-06 (Electrical/IT) | PKG-002/1_Working/DEL-02-06 | Required for electrical-in-bays layout, display system connectivity, PA |
| DEL-02-07 (Emergency Power) | PKG-002/1_Working/DEL-02-07 | Required for secondary door-opening mechanism specification |

### Required References

- OSR §10.2, §10.3.5, §10.3.8, §10.3.9, §10.6, §11.1.1
- Addendum 03 §1.8, §1.10, §1.12, §1.13, §1.14, §1.15, §1.16, §1.21
- Functional Program (Appendix B) — room schedule table
- Alberta Building Code (ABC) — occupancy, egress, accessibility requirements (location TBD; obtain full text before detailed design)

### Personnel Required

- Architect (Arch lead) — layout, space planning, room data sheets
- Mechanical Engineer (MEP lead) — exhaust mitigation, HVAC, plumbing coordination
- Electrical Engineer — bay services electrical, display system
- Fire Department representative (Owner) — operational review and confirmation
- Project Manager — coordination protocol management (see below)

### Interface Coordination Protocol [Lensing: D-002]

A formal coordination mechanism is required for tracking interface resolution with DEL-02-04 (Envelope/Doors), DEL-02-05 (Mechanical), DEL-02-06 (Electrical/IT), and DEL-02-07 (Emergency Power). The following protocol is proposed:

1. **Interface Register:** Maintain a log of all cross-deliverable interface items, their status, and responsible party. Specification Documentation section requires a "Coordination matrix" as an artifact — this register fulfills that requirement.
2. **Coordination Meeting Cadence:** TBD — establish regular coordination meetings (e.g., bi-weekly) during detailed design to review interface items.
3. **Sign-off Checklist:** Each interface item shall require sign-off from both the originating and receiving deliverable leads before it is considered resolved.
4. **Tracking:** Project Manager to own the interface register and escalate unresolved items.

**Note:** This protocol is proposed but not yet formalized. The specific cadence and tools should be determined at project kickoff.

---

## Steps

### Phase A: Proposal-Stage Production

**Step 1 — Review Requirements**

1.1 Read and extract all relevant scope items from the decomposition: SOW-0202, SOW-0203, SOW-0205, SOW-0206 (and related items SOW-0204, SOW-0214 for coordination context).

1.2 Review the Functional Program (Appendix B) room schedule for apparatus bay and support room sizing targets.

1.3 Review Addendum 03 §1.8, §1.10, §1.12, §1.13, §1.14, §1.15, §1.16, §1.21 for all firehall-specific clarifications.

1.4 Note interface scope items owned by other deliverables (DEL-02-04, DEL-02-05, DEL-02-06, DEL-02-07) to avoid scope duplication.

**Step 1A — Pre-Design Readiness Checklist** [Lensing: X-001]

Before commencing bay geometry (Step 2), confirm the following prerequisite inputs are available. If any item is not available, record as a risk/assumption and flag for resolution before detailed design:

| Input | Status | Action if Unavailable |
|---|---|---|
| Owner apparatus fleet data (actual Type 1 engine and aerial dimensions) | TBD — assumed dimensions used (see Step 2.1) | Flag as critical TBD; proceed with assumptions for proposal stage only [Lensing: A-004] |
| Alberta Building Code (ABC) full text | TBD — location not yet obtained | Cannot confirm occupancy, egress, or accessibility requirements without full text [Lensing: A-001] |
| AHJ post-disaster classification ruling | Intent to exempt per OSR §10.3.5 — formal ruling TBD | Proceed with exempted classification; confirm with AHJ before detailed design |
| NFPA 1, NFPA 1989, Alberta OHS applicability confirmation | ASSUMPTION — confirm with AHJ/MEP lead | Proceed with assumption; add to Standards verification [Lensing: F-002] |
| IES lighting criteria for apparatus bays | TBD — criteria not yet defined | Defer to Electrical Engineer during detailed design [Lensing: B-002] |

**Step 2 — Establish Apparatus Bay Geometry**

2.1 Determine apparatus bay plan dimensions based on:
- Type 1 engine dimensions (**ASSUMPTION:** typical Type 1 engine ~35--40 ft long, ~8--9 ft wide; **confirm with Owner's actual apparatus list before finalizing bay geometry** [Lensing: A-004])
- Type 1 aerial apparatus dimensions (**ASSUMPTION:** aerial apparatus may exceed 45 ft; **confirm with Owner** [Lensing: A-004])
- Target area: 2,000–2,200 sf per bay (Addendum 03 §1.21)
- Clear height: minimum 16 ft overhead door + structural depth above (Addendum 03 §1.10)

2.2 Establish drive-through configuration: confirm entry and egress doors on opposite ends of building.

2.3 Coordinate bay orientation with overall site plan (DEL-03-01) — fire apparatus must have direct heavy-duty asphalt routing to Waskasoo Avenue (SOW-0107).

**Step 3 — Lay Out Bay Services**

3.1 Mark electrical drop locations within each bay (coordinate with DEL-02-06).

3.2 Mark two (2) compressed air connections per bay (ceiling drop or wall mount — ASSUMPTION: ceiling-mounted drops per Functional Program Appendix B description).

3.3 Mark two (2) exhaust mitigation connection points per bay; coordinate with DEL-02-05 for system type (hose-reel, rail, or other direct capture).

3.4 Mark bay sump locations (floor drains) per bay (Addendum 03 §1.8).

3.5 Mark water fill station location (one ground-level station in fire apparatus bay area, 2-inch minimum; Addendum 03 §1.16).

3.6 Identify apparatus display system location: wall mount in bay closest to office area (OSR §10.6).

**Step 4 — Lay Out Decontamination and Support Spaces**

4.1 Position decontamination area between apparatus bays and office/shared spaces to establish contamination gradient (see Guidance — Principles).

4.2 Lay out within the decon zone:
- Decontamination room (150–200 sf)
- Two decontamination shower/WR units (50–60 sf each)
- Transition/access path to bunker gear locker room

4.3 Lay out adjacent to the decon zone:
- Bunker gear locker room (40 lockers; 350–550 sf range for Duty Gear Room; allow firefighter circulation)
- Fire gear storage (200–350 sf; climate controlled)
- SCBA/cascade room (150–200 sf; note FF&E exclusion for SCBA equipment)
- Compressor room (100–150 sf; for compressed air and SCBA fill system)
- Medical/EMS equipment storage (50–70 sf)

4.4 Confirm egress paths from all rooms comply with ABC (door widths, travel distance, assembly).

**Step 5 — Develop Bay Services Concept Narrative**

5.1 Prepare a short concept narrative (1–2 pages) describing:
- Compressed air system approach (compressor room → distribution → bay drops)
- Exhaust mitigation approach (system type, capacity basis of two apparatus per bay)
- Electrical in bays approach (panel location, circuit types, door operator coordination)

5.2 Note all interface decisions to be resolved in detailed design (e.g., exhaust system product selection, compressed air pressure/volume specification).

**Step 6 — Develop Bay Exhaust Mitigation Coordination Note**

6.1 Prepare a coordination note to DEL-02-05 specifying:
- Four bays; two exhaust connections per bay; two apparatus per bay capacity
- Preferred system type (hose-reel or rail) TBD — note in proposal as "direct capture system, type to be confirmed in detailed design"
- Bay plan layout reference showing connection point locations

**Step 7 — Produce Apparatus Bay Display Concept**

7.1 Describe the display system: wall-mounted TV/monitor in Bay 1 (closest to office), wired network connection for laptop, for dispatch data display (OSR §10.6).

7.2 Note IT/data infrastructure coordination with DEL-02-06.

**Step 8 — Assemble Proposal-Stage Package**

8.1 Compile the following artifacts:
- Apparatus bay layouts (floor plan drawings or diagrams)
- Decontamination/gear locker layouts (floor plan drawings or diagrams)
- Compressed air + bay services concept (narrative and/or schematic)
- Bay exhaust mitigation coordination note
- Apparatus bay display concept (narrative)

8.2 Review artifacts against all REQ-0202-xx requirements in Specification.md.

8.3 Identify any open items or items deferred to detailed design; record as TBD or assumptions.

**Step 8A — Owner Operational Review** [Lensing: D-003]

8A.1 Conduct a formal operational review with the Fire Department representative (Owner) before proposal submission. This review shall include:
- Walkthrough of proposed apparatus bay layouts (floor plan review)
- Confirmation that bay dimensions accommodate Owner's actual apparatus fleet (Type 1 engines, aerial apparatus dimensions)
- Validation of decontamination workflow (apparatus → decon → gear locker → shared spaces)
- Review of gear locker room layout for adequate circulation space for simultaneous donning
- Confirmation of services placement (electrical, compressed air, exhaust) from operational perspective

8A.2 Document sign-off or feedback from Fire Department representative. Any operational concerns should be resolved or recorded as TBD for resolution during detailed design.

8A.3 Record outcome: Fire Department approval, conditional approval with noted actions, or TBD items requiring follow-up.

---

### Phase B: Detailed Design (Post-Award)

**Step 9 — Elaboration at Design Development**

9.1 Confirm Owner's apparatus fleet dimensions (actual Type 1 engine and aerial apparatus in service) and adjust bay dimensions if required.

9.2 Develop room data sheets for all firehall support rooms.

9.3 Advance exhaust mitigation system from concept to design drawings (DEL-02-05 coordination).

9.4 Advance electrical bay layout to receptacle plan (DEL-02-06 coordination).

9.5 Resolve secondary door-opening mechanism type (generator circuit vs. manual release) with DEL-02-07.

**Step 10 — 60% and 100% Design Submissions**

10.1 Incorporate AHJ feedback from permit application into layouts.

10.2 Conduct a formal internal code-compliance review before AHJ permit submission. This review shall use a checklist (to be developed during detailed design) confirming:
- **ABC occupancy classification:** Firehall wing occupancy classification identified per ABC Table A-3 (likely Group F2 — fire station, or equivalent).
- **Occupant load:** Calculated per occupancy type and design criteria (e.g., 40 current personnel + future 50 max).
- **Egress paths:** All egress routes from apparatus bays and support spaces verified against ABC travel distance limits (location TBD — obtain full ABC text for exact limits).
- **Bay-specific pedestrian egress:** Personnel doors with marked egress paths confirmed from apparatus work areas; travel distance from inside bay to exit < ABC limit.
- **Accessibility requirements:** Per ABC Table A-5, identified which firehall support spaces require barrier-free access (e.g., office areas, shared facilities) and which may be exempt (apparatus bays for firefighter operational use).
- **Ventilation:** All rooms verified for adequate ventilation per ABC and hazard-specific requirements (e.g., diesel exhaust, gear storage climate control).
[Lensing: X-005]

10.3 Verify all 40 bunker gear lockers fit in the as-designed room with adequate circulation.

10.4 Confirm SCBA room is designed for expected compressor dimensions and electrical load (coordinate with equipment supplier after FF&E procurement decision).

10.5 Define and document construction hold/witness points for critical milestones. Develop an inspection checklist including: (a) sump installation verification before slab pour (type, capacity, connection to drainage), (b) exhaust connection rough-in inspection before ceiling closure (routing, connection type, capping), (c) electrical and compressed air embedded services verification before slab/ceiling concealment (conduit routing, box locations, future connection accessibility). [Lensing: X-003]

**Step 11 — IFC Package**

11.1 Issue construction drawings with:
- Apparatus bay floor plans and sections (showing sump locations, service drops, door dimensions)
- Decon and support space floor plans
- Coordination drawings for exhaust, electrical, and plumbing interfaces
- Door schedule (16'×16' OH doors, secondary mechanisms)
- Room finish schedule (concrete floors, sealed)

---

## Verification

| Check | Method | Acceptance Criterion |
|---|---|---|
| Four drive-through bays confirmed | Review floor plan | 4 bays shown; drive-through configuration (front + rear doors) on each |
| Bay area within target range | Area calculation from drawings | Each bay 2,000–2,200 sf (Addendum 03 §1.21); deviation to be noted and justified |
| Bay door clear height ≥ 16 ft | Section drawing review | 16 ft minimum confirmed in section |
| Bay services per bay | Checklist against drawings | Electrical, compressed air, 2× exhaust drops, sump shown per bay |
| Exhaust coordination completed | Coordination drawing or note | DEL-02-05 confirms system capacity for 2 apparatus per bay per bay |
| Decon area completeness | Room data sheet review | All sub-components per REQ-0202-08 shown |
| 40 bunker gear lockers fit | Locker layout plan | 40 lockers with circulation aisle confirmed |
| Locker room ventilation shown | HVAC coordination | Room ventilation indicated on drawings or HVAC schedules |
| SCBA/cascade room sized | Floor plan | 150–200 sf room confirmed |
| FF&E exclusions documented | Specification notes | SCBA equipment, compressor equipment noted as FF&E excluded from base |
| Display system location confirmed | Plan drawing | Bay 1 (nearest office) wall-mount location shown |
| Water fill station shown | Plumbing plan | One 2-inch minimum fill station in fire apparatus bay area |
| Secondary door mechanism noted | Door schedule or spec note | Mechanism type confirmed (generator circuit or manual release) |
| Owner/Fire Dept. operational review | Layout walkthrough review with Fire Department representative | Fire Department sign-off on apparatus bay layouts, gear room layouts, and operational workflow before proposal submission. [Lensing: D-003] |
| Internal code-compliance review | Internal ABC compliance checklist review before AHJ permit submission | All ABC requirements (occupancy classification, egress paths, travel distances, accessibility) verified internally before AHJ submission. Checklist — TBD; develop during detailed design. [Lensing: X-005] |
| ABC compliance confirmed | AHJ review; permit issuance | Building permit issued without outstanding firehall-wing objections |

---

## Records

The following records shall be produced and retained:

| Record | When Produced | Retention |
|---|---|---|
| Apparatus bay layout drawings (proposal stage) | Proposal submission | RFP response package |
| Decon/gear locker layout drawings (proposal stage) | Proposal submission | RFP response package |
| Bay services concept narrative | Proposal submission | RFP response package |
| Bay exhaust mitigation coordination note | Proposal submission | RFP response package; transition to DEL-02-05 coordination file |
| Apparatus bay display concept | Proposal submission | RFP response package |
| Room data sheets (all firehall support rooms) | Design Development | Design submission package |
| Coordination matrices (DEL-02-04, -05, -06, -07) | Design Development | Design coordination file |
| 60% and 100% design drawings | Per RFP §7.1.8 milestones | Design submission packages |
| IFC construction drawings | IFC milestone | Construction documents |
| AHJ permit application and approvals | Permitting phase | Project regulatory file |
| As-built drawings (firehall wing) | Post-construction | Closeout package (DEL-01-07) |
