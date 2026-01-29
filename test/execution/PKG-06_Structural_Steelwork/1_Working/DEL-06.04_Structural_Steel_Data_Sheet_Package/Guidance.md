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

## Conflict Table (for human ruling)

*No conflicts between sources identified at this time.*

| Conflict ID | Conflict | Source A (file + section) | Source B (file + section) | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|---------------------------|---------------------------|-------------------|--------------------|--------------|
| — | — | — | — | — | — | — |

## Pending Inputs (TBD Resolution)

| Item | Missing Input | Impact | Action Required |
|------|---------------|--------|-----------------|
| PI-06.04-001 | Employer's Requirements clauses for gangway/grating requirements | Data sheet field list and acceptance criteria remain TBD | Extract relevant clauses from Volume 2 Part 3 |
| PI-06.04-002 | Item identification/tag scheme | Cannot align data sheet IDs with drawings and BOM | Confirm tagging convention with project team |
| PI-06.04-003 | Performance criteria (slip resistance, design loads) | Governing criteria remain TBD | Extract performance clauses from ER |

## Cross-Document Traceability

| Document | Section | Linked Content |
|----------|---------|----------------|
| Datasheet.md | Identification | Deliverable identity consistent with Scope |
| Datasheet.md | Attributes | Package metadata (number, revision) — keep aligned with issue workflow |
| Datasheet.md | Construction | Suggested data sheet fields, linked deliverables |
| Specification.md | Suggested Field Sets | Field structure referenced in Considerations |
| Specification.md | Cross-Reference Matrix | Requirement-to-verification traceability |
| Procedure.md | Steps 1–5 | Workflow implementing the Principles and Considerations |
| Procedure.md | Verification | Criteria that validate Considerations are met |

**Cross-Deliverable Consistency (PKG-06):**
- DEL-06.01: Item IDs and configurations match drawing items
- DEL-06.02: Material/coating fields reflect specification clause requirements
- DEL-06.03: Design basis references included where applicable
- DEL-06.05: Required records fields (mill certificates, galvanizing certificates) align with installation/test record compilation
