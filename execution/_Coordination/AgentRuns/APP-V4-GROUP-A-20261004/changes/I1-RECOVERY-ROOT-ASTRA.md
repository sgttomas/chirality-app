# I1 Recovery Root consumer — private preparation

TASK `/root/group_a_execution_astra/file_act_root_consumer`, parent sole WORKING_ITEMS `/root/group_a_execution_astra`, delegated-harness-native Astra/low as supplied; no descendants. This is a new bounded recovery-consumer assignment, independent of later WR publication. Only private scratch and this report written. No maintained App, Git, Cargo, supplier/native UI/auth/model/network/download/credential operation.

## Frozen private candidate

`/private/tmp/chirality-recovery-root-01hhku68/app`, copied from the actual current maintained App after recording its complete source manifest. The baseline was rechecked both immediately after copying and at final freeze; no drift found. All14 reviewed integrated core hashes and the exact adopted ledger0.3 source hashes matched their named integration/adoption records. No Git revision was queried or inferred from the parent's PR label.

`baseline-manifest.json`, original changed-file `preimages/`, complete successor `source-manifest.json`, `core-pins.json`, exact `recovery-root.patch` and `freeze.json` are retained beside the private App. Three original files changed and three new files added; all other261 originals remain unchanged. runtime_session.rs is untouched. hosting.rs retains its exact reviewed production prefix and adds only the parent-authorized cfg(test) inclusion of the owned new recovery_root_tests.rs. None of the14 core production/resource bytes is changed.

Prepared for independent source review and controlled compilation, not implementation fan-in READY. No Cargo lane was granted; WR owns it. Rust parser and frontend checks passed, with no Rust type-check/test execution claim.

## Actual consumer and source boundaries

- `lib.rs` adds `read_recovery_custody(modeHomeClass, generation)`. It retains the actual active HomeSession Arc under a short Root try-lock, releases Root before touching Host, then verifies the original Arc remains selected before return. No Root guard spans Host/queue access; no ledger/history/runtime lock is acquired. Busy Root returns a read limit. It does not resolve a caller's historical pointer into operational authority.
- `recovery_root_view.rs::read` compares actual class and full current generation with the person's selected source, then reads only the existing `Host::recovery_custody().snapshot()` capability and cached source observations. Pre/post full-generation and App-session equality refuse mixed-source results. Null generation is retained as null so metadata can be read before supplier startup; no live turn/generation/session is minted.
- The result wraps original custody fields with source home/generation/App-session, explicit read time and standing. It does not rewrite or merge `index`, `metadataIndex`, `executionGeneration`, per-item association, or unknown correlation. Shared ledger historical rows retain their own original home and generation even when the currently selected Host is another source. Queue count remains that Host's own count.
- `RecoveryCustodyPanel.tsx` sits beside the unchanged Native History panel. It refreshes only on the person's button; it adds no timer or read to host_status/ordinary polling. The existing core getter is a cached view, not durable I/O. React keys reset panel state when selected home/full generation changes; the response is also checked against the selected source before display. Pending asynchronous results cannot become another keyed panel's data.
- Sections distinguish retained in-memory observations/loss events, pending persistence, restart events derived from persisted prior-session facts, historical execution pointers and later metadata provenance, and separately selected native History. Each known/unknown item turn and full tuple remains visible. Missing index/project/home limits remain visible as memory-only/cold unavailable; source unknowns are never backfilled from liveTurn or native History.
- The view displays no Resume/Continue action, makes no supplier request, writes no record/flush, and creates no human-act, workflow-run or external-operation claim. Native History/Continue implementation and command routes are unchanged. The0.3/older0.2 rejection boundary is shown: preserve ledger bytes on rollback; never strip pointers to downgrade.

## Verification actually executed

- `rustfmt --edition 2021 --config skip_children=true` on new recovery_root_view.rs/recovery_root_tests.rs passed; `--emit stdout` parsing of private lib.rs and hosting.rs passed into private parser outputs. This is parsing, not type checking.
- Existing local TypeScript `tsc --noEmit -p <private>/app/tsconfig.json` passed. Dependencies were reused by symlink; nothing installed or downloaded.
- Existing Vite7.3.6 build in private App passed:32 modules,379ms, private asset `dist/assets/index-BcBKqHie.js`.
- `validation/panel-controls.mjs`:3 synthetic actual-component controls passed — initial render makes no read/flush/poll, foreign-home response is refused, and rendered live/pending/persisted/known/legacy-unknown/native-History labels retain provenance. This is synthetic React-state scheduling and JSX inspection, not browser/native evidence.
- First component-control attempt failed because the synthetic text collector inserted a separator alongside existing JSX whitespace, producing doubled whitespace in an exact substring. Original script/log are preserved as `panel-controls.original.*`. Only the collector's whitespace normalization was repaired; product source was unchanged and the semantic text oracles remain identical. No product repair or predecessor defect is inferred from that harness issue.
- Final mechanical check passed: full maintained baseline still matches, exact changed set only, reviewed hosting prefix unchanged, all adopted source pins match. No runtime is running.

