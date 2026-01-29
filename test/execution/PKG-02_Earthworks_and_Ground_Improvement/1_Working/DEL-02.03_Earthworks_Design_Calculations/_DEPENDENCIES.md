# Dependencies: DEL-02.03 Earthworks Design Calculations

## Dependency Tracking Mode
`DECLARED`

## Inbound Dependencies (this deliverable depends on)

| TargetDEL | Type | Reason | Criticality | Status |
|-----------|------|--------|-------------|--------|
| DEL-02.04 | TI | Geotechnical parameters (c, φ, γ) and bearing capacity recommendations for bearing capacity calculations (Datasheet, Procedure 1.2) | HIGH | DECLARED |
| DEL-02.05 | TI | Topographic survey data for existing terrain in cut/fill volume calculations (Datasheet, Procedure 1.3) | HIGH | DECLARED |
| DEL-02.01 | IF | Proposed finish grades for cut/fill limits; mutual design coordination (Procedure 1.4) | MEDIUM | DECLARED |
| DEL-05.01 | TI | Loading conditions from concrete structures for bearing capacity design basis (Datasheet) | MEDIUM | INFERRED |
| DEL-06.01 | TI | Loading conditions from structural steel for bearing capacity design basis (Datasheet) | MEDIUM | INFERRED |

## Outbound Dependencies (other deliverables depend on this)

| SourceDEL | Type | Reason | Criticality | Status |
|-----------|------|--------|-------------|--------|
| DEL-02.01 | TI | Cut/fill quantities form design basis for cut/fill plans | HIGH | DECLARED |
| DEL-02.02 | TI | Design calculations for performance criteria and settlement limits | HIGH | DECLARED |

## Dependency Discovery Metadata
- Analyzed: 2026-01-29 06:15
- Analyzer: DEPENDENCY_DISCOVERY
- Content State: INITIALIZED
- Confidence: MEDIUM (explicit references to DEL-02.04, DEL-02.05; cross-package loads inferred)

## Notes
- Upgraded from NOT_TRACKED to DECLARED
- Cross-package dependencies: DEL-05.01 (PKG-05 Concrete Structures), DEL-06.01 (PKG-06 Structural Steelwork) for loading conditions
- Mutual coordination with DEL-02.01 (calcs inform drawings, drawings provide finish grades)
- Calculations are central to the PKG-02 design workflow: survey→geotech→calcs→drawings/specs
