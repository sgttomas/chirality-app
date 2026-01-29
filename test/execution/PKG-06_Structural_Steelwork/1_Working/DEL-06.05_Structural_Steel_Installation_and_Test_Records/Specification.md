# Specification: DEL-06.05 Structural Steel Installation & Test Records

## Scope

This deliverable provides evidence of completion, inspection, and testing for structural steelwork within **PKG-06 Structural Steelwork** (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252).

**Anticipated record artifacts:**
- Mill certificates
- Weld inspection records
- Galvanizing certificates

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252; Datasheet.md: Attributes; Procedure.md: Step 1; Guidance.md: Principles)

## Requirements

### Functional Requirements

- Provide a records package that demonstrates compliance to the structural steel technical specification and Employer’s Requirements (**TBD** explicit clause mapping) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).
- Ensure each record is traceable to the relevant steel item/assembly (e.g., heat number, item ID, drawing reference) (**TBD** traceability method) (ASSUMPTION; to be aligned with document control requirements).

### Record Index Structure (ASSUMPTION / TBD)

To improve completeness and auditability, compile an index that links each steelwork item to required record types. Format requirements remain **TBD** until ER clauses are extracted (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).

Minimum index fields (ASSUMPTION):
- Item ID (from drawings/BOM) (DEL-06.01 Structural Steel Design Drawing Set; Datasheet.md: Construction; Procedure.md: Step 2)
- Drawing reference(s) (DEL-06.01; Datasheet.md: Construction)
- Specification clause reference(s) driving the record (DEL-06.02 Structural Steel Technical Specification; Datasheet.md: Construction)
- Data sheet reference (DEL-06.04 Structural Steel Data Sheet Package where applicable; Datasheet.md: Cross-Document Points)
- Record category (Mill certificates / Weld inspection records / Galvanizing certificates) (Datasheet.md: Attributes; Guidance.md: Principles)
- Record identifier / filename and revision (Procedure.md: Step 5)
- Date / inspector or issuer (Guidance.md: Considerations; Procedure.md: Step 4)
- Status (received/accepted/TBD) (Procedure.md: Step 5)

### Performance Requirements

- Record acceptance criteria and test/inspection results against the governing specification requirements (**TBD** criteria until DEL-06.02 clauses are finalized) (DEL-06.02 Specification.md).

### Interface Requirements

- Coordinate record package requirements with the specification and data sheet field lists; dependencies are not tracked in-file (see `_DEPENDENCIES.md`) (Dependencies: NOT_TRACKED).
- Where Employer-responsible items exist, include records only for Contractor scope items and interface work as applicable (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49).

### Quality Requirements

- Records shall comply with the project’s document control and QA/QC requirements (format, approvals, retention, distribution) (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).
- Include signatures/identification of inspector/author, dates, and revision history as required (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).

## Standards

- Governing standards for inspection/testing and certification are **TBD** until extracted from Employer’s Requirements and the technical specification clauses (Source: test/Volume_2_Part_1_Employers_Requirements.pdf; test/Volume_2_Part_3_Employers_Requirements.pdf).

## Verification

- Completeness check: records provided for all required categories (mill certs / weld inspection / galvanizing) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252).
- Traceability check: each record maps to item ID(s) / drawings / data sheets (**TBD** mapping method).
- Archival check: files meet document control requirements (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).

## Cross-Reference Matrix (Specification → Procedure → Records)

| Requirement area | Primary procedure step(s) | Evidence / record type |
|------------------|---------------------------|------------------------|
| Required record categories defined (Mill certificates, Weld inspection records, Galvanizing certificates) | Procedure.md: Step 1 | Record category register (Datasheet.md: Attributes; Guidance.md: Principles) |
| Traceability scheme defined (item IDs, heat numbers, drawing references, spec clauses) | Procedure.md: Step 2 | Item ID / heat / drawing / spec clause mapping rules (**TBD**; Record Index Structure; Datasheet.md: Attributes; Guidance.md: Considerations) |
| Records collected from vendors/inspectors | Procedure.md: Step 3 | Vendor certificates + inspection reports with required identifiers (Guidance.md: Considerations) |
| Records verified (required fields, signatures, acceptance criteria) | Procedure.md: Step 4 | QA checklist / sign-offs (**TBD**; Guidance.md: Considerations) |
| Indexed package compiled (records index + folder structure + compiled PDF set) | Procedure.md: Step 5 | Records index (per Record Index Structure) + compiled PDF set (**TBD**; Datasheet.md: Construction; Guidance.md: Examples) |
| Document control applied | Procedure.md: Step 6 | Revision history / approvals (**TBD**; Datasheet.md: Attributes) |

## Documentation

**Deliverable artifacts:**
- Mill certificates
- Weld inspection records
- Galvanizing certificates

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252; Datasheet.md: Attributes; Procedure.md: Step 1)

**Documentation requirements:**
- Maintain revision history and approvals per document control requirements (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Datasheet.md: Attributes; Procedure.md: Step 6).
- Record package files (index + supporting PDFs), checklists, approval/sign-off evidence (**TBD**) (Procedure.md: Records).

## Cross-Document Notes

- Datasheet: record package number, record categories, traceability basis should remain consistent with document control and the Procedure's release workflow (Datasheet.md: Attributes; Procedure.md: Steps).
- Technical Specification (DEL-06.02): record package should align to inspection/hold points, acceptance criteria, and certificate requirements in the specification clauses for materials, fabrication, and protective systems (DEL-06.02 Specification.md: Quality Requirements, Records and Submittals; Datasheet.md: Cross-Document Points).
- Drawings (DEL-06.01): trace records to drawing item IDs, assemblies, and critical weld/coating locations (Datasheet.md: Cross-Document Points).
- Design Calculations (DEL-06.03): critical design assumptions affecting inspection/hold points should be traceable to record requirements (DEL-06.03 Specification.md: Cross-Document Notes; Datasheet.md: Cross-Document Points).
- Data Sheets (DEL-06.04): use "Required Records" fields to drive record completeness for gangway and grating items (DEL-06.04 Specification.md: Quality Requirements, Suggested Field Sets; Datasheet.md: Cross-Document Points).
- Guidance: provides principles and considerations for traceability, completeness, and record organization (Guidance.md: Principles, Considerations).
- Procedure: defines how records are collected, verified, indexed, and compiled (Procedure.md: Steps, Verification).
