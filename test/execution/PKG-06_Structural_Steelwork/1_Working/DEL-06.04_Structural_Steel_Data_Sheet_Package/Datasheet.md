# Datasheet: DEL-06.04 Structural Steel Data Sheet Package

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-06.04 |
| Name | Structural Steel Data Sheet Package |
| Package | PKG-06 Structural Steelwork |
| Discipline | Structural |
| Type | Data Sheet |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Data Sheet Package Number | Per project numbering / document control system (**TBD**, Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD) |
| Included Data Sheets | Gangway data sheets; Grating data sheets (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:251; Specification.md: Scope; Procedure.md: Step 1) |
| Item Identification | Tag/ID scheme **TBD** (to align with drawings and BOM) (Specification.md: Interface Requirements; Procedure.md: Step 3; Guidance.md: Principles) |
| Revision | 00 (initial draft) — **ASSUMPTION** pending project revision scheme (Procedure.md: Step 5) |
| Classification | Structural – Steelwork (PKG-06) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:238-252) |

## Conditions

**Context & intended use:**
- This deliverable defines and substantiates structural steelwork items via data sheets in accordance with Employer’s Requirements (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:251).
- Package scope includes steel platforms, stairs, gangways, access structures, handrails, and pipe supports; this data sheet package focuses on gangways and grating as listed in the anticipated artifacts (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:242; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:251).

**Design/environmental criteria referenced by these data sheets:** **TBD** (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD).

## Construction

**Data sheet content focus:**

Anticipated artifacts (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:251; `_CONTEXT.md`):
- Gangway data sheets
- Grating data sheets

Each data sheet should capture (at minimum): geometry, material/protective system, design basis references, and any inspection/acceptance requirements (**TBD** until ER clauses extracted).

**Suggested data sheet fields (ASSUMPTION / TBD):**
- Item ID / Tag (aligned to drawings DEL-06.01) (Specification.md: Interface Requirements; Guidance.md: Principles)
- Drawing reference(s) (DEL-06.01 Structural Steel Design Drawing Set) (Specification.md: Suggested Field Sets)
- Specification clause reference(s) (DEL-06.02 Structural Steel Technical Specification) (Specification.md: Suggested Field Sets; Guidance.md: Cross-Document Notes)
- Calculation reference(s), where applicable (DEL-06.03 Structural Steel Design Calculations) (Specification.md: Suggested Field Sets; Guidance.md: Cross-Document Notes)
- Material / protective system identifier (TBD; references DEL-06.02)
- Required records / certificates (DEL-06.05 Structural Steel Installation & Test Records: mill certificates, weld inspection records, galvanizing certificates) (Specification.md: Quality Requirements, Suggested Field Sets; Guidance.md: Considerations)

## References

- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:238-252 — PKG-06 scope and DEL-06.04 definition.
- test/Volume_2_Part_1_Employers_Requirements.pdf — general requirements: document control / QA expectations (location TBD).
- test/Volume_2_Part_3_Employers_Requirements.pdf — building works requirements affecting gangways/grating (location TBD).
- See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally).
- See `_REFERENCES.md` and `execution/PKG-06_Structural_Steelwork/0_References/` for package reference index (currently empty / TBD).

## Cross-Document Points

- Technical Specification (DEL-06.02): data sheet fields should reflect the material/workmanship/coating clauses (DEL-06.02 Specification.md).
- Design Calculations (DEL-06.03): data sheets should reference any calculation assumptions or design loads where applicable (DEL-06.03 Specification.md).
- Drawings (DEL-06.01): item IDs and configurations should match drawings to avoid mismatches at procurement/installation.
- Specification → Procedure traceability: see `Specification.md` Cross-Reference Matrix for how requirements map to Procedure steps and evidence.
