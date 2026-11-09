# Two usable journeys required before 4.0.0

## Current product/UI priority

The owner reports that the App is still a skeleton with substantial UI work
remaining. Functional J1/J2/P3 development observations establish their actual
subjects; they do not establish publication usability or owner acceptance.
Product/UI work takes priority; final packaging/signing readiness is parked.
The v3 overall visual form remains the reference, without importing v3 tools.

The current increment puts the conversation composer and Send before optional
model/effort and long role/fork explanations. Connection has one primary
ChatGPT sign-in action and a separate oMLX/local alternative; advanced sign-in
and exact source/response diagnostics remain available in disclosures. Run's
project context distinguishes a known project with an unavailable readable
folder from a missing project, and never substitutes the workflow library's
path. Named task steps and turn regions improve accessible structure; raw
command details, output and reasoning are optional while messages, statuses,
requests and failures remain readable.

The active access scope is account plus oMLX/local. Standalone OpenAI API-key
mode and its qualification commitment are omitted by owner direction; local
bearer credentials remain required. Keyed oMLX is received through the
adopted Codex-custody dedicated local home: the person prepares it, enters the
key in a native secure field and switches between account and local homes
(DEL-01-05 current account/oMLX increment). That glue integrates only after the
native local-home commands. A bounded keyed response and read-only command
passed on the [identified development subject](../../../PKG-01/DEL-01-05/Work/LOCAL_PROVIDER_CUSTODY.md#current-native-observation);
broader oMLX compatibility remains open. The supplier lane owns the selected 0.167.0 advance;
this UI increment adds no generated protocol or native credential behavior.

The retained source-rendered visual checkpoint uses actual components, the
existing v3-derived palette/IBM Plex assets and invented data:
`/Users/ryan/dev/chirality-t3/scratch/app-ui-product-focus-33e4bppo/visual/`.
`VISUAL_CHECKPOINT.json` identifies the actual PNG/HTML outputs, including
`conversation-final.png` and `connection-revised.png`. These are browser
source-design observations, not AppKit/WebKit interaction, model use, native AX
qualification or visual/usability acceptance. Current Work holds the product
meaning; check/review execution belongs in the implementation PR.

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

The initial standing was **J1 open; J2 open**. Later evidence and its limits
are recorded below; signing, notarization, layout fixtures, test counts and
merged PRs alone do not demonstrate a journey. Implementation returns reconcile
the owning Work account and dependency meaning and supply candidate results to
DEL-09-02. The [publication punchlist](../../../_Coordination/PUBLICATION_PUNCHLIST.md)
indexes this result; it is not another requirements source.

## Mounted transition coverage (2026-11-05)

Subject: integrated App main `0f6d8388420b5ba2bb513bb9f30fb80b65088e21`
plus additive tests in `run-journey.test.mjs` and `make-journey.test.mjs`.
Product `RunJourney.tsx` and `MakeJourney.tsx` bytes were unchanged.

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

The two focused suites covered these transitions in the Node/miniDOM harness.
Mutation checks found failures when the run-generation guard, draft-name
stale-reveal comparison or library comparison was removed. The checks provide
no native or end-to-end J1/J2 evidence; earlier trial-doubt tests emitted
act-wrapping warnings.

The owner's testing correction assigns development execution to agents. Owner
testing begins after Agent 0's publication-ready recommendation. Person-act
semantics and separate authority for credentials, model/network choice, signing,
existing owner data and execution holds remain unchanged.

## Current real-model result — 2026-11-08

The [native actual account](../../../PKG-09/DEL-09-02/Work/J1_REAL_MODEL_ACTUAL_20261108.md)
records project setup, owner sign-in, included-workflow selection, useful
GPT-6.1 Terra/medium execution, a saved take-off independently matching the
checking key, results found in the conversation and the ended run in Results,
and normal Quit. The raw CSV is unchanged. This demonstrates J1's core path
on the identified development subject; it is not owner acceptance or installed
qualification. The owner's sign-in-status usability finding remains open with
the product owner. J2 remains open, and no second model campaign is authorized
by this one-workflow result. ScopeOfWork and dependency conditions retain their
meaning.

The later [0.167 account workflow segment](../../../PKG-09/DEL-09-02/Work/P3_NEXT_WITNESS_PROPOSAL.md#current-account-workflow-segment)
on development source `02506cce` exercised the revised Run guide, one native
write approval, a checked saved review and the ended run in Results, followed
by normal Quit. It preserves the earlier observations and their separate
subjects; it is neither owner usability acceptance nor installed qualification.


## Ordinary effort interaction

The J1 effort-chooser finding has a focused source repair in
[the access account](../../../PKG-01/DEL-01-05/Work/ACCOUNT_AND_PROVIDER_ACCESS.md#offered-per-model-effort-for-ordinary-text).
It offers the selected model's reported effort choices for ordinary text,
including plan/default and a pending run-end notice, without private config
editing. This supplies no new journey observation or qualification and changes
no registration/trial rule or dependency condition. The retained J1/J2 actual
accounts keep their original artifacts and operator attribution.
