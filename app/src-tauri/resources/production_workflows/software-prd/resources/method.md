# software-prd — method

Each step below states the work, the preparation before any human decision, and
what to do when inputs are incomplete, checks fail, or work is interrupted.
Locations, records, and the acceptance snapshot are defined in the
[contract](contract.md).

## Before starting

Resolve the inputs in the contract from the assignment and actual host context.
Before writing, inspect `PRD_TARGET`, any predecessor PRD and its acceptance
record, and concurrent edits. Keep the new candidate separate from an accepted
predecessor. Do not replace another project's basis or overwrite unrelated
work. Record the selected workflow's source-qualified identity and content
hash; an unqualified name does not authorise switching to another library's
version.

## 1. Intake and triage

Read the human's request and relevant conversation first. Recover what is being
attempted, the reasons it matters, existing commitments, and the questions still
being explored. Identify whether this is initial formation, continuation of a
draft, or proposed revision of an accepted PRD. Return out-of-scope maintenance
to its appropriate assignment; do not generate a PRD to make the request fit. If
the undertaking is to form a successor by examining an existing project, propose
`reverse-engineer-software` instead.

Inspect the supplied material and follow references that matter to the intended
product. A new project may start with little more than the conversation. A large
existing product does not require indiscriminate reading of every file before
useful drafting can begin.

For material used or withheld, record its identity and revision where available,
the relevant location, what it can support, and any limitation. Distinguish:

- human intent and adopted commitments;
- observations and test evidence about what exists;
- proposals, assumptions, and alternatives;
- navigation or explanatory material that points to a source without replacing
  it.

Record unreadable, missing, conflicting, superseded, or irrelevant material
explicitly where it affects the account. Do not use the absence of a source as
evidence that an obligation is excluded. Keep private data and credentials out
of copied evidence; use authorised redacted or synthetic examples when
sufficient and state their limits.

Triage leads to action: use the source within its supported scope; retain it as
context; hold an affected claim pending clarification; or exclude it from the
present basis with a reason. Expand investigation where a material decision
depends on it. Continue unaffected drafting when its grounds are adequate. Do
not stop the whole undertaking for a minor missing reference or hide a material
conflict to keep it moving.

Use tools that the host actually provides for extraction, search, comparison,
and identity checks. Read the relevant source beyond the search snippet. If
conversion, repository inspection, or a required source is unavailable, record
the limitation and bound the conclusions. This method requires neither a DOMAIN
knowledge root nor DBM publication tools or semantic-processing artifacts.

## 2. Develop the product account and confirm direction

Make the intention inspectable through a narrative of use, concrete scenarios,
alternatives, and definitions. Establish who uses or depends on the product,
what they should be able to accomplish, the present situation, and what the
project is to change or preserve. For a headless service, describe callers,
operators, exchanges, and resulting state instead of inventing screens or
personas.

Follow consequential cases across boundaries: starting conditions, actions,
results, interruptions, and recovery. Bring into consideration data ownership,
external interfaces, permissions, operating environments, compatibility,
performance, security, accessibility, observability, and delivery or transition
needs when they bear on this product. The
[product questions](product-questions.md) provide prompts, not a compulsory
catalogue. Supply no invented user research, target values, regulatory
obligations, or proof of feasibility.

Separate objectives, required behaviour, constraints, proposed designs, and
exclusions. Explain the reasons for important choices. Distinguish an act
excluded from a component because another participant owns it from a capability
excluded from the product. Record actual existing external owners or contracts;
mark future allocation unresolved instead of inventing deliverable IDs.

Develop a proportionate document plan. A feature may need one cohesive narrative
and a few requirements. A larger product may need an overview and several
normative annexes with clear boundaries and shared terminology. Product sections
and capability groupings do not become FEED Packages or Deliverables through
their inclusion in the PRD.

**Prepare checkpoint A.** Assemble one proposal: outcome, users and consumers,
boundary and inherited basis, important constraints, source inventory and
limitations, consequential open choices with options and consequences, and the
approach to authoring and examination. Check that each stated commitment traces
to the human's words or an identified source and that proposals are marked as
proposals. A sketch or draft may accompany it to elicit the decision.

**Checkpoint A: product direction and basis for authoring.** The human confirms
or corrects that position. An existing explicit direction covering these
matters satisfies the checkpoint; cite it and identify its scope rather than
asking for the same decision again. The checkpoint neither accepts the eventual
PRD nor freezes every design detail or heading.

Record the human's actual words and their source as a note in `PRD_RECORD.md`,
distinguish your interpretation, and carry the resulting decisions into the
draft. Checkpoint A needs no immutable snapshot; only checkpoint B is always
snapshotted. Reopen only affected decisions when the basis changes.

## 3. Author the PRD and carry its open work

Write the product account from the confirmed direction and identified sources.
Keep the substantive requirements, limits, relationships, and qualifications in
the body or explicitly included normative annexes. The reader should not have
to reconstruct a committed behaviour from trace tables. Place detailed source
tracking and authoring history in the working record.

Give each consequential requirement a stable reference, using the project's
existing convention or distinct PRD-local references. State the subject,
relevant conditions, required outcome, source or proposed rationale, and an
appropriate future means of examination. A proposed behaviour need not already
exist; evidence of current behaviour must not be presented as proof of the
proposed result. Mark new design proposals for the human's consideration.

Preserve the distinction between verification against the stated requirement
and validation of suitability for intended use. Describe observable outcomes and
representative acceptance scenarios without pretending to have tested an
unbuilt product. Do not invent numerical targets for the sake of measurability.
An unresolved target needs an owner, a reason it matters, and a point by which
dependent work needs its treatment.

