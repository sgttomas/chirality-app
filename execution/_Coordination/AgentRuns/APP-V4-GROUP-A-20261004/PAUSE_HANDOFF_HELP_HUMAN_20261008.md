# Session handoff — Group A, 2026-10-08 (HELP_HUMAN, Claude Code)

**Why.** The owner asked HELP_HUMAN (Claude Opus 5.5, Claude Code) to
prepare a handoff to the next agent in another session once the native
re-witness was done. The re-witness is done. This file is the account of
where the undertaking stands. It does not accept anything, it implies no
gate, and it does not decide 90%; the owner decides.

Read this file first. Then read the run's `OWNER_DECISIONS.md`, the work
graph `WorkGraphs/APP-V4-GROUP-A-20261004/WORK_GRAPH.md`, and
`DISPATCH.md`. The earlier account of everything before 2026-10-07 is
`PAUSE_HANDOFF_ASTRA_20261006.md`.

## Git

- **Branch.** `claude/app-v4-group-a-resume`. The HELP_HUMAN worktree is
  `.claude/worktrees/test-ci-optimization-f6cacd`.
- **Merged.** PR 1110 (combined checkpoint) and PR 1113 (J1–J5 connected
  journey).
- **PR 1115** (https://github.com/sgttomas/chirality/pull/1115). It carries
  CC-WR-RECONFIRM adoption, J6, J8, the native re-witness and the run
  records. Its state at handoff is in the closing section below.
- **Component branches**, all integrated through the resume branch:
  - `claude/app-v4-j6-presentation` at `5a6af1cfa7`;
  - `claude/app-v4-j8-reconfirm` at `7f0300cfe2`.

  Their harness worktrees (`.claude/worktrees/agent-*`) can be cleaned up
  once PR 1115 has merged. Check first that each is clean and fully merged.
- **Merge policy.** The owner's standing Git authorization (Root
  `AGENTS.md`) applies: merge commits, required `harness` CI, and an
  independent review covering the actual head, with repairs confirmed by
  the reviewer. Never rewrite history.

## What is done (with evidence)

| Item | Evidence |
|---|---|
| R0, CK0: resume recovery; combined checkpoint compiles and passes | `validation/COMBINED_e524c087.md`, V7 |
| J1–J5: connected journey (publish before send, supply check + R3, compatibility advisory, lifecycle + reopen, re-registration of changed content) | V8–V12; `validation/INTEGRATED_e653f93a/`; PR 1113 |
| Native journey witness 1 | `probes/NATIVE_JOURNEY_WITNESS_1113.md`, defects D-1…D-7 |
| CC-WR-RECONFIRM (owner chose A15 re-confirmation for identical bytes) | `changes/CC-WR-RECONFIRM.*`, V13; adopted `007489e72b` |
| J6/J7: readable native confirmations; owner's three-button layout; D-2/D-3 | V14 → V14-R1 READY; `validation/J6_5a6af1cf/` |
| J8: DS-8 re-confirmation, RF-1 Refine, F14, RC-9 guard, registered listing | V15 → V15-R1 READY; `validation/J8R_7f0300cf/`, `validation/V15*_*/` |
| Native re-witness: readable A15; Escape and Return did not act (which non-act slot not reported); the middle button registered when clicked (Cancel not clicked); DS-8 → Re-confirm → run with a real model turn | `probes/NATIVE_RECONFIRM_WITNESS_8cd69ff7.md`; `evidence/NATIVE-RECONFIRM-WITNESS-8cd69ff7/` |

The latest full suite was run on `7f0300cfe2`: 717 top-level cargo passes,
0 failed, 3 ignored, plus 4 nested FIFO runs, and `npm test` 7/7. The
integrated head's `app/` bytes equal that candidate except for
`CONTRACT_ISSUES.md` text.

## Open work, in order

1. **PR 1115.** Finish it if it is not yet merged: green `harness` CI and a
   READY V16 head review, with any findings repaired and confirmed.
