---
name: data-app-spec
description: Develop a declarative specification for an interactive data application with the human, from new intent through a design record or from an existing app; bind its domain knowledge and analyses, validate and examine it, obtain acceptance of the identified specification closure, and hand it to an agent build or to software-decomp as its accepted basis.
metadata:
  kind: instruction
  surface: workflow
---
# Specify an interactive data application

Use this method when the intended result is a specification from which an interactive
data application can be built: an explorer, monitoring map, quality-control chart,
calculator, simulator or decision-support tool of the family described in the
ontology's archetypes. The specification is written against an identified release of
the application-family ontology and its JSON Schema projection. When accepted, it is the
single contract the downstream work reads: a builder consumes the specification
closure (the specification plus the content-addressed assets, data products and
component bundles it pins) and nothing else.

The normal result is an owner-accepted, content-identified specification closure and a
handoff. The handoff goes either to `data-app-build`, when every component and capability the
specification needs exists, or to `software-decomp` group 1, which records it as its
accepted basis when new components, data products or builder capabilities are needed. A draft, a
review-pending candidate, a partial specification with stated coverage, a returned
candidate and a decision not to proceed are also reportable outcomes; none may be
described as an accepted specification. The method ends before decomposition,
implementation, build or release.

## Applicability and modes

- `new`: a specification formed from intent, conversation and supplied sources, through
  a design record (`formats/app_design.linkml.yaml`). The design record holds:
  - the needs, organised by the thesis's four perspectives;
  - options drawn from the pattern catalogue (`formats/patterns.yaml`);
  - choices bound by the human's rulings;
  - a trace from every need to the specification elements that answer it.

  The design record is the basis for validation: does the specified app answer the
  needs? The specification is the basis for verification: does the build conform? The
  builder reads only the specification closure.
- `derive`: a specification of an existing application, formed by inventorying it
  and deciding, for each observed behaviour, whether to reproduce, correct, omit or
  defer it. It follows the evidence discipline of `reverse-engineer-software`: the
  reference supplies evidence and exemplars, not requirements. A derived
  specification whose reference cannot be adequately observed may be re-scoped by
  ruling as a successor.
- `revise`: an amendment of an accepted specification. Preserve the predecessor,
  identify changed elements and re-examine affected elements only. Where a design record
  exists, revise it first and let its trace show which specification elements change.

Do not use this method for software that is not a data application of this family.
Chat or LLM features, CRUD and forms, multi-user write-back, games, real-time control
and GIS editing are out of scope. Where an app contains them, record the part as out
of scope rather than approximate it. For a general software product, use
`software-prd`.

## Roles

HELPS_HUMANS normally leads the design with the human, directly or through
HELP_HUMAN, and owns the coherence of the assembled specification. Keep one
integration owner. WORKING_ITEMS organises sustained production when several bounded
contributions are needed (inventories, domain extraction, analysis binding,
examination) and integrates their returns; design decisions stay with HELPS_HUMANS and
the human. TASK carries bounded stages under its own brief and does not delegate.
HELP_HUMAN holds purpose and continuity and may run the method directly for a small app.

The human decides purpose, intended use, consequence tier, scope, consequential design
choices, fidelity rulings and acceptance. The human may delegate presentation and
routine design choices by a ruling; a delegation cannot cover a consequential choice. Domain experts and, where professional obligations apply, accountable
professionals examine and accept what their competence covers. Agents prepare,
extract, bind, check and repair: reckoning that supports, but does not perform,
those judgments.

## Sequence and checkpoints

```text
1. Intake and framing.
   Checkpoint A: purpose, intended use, consequence tier, mode, scope, source basis.
2. Design (new and revise modes): needs, options, authoring questions, sketch.
   Design checkpoint: the human rules the consequential choices and any delegation.
   Reference inventory instead, in derive mode.
3. Domain knowledge (workflow domain-knowledge-intake).
4. Analysis binding (workflow analysis-binding).
5. Author the specification: compile the candidate from choices recorded as ruled
   (a draft from proposed choices, labelled as one, may inform the design checkpoint).
6. Validate: structure, semantics, the design trace, coverage, buildability.
7. Examine independently; repair and backcheck.
8. Lock the closure and freeze the candidate.
   Checkpoint B: acceptance of the identified closure for its stated use.
9. Hand off to data-app-build or software-decomp without starting either.
```

Stages 2 to 5 overlap and iterate. Domain knowledge and binding can answer design
gaps; a changed answer returns the affected choice to the design checkpoint. Agents prepare a checked package before each
checkpoint; work between checkpoints adds no approvals. Return to the human between
checkpoints only for a choice that changes an agreed outcome, boundary, consequence
tier or reserved decision. Existing explicit direction may satisfy checkpoint A;
nothing substitutes for checkpoint B on the actual frozen candidate. Tier-dependent
reviews before checkpoint B are set out in [gates](resources/gates.md).

## Resources

Load [the contract](resources/contract.md) for inputs, locations, records and the
handoff to `software-decomp`. Use [the method](resources/method.md) for the current
stage, [gates](resources/gates.md) to select proportionate examination, and
[checks](resources/checks.md) before each checkpoint. A dispatched stage receives a
brief built from [the brief guide](resources/brief.md).

The package also holds the format, the design knowledge and the tools the method uses:
- **Formats** (`formats/`):
  - the application-family ontology ([app_family.linkml.yaml](formats/app_family.linkml.yaml),
    explained in [ONTOLOGY.md](formats/ONTOLOGY.md)) and its generated schema
    `app-spec.schema.json`;
  - the design ontology ([app_design.linkml.yaml](formats/app_design.linkml.yaml),
    explained in [DESIGN_ONTOLOGY.md](formats/DESIGN_ONTOLOGY.md)) and its schemas
    `app-design.schema.json` and `app-patterns.schema.json`;
  - [PROJECTION.md](formats/PROJECTION.md), the projection rules;
  - the pattern catalogue [patterns.yaml](formats/patterns.yaml).
- **Tools** (`tools/`), run from the package folder:
  - `check_spec.py`, the specification validator:
    `python3 -I tools/check_spec.py formats/app-spec.schema.json SPEC`;
  - `check_design.py`, the design checker:
    `python3 -I tools/check_design.py --schemas formats --catalogue formats/patterns.yaml DESIGN --spec SPEC`,
    with its mutation tests `test_check_design.py`;
  - `freeze_candidate.py`, which freezes a candidate (method §8);
  - `project_schema.py`, which regenerates the schemas from the ontologies
    (PROJECTION.md).

  They need Python 3 with PyYAML; the checkers and the freeze helper also need jsonschema.
- **Worked example** (`examples/`): a design record and the specification compiled from
  it, for an illustrative groundwater monitoring review app.

A project that uses the method binds the releases it uses by content hash; see the
contract.
