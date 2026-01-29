# Datasheet: DEL-02.06 Earthworks Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-02.06 |
| Name | Earthworks Installation & Test Records |
| Package | PKG-02 Earthworks & Ground Improvement |
| Discipline | Civil |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Current state | INITIALIZED |

## Attributes

| Attribute | Value | Specification § | Guidance § | Procedure Step |
|-----------|-------|-----------------|------------|----------------|
| Record package ID | **TBD** — per D&B Contractor QA/QC document control | R8 | Document Control | Step 15 |
| Date range | **TBD** — construction activity dates (start to completion) | R8 | Real-Time Documentation | Step 15 |
| Location / area | **TBD** — earthworks zones, grid coordinates, station limits | R7, R8 | Coverage | Steps 6, 8, 10 |
| Testing / inspection method | **TBD** — field density tests, proof rolling, survey verification | R2, R4, R5 | Test Method Selection | Steps 5, 6 |
| QA/QC signoff | **TBD** — field inspector, QA/QC manager, geotechnical engineer | R9 | Approval Workflow | Steps 12-14 |
| Revision | **TBD** — initial submittal or revised per review comments | R8 | Document Control | Step 19 |
| Record format | **TBD** — field test forms, compiled record package, digital database | R8 | Real-Time Data Management | Step 4 |
| Acceptance criteria | **TBD** — compaction %, grade tolerances, proof rolling criteria | R2, R4, R5 | Coverage | Steps 1, 7 |

## Context & Conditions

**Project Context:**
- Location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC. Source: decomposition Section 1 (location TBD).
- Contract type: Design & Build. Source: decomposition Section 1 (location TBD).
- Package scope: Site grading, excavation, filling, ground improvements, geotechnical works, surveys. Source: decomposition PKG-02 scope (location TBD).

**Scope Boundaries:**
- This decomposition covers the Contractor's scope of work only. Employer-responsible items excluded except for interface connections. Source: decomposition Section 1.2 Scope Focus (location TBD).
- Deliverable intent: Provides evidence of completion, inspection, and testing for earthworks activities to demonstrate compliance with design requirements and acceptance criteria. Source: _CONTEXT.md; decomposition DEL-02.06 entry (location TBD).

**Technical Context:**
- Operating/environmental details: **TBD** (ER will define compaction requirements, testing frequency, acceptance criteria, weather constraints).
- **ASSUMPTION**: Records generated during construction by field QA/QC personnel; compiled and submitted for Employer review/acceptance.
- Coordination with DEL-02.01 (design grades), DEL-02.02 (acceptance criteria), DEL-02.03 (quantities), DEL-02.08 (testing protocols).

## Record Content (Anticipated Artifacts mapped to Requirements)

| Record Type | Specification § | Guidance § | Procedure Step | Status |
|-------------|-----------------|------------|----------------|--------|
| Compaction Test Records | R2, R3 | Real-Time Documentation, Test Method | Steps 6-7 | **TBD** |
| Proof Rolling Records | R4 | Coverage | Steps 8-9 | **TBD** |
| Survey Conformance Records | R5, R6 | Completeness | Steps 10-11 | **TBD** |

### Compaction Test Records

| Data Element | Description | Specification § |
|--------------|-------------|-----------------|
| Test location | Stationing, grid coordinates, elevation | R2 |
| Test date | Date and weather conditions | R2 |
| Soil/fill description | Material type and source | R3 |
| Test method | Nuclear density gauge, sand cone, other | R2 |
| Field results | Dry density, moisture content | R3 |
| Laboratory reference | Maximum density, optimum moisture (Proctor) | R3 |
| Percent compaction | Achieved vs. specification requirement | R3 |
| Pass/fail determination | Acceptance decision and corrective action | R3 |
| Inspector signature | Name, signature, date | R9 |
| Geotechnical review | Engineer acceptance if required | R9 |

### Proof Rolling Records

| Data Element | Description | Specification § |
|--------------|-------------|-----------------|
| Proof rolling date | Date and weather conditions | R4 |
| Area/limits | Stationing, grid coordinates | R4 |
| Equipment | Loaded truck weight, axle configuration | R4 |
| Visual observations | Deflections, rutting, pumping, soft areas | R4 |
| Pass/fail determination | Acceptance decision and remedial action | R4 |
| Inspector signature | Name, signature, date | R9 |
| Photographs | Operations and deficient areas | R4 |

### Survey Conformance Records

| Data Element | Description | Specification § |
|--------------|-------------|-----------------|
| Survey date | Date and surveyor identification | R5 |
| Location/area surveyed | Stationing, grid coordinates | R6 |
| As-built elevations | Measured grades | R5, R6 |
| Design grades | Reference from DEL-02.01 | R5, R6 |
| Grade conformance | Within tolerance or requiring correction | R6 |
| Survey data | Spot elevations, cross-sections, surface model | R6 |
| Surveyor certification | Name, signature, date | R9 |

**Configuration Notes:**
- **TBD** — details require ER volumes; ER will specify compaction requirements, testing frequency per ASTM, acceptance criteria, record format/submittal requirements.
- Records organized by earthworks zone, construction sequence, or activity type.
- Coordination with DEL-02.09 (Compaction Verification Plan) for testing methodology.
- Coordination with PKG-04, PKG-05, PKG-06 for subgrade acceptance before subsequent work.

## Cross-Document Traceability

| Document | Key Linkages |
|----------|--------------|
| Specification.md | Requirements R1-R9 define record content; V1-V3 define verification criteria |
| Guidance.md | Principles inform record quality, completeness, traceability, timeliness |
| Procedure.md | Steps 1-22 define testing and recording workflow; Verification implements V1-V3 |

## References

| Reference | Description | Location |
|-----------|-------------|----------|
| _CONTEXT.md | Deliverable identity, description, anticipated artifacts | This folder |
| Decomposition | PKG-02 scope, DEL-02.06 entry | `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (location TBD) |
| Specification.md | Requirements R1-R9, Verification V1-V3 | This folder |
| Guidance.md | Principles, Considerations, Trade-offs | This folder |
| Procedure.md | Steps 1-22, Verification, Records | This folder |
| _REFERENCES.md | ER volumes and reference materials | This folder (currently empty; pending) |
| DEL-02.01 | Design Drawing Set (design grades) | PKG-02 |
| DEL-02.02 | Technical Specification (acceptance criteria) | PKG-02 |
| DEL-02.04 | Geotechnical Reports (compaction requirements) | PKG-02 |
| DEL-02.08 | Sampling & Testing Program (testing protocols) | PKG-02 |
| DEL-02.09 | Compaction Verification Plan | PKG-02 |
