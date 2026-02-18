# Guidance: DEL-02-06 Electrical Power, Lighting, IT/Telecom & PA

## Purpose

This deliverable exists to define the electrical power, lighting, IT/telecommunications, and PA systems for the Main Public Services Building (PSB). These systems are foundational to the operational functionality of both the Fire Department and Public Works functions within the building.

Key reasons this deliverable is required:
- The OSR explicitly defines performance requirements for electrical (§10.4), lighting (§10.5), and IT/telecom including PA (§10.6), which must be addressed in the proposal design package.
- The meeting room must support 15 concurrent Emergency Management internet access points — a critical operational requirement tied to OBJ-002 (Fire Dept operational functionality).
- The Fire Department requires a dispatch display system in the apparatus bay area to receive and display emergency dispatching data.
- The building must operate reliably for 50 years; electrical and IT infrastructure choices made at this stage have long lifecycle implications.

*(Source: OSR §10.4, §10.5, §10.6; Decomposition FINAL v1.0, OBJ-001, OBJ-002)*

---

## Principles

### P-01: Current Needs Plus Future Flexibility
The electrical distribution design should not merely satisfy today's loads. The OSR explicitly requires future flexibility (OSR §10.4). This means:
- Panel capacity with appropriate spare circuits/capacity for future additions (ASSUMPTION: spare capacity recommended; quantum not specified in OSR)
- Conduit and rough-in provisions where future loads are plausible
- Modular IT/data infrastructure that can be expanded as needs evolve

### P-02: IES-Compliant Lighting as the Baseline
The IES standard (referenced in OSR §10.5) establishes illuminance targets by task type. For a combined Fire Hall and Public Works facility, different zones will have different IES target categories:
- Office/shared spaces: general office illuminance targets (ASSUMPTION: IES category for office-type spaces)
- Apparatus bays: higher illuminance for maintenance/task activities on equipment (ASSUMPTION: IES Recommended Practice for Lighting of Fire Stations, or equivalent task-based targets)
- Corridors, washrooms: lower illuminance per IES zoning

ASSUMPTION: The Design-Builder's Electrical Engineer will confirm applicable IES target footcandle levels per space type during design development.

### P-03: LED is Non-Negotiable
OSR §10.5 specifies energy-efficient LEDs. This is not a choice but a baseline requirement. LED selection should prioritize:
- Long lamp life to minimize maintenance burden over the 50-year building life
- Colour rendering appropriate for task environments (ASSUMPTION: CRI 80+ for general spaces; higher for detailed inspection areas — now reflected in Specification R-06 per C-004)
- Dimmable capability where appropriate for meeting room / multi-use spaces (ASSUMPTION — not explicitly required by OSR, but merit-based rationale provided below)

**Dimming Capability Rationale (D-003):** The meeting room serves a dual function as an EM command room (Consideration C-05). During extended EM operations, lighting conditions may need to shift between: (a) full illumination for general meetings and training, (b) reduced illumination for extended screen-based command room operations where overhead glare on monitors degrades readability and video conferencing comfort, and (c) presentation-mode lighting for projector or screen-based presentations. Dimmable fixtures in the meeting room/multi-use spaces would provide this operational flexibility at minimal incremental cost for LED drivers capable of dimming. This is recommended as a design consideration but not mandated — the Design-Builder should evaluate whether the dual-use operational merit justifies the cost of dimmable drivers.

### P-04: Emergency Lighting as a Code Floor, Not a Design Ceiling
OSR §10.5 requires emergency exit lights with internal battery backup above personal doors per code. The code requirement is the minimum. The Design-Builder should consider whether additional emergency lighting (e.g., emergency battery-backed task lighting in apparatus bays) is appropriate for operational continuity, noting this must be coordinated with the generator design in DEL-02-07.

ASSUMPTION: Generator-backed circuits will be the primary means of extended emergency lighting; battery backup above personal doors is a secondary/code-minimum layer.

### P-05: IT Infrastructure as Operational Infrastructure
For a Fire Department, IT infrastructure is not administrative — it is operational. The meeting room's EM workstation requirement (15 concurrent access points) means the IT design must treat network capacity and reliability as mission-critical at that location. Recommendations:
- Dedicated switch or VLAN for EM workstations in the meeting room to ensure bandwidth
- Consider PoE (Power over Ethernet) infrastructure to simplify workstation power management — **Clarification (E-003):** PoE is a recommendation within Guidance only; it is not reflected in Specification R-12 as a requirement. If the Design-Builder determines PoE is warranted for workstation power management, this should be elevated to a Specification requirement at that time. Until then, it remains a design consideration.
- Cable routing from IT room to meeting room should follow a resilient path

*(Source: OSR §10.6; SOW-0208; SOW-0224 — IT design approach is ASSUMPTION/best practice)*

### P-06: PA System — Simple and Reliable
The OSR calls for a "simple" PA system (OSR §10.6). This language indicates the Owner is not seeking a complex integrated AV system. Priorities:
- Full coverage of the main building (all occupied areas audible)
- Reliability over sophistication
- Clear intelligibility (voice paging is primary use case — ASSUMPTION)

