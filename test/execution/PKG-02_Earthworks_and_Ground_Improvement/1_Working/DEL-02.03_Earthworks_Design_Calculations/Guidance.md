# Guidance: DEL-02.03 Earthworks Design Calculations

## Purpose

Provide calculation principles and practical considerations to ensure Earthworks Design Calculations achieve accuracy, traceability, and design adequacy while satisfying PKG-02 objectives and Specification requirements R1-R6.

**Deliverable Role:** Design calculations establish the engineering basis for earthworks design. They translate geotechnical data and design criteria into quantified outputs (cut/fill volumes, bearing capacity) that inform design drawings (DEL-02.01), specifications (DEL-02.02), and construction execution.

Source: _CONTEXT.md; decomposition DEL-02.03 entry (location TBD).

## Principles

### P1: Accuracy and Verification
**Principle:** Calculations must be accurate, independently checked, and based on valid inputs and methods.

**Rationale:** Design calculations form the engineering basis for earthworks construction. Errors propagate to drawings, specifications, and field execution, creating safety and cost risks.

**Application:**
- Use established calculation methods from recognized codes and standards.
- Document all assumptions and verify they are reasonable.
- Independent check required by qualified engineer (different from preparer) per R6.
- Verify calculation inputs (geotechnical data, survey data, loads) are from approved sources.
- Cross-check results for reasonableness and consistency.
- **ASSUMPTION**: Aligns with standard engineering QA/QC practice.

**Specification mapping:** Supports R1 (engineering basis), R5 (documentation), R6 (checking).

### P2: Traceability and Documentation
**Principle:** Calculations must be traceable from inputs through methods to outputs; all sources, assumptions, and criteria must be documented.

**Rationale:** Traceability enables design verification, independent checking, future modifications, and regulatory compliance. Poor documentation creates ambiguity and rework.

**Application:**
- Clearly identify and reference all input data sources (DEL-02.04, DEL-02.05, ER, codes/standards).
- Document all assumptions explicitly; state basis for assumptions where possible.
- Show calculation method step-by-step; cite equations, code clauses, or software tools used.
- Present results clearly with units and significant figures appropriate to input precision.
- Include sketches or diagrams where they aid understanding (e.g., bearing capacity model, cross-section locations).
- **ASSUMPTION**: Standard calculation format per project or Contractor template.

**Specification mapping:** Supports R5 (design basis documentation), R6 (document control).

### P3: Design Conservatism and Factor of Safety
**Principle:** Apply appropriate factors of safety and conservative assumptions where uncertainties exist.

**Rationale:** Geotechnical parameters, loading conditions, and construction variability introduce uncertainty. Conservative design reduces risk of bearing capacity failure, excessive settlement, or inadequate cut/fill balance.

**Application:**
- Use code-required or ER-specified factors of safety for bearing capacity.
- Apply conservative soil parameters where site investigation data is limited.
- Account for construction tolerances in cut/fill calculations (e.g., over-excavation, compaction shrinkage).
- Balance conservatism with economy; excessive conservatism increases cost without proportional risk reduction.
- Document basis for safety factors and conservative assumptions.
- **TBD**: Specific factors of safety and design criteria pending ER requirements and DEL-02.04.

**Specification mapping:** Supports R1 (engineering basis), R3 (bearing capacity).

### P4: Multi-Deliverable Coordination
**Principle:** Ensure calculation outputs are consistent with design drawings, specifications, geotechnical reports, and survey data.

**Rationale:** Calculations exist within a web of interdependent deliverables. Inconsistencies between calculations, drawings, and specifications create field confusion and rework.

**Application:**
- Cut/fill quantities (R2) must align with DEL-02.01 grading plans and DEL-02.05 survey topography.
- Bearing capacity results (R3) must support loads shown in DEL-02.01 and performance criteria in DEL-02.02.
- Calculation assumptions must be consistent with DEL-02.04 geotechnical recommendations.
- Coordination typically managed through design review and issue cycle.
- **ASSUMPTION**: Multi-disciplinary design coordination process in place.

**Specification mapping:** Supports R1, R2, R3, R4; enables verification V4 (calculation accuracy and coordination).

## Requirement Guidance

