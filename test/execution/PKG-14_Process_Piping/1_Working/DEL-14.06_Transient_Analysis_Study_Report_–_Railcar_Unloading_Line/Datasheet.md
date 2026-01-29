# Datasheet: DEL-14.06 Transient Analysis Study Report – Railcar Unloading Line

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-14.06 |
| Name | Transient Analysis Study Report – Railcar Unloading Line |
| Package | PKG-14 Process Piping |
| Discipline | Mechanical |
| Type | Report |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Report Type | Transient (surge/water hammer) analysis study (scope: Specification.md Scope; rationale: Guidance.md Purpose; procedure: Procedure.md Purpose) |
| System Analyzed | Railcar unloading line (32 railcar stations to storage tanks or direct to marine loading) (scope: Specification.md Scope; conditions: Conditions - System Description; requirements: Specification.md FR-1; procedure: Procedure.md Step 1; cross-reference DEL-14.01, PKG-10) |
| Analysis Software | **TBD** — **ASSUMPTION**: AFT Impulse, WANDA, or equivalent transient analysis software (requirements: Specification.md PR-4; standards: Specification.md Standards - Software; rationale: Guidance.md Principles item 4; procedure: Procedure.md Prerequisites; examples: Guidance.md Examples item 1) |
| Design Standard | ASME B31.3 + transient analysis best practices (requirements: Specification.md PR-1, Standards section; rationale: Guidance.md Principles item 1; procedure: Procedure.md Prerequisites; cross-reference DEL-14.01, DEL-14.03) |
| Analysis Scenarios | Pump startup/shutdown, valve closing, power failure, operational upsets (conditions: Conditions - Transient Scenarios; requirements: Specification.md FR-5; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 2; examples: Guidance.md Examples item 2) |

## Conditions

**System Description:**
- **System:** Railcar unloading piping from 32 railcar unloading stations to storage tanks or direct to marine loading (attributes: System Analyzed; scope: Specification.md Scope; requirements: Specification.md FR-1; procedure: Procedure.md Step 1; cross-reference DEL-14.01, PKG-10, PKG-13)
- **Product:** CSD (Crude Super Degummed) canola oil (source: Decomposition Section 1.1; scope: Specification.md Scope; requirements: Specification.md FR-3; rationale: Guidance.md Considerations - Fluid Properties; procedure: Procedure.md Step 1; cross-reference DEL-14.01, DEL-14.02)
- **Throughput:** 1,000,000 MT per annum (source: Decomposition Section 1.1; procedure: Procedure.md Prerequisites; cross-reference DEL-14.01)
- **Flow rate:** **TBD** — based on throughput and operational scenarios (continuous vs. batch unloading) (requirements: Specification.md FR-1; interface: Specification.md IR-3; procedure: Procedure.md Prerequisites, Step 1; cross-reference DEL-14.03, PKG-15)
- **Operating pressure:** **TBD** (location TBD: ER Volume 2 Part 2 or process design basis; requirements: Specification.md FR-1; interface: Specification.md IR-2; procedure: Procedure.md Prerequisites, Step 1; cross-reference DEL-14.03)
- **Piping length:** **TBD** — from railcar area to tank farm (estimated several hundred meters) (requirements: Specification.md FR-2; interface: Specification.md IR-1; rationale: Guidance.md Considerations - System Characteristics; procedure: Procedure.md Step 1; cross-reference DEL-14.01)

**Transient Scenarios to Analyze:**
- Normal pump startup (gradual flow increase) (attributes: Analysis Scenarios; requirements: Specification.md FR-5; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 2; examples: Guidance.md Examples item 2)
- Normal pump shutdown (controlled flow decrease) (attributes: Analysis Scenarios; requirements: Specification.md FR-5; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 2)
- Pump trip / power failure (sudden flow stoppage, negative surge/cavitation risk) (attributes: Analysis Scenarios; requirements: Specification.md FR-5, PR-3; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Operational Considerations; procedure: Procedure.md Step 2; examples: Guidance.md Examples item 2)
- Valve closing — normal rate (controlled closure) (attributes: Analysis Scenarios; requirements: Specification.md FR-5; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 2; cross-reference DEL-14.08)
- Valve closing — emergency rate (rapid closure for emergency shutdown) (attributes: Analysis Scenarios; requirements: Specification.md FR-5; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Operational Considerations; trade-offs: Guidance.md Trade-offs item 1; procedure: Procedure.md Step 2; examples: Guidance.md Examples item 2; cross-reference DEL-14.08)
- Operational upsets **TBD** (specific upset scenarios per operational philosophy) (attributes: Analysis Scenarios; requirements: Specification.md FR-5; procedure: Procedure.md Prerequisites, Step 2)

