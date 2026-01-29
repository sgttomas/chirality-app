# Guidance: DEL-06.05 Structural Steel Installation & Test Records

## Purpose

- Support development of the records package that provides evidence of completion, inspection, and testing for PKG-06 structural steelwork (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252).
- Provide interpretation so records remain traceable to drawings/specification/data sheets and support Employer/Engineer review and handover (ASSUMPTION; confirm in ER clauses).

This deliverable is a **Record** produced by **D&B Contractor (QA/QC)** (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252).

## Principles

- Traceability: each record should map to the relevant steel item/assembly and the governing requirement clause (ASSUMPTION; traceability requirements TBD).
- Completeness: ensure all anticipated record categories are captured (mill certs, weld inspection, galvanizing certificates) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252).
- Authority: use Employer’s Requirements and document control expectations as the basis for record format, approvals, and retention; clauses **TBD** until extracted (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).

## Considerations

- Align “required records” lists with DEL-06.02 (Technical Specification) clauses and DEL-06.04 (Data Sheet Package) fields so records are not missed (Dependencies: NOT_TRACKED).
- Ensure certificates/inspection reports include identifiers sufficient for traceability (heat numbers, coating batch, inspection date, inspector ID) (**TBD** exact fields).
- Package scope focus remains Contractor-only; Employer-responsible items excluded except interfaces (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49).
- Use a single “record index” as the backbone; avoid relying on file naming alone for traceability (ASSUMPTION; see Specification.md: Record Index Structure).

## Trade-offs

- Centralized record package vs distributed records: centralized packages aid review but require strict indexing; distributed records reduce compilation effort but risk gaps (TBD).
- Scanned vendor certs vs structured record forms: scans are common but can hinder traceability/search; choose approach based on ER/document control requirements (**TBD**).

## Examples

- Create a records index (spreadsheet/table) listing each item ID and required record types with status (ASSUMPTION; format TBD).
- For galvanizing/coating, attach both certificates and inspection hold-point sign-offs where required (**TBD** until ER/spec clauses extracted).

## Conflict Table (for human ruling)

*No conflicts between sources identified at this time.*

| Conflict ID | Conflict | Source A (file + section) | Source B (file + section) | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|---------------------------|---------------------------|-------------------|--------------------|--------------|
| — | — | — | — | — | — | — |

## Pending Inputs (TBD Resolution)

| Item | Missing Input | Impact | Action Required |
|------|---------------|--------|-----------------|
| PI-06.05-001 | Employer's Requirements clauses for QA record requirements | Record templates and acceptance criteria remain TBD | Extract relevant clauses from Volume 2 Part 1 |
| PI-06.05-002 | Document control retention requirements | Archival and retention standards remain TBD | Confirm retention requirements with ER |
| PI-06.05-003 | Inspection/testing standards for structural steel | Specific inspection procedures remain TBD | Extract clauses from Volume 2 Part 3 |

## Cross-Document Traceability

| Document | Section | Linked Content |
|----------|---------|----------------|
| Datasheet.md | Identification | Deliverable identity consistent with Scope |
| Datasheet.md | Attributes | Package metadata (number, categories, traceability basis) — keep aligned with issue workflow |
| Datasheet.md | Construction | Suggested package contents, index structure |
| Specification.md | Record Index Structure | Index field requirements referenced in Considerations |
| Specification.md | Cross-Reference Matrix | Requirement-to-verification traceability |
| Procedure.md | Steps 1–6 | Workflow implementing the Principles and Considerations |
| Procedure.md | Verification | Criteria that validate Considerations are met |

**Cross-Deliverable Consistency (PKG-06):**
- DEL-06.01: Records trace to drawing item IDs and critical weld/coating locations
- DEL-06.02: Record requirements match specification inspection/acceptance clauses
- DEL-06.03: Critical design assumptions map to inspection/record requirements
- DEL-06.04: Data sheet "Required Records" fields drive record completeness
