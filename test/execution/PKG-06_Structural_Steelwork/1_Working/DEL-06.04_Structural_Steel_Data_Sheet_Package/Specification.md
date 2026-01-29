# Specification: DEL-06.04 Structural Steel Data Sheet Package

## Scope

This deliverable defines and substantiates structural steelwork items via a data sheet package, in accordance with Employer’s Requirements (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:251).

**Anticipated artifacts:**
- Gangway data sheets
- Grating data sheets

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:251; Datasheet.md: Attributes; Procedure.md: Step 1; Guidance.md: Examples)

## Requirements

### Functional Requirements

- Provide a data sheet template/structure that captures the key technical attributes needed for procurement, fabrication, and QA verification for gangways and grating (**TBD** exact fields) (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD).
- Ensure each data sheet can be traced to the corresponding drawing item/assembly and (where applicable) calculation case (ASSUMPTION; dependencies coordinated externally).

#### Suggested Field Sets (ASSUMPTION / TBD)

Field sets below are proposed to make the deliverable checkable and to align with DEL-06.05 record compilation; confirm against Employer’s Requirements clauses (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD).

**Gangway data sheet (example fields):**
- Item ID / drawing reference (**TBD** identification scheme)
- Geometry (length, width, slope, landing details) (**TBD**)
- Material and protective system reference (via DEL-06.02 clause reference) (DEL-06.02 Specification.md)
- Design basis reference (via DEL-06.03 calculation reference) (DEL-06.03 Specification.md)
- Connection/support assumptions (Dependencies: NOT_TRACKED)
- Required records / certificates (maps to DEL-06.05) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252)

**Grating data sheet (example fields):**
- Item ID / drawing reference (**TBD** identification scheme)
- Panel type and configuration (**TBD**)
- Material and protective system reference (via DEL-06.02 clause reference) (DEL-06.02 Specification.md)
- Slip resistance / performance criteria (**TBD**) (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD)
- Required records / certificates (maps to DEL-06.05) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252)

### Performance Requirements

- Capture the governing performance criteria required by the Employer’s Requirements (e.g., design loads, exposure/durability criteria, slip resistance where applicable) as explicit fields (**TBD** until ER clauses extracted) (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD).
- Ensure each data sheet identifies acceptance criteria (inspection/hold points) suitable for QA/QC records (ASSUMPTION; align to DEL-06.05 record types).

### Interface Requirements

- Coordinate item identification and configuration with the drawing set and BOMs; dependency edges are not tracked in-file (see `_DEPENDENCIES.md`) (Dependencies: NOT_TRACKED).
- Where Employer-responsible items exist, document only the interface connection requirements (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49).

### Quality Requirements

- Data sheets shall comply with project document control, revisioning, and approval expectations (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).
- Include fields for required supporting documents (e.g., material certificates, galvanizing/coating certificates) where relevant (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252).

## Standards

- Governing standards for gangways and grating are **TBD** until extracted from Employer’s Requirements (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD).

## Verification

- Consistency check: data sheet values and identifiers match drawings and specification clauses (Dependencies: NOT_TRACKED).
- Completeness check: required fields populated or marked **TBD** with rationale (ASSUMPTION).
- Units and nomenclature check (ensure consistent terminology across PKG-06 documents).

## Cross-Reference Matrix (Specification → Procedure → Evidence)

| Requirement area | Primary procedure step(s) | Evidence / output |
|------------------|---------------------------|------------------|
| Item list complete (Gangway data sheets, Grating data sheets) | Procedure.md: Step 1 | Item list / register (**TBD**; Datasheet.md: Attributes) |
| Template fields defined (geometry, material/protective system, linked documents, required records) | Procedure.md: Step 2 | Approved template(s) (**TBD**; Suggested Field Sets; Guidance.md: Examples) |
| Data populated from design documents (DEL-06.01, DEL-06.02, DEL-06.03) | Procedure.md: Step 3 | Completed data sheets with drawing/spec/calc references (Guidance.md: Principles, Considerations) |
| QA consistency review done (identifiers/values match; record fields align with DEL-06.05) | Procedure.md: Step 4 | Check record; alignment to DEL-06.05 record types (mill certificates, weld inspection records, galvanizing certificates) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252; Guidance.md: Considerations) |
| Document control applied | Procedure.md: Step 5 | Revision history / approvals (**TBD**; Datasheet.md: Attributes) |

## Documentation

**Deliverable artifacts:**
- Gangway data sheets
- Grating data sheets

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:251; Datasheet.md: Attributes; Procedure.md: Step 1)

**Documentation requirements:**
- Maintain revision history and approvals per document control requirements (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Datasheet.md: Attributes; Procedure.md: Step 5).
- Data sheet package files (native + PDF), check record, supporting certificates as applicable (**TBD**) (Procedure.md: Records).

## Cross-Document Notes

- Datasheet: metadata fields should align with project numbering and Procedure’s release workflow (Datasheet.md: Attributes; Procedure.md: Steps).
- Technical Specification (DEL-06.02): data sheet fields should match the requirement clauses (DEL-06.02 Specification.md).
- Installation/Test Records (DEL-06.05): required certificate/inspection record types should be listed on the relevant data sheets (DEL-06.05 Datasheet.md, once drafted).
