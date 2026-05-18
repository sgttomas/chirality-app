# Guidance — DEL-011-06 Service Pit/Trench

---

## Terminology Note

> Throughout this deliverable's document set, **"service pit"** is used as the primary term. **"Service trench"** appears in some sources (notably the Appendix B floor plan) and is treated as a synonym. If the project team determines these terms refer to distinct geometries (e.g., a pit is enclosed on all sides while a trench is open-ended), the canonical term should be established and the alias documented. Until clarified, both terms refer to the same below-grade feature. *(Per Lensing Item B-003 — Normalization: inconsistent terminology across documents.)*

---

## Purpose

The service pit/trench exists to enable mechanics to perform under-equipment servicing on large, heavy landfill maintenance equipment (such as motor scrapers and tracked/packer units) without requiring the equipment to be raised on hoists. A below-grade pit allows mechanics to stand and work comfortably beneath the equipment's undercarriage at grade level, which is practical for the scale of equipment operated at the West Dried Meat Lake Regional Landfill.

This is a permanent, structural feature of the New North Shop addition. Its design and construction directly affect long-term worker safety, maintenance productivity, and building utility. Getting the structural construction right at this stage is critical because the pit cannot be easily modified post-construction.

**Source:** RFP §3.4; Decomposition SOW-0028; Decomposition Vocabulary Map ("Service Pit — below-grade pit/trench for under-equipment servicing").

---

## Principles

1. **Structural first.** The pit is a structural opening in the building slab. It must be built to the IFC structural drawings (DEL-002-06) without deviation. Any field changes require structural engineer approval.

2. **Safety is non-negotiable.** The pit is a fall hazard and a potential confined space. Edge protection and ventilation are not optional features — they are explicit RFP requirements and are subject to Alberta OHS Code.

3. **Coordinate early with MEP trades.** Ventilation rough-in (PKG-013) and lighting rough-in (PKG-015) must be coordinated before concrete placement. It is impractical to core-drill pit walls after construction for conduit or ductwork.

4. **Sequencing dependency on foundation.** Per _DEPENDENCIES.md, the pit excavation cannot begin until PKG-010 (Foundation Construction) is complete. Coordinate the construction schedule accordingly.

5. **Downstream coordination.** PKG-012 (Interior Construction & Fit-Out) will require equipment access via the pit for maintenance activities. The as-built condition of the pit (dimensions, access arrangement, cover type) should be documented for handover.

6. **Resolve design decisions before IFC drawings.** Several key design parameters (pit dimensions, access method, cover type, drainage scope) require Owner input or inter-discipline coordination before the structural engineer can finalize DEL-002-06. Early resolution prevents construction delays. *(Added per Lensing Items A-004, A-005 — multiple TBD items depend on upstream design decisions.)*

---

## Considerations

### Pit Dimensions and Equipment Compatibility
The conceptual drawing (Appendix B, R-04) shows the service trench in the main bay area of the New North Shop but does not provide explicit pit dimensions. The structural engineer will establish these in DEL-002-06. Key dimensional drivers are:

- **Depth:** Must allow a mechanic to stand upright beneath the undercarriage of the landfill's heavy equipment fleet. ASSUMPTION: working depth of approximately 1.5–1.8 m (5–6 ft) is typical for maintenance pits serving motor scrapers and similar equipment. This is an ASSUMPTION — the structural engineer must confirm based on equipment fleet specifications.
- **Width:** Must match bay width or be narrower for structural reasons. ASSUMPTION: width will be set to accommodate the track/wheel gauge of the equipment being serviced.
- **Length:** ASSUMPTION: sized to allow access to the full undercarriage of the longest equipment type. Exact length TBD.

The GC should request confirmed equipment dimensions from the Owner (Camrose County) early in design to inform the structural engineer's work on DEL-002-06. Without Owner-confirmed fleet dimensions (undercarriage clearance, wheel/track gauge, overall length), the structural engineer cannot finalize DEL-002-06 and all dimensional requirements remain TBD. This is the single most critical data dependency for this deliverable. *(Enriched per Lensing Item A-005 — TBD_Question: Owner fleet data not yet received.)*

### Ventilation — Safety Critical
Below-grade maintenance pits in heavy equipment shops accumulate exhaust gases, fuel vapors, and oil mist. Alberta OHS Code provisions for confined spaces (Part 5) and ventilation requirements for maintenance areas (Part 25) apply. The mechanical design (PKG-003) must address:
- Continuous forced ventilation while the pit is occupied
- Atmospheric testing requirements for confined space entry if applicable
- Exhaust discharge routing
- **Measurable performance criteria** — minimum air changes per hour or maximum contaminant levels per Alberta OHS Code Parts 5/25. The mechanical engineer (PKG-003) must define these thresholds so that Specification REQ-011-06-02 can be verified with an objective acceptance standard. *(Enriched per Lensing Item F-003.)*

