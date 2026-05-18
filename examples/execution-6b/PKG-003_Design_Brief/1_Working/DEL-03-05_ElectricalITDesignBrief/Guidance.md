# Electrical/IT Design Brief — Guidance

## Purpose

The Electrical/IT Design Brief serves two roles within the Penhold PSB proposal:

1. **Design Justification:** Explain *why* specific electrical and IT systems were selected to meet the Owner's operational needs and RFP requirements. The narrative supports evaluation scoring under "Design Brief" (5 evaluation points total for all five discipline sub-briefs per RFP §8.3) and provides context for both the evaluation committee and the design team.

2. **Proposal Persuasion:** Demonstrate that the electrical/IT design is thoughtful, coordinated, and reflects the team's understanding of the combined fire hall and public works operations facility's operational and technical requirements.

The brief is not a specification or technical document; it is a story about design decisions and their rationale. The audience is the Owner's evaluation committee — not an electrical engineer reviewing shop drawings.

**Scoring context:** The Design Brief category is allocated 5 evaluation points total (RFP Section 8.3), shared across five discipline sub-briefs. The electrical sub-brief should prioritize content that demonstrates: (a) the team has read and understood all OSR electrical/IT requirements including Addendum 03 additions, (b) design choices are justified with operational rationale not just code compliance, and (c) cross-discipline coordination is visible and substantive. **ASSUMPTION:** Each discipline sub-brief contributes proportionally to the 5-point allocation; the electrical sub-brief's contribution is maximized by addressing all seven sub-topics with persuasive rationale rather than by volume alone. (Source: RFP Section 8.3; Decomposition Evaluation Criteria Crosswalk)

**Self-assessment criteria for persuasion:** Before finalizing, review each narrative section against these questions:
- Does each section explain *why* this approach was chosen, not just *what* was chosen?
- Would a non-specialist evaluator understand the operational benefit of each design decision?
- Does the narrative demonstrate that the design team has coordinated across disciplines (not just stated it)?
- Are all seven sub-topics addressed with source-anchored rationale, not generic statements?
If the answer to any question is "no," the corresponding section needs strengthening before submission.

---

## Principles

### P-01: Operations-Driven Design
The electrical/IT systems serve the facility's operational mission: firefighting, emergency response, public works operations, and community services. Every design choice should trace back to operational needs and constraints stated in the RFP or Addenda.

**Application:** LED lighting in apparatus bays benefits from reduced heat (improves apparatus storage), long fixture life (less access-at-height maintenance), and reduced load on emergency backup power. These are operational benefits, not just energy savings.

### P-02: Transparency About Trade-Offs
Name each significant trade-off, state the choice made, and explain the rationale. This applies especially to decisions where multiple approaches are defensible (e.g., centralized vs. distributed building controls; full vs. partial backup power).

**Application:** Generator load shedding strategy — brief should name non-critical loads that shed on generator start, confirm which critical loads are protected per Addendum 03 §1.15, and explain why this approach meets operational needs at reasonable cost.

### P-03: Visible Coordination Across Disciplines
Electrical systems do not operate in isolation. The brief earns credibility by explicitly acknowledging where electrical design connects to other disciplines:
- **Mechanical:** Generator fuel supply and transfer switching; overhead door opener compatibility (RFP OSR §10.4); HVAC controls integration
- **Structural/Architectural:** Panel placement and accessibility; fixture heights for machinery clearance (RFP OSR §10.5); cable routing through building structure
- **IT/Dispatch:** Apparatus bay display system for emergency dispatch data (RFP OSR §10.6)

### P-04: Compliance as a Minimum, Differentiation Beyond
Code compliance (Alberta Building Code, Canadian Electrical Code, IES lighting standards) is non-negotiable but not noteworthy. The brief should focus on *beyond-code* choices — energy efficiency, maintainability, future flexibility — that differentiate the proposal.

**Application:** "Lighting follows IES recommendations and uses energy-efficient LED per RFP OSR §10.5. Beyond code minimum, occupancy controls and zone-based lighting schedules reduce operating costs and extend lamp life by matching operation to actual occupancy patterns."

### P-05: Source-Anchored Statements
Every system selection claim should anchor to a source. "We propose LED lighting" is a statement. "LED lighting is specified per RFP OSR §10.5 (p. 42) which requires IES-compliant, energy-efficient LEDs; this choice also supports energy efficiency objectives and reduces maintenance access frequency over the 50-year design life" is persuasive and source-anchored.

