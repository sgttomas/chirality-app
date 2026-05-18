# Guidance — DEL-006-02: Water Distribution Plans

**Deliverable ID:** DEL-006-02
**Document Type:** Guidance (directional)
**Revision:** R1 — 2026-02-26 (Pass 3 enrichment)
**Status:** SEMANTIC_READY

---

## Purpose

DEL-006-02 (Water Distribution Plans) exists to translate the conceptual plumbing layout (Appendix B — Plumbing) and the RFP's water system requirements into a fully coordinated, P.Eng.-stamped drawing set that construction trades can use to install the water distribution network within the New North Shop Addition.

This deliverable supports three objectives:
- **OBJ-001:** Deliver a code-compliant, fully functional shop addition (the water supply system is a core operational requirement for the landfill maintenance shop).
- **OBJ-003:** Produce complete, P.Eng.-stamped IFC design documentation across all disciplines — this drawing set is the plumbing discipline's primary distribution drawing.
- **OBJ-004:** Install and commission all mechanical, plumbing, and water storage systems to operational readiness — this drawing set is the design authority for the water supply distribution scope.

The drawing set is a design deliverable, not a construction deliverable. Its downstream use is by the installation trades (PKG-014 — Plumbing & Water Systems Installation) and by the Safety Code Officer conducting inspections.

### Drawing Set Quality Objectives [D-003]

To translate OBJ-001, OBJ-003, and OBJ-004 into actionable quality targets for the Plumbing Engineer, the following drawing-set-specific quality objectives are proposed:

| Quality Objective | Target | Linked Objective | Notes |
|---|---|---|---|
| Coordination review cycles | TBD — target maximum number of coordination review cycles before IFC (ASSUMPTION: 2 cycles typical for design-build of this scale) | OBJ-003 | Fewer cycles indicate better preliminary coordination quality |
| Unresolved RFIs at IFC | TBD — target zero unresolved RFIs affecting plumbing distribution at IFC issue | OBJ-003 | Unresolved RFIs at IFC risk construction delays |
| SOW traceability | 100% — all SOW items traceable to drawing sheet content | OBJ-003 | See Specification.md — SOW-to-Drawing Traceability matrix |
| Constructability review | TBD — confirm whether constructability review with installation trades (PKG-014) is required before IFC | OBJ-004 | ASSUMPTION: beneficial for cistern-fed system with non-standard pressure source |
| Code review completion | All applicable code provisions verified before P.Eng. stamp | OBJ-001 | Per Procedure Step 8 |

**Note:** These quality objectives are proposals based on project context. The Project Manager and Plumbing Engineer should confirm, adjust, or supplement these targets during design development.

---

## Principles

### 1. Cistern-First Design Mindset

The project has no municipal water connection. All service water is supplied from the 50,000 L cistern (RFP §3.4). The distribution design must be conceived as a closed system with a single source of supply. This has implications for:
- System pressure (pump-dependent, not mains-dependent)
- Water quality/treatment considerations (if applicable — TBD by Plumbing Engineer)
- Freeze protection for any exposed piping (Alberta climate; ASSUMPTION: relevant)
- Filling cycle management (cistern refill vs. demand)

The distribution drawings must reflect this closed-system reality, including showing the interface point between the cistern/pump subsystem (DEL-006-04) and the distribution network.

### 2. Conceptual Layout as the Design Anchor

Appendix B (Plumbing) provides the County's spatial intent for fixture and drain locations. The plumbing drawings must honor those locations or flag deviations for County review. Key locations from the conceptual drawing:
- Emergency shower: south end of shop, near utility/parts transition
- Water tap & pressure washer reel: south wall, near roll door
- Water tap: near washroom/utility area
- Wash station: central-south, adjacent to parts room
- Washroom: utility room area

The Plumbing Engineer has design latitude on routing, pipe sizing, and material selection, but fixture locations are the County's operational intent and should not move without County concurrence.

### 3. Separation of Deliverables

PKG-006 is structured as multiple discrete drawing deliverables. DEL-006-02 is specifically the water supply distribution. The Plumbing Engineer should take care not to replicate content that belongs in sibling deliverables:
- DEL-006-03 covers drains and vents
- DEL-006-04 covers the cistern vessel and pump details
- DEL-006-05 covers the septic system

