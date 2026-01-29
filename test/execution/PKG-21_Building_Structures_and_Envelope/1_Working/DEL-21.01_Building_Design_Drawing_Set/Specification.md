# Specification: DEL-21.01 Building Design Drawing Set

## Scope

This specification defines the requirements for the **Building Design Drawing Set** within **PKG-21 Building Structures & Envelope**.

**Purpose:** Defines the design arrangement and details for building per ER requirements.

**Source:** Decomposition document line 513

**Package Scope Context:**

PKG-21 scope: MCC building structure, cladding, roofing, doors, windows, operator shelters

**Source:** Decomposition document line 507

**Anticipated Deliverable Artifacts:**

Per decomposition (line 513):
1. MCC building general arrangements (GAs)
2. Floor plans
3. Elevations
4. Sections
5. Operator shelter drawings

**Inclusions:**
- Architectural/structural design arrangements
- Building layout and spatial organization
- Structural framing systems
- Envelope systems (walls, roofing, cladding)
- Opening schedules (doors, windows)
- Foundation interface details
- Vertical and horizontal coordination dimensions
- Material specifications (general notes on drawings)
- Site context and building locations

**Exclusions:**
- Detailed mechanical, electrical, plumbing systems (covered under PKG-22 Building Interior & MEP)
- Shop/fabrication-level detailing (covered under DEL-21.06 Building Shop Design Drawing Set)
- Detailed calculations and engineering analysis (covered under DEL-21.03 Building Design Calculations)
- Installation/construction sequencing (covered under DEL-21.05 and construction methodology)

## Requirements

### Functional Requirements

**Drawing Content Requirements:**

FR-01: **Building General Arrangements**
- Overall building dimensions and footprint
- Column grid layout and designation
- Floor-to-floor heights and overall building height
- Roof configuration and slopes
- **TBD** — Specific space requirements and functional zones (pending MCC equipment layout definition)

**Source:** Typical building design drawing content; **TBD** pending ER requirements

FR-02: **Floor Plans**
- Equipment layout zones (general clearances)
- Door and window locations
- Wall construction types
- Fire-rated separations (if applicable)
- Accessibility routes and barrier-free design features
- Floor elevation references
- **TBD** — Room/space identification and functions

**Source:** NBC 2020 Part 3 (barrier-free design); typical industrial building requirements

FR-03: **Elevations**
- Exterior facade appearance and materials
- Window and door elevations
- Finish floor and roof elevations
- Cladding transitions and material boundaries
- **TBD** — Architectural features and branding (if required)

**Source:** Standard building drawing requirements

FR-04: **Building Sections**
- Interior vertical clearances
- Roof structure and drainage
- Foundation/floor interface
- Envelope assembly thicknesses
- Mechanical/electrical overhead clearances
- **TBD** — Equipment crane/lifting provisions (if required for MCC building)

**Source:** Standard building drawing requirements

FR-05: **Operator Shelter Drawings**
- Shelter layout and dimensions
- Door/access provisions
- Environmental protection features (heating, ventilation)
- Structural support and anchorage details
- **TBD** — Number of shelters and specific locations (related to 32 railcar unloading stations per decomposition Section 1.1)

**Source:** Decomposition Section 1.1 (32 railcar unloading stations)

### Performance Requirements

PR-01: **Structural Performance**
- Comply with NBC 2020 structural provisions
- Meet site-specific seismic design requirements per NBC 2020
- **TBD** — Snow load (NBC 2020 climatic data for Surrey, BC)
- **TBD** — Wind load (NBC 2020 or wind tunnel study if required)
- **TBD** — Live loads per occupancy classification
- Foundation bearing capacity per geotechnical investigation — **TBD**

**Source:** NBC 2020; **TBD** location TBD pending code analysis and site data

PR-02: **Envelope Performance**
- Meet NBC 2020 thermal performance requirements (if conditioned space)
- Air barrier and vapor control per NBC 2020 Part 5
- Water penetration resistance per NBC 2020
- **TBD** — ASHRAE 90.1 energy performance requirements (if applicable)
- **TBD** — Condensation control and durability in coastal climate

**Source:** NBC 2020 Part 5; ASHRAE 90.1; **TBD** location pending building thermal analysis

PR-03: **Fire Safety Performance**
- Meet NBC 2020 Part 3 fire safety requirements
- **TBD** — Fire resistance ratings (if required based on occupancy and building size)
- **TBD** — Flame spread and smoke development ratings for interior finishes
- Egress provisions per NBC 2020 (travel distances, exit widths)

**Source:** NBC 2020 Part 3; **TBD** location pending fire safety analysis

PR-04: **Accessibility Performance**
- Comply with NBC 2020 Part 3 Div B Section 3.8 (barrier-free design)
- **TBD** — Accessible entrances, routes, and facilities
- **TBD** — Door clearances and hardware (lever handles, etc.)

**Source:** NBC 2020 Part 3 Div B Section 3.8

