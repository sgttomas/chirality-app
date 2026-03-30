# Guidance — DEL-004-03 Power Distribution Plans

---

## Purpose

DEL-004-03 Power Distribution Plans exists to translate the project's three-phase power distribution system from a system-level concept (Single-Line Diagram, DEL-004-02) into a floor-plan-level construction document. This drawing set is the primary reference that the electrical installation subcontractor (PKG-015) will use to route conduit, size conductors, locate panels, and connect all power loads throughout the New North Shop addition.

The drawing set enables:
- Construction sequencing of electrical rough-in within the building structure
- Coordination between electrical, mechanical, and structural trades during construction
- Alberta Safety Code inspection at rough-in and final stages
- Owner (Camrose County) visibility into power infrastructure before construction commences

This deliverable sits within a family of electrical design documents (DEL-004-01 through DEL-004-09) and must be read in conjunction with DEL-004-02 (Single-Line Diagram), DEL-004-05 (Receptacle Layout Plans), and DEL-004-06 (Panel Schedules) for a complete picture.

---

## Principles

### Principle 1 — Three-Phase Distribution is Foundational
The RFP explicitly requires the building to run on three-phase power (RFP §3.4). This is the governing constraint for the entire electrical system design. All panelboard selection, feeder sizing, and equipment circuit design must be premised on three-phase service. The power distribution plans must clearly show the three-phase service entry point and confirm three-phase distribution to all panels and three-phase loads.

### Principle 2 — Heavy Industrial Loads Drive the Design
The shop is designed for heavy equipment maintenance. The load profile is dominated by high-current industrial loads: two 5-tonne overhead cranes, welding-grade receptacles (50A/240V per ASSUMPTION D-009), a 70A fire hose pump, a 70A pressure washer, and a 40A compressor. The power distribution plan must size feeders and panels to accommodate these loads simultaneously, with appropriate demand factors per the applicable electrical code. The lighting and small-receptacle loads are secondary by comparison.

### Principle 3 — Conceptual Drawing is a Minimum, Not a Ceiling
Appendix B (Electrical) is a conceptual drawing. It establishes the minimum scope: load types, quantities, and approximate locations. The electrical engineer must treat it as a starting point and determine whether any loads are missing, whether circuit groupings are optimal, and whether code requirements mandate additional provisions (e.g., GFCI, dedicated circuits, arc-fault protection). The IFC drawing set must be complete and code-compliant; it need not be constrained to the exact layout shown in the conceptual drawing if engineering judgment indicates adjustments are required.

### Principle 4 — MEP Coordination is Non-Negotiable
Several loads on the power distribution plan originate with other disciplines: the makeup air unit, heating system, and air exchanger are mechanical loads that require electrical feeds. The electrical engineer must coordinate with the mechanical engineer (PKG-003) to confirm motor ratings, starter/VFD requirements, and connection points before the IFC drawing set is finalized. Similarly, plumbing equipment (cistern pump, wash bay pump) may require electrical feeds — coordinate with PKG-006.

### Principle 5 — Preliminary Approval Gates IFC Release
The County must approve the preliminary electrical design (DEL-004-01) before IFC drawings are issued (RFP §3.3.2, SOW-0010d). The power distribution plans, as part of the IFC set, must not be issued for construction without that approval. This gate exists to prevent rework caused by Owner-directed scope changes after construction has begun.

---

## Considerations

### Drawing Organization
ASSUMPTION: For a building of this size and load complexity, a minimum of the following plan sheets is expected in the power distribution drawing set:
- Electrical site plan (service entry, site conduit routing)
- Main shop power plan (crane rails, welding circuits, heavy receptacles, equipment circuits)
- Ancillary area power plan (wash bay, parts room, utility room, office)
- Electrical notes and legend sheet
- Cross-reference sheet to panel schedules (DEL-004-06)

The exact sheet count and organization is at the electrical engineer's discretion and must reflect code requirements and construction usability.

### Panelboard Location
The conceptual drawing (App B — Electrical) does not explicitly identify panelboard locations. The electrical engineer must select panelboard locations that: (a) minimize feeder lengths to high-current loads (cranes, welding stations), (b) are accessible for maintenance, (c) comply with clearance requirements under the applicable electrical code, and (d) are coordinated with the structural engineer for wall/column penetrations. Panel location is TBD pending detail design.

