# _DEPENDENCIES.md

## Dependency Tracking Mode
`DECLARED`

## Inbound Dependencies (this deliverable depends on)

| TargetDEL | Type | Reason | Criticality | Status |
|-----------|------|--------|-------------|--------|
| DEL-04.01 | IF | Drawing elements (sections, details, tolerances) this specification governs (Specification R2.1: "cross-referenced to DEL-04.01") | MEDIUM | DECLARED |
| DEL-04.03 | TI | Calculation outputs for material properties, design parameters, and layer thicknesses (Specification R2.2: "cross-referenced to DEL-04.03 calculation sheet") | HIGH | DECLARED |
| DEL-03.01 | IF | Utility trench backfill compaction and pavement restoration coordination (Specification R1.4: "PKG-03 Interfaces") | MEDIUM | DECLARED |
| DEL-05.01 | IF | Structure-to-pavement transitions and foundation protection coordination (Specification R1.4: "PKG-05 Interfaces") | MEDIUM | DECLARED |
| DEL-07.01 | IF | Rail crossing embedment, track elevation coordination (Specification R1.4: "PKG-07 Interfaces") | MEDIUM | DECLARED |
| DEL-08.01 | IF | Pavement termination at wharf edge, loading compatibility coordination (Specification R1.4: "PKG-08 Interfaces") | MEDIUM | DECLARED |

## Outbound Dependencies (other deliverables depend on this)

| SourceDEL | Type | Reason | Criticality | Status |
|-----------|------|--------|-------------|--------|
| DEL-04.01 | TI | Provides material and tolerance specification clauses for drawing annotations (Datasheet: "this specification governs" drawing elements) | MEDIUM | DECLARED |
| DEL-04.04 | TI | Provides testing requirements, acceptance criteria, and non-conformance procedures (Specification R2.3: "cross-referenced to DEL-04.04 test records") | HIGH | DECLARED |

## Dependency Discovery Metadata
- Analyzed: 2026-01-29 14:45
- Analyzer: DEPENDENCY_DISCOVERY
- Content State: INITIALIZED (Datasheet, Specification, Guidance, Procedure populated)
- Confidence: HIGH (explicit cross-references in specification requirements sections)

## Notes
- **Mutual dependency with DEL-04.01**: Specification and drawings are tightly coupled - drawings show what is built, specification states how it shall be built. This is a normal design documentation coordination pattern.
- **Cross-package interfaces (PKG-03, PKG-05, PKG-07, PKG-08)**: Specification R1.4 explicitly requires interface coordination clauses with these packages. These are bidirectional coordination interfaces.
- **DEL-04.03 is the design authority**: Material properties and pavement sections specified in DEL-04.02 are validated by DEL-04.03 calculations (HIGH criticality dependency).
- **DEL-04.04 is downstream consumer**: Test records document conformance to specification requirements (HIGH criticality outbound dependency).
