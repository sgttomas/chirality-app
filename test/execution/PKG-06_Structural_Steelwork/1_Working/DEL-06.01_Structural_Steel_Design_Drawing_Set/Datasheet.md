# Datasheet: DEL-06.01 Structural Steel Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-06.01 |
| Name | Structural Steel Design Drawing Set |
| Package | PKG-06 Structural Steelwork |
| Discipline | Structural |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value | Specification § | Procedure Step |
|-----------|-------|-----------------|----------------|
| Drawing Number | Per project numbering / document control system (**TBD**, Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD) | Documentation | Step 5 |
| Sheet Size | Per project drawing standards (**TBD**, Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD) | Drawing Content | Step 5 |
| Scale | Per drawing content; legible at issue size (**TBD**, Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD) | Drawing Content | Step 4 |
| CAD Standard | Per project CAD / drafting convention (**TBD**, Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD) | Standards | Step 5 |
| Revision | 00 (initial draft) — **ASSUMPTION** pending project revision scheme | Documentation | Step 5 |
| Classification | Structural – Steelwork (PKG-06) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:238-252) | Scope | — |
| Drawing Set Scope | Platform GAs, stair drawings, gangway drawings, pipe rack drawings, handrail details (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:248) | Scope | Steps 1, 6 |

## Conditions

**Context & intended use:**
- This deliverable defines the design arrangement and detailing for structural steelwork within the Contractor’s scope (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:248; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49).
- Package scope includes steel platforms, stairs, gangways, access structures, handrails, and pipe supports (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:242).
- Intended users: engineering/design reviewers, fabricators (shop drawing development), construction/QA teams (ASSUMPTION; to be confirmed in ER clauses).

**Design/environmental criteria:** **TBD** (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD). See DEL-06.03 Structural Steel Design Calculations for governing design basis, load cases, and code requirements (Specification.md: Interface Requirements; Guidance.md: Considerations).

## Construction

**Configuration focus (drawing content):**

Anticipated artifacts within this drawing set (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:248; `_CONTEXT.md`):
- Platform general arrangements (GAs)
- Stair drawings
- Gangway drawings
- Pipe rack / pipe support drawings
- Handrail details

**Material definition approach:** steel member sizes, material grades, protective coatings, and connection detailing are shown and/or referenced on drawings; materials/workmanship/coating requirements cross-reference DEL-06.02 Structural Steel Technical Specification (details **TBD** until Employer's Requirements clauses and design basis are extracted) (Specification.md: Requirements; Guidance.md: Considerations).

**Linked deliverables (for traceability):**
- DEL-06.02 Structural Steel Technical Specification (materials/workmanship/coatings)
- DEL-06.03 Structural Steel Design Calculations (assumptions, load cases, governing results)
- DEL-06.04 Structural Steel Data Sheet Package (gangway/grating item sheets, where applicable)
- DEL-06.05 Structural Steel Installation & Test Records (inspection/records evidence)

## References

- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:238-252 — PKG-06 scope and DEL-06.01 definition.
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49 — scope focus (Contractor scope only; Employer-responsible items excluded except interfaces).
- test/Volume_2_Part_1_Employers_Requirements.pdf — general requirements: document control / QA expectations (location TBD).
- test/Volume_2_Part_3_Employers_Requirements.pdf — building works requirements affecting structural steel (location TBD).
- See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally).
- See `_REFERENCES.md` and `execution/PKG-06_Structural_Steelwork/0_References/` for package reference index (currently empty / TBD).

## Cross-Document Traceability

| Document | Section | Linked Content |
|----------|---------|----------------|
| Specification.md | Scope | Anticipated artifacts (Platform GAs, stair drawings, gangway drawings, pipe rack drawings, handrail details) |
| Specification.md | Requirements: Drawing Content | Minimum content requirements (title blocks, general notes, interfaces, drawing index) |
| Specification.md | Documentation | Document control and revision requirements |
| Specification.md | Cross-Reference Matrix | Requirement-to-verification traceability |
| Guidance.md | Principles | Intent behind drawing conventions and interface explicitness |
| Guidance.md | Considerations | Trade-offs for constructability, QA/QC support, cross-references |
| Procedure.md | Steps 1–8 | Production and verification workflow |
| Procedure.md | Verification | Acceptance criteria for scope completeness, content minimum, interfaces |
| Procedure.md | Records | Documentation outputs matching this Datasheet's scope |

**Cross-Deliverable Consistency (PKG-06):**
- DEL-06.02: Materials, workmanship, and coating requirements referenced on drawings
- DEL-06.03: Design basis, load cases, and governing calculations referenced in drawing notes
- DEL-06.04: Gangway/grating item data sheets referenced where applicable
- DEL-06.05: Installation and test records requiring traceability to drawing elements (weld inspection points, coating zones)
