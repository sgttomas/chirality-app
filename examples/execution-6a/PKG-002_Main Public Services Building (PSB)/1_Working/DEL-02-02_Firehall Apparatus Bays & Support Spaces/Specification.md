# Specification: DEL-02-02 — Firehall Apparatus Bays & Support Spaces

**Enrichment Status:** Pass 3 semantic lensing complete (2026-02-17). All warranted items from _SEMANTIC_LENSING.md have been incorporated with provenance or converted to TBD/Conflict Table entries.

---

## Scope

### In Scope

This deliverable covers the design-proposal documentation for the following components of the PSB Firehall wing:

1. **Apparatus bays** — four (4) drive-through bays, including bay layout, dimensional strategy, services integration concept, and floor design.
2. **Bay services** — electrical, compressed air, and vehicle exhaust mitigation connections (two per bay).
3. **Bay exhaust mitigation coordination** — coordinated with DEL-02-05 (Mechanical) for direct exhaust capture design.
4. **Decontamination area** — decon room, shower/washroom, access to gear storage and office areas.
5. **Gear storage spaces** — bunker gear locker room (40 lockers), duty gear room, fire gear storage.
6. **Support rooms** — SCBA/cascade room, compressor room, medical/EMS equipment storage.
7. **Apparatus bay display concept** — wall-mounted display system in the bay closest to office area.

### Out of Scope

- Vehicle exhaust ventilation mechanical system design (detailed design belongs to DEL-02-05).
- Electrical distribution design, receptacle layouts, and PA system (belongs to DEL-02-06).
- Overhead door specification and structural bay clearance (belongs to DEL-02-04).
- Emergency generator and backup power system (belongs to DEL-02-07).
- SCBA equipment procurement (treated as FF&E; not in base construction per Addendum 03 §1.18).
- Public Works bays and support spaces (belongs to DEL-02-03).
- Shared spaces (kitchen, offices, meeting/training room) — belongs to DEL-02-01.

---

## Requirements

### REQ-0202-01: Number and Type of Apparatus Bays

**Shall:** Provide four (4) drive-through apparatus bays suitable for Type 1 engines and Type 1 aerial apparatus.

- Source: OSR §10.2; SOW-0202
- Note: Drive-through configuration (front and rear overhead doors) is required for operational fire response.

### REQ-0202-02: Bay Dimensional Adequacy

**Shall:** Each apparatus bay shall accommodate at minimum one large fire apparatus per bay, with future capacity for two apparatus per bay (four large + four small per OSR §10.3.5).

- Bay area target: 2,000–2,200 sf per bay (source: Functional Program Appendix B; Addendum 03 §1.21).
- Overhead door clear height: minimum 16 feet. (Source: Addendum 03 §1.10; SOW-0215)
- Overhead door size: 16' × 16'. (Source: OSR §10.3.9; SOW-0216)
- Overhead door hardware: "'car wash' grade hardware" per OSR §10.3.9. **Note:** The standard, rating, or performance criteria that constitute "car wash grade" — TBD; specify corrosion resistance rating, material specification, or applicable standard during detailed design. [Lensing: C-004]

### REQ-0202-03: Bay Services — Electrical, Compressed Air, Exhaust Mitigation

**Shall:** Each apparatus bay shall be provided with:
- Electrical service (coordinate with DEL-02-06 for layout)
- Compressed air connection — **Note:** Air quality grade (breathing air vs. shop air), pressure, volume, and connection type for bay connections — TBD. Confirm whether bay compressed air is shop-air grade or breathing-air grade. [Lensing: A-002]
- Two (2) vehicle exhaust mitigation connections per bay — **Note:** "Vehicle exhaust mitigation connections" (this requirement) are related to but may differ from "direct exhaust ventilation" (REQ-0202-04). See Guidance Trade-off 3 and Lensing item F-001 for clarification of the distinction between source-capture connections and ventilation system design.

- Source: OSR §10.2; SOW-0203
- Coordination: DEL-02-06 (Electrical), DEL-02-05 (Exhaust mechanical design)

### REQ-0202-04: Bay Direct Exhaust Ventilation

**Shall:** Direct exhaust ventilation for fire apparatus bays shall be provided, sized to accommodate two apparatus per bay.

- Source: OSR §11.1.1; Addendum 03 §1.12; SOW-0204
- Note: Detailed mechanical design is in DEL-02-05; this deliverable provides the layout coordination and bay-level concept.

### REQ-0202-05: Bay Sumps

**Shall:** Bay sumps shall be provided in all fire apparatus bays to allow for snow melt and minor washing.