PR-05: **Operational Performance**
- Support terminal continuity during construction (OBJ-5: "The Works minimize disturbance to existing Terminal commercial activities")
- **TBD** — Equipment access and maintenance clearances
- **TBD** — Crane/lifting provisions for MCC equipment installation and maintenance
- Design life: **TBD** — **ASSUMPTION**: 25-50 years typical for industrial structures
- **TBD** — Corrosion protection in marine/industrial environment

**Source:** Decomposition Section 2 (OBJ-5); **ASSUMPTION** on design life

### Interface Requirements

IR-01: **Site Civil Interface**
- Building locations coordinated with site civil drawings (grading, drainage)
- Foundation elevations coordinated with finish site grades
- **TBD** — Stormwater connections and roof drainage tie-ins
- **TBD** — Access roads and pavement interfaces

**Source:** Typical civil-building interface requirements; dependencies coordinated externally per `_DEPENDENCIES.md`

IR-02: **Structural Foundation Interface**
- Foundation design coordinated with geotechnical investigation
- **TBD** — Foundation type (spread footings, piles, mat, etc.)
- **TBD** — Bearing capacity and settlement criteria

**Source:** Typical foundation design requirements; **TBD** pending geotechnical data

IR-03: **Building MEP Interface**
- Coordination with PKG-22 (Building Interior & MEP)
- **TBD** — HVAC equipment locations and clearances
- **TBD** — Electrical equipment layout within MCC building
- **TBD** — Plumbing and fire suppression penetrations
- **TBD** — Roof-mounted equipment support provisions

**Source:** Anticipated interface with PKG-22; dependencies coordinated externally

IR-04: **Electrical Equipment Interface**
- MCC building sized for electrical distribution equipment
- **TBD** — Equipment heat loads and ventilation requirements
- **TBD** — Equipment access and removal provisions
- **TBD** — Cable entry/exit points

**Source:** MCC building function per decomposition; **TBD** pending electrical equipment data

IR-05: **Hazardous Area Classification Interface**
- Building envelope and ventilation provisions coordinated with facility hazardous area classification
- **TBD** — Non-sparking / explosion-proof requirements (if any)
- **TBD** — Ventilation and purge provisions

**Source:** Anticipated hazardous area classification requirement; **TBD** pending classification study

### Quality Requirements

QR-01: **Drawing Standards Compliance**
- Comply with project CAD standards manual — **TBD**
- Comply with project drawing numbering system — **TBD**
- Comply with project layer/naming conventions — **TBD**
- Drawing title block format per project standards — **TBD**

**Source:** Typical project CAD standards; **TBD** location pending project standards documents

QR-02: **Design Review and Checking**
- Self-check by originator
- Independent check by qualified checker
- Interdisciplinary coordination check (IDC)
- Design review per project Quality Management Plan
- **TBD** — Specific review checklists and hold points

**Source:** Typical engineering quality procedures; **TBD** location in project QA/QC procedures

QR-03: **Accuracy and Completeness**
- Dimensions verified and coordinated
- No conflicts between plan, elevation, and section views
- Material specifications consistent with project specifications (DEL-21.02)
- Details referenced and provided
- **TBD** — Tolerance requirements for construction

**Source:** Standard drawing quality requirements

QR-04: **Regulatory Compliance**
- Design complies with NBC 2020 and applicable provincial building code
- Design complies with all permit requirements
- **TBD** — Authority having jurisdiction (AHJ) approval requirements
- **TBD** — Building permit submission requirements

**Source:** NBC 2020; regulatory compliance per OBJ-6 ("The Works comply with all permits, codes, and authority requirements" — Decomposition Section 2)

## Standards

**Governing Codes (Canadian):**

- **NBC 2020** — National Building Code of Canada 2020
  - Part 3: Fire Protection, Occupant Safety, and Accessibility
  - Part 4: Structural Design
  - Part 5: Environmental Separation
  - Part 9: Housing and Small Buildings (if applicable)

- **ABC 2019** or **BCBC 2018** — **TBD**: Confirm applicable provincial building code (Alberta Building Code 2019 or British Columbia Building Code 2018)

**Source:** Building design in Canada requires compliance with NBC and provincial adoptions

**Structural Design Standards:**

- **CSA A23.3-19** — Design of Concrete Structures
- **CSA S16-19** — Design of Steel Structures
- **CSA S6-19** — Canadian Highway Bridge Design Code (if applicable to structural elements)
- **TBD** — Foundation design standards (CSA S136 for cold-formed steel, etc.)

**Source:** Datasheet references (line 58); structural standards for building design

**Energy/Mechanical Standards:**

- **ASHRAE 90.1** — Energy Standard for Buildings Except Low-Rise Residential Buildings
  - **TBD** — Applicability depends on building conditioning and energy requirements

**Source:** Datasheet references (line 58)

**Accessibility Standards:**

- **CSA B651-18** — Accessible Design for the Built Environment (referenced by NBC 2020)

