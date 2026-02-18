# Guidance — DEL-02-05: Electrical/IT Concept Narrative

---

## Terminology Note

**Main Equipment Room (MER):** The canonical term for the IT/telecommunications room in this deliverable is "Main Equipment Room" abbreviated as "MER." Earlier document drafts and some source references use "telecom room" as an equivalent term. All four documents for DEL-02-05 use "MER" as the standard designation. (Semantic Lensing F-002)

---

## Purpose

This deliverable exists to establish the conceptual electrical and IT architecture for the Penhold Public Services Building, giving the Town's evaluation committee confidence that the proponent team understands how power, communications, lighting, safety, and security systems will serve the combined Fire Hall and Public Works facility.

DEL-02-05 is the Electrical Engineer's contribution to the PKG-002 Conceptual Design package. It is evaluated under OBJ-003 (Proposed Conceptual Design, 20 pts — the highest-weighted single technical criterion). A strong Electrical/IT Concept Narrative demonstrates:

1. **Operational understanding** — power reliability for fire response, public works operations, emergency command, and cold-climate conditions.
2. **Code compliance** — clear pathways to Alberta Building Code, CEC Part I, Alberta Fire Code, and IES lighting standards.
3. **Cross-discipline integration** — generator scope coordinated with DEL-02-04; architectural layout followed from DEL-02-01; solar orientation consistent with Addendum 03.
4. **Addendum 03 compliance** — all electrical-relevant program clarifications explicitly embedded.
5. **Forward-looking provisions** — solar-ready roof, access control and security infrastructure for future retrofit, IT scalability.

(Source: _CONTEXT.md; Decomposition §6 OBJ-003; RFP 7.1.1)

---

## Principles

### P-001: Operational Reliability is the Foundational Design Value

The electrical systems for a combined fire hall and public works operations facility must prioritize **uninterrupted operational readiness**, not just code minimum. This means:

- Generator backup ensures continuous power to the ICP meeting room (emergency command), kitchen, bathrooms, and bay door secondary opening — all per Addendum 03 minimum requirements.
- Lighting in apparatus bays must meet functional safety levels without exception; failures in apparatus bay lighting impair emergency response.
- IT infrastructure must support fire dispatch connectivity and radio charging even during utility outages.

**Rationale:** A fire hall that loses utility power cannot afford to lose dispatch, command, or bay access. The concept narrative must convince evaluators that operational imperatives are understood and embedded in the design.

(Source: Addendum 03 generator requirement; _CONTEXT.md; Decomposition OBJ-003)

### P-002: Electrical Concept Follows the Architectural Layout

The electrical narrative must be spatially coherent with the architectural concept in DEL-02-01:

- Main service entrance location is tied to the utility entry point shown on the civil site plan (DEL-02-02).
- Switchgear and distribution panel locations are coordinated with the mechanical room shown in DEL-02-01.
- Lighting zones match architectural space categories (high-bay apparatus bays, office areas, residential quarters, shared spaces).
- Main Equipment Room (MER) placement follows from the architectural floor plan.

**Rationale:** Evaluators read PKG-002 as an integrated multi-discipline package. Electrical concepts that appear inconsistent with the architectural layout signal weak team coordination.

(Source: Decomposition §8 PKG-002 description; RFP 7.1.1; DEL-02-01 cross-reference in _REFERENCES.md)

### P-003: Addendum 03 Solar Provisions Are a Mandatory Design Element

Solar-capable roof electrical rough-ins are not optional enhancements — they are a program requirement under Addendum 03. The roof orientation constraint (flat, south, west, or southwest) must be reflected in the electrical narrative as an established design parameter, not a future consideration.

**Rationale:** Addendum 03 governs over the base RFP (Decomposition §2). Failure to address solar provisions explicitly risks non-compliance under SOW-0010 (embed program clarifications and special requirements).

(Source: Addendum 03 solar-capable roofing requirement; Decomposition SOW-0010; Decomposition §2 addenda rule)

### P-004: Access Control and Security Are Additional Options — But Base Design Must Support Them

Access control (Option 3) and security cameras (Option 4) are priced separately in Appendix H Schedule A and are not in the base cost. However, the base design must include conduit runs, controller location provisions, and MER space allocation so these systems can be added without major rework.

