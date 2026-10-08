# V16-R1 — confirmation of the V16 repairs at `87d411d774`

2026-10-08. Type 2 TASK reviewer for run `APP-V4-GROUP-A-20261004`, dispatched
by HELP_HUMAN (Claude Opus 5.5, Claude Code). Harness-native child, no
delegation. I wrote V16 and none of the repair.

**Worktree.** I worked in my own worktree, detached at `87d411d774` (parent
`58a7bd4ccc`). My uncommitted V16 file had to be moved aside first, because
the repair commit tracks the same path. Its sha256, `84e055c5…c9f559`, equals
the committed `reviews/V16-PR1115-HEAD.md`, so nothing was lost.

**Writes and calls.** My only write is this file. The one network call was
the allowed read-only `gh pr view 1115`, which reports
`headRefOid` `87d411d774ea…`. No commit, fetch, build, credentials,
`~/.codex`, model call, UI launch or native act.

**Verdict: READY.** F1 is repaired: from a clean `git archive` of the head,
both evidence folders verify in full and every file in them is covered.
F2–F11 are repaired as recommended. The only app change is the CI-22 (c)
text, which is now accurate and consistent. The two new records
(OWNER_DECISIONS "Scratch Codex home cleanup" and the pause handoff) are
accurate where I could check them. Five NOTEs remain (R1-N1…N5), none
gating.

## Checks

| Check | Result | How |
|---|---|---|
| App bytes | `git diff 58a7bd4ccc 87d411d774 -- projects/chirality-app-v4/app` touches only `CONTRACT_ISSUES.md`, within CI-22 (c): 11 lines added, 10 removed | `git diff` |
| Re-witness evidence, clean archive | **24/24 OK**; 24 files besides `SHA256SUMS`, so every file is covered. The 23 earlier lines are unchanged, and one line was added for `workspace-listing.sha256` | `git archive 87d411d774 <run dir>`, extract to scratch, `shasum -a 256 -c`, `find -type f \| wc -l`, `git diff` of `SHA256SUMS` |
| 1113 evidence, clean archive | **29/29 OK**; 29 files besides `SHA256SUMS` | same |
| 9 re-witness workspace records | Same hashes as the bytes I checked in V16 | unchanged `SHA256SUMS` lines |
| `workspace-listing.sha256` | 18 entries, which verify **18/18 OK against the live temp workspace** (`$TMPDIR/chirality-v4-rewitness.xkv1jXeRgo/workspace`, still present). One revision-store folder (`a5138158…`) and one published copy. Its 9 record hashes equal `SHA256SUMS`. `WORKFLOW.md` `44049bcd…` and `REVIEW-NOTES.md` `4ab54fd3…` equal the WR `run_text` record's file hashes | read-only `shasum -c` in that folder; `find` |
| Scratch Codex home deleted | `…/chirality-v4-witness-codex-home.skB5uW2FWI`: "No such file or directory" | `ls` |
| Handoff references | They exist: `PAUSE_HANDOFF_ASTRA_20261006.md`, `validation/COMBINED_e524c087.md`, `validation/INTEGRATED_e653f93a/`, `dependencies/RESTORE_20261007.md`, D-7 in the 1113 record, `handshake.rs:108 hosts_codex_initialize_then_thread_start`. PRs #1110 (`e33f3e2f1b`) and #1113 (`f4358eb0be`) are merge commits in the history | `ls`, `grep`, `git log --grep` |

## Status of V16 findings

