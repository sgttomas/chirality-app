# Parent-only opt-in production backend smoke

Prepared 2026-10-05 by TASK runtime_integration for WORKING_ITEMS/Parent. This is a real Host test, not a transport double. **Author/children must not run it or read authentication storage.** Source preparation and explicitly granted `--no-run` compilation are the only child checks. Product files/dependencies are unchanged.

`tests/native_backend_smoke.rs` contains one `#[ignore]` test. Ordinary Cargo tests do not execute it. Even explicit `--ignored` fails before path lookup/auth/supplier access unless both exact gate values below are present. These are execution guards, not verified actor identity or authority; Parent instructions still govern who may invoke it.

## Parent's existing authorization/configuration

Parent exclusively supplies the approved stock 0.160.0 binary and its already authorized, originally mktemp-created auth home. The known minimal private config uses file credential storage, skeleton_local default, plugins/analytics off and no hooks/imports/auto-approval configuration. Parent alone adds/configures medium and restores its privately retained config bytes afterward. The harness makes no direct config/auth file read/write, sign-in, credential copy or deletion in that home. Stock Codex itself uses its credential/config/history custody there when Parent executes. Native supplier history/logs may be written there; they are not scratch App ledger data and remain Parent-controlled.

Parent clears inherited CODEX_*/OPENAI_* overrides without exposing their values, keeps its native permission choices, chooses the actual configured provider, and supervises the process group with a hard outer deadline. No harness-added approval/sandbox/plugin/effort overrides are used. Production Host's existing analytics session setting remains unchanged.

## Exact invocation — Parent only, not executed by author

Use an immutable reviewed source copy and its approved offline cache. Set these values privately; do not echo auth paths/configuration or enable shell tracing:

```sh
CHIRALITY_RUN_NATIVE_BACKEND_SMOKE=parent-authorized-0160-one-greeting \
CHIRALITY_NATIVE_SMOKE_CONFIG_ASSERTION=parent-controls-medium-and-native-policy \
CHIRALITY_NATIVE_SMOKE_BIN="$task_parent_approved_0160_binary" \
CHIRALITY_NATIVE_SMOKE_AUTH_HOME="$task_parent_authorized_auth_home" \
CHIRALITY_NATIVE_SMOKE_PROVIDER="$task_parent_configured_provider" \
CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home \
CARGO_NET_OFFLINE=true \
cargo test --offline --locked \
  --manifest-path "$task_immutable_candidate/app/src-tauri/Cargo.toml" \
  --test native_backend_smoke parent_authorized_stock_native_one_greeting \
  -- --ignored --exact --nocapture --test-threads=1
```

The test requests **gpt-6.1-sol**, requires the native thread response to report that exact model/provider and **reasoningEffort=medium**, or fails a named gap before sending. An absent effort report is not silently inferred from Parent's assertion. Main-binary SHA must match `112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b` and the native label must be `codex-cli 0.160.0`; full supplier qualification remains unverified-development.

The production path uses fresh private system-temp workspace and App guidance/ledger; its Codex version-probe home is created by actual `mktemp -d <owned-scratch>/version-probe-XXXXXX`, not create_dir; seeds/composes HELP_HUMAN guidance, initializes the actual pointer ledger, starts actual Host, creates a native thread, sends exact text through the production conversation helper/Host API, and receives real native frames through the production observer/reducer. No App window, Tauri IPC, external host document/import, reserved act, userVerification, enrollment/key/seal or dispatch operation is exercised.

Exact prompt:

> Reply with exactly: Hello from the synthetic backend smoke. Do not use tools, read files, delegate, or take external actions.

## Acceptance/publication and cleanup limits