Keep one account of each material open question: what is unknown or undecided,
what constrains its answer, which work may rely on it, the proposed
investigation or decision owner, and the condition by which it must be
resolved. Distinguish a missing source, an unresolved intention, an unverified
assumption, a later design choice, and a writing defect; their treatments
differ. A human may accept a specified uncertainty for the next phase without
turning it into a verified fact.

Scale detail to the product's novelty, interactions, stakes, and inherited
basis. The PRD need not contain the detailed design expected at 60%. Explain the
exposure of hidden interacting assumptions concretely rather than manufacturing
a completeness score or gate threshold.

Use bounded investigations to settle questions that materially affect the
basis. State their purpose, source scope, permissible writes, expected return,
and checks. Keep prototypes isolated from production. Preserve useful results
and limitations.

Where contributions are delegated, retain the brief and return, identify actual
sources and settings where available, and keep writes disjoint. The integration
owner assembles the document and examines shared meanings and boundaries.
Cross-section contradictions return for repair or human decision.

## 4. Examine the complete candidate and repair it

Identify the complete candidate, including every normative annex and
incorporated reference necessary to interpret its commitments, and freeze it
with its candidate manifest. Check links, identities, requirement references,
open-question treatment, source currency, and the correspondence between the
accepted direction and the authored account. Tools can check represented
structure; their success does not establish that a requirement captures the
intended product.

Obtain a separate examination from a competent human reviewer or a separate
review instance that did not author the candidate. Give the reviewer the frozen
candidate, the relevant original directions and sources, open questions, and a
bounded brief (see the [record and review guide](records-and-review.md)) to
seek defects and unsupported claims across the whole product account, including
interfaces, exclusions, acceptance scenarios, and the grounds for consequential
assumptions. A same-model reviewer is independent in preparation, not model
diversity. Its report is a contribution for human assessment.

When a separate reviewer or required source cannot be obtained, retain the
candidate and report the outstanding examination. Author self-checks remain
useful but do not satisfy this step. Do not mark the candidate ready for
acceptance until the required examination is complete. Discussion with the
human can continue meanwhile.

Record findings with candidate location, supporting material, explanation,
consequence, and proposed treatment. Repair mechanical or editorial defects
within authority. Present changes to commitments, source authority, accepted
constraints, or the treatment of consequential uncertainty to the human; do not
request a ruling on every typographical correction.

Backcheck corrections and assess related sections. Changes after review require
coverage of the changed content and its effects under a new candidate identity.
A targeted rerun may suffice, but the final assembled set must have a coherent
review account. Report coverage and limitations; a lack of findings is not proof
of completeness.

## 5. Obtain acceptance of the identified product basis

**Prepare checkpoint B.** Freeze the final candidate and its manifest. Assemble
the exact normative set, the source and review account, remaining findings and
open questions, the proposed accepted portions, shared constraints, and any
proposed exclusions, and the proposed next use. Explain what the human is
accepting, what remains to be developed, and which limitations the next phase
must preserve. Include relevant technical reviewers where the project requires
their competence or authority.

**Checkpoint B: reviewed PRD and passage to FEED.** The human may accept, return
for revision, accept a clearly identified limited basis with an explicit
treatment of remaining work, or stop the undertaking. Resolve contradictory
directions and any material ambiguity about which content is accepted before
relying on the decision. Accepted limitations cannot waive higher-priority
obligations or imply that a missing review occurred.

Write the checkpoint B snapshot defined in the [contract](contract.md) from the
actual response. Update `_LATEST_ACCEPTED.md` only for an accepted or
limited-basis acceptance; a returned or stopped outcome leaves the pointer on
the predecessor. Use the host's established
approval mechanism where one exists. A changed candidate requires renewed
examination and an applicable acceptance of its changed basis; preserve
unaffected prior decisions and the historical candidate, and never transfer an
old acceptance to new bytes.

## 6. Preserve the result and hand off without starting FEED

When authorised, place the accepted PRD, or a byte-identical working copy, at
`PRD_TARGET` and verify its hash against the snapshot. If that target changed
concurrently or cannot be written, stop that write, preserve the accepted
candidate, and record issue to `PRD_TARGET` as outstanding in
`HANDOFF_STATE.md`. Do not claim delivery from a prepared but unverified copy.

The handoff gives WORKING_ITEMS the exact accepted input for `software-decomp`
when the human directs FEED. `software-decomp` performs its own three grouped
checkpoints; this workflow neither supplies their decisions nor manufactures the
Scope Ledger, Context Envelopes, Packages, Deliverables, or setup state. Existing
human direction may already authorise that continuation; otherwise the accepted
PRD supplies no independent permission to start it.

For continuity, prefer carrying the context through PRD acceptance,
decomposition, and setup where the project's loop allows it. If interrupted
sooner, retain the current candidate, actual decisions, sources, findings, work
position, and next bounded action in the working record. On resumption inspect
actual files and concurrent changes; do not repeat completed work or treat a
recommendation in a handoff as authority. Do not pretend a project graph or
execution root exists before setup.

For later PRD amendments, prepare a candidate against the accepted predecessor,
identify the changed commitments and downstream consumers, and repeat affected
examination and checkpoint B. If accepted decomposition is affected, hand the
amendment and its impact to `scope-change` through the applicable owner; do not
edit decomposition or its derivatives under this assignment. PRD acceptance
does not close those propagation obligations.

Stop at the present authoring boundary. Neither a completed PRD nor registration
of this method automatically launches another workflow.
