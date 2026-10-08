# V12 — independent integration review of J1–J5

2026-10-07. I am a Type 2 TASK reviewer (Claude Opus 5.5, Claude Code). I am the
same reviewer as V7, and HELP_HUMAN dispatched me. I did not delegate, and I did
not author any of the code or records reviewed here. My only write is this file,
and I made no commit. I made one network contact, by mistake: a `git fetch
--dry-run`. It updated no ref, and I used no fetched data. Everything else was
offline, and I used no credentials, no `~/.codex`, no model call and no native
UI.

## Candidate and scope

- **Candidate:** `f1ec8d558982653e9beb518b4b6842e56fef6546`, on branch
  `claude/app-v4-group-a-resume`.
- **Reviewed heads:**
  - J1 + J3 (including J2 through `75306094ed`) at `2e2a02844a` (V9/V10 READY);
  - J4 + J5 at `8d98de95a8` (V11 READY);
  - J2 at `00eb79ca5e` (V8 READY).
- **Integration merges:** `040d9af602` (J2), `d91fc9a360` (J1+J3) and
  `e653f93a1d` (J4+J5).
- **After `e653f93a1d`:** the four later commits (`4009dd12f3`, `215f8fae3a`,
  `e6c50456a6`, `f1ec8d5589`) change no App path.
- **Records reviewed:** everything added under `projects/chirality-app-v4/execution`
  since `0fb6f4a8bc`. That is 192 files and 3.44 MB, almost all of it
  validation logs.

## Method actually performed

1. **Merge recomputation.** For each integration merge, I ran `git merge-tree
   --write-tree` on its two parents. Then I diffed the conflict-marked
   auto-merge tree against the actual merge commit, under
   `projects/chirality-app-v4`.
2. **Per-file union classification.** For every App path, I compared the
   blob at `f1ec8d5589` with the two reviewed heads and with their merge base
   `1dad2331e8`. J4/J5 branched there, from the J1/J3 branch before the V10
   R-1…R-5 repairs. For the two files that differ from both heads, I listed
   every line the candidate drops relative to each head.
3. **Diff reading.**
   - The complete `1dad2331e8 → 8d98de95a8` diff of `runtime_session.rs` and
     `lib.rs`, and the J5 core of `workflow_library.rs`.
   - The complete `1dad2331e8 → 2e2a02844a` diff of `runtime_session.rs`.
   - At the candidate: `open_library`, every writer of `WorkflowRootSession` and
     `app_user_data`, and the J4 journey's calls to `open_library` and
     `create_selected_draft`.
4. **Reproduction.** I extracted `git archive f1ec8d5589 projects/chirality-app-v4`
   into my scratch folder and ran `cargo test --offline --locked` there with:
   - `CARGO_HOME=~/Library/Caches/chirality-dev/cargo-home-group-a` and
     `CARGO_NET_OFFLINE=true`;
   - the stock Codex 0.160.0 `bin/codex`, sha256 checked as `112fae7a…4b4b`;
   - `codex-path` prepended and `/usr/sbin` appended to `PATH`;
   - cargo/rustc 1.92.0.

   I also ran `tsc --noEmit` and `schemas/sync.py` on the same extract. To test
   the V11 count note, I ran the same suite on an extract of `8d98de95a8`, and
   counted `#[test]` attributes at each head.
5. **Main merge.** `git merge-tree --write-tree --name-only f1ec8d5589 origin/main`,
   with local `origin/main` at `0b6c5d7362`, then a diff of its tree against
   the candidate under `projects/chirality-app-v4`.
6. **Records.** I checked these against their sources:
   - the OWNER_DECISIONS additions;
   - the work-graph rows;
   - the four integrated logs;
   - the hash tables in V8, V10 and V11;
   - V11's count note.

   I read `CAPTURE_CUSTODY_DECISION.md` and the 2026-10-05 SEAL-2 deferral as
   the basis for the SEAL-2 explanation. I could not read the active chat, so I
   could not check owner quotes against their source.
7. **Hygiene.**
   - I ran main's `validate_run_record_leaks.py --base 0fb6f4a8bc --head f1ec8d5589`.
   - I grepped the added lines for credential patterns and absolute paths.
   - I hashed all added record files to find duplicates.

## Answers

### 1. App bytes

The App tree at `f1ec8d5589` has 273 paths. 266 are identical at the candidate
and both reviewed heads. The other seven break down as follows:

- **Unchanged by J1/J3 since the merge base, so they come from J4/J5 exactly:**
  `lib.rs`, `workflow_journey_tests.rs`, `workflow_library.rs` and
  `workflow_library_tests.rs`.
- **Unchanged by J4/J5 since the merge base, so it comes from J1/J3 exactly:**
  `src/App.tsx`.
- **Differ from both heads (resolved conflicts):** `runtime_session.rs` and
  `CONTRACT_ISSUES.md`.

How each merge was resolved:

- **`d91fc9a360` (J1+J3).** It merges with no conflict, and the actual commit
  equals the auto-merge.
