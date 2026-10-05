# I1 explicit App context owning APIs — 2026-10-05

TASK `/root/group_a_execution/runtime_core_production`, parent `/root/group_a_execution`; no delegation. Adopts independently reviewed REC R1 packetef5039ee/source reviewa1842f and ACCESS packetab7afcd/reviewb415a5eb plus NIR923907 concurrence. Writes only access.rs, bounded hosting/recovery APIs, isolated tests and description-only REC schema/manifest/this record. No shared lib/runtime/App, Design/Git/dependencies/live/auth/model/download changes. Parent PR1089/source5a526 transport remains historical; this candidate extends actual context source/sole ledger ownership without rebinding that evidence.

## Available exact interfaces

```rust
ConversationSelection::new_explicit(&str conversation,Option<&str> project)
    -> Result<Self,String>
ConversationSelection::project() -> Option<&str>
ConversationSelection::canonical_record() -> Option<Value>
ConversationSelection::view() -> Value
ConversationSelection::recovery_home() -> Option<&'static str>
ExplicitAppProjectContext::known(&str reference,AppProjectSource) -> Result<Self,String>
ExplicitAppProjectContext::unknown() -> Self
ExplicitAppProjectContext::{reference(),source_caption(),view()}
Host::observe_conversation_project(&Value full_generation,&str thread,
    Option<&str> recovery_home,&ExplicitAppProjectContext) -> Result<Value,String>
Host::bind_attachment_context(&PreparedAttachmentDispatch,
    &ExplicitAppProjectContext,Option<&str> recovery_home) -> Result<Value,String>
Host::flush_recovery_observations() -> Value
```

ExplicitAppProjectContext is Clone/private/noDeserialize. AppProjectSource is configured or opened App directory, supplied by native Root/shared owner; reference nonempty/lossless, no cwd/nativeprojectId/Codex home/WR/renderer inference or identity service. Freeze reference or explicit absence before awaits; getters do not hydrate capability. API-private type alone is not native picker/provenance qualification.

ACCESS known new(c,p)/canonical0.2 fields and behavior unchanged. Unknown lives in private no-schema/no-project choice state, never fake/nullable canonical record; derived snapshot preserves top state/selection/thread/refusal for existing claim/finalize. Unknown refuses project last-choice offers, no model default or cache/save key, but explicit person entry/provider/model and native home/generation guards still start ordinary input. Project getter frozen, cloned views do not retag. recovery_home only reads actual stored start_params home kind (account→H-acct,api-key→H-key), never provider label/opaque generation.home/cwd. Continued source with no owning class passes None and remains hot-only rather than inventing account class.

REC index HomeH-acct/H-key, native opaque H5home, native thread cwd/projectId, explicit App project and WR run are distinct. Observe requires current ready/open fullG and actual operational thread. Existing P index retained even current Q; no retag/backfill. Only no prior index plus actual CURRENT known Root reference+owning class+configured ledger appends current index observation, indexed state and full generation reference. None project/home/ledger yields no row with explicit limit; native ID is never guessed before assignment.

Bind takes actual private PreparedAttachmentDispatch/source/token. Exact opaque owner DEL-01-04 tag value is compact UTF8 JSON `[actualSubmissionToken, projectRef|null]`, no normalization or new fields/kind/store. Merge every durable tag and hot binding before same-token idempotence/conflict. Historical P stays P; current Q/null separate same/different/unbound. Missing index/home/ledger is hot-only/no cold lookup; same known-P plus failed durable Q remains hot and prevents R retag. Repeated Q stays idempotent with memory-only limitation, not an automatic durability upgrade. Complete conflict remains explicit; old unknown tags/rows preserved. Tag does not establish native receipt/turn/actor/run/provenance or blanket-hold ordinary input. After IO source changes are reported against captured old context, not applied to successor.

## Sole ledger IO seam

Host retains one Arc<Mutex<RecoveryLedger>> and one writer mutex; consumer never opens a competing writer. State lock captures immutable pointer-only summary entries/order into pending queue, using safely observed durable entries plus earlier queued facts for original RQ history/dedup guards. Snapshot exposes retained observed ledger snapshot/pending facts/projection limits without acquiring ledger while holding Inner. Actual writer admission/ledger IO happens outside Inner; ledger guard is dropped before state recheck/cache update. No background service or new store.

Native paths use nonblocking writer admission: busy writer retains actual captured queue/order with visible unpersisted limit, never silently skips. Failed append keeps failed/front+later facts queued; only actually appended prefix is removed. Pure projection retains exact existing RT14/RT15/closure/foreign/failed-write acknowledgment checks and dedup behavior. New context methods pin fullG/thread across writer waits/rechecks; pause/source changes cannot attribute old context to successor. Ordinary filesystem latency is not a new hard deadline guarantee. Actual paused-ledger test proves native on_line/Stop does not wait behind that owner, keeps request facts then flushes in order after release; it does not qualify arbitrary filesystems.

Canonical REC0.2 resource copied from reviewed source3f1d7f: descriptions only. Independent annotation-stripped comparison before adoption returned identical structure/ID/properties/constraints; no nullable project/index successor. Manifest updates only that source identity. No native body/transcript/cache or project/run namespace fields added.

## Actual tests/failure and source freeze

Manager-exclusive Cargo, approved CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home, CHIRALITY_SKIP_CODEX=1, offline/locked, cwd app/src-tauri. First compile exit101: initial pure request summary extraction still referenced self.entries and returned legacy no-op (). Fixed faithfully by explicit prior-entry input and Option<Entry> dedup; wrapper still uses actual ledger history, queued projection uses retained durable+earlier captured history. No runtime failure or oracle weakening.