Success separately requires observed native userMessage echo of that exact text (client write alone is not receipt), an actual native terminal event with completed status, and the byte-exact synthetic greeting. All native item/snapshot/terminal evidence is bound to the selected full generation, thread and native turn ID; a same-thread foreign turn fails, never supplying missing selected-turn evidence. Reply equality does not trim or normalize; the actual observed string is published only after exact equality. If native text echo is not provided by this path, the test reports that precise gap rather than claiming receipt. It checks one App-observed ledger session row, non-answerable historical custody and absence of prompt/reply payload in the pointer ledger. Role composition/supply identity is recorded; **model role adoption/enforcement is not established**.

Only allowlisted synthetic greeting, terminal/model/effort/role/source identities and bounded ledger/outcome facts print. No raw journal/account snapshot/reasoning/supplier prompt/config/auth material is printed or written by the harness. Unexpected response text is never published. Compile-time hashes cover the test, Host, runtime helper, native requests, lib and lockfile; Parent matches them to its immutable candidate. They identify this backend slice, not a full App/UI/release artifact.

Any native request, unknown/tool/delegation item or unselected conversation activity fails without authorizing it. The harness never calls a person-answer/grant operation. It may interrupt an actually observed live turn, then uses production process-group stop. Standard Host service/error replies remain its existing behavior. Native auto-approval/hooks can act before observation: **prompt+polling is not pre-execution tool enforcement**, and cannot guarantee zero side effects for arbitrary configs. The Parent's known no-hook/non-auto-approval fixture bounds this run; if guaranteed zero effects under arbitrary config are required, do not run this probe.

Normal handshake/thread waits use the production 15-second config limit, turn operations retain production 20-second waits, terminal polling stops after 45 seconds, and normal process-group cleanup uses production bounded stop. Host's synchronous version probe/filesystem operations do not supply a hard whole-run deadline. Parent must supervise that deadline and track/stop the actual owned supplier descendant groups: Host uses process_group(0), so the supplier PGID is distinct from outer Cargo/test. Killing only the outer group is insufficient. Normal Host.stop cleanup and Parent hard-deadline supervision are different facts; a hard-bound/kill-path qualification is not claimed. Private App scratch is removed on ordinary return/unwind; authenticated supplier storage is never cleaned by this test. No filesystem crash/power-loss proof follows.

This real supplier/configured-provider path does not cryptographically attest the upstream model, prove UI/IPC/native confirmation, full role adoption, tool/request/interrupt paths, source qualification or Group A completion. Parent alone owns live execution and records its actual result. Preparation/compilation is never described as a successful live smoke.

## Original proposed preparation — preserved, not a live result

Manager-granted isolated compilation: `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test --offline --locked --no-run --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml --test native_backend_smoke`, exit0, 2.98s, no warnings. Test executable produced; **zero tests executed**. No auth/path gate lookup, supplier/model/window/network action occurred. Slot released. Source remains frozen for independent review and Parent-controlled invocation.

| Preparation-time source; Parent must match compiled report at invocation | SHA-256 |
|---|---|
| `app/src-tauri/tests/native_backend_smoke.rs` | `162a48fdaeb5daa14c2f9c5feb6dbba62ab3f91efe78b0bcc92fd5d49340c50e` |
| `app/src-tauri/src/hosting.rs` | `767cc2681197e760cbae8af1cb54cb998cbedaf0d7a6eecc17249743a6b381a4` |
| `app/src-tauri/src/runtime_session.rs` | `c96db03894b242f78a7029b5e04063f639fb02dc13b0c8de59de4b3e9e0e88b9` |
| `app/src-tauri/src/native_requests.rs` | `bb3317458e40ade1e623f86ed771c196a97e07ca7e4daa8a89931b3ea6ee6992` |
| `app/src-tauri/src/lib.rs` | `e1897437ab1c7f07c823d892e2c8102d4370503deb7745eed531f930fdf8e7e3` |
| `app/src-tauri/Cargo.lock` | `2fad2d658b3ffaf7b3973d5ab7da693788613f7462eaeca9d4b6b9ad826f7012` |

## Narrow successor corrections — source prepared, no execution