### P-06: Explicit Scope Boundaries for Optional Items
Access control (Additional Option 12.3) and security/camera (Additional Option 12.4) are priced separately. The brief must be explicit: base electrical design includes the infrastructure (conduit, power, cabling) to support these systems; the optional items cover equipment and installation. Without this clarity, the evaluator cannot assess what is included in the base proposal.

---

## Considerations

### C-01: Facility Type and Operational Profile
This is a combined fire station and public works facility. Electrical design must serve both:

- **Fire Department:** 24/7 partial staffing; apparatus bays with heavy equipment and combustion residue; emergency response dispatch system (RFP OSR §10.6 dispatch display requirement); life safety systems (fire alarm, emergency egress lighting).
- **Public Works:** Regular business-hours operations; workshop and equipment bays; occasional welding/idling (mechanical ventilation coordination); exterior yard lighting (Additional Option 12.2) and gate/access control.
- **Shared spaces:** Meeting room / ICP with 15 concurrent internet access points for Emergency Management (RFP OSR §10.6); kitchen on emergency backup power (Addendum 03 §1.15).

The operational duality must be evident in lighting zone strategies, backup power prioritization, and IT infrastructure placement.

### C-02: Generator Sizing and Critical Loads
Addendum 03 §1.15 establishes the minimum generator critical load list: kitchen, meeting room/ICP, two bathrooms, bay door secondary opening mechanism. The Electrical brief must:

- State these minimum loads explicitly
- State whether bay door secondary opening is generator-powered or manual (both are acceptable per Addendum 03 §1.15)
- Note that generator capacity determination is the Mechanical Engineer's responsibility (DEL-02-04); the Electrical brief confirms the transfer switching design and load shed strategy consistent with stated generator capacity
- Avoid contradicting the generator sizing stated in DEL-02-04

This is a coordination dependency. The brief should state a capacity assumption clearly and label it as such if DEL-02-04 is not yet finalized.

### C-03: Solar-Readiness Is a Binding Requirement
Addendum 03 §1.17 states: "Yes, solar capable roofing is required. Roof orientation can be flat, south, west, or southwest sloped to accommodate solar panels in the future." This is not optional. RFP OSR §10.3.9 also states solar loading capabilities must be considered.

The brief must confirm:
- Roof orientation (from DEL-02-01 Architectural Concept)
- Electrical infrastructure pre-positioned for future solar: conduit runs, panel space reservation, appropriately sized disconnects
- What is in base contract (infrastructure) vs. future Owner addition (solar equipment/installation)
- That solar equipment and installation are not in the base contract

**Phasing statement (required):** "Solar installation is not included in the base contract; however, electrical infrastructure (conduit from roof to electrical room, reserved panel space, and appropriately sized disconnects) is included in base scope to enable a cost-effective future solar addition at Owner's discretion."

### C-04: IT and Emergency Communications Focus
RFP OSR §10.6 has three specific requirements that must all appear in the brief:
1. IT/data compatibility throughout main structure
2. Meeting room: 15 concurrent internet access points for Emergency Management
3. Apparatus bay: wall-mounted dispatch display system in the bay closest to the office (TV + laptop with dispatch data connectivity)
4. PA system: throughout main structure only (not in ancillary buildings)

These are detailed, specific requirements. The brief must address each by name. Omitting the 15-concurrent-access-point requirement or the dispatch display system would indicate the team has not read the OSR carefully — which undermines evaluator confidence.

### C-05: Access Control and Security — Clear Scope Delineation
Access control (§12.3) and security/camera (§12.4) are Additional Optional Items. However, the electrical infrastructure to support them — conduit, power outlets, data cabling, panel capacity — is a base design responsibility. The brief must make this two-layer structure explicit:

- **Base contract:** Electrical and data infrastructure ready to receive access control and security systems
- **Additional Option 12.3:** Access control equipment and installation (multi-zone, main structure only; ancillary buildings excluded per OSR §12.3)
- **Additional Option 12.4:** Security and camera equipment, installation, and monitoring costs (priced separately per OSR §12.4)

The Town has stated no preference on suppliers (Addendum 03 §1.19), so the brief should describe the infrastructure approach rather than proposing specific brands.

### C-06: Lighting Design for Harsh Industrial Zones
Apparatus bays and public works bays are harsh environments: vehicle exhaust, road salt, moisture from washing and snow melt (Addendum 03 §1.8: all bays require sumps), mechanical impact risk. The brief should address:

- Fixture protection ratings appropriate for wet/corrosive environments in bay areas
- Fixture mounting heights that avoid interference with apparatus and equipment (RFP OSR §10.5)
- Weatherproof covers on switches at person doors of ancillary buildings (RFP OSR §10.5)
- LED fixture standardization across zones to reduce spare parts inventory and simplify maintenance

### C-07: Design for Maintainability
Durability and ease of maintenance is a 15-point evaluation criterion (RFP §7.1.4). The Electrical brief should support DEL-05-04 (Electrical Maintainability) by including:

- Electrical panel locations that are safely and conveniently accessible for maintenance staff
- Standardized fixtures and control components using locally available parts
- Clear labeling and documentation strategy (one-line diagrams, panel schedules, as-built drawings) delivered in O&M manuals at project close-out
- Fixture and component lifecycles consistent with the 50-year main building design life and 20-year cold storage design life

---

## Trade-offs

### T-01: LED Fixtures vs. Traditional Lighting
**Choice:** LED throughout all buildings.

| Factor | Assessment |
|--------|------------|
| **Pro** | Energy savings (40–60% vs. fluorescent); 50,000+ hour rated life reduces maintenance access frequency; reduced heat gain in apparatus bays; reduced load on emergency backup generator |
| **Con** | Higher upfront unit cost; requires lighting control infrastructure; some occupants prefer warmer tones |
| **Resolution** | Long-term operational savings, reduced maintenance access at height, and compatibility with IES requirements (RFP OSR §10.5) outweigh upfront premium. Color temperature selection (3000–3500K recommended) addresses occupant preference. |
| **Source** | RFP OSR §10.5, p. 42 |

### T-02: Full Facility Backup vs. Critical Loads Only
**Choice:** Partial backup power — critical loads as defined by Addendum 03 §1.15.

| Factor | Assessment |
|--------|------------|
| **Pro (partial)** | Lower generator cost and fuel consumption; Addendum 03 explicitly defines minimum scope; operational sufficiency for emergency response |
| **Con (partial)** | Non-critical areas (offices, non-essential HVAC) lose power during outage |
| **Pro (full)** | Maximum operational continuity during extended outages |
| **Con (full)** | Significantly higher generator cost; larger footprint; higher fuel storage requirement |
| **Resolution** | Addendum 03 §1.15 defines the minimum requirement; brief should state whether base design meets minimum only or exceeds it, with rationale. Exceeding minimum (e.g., adding HVAC for residential quarters) should be justified if proposed. |
| **Source** | Addendum 03 §1.15, p. 4 |

### T-03: Centralized vs. Distributed Building Controls
**Choice:** TBD — brief should state the team's choice and rationale.

| Factor | Assessment |
|--------|------------|
| **Centralized (BACnet/Modbus)** | Single monitoring point; energy optimization; coordinated responses (e.g., HVAC setback when security armed); requires IT support and network infrastructure |
| **Distributed (independent thermostats/switches)** | Simpler; lower cost; lower IT dependency; failure independence; limited optimization capability |
| **Resolution** | The choice should reflect the Town's IT support capacity and operational preferences. A small municipality with limited IT staff may benefit from distributed simplicity. The brief should name the choice, state the rationale, and note the impact on facility operations. |

### T-04: Generator-Powered vs. Manual Bay Door Secondary Opening
**Choice:** TBD — both are acceptable per Addendum 03 §1.15.

| Factor | Assessment |
|--------|------------|
| **Generator-powered** | Automatic/powered operation during utility outage; adds to generator load; requires electrical integration with door opener circuit |
| **Manual override** | Independent of all electrical systems; zero electrical load; requires staff to manually operate during outage (practical for a staffed fire station) |
| **Resolution** | Both options satisfy the requirement. The brief should state the choice and rationale. For a fire station with 24/7 staffing, manual override may be equally practical and lower cost/complexity. |
| **Source** | Addendum 03 §1.15, p. 4 |

---

## Examples

### EX-01: Power Distribution and Generator Strategy Narrative
*"Electrical service is located within a few feet of the site (Addendum 03 §1.6); site servicing tie-in costs are covered under the site servicing cash allowance per Addendum 03 §1.7. Main distribution panel is located in a designated electrical room accessible for maintenance without entering operational areas. Electrical service is sized to accommodate current program loads plus future flexibility including solar PV additions.*

