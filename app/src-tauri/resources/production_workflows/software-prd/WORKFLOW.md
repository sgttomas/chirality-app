---
name: software-prd
description: Develop a product requirements document for a new software product or a defined development undertaking with the human, examine the complete candidate independently, and hand the human-accepted PRD to software-decomp as its accepted basis. For a successor PRD formed by examining an existing project, use reverse-engineer-software. Not for maintenance, bug repair, issue-ticket execution, or stand-alone data repair or analysis.
metadata:
  kind: instruction
  surface: workflow
---
# Develop a software product requirements document

Develop a readable product basis that the human recognises as their intended
undertaking and that another participant can use for decomposition and project
setup. Work through conversation, concrete proposals, evidence, and an evolving
document. Give the human consequential choices with their reasons and
consequences. Reserve judgment for people; agents contribute reckoning,
preparation, and checks.

This package applies chapter 2 of the management manual
(`docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Consolidated_v9.md#ch_2`,
"A basis that supports action") to a software PRD as six working steps and two
grouped human checkpoints, A and B; section 2.5, "Prepare the decision before
requesting it", governs how each checkpoint is prepared. Registration of this method and acceptance of a PRD
produced by one of its runs are separate decisions.

## Applicability

Use this method for a new software product or a defined development
undertaking within an existing product: a feature, application, service, API,
library, platform, integration, or a coordinated product comprising several of
these. A product need not have a graphical interface. Its users may act through
other software, and its outcome may depend on several systems or organisations.

Do not select it for a patch, bug repair, issue-ticket execution, routine
upkeep, dependency update, stand-alone database repair, or analysis assignment.
Size, difficulty, and the number of affected files do not turn maintenance into
product development. A maintenance finding can motivate a separately directed
product project; preserve that distinction and the existing repair obligation.
A feature request recorded in a ticket can supply the initial intent of a
genuine development project. Inspect the purpose rather than classifying by
keywords.

**Relation to `reverse-engineer-software`.** When the new product basis is to
be formed by examining an existing software project, recovering its exemplars
and lessons, and developing its successor, use `reverse-engineer-software`.
Use this workflow when the PRD is formed from intent, conversation, and
supplied sources without that reverse-engineering inquiry. Both workflows use the same
checkpoints A and B and hand `software-decomp` an accepted basis carrying the
same basis-identity fields its group 1 consumes: path, content hash, separate
acceptance decision record, accepted portions and shared constraints (contract
resource, "Handoff to `software-decomp`"). An existing codebase can still be a source here, examined within its
supported scope; selecting this workflow does not require a reference-project
study.

The normal result is a human-accepted, content-identified PRD and a handoff that
`software-decomp` group 1 can record as its accepted basis. A draft, a review-pending candidate, a returned candidate, or a
decision not to pursue the product are also reportable outcomes; none may be
described as an accepted PRD. The method ends before decomposition, project
setup, production implementation, or release.

## Roles

HELPS_HUMANS normally leads the design with the human, directly or through
HELP_HUMAN, and owns the coherence of the assembled product account. Keep one
integration owner. HELP_HUMAN may conduct the alignment conversation, route the
undertaking to HELPS_HUMANS, or dispatch a bounded Type 2 contribution such as
the independent examination. Where sustained document production warrants
WORKING_ITEMS, arrange that undertaking through the human or HELP_HUMAN;
WORKING_ITEMS organises the writing and integrates returns while design
decisions stay with HELPS_HUMANS and the human. WORKING_ITEMS is also the usual
consumer of the handoff when the human directs `software-decomp`.

The workflow is compatible with HELP_HUMAN, HELPS_HUMANS and WORKING_ITEMS;
TASK does not select or run it. Bounded inspections, comparisons, section
writing, and reviews may still be assigned to TASK with a brief naming sources,
write targets, return, and checks. TASK works from that brief without
selecting this workflow, does not delegate, and returns integration needs and human decisions to
its caller. Selection does not change role or create a PRD-specific agent.

## Sequence and grouped checkpoints

```text
1. Intake and triage.
2. Develop the product account and confirm direction.
   Checkpoint A: product direction and basis for authoring.
3. Author the PRD and carry its open work.
4. Examine the complete candidate and repair it.
5. Obtain acceptance of the identified product basis.
   Checkpoint B: reviewed PRD and passage to FEED.
6. Preserve the result and hand off without starting FEED.
```

Agents prepare a concrete, checked package before each checkpoint; source
examination, writing, investigation, and routine repair between them add no
approvals. Uncertainty alone creates no extra prompt. Return to the human
between checkpoints only when a choice would change an agreed outcome,
constraint, boundary, or reserved decision.

- **Before checkpoint A**, prepare the proposed outcome, users and consumers,
  boundary, inherited basis, important constraints, source inventory and
  limitations, consequential open choices, and the approach to authoring and
  examination. Check source identities and that each stated commitment traces
  to the human's words or an identified source. An existing explicit direction
  covering these matters satisfies checkpoint A; cite it and its scope rather
  than asking again.
- **Before checkpoint B**, freeze the complete candidate and its manifest,
  obtain the independent examination, repair and backcheck within authority,
  and run link, identity, requirement-reference, and open-question checks.
  Present the exact normative set, the source and review account, remaining
  findings and open questions, and the proposed accepted portions and next use.

Neither checkpoint accepts the completed product or authorises work beyond its
stated scope.

## Inputs, outputs, and handoff

The brief supplies the product boundary, the human decision-maker, the selected
workflow identity, `WORKING_ROOT`, `RUN_ROOT`, `PRD_TARGET`, and permitted
writes. When it names no locations and the project has no convention, the
defaults are `RUN_ROOT = {WORKING_ROOT}/planning/prd/<run-id>/` and
`PRD_TARGET = docs/PRD.md` (relative to `WORKING_ROOT`). The run keeps a
working record and candidate and freezes each examined candidate. Checkpoint A
is recorded as a note in `PRD_RECORD.md`; it needs no immutable snapshot. Only
checkpoint B is always snapshotted: its decision is recorded in an immutable
snapshot (`DECISION.md`, `ACCEPTED_MANIFEST.csv`, `HANDOFF_STATE.md`) outside
the content it identifies.
The handoff names the PRD identity (path, content hash, revision where
versioned, and included set), the separate decision record, and the
accepted-portions list with shared constraints, explicit exclusions, and open
work, which is exactly what `software-decomp` group 1 records as its accepted
basis.

## Resources

Load [inputs, outputs, and the handoff contract](resources/contract.md) when
framing the assignment and again before checkpoint B. Use
[the detailed method](resources/method.md) for the current step. The
[product questions](resources/product-questions.md) support steps 1 to 3; the
[record and review guide](resources/records-and-review.md) supports the working
record, the independent examination, and interruption.
