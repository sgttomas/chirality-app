# V7 — independent review of the combined pause checkpoint

2026-10-07. Type 2 TASK reviewer (Claude Opus 5.5, Claude Code), dispatched by
HELP_HUMAN (Claude Opus 5.5, Claude Code, 2026-10-07). No delegation. I did not
author any of the code or records under review. Sole write: this file. No
commit, push, network, credentials, `~/.codex`, model call or native UI.
Read: Root `AGENTS.md`, `agents/AGENT_TASK.md`, `projects/chirality-app-v4/loop/LOOP_INIT.md`.

## Candidate and scope

- Candidate: **`3d0db214cb339695709a4c6be0b9510d51e6c95e`** (branch
  `claude/app-v4-group-a-resume`).
- Base: merged PR 1099, `c1571f7febcb4b710c8aa5633f1f5c4460c3faf3`.
- Commits reviewed: `0a2ed81b47` (five-contribution fan-in plus run records),
  `e524c087f5` (handoff addendum only), `3d0db214cb` (run records only).
- App source at the candidate equals `e524c087f5` and `0a2ed81b47`: every path
  in the three integration records has the same hash at all three commits, and
  `git diff --name-status 0a2ed81b47 3d0db214cb -- projects/chirality-app-v4/app`
  is empty.
- All 253 changed paths are under `projects/chirality-app-v4/`; none are
  deleted; nothing under `foundation/thesis/`.

## Method actually performed

1. **Hash check.** For every path in `changes/I1-RECOVERY-CUSTODY-INTEGRATION.json`
   (14), `changes/REC-WR-RS-BOUNDED-INTEGRATION.json` (20) and
   `changes/I2-COMPATIBILITY-CORE-INTEGRATION.json` (3), I computed sha256 of
   `git show <rev>:<path>` at the candidate, `e524c087f5`, `0a2ed81b47` and the
   base, and checked the I2 preimages at the base.
2. **Fan-in reconstruction.** I extracted the base App tree with `git archive
   c1571f7feb` into a scratch folder and applied, in order, the five retained
   contribution patches with `git apply --check` then `git apply`:
   `recovery/PAUSE-ASTRA-20261006/rec/cold03.patch` (REC custody),
   `.../rec-root/recovery-root.patch` (REC Root),
   `.../compatibility/compatibility-core.patch`,
   `changes/I2-WR-PUBLICATION-IMPLEMENTATION-ASTRA.patch` (WR) and
   `changes/private-rs-supply-current-tests/implementation.patch` (RS). All
   applied cleanly. `diff -rq` against `git archive 3d0db214cb` of the App tree
   reports exactly one difference: `CONTRACT_ISSUES.md`.
3. **Review-basis chain.** I compared the shared files across the retained
   review manifests (`rec/baseline-manifest.json`, `rec/repaired-manifest.json`,
   `rec/cold03-manifest.json`, `rec-root/baseline-manifest.json`,
   `rec-root/source-manifest.json`, `compatibility/BASE_MANIFEST.json`,
   `wr/basis-manifest.json`, `changes/private-rs-supply-current-tests/joined-source-manifest.json`,
   `CURRENT_APP_SOURCES.json`) with the base and candidate hashes.
4. **Diff reading.** I read the full base-to-candidate diffs of `lib.rs`,
   `hosting.rs`, `recovery.rs`, `records.rs`, `workflow_workspace.rs`,
   `execution_compatibility.rs`, `App.tsx`, `RecoveryCustodyPanel.tsx`,
   `recovery_root_view.rs`, `runtime_core/MANIFEST.json`, `SOURCE_MAP.json`,
   `schemas/manifest.json`, both `policy_standing` `basis.json` files and
   `CONTRACT_ISSUES.md`, plus every `#[path]`/`mod` declaration that routes the
   new modules and test modules.
5. **Canonical-source check.** For every resource manifest and source map
   under `src-tauri/resources/` and `src-tauri/schemas/manifest.json` at the
   candidate, I checked the file hash against the manifest and the bytes
   against the named canonical source (Git bytes). I checked every changed
   Design file against the hashes pinned in `CC-WR-RS-SOURCE-ADOPTION.json`,
   `CC-WR-END-NOTICE-SOURCE-ADOPTION.json` and `CC-REC-ITEM-TURN-SOURCE-ADOPTION.json`.
