# Builder input contract

This contract states what a builder may read, what it must produce, what it must not
do, and when it must refuse. It is the interface the `data-app-spec` workflow hands
downstream, and `data-app-build` applies it.

## Two kinds of builder

| | Agent builder | Builder program |
|---|---|---|
| What builds | An agent under `data-app-build` | A versioned program |
| What decides conformance | A conformance suite generated from the specification before the build, by another contributor, and frozen by hash | The same suite, plus bit-reproducibility |
| Identity of a build | The build tree hash, with the suite results | The artifact hash, reproducible from the closure |
| Rebuild | May produce different code; must pass the same frozen suite; acceptance does not transfer | Produces the same bytes |

Everything else in this contract applies to both: what may be read, the preconditions,
what must not be done, what must be implemented, and failing closed. An agent builder
does not reliably follow a specification by itself, and regenerating code gives different
code. The suite, the element map and independent examination are this contract's answer,
not trust in the builder.

## The single contract, precisely

"The builder reads nothing but the specification" means the builder reads **nothing
but the specification closure**:

1. the canonical specification `appspec.json`, identified by SHA-256;
2. its closure lock `appspec.lock`;
3. the closure members the lock names, each verified by hash:
   - assets (text, documents, images);
   - bundled datasets and data product manifests;
   - component bundles with their interface entries;
   - domain knowledge packs;
   - the template expansion record, if templates are used;
4. the builder's own declared, versioned **capability manifest** and **defaults**;
5. for an agent builder, the frozen **conformance suite**. It is meant to add no
   meaning. Whether it does is examined: a separate agent checks it against the
   specification before it is frozen. The builder may not edit it.

The capability manifest lists the view kinds, transforms, layout shells, targets and
expression functions the builder implements. The defaults are presentation choices the
specification leaves open (fonts, spacing, a palette when none is named); they are
recorded in every build manifest.

The strict alternative, with everything inline in one document, cannot hold. Bound
analyses such as a simulation engine or a kriging library would have to be re-described
as code inside the specification, which turns the specification into a programming
language.

## Preconditions (the builder refuses otherwise)

| # | Condition | On failure |
|---|---|---|
| P1 | `appspec_version` is within the builder's supported range | Refuse; name the range; migration happens before build, never inside it |
| P2 | Structural and semantic validation pass in the **buildable** profile: no errors, no open build-blocking gaps, no fidelity decision undecided, deferred or selected without a made ruling, no `standing: TBD` elements in the covered scope | Refuse with the validator report |
| P3 | Every closure member is present and its hash matches the lock | Refuse; name the member |
| P4 | Every kind, transform, expression function and target the specification uses is in the capability manifest | Refuse; list unsupported elements by path. Never skip or approximate. |
| P5 | No `x-` extension appears on an element the build covers | Refuse; extensions are not buildable semantics |
| P6 | Every component bundle matches its interface entry and provides an entry point for the selected target runtime | Refuse; name the component |

A build presented for acceptance starts from an accepted closure. A draft build, made
to examine a specification, may start from a frozen candidate and is labelled draft.
Deployment requires the owner's acceptance of the built application under
`data-app-build`, with the tier's conditions (`data-app-spec`'s `gates.md`). The deployment
step checks this, not the builder.

## What the builder must not do

- Read anything outside the closure: no fetching at build time; no reading of a
  reference app's source, documentation or deployment.
- Make semantic choices the specification does not make: labels, units, rounding,
  ordering, palettes for meaningful encodings, thresholds, defaults for missing values.
  Presentation defaults come only from its declared defaults or the build profile's
  theme, and are recorded.
- Substitute behaviour for an unsupported feature, catch failures broadly, or fill a
  missing value. Failures are explicit, as the specification declares them.
- Hand-edit or post-process its own outputs.
- Edit the conformance suite, or change an expected value. A failing test is fixed in
  the build, or reported as a specification finding.
- Settle an ambiguity. The builder stops that element and reports the element path, the
  question and the options; data-app-spec `revise` answers it.
- Claim, imply or display acceptance. It may display the acceptance record's actual
  contents when supplied, naming what was accepted (the specification or this build),
  for which purpose, and its hash.
- Perform external effects. Deployment and data publication are separate steps, so a
  rebuild never repeats them.

## What the builder must implement

- The semantics in `data-app-spec`'s `formats/ONTOLOGY.md` §6:
  - data-flow recomputation and lazy evaluation;
  - state and domain rules;
  - interaction ordering and snapshots;
  - scenario evaluation;
  - metric rounding and missing rules;
  - fidelity decisions as specified behaviour.
- The expression semantics the format defines.
- Empty, error and precondition-failure states with their declared messages.
- The provenance policy: data citations and vintage; app, specification and component
  identities; per-result provenance where requested.
- Materialisations the build profile requests, with an equivalence check against the
  runtime path for each.

## Outputs

| Output | Content |
|---|---|
| Build artifact | The application for the selected target (e.g. a static web bundle, a Shiny app directory, a shinylive export) |
| Build manifest | Specification SHA-256, lock SHA-256, builder version (for an agent builder: the host's agent identity and the workflow version) and capability manifest hash, environment image digest, defaults applied, materialisations computed with equivalence results, target, suite manifest hash |
| Element map | Every specification element in the coverage, with the code that realises it and the tests that cover it (`data-app-build`) |
| Generated test suite | Known-answer tests, pipeline tests, property tests, UI contract checks, data contract checks, equivalence and determinism checks |
| Provenance package | PROV-O / RO-Crate record of the build and its evidence |
| Build report | What was built for which coverage; checks run and their results |

## Determinism

- **Bit-reproducible (builder program).** Given the same closure, builder version and pinned build
  environment, two builds produce bit-identical artifacts. This uses the
  reproducible-builds.org definition: verify by rebuilding and comparing hashes. The
  build date and other volatile values are excluded from the artifact or fixed by a
  declared epoch.
- **Conformance-reproducible (agent builder).** Two builds from the same closure pass the
  same frozen suite. The accepted build is identified by its tree hash, and acceptance
  does not transfer to another build.
- **Numerical results.** These are tolerance-reproducible across platforms, not bitwise.
- **Live sources.** Determinism covers the build. A specification with live external
  sources has runtime outputs that vary with the data. The app must show data freshness
  where the specification declares it.

Determinism is a reproducibility property. It does not make the output correct
(thesis Chapter 6 §6.7.3); correctness rests on the tests and their oracles.

## Failure behaviour

The builder fails closed:
- Every diagnostic names the specification element path, the rule and the evidence.
- No partial artifact is produced. The one exception: the specification's `coverage`
  declares a partial scope and the build profile requests a partial build. The artifact
  is then labelled partial in its manifest and in the app.

## Questions an adopting project settles

- Its targets and the component runtimes they need.
- Whether the build profile lives inside the specification or beside it.
- The capability manifest's scope: which view kinds and transforms its builder supports.
- Whether to add a builder program beside the agent builder.
