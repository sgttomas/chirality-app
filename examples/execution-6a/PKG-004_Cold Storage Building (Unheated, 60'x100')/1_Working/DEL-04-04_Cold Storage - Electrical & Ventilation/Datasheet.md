# Datasheet: DEL-04-04 — Cold Storage Electrical & Ventilation

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-04-04 |
| Name | Cold Storage — Electrical & Ventilation |
| Package | PKG-004 Cold Storage Building (Unheated, 60'×100') |
| Discipline | MEP |
| Type | Building design package (4-doc bundle) |
| Responsible Party | Design-Builder (MEP) |
| Project | Town of Penhold Public Services Building |
| RFP Reference | AB-2024-07156 |
| Decomposition Reference | Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| Scope Coverage | SOW-0300 (MEP aspects) |
| Objective Support | OBJ-004 |

## Attributes

### Building Context

| Attribute | Value | Source |
|-----------|-------|--------|
| Building type | Unheated cold storage | OSR §10.2 |
| Building footprint | 60' × 100' clear-span | OSR §10.2; SOW-0301 |
| Ceiling / ridge height | TBD (confirm from DEL-04-01 design basis) | **[B-001]** DEL-04-01 design basis; required for lighting fixture height (R-07) and ventilation sizing (R-11) |
| Eave height | TBD (confirm from DEL-04-01 design basis) | **[B-001]** DEL-04-01 design basis |
| Maximum stored equipment height | TBD (confirm from operations: tractors, loaders, graders, pickup trucks with possible attachments) | **[C-5, E-003]** Required for fixture height determination and maintenance access planning |
| Intended use | Seasonal equipment (trucks, tractors, graders, loaders, bobcats), materials, and supplies storage | OSR §10.2; OSR §10.3.5 |
| Design life | 20 years | OSR §10.2 (General) |
| Users | Volunteer firefighters, crew members, Public Works staff | OSR §10.3.4 |

### Climate Conditions

| Attribute | Value | Source |
|-----------|-------|--------|
| Location | Penhold, Alberta (Red Deer region) | OSR §11.3 |
| Climate classification | Cold climate; significant snow and wind loads; prolonged sub-zero winter periods | OSR §11.3 |
| Design temperatures (winter minimum) | TBD (obtain from Environment Canada climate normals for Penhold/Red Deer region; approximately –20°C to –30°C typical for design) | **[B-003]** Required for ventilation sizing and cold-temperature equipment rating; critical for emergency lighting battery selection |
| Design temperatures (summer maximum) | TBD (obtain from Environment Canada climate normals; approximately 25–30°C typical) | **[B-003]** Required for HVAC and cooling assessment |
| Heating degree days (annual) | TBD (obtain from Environment Canada climate normals for Penhold; Red Deer ~5,150 HDD/year typical) | **[B-003]** Required for ventilation approach assessment and energy consumption projection |
| Cooling degree days (annual) | TBD (obtain from Environment Canada climate normals; Red Deer ~125 CDD/year typical) | **[B-003]** Required for summer ventilation strategy |
| Typical winter humidity range | TBD (obtain from Environment Canada climate normals and building simulation; condensation risk highest when 40–70% RH interior meets cold exterior surfaces) | **[B-003, C-2]** Required for condensation risk analysis and ventilation sizing |
| Extreme wind speed (3-second gust) | TBD (per National Building Code of Canada; obtain from Wind Climate study for site) | **[B-003]** Required for passive ventilation effectiveness assessment (stack effect and wind-driven infiltration); critical to passive/hybrid ventilation approach |
| Seasonal precipitation (snow) | TBD (obtain from Environment Canada; Red Deer ~330 mm annual precipitation, ~150 cm seasonal snow) | **[B-003]** Required for roof loading (affects ventilation opening flashing and drainage design) |

### Electrical System Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Electrical design basis | Meet current needs and allow future flexibility | OSR §10.4 |
| Receptacles — interior | Required; quantity and circuit layout TBD | OSR §10.4 |
| Receptacles — exterior | Required; quantity and location TBD | OSR §10.4 |
| Block heater receptacles | TBD — Confirm whether block heater receptacles are required for equipment stored in the unheated building; common operational need in cold-climate Alberta (if yes, add to receptacle requirements and electrical load calculation) | **[E-002]** Owner operations / DB MEP to confirm |
| Overhead door opener coordination | Required; electrical supply to motorized openers | OSR §10.4; SOW-0302 |
| Number of overhead doors (motorized) | 2 (one per side) × 16'×16' with motorized openers | OSR §10.3.9; SOW-0302 |
| Electrical service size | TBD — Estimated service size (amps) to be determined by DB MEP engineer based on connected load calculation (lighting, receptacles, two door openers, ventilation fans if active, and block heaters if required) | **[A-004]** DB MEP engineer based on load calculation |
| Grounding | Required per code | OSR §10.4 |

