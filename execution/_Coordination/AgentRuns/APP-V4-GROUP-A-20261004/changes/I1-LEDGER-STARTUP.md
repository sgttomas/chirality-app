# I1 App-owned recovery ledger startup — bounded source/test adoption

2026-10-05. TASK `/root/group_a_execution/runtime_integration`, parent `/root/group_a_execution`, delegated-harness-native descendant; supplied gpt-6.1-sol/medium, no descendants. Scope: lib.rs/App.tsx/runtime_session.rs, new tests/recovery_startup.rs and this evidence note. Consumes actual completed V3-I4-OBSERVATION-INTEGRATION READY and V2-I1-REC-RT READY, with V0-REC-R9-LEDGER/V0-REC-RT-LINK placement/mapping. No Host/native_requests/recovery/Design/schema/dependency/Git/instruction edits. Root/TASK/v4 LOOP basis and preceding consulted sources remain recorded in I1/I4 integration returns; RECOVERY §7 storage/error obligations and current configure_recovery/start interfaces were read for this unit.

## Actual startup wiring

The App resolves its own host user-data directory through app.path().app_data_dir(), independently of supplier configuration and instruction-seeding success. `RecoveryStartup::initialize` selects only `<App-own-user-data>/runtime/recovery.ledger.jsonl`, calls the existing actual `Host.configure_recovery`, and retains the real success/error result in main-process startup state. Setup initializes it synchronously before the first supplier spawn. Both automatic and manual start also use `start_with_recovery`; its mutex/attempt guard makes initialization exactly once for this App session, never a second ledger/session_started when a window/start action repeats. A failed attempt is retained; another start does not silently reconfigure, retry after supplier start or relocate. A new App process may attempt its same configured location again.

A resolved App-owned path must be absolute and outside the configured Codex home (existing ancestors/symlinks resolved for the comparison); ambiguous relative-home separation is a visible recording limit rather than a Codex configuration change. App root/runtime/ledger symlink redirection is refused and preserved. Unavailable resolution/storage, readonly/unwritable files, malformed/nonconforming or unterminated history all expose their actual error, with no fallback to Codex home, project RS records, run evidence or another user-selected location. Existing evidence is not deleted, truncated, rewritten or treated as a new empty history on refusal.

The helper creates the needed App runtime directories and lets the existing schema-gated core append its pointer-only session entry with file-data sync. It then syncs the ledger parent and each newly created directory's parent before reporting configured. `directoryPublication=sync-calls-succeeded` means those actual OS calls returned successfully; no physical crash/storage qualification is inferred. If a later directory publication call fails after Host accepted the ledger, state remains initialization-failed with hostConfigured=true and directoryPublication=not-confirmed, preserving the explicit recording limit rather than hiding a partially configured Host.

Initialization errors are not propagated as supplier-start suppression: the shared helper unconditionally calls its start operation after retaining initialization status, and returns that operation's own result. Existing supplier protocol handling/replies remain with Host and are not gated by ledger initialization. This unit's synthetic starter callbacks demonstrate that control flow; it does not claim a new actual supplier reply/network witness. Missing supplier configuration remains its own independently reported error.

## Status/UI and custody limits

`host_status.recoveryInitialization` now exposes actual state (not-initialized/configured/initialization-failed), hostConfigured, selected path display/native-byte identity, pathDisplayLimit, existing/new/not-established file state, configurationError, directoryPublication, blocksSupplierStart=false and App-observed/no-native-human-act-proof standing. This startup-owned configuration error is retained even though failed Host.configure_recovery does not set Host.recoveryPersistenceError. Later runtime persistence errors remain a distinct field.

The App shows selected ledger location and actual initialization/error state, with a visible alert that ledger failure does not block native processing and App recovery recording remains limited. Full initialization/historical pointer state is inspectable. Non-Unicode display is labelled lossy; all file operations use the retained native PathBuf, not the display string. Startup records and earlier request summaries remain ordinary App-observed pointers; earlier requests are non-answerable, never promoted into the fresh live register. No native payload/question/secret answer/credential copy, retention/deletion rule, new human act, native capture proof or trusted cold replay is introduced.

## Checks on the actual assembled source

Manager granted the serialized offline Cargo slot. `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test --offline --test recovery_startup --test runtime_integration --test external_observation_integration`: compile/command exit 0; **6/6 startup**, **10/10 I1**, **4/4 I4**, 0 failed/ignored. Times 0.10/0.17/0.12 s. Only an unused test import was then removed; focused startup rerun passed **6/6**, exit 0, 0.08 s, no warning. One intervening root-directory Cargo invocation had no manifest (exit101) and was immediately rerun in src-tauri; it did not execute a test or indicate a product failure. Shared implementation/source was unchanged during that test-only cleanup. Cargo slot released after completion.

