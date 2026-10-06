# I1 recovery custody core — private implementation

TASK `/root/group_a_execution_astra/remaining_local_receiving`, parent `/root/group_a_execution_astra`; Astra/low supplied, native delegated child, no descendants. 2026-10-05. This sole maintained report accompanies private source work. No maintained App, Design/schema, graph, Git, supplier/native/auth/model/network/download/credential action. Parent's supplied `b44f6bfc` source checkpoint was copied without Git inquiry. Parent owns shared Root/UI integration and candidate archive.

**Current standing: private ledger0.3 core compiled and43 distinct controls passed; independent backcheck and Root consumer integration remain pending.** Exact checked source/executable are retained. Earlier failures/partial0.2 evidence remain historical. No fan-in readiness, RC1-COLD independent closure or native restart witness is claimed. Initial parser-only preparation is retained below as history. Applicable Root/TASK/v4 LOOP and complete Field Book reading/provenance are in `I1-RECOVERY-CUSTODY-NEXT-ASTRA.md`; source-fit obligation and external PI-6 limit remain there.

Private stationary App: `/tmp/chirality-rec-custody-astra.bo0pfG/app` (copied without node_modules/target). Baseline copies, `baseline-manifest.json`, `custody-schema-origin.json`, `manifest.json`, `recovery-custody.patch` and parser outputs are in its parent directory. The source patch is against the two actual baseline files; three new private files are included. Maintained hosting/recovery bytes were independently compared with the baseline after edits and remain equal.

## Supplied private production changes

- Host-owned `execution_custody.rs` captures pointer state directly from admitted `on_line` item notifications and guarded `remember_turn` calls. It retains full generation/thread/turn/item identity, no native payload. Terminal/completed sets prevent late starts reviving finished work. Renderer polling supplies no input.
- Actual `observe_conversation_project` binds this state to an admitted existing/new index without changing historical project P to current Q. Pointer snapshots refresh from the owning ledger/pending rows so opaque tags/fork/source metadata are retained. Only existing `conversation_index` shape is appended.
- `close_generation` captures loss before the request register closes, retaining outstanding references and actual stop/exit cause. Duplicate close cannot emit another loss. Existing immutable queue, sole writer, pending errors and retired-source lifetime are reused; no new ledger/store/service or resume/send is added.
- `RecoveryCustodyView` projects successfully persisted index history separately from live/queued state. Canonical full generation and session order prevent delayed old-generation rows from replacing newer same-home observations. Relaunch outputs the defined `app_restart_interruption` only when prior-session live/lost pointers and end standing support it. Clean session end alone never proves quit-with-live-work. Missing/mismatched history remains limited/unjoined.
- Missing explicit home/project/index stays memory-only, with cold lookup unavailable. No fake project or new shape is introduced. Supplier-native History, external proposal mapping, current workflow/run inference, actual stop/quit qualification and human-act authority remain absent from this API.

## Frozen Root consumer API

```rust
Host::recovery_custody(&self) -> crate::recovery::RecoveryCustodyView
RecoveryCustodyView::snapshot(&self) -> serde_json::Value
```

Read-only: no flush, append, supplier read, resume or admission side effect. `RecoveryCustodyView` has no public constructor/Deserialize and is not a source capability. Root must call it on the **actual current HomeSession Host**, keep it beside the existing native History view, and render its limited standing. A displayed or serialized view cannot be passed back to establish authority.

| Snapshot key | Meaning and limits |
|---|---|
| `live.events` | Source-observed `observation_lost` custody events for bound conversations; not a claim that this whole event was durably stored |
| `live.observations` | Current/historical in-memory pointer state, full generation reference and thread, turn/open-item references, indexKnown; no native content |
| `live.limits` | Unknown owning index/home means hot-only loss and cold lookup unavailable |
| `restartEvents` | Custody-schema restart events derived only from successfully persisted prior-session index/end facts |
| `historicalConversations[].index` | Original selected persisted index row; App last observation, not current Codex state or native history |
| `historicalConversations[].standing`, `.nativeHistory` | Explicit pointer-only and separately-read native history labels |
| `pendingPointerFacts` | This Host's actual unpersisted queue count; not cross-home completeness |
| `limits` | Ledger unavailable/malformed correlation, queue pending, writer error and uncertain clean-end cases |
| `standing`, `automaticResume` | App metadata only, no stronger act/run/effect inference; automaticResume always false |

Root scope requested after core checking: wire this API into its actual recovery status and render live-loss and prior-session observations with the provided labels/limits, retaining the current HomeSession and separately selected native-history generation. The generic status consumer must not call flush or make queued rows look durable. Child/shared editing has not begun here.

## Prepared controls and execution boundary

