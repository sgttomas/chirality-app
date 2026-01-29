# _DEPENDENCIES.md

## Dependency Tracking Mode
`DECLARED`

## Inbound Dependencies (this deliverable depends on)

| TargetDEL | Type | Reason | Criticality | Status |
|-----------|------|--------|-------------|--------|
| DEL-00.01 | TI | Temporary facility locations for water routing (Specification.md line 60) | MEDIUM | DECLARED |
| DEL-00.02 | TI | Materials and installation standards (Specification.md line 60) | MEDIUM | DECLARED |

## Outbound Dependencies (other deliverables depend on this)

| SourceDEL | Type | Reason | Criticality | Status |
|-----------|------|--------|-------------|--------|
| *(To be discovered when analyzing downstream deliverables)* |

## Dependency Discovery Metadata
- Analyzed: 2026-01-29 06:45
- Analyzer: DEPENDENCY_DISCOVERY
- Content State: INITIALIZED
- Confidence: MEDIUM

## Notes
- Both dependencies are intra-package (within PKG-00)
- Water routing depends on knowing facility locations from drawings
- Installation standards come from technical specification
