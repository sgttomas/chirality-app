# P-2 connected candidate selection follow-on

Parent WORKING_ITEMS explicitly commissioned this bounded follow-on after conservative route B: connect candidate selection and prove refusal, without lib/UI edits or runnable admission. The TASK remained the same delegated-harness-native child, with no descendants. Manager basis `f0072e0a05aced1683291592c9806002f2c6f016` was merged without rewriting history in `640163a`; it includes P3 runtime work. Existing runtime `run_admission` is unchanged.

`WorkflowRootSession::select_production_bundle(root: PathBuf, name: &str)` resolves exact physical candidate bytes through the catalog. `select_production_copy(name: &str)` uses the actual active library while retaining its owner lock. Successful explicit selection receives a fresh reference/time and preserves candidate standing. Failed resolution leaves the previous selection intact. Existing point-of-use checks remain in Selection; no candidate is represented as LS-5/LS-8 or historical shipping.

Snapshot `productionCatalog` is `{standing, entries:[{name, revision, origin, sourceRoot, revisionMethod, identity, runnable:false, runLimit}]}`; catalog load failure gives empty entries and a limit. These are embedded candidate inventory observations. Native resource-root resolution, commands and UI remain manager-owned. Snapshot selection keeps existing package/currentLimit/runnable/runLimit fields; candidate runLimit states TT-1/TX-1 refusal.

Three maintained connected tests use the existing synthetic Python transport fixture, not a supplier binary or native App launch. With a valid conversation they prove selected bundle/copy candidates refuse preparation before session run creation, WR/RS files or record-directory creation, or any new transport frame. They also cover manifest/registry mutation, failed re-selection preserving the pinned selection, and a real synthetic-A15 registered slot refusing candidate reinterpretation while retaining its registered standing. This is connected refusal proof, not positive candidate execution or human-act qualification.

Focused tests initially passed 3/3. The full existing workflow-root regression suite is run on the final changes; its exact result follows below. No dependency downloads, credentials, supplier launch, native UI, push, Design edits or authority pin changes.

## Additional exact source reads

Basis: `f0072e0a05aced1683291592c9806002f2c6f016`. Earlier sources remain in SOURCE_READS.json.

- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BUNDLE-INPUTS-20261008/CC-WR-PKG-CANDIDATE-01.md` — sha256 `a1c14c9122e1853fcfe1b74efae0b67146764a4613fd27d088fb60284d912e25` (bounded relevant sections read).
- `projects/chirality-app-v4/app/src-tauri/src/runtime_session.rs` — sha256 `2f2a7c1dd1e50590aeb65dab49eb7e0e1b7a48e676561fb38a06d28faaa650b4` (bounded relevant sections read).
- `projects/chirality-app-v4/app/src-tauri/src/workflow_library.rs` — sha256 `5d30ba3373f2b1137ee68b88ee60bc59f49c644aeaa4f1268a9dcc71c1ce4b31` (bounded relevant sections read).

## Final checks

- `cargo test --offline --locked --lib runtime_session::workflow_root_tests`: 55 passed, 0 failed, 364 filtered, 41.27 seconds. Includes all three final P-2 tests and existing registered/development lifecycle regressions.
- `git diff --check`: passed.
- Owner Git identity rechecked: Ryan C Tufts <ryan@chirality.ai>; no author/committer environment overrides.
- Official staged private-term validator runs before the follow-on commit. Parent retains independent review and native/UI integration responsibility.