---

## Considerations

### C-01: Generator Integration Boundary
The boundary between this deliverable (DEL-02-06) and the Emergency Power deliverable (DEL-02-07) must be clearly defined. This deliverable covers the normal distribution system. DEL-02-07 covers generator sizing, ATS, and the essential loads circuit. The Design-Builder must ensure:
- Normal distribution design accounts for where the ATS will tie in
- Essential loads circuits are identified in coordination with DEL-02-07
- The PA system, meeting room IT, apparatus bay display, and general lighting are appropriately classified as essential or non-essential loads per R-17

**Essential vs. Non-Essential Load Classification Rationale (B-003, B-004):** For a fire department operations building, the classification of loads as essential (generator-backed) vs. non-essential has direct safety implications. The following discernment framework is recommended (ASSUMPTION per B-004 — no source document prescribes this framework):

- **Essential load candidates:**
  - PA system (required for emergency paging and apparatus notifications during power outages)
  - Apparatus bay display system (dispatching and emergency information must be available during emergencies)
  - Emergency lighting (code-minimum battery backup above personal doors, plus generator-backed general egress lighting in main corridors/exits)
  - Minimum IT infrastructure to maintain EM command room capability (meeting room display, network connectivity, workstation power)

- **Non-essential load candidates:**
  - General office lighting (except exit lighting)
  - Non-critical receptacles in non-operational spaces
  - Kitchen/breakroom loads
  - Optional/convenience loads

- **Decision factors:**
  - (a) Is the system required during an emergency event that may coincide with a power outage?
  - (b) Does the CEC or ABC mandate generator backup for this load category?
  - (c) What is the operational impact on fire department operations if this load is unavailable during the generator start-up interval (typically 10-30 seconds)?
  - (d) What is the safety-critical implication of losing this load during an extended outage?

The final classification shall be documented in Specification R-17, coordinated with DEL-02-07 load sizing, and confirmed in the electrical design basis narrative.

*(Source: Decomposition DEL-02-07; SOW-0222; B-003, B-004)*

### C-02: Apparatus Bay Electrical — Coordination with DEL-02-02
SOW-0203 is shared between DEL-02-02 (Firehall Functional Areas) and DEL-02-06 (Electrical). The electrical outlets/services within apparatus bays are within DEL-02-06 scope, but the compressed air and exhaust mitigation are in DEL-02-02. Design-Builder must confirm service outlet locations in coordination with apparatus bay layout.

*(Source: Decomposition SOW-0203 note)*

### C-03: Exterior Receptacles in a Municipal Operations Environment
The main building will be accessed by volunteer firefighters in all weather conditions. Exterior receptacle locations, GFCI protection requirements, and weatherproof cover ratings must reflect the Alberta climate (freeze-thaw cycling, wet/icy conditions). ASSUMPTION: tamper-resistant weatherproof covers and GFCI protection are expected as minimum practice.

### C-04: Apparatus Bay Display System — Minimum Viable vs. Future-Ready
OSR §10.6 describes the apparatus bay display as potentially "as simple as a mounted TV with hardware to connect to a laptop." This sets a low minimum bar. The Design-Builder should consider:
- Wall-mount structural support in the bay closest to the office area
- Power receptacle and data outlet at the display location
- Whether conduit for future network integration is worthwhile at minimal cost
The minimum compliant solution is a wall-mounted TV with HDMI/display connectivity.

*(Source: OSR §10.6)*

### C-05: Meeting Room — Dual Use as EM Command Room
The meeting room is sized for 40 people but must also function as an Emergency Management command room with 15 simultaneous internet-connected workstations. The electrical and IT design must support:
- Adequate power outlets at workstation positions (not just perimeter power)
- 15 data connections accessible at table or floor box locations (ASSUMPTION — floor boxes or furniture raceways implied)
- Lighting appropriate for both general meeting use and extended command room operations

*(Source: OSR §10.2; §10.6; SOW-0208)*

### C-07: Fire Alarm System Scope Boundary
**Note (X-001):** This deliverable covers electrical power distribution, lighting, IT/telecom, and PA systems but explicitly excludes fire alarm system design and integration. For an electrical deliverable in a fire station, the exclusion of fire alarm scope is notable and requires explicit acknowledgment.

**Scope Boundary:** Fire alarm system design, fire alarm power supply, and fire alarm circuit requirements (if any) are OUT OF SCOPE for DEL-02-06. The fire alarm system may be covered under another deliverable — possible candidates include:
- DEL-02-05 (Mechanical, Plumbing, Ventilation & Exhaust) — if fire alarm is grouped with building systems
- A dedicated fire protection/life safety deliverable (TBD — confirm)
- Owner-furnished systems (if fire alarm is excluded from Design-Builder scope)