- Source: Addendum 03 §1.8; SOW-0214
- **Note:** Sump sizing criteria (capacity, drainage rate, or reference standard) — TBD. Acceptance basis for sump adequacy should be defined during detailed design. Coordinate with DEL-02-05 for drain sizing. [Lensing: A-005]

### REQ-0202-06: Bay Floor Material

**Shall:** Apparatus bay floors shall be concrete, including concrete aprons at overhead door access points.

- Source: OSR §10.3.8; Addendum 03 §1.3; SOW-0217
- **Note:** Floor performance specification (minimum compressive strength, slip resistance rating, chemical resistance for decontamination areas, or reference standard) — TBD. Current description is "sealed concrete; resilient, easily cleaned of mud/dust" (OSR §10.3.8), which does not constitute a performance specification. [Lensing: F-004]

### REQ-0202-07: Overhead Doors — Secondary Opening Mechanism

**Shall:** Apparatus bay overhead doors shall have a secondary opening mechanism (manual or backup generator power) for use when the primary electrical supply is unavailable.

- Source: Addendum 03 §1.15; SOW-0216
- Coordination: DEL-02-07 (Emergency Power) for backup power integration.

### REQ-0202-08: Decontamination Area

**Shall:** Provide a decontamination area including:
- Decontamination room (150–200 sf approximate)
- Washrooms and shower (two decontamination shower/WR units, 50–60 sf each)
- Access to fire gear lockers
- Equipment storage
- Breathing air compressor room
- Medical equipment storage
- Access to office/shared areas
- **Contamination-gradient zoning:** The decontamination area shall be positioned to provide a transition zone between apparatus bays (dirty zone) and office/shared areas (clean zone), maintaining separation between contaminated and clean environments. **ASSUMPTION:** Contamination-gradient zoning is an industry-standard firehall design principle; it is implied by the requirement for decon area to include "access to office/shared areas" but is not explicitly stated as a zoning requirement in the OSR. [Lensing: B-004]

- Source: OSR §10.2; SOW-0205; Functional Program Appendix B; Addendum 03 §1.21
- See also: Guidance, Principle 1 — Operational Sequence as Layout Driver.

### REQ-0202-09: Bunker Gear Lockers

**Shall:** Provide a bunker gear locker room with forty (40) bunker gear lockers, sized to allow firefighters to get in and out (approximate area: 350–550 sf per Duty Gear Room classification in Addendum 03 §1.21).

- Source: Addendum 03 §1.13, §1.21; SOW-0206

### REQ-0202-10: Gear Locker Room Ventilation

**Shall:** The bunker gear locker room shall be ventilated at the room level. Direct ventilation to individual lockers is not required.

- Source: Addendum 03 §1.14

### REQ-0202-11: SCBA / Cascade Room

**Shall:** Provide an SCBA/cascade room of approximately 150–200 sf with provisions for breathing air compressor equipment and SCBA storage/maintenance.

- Source: Functional Program Appendix B; Addendum 03 §1.21; OSR §10.2 (compressor room referenced)
- Note: SCBA equipment procurement is FF&E and is not included in base construction cost.

### REQ-0202-12: Fire EMS Storage (Medical Equipment Storage)

**Shall:** Provide medical/EMS equipment storage of approximately 50–70 sf within or adjacent to the decontamination area.

- Source: Functional Program Appendix B; Addendum 03 §1.21; OSR §10.2; SOW-0205

### REQ-0202-13: Fire Gear Storage

**Shall:** Provide fire gear storage of approximately 200–350 sf (climate controlled per Functional Program).

- Source: Functional Program Appendix B; Addendum 03 §1.21
- **Note:** "Climate controlled" is ambiguous — clarify whether this means heated only, heated and cooled, or temperature and humidity controlled, and specify acceptable temperature/humidity range. TBD: confirm with Owner/MEP lead. [Lensing: C-001]

### REQ-0202-18: Simultaneous Gear Donning Capacity (PROPOSED)

**Shall:** The bunker gear locker room layout shall allow a minimum of TBD firefighters to don gear simultaneously without interference.

- Source: **ASSUMPTION** — Guidance Principle 5 states "two firefighters to don gear simultaneously without interference" as an operational expectation; not explicitly stated in OSR or Addendum 03. Confirm minimum simultaneous donning capacity with Owner (Fire Department). [Lensing: C-003]
- Note: This requirement is proposed based on Guidance analysis. Pending Owner confirmation, the minimum number may need adjustment.

### REQ-0202-14: Apparatus Bay Display System