| Requirement | Principles Applied | Key Considerations |
|-------------|-------------------|-------------------|
| R1: Engineering basis and verification | P1, P2, P3 | Accuracy, traceability, conservatism |
| R2: Cut/fill quantity calculations | P1, P2, P4 | Accurate survey data, coordination with drawings, allowances for tolerances |
| R3: Bearing capacity calculations | P1, P2, P3, P4 | Valid geotechnical data, appropriate safety factors, coordination with loads and ground improvement |
| R4: PKG-02 scope coverage | P4 | Multi-deliverable coordination, completeness |
| R5: Design basis documentation | P2, P3 | Traceability, assumptions documented, references cited |
| R6: Document control and checking | P1, P2 | Independent check, revision control, approvals |

## Considerations

### Calculation Development Considerations

1. **Input Data Quality and Availability:**
   - Confirm geotechnical investigation from DEL-02.04 is complete and provides adequate data for bearing capacity calculations.
   - Confirm topographic survey from DEL-02.05 has sufficient accuracy and coverage for cut/fill calculations.
   - Identify design criteria and loading conditions from ER and adjacent packages.
   - **TBD**: Specific input data pending DEL-02.04, DEL-02.05, and ER.

2. **Calculation Methods and Tools:**
   - Select appropriate calculation methods per codes/standards and ER requirements.
   - Use software tools where appropriate (Civil 3D for cut/fill, geotechnical software for bearing capacity); document software version and settings.
   - Verify software results with hand calculations or benchmark cases where feasible.
   - **TBD**: Specific methods and tools pending ER and design criteria.

3. **Design Assumptions:**
   - Clearly state all assumptions (soil parameters, loading conditions, factors of safety, construction tolerances).
   - Verify assumptions are reasonable and conservative where uncertainty exists.
   - Coordinate assumptions with DEL-02.04 geotechnical recommendations.
   - Flag assumptions requiring validation or confirmation.

4. **Output Application:**
   - Cut/fill quantities inform construction cost estimates, material procurement, and scheduling.
   - Bearing capacity results inform ground improvement requirements, foundation depths, and pavement design.
   - Ensure outputs are in format usable by downstream deliverables (drawings, specifications, construction planning).

### QA/QC Considerations

1. **Independent Checking:**
   - Independent check required per R6; checker must be different qualified engineer than preparer.
   - Checker verifies inputs, methods, calculations, and results; signs off on calculation package.
   - Checker checks coordination with related deliverables (drawings, specifications, geotechnical reports).
   - **ASSUMPTION**: Standard engineering checking practice per project QA/QC plan.

2. **Cross-Document Verification:**
   - Confirm calculation outputs align with DEL-02.01 (Design Drawing Set), DEL-02.02 (Technical Specification), DEL-02.04 (Geotechnical Reports).
   - Verify terminology and values are consistent across all four documents (Datasheet, Specification, Guidance, Procedure).

3. **Review Workflow:**
   - Internal calculation check (independent checker).
   - Design review for coordination with drawings and specifications.
   - Geotechnical review for bearing capacity calculations (if warranted).
   - Employer review and approval per R6 document control requirements.
   - **ASSUMPTION**: Standard D&B QA/QC workflow applies.

## Trade-offs

### Calculation Detail and Complexity
**Trade-off:** More detailed calculations provide higher confidence but require more effort and time. Simpler calculations are faster but may be less accurate or require conservative assumptions.

**Guidance:**
- Use detail level appropriate to design significance and project risk.
- Critical or high-consequence calculations (bearing capacity near structures, large cut/fill volumes) warrant detailed analysis.
- Less critical calculations may use simplified conservative methods.
- Balance effort with schedule and budget constraints.
- **ASSUMPTION**: Design-build projects favor efficient calculations with appropriate conservatism.

**Principle reference:** P1 (Accuracy), P3 (Conservatism).

**Procedure coordination:** Step 3 in Procedure.md addresses calculation development where this balance is applied.

### Software vs. Manual Calculations
**Trade-off:** Software enables complex analysis and automation but requires validation and documentation. Manual calculations are more transparent but may be impractical for complex geometry or iterative analysis.