ASSUMPTION: ventilation for the pit may be integrated with the shop's general ventilation (forced air makeup system noted on App B) or may require dedicated pit-level supply/exhaust. This must be resolved during mechanical design and coordinated with the GC before concrete placement.

### Lighting — Task Illumination
Pit lighting must provide adequate illumination for close mechanical inspection and servicing work. ASSUMPTION: pit-wall-mounted or overhead fixtures at pit level will be required. Electrical rough-in (conduit, junction boxes) must be embedded in pit walls during concrete construction. Coordinate with PKG-004 and PKG-015 before concrete placement.

**Measurable performance criteria** — minimum lux level for mechanical inspection/servicing tasks should be defined by the electrical engineer (PKG-004) with reference to an applicable illumination standard (e.g., IESNA). This enables verification of Specification REQ-011-06-03 against an objective threshold. *(Enriched per Lensing Item D-002.)*

### Floor Drainage
Heavy equipment maintenance produces oil, coolant, and wash-water runoff. ASSUMPTION: the pit floor will require floor drains connected to the building's drainage/sump system. This must be coordinated with PKG-006 (Plumbing Design) and PKG-014 (Plumbing & Water Systems Installation). Confirm drain rough-in requirements before concrete pour.

**Scope boundary note:** The scope boundary for pit floor drainage between this deliverable and PKG-006/PKG-014 is not explicitly defined in any source. Procedure treats drain rough-in as in-scope (Step 4.2, Step 8.4), but Specification did not previously address pit floor drainage. This is recorded in the Conflict Table as C-011-06-04. *(Enriched per Lensing Item E-002.)*

### Access and Egress
A safe means of entry and egress is required. Options include integrated concrete steps, removable steel stairs, or a ladder. ASSUMPTION: steps or stairs are preferable for a permanent facility. The access method affects pit end-wall structural detailing. Confirm with structural engineer during IFC drawing development.

**Decision path:** The access/egress method must be selected before the structural engineer can finalize end-wall detailing in DEL-002-06. Responsible parties: structural engineer and architect. The GC should raise this as a coordination item during preliminary design review. No decision deadline is currently assigned — this should be tracked. *(Enriched per Lensing Item A-004 — MissingSlot: decision path and responsible party were absent.)*

### Cover and Edge Protection
When equipment is positioned over the pit, the pit edges must be protected. When the pit is not in use, a cover or railing system prevents inadvertent falls. ASSUMPTION: a removable steel grating or cover system is typical for vehicle service pits. Safety railings may also be required at the perimeter when the pit is open and unoccupied. Coordinate cover/railing design with structural and architectural IFC drawings.

**Requirement clarity:** There is ambiguity across documents about whether a pit cover/grating system is required or conditional. Specification REQ-011-06-11 now establishes a requirement (ASSUMPTION) for a cover system. If the project team determines no cover is required, that decision and its rationale should be recorded. *(Enriched per Lensing Item E-001.)*

### Concrete Superstructure Interface
The pit is constructed as part of the building slab system. Interface details with DEL-011-01 (Concrete Superstructure) and the building foundation (PKG-010) must be resolved in the structural IFC drawings. The GC must not proceed with pit excavation or concrete work until DEL-002-06 is issued.

### Cold-Weather Concrete Protection *(added per Lensing Item D-001)*
Given the Alberta climate, concrete placements for this deliverable may occur during cold-weather conditions (ambient temperature below +5 degrees C). Cold-weather concrete protection is a standard Alberta construction concern.

**Rationale and normative basis:** CSA A23.1 (Concrete Materials and Methods of Concrete Construction) includes requirements for cold-weather concreting. ACI 306 (Guide for Cold Weather Concreting) provides additional guidance. Procedure Step 5.4 references ACI 306 as an ASSUMPTION.

**Decision framework:** The structural engineer and GC should determine:
- Whether the project concrete specification (via DEL-002-06 or the project quality plan) includes cold-weather concrete requirements.
- If not, whether CSA A23.1 cold-weather provisions apply by default under the Alberta Building Code.
- The threshold temperature below which cold-weather protection measures must be implemented.

This rationale supports Specification REQ-011-06-04 (structural integrity / concrete placement) and Procedure Step 5.4. *(Added per Lensing Item D-001 — RationaleGap: cold-weather protection referenced in Procedure as ASSUMPTION with no normative basis or rationale in Specification or Guidance.)*

### Underground Utility Locates *(added per Lensing Item F-002)*
Procedure Step 2.3 requires underground utility locates before excavation, currently marked as ASSUMPTION.

**Rationale and regulatory basis:** Underground utility locates before excavation are a standard requirement in Alberta construction. Alberta One-Call (Alberta Utilities Commission regulation) requires notification before ground disturbance. Alberta OHS Code Part 32 (Excavation) also requires identification of underground utilities before excavation commences. This is not discretionary — it is a regulatory requirement.