**Shall:** Provide a display system (wall-mounted display/TV with connectivity to a laptop) in the apparatus bay closest to the office area, for displaying emergency dispatch information.

- Source: OSR §10.6; SOW-0225
- Note: IT/data connectivity is coordinated with DEL-02-06.

### REQ-0202-15: Water Fill Station

**Shall:** Provide one (1) ground-level water fill station in the fire apparatus bay area; minimum 2-inch connection.

- Source: Addendum 03 §1.16; SOW-0223
- Coordination: DEL-02-05 (Plumbing) for water supply design.

### REQ-0202-16: Compressed Air — Compressor Room

**Shall:** Provide a compressed air compressor room of approximately 100–150 sf to house the breathing air compressor and distribution equipment.

- Source: Functional Program Appendix B; Addendum 03 §1.21; OSR §10.2
- **Note:** Clarify whether this compressor room serves both SCBA/cascade breathing-air system (REQ-0202-11) and bay compressed-air distribution (REQ-0202-03), or whether these are separate systems requiring separate equipment. Air quality grade, pressure, and volume for bay connections — TBD. [Lensing: A-002, E-002]

### REQ-0202-17: Code Compliance

**Shall:** All spaces shall comply with the Alberta Building Code (ABC) for occupancy type, egress, ventilation, and accessibility as applicable.

- Source: RFP §7.1.3; OSR general requirements
- Note: AHJ has indicated intent to exempt post-disaster importance category (OSR §10.3.5); verify with AHJ during design.
- **Acceptance criteria — TBD:** Specify which ABC occupancy classification applies to firehall wing, egress travel-distance limits, and accessibility provisions for self-check before AHJ submission. [Lensing: A-003]
- **Accessibility specifics — TBD:** Identify which firehall support spaces require barrier-free access under ABC and whether apparatus bays require accessible routes. Volunteer fire department facilities have specific accessibility considerations that may differ from general commercial occupancy. [Lensing: D-001]
- **Emergency egress from apparatus bays — TBD:** Add bay-specific pedestrian egress requirements (e.g., personnel doors for pedestrian egress when overhead doors are closed, travel distance from inside bays to exits). [Lensing: F-003]

---

## Standards

| Standard | Applicability | Access Status |
|---|---|---|
| Alberta Building Code (ABC) | Building occupancy, egress, ventilation, accessibility | Referenced; full text not accessed — **location TBD.** Obtain full text and confirm occupancy classification, egress travel-distance limits, and accessibility provisions with AHJ before detailed design. [Lensing: A-001] |
| NFPA 1 / NFPA 101 (Life Safety Code) | Fire station life safety requirements | **ASSUMPTION:** likely applicable for firehall design; confirm applicability with AHJ. **No verification step currently exists** — see Verification table note. [Lensing: A-001, F-002] |
| NFPA 1989 (Breathing Air Quality) | SCBA/cascade system standards | **ASSUMPTION:** likely applicable; confirm with MEP lead. **No verification step currently exists** — see Verification table note. [Lensing: A-001, F-002] |
| IES Lighting Standards | Lighting levels for apparatus bays | Referenced in OSR §10.5; specific IES criteria — **TBD.** Determine applicable illuminance levels for apparatus bays with Electrical Engineer. [Lensing: B-002] |
| Alberta OHS Regulation | Workplace health and safety for fire department facility | **ASSUMPTION:** applicable; confirm with AHJ and Owner. **No verification step currently exists** — see Verification table note. [Lensing: A-001, F-002] |
| CCDC 14-2013 | Design-Build contract form | Referenced in RFP; governs contract structure |

---

## Verification

