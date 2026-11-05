# Two usable journeys required before 4.0.0

## Owner direction and scope, 2026-11-03

After using signed candidate `b3dd4145` (source `f664ee1d`), the owner reported
that it still presents a walking skeleton and directed continued product work.
The owner specified the primary journey: “set up a project, select an existing
workflow, run it through completion.” Separately: do useful work, turn it into
a reusable workflow and resume it later without the agent translating the
application's engineering controls. The owner then confirmed “both journeys
now before 4.0.0 ships” and authorized proceeding.

This is the publication completion interpretation of DEL-02-02's existing
OUT-001/002/003 and CLM-005, with DEL-01-04's interaction contribution and
DEL-01-05's access inputs. It does not replace their ScopeOfWork, remove any
acceptance criterion, or authorize credentials, enrollment or publication.
Journey 1 is implemented and demonstrated first; journey 2 is not deferred
beyond this release. The actual joined examination remains DEL-09-02's work.

## J1 — use an existing workflow

A person can, through the App:

1. Set up an existing project, understand required settings/access and reach a
   usable workspace. Missing prerequisites name a concrete next action; setup
   does not rely on an agent assembling unexplained paths on the person's behalf.
2. Find and select an existing available workflow, understand which source and
   revision is selected, and supply its required inputs. Creating or registering
   a new workflow is not a prerequisite for this journey.
3. Start it deliberately, follow progress and respond to questions or approvals
   where required. Waiting, failed, interrupted and completed states remain
   distinct. A technical acknowledgment is not reported as completed work.
4. Reach completion and find the resulting work, its location and any remaining
   action. The App must not require interpretation of raw engineering records
   to determine what happened.

Completion evidence names the actual available workflow, project, candidate,
selected access mode, inputs, person acts, result and limitations. The workflow
must exercise useful work and real execution; a mocked success screen is not
completion. Source tests support the result; the owner-visible journey on the
identified candidate must also be observed.

## J2 — create, save, return and reuse

A person can, through the App:

1. Do useful work in a conversation and turn that work into a workflow draft.
2. Trial it, understand the result, revise if necessary and perform the actual
   review/registration act against the identified content. Merely writing a
   file or receiving a successful tool response is not registration.
3. Later find the saved workflow and run it again in the intended project with
   new inputs, preserving source and revision identity.
4. Return to unfinished work after closing/reopening and resume it without
   losing the draft, confusing read-only history with continuation, or silently
   replaying already completed actions.

J2's finish is a demonstrated create/trial/review/register/reuse sequence plus
actual return to unfinished work. Registration/collision/refinement behavior
still follows WORKSPACE_AND_REGISTRATION; this short journey does not waive
its other applicable cases.

## Shared finish conditions and boundaries

Questions and approvals use understandable consequences and actual person
acts. Cancellation, readable errors, recovery and normal close/reopen/Quit are
part of usability. Claims about completion, registration and recovery must
match the host's observed state. Relevant focused regressions and applicable
native qualification remain required, especially for persistence/permissions.

The selected v3 colors/fonts remain a visual reference, not proof of usability
or a request for broad v3 regression testing. No wholesale redesign is assumed:
repair demonstrated obstacles to these journeys using existing behavior where
it is sound. Diagnostics remain reachable without dominating the main task.
New filesystem defaults, permission changes or authentication behavior require
proper implementation/authority; a presentation change must not conceal them.

## Reconciliation of prior delivery

PRs #84, #86 and #87 improved setup/navigation, received-history inspection and
workflow drafting. PRs #88 and #89 repaired interruption/submission behavior.
Their source checks and the limits recorded in DEL-01-04's
[workspace presentation account](../../../PKG-01/DEL-01-04/Work/WORKSPACE_SETUP_PRESENTATION.md)
remain valid. Those changes did not demonstrate either complete journey.
The owner's present report establishes dissatisfaction with the product
experience; it is not a finding that every underlying capability is absent.

Current standing: **J1 open; J2 open.** No completed journey is inferred from
signing, notarization, layout fixtures, test counts or merged PRs. Implementation
returns must update the owning Work account with the changed behavior and actual
checks, reconcile affected ScopeOfWork/dependency meaning, and provide candidate
results to DEL-09-02. Scope and dependency contracts are unchanged by this
clarification; no maturity or acceptance status is advanced here.

