# Specification: DEL-14.03 Process Piping Design Calculations

## Scope

This specification defines the requirements for **Process Piping Design Calculations** within **PKG-14 Process Piping**.

**Description** (source: Decomposition DEL-14.03; attributes: Datasheet.md Calculation Type; rationale: Guidance.md Purpose): Provides the engineering basis and sizing/verification calculations for process piping.

**Calculation outputs** (source: Decomposition DEL-14.03; attributes: Datasheet.md Calculation Sections; construction: Datasheet.md Construction section; procedure: Procedure.md Steps 1-3):
- Pipe sizing calculations (hydraulic analysis) (construction: Datasheet.md Construction item 1; procedure: Procedure.md Step 1; examples: Guidance.md Examples - Typical pipe sizing)
- Stress analysis (sustained, occasional, thermal loads per ASME B31.3) (construction: Datasheet.md Construction item 2; procedure: Procedure.md Step 2; examples: Guidance.md Examples - Typical stress analysis)
- Flexibility analysis (thermal expansion per ASME B31.3) (construction: Datasheet.md Construction item 3; procedure: Procedure.md Step 3; examples: Guidance.md Examples - Typical flexibility analysis)

**Piping systems covered** (source: Decomposition PKG-14 Scope; construction: Datasheet.md Construction item 1; referenced in DEL-14.01):
- Railcar unloading headers, marine loading export lines, recycle lines, nitrogen distribution, tank piping

## Requirements

### Functional Requirements

**Pipe Sizing Calculations** (construction: Datasheet.md Construction item 1; rationale: Guidance.md Principles item 1; procedure: Procedure.md Step 1):
- FR-1: Calculate pipe diameters to support 1,000,000 MT/annum throughput (source: OBJ-2; conditions: Datasheet.md Flow rates; rationale: Guidance.md Principles item 1; procedure: Procedure.md Step 1; verification: Verification - Acceptance criteria; cross-reference DEL-14.01, DEL-14.04)
- FR-2: Determine flow velocities and pressure drops for each piping system (construction: Datasheet.md Construction item 1 - Outputs; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations - Pipe Sizing; procedure: Procedure.md Step 1; verification: Verification - Acceptance criteria)
- FR-3: Verify velocities within acceptable limits (avoid erosion, water hammer, excessive pressure drop) (construction: Datasheet.md Construction item 1 - Outputs; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations - Pipe Sizing; procedure: Procedure.md Step 1; verification: Verification - Acceptance criteria; typical range 1.5-3.0 m/s)
- FR-4: Support operational flexibility (direct rail-to-ship and tank storage modes per OBJ-4) (considerations: Guidance.md Considerations - Pipe Sizing; procedure: Procedure.md Step 1; referenced in DEL-14.01)

**Stress Analysis** (construction: Datasheet.md Construction item 2; rationale: Guidance.md Principles items 2, 4; procedure: Procedure.md Step 2):
- FR-5: Verify piping and supports comply with ASME B31.3 stress limits under all load combinations (code: Datasheet.md Design Code; construction: Datasheet.md Construction item 2; rationale: Guidance.md Principles item 2; performance: PR-6; procedure: Procedure.md Step 2; verification: Verification - Acceptance criteria; cross-reference DEL-14.01, DEL-14.02)
- FR-6: Calculate pipe support loads for coordination with structural design (construction: Datasheet.md Construction item 2 - Outputs; rationale: Guidance.md Principles item 4; interface: IR-6; procedure: Procedure.md Step 2; verification: Verification - Acceptance criteria; cross-reference PKG-05, PKG-06, DEL-14.01)
- FR-7: Calculate equipment nozzle loads for coordination with equipment packages (construction: Datasheet.md Construction item 2 - Outputs; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Stress Analysis; interface: IR-5; procedure: Procedure.md Step 2; verification: Verification - Acceptance criteria; cross-reference PKG-13, PKG-15, PKG-16)

**Flexibility Analysis** (construction: Datasheet.md Construction item 3; rationale: Guidance.md Principles item 3; procedure: Procedure.md Step 3):
- FR-8: Analyze thermal expansion and verify thermal stresses within ASME B31.3 allowables (code: Datasheet.md Design Code; construction: Datasheet.md Construction item 3; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Flexibility Analysis; procedure: Procedure.md Step 3; verification: Verification - Acceptance criteria; cross-reference DEL-14.01, DEL-14.02)
- FR-9: Verify equipment nozzle loads from thermal expansion within vendor allowables (construction: Datasheet.md Construction item 3 - Outputs; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Flexibility Analysis; interface: IR-5; procedure: Procedure.md Step 3; verification: Verification - Acceptance criteria)
- FR-10: Identify mitigation measures if stresses/loads excessive (expansion loops, expansion joints, spring hangers) (construction: Datasheet.md Construction item 3 - Outputs; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Flexibility Analysis; trade-offs: Guidance.md Trade-offs item 3; procedure: Procedure.md Step 3; cross-reference DEL-14.01, DEL-14.02)

### Performance Requirements