- **`e653f93a1d` (J4+J5).** Against the conflict-marked auto-merge tree, the
  actual merge differs only by deleting the marker lines: three in
  `CONTRACT_ISSUES.md` and six in `runtime_session.rs`.
  - Both sides of each conflict are kept, as stated: the `held_successors`
    field, then the `app_user_data` field, and both `Default` lines.
  - CI-20 (j) is complete, and the CI-21 heading follows it.
  - Every non-conflicting hunk equals Git's three-way result. That includes
    J5's `set_app_user_data`, the `attach_app_kept_bases` call in
    `open_library`, `discard_unbased_copy` in `create_selected_draft`, and the
    journey test module routing.
- **`040d9af602` (J2).** The actual merge keeps the main line's repaired CI-17
  text, drops the J2 side's stale CI-17 text, and keeps CI-19. The J2 side
  never edited CI-17 (its text equals base `3d0db214cb`), so nothing J2
  authored was dropped.

Lines lost relative to each head:

- **Against `2e2a02844a`.** The candidate drops only the stale CI-17 lines and
  the two `runtime_session.rs` lines that J5 replaced. Those are
  `LibraryOwner::open` becoming `let mut owner`, and the bare `record_base`
  call.
- **Against `8d98de95a8`.** It drops only the stale CI-17 lines and the J1/J3
  R-2/R-5 rewrites of `start_workflow_run`.

So no hunk from either side was lost. `CONTRACT_ISSUES.md` has 21 CI headings,
no conflict markers, and the repaired CI-17.

### 2. Semantic interactions in `runtime_session.rs`

I found no conflict between J5 and the J1/J3 run lifecycle.

- **No shared state.** J5 adds `app_user_data`, which only `open_library`
  reads, and changes only `open_library` and `create_selected_draft`. J1/J3
  add `held_successors` and run-lifecycle state, which only run preparation and
  start read. No J1/J3 path reads library bases. No J5 path reads or writes
  runs, conversations or holds.
- **`create_selected_draft` is a library copy.** It neither prepares a run nor
  touches the selection's run binding, so the R-5 reservation and the
  one-live-run rules do not apply to it. J5-2's discard path removes only
  byte-exact draft files.
- **`open_library` wiring.**
  - The production `WorkflowRootSession` is created once (`lib.rs:945`) and
    receives `set_app_user_data` at setup (`lib.rs:983`), before any library
    can be opened.
  - Nothing else replaces that session. The only other
    `WorkflowRootSession::default()` calls are in `#[cfg(test)]` code.
  - A re-opened root returns early, so it never attaches twice.
  - If attaching fails, `open_library` returns before inserting the library.
    Its runs cannot then be prepared, which fails closed.
  - If the App data folder is unavailable, bases stay in memory only. CI-21
    discloses this.
- **Tests across both.** The J4 journey calls `open_library`,
  `create_selected_draft` and the run lifecycle together. It passes on the
  integrated tree, which also carries the R-1…R-5 repairs.

### 3. Records

What the evidence supports:

- **Integrated logs** (`validation/INTEGRATED_e653f93a/`). `rust.log` has 40
  targets and 44 result lines. That is 681 passes = 677 top-level + 4 nested,
  0 failures and 3 ignored. Node shows 3/3, the build passes, and the schema
  sync reports 6 matches. The four logs have no summary record or exit
  status (F6).
- **My reproduction at `f1ec8d5589`.** I got the same figures: 677 + 4, 0
  failed, 3 ignored, exit 0, 75.8 s. Log sha256 is
  `19ece8f44ca8411eb6fda310493f8712f1e189594ee840387b6e08fd3b821ec6`. It is in
  my scratch folder and not retained. `hosts_codex_initialize_then_thread_start`
  and all nine `credential_rpc_*` tests passed on the first run, so no rerun
  was needed. `tsc` exited 0, and the sync check passed.
- **The V11 count note is correct.** My run on a fresh archive of `8d98de95a8`
  gives 668 + 4, 0 failures, 40 targets and 44 result lines (log sha256
  `6b1e169a…f107`). That agrees with `validation/J5_fde13bc6/v11-full-2-cargo-test.log`.
  - The static `#[test]` counts are 664 at `8d98de95a8` and 673 at the
    candidate. The +9 is exactly the R-1…R-5 tests from `1dad2331e8 → 2e2a02844a`.
  - V11's reviewer section reports "46 result lines … 677 top-level" for
    `git archive 8d98de95a8`, and 674 + 4 for `fde13bc6dc`. Both are +9 over
    what those trees contain. So that run included the J1/J3 R-repairs, and
    was not of `8d98de95a8` alone.
  - The note hedges this as "most likely", and its conclusion is
    right. V11's line saying "full suite passes on `8d98de95a8`" is now
    independently confirmed by my run. See F3.
- **Review hash tables.** V11's six file hashes match `8d98de95a8`. V8 and
  V10 have no hash tables in their final sections. The final verdicts are V8
  READY at `00eb79ca5e`, V9 READY for J1 scope, V10 READY at `2e2a02844a`, and
  V11 READY for J4 and J5.
