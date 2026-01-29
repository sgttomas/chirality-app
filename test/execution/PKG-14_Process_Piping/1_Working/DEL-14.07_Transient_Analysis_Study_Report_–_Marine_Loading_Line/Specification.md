# Specification: DEL-14.07 Transient Analysis Study Report – Marine Loading Line

## Scope

Transient (surge/water hammer) analysis for marine loading export line piping system to verify design pressure adequacy and identify mitigation measures (source: Decomposition DEL-14.07; attributes: Datasheet.md Report Type; rationale: Guidance.md Purpose).

**Report outputs** (source: Decomposition DEL-14.07; construction: Datasheet.md Construction section; procedure: Procedure.md Steps 1-5):
- Transient model (construction: Datasheet.md Construction item 1; procedure: Procedure.md Step 1; examples: Guidance.md Examples item 1)
- Surge results (pressure vs. time plots, maximum surge pressures) (construction: Datasheet.md Construction item 2; procedure: Procedure.md Step 2, Step 3; examples: Guidance.md Examples item 2)
- Mitigation recommendations (construction: Datasheet.md Construction item 3; procedure: Procedure.md Step 4; examples: Guidance.md Examples item 3)
- Final report (construction: Datasheet.md Construction item 4; procedure: Procedure.md Step 5)

## Requirements

### Functional Requirements

**Transient Model** (construction: Datasheet.md Construction item 1; rationale: Guidance.md Principles item 4; quality: QR-1; procedure: Procedure.md Step 1):
- FR-1: Model marine loading export line piping system from storage tanks or railcar headers to marine loading arms at berth (attributes: Datasheet.md System Analyzed; conditions: Datasheet.md System Description; rationale: Guidance.md Purpose; procedure: Procedure.md Step 1; cross-reference DEL-14.01, PKG-11, PKG-13)
- FR-2: Include piping geometry (lengths, diameters, elevations) from DEL-14.01 (construction: Datasheet.md Construction item 1 - Piping geometry; interface: IR-1; quality: QR-1; rationale: Guidance.md Considerations - System Characteristics; procedure: Procedure.md Prerequisites, Step 1; verification: Verification - Model verification; examples: Guidance.md Examples item 1; cross-reference DEL-14.01)
- FR-3: Include fluid properties for CSD canola oil (density, bulk modulus, viscosity) (construction: Datasheet.md Construction item 1 - Fluid properties; conditions: Datasheet.md Product; quality: QR-1; rationale: Guidance.md Considerations - Fluid Properties; procedure: Procedure.md Prerequisites, Step 1; verification: Verification - Model verification; examples: Guidance.md Considerations - Fluid Properties)
- FR-4: Include boundary conditions (pump curves, tank levels, loading arm configuration) (construction: Datasheet.md Construction item 1 - Boundary conditions; interface: IR-3, IR-4, IR-5; quality: QR-1; rationale: Guidance.md Considerations - Operational Considerations; procedure: Procedure.md Prerequisites, Step 1; verification: Verification - Model verification; cross-reference PKG-11, PKG-13, PKG-15)

**Transient Analysis** (construction: Datasheet.md Construction item 2; attributes: Datasheet.md Analysis Scenarios; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 2):
- FR-5: Analyze normal and emergency transient scenarios (pump start/stop/trip, loading arm ESD, ship disconnect, upsets) (conditions: Datasheet.md Transient Scenarios; rationale: Guidance.md Principles item 2; quality: QR-2; procedure: Procedure.md Step 2; documentation: Documentation - Report content; examples: Guidance.md Examples item 2; cross-reference PKG-11)
- FR-6: Calculate surge pressures at critical locations (pump discharge, high points, loading arm, tanks) (construction: Datasheet.md Construction item 2 - Pressure vs. time plots; rationale: Guidance.md Principles item 4; considerations: Guidance.md Considerations - System Characteristics; procedure: Procedure.md Step 2; documentation: Documentation - Report content; examples: Guidance.md Examples item 2)
- FR-7: Compare surge pressures vs. design pressure (ASME B31.3 limits) (construction: Datasheet.md Construction item 2 - Maximum surge pressures; conditions: Datasheet.md Design Criteria; performance: PR-1; standards: Standards - ASME B31.3; procedure: Procedure.md Step 3; verification: Verification - Acceptance; cross-reference DEL-14.03)
- FR-8: Identify scenarios where surge pressures exceed limits (construction: Datasheet.md Construction item 2 - Identification; requirements: FR-7; performance: PR-1, PR-2; procedure: Procedure.md Step 3; verification: Verification - Acceptance; examples: Guidance.md Examples item 2)

