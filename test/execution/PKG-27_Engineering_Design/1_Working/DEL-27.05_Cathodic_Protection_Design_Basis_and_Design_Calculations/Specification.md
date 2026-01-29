# Specification: DEL-27.05 Cathodic Protection Design Basis & Design Calculations

## Scope

Defines requirements for **Cathodic Protection Design Basis & Design Calculations** within **PKG-27 Engineering Design**.

**Purpose:** Provides engineering basis and sizing/verification calculations for cathodic protection system to prevent corrosion of buried and submerged steel structures.

**Artifacts:** CP design basis, anode layout calculations, current demand calculations, design drawings (where applicable)

**Structures protected:** Storage tanks, buried piping, marine structures (piles, sheet piles, loading platforms)

**Source:** _CONTEXT.md; Datasheet.md

## Requirements

### Functional Requirements

**FR-1: CP System Selection** - Select ICCP or sacrificial anode system based on structure types, environment, lifecycle cost, maintenance considerations
**FR-2: Current Demand Calculation** - Calculate total protection current for all structures per NACE SP0169 or CSA Z662
**FR-3: Anode Design** - Size and locate anodes (sacrificial or impressed current) to provide adequate protection over design life
**FR-4: Monitoring Provisions** - Specify test stations and monitoring equipment for CP system performance verification

**Source:** Datasheet.md; **ASSUMPTION**: Standard CP functional requirements per NACE

### Performance Requirements

**PR-1: Protection Criteria** - CP system shall achieve and maintain protection potentials per NACE SP0169 or CSA Z662 (typically -850 mV vs. Cu/CuSO₄ for steel in soil)
**PR-2: Design Life** - CP system designed for **TBD** years (typical 25-30 years ICCP; 20-25 years sacrificial)
**PR-3: Uniform Distribution** - Current distribution shall protect all structure surfaces; no under-protected areas

**Source:** **ASSUMPTION**: CP performance criteria per NACE standards; **TBD** — Project-specific design life

### Interface Requirements

**IR-1:** Coordinate with structural design (PKG-05, PKG-06, PKG-08) for structure surface areas, embedment details
**IR-2:** Coordinate with piping design (PKG-14) for buried piping routes, materials, coatings
**IR-3:** Coordinate with electrical design (PKG-17) for rectifier power supply (if ICCP)
**IR-4:** Coordinate with coating specifications for coating efficiency assumptions

**Source:** Datasheet.md; **ASSUMPTION**: Multi-discipline coordination essential for CP design

### Quality Requirements

**QR-1: Calculation Quality** - Calculations per NACE methodology; independent check by qualified CP specialist
**QR-2: Design Code Compliance** - Comply with NACE SP0169, CSA Z662, and applicable codes
**QR-3: Site Data Quality** - Soil/water resistivity data from qualified testing per NACE TM0497

**Source:** **ASSUMPTION**: Engineering calculation quality per ISO 9001 and NACE

## Standards

- NACE SP0169, NACE TM0497, CSA Z662, ISO 15589 series, DNV RP-B401 (marine), ISO 9001

**Source:** Datasheet.md

## Verification

- Independent check by qualified CP specialist
- Verify against NACE/CSA criteria
- Sensitivity analysis for key parameters (resistivity, current density, coating efficiency)
- Field testing after installation to verify design assumptions

**Source:** **ASSUMPTION**: Standard CP verification approach

## Documentation

**Outputs:** CP design basis, current demand calculations, anode layout calculations, design drawings
**Format:** Calculation sheets (hand calc or software output), drawings per project CAD standards
**Approvals:** CP Specialist (originator), Senior CP Specialist or P.Eng. (checker), Discipline Lead (approver)

**Source:** Datasheet.md; **ASSUMPTION**: Standard calculation documentation per project QMS
