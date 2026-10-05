# P0-HOST — hosting product propagation

Status: implemented and checked; ready for independent review and manager integration. No qualification, owner acceptance, release or whole-Group-A closure claimed. TASK `/root/group_a_execution/hosting_propagation`, delegated-harness-native child of `/root/group_a_execution`; no descendants. Writes only hosting.rs, handshake.rs, hosting_contract.rs, maintained supplier resource mirrors and this return. No credentials, authentication, live provider/model turn, download, Git mutation, Design or governing instruction amendment.

CI-2 full generation identity is `{appSession, home, spawnCounter}` throughout lifecycle, request, journal, exit, snapshot and thread exports. Secure fallible session minting on first start gives each Host its own session; home is an opaque hash of the App-owned path, never the path itself. Pipe readers retain the full owning generation; foreign session/home/counter frames cannot settle pending current requests. Integer caches stay internal. Pre-spawn null is retained. Handshake delivery holds all frames until ready and retains receipt order, including native initialize responses.

CI-7 normal three-part checks remain required: exact observed label, content comparisons and exact generated bundle/manifest hashes. Current expected full qualified distribution identity is absent, so successful current checks stay unverifiable. `expected_sha256` is only a development main-binary assertion; known mismatch always refuses even with development enabled. Explicit development start uses LT-24, retains unchanged verification reason, and carries unverified-development through ready/version/lifecycle/thread/stop. No matching main binary can emit verified/LT-04. Maintained supplier resources are byte mirrors of reviewed SUP1 compact experimental root/v2 and manifest; no missing native files are claimed committed. Public supplier pin now 0.160.0; generated identity carries full exact digests.

CI-8 snapshot/thread diagnostics disclose model Responses websocket prewarm at thread-start before a turn. Historical observation source0.158.0 remains separate from current child0.160.0; snapshot does not pretend to observe sockets and states sampling limits. Startup entries preserve plugin/provider/account dependence. No provider config changes, network veto or new model default. `thread_start_selected(cwd, model, model_provider)` sends both explicit native fields and records requested versus supplier reported thread scope. Compatible legacy `thread_start(cwd)` returns truthful no-selection refusal. Parent must wire blank user-choice model/provider controls to new method; no silent configured default.

Offline double integration tests cover same home/counter across Host instances, later home/spawn identity, unchanged early native frame, ordered journal, explicit selection/refusal, matching binary remaining development, mismatch refusal, and absent explicit development authorization. Unit negatives exercise foreign session/home/counter/bare-integer response rejection while current pending request remains unresolved, then current full identity correlation. Real handshake uses scratch mktemp homes, local unavailable model/provider stand-in, plugins/analytics off, no turn, socket check and preserved old negative assertions.

## Source reading identities