Agent 0 owns design and integration. The existing product/frontend manager owns
the first implementation increment and its reconciliation. Native qualification
owns the observed candidate results, with owner acts reserved to the owner.
The coordination [publication punchlist](../../../_Coordination/PUBLICATION_PUNCHLIST.md)
only indexes this result; it is not another requirements source.

## Mounted transition coverage (2026-11-05)

Subject: integrated App main `0f6d8388420b5ba2bb513bb9f30fb80b65088e21`
plus this additive test contribution. Product `RunJourney.tsx` and
`MakeJourney.tsx` bytes are unchanged. The same-PR change is confined to the
existing `run-journey.test.mjs` / `make-journey.test.mjs` suites and owning
Work/current coordination reconciliation. ScopeOfWork, dependency conditions,
product acceptance, source pins and package/lock bytes retain their meaning.

The prior #125 and #128 source/mounted results did not exercise two transitions.
The historical renderer accounts retain exactly their original subjects and
unrendered limits:
[run results](../../../PKG-09/DEL-09-02/Work/RENDERER_RUN_RESULTS_20261104.md)
and [returning draft](../../../PKG-09/DEL-09-02/Work/RENDERER_RETURNING_DRAFT_20261104.md).
This later check does not turn those observations into a render of a new subject.

- **Open run and source replacement:** mount the whole Run guide with an open
  run displaying Working. Retain that exact row while replacing, separately,
  the spawn counter, App session and home, with active/waiting activity under
  the same bare conversation ID. Earlier-generation rows become read-only
  Results with “Open in an earlier Codex session”, no Show action, and a retained
  evidence link. Another home's row is excluded from the current home's view;
  no old run becomes current Progress or borrows the replacement request.
  A separately constructed run of the exact new source supplies the positive
  waiting/working control; its explicit Answer navigation targets that source's
  conversation without a host command. The original open row is never ended,
  rewritten or rebound. Existing direct unit checks still cover `runReading`'s
  home check; mounted home replacement also exercises the guide's outer home
  exclusion rather than exposing a private component solely for a test.
- **Queued Continue and superseded reveal:** first verify that a fresh Continue
  scrolls/focuses its own Draft state once. Before the next reveal effect can
  commit, a constructed microtask changes the selected draft, or replaces the
  active library with a same-name draft. The later draft's state renders, but
  the stale reveal neither scrolls nor focuses it. A subsequent observation
  cannot resurrect that reveal; a fresh explicit Continue still works. No
  workflow command, conversation opening or prepared message is issued, and
  the retained draft/trial rows remain unchanged.

Inputs reuse the existing host, `runRow`, draft and `producerTrials` fixtures.
Replacement generations/homes, current run, library, draft findings and timing
are explicitly constructed. The retained trial rows have the existing native
producer **shape**; no Rust producer, native History, durable relaunch, model or
new actual trial was executed here. React is mounted through the maintained
Node/miniDOM harness. Instrumented `focus()` and `scrollIntoView()` record the
actual target calls, not visual positioning, OS keyboard or AX behavior.

Both focused suites pass: 38 tests, zero skips, under the normal shared slot
wrapper with fresh scratch Codex home and offline dependencies. The initial
run had 37 passes and a new assertion that used the wrong existing user wording
(“not valid” rather than “draft — not valid for registration”); its assertion
was corrected, with no product-code change. Existing act-wrapping warnings from
older trial-doubt tests remain visible in the full focused log.

Mutation checks in a private source copy confirm that the new transitions fail
when the run-generation guard is removed (two failures), when the draft-name
stale-reveal comparison is removed (one), or when the library comparison is
removed (one). The product checkout was not changed by those checks. Logs and
mutated copies are retained in the named task scratch recorded in the PR.
No broader suite, build or live renderer rerun was needed for these test-only
changes. Independent review and checks of the final PR head are recorded with
that PR; the test counts alone supply no native/end-to-end J1/J2 evidence.

The owner's testing correction assigns development execution to agents. J1
first use/useful real-model work/results finding is the next owned product
result; J2 remains required before release. Native owns the current agent
first-use attempt and exact unavailable capability. Owner testing begins after
Agent 0's publication-ready recommendation, rather than filling our regression
run sheet. This changes neither person-act semantics nor the separate authority
for credentials, model/network choice, signing, existing owner data or execution
holds. Agent 0 owns final integration and any subsequent native evidence join.