The ASSUMPTION label in Procedure Step 2.3 can be considered well-founded: utility locates are required. However, for this specific deliverable (pit excavation within the building footprint), the applicability depends on whether underground utilities exist within the excavation zone. The GC should confirm with the Owner and the plumbing/electrical design teams. *(Added per Lensing Item F-002 — RationaleGap: utility locate requirement had no supporting rationale or regulatory basis.)*

### As-Built Survey Rationale *(added per Lensing Item X-003)*
Specification Documentation item 5 requires as-built survey information, citing "ASSUMPTION: required per RFP section 3.3.2 'as-built survey'."

**Rationale:** RFP §3.3.2 includes a general reference to as-built documentation requirements. It is not confirmed whether this requirement applies specifically to the service pit or is a general project requirement. The project team should confirm:
- Whether RFP §3.3.2 mandates as-built dimensional surveys for individual construction features (like the pit), or only for the overall building.
- If as-built survey is confirmed as required for this deliverable, the required level of detail (dimensional tolerance, survey method) should be specified.

As-built dimensional verification is a critical oversight foundation for the completed pit — the pit cannot be inspected dimensionally after backfill/slab integration. *(Added per Lensing Item X-003 — RationaleGap: as-built survey requirement sourced from ASSUMPTION without confirmed RFP basis.)*

---

## Trade-offs

| Trade-off | Options | Consideration |
|---|---|---|
| Pit depth | Deeper = better working clearance; shallower = simpler construction and lower structural cost | Driven by equipment fleet; must satisfy mechanic ergonomics. TBD pending Owner equipment data and structural engineering. |
| Cover system | Removable steel grating (allows light/ventilation to pass through) vs. solid steel plate covers | Grating improves ventilation; solid plates provide a flat floor surface when pit not in use. Code requirements may govern. TBD. See also REQ-011-06-11. |
| Ventilation method | Dedicated pit-level forced ventilation vs. integration with general shop ventilation | Dedicated system is safer but more costly. Mechanical engineer to determine per OHS Code requirements. TBD. |
| Access/egress | Integrated concrete steps vs. removable steel stair vs. ladder | Steps are safer and more convenient; ladder is simpler but less accessible. Building code accessibility requirements may apply. Decision required before DEL-002-06 finalized. TBD. |
| Floor drain integration | Drain connected to wash bay sump system vs. separate pit drain | Coordination with PKG-006 and PKG-014 required. Scope boundary for drain rough-in TBD (see Conflict Table C-011-06-04). TBD. |
| Waterproofing extent | Full waterproofing membrane vs. damp-proofing coating vs. none (interior location) | Below-grade concrete in interior location — groundwater exposure depends on site conditions. Structural engineer to determine in DEL-002-06. See REQ-011-06-12. TBD. *(Added per Lensing Item C-002.)* |

---

## Examples

No directly comparable precedent projects are available in accessible sources. TBD — examples of similar heavy-equipment service pit designs may be identified during preliminary design phase.

---

## Conflict Table (for human ruling)

The following items require resolution. Items C-011-06-01 through C-011-06-03 are open design decisions flagged in the original Pass 1/2 drafting. Item C-011-06-04 was added during Pass 3 enrichment.

| Conflict ID | Topic | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| C-011-06-01 | Pit dimensions (depth, width, length) not specified in any accessible source | RFP §3.4 (functional requirement only) | App B (Shop) R-04 (conceptual only, no pit dimensions) | Datasheet Attributes; Specification REQ-011-06-09; Procedure Step 4 | Structural engineer to establish in DEL-002-06, informed by Owner equipment fleet data | TBD |
| C-011-06-02 | Ventilation: dedicated pit system vs. integration with general shop ventilation | RFP §3.4 (requires ventilation) | No mechanical design yet available | Specification REQ-011-06-02; Procedure Step 6 | Mechanical engineer to determine in PKG-003 design per OHS Code requirements | TBD |
| C-011-06-03 | Floor drainage: pit drain routing and connection point not specified | RFP (no specific pit drainage requirement stated) | Plumbing design (PKG-006) not yet available | Datasheet Attributes; Procedure Step 6 | Plumbing engineer to determine in PKG-006 design | TBD |
| C-011-06-04 | Floor drainage scope boundary: Specification scope is silent on whether pit floor drainage is in-scope or out-of-scope for this deliverable; Procedure Steps 4.2 and 8.4 treat drain rough-in and drain testing as in-scope; Guidance and Datasheet reference drainage as TBD | Specification "In Scope" / "Out of Scope" (silent on pit floor drainage) | Procedure Steps 4.2 and 8.4 (treat drain rough-in as in-scope construction work) | Specification Scope; Procedure Steps 4, 8; Datasheet Attributes (Drainage row) | Plumbing engineer via PKG-006 and project scope definition to clarify whether drain rough-in is within this deliverable or PKG-014 | TBD |

*(C-011-06-04 added per Lensing Item E-002 — Conflict: scope boundary for pit floor drainage not explicitly defined.)*
