# Guidance: DEL-02-02 — Firehall Apparatus Bays & Support Spaces

**Enrichment Status:** Pass 3 semantic lensing complete (2026-02-17). Rationale for post-disaster exemption, contamination-gradient zoning, and compressed air system architecture elaborated; trade-offs clarified.

---

## Purpose

This deliverable exists to demonstrate — at the proposal stage — that the Design-Builder understands and can satisfy the operational requirements of the Penhold Fire Department within the integrated Public Services Building.

The apparatus bays are the operational core of the Fire Department wing. The quality, layout, and coordination of the bay program directly determines whether the Fire Department can respond effectively to emergencies. This deliverable (DEL-02-02) captures the firehall-specific layout and systems concept that:

- Demonstrates apparatus accommodation (Type 1 engines, Type 1 aerial apparatus) with correct clear heights and drive-through geometry;
- Shows a coherent decontamination and gear management workflow from apparatus to locker to shower to office;
- Provides an integrated bay services concept (compressed air, electrical, exhaust mitigation, display system) that will be elaborated in detailed design;
- Supports OBJ-002: operationally functional Fire Department facilities.

Source: OSR §10.2; Decomposition FINAL v1.0 PHASE7, OBJ-002; RFP §7.1.1–§7.1.2.

---

## Principles

### 1. Operational Sequence as Layout Driver

The layout of the firehall wing should trace the operational sequence from apparatus arrival/departure through decontamination to gear storage to rest/office spaces. This workflow — often called the "contamination gradient" — separates dirty (apparatus) zones from clean (office/shared) zones. The decontamination area acts as the transition zone.

**Rationale:** Volunteer firefighters move from apparatus bay → decon → gear lockers → shared spaces. A layout that requires crossing contamination zones increases exposure risk and reduces operational efficiency.

Source: OSR §10.2 (decon area must include access to office/shared areas); SOW-0205. **ASSUMPTION:** Contamination-gradient planning principle is industry-standard firehall design practice; specific protocol not explicitly stated in OSR but consistent with requirements.

### 2. Drive-Through Configuration

All four apparatus bays must be drive-through (separate front and rear overhead doors). This allows apparatus to exit facing forward without reversing, which is critical for emergency response times.

Source: OSR §10.2; SOW-0202 — "drive-through apparatus bays."

### 3. Bay Services Completeness per Bay

Each bay must be self-sufficient with electrical, compressed air, and dual exhaust mitigation. The design should not assume apparatus will always park in a specific bay. Equipment standardization (uniform hook-up locations bay to bay) reduces response friction.

Source: OSR §10.2; SOW-0203. **ASSUMPTION:** Uniform placement of services within each bay is good practice for fire station design; specific position not mandated beyond "in each apparatus bay."

### 4. Exhaust Mitigation — Two per Bay

The requirement for two exhaust mitigation connections per bay (OSR §10.2; SOW-0203) combined with the direct exhaust ventilation requirement (Addendum 03 §1.12) for two apparatus per bay implies the design should plan for simultaneous occupancy of two apparatus in each bay. Coordinate with DEL-02-05 for the direct capture system (e.g., hose-reel exhaust extraction or rail-based system).

**ASSUMPTION:** "Two exhaust mitigation connections" refers to vehicle tailpipe capture connections (one per apparatus position per bay), consistent with direct exhaust capture system practice. Not defined further in OSR.

### 5. Gear Locker Room — Adequate Circulation, Not Just Locker Count

The Addendum 03 §1.21 sizing guidance for the bunker gear locker room ("should have 40 bunker gear lockers and thus should be sized to fit 40 lockers with room for firefighters to get in and out") emphasizes functional circulation, not just net area. A minimum target of 350–550 sf (Duty Gear Room range, Addendum 03 §1.21) is reasonable. The layout should allow two firefighters to don gear simultaneously without interference.

Source: Addendum 03 §1.13, §1.21; SOW-0206. **ASSUMPTION:** Simultaneous donning for multiple personnel is an operational expectation for a volunteer department with 40 personnel; not explicitly stated but implied by sizing guidance.

### 6. Display System — Simplicity and Reliability

The fire apparatus bay display system should be straightforward: a wall-mounted TV/monitor in the bay closest to the office area, with wired network connectivity for a laptop. The OSR states: "It is intended the laptop would receive dispatching data and display the data on the mounted display" (OSR §10.6). Overly complex AV systems are not appropriate for a volunteer department environment.

Source: OSR §10.6; SOW-0225.

### 7. SCBA Room — Future Equipment Sizing