6. **Reproduction.** On a `git archive 3d0db214cb` extract of
   `projects/chirality-app-v4` in my scratch folder (not the checkout), with
   the brief's environment (`CARGO_HOME=~/Library/Caches/chirality-dev/cargo-home-group-a`,
   `CARGO_NET_OFFLINE=true`, `CARGO_TARGET_DIR=$TMPDIR/v7-review-target`, stock
   Codex 0.160.0 `bin/codex` sha256 verified as `112fae7a…4b4b`, its
   `codex-path` on `PATH`): `cargo test --offline --locked` in `src-tauri`.
   Toolchain cargo 1.92.0, rustc 1.92.0. I also ran `tsc --noEmit` and
   `python3 schemas/sync.py` on the same extract.
   My first run extracted only `app/` and failed one test,
   `attachments::embedded_assets_match_canonical_sources_...` (`NotFound`),
   because that test reads canonical sources under `execution/`. That failure
   was an artifact of my extraction; I re-extracted the whole
   `projects/chirality-app-v4` tree and reran.
7. **Claims.** I checked the counts, hashes and statements in
   `validation/COMBINED_e524c087.md` and its logs, `PAUSE_HANDOFF_ASTRA_20261006.md`,
   `OWNER_DECISIONS.md` (3d0db addition), `READING.md`, `dependencies/RESTORE_20261007.md`,
   the work-graph changes, `probes/NATIVE_UI_B44_*`, `RETAINED.json` and the
   final verdict sections of the five V6 reviews.
8. **Hygiene.** I ran `origin/main`'s `tools/validation/validate_run_record_leaks.py
   --base c1571f7feb --head 3d0db214cb` (read-only), grepped the added lines for
   credential patterns and home paths, hashed every added file to find
   byte-identical duplicates, and listed the largest additions.

## Answers

### 1. Integration preservation

All 37 recorded hashes were checked. 36 match at the candidate. The one
mismatch is `src-tauri/src/hosting.rs` in `I1-RECOVERY-CUSTODY-INTEGRATION.json`
(`45bd26eb…`); the candidate has `2e927378…`, which is the REC Root postimage in
`REC-WR-RS-BOUNDED-INTEGRATION.json`. This is sequential layering, not loss:
REC Root's reviewed baseline (`rec-root/baseline-manifest.json`) and the
compatibility baseline both have `hosting.rs = 45bd26eb…`. REC Root's only
`hosting.rs` hunk appends a `#[cfg(test)]` declaration of `recovery_root_tests`
(`recovery-root.patch` lines 1–9). See F1.

I2 preimages: `execution_compatibility.rs` at the base is `ecdfb8b0…`, as
recorded. The two new files are absent at the base, as recorded.

The patch reconstruction (method 2) reproduces every App file at the candidate
byte for byte except `CONTRACT_ISSUES.md`. So the candidate holds the five
contributions and nothing else in code: no lost hunks and no extra hunks.

App paths changed between base and candidate that no integration record
covers: **only `projects/chirality-app-v4/app/CONTRACT_ISSUES.md`** (+33 lines,
new CI-16 and CI-17 log entries). Its candidate hash `cfb790b9…` is already in
the REC Root and compatibility review baselines. The WR basis still had the
base hash `c499a9fc…`. It is the contract-issue log that LOOP_INIT requires,
not code. See F2 and F3.

### 2. Interactions

- **Shared files.** The only App file touched by two contributions is
  `hosting.rs` (custody, then REC Root), and those changes were stacked and
  reviewed in that order. `lib.rs` and `App.tsx` are touched by REC Root alone.
  `recovery.rs` and `runtime_core/MANIFEST.json` are touched by custody alone.
  `records.rs`, `RS_RECORD.schema.json`, `schemas/manifest.json` and the two
  `basis.json` files are touched by RS alone. `workflow_workspace.rs` and
  `SOURCE_MAP.json` are touched by WR alone. `execution_compatibility.rs` is
  touched by compatibility alone. The WR+RS joined review tree
  (`joined-source-manifest.json`, 261 entries) equals the candidate except in
  REC and compatibility files and the four ignored `gen/schemas` outputs. So WR
  and RS were reviewed together on top of each other, and RS's
  `use crate::workflow_workspace::publication` dependency was present when it
  was reviewed.