### Crane Circuit Considerations
Overhead crane circuits are subject to specific code provisions (ASSUMPTION: CEC Section 40 or equivalent Alberta adoption governs crane and hoist wiring; location TBD in source). Crane power supply typically requires a dedicated disconnect per crane, conductor sizing based on the actual crane duty cycle, and coordination with the crane manufacturer's requirements. The electrical engineer must obtain crane specifications (from the crane supplier, coordinated through PKG-016) before finalizing crane circuit design.

### Welding Receptacle Distribution
RFP §3.4 specifies "multiple electrical plugs throughout the shop area suitable for connecting high voltage welding equipment." The conceptual drawing (App B — Electrical) shows 50A receptacle symbols at the welding station and at multiple locations in the main shop and on the work bench wall. Decomposition Decision D-009 assumes 50A/240V; this is an **ASSUMPTION** that must be confirmed against the County's welding equipment specifications before IFC issue, as the County is responsible for supplying welding equipment specifications (RFP §3.4, SOW-0204).

### Service Entry and Utility Coordination
The electrical service tie-in is a Proponent responsibility (Decomposition SOW-0081). The power distribution plans should show the service entry point and the transition from the utility service to the building's main disconnect/panel. The electrical engineer must coordinate with the local utility to confirm: available service voltage and capacity, metering requirements, and service entrance requirements. Service voltage (120/208V or 347/600V three-phase) is TBD pending utility coordination.

### Load Calculation and Panel Sizing
ASSUMPTION: The electrical engineer will perform a load calculation per the applicable electrical code to size the main service, feeders, and panelboards. The calculation must account for: crane demand factors, welding receptacle demand factors, motor loads (fans, pumps), heating loads, and lighting loads. The load calculation is a deliverable under DEL-004-08 (Electrical Calculation Package), not this drawing set; however, the panel and conductor sizes shown on the power distribution plans must be consistent with that calculation.

### Conduit Material and Conductor Sizing Conventions (Enrichment: A-004)

The power distribution plans should establish and clearly show the conduit material specification and minimum conductor sizing conventions used throughout the building. The Guidance Trade-offs section mentions rigid steel conduit for above-slab power conduit routing but does not establish it as a default convention for the plans. The Electrical Engineer should:
- Specify the default conduit type for power circuits (e.g., rigid steel conduit, EMT, PVC) and any location-specific exceptions (Enrichment: A-004)
- Indicate minimum conductor sizing conventions consistent with the applicable electrical code and load requirements
- Document conduit type selection rationale (environment, load type, cost) in the drawing general notes or electrical specification (DEL-004-09)
- Source: Guidance Trade-offs (conduit routing above vs. below slab); **ASSUMPTION**: rigid steel conduit is the likely default for an industrial maintenance shop environment; Electrical Engineer to confirm

### Code Interpretation Notes (Enrichment: D-001)

**ASSUMPTION:** The following code interpretation notes are provided as directional guidance for key CEC provisions that drive design decisions on this project. The Electrical Engineer is the authority for final code interpretation. Specific code section references are **TBD** (location TBD in source text).

- **Demand factors for welding receptacles:** CEC provisions governing demand factors for welding equipment affect the sizing of feeders and panels serving welding receptacle circuits. The Electrical Engineer must determine the applicable demand factor based on the number and rating of welding receptacles and the expected duty cycle. (Source: ASSUMPTION — CEC Part I, applicable section TBD)
- **Crane wiring rules:** CEC Section 40 (or Alberta-adopted equivalent) governs crane and hoist wiring, including disconnect requirements, conductor sizing for crane duty cycles, and pendant/festoon wiring provisions. The Electrical Engineer must apply these rules when designing crane circuits per REQ-003-02. (Source: ASSUMPTION — CEC Section 40; location TBD)
- **GFCI/AFCI applicability:** See subsection below. The Electrical Engineer must assess which receptacle locations require GFCI and/or AFCI protection under the applicable code edition. (Source: ASSUMPTION — CEC Part I, applicable section TBD)
- **Grounding and bonding:** CEC provisions for grounding electrode systems and equipment bonding apply to the entire electrical installation. The power distribution plans must show these elements per REQ-003-17. (Source: ASSUMPTION — CEC Part I, applicable section TBD; Enrichment: F-003)

