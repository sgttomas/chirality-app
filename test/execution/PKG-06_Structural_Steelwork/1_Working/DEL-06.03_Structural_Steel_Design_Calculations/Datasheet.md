# Datasheet: DEL-06.03 Structural Steel Design Calculations

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-06.03 |
| Name | Structural Steel Design Calculations |
| Package | PKG-06 Structural Steelwork |
| Discipline | Structural |
| Type | Calculation |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Calculation Number | Per project numbering / document control system (**TBD**, Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD) |
| Software Used | **TBD** (to be recorded when analysis method is selected) (Procedure.md: Step 3) |
| Design Basis / Code | **TBD** until extracted from Employer's Requirements (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD; Specification.md: Standards; Guidance.md: Principles) |
| Load Cases | **TBD** (to be listed explicitly in the calculation index) (Specification.md: Calculation Package Structure; Procedure.md: Step 4) |
| Revision | 00 (initial draft) — **ASSUMPTION** pending project revision scheme (Procedure.md: Step 7) |
| Classification | Structural – Steelwork (PKG-06) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:238-252) |
| Calculation Coverage | Platform structural calculations, Pipe rack calculations, Connection design calculations (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:250; Specification.md: Scope; Procedure.md: Step 1) |

## Conditions

**Context & intended use:**
- This deliverable provides the engineering basis and sizing/verification calculations for PKG-06 structural steelwork (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:250).
- Package scope includes steel platforms, stairs, gangways, access structures, handrails, and pipe supports (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:242).
- Intended users: structural designer/checker, interdisciplinary reviewers, and (as needed) fabricator/contractor review (ASSUMPTION; confirm in ER clauses).

**Design/environmental criteria:** **TBD** (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD).

## Construction

**Calculation artifacts (anticipated):**

Anticipated artifacts (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:250; `_CONTEXT.md`):
- Platform structural calculations
- Pipe rack calculations
- Connection design calculations

**Outputs expected:** calculation summaries, governing assumptions, load cases, results summary, interface assumptions register, and independent check record that can be referenced by drawings (DEL-06.01) and specification (DEL-06.02) (ASSUMPTION; to be refined when ER clauses are extracted) (Specification.md: Calculation Package Structure; Guidance.md: Examples).

**Linked deliverables (for traceability):**
- DEL-06.01 Structural Steel Design Drawing Set (drawing notes and details reference calculation assumptions, governing load cases, and results for member sizing)
- DEL-06.02 Structural Steel Technical Specification (material/coating/workmanship assumptions aligned; performance requirements reference design basis from calculations)
- DEL-06.04 Structural Steel Data Sheet Package (gangway/grating item sheets reference design justification where applicable)
- DEL-06.05 Structural Steel Installation & Test Records (critical welds, bolting categories, coating systems requiring inspection based on design assumptions) (Specification.md: Cross-Document Notes; Guidance.md: Cross-Document Notes, Considerations)

## References

- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:238-252 — PKG-06 scope and DEL-06.03 definition.
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49 — scope focus (Contractor scope only; Employer-responsible items excluded except interfaces).
- test/Volume_2_Part_1_Employers_Requirements.pdf — general requirements: document control / QA expectations (location TBD).
- test/Volume_2_Part_3_Employers_Requirements.pdf — building works requirements affecting structural steel design basis (location TBD).
- See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally).

## Cross-Document Points

- Specification (DEL-06.02): calculation assumptions and governing criteria should align to the technical specification clauses (DEL-06.02 Specification.md).
- Drawings (DEL-06.01): drawing notes and details should be consistent with calculation assumptions and results (DEL-06.01 Guidance.md; DEL-06.01 Specification.md).
- Data sheets (DEL-06.04): any standard details (gangway/grating) requiring design justification should be traceable to this calculation package (DEL-06.04 Guidance.md).
- Specification → Procedure traceability: see `Specification.md` Cross-Reference Matrix for how requirements map to Procedure steps and evidence.
