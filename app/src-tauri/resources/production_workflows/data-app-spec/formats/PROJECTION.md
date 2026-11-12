# Projection: from the ontology to the JSON Schema

This document describes how
[`app-spec.schema.json`](app-spec.schema.json) is derived from
[`app_family.linkml.yaml`](app_family.linkml.yaml), what the projection keeps, what it
loses, and which rules therefore belong to the semantic validator.

## Principle

The ontology is the source; the JSON Schema is a generated projection that serves one
consumer: structural validation of specification files. It is never edited by hand.
The model is authored once in LinkML and other artifacts are generated from it, as the
LinkML documentation recommends. Regenerating and comparing detects drift. From the
package folder:

```sh
python3 -I tools/project_schema.py formats/app_family.linkml.yaml formats/app-spec.schema.json --check
python3 -I tools/project_schema.py formats/app_design.linkml.yaml formats/app-design.schema.json --check
python3 -I tools/project_schema.py formats/app_design.linkml.yaml formats/app-patterns.schema.json --root PatternCatalogue --check
```

The projection here is produced by `tools/project_schema.py`, not by
LinkML's own `gen-json-schema`. It implements exactly the rules below and refuses LinkML
constructs it does not support. A project may adopt LinkML's generators instead. Their
sample output declares draft-07, so confirm the emitted draft before relying on 2020-12
keywords.

## Projection rules (as implemented)

| LinkML construct | JSON Schema 2020-12 projection |
|---|---|
| `tree_root` class (`AppSpec`) | Root `$ref` |
| Concrete class | `$defs/<Class>`: `type: object`, `properties` from all induced slots (ancestors first, then mixins, then own), `required`, `additionalProperties: false`, `patternProperties: {"^x-": …}` (visible extensions) |
| Abstract class with a type-designator slot (`kind`) | `$defs/<Class>` as a discriminated union: `kind` must be one of the concrete descendants, and an `if kind = X then $ref X` branch per descendant (gives precise errors; equivalent to `oneOf` with `const`, the pattern the research recommends) |
| Abstract class without a designator (`DataNode`) | No definition; it can only be referenced by identifier |
| `designates_type` slot | `const: <ClassName>` in each concrete class: every object names its ontology class |
| Mixin (`Claimable`) | Its slots are copied into each class that uses it ("rolled down") |
| Slot with a class range whose class has an identifier, not inlined | String matching the identifier pattern, annotated `x-appspec-ref: <Class>` |
| Slot with a class range, inlined | `$ref` to the class definition |
| `multivalued` | `type: array` of the item schema |
| `any_of` ranges | `anyOf` of the alternatives (units: UCUM string or `CurrencyUnit`) |
| Enum | `$defs/<Enum>` with `enum` of the permissible values |
| Built-in types | string, integer, number, boolean; `date`, `datetime` and `uri` as strings with `format` |
| Custom types (`Identifier`, `Expression`, `IsoDuration`, `Sha256`, `ElementPath`, `UcumCode`) | Base type plus `pattern` where defined, annotated `x-appspec-type: <Type>` |
| `pattern`, `minimum_value`, `maximum_value` | `pattern`, `minimum`, `maximum` |
| Class annotation `level`; `is_a` | `x-appspec-level`, `x-appspec-is-a` annotations (JSON Schema ignores unknown keywords; the semantic validator reads them) |
| Class `description`, slot `description` | `description` |

## What the projection loses

These losses match those the LinkML documentation lists for its own JSON Schema
generator: inheritance is flattened; references become strings
without meaning; enumeration meanings and mappings (`exact_mappings`, `close_mappings`
to PROV, SOSA, DCAT, CSVW) are dropped; uniqueness cannot be expressed. In addition,
for this ontology:

- **Cross-element meaning.** Whether a referenced element exists and has the right
  class; whether an expression's `$names` are state variables; whether bindings match a
  component's interface.
- **Exclusivity rules.** Exactly one of value / expression / state / TBD in a parameter
  binding; exactly one of ref / items in a placement.
- **Behavioural semantics.** Recomputation, interaction ordering, scenario evaluation,
  rounding order (ONTOLOGY.md §6). No schema language expresses these; they are
  normative text and are tested by building and running.
- **Profiles.** Whether a specification is buildable (no open blocking gaps, no
  undecided fidelity decisions, no placeholders) is a property of the whole document.
- **Formats.** JSON Schema 2020-12 treats `format` as an annotation unless a validator
  enables format assertion. `tools/check_spec.py` enables it;
  a stricter projection would add patterns for dates.

## Semantic rules (second validation layer)

Implemented in `tools/check_spec.py`:

| Rule | Check |
|---|---|
| R-ID | Identifiers unique across the specification |
| R-REF | Every `x-appspec-ref` value resolves to an element of that class or a subclass |
| R-PATH | Every element path starts with an existing identifier |
| R-EXPR | Every `$name` in an Expression is a StateVariable |
| R-PB1 | ParameterBinding: exactly one of value, expression, from_state, tbd |
| R-PL1 | Placement: exactly one of ref, items; refs resolve |
| R-IF1 | Analysis, scenario and test bindings name declared component parameters and ports |
| R-COV | A state variable set by a control is read somewhere (warning) |
| R-KAT | Every analysis component has a known-answer test (warning) |
| R-RUL | A ruling marked `made` has `decided_by` and `evidence` |
| R-TBD1 | Elements with `standing: TBD` block a build |
| R-GAP, R-FD | Open gaps blocking build, and undecided or deferred fidelity decisions, block a build |
| R-FD2 | A fidelity selection other than `undecided` or `defer` names a ruling (error if not); it binds, and stops blocking a build, only once that ruling is `made` |

Not yet implemented: unit compatibility (dimensional analysis of expressions
over UCUM units), archetype obligations, consequence-tier obligations, expression
parsing against the adopted expression grammar, closure resolution (every asset and
component bundle present with matching hash).

## Evidence that both layers are needed

On first run, R-IF1 found five binding errors in example specifications that the JSON
Schema layer had passed. Conversely, JSON Schema caught seven
YAML authoring errors (unquoted commas in flow mappings) that the semantic layer could
not have seen. Each layer establishes a different, limited claim; neither establishes
that a specification is correct or adequate.

## Proposed changes to the projection for 0.2

- Use `unevaluatedProperties: false` where objects are composed with `allOf`, and a
  `$dynamicRef`-based strict "buildable" profile over the core schema.
- Project a uniform TBD marker as `anyOf [value, TbdMarker]` for required value slots.
- Generate a JSON-LD context from the same source so specifications can be read as
  linked data with the PROV, SOSA, QUDT and DCAT alignments the projection drops.
- Pin the projector (LinkML version and flags, or this tool's hash) in the
  specification toolchain lock, and record the ontology hash in the schema
  (`$comment: ontology_sha256=…`, already done).
