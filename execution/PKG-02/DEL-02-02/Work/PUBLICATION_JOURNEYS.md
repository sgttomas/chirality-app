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