| Command | Actual result |
| --- | --- |
| `cargo test --offline --locked --lib explicit_context_` | exit0;3passed;4.35s compile,0.26s test |
| `cargo test --offline --locked --test explicit_context` | exit0;3passed;7.51s compile,0.02s test |
| `cargo test --offline --locked --lib hosting::` | exit0;46passed/1ignored actual-supervised helper;7.57s test |
| `cargo test --offline --locked --lib access::` | exit0;5passed;0.01s |
| `cargo test --offline --locked --lib recovery::` | exit0;10passed;0.23s |
| `cargo test --offline --locked --test recovery_startup` | exit0;6passed;0.07s |

Connected actual disk/private packet controls: index P/currentRootQ with different native cwd, Q/null exact tags and idempotence; no index/home produces no row/hot limit; real torn append preserves hot Q conflict/R refusal and same-Q cold limit; actual paused ledger mutex permits request/actual cat Stop, preserves immutable listed→closed summary order after release and rejects old context after source closes. Public tests cover unknown selection no-row/default/offer, actual home-kind getter, exact Unicode codec/durable+hot ambiguity, known0.2 shape/clonedview nonhydration. Existing transport blocking/EOF/Stop/source/late-reply/recovery/ledger oracles all pass. Fixture classes/strings establish test source relationships, not real provider/native/picker qualification.

Cargo RELEASED immediately; Core source/API frozen for independent review and shared consuming tests. Shared Root/picker context must be actual before await and bind actual returned token, choose home only from actual owning class, display P/currentQ/submissionQ separately. WR prefix interface remains independent; this ordinary path claims NO TC2 prefix or run. No current view backfills provenance, no unknown row automatically blocks text/attachments, and no output is an accepted App act.

## Frozen production/test/resource seals

| Subject | SHA-256 |
| --- | --- |
| `app/src-tauri/src/hosting.rs` | `57aed4efad089457138a070bf1a4650ef175966a2a94d49b4e8fbeeeacf37bd8` |
| `app/src-tauri/src/access.rs` | `cf6a439f98433b3fbfb1d96a7fb0f4270b080e1b7bb1e1a6bcf470b78716a5ac` |
| `app/src-tauri/src/recovery.rs` | `da5c7b0d6d82cc4e10f3eb0face6e92454aa9c468e4d92736c8fb36b82028877` |
| `app/src-tauri/tests/explicit_context.rs` | `aa3ea786b187306160e351e5236b680dd3e2a5862b15285a93dd5047a300c0ae` |
| `app/src-tauri/resources/runtime_core/recovery.app-ledger-entry.schema.json` | `3f1d7f27f68a523c459ebcb9ce3dcd40a5de54fc4b9b16d20fd4e6b4c3f05c67` |
| `app/src-tauri/resources/runtime_core/manifest.json` | `36e5e8f532667a1bc7c6a9e5c3d322b06e09c9bc9b8166c54fc02dac513b8cfc` |

## Additive shared actual-private consumer witness

Parent separately released cfg(test)-only joined fixture on original production57aed. New existing-Host inline helpers/two cases call ACTUAL runtime_session::submit_selected_attachments with real AttachmentSelectionSession/native selected-path callback, private handles/whole order, actual prepared packet/SourceRequest/owning custody/sole ledger and env-cleared cat outbound/correlated synthetic response. No DTO receipt/picker reconstruction, second ledger, product test-support API or production change. Known historicalP/currentRootQ remains separate from nativecwd; unknown context/home has hot limit/no row; actual bytes/source drift and stalefullG emit zero cat bytes; native error/raw outcome/selected sources remain visible and refresh does not resend. No WR prefix/native provider qualification follows.

Test-only whole Host cf798098bd40bc2de4c5dac6ec15c929f45e7fe6a6b8d75dcd6abcb1dbd26b70, conversation block4ff112eb9915202fa4ce2396a2e98a94dffbbcbf3123116ccd263fc91a82a202. Mechanical deletion of exactly new comment/helpers/two test bodies reconstructs original WHOLE Host57aed4efad089457138a070bf1a4650ef175966a2a94d49b4e8fbeeeacf37bd8 (asserted); owning production review remains on those unchanged bytes.

Actual run owner `/root/group_a_execution/history_product_join`, parent-granted serialized Cargo slot, approved isolated cache/offline/locked; no duplicate Core run. Joined against frozen runtime_session7c5a31458330141cf698ab4a9104eebae06cfb404f59afd5b42623b028338c49/lib921c6e09c83d15e1aee18d02eb16d4ddc7ed84d3b7afbdf207b64210d975035b/App9864feeae0c317af0590d22ae0a9c5634bf1fa0672b81e77f62bc376ac22257f/attachment integration52c63ca004731927d1d1260cd9cebfc455ba71211384a191438bb06112c82f3f. Shared owner reported actual `--lib shared_attachment_` PASS2/2 exit0,3.25s compile/0.56s tests; external attachment5 plus affected70 PASS75 exit0. Full original output in shared owner's tool turn/record, not authored or relabeled Core execution here. No test failure on this additive witness, no source polish after freeze. Cargo RELEASED immediately; shared product source/qualification ownership remains separate.

Actual combined shared execution total77/77 passed (joined2 +external/affected75), as returned by shared owner and Parent. Product home-class consuming warrant is ONLY H-acct from the actual existing account start_params branch; unknown continued association remains None/hot-only. H-key getter maps an actually owned API-key home-kind branch in Core but no product branch/native/API-key qualification or sign-in witness is established here. This Core API/test-join contribution does not certify whole shared production/UI or broaden access/supplier support. Final source unchanged; no rerun/test expansion beyond returned actual output.
