# Guidance: DEL-07.02 Rail Works Technical Specification

**Enrichment Status:** Pass 3 Complete (3-pass enrichment: Initial draft, Cross-reference enrichment, Final reconciliation)

## Purpose
- Guide creation of the rail works technical specification capturing performance, materials, and workmanship requirements for PKG-07 rail works (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:259, :266).
- Ensure the specification is structured so downstream deliverables (drawings, calculations, ITRs) can reference it consistently (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:265-268).

## Principles
- Treat the Employer’s Requirements as authoritative; extract clauses into requirements statements and mark any gaps as **TBD** (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, clauses TBD).
- Keep scope aligned to PKG-07 rail works (Tracks 6 & 7 new works; Track 5 restoration/modifications; ballast; end stops) and avoid specifying Employer-responsible scope except interfaces (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47, :259).
- Write requirements so they are verifiable: each requirement should have a verification method and a record output (enabling DEL-07.04) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:268).

## Considerations
- Organize the document around the anticipated artifacts list (rail, ballast, track construction) so completeness is obvious (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:266).
- Identify where calculations (DEL-07.03) provide the design basis for performance criteria and reference them explicitly once available (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:267).
- Coordinate interfaces through external coordination workflows (NOT_TRACKED; see `_DEPENDENCIES.md`) and document assumptions/constraints clearly (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47).
- Maintain an explicit requirements traceability / compliance matrix so any **TBD** and **ASSUMPTION/PROPOSAL** items are visible for resolution and so DEL-07.04 record requirements can be traced back to governing clauses (Source: Procedure.md: Steps; and test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:268).

## Trade-offs
- Specificity vs flexibility: overly prescriptive specs can constrain design changes, while vague specs can cause rework and QA ambiguity; balance is **TBD** until ER clauses are extracted (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, clauses TBD).
- Template reuse vs project-specific needs: reuse structure where helpful, but ensure unique rail works constraints are captured explicitly.

## Examples (from anticipated artifacts)
- Rail specification section covering material/workmanship/testing requirements (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:266).
- Ballast specification section covering material gradation/placement/testing requirements (TBD until ER clauses are extracted; Source: test/Volume_2_Part_2_Employers_Requirements.pdf, clauses TBD).
- Track construction specification section covering construction tolerances, inspections, and records linkage to DEL-07.04 (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:268).

## Cross-Document Notes
- Datasheet: Datasheet.md captures the metadata/document control fields to align with the ER general requirements (TBD).
- Specification: Specification.md is the normative requirement set; ensure every requirement is traceable to ER clauses or marked **ASSUMPTION/PROPOSAL**.
- Procedure: Procedure.md defines the drafting/review steps used to demonstrate the specification was checked prior to issue.