Cross-referencing (rather than duplicating) interface points will keep the set coherent.

### 4. Coordination Is a Core Deliverable Attribute

This is a design-build project (RFP §1.0, §3.4) with full interdisciplinary coordination required before IFC issue (OBJ-003). The water distribution drawings must be coordinated with structural (slab penetrations, sleeve locations), mechanical (utility room layout), electrical (pump power, heat tracing if used), and architectural (room layouts, ceiling heights). Unresolved coordination issues at IFC stage are a project risk; identify them early in design development.

---

## Considerations

### Alberta Climate — Freeze Protection

The project is located near Ferintosh, Alberta, in a cold-climate region. Any water supply piping in unheated areas, exterior walls, or locations exposed to freezing temperatures must include appropriate freeze protection measures. ASSUMPTION: this applies to at least some piping runs given the building type (large shop with overhead doors, exterior connections for bulk fill). Freeze protection strategy (insulation, heat tracing, drain-down provisions) to be determined by the Plumbing Engineer and shown on the drawings or referenced to the specification.

**Note:** Freeze protection is now formalized as REQ-012 in Specification.md [F-001]. Freeze protection design parameters are recorded in Datasheet.md — Freeze Protection Parameters [B-002]. Procedure.md includes a dedicated freeze protection design step [C-004].

### Emergency Shower Compliance

Emergency showers in industrial settings are subject to specific flow rate and water temperature (tepid water) requirements. ASSUMPTION: ANSI Z358.1 or an equivalent Alberta-applicable standard governs. The supply line sizing and any tempering valve requirements must be addressed in the drawing set or specification (DEL-006-08). This is a worker safety item.

**Note:** Specification.md REQ-002 now includes quantified acceptance criteria (temperature range, flow rate, duration) pending confirmation of the applicable standard [C-001, C-002].

### Bulk Water Fill — External Interface

The bulk water fill system (RFP §3.4, SOW-0044) serves an external filling function (filling trucks or equipment externally from the cistern). The piping interface between the bulk fill connection and the cistern/pump system is a boundary between DEL-006-02 and DEL-006-04. Clear demarcation of scope between these two drawing sets should be established early to avoid gaps or duplications.

**Note:** See CF-002 in the Conflict Table below. Specification.md REQ-006 notes [D-001] document this unresolved scope boundary.

### Pressure Washer Supply

The pressure washer reel supply (SOW-0049) represents a high-flow demand point. The Plumbing Engineer should assess whether the service water distribution pipe sizing is adequate to serve simultaneous loads (multiple taps, pressure washer reel, emergency shower) at minimum acceptable pressure, referencing the hydraulic calculations in DEL-006-07.

### Washroom and Laundry Expansion

The RFP (§3.4) requires expansion of washroom facilities to include a urinal and locker/change room with laundry services. Hot water supply (ASSUMPTION: required) for laundry and washroom introduces a water heating requirement that is not explicitly called out in the RFP. The Plumbing Engineer should confirm hot water system scope and include supply connections in this drawing set.

**Note:** See CF-001 in the Conflict Table below. This is the most consequential unresolved scope question for DEL-006-02 [A-001].

### Drawing Numbering and Sheet Organization

A drawing numbering convention aligned with the project's overall drawing set convention (TBD — to be established in preliminary design) will be required. ASSUMPTION: a "P" prefix designation (e.g., P-100 series) is typical for plumbing plans in Alberta design-build projects. Confirm convention with the project team.

**Note [D-002]:** The drawing numbering convention is currently an unresolved assumption in both this document and Procedure.md Step 2. Actionable preparation steering requires a settled convention before drawing production begins. The Project Manager should confirm the project-wide drawing numbering convention.

### Requirements Review Cadence [X-006]

Specification.md requirements should be reviewed and updated at defined milestones during design development to ensure they remain current as the design evolves. The following review points are recommended:

