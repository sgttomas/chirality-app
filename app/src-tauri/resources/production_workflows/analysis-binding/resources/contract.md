# analysis-binding: contract

## Inputs

- The application's questions, data contracts and consequence tier.
- The accepted domain knowledge pack(s): methods, assumptions, parameter tables and
  criteria.
- The component registry, with existing entries and their known-answer tests.
- Candidate implementations: packages, repositories at revisions, and licences.
- In derive mode: the reference application's analysis code at a pinned revision.
- Permitted execution: whether reference values may be computed by running a candidate
  library or an independent implementation, and in what environment.
- Locations: `BINDING_ROOT` and the registry location, plus permitted writes.

## Component entry

A component entry is an ontology `AnalysisComponent`:
- id and semantic version;
- `implements`: a Method from the pack;
- `implementation`: language, package and version, entry point, source repository and
  revision, licence, and bundle SHA-256 once built;
- `inputs` and `outputs`: typed ports with schemas, units and CRS;
- `parameters`: type, domain, default, unit and description;
- `determinism`;
- `tolerance`, with its rationale;
- `preconditions`, with failure semantics;
- `known_answer_tests`;
- `known_limitations`.

The entry is the only thing the builder and the specification validator read about the
component.

A component whose implementation does not exist yet has two markers:
- `bundle_tbd`, pointing to a gap;
- a **component specification** in `BINDING_ROOT/components/<id>/SPEC.md`, holding the
  method, interface, behaviour cases, known-answer tests and acceptance verification.

That specification is the input to a decomposition deliverable, and the implementing
assignment carries it as its basis.

## Binding

A binding is an ontology `Analysis`:
- `component` and `method`;
- `inputs`: port to data node and field map;
- `parameters`: exactly one of value, expression, state reference or TBD for each, with
  `basis` and `standing`;
- `outputs`: port to result;
- `preconditions`, each with a message element;
- `recompute`;
- `result_semantics`: statements of meaning that the interface cannot carry (frozen
  baseline limits, eigenvalue versus realised ratio, clamping, NA versus zero).

## Records

| Path under `BINDING_ROOT` | Content | Consumer |
|---|---|---|
| `bindings/<analysis-id>.yaml` | The binding and the component entry it uses | data-app-spec |
| `assessment/<component-id>.md` | Candidate implementations and their assessment, chosen version, version-behaviour differences, licence | Examiner, later revisions |
| `kat/<component-id>/` | Test definitions, input fixtures with hashes, expected values with sources, oracle computations | Builder test generation, examiner |
| `review/<id>/` | Examiner brief, return, backcheck | data-app-spec checkpoint B |
| `components/<id>/SPEC.md` | Specification of a new component | Decomposition |

## Invariants

- A parameter value has grounds:
  - observed in reference code at a revision;
  - documented by a source;
  - derived by a stated calculation;
  - or ruled.
  An unknown value stays TBD.
- A known-answer test's expected values come from an oracle independent of the
  implementation under test. A derived expected value is marked as such until it is
  confirmed.
- An expected value changes only with a recorded substantive reason and the
  examiner's agreement. A failing test is never edited to pass.
- Tests run against the implementation the build links, not a parallel
  re-implementation (thesis Chapter 8 §8.5.2).
- Version pins are explicit when library versions differ in behaviour, for example
  qcc 2.7 and 3.0.
