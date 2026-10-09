# Dormant original-call custody — implementation brief candidate

READ-ONLY candidate; no code/build release inferred. Checkout `/private/tmp/cce-call-custody`, branch codex/app-v4-call-custody, basis `f028d12edcd23c8aaf6a1b67e6efc66a3cfda19b`. Current CCE_CALL_CUSTODY_PROPOSAL.md SHA `caa033bb091308fa77ba9b86ce9351d8eb44771654ac86ea3fb7cb947a944561`; all13 listed source pins match this basis, recorded in `/private/tmp/CCE_CALL_SOURCE_PINS.json`.

Host concurrence `/private/tmp/CCE_CALL_CUSTODY_HOST_CONCURRENCE.md` addresses earlier proposal e6be1045… at378fac…. The current proposal adds exactly its requested bounded-allocation/call caps, classify-before-default-error and reply-cut refinements; that diff was inspected. Source selection is for this dormant test-only exception, not production dynamic-tool registration or a managed service. AA-CAP and current-source S4 positive holds remain independent.

## Four gates

1. **Offer gate:** a cfg(test)-only constructor, exact fixed definition and explicit original fresh thread/start request. Ordinary starts have no dynamicTools; resume/fork have no route into this gate.
2. **Manager-admission gate:** actual complete-written Host SourceRequest, correlated schema-valid start result, successful native thread insertion and successful insertion of the same original HELP_HUMAN/WORKING_ITEMS RoleBinding. Only then issue the private handoff. activeAdmission/start_admitted, generic bind and caller Values are not credentials.
3. **Original-call gate:** genuine current server-request classification, active matching offer/manager continuity, exact tool and bounded valid arguments; then the actual RequestRegister admission issues one private non-deserializable handle. No reconstructed receipt/frame selects a call.
4. **Reply gate:** prepare the exact original unsettled request and recheck source/pipe, offer/manager continuity, original call identity and supplier resolution at the final frame_write→source gate→Inner cut. Release source locks before IO. Facts arriving after that cut cannot unsend admitted bytes. Record actual local write result; no retry, TASK/session creation or delivery inference.

Independent review of this exact brief precedes code. Exact frozen code review precedes process-free execution if required by the parent. No compiler/test run while Group C owns the first shared build window; use the manager's existing offline cache/target only after coordination.

## Proposed source fence

* hosting.rs: private pending offer/start pin, received-call slot/handle hook, closure/replacement invalidation and original reply cut; module inclusion under hosting, not lib.rs.
* native_requests.rs: private provenance-aware classification/settlement exception and borrowed original-entry lookup. Ordinary receive/prepare paths retain their current behavior and bytes.
* New hosting_call_custody.rs and hosting_call_custody_tests.rs: definition, bounded validation/state/handles and in-process synthetic tests.
* runtime_session.rs: HistorySession original-start reconciliation success-insertion branch and one optional continuity owner only. No role/workflow initiation, commands or C3 changes.
* role_lifecycle.rs: narrow private original-manager-insertion handoff check/accessor. Existing generic binding/observe APIs do not mint it; no RoleSourceLease.
* New resources/distribution-successor/CCE_CALL_CUSTODY_CORE.md: provisional limits/meaning and test classification.

No lib.rs, role_supply.rs, Cargo/dependency, canonical Design/schema, AA-CAP module, B pins, held first-summary/Route B, Stop/child/probe/quit, managed records, filesystem resolver or public UI/command edit. If the source chain cannot be implemented inside these seven paths without reverse locks, return the exact contradiction before expanding.

## Offer and successful-insertion handoff

Use the exact function definition/inputSchema and unavailable content from the selected proposal. Construct the definition before Host registration; attach it only through a private explicit pending-offer parameter on the selected fresh thread/start. Bind exact sent definition digest, common/role/combined guidance identities, original requestRef/ID/frame, Host instance and full H5. No shared next-start flag and no capabilities JSON switch. Test-only activation is unavailable in normal builds, including feature-enabled builds.

HistorySession::reconcile currently calls PreparedStart.observe, then Host.thread_start_dispatch_finish, sets activeAdmission, and only then attempts self.roles.insert(binding). Preserve ordinary behavior; create no offer credential from activeAdmission. For an opted-in start, obtain an opaque Host original-start pin from the same successful finish path, reusing its actual write/result/native insertion checks. It is not returned from JSON or from a generic binding API. After roles.insert succeeds, retrieve the exact inserted binding and verify original Start origin, manager role, request/generation/thread/supply/common-role identity against that Host pin. Failed insertion produces no handoff. Do not repair the separate activeAdmission-reporting issue in this slice.

