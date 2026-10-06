# V5 workflow witness preparation — independent review

2026-10-05. Reviewer: `/root/group_a_execution_astra/workflow_witness_review`, TASK, gpt-6-astra / low, native delegated descendant of `/root/group_a_execution_astra`. No delegation. Read-only review of the private helper; only this report authored. No Cargo, helper/test execution, supplier, native dialog, authentication, model, network or download activity. No source repairs made.

Disposition: **NOT READY for Parent execution**. Findings concern the private witness preparation, not a blanket reopening of prior product reviews. The a515 concurrent archive failure remains unresolved; an isolated pass does not repair it. Corrected candidate and compiled artifact are still prerequisites.

## Blocking findings

1. **P1 — outer timeout abandons supplier process ownership.** `parent_launch.py` timeout handler calls only `process.terminate()` and waits ten seconds. SIGTERM terminates the Rust harness without running its Rust `Guard::drop`; `hosting.rs:738` places the app-server in its own process group. Killing the harness or its group alone cannot guarantee supplier descendants end. A second timeout also escapes without kill/reap. Normal Guard cleanup ignores `Host::stop` errors and records no surviving-group result. Preserve an owned supplier PID/group identity outside harness memory immediately upon spawn (including the version-probe boundary), provide a Parent-owned timeout/finally kill/reap path for every owned process, and retain cleanup outcome before declaring bounded execution. Do not identify processes by names or kill unrelated processes. This is a private harness repair; no change to production authority is implied.

2. **P1 — launcher can report success without running the witness.** `parent_launch.py` launches libtest with a hardcoded exact filter and trusts exit code alone. Rust libtest exits successfully for zero matching tests; a supplied/reviewed executable without this injected module therefore produces exit 0 and the launcher's native-failed-turn standing despite no journey. Require a matching compiled binding and an actual one-test result plus a fresh, validated `witness-result.json` from this unique root. Missing result must fail. Bind result to the test executable, candidate, fixture, launcher and invocation; a user-entered checksum alone does not establish these relationships.

3. **P2 — claimed HTTP400 causality is not tested.** Fixture line 41 accepts any native `failed` status; launcher logs POST observations but never requires one. A local pre-provider failure can retain the userMessage and pass the native page comparison while no HTTP400 happened. `witness-result.json` then labels the run “loopback HTTP400 native failed turn.” Require an owned provider request/400 response observation and the matching native terminal error evidence, or downgrade the standing explicitly to a native failed-turn source comparison with cause unknown. Preserve the full failing observation rather than adding a retry. This does not challenge the usefulness of real native page comparison independent of error cause.

## Preparation and evidence gaps (must resolve before execution)

- `prepare_compile.py` hashes the copied app after injection and takes the fixture hash later from the original input path. It does not retain an original candidate manifest or prove that the only differences from the identified candidate are the injected module and appended declaration. Retain source-before-copy manifest, copied pre-injection manifest, exact injection diff, hash the *copied* fixture, bind the resolved commit/archive and final binary to them, and reject unexpected drift. It currently makes no compiled claim; this gap is prospective.
- Complete supplier package provenance is not validated by the launcher, only main-binary SHA. Bind the previously approved complete-package manifest and sibling executable inputs before execution; do not infer layout qualification from main SHA. Preserve its historic provenance independently of this witness result.
- Copy/build viability is unverified: the helper removes `node_modules` and `dist`, supplies a minimal Cargo environment, invokes Tauri build, then rejects all source changes. Validate exact copied build prerequisites and intentional generated outputs when the lane is released; retain a failed compilation intact. I did not run Cargo and do not claim a confirmed compile failure.
- Native terminal status, list/turn pagination and packaging have not been exercised. The fixture loads one turns page; absence of its turn on that page fails through production `items_page`, rather than minting authority. A newly created one-turn thread is the intended bounded case; expand paging only if actual evidence requires it.
- Failure diagnostics are weak: most Rust assertions run before result write; keep bounded Host/source snapshots on failure and cleanup so an unexpected request or supply failure is diagnosable. The launch log alone need not retain source receipts.

## Source-path findings that do not require repair