- **Registrations.** `read_recovery_custody` is defined once and registered
  once in `generate_handler!`. `mod recovery_root_view` is declared once.
  Command arguments `mode_home_class`/`generation` match the frontend's
  `modeHomeClass`/`generation` under Tauri's camelCase mapping.
  `RecoveryCustodyPanel` is imported and rendered once.
- **Schema and manifest entries.** No two contributions edit the same manifest.
  All 12 `runtime_core/MANIFEST.json` rows, 9 `SOURCE_MAP.json` rows and 6
  `schemas/manifest.json` rows match file hashes and canonical source bytes. So
  do the attachments (3), catalog_adapter (44), external_trace (10 + 6),
  hosting (1) and policy_standing (4) manifests. Both `basis.json` pins were
  updated to the new `RS_RECORD.schema.json` hash `84200fd0…`. All 13 changed
  Design files equal the hashes pinned by the three source-adoption records.
  `schemas/sync.py` reports 6 matches. The one gap is F9.
- **Test-module routing.** The new modules are routed as
  `hosting::execution_custody(_tests)`, `hosting::recovery_root_tests`,
  `records::supply::tests`, `workflow_workspace::publication::tests` and
  `execution_compatibility::report::tests`. All are `#[cfg(test)]` where they
  should be. The base-to-candidate diff adds 45 `#[test]` attributes and
  removes none. Each of the 45 tests, including
  `hosting::conversation_transport_tests::recovery_custody_rc2_cross_session_actual_tag_writer_keeps_new_metadata`,
  appears as `... ok` in `validation/COMBINED_e524c087/rust.log`. The removed
  `record_supply_original_control.rs` is absent and unreferenced.
- **Semantic coupling.** REC does not reference WR, RS or the compatibility
  code. Compatibility uses only base modules (`role_lifecycle`,
  `workflow_workspace::Selection`). RS uses WR. Nothing found conflicts.

### 3. Claims

Verified as stated:

- **COMBINED_e524c087.md.**
  - The five log hashes match.
  - There are 40 `Running`/`Doc-tests` targets. The summary lines sum to 599
    passes, which is 595 top-level plus 4 nested FIFO executions. There are 0
    failures and 3 ignored, and the run took 58.94 s.
  - 550 → 595 is exactly the 45 new tests, and `b44f6bfc..c1571f7feb` changes
    no App file.
  - Node shows 3 passed and 0 skipped. The schema-sync and frontend logs are as
    stated.
  - The "what it does not establish" section is accurate: every warning is
    dead code, and it names the unconnected WR, lifecycle and compatibility
    parts.
  - Two wording errors: F4 and F5.
- **My reproduction agrees.** 40 targets, 599 summary passes (595 top-level
  plus 4 nested), 0 failures, 3 ignored, exit 0. Log sha256 `76cf358f41840232fe461d632eac18835bb262acff4c24d1119520e97a57eaaf`
  (scratch only, not retained in the repository). `tsc --noEmit` exits 0, and
  `schemas/sync.py` reports 6 matches.
- **PAUSE_HANDOFF.**
  - The path counts (14, 6, 5, 9, 3) match the integration records.
  - "only a cfg(test) inclusion on reviewed Host" is true (recovery-root.patch).
  - "23 independent" for custody matches V6-RECOVERY-CUSTODY-CORE's 15 + 1 + 7.
  - All five V6 reviews end READY for bounded fan-in or adoption at the
    integrated bytes.
  - `RETAINED.json` indexes 90 files, all present and hash-equal.
  - `evidence/NATIVE-WORKFLOW-832-USED/` holds 21 files plus `RETAINED.json`.
  - Its statements that the fan-in was "uncommitted" and "not compiled" were
    true when written. They are superseded by `COMBINED_e524c087.md` and the
    3d0db work graph.
