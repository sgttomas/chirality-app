# data-app-spec: briefs for dispatched stages

A dispatched agent knows only its brief (AGENTS.md: "An assignment travels
whole"). Carry the host, safety and data rules in it.

## Fields every stage brief states

| Field | Meaning |
|---|---|
| `Purpose` | The stage's contribution to the specification |
| `Role` | TASK unless the stage needs coordination |
| `Basis` | Identities of the ontology and schema releases, the candidate or inventory being worked on, and the sources |
| `Scope` | Which app, module, analysis or knowledge items |
| `Evidence rules` | Cite a source for every external claim; label findings observed / documented / inferred / TBD; do not invent values |
| `Permitted observation and execution` | e.g. initial HTML only; no live interaction; no execution of downloaded code; clone into a fresh temporary directory and delete it afterwards |
| `Write boundary` | Exact files or directory |
| `Return` | Location, a summary of decision-relevant findings, TBD list, checks run |

## Stage-specific additions

- **Reference inventory:** the ontology headings to fill, and the "what a spec must
  say beyond the UI" list.
- **Design preparation (new mode):**
  - the intent and its source;
  - the catalogue version;
  - the needs to prepare options for;
  - that proposed answers are labelled as proposals;
  - that no need, decision or obligation may be invented.
- **Independent examination:**
  - the frozen candidate id and manifest;
  - the original directions;
  - the review categories;
  - that the examiner must not edit the candidate;
  - that its return lists coverage and limits.
- **Validation run:** the exact tool versions and the frozen bytes to validate.

State the time box in every inventory brief, and what to return when it runs out.
