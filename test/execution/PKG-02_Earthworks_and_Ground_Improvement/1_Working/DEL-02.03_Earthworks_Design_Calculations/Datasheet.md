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

| Attribute | Value | Specification § | Guidance § | Procedure Step |
|-----------|-------|-----------------|------------|----------------|
| Calculation package ID | **TBD** — to be assigned per project document numbering system | R6 | P2 | Step 2.4 |
| Calculation method | **TBD** — manual calculations, spreadsheet, geotechnical software; **ASSUMPTION**: combination | R5 | P1, Trade-offs | Step 3 |
| Design inputs | **TBD** — DEL-02.04 (geotechnical), DEL-02.05 (survey), ER design criteria | R2, R3 | P4 | Step 1 |
| Software / tools | **TBD** — e.g., AutoCAD Civil 3D (cut/fill), geotechnical analysis software (bearing capacity) | R5 | P1, Trade-offs | Step 3 |
| Check status | **TBD** — independent check required per R6 | R6 | P1 | Step 4.4 |
| Revision | **TBD** — to be tracked per document control (R6) | R6 | P2 | Step 5 |
| Calculation format | **TBD** — typically structured per standard calculation template; **ASSUMPTION** | R5 | P2 | Step 2.3 |

## Context & Conditions

**Project Context:**
- Location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC. Source: decomposition Section 1 (location TBD).
- Contract type: Design & Build. Source: decomposition Section 1 (location TBD).
- Package scope: Site grading, excavation, filling, ground improvements, geotechnical works, surveys. Source: decomposition PKG-02 scope (location TBD).

**Scope Boundaries:**
- This decomposition covers the Contractor's scope of work only. Employer-responsible items excluded except for interface connections. Source: decomposition Section 1.2 Scope Focus (location TBD).
- Deliverable intent: Provides the engineering basis and sizing/verification calculations for earthworks. Source: _CONTEXT.md; decomposition DEL-02.03 entry (location TBD).

**Design Context:**
- Calculations provide engineering basis for DEL-02.01 (Design Drawing Set) and DEL-02.02 (Technical Specification).
- Calculation inputs from DEL-02.04 (Geotechnical Reports) and DEL-02.05 (Survey Reports).
- Design criteria: **TBD** — pending ER requirements.
- Loading conditions: **TBD** — structural loads, equipment loads, pavement loads from adjacent packages.

## Calculation Content (Anticipated Artifacts mapped to Requirements)

| Section | Purpose | Specification § | Guidance § | Procedure Step | Status |
|---------|---------|-----------------|------------|----------------|--------|
| 1. Cut/Fill Quantity Calculations | Determine earthwork volumes for site grading | R2 | P1, P2, P3, P4 | Step 3.1 | **TBD** |
| 2. Bearing Capacity Calculations | Verify soil bearing capacity for proposed loads | R3 | P1, P2, P3, P4 | Step 3.2 | **TBD** |

### 1. Cut/Fill Quantity Calculations (R2)

**Inputs:**

| Input | Source | Status |
|-------|--------|--------|
| Existing topography | DEL-02.05 (Survey Reports) | **TBD** |
| Proposed finish grades | DEL-02.01 (Design Drawing Set) | **TBD** |
| Site limits and grading extents | DEL-02.01 | **TBD** |

**Method:**
- **TBD** — typical methods: cross-section method, average end area, digital terrain modeling (DTM)
- Software: **TBD** — e.g., AutoCAD Civil 3D, or manual calculation

**Outputs:**

| Output | Value | Units |
|--------|-------|-------|
| Total cut volume | **TBD** | m³ |
| Total fill volume | **TBD** | m³ |
| Net cut/fill balance | **TBD** | m³ |
| Haul quantities/distances | **TBD** | m³·km |
| Volumetric breakdown by zone | **TBD** | m³ |

**Coordination:** Quantities support DEL-02.01 (drawings), DEL-02.02 (specification), and field execution planning.

### 2. Bearing Capacity Calculations (R3)

**Inputs:**

| Input | Source | Status |
|-------|--------|--------|
| Soil parameters (c, φ, γ) | DEL-02.04 (Geotechnical Reports) | **TBD** |
| Groundwater level | DEL-02.04 | **TBD** |
| Loading conditions | PKG-04, PKG-05, PKG-06 | **TBD** |
| Foundation depths/configurations | Design | **TBD** |

**Method:**
- **TBD** — typical methods: Terzaghi, Meyerhof, Canadian Foundation Engineering Manual
- Software: **TBD** — geotechnical analysis software, spreadsheet calculations

**Outputs:**

| Output | Value | Units |
|--------|-------|-------|
| Ultimate bearing capacity | **TBD** | kPa |
| Factor of safety | **TBD** | — |
| Allowable bearing capacity | **TBD** | kPa |
| Settlement estimates | **TBD** | mm |
| Ground improvement requirements | **TBD** | — |

**Coordination:** Results inform DEL-02.01 (ground improvement zones), DEL-02.02 (ground improvement specification), DEL-02.04 (geotechnical design).

**Configuration Notes:**
- All calculations shall be traceable to design inputs, assumptions, and methods (R1, R5).
- Calculations shall support design shown in DEL-02.01 and requirements in DEL-02.02.
- Calculations require independent checking per QA/QC requirements.
- Details require ER volumes, geotechnical data, and design criteria (currently **TBD**).

## Cross-Document Traceability

| Document | Key Linkages |
|----------|--------------|
| Specification.md | Requirements R1-R6 define mandatory calculation scope; V1-V4 define verification criteria |
| Guidance.md | Principles P1-P4 inform calculation accuracy, traceability, conservatism, coordination |
| Procedure.md | Steps 1-5 define calculation workflow; Step 4 implements independent checking (V4) |

## References

| Reference | Description | Location |
|-----------|-------------|----------|
| _CONTEXT.md | Deliverable identity, description, anticipated artifacts | This folder |
| Decomposition | PKG-02 scope, DEL-02.03 entry | `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (location TBD) |
| Specification.md | Requirements R1-R6, Verification V1-V4 | This folder |
| Guidance.md | Principles P1-P4, Considerations, Trade-offs | This folder |
| Procedure.md | Steps 1-5, Verification, Records | This folder |
| _REFERENCES.md | ER volumes and reference materials | This folder (currently empty; pending) |
| DEL-02.01 | Design Drawing Set | PKG-02 |
| DEL-02.02 | Technical Specification | PKG-02 |
| DEL-02.04 | Geotechnical Reports | PKG-02 |
| DEL-02.05 | Survey Reports | PKG-02 |
