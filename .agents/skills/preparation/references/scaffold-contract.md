# Scaffold Contract

## Operation map

| Operation | Required accepted input | Result |
|---|---|---|
| Package hierarchy | package ID and name | package lifecycle directories |
| Package references | package identity and available references | files or `_REFERENCE_INDEX.md` |
| Deliverable fileset | deliverable and package fields plus decomposition reference | five control files |
| Aggregation prerequisites | execution root | `_Aggregation` root and neutral templates |
| Category hierarchy | category ID and name | category lifecycle directories |
| Knowledge-type fileset | knowledge-type and category fields plus decomposition reference | five control files |
| Domain tool roots | execution root | hypergraph and closure structural roots |

Package and category lifecycle hierarchies contain `0_References/`, `0_References/_Archive/`, `1_Working/`, `1_Working/_Archive/`, `2_Checking/`, `2_Checking/From/`, `2_Checking/To/`, `3_Issued/`, and `3_Issued/_Archive/`.

## Context files

A deliverable `_CONTEXT.md` records its ID and canonical name, package ID and canonical name, discipline, type, responsible party, exact accepted description, anticipated artifacts, decomposition path, and deliverable ID.

A knowledge-type `_CONTEXT.md` records its ID and canonical name, category ID and canonical name, discipline, type, responsible party, exact accepted description, anticipated artifacts, decomposition path, knowledge-type ID, and category ID.

Do not normalize or embellish accepted field values. Use `TBD` only when the accepted source itself is unresolved, and report that condition.

## Dependency file

`_DEPENDENCIES.md` is a durable container with:

- a human-owned coordination mode: `NOT_TRACKED`, `DECLARED`, or `FULL_GRAPH`;
- human-declared upstream and downstream entries, including reason, required maturity, and location when supplied;
- an extracted dependency-register section initialized to `NOT_RUN_YET`;
- run-history, lifecycle-summary, and consumer-handoff placeholders.

Do not infer dependency edges. For `NOT_TRACKED`, state that humans coordinate dependencies externally.

## Remaining control files

- `_STATUS.md`: initialize `Current State: OPEN` and one dated history entry
  naming the actual actor only when the file is newly created.
- `_REFERENCES.md`: list supplied reference names or IDs, locations, and relevance; otherwise state that references are not yet identified.
- `_SEMANTIC.md`: create a `PLACEHOLDER` lens with no engineering assertions. A later semantic workflow may replace it.
- `_MEMORY.md`: optional and outside the minimum fileset. Create it only when explicitly selected and authorized, with headings for decisions, domain context, open items, proposal history, and interfaces.

Aggregation templates, when requested, are structural only. The target-schema CSV begins with `RecordID,SourceID,SourcePath,SectionRef,EntityType,Key,Value,Notes,Confidence,Tags` and no data rows.