The SCBA/cascade room at 150–200 sf (Addendum 03 §1.21) must be sized for the compressor, cascade cylinders, and fill station equipment typical for a volunteer department. SCBA equipment is FF&E (excluded from base construction per Addendum 03 §1.18). The room should nonetheless be designed for expected equipment clearances, electrical load, and ventilation requirements.

**ASSUMPTION:** SCBA cascade system sizing for a 40-person volunteer department is in the range of a 4–6 cylinder cascade with a high-pressure compressor; room design should accommodate typical municipal fire department equipment. Confirm with Owner during detailed design.

---

## Considerations

### Coordination with Other Deliverables

| Interface | Topic | Deliverable |
|---|---|---|
| Overhead doors | 16'×16' specification, door hardware, secondary mechanism | DEL-02-04 |
| Direct exhaust ventilation mechanical system | Two apparatus per bay, design and equipment | DEL-02-05 |
| Plumbing | Bay sumps, decon showers, water fill station supply | DEL-02-05 |
| Electrical in bays | Receptacles, compressed air outlets, display wiring | DEL-02-06 |
| IT/data connectivity | Display system network, PA in firehall wing | DEL-02-06 |
| Generator/backup power | Secondary door-opening on generator | DEL-02-07 |
| Structural bay clearances | Roof height for 16 ft door + structural depth overhead | DEL-02-04 |

### Volunteer Department Context

The Penhold Fire Department is a volunteer department with current 40 personnel and future maximum of 50 (OSR §10.3.5). Key implications:

- Apparatus bays may sit unoccupied for extended periods between calls; design must accommodate standing equipment reliably (floor drains, climate, battery maintenance).
- Gear donning must be fast; locker room layout should prioritize egress speed.
- Decon facilities serve a dual purpose: post-incident decon and routine equipment maintenance.
- Staff are not full-time facility managers; systems must be simple to operate and maintain.

Source: OSR §10.3.5; OSR §10.3.4.

### Bay Sump Sizing

The Addendum 03 §1.8 confirms all bays require sumps for snow melt and minor washing. Sump sizing should account for snow accumulation from large apparatus (Type 1 engines, aerial ladders bring significant snow/ice accumulation in Alberta winters). Coordinate drain sizing with DEL-02-05.

### Compressed Air System Architecture

The source documents reference both "compressed air" for apparatus bays (REQ-0202-03; OSR §10.2) and a "compressed air compressor room" (REQ-0202-16) alongside the "SCBA/cascade room" (REQ-0202-11). The relationship between these systems requires careful clarification during detailed design:

**System Types and Characteristics:**
- **Bay compressed air (shop air):** Used for tire inflation, pneumatic tools, equipment operation during apparatus maintenance. Typically 80–100 psi, standard compressor quality, no breathing-air certification required.
- **SCBA/breathing-air system:** High-pressure (3,000–4,500 psi), breathing-air grade (NFPA 1989 certified), used for cascade fill system and SCBA equipment servicing. Requires specialized filtration, desiccation, and testing protocols.

**Design Decision — One or Two Compressor Rooms?**
The available sources do not explicitly state whether:
- **Option A (integrated):** One compressor room houses both systems (shop-air compressor for bays + breathing-air compressor for SCBA cascade), physically separated or served by the same equipment with dual feed lines.
- **Option B (separate):** Two separate compressor rooms — one for shop air (bay services), one for breathing air (SCBA cascade).

**MEP Lead Determination:**
The MEP lead shall decide during detailed design based on:
1. **Operational efficiency:** Can shop air and breathing air be safely distributed from adjacent/separate equipment within one room, or should they be completely segregated?
2. **Maintenance access:** Which configuration provides better access for equipment servicing and hose connection?
3. **Cost and footprint:** Combined room vs. separate rooms trade-off.

**Pending Clarifications [Lensing: E-002, A-002]:**
- **Air quality grade for bay compressed air:** Confirm whether bay compressed air is shop-air grade or breathing-air grade.
- **Pressure and volume specification:** Bay services compressed air — specify pressure (typical 80–100 psi for shop air), volume (cubic feet per minute), and connection type for bay connections.
- **Distribution routing:** Confirm whether ceiling-drop or wall-mount is preferred for bay compressed air distribution.

Source: Specification REQ-0202-03, REQ-0202-11, REQ-0202-16; Datasheet Construction table.

### Contamination-Gradient Zoning

The decontamination area is a critical operational feature that manages contamination risk for personnel. The firehall layout should be organized as a **contamination-gradient sequence:**