**Calculation accuracy** (rationale: Guidance.md Principles items 1, 2, 3; quality: QR-2; procedure: Procedure.md Step 4):
- PR-1: Calculations shall use recognized engineering methods (Darcy-Weisbach for hydraulics, ASME B31.3 for stress) (construction: Datasheet.md Construction items 1, 2; rationale: Guidance.md Principles items 1, 2; standards: Standards section; procedure: Procedure.md Step 1, Step 2; examples: Guidance.md Examples sections)
- PR-2: Software calculations (CAESAR II, AutoPIPE, etc.) shall be validated and verified (attributes: Datasheet.md Software/Tools; quality: QR-2; procedure: Procedure.md Prerequisites, Step 2, Step 4; verification: Verification - Calculation check)
- PR-3: Hand calculations shall follow industry-standard formulations with references (quality: QR-1; procedure: Procedure.md Step 1; verification: Verification - Calculation check; examples: Guidance.md Examples - Typical pipe sizing)

**Design criteria** (conditions: Datasheet.md Design Conditions; rationale: Guidance.md Principles items 1, 2, 4; procedure: Procedure.md Step 1):
- PR-4: Pipe sizing based on flow rates **TBD** (location TBD: ER Volume 2 Part 2 or process design basis) (requirements: FR-1, FR-2; conditions: Datasheet.md Flow rates; procedure: Procedure.md Prerequisites, Step 1; cross-reference DEL-14.04)
- PR-5: Design pressure and temperature per ASME B31.3 (operating conditions + margin) (code: Datasheet.md Design Code; conditions: Datasheet.md Design Conditions; rationale: Guidance.md Principles item 2; standards: Standards section; procedure: Procedure.md Prerequisites, Step 2; cross-reference DEL-14.02, DEL-14.04)
- PR-6: Stress analysis load combinations per ASME B31.3 (sustained, occasional, thermal) (code: Datasheet.md Design Code; requirements: FR-5; rationale: Guidance.md Principles items 2, 4; standards: Standards section; procedure: Procedure.md Step 2; examples: Guidance.md Principles item 4)
- PR-7: Seismic loads per NBC 2020 **ASSUMPTION** (location TBD: ER Volume 2 Part 1) (conditions: Datasheet.md Seismic criteria; rationale: Guidance.md Principles item 4; considerations: Guidance.md Considerations - Stress Analysis; standards: Standards section; procedure: Procedure.md Prerequisites, Step 2; cross-reference DEL-14.01, DEL-14.02)

### Interface Requirements

(rationale: Guidance.md Considerations sections; procedure: Procedure.md Prerequisites, Steps 1-3):
- IR-1: Piping geometry from DEL-14.01 (drawings) (construction: Datasheet.md Construction items 2, 3 - Inputs; considerations: Guidance.md Considerations - Stress Analysis; procedure: Procedure.md Prerequisites, Step 2; examples: Guidance.md Examples - Typical stress analysis; cross-reference DEL-14.01)
- IR-2: Material properties and allowable stresses from DEL-14.02 (specification) (construction: Datasheet.md Construction items 2, 3 - Inputs; conditions: Datasheet.md Design Conditions; procedure: Procedure.md Prerequisites, Step 2; cross-reference DEL-14.02)
- IR-3: Design conditions (pressure, temperature, flow) from DEL-14.04 (data sheets) (requirements: FR-1, PR-4; construction: Datasheet.md Construction items 1, 2, 3 - Inputs; conditions: Datasheet.md Design Conditions; procedure: Procedure.md Prerequisites, Step 1; cross-reference DEL-14.04)
- IR-4: Dynamic loads from DEL-14.06, DEL-14.07 (transient analyses) (construction: Datasheet.md Construction item 2 - Inputs; considerations: Guidance.md Considerations - Stress Analysis; trade-offs: Guidance.md Trade-offs item 2; procedure: Procedure.md Step 2; cross-reference DEL-14.06, DEL-14.07)
- IR-5: Equipment nozzle load allowables from PKG-13, PKG-15, PKG-16 (requirements: FR-7, FR-9; construction: Datasheet.md Construction items 2, 3 - Outputs; rationale: Guidance.md Principles items 2, 3; considerations: Guidance.md Considerations - Stress Analysis, Flexibility Analysis; procedure: Procedure.md Prerequisites, Step 2, Step 3; verification: Verification - Acceptance criteria)
- IR-6: Structural support capacity from PKG-05, PKG-06 (requirements: FR-6; construction: Datasheet.md Construction item 2 - Outputs; procedure: Procedure.md Step 2; verification: Verification - Acceptance criteria; cross-reference PKG-05, PKG-06)

### Quality Requirements

(rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 4, Step 5):
- QR-1: All calculations checked by independent qualified engineer (performance: PR-3; procedure: Procedure.md Step 4; verification: Verification - Calculation check)
- QR-2: Software models verified (geometry, loads, boundary conditions, material properties) (performance: PR-2; attributes: Datasheet.md Software/Tools; procedure: Procedure.md Step 2, Step 4; verification: Verification - Calculation check; examples: Guidance.md Examples - Typical stress analysis)
- QR-3: Results validated against acceptance criteria (stress ratios ≤ 1.0) (requirements: FR-5, FR-8; verification: Verification - Acceptance criteria; procedure: Procedure.md Step 2, Step 3, Step 4)
- QR-4: Calculation documentation format per project standards **TBD** (attributes: Datasheet.md Revision Control; procedure: Procedure.md Step 5; documentation: Documentation section)

