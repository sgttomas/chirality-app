# Guidance — DEL-015-03 Receptacle Installation

---

## Purpose

This deliverable provides a permanently installed, code-compliant array of electrical receptacles throughout the New North Shop addition at the West Dried Meat Lake Regional Landfill Maintenance Shop. The receptacle network enables day-to-day operational flexibility for maintenance activities, including welding, power tool use, equipment servicing, and general workshop tasks.

The receptacle installation directly supports:
- OBJ-001: Deliver a code-compliant, fully functional maintenance shop addition that satisfies the County's operational program and passes all applicable inspections. [Source: Decomposition §5]
- OBJ-005: Install and commission all electrical and low-voltage systems to operational readiness, including receptacles per the electrical drawing. [Source: Decomposition §5]

---

## Principles

### 1. Operational Purpose Drives Layout

The electrical drawing (App B-Elec) reflects a working maintenance shop for heavy equipment servicing. The receptacle distribution is organized around workstation types:
- **Welding station (NE corner):** High-density concentration of heavy-duty and welding-grade receptacles (50A/240V, 30A/240V, 20A/240V) — the most demanding load zone.
- **Main shop perimeter and columns:** Distributed 20A/120V and 20A/240V receptacles supporting moveable equipment, power tools, and drop cords at any bay position.
- **Parts room, office, utility room:** 15A/120V circuits for lighter office and tool-storage use.
- **Wash bay:** Mixed 15A/120V and 20A/120V service with exhaust fan circuit.

Source: App B-Elec (conceptual layout and legend)

### 2. Welding Receptacle Rating Is an Assumption Pending County Confirmation

The RFP §3.4 states: "Multiple electrical plugs throughout the shop area suitable for connecting high voltage welding equipment (County to supply welding equipment specifications)." The welding equipment specifications were not provided in the RFP package. The project team assumed 50A/240V industrial-grade per the electrical drawing and Decomposition D-009. If the County's actual welder plug configuration differs (e.g., 60A, or a specific NEMA configuration), the design must be revised — this is a declared scope change trigger.

**Terminology Note [Ref: F-002]:** The RFP uses "high voltage welding equipment," the Specification uses "welding-grade receptacles," and the Datasheet uses "welding-grade high-voltage." For consistency across project documents, this document set uses the term **"welding-grade receptacles"** to refer to the 50A/240V receptacles intended for welding equipment. The term "high-voltage" in the RFP context refers to higher-voltage industrial equipment (240V), not high-voltage in the utility/transmission sense (which typically means above 1000V). The voltage class of all receptacles in this deliverable is "low-voltage" per electrical industry definitions.

Source: RFP §3.4; Decomposition D-009; SOW-0057; _SEMANTIC_LENSING.md F-002

### 3. Three-Phase Service Is Foundational

All receptacle circuits are downstream of the three-phase power service (DEL-015-01). The receptacle installation cannot be energized or commissioned until DEL-015-01 is complete and the main distribution is live. The panel schedules (DEL-004-06) will define which phase(s) serve each receptacle circuit.

Source: Decomposition DEL-015-01 (upstream dependency); RFP §3.4

### 4. IFC Drawings Are the Final Authority

The conceptual electrical drawing (App B-Elec) establishes intent and approximate layout. The Issued for Construction drawings produced under PKG-004 (DEL-004-05 Receptacle Layout Plans; DEL-004-06 Panel Schedules; DEL-004-09 Electrical Specification) are the binding installation authority. The Electrical Contractor must follow the IFC drawings and report any conflicts to the designer before proceeding.

**Field Change Authority [Ref: X-001]:** Not all deviations from IFC drawings require a formal RFI or design revision. Minor field adjustments within normal trade practice (e.g., slight repositioning of a receptacle box to avoid a framing obstruction, provided the adjustment does not affect circuit length, capacity, or code compliance) may be within the Electrical Contractor's field judgment. However, the threshold between a minor field adjustment and a conflict requiring designer input is TBD. Until this threshold is formally defined (recommended: by the Project Manager in coordination with the Designer before construction begins), all deviations from IFC drawings should be documented and reported to the Designer for approval. Source: _SEMANTIC_LENSING.md X-001.

