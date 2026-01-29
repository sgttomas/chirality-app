# Datasheet: DEL-02.05 Survey Reports

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-02.05 |
| Name | Survey Reports |
| Package | PKG-02 Earthworks & Ground Improvement |
| Discipline | Civil |
| Type | Report |
| Responsible | D&B Contractor (Surveyor) |
| Current state | INITIALIZED |

## Attributes

| Attribute | Value | Specification § | Guidance § | Procedure Step |
|-----------|-------|-----------------|------------|----------------|
| Report date | **TBD** — to be established upon report issue | R6 | Data Quality | Step 20 |
| Report number | **TBD** — per D&B Contractor document control system | R6 | Data Quality | Step 15 |
| Revision | **TBD** — initial issue (Rev 0) or as revised | R6 | Data Quality | Step 18 |
| Author / organization | **TBD** — D&B Contractor or licensed surveying firm | R8 | Regulatory Compliance | Step 19 |
| Basis of report | **TBD** — field survey data, survey control network, coordinate system from ER | R2, R7 | Accuracy | Steps 5-8 |
| Survey format | **TBD** — digital file formats (CAD, GIS, point cloud), printed plan sheets | R10 | Data Quality | Step 7 |
| Survey accuracy | **TBD** — horizontal/vertical accuracy per ER specifications or survey standards | R7 | Accuracy | Step 6 |
| Coordinate system | **TBD** — project coordinate system, datum, projection per ER | R9 | Coordination | Step 2 |
| Survey control network | **TBD** — control monuments, benchmarks, reference points | R2 | Control Network | Step 3 |

## Context & Conditions

**Project Context:**
- Location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC. Source: decomposition Section 1 (location TBD).
- Contract type: Design & Build. Source: decomposition Section 1 (location TBD).
- Package scope: Site grading, excavation, filling, ground improvements, geotechnical works, surveys. Source: decomposition PKG-02 scope (location TBD).

**Scope Boundaries:**
- This decomposition covers the Contractor's scope of work only. Employer-responsible items excluded except for interface connections. Source: decomposition Section 1.2 Scope Focus (location TBD).
- Deliverable intent: Documents analysis and results for survey reports required for design verification and approvals. Source: _CONTEXT.md; decomposition DEL-02.05 entry (location TBD).

**Technical Context:**
- Operating/environmental details: **TBD** (ER will define site boundaries, existing features, coordinate system, required accuracy).
- **ASSUMPTION**: Surveys will be performed by licensed professional land surveyor.
- Coordination with DEL-02.01 (Earthworks Drawings), DEL-02.04 (Geotechnical Reports — for investigation locations), all design packages for existing conditions baseline.

## Report Content (Anticipated Artifacts mapped to Requirements)

| Report | Specification § | Guidance § | Procedure Step | Status |
|--------|-----------------|------------|----------------|--------|
| Topographic Survey Report | R1, R2, R7 | Accuracy, Completeness | Steps 5-8, 13 | **TBD** |
| Utility Locate Report | R3, R4 | Completeness | Steps 9-12, 14 | **TBD** |

### Topographic Survey Report

| Section | Content | Specification § | Status |
|---------|---------|-----------------|--------|
| Survey methodology | Equipment, methods, procedures | R2 | **TBD** |
| Survey control network | Horizontal/vertical control points, benchmarks | R2 | **TBD** |
| Coordinate system | System, datum, projection | R9 | **TBD** |
| Site topography | Contours, elevations, features | R1, R2 | **TBD** |
| Existing features | Structures, pavements, drainage, vegetation | R1, R2 | **TBD** |
| Property boundaries | Boundary lines, monuments | R1, R2 | **TBD** |
| Accuracy statement | Horizontal/vertical accuracy certification | R7, R8 | **TBD** |
| Digital survey data | CAD files, GIS data, point cloud | R10 | **TBD** |
| Survey plan sheets | Printed plans showing existing conditions | R2 | **TBD** |

### Utility Locate Report

| Section | Content | Specification § | Status |
|---------|---------|-----------------|--------|
| Investigation methodology | Records search, field locating methods | R4 | **TBD** |
| Existing utilities | Type, location, depth, owner | R3 | **TBD** |
| Utility markings | Field markings and survey coordinates | R4 | **TBD** |
| Conflict assessment | Conflicts with proposed design | R3, R4 | **TBD** |
| Limitations | Disclaimers (private utilities, depth estimates) | R4 | **TBD** |
| Utility location plans | Plan sheets showing utility locations | R4 | **TBD** |

**Configuration Notes:**
- **TBD** — details require ER volumes; ER will specify survey scope, accuracy requirements, deliverable formats, coordinate system.
- Survey reports must be compatible with CAD/BIM software used for design (e.g., AutoCAD, Civil 3D).
- Utility locates may require coordination with utility owners and third-party locating services.
- Coordination with PKG-04, PKG-05, PKG-06, PKG-08 for existing conditions in their design areas.

## Cross-Document Traceability

| Document | Key Linkages |
|----------|--------------|
| Specification.md | Requirements R1-R10 define report content; V1-V3 define verification criteria |
| Guidance.md | Principles inform accuracy, data quality, coordination; Trade-offs guide scope vs. cost |
| Procedure.md | Steps 1-20 define survey and reporting workflow; Verification implements V1-V3 |

## References

| Reference | Description | Location |
|-----------|-------------|----------|
| _CONTEXT.md | Deliverable identity, description, anticipated artifacts | This folder |
| Decomposition | PKG-02 scope, DEL-02.05 entry | `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (location TBD) |
| Specification.md | Requirements R1-R10, Verification V1-V3 | This folder |
| Guidance.md | Principles, Considerations, Trade-offs | This folder |
| Procedure.md | Steps 1-20, Verification, Records | This folder |
| _REFERENCES.md | ER volumes and reference materials | This folder (currently empty; pending) |
| DEL-02.01 | Design Drawing Set | PKG-02 |
| DEL-02.04 | Geotechnical Reports (investigation locations) | PKG-02 |
