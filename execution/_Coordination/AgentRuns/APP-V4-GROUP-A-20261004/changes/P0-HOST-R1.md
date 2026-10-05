# P0-HOST-R1 — independent hosting-review repairs

2026-10-04. Status: repaired and checked; ready for independent backcheck. TASK `/root/group_a_execution/hosting_propagation`, delegated-harness-native child of `/root/group_a_execution`; no descendants. Original P0-HOST and V1-HOST retained unchanged. Scope: hosting.rs, hosting_contract.rs and this successor evidence. No instruction, Design, schema, supplier resource, Cargo manifest/lock, manager lib/UI or ACT source changed. No authentication, credentials, network/download command, live provider turn or Git mutation.

V1-HOST found two defects. First, the contradictory initialize-response branch did not deliver held frames before closing, so a later spawn could erase the early notification and response. Both failure branches now use the same bounded helper to drain every held native frame in receipt order to the journal, marked generationNeverReady, before generation closure. The regression checks exact unchanged early notification and contradictory initialize response, full generation identity, positions 1/2, never-ready metadata, and equality after an explicit stop/new start. It preserves the earlier readiness-refusal oracle. No restart machinery added.

Second, binary-read failure could hide an already observed contradictory version label behind an unverifiable fallback and authorize development. The label comparison now precedes any binary content-read fallback. A maintained test double prints the wrong version then removes its executable; the start remains mismatch(observed version label), refused, and no child exists. No development option bypass. All prior negative tests remain.

Source stayed frozen during ACT's exclusive Cargo slot. After manager grant, all checks used CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home, --offline and --locked, against the current maintained candidate:

- `cargo test --offline --locked --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml --lib hosting_identity_tests -- --nocapture`: 2/2 pass.
- Same command with `--test hosting_contract`: 5/5 pass; includes both repaired paths and all prior contract negatives.
- Same command with `--test handshake`: 1/1 real stock 0.160.0 pass, exact approved binary SHA-256 112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b. Scratch mktemp home/probe/workspace, explicit skeleton_local/skeleton-no-model, plugins/analytics off, no authentication/turn. LT-01/LT-24/LT-06/LT-09/LT-17/LT-23; 704 ms start-to-thread; empty sampled internet socket list. Scratch cleanup completed. Bounded socket absence only, not continuous monitoring or universal no-network claim.

Shared test-helper dead-code warning only; no check failure. Scoped git diff --check passed. Exact real hosting schema export is available at app/src-tauri/target/tmp/skeleton-output/hosting-records.json for manager's connected consumer check. Earlier strict connected Node pass remains at P0-HOST's identified prior source; no new Node pass borrowed from it. Source frozen and Cargo slot released after these affected checks. Independent backcheck, combined candidate verification and acceptance/qualification remain separate.

## Exact input and repaired output identities

- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/P0-HOST.md` — `fe81fd5958f63414bf346e8a56f82b49f40d3e26b38ea40914db5eb6435ac9c9`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V1-HOST.md` — `d249dc221877d981220d3f1f3cbb39792c2cde67a0eaf68debddf671c8a16217`
- `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` — `33684e1cc9a01248f00242a3fd1a11db6b35caa1d7cd411292515cb9f8fc5725`
- `projects/chirality-app-v4/app/src-tauri/tests/hosting_contract.rs` — `6a60f73204392801d23c75d1c0955db4911b1fb4357da949dc71b02f5515c561`
- `projects/chirality-app-v4/app/src-tauri/tests/handshake.rs` — `848bb38c0cd32b36c97e34da09aa59606a7747241170f8c89f01c411571845a2`