The successful insertion owns one private continuity cell in HistorySession; Host gets only a private pin referencing that cell. Owner drop/replacement explicitly invalidates the cell atomically even if another temporary reference exists. Historical imported/generic binding, resume/fork and PreparedStart.observe alone cannot issue it. Existing role bindings are immutable after insertion; any future invalidation path must retire the cell. Generation closure also invalidates Host offer use regardless of role-history retention.

Handoff construction occurs outside Host Inner. HistorySession's existing owner→Host direction may call the narrow Host adoption method after successful insertion; Host never calls back into role/session/EXEC/C3 or acquires their locks. The receive/reply hook reads immutable pin metadata and its atomic alive flag only. Final eligibility's atomic read is the role-continuity cut: earlier invalidation refuses; later invalidation is post-cut, not an ability to unsend. No role owner lock is acquired under Inner.

## Frozen candidate development caps

These are test-only candidate capacities, not accepted provider/C3 project limits. Reject without truncation; never allocate from byteLength or an incoming count.

| Dimension | Proposed ceiling |
|---|---|
| Pending/active offers |1 per Host generation; terminal/ineligible offer cannot be silently replaced in that generation |
| Admitted calls |1 total per offer, including settled call; retain its fixed identity tombstone for duplicate/conflict detection; no queue/replenishment |
| Whole incoming parsed call serialization |32768 bytes |
| arguments serialization |16384 bytes |
| Parsed containers/nodes/width |depth8;512 total values plus object keys;64 members/elements per container |
| Any string / object key |8192 /256 UTF-8 bytes, with tighter fields below |
| H5 strings, thread/turn/call ID, RPC string ID, original request/supply refs, base.id, question ID, claim ID |256 UTF-8 bytes each; RPC ID is original string or integer, not coerced |
| base.path |4096 UTF-8 bytes, nonempty; opaque selector, not resolved/accepted path |
| claimIds |0–32 unique exact strings; empty valid; no synthetic default claims |
| base.sha256 |exact64 lowercase ASCII hex bytes, no LF/whitespace |
| base.byteLength |mathematical integer0…9007199254740991; finite integral JSON float representations accepted within that exactly representable development range |
| Offered start/definition serialization |65536 /4096 bytes; limit before offered dispatch; ordinary non-offered construction unchanged |
| Added core retained / validation scratch / incremental core workspace |16384 /65536 /131072 bytes |
| Fixed response frame |2048 serialized bytes including bounded original RPC ID |

The retained handle stores bounded identity fields, frame/argument/definition digests and private slot identity. Original parsed payload/receipt remains in existing Host journal and RequestRegister; do not clone another request/argument tree into the core. There is no journal search to reconstruct a capability. Digest identity uses the existing named PF1 method without modifying AA-CAP; preflight the tighter limits first. A bounded counting serializer may check the tighter byte ceilings before PF1's bounded hash pass; no whole-frame to_vec/string for validation. Two bounded passes are explicit, not an unbounded cache.

New argument validation implements the entire selected fixed closed inputSchema: required/exact keys at arguments and base; types; nonempty selectors; exact hex; integer range; unique claim IDs. Compare at most32² pairs of bounded IDs, no untrusted-size sets/vectors. DynamicToolCallParams requires its generated required fields/types and tool identity; namespace must be absent/null because no namespace is offered. Unknown extra native envelope/params fields are retained and hashed within caps, not treated as authority. No filesystem resolution or acceptance of base/question/claims occurs.

Do not build a generic jsonschema validator in the new receive/reply hook. Existing full thread/start validation still runs through PreparedStart.observe and Host.thread_start_dispatch_finish, outside Inner at their existing locations. Do not add another full-schema invocation: normal successful start already validates params/response in role observation and response in Host finish. Their existing full generated-schema compilation/caches and SourceRequest/journal copies are **not** bounded by the new core-workspace claim; record them separately rather than citing existing transport as a memory guarantee. Measure new retained capacities and core allocation/scratch; stop if these proposed limits cannot be demonstrated.

