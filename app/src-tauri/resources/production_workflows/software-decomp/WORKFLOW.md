---
name: software-decomp
description: Organize software intent into cohesive work domains and implementable bounded contexts.
metadata:
  kind: instruction
  surface: workflow
---

# software-decomp

Organize software intent into cohesive work domains and implementable bounded contexts.

WORKING_ITEMS coordinates this undertaking and assigns bounded contributions to TASK.

This package implements the grouped-checkpoint Chirality v3 edition of
`sgttomas/chirality:docs/COMPATIBILITY_FORMATS.md#historical-decomposition-contract` (private archive) (commit `9b005c23a`, 2026-09-09; a prospective
amendment, see the standard's status note), as amended by D-GOV-47
(2026-09-26: optional combined review for a small, reversible undertaking) and
D-GOV-48 (2026-09-26: every scope item, whether IN, OUT or TBD, has one Package
home, superseding D-GOV-47's IN-only rule). That citation is provenance:
conformance is determined from this package's own contract and method, which
state the rules that apply. An in-flight project keeps the edition it adopted;
nothing is retrofitted.

## Method

1. Record the accepted basis identity and accepted portions, then extract atomic scope, objectives and unresolved decisions from that accepted software intent. Carry actual needed inputs with their responsible consumer, intended use/condition and source; leave unknown bindings explicit for local need authoring in setup.
2. Define flat Packages and Deliverables, judging semantic coupling and verification demands. State how each Deliverable will be known to be done and how each Objective will be checked, name the thin end-to-end path where the undertaking has an integrated path, and record any coupled core.
3. Specify each Context Envelope, artifact, interface, acceptance condition, and source mapping, and prepare checks before each grouped human checkpoint.
4. Preserve stable IDs through three checkpoint groups: basis; proposed structure with findings; and audited final acceptance for downstream use. For a small, reversible undertaking the human may choose to decide all three in one sitting after the independent audit.

## Resources

Load [inputs, modes, and output contracts](resources/contract.md) when framing the assignment. Use [the detailed method](resources/method.md) for the current stage. Resolve tool commands against the declared tool root.