Tests execute actual Host.configure_recovery and real scratch-file/schema/directory-sync mechanics through the shared starter helper. Starter callbacks are explicitly synthetic (no supplier binary/process). Covered: initialization before starter observation, exactly one session append across repeated starts/no relocation, malformed-tail refusal with bytes preserved and starter still invoked, unresolved root/Codex-home collision/file-as-directory failure, actual readonly existing-ledger failure under observed **UID 501** (not the privileged-euid skip branch), preserved historical nonanswerable pointers and native payload exclusion, and runtime symlink refusal with no alternate file written. Unique scratch folders are removed after tests; no live App-user-data/Codex-home/credential storage was read or written by these tests.

Transient SSR renders the actual App component with an explicitly synthetic initial host-state fixture and stub native IPC. Exit 0: configured/path/native-byte and sync-call status visible, historical nonanswerable flag preserved, failed status/error alert visible and independent-native-processing limit stated. It executes no native start/window/IPC. Frontend tsc --noEmit exit 0; diff check passed. Source/test fingerprint table below freezes the final candidate; no shared source changes after these results.

## Remaining responsibilities

Focused independent startup/source review is required before fan-in. Physical application startup/manual-start/window/native picker/confirmation, live supplier/protocol behavior, crash/power-loss/filesystem durability and other-platform directory publication are not qualified here. On targets where directory sync cannot be established, that failure is explicitly shown. Complete quit/session accounting, conversation/run/tag/recovery history reads, multi-home lifecycle, userVerification device flow, Codex history reconstruction, protected capture/SEAL-2 and trusted human-act cold replay remain separately unfinished. Existing I1/I4 native/model/host-origin/currency proof limits are retained. This adopts the named technical ledger startup contribution; it does not complete Group A, pass a stage gate, grant acceptance or release the product.

## Frozen startup candidate

| Project-relative file | SHA-256 |
|---|---|
| `app/src-tauri/src/lib.rs` | `6e2e6cfe69a266b472dcc49791c1ce1b27efe781a02985d0ed908d0deafda274` |
| `app/src-tauri/src/runtime_session.rs` | `0490c69820e41153d07bc8e56ac7ab7130a246fa71294118cdfffc3c448f5232` |
| `app/src/App.tsx` | `5022b98a8d703142fbc735ac46e1831b39b438e8adc8e7ae0d78e70c53219ee8` |
| `app/src-tauri/tests/recovery_startup.rs` | `778562fa9f550014753e6b31b91e05eae2c1b8925ac007fcb3f7a3a100b69a78` |
| `app/src-tauri/tests/runtime_integration.rs` | `18ed6496863eb76cc950c96e162ddb955139a92d776a313c3a9e7a4591195ee2` |
| `app/src-tauri/tests/external_observation_integration.rs` | `1a59b14714d7be5a200d2848a0b15b71c8f71dea27b330659e2741548221eae8` |

## Named source origins

| Repository-relative origin | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V3-I4-OBSERVATION-INTEGRATION.md` | `1aa75274b2957f5e5c7795c141d020f129d98dfd572fbd3fe0cb3e4169f1d985` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V2-I1-REC-RT.md` | `e0af5cdcac9683c82482b2f4b4cf8dbc859adead7c477fbd9adef0b2eaf3a45f` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V0-REC-R9-LEDGER.md` | `6b142b530e47418c659c5687a38196f62b37f247f3e971034cccfffdeb5ba34d` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V0-REC-RT-LINK.md` | `2e0ed798040f8a71a9f89c6ba5101f1a819a1db7d8a8716316c6fce46a8d4607` |
| `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` | `71ec04b2a67893e133d94c756a3bada17eedcc783ea82d0ffd9d16f44d1ca97a` |
| `projects/chirality-app-v4/app/src-tauri/src/recovery.rs` | `4aefbdc26f4956a50788a21089c650ce80a4509727105485ce91d036396d49d0` |
| `projects/chirality-app-v4/app/src-tauri/src/native_requests.rs` | `5879e6d034820e5d26c6dea1a4947ab851a39c0598aa675753ab6948e3030dbe` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md` | `9b443fbc5e7fc617e51e18c4cb8aec7af0d429bc7fefe3e0ec9e52f968aa79d1` |
