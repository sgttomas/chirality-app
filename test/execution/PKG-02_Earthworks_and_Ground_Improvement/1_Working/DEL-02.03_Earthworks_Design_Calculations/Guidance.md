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

| Attribute | Value |
|-----------|-------|
| Specification mapping | R1, R5, R6 |
| Datasheet mapping | Check status, Calculation method attributes |
| Procedure Step | Steps 3, 4.4 |

### P2: Traceability and Documentation
**Principle:** Calculations must be traceable from inputs through methods to outputs; all sources, assumptions, and criteria must be documented.

**Rationale:** Traceability enables design verification, independent checking, future modifications, and regulatory compliance. Poor documentation creates ambiguity and rework.

**Application:**
- Clearly identify and reference all input data sources (DEL-02.04, DEL-02.05, ER, codes/standards).
- Document all assumptions explicitly; state basis for assumptions where possible.
- Show calculation method step-by-step; cite equations, code clauses, or software tools used.
- Present results clearly with units and significant figures appropriate to input precision.
- Include sketches or diagrams where they aid understanding.
- **ASSUMPTION**: Standard calculation format per project or Contractor template.

| Attribute | Value |
|-----------|-------|
| Specification mapping | R5, R6 |
| Datasheet mapping | Calculation format attribute |
| Procedure Step | Steps 2.3, 3.3 |

### P3: Design Conservatism and Factor of Safety
**Principle:** Apply appropriate factors of safety and conservative assumptions where uncertainties exist.

**Rationale:** Geotechnical parameters, loading conditions, and construction variability introduce uncertainty. Conservative design reduces risk of bearing capacity failure, excessive settlement, or inadequate cut/fill balance.

**Application:**
- Use code-required or ER-specified factors of safety for bearing capacity.
- Apply conservative soil parameters where site investigation data is limited.
- Account for construction tolerances in cut/fill calculations.
- Balance conservatism with economy; excessive conservatism increases cost.
- Document basis for safety factors and conservative assumptions.
- **TBD**: Specific factors of safety and design criteria pending ER and DEL-02.04.

| Attribute | Value |
|-----------|-------|
| Specification mapping | R1, R3 |
| Datasheet mapping | Calculation Content section 2 (bearing capacity) |
| Procedure Step | Step 3.2 |

### P4: Multi-Deliverable Coordination
**Principle:** Ensure calculation outputs are consistent with design drawings, specifications, geotechnical reports, and survey data.

**Rationale:** Calculations exist within a web of interdependent deliverables. Inconsistencies between calculations, drawings, and specifications create field confusion and rework.

**Application:**
- Cut/fill quantities (R2) must align with DEL-02.01 grading plans and DEL-02.05 survey topography.
- Bearing capacity results (R3) must support loads in DEL-02.01 and criteria in DEL-02.02.
- Calculation assumptions must be consistent with DEL-02.04 geotechnical recommendations.
- Coordination typically managed through design review and issue cycle.
- **ASSUMPTION**: Multi-disciplinary design coordination process in place.

| Attribute | Value |
|-----------|-------|
| Specification mapping | R1, R2, R3, R4; enables V4 |
| Datasheet mapping | All Calculation Content sections |
| Procedure Step | Steps 1, 3, 4.5 |

## Requirement-Principle Traceability

| Requirement | Principles Applied | Key Considerations | Procedure Step |
|-------------|-------------------|-------------------|----------------|
| R1: Engineering basis and verification | P1, P2, P3 | Accuracy, traceability, conservatism | Steps 1-3 |
| R2: Cut/fill quantity calculations | P1, P2, P4 | Accurate survey data, coordination with drawings, allowances | Step 3.1 |
| R3: Bearing capacity calculations | P1, P2, P3, P4 | Valid geotechnical data, safety factors, coordination | Step 3.2 |
| R4: PKG-02 scope coverage | P4 | Multi-deliverable coordination, completeness | Step 2.1 |
| R5: Design basis documentation | P2, P3 | Traceability, assumptions documented, references cited | Steps 2.3, 3.3 |
| R6: Document control and checking | P1, P2 | Independent check, revision control, approvals | Steps 2.4, 4.4, 5 |

## Considerations

### Calculation Development Considerations

1. **Input Data Quality and Availability:**
   - Confirm geotechnical investigation from DEL-02.04 is complete for bearing capacity calculations.
   - Confirm topographic survey from DEL-02.05 has sufficient accuracy for cut/fill calculations.
   - Identify design criteria and loading conditions from ER and adjacent packages.
   - **TBD**: Specific input data pending DEL-02.04, DEL-02.05, and ER.
   - **Procedure reference:** Step 1.

2. **Calculation Methods and Tools:**
   - Select appropriate calculation methods per codes/standards and ER requirements.
   - Use software tools where appropriate; document software version and settings.
   - Verify software results with hand calculations or benchmark cases where feasible.
   - **TBD**: Specific methods and tools pending ER and design criteria.
   - **Procedure reference:** Step 3.

3. **Design Assumptions:**
   - Clearly state all assumptions (soil parameters, loading conditions, factors of safety).
   - Verify assumptions are reasonable and conservative where uncertainty exists.
   - Coordinate assumptions with DEL-02.04 geotechnical recommendations.
   - Flag assumptions requiring validation or confirmation.
   - **Procedure reference:** Step 3.

4. **Output Application:**
   - Cut/fill quantities inform construction cost estimates, material procurement, scheduling.
   - Bearing capacity results inform ground improvement requirements, foundation depths.
   - Ensure outputs are in format usable by downstream deliverables.
   - **Procedure reference:** Step 3.

### QA/QC Considerations