**Guidance:**
- Use software for tasks where it provides clear efficiency (3D cut/fill modeling, iterative bearing capacity analysis).
- Use manual calculations for simple or critical checks, or to verify software results.
- Document software tools, versions, and key inputs/settings.
- Verify software results with hand calculations or benchmark cases where feasible.
- **TBD**: Software tools pending project standards and ER requirements.

**Principle reference:** P1 (Accuracy and Verification), P2 (Traceability).

### Design Conservatism Level
**Trade-off:** Conservative design reduces risk but may increase cost (excessive ground improvement, over-excavation, larger factors of safety). Optimized design reduces cost but requires higher confidence in inputs and methods.

**Guidance:**
- Apply code-required or ER-specified factors of safety as baseline.
- Use conservative assumptions where data is limited or uncertain (e.g., sparse geotechnical investigation, variable soil conditions).
- Use less conservative assumptions where data is robust and risks are well-understood.
- Consider construction variability and quality control capability when selecting factors of safety.
- Balance risk and cost; document basis for conservatism level.
- **TBD**: ER may specify required conservatism or design philosophy.

**Principle reference:** P3 (Design Conservatism and Factor of Safety).

## Examples

**Note:** Specific examples require ER requirements, DEL-02.04 geotechnical data, and DEL-02.05 survey data. The following are typical examples for this deliverable type:

1. **Cut/Fill Quantity Calculation Example (R2):**
   - **Inputs:** Existing topography from DEL-02.05; proposed finish grades from DEL-02.01; grading limits.
   - **Method:** Average end area method or DTM (Civil 3D).
   - **Outputs:** Total cut = [TBD] m³; Total fill = [TBD] m³; Net balance = [TBD] m³.
   - **Allowances:** +5% for compaction shrinkage, +2% for over-excavation tolerance; **ASSUMPTION**.
   - **TBD**: Specific volumes pending survey data and design.

2. **Bearing Capacity Calculation Example (R3):**
   - **Inputs:** Soil parameters from DEL-02.04 (friction angle φ = [TBD]°, cohesion c = [TBD] kPa); foundation depth D = [TBD] m; groundwater depth = [TBD] m.
   - **Method:** Terzaghi bearing capacity equation; factor of safety = [TBD] (typically 2.5-3.0).
   - **Outputs:** Ultimate bearing capacity qu = [TBD] kPa; Allowable bearing capacity qa = qu/FS = [TBD] kPa.
   - **Verification:** Compare qa to design loads from pavements/structures; if inadequate, specify ground improvement.
   - **TBD**: Specific values pending DEL-02.04 geotechnical data and design criteria.

## Procedure Coordination

Steps in Procedure.md implement the verification expectations and calculation principles outlined above:

- **Step 1:** Input compilation addresses Considerations (Input Data Quality and Availability).
- **Step 2:** Scope confirmation addresses Principle P4 (Coordination) and R4.
- **Step 3:** Calculation development addresses Principles P1 (Accuracy), P2 (Traceability), P3 (Conservatism), P4 (Coordination).
- **Step 4:** Checking and verification address P1 (Verification), P2 (Documentation), and verification V1-V4.
- **Step 5:** Issuance addresses R6 (Document Control).

## Conflict Table (for human ruling)

No conflicts identified from available sources at this stage. If conflicts arise during calculation development (e.g., between ER design criteria and geotechnical recommendations, between survey data and existing site conditions, or between calculation results and design feasibility), they should be documented here with:

- Conflict ID
- Conflict description
- Source A (file + section)
- Source B (file + section)
- Impacted requirements
- Proposed resolution
- Human ruling (TBD)

## References

- _CONTEXT.md: Deliverable identity, description, and anticipated artifacts.
- Decomposition file: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — PKG-02 scope, DEL-02.03 entry, Section 1.2 Scope Focus (location TBD).
- Specification.md: Requirements R1-R6 and verification items V1-V4.
- Datasheet.md: Calculation content and attributes.
- Procedure.md: Calculation workflow steps 1-5.
- _REFERENCES.md: Currently empty; ER volumes and reference materials pending.
- Related deliverables: DEL-02.01, DEL-02.02, DEL-02.04, DEL-02.05.
