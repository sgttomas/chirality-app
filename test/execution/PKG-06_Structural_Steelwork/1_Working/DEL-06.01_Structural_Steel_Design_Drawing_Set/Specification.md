# Specification: DEL-06.01 Structural Steel Design Drawing Set

## Scope

This specification governs development of the **Structural Steel Design Drawing Set** for **PKG-06 Structural Steelwork** (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:238-252).

The deliverable defines the design arrangement and details for structural steel per Employer’s Requirements, within the Contractor’s scope of work (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:248; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49).

**Anticipated deliverable artifacts:**
- Platform GAs
- stair drawings
- gangway drawings
- pipe rack drawings
- handrail details

## Requirements

### Functional Requirements

- Provide a coherent drawing package covering the anticipated artifacts for DEL-06.01 (platforms, stairs, gangways, pipe racks/pipe supports, handrails) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:248).
- Drawings shall clearly identify structural steel elements within PKG-06 scope: platforms, stairs, gangways, access structures, handrails, pipe supports (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:242).
- Drawings shall include sufficient information for downstream detailing/fabrication, erection planning, and inspection planning (**TBD** acceptance criteria; Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD).
- Include a consistent “design basis / assumptions” note set on drawings that references the governing calculation package and technical specification (ASSUMPTION; aligns to deliverable set intent, Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:248-250).

### Drawing Content (Minimum) — **ASSUMPTION / TBD**

Until Employer's Requirements clauses and project drafting standards are extracted, the minimum expected content is treated as **ASSUMPTION** and should be confirmed (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).

- Title blocks with document control metadata (drawing number, revision, status) (Procedure.md: Step 5; Datasheet.md: Attributes).
- General notes referencing:
  - DEL-06.02 Structural Steel Technical Specification for material/workmanship/coating requirements.
  - DEL-06.03 Structural Steel Design Calculations for governing assumptions/load cases and design basis.
  - DEL-06.04 Structural Steel Data Sheet Package for gangway/grating item specifics (where applicable).
- Explicit interface assumptions where needed (base plate elevations, anchor bolt assumptions, support loads) (Procedure.md: Steps 2, 7; Dependencies: NOT_TRACKED).
- A drawing index / sheet list identifying the five anticipated artifact groups: Platform GAs, stair drawings, gangway drawings, pipe rack drawings, handrail details (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:248; Datasheet.md: Attributes; Guidance.md: Examples).

### Performance Requirements

- Drawings shall reflect the governing design basis and code/standard requirements specified in the Employer’s Requirements (specific clauses **TBD**) (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD).
- Any project-level parameters that materially constrain the steelwork arrangement (e.g., operational requirements, interface boundaries) shall be represented or cross-referenced on the drawings (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).

### Interface Requirements

- Coordinate interfaces to adjacent scopes (foundations, equipment, piping, electrical, civil) through project coordination workflows; dependency edges are not tracked in-file (see `_DEPENDENCIES.md`) (Procedure.md: Steps 2, 7; Dependencies: NOT_TRACKED).
- Where Employer-responsible items exist, include only interface connection details (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49; Guidance.md: Considerations).
- Cross-reference DEL-06.02 (Technical Specification), DEL-06.03 (Design Calculations), DEL-06.04 (Data Sheet Package), and DEL-06.05 (Installation & Test Records) so material/coating, design assumptions, and QA/QC requirements are traceable (ASSUMPTION based on deliverable set organization; Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:248-252; Datasheet.md: Construction; Guidance.md: Considerations).

### Quality Requirements

- Drawings shall comply with the project’s general requirements for document control, review/check, and quality records (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).
- Drawings shall be internally reviewed/checked before issue for review (CHECKING) (ASSUMPTION; verification workflow in Procedure.md).

## Standards

- Employer’s Requirements volumes are the controlling standards source for this deliverable; applicable structural codes/standards and drafting conventions are **TBD** until clauses are extracted (Source: test/Volume_2_Part_1_Employers_Requirements.pdf; test/Volume_2_Part_3_Employers_Requirements.pdf).

## Verification

**Verification methods for Drawing deliverables:**

- Drawing self-check + peer/independent check (Procedure.md: Steps).
- Interdisciplinary check (IDC) focusing on foundations/equipment/piping interfaces (Dependencies: NOT_TRACKED).
- CAD/drafting standard compliance check (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).

**Acceptance criteria:**
- **TBD** — to be defined per project QA/QC and document control procedures (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).

## Cross-Reference Matrix (Specification → Procedure)

| Requirement area | Primary verification step(s) | Record / evidence |
|------------------|------------------------------|------------------|
| Artifact completeness (Platform GAs, stair drawings, gangway drawings, pipe rack drawings, handrail details) | Procedure.md: Steps 1, 6 | Checked drawing set with issue/revision metadata (**TBD** checklist format; Datasheet.md: Attributes) |
| Drawing content minimum (title blocks, general notes, interfaces, drawing index) | Procedure.md: Steps 5, 6 | Self-check and independent check records (**TBD**) |
| Interfaces (foundations/equipment/piping) | Procedure.md: Steps 2, 7 | IDC comments / resolutions (**TBD**; Guidance.md: Principles) |
| Cross-references to DEL-06.02, DEL-06.03, DEL-06.04 | Procedure.md: Steps 3, 4, 6 | Drawing note verification (Datasheet.md: Construction; Guidance.md: Considerations) |
| Document control / metadata | Procedure.md: Step 5 | Transmittal / revision history (**TBD**; Datasheet.md: Attributes) |
| Quality review (self-check, IDC, independent check) | Procedure.md: Steps 6, 7, 8 | Check records and approval signatures (**TBD**) |

## Documentation

**Required documentation outputs:**
- Platform GAs
- stair drawings
- gangway drawings
- pipe rack drawings
- handrail details

**Documentation requirements:**
- All documents shall comply with project document control procedures (**TBD** specifics) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).
- Revision control per project numbering system — **TBD**.
- Ensure drawing metadata aligns with `Datasheet.md` attributes and the document control requirements for issue packaging (Procedure.md: Records).

## Cross-Document Notes

- Datasheet: defines the core identification and metadata expectations for the drawing set and should stay consistent with this specification (Datasheet.md: Attributes).
- Guidance: provides intent and trade-offs so the drawing conventions support constructability, safety, and review clarity (Guidance.md: Principles, Considerations).
- Procedure: defines the workflow and verification checks that demonstrate requirements satisfaction before the drawing set is released (Procedure.md: Steps, Verification).
