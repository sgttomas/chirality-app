# V3-I1-LEDGER-STARTUP — independent actual App configuration review

2026-10-05. **READY for bounded startup fan-in. No blocking, major or minor finding.** This verifies actual ledger configuration/start-helper wiring and its retained status/error boundary; no physical App startup, supplier/native or crash-durability qualification is implied.

Independent TASK `/root/group_a_execution/aac_contract_review`, delegated-harness-native child of WORKING_ITEMS `/root/group_a_execution`, no delegation. Applied previously read software-code-review skill. Read frozen return, actual lib setup/manual/automatic paths, RecoveryStartup/helper, App status presentation, new startup tests and reviewed ledger/mapping inputs. Only this report written. Manager granted exclusive Cargo for recovery_startup and the slot was released immediately after its independent pass. No network/auth/credentials/model/supplier/native-window use, product/Design edits or Git mutation.

## Exact candidate and preservation

Return `changes/I1-LEDGER-STARTUP.md` SHA `70e5ec7dfe5bb2fad874443bc384cb2862c908654b89ca107e614f328fd5490a`. All six frozen source/test fingerprints match before/after checking:

| Project-relative file | SHA-256 |
|---|---|
| app/src-tauri/src/lib.rs | 6e2e6cfe69a266b472dcc49791c1ce1b27efe781a02985d0ed908d0deafda274 |
| app/src-tauri/src/runtime_session.rs | 0490c69820e41153d07bc8e56ac7ab7130a246fa71294118cdfffc3c448f5232 |
| app/src/App.tsx | 5022b98a8d703142fbc735ac46e1831b39b438e8adc8e7ae0d78e70c53219ee8 |
| app/src-tauri/tests/recovery_startup.rs | 778562fa9f550014753e6b31b91e05eae2c1b8925ac007fcb3f7a3a100b69a78 |
| app/src-tauri/tests/runtime_integration.rs | 18ed6496863eb76cc950c96e162ddb955139a92d776a313c3a9e7a4591195ee2 |
| app/src-tauri/tests/external_observation_integration.rs | 1a59b14714d7be5a200d2848a0b15b71c8f71dea27b330659e2741548221eae8 |

Parent supplied actual retained I4-reviewed predecessor bytes at `/var/folders/0s/50y7rb796d1bqdxmpcz6qg800000gn/T/i4-integration-preserved-uq76e5xj/app/`. Independently read hashes match V3-I4 seals: lib `8b89d003…`, runtime_session `8ac9ff2c…`, App `a6901699…`. Full byte diffs against these actual predecessors show only startup state/configure wiring, the new helper and its ledger-path comment, and replacement of the pending-status UI paragraph with actual ledger/error presentation. Existing runtime view/access/guidance and external native-selection functions, routes and UI remain byte-identical outside those changes. This comparison uses preserved bytes, not reconstructed sources. Host/native_requests/recovery hashes also remain the exact V2-I1-REC-RT sealed core; I1/I4 integration test files are unchanged.

## Behavior and contract assessment

The App resolves its own app_data_dir separately from instruction seeding or supplier configuration, stores that real result and initializes the actual Host before first supplier start. Both automatic and manual starts use the shared start_with_recovery helper. Its startup mutex and attempted flag prevent a second configuration/session_started or relocation during repeated starts; retained failure is not silently retried after supplier start. A fresh App process can make a new attempt at its same location.

Only `<App-own-user-data>/runtime/recovery.ledger.jsonl` is selected. Relative/ambiguous roots or Codex-home comparison, root/runtime/file symlinks and unusable storage produce visible failure with no fallback. Existing ancestors are resolved for separation. File operations retain native PathBuf identity; display is explicitly lossy when needed. Unreadable/nonconforming/unterminated history is refused with bytes preserved rather than treated as empty history. A new file observation is distinguished from a found existing file; no historical request becomes live custody.

The core validates and syncs its pointer-only session append; the helper syncs the ledger directory and parents of every newly created directory before reporting configured. Its label is accurately `sync-calls-succeeded`, not a physical durability witness. If Host accepts the ledger but directory publication fails, configured remains separately true while state is initialization-failed and publication not-confirmed with actual error. No partially configured state is disguised as complete initialization. Other-platform behavior and interruption at these points remain examination obligations.

Startup recording failure is retained but does not suppress the starter callback or substitute its result: start_with_recovery invokes the native-boundary start after initialization and returns the start operation's own result. Host protocol replies remain independent. Missing supplier configuration is still its own error. Actual initialization failure lives in recoveryInitialization even when Host.recoveryPersistenceError is null; later persistence errors remain distinct. App UI shows selected path, real state/error alert and recording limit, without claiming old pointer data supplies native human-act proof. No secret/native-content copy, cold act replay, relocation, retention/deletion choice or common service is introduced.

## Independent checks and limits

From repository root:

```sh
CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home CHIRALITY_SKIP_CODEX=1 cargo test --offline --locked --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml --test recovery_startup
```

Exit 0; **6/6 pass**, 0 failed/ignored/filtered, 0.04s. Actual `id -u` is **501**, so the readonly-ledger test exercised nonprivileged permission refusal rather than its euid0 early return. The tests run actual Host.configure_recovery, schema/file/directory-sync mechanisms and explicit synthetic starter callbacks. They cover before-start configuration, once/no-relocation, malformed tail refusal with unchanged bytes and continued starter, root/Codex collision/file obstruction, linked runtime refusal, readonly ledger and preserved historical nonanswerable/payload-free summaries. No supplier process or native window is exercised.

Author's assembled-source evidence additionally records runtime_integration 10/10 and external_observation_integration 4/4, frontend tsc and synthetic SSR presentation pass. Those broader checks are attributed to the author, not repeated or converted into native witnesses. The wrong-directory Cargo exit101 was an invocation failure before tests; no product failure is hidden. The final unused-import cleanup changed no shared source or oracle.

Return: startup location/configuration/status contribution is suitable for manager fan-in at these hashes. Complete quit/session accounting, conversation/run/tag/native-history recovery, multi-home/account/device verification, physical startup/manual-start/protocol behavior, filesystem crash/power-loss qualification and protected human-act cold custody remain with their existing owners. This closes neither full I1/Group A production nor acceptance/release and adds no approval gate.