New validation work per accepted call: one bounded shape/schema/digest admission, at most one bounded original-argument identity recheck at preparation and one at final cut. No revalidation loop/history scan, accumulating errors or automatic retry. Once the single call slot is spent, further calls get a bounded explicit capacity refusal while ordinary custody still records them; they do not allocate another core slot. Existing ordinary Host history remains outside this fixed new storage bound.

## Classification, original handle and fixed settlement

At Host.on_line's genuine admitted server-request branch, before native_requests.receive selects its default item/tool/call unsupported error, pass a private offer provenance token to a narrow register method. No offer uses the unchanged receive method/default bytes. The token cannot be constructed from capabilities/role/argument JSON. Require full Host/H5/home/thread, live manager pin, exact tool, valid scalar RPC identity, callId/turnId and bounded argument validation. Duplicate RPC identity follows existing duplicate-request refusal; repeated callId under another RPC cannot mint a second handle.

Valid offered call registers as known-answerable with private offered provenance and one outstanding original request. Handle binds Host, H5, offer/start identity, thread/turn/callId/RPC identity, original receipt and exact parsed tool/arguments. It is non-Clone/non-Serde and cannot be replaced by a client SourceRequest or AA-CAP status. Public entries()/journal() copies cannot manufacture it. Prepare/reply checks the slot identity plus original register entry, not an index alone.

Use a private prepare_offered_unavailable method gated by that handle, not a broadened generic person/named-service origin or new capabilities flag. Exact result is:

`{"success":false,"contentItems":[{"type":"inputText","text":"managed-service-unavailable: no TASK session was created"}]}`

Record fixed app-rule:managed-service-unavailable origin. A local written result may use existing answered standing to mean a response body was written; it does not mean tool success or delivery. The response's success remains false, acknowledgment remains not-observed unless the existing actual resolution mechanism supplies its own later fact. No person-decline claim is invented. Source owners must confirm this projection in brief review.

Malformed/additional/overlimit arguments: fixed invalid-params RPC error(-32602), no handle. Wrong/unoffered tool or unsupported namespace: existing unsupported response or scoped fixed refusal(-32601), no handle. Capacity exhausted: bounded explicit refusal, no new core call. Never echo arbitrary argument text in errors. Closed/superseded/duplicate/resolved originals produce no new reply or retarget. All ordinary server-request records, mandatory error replies, journaling and notifications continue.

## Reply and race table

The current reply_eligible clones all entries and scans journal. Do not use that clone to claim bounded new validation. Add a private borrowed lookup of the exact offered original entry and bounded resolution state; preserve ordinary reply_eligible unchanged. Observe existing serverRequest/resolved through the same existing scope rules into the one call slot before reply eligibility. RequestRegister remains the primary lifecycle authority, not an independent contradictory core state.

| Point | Required result |
|---|---|
| Before offer activation / failed/partial/mismatched start / insertion failure | Ordinary unsupported call handling; no active offer or original-call handle |
| Resolution/closure before reply preparation | Refuse preparing new reply; retain original evidence |
| Resolution/closure while waiting for frame_write | Recheck after acquiring it; no bytes if original is no longer eligible |
| Final cut | frame_write→source gate→Inner; check original pipe/generation, register unsettled state, matching handle/offer/payload, manager alive flag and observed resolution; set one in-flight marker |
| After cut/during actual IO | Release source locks; bytes may already be in flight. No unsend promise or retroactive no-attempt label |
| Successful local write with later resolution/closure | Retain actual written fact and ordering; no delivered/acknowledged claim, no successor settlement; preserve the existing supplier-resolution fact |
| Error/reported partial write | Unknown delivery; mark this attempt final, never retry; no TASK/session record |
| Copied handle/JSON, wrong Host/H5/thread/turn/call/payload | Refuse; no replacement source or new reply |

No ROLE/EXEC/C3 callback, mutex acquisition or filesystem IO under the receive/reply Inner section. Only immutable handoff data and atomic continuity check. Post-cut result/role invalidation is not converted into pre-cut cancellation. If existing RequestRegister written/resolved mechanics cannot retain both actual local-write and resolution order without changing accepted record meaning, return that exact boundary before code rather than invent a schema field.

## Process-free first proof and controls

