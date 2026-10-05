# I1 native history query/receiving seam — 2026-10-05

TASK `/root/group_a_execution/runtime_core_production`, parent `/root/group_a_execution`; native descendant, no delegation. Writes: new native_history.rs, tests/native_history.rs and this note only. Existing hosting/lib/runtime_session/App/core modules, Design/schemas/resources/dependencies and Git remain untouched. No stock supplier/model/credential/network/download or enrollment/key action. This is the bounded next receiving seam; shared vertical wiring follows independent review.

## Available frozen API

- NativeHistory::new(explicit_home, full_generation), home/generation/selected_thread/selection_epoch getters.
- list_threads(cursor,direction), select(native_thread_id), read_metadata, turns_page(cursor,direction), items_page(known_turn_id,cursor,direction), read_goal, read_child(native_known_child_id), continue_query.
- HistoryQuery has immutable private fields with id/home/generation/method/params getters. Its local query ID/factory nonce are correlation only, never supplier RPC IDs or authority. No deserialization constructor.
- receive(query,actual_source_home,actual_source_generation,native_result), receive_error with native RPC error, waiting_ended, close_generation, snapshot and resumed_thread candidate.

Factories use unchanged maintained0.160 parameters and response/error schemas (Draft7, offline/local definitions, no retrieval/fallback). Resume is EXACT threadId-only: no guidance/base/config/model/provider/policy/history/path override. Metadata reads request includeTurns:false; turn pages use summary and an explicit native direction; item pages preserve per-turn identity. List defaults to the supplier's normal interactive/non-archived inventory; no complete-home enumeration claim.

The shared dispatcher must use exact params, bind actual current ready home/full generation before native dispatch and provide actual correlated response source metadata. It must carry the actual Host RPC request ID/ref separately for ROLE's trusted binding. This module does not dispatch, authenticate a transport source, insert a Host thread registry row, or prove a person's reserved act.

## Actual receiving behavior

All queries bind full H5 tuple and selected home. Private selection epoch, per-stream latest revision and unique factory nonce reject foreign, closed, older selection/query or other-view callbacks before view mutation. Native thread/goal/item-turn relationships are checked alongside complete maintained schema validation. No thread home is guessed from UUID, path, provider, sessionId or source labels.

Opaque next/backwards cursors are kept exactly, scoped to stream/direction; backwards uses the reverse native direction. Missing cursor is not-reported, null is exhausted, string is available. Goal omitted, goal null and reported goal remain distinct. Empty/summary/notLoaded/inProgress/native extras remain raw supplier facts, not missing events or live App binding.

Only transient displayed native pages/metadata are held; latest turn/item page replaces the prior page, with pointer/cursor sets for navigation. No filesystem persistence or durable transcript store exists. Closing the generation discards selected native view and refuses old callbacks. Native plan item/turn IDs remain in the raw page; prior checklist updates are explicitly unrecoverable from supplier history, never reconstructed from messages.

Children become readable only from received collab receiverThreadIds or subAgentActivity agentThreadId. Child reads retain native metadata plus unknown App role and no return/review/integration inference; parent completion does not settle a child. This seam offers no child turn/delegation action.

App role is explicitly Unknown absent original request-bound supplied-role evidence. Native agentRole, current store/user configuration, forkedFromId, instruction paths or a runtime record's existence do not assign it. Coordinated directly with workflow_role_production: its immutable trusted RoleBindings.lookup(home,thread) may be rendered alongside this native view by the shared owner. This receiver imports no role JSON and claims no fixed-role qualification.

Read/select pages remain indexed-read-only, even if native data contains active history. continue_query merely prepares the explicit Continue action; only a matching native resume result can produce resumed_thread candidate metadata, excluding notLoaded/systemError/directInput:false. It is NOT active registration or provider execution; owner must recheck scope and actual direct-input facts before binding. Native resume errors/wait limits/closure remain distinct, with no automatic replay or role injection.

## Evidence and limits

Manager-granted Cargo, approved isolated cache and cwd app/src-tauri:
`CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test --offline --locked --test native_history` → **exit0; 8 passed, 0 failed, 0 ignored**, 0.23s after 0.47s final compile, no warnings. Initial8/8 pass had unused getter/side-thread warnings; added coordinated getter assertions and explicit side-thread relationship guard, then8/8 reran. No failing test, weakened oracle or dependency change. Test imports the new file by path, so no shared lib declaration was required. Cargo released promptly.

Cases cover exact query/resume shapes; native notLoaded/summary/ended-vs-inProgress and unknown role despite native role/fork metadata; opaque cursor direction/stream plus absent/null distinction; full tuple/selection/factory stale refusal with unchanged view; full schema and relational atomic refusal; goal availability; explicit resume/error/wait/close eligibility; native plan/item IDs and known-child lookup/status. All native payloads are invented schema-checked fixtures inside tests; no supplier or live witness is established.

After independent review, shared owner can wire selected home→native list→metadata/turn/item/goal/child view→explicit Continue. Only a validated matching resume response should feed a separate active Host binding; ROLE evidence stays its own immutable seam. Actual stock history/resume, same-home recovery, fixed-lifetime guidance, native UI/role source persistence and provider/supplier qualification remain unfinished witnesses/production at their existing homes.

## Source basis and frozen seals