**Mitigation** (construction: Datasheet.md Construction item 3; rationale: Guidance.md Principles item 3; procedure: Procedure.md Step 4):
- FR-9: Recommend surge mitigation measures (surge relief valves, loading arm valve closing time limits, accumulators) (construction: Datasheet.md Construction item 3; requirements: FR-8; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Operational Considerations; trade-offs: Guidance.md Trade-offs items 1-4; procedure: Procedure.md Step 4; verification: Verification - Mitigation verification; documentation: Documentation - Report content; examples: Guidance.md Examples item 3; cross-reference PKG-11, PKG-16, DEL-14.08)
- FR-10: Provide implementation details (equipment sizing, locations, set points) (construction: Datasheet.md Construction item 3; requirements: FR-9; rationale: Guidance.md Principles item 3; procedure: Procedure.md Step 4; documentation: Documentation - Report content; examples: Guidance.md Examples item 3; cross-reference DEL-14.01, PKG-11)

### Performance Requirements

(conditions: Datasheet.md Design Criteria; rationale: Guidance.md Principles item 1; procedure: Procedure.md Step 3; verification: Verification - Acceptance):
- PR-1: Maximum surge pressures shall not exceed pipe design pressure per ASME B31.3 (design standard: Datasheet.md Design Standard; requirements: FR-7, FR-8; conditions: Datasheet.md Design Criteria; standards: Standards - ASME B31.3; rationale: Guidance.md Principles item 1; procedure: Procedure.md Step 3; verification: Verification - Acceptance; cross-reference DEL-14.03)
- PR-2: Maximum surge pressures shall not exceed equipment pressure ratings (pumps, tanks, loading arms) (construction: Datasheet.md Construction item 2 - Maximum surge pressures; requirements: FR-8; conditions: Datasheet.md Design Criteria; interface: IR-3, IR-4, IR-5; procedure: Procedure.md Step 3; verification: Verification - Acceptance; cross-reference PKG-11, PKG-13, PKG-15)
- PR-3: Minimum surge pressures shall not cause cavitation or vacuum collapse (construction: Datasheet.md Construction item 2 - Minimum surge pressures; conditions: Datasheet.md Transient Scenarios - Pump trip; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - System Characteristics; procedure: Procedure.md Step 3; verification: Verification - Acceptance)
- PR-4: Analysis shall use validated transient analysis software (AFT Impulse, WANDA, or equivalent) (attributes: Datasheet.md Analysis Software; requirements: FR-1; standards: Standards - Software; quality: QR-1; procedure: Procedure.md Prerequisites; examples: Guidance.md Examples item 1)
- PR-5: Model shall be verified against piping drawings and design data (construction: Datasheet.md Construction item 1; requirements: FR-2, FR-3, FR-4; interface: IR-1, IR-2, IR-3, IR-4, IR-5; quality: QR-1; rationale: Guidance.md Principles item 4; procedure: Procedure.md Step 1; verification: Verification - Model verification; cross-reference DEL-14.01, DEL-14.03)

### Interface Requirements

(rationale: Guidance.md Principles item 4; considerations: Guidance.md Considerations - System Characteristics, Operational Considerations; procedure: Procedure.md Prerequisites, Step 1):
- IR-1: Piping geometry from DEL-14.01 (P&IDs, piping GAs, isometrics) (construction: Datasheet.md Construction item 1 - Piping geometry; requirements: FR-2; quality: QR-1; procedure: Procedure.md Prerequisites, Step 1; verification: Verification - Model verification; examples: Guidance.md Examples item 1; cross-reference DEL-14.01)
- IR-2: Design pressure and temperature from DEL-14.03 (design calculations) (construction: Datasheet.md Construction item 2 - Maximum surge pressures; requirements: FR-7; performance: PR-1; conditions: Datasheet.md Design Criteria; procedure: Procedure.md Prerequisites, Step 3; verification: Verification - Acceptance; cross-reference DEL-14.03)
- IR-3: Pump data from PKG-15 (pump curves, inertia, coastdown characteristics) (construction: Datasheet.md Construction item 1 - Boundary conditions; requirements: FR-4; conditions: Datasheet.md Transient Scenarios; rationale: Guidance.md Considerations - Operational Considerations; procedure: Procedure.md Prerequisites, Step 1; verification: Verification - Model verification; cross-reference PKG-15)
- IR-4: Tank data from PKG-13 (levels, nozzle elevations, pressure ratings) (construction: Datasheet.md Construction item 1 - Boundary conditions; requirements: FR-4; performance: PR-2; procedure: Procedure.md Prerequisites, Step 1; verification: Verification - Model verification; cross-reference PKG-13)
- IR-5: Marine loading arm data from PKG-11 (configuration, ESD valve types, actuation, closing times) (construction: Datasheet.md Construction items 1, 3 - Boundary conditions, Loading arm ESD valve closing time; requirements: FR-4, FR-9; conditions: Datasheet.md Transient Scenarios; trade-offs: Guidance.md Trade-offs item 1; procedure: Procedure.md Prerequisites, Step 1, Step 4; verification: Verification - Model verification, Mitigation verification; cross-reference PKG-11, DEL-14.08)
- IR-6: Loading arm ESD valve closing time requirements output to DEL-14.08 (valve closing time verification) (construction: Datasheet.md Construction item 3 - Loading arm ESD valve closing time; requirements: FR-9, FR-10; interface noted above; rationale: Guidance.md Principles item 3; procedure: Procedure.md Step 4; verification: Verification - Mitigation verification; cross-reference DEL-14.08, PKG-11)

