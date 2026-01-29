# Guidance: DEL-06.04 Structural Steel Data Sheet Package

## Purpose

- Support development of the data sheet package that defines and substantiates structural steelwork items for PKG-06, focusing on gangways and grating as anticipated artifacts (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:251).
- Provide interpretation so the data sheet fields enable traceability to specification clauses, drawing items, and QA record types (DEL-06.01 through DEL-06.05) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:248-252).

This deliverable is a **Data Sheet** produced by the **D&B Contractor** within the Contractor’s scope (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:251; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49).

## Principles

- Data sheets should be “checklistable”: each field should be objectively verifiable via drawings, calculations, or certificates/inspection records (ASSUMPTION).
- Avoid false precision: if a criterion is not yet confirmed from Employer’s Requirements, mark the field **TBD** and cite the missing source (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD).
- Use consistent identifiers so gangway and grating data sheets align with drawings and QA record packages (Dependencies: NOT_TRACKED; coordinated externally).

## Considerations

- Gangways and grating typically need: geometry, support/connection details, material/protective system, design basis references, and inspection/acceptance requirements (**TBD** exact fields) (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD).
- Ensure data sheet values do not contradict calculation assumptions (DEL-06.03) or specification clauses (DEL-06.02) (Dependencies: NOT_TRACKED).
- Where QA/QC records are anticipated (mill certs, galvanizing certificates), include an explicit “Required Records” field to support DEL-06.05 compilation (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252).
- Keep references “by identifier” rather than prose: use drawing number, spec clause reference, and calc reference fields so traceability survives document updates (ASSUMPTION).

## Trade-offs

- Detailed vs minimal data sheets: more fields improve QA/procurement clarity but require more inputs early (TBD).
- Generic templates vs item-specific fields: standard templates reduce effort but may omit critical gangway/grating attributes; balance to be refined as ER clauses are extracted (TBD).

## Examples

- Create separate templates for gangway and grating data sheets to match anticipated artifacts (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:251).
- Include a “Linked Documents” block: drawing reference(s), calculation reference(s), and specification section reference(s) (ASSUMPTION; format TBD).

## Local Conflict Table (if unresolved)

| Topic | Issue | Impact | Needed to resolve | Owner |
|-------|-------|--------|-------------------|-------|
| Required fields/criteria | ER clauses for gangway/grating requirements not yet extracted | Data sheets cannot be completed beyond placeholders | Identify relevant ER clauses and confirm field list | Human |

## Cross-Document Notes

- Technical Specification (DEL-06.02): the data sheet fields should mirror the clause structure and acceptance criteria (DEL-06.02 Specification.md).
- Design Calculations (DEL-06.03): reference any governing assumptions or loads, where applicable (DEL-06.03 Datasheet.md).
- Installation/Test Records (DEL-06.05): use “Required Records” fields to ensure all certificates/inspection logs can be compiled (DEL-06.05 Specification.md, once drafted).
- Specification → Procedure traceability: use the `Specification.md` Cross-Reference Matrix to keep evidence expectations aligned.