Source: RFP §3.3.2; Decomposition PKG-004 deliverables

### 5. Code Compliance Is Non-Negotiable

All installation must conform to the Canadian Electrical Code (CEC) Part I as adopted in Alberta, and must receive Safety Codes Officer inspection sign-off before energization. The County project representative must be present at all inspections and receive copies of all reports.

Source: RFP §3.3.2; REQ-015-03-04

---

## Considerations

### Maintenance Shop Environment

A heavy equipment maintenance shop is a demanding electrical environment. Consider:
- **Mechanical damage risk:** Receptacles at or near floor level in vehicle bays may be exposed to physical damage from equipment. Recessed, surface-mounted industrial boxes, or height-positioned mounting may be appropriate. TBD per IFC drawings.
- **Dust and moisture:** Wash bay receptacles and any exterior-adjacent locations require weatherproof or in-use covers. Shop floor areas subject to wash-down may similarly require protective covers.
- **Load diversity:** The main shop will operate multiple high-demand loads simultaneously (welders, air compressors, power tools). Panel capacity and circuit protection must account for concurrent use. This is a design consideration for PKG-004, not the installer — however, the Electrical Contractor should flag unexpected load conflicts during installation review.

**Device Grade and Quality Criteria [Ref: C-004]:** The maintenance shop environment (mechanical damage risk, dust exposure, moisture in wash bay, high-demand cycling at welding stations) suggests that specification-grade or industrial-grade devices are appropriate rather than commercial/residential-grade. Key quality distinctions:
- **Specification-grade** devices (vs. commercial-grade) typically offer heavier-duty internal contacts, better terminal design for secure wiring, and longer service life under frequent use.
- **Industrial-grade** devices add enhanced impact resistance, higher duty-cycle ratings, and may include features suited to harsh environments (e.g., corrosion-resistant faceplates).
- Selection should align with the environmental demands of each zone (e.g., industrial-grade in the main shop and welding station; specification-grade may be adequate in the office and parts room).
- Final device grade is TBD pending confirmation in DEL-004-09 (IFC Electrical Specification). Source: _SEMANTIC_LENSING.md C-004.

Source: ASSUMPTION based on facility type (heavy equipment maintenance shop); App B-Elec

### GFCI Requirements

The CEC requires GFCI protection in wet/damp locations. The wash bay is explicitly a wet area. The office and utility room may also require GFCI protection depending on proximity to sinks or water sources. Specific GFCI requirements are TBD pending DEL-004-09 (Electrical Specification).

Source: ASSUMPTION based on CEC general principles; App B-Elec

### Sequencing with Other PKG-015 Deliverables

- DEL-015-01 (Three-Phase Power Service) must be substantially complete and the main distribution board/panels installed before receptacle rough-in wiring can be terminated and tested.
- DEL-015-02 (Lighting) and DEL-015-03 (Receptacles) can be roughed-in concurrently, but share the same panel infrastructure. Circuit assignments must be coordinated to avoid overloading panel circuits.
- DEL-015-04 (Equipment Power Circuits) covers large fixed-equipment circuits. Any receptacles that may double as equipment power connections (e.g., compressor, pressure washer) must be clearly assigned to the correct deliverable to avoid scope overlap. The current decomposition places 40A compressor, 70A fire hose pump, and 70A pressure washer under DEL-015-04.

Source: Decomposition §7 PKG-015 table; _DEPENDENCIES.md

### Upstream IFC Deliverable Tracking [Ref: E-001]

The Electrical Contractor's work on DEL-015-03 depends on timely receipt of IFC deliverables from PKG-004 (DEL-004-05, DEL-004-06, DEL-004-09). To mitigate schedule risk:
- **Before Phase 1:** Confirm with the Project Manager that all three IFC deliverables are on track for the scheduled release. If any are delayed, assess impact on receptacle procurement lead times and rough-in scheduling.
- **Before Phase 2:** Confirm that IFC drawings are issued at current revision and no revision is pending. Do not commence rough-in against superseded drawings.
- **Ongoing:** If any upstream IFC deliverable revision is issued after rough-in has begun, assess field impact and coordinate with the Designer and Project Manager before proceeding.

