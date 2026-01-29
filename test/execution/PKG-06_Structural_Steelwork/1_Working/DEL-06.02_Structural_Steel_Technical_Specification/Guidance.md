# Guidance: DEL-06.02 Structural Steel Technical Specification

## Purpose

- Support development of the technical specification defining performance, materials, and workmanship requirements for PKG-06 structural steelwork (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:249).
- Provide interpretation so the specification clauses remain consistent with drawings, calculations, data sheets, and installation/test records deliverables (DEL-06.01 through DEL-06.05) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:248-252).

This deliverable is a **Specification** produced by the **D&B Contractor** within the Contractor’s scope (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:249; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49).

## Principles

- Traceability first: write clauses so QA/QC records (mill certificates, weld inspection records, galvanizing certificates) can demonstrate compliance via DEL-06.05 Structural Steel Installation & Test Records (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252; Specification.md: Quality Requirements, Records and Submittals; Procedure.md: Step 4).
- Use Employer's Requirements as the primary authority for codes/standards, tolerances, and acceptance criteria; do not embed unsourced standards lists (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD; Specification.md: Standards; Procedure.md: Step 1).
- Keep the interface boundary explicit: include only Contractor scope, and treat Employer-responsible items as interface-only (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49; Specification.md: Interface Requirements; Datasheet.md: Conditions).

## Considerations

- Ensure the document structure mirrors the anticipated artifacts list (Structural steel specification, Handrail specification, Grating specification) so reviewers can find requirements quickly (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:249; Datasheet.md: Attributes; Specification.md: Scope; Procedure.md: Step 2).
- Align key assumptions and terminology with the drawing set (DEL-06.01), calculations (DEL-06.03), and data sheets (DEL-06.04) deliverables; discrepancies become rework late in design (ASSUMPTION; dependencies coordinated externally; Specification.md: Functional Requirements; Procedure.md: Verification).
- Identify sections that are presently **TBD** due to missing ER clause extraction (e.g., governing codes, coating systems, inspection regimes) to avoid false precision (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD; Specification.md: Standards, Performance Requirements; Procedure.md: Step 3).
- Ensure clauses are "recordable": for each major requirement, name the evidence/record expected (mill certificates, weld inspection records, galvanizing certificates) so DEL-06.05 can compile without guesswork (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252; Specification.md: Records and Submittals; Procedure.md: Step 4).

## Trade-offs

- Prescriptive vs performance-based clauses: prescriptive clauses simplify procurement and QA, but may constrain Contractor means/methods (TBD until ER intent is confirmed; Specification.md: Requirements; Procedure.md: Step 3).
- One combined document vs multiple sub-specs: splitting into three documents (Structural steel specification, Handrail specification, Grating specification) improves focus but increases coordination overhead; decomposition anticipates all three artifacts (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:249; Datasheet.md: Attributes; Specification.md: Scope; Procedure.md: Step 2).

## Examples

- Add a "Records and Submittals" section that enumerates the record types needed for DEL-06.05 Structural Steel Installation & Test Records (mill certificates, weld inspection records, galvanizing certificates) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252; Specification.md: Records and Submittals, Cross-Reference Matrix; Procedure.md: Step 4).
- Include a "Drawing/Calculation References" section indicating how the specification ties to DEL-06.01 (Design Drawing Set), DEL-06.03 (Design Calculations), and DEL-06.04 (Data Sheet Package) for design basis and traceability (ASSUMPTION; cross-document traceability; Specification.md: Interface Requirements; Datasheet.md: Construction).

## Conflict Table (for human ruling)

*No conflicts between sources identified at this time.*

| Conflict ID | Conflict | Source A (file + section) | Source B (file + section) | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|---------------------------|---------------------------|-------------------|--------------------|--------------|
| — | — | — | — | — | — | — |

## Pending Inputs (TBD Resolution)

| Item | Missing Input | Impact | Action Required |
|------|---------------|--------|-----------------|
| PI-06.02-001 | Employer's Requirements clauses for structural steel/handrail/grating standards | Cannot finalize acceptance criteria; codes remain TBD | Extract relevant clauses from Volume 2 Part 3 |
| PI-06.02-002 | Coating/protective treatment requirements | Galvanizing/coating specifications remain TBD | Extract coating clauses from ER |
| PI-06.02-003 | Inspection and hold point requirements | QA/QC hold points and acceptance criteria remain TBD | Extract inspection clauses from ER |

## Cross-Document Traceability

| Document | Section | Linked Content |
|----------|---------|----------------|
| Datasheet.md | Identification | Deliverable identity consistent with Scope |
| Datasheet.md | Attributes | Document metadata (number, revision, standards) — keep aligned with issue workflow |
| Datasheet.md | Construction | Linked deliverables (DEL-06.01/03/04/05) for traceability |
| Specification.md | Requirements | Clause structure that Procedure verifies |
| Specification.md | Records and Submittals | Record types aligned to DEL-06.05 |
| Specification.md | Cross-Reference Matrix | Requirement-to-verification-to-records traceability |
| Procedure.md | Steps 1–6 | Workflow implementing the Principles and Considerations |
| Procedure.md | Verification | Criteria that validate Considerations are met |

**Cross-Deliverable Consistency (PKG-06):**
- DEL-06.01: Drawing notes reference this specification; terminology must align
- DEL-06.03: Design basis assumptions inform performance requirements; values must be consistent
- DEL-06.04: Data sheet fields reflect this specification's material/coating requirements
- DEL-06.05: Record types (mill certificates, weld inspection, galvanizing certificates) called up in this specification
