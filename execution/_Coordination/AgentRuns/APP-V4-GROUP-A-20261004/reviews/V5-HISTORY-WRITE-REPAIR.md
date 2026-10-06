# V5 history failed-write repair independent review

2026-10-05. **READY for bounded manager fan-in; no blocking findings.** Parent's exact repaired checkpoint/archive validation remains required before publication. This review neither passes that archive nor closes Group A.

## Identity and boundary

Actual delegated-harness-native TASK `/root/group_a_execution_astra/history_write_review`, parent `/root/group_a_execution_astra`, gpt-6-astra / low; fresh bounded child, no delegation. Applied software-code-review. Independent from repair author and live-source integrator. Sole maintained write is this report; synthetic scratch `/tmp/history-write-independent-x_41qwag`. No source, Git, supplier, native UI, model, network, download or credential operation. Manager explicitly released independent binary/probe execution after diagnosis released resources. No Cargo was run.

## Candidate and causal assessment

Original archive a515b5bf192ed097f0544869331dfb8cfce3db4d failed with 213 pass / 1 fail / 1 ignore at history `sentFrame.is_null()`. Preserved binary SHA dd319259d831b156bf3581a6b0949162fbc3e29fd67c202601be9b2a3ba18c84 independently rehashed. Old worker's isolated 1/0 remains nonreproduction, not repair. Author's concurrent original Host run separately failed additive-guidance's write-failure assertion (93/1/1), not the original archive history assertion.

Reviewed author manifest and every listed evidence file hash (all matched), original concurrent failure log, raw fixture/probe source and child-reader matches. The raw concurrent fixture obtains pipe peer before killing/waiting its child, completes a write, then finds that peer handle in another still-owned child through libproc. This substantiates the fixture's false assumption that child exit means no readers; it is not a claim that original archive process FDs were captured retrospectively. Producer source marks written only after actual write_complete succeeds, consistent with observed sentFrame. No producer repair is warranted by this evidence.

The complete source diff changes only `#[cfg(test)] install_broken_test_input` at hosting.rs:1939: replace killed-cat pipe construction with read-only /dev/null File → OwnedFd → ChildStdin. Original test bodies/assertions and harness concurrency are unchanged. Live and private Host SHA c8fcbfa53c7e3db24fc771c9dc883d8bfd6481512f6d06ecc39164bff71a92f3; old e5b908ba9635b74ff27c79f4f568c139967aaa4edfa0f9a16dadde50dfe4db34. Independent archived regular-file comparison results below. No project software-workflow.json exists, so source scope was compared directly rather than invoking a profile validator.

capture_pipe still executes fstat and F_DUPFD_CLOEXEC; check_bound still checks source generation, epoch and identity; write_complete still executes actual write_all/flush. Read-only access survives duplication and fails at OS write, so this does not mock a producer outcome or convert the case into a prewrite refusal.

Five helper consumers were examined: scoped thread start; text turn write failure/wait; steering write failure/wait; history failed-write/foreign/latest/closed admission; synthetic credential failed-write/logout. Their criteria concern write-failed, uncertainty, absent sentFrame, admission refusal and safe retention—not EPIPE specifically. Existing positive actual-pipe cases remain in the affected Host suite. /dev/null's common inode means this helper should not be used to prove pipe replacement identity; none of these consumers does so. No public contract, persistence format, release configuration or dependency changes.

## Independent verification

Copied and rehashed immutable repaired binary 7eeb55acac6ada51e3bb8180c5b240ed8dbc3112de6ec63ceae7af1d5251c436 from author's source-bound private compile. Rechecked live Host equality and full original-to-live helper-only diff. Commands used CARGO_NET_OFFLINE=true and CHIRALITY_SKIP_CODEX=1, with no concurrency restriction:

- `repaired-tests hosting::conversation_transport_tests::history_bridge_failed_write_foreign_latest_revision_and_closed_refuse_admission --exact --nocapture`: exit 0, 1 pass / 0 fail, 0.23s.
- `repaired-tests hosting:: --nocapture`: exit 0, 94 pass / 0 fail / 1 existing ignore, 7.63s; includes all five helper consumers and positive controls.
- Independent Rust probe, compiled using rustc and no dependencies: eight threads perform 100 read-only File→OwnedFd→ChildStdin→F_DUPFD_CLOEXEC (Darwin cmd 67) captures each; File metadata checks fstat device/inode after duplication; actual nonempty write_all/flush must return raw errno 9 (EBADF). Main thread concurrently spawns/kills/waits 100 synthetic /bin/cat children. Result: 800 EBADF, zero successful writes; all owned children/threads joined. This independently tests the repaired boundary under concurrent spawning rather than relying only on a passing rerun.

Raw source/logs and immutable binary retained in the scratch above; hashes below make observations recoverable. Original failed archive and all author failures remain unchanged. Resource release: session55684 finished exit0; probe command finished exit0; no owned process, Cargo/target or source hold remains.

## Exact evidence and reading origins

Compared 247 original App regular files against each tree. Private differences: `['src-tauri/src/hosting.rs']`. Live differences: `['src-tauri/src/hosting.rs']`.

| Scratch artifact | SHA-256 |
|---|---|
| exact.log | 2d00588be3ed543a04f7b32a5e4078ea039ac264347be55e81dab07365e508ff |
| hosting.log | bda5434bae7fe1e6832774172dbd5a131fa6a67928720797919287b83f00fb30 |
| probe | 581d242cb02acccd43029152c4c360bd00720a2583158e2d707d890706cec31e |
| probe.log | 4b4e4fe78e3bde819bbb83fa86b83b2f8032683b0cd23faee2259e1607d73ed9 |
| probe.rs | 7aec371bdfaa1bf80c1ebb3be5fc109e12ec68b8f54f9b050e5d1a02c6b67c09 |
| repaired-tests | 7eeb55acac6ada51e3bb8180c5b240ed8dbc3112de6ec63ceae7af1d5251c436 |
| results.json | 31cde8de7f8a1497bc199687123d5974c214a317a3a2eae29e73cfd1b756bbc3 |

Read actual Root AGENTS, TASK, selected skill, Loop, manual README, manual headings and §11, full Field Book, manager handoff, original diagnostic handoff/failure JSON; graph current route and affected I1/archive scope (large initial output truncated, targeted follow-up read). No other role body or workflow body loaded.

| Origin | SHA-256 |
|---|---|
| AGENTS.md | f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977 |
| agents/AGENT_TASK.md | 1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7 |
| .agents/skills/software-code-review/SKILL.md | ee085d589c44f912d11a59eead8edac214f0343761d26b0d33e886a979888bca |
| projects/chirality-app-v4/loop/LOOP_INIT.md | c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd |
| docs/alignment-manual/README.md | 5eee30d902c57a251bf885f91bfa0481a7834ec6945c3382baf15d2e2980c63d |
| docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md | 2535efe547f2368e06d965d189efc47c7c46f28c2d6fd4777b0b8cece9003fa7 |
| docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md | 02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3 |
| projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/MANAGER_ASTRA_HANDOFF.md | 46c078a4032264bce86e19b31c63d087b5e31c695896436a76f4ec96114fa7f1 |
| projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I1-HISTORY-WRITE-ARCHIVE-DIAG-HANDOFF.md | ada85b1249927aa4d4d68441d7f39795af049a35a205ab5820252407cada27f1 |
| projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/validation/WORKFLOW_ARCHIVE_a515b5bf_FAILED.json | 1e5a68d62b53de8989391c91a7af4b98135d3c37affbbcf820f6f1cd4d826c0e |
| projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/evidence/HISTORY-WRITE-ASTRA-DIAG/manifest.json | 3898a1b4733d977dc73a00327c3a9aead47fe0ca0a90aa1f5bf5325152a1b1c4 |
| projects/chirality-app-v4/execution/_Coordination/WorkGraphs/APP-V4-GROUP-A-20261004/WORK_GRAPH.md | 7af351749f4a2bc38760b50a61f6f3e5ab277f0f7aed6aaec464f5382be0260a |
