# I1 generic recovery custody — next local boundary

2026-10-05. TASK `/root/group_a_execution_astra/remaining_local_receiving`, parent `/root/group_a_execution_astra`; native delegated child, Astra/low as supplied, no delegation. Read-only source-fit investigation except this sole report. Parent retains candidate freeze and Git metadata; no Git/Cargo/tests/supplier/native/auth/network/credentials/model execution. Existing PI-6 external binding assessment remains unchanged.

**Result: a coherent local implementation assignment is ready at the bounded, explicitly indexed-conversation boundary.** Add native-source execution-pointer capture to the existing Host/sole recovery ledger, produce the defined loss/restart custody projection, and expose it in the existing App recovery reader. This is a real producer→persistence→consumer path. It needs no host catalog, external operation, model call, OI-003 ruling or DECISION-3 resumption. It does not supply the external native-item→proposal association. It is not full DEL-01-02 completion or a substitute for later native restart examination.

## Requirement and semantic comparison

DEL-01-02 ScopeOfWork REQ-005/006 and AC-006/007 require restart-visible prior observations, explicit unknowns and pointer-only custody supplied to the UI/evidence boundary. `Design/EXECUTION_AND_RECOVERY.md` §3.2 CV-08…10, §5 SQ-R R-2/R-5 and SQ-X X-1/X-2, §7 and §8 provide the particular contract:

- A generation close loses observation, while observer window loss does not. `observation_lost` contains the actual home/generation, conversations, live turns, in-flight item references and outstanding request references; all remain App-observed facts.
- The existing ledger `conversation_index.lastObservedExecution` expressly holds execution state, live/lost turn, cause and open item IDs/types. It does not retain native message/item content. On relaunch, `app_restart_interruption` names each conversation with live work at the prior end. Codex status is displayed beside the App account, never substituted for it.
- §8.2 names DEL-01-03/01-04 display as a direct consumer independent of ADAPTER and RS. Recovery writes its own format; it does not map a workflow run, external operation or RS record.

This is not a gap inferred from spelling alone. The following semantic paths were inspected:

| Existing source path | Already supplied | Actual remaining boundary |
|---|---|---|
| `hosting.rs` `on_line` / `remember_turn` (around 1589, 1727) | Full-generation, receipt-ordered native source and terminal guard; actual turn state retained in `conversation_turns` | No execution-pointer ledger projection at these state transitions |
| `hosting.rs` `close_generation` (around 863) | Pending requests become unknown; server register closes and summaries queue; matching turns gain `observationEnded` | Turn/item pointer state and specific generation-loss event are not projected to durable index/custody |
| `native_items.rs` `consume`, `item`, `close` (142–189, 246 onward) and `runtime_session.rs` `receive` | Live start/completion references and unknown-on-close semantics; prior in-memory views and checklist limits | Disposable, observer-driven receiving state. `lib.rs:host_status` drives it by polling. It cannot be the sole durable producer when no window polls |
| `hosting.rs:observe_conversation_project` (around 560–574) | Actual explicit App project/home admission, original index/tags, existing ledger append | Production initializes only `lastObservedExecution.state=indexed`; an existing index is returned unchanged. Search of maintained production code found no other execution-state/openItems index producer |
| `RecoveryLedger`, `CapturedRecoveryQueue`, `AppRuntimeCustody` | Canonical pointer schema validation, append/sync, immutable queued rows, per-source ordering, retained queues after Host retirement, one actual session/ledger, visible failure | Reuse this infrastructure for new metadata. It currently carries request summaries/context plus session metadata, not the missing execution transitions |
| `recovery.rs:start_session` and actual `lib.rs` / App recovery display | Reads prior session end and exposes ledger/history status; App recovery details already show historical pointers | No per-conversation restart projection from prior live/lost execution facts; native History stays separately sourced and explicit Continue stays separate |

The admitted runtime ledger resource already defines `lastObservedExecution.state`, `liveTurn`, `lostCause`, `abortNoteExpected`, `openItems[{itemId,itemType}]`, and `lastLoadedGeneration`. No new content store, ledger kind, persistence service or field widening is needed for the bounded indexed path. Custody-event schema is a separate output shape, not a license to append that shape to the ledger. Reconstruct the bounded historical custody projection from allowed pointer facts and label its source/time/limitations truthfully.