- **Native Cancel.** Every record claims that native Cancel is unverified,
  never that it succeeded:
  - handoff lines 83 and 87;
  - `NATIVE_UI_B44_RESULT.json` `second_pass.result` and `limits`;
  - the e524 commit body.

  The e524 addendum states truthfully that no agent saw which control dismissed
  the late popup, and that no record inventory was taken after the dismissal.
  So `workspace_files_after_quit` in the result file predates that dismissal.
- **Human-confirmed A4.** The handoff (line 48) and the result file
  (`first_pass.owner_clarification`) agree word for word on the owner quote,
  and on the split: the agent selected the fixture and opened the flow, the
  human confirmed, and the tool did not see the dialog. The proposal's
  dismiss-only boundary is preserved. No record claims an automatic-capture
  defect or an engineering qualification.
- **Owner quotes.** I have no access to the source chats. I can check only
  internal consistency, and every quote I found is the same wherever it
  appears. The 3d0db answers are quoted as the selected option labels, with
  their custody stated.
- **RESTORE_20261007.md.** Verified in full:
  - 31 crate archives totalling 3,402,493 bytes (= 3,223,082 + 179,411);
  - every archive in the isolated home's `registry/cache` matches the listed
    byte count and sha256, and every hash appears in `DOWNLOAD_SET.json` or
    `COMMONMARK_DOWNLOAD_SET.json`;
  - 27 index files totalling 1,183,319 (19) + 607,475 (8) bytes, and all 27
    raw bodies in `approved-index-group-a` match their listed sha256.
- **READING.md.** The pins checked for Root `AGENTS.md` (`f96feb19…3977`),
  `AGENT_HELP_HUMAN.md` (`0c2fe7a3…3c87`) and `LOOP_INIT.md` (`c2e88f81…85bd`)
  match the candidate.

Claims needing a correction: F3, F4, F5, F6, F7 and F8 below.

### 4. Hygiene

- **Secrets.** None found. `validate_run_record_leaks.py` from main reports
  `PASS: 202 changed run-record file(s) scanned; 0 possible credential(s); 0
  machine-local symlink(s)`. My own pattern scan of the added lines found no
  key, token or private-key material. The `auth.json` mentions are prohibitions
  in prose and test assertions that the file is absent.
- **Home paths.** No App file in the diff contains an absolute home path. 43
  run-record files do: logs, manifests, reviews and evidence helpers. They
  point to `/Users/ryan/.codex/worktrees/…`, `/Users/ryan/.rustup`,
  `/tmp/...` and `/private/tmp/...`. As historical provenance these are
  acceptable. The one that reads as a standing build instruction is F6.
- **Large and duplicate evidence.** 3.59 MB is added in total. About 0.44 MB is
  byte-identical copies inside the run:
  - eight identical `rec-root/validation/*.source.json` files (33,146 B each);
  - three identical `NATIVE-WORKFLOW-832-USED/{commit-app-manifest,copied-pre-injection,source-before-copy}.json`
    files (44,568 B each);
  - `rec/cold03.patch` = `rec/cold03-checked/cold03.patch` (95,445 B);
  - `CC-REC-ITEM-TURN-SOURCE-ADOPTION.json` stored three times;
  - the compatibility patch stored twice.

  A further about 0.32 MB is `changes/proposed-rs-supply/RECORD_SEMANTICS.md`
  and `RS_RECORD.schema.json`, which are identical to the adopted Design files.
  The largest file is `compile.stdout.jsonl` (356 KB). Each file is cited by a
  manifest or index, so each is plausibly needed for byte-exact custody. None
  must be kept off main. See F10.

## Findings

