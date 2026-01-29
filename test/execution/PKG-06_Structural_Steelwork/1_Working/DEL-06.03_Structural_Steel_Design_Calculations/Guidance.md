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

## Local Conflict Table (if unresolved)

| Topic | Issue | Impact | Needed to resolve | Owner |
|-------|-------|--------|-------------------|-------|
| Design basis | ER clauses for loads/design criteria not yet extracted for steelwork | Calculations cannot be finalized | Identify relevant ER clauses and confirm design basis | Human |

## Cross-Document Notes

- Datasheet: calculation number, software, design basis/code, load cases should remain consistent with document control and the Procedure's release workflow (Datasheet.md: Attributes; Procedure.md: Steps).
- Drawings (DEL-06.01): calculation assumptions/results (governing load cases, member sizing, design notes) should be reflected in drawing notes/details where applicable (DEL-06.01 Specification.md: Interface Requirements; Specification.md: Cross-Document Notes).
- Technical Specification (DEL-06.02): material/coating/workmanship assumptions must align between calculations and specification clauses (DEL-06.02 Specification.md; Specification.md: Cross-Document Notes).
- Data Sheets (DEL-06.04): gangway/grating standard details requiring design justification should be traceable to this calculation package (Specification.md: Cross-Document Notes).
- Installation/Test Records (DEL-06.05): calculation-identified critical items (critical welds, bolting categories, coating systems) should map to inspection/record requirements (Specification.md: Cross-Document Notes; Considerations).
- Specification → Procedure traceability: use the `Specification.md` Cross-Reference Matrix to keep calculation evidence aligned to requirements.