**Rationale:** Separating the infrastructure provision from the system itself keeps base cost competitive while allowing the Owner to exercise options. Evaluators expect the proponent to understand this distinction.

(Source: Decomposition vocabulary map; Addendum 03; RFP Appendix H Schedule A; _CONTEXT.md)

### P-005: LED Lighting Must Be Justified by Space Function, Not Just Technology

The IES-referenced LED approach must be applied at the space level, not stated generically. Different spaces in the PSB have fundamentally different lighting requirements:

- Apparatus bays: high illuminance (ASSUMPTION: 300–500 lux), cool white for task visibility, high luminaire mounting to avoid obstruction by equipment.
- Offices and administrative areas: moderate illuminance (ASSUMPTION: 300–400 lux), occupancy sensors appropriate.
- Residential quarters (fire hall): warm white, lower lux levels appropriate for living areas.
- Cold Storage building: minimal lighting, freeze-rated fixtures required (ASSUMPTION: cold-temperature-rated LED fixtures).

**Rationale:** A space-by-space lighting approach demonstrates operational understanding and IES familiarity, increasing evaluation score credibility.

(Source: _CONTEXT.md LED per IES; Decomposition DEL-02-05 description; IES Recommended Practices — specific standards TBD)

### P-006: Fire Alarm Is a Non-Negotiable Life Safety System

The fire alarm system concept must address:

- Addressable FACP (more flexible and maintainable than conventional systems for a multi-zone facility).
- Heat detectors in apparatus bays (high ambient temperatures may defeat smoke detectors — ASSUMPTION based on fire hall building type conventions).
- Smoke detectors in all occupied spaces, mechanical rooms, and storage areas.
- Manual pull stations per Alberta Building Code requirements.
- HVAC interface (apparatus bay exhaust fans may interlock with alarm conditions).
- Emergency lighting and exit signs on dedicated circuits with battery backup.

**Rationale:** Life safety systems are code-mandated and non-negotiable. A strong concept demonstrates both code compliance and operational familiarity with fire station environments.

(Source: _CONTEXT.md; Alberta Building Code — ASSUMPTION applicable; Alberta Fire Code — ASSUMPTION applicable; ULC S524 — ASSUMPTION applicable)

---

## Considerations

### C-001: Generator Coordination with Mechanical Concept (DEL-02-04)

The electrical narrative must not contradict the generator fuel type, size, or location established in DEL-02-04. The Electrical Engineer's scope is the electrical connection side: ATS, essential panel, essential load list, and transfer switching logic.

**How to address:** Include an explicit coordination statement referencing DEL-02-04 for generator specification details. State assumptions used for electrical design (e.g., assumed generator output voltage, ATS type) and flag them as subject to confirmation at detailed design.

(Source: _REFERENCES.md DEL-02-04 cross-reference; Decomposition DEL-02-04 description)

### C-002: Solar Provisions Must Be Proportional — Provisions, Not Installation

The narrative must clearly distinguish between:
- **Solar provisions** (what is being provided now): conduit, breaker space, inverter stub-out — low cost, enables future retrofit without major electrical redesign.
- **Solar installation** (not in scope): PV panels, mounting, inverter, utility interconnect agreement — these are future decisions.

This distinction keeps base cost competitive while satisfying the Addendum 03 solar-capable requirement.

(Source: Addendum 03; Decomposition C-11 re: FF&E additional item model as analogous; DEL-04-03 sustainability scope)

### C-003: IT Scalability Is an Operational Investment

Municipal public services facilities have a 50-year design life. IT infrastructure installed today must accommodate:
- IP-based fire dispatch systems (CAD workstations, radio interfaces).
- Future body camera and in-vehicle video systems (higher bandwidth).
- Public works fleet management and work order systems.
- Network-connected building systems (access control, CCTV, building automation).

**How to address:** Specify a fiber backbone from the Main Equipment Room (MER) to distribution points, with copper horizontal runs to endpoints. Reserve 25% spare conduit capacity (ASSUMPTION: standard structured cabling practice). This approach supports bandwidth growth without re-running backbone cabling.