| ID | Status | Evidence |
|---|---|---|
| F1 (MAJOR) | **Repaired** | Both `workspace-records/` trees are committed: 9 files plus `workspace-listing.sha256` for the re-witness, and 18 files for 1113, matching the 1113 record's "(18 files)". Both checksum files verify from a clean archive (see above). The witness record says the files were force-added past `**/.chirality/`. `.gitignore` is unchanged, so later witnesses need the same `git add -f`; the handoff's witness recipe does not mention it (R1-N5) |
| F2 (MINOR) | **Repaired** | Row 5 now reads "**Return did not act.** … which slot Return took is not reported", citing `lib.rs:703`. The findings bullet, CI-22 (c), WORK_GRAPH J6, the handoff and the PR body read the same. CI-22 (c) keeps "Return chooses 'Don't ‹act›'" only as the design's plugin mapping, which is correct |
| F3 (MINOR) | **Repaired** | Each now says "the middle button registered when clicked; the Cancel button was not clicked", or "Of the controls the owner used, only the middle button acted": CI-22 (c), the findings, WORK_GRAPH J6, the handoff table and the PR body |
| F4 (MINOR) | **Repaired** | CI-22 (c) now puts the gating requirement in the past ("before the witness Escape had to be observed natively …") and lists the witnessed facts, the unreported slot, Cancel not clicked, and A16/request answers not witnessed. No contradiction remains. Its list structure absorbs the following file-act paragraph (R1-N1) |
| F5 (MINOR) | **Repaired** | Row 1 says D-3 is repaired for the formatted view only, and that the compact App-state JSON still prints `"root":{"bytes":[…]}` (`01`). The J7 row says the same. J7 is marked COMPLETE with that residual disclosed, but the residual is not in the handoff's follow-up list (R1-N3) |
| F6 (MINOR) | **Repaired** | **Row 11.** The listing text is marked as seen on screen and not retained. The store folder and copy now rest on `workspace-listing.sha256`, which I independently re-verified against the live workspace. **Row 12.** `runnable` is marked not retained. **Row 13.** The reply is "**not verifiable from the retained evidence**", with the reason given (the rollout file was in the home the owner chose to delete). **Account items.** A new paragraph lists the build command, the supplier, "no process" and the spoken words as HELP_HUMAN's account. **Row 6.** It says the store and copy contents are "not retained separately". Their bytes are in fact retained under identical hashes in the 1113 records (`44049bcd…`, `4ab54fd3…`); this is an observation, not a defect |
| F7 (MINOR) | **Repaired** | The new "Who did what" paragraph limits the owner's acts to the four dialog answers. It names HELP_HUMAN's steps and explains that the App's "the person" / `startedBy: person` is its interface label, not evidence of the owner. The PR body now reads "The owner gave the four dialog answers … HELP_HUMAN drove every other App step". Nothing implies personal owner review |
| F8 (NOTE) | **Repaired** | "Ledger line 2, slot sequence 1" in row 11, WORK_GRAPH J8 and the PR body; row 6 reads "first line … slot sequence 1" |
| F9 (NOTE) | **Repaired** | WORK_GRAPH J8: "integrated `6889359941` (app bytes equal `7f0300cfe2`; the CI-24 (b) R1-1 text followed in `8cd69ff7fc`)", which matches my `git diff`. DISPATCH has a new entry for the R1-1 confirmation, the re-witness, V16 and the repair, which is accurate against V16 (F1 MAJOR, F2–F7 MINOR, F8–F11 notes) |
| F10 (NOTE) | **Repaired** | PR body: "Of the reviewer's 8 mutations, 6 were killed; N6 and N8 survived …". CI-23 is listed once, with its owner. The logs list adds `J6_0501d540/` and `J8_1a74f7f3/`. The evidence folders are named through the F1 bullet |
| F11 (NOTE) | **Repaired** | An appended OWNER_DECISIONS clarification: "two key presses (Escape, Return) and two clicks (Register, Re-confirm)". The original line is not edited in place |

## New records

- **OWNER_DECISIONS "Scratch Codex home cleanup — 2026-10-08".**
  - It quotes the answer **"Delete it now (Recommended)"** and states
    custody.
  - It names the path, which is the same one as in the launch approval, and
    says it is not `~/.codex`.
  - The effect claims (process check, `~/.codex` untouched) are HELP_HUMAN's
    account and are not verifiable here. The path's absence I confirmed.
  - The entry correctly notes that a future witness needs a fresh owner
    sign-in. The re-witness record discloses that the deletion is why the
    model reply cannot be verified.