### Quality Requirements

(quality: Specification.md QR sections; rationale: Guidance.md Principles item 4; procedure: Procedure.md Step 1, Step 3, Step 6):
- QR-1: Transient model verified (geometry matches drawings, fluid properties correct, boundary conditions reasonable) (construction: Datasheet.md Construction item 1; requirements: FR-2, FR-3, FR-4; performance: PR-5; rationale: Guidance.md Principles item 4; procedure: Procedure.md Step 1; verification: Verification - Model verification; examples: Guidance.md Examples item 1)
- QR-2: Sensitivity analysis performed on critical parameters (loading arm ESD valve closing time, pump inertia) (requirements: FR-5; considerations: Guidance.md Considerations - Operational Considerations; trade-offs: Guidance.md Trade-offs item 1; procedure: Procedure.md Step 3; verification: Verification - Sensitivity analysis; cross-reference PKG-11, DEL-14.08)
- QR-3: Results validated (surge pressures reasonable and consistent with physical expectations) (construction: Datasheet.md Construction item 2; requirements: FR-6, FR-7; performance: PR-1, PR-2, PR-3; rationale: Guidance.md Principles items 1, 2; procedure: Procedure.md Step 3; verification: Verification - Results validation; examples: Guidance.md Examples item 2)
- QR-4: Independent review by qualified engineer (piping or process engineer with transient analysis experience) (procedure: Procedure.md Prerequisites, Step 6; verification: Verification - Independent review)

## Standards

**Design codes** (design standard: Datasheet.md Design Standard; rationale: Guidance.md Principles item 1; procedure: Procedure.md Prerequisites):
- ASME B31.3 — Process Piping (design pressure limits) (requirements: FR-7; performance: PR-1; conditions: Datasheet.md Design Criteria; rationale: Guidance.md Principles item 1; verification: Verification - Acceptance; cross-reference DEL-14.01, DEL-14.02, DEL-14.03)

**Transient analysis references** (rationale: Guidance.md Principles items 1, 2, 4; procedure: Procedure.md Prerequisites):
- Thorley, "Fluid Transients in Pipeline Systems" (rationale: Guidance.md Principles item 1; examples: Guidance.md Principles item 1 - Joukowsky equation)
- Wylie & Streeter, "Fluid Transients in Systems" (rationale: Guidance.md Principles item 1)
- Software user manual (AFT Impulse, WANDA, or equivalent) **TBD** (attributes: Datasheet.md Analysis Software; performance: PR-4; quality: QR-1; procedure: Procedure.md Prerequisites)

**Software** (attributes: Datasheet.md Analysis Software; requirements: FR-1; performance: PR-4; quality: QR-1; procedure: Procedure.md Prerequisites):
- AFT Impulse, WANDA, or equivalent transient analysis software **TBD** (construction: Datasheet.md Construction item 1 - Software input file; rationale: Guidance.md Principles item 4; procedure: Procedure.md Prerequisites, Step 1; verification: Verification - Model verification; examples: Guidance.md Examples item 1)

## Verification

**Model verification** (construction: Datasheet.md Construction item 1; requirements: FR-2, FR-3, FR-4; performance: PR-5; quality: QR-1; procedure: Procedure.md Step 1; verification table):
- Geometry matches DEL-14.01 drawings (requirements: FR-2; interface: IR-1; procedure: Procedure.md Step 1; verification table; cross-reference DEL-14.01)
- Fluid properties correct for CSD canola oil (requirements: FR-3; quality: QR-1; procedure: Procedure.md Step 1; verification table)
- Boundary conditions reasonable (pump curves, tank levels, loading arm configuration) (requirements: FR-4; interface: IR-3, IR-4, IR-5; quality: QR-1; procedure: Procedure.md Step 1; verification table; cross-reference PKG-11, PKG-13, PKG-15)