- `AGENTS.md` — `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`
- `agents/AGENT_TASK.md` — `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`
- `projects/chirality-app-v4/loop/LOOP_INIT.md` — `45c23cf477e23aff1d0152189caf7e8ebfb53eca42e3a1fae87a06af8c197f28`
- `projects/chirality-app-v4/README.md` — `f1f90e46054a7e1c178736a4fa645ed9edb17538e94cd9329c2bf5e48a5136b8`
- `docs/alignment-manual/README.md` — `31217d30b0d2743bef0d7c1a54bb9a81814d56b24ff0961cf01d9532952e305f`
- `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` — `08ca0e40cd5157574a011bac57d539e77e9007a0d46494785da8b92745391b1a`
- `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` — `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/OWNER_DECISIONS.md` — `57e9412cbbc84862c2658a573ed9390a333ace8400c22bd6a81c8ce0eb77535a`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-H.md` — `b5b4544ae5c5f9983e87c8d044869e4af7906d03332f8821d4e77a7587f50ae9`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V0-H-R1.md` — `210f10cf78082699e0cea35cad088ed556548ebe407ea996035c0518048bb6f2`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V0-SUP1.md` — `28f811b68ebbd18c24086fc8ec45a05421f2bf29211bf5104e614bab5c697b30`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/HOSTING_BOUNDARY.md` — `b01ef84d5fcfd494cbf60c81860c5d0ccd159ccb90598147184b6f8c17475cc5`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Design/ACCOUNT_AND_PROVIDER_ACCESS.md` — `0f177361460a30c52615607457289c1fe275f55264cbe0d95f9c6d4e0ed0ed57`
- `projects/chirality-app-v4/app/README.md` — `a9a764698d351803cf8c8f93cdfdd0bc2e3de0c01e6a20e28525d6fc0e020c7f`

## Execution and checks

Manager granted the shared Cargo slot after P0-ACT source freeze. All commands used the isolated approved `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home` and offline locked mode:

- `cargo test --offline --locked --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml --lib hosting_identity_tests -- --nocapture`: 2/2 pass.
- Same command with `--test hosting_contract`: 4/4 pass, including version-label and actual handshake contradiction refusal (no-version remains distinct).
- Same command with `--test handshake`, using the authorized machine-local 0.160.0 supplier path and expected development binary SHA-256 `112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b`: 1/1 pass. Initialize, initialized, explicit local provider/model thread/start and deliberate stop executed; no turn. Lifecycle was LT-01, LT-24, LT-06, LT-09, LT-17, LT-23. Start-to-thread 684 ms; sampled process-group internet sockets empty; all scratch homes removed. No independent continuous socket monitor or universal no-network claim.

The real handshake exported maintained records for the manager's Node/schema consumer at `app/src-tauri/target/tmp/skeleton-output/hosting-records.json`. Shared helper dead-code warning only; no compile/test failure. Scoped `git diff --check` passed. Cargo slot released after these checks; source held for independent review. Parent owns lib/UI integration and whole-candidate validation.

## Candidate output identities

- `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` — `c645507678c4e8968eb8a97cb4932b6da01247fabff3845dbe7922601560b0b1`
- `projects/chirality-app-v4/app/src-tauri/tests/handshake.rs` — `848bb38c0cd32b36c97e34da09aa59606a7747241170f8c89f01c411571845a2`
- `projects/chirality-app-v4/app/src-tauri/tests/hosting_contract.rs` — `8201fb17ee7a77affa7236b74a4f3004e4fcaf176b175068f53e284f9f2e0e07`
- `projects/chirality-app-v4/app/src-tauri/resources/supplier/0.160.0/MANIFEST.sha256` — `411ea5d47035908768562eecfed33f16e2cb3de944c84c96fd8e70ca7086b8be`
- `projects/chirality-app-v4/app/src-tauri/resources/supplier/0.160.0/codex_app_server_protocol.schemas.json` — `7243ba241962af92ca60581f1a81808ebda4212a800f8b205f54703bcfd508c5`
- `projects/chirality-app-v4/app/src-tauri/resources/supplier/0.160.0/codex_app_server_protocol.v2.schemas.json` — `e77b7d1436a78f431a74b2cb263a862e92ae40d70411bc63835b47ab2168827c`

## Strict lifecycle-schema repair backcheck

Manager's connected Node run identified an unsupported nested `versionIdentity.supplierStanding` member on LT-09. Removed that member only; supplier standing remains in the supported lifecycle top-level, snapshot and thread metadata. Canonical schemas remain strict and unchanged; existing assertions retained. The earlier source hash above is historical.

After manager granted the repair Cargo slot, reran the real offline 0.160.0 handshake with the same isolated approved Cargo cache and exact supplier binary assertion: 1/1 pass, 720 ms start-to-thread, empty sampled internet sockets. Then `npm test` under the same environment passed all three Node checks, including strict lifecycle/client-record validation; its Rust decide flow passed 3/3 and real handshake passed 1/1. This is the connected receiving check on the repaired hosting output, not qualification. Cargo slot released immediately; source frozen for manager review.

Repaired `app/src-tauri/src/hosting.rs` SHA-256 `a7c1867acea11e4211f74f071b91a9529cbbfe56ead320845c4502790db1d8ac`.
