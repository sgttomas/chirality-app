# Datasheet: DEL-23.01 Fire Protection Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-23.01 |
| Name | Fire Protection Design Drawing Set |
| Package | PKG-23 Fire Protection |
| Discipline | Specialty |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |
| Project | Canola Oil Transload Facility — Phase 1 |
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Drawing Number Prefix | **TBD** | **ASSUMPTION**: Per project drawing numbering system |
| Sheet Size | ANSI D (24" × 36") | **ASSUMPTION**: Typical for industrial facility general arrangement drawings |
| Scale | As noted on drawings | **ASSUMPTION**: Varied scales per drawing type (site plan 1:500, details as required) |
| CAD Standard | **TBD** | **ASSUMPTION**: AutoCAD or equivalent, per project CAD manual |
| Revision | Rev 0 (initial issue) | **ASSUMPTION**: Initial design phase |
| Classification | For Design & Construction | Decomposition: DEL-23.01 |
| Drawing Types | Layout, details, single-line diagrams | **ASSUMPTION**: Typical fire protection drawing set composition |
| Coordinate System | **TBD** | **ASSUMPTION**: Site coordinate system per project survey control |
| Units | SI (metric) | **ASSUMPTION**: Canadian project standard |

## Conditions

**Operating / Environmental Context:**

This drawing set defines the design arrangement and details for fire protection systems serving a canola oil transload facility with the following conditions:

| Condition | Value | Source |
|-----------|-------|--------|
| Facility Type | CSD Canola Oil Transload | Decomposition Section 1.1 |
| Permitted Throughput | 1,000,000 MT per annum | Decomposition Section 1.1 |
| Storage Capacity | 45,000 MT (3 × 15,000 MT tanks) | Decomposition Section 1.1 |
| Railcar Capacity | 32 unloading stations on 2 tracks | Decomposition Section 1.1 |
| Product Classification | Combustible liquid (Class IIIA per NFPA 30) | **ASSUMPTION**: CSD canola oil flash point typically >93°C (200°F) |
| Operating Temperature Range | -40°C to +40°C ambient | **ASSUMPTION**: Fraser Valley climate, BC |
| Environmental Classification | Outdoor industrial | Site location |
| Hazardous Area Classification | Class I, Division 2 (anticipated in loading areas) | **ASSUMPTION**: To be confirmed per facility hazardous area classification study (DEL-30.03) |
| Seismic Requirements | 2020 NBCC seismic provisions | **ASSUMPTION**: BC location requires seismic design |
| Design Life | 25 years minimum | **ASSUMPTION**: Typical industrial facility design life |
| Fire Protection Zones | Tank farm, marine loading, railcar unloading, pump house, building areas | **ASSUMPTION**: Typical facility zoning |

**Fire Protection Requirements:**

| Requirement | Value | Source |
|-------------|-------|--------|
| Fire Water Demand | **TBD** | To be determined per DEL-23.03 (Fire Protection Design Calculations) |
| Hydrant Flow Rate | **TBD** (typically 1,500 gpm minimum per hydrant) | **ASSUMPTION**: NFPA 30 requirements for combustible liquid facilities |
| Fire Water Duration | **TBD** (typically 2–4 hours) | **ASSUMPTION**: Per NFPA 30 and risk assessment |
| Fire Water Pressure | **TBD** | To be calculated per hydraulic analysis (DEL-23.03) |
| Fire Water Source | **TBD** | To be coordinated with Employer and municipal supply |

## Construction

**Materials / Configuration:**

The fire protection design drawing set comprises the following anticipated artifacts:

| Drawing Type | Content | Purpose | Source |
|--------------|---------|---------|--------|
| Fire Water Loop Layout | Site plan showing fire water piping layout, loop configuration, isolation valves, connections | Defines overall fire water distribution | Decomposition: DEL-23.01 anticipated artifacts |
| Hydrant Locations | Site plan showing fire hydrant locations, coverage radii, access routes | Ensures code-compliant fire hydrant spacing and accessibility | Decomposition: DEL-23.01 anticipated artifacts |
| Fire Alarm System Drawings | Fire detection/alarm system layout, device locations, wiring diagrams, panel schedules | Defines fire detection and notification system | Decomposition: DEL-23.01 anticipated artifacts |

**Additional Drawing Content (typical):**