## Standards

(code: Datasheet.md Design Code; rationale: Guidance.md Principles items 1, 2, 3; procedure: Procedure.md Prerequisites; cross-reference DEL-14.01, DEL-14.02):
- ASME B31.3 — Process Piping (Chapter III Design; Appendix P Flexibility Analysis) (code: Datasheet.md Design Code; construction: Datasheet.md Construction items 2, 3; requirements: FR-5, FR-8, PR-5, PR-6; rationale: Guidance.md Principles items 2, 3; procedure: Procedure.md Prerequisites, Steps 2-3; examples: Guidance.md Principles items 2, 3, 4; referenced in DEL-14.01, DEL-14.02)
- CAESAR II, AutoPIPE, or equivalent — pipe stress analysis software **TBD** (attributes: Datasheet.md Software/Tools; construction: Datasheet.md Construction items 2, 3 - Software; performance: PR-2; quality: QR-2; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Stress Analysis; procedure: Procedure.md Prerequisites, Step 2; examples: Guidance.md Examples - Typical stress analysis)
- Darcy-Weisbach equation — hydraulic pressure drop calculations (construction: Datasheet.md Construction item 1 - Methodology; performance: PR-1; rationale: Guidance.md Principles item 1; procedure: Procedure.md Step 1; examples: Guidance.md Examples - Typical pipe sizing)
- NBC 2020 — seismic and wind loads **ASSUMPTION** (conditions: Datasheet.md Seismic criteria; performance: PR-7; rationale: Guidance.md Principles item 4; considerations: Guidance.md Considerations - Stress Analysis; procedure: Procedure.md Prerequisites, Step 2; cross-reference DEL-14.01, DEL-14.02)
- ER Volume 2 Part 1, Part 2 — project-specific design criteria (conditions: Datasheet.md Design Conditions; procedure: Procedure.md Prerequisites; referenced in DEL-14.01, DEL-14.02)

## Verification

**Calculation check** (quality: QR-1, QR-2, QR-3; procedure: Procedure.md Step 4):
- Independent check by qualified engineer (not calculation originator) (quality: QR-1; procedure: Procedure.md Prerequisites, Step 4; verification table)
- Software output verification (geometry, loads, results reasonableness) (quality: QR-2; attributes: Datasheet.md Software/Tools; procedure: Procedure.md Step 4; examples: Guidance.md Examples - Typical stress analysis)
- Design code compliance (ASME B31.3 stress limits) (code: Datasheet.md Design Code; requirements: FR-5, FR-8; quality: QR-3; standards: Standards section; procedure: Procedure.md Step 2, Step 3, Step 4)
- Sensitivity analysis for critical parameters (quality: QR-3; considerations: Guidance.md Trade-offs item 2; procedure: Procedure.md Step 4)

**Acceptance criteria** (quality: QR-3; procedure: Procedure.md Verification section):
- All stress ratios ≤ 1.0 (within ASME B31.3 allowables) (requirements: FR-5, FR-8; quality: QR-3; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 2, Step 3; verification table)
- Equipment nozzle loads within vendor allowables (requirements: FR-7, FR-9; construction: Datasheet.md Construction items 2, 3 - Outputs; interface: IR-5; procedure: Procedure.md Step 2, Step 3; verification table)
- Pipe support loads within structural capacity (requirements: FR-6; construction: Datasheet.md Construction item 2 - Outputs; interface: IR-6; procedure: Procedure.md Step 2; verification table; cross-reference PKG-05, PKG-06)
- Flow velocities within acceptable range (typically 1.5-3.0 m/s for liquids) (requirements: FR-3; construction: Datasheet.md Construction item 1 - Outputs; rationale: Guidance.md Principles item 1; procedure: Procedure.md Step 1; verification table)

## Documentation

**Calculation package** (quality: QR-4; procedure: Procedure.md Step 5, Records section):
- Calculation summary cover sheet (procedure: Procedure.md Step 5; documentation format per QR-4)
- Design basis and inputs (conditions: Datasheet.md Design Conditions; interface: IR-1, IR-2, IR-3; procedure: Procedure.md Step 1)
- Methodology and references (performance: PR-1; standards: Standards section; procedure: Procedure.md Steps 1-3; examples: Guidance.md Examples sections)
- Calculations (hand calcs or software output) (construction: Datasheet.md Construction sections; performance: PR-2, PR-3; procedure: Procedure.md Steps 1-3)
- Results summary and conclusions (construction: Datasheet.md Construction items - Outputs; requirements: FR sections; procedure: Procedure.md Steps 1-3)
- Check sign-off (quality: QR-1; procedure: Procedure.md Step 4; verification: Verification - Calculation check)

**Storage:** `2_Checking/` (review) → `3_Issued/` (approved) (attributes: Datasheet.md Revision Control; quality: QR-4; procedure: Procedure.md Step 5, Records section)