### Code Compliance — GFCI and AFCI
ASSUMPTION: Alberta Safety Code adoption of CEC Part I may require GFCI protection for receptacles in wet or damp locations (wash bay, washroom) and may require AFCI protection in office/sleeping areas. The electrical engineer must assess and apply applicable requirements. These provisions should be noted on the power plans or specifications.

### Future Expansion
The RFP does not explicitly address provisions for future electrical expansion. If the electrical engineer recommends spare breaker positions or capacity, this should be flagged to the Owner through the preliminary design process. ASSUMPTION: No explicit future expansion requirement exists in sources; do not add expansion provisions without Owner direction.

**Rationale clarification (Enrichment: D-003):** The statement "do not add expansion provisions without Owner direction" is intended to prevent scope creep, not to discourage professional recommendation. Under the design-build duty of care (CCDC 14-2013), the Electrical Engineer may be expected to proactively advise the Owner on the benefits and costs of spare capacity during the preliminary design phase (DEL-004-01). The Electrical Engineer should:
- Identify whether spare panel capacity or conduit provisions would provide value given the building's industrial use and potential for equipment changes
- Present the recommendation to the Owner as part of the preliminary design submission (Step 5)
- Document the Owner's decision (accept/reject spare capacity) for the record
- **TBD:** Confirm whether proactive recommendation of spare capacity is expected as part of the design-build scope or is a change order item (Source: CCDC 14-2013 scope of services; not in accessible sources)

### Inspection Report Content and Deficiency Tracking (Enrichment: E-004)

The Procedure Records table lists "Inspection reports (rough-in, final)" as a required record, but neither Procedure nor Guidance previously specified what the report must contain or how inspection deficiencies feed back into the drawing set. The following guidance is provided:

- **Inspection report minimum content (ASSUMPTION — standard Alberta Safety Codes practice):**
  - Date of inspection
  - Inspector identification (Safety Codes Officer name/number)
  - Scope of inspection (rough-in vs. final)
  - Items inspected (by reference to drawing sheets/areas)
  - Pass/fail determination per item
  - Deficiency descriptions (if any), with reference to code section violated
  - Required corrective actions and re-inspection requirements

- **Deficiency tracking:**
  - Inspection deficiencies shall be logged by the Electrical Contractor and communicated to the Electrical Engineer of Record
  - If a deficiency indicates a design error (as opposed to installation error), the Electrical Engineer must issue a revised drawing or clarification
  - Corrective actions shall be tracked to closure before requesting re-inspection
  - Source: ASSUMPTION — standard Safety Codes inspection practice; specific Alberta requirements **TBD** (location TBD in Safety Codes Act/regulations)

### Risks and Contingencies (Enrichment: E-002)

The following key risks may affect the power distribution plan IFC timeline. The Electrical Engineer and Project Manager should monitor these and develop contingency plans:

| Risk | Impact | Recommended Mitigation |
|---|---|---|
| Delayed utility coordination — service voltage not confirmed | All panelboard and wiring specifications are TBD; cannot finalize power plans | Initiate utility coordination early in preliminary design phase; escalate through Project Manager if response delayed beyond 2 weeks of initial request (ASSUMPTION: 2-week target) |
| Late crane specifications from supplier (PKG-016) | Crane circuit sizing (REQ-003-02) cannot be finalized; may require placeholder circuits on drawings | Track crane spec receipt as a gated prerequisite (see Procedure enrichment D-002); if specs not received by drawing production start, size circuits conservatively and note on drawings as "subject to confirmation" |
| County-directed scope changes after preliminary design | Rework on power distribution plans if scope changes are substantial | Ensure preliminary design submission (Step 5) captures all County requirements; document County approval clearly (see REQ-003-14 acceptance criteria, Enrichment X-001) |
| Welding equipment specifications not provided by County | Welding receptacle rating remains ASSUMPTION (50A/240V per D-009); may require circuit and panel resizing if actual equipment differs | Request welding equipment specs from County concurrently with preliminary design submission; note ASSUMPTION on drawings until confirmed (Source: RFP §3.4, SOW-0204) |
| Missing fire alarm / emergency power scope determination | If fire alarm or emergency power is within scope and discovered late, significant rework may be required | Resolve REQ-003-18 (fire alarm/emergency power scope TBD) during preliminary design phase before committing panel and feeder sizing (Enrichment: F-005) |