**Coordination Note:** If fire alarm power supply, dedicated conduit, or circuit requirements exist in a separate deliverable, they may impose coordination requirements on this deliverable's electrical distribution design (e.g., dedicated fire alarm panel location, power backup for fire alarm circuits). The Design-Builder should confirm the fire alarm ownership/scope boundary with the Owner and project team during pre-award design meetings.

ASSUMPTION — fire alarm system is out of scope for DEL-02-06. The scope boundary and coordination requirements should be confirmed during design development.

*(Source: entire document set scanned; no fire alarm reference found in DEL-02-06 scope — flagged per X-001)*

### C-06: Fixture Height in Bay Areas
OSR §10.5 explicitly notes fixture heights must be adjusted to avoid interference with machinery. In fire apparatus bays accommodating Type 1 aerial apparatus, ceiling clearances will be significant. Fixture mounting heights, aiming angles, and guard/protection requirements must be confirmed with the architectural/structural team.

*(Source: OSR §10.5; SOW-0202)*

---

## Trade-offs

### T-01: Lighting Quality vs. Energy Cost — Lifecycle Cost Optimization (A-005)
**Tension:** Higher-CRI LED fixtures or higher-capacity IT infrastructure provide better performance but may have higher upfront capital cost.
**Resolution:** OSR §10.5 mandates IES compliance and energy-efficient LEDs. Within those constraints, the Design-Builder should optimize for lifecycle cost rather than lowest first cost, given the 50-year building life requirement (OSR §10.2; SOW-0201).
**Rationale:** A fixture that requires replacement in 10 years costs more over the building lifecycle than a slightly more expensive fixture rated for 25+ years. Similarly, a structured cabling infrastructure designed for future expansion costs less per lifecycle than upgrading/replacing infrastructure in 15 years.

**Lifecycle Cost Principle (A-005, T-01):** For a facility designed for a 50-year operational life, lifecycle cost optimization is the preferred value driver for fixture and infrastructure selection decisions. This means evaluating options not only on initial capital cost but on total cost of ownership including:
- Energy consumption over building life (LEDs with better lumens-per-watt and lower maintenance)
- Lamp/component replacement frequency and labor cost (long-life LED fixtures reduce maintenance cycles)
- Operational availability (higher-quality fixtures reduce emergency replacement/downtime)
- Future-readiness (conduit, cabling, and panel capacity for future expansion reduce lifecycle replacement costs)
- Disposal/environmental costs over full building life

ASSUMPTION — this principle is inferred from the 50-year design life requirement and is not explicitly stated in the OSR, but it is consistent with the intent of a long-lived public facility and should guide the Design-Builder's value engineering decisions.

### T-02: IT Infrastructure Complexity vs. Simplicity
**Tension:** Fully managed, enterprise-grade network infrastructure vs. simple passive infrastructure.
**Resolution:** OSR §10.6 calls for IT/data "compatibility" — not a managed system. The Owner's expectation is that the building infrastructure supports connectivity; the network management layer is likely an Owner-furnished function.
**Rationale:** Design-Builder should provide structured cabling infrastructure (passive) to a central IT room, sized to support future expansion. Active network equipment is likely Owner-furnished and operated. ASSUMPTION — confirm scope boundary with Owner during design.

### T-03: PA System Scope vs. Adequacy
**Tension:** "Simple" PA system vs. ensuring all areas including large bays are adequately covered.
**Resolution:** The Design-Builder should take "simple" to mean straightforward in architecture (head-end amplifier, passive speaker distribution), not compromised in coverage. Bay areas with high ambient noise levels from apparatus will require appropriate speaker spacing/power to ensure intelligibility.
**Rationale:** PA system failures in an emergency operations context have safety implications. The system must be simple to operate but acoustically adequate. ASSUMPTION.

---

## Examples

### Example: Apparatus Bay Electrical Service Points
The OSR states that each apparatus bay will have electrical services. A typical fire apparatus bay service point layout includes receptacles at the bay front (near overhead doors) and along bay side walls for apparatus maintenance and charging needs, plus a dedicated circuit for the overhead door opener. No specific circuit count or receptacle density is prescribed in OSR §10.4 beyond requiring coordination with mechanical systems.
*(Source: OSR §10.4, §10.2 — layout specifics are ASSUMPTION based on typical firehall practice)*

### Example: 15-Workstation Meeting Room Layout
A 15-workstation emergency management layout in a 40-person meeting room would typically require:
- Floor boxes or perimeter raceways at table positions (power + data per workstation)
- A dedicated patch panel or switch connection in the room or adjacent IT closet
- 15 RJ45 data ports minimum with cabling run to the building IT room
Exact layout is ASSUMPTION — confirmed by functional program details not yet accessed.
*(Source: OSR §10.6; SOW-0208 — specifics are ASSUMPTION)*

---

## Conflict Table (for human ruling)

No unresolved source conflicts identified at P1/P2 stage. Potential boundary ambiguities are noted as Considerations above (C-01: generator boundary; C-02: apparatus bay electrical boundary with DEL-02-02) and should be confirmed during design development rather than treated as conflicts.
