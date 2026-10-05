# I1 actual Host history/start receipt bridge — 2026-10-05

TASK `/root/group_a_execution/runtime_core_production`, parent `/root/group_a_execution`; native descendant, no delegation. Parent released Host source/Cargo after its separately owned backend smoke. Author owns hosting.rs bridge/inline tests and this record only; shared lib/App/runtime_session wiring belongs to history_product_join. Frozen native_history/role_lifecycle, Design, schemas/dependencies and Git untouched. No native supplier/model/auth/credential/network/download/key execution. Actual mock writes use env-cleared /bin/cat, reaped after each exchange. Parent live evidence and its source pins remain historical, not rebound to this successor.

## Frozen API

SourceRequest and HistoryDispatch are Clone, private-backed and not deserializable. SourceRequest exposes generation()->&Value, request_id()->&Value, request_ref()->&str, attempted_frame()->&Value and evidence()->Value. HistoryDispatch exposes query()->&HistoryQuery, source()->&SourceRequest and evidence()->Value. No returned JSON can be imported as either capability. Weak source ownership avoids retaining the Host through a receipt cycle; different Host instances reject each other's receipts even when their tuples/IDs are identical.

```rust
Host::history_dispatch(&HistoryQuery) -> Result<HistoryDispatch,String>
Host::history_wait(&HistoryDispatch,Duration) -> Result<Value,String>
Host::history_dispatch_status(&HistoryDispatch) -> Result<Value,String>
Host::history_admit_resume(&NativeHistory,&HistoryDispatch) -> Result<Value,String>
Host::thread_start_with_guidance_dispatch(&Value,cwd:&str,model:&str,
    model_provider:&str,guidance:&str) -> Result<SourceRequest,String>
Host::source_request_wait(&SourceRequest,Duration) -> Result<Value,String>
Host::source_request_status(&SourceRequest) -> Result<Value,String>
Host::source_request(&Value generation,&Value actual_rpc_id) -> Result<SourceRequest,String>
Host::thread_start_dispatch_finish(&SourceRequest) -> Result<Value,String>
```

Evidence keys: generation,home,requestIdentity (actual supplier RPC ID),requestRef,attemptedFrame,sentFrame,writeResult,outcome,waitingEnded,response,writeError,sourceCurrent. sentFrame is null until actual pipe write returns success; a concurrently visible attempt reports write-in-progress. Failed write preserves attemptedFrame with write-failed/unknown-no-response. Pending wait expiry sets waitingEnded and retains pending outcome/correlation; status sees later source-bound result/error without resending. Registered write failure/native error/wait return a receipt/evidence, whereas pre-registration refusal returns Err. The source receipt account is private ephemeral memory alongside the unchanged native journal, not a new public client-record schema, transcript cache or durable receipt store.

The existing sender is split into shared begin/wait helpers. Full generation checked with ready/open state before registration; actual source pipe acquired while registration is locked, retained through write with state lock released for reader progress, then released before state lock reacquisition. Existing synchronous request/start/text/steer/interrupt signatures and behavior are preserved, including handshake state, old native errors, wait strings, raw correlation, generation-race guards and independent terminal lifecycle. Start native body uses the same selected model/provider/cwd helper and exact additive developerInstructions only. No base/config/role/policy/approval/sandbox override, actor authority or resource/root setting veto was added.

## History admission

Typed query factories retain exact method/params/home/full tuple; only their published list/read/turns/items/goal/resume packets dispatch. Local HistoryQuery.id remains local; tests set supplier allocation to41 while local query ID differs. Receipt retains the exact full private query, not a guessed pointer or reconstructed sent frame.

History receiving still validates complete pinned0.160 native results. Operational insertion is separate: only original ID-only explicit Continue query, matching latest thread-state resolution/full factory query, current resumed_thread candidate and successful actual write/correlated native response qualify. Under Host lock it rechecks current ready/open/full tuple, home, native thread ID/status/direct-input and refuses duplicate admission. A read result, notLoaded/direct-input false, newer pending query, foreign/malformed/error result, closed/replaced tuple or failed-write fabricated receiving candidate cannot register. Unknown original App role remains Unknown; native agentRole/current selector/full-history relation does not infer a role. Read-only views remain read-only.