Use actual Host thread/start dispatch over an anonymous CLOEXEC pipe, not Host.start. Synthetic ready Host has no Child. Compose small synthetic common/manager guidance through existing role_supply builders, use actual PreparedStart/Host finish and successful RoleBindings insertion, and assert the private handoff is issued only on that path. No role string or manufactured role binding substitutes for insertion. Synthetic response/notification frames are explicitly labelled, not supplier observations.

Small positive outgoing start/reply frames≤2048 bytes are drained from a retained anonymous-pipe reader with1000ms/4096-byte acquisition bounds; writer nonblocking prevents fixture deadlock. Compare exact actual start bytes including the sole fixed dynamicTools definition. Incoming call then produces exactly one unavailable response through actual write_complete. Test-only scheduling hooks outside source/Inner inject resolution before prepare, while queued for frame_write, before eligibility and after eligibility/before settlement. No reentrant automatic-reply request is injected while holding frame_write. Failed/partial writes are explicitly simulated, never produced by closing a reader/SIGPIPE. RAII closes only these descriptors; no process/signal/wait/reap, TASK launch or records.

Required negatives: ordinary no-offer start/tool call byte preservation; manager vs TASK/generic/history/resume/fork; successful native admission but failed role insertion; original source substitution/partial write/wrong result; malformed/additional args and exact digest LF; zero and32 claim selection, each cap/one-over including integer forms; duplicate call/RPC identity; retired manager pin/drop; closed/new generation; copied handle and changed arguments; all reply-cut schedules/no double reply; ordinary automatic errors and full journal retained. Allocation measurements cover new bounded core separately from existing full-start validation; no native-schema shortcut is introduced for original manager admission.

## Capacity and return gate

Approximately3.2GiB free was reported. No build now. After independent brief/code gates and manager's build-window coordination, use the existing compatible offline CARGO_HOME and `/private/tmp/hosting-s2-target`, serial filtered call-custody tests, CARGO_INCREMENTAL=0 and skip supplier. No downloads, duplicate target or deletion of other work/evidence; actual capacity failure is reported, not a proof waiver. Group C gets its first build window.

Return exact frozen source, all actual-vs-simulated results and original failures for independent review before commit. No S4 requalification from the earlier note, no current B positive repin/export, RoleSourceLease, managed service or public activation. This brief is the concrete pre-code review package, not a claim the seven-file implementation is ready.

## Exact post-cut settlement boundary — code release blocked pending owning concurrence

Current `native_requests.rs:406` written() returns immediately unless the original entry is still `settling`. Its resolved() can change that state to `resolved-by-supplier` while reply IO is in flight. Thus Host.write_reply can observe an actual successful local write while the canonical register still reports not-attempted. This is the precise branch that prevents treating existing generic write_reply as a complete implementation of gate4. Do not change generic written(), resolution or ordinary request behavior to fix it in this tranche.

Proposed offered-only treatment: a private reply-attempt slot is reserved at the final eligibility cut and keeps original call capability, cut receipt position, in-flight flag and one terminal local-write outcome. The same original-call slot separately retains actual matching resolution receipt/order. Both components are fixed-cardinality and source-bound. Completion stores Written or WriteFailed/UnknownDelivery once even if resolution or closure was observed after the cut; it never revives the request, retries, retargets, creates acknowledgment or claims delivery. Resolution before the cut still prevents the attempt entirely. Caller-visible test metadata distinguishes no attempt from admitted/in-flight/completed local attempt.

A private offered settlement adapter may use existing written() only while the exact entry remains settling. If it has become supplier-resolved or closed after the cut, leave that primary resolution/closure standing and original fields intact, and expose the later local write only in the explicitly separate private offered-attempt projection. That projection must name the canonical register as incomplete for this combined observation; it must not present its historical not-attempted field as the current effective write outcome. No extra fields enter the closed ordinary record schema. Existing full journal and native resolution payload remain unchanged; the private projection joins them by the original capability, never reconstructs authority from them.

This is a proposed source-owned test-only representation, not a resolved semantic choice. Host/native-request/EXEC owners and independent reviewer must concur that retaining canonical historical state plus this separate exact offered-attempt observation satisfies the selected proposal's evidence duty. If they require canonical record alteration instead, return that specific contract/schema treatment before implementation. Do not silently map the source back to answered/settling, infer acknowledgment, or call the whole ordinary record corrected. Until this narrow offered-only treatment is reviewed, the brief is a precise blocked pre-code return, not READY for implementation.
