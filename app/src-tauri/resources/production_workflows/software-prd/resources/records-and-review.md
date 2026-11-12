# software-prd — records, review, and handoff

These specimens support the `software-prd` method. Field names and illustrative IDs are local examples, not additions to Chirality's global schemas or decomposition identifiers. The required acceptance and handoff records are defined in the [contract](contract.md). Keep a small run's information in one supporting record where practical. Split registers or annexes only when separate working surfaces improve use, delegation, or examination.

## Working record

`PRD_RECORD.md` can hold the following sections:

- Assignment, product boundary, actual role and selected workflow origin, permitted writes, and the intended PRD location.
- Sources and their permitted use, including identity, relevant location, limitations, and treatment.
- Human directions with actual words and references, separately identified agent interpretations, and checkpoint coverage.
- Material open questions, assumptions, conflicts, and the work needed to address them.
- Current draft and contribution locations, review evidence, findings, and the next bounded work.

A source table might read:

| Source | Contribution | Treatment |
|---|---|---|
| Recorded owner direction, identified passage | Protect manual work while a proposal is inspected | Use as intent; proposed technical wording remains reviewable |
| Existing history specification, identified accepted revision | Behaviour the extension must preserve | Use within its stated scope; examine later amendments |
| Prototype result, identified candidate and scenarios | Demonstrates separate preview in the exercised cases | Use as limited evidence, not production qualification |
| Earlier agent proposal | A considered alternative | Context only unless a human decision adopts it |
| Referenced interface document not yet accessible | Possible external constraint | Hold dependent claims; record the access or clarification needed |

“Use” identifies a role in the authoring basis. It does not make every statement in a source true or resolve a conflict with a higher-priority instruction. Keep the reason for withholding or limiting material where a later writer might otherwise revive it.

## Requirement and open-question relationship

In the editor illustration, a PRD-local requirement could state:

> When the user rejects an unapplied proposal, the editor leaves the live document, including manual work performed while the proposal was open, unchanged. The preservation account identifies which editing-state properties are included. The intended benefit is that users can keep working while considering assistance.

Until the relevant properties are defined, the statement remains incomplete in that respect. Its source is the owner's preservation intention; it is not evidence that the implementation satisfies it. A related open question might be:

```text
Question: Which editing-state properties must rejection preserve?
Basis:    <owner direction and applicable product specification>
Affected: Rejection behaviour, history integration, validation scenarios
Work:     Inspect current editing state and prepare a proposed boundary.
Owner:    <actual responsible design participant>
Needed:   Before accepting the preservation account on which FEED relies.
Status:   Open; no accepted answer recorded.
```

Another question, such as the internal mechanism for comparing revisions, may remain for later design if its constraints and consequences are clear. Treat each according to its effect on the proposed reliance.

## Bounded review brief

The reviewer needs the actual candidate and its sources rather than only the author's summary of why it is good.

```text
Undertaking: Examine this complete PRD candidate for use in FEED.
Candidate:   <main document, normative annexes, and content identities>
Basis:       <original directions, accepted constraints, source record>
Focus:       Intended use; inherited commitments; boundaries; observable
             outcomes; open choices; unsupported claims; cross-section fit.
Writes:      <review return only>
Return:      Coverage, findings with source locations, missing inputs,
             proposed treatment, and limitations of the examination.
Authority:   No PRD edits, human dispositions, or acceptance claims.
```

An agent reviewer reports what it examined and what it found. A human review has its own competence and decision scope. Neither should be represented by the other. When a fresh review instance cannot be launched, record that fact and retain the pending review obligation rather than impersonating another reviewer in the same context.

Useful finding categories inherited from the DBM practice are:

| Category | Examination |
|---|---|
| Incorrect | Does the statement contradict the applicable basis? |
| Unsupported | Is a factual assertion or claimed feasibility unsupported? |
| Missing | Has a material obligation or qualification disappeared? |
| Flattened | Has a proposal, assumption, conflict, or TBD become settled prose? |
| Outdated | Has superseded material been restored? |
| Incomplete | Is the topic present but insufficiently developed for the next use? |

These categories guide the review; they do not determine a human disposition. A legitimate proposed capability is not “unsupported” merely because it is not built. Its status, reason, constraints, and unresolved feasibility must be expressed honestly. The reviewer should not force every proposal into the form of a proven existing fact.

For each substantive finding, identify the candidate passage, source or missing grounds, consequence, proposed response, and disposition status. Record a repair made within authoring discretion as such. Record a decision about scope, an accepted constraint, or consequential uncertainty only from the actual human response. Backcheck corrections against the current candidate and assess their effect on related passages.

## Candidate and acceptance identity

The [contract](contract.md) defines the frozen candidate, its manifest, and
the checkpoint B snapshot. In a simple file host, a run might look like this:

```text
<RUN_ROOT>/
  PRD_RECORD.md                       sources, directions, open work, review links
  candidate/PRD.md                    working text
  review/<candidate-id>/...           retained reviewer returns and backchecks
  candidates/<candidate-id>/          frozen PRD, included annexes, CANDIDATE_MANIFEST.csv
  checkpoint_snapshots/B-<UTC>/       DECISION.md, ACCEPTED_MANIFEST.csv, HANDOFF_STATE.md
  checkpoint_snapshots/_LATEST_ACCEPTED.md
```

Keep the decision outside the files whose hashes it cites. A decision record can
identify the manifest without claiming that the manifest includes its own hash.
Record whether a linked file is normative content, evidence, or navigation so a
reader knows what the human actually accepted. If the human accepts only a
feature within a broader document, identify that portion and its common
constraints; do not present the remainder as accepted or consume it during
FEED.

## Pause, resumption, and return

Before a meaningful pause, retain the candidate, known sources, explicit decisions, completed contributions, open findings, unresolved questions, and next proposed work. Cite the actual locations. A suggested next action belongs to the outgoing agent; it does not become the owner's instruction through repetition.

On return, inspect the files and current instructions before relying on the handoff. New sources, concurrent changes, or a later human decision may invalidate part of the earlier preparation. Reopen the affected work and preserve the rest. Do not manufacture an accepted predecessor, completed setup, or project DAG when the undertaking has not reached that point.

The final return states whether the result is a draft, review-pending candidate, human-accepted basis, human-accepted limited basis, returned candidate, or stopped undertaking. These are descriptive outcomes, not new deliverable lifecycle states. Include exact paths and decision references, acceptance scope, current source and review limitations, open work and its owners, and the `HANDOFF_STATE.md` path that `software-decomp` group 1 reads. Do not start FEED without the applicable human direction.
