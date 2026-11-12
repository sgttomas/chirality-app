# analysis-binding: known-answer tests

A known-answer test checks a component against an expected result that does not
come from the component itself. It is the main evidence of numerical verification.
It is not evidence of applicability or adequacy.

## Oracle layers

Use the strongest oracle available for each component; combine layers where one
is weak.

| Layer | Oracle | Examples |
|---|---|---|
| 1 | Certified reference data | NIST Statistical Reference Datasets for statistical primitives (certified values to 16 significant digits for linear regression) |
| 2 | Standard tables and worked examples | NIST/SEMATECH e-Handbook EWMA and CUSUM examples; qcc vignette viscosity limits; gstat meuse variogram fits |
| 3 | Published domain results | A package's documented examples; a paper's table of results, where reproducible |
| 4 | Properties and metamorphic relations | Ordinary kriging with zero nugget reproduces the data at sampled points. Scaling observations by c scales centre and σ̂ by c, and flags do not change. A scenario with zero intervention equals the status quo. |
| 5 | Independent implementation | A separately written computation of the same formulas (for example, a standard-library re-implementation), marked "derived" until confirmed against the pinned library |

In `derive` mode, the outputs the reference application displays are an oracle
independent of the component. Their tolerance is the displayed precision, and the display rules (rounding,
"<0.0001", signed zero) are tested as a separate formatting function. If they cannot be
reproduced, test the method variants and the dependency versions current when the
reference was built before recording a conflict. A library's later release can change
results that an older reference depends on.

## Each test records

- **Subject:** the component, or for a pipeline test, the analysis plus the state
  settings.
- **Oracle:** its kind, source and locator.
- **Inputs:** inline values or a fixture file with its SHA-256.
- **Parameter values.**
- **Expected outputs.** Each is a value with a tolerance, a predicate, or a selector
  such as "indices where true".
- **Tolerance rationale:** the published precision, a solver tolerance, or
  platform floating-point limits.
- **Confirmation status.** A derived expectation is not relied on until it is
  confirmed.

## Rules

- **When tests run:** on every build. A failure blocks the build.
- **Changing expectations:** an expected value changes only with a recorded
  substantive reason and the examiner's agreement.
- **What a test exercises:** the bundled implementation the build links, through
  the same entry point the application uses.
- **When oracles disagree:** if a published result cannot be reproduced from
  defaults, record a conflict. Do not adjust parameters until the
  test passes.
- **Discriminating power:** show that the tests fail for plausible wrong
  bindings. Examples: an alternative aggregation rule, another version of the
  pinned library, a different tie order. Record the runs.
- **Order:** where row order or ties can change a result, add a test that feeds the
  same rows in shuffled order with a recorded seed.
- **Tolerances across platforms:** BLAS and library versions change floating-point
  results, so cross-platform equality is tolerance-based. Bitwise equality is
  required of the builder's output, not of numerical results.