| Review Point | Trigger | Focus |
|---|---|---|
| Post-preliminary design approval | DEL-006-01 approved by County | Confirm scope boundaries (CF-001, CF-002 resolutions), update TBD requirements with preliminary design decisions |
| Post-hydraulic calculations | DEL-006-07 complete | Confirm pipe sizing, flow rates, pressure parameters; populate Datasheet.md fixture flow rates |
| Pre-IFC internal review | Prior to Step 7 coordination review | Verify all requirements are addressed in drawing set; complete SOW traceability matrix |
| Post-coordination review | Step 7 complete | Incorporate coordination-driven requirement changes; resolve any new conflicts |

**Note:** This cadence ensures that requirements remain current through the preliminary-to-IFC design evolution. The Plumbing Engineer and Project Manager should confirm or adjust these review points.

---

## Trade-offs

| Trade-off | Option A | Option B | Consideration | Proposed Authority |
|---|---|---|---|---|
| Pipe material for service water | CPVC (cost-effective, widely used) | Copper (more durable, premium) | Cost vs. durability; cistern-fed system does not have municipal water chemistry — may affect material selection | Plumbing Engineer judgment, confirmed in DEL-006-08 |
| Hot water system type | Central storage tank heater | Point-of-use tankless heaters | Central system is simpler to maintain; point-of-use avoids long hot water runs | Plumbing Engineer recommendation to County |
| Freeze protection approach | Insulation only (passive) | Insulation + heat tracing (active) | Alberta climate; active system adds electrical load (coord. with PKG-004) | Plumbing Engineer judgment based on routing |
| Bulk fill interface | Shown in DEL-006-02 | Shown in DEL-006-04 | Clear split avoids duplication; either approach is valid if cross-referenced | PKG-006 Plumbing Engineer to decide at preliminary design stage |

---

## Examples

No design examples are available in the source documents. The Appendix B (Plumbing) conceptual drawing (R-06) provides the spatial reference for fixture locations and plumbing areas. Refer to that drawing as the baseline for layout intent.

For system parameters, the RFP §3.4 provides the only explicitly cited values:
- 50,000 L cistern (minimum)
- 100 LPM pump (minimum)
- 2.5 inch filling connection
- 2,000 US Gallon (~7,571 L) septic tank

All other design parameters (pipe sizes, materials, pressure setpoints, flow rates per fixture) are to be established by the Plumbing Engineer through design calculation and confirmed in DEL-006-07 and DEL-006-08.

**[E-001] Note:** The absence of comparable design examples is acknowledged. The Plumbing Engineer should identify whether comparable cistern-fed industrial shop plumbing designs or standard plumbing plan exemplars are available from their practice library or industry references during design development. If identified, reference them here to provide data-level evidence for design guidance.

---

## Conflict Table (for human ruling)

The following conflicts and ambiguities have been identified. Items from Pass 1+2 are retained; items surfaced by Pass 3 semantic lensing are noted with their item IDs.

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CF-001 | Hot water provision: RFP §3.4 specifies cistern, pump, and septic but does not explicitly require a water heater. However, washroom expansion (urinal + locker/change room + laundry — RFP §3.4) implies hot water need. **[A-001]** Prescriptive direction for the distribution network cannot be finalized without knowing if hot water piping is in scope of DEL-006-02 or a separate deliverable. | RFP §3.4 (no explicit water heater requirement) | RFP §3.4 (washroom + laundry expansion scope implies hot water) | Specification.md REQ-004, REQ-005; Datasheet.md Construction section | Plumbing Engineer / County to confirm scope; include in DEL-006-01 preliminary design | TBD |
| CF-002 | Scope boundary for bulk water fill piping: unclear whether distribution piping to the bulk fill connection point is part of DEL-006-02 (distribution) or DEL-006-04 (cistern/pump details). **[D-001]** Definitive directive authority for the drawing set requires an unambiguous scope boundary. REQ-006 currently uses "shall show, or reference by cross-drawing" to accommodate either split. | _CONTEXT.md — DEL-006-02 scope includes "supply lines, pressurization systems" | Decomp. — DEL-006-04 explicitly covers "Cistern & Pump Details" | Specification.md REQ-006; Datasheet.md Drawing Sheet scope | Plumbing Engineer to define interface at preliminary design stage; confirm in DEL-006-01 | TBD |
