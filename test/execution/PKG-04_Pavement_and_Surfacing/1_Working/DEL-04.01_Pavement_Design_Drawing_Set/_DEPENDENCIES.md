# _DEPENDENCIES.md

## Dependency Tracking Mode
`DECLARED`

## Inbound Dependencies (this deliverable depends on)

| TargetDEL | Type | Reason | Criticality | Status |
|-----------|------|--------|-------------|--------|
| DEL-04.02 | TI | Material and workmanship specifications for drawing annotations (Specification R2.1: "shall reference DEL-04.02 clauses") | HIGH | DECLARED |
| DEL-04.03 | TI | Pavement layer thicknesses and design parameters for section drawings (Datasheet: "Design Parameters TBD pending DEL-04.03") | HIGH | DECLARED |
| DEL-02.05 | TI | Geotechnical investigation and survey data for subgrade design basis (Procedure: "Site survey data, geotechnical report") | HIGH | INFERRED |
| DEL-03.01 | IF | Surface drainage tie-in elevations at catch basins and manholes (Guidance P2: "Surface drainage slopes must tie into catch basin invert elevations") | MEDIUM | DECLARED |
| DEL-05.01 | IF | Structure finished floor elevations for pavement-to-building grade coordination (Guidance P2: "Pavement grades at building perimeters must match finished floor elevations") | MEDIUM | DECLARED |
| DEL-07.01 | IF | Track top-of-rail elevations and clearance envelopes for rail crossing details (Guidance P2: "Pavement elevations at rail crossings must accommodate track top-of-rail") | MEDIUM | DECLARED |
| DEL-08.01 | IF | Berth elevations and wharf edge details for pavement termination limits (Guidance P2: "Pavement termination at wharf edge must coordinate with berth elevations") | MEDIUM | DECLARED |

## Outbound Dependencies (other deliverables depend on this)

| SourceDEL | Type | Reason | Criticality | Status |
|-----------|------|--------|-------------|--------|
| DEL-04.04 | TI | Provides drawing sections and tolerances as basis for field testing acceptance criteria (Datasheet: "Drawing section details establish the acceptance criteria for DEL-04.04") | HIGH | DECLARED |

## Dependency Discovery Metadata
- Analyzed: 2026-01-29 14:30
- Analyzer: DEPENDENCY_DISCOVERY
- Content State: INITIALIZED (Datasheet, Specification, Guidance, Procedure populated)
- Confidence: HIGH (explicit cross-references in specification and guidance documents)

## Notes
- **DEL-02.05 inference**: The documents reference "geotechnical investigation" and "site survey data" without explicitly naming a deliverable. DEL-02.05 (Survey Report) is inferred as the likely source based on PKG-02 (Earthworks & Ground Improvement) scope. Human review recommended to confirm target deliverable.
- **Cross-package interfaces (PKG-03, PKG-05, PKG-07, PKG-08)**: These are bidirectional coordination interfaces. While DEL-04.01 depends on elevation data from these packages, those packages may also need pavement extents/grades from DEL-04.01. Outbound edges to these packages should be discovered when analyzing those deliverables.
- **OBJ-8 (Future Expandability)**: Phase 2 expansion provisions require coordination with future design input. No explicit deliverable dependency identified; flagged as ASSUMPTION in Datasheet pending Phase 2 design.