> Note: These risks are ASSUMPTION-level assessments based on the project context and common design-build practice. The Project Manager should maintain the authoritative project risk register.

---

## Trade-offs

| Trade-off | Description | Recommended Approach |
|---|---|---|
| 120/208V vs. 347/600V service | Higher-voltage service (347/600V) reduces conductor sizes for large loads but may limit availability of 120V convenience receptacles without transformers | TBD pending utility coordination; engineer to recommend based on utility availability and load mix |
| Centralized vs. distributed panelboards | A single large panel minimizes panel count but increases feeder lengths to distant loads; distributed panels reduce feeder lengths but add panel cost | ASSUMPTION: Given building size (130' × 100') and load distribution, at least two sub-panels (one for crane/heavy loads, one for general) is likely optimal; engineer to confirm |
| Welding receptacle quantity | More receptacles provide operational flexibility; fewer reduce panel space and circuit cost | RFP requires "multiple" — ASSUMPTION: minimum of one per work area shown on App B; engineer to confirm with Owner at preliminary design |
| Conduit routing above vs. below slab | Above-slab conduit is accessible for future changes but exposed to damage; below-slab conduit is protected but difficult to modify | ASSUMPTION: Given heavy equipment operations on floor, above-slab power conduit to be protected in rigid steel conduit or surface raceway; below-slab for service pit and structural penetrations only. Engineer to confirm |

---

## Examples

Examples of power distribution plan content consistent with source materials:

- App B (Electrical) conceptual drawing shows the relative locations of: welding station (north wall, top of plan), work benches (north wall), 5-tonne crane positions (mid-building, north-south orientation), Service Pit (east zone), wash bay (east, 24' wide), parts room, utility room (center-south), and office (west-center). The power distribution IFC drawing will use this spatial arrangement as a baseline for circuit routing. (Source: App B Electrical, conceptual layout)

- App B (Electrical) legend identifies the following symbols in use: L (Lights), E (Exhaust Fan), 15 (15A/120V), 20 (20A/120V or 20A/240V — differentiated by fill/line style), 30 (30A/240V), 50 (50A/240V). The IFC drawing set must use a consistent, code-compliant legend. (Source: App B Electrical, legend)

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-003-01 | The App B (Electrical) legend shows "20 Amp 120V" and "20 Amp 240V" as separate legend entries with different symbols, but the floor plan layout uses the numeral "20" for both without consistent differentiation visible at this resolution. It is unclear from the conceptual drawing which 20A receptacles are 120V vs. 240V at each specific location. | App B (Electrical) — legend | App B (Electrical) — floor plan layout | REQ-003-08, DEL-004-05 Receptacle Layout Plans | Engineer to resolve at detail design by reviewing layout intent with Owner; interim ASSUMPTION: locations near work benches are 20A/240V; locations in office/ancillary areas are 20A/120V | TBD |
| CONF-003-02 | Service voltage is not specified in the RFP or Appendix B beyond "three-phase power." The power distribution plan cannot be completed without knowing whether the service is 120/208V three-phase or 347/600V three-phase, as this affects all panelboard and wiring specifications. | RFP §3.4 ("three-phase power") | No further source specification | REQ-003-01, all circuit requirements | Electrical engineer to confirm service voltage with utility (ATCO Electric or local utility) during preliminary design | TBD |
| CONF-003-03 | The App B (Electrical) notes list "6 Ceiling Fans for Main Shop" but the floor plan does not clearly show ceiling fan symbols distinct from high bay light symbols at this resolution. Fan locations are therefore uncertain. | App B (Electrical) — notes | App B (Electrical) — floor plan | REQ-003-11 | Engineer to assign ceiling fan locations based on shop layout optimization; confirm with Owner at preliminary design | TBD |
