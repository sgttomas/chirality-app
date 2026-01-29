# Datasheet: DEL-21.01 Building Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-21.01 |
| Name | Building Design Drawing Set |
| Package | PKG-21 Building Structures & Envelope |
| Discipline | Buildings |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md` and `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (line 513)

## Attributes

| Attribute | Value |
|-----------|-------|
| Drawing Number Prefix | **TBD** — To be assigned per project drawing numbering system |
| Sheet Size | **TBD** — **ASSUMPTION**: ANSI D (24×36 inches) or ISO A1, typical for building design drawings |
| Scale | **TBD** — **ASSUMPTION**: Varies by drawing type (1:100, 1:50, 1:20 typical for building plans/elevations/sections) |
| CAD Standard | **TBD** — To be defined per project CAD standards manual |
| Drawing Software | **TBD** — **ASSUMPTION**: AutoCAD or Revit typical for building design |
| Coordinate System | **TBD** — **ASSUMPTION**: Project coordinate system to be established per site survey |
| Units | **TBD** — **ASSUMPTION**: Metric (mm) typical for Canadian building projects |
| Revision Tracking | **TBD** — Per project document control procedures |
| Classification | **TBD** — Per project security/confidentiality classification |

## Conditions

**Project Context:**

Project: Canola Oil Transload Facility — Phase 1
Location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
Employer: DP World Fraser Surrey Inc.
Contract Type: Design & Build

**Source:** Decomposition document Section 1.1

**Building Scope:**

Package scope: MCC building structure, cladding, roofing, doors, windows, operator shelters

**Source:** Decomposition document (line 507, PKG-21 scope definition)

**Environmental/Operational Context:**

- Location climate: Coastal BC (Fraser Valley) — **TBD**: Design temperatures, wind loads, precipitation
- Seismic zone: **TBD** — **ASSUMPTION**: Western Canada seismic provisions apply (NBC 2020 seismic design)
- Hazardous area classification: **TBD** — Subject to facility hazardous area classification study
- Marine environment exposure: **ASSUMPTION**: Site proximity to marine terminal may affect corrosion protection requirements
- Design life: **TBD** — **ASSUMPTION**: 25-50 years typical for industrial building structures
- Occupancy classification: **TBD** — **ASSUMPTION**: Industrial occupancy (Group F) per NBC 2020, Part 3
- Fire rating requirements: **TBD** — To be determined based on occupancy and building code analysis

**Adjacent Facilities:**

- Existing terminal operations — continuity requirements per OBJ-5 (Terminal Continuity): "The Works minimize disturbance to existing Terminal commercial activities"
- **TBD** — Specific interface requirements with existing terminal buildings/infrastructure

**Source:** Decomposition Section 2 (Project Objectives)

## Construction

**Anticipated Drawing Artifacts:**

Per decomposition (line 513):
1. MCC building general arrangements (GAs)
2. Floor plans
3. Elevations
4. Sections
5. Operator shelter drawings

**Building Types:**

- **MCC Building:** Motor Control Center building housing electrical distribution equipment
  - Function: **TBD** — Electrical equipment enclosure, personnel access
  - Size/footprint: **TBD**
  - Number of stories: **TBD**
  - Construction type: **TBD** — **ASSUMPTION**: Pre-engineered metal building or modular construction typical for industrial MCC buildings

- **Operator Shelters:** Personnel shelters for railcar unloading operations
  - Function: **TBD** — Weather protection for operators during railcar connection/disconnection
  - Number of shelters: **TBD** — **ASSUMPTION**: Related to 32 railcar unloading stations (decomposition Section 1.1)
  - Size: **TBD**
  - Construction type: **TBD**

**Primary Materials:**

- **TBD** — Structural system (steel frame, concrete, hybrid)
- **TBD** — Cladding/envelope system (insulated metal panels, precast concrete, etc.)
- **TBD** — Roofing system
- **TBD** — Door and window specifications
- **ASSUMPTION**: Materials selected for durability in industrial/marine environment

**Drawing Content Requirements:**

- Foundation interface details
- Structural framing arrangements
- Roof framing and drainage
- Wall/cladding systems
- Door and window schedules and details
- Floor plans showing equipment layout clearances
- Sections showing interior clearances and vertical coordination
- Site plan showing building locations
- **TBD** — Fire egress routes and fire-rated assemblies
- **TBD** — Accessibility provisions per barrier-free design requirements

## References

**Decomposition Document:**
- `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (line 513, PKG-21 section lines 503-519)

**Deliverable Context Files:**
- `_CONTEXT.md`
- `_REFERENCES.md` (no specific references identified yet)

**Applicable Codes and Standards (Buildings Discipline):**

Canadian Building Codes:
- **NBC 2020** — National Building Code of Canada 2020 (structural design, fire safety, barrier-free design)
- **ABC 2019** — **ASSUMPTION**: Alberta Building Code 2019 or British Columbia Building Code (to be confirmed — **TBD**: applicable provincial code)

Structural Design Standards:
- **CSA A23.3** — Design of Concrete Structures
- **CSA S16** — Design of Steel Structures

Energy/Mechanical Standards:
- **ASHRAE 90.1** — Energy Standard for Buildings (envelope performance, if conditioned space)

**Additional Standards/Requirements:**
- **TBD** — Employer's Requirements Volume 2 Part 3 (Building Works) — not yet accessed per user instruction
- **TBD** — Project-specific drawing standards manual
- **TBD** — CAD layer/naming conventions
- **TBD** — Accessibility requirements (CSA B651 or NBC Part 3 Div B)
- **TBD** — Wind load standard (NBCC or reference wind tunnel study if required)
- **TBD** — Seismic design requirements per NBC 2020 or site-specific seismic hazard assessment

**Cross-References:**

Dependencies coordinated externally (NOT_TRACKED mode per `_DEPENDENCIES.md`)

Related deliverables (same package):
- DEL-21.02: Building Technical Specification
- DEL-21.03: Building Design Calculations
- DEL-21.04: Building Data Sheet Package
- DEL-21.05: Building Installation & Test Records
- DEL-21.06: Building Shop Design Drawing Set

**Potential upstream dependencies (to be coordinated externally):**
- Site civil/grading drawings (elevation/datum coordination)
- Electrical equipment layout requirements (MCC sizing/configuration)
- Hazardous area classification study
- Geotechnical investigation (foundation design input)

**Potential downstream dependencies (to be coordinated externally):**
- Building MEP drawings (PKG-22)
- Structural calculations (DEL-21.03)
- Building specifications (DEL-21.02)
- Shop/fabrication drawings (DEL-21.06)
