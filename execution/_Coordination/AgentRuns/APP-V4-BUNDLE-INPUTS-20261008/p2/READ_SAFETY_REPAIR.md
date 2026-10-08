# Candidate read-safety review repair

Parent-routed independent review identified that manifest and registration-ledger reads could block on a substituted FIFO: the previous path check rejected links but did not establish regular-file type. Parent expanded the TASK fence for a bounded shared read-safety repair; no new workflow authority or runnable standing is added.

A single internal workflow read helper rejects known non-regular files before opening, uses Unix `O_NOFOLLOW | O_NONBLOCK`, verifies regular-file type on the opened descriptor, then reads that descriptor. This prevents the final component from becoming a blocking FIFO or followed link between metadata check and open. The installed manifest resolver and existing ledger reader use the helper at every check. The ledger's missing-file treatment and its schema, sequence, and reconfirmation validators are unchanged. Existing ancestor-path checks remain. On non-Unix platforms the helper explicitly fails closed because an equivalent no-follow guarantee is not implemented; this repair is checked on the current Unix/macOS target only.

Two maintained FIFO tests check both initial selection/recognition and retained selection point-of-use refusal. A nonblocking read/write anchor and a two-second receive deadline make the negative test itself bounded even if blocking-read behavior regresses: the anchor is released before joining the worker. Healthy reads return the non-regular-file refusal immediately, while the writer is still held. These are filesystem mechanics tests, not native supplier or App execution.

Repair source basis `e076c98b510bcc1436790d6e858a3af2299a3c3c` (bounded reader/caller/test sections read):

- `projects/chirality-app-v4/app/src-tauri/src/workflow_workspace.rs`: sha256 `3fe6876148d991760b3fd12dc71bb37794e233009bc547a9fd6ca1429bce0dc5`.
- `projects/chirality-app-v4/app/src-tauri/src/workflow_catalog.rs`: sha256 `5d073f4e2494f7319e89e42be5e0d089d8c2ec71e96b621d3aa33174a6512dba`.
- `projects/chirality-app-v4/app/src-tauri/src/workflow_library.rs`: sha256 `5d30ba3373f2b1137ee68b88ee60bc59f49c644aeaa4f1268a9dcc71c1ce4b31`.
- `projects/chirality-app-v4/app/src-tauri/src/p2_production_catalog_tests.rs`: sha256 `7f2867eb952407ef65614a4d0e08a2177cc353e73bb6c572dc875b414c48f752`.

Focused FIFO tests passed 2/2 before the additional no-special-file-open preflight. The final full affected workflow workspace result is recorded below.

Final checks:

- `cargo test --offline --locked --lib workflow_workspace::`: 96 passed, 0 failed, 325 filtered; includes both FIFO tests and existing registry/catalog regressions.
- `cargo test --offline --locked --lib p2_root_candidate`: 3 passed, 0 failed, 418 filtered; connected candidate selection/refusal remains intact.
- `git diff --check`: passed. Official staged private-term validation is run before commit.
- Current candidate admission remains refused. Manager owns final joined-head review and native/UI integration; no supplier launch, download, credentials, release, push or authority change.
