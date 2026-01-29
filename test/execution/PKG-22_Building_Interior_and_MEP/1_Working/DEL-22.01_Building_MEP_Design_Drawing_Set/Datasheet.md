# Datasheet: DEL-22.01 Building MEP Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-22.01 |
| Name | Building MEP Design Drawing Set |
| Package | PKG-22 Building Interior & MEP |
| Discipline | Buildings |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Drawing Number Prefix | **TBD** — Per project drawing numbering system |
| Sheet Size | **TBD** — **ASSUMPTION**: ISO A1 or ANSI D per project CAD standards |
| Scale | **TBD** — Varies by drawing type (typical: 1:50, 1:100 for plans; NTS for schematics) |
| CAD Standard | **TBD** — Per project CAD Manual |
| File Format | **TBD** — **ASSUMPTION**: DWG native + PDF for issue |
| Revision Control | **TBD** — Per project document control procedure |
| Classification | For Construction |
| Drawing Disciplines | HVAC (H), Plumbing (P), Electrical Building Services (E), Fire Protection (FP) |

**Source:** Decomposition REVISED_v2.md, DEL-22.01 entry; _CONTEXT.md

## Conditions

**Operating / Environmental Context:**

This drawing set defines the design arrangement and details for building MEP systems serving the MCC building and any other project buildings within the facility scope.

**Source:** Decomposition REVISED_v2.md, PKG-22 scope; DEL-22.01 description

### System Operating Conditions

| Condition | Value |
|-----------|-------|
| Building Type | MCC building (Motor Control Center building) |
| Indoor Design Temperature | **TBD** — Per ASHRAE 90.1 and building occupancy type |
| Indoor Humidity Range | **TBD** — Per building function |
| Outdoor Design Temperature (Winter) | **TBD** — Per NBC 2020 climate data for Surrey, BC |
| Outdoor Design Temperature (Summer) | **TBD** — Per NBC 2020 climate data for Surrey, BC |
| Hazardous Area Classification | **TBD** — Per facility hazardous area study (Note: building interior likely non-hazardous) |
| Seismic Design Category | **TBD** — Per NBC 2020, Site Class for Surrey, BC |
| Design Life | **TBD** — **ASSUMPTION**: 25 years minimum per industrial facility practice |
| Building Occupancy Classification | **TBD** — Per NBC 2020 Part 3 (likely Group F - Industrial) |

**Source:** NBC 2020 requirements (location TBD); ASHRAE 90.1 (location TBD)

### MEP System Context

| System | Description |
|--------|-------------|
| HVAC | Heating, ventilation, and air conditioning for building environmental control |
| Plumbing | Domestic water, sanitary drainage, and process water systems |
| Electrical (Building Services) | Interior lighting, receptacles, small power distribution (excludes main electrical distribution covered by PKG-17) |
| Fire Suppression | Automatic sprinkler system, standpipe connections, fire alarm interfaces |

**Note:** This package covers building interior MEP only. Main electrical power distribution is PKG-17; process systems are other packages.

**Source:** Decomposition REVISED_v2.md, PKG-22 scope description

## Construction

**Materials / Configuration:**

### Anticipated Drawing Artifacts

Per Decomposition REVISED_v2.md, DEL-22.01 anticipated artifacts:

1. **HVAC layout** — Ductwork routing, equipment locations, diffuser schedules, control zones
2. **Plumbing layout** — Piping routing, fixture locations, equipment schedules, drainage layout
3. **Interior electrical layout** — Lighting layout, receptacle locations, panel schedules, circuit routing
4. **Fire suppression layout** — Sprinkler head layout, piping routing, standpipe locations, system zones

**Source:** Decomposition REVISED_v2.md, DEL-22.01 anticipated artifacts

### Drawing Set Organization (Typical)

**ASSUMPTION**: Standard MEP drawing set organization to be confirmed with project CAD standards:

- **Mechanical (HVAC) Drawings:**
  - Floor plans showing ductwork, equipment locations, diffusers
  - Sections and details
  - Equipment schedules and specifications
  - Control system schematics (interface to PKG-19 Control Systems)

- **Plumbing Drawings:**
  - Floor plans showing piping, fixtures, equipment
  - Riser diagrams
  - Equipment schedules
  - Details and connections

- **Electrical (Building Services) Drawings:**
  - Lighting plans with fixture schedules
  - Power plans with receptacle locations
  - Panel schedules and circuit routing
  - Details and connections (interface to PKG-17 main power distribution)

- **Fire Protection Drawings:**
  - Sprinkler layout plans
  - System riser diagrams
  - Hydraulic calculation reference
  - Details and connections to water supply (interface to PKG-03 Site Services)

### Installation Sequence Considerations

**Decision DEC-06** from Decomposition: "MCC building equipment installed on-site after building erection"

This affects installation sequencing shown on MEP drawings. Building structure (PKG-21) must be complete before MEP installation begins.

**Source:** Decomposition REVISED_v2.md, Section 7 Decisions Captured, DEC-06

## References

### Project References

- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- Context: `_CONTEXT.md`
- Dependencies: `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)
- Additional references: See `_REFERENCES.md` and `execution/PKG-22_Building_Interior_and_MEP/0_References/`

### Applicable Standards

**Buildings Discipline Standards (ASSUMPTION: applicable per industry practice):**

- **NBC 2020** — National Building Code of Canada 2020 (building code requirements)
- **ABC 2019** — **TBD** — Identify full name and applicability (location TBD)
- **ASHRAE 90.1** — Energy Standard for Buildings Except Low-Rise Residential Buildings
- **CSA A23.3** — Design of Concrete Structures (structural interfaces)
- **CSA S16** — Design of Steel Structures (structural interfaces)

**MEP-Specific Standards (to be confirmed):**

- **ASHRAE 62.1** — Ventilation for Acceptable Indoor Air Quality — **TBD** (location TBD)
- **NFPA 13** — Installation of Sprinkler Systems — **TBD** (location TBD)
- **CSA B64** series — Plumbing standards — **TBD** (location TBD)
- **CEC (CE Code)** — Canadian Electrical Code — **TBD** (location TBD)

**Source:** Applicable standards inferred from Buildings discipline; specific editions and applicability TBD per Employer's Requirements

### Cross-References

**Related Deliverables (coordination required):**

- **PKG-17** — Electrical Power Distribution (main power feed to building panels)
- **PKG-19** — Control Systems (HVAC controls, BAS interfaces)
- **PKG-21** — Building Structures & Envelope (architectural/structural coordination)
- **PKG-03** — Site Services (water supply for fire protection, sanitary connections)

**Source:** Inferred from scope interfaces; formal dependencies tracked externally per `_DEPENDENCIES.md`