## Coherent assignment and ownership

Commission one I1 Host/REC owner for `hosting.rs`, `recovery.rs` and a small owned metadata/custody helper if useful, with Parent as sole shared `runtime_session.rs`/`lib.rs`/`App.tsx` integrator. Reuse the maintained recovery schemas; copy the existing custody schema as an exact owned resource only through ordinary manifest/resource adoption if production validation needs it. No Design rewrite is established as necessary by this assessment.

1. **Capture at the native source.** Consume current full-generation admitted turn/item start/completion observations in the main-process source path, not public renderer JSON, an imported ledger or `host_status` polling. Keep only thread/turn/item IDs, item type, last status and observed cause/time. Preserve the existing terminal guards and original raw evidence. A renderer detach does not generate loss.
2. **Persist through the actual sole queue/ledger.** For a conversation already admitted with explicit home class and known project, append updated index snapshots with original project/tags/fork provenance unchanged. Include started-not-completed item references and live/lost turn before state is retired. Capture immutable rows before IO and reuse the reviewed nonblocking/pending/error and retired-source behavior. Do not turn persistence failure into a supplier stop or claim confirmed cold custody. Known closed/completed state must remove live eligibility while retaining appropriate loss metadata, rather than reviving a turn.
3. **Generation loss and restart projection.** At the actual end-of-generation path, report the affected home/full tuple once, with the defined live/in-flight references and actual observed cause. On App restart derive the prior conversation interruption from successfully persisted pointer history and prior session standing. Do not claim a system termination was observed when the only fact is ended-without-record. Do not manufacture quit-with-live-work, a stop request, or graceful-stop note without the existing source actually establishing it. Distinct supplier-history readings remain separate, and no automatic resume/send occurs.
4. **Consume in the real App recovery view.** Add the typed/projection result to the existing Root recovery status and render prior live/lost conversations, item refs, source standing and missing-persistence/history limits. The schema/API must be usable by later receivers, but this assignment ends at the present UI recovery consumer. Existing native History/Continue remains the source for prior native content and explicit continuation. Merely adding an unused reducer or a test-only exporter is insufficient.

**Bounded missing-data rule:** current `conversation_index.project` is mandatory. CC-REC-ATTACHMENT-PROJECT-CONTEXT (§7.1) explicitly prohibits a fake/null/cwd-derived project row and permits memory-only behavior with cold-lookup limits when the actual index is absent. Preserve that rule: live loss facts can remain visibly memory-only, and absence after restart is unknown/unavailable, never proof of no live work. Do not expand this assignment into solving projectless durable indexing by changing the schema. The supplied path is independently usable for actual explicitly indexed conversations; claim that extent.

## Offline checks required for this assignment

No checks below were executed in this assessment. Use existing source-bound Host fixture lanes and a real owned temporary ledger; no live supplier is necessary to examine own-code behavior.

- Admit an indexed thread through the actual explicit context path, deliver synthetic native turn-start/item-start to the actual Host source while never polling the UI, then close the generation. Inspect exact queued/durable pointer rows and the produced loss view. This proves capture does not depend on an observer.
- Reopen the ledger under a new actual App session and exercise the real recovery projection/Root consumer. Prior live turn/item refs and unknown standing survive; current native status is a separate field. No resume, text send, human act, external effect or run end is created.
- Repeat closure/status reads/restart projections: no duplicate durable transition or side effect; generation/home/session isolation holds for equal thread/turn/item labels. A stale old-generation notification cannot change successor custody. Preserve the existing terminal-before-late-start regression.
- Complete an item or turn before loss; it is not falsely in flight. A child/other home still active remains separate. Detach/hide/reload only leaves main-process capture running and creates no generation-loss event.
- Exercise current admission with unknown project/home, historical P plus current Q, existing tags/fork, unavailable ledger, busy writer, append error and retired Host. No fake context, row mutation, dropped pending fact, raw content or false durable claim. Reuse the reviewed queue controls rather than weakening them.
- Reopen with torn/unreadable ledger and missing end record; retain bytes and unavailable/ended-without-record limits. Do not invent the lost frames, item content, exact termination time or quit cause. Check both current event and restarted projection against their unchanged schemas.
- Validate actual App status/presentation and native-history separation using the ordinary offline UI/test lane. Actual native multi-home quit/relaunch behavior and crash/power-loss durability remain Parent-only later evidence, not inferred from fixture success.

