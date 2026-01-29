# Datasheet: DEL-11.03 Marine Loading Design Calculations

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-11.03 |
| Name | Marine Loading Design Calculations |
| Package | PKG-11 Marine Loading System |
| Discipline | Process |
| Type | Calculation |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Objectives Mapping

This deliverable contributes to the following project objectives (per decomposition Section 6):
- **OBJ-1 Safe & Reliable Operation** — calculations verify loading arm envelope for safe vessel approach/departure
- **OBJ-2 Throughput Capacity (1,000,000 MT/annum)** — calculations verify system sizing supports design throughput
- **OBJ-4 Operational Flexibility** — envelope calculations confirm accommodation of diverse vessel sizes
- **OBJ-7 Environmental Protection** — drainage/containment calculations verify spill management capacity

## Attributes

| Attribute | Value |
|-----------|-------|
| Calculation register/index | **TBD** — list of calculations with IDs, titles, revisions |
| Tools/software used | **TBD** — spreadsheet/CAD/specialty software per calculation type |
| Governing codes/standards | **TBD** — confirm per ER and project code register |
| Load cases/scenarios | **TBD** — per design basis and operating envelope |
| Revision | **TBD** |
| Classification | **TBD** (e.g., IFC/IFA per project conventions) |

## Conditions

**Operating / Environmental Context:**

Provides the engineering basis and sizing/verification calculations for the marine loading system, demonstrating compliance with design requirements and deriving constraints for layout drawings.

**Design basis (to be confirmed from ER and DEL-11.02):**

| Parameter | Value | Source |
|-----------|-------|--------|
| Product | Canola oil (refined vegetable oil) | ER **TBD** |
| Design loading rate | **TBD** m³/hr | DEL-11.02 §3 |
| Operating temperature | **TBD** (typical 20–60°C) | DEL-11.02 §3 |
| Design pressure | **TBD** barg | DEL-11.02 §3 |
| Ambient temperature range | **TBD** (approx. –10°C to +35°C) | Site data |
| Design vessel range | **TBD** (manifold height/position ranges) | ER / berth data |
| Rainfall design storm | **TBD** (for drainage calculations) | Site data |
| Nitrogen supply pressure | **TBD** barg | DEL-18 utilities |
| Design life | **TBD** — **ASSUMPTION**: 25 years minimum | ER **TBD** |

## Construction

**Calculation package contents (from decomposition):**

| Calculation Topic | Purpose | Key Inputs | Key Outputs |
|-------------------|---------|------------|-------------|
| Loading arm reach/envelope | Verify arm reach accommodates design vessel range | Berth geometry, vessel manifold data, OEM arm data (DEL-11.06) | Operating envelope plot, clearance zones, reach requirements |
| Drainage calculations | Size drainage/containment for spill scenarios | Catchment areas, rainfall criteria, sump capacity | Drain sizing, sump capacity, pump requirements (if any) |
| Nitrogen purge calculations | Size nitrogen supply for purge/inert operations | System volume, target O₂ concentration, N₂ supply conditions | Required N₂ flow, purge time, supply capacity |

**Additional calculations (if required — TBD):**
- Pipe stress analysis (double-walled pipe thermal/seismic) — may be in DEL-14 or here
- ERC activation envelope (vessel drift limits) — OEM data or independent check
- Sump pump sizing (if pumped drainage) — linked to drainage calc

## Interfaces (Coordination Items)

Dependencies are coordinated externally (NOT_TRACKED). Calculations shall explicitly state their inputs and sources:

| Interface | Source/Adjacent Deliverable | Calculation Affected |
|-----------|----------------------------|---------------------|
| Design basis parameters | DEL-11.02 Technical Specification | All calculations |
| Loading arm OEM data | DEL-11.06 OEM Qualification | Envelope calculations |
| Berth/vessel data | Marine studies, ER, PKG-08 | Envelope calculations |
| Rainfall/drainage criteria | Site data, PKG-03 Drainage | Drainage calculations |
| Nitrogen supply conditions | DEL-18.xx (PKG-18 Utilities) | Nitrogen purge calculations |
| Layout constraints | DEL-11.01 Drawing Set | Output constraints |
| Pipe stress inputs | DEL-14.xx (PKG-14 Piping) | Expansion/stress calcs (if in scope) |

## Cross-Document Links

| Document | Link Point |
|----------|------------|
| Datasheet.md (this file) | Calculation attributes and design basis summary |
| Specification.md (DEL-11.03) | Calculation package requirements and acceptance criteria |
| Guidance.md (DEL-11.03) | Engineering rationale and methodology guidance |
| Procedure.md (DEL-11.03) | Production workflow and verification checklist |
| DEL-11.01 Drawing Set | Receives envelope/clearance constraints from calculations |
| DEL-11.02 Technical Specification | Provides design basis inputs; receives verified sizing outputs |
| DEL-11.04 Data Sheet Package | Receives duty points and verified values |
| DEL-11.06 OEM Qualification | Provides OEM arm data as calculation inputs |

## Deliverable Acceptance (Minimum)

| Acceptance Criterion | Verification Method | Reference |
|---------------------|---------------------|-----------|
| Calculation register provided with IDs, revisions, sign-off | Document review | Specification.md §Requirements |
| Each calculation includes: purpose, inputs, assumptions, method, results, conclusions | Completeness check | Specification.md §Requirements |
| Input sources documented and traceable | Traceability review | Specification.md §Requirements |
| Assumptions explicitly labeled and tracked | Completeness check | Guidance.md §Principles |
| Output constraints carried into DEL-11.01/11.02 | Cross-reference check | Procedure.md §Steps |
| Independent check completed | Check records | Procedure.md §Verification |

## References

- `_REFERENCES.md` — applicable reference document list
- `0_References/` — package reference materials
- Decomposition: `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (PKG-11 / DEL-11.03)
- Employer's Requirements: **TBD** (clause references pending extraction)
- Applicable standards: **TBD** (confirm per ER and project code register)
- `_DEPENDENCIES.md` — NOT_TRACKED (dependencies coordinated externally)
