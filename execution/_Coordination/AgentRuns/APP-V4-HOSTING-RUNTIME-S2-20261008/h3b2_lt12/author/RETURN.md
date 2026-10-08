# LT-12 author freeze — independent review requested

Basis `3d73db745edd3378e0bb254a1b263215ef0861e9`, reused `/Users/ryan/.codex/worktrees/hosting-lt23/chirality`, branch `codex/hosting-lt12`. Prior merged exporter candidate preserved as stash `preserved-merged-terminal-export-before-lt12`. No commit, new worktree, delegate, production export or supplier/App execution. Exactly five staged files are enumerated by CANDIDATE_FILES.json; no unstaged tracked delta. Parent owns run graph and integration. Exact released proposal e0d605da4829bb49c9093fa26708523369e426e926d58be0963a5822c632d1f5; proposal/review/RS/REC and instruction origins are hashed in ORIGINS.json.

## Actual source change

Host retains the original installed private LT-09 reference separately from the latest receipt; clears it on accepted start and releases it with Inner. It captures actual LT-12 after the existing close_generation call, reserves the sequence even when publication is ineligible, drops Inner and attachment_gate, schedules using the existing shared App controller, then flushes recovery observations in the existing post-lock position. No REC implementation or ordering change.

The closed private terminal kind maps only LT-12/exited-unexpectedly and LT-23/stopped. Existing controller/weak completion checks include kind/state, attempt, full H5 and event sequence. Existing pending-before-spawn, panic/failure, closing and one-per-App permit behavior is reused. Stop beginning from exited-unexpectedly invalidates the LT-12 reservation at its actual stop-request event; later LT-23 uses original LT-09 rather than the latest LT-12. Store producer adds only LT-12 to the explicit supported terminal set, with actual full event/generation and earlier LT-09 predecessor validation. Reader schemas and legacy event bytes are not changed. LT09/terminal export code and schemas are unchanged.

## Final validation

All final commands use offline Cargo cache `/Users/ryan/Library/Caches/chirality-dev/cargo-home-group-a`, shared `/private/tmp/hosting-s2-target`, CARGO_INCREMENTAL=0, CHIRALITY_SKIP_CODEX=1, `cargo test --offline --lib`, invented fixtures only.

| Feature state | Filter/arguments | Result | Log |
|---|---|---|---|
| default | `successor::tests -- --nocapture` | 69 passed, 2 intentionally ignored | lt12-affected-default.log |
| distribution-successor,custom-protocol | same | 69 passed, 2 intentionally ignored | lt12-affected-production.log |
| default | `-- distribution_ namespace attachment_host_queued_old_eof --nocapture` | 45 passed, 1 intentionally ignored | lt12-store-namespace-default.log |
| distribution-successor,custom-protocol | same | 45 passed, 1 intentionally ignored | lt12-store-namespace-production.log |

These sets overlap; counts are not additive. All 15 LT12 controls pass in both states. They cover actual zero/nonzero exits, whole events/immutable LT09, native established versus fresh receiver, original predecessor LT12→LT23, pending Stop invalidation, Stop-winning EOF, late LT09 success/error, spawn/panic/immediate completion, stale success/error/panic after Stop/restart, closing, cross-home single permit, namespace lease/replaced-root, exact token/row/sequence/foreign predecessor, missing predecessor/custody, actual nonzero request closure counts/repeated EOF, superseded EOF and selected source/predecessor tamper. Nonzero counts come from synthetic protocol activity: unknownNoResponse=1 and endedUnanswered=1 are captured before worker release, with source state closed before publication. Both feature sets include original reviewer_root_replacement_before_returned_descriptor_must_not_receive_writes; existing LT23/exporter/namespace regressions pass. No diagnostic export invocation was requested/performed.

Required staged private check: five changed files, three private terms, zero findings (`lt12-private-staged.log`). `git diff --cached --check` passes. Configured identity remains Ryan C Tufts / ryan@chirality.ai; no override. Production-feature compilation retains the previously documented ignored synthetic frontendDist index solely as an offline Rust harness input, not frontend/package/App evidence. Disk was 6.4 GiB before production compile, later 11 GiB; no cleanup or duplicate target. Shared target is released after these final runs.

## Failure/repair chronology (retained, not relabeled)

- First test writer was invoked from src-tauri with repository-relative paths; it failed before writing. The concurrent first compile therefore had no new LT12 test (lt12-first-default.log); this is not connecting evidence.
- First connecting compile failed because fixture used Host instead of the existing Arc<Host> start receiver (lt12-first-default-connecting.log). Corrected test ownership only. r2 connecting passed one test exercising both exit codes.
- Focused r1: four passed/two failed. Fixture used `from` instead of actual `fromState`, and a wait could capture a transient source-changed at-use response before the stable EOF reservation. Corrected actual field name and harness synchronization; no product change. r2 passed ten controls, r3 passed thirteen after further controls.
- Focused r4: fourteen passed/one failed because tamper fixture named selected-source instead of existing reference-source. Corrected fixture locator only; retained failure and worker unwind output. Final affected runs pass all fifteen LT12 tests.
- Caught intentional panic outputs are expected controls; test results distinguish these from failures. Raw prior logs remain alongside final logs. Product changes after early runs were comments and the support projection text; final four runs cover all frozen source bytes.

## Residuals and receiving consequence

The existing LT19 Stop-after-exited tuple remains inconsistent with its table row; later Stop may retain null fallback exit facts because ready EOF does not append the stopping-branch journal entry. Tests preserve this, and documentation explicitly rejects whole-trace validation. Individual LT12/LT23 envelopes can validate without repairing that trace. No LT13–16, automatic restart, new descendant policy, cold receiver/hydration, S3 or SEAL-2 authority. Production compiled selection/installed issuer remain absent. Blocked Store IO can retain the sole permit/namespace lease; no cancellation/deadline is promised.

Changed source identities deliberately require B fresh committed-source receipts and named pin adoption; no B files/pins changed. Existing LT09 and LT23 exchanges still reject LT12. A future LT12 exchange is separate. Independent exact-candidate review is pending; these are author checks, not independent acceptance.