## Existing warrants reused

`V1-I1-SHARED-APP-CUSTODY-R1.md` explicitly covers retained immutable pointer queue lifetime and single App session/ledger mechanical behavior, not full recovery. `V2-I1-REC-RT.md` covers request summary RT/RQ mapping, not generic turn/item loss. `V3-I1-LEDGER-STARTUP.md` covers actual startup location/configuration/status and pointer-only failure behavior, while leaving complete conversation/relaunch recovery open. `V2-I1-CONVERSATION-R1.md` preserves terminal/live-turn guards and explicitly leaves durable cause/quit/run accounting separate. These are historical scoped review warrants, not new reruns or blanket approval of a successor.

## Read provenance

Applicable Root/TASK/v4 LOOP basis is retained from the preceding report. The Field Book was now read completely in two untruncated ranges, lines 1–160 and 161–316; no App-v3 entry was consulted again. User Manual headings/index were already consulted. Below are current SHA-256 origin fingerprints of newly relied-on sources/records; reads were selective except the Field Book and custody schema. Hashes do not assert acceptance or frozen Git identity.

- `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` — `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/ScopeOfWork.md` — `6c62de1d749022a388d9a2c466655a35e06b0b9fa7779a7912f9df4424226a07`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md` — `e78b9ead452b0a1adb20cf07493a1eccbd2ee651e68d4f75772c440a6a228056`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/recovery.custody-event.schema.json` — `033398508abc813e90aee0a074a18cb91bd59be88b6991111504ae5662653773`
- `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` — `c8fcbfa53c7e3db24fc771c9dc883d8bfd6481512f6d06ecc39164bff71a92f3`
- `projects/chirality-app-v4/app/src-tauri/src/recovery.rs` — `f0fff309d2f8eec23046b5349e4969308ef26319a4e5b6eedf46b3c4da50bc31`
- `projects/chirality-app-v4/app/src-tauri/src/runtime_session.rs` — `05af3f76da30a02dd425d9de025c623402a2fbdfefcdfc99c5f7201590c041f6`
- `projects/chirality-app-v4/app/src-tauri/src/native_items.rs` — `585df2a401826e15c08bed8dda556c65c5d0ee2c4780c01e96eca10992893770`
- `projects/chirality-app-v4/app/src-tauri/src/native_history.rs` — `5d9a268639399ff70e44b9217c2a317986ddc653d4684e64f40af6acd77922ab`
- `projects/chirality-app-v4/app/src-tauri/src/lib.rs` — `aca501453e1897245fb3b53b37e7d28e5e330983594771c3d7816e935d7980cf`
- `projects/chirality-app-v4/app/src/App.tsx` — `e542116a6270783432e0d9724b4c6676888ca0c244492ab9140a360ac8b6a4cb`
- `projects/chirality-app-v4/app/src-tauri/resources/runtime_core/recovery.app-ledger-entry.schema.json` — `3f1d7f27f68a523c459ebcb9ce3dcd40a5de54fc4b9b16d20fd4e6b4c3f05c67`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V1-I1-SHARED-APP-CUSTODY-R1.md` — `85c50659c92af30ce78d631e39dc668ce0fb74b9041d941b0536759237d6dca8`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V2-I1-REC-RT.md` — `e0af5cdcac9683c82482b2f4b4cf8dbc859adead7c477fbd9adef0b2eaf3a45f`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V3-I1-LEDGER-STARTUP.md` — `2b7737680ed1a66ff4266cc51156ae6268c9697bfe9da0aa7cbf7bb7b186cf47`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V2-I1-CONVERSATION-R1.md` — `01084bf59381e38fc12c66c559dc4c1f9790ebd0784da6e41adf5b03c491ea62`
