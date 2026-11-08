# Pending loop and host-evidence decisions

These are recommendations for the owner, not adopted replacements. Source:
[issue 168](https://github.com/sgttomas/chirality-app/issues/168). This packet
also includes the coupled [ACT](../../../PKG-04/DEL-04-01/Work/PENDING_INTERPRETATIONS.md)
and [record-store/citation](../../../PKG-04/DEL-04-03/Work/PENDING_INTERPRETATIONS.md)
choices. LOOP F-12 here is distinct from PANEL F-12 in DEL-05-02.

## Basis and recommendation

The assessment uses App `88708dcf6f1463380aef702d870403928fd370bf` and the
current governing PRD, owning Scopes, dependency conditions and linked Work
at that revision. Contributor instructions use verified `library-v3.3.0`,
`ec3ee2d1b398eba1fb3227ccf93e2569df95bacd`, from the isolated export; that
selection adopts no product instruction or contract changes. Product and
historical source bindings remain separate.

Recommend resolving the contradictory LOOP summaries in favor of their
explicit event, replay and turn-state rules, with the companion amendments
below. E-7/F-12 narrow universal recording language; F-7 selects failure and
continuation behavior, including one missing pending-request transition.
Those consequences require an owner decision. F-5's error representation and
the host-evidence summary can be corrected without removing an obligation.
Keep TL-1's host/local reporter distinction and repair its local consumer after
the offering question below is settled for the affected input.

No OUT, REQ, AC, dependency condition, historical pin or implementation is
changed by this packet. The alternative throughout is to retain the broad
contract and repair its detailed consumers; that entails the concrete work
described below, rather than declaring the current code authoritative.

## E-7 and F-12: which events belong in the run record?

[LOOP](LOOP_RECEIVING_CONTRACT.md) §2.3 explicitly excludes **Return input
answered** from run-record membership. E-6 keeps delivery ordinals in operational
conversation state, not RS `seq`; §3.3 RA-4 keeps answers for replay and records
what an input led to. §3.4 likewise makes replay delivery, without recording a
replayed event again. Thus the detailed contract already distinguishes event
delivery from durable evidence. This is stronger grounding than a code match.

| Location | Before | Recommended candidate |
|---|---|---|
| E-7, first sentence | “An event that cannot be delivered to the panel is still written to the run record, and the failure changes nothing in the run.” | “An event belonging in the run record is still written there if panel delivery fails; delivery-only answers remain available for replay under §3.3 RA-4 and §3.4. Panel delivery failure changes nothing in the run.” |
| F-12, Record left | “Every event stays in the record (E-7)” | “Events belonging in the run record stay there (E-7); delivery-only answers are kept for replay (§3.3 RA-4).” |

Keep E-7's remaining sentences, F-12's gap/replay behavior, RA-4 and RS record
membership unchanged. This excludes delivery-only answers from the universal
recording claim; it does **not** remove any defined run, destination, checkpoint
or human-act entry. Replay retention remains the host owner's open OI-013
choice; “available” is subject to §3.4's explicit *events not held* answer.

Alternative: require every delivery event to be durable. That needs companion
changes to §2.3, E-6, RA-4, §3.4, RS kinds/reader and PANEL return/replay handling,
including non-run refusals and replay deduplication. It adds storage meaning;
merely reverting RA-4 or refreshing a pin would not implement it.

Consumer consequence: [PANEL](../../DEL-05-02/Work/PANEL_RECEIVING_CONTRACT.md)
§3.9/FD-3 must continue distinguishing an answer from its result and from a
person's act. Its scripted events and the local receiving projection do not
prove durable membership or actual host replay. A later host witness must
compare a record-bearing result and a delivery-only answer across a panel gap,
including an explicit retention gap, without inventing a human answer.

## F-5 and F-7: model failure and continuation

LOOP §4.1 point 2's **FB-CC-1 fixture basis** has no error finish-reason value;
§2.3 says an error is transport/service failure or an absent termination reason.
§3.2 already fails a no-call content-filter response, completes no-call length
only with no pending destination request, and sends rejected calls' class 1
results back for another request. None selects an actual host model interface.

| Location | Before | Recommended candidate |
|---|---|---|
| F-5, Record left | “Model interface failure (termination reason "error"; §4.1 point 2); turn failed” | “Model interface failure (service or transport error; §4.1 point 2); turn failed” |
| §2.3, Model interface failure, Evidence | Starts “Termination reason.” | Replace that opening with “Failure kind and available model-server or transport evidence.” Keep the following explanation that FB-CC-1 has no error termination-reason value. |
| §4 capability row | “Termination reason that distinguishes complete, length-truncated and error” | “Termination information that distinguishes complete, length-truncated and content-filtered responses, and separate service/transport or missing-reason failure evidence” |
| F-7, What happens next | “Class 1 results go to the model; the turn continues with the next model request, or completes if the response had no calls” | “With calls, class 1 results go to the model and the turn continues with the next model request. With no calls, content filter fails the turn; length completes it only when no destination request of the turn is pending, otherwise it awaits the destination answer (§3.2).” |
| §3.2, streaming → awaiting destination answer | “Termination *stop* with no tool calls while a destination request of this turn is pending” | “Termination *stop* or *length* with no tool calls while a destination request of this turn is pending” |
| Same transition, Record | “The turn does not complete (DF-5 Q-5)” | “Agent message complete (stop) or truncated (length); the turn does not complete (DF-5 Q-5).” |

F-6 still owns mid-stream failure or a stream ending without a reason; no calls
of that response dispatch. Keep MC-1/MC-11 rejection, correlation identities and
the existing post-answer deferred-result path. The pending-length transition
is a substantive completion of the table, not an already observed outcome.

There is a second coupled gap: DF-5 Q-9/DF-6 close a pending destination
request on run end or person cancellation, but not on a failed turn (including
no-call content filter). Keeping it pending after a terminal failure would
leave an actionable prompt and no truthful same-turn result path. Recommend
the following **substantive companion**, rather than relabelling failure as a
person's cancellation:

- In Q-9, replace “the run ends, or the person cancels the turn (F-11),
  while the request is pending” with “the run ends, the person cancels the
  turn (F-11), or the turn fails, while the request is pending”. Keep no
  grant, no carried-call dispatch and no later result in that turn.
- In DF-6, replace “cause: run ended · turn cancelled” with “cause: run
  ended · turn cancelled · turn failed”. In §3.2's failed-turn rules add:
  “Every still-pending destination request of the failed turn ends
  unanswered at end, cause turn failed; its carried call is not dispatched
  and its prompt offers no further choices.” Add the corresponding DF
  failure row: “Turn fails while request pending | Loop | destination_request_closed
  (unanswered at end, turn failed) | No grant, no carried-call dispatch,
  no deferred outcome in a later turn”. Preserve separately observed
  outcomes of calls already dispatched; missing outcomes stay unknown.
- In `LOOP_DESTINATION_REQUEST.schema.json`, add `turn failed` to
  `properties.endCause.enum`; in RS `RS_RECORD.schema.json`, add it to
  `$defs.destinationRequestClosed.properties.cause.enum`; in AS
  `AS_SETTINGS_IN.schema.json`, add it to the destination request
  `stateReason` enum. Keep the existing state names and all unrelated
  validation/attribution constraints. RS's R15/entry description must carry
  the same cause without asserting that a human cancelled or declined.
- Add AS §3.1's requested → no-grant transition: “The turn fails while the
  request is pending | no grant | Gone; carried call not sent | request
  unanswered at end, cause turn failed; RS destination_request_closed”.
  PANEL ND-2/FD-4 must consume that terminal report as “Not answered — turn
  failed”, with no choices or grant. For F-5, PANEL FD-1 must replace its
  demand for a failure's termination reason with “failure kind, available
  termination/service/transport evidence and reporter”; never invent an
  error finish reason.

This companion changes actual request-close vocabulary and consumers; it is
not part of the separate citation-only correction. Later implementation needs
targeted terminal-failure/pending-request regressions and independent scrutiny
of persistence and permission boundaries. A fixture expectation cannot adopt
it. Alternative: retain the existing close causes and require an explicit
run end to retire such a prompt; that needs a specified failed-turn prompt and
late-answer policy before use, and must not fabricate a person stop. The
recommended automatic terminal closure avoids leaving a grantable orphan.

Alternative: keep F-7's no-call completion for both reasons. That requires
changing §3.2's content-filter failure and pending-request rule, plus deciding
what happens to the waiting carried call. Recommendation rejects that loss of
the explicit pending request and failure distinction.

[Stream assembly](../../../../app/contract_inputs/PKG-05/DEL-05-01/Work/prototype/assemble_tool_calls.py)
and its 22 fixtures cover call assembly/rejection, including MC-1/2/11;
[destination flow](../../../../app/contract_inputs/PKG-05/DEL-05-01/Work/prototype/destination_flow.py)
uses scripted native/control inputs. Neither establishes all no-call turn
transitions, replay persistence or an actual host service error. The Rust
[receiving projection](../../../../app/src-tauri/src/receiving.rs) refuses
truncated/filtered/interrupted calls but implements no model turn loop. Later
conformance work must cover pre-stream error, mid-stream loss, no-call
filter/length, pending-length, pending-request failure closure and rejected-call continuation at its actual
host/interface basis. Existing passes keep their bounded subjects.

## TL-1: keep local and host outcomes distinguishable

LOOP TL-1/V-2 and CATALOG §4.1 reserve **not exposed on this surface** for a
host-returned outcome, relayed with the host named as reporter; an absent
offered entry is locally **not offered**. `receive_calls` locally sets
`not exposed on embedded surface` for a supplied entry whose `exposure.E` is
anything other than `exposed`, conflating `not exposed` and `unagreed`.

Candidate label repair: replace that local string with **“not offered on
embedded surface”**, retaining its local provenance and never calling it a host
response. This changes no dispatch/readiness decision. However, TL-1 also says
the loop never withholds a supplied entry on its own reading of exposure.
`receive_calls` receives a catalog, not an independently evidenced CI-5 offered
set; the inspected positive fixture has exposed entries and the receiving
tests do not settle this case. A string change alone cannot prove offering
conformance.

Recommend keeping the contract and preparing a bounded consumer repair: make
the actual host-supplied offered edition/set explicit before assigning local
*not offered*; keep host-returned *not exposed* as a separate relayed outcome.
If the current input is established to be the host's already filtered offered
set, the exposure-based rejection itself needs review under TL-1, rather than
being justified by its new label. Cover absent, explicitly excluded, unagreed
and reserved entries and a genuine host refusal; do not broaden dispatch as a
side effect of a label fix. The scope has been reported to App Agent 0; no
implementation repair is included here. Alternative: authorize local exposure
filtering and amend TL-1/CATALOG with explicit treatment of unagreed values;
that changes the offering contract and is not recommended merely to match code.

## Host-evidence CLM-001 / TBD-003: update facts, retain obligations

The [receiving binding](../../../PKG-09/DEL-09-06/Work/SWBPIPE_RECEIVING_BINDING.md)
separates current catalog-v4 selection, older v3/v2 sources, fixture admission,
limited host execution and activation/recovery limits. The
[v4 adoption](../../../PKG-09/DEL-09-06/Work/catalog-v4/RECEIVING_ADOPTION.md)
selects `sgttomas/SWBPIPE@9b6281e7eaca924e6166336b87b6d25937c1ca04` and five
source identities/read extents. It establishes offline receiving, not a live
Apply or criterion 17. The separate received historical local witness at
`sgttomas/chirality@3a4fa55369be67940b4d1de707b2bad8159dc0bd` reports one
summary call/follow-up on its recorded stock Codex/oMLX/model subject. It is not
an execution of the current catalog-v4 product. Later fixture admission and
cleanup accounts do not fill absent native cleanup acknowledgments.

Recommended exact replacements in [Scope](../ScopeOfWork.md), leaving their
other text and all OUT/REQ/AC/YAML conditions intact:

- CLM-001, replace “Actual host evidence is a received contribution under
  DEP-001, whose recorded standing is owner-reported building before
  agent-action integration; no delivered/adopted handoff or joined witness is
  established.” with “Actual host evidence is a received contribution under
  DEP-001. DEL-09-06 Work/SWBPIPE_RECEIVING_BINDING.md identifies the current
  source-bound receiving selection, separately received fixture evidence and
  a limited historical host execution witness with their actual subjects and
  limits. Their receipt does not establish actual host conformance to this
  contract or a joined product witness.”
- TBD-003, replace the sentence beginning “Exact host implementation
  candidate” with “Exact host implementation candidate, adopted
  catalog/record/checkpoint interfaces, detailed protocol/fixture
  representation and conformance observations must be supplied or agreed at
  their actual points of use. Later source-bound host inputs and limited
  evidence are identified in DEL-09-06 Work/SWBPIPE_RECEIVING_BINDING.md;
  their receipt does not by itself satisfy host conformance.”

Do **not** insert the earlier proposal's “applicable adopted” qualifier. It
could narrow the interface obligation. Keeping the old building-only sentence
would leave a false current summary; revising it grants no host acceptance.

## Effect on planned evidence and decision route

| Evidence | Consequence of the recommendations |
|---|---|
| P2 / J2 | The approved one-registration/one-fresh-reuse scope stays independent, twenty minutes, stop-only/no retries, preserving the current project and old-046 store. The coupled ACT/store observation is specified in the linked packet. This documentation changes neither source `475c9b8f9c868fe1be9d0e1ef33a9cdd72aec75f` nor its executable; no rebuild or repeat of its earlier trial/recovery follows. |
| P3 | Preserve App Codex versus host Chat Completions boundaries. Later applicable failure/interruption evidence must report the actual path and selected semantics; call fixtures cannot stand in for no-call state transitions, cancellation or recovery. |
| P5 | Before a joined-host failure/replay claim, decide E-7/F-12/F-7, receive the exact host/interface basis and test corresponding record, pending-request and reporter behavior. The factual Scope correction supplies no joined witness, native enforcement or acceptance. |

Next actor: App Agent 0 brings the coupled recommendations and alternatives to
the owner. After the decision, the responsible contract/implementation owners
reconcile the selected live consumers, copies and dependency meanings in one
reviewed change, preserving historical identities and unrun obligations.
App Agent 0 owns final integration and the publication recommendation.
