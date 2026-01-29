# Guidance: DEL-04.03 Pavement Design Calculations

## Purpose

This guidance clarifies how to review pavement design calculations to ensure inputs are properly sourced, methodology is appropriate, results are consistent with DEL-04.01 drawings and DEL-04.02 specifications, and OBJ-8 future expansion provisions are validated, while tracking all assumptions for resolution.

## Principles

### P1: Input Traceability is Foundation
Every calculation input must be traceable to an authoritative source:
- Traffic loading: Owner data, traffic study, or operational requirements
- Geotechnical parameters: Geotechnical investigation report or regional soil data
- Material properties: Laboratory test data, DEL-04.02 specifications, or design manual correlations
- Environmental data: Climate records, frost depth data, or geotechnical recommendations

**Rationale**: Calculations based on untraceable assumptions have no engineering validity. Explicit source documentation enables review and validation.

### P2: Methodology Must Be Recognized and Appropriate
Pavement design methodology must be:
- Based on recognized standard (TAC, AASHTO, PCA)
- Appropriate for project conditions (traffic, climate, materials)
- Approved by Engineer prior to analysis execution
- Within applicable range of the methodology (traffic levels, pavement types, climate conditions)

**Rationale**: Non-standard or inappropriate methodologies produce unreliable results. Using recognized methods provides confidence in design adequacy.

### P3: Results Must Be Cross-Checked for Reasonableness
Calculation results must be evaluated for reasonableness:
- Compare to similar projects (typical industrial pavement thickness ranges)
- Verify against design manual charts or nomographs (sanity check)
- Check sensitivity to input variations (results should be stable, not hypersensitive)
- Validate with independent calculation or alternate method (if results are unexpected)

**Rationale**: Calculation errors (input errors, software errors, methodology misapplication) can produce unreasonable results. Cross-checking catches errors before they propagate to drawings and construction.

### P4: Assumptions Must Drive Resolution Actions
Every **ASSUMPTION** or **TBD** must have:
- Clear description of what is assumed or unknown
- Impact assessment (which outputs are affected, how sensitive)
- Resolution path (who provides data, when expected, fallback approach)
- Tracking status (open, in-progress, resolved, closed)

**Rationale**: Unresolved assumptions become construction risks. Systematic tracking ensures resolution before final design issuance.

## Considerations

### Calculation Documentation Standards
- **Clarity**: Calculation steps should be understandable by another engineer without verbal explanation
- **Completeness**: All inputs, assumptions, references, formulas, intermediate results, and final outputs documented
- **Reproducibility**: Another engineer should be able to reproduce the results using the documented information
- **Traceability**: Each result cross-referenced to DEL-04.01 drawing section and DEL-04.02 specification clause

### Software Use and Validation
- **Software selection**: Use recognized pavement analysis software (KENPAVE, CIRCLY, MEPDG, or equivalent) with documented validation
- **Version control**: Document software name and version used (results may vary between versions)
- **Input verification**: Verify software inputs match calculation basis (layer thicknesses, moduli, loading, tire pressure)
- **Output interpretation**: Understand software output parameters (stress, strain, deflection units and sign conventions)
- **Hand calculation verification**: Perform hand calculation or simplified check to validate software results for at least one critical case

### Design Parameter Selection
- **Conservative assumptions**: When data is uncertain, select conservative values (lower subgrade strength, higher traffic loading) to err on side of safety
- **Realistic assumptions**: Avoid overly conservative assumptions that lead to uneconomical design (balance safety with cost)
- **Documented basis**: Document basis for each parameter selection (test data, design manual table, engineering judgment)
- **Sensitivity bounds**: Use sensitivity analysis to understand impact of parameter uncertainty on design adequacy

## Review Checklist

### Pre-Review Preparation (Procedure Step 5.3)
- [ ] Obtain calculation report, input summary, analysis worksheets, output summary, sensitivity analysis, OBJ-8 analysis
- [ ] Obtain DEL-04.01 latest drawing set for cross-referencing pavement sections
- [ ] Obtain DEL-04.02 latest specification for cross-referencing material properties
- [ ] Review Procedure assumption tracking log to identify open items affecting calculations