### Lighting System Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Lighting standard | IES (Illuminating Engineering Society) recommendations for storage facility occupancy category | OSR §10.5 |
| Lamp type | Energy-efficient LEDs with cold-temperature ratings suitable for unheated building | OSR §10.5; **[D-003, E-003]** |
| Emergency exit lights | Required above person doors with internal battery backup; cold-temperature rated units (min. –15°C or lower per code) | OSR §10.5; **[C-4, C-004]** |
| Number of person doors | 2 (one per side) | OSR §10.3.9; SOW-0302 |
| Emergency exit light locations | Above each person door, installed to meet Alberta Fire Code placement requirements | OSR §10.5; **[D-001]** |
| Switches at person doors | Required at each person door location; weatherproof covers for ancillary building use | OSR §10.5 |
| Fixture height | Adjusted to avoid interference with machinery (confirm maximum equipment height from DEL-04-01 and operations) | OSR §10.5; **[B-001, C-5, E-003]** |
| Interior foot-candle target | TBD — Design-Builder to advise per applicable IES storage occupancy category (confirm specific foot-candle value per IES publication) | OSR §10.5; **[A-003]** |
| Exterior building-mounted lighting | TBD — Confirm whether exterior fixtures are required for the cold storage building, or explicitly exclude from scope. OSR §10.5 addresses interior lighting; exterior lighting requirement is silent. | **[B-002, B-005, C-005]** OSR review / DB design team to confirm |

### Ventilation System Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Ventilation requirement | Adequate ventilation or alternate air circulation to prevent condensation and icing | OSR §11.1.2; SOW-0300 |
| Ventilation approach | Design-Builder to propose and justify (passive openings, active fans, or hybrid combination). OSR permits flexibility. | OSR §11.1.2 |
| Condensation mitigation | Required; primary design driver for this unheated building in cold climate | OSR §11.1.2; SOW-0300; **[P-1]** |
| Icing prevention | Required; floor icing is primary safety hazard requiring ventilation focus | OSR §11.1.2; SOW-0300 |
| Ventilation sizing criteria | TBD — What ventilation sizing criteria or airflow rate standard applies to an unheated 60'×100' storage building in Penhold, AB? Applicable standards include ASHRAE or NBCC guidance for cold-climate storage. DB MEP engineer to determine applicable benchmark or target metric (e.g., air changes per hour, CFM per square foot, humidity target) | **[A-002, B-004]** Specification R-11 labels this ASSUMPTION; no benchmark stated in OSR; authoritative engineering reference to be identified |
| Ventilation sizing | TBD (to be established by DB MEP engineer with stamped engineering calculations) | **[F-001]** |
| Ventilation controls | TBD (manual, thermostat-controlled, humidity-controlled, or passive stack-effect only); selection depends on chosen approach (active vs. passive vs. hybrid) | **[C-2, A-005]** |
| Condensation risk analysis | Required — DB to submit condensation risk analysis demonstrating proposed ventilation approach is sufficient for Penhold climate conditions, including first-winter post-occupancy monitoring protocol | **[X-001, F-003, X-003]** |

## Conditions

| Condition | Value | Source |
|-----------|-------|--------|
| Building is unheated | No heating system provided; ventilation must account for unheated interior | OSR §10.2; §10.3.5 |
| Climate zone | Penhold, Alberta (cold climate; significant snow and wind loads) | OSR §11.3 |
| Equipment stored | Same types as main building: trucks, tractors, graders, loaders, bobcats, etc. | OSR §10.3.5 |
| Operational context | Accessed by volunteer firefighters and Public Works staff | OSR §10.3.4 |
| Materials standard | Watertight, non-combustible, durable materials for all building systems | OSR §11.3 |
| Weatherproofing | Weatherproof covers on switches at person doors | OSR §10.5 |
| IT/Telecom in cold storage | Not required (IT/data requirements apply to main building only) | OSR §10.6 |
| PA system in cold storage | Not required (PA system for main building only) | OSR §10.6 (implied) |

## Construction

| Element | Description | Source |
|---------|-------------|--------|
| Electrical receptacles | Interior and exterior; coordinate with mechanical systems and door openers | OSR §10.4 |
| Lighting fixtures | LED type, IES-compliant, height adjusted for equipment clearance | OSR §10.5 |
| Emergency exit lights | Battery-backup units above person doors (2 locations) | OSR §10.5 |
| Weatherproof switches | At each person door entry point (2 locations minimum) | OSR §10.5 |
| Ventilation / air circulation | Method TBD by DB; must prevent condensation and icing | OSR §11.1.2 |
| Overhead door opener circuits | Dedicated electrical circuits for motorized openers (2 units) | OSR §10.4; SOW-0302 |
| Grounding system | Per applicable electrical code | OSR §10.4 |
| Materials durability | Non-combustible, watertight, suitable for cold/unheated environment | OSR §11.3 |

## References

| Reference | Location | Notes |
|-----------|----------|-------|
| OSR (Appendix A to RFP) — §10.2 | RFP PDF p.36 | Cold storage building description and access requirements |
| OSR §10.3.4 | RFP PDF p.39 | Project design requirements (safe access, maneuverability) |
| OSR §10.3.5 | RFP PDF p.40 | Structural objectives; equipment types stored; 20-year design life |
| OSR §10.3.9 | RFP PDF p.41 | Roof and door system; overhead door specs; person door requirements |
| OSR §10.4 | RFP PDF p.42 | Electrical system requirements |
| OSR §10.5 | RFP PDF p.42 | Lighting system requirements |
| OSR §11.1.2 | RFP PDF p.43 | Cold storage ventilation requirement |
| OSR §11.3 | RFP PDF p.44 | Materials requirements |
| Decomposition SOW-0300 | PHASE7.md | Ventilation/condensation/icing requirement; links DEL-04-04 |
| Decomposition SOW-0302 | PHASE7.md | Door and opener requirements |
| Decomposition OBJ-004 | PHASE7.md | Deliver unheated cold storage with moisture management |
| Environment Canada climate normals | location TBD | Climate data for Penhold/Red Deer region — [B-003] |
