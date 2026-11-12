# analysis-binding: method

## 1. Inventory the analysis needs

For each question or view that needs computation, record:
- the inputs and their data contract;
- the outputs, with types, units and CRS;
- candidate method families;
- the consequence of a wrong result and how detectable it would be.

Then separate:
- **Declarable work:** relational transforms in the closed vocabulary. Filter,
  aggregate, join, derive and similar operations stay in the specification.
- **Component work:** domain analyses that need a component, such as interpolation,
  statistical process control, population models, dispersion and optimisation.

The split exists because declarative view grammars cover relational and statistical
primitives but not domain analyses.

## 2. Select the method

From the domain pack, state for each method:
- the idealization;
- its assumptions;
- its applicability conditions;
- its limitations.

Check them against the application's actual data. For example:
- Is the baseline stationary?
- Are there enough stations each month for a variogram?
- Is a variable circular?

When the data do not meet a condition, take one of three courses:
- choose another method;
- surface a caveat that the application must show;
- return the finding.

In derive mode, the reference application's method is evidence, not a mandate.
Its fidelity decision states whether it is reproduced or corrected.

Prepare proposed rulings for consequential choices, with their effect on results:
- the estimator;
- the limit multiplier;
- the variogram family and fitting rule;
- the handling of non-detects;
- the treatment of a code/paper discrepancy.

The human or domain expert decides.

## 3. Discover and assess implementations

Search the registry first. For each new candidate, record:
- **purpose and maintenance:** releases and maintainer activity;
- **community use and testing:** the R Validation Hub's assessment headings;
- **licence;**
- **behaviour across versions.**

Choose and pin a version. Record behaviour changes that matter. A wrapper around a
library is a component in its own right. Keep it thin and give it its own version.

## 4. Define the interface

Write the component entry:
- typed ports with schemas, units and CRS;
- parameters with domains and units;
- outputs;
- determinism class;
- tolerance policy with its rationale;
- preconditions, each with a failure behaviour and a message;
- known limitations.

Keep the computation independent of UI, storage and clocks so that it can be
exercised directly. Pass seeds and random-number generator kinds explicitly for
stochastic components.

## 5. Bind

Map the application's data fields and state to ports and parameters. For each
parameter value, give its grounds and standing. Write `result_semantics` for every
meaning the interface does not carry. For example:
- limits are computed from the baseline only and not updated;
- rules are evaluated over baseline points too;
- λ is the dominant eigenvalue here and a realised ratio elsewhere;
- N (new) is clamped at zero in some tabs and not in others.

## 6. Design verification

Design the known-answer tests and property tests ([kat.md](kat.md)). Include:
- negative and boundary cases, such as too few observations, missing values,
  unparseable dates, a single station, or zero emission;
- application-level pipeline tests that set the relevant state.

Use `software-test-planning` to map risks to tests where the component is new code.

## 7. Examine

Give the examiner:
- the binding and component entry;
- the domain pack items;
- the sources;
- the tests and their oracles.

The examiner checks:
- method choice against applicability;
- parameter grounds;
- unit and CRS consistency;
- whether each test can distinguish correct from defective behaviour, since test
  count is not evidence (thesis Chapter 8 §8.5.2);
- that tests reach the implementation the build links.

Repair, then backcheck. Present findings that need a ruling.

## 8. Freeze or specify

Freeze bindings and component entries with hashes once bundles exist. For a missing
implementation, write the component specification for decomposition and mark the
binding `bundle_tbd`.

## 9. Hand off

Return:
- bindings and entries to `data-app-spec`;
- component specifications to decomposition, through `data-app-spec`'s handoff;
- open questions and rulings needed.

When a library version, a domain-pack edition or a method ruling changes, reopen
only the affected bindings and re-run their tests.