The mechanism for tracking upstream deliverable status is TBD — recommended to be established by the Project Manager as part of overall project coordination. Source: _SEMANTIC_LENSING.md E-001.

### Welding Station Density

The conceptual drawing shows a notably high receptacle density at the welding station in the NE corner, including 50A/240V (×3), 30A/240V (×3), 20A/240V (×2), and 20A/120V (×2) outlets in close proximity, along with an exhaust fan circuit. This cluster represents the highest electrical demand zone. Conduit routing, box fill, and conductor sizing in this zone require careful coordination during installation.

Source: App B-Elec

### Assumption Invalidation Handling [Ref: D-001]

Multiple requirements in this deliverable rest on assumptions that may be invalidated:
- **D-009 (welding receptacle rating — 50A/240V):** If County welder specifications differ, this triggers a declared scope change per Decomposition D-009. Guidance Principle 2 and CONF-015-03-01 address this scenario.
- **Device grade (specification-grade vs. industrial-grade):** If DEL-004-09 specifies a different device grade than assumed, procurement and potentially installation must be revised. Cost implications depend on the magnitude of the change.
- **GFCI/AFCI zone requirements:** If the applicable CEC edition or DEL-004-09 requires GFCI or AFCI in zones not currently anticipated, additional devices/breakers and potentially circuit modifications may be needed.

For any assumption invalidation after work has commenced:
1. Document the invalidated assumption and the new information.
2. Assess scope, schedule, and cost impact.
3. Submit a formal change notice to the Project Manager per the contract terms (CCDC 14-2013).
4. Do not proceed with affected work until the change is authorized.

Source: _SEMANTIC_LENSING.md D-001; Contract terms (CCDC 14-2013); Decomposition D-009

---

## Trade-offs

| Topic | Trade-off |
|---|---|
| Welding receptacle specification | 50A/240V assumed. If actual welder spec is higher (e.g., 60A), the circuit conductors, breakers, and device ratings must all be upgraded — retroactive changes after rough-in are costly. Early confirmation from County is preferred. |
| Receptacle mounting height / protection | Flush-mount vs. surface-mount box selection affects both cost and durability. Industrial surface-mount boxes offer better protection in shop environments but require more space. TBD in IFC drawings. |
| GFCI device vs. GFCI breaker | Either approach satisfies code. GFCI breakers protect the full circuit but are more expensive; GFCI devices protect only the outlet. Selection TBD in IFC specification (DEL-004-09). |

---

## Examples

The conceptual electrical drawing (App B-Elec) illustrates the intended layout using a symbol legend:

| Symbol | Meaning |
|---|---|
| (15) | 15A/120V receptacle |
| (20) unlabeled | 20A/120V receptacle |
| (20) with box | 20A/240V receptacle |
| (30) | 30A/240V receptacle |
| (50) | 50A/240V receptacle |
| L | Light fixture (not this deliverable) |
| E | Exhaust fan (not this deliverable) |

Source: App B-Elec legend

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-015-03-01 | Welding receptacle amperage: RFP §3.4 states "County to supply welding equipment specifications" but no specs were provided; Decomposition D-009 assumes 50A/240V. If County specs differ, the design changes. | RFP §3.4 (welding plug specs TBD) | Decomposition D-009 (assumes 50A/240V) | Datasheet Attributes, REQ-015-03-01, Welding station layout | County to confirm actual welder plug specifications before IFC drawings are finalized | TBD |
| CONF-015-03-02 | Scope boundary between DEL-015-03 and DEL-015-04 for receptacle-style equipment connections: any receptacles serving dual purposes (equipment power and general receptacle use) may fall in a scope gap between the two deliverables. [Ref: E-002] | Specification Scope — Excluded (DEL-015-04 covers equipment circuits) | Guidance — Sequencing with Other PKG-015 Deliverables (scope overlap noted) | Specification Scope, Datasheet Attributes | Project Manager / Decomposition authority to confirm scope assignment | TBD |
