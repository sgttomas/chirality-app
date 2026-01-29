# _DEPENDENCIES.md

## Dependency Tracking Mode
`DECLARED`

## Inbound Dependencies (this deliverable depends on)

| TargetDEL | Type | Reason | Criticality | Status |
|-----------|------|--------|-------------|--------|
| DEL-04.01 | TI | Pavement layout and section arrangement to analyze (Datasheet: "pavement sections validated by these calculations") | MEDIUM | DECLARED |
| DEL-04.02 | TI | Material properties used as calculation inputs (Datasheet: "material properties and construction requirements used as calculation inputs") | MEDIUM | DECLARED |
| DEL-02.04 | TI | Geotechnical investigation report providing subgrade CBR, soil classification, frost depth (Datasheet: "PKG-03 geotechnical deliverables... Geotechnical investigation report") | HIGH | INFERRED |
| DEL-05.01 | IF | Structure loading and elevations for pavement interface design (Datasheet: "PKG-05 structural deliverables") | MEDIUM | DECLARED |
| DEL-07.01 | IF | Track loading and vibration data for pavement design adjacent to rail works (Datasheet: "PKG-07 rail deliverables") | MEDIUM | DECLARED |

## Outbound Dependencies (other deliverables depend on this)

| SourceDEL | Type | Reason | Criticality | Status |
|-----------|------|--------|-------------|--------|
| DEL-04.01 | TI | Provides pavement thickness outputs for drawing section details (Procedure: "Handoff to DEL-04.01") | HIGH | DECLARED |
| DEL-04.02 | TI | Validates material property specifications; provides design parameter basis (Procedure: "Handoff to DEL-04.02") | HIGH | DECLARED |
| DEL-04.04 | TI | Provides target values and acceptance criteria for field testing (Procedure: "Handoff to DEL-04.04") | HIGH | DECLARED |

## Dependency Discovery Metadata
- Analyzed: 2026-01-29 15:00
- Analyzer: DEPENDENCY_DISCOVERY
- Content State: INITIALIZED (Datasheet, Specification, Guidance, Procedure populated)
- Confidence: HIGH (explicit cross-references in datasheet and procedure documents)

## Notes
- **DEL-02.04 inference**: The documents reference "Geotechnical investigation report" without specifying exact deliverable ID. DEL-02.04 (Geotechnical Report) in PKG-02 is inferred as the likely source. Human review recommended to confirm target deliverable vs. PKG-03 geotechnical scope.
- **Central calculation deliverable**: DEL-04.03 is the engineering design authority for pavement. It receives inputs from DEL-04.01 (layout) and DEL-04.02 (materials), and provides validated design outputs to all three peer deliverables.
- **Three HIGH-criticality outbound dependencies**: DEL-04.01, DEL-04.02, and DEL-04.04 all depend on DEL-04.03 calculation outputs. This makes DEL-04.03 a critical path deliverable within PKG-04.
- **Traffic loading data**: Required input from Owner/ER (not a project deliverable); flagged as TBD in calculation inputs.
- **Bidirectional coordination**: DEL-04.01/04.02 provide inputs to calculations AND receive outputs from calculations - this is a normal iterative design coordination pattern.
