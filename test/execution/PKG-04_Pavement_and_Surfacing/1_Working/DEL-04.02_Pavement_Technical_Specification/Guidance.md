# Guidance: DEL-04.02 Pavement Technical Specification

## Purpose

This guidance clarifies how to review and coordinate the Pavement Technical Specification (DEL-04.02) to ensure specification clauses are complete, technically sound, and consistent with DEL-04.01 (drawings), DEL-04.03 (calculations), and DEL-04.04 (test records), while maintaining OBJ-8 future expansion enforceability.

## Principles

### P1: Every Clause Must Be Enforceable and Verifiable
Specification clauses must be written such that:
- Requirements are objective and measurable (avoid subjective terms like "sufficient", "adequate", "proper" without quantification)
- Acceptance criteria are clearly stated (numerical limits, test methods, standards)
- Non-conformance is determinable (pass/fail decision is unambiguous)
- Testing or inspection method is specified (how conformance is verified)

**Rationale**: Ambiguous specification clauses lead to disputes during construction and acceptance. Clear, enforceable requirements enable efficient quality control per DEL-04.04.

### P2: Traceability Enables Change Management
Every specification requirement must trace to:
- Drawing element (DEL-04.01 section, detail, or note it governs)
- Calculation basis (DEL-04.03 design input or output)
- Testing procedure (DEL-04.04 test method and acceptance criterion)
- Employer's Requirement or standard (authoritative source)

**Rationale**: When drawings or calculations are revised, traceability identifies which specification clauses require review and update, preventing inconsistencies.

### P3: Assumptions and TBDs Must Not Be Hidden
Specification clauses based on **ASSUMPTION** or pending **TBD** resolution must be explicitly flagged:
- State the assumption or pending input clearly in the clause
- Reference the assumption tracking log ID
- Identify the resolution path (who resolves, required input, timing)

**Rationale**: Hidden assumptions become requirements that may not reflect actual project conditions. Flagging them enables prioritized resolution before construction.

### P4: Interface Requirements Prevent Rework
Interfaces between PKG-04 and adjacent packages (PKG-03, PKG-05, PKG-07, PKG-08) are high-risk areas for construction conflicts:
- Specification must clearly state coordination requirements (sequence, elevations, tolerances, protection measures)
- Interface clauses must be reviewed with adjacent package leads before issuance
- Changes to adjacent package work must trigger specification review

**Rationale**: Interface mismatches discovered during construction cause costly delays and rework. Specification-level coordination prevents issues.

## Considerations

