# Datasheet: DEL-14.03 Process Piping Design Calculations

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-14.03 |
| Name | Process Piping Design Calculations |
| Package | PKG-14 Process Piping |
| Discipline | Mechanical |
| Type | Calculation |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Calculation Type | Engineering calculations (pipe sizing, stress analysis, flexibility analysis) (scope: Specification.md Scope; rationale: Guidance.md Purpose) |
| Calculation Package | Multiple calculation sets for process piping systems (construction: Construction section; procedure: Procedure.md Steps 2-4) |
| Software/Tools | **TBD** — **ASSUMPTION**: CAESAR II or AutoPIPE for stress/flexibility; Excel/MathCAD for hydraulic sizing (requirements: Specification.md QR-1; procedure: Procedure.md Prerequisites; considerations: Guidance.md Considerations item 2) |
| Design Code | ASME B31.3 Process Piping (requirements: Specification.md Standards section; rationale: Guidance.md Principles item 1; procedure: Procedure.md Prerequisites; referenced in DEL-14.01, DEL-14.02) |
| Calculation Sections | Pipe sizing calculations, stress analysis, flexibility analysis (source: DEL-14.03 entry; scope: Specification.md Scope; construction: Construction section; procedure: Procedure.md Steps 2-4) |
| Number of Calculations | **TBD** — estimate: 20-40 sizing calcs, 10-20 stress analyses, 5-10 flexibility analyses (to be confirmed during execution per Procedure.md Step 1) |
| Revision Control | **TBD** — per project calculation numbering system (requirements: Specification.md QR-4; procedure: Procedure.md Step 6) |

## Conditions

**Design Conditions:**

- **Operating temperature:** **TBD** — **ASSUMPTION**: -10°C to +60°C for canola oil (requirements: Specification.md PR-1; procedure: Procedure.md Step 1; cross-reference DEL-14.01, DEL-14.02)
- **Design temperature:** **TBD** — per ASME B31.3 (operating + margin) (code: Design Code; requirements: Specification.md PR-1; rationale: Guidance.md Principles item 1; procedure: Procedure.md Step 2)
- **Operating pressure:** **TBD** — varies by system (railcar unloading, marine loading, recycle, nitrogen) (requirements: Specification.md PR-2; procedure: Procedure.md Step 1; cross-reference DEL-14.01, DEL-14.02, DEL-14.04)
- **Design pressure:** **TBD** — per ASME B31.3 (110% operating or code minimum) (code: Design Code; requirements: Specification.md PR-2; rationale: Guidance.md Principles item 1; procedure: Procedure.md Step 2)
- **Flow rates:** **TBD** — based on 1,000,000 MT/annum throughput (source: Decomposition Section 1.1; requirements: Specification.md FR-1; procedure: Procedure.md Step 1; cross-reference DEL-14.01)
- **Product properties:** **TBD** — CSD canola oil density, viscosity, vapor pressure (requirements: Specification.md FR-1, PR-1; procedure: Procedure.md Step 1, Step 2; cross-reference DEL-14.02)
- **Seismic criteria:** **TBD** — **ASSUMPTION**: NBC 2020 (location TBD: ER Volume 2 Part 1; requirements: Specification.md PR-5; rationale: Guidance.md Principles item 4; procedure: Procedure.md Step 1, Step 4; cross-reference DEL-14.01, DEL-14.02)
- **Environmental:** Fraser Surrey Terminal, BC (coastal/marine) (requirements: Specification.md FR-2; considerations: Guidance.md Considerations item 1; cross-reference DEL-14.01, DEL-14.02)

## Construction

**Calculation Deliverables** (source: Decomposition DEL-14.03; scope: Specification.md Scope; procedure: Procedure.md Steps 2-4):

**1. Pipe Sizing Calculations:**
- Hydraulic calculations for pipe diameter determination (requirements: Specification.md FR-1, PR-3; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 2; examples: Guidance.md Examples item 1; verification: Specification.md Verification - Calculation review)
- Inputs: Flow rates, fluid properties, allowable pressure drop, velocity limits (requirements: Specification.md FR-1, PR-1, PR-3; procedure: Procedure.md Step 1, Step 2)
- Methodology: Darcy-Weisbach equation, Hazen-Williams, or equivalent (rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations item 2; examples: Guidance.md Examples item 1)
- Outputs: Pipe sizes (DN/NPS), velocities, pressure drops, Reynolds numbers (requirements: Specification.md FR-1; procedure: Procedure.md Step 2; cross-reference DEL-14.01, DEL-14.02, DEL-14.04)
- **TBD** — Number of lines (estimated 50-100; procedure: Procedure.md Step 1)
- Typical systems: Railcar unloading headers, marine loading export lines, product recycle, nitrogen distribution (requirements: Specification.md FR-2; procedure: Procedure.md Step 2; cross-reference DEL-14.01)