| ID | Severity | Location | Evidence | Consequence |
|---|---|---|---|---|
| F1 | NOTE | `changes/I1-RECOVERY-CUSTODY-INTEGRATION.json:17` | Records `hosting.rs` `45bd26eb…`. The candidate has `2e927378…`, the REC Root postimage recorded in `REC-WR-RS-BOUNDED-INTEGRATION.json`. `rec-root/baseline-manifest.json` has `45bd26eb…`, and the REC Root hunk is a cfg(test) declaration only. | A reader who checks the I1 record alone sees a mismatch. The chain is verifiable, and the patch reconstruction proves no hunk was lost. Optionally add a supersession note. |
| F2 | NOTE | `app/CONTRACT_ISSUES.md:245-276` | This is the only App path outside every integration record. It is not produced by any of the five patches, and it is present in the REC Root and compatibility review baselines. | Not a code change. The integration records and the PAUSE_HANDOFF claim "exact … postimage checks" do not account for it. Name it in the PR description. |
| F3 | MINOR | `app/CONTRACT_ISSUES.md:274` | CI-17 says "Consumer propagation and actual cold-tuple tests remain pending; RC1-COLD is not closed". The candidate includes the cold03 tests, and V6-RECOVERY-CUSTODY-CORE's final verdict states "RC1-COLD is repaired". The REC Root consumer is also integrated. | The maintained contract-issue log understates the integrated state. Update CI-17 to say what remains open: native quit/relaunch, PI-6 and downstream adoption. |
| F4 | MINOR | `validation/COMBINED_e524c087.md:15` | Says "51 warnings". `cargo-build.log` shows `(lib) generated 50 warnings`. The 51 counts `^warning` lines, including that summary line. | A small factual error in the validation record. Correct it to 50. |
| F5 | NOTE | `validation/COMBINED_e524c087.md:5` | "App sources equal the 276-file pause manifest byte for byte". The commit holds 272 App files, which all match. The other 4 manifest entries are gitignored `src-tauri/gen/schemas/*` outputs of tauri-build. | Wording precision only. Say "the 272 tracked files match; 4 gitignored generated files are not committed". |
| F6 | MINOR | `PAUSE_HANDOFF_ASTRA_20261006.md:52, 56-62, 75` | Says in the present tense that "Immutable binaries stay at their reported private paths", tells the reader to retain the `/tmp` and `/private/tmp` homes, and gives a Cargo setup with `CARGO_HOME=/tmp/...` and `CARGO_TARGET_DIR=/Users/ryan/.codex/worktrees/077c/...`. OWNER_DECISIONS (3d0db) and WORK_GRAPH line 8 record that a restart destroyed these. Yet WORK_GRAPH line 10 says the handoff "remains the account". | A resuming agent could rely on paths and binaries that no longer exist, or reuse a machine-local Cargo setup in place of the restored one. Add a dated one-line pointer in the handoff to OWNER_DECISIONS "Resume in Claude Code" and `RESTORE_20261007.md`. |
| F7 | MINOR | `OWNER_DECISIONS.md:105` | "says the human has passed the 60% gate" is a paraphrase of the steer. No other record of that gate assessment exists in this run or in `Acceptances/`. Other owner entries in the file use exact quotes and state their custody. | LOOP_INIT reserves stage-gate assessment to the owner. The only record of a passed gate is unquoted. Add the owner's exact words and their custody. |
| F8 | NOTE | `WORK_GRAPH.md:7` (Branch bullet) | "Main's later commits touch Piping only". The origin/main ref fetched at 10:22 −06:00, before the 12:15 commit, also changes `tools/validation` (2), `docs/governance_harness` (1) and `exports/chirality-app` (1). The 08:19 fetch was Piping only. | Stale but harmless: the candidate and main share no paths (0 common), so there is no merge interaction. |
| F9 | NOTE | `app/src-tauri/resources/runtime_core/MANIFEST.json` | The new `recovery.custody-event.schema.json` is in `runtime_core/` and included by `execution_custody_tests.rs`, but it has no manifest row. Its bytes equal the Design source today (`03339850…`; origin in `rec/custody-schema-origin.json`). | No maintained check guards drift between the App copy and the Design source. Consider adding a row. |
| F10 | NOTE | Run records (see Hygiene) | About 0.44 MB of byte-identical copies inside the run. About 0.32 MB is copies identical to adopted Design files. `compile.stdout.jsonl` is 356 KB. No secrets, and no home paths in App files. | Optional: dedupe before merge. Nothing has to be withheld from main. |
| F11 | NOTE | `.github/workflows/*` on main | No workflow mentions `chirality-app-v4`. The REC Root panel has no maintained frontend test; its controls are in run evidence only (`rec-root/validation/panel-controls*.mjs`). | Required CI will not exercise this code. The evidence for merge is the local combined check plus this independent reproduction, both at these exact bytes. |
| F12 | NOTE | Branch head | While I was reviewing, HEAD moved to `47a6b9069a`, which adds 25 lines to `DISPATCH.md` only and changes no App path. I did not review `DISPATCH.md`. This review file is uncommitted. | The PR head differs from the reviewed `3d0db214cb` only by run records. Review those added records separately if required. |

