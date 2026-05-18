# Specification: DEL-02-06 Electrical Power, Lighting, IT/Telecom & PA

## Scope

### In Scope
This deliverable covers electrical power distribution, receptacle design, lighting design, IT/data/telecommunications infrastructure, PA system design, apparatus bay display system, and meeting room emergency management workstation connectivity for the **Main Public Services Building (PSB)** only.

Specific scope items addressed:
- SOW-0203 (electrical aspects): Electrical services in each fire apparatus bay
- SOW-0208 (IT/power aspects): Meeting room power/internet for 15 EM workstations
- SOW-0224: Building-wide IT/data and telecommunications infrastructure
- SOW-0225: Apparatus bay wall-mounted display system
- SOW-0226: PA system throughout main building
- SOW-0227: Electrical systems, receptacles (interior and exterior), with future flexibility
- SOW-0228: Lighting to IES recommendations using energy-efficient LEDs with emergency exit lighting

*(Source: Decomposition FINAL v1.0, PKG-002 Deliverables Table)*

### Out of Scope
- Backup generator design and emergency power distribution (covered by DEL-02-07)
- Site/utility service tie-ins and external electrical service (covered by DEL-03-04)
- Cold Storage Building electrical and ventilation (covered by DEL-04-04)
- PA system in cold storage building or other ancillary buildings — explicitly excluded per OSR §10.6 p.43
- Optional yard lighting (covered by DEL-05-02 — Optional Priced Item)
- Optional access control system (covered by DEL-05-03 — Optional Priced Item)
- Optional security and camera system (covered by DEL-05-04 — Optional Priced Item)
- Compressed air systems in apparatus bays (covered by DEL-02-02)
- Town branding signage (Optional Priced Item — DEL-05-05)

---

## Requirements

### R-01: Electrical Distribution — Current Needs and Future Flexibility
**Requirement:** The Design-Builder shall design electrical systems, including receptacles and grounding, to meet current operational needs and allow for future flexibility.
**Source:** OSR §10.4 (RFP p.42)
**Note:** The Design-Builder is to advise on optimal options considering program, budget, and operational needs.

### R-02: Receptacle Coverage — Interior and Exterior
**Requirement:** Electrical receptacles shall be installed at appropriate locations inside and outside the main building. Exterior receptacles and receptacles in wet locations shall be provided with tamper-resistant weatherproof covers and GFCI (Ground Fault Circuit Interrupter) protection per CEC requirements. Minimum receptacle density or spacing shall comply with CEC requirements for the applicable occupancy classification, or as recommended by the Design-Builder based on professional judgment if CEC minimum is not prescriptive for the specific occupancy type (TBD — confirm CEC spacing rules per E-001).
**Source:** OSR §10.4 (RFP p.42); CEC Part I; Guidance C-03
**Note:** ASSUMPTION (D-001, X-002, E-001) — OSR specifies receptacles "at appropriate locations" without density or spacing criteria. CEC has minimum spacing rules for commercial occupancies. GFCI protection on exterior and wet-location receptacles is mandatory per CEC (X-002 verification gap resolved). Terminology normalized (D-001): "tamper-resistant weatherproof covers and GFCI protection" is the consolidated term for exterior receptacle protection, with GFCI required as code-mandated minimum practice.

### R-03: Mechanical and Door Opener Coordination
**Requirement:** Electrical receptacle and distribution design shall be coordinated with mechanical systems and overhead door openers to ensure compatibility.
**Source:** OSR §10.4 (RFP p.42)

### R-04: Apparatus Bay Electrical Services
**Requirement:** Each of the four fire apparatus bays shall be provided with electrical services.
**Source:** OSR §10.2 (RFP p.36); Decomposition SOW-0203
**Note:** Compressed air and exhaust mitigation are covered under DEL-02-02 and DEL-02-05 respectively.

### R-05: Lighting Standard — IES Recommendations
**Requirement:** Lighting design shall follow IES (Illuminating Engineering Society) recommendations throughout the main building. Specific IES illuminance target values (footcandle levels) shall be identified for each space type, including but not limited to: office areas, apparatus bays, corridors, washrooms, and meeting room.
**Source:** OSR §10.5 (RFP p.42)
**Note:** TBD (B-002) — specific IES footcandle targets per space type are not yet enumerated. The Design-Builder shall consult the IES Lighting Handbook (location TBD) and document applicable illuminance categories during design development. Without numeric targets, compliance verification cannot be evaluated against a defined standard.

