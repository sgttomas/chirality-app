# Independent Host history/start-receipt bridge review — 2026-10-05

TASK `/root/group_a_execution/hosting_contract_review`, parent `/root/group_a_execution`; no delegation. Software-code-review applied. Only this report written; product, Design, supplier schemas, Git and dependency files unchanged. No native/provider/model/auth/network execution or reviewer Cargo run. Consumer held the shared Cargo slot during source assessment. Prior steering/sender/terminal review is accepted input, not duplicated qualification.

**NOT READY: one major blocking finding (HT-M1).** The remaining examined history/private-receipt path is suitable in its bounded source scope, but the new public start-finish API admits a contradictory native error/result envelope. No additional minor finding.

## Exact candidate

| Subject | SHA-256 |
| --- | --- |
| hosting.rs | `7ef6d6a909e690d67089a3ef1f9628633d3a54c0c8cac95925f3efa3dfc02201` |
| changes/I1-HISTORY-TRANSPORT.md | `d376cb4820bf101c037106d9c5660c084fc39857f9c15d4dcc828bc772c6655e` |
| conversation transport test block (author seal) | `5ef8acbb11c830966caa68815fa10fe20c1977a3365a034c4c816ab7ece88fce` |
| unchanged NativeHistory | `63b7358679a14244e18125f52fcd0bcbe319240463a944219de9b5016c8fe613` |
| unchanged role_lifecycle | `549fe28fe8155217ac961a29bf3dfe43b9103de12ccad585f609894e411bf7b3` |
| maintained native schema bundle | `7243ba241962af92ca60581f1a81808ebda4212a800f8b205f54703bcfd508c5` |

Source and record seals independently verified. Root/TASK/project/skill origins and current HOSTING/RECOVERY/ROLE/NPTD native basis remain those recorded in prior bounded reviews. Consulted unchanged NativeHistory current-resume guard and role_lifecycle observation refusal directly; no additional role activated.

## HT-M1 — reject native error before operational start insertion

**Major, blocking.** Location: hosting.rs:713–718 (`thread_start_dispatch_finish`); supporting path hosting.rs:984–999 (`on_line` response correlation), role_lifecycle.rs:328–345 (`observation`).

Trigger: dispatch a genuine guidance start against current ready generation, then receive a matching actual RPC reply containing both `result:<schema-valid ThreadStartResponse>` and `error:{code:-32600,message:"native refused",data:<retained detail>}`. Call `thread_start_dispatch_finish` with that genuine receipt. Source correlation currently records `response-observed-result` whenever result exists, even when error also exists. Finish tests method/successful write/result outcome, validates only `response.result`, then inserts the thread. It never checks `response.error`, so all of its predicates pass and it returns success despite explicit native refusal. This is established by direct source/control-flow tracing, not claimed as an executed Host reproduction.

Impact: a contradictory supplier reply becomes an operational known thread. The lifecycle observer correctly rejects any error member and thus cannot establish the corresponding role observation, leaving the Host admission inconsistent with the receiving/lifecycle facts. The claim that only a successful native start result qualifies for operational insertion is false for this envelope. Raw retention is required but is not permission to activate a contradictory response.

Basis: maintained JSONRPCResponse describes a successful **non-error** response; JSONRPCError describes an error outcome. Existing `history_admit_resume` explicitly refuses error, and the accepted `role_lifecycle::observation` rejects it independently of result shape. These are the applicable source-faithful semantics, not a new requirement to discard raw malformed evidence.

Repair: before schema validation/insertion, refuse any error-bearing start response; retain original response/client record/journal. Preserve actual matching ID/source binding and current generation/ready checks. Add one actual Host regression using the genuine start receipt and complete valid result plus native error, asserting refusal, unchanged operational thread count, raw error/result preservation, and lifecycle rejection. Keep valid ordinary start as control. No need to weaken receiving/schema checks or rewrite raw contradictory frames. A same-reviewer affected backcheck must bind successor hashes; this report does not approve moving repairs.

## Other examined paths and evidence

SourceRequest/HistoryDispatch are private-backed, Clone and non-deserializable. They preserve actual allocated supplier RPC ID/ref/frame and the complete private factory query; local query ID is not used for wire correlation. Weak source identity plus binding checks reject another Host even with identical visible IDs/tuples. No imported JSON receipt capability, invented native registration or transcript cache is introduced.

The shared begin/wait refactor retains full expected generation/open-ready admission under state lock and the accepted actual source-pipe ordering. The private receipt distinguishes write-in-progress/attemptedFrame from written/sentFrame and failed-write/unknown. Existing public client-record write semantics remain separate. Response may race write completion without promoting sentFrame before actual successful write. Source status retains correlated raw replies after timeout, and wait expiry does not resend or settle the outcome. Closure retains old evidence without successor admission.

History admission is restricted to original ID-only explicit Continue, exact latest resolved thread-state query/factory identity, current NativeHistory eligible resume and successful actual source write/correlated native result. It compares the retained raw result with validated receiving state, then under Host lock rechecks full tuple/home/ready/open/native ID and native loaded/direct-input eligibility. Newer pending/metadata/error state, foreign source, failed-write fabricated receiving candidate, stale/closed generation and duplicate insertion refuse. Read-only list/read pages do not register threads. Original App role stays Unknown; native agentRole and selector do not create role authority.

Start dispatch uses the accepted selected cwd/model/provider helper and exact additive developerInstructions. At the wrapper source level base/config/policy/approval/sandbox/collaboration overrides are omitted; actual supplier carriage/base inheritance is separately unproved. Normal finish validates complete native ThreadStartResponse and current generation/ready/duplicate insertion; HT-M1 is its missing contradictory-error check. Existing synchronous text/start/steer/interrupt signatures and terminal guards remain; no broadened actual supplier/model claim follows from them.

Author reports six bridge checks and thirty Host checks passing. All six new assertions were read: RPC41 distinct from local ID; receipt timeout/clone/late correlation; validated Continue admission then text; failed-write/foreign/newer revision/closure negatives; notLoaded/direct-false/native-error/wrong-ID raw negatives; exact guidance/start finish/lookup/malformed-result; joined HistorySession list/select/Continue plus Composition/start receipt/App-observed role. The initial incorrect fixture supply prefix and failed joined test are truthfully preserved; corrected fixture does not weaken product assertions. That positive joined test does not cover HT-M1. No reviewer broad suite repetition or synthetic evidence represented as stock/native qualification.

Return to original owner for HT-M1 only, followed by exact affected backcheck. Shared consumer/UI, durable receipt/custody/relaunch, cold role provenance, standalone activity/on-demand history expansion, real native/provider execution and supplier qualification remain separate production/witness obligations. This report reviews Host seams and the joined assertion's source semantics, not moving shared consumer code.