- **`PAUSE_HANDOFF_HELP_HUMAN_20261008.md`.** It is accurate where I could
  check:
  - the branches, `5a6af1cfa7` and `7f0300cfe2`;
  - the merged PRs;
  - the done table, against V13–V15-R1 and the re-witness;
  - the 717/0/3, 4 nested and 7/7 counts;
  - the open-work list, against CI-19…CI-25, O-1…O-5, R1-1 and the
    unwitnessed dialogs;
  - the standing constraints, against OWNER_DECISIONS and Root `AGENTS.md`;
  - the supplier hash, against `app/README.md:121`.

  It accepts nothing and leaves 90% to the owner. Two gaps: its "Closing
  state" section is an empty placeholder (R1-N4), and the D-3 residual is
  missing from the follow-ups (R1-N3).

## Notes (R1)

| ID | Severity | Where | Observation | Suggested repair |
|---|---|---|---|---|
| R1-N1 | NOTE | `CONTRACT_ISSUES.md` CI-22 (c), last sub-bullet | The text "**Known limit: file acts are excluded.** Their three slots are …" continues on the same line as "- The A16 and request-answer dialogs were not witnessed natively." Its continuation lines are indented 2 spaces, so in CommonMark the file-act limit renders inside that sub-bullet | Put the file-act limit on its own line, outside the new sub-list |
| R1-N2 | NOTE | Witness record, "Records" | "`workspace-listing.sha256` lists every workspace file". It lists every file under `.chirality/` (18). The workspace also holds `notes/witness.txt`, which is not listed | Say "every `.chirality/` file", or add the one file |
| R1-N3 | NOTE | WORK_GRAPH J7; handoff "Open work" | J7 is COMPLETE, but its criterion "native paths shown as readable text, not byte arrays" is only met for the formatted view. The compact-JSON residual is disclosed but routed nowhere | Add "D-3 residual: compact App-state JSON prints byte arrays" to the handoff's optional follow-ups |
| R1-N4 | NOTE | Handoff l. 20–22, l. 152–154 | "Its state at handoff is in the closing section below", but "Closing state" holds only "(Updated at handoff, below.)" | Fill in the PR 1115 state (head, CI, V16-R1 verdict, merge) before merge, or reword it as pending |
| R1-N5 | NOTE | Handoff "Machine-local resources" | Two issues. **(a) Temp roots.** It says the two temp roots "can be deleted" because their evidence is retained. The built witness binaries are retained only as hashes, so deleting them ends any re-hash; that is the owner's choice. **(b) Recipe.** The witness recipe does not mention that `workspace-records` need `git add -f` past `**/.chirality/` | Add "(binary retained by hash only)" and a recipe line "retain `.chirality/` evidence with `git add -f`" |

## Limits

- **App code.** No build or test, because the app code is unchanged; only
  the CI-22 (c) text changed, as `git diff` shows.
- **Workspace listing.** I checked it against the live temp workspace
  read-only. That workspace is machine-local and may be deleted (R1-N5).
- **The 1113 checksums.** The 1113 `SHA256SUMS` was generated at repair
  time. It attests the bytes as committed, not their state at the 1113
  witness. I did not review the 1113 record's other content.
- **Not verifiable from the repository:** the quoted owner answers,
  HELP_HUMAN's process check before deletion, and the model reply. They are
  disclosed as such.

## Return

- Verdict: **READY.** V16 F1–F11 are repaired. The evidence verifies
  24/24 and 29/29 from a clean archive of `87d411d774`. The app change is
  CI-22 (c) text only.
- R1-N1…N5 are optional NOTEs. R1-N4 (the handoff's empty closing state) is
  worth filling before merge.
- No owner question.