1. **Dirty zone** (apparatus bays) — where apparatus and personnel are exposed to diesel exhaust, smoke, fire residue, and environmental contaminants.
2. **Decontamination zone** (decon room, showers) — transitional area where gross decontamination occurs before entry to clean spaces.
3. **Gear transition zone** (bunker gear locker room) — where personnel don clean gear or store used gear pending decon and washing.
4. **Clean zone** (office, shared spaces, kitchen) — administrative and rest areas where personnel should not bring contaminated gear or equipment.

**Layout Implication:** The decon area must be positioned and designed so personnel moving from apparatus bays to office/shared areas are required to pass through decontamination facilities. This is an **operational flow requirement**, not just a space-provision requirement. The layout should make the contamination-gradient path the natural operational sequence.

**Sources:** OSR §10.2 requires decon area to include "access to office/shared areas" — this requirement implies a separation/transition design. Guidance Principle 1 elaborates the operational sequence. **ASSUMPTION:** Contamination-gradient zoning is an industry-standard firehall design principle; not explicitly mandated by ABC or OSR but consistent with firehall best practices and operational safety expectations.

### Generator — Bay Door Secondary Opening

Addendum 03 §1.15 states: "Bay doors require secondary opening mechanisms (either by backup generation power or manually opening)." This means the bay door operators must either (a) be on the emergency power circuit, or (b) have a manual release/chain. Coordinate resolution with DEL-02-07.

---

## Trade-offs

### Trade-off 1: Bay Count vs. Bay Depth

**Tension:** Four drive-through bays for Type 1 engines and aerial apparatus require significant building footprint. Future apparatus growth (4 large + up to 5 small, per OSR §10.3.5) may make some bays feel constrained.

**Resolution:** The OSR sets 4 bays as the required count (SOW-0202). The design should prioritize adequate depth for the longest current apparatus (aerial ladder) rather than adding a fifth bay. The 2,000–2,200 sf per bay sizing (Addendum 03 §1.21) reflects this.

**Rationale:** The owner has set a clear program; Design-Builder should not reduce bay count but may propose a bay layout that permits efficient future apparatus addition.

### Trade-off 2: Contamination Zoning vs. Building Compactness

**Tension:** Strict contamination-gradient zoning (apparatus → decon → clean) increases corridor length and building footprint compared to a compact, undifferentiated layout.

**Resolution:** The contamination gradient should be maintained as a design principle because OSR §10.2 and SOW-0205 explicitly require the decon area to include access to office/shared areas (implying separation between dirty and clean zones). Some footprint increase is acceptable and expected.

**Rationale:** Long-term health and safety of personnel and reduced contamination risk outweigh marginal compactness benefits.

### Trade-off 3: Exhaust Mitigation System Type

**Tension:** Direct capture systems (hose-reel or rail-based) have higher capital cost than general dilution ventilation but provide better source control for diesel particulate.

**Resolution:** Addendum 03 §1.12 and OSR §11.1.1 explicitly require "direct exhaust ventilation" — general dilution alone does not satisfy this requirement. System type selection (hose-reel vs. rail) is a DEL-02-05 decision.

**Rationale:** The Owner has resolved this trade-off by requiring direct exhaust; the DB's scope is to implement it effectively.

**Terminology Clarification [Lensing: F-001]:**

The Specification contains two related but distinct requirements:

- **REQ-0202-03: "Vehicle exhaust mitigation connections"** — refers to the physical connection points (typically two per bay) where exhaust hoses from apparatus tailpipes can be attached or where exhaust capture ductwork is located. These are **bay-level infrastructure** that DEL-02-02 must show on layout drawings.

- **REQ-0202-04: "Direct exhaust ventilation"** — refers to the **mechanical system design** that captures and exhausts diesel fumes from apparatus bays (sized for two apparatus per bay operation). This is a **DEL-02-05 scope item**.

**Integrated System Relationship:** These two requirements describe parts of one integrated system:
- DEL-02-02 specifies and locates the **bay-level source-capture connections** (two points per bay where hoses or ducts attach to apparatus).
- DEL-02-05 designs the **mechanical exhaust ventilation system** that pulls exhaust from those connections, treats it (if applicable), and exhausts it safely outdoors.

The MEP lead should confirm this scope allocation and document the connection points on a coordination drawing (e.g., "DEL-02-02 shows exhaust connection locations; DEL-02-05 provides mechanical system design to service those locations").

### Trade-off 4: Post-Disaster Importance Category Exemption

**Tension:** OSR §10.3.5 states the AHJ intends to exempt the firehall from post-disaster importance category because it is not the sole emergency-capable structure in the area. This exemption reduces structural design requirements (seismic category, importance factor) and potentially reduces cost, but also reduces the building's resilience.

**Resolution:** The AHJ ruling governs. The Design-Builder should design to the exempted classification unless/until the AHJ formally reverses this intent.