New start dispatch similarly returns real actual RPC/sent evidence before waiting, allowing lifecycle PreparedStart to freeze pre-dispatch composition with the actual allocated ID/ref. Start finish validates complete unchanged native ThreadStartResponse, then current readiness/full tuple and one-time insertion. Existing synchronous wrapper uses the same insertion behavior while preserving its original accepted shape/API; source_request retrieves the genuine retained receipt from its actual response ID rather than reconstructing params. Lifecycle observes only successful sent frame plus correlated result; role/source buffers remain its owner's responsibility.

## Actual checks and initial failures

Manager granted exclusive Cargo; cwd app/src-tauri, CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home. No other process compiled or ran native work in this slot.

| Run | Actual result |
| --- | --- |
| Initial `cargo test --offline --locked --lib history_bridge_` | exit0;5 passed,0 failed;7.18s compile,0.25s tests |
| Attempted joined-test insertion from wrong cwd | Python FileNotFoundError; no source edit occurred; following unchanged five-test run exit0,5 passed |
| First actual six-test joined run | exit101;5 passed,1 failed: lifecycle rejected fixture supply:fixture with supply identity absent |
| Corrected fixture `sup:fixture`, same product/assertions; `cargo test --offline --locked --lib history_bridge_` | exit0;6 passed,0 failed;1.20s compile,0.37s tests |
| `cargo test --offline --locked --lib hosting::` | exit0;30 passed,0 failed;0.36s tests |

Six checks exercise actual stdio/allocated RPC correlation and unchanged receiving reducers: before-wait genuine receipt, timeout/clone/late result; successful validated Continue then one-time registration and existing text transport; failed write/another Host/newer thread-state query/generation closure; notLoaded/direct false/native error/mismatched native ID/raw evidence; genuine exact start guidance/lookup/full native validation/duplicate finish; joined HistorySession list/select/Continue private receipt reconciliation and frozen Composition/start receipt/App-observed role. The joined case initially used the wrong supply identity prefix; correcting only that fixture was necessary and no failed production behavior is mislabeled fixed. Prior24 Host oracles remain unchanged and pass. Cargo released promptly after final runs.

Shared consumer provided the joined fixture sequence/method contract and owns actual runtime_session source. This test is in owned Host cfg(test), not a production test-support feature or invented imported capability. No real supplier/provider witness follows from synthetic native payloads. Cold role provenance/durable native reconstruction and broader supplier/UI qualification remain open. Source/API frozen for independent review before final shared UI checks.

## Frozen seals

| Subject | SHA-256 |
| --- | --- |
| `hosting.rs` | `7ef6d6a909e690d67089a3ef1f9628633d3a54c0c8cac95925f3efa3dfc02201` |
| `native_history.rs (unchanged)` | `63b7358679a14244e18125f52fcd0bcbe319240463a944219de9b5016c8fe613` |
| `role_lifecycle.rs (unchanged)` | `549fe28fe8155217ac961a29bf3dfe43b9103de12ccad585f609894e411bf7b3` |
| `supplier schemas (unchanged)` | `7243ba241962af92ca60581f1a81808ebda4212a800f8b205f54703bcfd508c5` |
| `conversation_transport_tests block` | `5ef8acbb11c830966caa68815fa10fe20c1977a3365a034c4c816ab7ece88fce` |

## HT-M1 start-envelope successor — 2026-10-05

Independent review of exact original7ef6d6 source was NOTREADY: thread_start_dispatch_finish accepted a genuine matching receipt with complete valid ThreadStartResponse result plus an error member, because correlation classified presence of result and the finish checked only that outcome/result schema. Original report seal e66c6918e3c83306a20e3b9f2e0abe8bebad6082fd650ba277afc8869c82a5db. Reviewer established this by source trace and ran no Cargo; no author original-version execution or copied private-capability repro is claimed. Original six passing tests did not cover mixed envelopes. Original record/source seals above remain historical.

After consumer source reservation release and reviewer Cargo release, author changes only the finish envelope predicate and adds one actual private-receipt inline regression. Finish now requires an object response, exact actual receipt RPC ID, absent method and error members, and present result before unchanged full native schema validation/current-generation insertion. Error-member presence refuses even null. Native journal/client correlation classification is untouched: mixed envelope can still be recorded response-observed-result as the original raw presence classification, but cannot admit a thread.

