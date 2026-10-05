# P0-HOST-R2 — failed-handshake snapshot metadata

2026-10-04. TASK `/root/group_a_execution/hosting_propagation`, delegated-harness-native child of `/root/group_a_execution`; no descendants. Status: bounded residual HOST-M1 repair checked, ready for same-reviewer backcheck. Original P0-HOST, P0-HOST-R1 and review records unchanged. Only hosting.rs, hosting_contract.rs and this successor record changed. No schemas, ACT/shared source, supplier resources, credentials, network, download, Git or instruction mutation.

Previously the contradiction branch returned before recording the initialize response identity/consistency, leaving a snapshot with empty identity and no-version-found despite journal evidence of a contradictory version. Handshake identity/consistency now update before the branch; a parsed contradiction remains refused, absent reported version remains distinct, and successful readiness uses the same recorded metadata. Exact native frames and never-ready delivery remain intact. Existing contradictory mismatch regression now asserts actual reported identity `{userAgent: codex/0.159.0}` and `contradicts-declared-pin` in the snapshot, in addition to previous refusal/frame-retention assertions. No test weakened.

Source held while ACT reviewer owned Cargo. After manager grant, ran only the affected regression with isolated approved CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home:

`cargo test --offline --locked --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml --test hosting_contract version_label_and_handshake_mismatches_refuse_readiness -- --nocapture`

Result: 1/1 pass after successful recompilation, four unrelated integration tests filtered. Test-helper dead-code warning only. Cargo slot promptly released to ACT; source frozen. No real supplier process/model turn executed for this focused double regression. Earlier full checks retain their identified prior source, not a new pass claim here. Same-reviewer backcheck and combined candidate validation remain manager work; no qualification or acceptance claimed. Scoped git diff --check passed.

## Exact inputs and repaired outputs

- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/P0-HOST-R1.md` — `c8b99f9227dfe6547dc0452d198fe44816f3d369a8af79a4a09f0b86196fbe76`
- `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` — `84d3e58c41fbdedd10b3316d3420c723db9b8eaaf05135797da7d52f764da596`
- `projects/chirality-app-v4/app/src-tauri/tests/hosting_contract.rs` — `ffb1aeefb0b7336a556059f21e2bf1ab4155d6f425d45efe7aaf6a66ac66ae7e`