No BLOCKING or MAJOR finding.

## Verdict

**MERGE.** The candidate holds exactly the five reviewed contributions, which
the retained patches reproduce byte for byte, plus `CONTRACT_ISSUES.md`. No
lost hunks, duplicate registrations, conflicting schema or manifest entries or
test-module routing errors were found. Every canonical-resource correspondence
holds. The combined test result reproduces independently: 595 top-level
passes, 0 failures. The records do not claim native Cancel, a native
qualification, the 90% gate or a release. F3, F4, F6 and F7 are cheap record
corrections, and I recommend adding them to the same PR. They are not
preconditions for merge.

## Repair confirmation — 2026-10-07

Same reviewer. Read-only check of repair commit `3858932890` and merge
`9b83f23f3a` (PR 1110 head). This append is my only write.

**Scope.** `git diff 3d0db214cb 9b83f23f3a -- projects/chirality-app-v4`
touches seven files: `app/CONTRACT_ISSUES.md`, `DISPATCH.md`,
`OWNER_DECISIONS.md`, `PAUSE_HANDOFF_ASTRA_20261006.md`,
`validation/COMBINED_e524c087.md`, `WORK_GRAPH.md` and this review. No other App
v4 file changed. The only App path is the contract-issue log, so no code,
schema, resource or test changed. `git diff 3858932890 9b83f23f3a --
projects/chirality-app-v4` is empty. The committed copy of this review
(sha256 `42373e62…6549`) is byte-identical to what I wrote.

| Finding | Repair | Status |
|---|---|---|
| F3 | CI-17 now records cold03 tests, RC1-COLD repaired for the core scope and Root consumer integrated. It keeps native quit/relaunch and PI-6 open. | Resolved |
| F4 | Now reads "50 warnings". | Resolved |
| F5 | Now reads "272 tracked files, plus 4 gitignored `src-tauri/gen/schemas` build outputs". | Resolved |
| F6 | A dated "Superseded machine-local facts" section marks the private trees, executables, Cargo home and settings, and the `.codex/worktrees/077c` target as gone. It points to the current records. | Resolved |
| F7 | Exact steer words with custody, plus the gate act. I confirmed "I am accepting the 60% gate cleared." verbatim at `APP-V4-GRAPH-CLOSURE-20261004/OWNER_DECISIONS.md:83`. I cannot see the init prompt, so I cannot check the steer quote against its source. | Resolved |
| F8 | Now lists Piping, `tools/validation`, `docs/governance_harness` and `exports/`, with no shared paths. This matches my check. | Resolved |
| F12 | `DISPATCH.md` reviewed: see below. | Resolved, with one NOTE |

**DISPATCH.md, F12.** The added section states the mechanism, agent type,
constraints and write scopes. Both
`claude/app-v4-j1-publication` and `claude/app-v4-j2-compatibility` exist
locally at `3d0db214cb`, so the base correction holds.

- **R1 (NOTE).** The correction names J1's worktree as
  `.claude/worktrees/app-v4-j1-publication`, but `git worktree list` shows the
  J1 branch checked out at `.claude/worktrees/agent-a30b47a03f09fe083`. The
  J2 branch is at `.claude/worktrees/agent-af2ce0ad2cee92fc1`. Record the
  actual paths, or drop them.

F1, F2 and F9–F11 were NOTEs and stand as written.

**Updated verdict: MERGE** at `9b83f23f3a`.