**Sensitivity analysis** (quality: QR-2; procedure: Procedure.md Step 3; verification table):
- Loading arm ESD valve closing time sensitivity (construction: Datasheet.md Construction item 3 - Loading arm ESD valve closing time; requirements: FR-9; interface: IR-6; trade-offs: Guidance.md Trade-offs item 1; quality: QR-2; procedure: Procedure.md Step 3; verification table; cross-reference DEL-14.08, PKG-11)
- Pump inertia sensitivity (interface: IR-3; considerations: Guidance.md Considerations - Operational Considerations; quality: QR-2; procedure: Procedure.md Step 3; verification table; cross-reference PKG-15)

**Results validation** (construction: Datasheet.md Construction item 2; requirements: FR-6, FR-7; performance: PR-1, PR-2, PR-3; quality: QR-3; procedure: Procedure.md Step 3; verification table):
- Surge pressures reasonable and consistent with Joukowsky equation (rationale: Guidance.md Principles item 1; quality: QR-3; procedure: Procedure.md Step 3; verification table; examples: Guidance.md Principles item 1)
- Maximum pressures compared to design limits (requirements: FR-7, FR-8; performance: PR-1, PR-2; procedure: Procedure.md Step 3; verification table; cross-reference DEL-14.03)
- Minimum pressures checked for cavitation (performance: PR-3; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 3; verification table)

**Mitigation verification** (construction: Datasheet.md Construction item 3; requirements: FR-9, FR-10; procedure: Procedure.md Step 4; verification table):
- Proposed mitigation measures effective (reduce surge to acceptable levels) (requirements: FR-9, FR-10; performance: PR-1, PR-2; rationale: Guidance.md Principles item 3; procedure: Procedure.md Step 4; verification table; examples: Guidance.md Examples item 3)
- Mitigation measures feasible and implementable (requirements: FR-10; procedure: Procedure.md Step 4; verification table; cross-reference DEL-14.01, PKG-11, PKG-16)

**Independent review** (quality: QR-4; procedure: Procedure.md Step 6; verification table):
- Qualified engineer review (model, results, conclusions) (quality: QR-4; procedure: Procedure.md Prerequisites, Step 6; verification table)
- Reviewer sign-off (quality: QR-4; documentation: Documentation - Final report; procedure: Procedure.md Step 6; verification table)

**Acceptance** (performance: PR-1, PR-2, PR-3; requirements: FR-8; procedure: Procedure.md Step 5; verification table):
- All surge scenarios analyzed (requirements: FR-5; verification table)
- Surge pressures within acceptable limits (with mitigation if required) (performance: PR-1, PR-2; requirements: FR-8, FR-9; verification table)
- Mitigation measures defined and implementable (requirements: FR-10; verification table; cross-reference PKG-11, DEL-14.08)
- Report complete and approved (quality: QR-4; documentation: Documentation section; verification table)

## Documentation

**Report content** (construction: Datasheet.md Construction item 4; quality: QR-4; procedure: Procedure.md Step 5):
- Executive summary (construction: Datasheet.md Construction item 4; quality: QR-4; procedure: Procedure.md Step 5)
- System description and analysis methodology (construction: Datasheet.md Construction item 4; requirements: FR-1; rationale: Guidance.md Principles items 1, 2; procedure: Procedure.md Step 5; examples: Guidance.md Principles sections)
- Transient model description and validation (construction: Datasheet.md Construction items 1, 4; requirements: FR-2, FR-3, FR-4; performance: PR-5; quality: QR-1; procedure: Procedure.md Step 5; verification: Verification - Model verification; examples: Guidance.md Examples item 1)
- Transient scenarios analyzed (construction: Datasheet.md Construction item 4; requirements: FR-5; conditions: Datasheet.md Transient Scenarios; procedure: Procedure.md Step 5; examples: Guidance.md Examples item 2)
- Results (pressure plots, maximum surge pressures) (construction: Datasheet.md Construction items 2, 4; requirements: FR-6, FR-7, FR-8; procedure: Procedure.md Step 5; verification: Verification - Results validation; examples: Guidance.md Examples item 2)
- Mitigation recommendations and implementation (construction: Datasheet.md Construction items 3, 4; requirements: FR-9, FR-10; procedure: Procedure.md Step 5; verification: Verification - Mitigation verification; examples: Guidance.md Examples item 3)
- Conclusions and design verification statement (construction: Datasheet.md Construction item 4; performance: PR-1, PR-2; quality: QR-4; procedure: Procedure.md Step 5; verification: Verification - Acceptance)

**Storage:** `2_Checking/` → `3_Issued/` (attributes: Datasheet.md Revision Control; quality: QR-4; procedure: Procedure.md Records section)

**Format:** PDF for issued report; native software files for transient model (attributes: Datasheet.md Analysis Software; quality: QR-4; procedure: Procedure.md Records section)
