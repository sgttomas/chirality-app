# Pending loop and host-evidence interpretations

Source: [issue 168](https://github.com/sgttomas/chirality-app/issues/168).
The exact candidates below remain unapproved. The two F-12 questions in this
record and DEL-05-02 are separate.

Pending LOOP product/contract reconciliation, excluded from cleanup. Exact candidate texts below are proposals, not accepted changes. Current Work/code/pins remain unchanged; compare governing source, event/record/continuation semantics, selected consumers and fixtures before deciding.

**E-7 — panel delivery versus record membership**

OLD: “An event that cannot be delivered to the panel is still written to the run record”

NEW: “An event belonging in the run record is still written if panel delivery fails”

Consequence: narrows a universal record claim to events belonging in the run record. This may change recording obligations and must be reconciled with delivery-only replay answers and actual record consumers.

**F-12 — delivery-only replay answers**

OLD: “Every event stays in the record (E-7)”

NEW: “Events belonging in the run record stay there (E-7); delivery-only answers are kept for replay (§3.3 RA-4)”

Consequence: explicitly separates delivery-only replay answers from run-record entries. Do not adopt it merely to match an implementation or refresh a historical pin.

**F-5 — model interface failure representation**

OLD: “Model interface failure (termination reason "error"; §4.1 point 2); turn failed”

NEW: “Model interface failure (service or transport error; §4.1 point 2); turn failed”

Consequence: removes an error termination-reason representation not found in the inspected event inventory. Establish the intended model-failure and emitted-record contract before changing this representation.

**F-7 — length/content-filter continuation and completion**

OLD: “Class 1 results go to the model; the turn continues with the next model request, or completes if the response had no calls”

NEW: “Class 1 results go to the model and the turn continues with the next model request; with no calls, content filter fails the turn, and length completes it when no destination request of the turn is pending (§3.2)”

Consequence: distinguishes content-filter failure, length completion and pending destination requests already described elsewhere, but changes failure/continuation expectations. Requires governing-source and consumer/fixture reconciliation; not ordinary prose cleanup.

**TL-1 — local refusal label observation; no replacement proposed**

At app/src-tauri/src/receiving.rs:38, the inspected code locally sets refusal = Some("not exposed on embedded surface".into()) when a catalog entry's exposure.E is not exposed. LOOP TL-1 and its retained clarification reserve host-reported “not exposed on this surface” for a relayed host outcome and distinguish local “not offered”. This is an observed source-label discrepancy requiring product-owner/consumer assessment, not a completed behavioral diagnosis. No code, test expectation or contract label was changed.


Pending DEL-05-01 factual Scope reconciliation, excluded from cleanup; no proposed wording applied:

CLM-001 OLD: “Actual host evidence is a received contribution under DEP-001, whose recorded standing is owner-reported building before agent-action integration; no delivered/adopted handoff or joined witness is established.”

Candidate NEW: “Actual host evidence is a received contribution under DEP-001. The current source-bound receiving account records later host source, fixture evidence and a limited host execution witness; it does not establish actual host conformance to this contract or a joined product witness.”

TBD-003 OLD: “Exact host implementation candidate, adopted catalog/record/checkpoint interfaces, detailed protocol/fixture representation and conformance observations must be supplied or agreed at their actual points of use; no present satisfaction is inferred beyond the recorded owner-reported building standing.”

Candidate NEW: “Exact host implementation candidate, applicable adopted catalog/record/checkpoint interfaces, detailed protocol/fixture representation and conformance observations must be supplied or agreed at their actual points of use. Later source-bound host inputs and limited evidence are identified in DEL-09-06 `Work/SWBPIPE_RECEIVING_BINDING.md`; their receipt does not by itself satisfy host conformance.”

Consequence: replaces a blanket historical building-only summary with later source/fixture/limited execution evidence, while leaving actual host conformance and joined product witness open. The phrase “applicable adopted” may narrow an existing interface obligation; no such narrowing is approved. Verify exact witness subject, accepted source standing and actual selected/historical/recovery bindings before deciding any coherent amendment. Basis reported: DEL-09-06 SWBPIPE_RECEIVING_BINDING.md selects sgttomas/SWBPIPE@9b6281e7eaca924e6166336b87b6d25937c1ca04; catalog-v4/RECEIVING_ADOPTION.md binds host merge, five source identities and read extents. Their receipt is not host conformance. OUT/REQ/AC and YAML conditions unchanged. 
## Decision route

These are pending questions, not approved replacements. One option is to retain
the governing contract and repair or clarify consumers to satisfy it. The other
is a coherent source/consumer amendment, with the applicable owner decision,
acceptance consequences and historical bindings made explicit. Neither a code
match nor a refreshed pin settles the choice.

Recommendation: compare the governing source, selected extents, actual readers
and fixtures before choosing a repair. Next actor: App Agent 0 prepares that
assessment and brings a bounded decision packet with companion changes to the
owner through the coordinator. The owner resolves commitment or
acceptance changes; the relevant implementation owner then carries the selected
repair. Existing Scope, code, pins and evidence are unchanged by this note.