- **OWNER_DECISIONS.**
  - Both sections give a custody statement, quote the answers as exact text,
    and state what each answer does not approve.
  - The SEAL-2 explanation matches `CAPTURE_CUSTODY_DECISION.md`: a protected
    key for the signed App, and staged A→B→A→B. CI-21(b) exists as cited.
  - One sentence goes beyond the owner's words (F1).
- **Work graph.** The J2–J5 statuses match the merges and logs, except for
  two inaccuracies (F2).
- **DISPATCH.md.** Unchanged since `0fb6f4a8bc`, which I confirmed under V7.

### 4. Hygiene

- **Secrets.** None found. The leak check reports `PASS: 191 changed
  run-record file(s) scanned; 0 possible credential(s); 0 machine-local
  symlink(s)`.
- **Home paths.** No added App line contains a home path. The record paths
  point to `/Users/ryan/ai-env/projects/chirality/.claude/worktrees/agent-*`
  checkouts (cargo `Compiling` lines) and to `~/Library/Caches/chirality-dev`.
  That is provenance, not a product dependency.
- **The F5 exception.** Four J1 logs (`validation/J1_8a785ac4/r5-final-*.log`)
  print the whole `PATH` environment value. It lists personal tool directories
  (`~/.opencode`, `~/.lmstudio`, `~/.local`) and is not needed as evidence.
- **Size and duplicates.**
  - The largest record files are about 117 KB.
  - The only duplicates are tiny `schema-sync` logs (7 + 3 copies).
  - The J1 folder holds 136 logs. They are kept as mutation and control
    evidence, and each is plausibly cited by V9 or V10.
- **Nothing found must be withheld from main.**

### Main merge

`git merge-tree` of `f1ec8d5589` with `origin/main` (`0b6c5d7362`) succeeds with
no conflicts. Its tree is identical to the candidate under
`projects/chirality-app-v4`. Since the merge base `0fb6f4a8bc`, main has
changed only `projects/chirality-piping` (1,054 paths).

## Findings

| ID | Severity | Location | Evidence | Consequence |
|---|---|---|---|---|
| F1 | MINOR | `OWNER_DECISIONS.md`, "Rerunning an unchanged workflow", Effect: "SEAL-2 stays deferred, to be weighed at the 90% gate" | The owner's recorded words are only "explain the implications…" and "A15 re-confirmation now (Recommended)". The earlier deferral was "Keep SEAL-2 deferred; continue other work", with no gate attached. | It attributes a gate timing to the owner that the owner did not state. Mark it as HELP_HUMAN's proposal, or remove it. |
| F2 | MINOR | `WORK_GRAPH.md`, J1 and J2 rows | The J1 row says "integrated `e653f93a1d`", but J1 was integrated at `d91fc9a360` (with J3). The J2 row says "Root wiring of `evaluate` is pending in J3", but J3 is COMPLETE and calls `evaluate_compatibility` at run preparation (`runtime_session.rs`, CK-1). | Stale or imprecise status. A reader could look for J1 in the wrong merge, or think the CK-1 wiring is still missing. |
| F3 | NOTE | `reviews/V11-J4-J5.md:392-403` | The reviewer's method states a fresh `git archive 8d98de95a8` gave 677 + 4 with 46 result lines. My fresh archive of `8d98de95a8` gives 668 + 4 with 44, and the static test count agrees. HELP_HUMAN's note at line 497 is correct. | The reviewer's suite evidence was not of the stated tree. The verdict stands, because `8d98de95a8` and the integrated tree both pass in my runs. The note could cite this confirmation. |
| F4 | NOTE | Merge `040d9af602`, `CONTRACT_ISSUES.md` | The J2 side's stale CI-17 text was dropped, and the main-line repair was kept. Because J2 never edited CI-17, this is correct. | None. Recorded because the merge commit message does not say it. |
| F5 | NOTE | `validation/J1_8a785ac4/r5-final-{1,2,3,4}*.log` | They print the full `PATH` environment value, including personal tool directories. | Not a secret. Optional: trim it before merge. |
| F6 | NOTE | `validation/INTEGRATED_e653f93a/` | Four raw logs. There is no summary naming the tree, environment, exit codes or log hashes, unlike `COMBINED_e524c087.md`. The "677" claim lives in the commit subject and the graph. | Traceability only. My reproduction confirms the figures. |
| F7 | NOTE | Method | I ran one `git fetch --dry-run` by mistake. It contacted GitHub, wrote no ref and was not relied on. All analysis used local refs. | Disclosed for custody. |

There are no BLOCKING or MAJOR findings.

## Verdict

**MERGE.** The App bytes at `f1ec8d5589` are a correct union of the reviewed
heads `2e2a02844a` and `8d98de95a8`:

- every file comes from a reviewed head or from a conflict resolution checked
  against Git's own three-way result;
- no hunk was lost;
- J5's draft-base wiring does not interact with the J1/J3 run lifecycle.

The integrated suite reproduces exactly (677 + 4 passed, 0 failed), and a main
merge touches no App v4 path. F1 and F2 are small record corrections and do not
block the merge.