**2. Stress Analysis:**
- ASME B31.3 stress analysis (sustained, occasional, thermal loads) (code: Design Code; requirements: Specification.md PR-4; rationale: Guidance.md Principles item 3; standards: Specification.md Standards section; procedure: Procedure.md Step 3; examples: Guidance.md Examples item 2; verification: Specification.md Verification - Calculation review)
- Inputs: Piping geometry, materials, operating conditions, support locations, loads (procedure: Procedure.md Step 1, Step 3; cross-reference DEL-14.01, DEL-14.02)
- Methodology: ASME B31.3 stress equations (B31.3-319.4.4 sustained, 319.4.3 occasional) (code: Design Code; rationale: Guidance.md Principles item 3; standards: Specification.md Standards section; examples: Guidance.md Examples item 2)
- Software: **TBD** — **ASSUMPTION**: CAESAR II or AutoPIPE (attributes: Software/Tools; requirements: Specification.md QR-1; procedure: Procedure.md Prerequisites; considerations: Guidance.md Considerations item 2)
- Outputs: Stress ratios, code compliance summary, support loads, equipment nozzle loads (requirements: Specification.md PR-4, QR-6; procedure: Procedure.md Step 3; verification: Specification.md Verification - Calculation review; cross-reference DEL-14.01 for support drawings, DEL-14.04)
- **TBD** — Critical lines requiring analysis (procedure: Procedure.md Step 1; criteria: Guidance.md Considerations item 3)

**3. Flexibility Analysis:**
- Thermal expansion analysis per ASME B31.3 (code: Design Code; requirements: Specification.md PR-6; rationale: Guidance.md Principles item 4; standards: Specification.md Standards section; procedure: Procedure.md Step 4; examples: Guidance.md Examples item 3; verification: Specification.md Verification - Calculation review)
- Inputs: Piping geometry, materials, temperature range, support configuration (procedure: Procedure.md Step 1, Step 4; cross-reference DEL-14.01, DEL-14.02)
- Methodology: ASME B31.3 Appendix P flexibility analysis, or equivalent software analysis (code: Design Code; rationale: Guidance.md Principles item 4; standards: Specification.md Standards section; examples: Guidance.md Examples item 3)
- Software: **TBD** — **ASSUMPTION**: CAESAR II or AutoPIPE (attributes: Software/Tools; requirements: Specification.md QR-1; procedure: Procedure.md Prerequisites)
- Outputs: Thermal displacements, thermal stresses, expansion loop adequacy, equipment nozzle loads, spring hanger loads (requirements: Specification.md PR-6, QR-6; procedure: Procedure.md Step 4; trade-offs: Guidance.md Trade-offs item 2; cross-reference DEL-14.01, DEL-14.02)
- **TBD** — Lines with significant temperature variation (procedure: Procedure.md Step 1; criteria: Guidance.md Considerations item 3; trade-offs: Guidance.md Trade-offs item 2)

## References

**Project References:**
- Decomposition file: /Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md
- ER Volume 2 Part 1 (General Requirements), Part 2 (Civil & Process Mechanical Works) (procedure: Procedure.md Prerequisites, Step 1)

**Applicable Standards:**
- ASME B31.3 — Process Piping (Chapter III Design; Appendix P Flexibility Analysis) (code: Design Code; requirements: Specification.md Standards section; rationale: Guidance.md Principles items 1, 3, 4; examples: Guidance.md Examples items 2, 3; referenced in DEL-14.01, DEL-14.02)
- **TBD** — Hydraulic calculation standards or references (considerations: Guidance.md Considerations item 2; examples: Guidance.md Examples item 1)

**Cross-references:**
- DEL-14.01 (Piping Drawings) — geometry, routing, supports (requirements: Specification.md IR-1; procedure: Procedure.md Step 1, Steps 2-4; examples: Guidance.md Examples item 4)
- DEL-14.02 (Piping Specification) — materials, allowable stresses, corrosion allowance (requirements: Specification.md IR-2; procedure: Procedure.md Step 1, Step 2, Step 3; examples: Guidance.md Examples item 4)
- DEL-14.04 (Data Sheet Package) — line design conditions, material classes (requirements: Specification.md IR-3; procedure: Procedure.md Step 1; examples: Guidance.md Examples item 4)
- DEL-14.06, DEL-14.07 (Transient Analyses) — dynamic loads, surge forces (requirements: Specification.md IR-5; considerations: Guidance.md Considerations item 4; procedure: Procedure.md Step 3; trade-offs: Guidance.md Trade-offs item 3)
- PKG-13, PKG-15, PKG-16 — equipment nozzle load allowables (requirements: Specification.md IR-4; procedure: Procedure.md Step 1, Step 3, Step 4)

**Related Objectives:**
- OBJ-1: Safe & Reliable Operation — stress analysis ensures code compliance and safe operation (requirements: Specification.md FR-3; rationale: Guidance.md Principles item 3; procedure: Procedure.md Step 3)
- OBJ-2: Throughput Capacity (1,000,000 MT/annum) — sizing calculations ensure adequate capacity (requirements: Specification.md FR-1; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 2)