**Design Criteria:**
- Surge pressures shall not exceed pipe design pressure (per ASME B31.3) (requirements: Specification.md PR-1; standards: Specification.md Standards - ASME B31.3; rationale: Guidance.md Principles item 1; verification: Specification.md Verification - Acceptance; procedure: Procedure.md Step 3; cross-reference DEL-14.03)
- Surge pressures shall not exceed equipment pressure ratings (pumps, tanks, valves) (requirements: Specification.md PR-2; interface: Specification.md IR-3, IR-4, IR-5; verification: Specification.md Verification - Acceptance; procedure: Procedure.md Step 3; cross-reference PKG-13, PKG-15, PKG-16)

## Construction

**Anticipated artifacts** (source: Decomposition DEL-14.06; scope: Specification.md Scope; procedure: Procedure.md Steps 1-4; documentation: Specification.md Documentation):

**1. Transient Model:**
- Software input file (AFT Impulse, WANDA, or equivalent) (attributes: Analysis Software; construction: item 1; requirements: Specification.md FR-1, PR-4; standards: Specification.md Standards - Software; quality: Specification.md QR-1; procedure: Procedure.md Step 1; examples: Guidance.md Examples item 1; cross-reference software user manual)
- Piping geometry (lengths, diameters, elevations) from DEL-14.01 (construction: item 1; requirements: Specification.md FR-2; interface: Specification.md IR-1; rationale: Guidance.md Considerations - System Characteristics; quality: Specification.md QR-1; procedure: Procedure.md Prerequisites, Step 1; verification: Specification.md Verification - Model verification; cross-reference DEL-14.01)
- Fluid properties (density, bulk modulus, viscosity for CSD canola oil) (construction: item 1; requirements: Specification.md FR-3; rationale: Guidance.md Considerations - Fluid Properties; quality: Specification.md QR-1; procedure: Procedure.md Prerequisites, Step 1; verification: Specification.md Verification - Model verification; examples: Guidance.md Considerations - Fluid Properties)
- Boundary conditions (pump curves, tank levels, valve locations and types) (construction: item 1; requirements: Specification.md FR-4; interface: Specification.md IR-3, IR-4, IR-5; quality: Specification.md QR-1; procedure: Procedure.md Prerequisites, Step 1; verification: Specification.md Verification - Model verification; cross-reference PKG-13, PKG-15, PKG-16)

**2. Surge Results:**
- Pressure vs. time plots at critical locations (pump discharge, high points, valve locations, tank connections) (construction: item 2; requirements: Specification.md FR-6; rationale: Guidance.md Principles item 4; considerations: Guidance.md Considerations - System Characteristics; procedure: Procedure.md Step 2, Step 3; documentation: Specification.md Documentation - Report content; examples: Guidance.md Examples item 2)
- Maximum and minimum surge pressures for each scenario (construction: item 2; requirements: Specification.md FR-6, FR-7, FR-8; performance: Specification.md PR-1, PR-2, PR-3; procedure: Procedure.md Step 3; verification: Specification.md Verification - Acceptance; examples: Guidance.md Examples item 2)
- Identification of scenarios exceeding design pressure limits (construction: item 2; requirements: Specification.md FR-8, FR-9; performance: Specification.md PR-1, PR-2; procedure: Procedure.md Step 3; verification: Specification.md Verification - Acceptance)

**3. Mitigation Recommendations:**
- Surge relief valves (location, sizing, set pressure) (construction: item 3; requirements: Specification.md FR-9, FR-10; rationale: Guidance.md Principles item 3; trade-offs: Guidance.md Trade-offs item 2; procedure: Procedure.md Step 4; examples: Guidance.md Examples item 3; cross-reference PKG-16)
- Valve closing time limits (minimum closing time to limit surge) (construction: item 3; requirements: Specification.md FR-9, FR-10; interface: Specification.md IR-6; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Operational Considerations; trade-offs: Guidance.md Trade-offs item 1; procedure: Procedure.md Step 4; verification: Specification.md Verification - Mitigation verification; cross-reference DEL-14.08, PKG-16)
- Accumulators or surge tanks (if required) (construction: item 3; requirements: Specification.md FR-9; rationale: Guidance.md Principles item 3; trade-offs: Guidance.md Trade-offs item 3; procedure: Procedure.md Step 4; examples: Guidance.md Examples item 3)
- Pipe design pressure increase (if surge mitigation not feasible by other means) (construction: item 3; requirements: Specification.md FR-9; rationale: Guidance.md Principles item 3; trade-offs: Guidance.md Trade-offs item 4; procedure: Procedure.md Step 4; cross-reference DEL-14.01, DEL-14.03)