| Drawing Type | Content | Source |
|--------------|---------|--------|
| Fire Water System Schematic | Single-line diagram showing fire water system configuration, connections, control valves | **ASSUMPTION**: Typical fire protection drawing set component |
| Fire Pump Details | Fire pump installation details (if required), connection details | **ASSUMPTION**: If fire pump is part of Contractor scope |
| Foam System Layout | Foam concentrate storage, proportioning systems, discharge devices (tank and marine loading areas) | **ASSUMPTION**: Likely required for combustible liquid storage per NFPA 30 |
| Fire Protection Details | Hydrant installation details, valve pit details, pipe supports, fire main penetrations | **ASSUMPTION**: Standard detail drawings |
| Fire Protection Zone Plan | Fire protection zone boundaries, equipment tagging, system boundaries | **ASSUMPTION**: Facilitates operations and maintenance |

**Drawing Coordination Requirements:**

| Interface | Coordination Requirement | Source |
|-----------|-------------------------|--------|
| Civil (PKG-03, PKG-04) | Fire water loop routing, hydrant locations, grading/drainage | **ASSUMPTION**: Interface coordination typical |
| Process Piping (PKG-14) | Foam system connections to tanks and marine loading arms | **ASSUMPTION**: Interface coordination typical |
| Electrical (PKG-17, PKG-18) | Power supply to fire pump, fire alarm panel power/backup | **ASSUMPTION**: Interface coordination typical |
| I&C (PKG-19, PKG-20) | Fire alarm system integration with facility control system | **ASSUMPTION**: Interface coordination typical |
| Marine Structures (PKG-08) | Marine fire main, hydrant/monitor locations on wharf | **ASSUMPTION**: Interface coordination typical |
| Buildings (PKG-21, PKG-22) | Building fire alarm system, sprinkler system interfaces | **ASSUMPTION**: Interface coordination typical |

**Drawing Production Standards:**

| Standard | Application | Source |
|----------|-------------|--------|
| CAD Layering | Per project CAD manual — **TBD** | **ASSUMPTION**: Project-specific standard |
| Line Types/Weights | Per project CAD manual — **TBD** | **ASSUMPTION**: Project-specific standard |
| Symbology | Fire protection symbols per NFPA/CSA standards | **ASSUMPTION**: Industry standard practice |
| Title Block | Per project drawing standards — **TBD** | **ASSUMPTION**: Project-specific standard |
| Sheet Numbering | Per project numbering system — **TBD** | **ASSUMPTION**: Project-specific standard |

## References

**Decomposition and Context:**
- Decomposition document: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section 5 (PKG-23), DEL-23.01
- Deliverable context: `_CONTEXT.md`
- Deliverable references: `_REFERENCES.md`

**Applicable Codes and Standards:**
- NFPA 30: Flammable and Combustible Liquids Code — **ASSUMPTION**: Primary governing standard for combustible liquid facilities
- NFPA 24: Standard for the Installation of Private Fire Service Mains and Their Appurtenances — **ASSUMPTION**: Governs fire water loop design
- NFPA 13: Standard for the Installation of Sprinkler Systems — **ASSUMPTION**: If sprinkler systems included
- NFPA 15: Standard for Water Spray Fixed Systems for Fire Protection — **ASSUMPTION**: May apply to tank cooling systems
- NFPA 16: Standard for the Installation of Foam-Water Sprinkler and Foam-Water Spray Systems — **ASSUMPTION**: Likely applicable for tank foam systems
- NFPA 72: National Fire Alarm and Signaling Code — **ASSUMPTION**: Governs fire alarm system design
- NFPA 20: Standard for the Installation of Stationary Pumps for Fire Protection — **ASSUMPTION**: If fire pump required
- National Building Code of Canada (NBCC) 2020 — **ASSUMPTION**: Applicable building code for BC
- British Columbia Fire Code (BCFC) — **ASSUMPTION**: Provincial fire code
- Alberta OHS Code — Decomposition: applicable standard
- CSA Z462: Workplace Electrical Safety — Decomposition: applicable standard
- Employer's Requirements Volume 2 Parts 1–3 — Decomposition: Section 3 (Reference Documents)

**Cross-References:**
- See `_DEPENDENCIES.md` for dependency tracking (NOT_TRACKED — dependencies coordinated externally)
- Related deliverables:
  - DEL-23.02: Fire Protection Technical Specification — defines performance, materials, workmanship requirements
  - DEL-23.03: Fire Protection Design Calculations — provides sizing and verification calculations (fire water demand, hydraulic calculations)
  - DEL-23.04: Fire Protection Data Sheet Package — equipment data sheets
  - DEL-23.05: Fire Protection Installation & Test Records — as-built verification

**Reference Materials:**
- See `0_References/` in package directory for reference materials — **TBD**
- Employer's Requirements — location **TBD**