*Emergency backup power is provided by a [TBD kW] diesel standby generator (see DEL-02-04 for generator sizing). Critical loads per Addendum 03 §1.15 are: kitchen, meeting room/ICP, two bathrooms, and bay door secondary opening mechanism ([generator-powered / manual — state choice]). Non-critical loads (office lighting, non-essential HVAC zones) shed automatically on generator start to maintain runtime on critical systems. Transfer switching is automatic with [TBD]-second transfer delay."*

### EX-02: Lighting Design Narrative
*"Lighting throughout all buildings follows IES recommendations and specifies energy-efficient LED fixtures per RFP OSR §10.5. Emergency exit lights above personal doors include internal battery backup per code requirements (RFP OSR §10.5). In apparatus bays and workshop bays, fixture mounting heights are adjusted to avoid interference with graders, tandem dump trucks, and type 1 ladders (per equipment clearance requirements, RFP OSR §10.3.9). Switches at person doors of ancillary (cold storage) buildings have weatherproof covers per RFP OSR §10.5.*

*Lighting controls use occupancy sensors in zones with intermittent use (apparatus bays, storage rooms) and scheduling controls in office areas. Color temperature is 3000–3500K throughout to balance task visibility with occupant comfort."*

### EX-03: IT/Telecommunications Narrative
*"IT/data compatibility is provided throughout the main structure per RFP OSR §10.6. The meeting room/ICP is provisioned for 15 concurrent internet access points to support Emergency Management operations. A dispatch display system is installed in the apparatus bay closest to the office area — a wall-mounted display connected to a laptop that receives dispatching data, consistent with RFP OSR §10.6. A simple PA system serves the main structure for general announcements and emergency notifications; ancillary buildings do not require PA coverage per RFP OSR §10.6.*

*Structured cabling (CAT6 minimum) provides voice, data, and video backbone throughout. A dedicated network equipment space with UPS backup ensures core communication resilience during power outages."*

### EX-04: Solar-Readiness Provisions Narrative
*"Solar-capable roofing is required per Addendum 03 §1.17. The roof is designed with [flat/south/southwest] orientation to optimize future solar PV or thermal installation (confirmed with Architect per DEL-02-01). Solar loading capability is incorporated in roof structural design per RFP OSR §10.3.9.*

*Electrical infrastructure included in base contract: (a) conduit run from roof to electrical room, (b) reserved panel space for future solar inverter breaker, (c) disconnects and overcurrent protection sized for future [TBD kW] solar capacity, (d) sub-metering provision for solar production tracking. Solar equipment and installation are not included in the base contract and are available at Owner's discretion in the future."*

---

## Conflict Table (for Human Ruling)

| Conflict ID | Conflict (short) | Source A (file + section) | Source B (file + section) | Impacted sections | Proposed Authority | Human ruling |
|---|---|---|---|---|---|---|
| C-1 | Generator capacity (kW) not specified in RFP or Addendum 03; only minimum load list provided | Addendum 03 §1.15 (critical loads defined) | DEL-02-04 (Mechanical Concept — generator sizing TBD) | R-05; T-02; EX-01 | Mechanical Concept (DEL-02-04) to determine capacity; Electrical brief references that assumption | TBD |
| C-2 | Bay door secondary opening: generator-powered vs. manual — brief must state a choice | Addendum 03 §1.15 ("either by backup generation power or manually opening") | Design-Builder choice | R-05; T-04 | Design-Builder team decision; both satisfy requirement | TBD |
| C-3 | Building controls architecture (centralized BACnet/Modbus vs. distributed) not specified by RFP | RFP OSR §10.4 (coordination with mechanical) | Team design decision | T-03; EX-02 | Team choice with consideration of Owner IT support capacity | TBD |

---

## Notes

- Guidance is based on direct reading of RFP OSR §§10.4, 10.5, 10.6, 10.3.9, 12.3, 12.4 (pp. 41–44) and Addendum 03 §§1.6, 1.7, 1.15, 1.17 (pp. 3–4). All guidance reflects these sources.
- **ASSUMPTION:** Design brief is a narrative document (not a drawing package). Author is Electrical Engineer with peer review by Lead Architect/Design Manager.
- **Location TBD:** Specific IES publication edition, Canadian Electrical Code edition applicable in Alberta, and NFPA 72 edition require access to current standards for exact citation.
- **Coordination:** This brief's production depends on concurrent/near-concurrent work on DEL-02-05 (Electrical/IT Concept Narrative) and DEL-02-04 (Mechanical Concept for generator sizing) to ensure mutual consistency in design rationale.
