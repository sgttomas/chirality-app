# data-app-spec: proportionate gates

Gates scale with the consequence of relying on the application, not with its size or
archetype. Every tier has the two human checkpoints. Higher tiers add examination and
widen the examiner's independence.

This scheme draws on the common mechanism found across assurance sources:
- state the intended use;
- determine the risk;
- scale the evidence and the reviewer's independence;
- keep a short record;
- have a second qualified person check the assessment.

Those sources include:
- FDA Computer Software Assurance and GAMP 5 (secondary sources only);
- IEEE 1012 integrity levels (secondary sources only);
- the US EPA graded approach to model evaluation;
- the R Validation Hub's two-person review.

It also applies Chirality's rule that numerical meaning warrants targeted checks and
independent scrutiny (AGENTS.md, Verification and authority) and the thesis's
proportionate-rigor argument (Chapter 7 §7.9.3).

| Tier | Typical use | Minimum evidence before checkpoint B | Examiners | Who accepts |
|---|---|---|---|---|
| T0 illustrative | Teaching or demonstration | Structural and semantic validation; the KATs each analysis component has (published, or derived and marked for confirmation); visible "demonstration" intended-use text | Separate agent for analysis bindings with numerical meaning | Owner |
| T1 exploratory | Public or analyst exploration with stated non-uses | T0, plus: at least one independent oracle per analysis component; data citation, vintage and licence displayed; disclaimer and non-uses visible; link health | Separate agent; peer reviewer for the domain pack | Owner |
| T2 decision support | Results inform identified decision makers | T1, plus: intended-use and risk record; property or metamorphic tests for each analysis; limitations and uncertainty visible where results are shown; conflicts between sources ruled by the domain expert | Separate agent; qualified domain expert for the domain pack, assumptions and bindings | Owner and accountable domain owner |
| T3 professional reliance | Compliance, inspection, regulatory or public-health reporting | T2, plus: independent verification and validation of each component (independent implementation or certified reference data); regulatory or benchmark cases where they exist; full provenance package per release; change control on KAT expected values | Independent V&V; external peer review where the domain expects it; professional of record | Owner; where professional obligations apply, also the accountable professional, for the application's professional use. Work products made with the application are authenticated one by one, under those obligations, outside the application |

The design checkpoint (new and revise modes) applies at every tier. At T0 it may be
held together with checkpoint B, when the human prefers one review of a small app.

At every tier:
- A KAT failure blocks the build.
- An expected value in the specification changes only through a specification
  revision, with a recorded substantive reason and the examiner's agreement. A derived
  test in a conformance suite that does not follow from the specification is a suite
  defect, repaired as `data-app-build` states.
- Deployment requires the owner's acceptance of the built application under
  `data-app-build`, with the tier's conditions. At T3, that includes the accountable
  professional's acceptance for professional use where obligations apply.
  Authentication attaches to each work product made with the app, not to the app.

At T3, release remains an owner act.

What the gates do not do:
- They do not establish that the application is adequate for its use. That remains
  the accountable person's judgment, informed by the evidence.
- A passing gate establishes only what its checks examined.
- Gates are not added at lower tiers merely to show concern. A control earns its
  place by what it contributes against its cost in attention and delay
  (thesis Chapter 3 §3.2.4).