Original proposed test SHA-256 `162a48fdaeb5daa14c2f9c5feb6dbba62ab3f91efe78b0bcc92fd5d49340c50e` and its compile-only/no-live standing above remain historical. Root/reviewer findings: mkdir Codex probe home did not satisfy LOOP's explicit mktemp-d rule; trim-plus-constant publication silently normalized reply; same-thread sibling turn could supply echo/reply for an empty selected terminal. Successor uses actual mktemp-d, byte-exact observed equality/publication and full selected generation/thread/turn guards at every accepting item/snapshot/terminal path. Two pure tests cover the original sibling-turn case and whitespace-negative oracle, with no native/model/filesystem/auth path execution.

Successor compilation/pure checks await the granted slot. Host steering review and its actual frozen source pins must be refreshed explicitly before Parent invocation; the preceding source table is historical and not silently rebound to current WIP. The live ignored test remains Parent-only, proposed and **never executed by author/children**.

Parent relayed that the independent reviewer executed the original 162a pure turn/reply cases and observed **0/2 conformity passes** (foreign-turn evidence and whitespace normalization violations). This author did not rerun the original; those actual reviewer facts are retained, not erased by successor assertions. Parent also reports a local-only watchdog dry run using owned PID birth/parent/group tracking, including a separate child PGID, with a hard 150s bound and controlled medium restoration/env clearing; no Codex/auth was used in that dry run. This is the Parent's specific supervision arrangement, not generic OS isolation or evidence that an outer-group kill reaches the supplier.

## Frozen repaired successor — actual steering basis deliberately adopted

Actual completed `reviews/V2-I1-STEERING.md` READY, SHA `6138d0f94e94e8c661c4afb321598537b1ceafa79de0c8882a0fd8918c92aaf4`, releases Host `d20d8ef399911f49f4604fa9530703c91a1f83cf0885e9609885dd12e39f6c75`. These exact digests were checked before this explicit pin refresh. Earlier preparation/current-WIP tables remain historical. No product or shared source was changed by this correction.

Granted successor `cargo test --offline --locked --no-run --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml --test native_backend_smoke`: exit0/5.54s, executable built, no live test. Focused `--test native_backend_smoke pure_smoke_evidence_tests`: exit0, **2/2 pure passes**, 1 live test filtered; no smoke env/path/auth/native/model operations. Cargo slot released. Exact successor test is proposed/frozen for actual independent smoke backcheck; **Parent live invocation remains held until that actual completed return**. A pure pass or compilation is never a live smoke result.

Executable built at `app/src-tauri/target/debug/deps/native_backend_smoke-8b4d768aa29ed2da`. It is not the earlier 162a executable identity. Parent must use the same immutable source and compare the emitted compiled-code pins; this newer Host/guidance path does not silently certify an older PR.

| Frozen repaired source/build artifact | SHA-256 |
|---|---|
| `app/src-tauri/tests/native_backend_smoke.rs` | `3e88cbeccf99d0e9865f7f1e19ccef979d2d63a8eb136bfd20ea0b8a578a3f3e` |
| `app/src-tauri/src/hosting.rs` | `d20d8ef399911f49f4604fa9530703c91a1f83cf0885e9609885dd12e39f6c75` |
| `app/src-tauri/src/runtime_session.rs` | `c96db03894b242f78a7029b5e04063f639fb02dc13b0c8de59de4b3e9e0e88b9` |
| `app/src-tauri/src/native_requests.rs` | `bb3317458e40ade1e623f86ed771c196a97e07ca7e4daa8a89931b3ea6ee6992` |
| `app/src-tauri/src/lib.rs` | `e1897437ab1c7f07c823d892e2c8102d4370503deb7745eed531f930fdf8e7e3` |
| `app/src-tauri/Cargo.lock` | `2fad2d658b3ffaf7b3973d5ab7da693788613f7462eaeca9d4b6b9ad826f7012` |
| `app/src-tauri/target/debug/deps/native_backend_smoke-8b4d768aa29ed2da` | `8533812017aec101f14e6e3f79d2b2b2350b5845589b133fb29b774e11bb45a0` |