(Source: _CONTEXT.md; 50-year design life per Decomposition OBJ-005; ASSUMPTION — IT scalability provisions are standard practice for public facilities)

### C-004: Lighting Controls Must Be Operationally Practical

Fire hall staff work irregular hours and need predictable, reliable lighting control. Overly automated systems (e.g., occupancy sensors with short timeouts in apparatus bays) can create hazardous conditions if lights turn off during active operations.

**How to address:** Manual control in apparatus bays with optional occupancy-based dimming (not full shutoff). Occupancy-based shutoff appropriate for offices, bathrooms, and storage areas. Daylight harvesting in perimeter offices only if cost-justified.

(Source: P-005 above; ASSUMPTION — operational safety practice for fire hall environments)

### C-005: Apparatus Bay Exhaust Coordination Has Electrical Implications

The fire apparatus direct exhaust ventilation system required by Addendum 03 (scope: DEL-02-04) involves fan motors, damper controls, and sensing equipment — all of which require electrical supply and control wiring from this deliverable's scope.

**How to address:** Note in the narrative that "electrical supply and control provisions for apparatus bay exhaust fan motors and damper actuators are coordinated with mechanical design per DEL-02-04." Do not design the HVAC controls in this deliverable; only establish that the electrical infrastructure supports them.

(Source: Addendum 03 apparatus bay exhaust requirement; Decomposition DEL-02-04; _REFERENCES.md DEL-02-04 cross-reference)

### C-007: EV Charging Infrastructure Readiness (Future Consideration)

A facility with a 50-year design life (Datasheet, Design Life — Main Building) and associated parking areas (DEL-03-01 scope) may benefit from conduit provisions to parking areas for future electric vehicle charging infrastructure. At the concept stage, this could be addressed by noting spare conduit capacity from the main switchgear to the parking area, with panel breaker space reserved for future EV charging circuits.

**How to address:** TBD — confirm with Owner / RFP whether EV charging readiness is desired. If so, include conduit and panel provisions in the electrical distribution concept (similar to the solar provisions model). If intentionally excluded, state the exclusion explicitly.

**Status:** TBD — no source document currently addresses EV charging. This consideration is included based on the 50-year design life and foreseeable transportation electrification trends. (Semantic Lensing X-001)

(Source: Datasheet — 50-year design life; ASSUMPTION — EV charging readiness is an emerging provision for public facilities with long design lives)

### C-008: CRI (Color Rendering Index) Values Are Operationally Important

Minimum Color Rendering Index (CRI) values should be established as a lighting quality parameter, not merely mentioned in examples. For a fire hall and public works facility:

- **CRI 90 minimum** for functional task areas (apparatus bays, workshops, offices) — accurate color rendering supports visual inspection of equipment, reading of color-coded labels, and general task performance.
- **CRI 80 minimum** for support and storage spaces — adequate color rendering for general orientation and safety.

**How to address:** Elevate CRI requirements from the example narrative (EX-003) into a stated consideration or specification requirement. Ensure that CRI values appear in both the lighting concept narrative section and the Specification (currently not captured as a requirement).

(Source: Guidance EX-003; IES Recommended Practices — specific CRI guidance location TBD; ASSUMPTION — CRI 90/80 split is standard practice for emergency services facilities) (Semantic Lensing F-003)

### C-006: Cold Storage Building Has Minimal but Specific Electrical Requirements

The 60'x100' Cold Storage building is unheated. Electrical provisions must account for:
- Freeze-rated LED fixtures (standard LED drivers may fail below -20°C — ASSUMPTION).
- Minimal power outlets for maintenance equipment (ASSUMPTION: standard practice).
- No HVAC electrical loads (unheated by design).
- Exterior lighting for security and access.

**How to address:** Describe Cold Storage electrical provisions as a discrete section or sub-section of the main narrative, noting the unheated condition and freeze-rated fixture requirement.

(Source: Decomposition DEL-02-05 description mentions Cold Storage; RFP Functional Program Appendix B — Cold Storage as separate building; ASSUMPTION: freeze-rated fixtures required for unheated Alberta building)

### C-009: Procedure Duration Estimates Are Conceptual Targets

