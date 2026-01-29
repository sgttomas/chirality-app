# Procedure: DEL-06.04 Structural Steel Data Sheet Package

## Purpose

This procedure defines the process for producing and managing the **Structural Steel Data Sheet Package** within **PKG-06 Structural Steelwork**.

The deliverable defines and substantiates structural steelwork items via data sheets in accordance with Employer’s Requirements (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:251).

**Deliverable type:** Data Sheet  
**Responsible party:** D&B Contractor

## Prerequisites

**Dependencies:**
- See `_DEPENDENCIES.md` — **NOT_TRACKED**: dependencies coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`).
- Confirm the latest drawings/specification/calculation inputs are available for populating fields (Dependencies: NOT_TRACKED).

**Reference materials:**
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (PKG-06 / DEL-06.04 definition) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:238-252).
- Employer's Requirements — relevant clauses **TBD** (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD).
- Document control / QA expectations (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).

**Personnel requirements:**
- Structural engineer/technologist and checker per project QA/QC expectations (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).

## Steps

1. **Identify items** — Compile the list of gangway and grating items requiring data sheets; create Item List/Register (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:251; Datasheet.md: Attributes; Specification.md: Scope, Cross-Reference Matrix).
2. **Define template fields** — Establish the required fields per item type (geometry, material/protective system, linked documents [DEL-06.01/DEL-06.02/DEL-06.03 references], required records [DEL-06.05]) (**TBD** until ER clauses extracted).
   - Use the suggested field sets in `Specification.md` as the starting point and mark deviations as TBD/assumption (Specification.md: Suggested Field Sets; Datasheet.md: Construction; Guidance.md: Examples).
3. **Populate from design** — Fill fields from drawings (DEL-06.01), specification (DEL-06.02), and calculations (DEL-06.03); ensure item IDs align with drawings and BOM; mark unknowns as **TBD** with source pointers (Specification.md: Cross-Reference Matrix; Datasheet.md: Construction; Guidance.md: Principles, Considerations).
4. **QA review** — Checker validates consistency across documents (item IDs, values, nomenclature) and that required record/certificate fields align with DEL-06.05 (mill certificates, weld inspection records, galvanizing certificates) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252; Specification.md: Cross-Reference Matrix; Guidance.md: Considerations).
5. **Issue preparation** — Apply numbering/revisioning and compile package (native + PDF, check record, supporting certificates as applicable) for CHECKING as required; ensure `Datasheet.md` attributes match package number and revision (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Datasheet.md: Attributes; Specification.md: Documentation).

## Verification

- Item list completeness: all gangway and grating items identified (Specification.md: Cross-Reference Matrix; Step 1).
- Template fields defined: geometry, material/protective system, linked documents (DEL-06.01/DEL-06.02/DEL-06.03), required records (DEL-06.05) (Specification.md: Suggested Field Sets, Cross-Reference Matrix; Datasheet.md: Construction; Step 2).
- Data populated: fields filled from DEL-06.01 (drawing references), DEL-06.02 (material/spec clauses), DEL-06.03 (calculation references where applicable); item IDs aligned with drawings and BOM (Specification.md: Cross-Reference Matrix; Datasheet.md: Attributes; Guidance.md: Principles; Step 3).
- Consistency check: identifiers and values match drawings (DEL-06.01), specification (DEL-06.02), calculations (DEL-06.03) (Dependencies: NOT_TRACKED; Specification.md: Verification; Guidance.md: Considerations; Step 4).
- Required records alignment: certificate/inspection record fields align with DEL-06.05 (mill certificates, weld inspection records, galvanizing certificates) (Specification.md: Cross-Reference Matrix; Guidance.md: Considerations; Step 4).
- Completeness check: required fields are populated or explicitly marked **TBD** (Specification.md: Verification; Step 4).
- Units and nomenclature check: consistent terminology across PKG-06 documents (Specification.md: Verification; Step 4).
- Cross-check: confirm `Specification.md` Cross-Reference Matrix evidence is available for the issue package (**TBD**; Specification.md: Cross-Reference Matrix).

## Records

**Documentation outputs:**
- Gangway data sheets
- Grating data sheets

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:251; Datasheet.md: Attributes; Specification.md: Scope, Documentation)

**Record management:**
- Data sheet package files (native + PDF), check record, and any supporting certificates referenced (as applicable) (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Specification.md: Documentation; Step 5).
- Filing convention: working files remain in `1_Working/`; review/issue copies can be packaged to `2_Checking/` / `3_Issued/` as adopted by the team (Source: README.md; Datasheet.md: References).
- Revision tracking: per project numbering system and `Datasheet.md` attributes (Datasheet.md: Attributes; Step 5).
- Retention requirements: **TBD**.

## Cross-Document Traceability

| Document | Section | Linked Content |
|----------|---------|----------------|
| Datasheet.md | Identification | Deliverable identity verified in Step 1 |
| Datasheet.md | Attributes | Package metadata (number, revision) verified in Step 5 |
| Datasheet.md | Construction | Suggested fields used in Steps 2, 3 |
| Specification.md | Scope | Anticipated artifacts checklist used in Step 1 |
| Specification.md | Suggested Field Sets | Field structure used in Step 2 |
| Specification.md | Cross-Reference Matrix | Verification traceability confirmed in Step 4 |
| Guidance.md | Principles | Intent guiding Steps 2, 3 (checklistable fields, consistent identifiers) |
| Guidance.md | Considerations | Trade-offs considered in Steps 2, 4 |
| Guidance.md | Examples | Template formats used in Step 2 |

**Cross-Deliverable Consistency (PKG-06):**
- DEL-06.01: Item IDs aligned with drawings (Step 3); drawing references included
- DEL-06.02: Material/coating fields reflect specification clauses (Step 3)
- DEL-06.03: Calculation references included where applicable (Step 3)
- DEL-06.05: Required records fields (mill certificates, galvanizing certificates) aligned in Step 4
