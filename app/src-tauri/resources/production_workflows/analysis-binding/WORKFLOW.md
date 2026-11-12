---
name: analysis-binding
description: Bind each computation a data application needs to a domain method and a versioned implementation with a typed interface, grounded parameter values, preconditions, explicit result semantics and known-answer tests, or specify the missing component as new work, with independent examination of numerical meaning.
metadata:
  kind: instruction
  surface: workflow
---
# Bind analyses to methods and implementations

Use this method when an application specification needs computation beyond its
closed transform vocabulary. Examples:
- control-chart limits and rules;
- spatial interpolation;
- a trend test;
- a dispersion model;
- a population projection with a breakeven search;
- a risk or prioritisation score.

The specification does not describe such analyses line by line. It binds them:
- a **method**: the domain idealization, with its assumptions and applicability;
- a **component**: a registry entry with a typed interface and a pinned, hashed
  implementation;
- an **analysis**: this application's use of the component, with inputs, parameter
  values and their grounds, preconditions and user messages, and the result's
  meaning stated explicitly.

The builder links the pinned component. It reads the interface from the
specification closure, never the component's source. This is the escape hatch
that keeps "the builder reads only the specification" true without turning the
specification into a programming language. The same design appears in
Vega's registries, Grafana's panel plugins and Vizro's rule that
configuration may "only reference registered names".

The normal result is a set of bindings ready for the specification, plus a
component specification for each component that does not yet exist. A new
component becomes work for decomposition: a deliverable whose acceptance includes
its known-answer tests.

## Three questions kept apart

A binding is examined against three different questions (thesis worked example;
Chapter 8 §8.5.2):

| Question | What answers it |
|---|---|
| **Numerical verification:** does the component compute the stated method correctly? | Known-answer tests against independent oracles, with justified tolerances |
| **Model applicability:** do the method and its inputs suit this application's data and question? | The method's assumptions and applicability in the domain pack, checked against the actual data contract |
| **Adequacy for the intended use:** do the results support the reliance the application invites? | The human's and the domain reviewer's judgment, informed by the other two |

A passing test answers only the first.

## Roles

- **Lead.** HELPS_HUMANS leads where method choice is a design question;
  WORKING_ITEMS leads where production dominates.
- **TASK** carries bounded contributions: interface drafting, known-answer-test
  sourcing, an independent oracle computation, and examination.
- **Separate examiner.** The binding has numerical meaning, so it is examined by a
  separate agent who did not author it (AGENTS.md, Verification and authority).
  Domain experts and independent verification join as the tier requires
  (`data-app-spec`'s gates).
- **Rulings.** The human or domain expert rules on consequential method choices,
  for example an estimator, a variogram selection rule, or reproducing a reference
  defect.

## Sequence

```text
1. Inventory the analysis needs.
2. Select the method; rule consequential choices.
3. Discover and assess candidate implementations.
4. Define or confirm the component interface.
5. Bind inputs, parameters, preconditions and result semantics.
6. Design verification: known-answer tests and properties.
7. Examine independently; repair and backcheck.
8. Freeze bindings and component entries, or specify new components.
9. Hand off to data-app-spec, and new components to decomposition.
```

Load [the contract](resources/contract.md) for the component entry and binding format,
[the method](resources/method.md) for each stage, [known-answer tests](resources/kat.md)
when designing verification, and [checks](resources/checks.md) before freezing.