The step-by-step duration estimates in Procedure.md (Steps 1-11) total approximately 28-40 hours of Electrical Engineer time. These estimates assume a qualified Electrical Engineer with prior fire hall / municipal facility experience, working from reasonably mature upstream deliverables (DEL-02-01 architectural concept, DEL-02-02 civil site concept, DEL-02-04 mechanical concept). The estimates also assume reference materials (RFP, Addendum 03, IES standards, applicable codes) have been pre-reviewed.

**Rationale:** Duration estimates are provided to support resource planning for proposal preparation. They are not contractual commitments. For teams with less fire hall experience or where upstream deliverables are less mature (e.g., architectural concept is still in flux), actual effort may exceed estimates by 50-100%. The integration review step (Step 10, 5-7 hours) is the longest single step because it requires cross-checking all nine-plus narrative sections against all specification requirements and the Addendum 03 checklist. (Semantic Lensing D-001)

(Source: ASSUMPTION -- duration estimates based on typical concept-stage narrative authorship for multi-discipline municipal facility design-build proposals)

### C-010: PA / Paging System Applicability (TBD)

Fire halls commonly use public address (PA) and paging systems for station alerting, overhead announcements, and coordination between apparatus bays and administrative areas. Whether a PA/paging system is within scope for this facility is TBD pending Owner or RFP clarification.

**How to address:** Confirm with the Owner whether a PA/paging system is required. If required, the electrical concept should include: speaker zone layout (apparatus bays, common areas, residential quarters), amplifier and head-end equipment location (in MER or separate), integration with fire dispatch alerting, and dedicated circuit provisions. If not required, state the exclusion explicitly in the narrative.

**Status:** TBD -- no source document currently addresses PA or paging. The abbreviation "PA" may appear in some project context references but is not definitively defined. This consideration is included based on standard fire hall communication practice. (Semantic Lensing A-003, E-002)

(Source: ASSUMPTION -- PA/paging is standard for fire halls; _CONTEXT.md and RFP do not explicitly address this system)

---

## Trade-offs

### T-001: Generator Essential Loads Only vs. Extended Coverage

| Option | Description | Cost Implication |
|---|---|---|
| A — Minimum coverage | Generator serves only Addendum 03 minimum: kitchen, ICP, 2 bathrooms, bay door secondary mechanism (~25 kW estimated) | Lower capital cost; meets code minimum |
| B — Extended coverage | Generator also serves emergency lighting, sump pumps, IT/MER, minimal HVAC for equipment protection | Higher capital cost; greater operational resilience |

**Recommendation:** Size essential panel for Addendum 03 minimum loads with 20% design margin (ASSUMPTION: ~30 kW), with capacity identified to add extended loads at detailed design if Owner chooses. This keeps base cost competitive while allowing scope expansion.

(Source: Addendum 03 generator essential loads; ASSUMPTION — 20% design margin is standard generator sizing practice)

### T-002: LED Lighting Control Complexity vs. Energy Savings vs. Operational Simplicity

| Option | Description | Trade-off |
|---|---|---|
| A — Manual switches | Manual on/off in all spaces | Simple, reliable; no energy savings beyond LED efficiency |
| B — Occupancy sensors in part-time spaces | Occupancy sensors in offices, bathrooms, storage; manual in operational bays | 20–30% additional energy reduction; minimal maintenance burden |
| C — Full building automation | Centralized lighting control with scheduling, daylight harvesting, remote management | Maximum energy savings; highest cost and maintenance; risk of operational friction |

**Recommendation:** Hybrid approach (Option B): manual control in apparatus bays (safety-critical), occupancy sensors in administrative and support areas. Matches fire hall operational culture and provides meaningful energy savings without complexity.

(Source: P-005; C-004; ASSUMPTION — hybrid approach is standard practice for fire hall lighting)

### T-003: IT Cabling Architecture — Fiber vs. All-Copper

| Option | Description | Trade-off |
|---|---|---|
| A — All copper (Cat 6A) | Copper horizontal cabling throughout; no fiber backbone | Lower initial cost; 100m distance limit may require additional distribution racks |
| B — Fiber backbone + copper horizontal | Fiber between MER and distribution points; copper from distribution to devices | Higher initial cost; unlimited backbone distance; future bandwidth capacity |