### R-06: Energy-Efficient LED Fixtures
**Requirement:** All luminaires shall be energy-efficient LEDs. LED fixtures shall meet the following minimum lighting quality criteria:
- Colour Rendering Index (CRI): minimum 80 for general spaces; TBD for detailed inspection areas (ASSUMPTION: higher CRI may be warranted in apparatus maintenance zones)
- Correlated Colour Temperature (CCT): TBD — Design-Builder to recommend appropriate CCT range per zone type (e.g., 3500K-4000K for offices; 4000K-5000K for task areas; ASSUMPTION per C-004)
**Source:** OSR §10.5 (RFP p.42); Guidance P-03
**Note:** ASSUMPTION (C-004) — OSR mandates energy-efficient LEDs but does not specify CRI or CCT values. Without these parameters, all LED fixtures would technically comply regardless of light quality. Guidance P-03 assumes CRI 80+ for general spaces.

### R-07: Emergency Exit Lighting
**Requirement:** Emergency exit lights shall be provided above personal doors with internal battery backup, as required by code.
**Source:** OSR §10.5 (RFP p.42)

### R-08: Lighting Levels, Fixtures, and Placement — Safe Task Performance
**Requirement:** The Design-Builder shall advise on lighting levels, fixture selection, and placement to ensure safe task performance throughout the facility.
**Source:** OSR §10.5 (RFP p.42)

### R-09: Weatherproof Switches at Person Doors
**Requirement:** Light switches at person doors shall have weatherproof covers, particularly for areas exposed to weather or ancillary building environments.
**Source:** OSR §10.5 (RFP p.42)

### R-09A: Lighting Control Strategy
**Requirement:** The Design-Builder shall specify a lighting control strategy addressing switching zones, occupancy sensors (where appropriate for the space type and operational use), and daylight harvesting potential (where applicable). If detailed lighting control specification is delegated to the Design-Builder's professional recommendation based on energy code compliance and operational needs, this delegation shall be explicitly documented in the design basis narrative with supporting rationale.
**Source:** ASSUMPTION (E-002) — no OSR requirement explicitly addresses lighting controls (R-05 through R-10 are silent on controls). For exhaustive operational verification, the control strategy should be specified or acknowledged as a design decision. Alberta Building Code Section 11 (Energy Efficiency) may mandate minimum lighting control provisions for commercial occupancies; confirmation required during design.

### R-10: Fixture Height — Machinery Clearance
**Requirement:** Fixture heights in bay and operational areas shall be adjusted to avoid interference with machinery, vehicles, and apparatus.
**Source:** OSR §10.5 (RFP p.42)

### R-11: Building-Wide IT/Data Compatibility
**Requirement:** IT/data compatibility (structured cabling or equivalent infrastructure) shall be provided throughout the main structure. Structured cabling infrastructure shall comply with TIA-568 or an equivalent recognized cabling standard (TBD — confirm applicable standard).
**Source:** OSR §10.6 (RFP p.42); SOW-0224
**Note:** ASSUMPTION (F-003) — OSR requires "IT/data compatibility" and "structured cabling or equivalent" but does not reference a specific cabling standard. TIA-568 is the industry-standard reference for commercial building telecommunications cabling. Compliance with a named standard enables verification of cable installation quality.

### R-12: Meeting Room — 15 Concurrent EM Internet Access Points
**Requirement:** The meeting/training room (minimum 40-person capacity) shall provide internet connectivity capable of supporting 15 concurrent access points for Emergency Management workstations simultaneously. The Design-Builder shall specify the connectivity approach: minimum 15 wired RJ45 data ports, or a wireless access point with verified 15-user concurrent capacity, or a combination thereof.
**Source:** OSR §10.6 (RFP p.42); SOW-0208; SOW-0224
**Note:** ASSUMPTION (C-003) — OSR does not specify wired vs. wireless. Procedure Step A-7 references "15 RJ45 data ports or wireless access point with 15-user capacity." The critical operational threshold (15 concurrent connections) must be unambiguously achievable by the chosen approach. Recommend specifying minimum acceptable approach to avoid ambiguity.