| Requirement | Verification Approach |
|---|---|
| REQ-0202-01 Bay count and type | Confirm 4 drive-through bays on floor plan drawings; verify apparatus templates fit |
| REQ-0202-02 Bay dimensions | Check plan drawings against 2,000–2,200 sf target; confirm 16 ft clear height in section drawings |
| REQ-0202-03 Bay services | Confirm electrical, compressed air, and exhaust connections shown on layout drawings per bay. **Strengthen:** Verify not only presence on drawings but also connection type, sizing, spacing, and air quality grade specification. Acceptance criterion: drawing shows for each bay — (a) electrical drop location and type, (b) compressed air connection (grade: breathing air vs. shop air), pressure, volume, and connection type, (c) two exhaust connections with specifications. [Lensing: X-002] |
| REQ-0202-04 Exhaust ventilation | Verify coordination drawing with DEL-02-05 shows two exhaust drop locations per bay |
| REQ-0202-05 Bay sumps | Confirm sump locations shown on floor plan and plumbing coordination. Acceptance criterion: sump capacity and drainage rate meet or exceed runoff from two apparatus per bay (including winter snow accumulation per Guidance Considerations). [Lensing: A-005] |
| REQ-0202-06 Bay floor | Confirm concrete floor and apron specifications in floor finish schedule. Acceptance criterion: floor finish schedule specifies minimum compressive strength, slip resistance rating (ASTM or equivalent), and chemical resistance rating for areas subject to decontamination cleaning or fuel/oil exposure. [Lensing: F-004] |
| REQ-0202-07 Secondary door mechanism | Confirm detail or specification note on drawings; coordinate with DEL-02-07 |
| REQ-0202-08 Decon area | Verify room data sheet and floor plan show all required sub-components |
| REQ-0202-09 Bunker gear lockers | Confirm 40-locker count in room data sheet; verify room area adequate |
| REQ-0202-10 Locker room ventilation | Confirm ventilation note in room data sheet or HVAC coordination |
| REQ-0202-11 SCBA room | Confirm 150–200 sf room on plan; note FF&E exclusion in documentation |
| REQ-0202-12 EMS storage | Confirm 50–70 sf space shown adjacent to decon area |
| REQ-0202-13 Fire gear storage | Confirm 200–350 sf climate-controlled space on plan. Acceptance criterion: HVAC schedule specifies target temperature range and humidity range (e.g., 15–20°C, 40–60% RH for typical gear preservation); mechanical system design verified to meet specified conditions. [Lensing: X-004] |
| REQ-0202-14 Display system | Confirm display location on bay closest to office; confirm connectivity noted |
| REQ-0202-15 Water fill station | Confirm fill station location on plan; 2-inch minimum noted in plumbing schedule |
| REQ-0202-16 Compressor room | Confirm 100–150 sf compressor room on plan |
| REQ-0202-17 Code compliance | Confirm egress paths, occupant loads, and accessibility on drawings; AHJ review at permit stage. Acceptance criteria for self-check before AHJ submission: (a) occupancy classification identified per ABC Table A-3, (b) occupant load calculated per occupancy type, (c) egress travel distances confirmed below ABC limits (location TBD), (d) accessibility requirements identified per ABC Table A-5 (which firehall spaces require barrier-free access), (e) bay-specific pedestrian egress verified (personnel doors with marked egress paths from apparatus work areas, travel distance < ABC limit from inside bay to exit). [Lensing: A-003, F-003] |
| REQ-0202-18 Simultaneous gear donning (PROPOSED) | Confirm locker room layout allows minimum TBD firefighters to don gear simultaneously; verify through layout review with Fire Department representative. [Lensing: C-003] |
| Standards applicability (NFPA 1, NFPA 1989, Alberta OHS) | Confirm applicability of NFPA 1, NFPA 1989, and Alberta OHS with AHJ and MEP lead during design development. Record confirmation or exclusion rationale. Acceptance criterion: design notes include acknowledgment statement confirming which standards apply to firehall wing design. [Lensing: F-002] |
| Construction hold/witness points | Define and document hold/witness points for critical construction milestones: (a) sump installation inspection before slab pour (verify type, size, connection to drainage system), (b) exhaust connection rough-in inspection before ceiling closure (verify routing, connection type, capping), (c) electrical and compressed air embedded services inspection before slab/ceiling concealment (verify conduit routing, box locations, future connection accessibility). TBD: specific inspection checklist to be developed during detailed design. [Lensing: X-003] |

---

## Documentation

### Anticipated Artifacts (from _CONTEXT.md)

1. **Apparatus bay layouts** — plan drawings showing all four drive-through bays with services locations, door positions, sump locations, display system location.
2. **Decontamination/gear locker layouts** — floor plans showing decon room, shower/WR units, bunker gear locker room (40 lockers), fire gear storage, duty gear room.
3. **Compressed air + bay services concept** — schematic or narrative describing electrical, compressed air, and exhaust mitigation distribution approach per bay.
4. **Bay exhaust mitigation coordination** — coordination document or drawing linking to DEL-02-05 direct exhaust system design.
5. **Apparatus bay display concept** — description or schematic of display system (wall-mounted TV/monitor with laptop connectivity) in closest bay to office.

### Supporting Documentation Required

- Room data sheets for each firehall support space
- Coordination matrix with DEL-02-04, DEL-02-05, DEL-02-06, DEL-02-07
- FF&E exclusion list (SCBA equipment, appliances)