**Design Implications [Lensing: C-002]:**
- **Structural design category:** Post-disaster classification exemption means the firehall wing is designed per standard occupancy category (e.g., Group F2, standard seismic design category) rather than post-disaster seismic importance category.
- **Seismic importance factor:** Exempted from heightened seismic design requirements that would otherwise apply to emergency-critical facilities.
- **Cost impact:** Exemption reduces seismic restraint costs, foundation design complexity, and structural redundancy costs.
- **Operational risk consideration:** If the exemption is later reversed (e.g., due to changed community planning or AHJ policy), the facility would need retrofit seismic upgrades. Confirm AHJ exemption ruling in writing before detailed design.
- **Owner awareness:** Document this exemption and its implications in design narrative and design development briefing to Owner (Penhold Fire Department) so they understand structural resilience assumptions if operational status changes.

The implications of this exemption versus full post-disaster classification should be documented for the Owner's awareness. Confirm AHJ ruling and document rationale during detailed design.

---

## Examples

### Room Size Reference (Addendum 03 §1.21 Table)

The following approximate sizes are provided directly in Addendum 03 §1.21 and are the primary sizing reference for proposal-stage layout. These are guidance, not hard limits.

| Room | Approximate Size Range (sf) |
|---|---|
| Apparatus Bays | 2,000–2,200 (each) |
| Fire Gear Storage | 200–350 |
| Fire EMS Storage | 50–70 |
| Duty Gear Room | 350–550 |
| Decontamination Room | 150–200 |
| Decontamination Shower/WR | 50–60 × 2 |
| SCBA Room | 150–200 |
| Compressor Room | 100–150 |

Source: Addendum 03 §1.21.

### Functional Program (Appendix B) — Apparatus Bay Equipment Notes

The Functional Program (Appendix B) identifies for Apparatus Bay 1:
- 120V/20A drops from ceiling
- 2 vehicle exhaust fume removal systems
- Compressed air lines dropped from ceiling
- LED lighting
- Marked for Type 1 engines; OH Doors 16'H × 16'W

Apparatus Bay 2/3/4 shared similar requirements with a note: "4 bays in total; OH doors 16'H × 16'W."

Source: Functional Program Appendix B (page 46 of RFP).

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CF-0202-01 | Bay count in Functional Program: Bay 1 is listed separately from Bays 2/3/4 (grouped), suggesting potentially different configurations. Bay 1 may have enhanced display/connectivity. | Functional Program Appendix B (page 46) — Bay 1 row vs. Bay 2/3/4 row | OSR §10.2; SOW-0202 — "four apparatus bays" stated uniformly | REQ-0202-01; REQ-0202-14 | PROPOSAL: Treat all four bays as equivalent for services; Bay 1 (closest to office) gets display system per OSR §10.6. | TBD |
| CF-0202-02 | Duty Gear Room vs. Bunker Gear Locker Room sizing: Addendum 03 §1.21 provides "Duty Gear Room 350–550 sf" and "Fire Gear Storage 200–350 sf" as separate entries, but it is unclear if the 40-locker room maps to one or both of these categories. This also creates a terminology inconsistency: documents use "Duty Gear Room," "bunker gear locker room," and "fire gear storage" with overlapping meaning. [Lensing: E-001, B-005] | Addendum 03 §1.21 (room table) — Duty Gear Room 350–550 sf | Addendum 03 §1.13 — "40 bunker gear lockers" with no explicit sf | REQ-0202-09; Datasheet Attributes; all documents (terminology normalization) | PROPOSAL: Map Duty Gear Room (350–550 sf) as the bunker gear locker room (40 lockers); Fire Gear Storage (200–350 sf) as a separate gear equipment storage room. Standardize terminology: use "Duty Gear Room" for the 40-locker room and "Fire Gear Storage" for the separate storage space across all documents. | TBD |
| CF-0202-03 | Exhaust terminology: REQ-0202-03 uses "vehicle exhaust mitigation connections" (two per bay) while REQ-0202-04 uses "direct exhaust ventilation" (sized for two apparatus per bay). It is unclear if these describe one integrated system or two separate systems. [Lensing: F-001] | Specification REQ-0202-03 — "vehicle exhaust mitigation connections" | Specification REQ-0202-04 — "direct exhaust ventilation"; Addendum 03 §1.12 | REQ-0202-03; REQ-0202-04; Guidance Trade-off 3; DEL-02-05 coordination | PROPOSAL: These describe one integrated system — bay-level source-capture connections (REQ-0202-03) fed by a direct exhaust ventilation system (REQ-0202-04). MEP lead to confirm. | TBD |