### Step 1: Input Verification (Specification §R1.1–R1.4 | Procedure Step 1)
- [ ] **Traffic loading**: Verify traffic data sources documented; if Owner data not provided, verify assumptions are reasonable and flagged
- [ ] **Geotechnical parameters**: Verify geotechnical report referenced; if not available, verify assumed values are conservative and flagged
- [ ] **Material properties**: Cross-check asphalt, concrete, base/subbase properties vs. DEL-04.02 specifications; verify consistency
- [ ] **Environmental data**: Verify climate data (MAAT, freeze-thaw cycles, frost depth) sourced and reasonable for Fraser Surrey, BC
- [ ] **Input units**: Verify all inputs have correct units (kN, MPa, mm, etc.) and unit conversions are correct
- [ ] **Input reasonableness**: Verify inputs are within reasonable ranges (e.g., subgrade CBR 2-10% typical for fine-grained soils, 10-80% for granular soils)

### Step 2: Methodology Review (Specification §R2.1–R2.5 | Procedure Steps 2, 3)
- [ ] **Design standard**: Verify design methodology (TAC, AASHTO, PCA) is appropriate and approved by Engineer
- [ ] **Design life**: Verify design life (25 years **ASSUMPTION**) is stated and appropriate
- [ ] **Reliability**: Verify reliability level (90% **ASSUMPTION**) is stated and appropriate for industrial pavement
- [ ] **Structural analysis**: Verify layered elastic analysis method (or equivalent) is appropriate; verify software is documented and validated
- [ ] **Load distribution**: Verify load configurations (single, tandem, tridem) match actual vehicle types; verify critical loading positions are analyzed
- [ ] **Fatigue analysis**: Verify fatigue damage accumulation method (Miner's rule or equivalent) is appropriate
- [ ] **Sensitivity analysis**: Verify sensitivity parameters (±20% subgrade, ±20% traffic, ±10% modulus) are analyzed and results documented
- [ ] **OBJ-8 analysis**: Verify Phase 2 ultimate loading case is analyzed for expansion corridors; verify comparison to Phase 1 loading is provided

### Step 3: Calculation Execution Review (Procedure Steps 2.3–2.5)
- [ ] **Calculation logic**: Verify calculation steps are logical and correct (formulas, layer arrangement, load application)
- [ ] **Software inputs**: If software is used, verify software input files match documented inputs (layer thicknesses, moduli, loading, tire pressure)
- [ ] **Software outputs**: Verify software output files are provided and interpreted correctly (stress, strain, deflection values and units)
- [ ] **Hand calculation check**: Verify at least one critical case is checked by hand calculation or simplified method to validate software results
- [ ] **Arithmetic verification**: Spot-check arithmetic in hand calculations or spreadsheet formulas

### Step 4: Output Review (Specification §R3.1–R3.3 | Procedure Step 4)
- [ ] **Output summary table**: Verify summary table includes pavement zone description, traffic, subgrade, layer thicknesses, critical stresses/strains, safety factors
- [ ] **Thickness results**: Verify calculated thicknesses are reasonable (compare to similar projects, design manual charts)
- [ ] **Safety factors**: Verify safety factors or reliability indices meet acceptance criteria (typically ≥1.0 for limit state design, or per design methodology)
- [ ] **Fatigue life**: Verify predicted fatigue life meets or exceeds design life (25 years or as specified)
- [ ] **Sensitivity results**: Verify sensitivity analysis shows design is robust to parameter variations (thickness changes are reasonable, not excessive)
- [ ] **OBJ-8 results**: Verify Phase 2 expansion corridor pavement thickness is adequate for ultimate loading; verify any capacity reserve during Phase 1 is documented

### Step 5: Traceability Audit (Specification §R3.2 | Procedure Step 4.2–4.4)
- [ ] **Drawing cross-references**: Verify each calculated thickness references corresponding DEL-04.01 drawing sheet and section number (use Procedure traceability matrix)
- [ ] **Specification cross-references**: Verify each material property used references corresponding DEL-04.02 specification clause
- [ ] **Test record cross-references**: Verify output summary identifies target values for DEL-04.04 field testing (thicknesses, densities)
- [ ] **Bidirectional consistency**: Verify DEL-04.01 drawing sections match calculated thicknesses; if discrepancies exist, identify for resolution
- [ ] **Terminology consistency**: Verify same terms used across Datasheet, Specification, Guidance, Procedure, DEL-04.01, DEL-04.02, DEL-04.04

### Step 6: Assumption and TBD Tracking (Specification §R3.3 | Procedure Step 1.6, 5.3)
- [ ] **All assumptions flagged**: Verify every **ASSUMPTION** in calculation is flagged inline and logged in Procedure assumption tracking log
- [ ] **All TBDs flagged**: Verify every **TBD** in calculation is flagged inline and logged in Procedure assumption tracking log
- [ ] **Coordination with DEL-04.01/04.02**: Verify assumption log cross-references DEL-04.01 and DEL-04.02 assumption logs for consistency
- [ ] **Resolution paths identified**: Verify each assumption/TBD has identified resolution path (who resolves, required data, timing)
- [ ] **Impact assessment**: Verify each assumption/TBD has impact assessment (which outputs are affected, sensitivity to assumption)
- [ ] **Critical path items**: Verify assumptions/TBDs that block construction or affect safety are identified and prioritized

### Step 7: Verification and Approval (Specification §R4.1–R4.3 | Procedure Step 5)
- [ ] **Self-check**: Verify calculation author performed and documented self-check (arithmetic, units, reasonableness, traceability)
- [ ] **Independent check**: Verify senior engineer or checker performed and documented independent check (methodology, inputs, execution, outputs)
- [ ] **Cross-document coordination**: Verify QA reviewer performed coordination review (consistency with DEL-04.01/04.02, traceability, assumption logging)
- [ ] **Approval signoffs**: Verify all required signoffs (author, checker, QA reviewer) are obtained

## Coordination Guidance

### Internal PKG-04 Coordination
- **DEL-04.01 coordination**: Schedule review meeting with DEL-04.01 drafter when calculation outputs are available; verify drawing sections match calculated thicknesses; identify any discrepancies requiring drawing or calculation revision
- **DEL-04.02 coordination**: Share calculation material property inputs with DEL-04.02 specification author for validation; update calculation if specification material changes
- **DEL-04.04 coordination**: Provide calculation output summary table to DEL-04.04 QA/QC lead as target values for field testing; identify critical test locations based on sensitivity analysis

### Cross-Package Coordination
- **Geotechnical coordination** (if PKG-03 or separate geotechnical package): Review geotechnical investigation report with geotechnical engineer; clarify any ambiguous or incomplete data; request additional testing if critical parameters are uncertain
- **PKG-05 coordination**: Share pavement loading analysis for structure-to-pavement interfaces; verify structure design accommodates pavement loading
- **PKG-07 coordination**: Share pavement loading analysis for rail crossing zones; verify rail design accommodates pavement loading and vibration
- **PKG-08 coordination**: Share pavement loading analysis for wharf edge zones; verify marine structure design accommodates pavement loading

### Owner/Engineer Coordination
- **Traffic data coordination**: Request Owner traffic loading data (vehicle types, axle loads, repetitions); if not provided, propose assumed loading for Owner approval and flag as **ASSUMPTION**
- **Design criteria coordination**: Confirm design methodology (TAC vs. AASHTO), design life, reliability level with Engineer; update calculation if criteria are clarified or revised
- **Phase 2 coordination (OBJ-8)**: Request Phase 2 ultimate loading assumptions from Owner for expansion corridor analysis; if not provided, propose conservative assumptions for Owner approval and flag as **ASSUMPTION**

## Trade-offs

### Design Conservatism vs. Economy
**Trade-off**: Conservative design (lower subgrade strength, higher traffic loading, higher reliability) increases pavement thickness and cost. Less conservative design reduces cost but increases risk of premature failure.

**Guidance**:
- Use realistic, well-documented inputs when data is available (geotechnical test results, traffic counts)
- Use conservative assumptions when data is uncertain or unavailable (err on side of safety)
- Use sensitivity analysis to understand cost impact of uncertainty (e.g., if ±20% subgrade uncertainty changes thickness by ±10 mm, cost impact is small and conservative design is justified)
- Consider life cycle cost (initial cost vs. maintenance cost vs. premature replacement cost)

### Mechanistic-Empirical vs. Empirical Design
**Trade-off**: Mechanistic-empirical design (layered elastic analysis, strain-based failure criteria) is more accurate but more complex and data-intensive. Empirical design (AASHTO empirical method, design charts) is simpler but less accurate and may not capture project-specific conditions.

**Guidance**:
- Use mechanistic-empirical design for complex projects (unusual traffic, unusual materials, critical pavements)
- Use empirical design for simple projects (standard traffic, standard materials, low-risk pavements) where simplicity and proven performance are valued
- For this project: Mechanistic-empirical approach recommended due to industrial loading, OBJ-8 future expansion requirements, and interface complexity (**ASSUMPTION** – confirm with Engineer)

### Sensitivity Analysis Depth
**Trade-off**: Extensive sensitivity analysis (many parameters, many variations) provides comprehensive understanding of design robustness but requires significant effort. Limited sensitivity analysis (few parameters, standard variations) is efficient but may miss important sensitivities.

**Guidance**:
- Always analyze sensitivity to subgrade bearing capacity (most uncertain and most influential parameter)
- Always analyze sensitivity to traffic loading (second most uncertain and influential)
- Optionally analyze sensitivity to material properties (asphalt modulus) if material properties are uncertain or non-standard
- Document sensitivity analysis scope and justify any parameters not analyzed

## Conflict Table (for human ruling)

No unresolved conflicts identified during Pass 3 cross-document consistency review.

| Conflict ID | Conflict | Source A (file + section) | Source B (file + section) | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|---------------------------|---------------------------|-------------------|-------------------|--------------|
| — | No conflicts identified | — | — | — | — | — |

**Note**: If conflicts are identified during calculation review or coordination activities (e.g., discrepancy between calculated thickness and DEL-04.01 drawing, or between material property assumption and DEL-04.02 specification), they shall be logged in this table per Specification §R3.3 and Procedure Step 4.3–4.4. Cross-deliverable conflicts that cannot be resolved locally shall be escalated to RECONCILIATION agent when humans request cross-package coherence checks.

## References

### Source Documents
- **Decomposition**: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section PKG-04, DEL-04.03, OBJ-8
- **Datasheet (DEL-04.03)**: Calculation Scope, Design Inputs, Calculation Outputs, Assumptions & TBDs, Cross-document Coordination
- **Specification (DEL-04.03)**: Requirements §R1.1–R5.2, Verification Methods, Standards
- **Procedure (DEL-04.03)**: Workflow Steps 1–7, Controls, Traceability Matrix, Assumption Log
- **DEL-04.01**: Pavement Design Drawing Set (pavement sections to validate)
- **DEL-04.02**: Pavement Technical Specification (material properties to use as inputs)
- **DEL-04.04**: Pavement Installation & Test Records (target values to provide)
- **Employer's Requirements Volume 2 Part 2**: Pavement design criteria (**location TBD**)

### Industry References
- **TAC Pavement Design and Rehabilitation Manual**: Canadian pavement design methodology
- **AASHTO Guide for Design of Pavement Structures**: US pavement design methodology
- **PCA Thickness Design for Concrete Highway and Street Pavements**: Concrete pavement design
- **ASTM D698**: Standard Proctor compaction test
- **CSA A23.1**: Concrete materials properties
