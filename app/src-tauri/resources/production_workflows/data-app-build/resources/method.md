# data-app-build: method

## 1. Admit the closure

Verify every lock entry's hash and the specification's own hash against the accepted
candidate. Run the structural and semantic validators in the buildable profile, and
check the builder input contract's preconditions P1 to P6:
- format version;
- no blocking gaps, undecided or unruled fidelity decisions, or placeholders in the
  coverage;
- closure members present;
- every kind, transform and expression function in the capability manifest;
- no extensions in the coverage;
- every component bundle with an entry point for the target.

Copy every closure member into `BUILD_ROOT/closure/`, at the lock's relative paths, and
verify each copy against the lock. Install component runtimes there from the locked
artifacts. The suite author and builder then work from this isolated tree, not from the
specification run's folder, where inventories and reference captures are within reach.

If any precondition fails, write the refusal in `admission.txt`, naming each element,
rule and reason, and stop. Do not build around a failure. A refusal is a result. It
usually returns to data-app-spec as a revision or to analysis-binding as missing components.

## 2. Generate and freeze the conformance suite

The suite author derives tests from the specification only:

| Test kind | From | Checks |
|---|---|---|
| Known-answer tests | `verification.known_answer_tests` | The bundled component, through its entry point, reproduces the expected values within tolerance |
| Property tests | `verification.property_tests` | The stated properties hold on generated inputs within the declared domain |
| Pipeline tests | Data sources, transforms, analyses, metrics | Each node's output on fixture inputs matches values computed from the specification's own rules |
| Data contract tests | Source schemas and rules | Valid fixtures pass; each rule's violating fixture yields its declared message and severity |
| UI contract tests | Controls, state, interactions, views, layout | Every control exists with its label and domain and changes what it should; every view appears where the layout puts it; empty, error and precondition messages appear under their conditions; verbatim text is verbatim |
| Disclosure tests | Purpose, provenance policy, caveats | Non-uses, caveats, data vintage and acceptance status appear as declared |
| Export tests | Exports | Sheets, columns and provenance fields as declared |
| Materialisation tests | Build profile | Precomputed results equal runtime results within tolerance |

Fixtures come from the closure, such as example datasets and test inputs, or are
generated deterministically from the schemas with a recorded seed.

Further rules:
- **Viewport.** Run UI tests at every viewport size the specification states, and at
  least at the reference's in `derive` mode. Include visibility checks: content the
  specification declares, such as a result table's rows or a legend's text, must be
  visible without scrolling at those sizes. A suite run only at a wider size misses
  clipping.
- **Order.** Where row order or ties affect a computation, include a test that feeds the
  same rows in shuffled order.
- **Mutation evidence.** Record the mutation runs that show discriminating power in
  `suite/`: what was mutated, and which tests failed.
- **Specification findings.** Before freezing, the examiner classifies each of the suite
  author's findings:
  - settled by the specification;
  - a material ambiguity;
  - immaterial, where a tolerant test is acceptable and recorded.

  A material ambiguity goes back to `data-app-spec` `revise`, and the suite is frozen only
  against the newly accepted candidate.

Before freezing, a separate examiner checks the suite against the specification:
- every expected value follows from the specification or the closure's fixtures;
- every element in the coverage has a test;
- the suite can tell a defective build from a correct one, e.g. a mutated threshold,
  label or rounding rule fails some test.

Then freeze the suite with `SUITE_MANIFEST.csv`. The builder reads the suite, but the
suite does not come from the builder. A suite defect found later follows the
contract's route: a new suite version, agreed by the examiner, with every result
re-run.

Where a test cannot be derived because the specification is silent, record a
specification finding rather than inventing the expected behaviour.

## 3. Build

The builder works from the closure and the frozen suite, under the builder input
contract:
- realise each element in the coverage and record it in `ELEMENT_MAP.csv` as it is
  written;
- call components through their bundles' entry points; never re-implement a bound
  component;
- take presentation defaults only from the build profile's theme or the declared
  defaults, and list each in the build manifest;
- treat every ambiguity as a specification finding: stop that element and report the
  element path, the question and the options seen; do not guess;
- make failures explicit, as the specification declares them; no broad exception
  handling and no silent fallbacks;
- write no code whose only purpose is to satisfy a test. A test that seems wrong is
  reported as a suspected suite defect, with its name and the reason, and goes by the
  contract's route.

## 4. Run and repair

Run the whole suite on the build tree. Repair the build until it passes. A suite
failure that the build cannot fix without contradicting the specification is a
specification finding. Record the tree hash with the results.

The integration owner then:
1. verifies the suite manifest;
2. recomputes the tree hash by the contract's method;
3. re-runs the whole suite on that exact tree, independently of the builder's report;
4. writes `conformance.txt` from its own run.

Before any run, check that no earlier test or app process is still alive.

## 5. Examine

Give a separate examiner:
- the closure;
- the frozen suite and its results;
- the element map;
- the build tree.

Do not give the builder's summary alone. The examiner checks:
- that every element in the coverage is realised where the map says;
- code that realises no element (unspecified behaviour);
- presentation defaults that change meaning;
- that tests reach the implementation the app uses, not a parallel copy (thesis
  Chapter 8 §8.5.2);
- that components are called, not re-implemented;
- that acceptance is displayed only as recorded.

The examiner also checks whether the suite can distinguish a correct build from a
defective one. For example, does a mutated threshold or label fail some test? The
examiner mutates copies of the real build, not a stand-in.

The examiner also runs the app and screenshots each tab at the specified viewport sizes.
In `derive` mode, it compares them with the reference captures, and records each
difference as ruled or unruled. A defect found outside the suite's reach is repaired in
the build. Where a test could have caught it, the defect is proposed for a later suite
version.

Repair within authority, backcheck, and present remaining findings without ruling
them.

## 6. Package and present

Write the build manifest. At T3, also write the full provenance package the gates
require. Present to the owner:
- the conformance results;
- the examination account and remaining findings;
- the specification findings raised;
- the tier's requirements for acceptance, such as professional authentication at T3.

Record the response in `checkpoint/ACCEPTANCE.md`.

## 7. Hand back

Return:
- the build id, tree hash and manifest path;
- the acceptance outcome;
- open findings;
- the proposed next step.

Deploy only on the owner's explicit direction, as a separate act. A rebuild repeats
stages 1 to 6 and does not repeat any external effect.

## Interruption and recovery

Keep the admission record, the frozen suite, the build tree with its element map, the
latest conformance results and open findings, at their actual locations. On return,
re-verify the closure hashes and the suite manifest before relying on anything. A
changed closure or suite invalidates conformance results and acceptance. An interrupted
test or build command is not proof that it stopped; check for running processes before
starting another (thesis Chapter 8 §8.5.1).
