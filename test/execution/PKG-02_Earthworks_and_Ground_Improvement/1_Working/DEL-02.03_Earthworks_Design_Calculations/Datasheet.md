# Datasheet: DEL-02.03 Earthworks Design Calculations

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-02.03 |
| Name | Earthworks Design Calculations |
| Package | PKG-02 Earthworks & Ground Improvement |
| Discipline | Civil |
| Type | Calculation |
| Responsible | D&B Contractor |
| Current state | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Calculation package ID | **TBD** — to be assigned per project document numbering system |
| Calculation method | **TBD** — manual calculations, spreadsheet, geotechnical software; **ASSUMPTION**: combination |
| Design inputs | **TBD** — DEL-02.04 (geotechnical data), DEL-02.05 (survey data), ER design criteria |
| Software / tools | **TBD** — e.g., AutoCAD Civil 3D (cut/fill), geotechnical analysis software (bearing capacity) |
| Check status | **TBD** — independent check required per R5 |
| Revision | **TBD** — to be tracked per document control (R6) |
| Calculation format | **TBD** — typically structured per standard calculation template; **ASSUMPTION** |

## Context & Conditions

**Project Context:**
- Location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC. Source: decomposition Section 1 (location TBD).
- Contract type: Design & Build. Source: decomposition Section 1 (location TBD).
- Package scope: Site grading, excavation, filling, ground improvements, geotechnical works, surveys. Source: decomposition PKG-02 scope (location TBD).

**Scope Boundaries:**
- This decomposition covers the Contractor's scope of work only. Employer-responsible items (permits obtained by Employer, nitrogen skid supply) are excluded except for interface connections. Source: decomposition Section 1.2 Scope Focus (location TBD).
- Deliverable intent: Provides the engineering basis and sizing/verification calculations for earthworks. Source: _CONTEXT.md; decomposition DEL-02.03 entry (location TBD).

**Design Context:**
- Calculations provide engineering basis for DEL-02.01 (Design Drawing Set) and DEL-02.02 (Technical Specification).
- Calculation inputs from DEL-02.04 (Geotechnical Reports) and DEL-02.05 (Survey Reports).
- Design criteria: **TBD** — pending ER requirements.
- Loading conditions: **TBD** — structural loads, equipment loads, pavement loads from adjacent packages.

## Calculation Content (Anticipated Artifacts mapped to Requirements)

The following calculation packages are anticipated, mapped to Specification requirements:

### 1. Cut/Fill Quantity Calculations (R2)
**Purpose:** Determine earthwork volumes for site grading, excavation, and fill placement.

**Inputs:**
- Existing topography from DEL-02.05 (Survey Reports)
- Proposed finish grades from DEL-02.01 (Design Drawing Set)
- Site limits and grading extents
- **TBD** — detailed input data pending survey and design

**Method:**
- **TBD** — typical methods: cross-section method, average end area, digital terrain modeling (DTM)
- Software: **TBD** — e.g., AutoCAD Civil 3D, or manual calculation

**Outputs:**
- Total cut volume (m³ or yd³)
- Total fill volume (m³ or yd³)
- Net cut/fill balance
- Haul quantities and distances (if applicable)
- Volumetric breakdown by zone or phase

**Coordination:** Quantities support DEL-02.01 (drawings), DEL-02.02 (specification), and field execution planning.

### 2. Bearing Capacity Calculations (R3)
**Purpose:** Verify soil bearing capacity to support proposed loads (pavements, structures, equipment).

**Inputs:**
- Soil parameters from DEL-02.04 (Geotechnical Reports): soil classification, strength parameters (cohesion, friction angle), groundwater level
- Loading conditions: **TBD** — pavement loads (PKG-04), equipment loads, structural loads (PKG-05, PKG-06)
- Foundation depths and configurations
- **TBD** — detailed input data pending geotechnical investigation

**Method:**
- **TBD** — typical methods: Terzaghi bearing capacity equations, Meyerhof equations, Canadian Foundation Engineering Manual, or applicable geotechnical codes
- Software: **TBD** — e.g., geotechnical analysis software, spreadsheet calculations

**Outputs:**
- Ultimate bearing capacity (kPa or psf)
- Allowable bearing capacity (with factor of safety)
- Settlement estimates (immediate and consolidation)
- Bearing capacity verification for proposed design
- Ground improvement requirements (if bearing capacity is insufficient)

**Coordination:** Results inform DEL-02.01 (ground improvement zones), DEL-02.02 (ground improvement specification), DEL-02.04 (geotechnical design).

**Configuration Notes:**
- All calculations shall be traceable to design inputs, assumptions, and methods (R1, R5).
- Calculations shall support design shown in DEL-02.01 and requirements in DEL-02.02.
- Calculations require independent checking per QA/QC requirements.
- Details require ER volumes, geotechnical data, and design criteria (currently **TBD**).

## Cross-Document Alignment

- **Specification.md:** Requirements R1-R6 define the mandatory calculation scope (cut/fill, bearing capacity), design basis, and verification requirements.
- **Guidance.md:** Provides principles for calculation accuracy, traceability, design conservatism, and coordination with design and construction deliverables.
- **Procedure.md:** Defines the calculation workflow and verification steps (Steps 1-5) to ensure completeness and accuracy against R1-R6.

## References

- _CONTEXT.md: Deliverable identity, description, and anticipated artifacts.
- Decomposition file: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — PKG-02 scope, DEL-02.03 entry (location TBD).
- Specification.md: Requirements R1-R6 and verification items V1-V4.
- Guidance.md: Calculation principles and considerations.
- Procedure.md: Calculation workflow and verification steps.
- _REFERENCES.md: Currently empty; ER volumes and reference materials pending.
- Related deliverables: DEL-02.01 (Design Drawing Set), DEL-02.02 (Technical Specification), DEL-02.04 (Geotechnical Reports), DEL-02.05 (Survey Reports).