Six source-connected tests in `execution_custody_tests.rs`: native source→actual ledger→loss/reopen projection without UI polling; terminal/item completion and foreign receipts; missing-index hot-only/status-read no write; busy writer and preserved P/tags under Q; actual append failure/restoration with exact once rows; delayed old-generation row versus newer cold observation. They use synthetic source fixtures and owned filesystem storage, no supplier subprocess/model. Custody output is checked against an exact unchanged copy of the accepted schema (SHA below). Existing retired queue tests remain mandatory affected coverage, not reimplemented or claimed run here.

Parser commands used `rustfmt --edition 2021 --emit stdout` for helper/recovery/tests and additionally `--config skip_children=true` for hosting; outputs were redirected to private parser files. All returned exit0. This parses syntax only and does not compile, validate schemas at runtime or establish tests passing. First compiler/test failures must be retained when the Parent grants Cargo. No such failure/output exists yet.

## Original pre-review source seal

- `src-tauri/src/hosting.rs` — `412a6f8b70c5ff6279d65f12c9ae56e63eb39489dc2de64ad19de451e0e13563`
- `src-tauri/src/recovery.rs` — `271fa3d80aac4f010026bc9073e018ca11c74e47493d34e7037d9a5cce9e3429`
- `src-tauri/src/execution_custody.rs` — `a03a27517a804b577ab8f077728c82bfc3cf1f26a295adb9df956bf173f5bf7b`
- `src-tauri/src/execution_custody_tests.rs` — `0586ca2b71af09584fa4cfb04da8e55951953c990f4412e8487d763b1659e7ed`
- `src-tauri/resources/runtime_core/recovery.custody-event.schema.json` — `033398508abc813e90aee0a074a18cb91bd59be88b6991111504ae5662653773`

Baseline:
- `src-tauri/src/hosting.rs` — `c8fcbfa53c7e3db24fc771c9dc883d8bfd6481512f6d06ecc39164bff71a92f3`
- `src-tauri/src/recovery.rs` — `f0fff309d2f8eec23046b5349e4969308ef26319a4e5b6eedf46b3c4da50bc31`

Private patch SHA-256 `e59c64fd2c0892b2aea46debfb8b663923ae117538deca5952ed99ff35a921a4`.

## V6 original failures and bounded repair — actual checked successor

Read `reviews/V6-RECOVERY-CUSTODY-CORE.md`. Original exact reviewed bytes/patch/manifest were preserved in private `original-v6/`; original source plus added regression vectors are preserved in `original-vectors/`. No original production source was edited until the new controls were written and executed.

First compilation succeeded (existing warnings retained). Original controls: `original-compile-controls.log` exit101, six original checks pass and RC1/RC3 fail with respectively “known item pointer disappeared” and a wrongly live u tuple. `original-rc2.log` exit101 fails on the actual cross-session existing-index→`bind_attachment_context` path because the reader selected a row without the new tag. These failures are preserved, not narrowed. Original binary was not separately copied before the repair rebuild; original source/test bytes, commands and logs are retained, and the final checked binary is preserved.

Repairs:

- **RC1:** all known open item IDs/types are written to existing openItems independently of liveTurn, including competing-turn pointers. No live turn is inferred from item/started. **Exact residual source fit:** ledger0.2 has no per-item turnId field. The full thread/turn/item relation survives in live/source custody; its cold per-item turn association cannot be faithfully reconstructed from this unchanged ledger. The API reports `openItemCorrelation` on every historical row. This is explicit evidence loss/format limitation, not full cold PI-6 fulfillment. If that full cold association is required in this production unit, a named accepted representation/schema decision is needed; no invented REC tag format or inferred liveTurn is used.
- **RC2:** metadata append session is distinct from the generation of the execution observation. Ranking uses the latter's session/counter; a valid current-session tag row retaining old lastLoadedGeneration is no longer discarded. `historicalConversations[].metadataIndex` separately preserves the latest appended metadata row, and `.executionGeneration` identifies the actual execution source. `index` remains the selected execution-bearing row; the two originals are not silently rewritten into a synthetic combined ledger row.
- **RC3:** the reducer receives the turn/completed source marker. A contradictory inProgress payload does not create live custody or admit late items; it produces an explicit limit, leaving the original source bytes unchanged.

The two original test functions added to the dedicated test file and the RC2 actual-writer function in Host were preserved unchanged through repair. Three additional checks cover production stop/quit cause versus a merely clean end, separate home equal labels and retained fork metadata, and absent/legacy history limits. Home/fork reader vectors are expressly constructed metadata inputs; they do not prove native multi-home behavior.