### R-13: Apparatus Bay Display System
**Requirement:** A display system shall be mounted on the wall in the fire apparatus bay closest to the office area for the purpose of displaying emergency information. The system shall be capable of connecting a laptop to a mounted display; the laptop receives dispatching data and displays it on the mounted display.
**Source:** OSR §10.6 (RFP p.42); SOW-0225

### R-14: PA System — Main Building Only
**Requirement:** A simple PA (public address) system shall be installed throughout the main PSB building. The PA system is not required in the cold storage building or other ancillary buildings.
**Source:** OSR §10.6 (RFP p.43); SOW-0226
**Note:** Terminology normalized (X-003): "cold storage building or other ancillary buildings" is the standard exclusion term used across all four documents.

### R-15: Code Compliance
**Requirement:** All electrical work shall comply with applicable Alberta codes and standards, including the following mandatory standards: Canadian Electrical Code (CEC), Part I, as adopted in Alberta (binding primary electrical code per A-001); Alberta Building Code (ABC) for emergency lighting and energy efficiency; and any other authority-having-jurisdiction (AHJ) requirements confirmed during the permitting process.
**Source:** RFP §7.1.2 (location TBD for specific clause); OSR §10.3.4; CEC Part I (binding standard)
**Note:** CEC Part I is confirmed as the binding applicable electrical code for Alberta installations (A-001, C-001 — strengthened from assumption to named binding code). The specific CEC edition adopted by Alberta should be confirmed with AHJ during design. Sealed electrical documents required per R-16.

### R-17: Essential vs. Non-Essential Load Classification
**Requirement:** The Design-Builder shall classify each electrical system within this deliverable's scope (PA system, meeting room IT infrastructure, apparatus bay display system, and general lighting circuits) as either essential or non-essential load for the purpose of generator backup coordination with DEL-02-07.
**Source:** Guidance C-01 (generator integration boundary); Decomposition SOW-0222; DEL-02-07 coordination
**Note:** ASSUMPTION (B-003) — no source document currently records this classification, yet it is an essential input for generator sizing and ATS circuit design in DEL-02-07. The classification has safety implications in a fire operations context.

### R-16: Sealed Documents
**Requirement:** All electrical design documents shall be sealed by an Alberta-registered Professional Engineer (Electrical).
**Source:** RFP §7.1.2 (location TBD for specific clause)
**Note:** ASSUMPTION — consistent with standard Alberta Design-Build practice and RFP §7.1.2 general professional sealing requirement.

---

## Standards

| Standard | Applicability | Access Status |
|----------|---------------|---------------|
| IES Lighting Handbook / IES Standards | Lighting design basis — referenced explicitly in OSR §10.5 | Not directly accessible — location TBD |
| Canadian Electrical Code (CEC), Part I | Electrical distribution, wiring, and receptacle installation — ASSUMPTION: likely applicable | Not directly accessible — location TBD |
| Alberta Building Code (ABC) | Emergency exit lighting, code-minimum requirements | Not directly accessible — location TBD |
| CCDC 14-2013 | Design-Build contract form; general obligations | location TBD |
| TIA-568 (or equivalent) | Structured cabling standard for building IT/data infrastructure (ASSUMPTION per F-003) | Not directly accessible — location TBD |
| RFP 2024_004 — OSR §10.4, §10.5, §10.6 | Owner performance requirements for electrical, lighting, IT, and PA | Accessible |

---

## Verification