**Recommendation:** Option B — fiber backbone where building dimensions exceed copper limits or where long-term bandwidth scalability is prioritized for a 50-year facility. Document cost differential at detailed design.

(Source: C-003; 50-year design life; ASSUMPTION — fiber backbone is standard practice for public facilities with long design lives)

### T-004: Access Control and Security — Infrastructure Now vs. Full System Now

| Option | Description | Trade-off |
|---|---|---|
| A — Infrastructure only (base) | Conduit, controller location, and MER space reserved; no system installed | Low base cost; future retrofit possible |
| B — Full system (additional option) | Complete access control and CCTV system installed at construction | Higher cost (Additional Options 3 and 4); full capability at occupancy |

**Recommendation:** Base design includes infrastructure provisions only (Option A). Price complete systems as Additional Options 3 and 4 per Appendix H Schedule A/B. Narrative must describe both the base infrastructure and the optional full systems to support pricing of both.

(Source: Decomposition vocabulary map; RFP Appendix H; _CONTEXT.md; Addendum 03)

---

## Examples

### EX-001: Effective Solar-Capable Roof Electrical Provision Statement

A well-written solar provisions section states provisions concretely and distinguishes them from solar installation:

> "The electrical design includes roof-ready provisions for future photovoltaic installation, consistent with the Addendum 03 solar-capable roof requirement. The roof orientation (south-facing slope / flat, per Addendum 03) supports a future array estimated at 25–50 kW, subject to detailed structural and electrical design. Provisions include: (1) 2-inch conduit routed from the main switchgear room to the roof penetration point, sized to accommodate future PV output conductors; (2) two spare 60A breaker spaces reserved in the main distribution panel for future solar inverter connection; (3) floor space allocation of 4 linear feet adjacent to the main switchgear for a future string or micro-inverter assembly. These provisions are included in the base electrical scope; PV panels, mounting hardware, and inverter equipment are not included in this proposal."

**Strength:** Concrete, distinguishes provisions from installation, cites Addendum 03, states limitations clearly.

### EX-002: Generator Essential Load Narrative That Satisfies Addendum 03

> "The essential electrical panel is sized to support the following minimum loads per Addendum 03: kitchen equipment (estimated 15 kW), meeting room / Incident Command Post (estimated 5 kW), two bathrooms (estimated 3 kW), and fire apparatus bay door secondary opening mechanism (estimated 2 kW), totaling an estimated 25 kW critical load. The essential panel is fed via an automatic transfer switch (ATS) coordinated with the diesel / natural gas standby generator specified in the Mechanical Concept Narrative (DEL-02-04). Transfer switching is automatic on utility voltage loss, with a soft-start delay to manage generator loading. Manual bypass is provided for ATS maintenance. Generator capacity and fuel type are per DEL-02-04."

**Strength:** Directly satisfies R-EL-05; cites Addendum 03 explicitly; defers generator sizing to DEL-02-04; provides estimated load figures; describes ATS logic.

### EX-003: LED Lighting Narrative Demonstrating IES Awareness

> "Lighting design follows IES Recommended Practice standards. Fire apparatus bays are designed for a maintained average illuminance of 300–500 lux (ASSUMPTION: consistent with IES RP-5 and NFPA fire station guidelines) using LED high-bay fixtures mounted at truss chord level to avoid interference with apparatus. Fixtures are rated for dusty environments and selected for ease of re-lamping from a rolling maintenance platform. Office areas target 300–400 lux average using LED panel troffers with integral occupancy sensors and manual override. Residential quarters use warm-white LED (2700K) at 150–200 lux, consistent with a residential living environment. All LED selections target a minimum CRI of 90 for functional task areas and 80 for support/storage spaces. Cold Storage building uses freeze-rated LED strip fixtures rated for operation to –40°C, given the unheated building condition."

**Strength:** Space-by-space rationale; IES cited; Cold Storage exception noted; CRI and color temperature addressed; operational environment (dust, maintenance access) acknowledged.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| (None identified in this pass) | — | — | — | — | — | TBD |

> No conflicts between source documents were identified for this deliverable in this run. If contradictions emerge during authorship (e.g., between Addendum 03 essential loads and Functional Program power requirements), they should be added here for human ruling before detailed design.