Actual final results: 11/11 dedicated custody controls pass; RC2 actual writer 1/1; existing explicit-context3/3, App-custody7/7 (including actual retired queue and IO failure), original Host terminal1/1, prepared-turn terminal1/1, REC ledger/mapping10/10, NativeView5/5. Thus **39 distinct final checks pass**. The focused repaired 8+1 predecessor passes are not added to that total. No broader suite, native App or supplier qualification is claimed. Existing affected IPC fixtures use their own bounded local cat/pipe arrangements; no Codex, external host or model was launched.

Current API adds `metadataIndex`, `executionGeneration`, and `openItemCorrelation` to each historicalConversations row. Root must show metadata and execution provenance separately and preserve the correlation limitation. The API still only reads owner state; it does not flush/append/send. Root implementation remains unstarted in this child's scope.

All commands, exit codes, source/log SHA-256, known Cargo environment and toolchain versions are in private `repaired-manifest.json`; `affected-results.json` retains direct checked-binary commands and results. `private-app-sources.sha256` inventories the copied actual build inputs. `checked-lib-tests` is the exact final retained test binary. `recovery-custody-repaired.patch` is the current source patch. Shared Cargo/source lane is released after this return; maintained product bytes still match the original baseline.

### Repaired source seal

- `src-tauri/src/hosting.rs` — `45bd26eb798db9df04a639213de7702bedad4ef89c962d521b146ab92cc2406f`
- `src-tauri/src/recovery.rs` — `47b271401eccc1775ee3137c0b9d4faa31e163356d1ff63d49713b1825842c6f`
- `src-tauri/src/execution_custody.rs` — `457b46849f2bd6aa21c10252799f5998e8936b2a710fca0775dc9a70aaf275fa`
- `src-tauri/src/execution_custody_tests.rs` — `52f2cd75128143393d71f2336ba8d1fd78c1df308ec2e5f31464baf2b4a1e855`
- `src-tauri/resources/runtime_core/recovery.custody-event.schema.json` — `033398508abc813e90aee0a074a18cb91bd59be88b6991111504ae5662653773`

Patch `2cdc85c9a64697ae0819807a32e66aa0ebba3a1a53caa35988a3fe5e0fe8b885`; retained binary `96f0ce63c28ffdb3c8daa3a1f0c64ff07c2ae88cc9535a60f969d71310223c50`.

## Adopted ledger0.3 — private RC1-COLD draft (historical preparation)

Parent supplied `changes/CC-REC-ITEM-TURN-SOURCE-ADOPTION.json`, independently READY V6-S1. Read the exact adopted §7.2 and verified every adoption-manifest source hash. This is explicit new technical source basis, not retrospective amendment of the previous0.2 evidence. The previous partial source/manifest/patch are retained in private `pre-cold-0.2/`; original V6 failures and the39-check partial successor remain intact.

Privately copied the exact canonical0.3 ledger schema, exact archived0.2 schema and six adopted examples into runtime_core, and updated its MANIFEST source pins. No maintained product/resource write occurred. Custody-event0.2 is unchanged. New source-owned pointer rows now retain each actual known turnId with itemId/type, independently of liveTurn; the existing full-generation/thread scope and `(turnId,itemId)` map remain the identity boundary. Item-only events still do not create restart live work.

The Root API is unchanged in signature and adds `historicalConversations[].openItemAssociations[]`: generation (full original tuple), home, threadId, turnId (null only for absent historical association), itemId/type, per-item correlation label, fullTuple (null for missing turn), and pointer-only standing. `index` stays the original persisted row. `metadataIndex` remains distinct latest append provenance. `executionGeneration` remains the execution source. No association is backfilled from liveTurn or another source; unknown generation rows remain unjoined with their existing limit. `openItemCorrelation` now describes this per-item rule rather than asserting that all ledger rows lack correlation. Root must render known and unknown per item and cannot treat either as native content/current liveness.

Four additional cold03 controls are written: actual Host item-only/competing-turn source→queue/ledger→reopen exact tuple; same item label and completion/terminal isolation across turns; mixed known/legacy absent association beside liveTurn without migration; exact six adopted schema outcomes plus old-reader rejection. Three parser checks pass. **No Cargo/compilation/tests have run on this0.3 successor**; Parent still owns that lane. Earlier39 passes do not cover it. The older-reader boundary remains explicit:0.2 rejects known-turn rows; preserve files on rollback, no stripping or automatic downgrade.

Current private `cold03.patch` and `cold03-manifest.json` freeze the successor and adopted source provenance. Required next steps are permitted execution, original reviewer backcheck, and Root actual consumer adoption; source adoption alone closes no RC1-COLD or whole-core obligation.

### Ledger0.3 draft seal