| Origin | SHA-256 |
| --- | --- |
| `projects/chirality-app-v4/app/src-tauri/src/native_history.rs` | `c65fd6598d0d37cbeb175cb11c8f79b02ca5f3598c021115d524e2600910a9fe` |
| `projects/chirality-app-v4/app/src-tauri/tests/native_history.rs` | `9d538238851293f76a5451511d951d74636b5e5fc8b3d98b0d8ec56b73972174` |
| `projects/chirality-app-v4/app/src-tauri/resources/supplier/0.160.0/codex_app_server_protocol.schemas.json` | `7243ba241962af92ca60581f1a81808ebda4212a800f8b205f54703bcfd508c5` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md` | `9b443fbc5e7fc617e51e18c4cb8aec7af0d429bc7fefe3e0ec9e52f968aa79d1` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-03_Native plans, tools and delegation views/Design/NATIVE_PLANS_TOOLS_DELEGATION.md` | `8b8d0e46a25b6872e806aa49cc9e7604515d643bbd4a51c0913bbcace2585c54` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/ROLE_SUPPLY.md` | `b279a23a5c8d8b2170618a062b3a5ccc3ea07a1cecdfcec7c61d0320f6559ba9` |

## I1-HISTORY-R1 semantic-state/provenance successor — 2026-10-05

Read V2-I1-HISTORY in full after publication. Preserve its original module c65fd6598d0d37cbeb175cb11c8f79b02ca5f3598c021115d524e2600910a9fe, test9d538238851293f76a5451511d951d74636b5e5fc8b3d98b0d8ec56b73972174 and record50739c01c25feb8cf9958f164fdf2539fb4c9d45726f8c030fc362d2b6285a29 seals above. Reviewer copied byte-identical originals and ran three public-API regressions: **3/3 negative assertions failed, exit101**, with positive initial resume/error controls passing. This successor is not certified by that original verdict; same-reviewer frozen backcheck remains ahead. No independent rerun of the old copied source is claimed here.

| Finding | Concrete successor behavior/actual new regression |
| --- | --- |
| HIST-M1 | Successful resume retains its accepted thread-state revision. Candidate eligibility requires that revision remain current, no current pending thread-state query/error, and open generation; newer metadata or Continue immediately withholds old success. Original notLoaded/directInput:false sequence, pending/timeout/new success and superseded old pending read are covered. Old native response remains raw historical evidence rather than current eligibility. |
| HIST-M2 | Current errors and resolutions are keyed by owning logical stream/query/revision; same-stream success clears only its current error. Native error/query is retained in errorHistory. Goal error→goal:null success recovers current standing; metadata or goal success does not erase unrelated goal/child failure. Child error→same-child metadata success recovers without losing old native error. Original unavailable/erasure sequences are tested. |
| HIST-M3 | Only completed spawnAgent with native sender/receiver provenance establishes a new collab parent-child edge. In-progress/failed spawn, sendInput/wait/closeAgent/resumeAgent receivers remain standalone native references and do not permit read_child. Later calls update an already-known child's last observed reference without rebinding its original parent/source item; conflicting read metadata stays raw and does not replace provenance. SubAgentActivity references are also kept separately without silently granting a completed-spawn parent edge in this slice. |

The original paragraph admitting every collab/activity reference as a readable child is superseded by this named completed-spawn correction. Raw calls/items remain unchanged in displayed native pages. New receiverReferences holds only source-bound pointer/tool/status metadata; no new role or broader reference-based control is adopted. App role remains Unknown, even for native role/fork fields. Exact native query/resume bodies, source schemas, opaque/null cursor semantics, home/full-tuple guards and read-only versus separate active registration remain unchanged. Public API signatures remain frozen.

New snapshot fields expose errorsByStream, errorHistory, streamResolutions, resumeEligibilityCurrent and standalone receiverReferences. The legacy selected.error remains a view of current stream failures for existing consumers; historical errors do not masquerade as current unavailable after same-stream recovery. Goal availability follows its own current error/pending resolution. Prior resume payload is explicitly last-observed evidence until a matching current revision makes it eligible; query preparation/waiting is never success.

Actual command, cwd app/src-tauri and approved isolated CARGO_HOME, serialized manager grants: `cargo test --offline --locked --test native_history`. Initial repaired source **12/12 passed** (original8 +four new groups). Read the full report and added its requested child-stream control without changing product source; after lifecycle reviewer released its short slot, final **13/13 passed, exit0, 0 failed/ignored, no warnings**, 0.23s after0.66s compile. Original eight tests/oracles remain; five new groups cover uncovered combinations. No successor test failure, weakened criterion or fabricated status-only pipeline claim. Cargo released immediately for actual same-case reviewer backcheck.

Only owned native_history.rs/test and this record changed. No Host/lib/UI/runtime_session/Design/schema/dependency/Git/source-qualification/native/model/auth/network action. ROLE's private binding remains separate, coordinated with its owner; this seam has no original role evidence importer. Supplier history/resume/native UI/durable role-source reconciliation and qualification obligations remain at their existing homes.

| Frozen successor subject | SHA-256 |
| --- | --- |
| `native_history.rs` | `63b7358679a14244e18125f52fcd0bcbe319240463a944219de9b5016c8fe613` |
| `tests/native_history.rs` | `b473c4ddaacf52f0bf0aac60bb12efe1bd20a76a02e63cf68a122838a25d234e` |
| `V2-I1-HISTORY original verdict` | `d04f5a893c6b22f7f3dc6089ec784d328408faa4f2ed6f930854119ddb391ea1` |
