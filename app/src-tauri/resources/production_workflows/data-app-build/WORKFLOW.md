---
name: data-app-build
description: Build an interactive data application with an agent from an accepted specification closure only, decide conformance with a test suite generated from the specification before the build, examine the result independently, and present the built application for the owner's acceptance without deploying it.
metadata:
  kind: instruction
  surface: workflow
---
# Build a data application from its specification

Use this method when an accepted app specification exists and the human directs an
agent to build it. It applies to the family the data-app-spec workflow serves. The
specification closure is the only input that carries meaning:
- the canonical specification and its lock;
- the assets, data products, component bundles and knowledge packs the lock pins.

A build presented for acceptance starts from an accepted closure. A draft build, made to
examine a specification before acceptance, may start from a frozen candidate. It is
labelled draft throughout and is never presented for acceptance or deployed.

The builder reads nothing else: no design record, no reference app, no working notes.
Anything the build needs that the closure does not say is a specification defect. It
goes back to `data-app-spec` in `revise` mode; it is never settled in the build.

The normal result is a built application with its conformance report, element map,
build manifest and examination record, presented for the owner's acceptance for its
consequence tier. Other reportable outcomes:
- a refusal that names the unmet preconditions;
- a partial build of a declared partial coverage;
- a returned build.

None of these is a deployed or released application. Deployment and release are
separate owner acts.

## Why conformance decides, not the builder

An agent builder does not give the bit-reproducibility a deterministic builder program
would. Agents do not reliably follow specifications, and regenerating code from the same
specification gives different code. This method therefore does three things:
- it generates the conformance suite from the specification before the build, by a
  contributor other than the builder, and has it examined against the specification
  before it is frozen;
- it requires an element map from every specification element to the code that
  realises it;
- it has a separate agent examine the build against the specification.

Two builds from one closure may differ in code. Both must pass the same suite. A passing
suite establishes conformance to what the suite checks: it is not correctness beyond the
tests' oracles, and not adequacy for use (thesis Chapter 6 §6.7.3).

## Roles

WORKING_ITEMS normally owns the build as its integration owner. HELPS_HUMANS may hold it
where the build is small. One integration owner keeps the closure, the suite, the
builder's returns and the examination together.

TASK contributors carry bounded parts, and none delegates:
- **Suite author.** Generates the conformance suite from the specification and does not
  build.
- **Builder.** Builds against the frozen suite and does not edit it.
- **Examiner.** A separate agent that authored neither. It examines the suite before it
  is frozen and the build afterwards.

The human directs the build, rules on any specification revision it exposes, accepts the
built application for its tier, and alone deploys or releases it.

## Sequence

```text
1. Admit the closure: verify hashes, validate in the buildable profile, check capability.
   Refuse with a report if a precondition fails.
2. Generate the conformance suite from the specification; examine it; freeze it.
3. Build against the closure and the frozen suite; keep the element map.
4. Run the suite; repair the build, never the suite or the specification.
5. Examine independently; repair and backcheck.
6. Package: build manifest, conformance report, provenance record.
   Checkpoint: the owner's acceptance of the built application for its tier.
7. Hand back. Deployment, if directed, is a separate act.
```

A defect found at any stage that lies in the specification, rather than in the build,
stops the build for that element. Report it as a specification finding for `data-app-spec`
`revise`. Unaffected elements may continue when the owner says so.

## Resources

Load [the contract](resources/contract.md) for inputs, outputs and records, and [the
method](resources/method.md) for the stage in hand. Use [checks](resources/checks.md)
before the checkpoint. Dispatch builders and suite authors with [the brief
template](resources/brief.md). The builder's obligations are in the [builder input
contract](resources/builder-input-contract.md).