Four **written, unexecuted** Rust controls use the exact production Root helper and core producer/ledger/view:

1. Actual Host item-only notifications with identical item IDs on two turns → real immutable queue while writer is held → read preserves pending versus old durable row and writes nothing → explicit owner flush → exact known tuples → source loss and new Host ledger reopen → same original execution generation, no invented liveTurn/restart-live-work/automatic resume/native request.
2. Missing project/index retains in-memory pointers and limits, leaves cold history empty, and repeated read changes no ledger bytes.
3. Foreign home/session/generation and busy Root refuse retargeting; uncontended inverse succeeds; reads while original writer/ledger/runtime/history locks are held establish no such acquisition or flush.
4. Actual ledger append/reopen with mixed known/legacy absent-turn pointers and later-session metadata preserves original executionGeneration, latest metadata session, unknown legacy turn/fullTuple despite liveTurn, and original byte prefix. This last vector constructs pointer metadata explicitly; it is not a supplier witness.

Parent authorized only the cfg(test) child inclusion in hosting.rs because its actual producer/queue fields are private. No public synthetic producer or production API was introduced. Compile and execute these tests under a later granted lane; preserve first failures and source preimages before any repair. Then run affected core/Root checks and obtain exact-candidate independent backcheck. Original43 author/23 reviewer core results remain their bounded antecedent warrant, not tests of this new consumer.

## Remaining limits

Actual native startup/loss/quit/relaunch, UI/accessibility and human recovery choices remain Parent witnesses. This consumer supplies pointer presentation only; external PI-6 dispatch mapping, broader recovery qualification, source adoption/propagation closeout, WR publication and Group A acceptance remain separate. No automatic resume or RS evidence conversion is added to fill those gaps.

## Exact candidate hashes

Patch `96c1373cf42e0a9f6c28023b4382d10adebdbf86eb7ebcf7900dbfdfecd5e714`; baseline manifest `f6c9019dd9846a122a109f715f7b77a4789ac6532b237fc4c715c318b180e93a`; successor manifest `5dc6e30bc4757ce5e3168af94b81c8325e0c3f570bbac90f73ff4dccd96a1e44`.

- `src-tauri/src/hosting.rs`: `2e9273784e6acc96b3898ec5981dee0f00689757aadabe3c8d771933066021d8`
- `src-tauri/src/lib.rs`: `7718c9c0b312343e31a67635189b9f9ddab3c6dfd364f2fe15a5dc02ebdb9939`
- `src-tauri/src/recovery_root_tests.rs`: `cf80bf2629ebac12dd9255f10db0e2fd14ac39507626baee8de0d7f94a3723f6`
- `src-tauri/src/recovery_root_view.rs`: `5153a23003df25a2bb514b4f89153d08124d3e09c36c4c51c992c6913e482719`
- `src/App.tsx`: `af88bb05e53c17742dea47ef525d71826f934be466039858d53aad403ea3e70b`
- `src/RecoveryCustodyPanel.tsx`: `0e18949c9689d19ff84d04bd156874ff0ed854a727effbedd9b5f5efa4290557`

## Actual consultation pins

Root/TASK/v4 Loop/manual entry context carries forward from the same TASK session; new reading covers the named implementation/integration/adoption/core review and actual §7.2 source plus Host/REC/Root/History/runtime joins. No broader role or workflow loaded. Hashes identify consulted files, not a claim of whole-file reading.

- `AGENTS.md`: `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`
- `agents/AGENT_TASK.md`: `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`
- `projects/chirality-app-v4/loop/LOOP_INIT.md`: `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I1-RECOVERY-CUSTODY-ASTRA.md`: `35df33925953301e616c27d73ef2eacacfa08a0b43c36db33633bbc546abd590`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I1-RECOVERY-CUSTODY-INTEGRATION.json`: `a86051abb259397a24a0ae2d0c6af9d7e1480ff6852b10b8029c5a99acc664fa`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-REC-ITEM-TURN-SOURCE-ADOPTION.json`: `adcadda1b3f88d1e67349c8c36d459a9611640181446429781363c9f09f9c166`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V6-RECOVERY-CUSTODY-CORE.md`: `c5a47cde2a1df346767459a23129e41ce81928b59a54dfcfaa65273535c511db`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md`: `088cb70f9124e09845b27dad785009fca56674e276f11dd32ae650622bdb1856`