1. **Independent Checking:**
   - Independent check required per R6; checker must be different qualified engineer.
   - Checker verifies inputs, methods, calculations, and results; signs off on calculation package.
   - Checker checks coordination with related deliverables.
   - **ASSUMPTION**: Standard engineering checking practice per project QA/QC plan.
   - **Procedure reference:** Step 4.4.

2. **Cross-Document Verification:**
   - Confirm calculation outputs align with DEL-02.01, DEL-02.02, DEL-02.04.
   - Verify terminology and values are consistent across all four documents.
   - **Procedure reference:** Step 4.6.

3. **Review Workflow:**
   - Internal calculation check (independent checker).
   - Design review for coordination with drawings and specifications.
   - Geotechnical review for bearing capacity calculations (if warranted).
   - Employer review and approval per R6 document control requirements.
   - **ASSUMPTION**: Standard D&B QA/QC workflow applies.
   - **Procedure reference:** Step 4.

## Trade-offs

### Calculation Detail and Complexity
**Trade-off:** More detailed calculations provide higher confidence but require more effort. Simpler calculations are faster but may require conservative assumptions.

**Guidance:**
- Use detail level appropriate to design significance and project risk.
- Critical calculations warrant detailed analysis.
- Less critical calculations may use simplified conservative methods.
- Balance effort with schedule and budget constraints.

| Attribute | Value |
|-----------|-------|
| Principle reference | P1 (Accuracy), P3 (Conservatism) |
| Specification mapping | R1, R2, R3 |
| Procedure Step | Step 3 |

### Software vs. Manual Calculations
**Trade-off:** Software enables complex analysis and automation but requires validation. Manual calculations are more transparent but may be impractical for complex geometry.

**Guidance:**
- Use software for tasks where it provides efficiency (3D cut/fill modeling, iterative analysis).
- Use manual calculations for simple or critical checks, or to verify software results.
- Document software tools, versions, and key inputs/settings.

| Attribute | Value |
|-----------|-------|
| Principle reference | P1 (Accuracy), P2 (Traceability) |
| Datasheet mapping | Software/tools attribute |
| Procedure Step | Step 3 |

### Design Conservatism Level
**Trade-off:** Conservative design reduces risk but may increase cost. Optimized design reduces cost but requires higher confidence in inputs.

**Guidance:**
- Apply code-required or ER-specified factors of safety as baseline.
- Use conservative assumptions where data is limited or uncertain.
- Balance risk and cost; document basis for conservatism level.

| Attribute | Value |
|-----------|-------|
| Principle reference | P3 (Design Conservatism) |
| Specification mapping | R1, R3 |
| Procedure Step | Step 3.2 |

## Examples

**Note:** Specific examples require ER requirements, DEL-02.04 geotechnical data, and DEL-02.05 survey data.

1. **Cut/Fill Quantity Calculation Example (R2):**
   - **Inputs:** Existing topography from DEL-02.05; proposed finish grades from DEL-02.01.
   - **Method:** Average end area method or DTM (Civil 3D).
   - **Outputs:** Total cut = [TBD] m³; Total fill = [TBD] m³.
   - **Allowances:** +5% for compaction shrinkage, +2% for over-excavation; **ASSUMPTION**.
   - **Procedure reference:** Step 3.1.

2. **Bearing Capacity Calculation Example (R3):**
   - **Inputs:** Soil parameters from DEL-02.04 (φ = [TBD]°, c = [TBD] kPa).
   - **Method:** Terzaghi bearing capacity equation; FS = [TBD].
   - **Outputs:** Ultimate bearing capacity qu = [TBD] kPa; Allowable qa = [TBD] kPa.
   - **Procedure reference:** Step 3.2.

## Procedure Coordination

| Procedure Step | Guidance Element | Key Focus |
|----------------|------------------|-----------|
| Step 1 | Considerations (Input Data Quality) | Validate inputs before calculations |
| Step 2 | P4 (Coordination), R4 | Define scope and documentation requirements |
| Step 3 | P1, P2, P3, P4, Trade-offs | Develop calculations |
| Step 4 | P1 (Verification), QA/QC Considerations, V1-V4 | Check and verify |
| Step 5 | R6 (Document Control) | Control and issue deliverable |

## Conflict Table (for human ruling)

No conflicts identified from available sources at this stage. If conflicts arise during calculation development, document here with:

| Column | Description |
|--------|-------------|
| Conflict ID | Unique identifier |
| Conflict | Short statement of conflict |
| Source A | File + section |
| Source B | File + section |
| Impacted requirements | R1-R6 affected |
| Proposed resolution | PROPOSAL |
| Human ruling | TBD |

## Cross-Document Traceability

| Document | Key Linkages |
|----------|--------------|
| Datasheet.md | Attributes mapped to P1-P4; Calculation Content sections |
| Specification.md | Requirements R1-R6 mapped to P1-P4; V1-V4 linked to QA/QC Considerations |
| Procedure.md | Steps 1-5 implement principles and verification expectations |

## References

| Reference | Description | Location |
|-----------|-------------|----------|
| _CONTEXT.md | Deliverable identity, description, anticipated artifacts | This folder |
| Decomposition | PKG-02 scope, DEL-02.03 entry, Section 1.2 Scope Focus | `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (location TBD) |
| Specification.md | Requirements R1-R6, Verification V1-V4 | This folder |
| Datasheet.md | Calculation content and attributes | This folder |
| Procedure.md | Steps 1-5, Verification, Records | This folder |
| _REFERENCES.md | ER volumes and reference materials | This folder (currently empty; pending) |
| Related deliverables | DEL-02.01, DEL-02.02, DEL-02.04, DEL-02.05 | PKG-02 |