**Source:** NBC 2020 Part 3 Div B Section 3.8 references CSA B651

**Drawing and Documentation Standards:**

- **TBD** — Project CAD standards manual
- **TBD** — Project document management procedures
- **TBD** — Drawing sheet templates and title blocks

**Employer's Requirements:**

- **TBD** — Employer's Requirements Volume 2 Part 3: Building Works (not yet accessed per user instruction)
  - Expected to contain project-specific building performance requirements, materials, finishes, and acceptance criteria

**Source:** Decomposition Section 3 (Reference Documents)

**Additional Industry Standards:**

- **TBD** — CISC Handbook of Steel Construction (if steel framing)
- **TBD** — CSSBI (Canadian Sheet Steel Building Institute) standards for metal building systems
- **TBD** — Manufacturer standards for modular building construction (if modular construction approach)

## Verification

**Verification Methods for Drawing Deliverables:**

VM-01: **Design Review (Peer Check)**
- Independent technical review by qualified checker
- Review against requirements (ER, codes, standards)
- Constructability review
- **TBD** — Review checklist and approval criteria

**Source:** Typical engineering review process

VM-02: **Dimensional Verification**
- Check dimensions for consistency across plans, elevations, sections
- Verify column grid dimensions and member sizes
- Check floor-to-floor heights and clearances
- Verify foundation/structural interface dimensions

**Source:** Standard drawing verification

VM-03: **Interdisciplinary Check (IDC)**
- Coordination with civil/site drawings (elevations, site constraints)
- Coordination with MEP drawings (PKG-22) for space and penetration conflicts
- Coordination with structural calculations (DEL-21.03) for member sizes and loads
- Coordination with specifications (DEL-21.02) for materials and systems
- **TBD** — IDC meeting schedule and coordination procedures

**Source:** Typical multi-discipline coordination; cross-references to DEL-21.02, DEL-21.03, PKG-22

VM-04: **CAD Standards Compliance Check**
- Verify layer usage per project standards
- Verify line weights and styles
- Verify text styles and annotation standards
- Verify title block and revision tracking
- **TBD** — Automated CAD checking tools (if available)

**Source:** Project CAD standards (TBD location)

VM-05: **Code Compliance Review**
- Verify compliance with NBC 2020 provisions
- Check egress routes and travel distances
- Check barrier-free design provisions
- Verify fire-rated assemblies (if required)
- **TBD** — Third-party code review (if required)

**Source:** NBC 2020 requirements

**Acceptance Criteria:**

AC-01: All drawings reviewed and approved per project quality procedures
AC-02: No unresolved IDC comments or conflicts
AC-03: Design complies with applicable codes and standards
AC-04: Drawing set is complete (no missing sheets or details)
AC-05: **TBD** — Employer review and acceptance criteria
AC-06: **TBD** — Authority having jurisdiction acceptance (building permit approval)

## Documentation

**Required Documentation Outputs:**

Per decomposition (line 513):
1. **MCC Building General Arrangements (GAs)**
   - Overall building layout, column grid, roof plan
   - Typical sheets: Site plan, floor plan, roof plan, foundation plan

2. **Floor Plans**
   - Equipment layout zones and clearances
   - Door/window locations
   - Wall types and fire separations
   - Accessibility features

3. **Elevations**
   - All building facades (North, South, East, West)
   - Material callouts and finishes
   - Window/door elevations

4. **Sections**
   - Building sections showing vertical coordination
   - Wall sections showing envelope assemblies
   - Detail sections as required

5. **Operator Shelter Drawings**
   - Shelter plans and elevations
   - Structural support details
   - Access and environmental control features

**Supporting Documentation:**

- Drawing index/list
- Abbreviations and symbols legend
- General notes and material specifications
- Door and window schedules
- Wall type and finish schedules
- Detail index (if numerous details)
- **TBD** — As-built / record drawing requirements

**Documentation Management:**

- **Revision control:** Per project document numbering system — **TBD**
- **Format:** Electronic files (CAD native + PDF) — **ASSUMPTION**
- **Naming convention:** Per project document management system — **TBD**
- **Storage location:** Project document management system — **TBD**
- **Transmittal requirements:** Per project document control procedures — **TBD**
- **Review copies:** Issued to `2_Checking/To/` per deliverable lifecycle
- **Issued copies:** Issued to `3_Issued/` upon approval per deliverable lifecycle

**Record Retention:**

- **TBD** — Retention period per project and regulatory requirements
- **TBD** — Archive procedures for design documentation

**Deliverable Lifecycle Management:**

Per `_STATUS.md`:
- Current state: INITIALIZED
- Working location: `1_Working/DEL-21.01_Building_Design_Drawing_Set/`
- Review/checking: `2_Checking/` (deliverable folder structure)
- Issued: `3_Issued/` (deliverable folder structure)

**Source:** `_STATUS.md` and deliverable folder structure per README.md