- `src-tauri/resources/runtime_core/MANIFEST.json` — `3fab962fbc308f2b63759e5c76d6958de7004cacf4b9bf5fbd3e40c79b67e92d`
- `src-tauri/resources/runtime_core/recovery.app-ledger-entry.item-turn.competing-turns.valid.json` — `34a04a4fb66c00669f9f78be4dde128714e05412c792fad0fd3dd8a69ae03abd`
- `src-tauri/resources/runtime_core/recovery.app-ledger-entry.item-turn.empty-turn.invalid.json` — `bcd7ca07f8f0f7be8d6d870dbb61aef844b8a1387ccd8337d66c07b348fa1d4d`
- `src-tauri/resources/runtime_core/recovery.app-ledger-entry.item-turn.item-only.valid.json` — `73a9c24b612b2cd9b6d6bebc45eb2304bf6e33fc0dac8866495330c9b763d88e`
- `src-tauri/resources/runtime_core/recovery.app-ledger-entry.item-turn.legacy-unknown.valid.json` — `b961aab3df10a904820b71245f2dbd5df98ffe067291130995f8f96ba7355c01`
- `src-tauri/resources/runtime_core/recovery.app-ledger-entry.item-turn.null-turn.invalid.json` — `a5c0e830c894c0214ebfe4ac83fb136a99dea3a3064aa4cacc8356130129643a`
- `src-tauri/resources/runtime_core/recovery.app-ledger-entry.item-turn.payload.invalid.json` — `20be8a6b953c00e441aced9640e68fcd4a99932cf8e79e5c1ac0220825286510`
- `src-tauri/resources/runtime_core/recovery.app-ledger-entry.schema.json` — `8a400991244e6dc389f4159bafb65f6486d4b2609ba0a92d030469c434e0a81b`
- `src-tauri/resources/runtime_core/recovery.app-ledger-entry.v0.2.schema.json` — `3f1d7f27f68a523c459ebcb9ce3dcd40a5de54fc4b9b16d20fd4e6b4c3f05c67`
- `src-tauri/resources/runtime_core/recovery.custody-event.schema.json` — `033398508abc813e90aee0a074a18cb91bd59be88b6991111504ae5662653773`
- `src-tauri/src/execution_custody.rs` — `a9d95f8fb19efe5072a07fd090f34e2f2d90444e3838fbc47594d8ac637bbffd`
- `src-tauri/src/execution_custody_tests.rs` — `976844fa75577ab919b80def97f9622c9ce476fb26e36fddece58d6a5da28257`
- `src-tauri/src/hosting.rs` — `45bd26eb798db9df04a639213de7702bedad4ef89c962d521b146ab92cc2406f`
- `src-tauri/src/recovery.rs` — `2e3c52c8fbc02b92067310a2a9caca9bfbd241ac99c79d49e1285c766014687f`

## Ledger0.3 actual checked freeze — lane released

Parent explicitly released the copied-UI-bundle Cargo lane. On the frozen0.3 source, first compilation and all15 dedicated custody controls passed (exit0); no0.3 compiler/test failure or repair occurred. Canonical log `cold03-first-controls.log` retains existing warnings and the actual result. The same source then passed28 affected checks: actual RC2 writer1, explicit-context3, App-custody7, Host terminal1, prepared-turn terminal1, recovery10 and NativeView5. **43 distinct checks pass on this0.3 candidate**; the previous39 on0.2 are separate historical evidence, not added again.

The cold tests observe actual synthetic Host pointer production through the real immutable queue/ledger and reopen projection. Known item-only and competing-turn associations retain exact original turnId, including identical item labels in distinct turns; matching item/turn completion removes only its tuples. Legacy absence stays unknown even beside liveTurn, with no migration/backfill. Item-only input creates neither liveTurn nor restart live-work. Exact adopted schema/legacy examples retain their stated validity and older-reader rejection. These are own-code/format observations, not a native supplier or UI witness.

Immutable review handoff: `/tmp/chirality-rec-custody-astra.bo0pfG/cold03-checked/app`; its `CHECKED.json` binds source seals, actual known environment/command/cwd, log hashes, all results and retained executable hash. `APP-SOURCES.sha256` covers the complete copied build-input tree, and `cold03.patch`/`source-adoption.json` retain patch and accepted-source provenance. Exact checked executable remains `/tmp/chirality-rec-custody-astra.bo0pfG/cold03-checked-lib-tests`; affected checks ran that preserved binary. No source file changed between draft seal and execution freeze. Original0.2 fail/repair artifacts remain untouched.

The Cargo lane is released to Parent. Current maintained Host/REC still match the original supplied product baseline; no maintained product/schema resource or shared Root source was changed by this TASK. Request original reviewer backcheck before RC1-COLD/core closure, followed by the sole Root receiver's actual integration and independent review. No further compile/fixture activity is running.

Checked binary SHA-256 `3239f1a96bdc94be14ac2d6cbc73be0303397fbf88ccbf74d6d28a8b7f4681f2`.