The module is injected into a private copied `runtime_session` test context. It calls real `WorkflowRootSession::select_development_copy`, `prepare_run`, `WorkflowRun::send`, and `check_native_supply`. Production send at runtime_session.rs:4088–4122 uses actual scoped Host typed prepared input and finish; supply at 4123–4208 uses actual history dispatch/receive, accepted observation, Host page mint/revalidation, cursor continuation, seal and WR comparison. No synthetic native page authority, A15 receipt or maintained dated-run include was found. `WorkflowRootSession::snapshot` uses try_lock for runs, so holding the run lock at fixture report construction does not establish the feared snapshot deadlock.

Fresh launcher HOME/CODEX_HOME/TMPDIR, empty workspace and holding copy support isolation from real user homes. They do not prove OS network containment or automatic process cleanup. The watchdog aborts unexpected server requests/tool item starts; it is observation and Stop, not a grant. Source observation, supplied native copy, workflow adoption, registration/A15, and completed workflow execution remain distinct; adoption is correctly unknown.

## Return and next boundary

Manager may commission bounded private preparation repairs preserving these originals. Obtain the corrected source basis and explicit Cargo release; compile only the copied source, retain the exact compiler-artifact executable and full binding, then independently review affected helper repairs and actual compile/result binding. Parent alone executes the reviewed artifact. This review author performed no fixes and cannot serve as independent review of future self-authored repairs. No publication, acceptance, supplier qualification or original archive repair is established here.

## Consulted origins and SHA-256

Root instructions were supplied in the task and checked from their file hash; TASK and skill were read in full. Loop entry, manager/private handoffs and Group A graph were read; manual guide headings and Field Book full text were consulted. Product sources were read selectively along the call path; current runtime_session/hosting had no diff from a515 at review time. No other role bodies loaded.

- `AGENTS.md` — `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`
- `agents/AGENT_TASK.md` — `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`
- `.agents/skills/software-code-review/SKILL.md` — `ee085d589c44f912d11a59eead8edac214f0343761d26b0d33e886a979888bca`
- `projects/chirality-app-v4/loop/LOOP_INIT.md` — `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd`
- `docs/alignment-manual/README.md` — `5eee30d902c57a251bf885f91bfa0481a7834ec6945c3382baf15d2e2980c63d`
- `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` — `2535efe547f2368e06d965d189efc47c7c46f28c2d6fd4777b0b8cece9003fa7`
- `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` — `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3`
- `projects/chirality-app-v4/execution/_Coordination/WorkGraphs/APP-V4-GROUP-A-20261004/WORK_GRAPH.md` — `8bab12b4e735065056a3c59438275b90970edc877f7970f28ba677b3f7a02637`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/MANAGER_ASTRA_HANDOFF.md` — `046e48e9b2b41fe8995237417a08fb91ff216106958d65c6be319918cde36576`
- `/private/tmp/chirality-parent-workflow-witness-lncXTF/prepare_compile.py` — `ed060a77cff38fd7f2edb962e2dfaff08aa1d12392be8b9a09c038977ffdc0d9`
- `/private/tmp/chirality-parent-workflow-witness-lncXTF/HANDOFF.json` — `a39f50ed1f93d427eeb06974994214630451c61b4fb2b70274391f399cfc5ad2`
- `/private/tmp/chirality-parent-workflow-witness-lncXTF/parent_launch.py` — `221efe9a3e994ce6e1ce2db2afd3981aedc67574bdd204484cfe29b044787363`
- `/private/tmp/chirality-parent-workflow-witness-lncXTF/parent_stock_workflow_witness.rs` — `461c512505f48dfbee54cd1aeb08abc42c65af6ac7830c4b385ac52a35682d70`
- `/private/tmp/chirality-parent-workflow-witness-lncXTF/HANDOFF.md` — `ecee5b5c1e0122674444ee08822644124840819d4f18fce9b505751557a4970d`
- `projects/chirality-app-v4/app/src-tauri/src/runtime_session.rs` — `05af3f76da30a02dd425d9de025c623402a2fbdfefcdfc99c5f7201590c041f6`
- `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` — `e5b908ba9635b74ff27c79f4f568c139967aaa4edfa0f9a16dadde50dfe4db34`
- `projects/chirality-app-v4/app/src-tauri/src/native_history.rs` — `5d9a268639399ff70e44b9217c2a317986ddc653d4684e64f40af6acd77922ab`
- `projects/chirality-app-v4/app/src-tauri/src/workflow_catalog.rs` — `88b069dea9a7061e610537349346c51670b5fdbe843dd7640ffaffe28389962f`
