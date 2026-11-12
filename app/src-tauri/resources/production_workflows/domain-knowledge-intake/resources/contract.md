# domain-knowledge-intake: contract

## Inputs

- **Knowledge needs.** The list of needs and, for each, its intended use in the
  application: display, computation, classification, or a determination someone
  relies on. The use sets the rigor.
- **Scope.** Jurisdiction, domain, the edition or date of applicability, and exclusions.
- **Sources and access terms.**
  - Documents, standards (including paywalled ones and what access the project has),
    papers, datasets, and source code at a revision.
  - Expert contacts, with permitted use of their input. Private expert input stays
    out of public packs.
- **The domain reviewer and the accepting authority.**
- **Locations.** `PACK_ROOT` and the permitted writes.

## The pack

A pack lives at `PACK_ROOT/<pack-id>/<version>/`:

| Path | Content | Consumer |
|---|---|---|
| `pack.yaml` | A `DomainModel` fragment in ontology classes. Items are `Criterion`, `ClassificationScheme`, `Method` with assumptions, applicability and limitations, `Assumption`, `ParameterTable` with `row_basis`, `Definition` and `Caveat`. It also holds the `SourceReference` list and its `Conflict` and `Ruling` entries. | Specifications that reference it |
| `evidence/<source-id>.md` | For each extracted item: locator, verbatim text or table cells where precision matters, and the extraction note | Verifier, domain reviewer |
| `tests/` | Cases for rule tables and conversions, each with its source. Example: Tier 1 lookups giving land use, soil, depth and analyte → guideline value and unit. | Analysis binding, CI |
| `PACK_MANIFEST.csv` | `Path,SHA256,Role` for every file above | Acceptance, specifications' closure locks |

The pack's identity is `<pack-id>@<version>` plus the SHA-256 of `PACK_MANIFEST.csv`.
Specifications record it in `domain.knowledge_packs` (ontology `KnowledgePackRef`).

## Decision record

Write `PACK_ROOT/<pack-id>/decisions/<version>-<UTC>/DECISION.md` outside the pack
content:

```text
Pack:              <pack-id>@<version>; PACK_MANIFEST.csv SHA-256
Reviewer:          <person or appointed role; competence basis>
Response:          <actual words and source reference>
Outcome:           accepted | accepted for a limited scope | returned | stopped
Scope of use:      <uses for which reliance is accepted; uses excluded>
Items excluded:    <items not accepted, with reason>
Rulings:           <conflicts ruled, by whom>
Open items:        <TBD items and their consequence>
Predecessor:       <earlier version superseded, or "initial">
```

## Invariants

- No item without a locator. No numerical value without its unit and source edition.
  No invented value: missing knowledge stays TBD with its consequence.
- Expert judgment is recorded as the expert's, with date, scope and method. An agent
  never originates it.
- A conflict between sources stays visible until inquiry resolves it or the
  appropriate authority rules on it. A ruling does not make the losing claim false.
  It selects what the pack uses.
- An accepted pack is never edited. A changed item makes a new version, and the
  predecessor stays available.
- Acceptance covers the stated scope of use only. An application with another use
  needs its own examination.