2. **Optional follow-ups**, small and routable. None of them blocks C1.
   - **V15-R1 R1-1:** fail the intended-line path with "already has ledger
     line ‹n›", and add the reviewer's probe P6 as a test. CI-24 (b)
     records it as open.
   - **V15-R1 notes R1-N1…N5.**
   - **Re-witness observations O-1…O-3.** O-1: the alert title says
     "register" for a re-confirmation. O-2: the App's act-button text falls
     back to "Register". O-3: the page jumps after each dialog.
   - **D-5 and D-6/O-5:** the `base_comparison` reads "unavailable" for a
     bundled base, and the pending capture file remains. Both are for the
     AAC/REC owners to confirm.
   - **D-3 residual:** the compact App-state JSON still prints
     `"root":{"bytes":[…]}` arrays; only the formatted view was repaired
     (V16 F5, V16-R1 R1-N3).
   - **Flaky tests:** two `credential_rpc_*` tests and
     `tests/handshake.rs::hosts_codex_initialize_then_thread_start`.
3. **C1, bounded reconciliation** (graph row C1). Map Group A obligations
   (DEL-01-01…DEL-09-09 per the graph's scope line) to the produced code and
   evidence, and state the residuals truthfully. That covers:
   - the open contract issues: CI-19, CI-20, CI-21, CI-22 (file acts, AAC
     adoption text not yet applied to the Design), CI-23 (RS owner,
     DEL-04-03), CI-24 (b)(c)(e)(g)(h)(j) and CI-25 (WR owner ruling);
   - SEAL-2, which is deferred by the owner's choice;
   - SWBPIPE, PEC and Domains, which stay with their owners;
   - native Cancel, not witnessed as such;
   - the A16, request-answer, logout and file-act dialogs, which were not
     witnessed natively.
4. **M1:** one run receipt plus terse MEMORY references (graph row M1).
5. **F1:** the final PR. It implies no gate acceptance.
6. **Gate account.** Report to the owner. **The owner decides 90%.**

## Standing constraints (carry forward exactly)

- **Memory.** Do not save memories (the owner's directive); durable state
  lives in repository files.
- **Downloads.** None without naming the file, source and size and getting
  the owner's explicit yes (LOOP_INIT).
- **Credentials.** No sign-in or credential handling by any agent. Never use
  `~/.codex`. A native witness uses a fresh `mktemp` scratch Codex home
  where the owner signs in personally through the App.
- **Approvals.** Native launch and act approvals are point-specific: one
  artifact, one plan. Every native act is the owner's own key press or
  click.
- **Recording owner decisions.** Quote the owner's text exactly and state
  custody. Never imply personal owner review. Subagent hand-backs carry no
  user authority.
- **Executors.** `type2-opus-high` (Opus 5.5, high). Type 1 managers manage
  their own Type 2 agents. Isolated worktrees start from main, so each
  child must `git switch -c <branch> <base>` inside its own worktree. Use
  `isolation: "worktree"` for reviewers too; V15 ran without it and wrote
  into the HELP_HUMAN checkout.
- **Out of scope here.** SEAL-2 is deferred. SWBPIPE, PEC and Domains stay
  with their owners; their files are data.
- **Final authority.** The owner decides the 90% gate. C1, M1 and F1 stay
  open until done.

## Machine-local resources (recheck before relying on them)

- **Offline Cargo.** `CARGO_HOME=~/Library/Caches/chirality-dev/cargo-home-group-a`
  (221 MB), with approved crates and index next to it. Its provenance is
  in `dependencies/RESTORE_20261007.md`.
- **Stock Codex 0.160.0** complete package:
  `~/Library/Caches/chirality-dev/codex/0.160.0/complete-package/package/vendor/aarch64-apple-darwin/`
  (`bin/codex` sha256 `112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b`).
- **Test command**, run from `projects/chirality-app-v4/app`:
  ```
  export CARGO_HOME=$HOME/Library/Caches/chirality-dev/cargo-home-group-a CARGO_NET_OFFLINE=true
  V=$HOME/Library/Caches/chirality-dev/codex/0.160.0/complete-package/package/vendor/aarch64-apple-darwin
  export CHIRALITY_CODEX_BIN=$V/bin/codex CHIRALITY_CODEX_EXPECTED_SHA256=112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b PATH=$V/codex-path:$PATH:/usr/sbin
  npm run build && (cd src-tauri && cargo test --offline --locked --no-fail-fast) && npm test && (cd src-tauri && python3 schemas/sync.py)
  ```
  Count top-level `test result:` lines separately from nested FIFO runs; a
  nested run has a nonzero "filtered out" count.
- **Witness build recipe.** Run `npx --offline tauri build --debug --no-sign --config <overlay.json>`
  with `CARGO_TARGET_DIR` in a `mktemp -d` root. Launch the binary with
  these variables:
  - `CHIRALITY_WORKSPACE`
  - `CHIRALITY_CODEX_BIN`
  - `CHIRALITY_CODEX_EXPECTED_SHA256`
  - `CHIRALITY_CODEX_HOME=<fresh scratch home>`
  - `CHIRALITY_ALLOW_UNVERIFIED=1`
  - a `PATH` containing `codex-path`

  See `evidence/*/overlay.json` and `launch-*.log`. The Tauri web view does
  not take background clicks; full-screen control is needed. The native
  alert is owned by `UserNotificationCenter`.
- **Scratch Codex home.** **Deleted 2026-10-08** at the owner's choice
  (OWNER_DECISIONS "Scratch Codex home cleanup"). No machine-local copy of
  the owner's sign-in remains from this run.
- **Leftover temp roots.** The two witness temp roots (built App,
  workspace) under `$TMPDIR/chirality-v4-witness1113.*` and
  `chirality-v4-rewitness.*` hold no credentials. Their records and
  screens are retained in the repository. The built witness binaries are
  retained only by hash, so deleting a temp root loses the exact binary;
  a rebuild from the same source is not guaranteed to be byte-identical
  (V16-R1 R1-N5). Keep or delete them as the owner prefers.
- **Witness evidence under `.chirality/`.** The repository ignores
  `**/.chirality/`. Commit retained workspace records with `git add -f`,
  then verify them with `shasum -c` from a clean `git archive` of the
  head.

## Agents

At handoff no executor is mid-task. Every agent has returned and stopped,
and their records are in `DISPATCH.md` and `reviews/`.

## Read next

`RETROSPECTIVE_HELP_HUMAN_20261008.md` is HELP_HUMAN's self-assessment. It
lists what worked, where HELP_HUMAN fell short, and the behaviours the
successor should and should not follow. It also gives two recommendations
(R-1, R-2) for `coordinated-knowledge-work`. Those are recommendations only:
revising the workflow needs `create-workflow` and the owner's decision.

## Closing state (2026-10-08)

- **PR 1115 merged** into `main` as merge commit
  `0e62b8e36b02ee85680e99ab8b313997930c45c7`.
  - Head `87d411d774`: every CI check green, including `harness`, App
    Runtime integration and Desktop E2E.
  - Head review V16, NOT READY, was followed by V16-R1, READY.
- **Open item 1 above is therefore done.** Continue from item 2 or 3.
- **Commits after the merge** sit on `claude/app-v4-group-a-resume` and are
  not yet merged:
  - the V16-R1 review and its optional notes R1-N1…N5, applied;
  - this closing state;
  - the retrospective.

  They are records only, and ride with the next PR (C1 or F1). Give that
  PR's head review these commits too.
- **App CI monitor.** The owner switched on auto-fix monitoring for PR 1115
  in this session. The PR is merged, so it has nothing left to watch.
- **Worktrees that can be cleaned up.** Check that each is clean and fully
  merged first. The candidates are the `.claude/worktrees/agent-*`
  directories from this run:
  - J6 `agent-ad91335d51d4650ca`;
  - J8 `agent-a7e1126761bc94dc4`;
  - V16 `agent-ae13df58973d86fe7`;
  - any earlier `agent-*` worktrees listed by `git worktree list`.