**4. Final Report:**
- Executive summary (construction: item 4; quality: Specification.md QR-4; documentation: Specification.md Documentation - Report content; procedure: Procedure.md Step 5)
- System description and analysis methodology (construction: item 4; requirements: Specification.md FR-1; quality: Specification.md QR-4; rationale: Guidance.md Principles items 1, 2; documentation: Specification.md Documentation - Report content; procedure: Procedure.md Step 5; examples: Guidance.md Principles items 1, 2, 4)
- Transient model description and validation (construction: items 1, 4; requirements: Specification.md FR-2, FR-3, FR-4, PR-5; quality: Specification.md QR-1; documentation: Specification.md Documentation - Report content; procedure: Procedure.md Step 5)
- Transient scenarios analyzed (construction: item 4; requirements: Specification.md FR-5; conditions: Transient Scenarios; documentation: Specification.md Documentation - Report content; procedure: Procedure.md Step 5)
- Results (pressure plots, maximum surge pressures) (construction: items 2, 4; requirements: Specification.md FR-6, FR-7, FR-8; documentation: Specification.md Documentation - Report content; procedure: Procedure.md Step 5; examples: Guidance.md Examples item 2)
- Mitigation recommendations and implementation (construction: items 3, 4; requirements: Specification.md FR-9, FR-10; documentation: Specification.md Documentation - Report content; procedure: Procedure.md Step 5; examples: Guidance.md Examples item 3)
- Conclusions and design verification statement (construction: item 4; requirements: Specification.md FR-8; performance: Specification.md PR-1, PR-2; quality: Specification.md QR-4; documentation: Specification.md Documentation - Report content; verification: Specification.md Verification - Acceptance; procedure: Procedure.md Step 5)

## References

**Project References:**
- Decomposition file: /Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md
- ER Volume 2 Part 1, Part 2 (procedure: Prerequisites; cross-reference DEL-14.01, DEL-14.02)

**Applicable Standards:**
- ASME B31.3 — Process Piping (design pressure limits) (design standard: Attributes; requirements: Specification.md PR-1, Standards section; rationale: Guidance.md Principles item 1; procedure: Prerequisites; cross-reference DEL-14.01, DEL-14.02, DEL-14.03)
- Transient analysis references (standards: Specification.md Standards - Transient analysis references; rationale: Guidance.md Principles items 1, 2, 4; procedure: Prerequisites):
  - Thorley, "Fluid Transients in Pipeline Systems" (rationale: Guidance.md Principles item 1; examples: Guidance.md Principles item 1 - Joukowsky equation)
  - Wylie & Streeter, "Fluid Transients in Systems" (rationale: Guidance.md Principles item 1)
  - Software user manual (AFT Impulse, WANDA, or equivalent) **TBD** (attributes: Analysis Software; standards: Specification.md Standards - Software; procedure: Prerequisites)

**Cross-references:**
- DEL-14.01 (Process Piping Design Drawings) — piping geometry, P&IDs (construction: Construction item 1 - Piping geometry; requirements: Specification.md FR-2; interface: Specification.md IR-1; procedure: Prerequisites, Step 1; verification: Specification.md Verification - Model verification; examples: Guidance.md Examples item 1)
- DEL-14.03 (Process Piping Design Calculations) — design pressure and temperature (construction: Construction item 2 - Maximum surge pressures; requirements: Specification.md FR-7; interface: Specification.md IR-2; performance: Specification.md PR-1; conditions: Design Criteria; procedure: Prerequisites, Step 3; verification: Specification.md Verification - Acceptance)
- DEL-14.08 (Valve Closing Time Verification) — valve closing time requirements (construction: Construction item 3 - Valve closing time limits; requirements: Specification.md FR-9; interface: Specification.md IR-6; rationale: Guidance.md Principles item 3; trade-offs: Guidance.md Trade-offs item 1; procedure: Step 4; examples: Guidance.md Examples item 3)
- PKG-10 (Railcar Unloading System) — railcar unloading configuration (attributes: System Analyzed; requirements: Specification.md FR-1; procedure: Step 1)
- PKG-13 (Storage Tanks) — tank data (levels, elevations, ratings) (construction: Construction item 1 - Boundary conditions; requirements: Specification.md FR-4; interface: Specification.md IR-4; procedure: Prerequisites, Step 1; cross-reference PKG-13)
- PKG-15 (Pumps) — pump curves, inertia, coastdown (construction: Construction item 1 - Boundary conditions; requirements: Specification.md FR-4; interface: Specification.md IR-3; rationale: Guidance.md Considerations - Operational Considerations; procedure: Prerequisites, Step 1; cross-reference PKG-15)
- PKG-16 (Valves) — valve types, actuation, closing times (construction: Construction items 1, 3 - Boundary conditions, Valve closing time limits; requirements: Specification.md FR-4, FR-9; interface: Specification.md IR-5, IR-6; trade-offs: Guidance.md Trade-offs item 1; procedure: Prerequisites, Step 1, Step 4; cross-reference PKG-16)

**Related Project Objectives:**
- OBJ-1: Safe & Reliable Operation — transient analysis ensures piping designed to withstand operational transients safely (requirements: Specification.md FR-8, PR-1, PR-2; rationale: Guidance.md Principles item 1; procedure: Purpose)
- OBJ-2: Throughput Capacity — analysis verifies system can operate at design flow rates (attributes: System Analyzed - Throughput; requirements: Specification.md FR-1)
