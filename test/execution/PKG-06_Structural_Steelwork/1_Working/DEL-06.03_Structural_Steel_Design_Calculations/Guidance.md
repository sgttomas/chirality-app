# Guidance: DEL-06.03 Structural Steel Design Calculations

## Purpose

- Support development of the calculation package that provides engineering basis and sizing/verification for PKG-06 structural steelwork (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:250).
- Provide interpretation so the calculation assumptions/results remain consistent with drawings, specification, data sheets, and QA record requirements (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:248-252).

This deliverable is a **Calculation** produced by the **D&B Contractor** within the Contractor’s scope (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:250; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49).

## Principles

- Traceability: calculations should clearly state inputs, assumptions, load cases, and governing outcomes so reviewers can link results to drawing details (DEL-06.01) and specification clauses (DEL-06.02) (ASSUMPTION; best practice; Specification.md: Calculation Package Structure; Cross-Document Notes).
- Use Employer's Requirements as the authority for design basis, codes/standards, and environmental criteria; do not embed unsourced code lists (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD; Specification.md: Standards; Datasheet.md: Attributes).
- Highlight interface assumptions explicitly (support conditions, equipment and piping loads, foundation stiffness assumptions) in an Interface Assumptions Register because dependencies are coordinated externally (Dependencies: NOT_TRACKED; see `_DEPENDENCIES.md`; Specification.md: Calculation Package Structure; Examples).

## Considerations

- Ensure the calculation package covers the three anticipated artifacts: Platform structural calculations, Pipe rack calculations, Connection design calculations (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:250; Datasheet.md: Attributes; Specification.md: Scope; Procedure.md: Step 1).
- Identify where assumptions are pending (loads, exposure class, corrosion allowance/protective systems, design life) and mark as **TBD** rather than inventing values (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD; Specification.md: Calculation Package Structure; Datasheet.md: Attributes).
- Consider how calculation outcomes affect downstream installation/test records (DEL-06.05) — e.g., critical welds, bolting categories, coating systems requiring inspection (ASSUMPTION; DEL-06.05 record types include mill certificates, weld inspection records, galvanizing certificates, Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252; Specification.md: Cross-Document Notes; Datasheet.md: Construction).

## Trade-offs

- Simplified hand calcs vs detailed 3D analysis: simplified methods can be transparent but may miss load paths; analysis detail level is **TBD** pending ER requirements and design complexity (Specification.md: Performance Requirements; Procedure.md: Step 3; Datasheet.md: Attributes).
- Conservative assumptions vs material efficiency: conservative load/path assumptions reduce risk but may increase steel tonnage; decisions should be documented in calculation narratives and results summary (TBD; Specification.md: Calculation Package Structure; Procedure.md: Step 5).

## Examples

- Provide a "Load Case Summary" and "Governing Member Summary" table to help the drawing team (DEL-06.01) place key notes/details (ASSUMPTION; format TBD; Specification.md: Calculation Package Structure; Procedure.md: Step 5).
- Include an "Interface Assumptions Register" capturing assumed loads/supports from other disciplines (equipment/piping loads, foundation assumptions) (Dependencies: NOT_TRACKED; format TBD; Specification.md: Calculation Package Structure; Principles).
- Example section headers (ASSUMPTION / TBD): "Calculation Index", "Assumptions", "Inputs", "Analysis Method", "Load Cases/Combinations", "Results Summary", "Independent Check Record", "Drawing Notes/Implications" (Specification.md: Calculation Package Structure).

## Conflict Table (for human ruling)

*No conflicts between sources identified at this time.*

| Conflict ID | Conflict | Source A (file + section) | Source B (file + section) | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|---------------------------|---------------------------|-------------------|--------------------|--------------|
| — | — | — | — | — | — | — |

## Pending Inputs (TBD Resolution)

| Item | Missing Input | Impact | Action Required |
|------|---------------|--------|-----------------|
| PI-06.03-001 | Employer's Requirements clauses for loads/design criteria | Calculations cannot be finalized; load cases remain TBD | Extract relevant clauses from Volume 2 Part 3 |
| PI-06.03-002 | Project calculation/document control standards | Calculation format and numbering remain TBD | Extract clauses from Volume 2 Part 1 |
| PI-06.03-003 | Design life and environmental criteria | Durability and exposure assumptions remain TBD | Confirm design basis with ER clauses |

## Cross-Document Traceability

| Document | Section | Linked Content |
|----------|---------|----------------|
| Datasheet.md | Identification | Deliverable identity consistent with Scope |
| Datasheet.md | Attributes | Calculation metadata (number, software, design basis, load cases) — keep aligned with issue workflow |
| Datasheet.md | Construction | Linked deliverables (DEL-06.01/02/04/05) for traceability |
| Specification.md | Calculation Package Structure | Minimum content requirements referenced in Considerations |
| Specification.md | Cross-Reference Matrix | Requirement-to-verification traceability |
| Procedure.md | Steps 1–7 | Workflow implementing the Principles and Considerations |
| Procedure.md | Verification | Criteria that validate Considerations are met |

**Cross-Deliverable Consistency (PKG-06):**
- DEL-06.01: Calculation assumptions/results (governing load cases, member sizing) reflected in drawing notes/details
- DEL-06.02: Material/coating/workmanship assumptions aligned between calculations and specification clauses
- DEL-06.04: Gangway/grating design justification traceable to this calculation package
- DEL-06.05: Critical items (welds, bolting, coating systems) identified in calculations map to inspection/record requirements