The regression uses actual env-cleared /bin/cat source write/private receipt/correlation with complete valid result plus native error object and explicit null-error member; both refuse before operational insertion and retain actual sent frame/raw result/error/status. An actual foreign-RPC frame is journaled uncorrelated, does not populate the receipt, and leaves pending after waiting. Existing ordinary valid start/control, history receiving, lifecycle join, wrapper/steering/terminal/ledger cases remain unchanged.

| Command | Actual result |
| --- | --- |
| `cargo test --offline --locked --lib history_bridge_` | exit0;7 passed,0 failed;1.38s compile,0.37s tests |
| `cargo test --offline --locked --lib hosting::` | exit0;31 passed,0 failed;0.37s tests |

Same isolated approved cache/cwd; no native/model/auth/network operation or shared source edit. Cargo released after those runs. No failed successor run or oracle weakening. Mechanical inverse of exactly this predicate and new test reconstructs original whole-file SHA7ef6d6a909e690d67089a3ef1f9628633d3a54c0c8cac95925f3efa3dfc02201, confirming all other original Host bytes preserved. API/source frozen for same-reviewer backcheck; shared integration final affected checks remain manager-owned.

| Successor seal | SHA-256 |
| --- | --- |
| `hosting.rs` | `0c381383a6c68d15bae9935b2ebca1e2f2f24099f27291714aaa72263a281a2d` |
| `conversation_transport_tests block` | `4a1a686cfae4b3426bd5751ff6b414baef94743f78d8e8a85c39eb735a6e3056` |
| `new mixed-envelope regression` | `b66ca541e403b2540dc6202d88e30212ca6a67d86bc0371318983c317be44783` |

## Shared registration-refusal receipt witness — additive cfg(test) only

Parent authorized the shared HistorySession owner's request for a genuine private-receipt assertion after its start_dispatched repair. Only the existing joined cfg(test) fixture is extended; Host production/API remains exactly HT-M1-reviewed production. A fresh actual /bin/cat start write and complete native result use an invalid local supply reference. start_dispatched returns Err while retaining actual request ID/ref/write/pending-or-observed outcome and rolePreparationError. After waiting and reconciliation, the original receipt still reports correlated native result; no new operational thread/role or second send is created. Immediate outcome allows pending or result to respect actual reader timing; post-wait outcome is explicitly result. No imported/fabricated receipt or production test-support API.

Frozen test candidate whole Host SHA fe3d797cff2cc2bd89b41673052fa0cd6012ab1e24b8ad11b5c2ad5895075315; conversation testblock2352f8b8d19fd6795610b392204ec43ba334a2d6973ee845fbfceba9f5e5ceca; added extension c85accd90109701874b225d8e6af5a6618479de4542f647b74a59032183f9add. Production before the first cfg(test) module is unchanged at d0f14888f27a09504756bd5ee2aa4249fe407eba81bbdf285b082c2e7a94cd61. Mechanical deletion of exactly the additive extension reconstructs whole-file0c381383a6c68d15bae9935b2ebca1e2f2f24099f27291714aaa72263a281a2d (asserted). No existing oracle changed.

Parent assigned actual combined execution to history_product_join's Cargo slot; this author did not launch a duplicate Cargo run. Source syntax emit-to-stdout check passes without rewriting. Actual combined output will be attributed below when returned; frozen preparation alone is not a passing test claim.

Actual combined return from `/root/group_a_execution/history_product_join` on frozen Hostfe3d797c:

| Sibling-executed check | Reported actual result |
| --- | --- |
| `cargo test --offline --locked --lib history_bridge_` with approved isolated cache | exit0;7/7 passed;2.98s compile,0.38s run; genuine joined registration-refusal extension and HT-M1 mixed-envelope regression passed |
| Shared history/conversation/recovery/runtime integration groups | exit0;7+5+6+10=28/28 passed;3.74s compile;respective0.25/0.06/0.08/0.17s runs |

Sibling's original tool turn retains full output and its record owns shared source/check details. This author attributes the communicated execution rather than claiming its own duplicate run. Cargo RELEASED; no additional source change after freeze. Test-only candidate ready for independent shared review; original Host production R1 remains unchanged, and no supplier qualification follows from mock evidence.
