# Guidance: DEL-06.01 Structural Steel Design Drawing Set

## Purpose

- Support development of the structural steel design drawings that define arrangement and detailing for PKG-06 steel platforms, stairs, gangways, access structures, handrails, and pipe supports (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:242; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:248).
- Provide interpretation that complements the Specification and Procedure by clarifying how drawing content ties to intent, interfaces, and verification (Specification.md: Requirements; Procedure.md: Verification).

This deliverable is a **Drawing** produced by the **D&B Contractor** within the Contractor’s scope (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:248; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49).

## Principles

- Align drawing content to the Employer's Requirements-defined design basis and review expectations; treat code/standard references as **TBD** until confirmed from ER clauses (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD; Specification.md: Standards).
- Make interfaces explicit (bases, anchor bolt assumptions, equipment support points, handrail terminations, pipe support geometry) so interdisciplinary coordination can proceed even when dependencies are coordinated externally (Dependencies: NOT_TRACKED; see `_DEPENDENCIES.md`; Specification.md: Interface Requirements; Procedure.md: Steps 2, 7).
- Prefer clarity and unambiguous detailing over drawing density: reviewers should be able to trace each artifact (Platform GAs, stair drawings, gangway drawings, pipe rack drawings, handrail details) to a defined scope element and verification step (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:248; Datasheet.md: Attributes; Specification.md: Scope; Procedure.md: Steps 1, 6).

## Considerations

- Contractor-only scope focus: exclude Employer-responsible items except for required interface connections (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49; Specification.md: Interface Requirements).
- Treat governing loads, design life, and environmental criteria as **TBD** until extracted from ER volumes; avoid embedding uncited numeric values (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD; Datasheet.md: Conditions).
- Drawings should support downstream QA/QC and record deliverables (DEL-06.05 Structural Steel Installation & Test Records) by clearly identifying steelwork requiring traceability (e.g., weld inspection points, coating zones) (clauses **TBD**) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252; Datasheet.md: Construction; Specification.md: Interface Requirements).
- Use consistent cross-references: drawings should point to DEL-06.02 for materials/workmanship/coatings, DEL-06.03 for design basis assumptions, and DEL-06.04 for gangway/grating data sheets (ASSUMPTION; aligns to deliverable set intent, Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:248-252; Specification.md: Drawing Content).

## Trade-offs

- Constructability vs. minimalism: additional views/sections improve erection safety and QA but increase drafting effort (Procedure.md: Step 4; **TBD** level of detail criteria).
- Standardization vs. optimization: standardizing handrail/stair details reduces fabrication risk but may add weight/cost (**TBD**; balance against project cost/schedule priorities).
- Early issue for coordination vs. completeness: issuing early "for IDC" sets helps interfaces (Procedure.md: Step 7) but must be clearly marked (Procedure.md: Step 5; Datasheet.md: Attributes) to prevent construction misuse (ASSUMPTION; align with document control practices in Volume 2 Part 1, location TBD).

## Examples

- Use the anticipated artifact list (Platform GAs, stair drawings, gangway drawings, pipe rack drawings, handrail details) as a checklist to confirm the drawing set is complete (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:248; Datasheet.md: Attributes; Specification.md: Scope; Procedure.md: Step 1).
- Follow the project's drawing metadata and issue conventions (numbering, revisioning, transmittals) when available (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Datasheet.md: Attributes; Procedure.md: Step 5).
- Example sheet organization (ASSUMPTION / TBD): add a drawing index / sheet list grouped by the five artifact categories (platforms, stairs, gangways, pipe racks/pipe supports, handrails) to make review completeness checkable (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:248; Specification.md: Drawing Content).

## Conflict Table (for human ruling)

*No conflicts between sources identified at this time.*

| Conflict ID | Conflict | Source A (file + section) | Source B (file + section) | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|---------------------------|---------------------------|-------------------|--------------------|--------------|
| — | — | — | — | — | — | — |

## Pending Inputs (TBD Resolution)

| Item | Missing Input | Impact | Action Required |
|------|---------------|--------|-----------------|
| PI-06.01-001 | Employer's Requirements clauses for structural steel design basis (codes, loads, environmental criteria) | Cannot finalize design basis notes on drawings; design criteria remain TBD | Extract relevant clauses from Volume 2 Part 3 and confirm design criteria |
| PI-06.01-002 | Project document control procedures (numbering, revisioning, transmittal) | Drawing metadata and title block format remain TBD | Extract clauses from Volume 2 Part 1 |
| PI-06.01-003 | CAD/drafting standards | CAD layer conventions and sheet formats remain TBD | Confirm project drafting standards |

## Cross-Document Traceability

| Document | Section | Linked Content |
|----------|---------|----------------|
| Datasheet.md | Identification | Deliverable ID, package, discipline, type — must match drawing title blocks |
| Datasheet.md | Attributes | Drawing metadata (number, revision, scale, CAD standard) — keep aligned with title block conventions |
| Datasheet.md | Cross-Document Traceability | Full traceability matrix across 4 documents |
| Specification.md | Requirements: Drawing Content | Minimum content checklist referenced in Considerations |
| Specification.md | Interface Requirements | Scope exclusions (Employer items) and cross-references to DEL-06.02/03/04 |
| Specification.md | Cross-Reference Matrix | Requirement-to-verification traceability used in Trade-offs |
| Procedure.md | Steps 1–8 | Workflow that implements the Principles and Considerations |
| Procedure.md | Verification | Criteria that validate Considerations are met |

**Cross-Deliverable Consistency (PKG-06):**
- DEL-06.02: Materials/workmanship/coatings — drawings reference this specification for technical requirements
- DEL-06.03: Design basis/load cases — drawings reference calculation package for governing assumptions
- DEL-06.04: Data sheets — gangway/grating item specifics referenced where applicable
- DEL-06.05: Installation and test records — drawings identify elements requiring QA/QC traceability