## Controlled execution on unchanged private freeze — 2026-10-05

Parent released the sole shared Cargo lane after RS finished. **First compilation and all4 connected consumer tests passed without any source/type/test repair.** All frozen source hashes are unchanged from the parser/frontend preparation above. No initial Rust failure exists to repair or reinterpret. The earlier component-harness whitespace issue remains disclosed in its original section.

Executed the frozen private App only with explicit `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home`, shared App `CARGO_TARGET_DIR`, `CARGO_NET_OFFLINE=true`, `CHIRALITY_SKIP_CODEX=1`, and Cargo `--offline --locked`. The runner removes supplier bin/home/hash/workspace environment inputs. Existing unrelated compiler warnings remain, with no warning-suppression edits. Every test uses synthetic own-code/native-source or bounded local IPC fixtures; none starts Codex, a model, native UI, external host, authentication or network operation.

**56 distinct Rust checks pass**, with no duplicate case names across these selected commands:

| Selection | Passes | Purpose |
|---|---:|---|
| `recovery_root_tests` | 4 | Actual producer → queued/durable → reopen → actual Root consumer; read purity, missing index, source/refusal and lock inverses, legacy unknown versus later metadata |
| `execution_custody_tests` | 15 | Integrated reviewed REC0.3 producer/reopen/legacy and original repaired source controls |
| `app_custody` | 7 | Sole writer, retired queues, I/O failure, shared home and original ownership |
| `recovery_custody_rc2` | 1 | Actual cross-session metadata writer retains new metadata with original execution provenance |
| `recovery::` | 10 | REC ledger/framing/generation/transition/validation boundaries |
| `workflow_root` | 8 | Existing Root contexts and WRC1 competing-lock inverses remain valid |
| `file_act_consumer_tests` | 4 | Retained connected file-act consumers remain valid beside new Root command |
| `history_bridge` | 7 | Existing native History/Continue receiving/control paths remain unchanged |

The original four written tests are now executed evidence. Queued facts stay distinct from persisted index rows while the writer is held; reading changes no ledger bytes; explicit later owner flush preserves both identical item labels under their own turn IDs. New Host reopen receives the original full execution generation and exact item associations while current generation remains null; item-only evidence creates no liveTurn, restart-live-work or automatic native request. Missing project/index stays hot-only. Foreign home/session/counter and held Root refuse the read without retargeting, while the inverse read succeeds with writer/ledger/history/runtime locks held. Mixed legacy items retain null turn/fullTuple despite a liveTurn beside them; latest metadata session remains separately visible and ledger bytes are not migrated.

`validation/run.py` and each named `*.json`, `*.source.json`, `*.log` retain exact commands, cwd, exit, timing, source/log hashes. `CHECKED.json` binds all selected results, explicit known environment, versions and the exact copied executable. The original command manifests include the existing private build outputs; every final source entry was independently compared against every command manifest and final source-manifest, with equality. No App source or frontend asset changed during the Rust checks.

Immutable handoff: `checked/app` contains the frozen complete source without build/dependency trees; `checked/source-manifest.json` matches the original successor manifest. `validation/checked-lib-tests` is the exact binary used by the successful commands, copied before releasing shared target ownership. The original app path remains stationary because compiled fixture references use its CARGO_MANIFEST_DIR. No entire suite or broader native qualification is claimed. Original core43/independent23 and earlier file-act results are not added to this56.

- Patch: `96c1373cf42e0a9f6c28023b4382d10adebdbf86eb7ebcf7900dbfdfecd5e714` (unchanged).
- Source manifest: `5dc6e30bc4757ce5e3168af94b81c8325e0c3f570bbac90f73ff4dccd96a1e44` (unchanged).
- Checked executable: `203574e3c1d236d5b463d59fcfb5be2a78069ada9cf65ee5b99caa847f80b74e`.
- CHECKED.json: `c6be1625ea8674449bc0fb3c84e1e2f694d4cae3bc56cf74931f5727fefb0944`.

All processes finished and Cargo reservation released to Parent/reviewer. Independent exact-source/executable backcheck remains the next disposition; no maintained integration, native witness, source-adoption closeout or Group A acceptance is implied.