| Requirement | Verification Approach |
|-------------|----------------------|
| R-01: Electrical distribution — current and future | Design narrative confirms flexibility provisions; engineering review at DD/60%/100% milestones. Verification shall include measurable future-flexibility indicators: (a) percentage of spare circuit capacity in each panel (TBD — recommend minimum 20%; ASSUMPTION per A-003), (b) spare conduit provisions documented on drawings, and (c) spare panel space identified on panel schedule. Future flexibility acceptance criterion: Design must document explicit spare capacity provisions and conditions under which they are deployable. |
| R-02: Interior/exterior receptacles | Receptacle plan reviewed against room/area schedule and exterior elevation drawings. Verification shall confirm: (a) GFCI protection provided on all exterior receptacles and wet-location receptacles per CEC requirements (X-002 — mandatory verification), (b) tamper-resistant weatherproof covers specified at all exterior locations, and (c) receptacle density/spacing meets CEC minimum for applicable occupancy classification or Design-Builder recommendation documented with rationale. Receptacle schedule to include CEC spacing basis reference. |
| R-03: Mechanical/door opener coordination | Coordination matrix or coordination meeting minutes between electrical and mechanical discipline leads |
| R-04: Apparatus bay electrical services | Electrical plan checked to confirm service points in each of the four apparatus bays |
| R-05: Lighting — IES recommendations | Lighting calculation report (photometric study) submitted confirming compliance with IES footcandle targets |
| R-06: LED fixtures | Fixture schedule confirms all luminaires are LED type |
| R-07: Emergency exit lighting | Fixture schedule and electrical plan show emergency exit lights with battery backup above all personal doors |
| R-08: Lighting levels and placement | Photometric study and fixture layout reviewed by Electrical Engineer; Owner review at DD stage |
| R-09: Weatherproof switches | Details and specification confirm weatherproof switch/cover ratings at applicable locations |
| R-10: Fixture height | Fixture mounting heights confirmed on electrical/reflected ceiling plan; checked against equipment clearance envelopes |
| R-11: Building-wide IT/data | Data/telecom plan reviewed for coverage of all occupied areas in main building |
| R-12: 15 concurrent EM access points | Meeting room data infrastructure design demonstrates 15-port capacity; network switch/patch panel schedule confirmed |
| R-13: Apparatus bay display system | Display system design confirmed on electrical/IT plan; connectivity basis (HDMI/network) documented. Verification shall include: (a) minimum display size (TBD — ASSUMPTION per D-004: recommend minimum 55" for readability at apparatus bay viewing distances), (b) minimum resolution (TBD — ASSUMPTION: recommend 1080p minimum), (c) end-to-end functional acceptance test confirming laptop-to-display connection per Procedure Step C-4. Quality acceptance criteria (screen size, resolution) shall be documented in equipment specification sheet. |
| R-14: PA system — main building | PA riser diagram and speaker layout plan cover all main building areas; cold storage building and other ancillary buildings excluded. Verification shall include: (a) measurable intelligibility criterion per F-004 (TBD — recommend Speech Transmission Index (STI) score of 0.50 or greater, or equivalent zone coverage test), (b) speaker layout ensures audible signal in all main building occupied areas including apparatus bays, (c) end-to-end commissioning test per Procedure Step C-4 confirming coverage and intelligibility in all zones. |
| R-09A: Lighting control strategy | Design basis narrative documents lighting control approach (switching zones, occupancy sensors, daylight harvesting); specification or delegation statement confirmed at DD stage with rationale. If energy code compliance is the basis, cite specific ABC energy requirements. |
| R-15: Code compliance | AHJ permit application and inspection records; sealed drawings submitted to building permit authority; conformance with CEC Part I confirmed in design basis narrative. |
| R-16: Sealed documents | Electrical drawings and specifications bear Alberta P.Eng. seal at each milestone submission where sealed documents are expected per C-002 (DD, 60%, and 100% IFC — not only at IFC). Verification: title block review confirms P.Eng. stamp and signature at DD, 60%, and 100% IFC submissions. |
| R-17: Essential/non-essential load classification | Load classification table documented and coordinated with DEL-02-07; confirmed in electrical design basis narrative |

---

## Documentation

### Required Deliverable Artifacts (from _CONTEXT.md Anticipated Artifacts)
1. **Electrical distribution design** — single-line diagram and distribution panel schedule showing service entry, sub-panels, circuit distribution, and load summary
2. **Receptacle plan** — floor plan showing interior and exterior receptacle locations, circuit assignments, and weatherproof designations
3. **Lighting design (IES-compliant LED)** — reflected ceiling plan with fixture schedule, photometric summary, and IES compliance statement
4. **Data/telecom plan** — data outlet layout, backbone cabling routing concept, meeting room EM connectivity detail (15-port capacity)
5. **PA system design** — speaker layout plan, amplifier/head-end location, coverage narrative
6. **Meeting room EM workstations connectivity** — detail drawing or narrative confirming power and internet provisions for 15 concurrent workstations

### Additional Expected Documentation (ASSUMPTION — consistent with RFP §7.1.8 milestone submissions)
- Electrical design basis narrative (assumptions, code basis, load calculations summary)
- Coordination notes with mechanical discipline (DEL-02-05) and generator design (DEL-02-07)
- Apparatus bay display system technical description