### Specification Style and Language
- **Active voice with "shall"**: Use "Contractor shall..." for mandatory requirements (avoid passive voice "The subgrade will be compacted...")
- **Consistent terminology**: Use the same terms as DEL-04.01 drawings and DEL-04.03 calculations (e.g., if drawings say "wearing course", don't use "surface course" in specification)
- **Avoid redundancy**: Don't repeat standard specifications verbatim; reference the standard and state project-specific deviations only
- **Numerical precision**: State tolerances with appropriate precision (e.g., "±10 mm" not "approximately 10 mm")

### Material Specification Approach
- **Performance vs. prescriptive**: Performance specifications state required properties (e.g., "asphalt binder meeting PG 58-34"); prescriptive specifications state exact materials (e.g., "XYZ brand asphalt binder"). Performance specifications allow contractor flexibility and competition; prescriptive specifications ensure specific material. Use performance approach unless ER requires specific product.
- **Equivalency provisions**: If specifying by brand name, include "or approved equal" and state basis of equivalency (performance properties that must be matched)
- **Material sourcing restrictions**: If ER restricts material sources (e.g., local aggregate only, approved supplier list), state clearly in specification

### Testing Frequency Balance
- **Statistical sufficiency**: Testing frequency must be high enough to provide confidence in acceptance decision (sampling theory)
- **Cost vs. risk**: Higher testing frequency increases cost but reduces risk of accepting non-conforming work
- **Industry standards**: Use testing frequencies from applicable standards (OPSS, MMCD, TAC) as baseline; adjust for project-specific risk or Owner requirements
- **Critical areas**: Specify higher testing frequency in critical areas (heavy load zones, Phase 2 expansion corridors per OBJ-8)

### Submittal Review Timing
- **Lead time adequacy**: Ensure submittal approval lead times (e.g., 30 days for mix designs) are realistic for review, testing, and approval cycle
- **Dependencies**: Identify submittal dependencies (e.g., aggregate source approval before mix design submittal)
- **Re-submittal provisions**: Specify requirements for re-submittal if initial submittal is rejected (what must be corrected, re-testing requirements)

## Review Checklist

### Pre-Review Preparation (Procedure Step 3.1)
- [ ] Confirm Datasheet Assumptions & TBDs are current
- [ ] Obtain latest DEL-04.01 drawing set for cross-referencing material call-outs and tolerances
- [ ] Obtain latest DEL-04.03 calculation results for material properties and design parameters
- [ ] Review Procedure assumption log to identify open items affecting specification clauses

### Step 1: Material Clause Review (Specification §R1.1 | Procedure Step 2.3)
- [ ] **Asphalt materials**: Binder grade, aggregate gradation, filler, RAP content limits, tack coat specified
- [ ] **Concrete materials**: Cement type, strength class, aggregate requirements, admixtures, reinforcement, joint materials, curing compounds specified
- [ ] **Base/subbase materials**: Aggregate gradation, plasticity limits, compaction properties specified
- [ ] **Line marking materials**: Paint or thermoplastic type, color, reflectivity, primer specified
- [ ] **Standard references**: Each material clause references applicable standard (OPSS, MMCD, ASTM, CSA, AASHTO) or flags as **TBD**
- [ ] **Owner-approved standards**: Verify standards referenced are acceptable per ER (or flag as **ASSUMPTION** pending ER confirmation)
- [ ] **Material sourcing**: Submittal requirements, approval lead times, and equivalency provisions stated
- [ ] **Cross-references**: Material specifications match DEL-04.01 drawing material call-outs (use Procedure traceability matrix to verify)
- [ ] **Calculation consistency**: Material properties (strength, density, gradation) match DEL-04.03 design inputs

### Step 2: Workmanship Clause Review (Specification §R1.2 | Procedure Step 2.4)
- [ ] **Subgrade preparation**: Clearing, grading, moisture conditioning, compaction, proof rolling procedures specified
- [ ] **Base/subbase placement**: Lift thickness, moisture control, compaction, surface preparation specified
- [ ] **Asphalt paving**: Mix temperature, weather limitations, placement procedures, compaction equipment and pattern, joint construction specified
- [ ] **Concrete placement**: Formwork, mixing, placing, finishing, joint construction, curing procedures specified
- [ ] **Line marking**: Surface preparation, application equipment, material application rate, bead application, weather limitations specified
- [ ] **Tolerances**: Grade tolerance, thickness tolerance, smoothness tolerance specified and consistent with DEL-04.01 drawing tolerances
- [ ] **Interface handling**: Transitions to utilities (PKG-03), structures (PKG-05), rail (PKG-07), marine (PKG-08) specified
- [ ] **Construction sequence**: Sequence of operations specified where order matters (e.g., subgrade compaction before base placement)
- [ ] **Environmental controls**: Dust control, erosion control, stormwater management during construction specified (coordinate with PKG-03 or site establishment PKG-00)

### Step 3: Quality Control Clause Review (Specification §R1.3 | Procedure Step 2.5)
- [ ] **Material testing**: Aggregate gradation, asphalt mix verification, concrete strength, concrete air content testing specified with frequencies
- [ ] **In-place testing**: Subgrade compaction, base compaction, asphalt compaction, thickness verification (cores), smoothness testing specified with frequencies
- [ ] **Testing methods**: Specific test methods referenced (ASTM D698, D1556, D6938, etc.)
- [ ] **Acceptance criteria**: Numerical limits stated for each test (compaction %, strength MPa, thickness tolerance mm, etc.)
- [ ] **Testing frequency sufficiency**: Verify testing frequency provides adequate statistical confidence (consider area coverage, risk level, industry standards)
- [ ] **Testing feasibility**: Verify testing methods and frequencies are feasible given project scope and schedule
- [ ] **Laboratory accreditation**: Testing laboratory accreditation requirements specified (ISO 17025 or equivalent)
- [ ] **Non-conformance procedures**: Identification, documentation, corrective action, re-testing, and disposition procedures specified
- [ ] **Documentation requirements**: Daily QC reports, material certifications, mix design submittals, test location plans, core sample results, NCR procedures specified (supporting DEL-04.04)
- [ ] **OBJ-8 enhanced testing**: Higher testing frequency or additional testing specified for Phase 2 expansion corridor areas (e.g., double standard frequency)

### Step 4: Interface Coordination Review (Specification §R1.4 | Procedure Step 3.4)
- [ ] **PKG-03 interfaces**: Utility trench backfill compaction, pavement restoration, catch basin rim adjustments, schedule coordination specified
- [ ] **PKG-05 interfaces**: Structure-to-pavement transitions, grade matching, joint construction, drainage, foundation protection specified
- [ ] **PKG-07 interfaces**: Rail crossing embedment, track elevation coordination, compaction restrictions, drainage at crossings specified
- [ ] **PKG-08 interfaces**: Pavement termination at wharf edge, drainage, edge protection, loading compatibility, construction sequence specified
- [ ] **Coordination meetings**: Verify interface clauses have been reviewed with PKG-03, PKG-05, PKG-07, PKG-08 package leads
- [ ] **Interface assumptions**: Any assumptions regarding adjacent package work are flagged and logged in assumption tracking log

### Step 5: OBJ-8 Future Expandability Review (Specification §R1.5 | Procedure Step 2.6)
- [ ] **Design for ultimate loading**: Specification states Phase 2 expansion corridor pavement designed for ultimate loading (reference DEL-04.03 Phase 2 design case)
- [ ] **Construction joint details**: Sawcut or formed joints at Phase 2 tie-in locations specified; joint protection measures specified
- [ ] **Utility penetration documentation**: Requirement to document utility penetrations through pavement specified (coordinate with PKG-03)
- [ ] **Enhanced as-built documentation**: Survey verification, material records, compaction test location plans with enhanced detail for expansion corridors specified
- [ ] **Enforceability**: Verify OBJ-8 provisions are clear, measurable, and enforceable (not vague or aspirational)

### Step 6: Traceability Audit (Specification §R2.1–R2.3 | Procedure Step 2.7)
- [ ] **Drawing cross-references**: Every material and tolerance in specification references corresponding DEL-04.01 drawing section/detail (use Procedure traceability matrix)
- [ ] **Calculation cross-references**: Material properties and thicknesses reference corresponding DEL-04.03 calculation sheets (use Procedure traceability matrix)
- [ ] **Test record cross-references**: Quality control requirements reference DEL-04.04 test record templates
- [ ] **Bidirectional consistency**: Drawing material call-outs reference specification clause numbers; specification clauses reference drawing sheet/detail numbers
- [ ] **Terminology consistency**: Same terms used across Datasheet, Specification, Guidance, Procedure, DEL-04.01, DEL-04.03, DEL-04.04

### Step 7: Assumption and TBD Tracking (Specification §R3.2 | Procedure Steps 1.3–1.5, 3.3)
- [ ] **All assumptions flagged**: Every **ASSUMPTION** in specification is flagged inline and logged in Procedure assumption tracking log
- [ ] **All TBDs flagged**: Every **TBD** in specification is flagged inline and logged in Procedure assumption tracking log
- [ ] **Coordination with DEL-04.01/04.03**: Assumption log cross-references DEL-04.01 and DEL-04.03 assumption logs for consistency
- [ ] **Resolution paths identified**: Each assumption/TBD has identified resolution path (who resolves, required input, timing)
- [ ] **Critical path items**: Assumptions/TBDs that block construction are identified and prioritized

## Coordination Guidance

### Internal PKG-04 Coordination
- **DEL-04.01 coordination**: Schedule review meetings with DEL-04.01 drafter when specification material or tolerance clauses are drafted; verify drawing call-outs match specification clause numbers
- **DEL-04.03 coordination**: Share specification material property clauses with DEL-04.03 engineer for validation against calculation inputs; update specification if calculations reveal different properties are needed
- **DEL-04.04 coordination**: Provide draft specification quality control section to DEL-04.04 QA/QC lead early to enable test record template development; verify testing requirements are documented in DEL-04.04 procedures

### Cross-Package Coordination
- **PKG-03 coordination meetings**: Review utility trench backfill compaction requirements, pavement restoration sequence, catch basin rim adjustment requirements
- **PKG-05 coordination meetings**: Review structure-to-pavement transition details, grade matching tolerances, joint construction methods
- **PKG-07 coordination meetings**: Review rail crossing embedment requirements, track elevation coordination, compaction restrictions near track
- **PKG-08 coordination meetings**: Review pavement termination details, loading compatibility, construction sequence relative to wharf completion

### Owner/Engineer Coordination
- **ER clarification RFIs**: Prepare RFIs for ambiguous or missing pavement specification requirements in ER; propose interpretations with **ASSUMPTION** flagging in specification until ER response received
- **Standards approval**: Confirm applicable standards (OPSS vs. MMCD, TAC design manual edition, CSA edition) with Owner/Engineer; flag as **ASSUMPTION** until confirmed
- **Submittal procedure confirmation**: Verify submittal approval lead times and procedures with Owner/Engineer or project quality plan

## Trade-offs

### Prescriptive vs. Performance Specifications
**Trade-off**: Prescriptive specifications (specifying exact materials, procedures, equipment) provide certainty but reduce contractor flexibility. Performance specifications (specifying required outcomes) allow optimization but increase risk of non-conformance if acceptance criteria are not well-defined.

**Guidance**:
- Use performance specifications where ER allows flexibility and where multiple material/method options are acceptable
- Use prescriptive specifications where specific material or method is required by ER, or where performance criteria are difficult to verify
- Ensure performance specifications have clear, objective acceptance criteria (numerical limits, test methods)

### Testing Frequency: Cost vs. Risk
**Trade-off**: Higher testing frequency increases construction cost and time but reduces risk of accepting non-conforming work. Lower frequency reduces cost but increases acceptance risk.

**Guidance**:
- Use baseline testing frequencies from applicable standards (OPSS, MMCD, TAC)
- Increase frequency for critical areas (heavy load zones, Phase 2 expansion corridors per OBJ-8)
- Decrease frequency for low-risk areas only if ER permits and Owner approves
- Consider contractor's quality control record (higher frequency for unproven contractors)

### Standard Reference vs. Specification Text
**Trade-off**: Referencing standards by number (e.g., "per OPSS 310") minimizes specification length but requires readers to obtain standards. Repeating standard text in specification makes it self-contained but risks transcription errors and version control issues.

**Guidance**:
- Reference standards by number and edition (e.g., "OPSS 310, Revision 2020")
- State project-specific deviations or additions to standard in specification text
- Do not repeat standard text verbatim; summarize key points if needed for clarity
- Provide standard references list in specification for contractor convenience

## Conflict Table (for human ruling)

No unresolved conflicts identified during Pass 3 cross-document consistency review.

| Conflict ID | Conflict | Source A (file + section) | Source B (file + section) | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|---------------------------|---------------------------|-------------------|-------------------|--------------|
| — | No conflicts identified | — | — | — | — | — |

**Note**: If conflicts are identified during future reviews or coordination activities, they shall be logged in this table per Specification §R3.2 and Procedure Step 3.3. Cross-deliverable conflicts (e.g., with DEL-04.01, DEL-04.03, DEL-04.04, or PKG-03/05/07/08) that cannot be resolved locally shall be escalated to RECONCILIATION agent when humans request cross-package coherence checks.

## References

### Source Documents
- **Decomposition**: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section PKG-04, DEL-04.02, OBJ-8
- **Datasheet (DEL-04.02)**: Attributes, Key Performance Requirements, Conditions, Construction, Assumptions & TBDs, Cross-document Coordination
- **Specification (DEL-04.02)**: Requirements §R1.1–R3.3, Verification Methods, Standards
- **Procedure (DEL-04.02)**: Workflow Steps 1–6, Controls, Traceability Matrix, Assumption Log
- **DEL-04.01**: Pavement Design Drawing Set (material call-outs and tolerances to match)
- **DEL-04.03**: Pavement Design Calculations (material properties and design parameters to validate)
- **DEL-04.04**: Pavement Installation & Test Records (testing procedures and acceptance criteria to support)
- **Employer's Requirements Volume 2 Part 1 & 2**: Specification requirements (**location TBD**)

### Industry References
- **OPSS** (Ontario Provincial Standard Specifications) or **MMCD** (BC Master Municipal Construction Documents): Standard pavement specifications
- **TAC Pavement Design and Rehabilitation Manual**: Design methodology and material standards
- **CSA A23.1/A23.2**: Concrete materials and testing standards
- **ASTM D698, D1556, D6938, D4123**: Testing method standards
- **AASHTO M320**: Performance Grade Asphalt Binder specification
