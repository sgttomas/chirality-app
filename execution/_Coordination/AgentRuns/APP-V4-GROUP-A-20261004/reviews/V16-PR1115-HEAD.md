# V16 — independent head review of PR 1115 at `58a7bd4ccc`

2026-10-08. Type 2 TASK reviewer for run `APP-V4-GROUP-A-20261004`, dispatched
by HELP_HUMAN (Claude Opus 5.5, Claude Code). Harness-native child, no
delegation. I wrote none of the material reviewed here. I worked on branch
`review/v16`, created at `58a7bd4ccc` in my own worktree. My only write is
this file. No commit, fetch, credentials, `~/.codex`, model call, UI launch,
build or native act. The one network call was the allowed read-only
`gh pr view 1115 --json body,…`.

**Verdict: NOT READY.** One MAJOR finding gates merge, and its repair is
mechanical. F1: the witness's workspace records are not in the PR. The
record says they are kept "byte for byte", and `SHA256SUMS` lists them, but
`**/.chirality/` in `.gitignore` kept all 9 files out of the commit. At the
PR head, `shasum -c` fails 9 of 23 lines. The files exist only in
HELP_HUMAN's checkout. There they match `SHA256SUMS` exactly, so a forced add
repairs F1. The 1113 witness record, also in this PR, has the same gap: 18
files.

The app change is only `CONTRACT_ISSUES.md` text, and the CI-24 (b) bullet
is accurate. Most observations in the witness record match the screens and
records. The MINOR findings are wording that goes beyond the evidence, all
textual:

- **F2.** "Return chose Don't register".
- **F3.** "Only the middle button acted".
- **F4.** Stale "Escape: not yet observed" text in CI-22 (c).
- **F5.** "D-3 repaired".
- **F6.** Claims cited to evidence that does not show them.
- **F7.** Who drove the non-dialog steps.

I recommend fixing them in the same repair commit, but they do not gate
merge. Nothing suggests personal owner review beyond the dialog presses and
the owner's quoted words. The PR body's "owner pressed every key and button"
is broader than the record (F7).

## Candidate and basis

| Item | Value | How checked |
|---|---|---|
| Head | `58a7bd4ccc` (`claude/app-v4-group-a-resume`); PR 1115 `headRefOid` `58a7bd4ccc40…` | `git log -1`; `gh pr view` |
| Commits since the J8 review candidate | `fdfdcd0b6e`, `b656cf6a9c`, `6889359941` (merge), `8cd69ff7fc`, `b8c26320ef`, `bf8fa4c732`, `58a7bd4ccc` | `git log 7f0300cfe2..58a7bd4ccc` |
| Non-validation files changed since `7f0300cfe2` | `app/CONTRACT_ISSUES.md`, `DISPATCH.md`, `OWNER_DECISIONS.md`, the evidence folder (15 files), the witness record, `reviews/V15-J8-RECONFIRM-R1.md`, `WORK_GRAPH.md`; the rest is `validation/J8R_7f0300cf/` and `validation/V15R1_7f0300cf/` | `git diff --stat` |
| `CONTRACT_ISSUES.md` | `9d58db66…a4e2facc` | `shasum -a 256` |
| Witness record | `acede887…c79cb37e` | same |
| `DISPATCH.md` / `WORK_GRAPH.md` | `d0d5b189…33a40514` / `b7609f6b…3e4288b1` | same |
| Evidence `SHA256SUMS` | `6aa37afd…dec38ba8`, 23 lines | same |

## (1) App bytes

- **Only `CONTRACT_ISSUES.md` changes.**
  `git diff --stat 7f0300cfe2 58a7bd4ccc -- projects/chirality-app-v4/app`
  shows one file, with 17 lines added and 1 removed.
  - `7f0300cfe2 → 6889359941` is empty, as the R1-1 confirmation found.
  - `6889359941 → 8cd69ff7fc` adds 11 lines, the CI-24 (b) bullet.
  - `8cd69ff7fc → 58a7bd4ccc` adds 6 lines and changes 1, the CI-22 (c)
    "Witnessed" sentence.
- **The CI-24 (b) R1-1 bullet is accurate.** It matches V15-R1 R1-1 and
  probe P6 on each element:
  - the condition: an *Intended* attempt after an append that wrote nothing;
  - the behaviour: refused on `ledger_seq`, then the quoted "durability
    uncertain" text;
  - the safety facts: one line, a readable ledger, ‹k› not held;
  - the gap: the *not completed* line is never shown;
  - the repair, with P6 as its test, left open.

  The R1-1 confirmation already covers this. I agree with it.
- **The CI-22 (c) addition** has four parts:
  - **Escape.** "Escape closed the alert with no capture or registration" is
    supported. The screens show the App's "native confirmation dismissed;
    no capture/registration" (`02`), and the retained records hold no
    capture for review `a77c04d8`.
  - **Escape's slot.** "Which non-act slot Escape takes is not shown by the
    App" is accurate. `lib.rs:703` maps every non-act result (`Ok(None)`) to
    the same status.
  - **A16 and request answers.** "Not witnessed natively" is accurate.
  - **Overclaims and a stale sentence.** "Return chose 'Don't register'" is
    an inference stated as an observation (F2). "Only the middle button
    acted" overstates, because Cancel was never pressed (F3). The sentence
    before the addition still reads "Escape: not yet observed … unestablished
    … must be witnessed natively before any person relies on the build"
    (F4).

## (2) Native re-witness record

**Integrity.** The 14 committed evidence files pass `shasum -a 256 -c`. The
9 `workspace-records/.chirality/…` entries fail with "No such file" (F1).
`git ls-tree -r 58a7bd4ccc` of the evidence folder lists 15 paths and no
`workspace-records`. `git check-ignore -v` names `.gitignore:8:**/.chirality/`.

I read the 9 files from HELP_HUMAN's checkout, read-only
(`…/test-ci-optimization-f6cacd/…/evidence/NATIVE-RECONFIRM-WITNESS-8cd69ff7/`).
There, all 23 lines of the identical `SHA256SUMS` verify OK (`diff` of the
two sums files is empty). I used those bytes for the checks below.

**Claims checked against evidence:**

| Record claim | Evidence | Result |
|---|---|---|
| Binary `63f2d8d0…e555a1`, re-hashed at both launches | Line 1 of `launch-1.log` and `launch-2.log`; equal to the hash in the OWNER_DECISIONS launch approval | Confirmed |
| Built from `8cd69ff7fc`; app bytes = `7f0300cfe2` + CI-24 text | `source-head.txt` = `8cd69ff7fc8e…`; my diff in (1) | Source confirmed. The build command, "offline" and the binary-to-source link are not retained (F6) |
| Identifier `dev.chirality.v4.rewitness` | `overlay.json` | Confirmed |
| Codex 0.160.0, `bin/codex` `112fae7a…b4b`, `CHIRALITY_ALLOW_UNVERIFIED=1` | Not retained. The hash equals the expected hash in `app/README.md:121` | HELP_HUMAN's account (F6) |
| Launch at 02:53:24Z and 03:04:24Z; exit 0 | Launch logs | Confirmed. "App menu's Quit" and "left no process" are not retained |
| Row 1: "not runnable" (CI-18); review `a77c04d8…`, digest `1fc901a5…277df` | `01` | Confirmed. **"Paths are shown as text, not byte arrays (D-3 repaired)" is contradicted by `01`** (F5) |
| Row 2: statement contents; buttons [Cancel] … [Register] [Don't register]; App readable beside the alert | `01` | Confirmed |
| Row 3: Escape → dismissed, nothing recorded | `02`; captures and act log hold only descriptors `1db6946a` and `c0000a8f` | Confirmed from the final state. The owner's "dialog closed" is not retained |
| Row 4: review `f440554a…`, digest `ddef582c…`; "Don't register" highlighted as default | `03` (blue button) | Confirmed |
| Row 5: Return → dismissed, nothing recorded; "**Return chose 'Don't register'**" | `04`; records | No act confirmed. Which slot was chosen is inferred (F2) |
| Row 6: review `1db6946a…`, digest `e7ead527…`; ledger `registered`, sequence 1, 03:03:57.410Z; one capture and act-log entry | `05`; `workflow-registry.jsonl` line 1; capture `486044ef…`; `acts.jsonl` seq 1 | Confirmed. The offer digest `7513e843…` in `05` equals the capture. "One revision-store folder and a published copy" are not retained (F6) |
| Row 7: no selection after relaunch | `06` (`"selection": null`) | Confirmed |
| Row 8: listing label and "offered" | `06` | Confirmed |
| Row 9: DS-8 review `c0000a8f…`, digest `06736e59…09c5`, quoted sentence | `07` | Confirmed verbatim |
| Row 10: statement, purpose, quoted sentence, [Cancel] [Re-confirm] [Don't re-confirm], default | `08` | Confirmed. The offer digest `f1237c14…` equals capture `ab59a9c4…` |
| Row 11: `re-confirmed`, disposition *re-confirmation*, "sequence 1", 03:05:35.355Z, `reconfirms` revision 1 | Ledger line 2: `ledger_seq` 2, `sequence` 1, `reconfirms.sequence` 1, same `store_path` as line 1 | Confirmed. "Sequence 1" is the slot; the line itself is ledger line 2 (F8) |
| Row 11: status `newRevision:false`, `selectable`, `state` | `09` | Confirmed |
| Row 11: listing "registered — selectable in this App session" (`09`) | Not in `09` or any other screen | Not evidenced (F6) |
| Row 11: no new store folder or published copy | Only the identical `store_path` is retained | Consistent; not shown (F6) |
| Row 12: `runnable: true`, standing "registered revision" | Not in any screen. The WR selection record has `"standing": "registered"` | Partly evidenced (F6) |
| Row 12: CK-1, CK-2, "selection and run_text recorded before send … run opened" | `10` | Confirmed |
| Row 12: RS `run_opened` cites name, origin `project`, revision `1b1733864cd8…` | The `runs/…/2c32e50c….jsonl` line 1 (`revisionVerification: verified`) | Confirmed. Order: selection 03:06:22.678Z, `run_text` 03:07:50.412Z, `run_opened` 03:07:58.617Z |
| Row 13: model `gpt-6.1-sol` (openai) | `10`, conversation selector "… openai/gpt-6.1-sol" | Confirmed |
| Row 13: native user message began "[Chirality] Workflow run start: …" | WR `run_text` record `start_line` (text identity `dfc0b22d…`) | The prepared text is confirmed. What was delivered natively is not retained |
| Row 13: the model's reply (quoted) | No screen; the RS log has only `run_opened` | **Not verifiable from the evidence** (F6). The record does correctly say adoption is unknown |
| O-1: title "register workflow" on the re-confirmation | `08` | Confirmed |
| O-2: "Register this review…" button; "before choosing Register" | `08`, `09` | Confirmed |
| O-5: `captures/pending/…` remain | Both pending files retained | Confirmed |

**Escape, Cancel, defaults, "no new revision" and the model reply.**

- **Escape.** Stated correctly as "did not act", with the slot unknown.
- **Cancel.** Correctly "not witnessed as such" in the findings. Contradicted
  in spirit by "only the middle button acted" (F3).
- **Defaults.** Witnessed for A15 and the re-confirm variant (`03`, `05`,
  `08`). In `01` no button is highlighted, because the alert was not key;
  the record does not claim a default there.
- **"No new revision."** Supported by the screens' statement text and by
  `newRevision: false`. The folder claim is not shown (F6).
- **Model reply.** Not verifiable (F6).

**Owner review.** The record attributes to the owner only these:

- the presses of Escape, Return, Register and Re-confirm;
- the words "dialog closed", "done", "done" and "done".

It never says the owner read or reviewed the statement or the review.
Neither OWNER_DECISIONS nor the record claims an owner review. However, the
retained App records say `selected_by: "the person (App interface)"` and
`startedBy: {kind: person}`. Per the record header and the approved plan
("HELP_HUMAN sends one real model turn"), HELP_HUMAN drove those steps. The
record does not say so (F7).

## (3) Run records

**OWNER_DECISIONS** (diff `b9a818d580..58a7bd4ccc`; added in `81a18adea4`,
`9d1e0bb0cd` and `bf8fa4c732`):

- **"Native confirmation default key — 2026-10-08".** It quotes the answer
  **"Three buttons; Return is safe (Recommended)"** and states custody: "a
  structured answer in the active Claude Code chat". The options offered are
  listed. The effect is labelled as HELP_HUMAN's.
- **Correction.** It is appended, not edited in place. It attributes the
  overstatement to HELP_HUMAN's effect line and says "The owner's answer is
  unchanged". This is correct handling.
- **"Native re-witness launch — 2026-10-08".** It quotes **"Approve; reuse
  sign-in (Recommended)"**, with custody stated. The approved artifact hash
  equals both launch logs, and the plan (two launches; Escape, Return,
  Register, then Re-confirm; HELP_HUMAN sends one turn) matches the
  record's steps.
  - Its last line, "Each dialog act is the owner's own key press", is loose:
    Register and Re-confirm were clicks. That is a NOTE inside F11.
- **Not checkable here.** I cannot compare the quoted answers with the chat
  itself, which is not in the repository. They are internally consistent
  and their custody is stated.

**DISPATCH.md** (`81a18adea4..58a7bd4ccc`). Every checkable claim holds:

- `1a74f7f307`'s parent is `39519096c4`. Its `a15_native.rs` and
  `act_control_a15.rs` blobs (`55abed0e…`, `be7bb384…`) equal those at
  `007489e72b`.
- `reviews/V15-J8-RECONFIRM.md` has sha256 `16c99a2c…6366`.
- `SHA256SUMS` verifies in full in `validation/J8_1a74f7f3/` (17),
  `V15_1a74f7f3/` (15), `J6_5a6af1cf/` (21), `J8R_7f0300cf/` (25) and
  `V15R1_7f0300cf/` (14). The V15R1 hashes equal those in the V15-R1
  review's table.
- `8868614f93` is an ancestor of `5a6af1cfa7`.
- `745f09397c` (parents `79bb77ef50`, `5a6af1cfa7`) has `app/` equal to
  `5a6af1cfa7`.
- `6889359941` (parents `b656cf6a9c`, `7f0300cfe2`) has `app/` equal to
  `7f0300cfe2`.

The last entry ends "sent to the reviewer for confirmation". The
confirmation (`b8c26320ef`) and the re-witness are not recorded in DISPATCH
(F9).

**WORK_GRAPH.md** (same range). Every checkable count holds:

| Claim | Source |
|---|---|
| J6: 698 top-level passes, 15 mutations | V14-R1 table; 15 `j6-v14-m*.log` files |
| J8: 686 passes | 690 summed `test result` lines, which is 686 plus 4 nested |
| J8: 6 mutations | 6 `j8-mut*.log` files |
| J8 repairs: 717 passes, 13 mutations, F1 control red | V15-R1; 13 `j8r-mut-*.log` files |

Three items are imprecise or stale (F8, F9):

- "Integrated `6889359941` (app bytes equal `7f0300cfe2` apart from the
  CI-24 (b) text)". The merge commit itself is byte-equal; the text came in
  `8cd69ff7fc`.
- "Sequence 1" (F8).
- The J7 row still says "ACTIVE: combined into J6", although J6 is
  COMPLETE and D-3 is still partly visible (F5).

## (4) PR description

These claims are accurate:

- the CC-WR-RECONFIRM, J6 and J8 summaries, against V13, V14/V14-R1 and
  V15/V15-R1;
- J6 checks: 698/0/3, 4 nested, 7/7, 15 implementer mutations, 8 reviewer
  mutations killed;
- J8 checks: 717/0/3, 4 nested, 13 implementer mutations, probes P1–P7;
- "`app/` bytes equal `7f0300cfe2` except `CONTRACT_ISSUES.md` text";
- R1-1 recorded as an open limit, confirmed by the reviewer;
- the open list, including native Cancel and O-1 to O-5.

These are not:

- "**owner pressed every key and button**" drops the record's "dialog"
  qualifier (F7).
- "Escape and Return did not act. **Only the middle button registered**"
  (F3).
- "one *re-confirmed* line (sequence 1 …)" (F8).
- "a real model turn observed", with no note that the reply is not retained
  (F6).
- The J8 checks omit that the reviewer's N6 and N8 mutations survived
  (V15-R1 R1-N3).
- "CI-19 to CI-25 … and CI-23" lists CI-23 twice.
- The logs list omits `validation/J8_1a74f7f3/` and the witness evidence
  folders (F10).

## Findings

| ID | Severity | Where | Failure (evidence) | Repair |
|---|---|---|---|---|
| F1 | **MAJOR** (gates merge) | `evidence/NATIVE-RECONFIRM-WITNESS-8cd69ff7/workspace-records/` (9 files); `evidence/NATIVE-JOURNEY-WITNESS-1113/workspace-records/` (18 files); `.gitignore:8` `**/.chirality/` | **What the records claim.** The witness record (l. 55–57) says the workspace records "are kept byte for byte". `SHA256SUMS` lists 9 such files, and NATIVE_JOURNEY_WITNESS_1113 (l. 53–54, commit `9f26d5333e`, also in this PR) claims 18. **What the PR holds.** None of these files is in the tree at `58a7bd4ccc` (`git ls-tree`), and `shasum -c` at the head fails 9/23. The only copies sit untracked and ignored in HELP_HUMAN's worktree, where they verify OK. Removing that worktree would lose the ledger, act log, captures, RS run log and WR records that support the witness rows 3, 5, 6, 11 and 12 | `git add -f` both `workspace-records/` trees and commit. From a clean checkout of the new head, rerun `shasum -a 256 -c SHA256SUMS` (expect 23/23). Optionally add a `SHA256SUMS` for the 1113 evidence. Consider a `.gitignore` negation for `**/evidence/**/workspace-records/**` so later witnesses do not repeat this |
| F2 | MINOR | Witness row 5 and Findings l. 65; CI-22 (c) "Return chose 'Don't register'"; WORK_GRAPH J6 | **Stated.** As an observation. **Shown.** The App reports the same `Ok(None)` status for every non-act (`lib.rs:703`), exactly as for Escape. The evidence shows no act, with "Don't register" highlighted as the default (`03`). That Return chose it is a sound inference from macOS default-button behaviour and the plugin mapping, but it is not observed | Word it as: "Return did not act; with 'Don't register' highlighted as the default, Return took the default slot (the App does not report which non-act slot)" |
| F3 | MINOR | CI-22 (c) "only the middle button acted"; Findings l. 65–66; WORK_GRAPH J6 "only the middle button registered"; PR body | The Cancel button was never pressed (record l. 69–71). The evidence shows only that Escape and Return did not act and that the middle button did | "Of Escape, Return and the middle button, only the middle button acted; the Cancel button was not pressed" |
| F4 | MINOR | CI-22 (c), the sentence before the addition | "Escape: not yet observed. Which button Escape triggers … is unestablished … must be witnessed natively before any person relies on the build for an act" now sits directly before "Witnessed 2026-10-08 … Escape closed the alert". The paragraph contradicts itself | Re-scope that sentence to what is still unwitnessed (A16 and request answers, and other platforms), or put it in the past tense |
| F5 | MINOR | Witness row 1, "(D-3 repaired)"; WORK_GRAPH J7 row | Screen `01`, the compact library-state JSON below "Prepare exact selected workflow text", shows `"root":{"bytes":[47,112,114,105,118,97,116,101,…` — a native path still printed as a byte array. The pretty-printed library view above it shows text | Say "D-3 repaired in the library and selection views; one compact state view still prints `root` as bytes (`01`)". Keep J7 open, or route the remainder |
| F6 | MINOR | Witness rows 6, 11, 12, 13; Artifact and environment | Claims are presented as observed but are not in the retained evidence: **(a)** the listing "registered — selectable in this App session", cited to `09`, which does not show it; **(b)** `runnable: true` and standing "registered revision"; **(c)** the store folder and published copy written or not written; **(d)** the model's reply text; **(e)** the build command, supplier version and hash, `CHIRALITY_ALLOW_UNVERIFIED`, Darwin version, "Quit … left no process", and the owner's spoken words. These may all be true; they are HELP_HUMAN's account | Mark them "observed by HELP_HUMAN; not retained", and fix the `09` citation. If the bytes still exist, retain the model reply (screen or transcript excerpt) and a listing of `workflow-revisions/`. Otherwise mark the reply "not verifiable from retained evidence" |
| F7 | MINOR | Witness header; PR body | **App records.** The retained WR selection record (`selected_by: "the person (App interface)"`) and RS `run_opened` (`startedBy: person`) attribute selection and run start to "the person". **Who acted.** HELP_HUMAN drove the App, and the plan has HELP_HUMAN send the turn. The record does not say who clicked Select, Prepare and Send or who typed the person text. **The PR body.** It says the owner "pressed every key and button", which is broader than the record's "every dialog key and button" | Add to the record: "Steps 1, 7–9 and 12–13 were performed by HELP_HUMAN; the App labels any UI input 'the person'; the owner's acts are the four dialog presses only." In the PR body, write "every dialog key and button" |
| F8 | NOTE | Witness row 11; WORK_GRAPH J8; PR body | "Sequence 1" is the revision slot (`sequence`). The re-confirmed line is ledger line 2 (`ledger_seq: 2`). A reader may think the ledger has two lines numbered 1 | "Ledger line 2, `re-confirmed`, citing revision sequence 1" |
| F9 | NOTE | `DISPATCH.md` tail; WORK_GRAPH J8 and J7 | DISPATCH does not record the R1-1 confirmation outcome or the re-witness. WORK_GRAPH says "integrated `6889359941` (… apart from the CI-24 (b) text)" although `6889359941` is byte-equal and the text is in `8cd69ff7fc`. The J7 row is stale | Append one DISPATCH line. Reword to "integrated `6889359941` (app bytes equal `7f0300cfe2`); CI-24 (b) text `8cd69ff7fc`". Update J7 |
| F10 | NOTE | PR body | The J8 checks omit the surviving reviewer mutations N6 and N8 (R1-N3). CI-23 is listed twice. The logs list omits `validation/J8_1a74f7f3/` and the evidence folders | Add "8 reviewer mutations, 6 killed, N6 and N8 survived (optional tests)", and the folders |
| F11 | NOTE | OWNER_DECISIONS launch effect | "Each dialog act is the owner's own key press": Register and Re-confirm were clicks. The answer quotes and custody cannot be compared with the chat from the repository | Optional: "own key press or click". No change is needed for custody |

## Limits

- No build, test, launch or native act. The app code is unchanged from the
  candidates reviewed in V14-R1 and V15-R1, and I checked that by `git diff`
  only.
- **Workspace records.** They were read from HELP_HUMAN's untracked checkout
  (`/Users/ryan/ai-env/projects/chirality/.claude/worktrees/test-ci-optimization-f6cacd/…`),
  not from the PR. If those bytes change before F1 is repaired, my record
  checks do not carry over. Rerun `shasum -c`.
- **Screens.** I viewed all 10 at their native resolution, and cropped `01`
  for F5. The screens show what was on screen at capture. They do not prove
  who pressed what.
- **Not verifiable from the repository:** the owner's spoken words, the chat
  answers, the model's reply, the supplier's identity at run time, and the
  link between the binary hash and a build of `8cd69ff7fc`.
- **The App route while the alert is open.** The in-App "Content named by an
  open native confirmation" section is not visible in any retained screen.
  The record claims only that the window stayed readable, which `01`, `03`,
  `05` and `08` support. The overflow route for logout and A16 remains
  unwitnessed.
- **The 1113 witness record.** Beyond its retention claim (F1), I did not
  review it.
- `main` is the local ref (`2007709549`), not fetched.

## Return

- Verdict: **NOT READY**, gated only by F1. Force-add the two
  `workspace-records/` trees (27 files) and re-verify `SHA256SUMS` from a
  clean checkout of the new head. With F1 repaired and nothing else changed
  in the app, I would expect READY on a confirmation pass.
- **Recommended in the same commit:** the F2–F7 wording fixes in the
  witness record, CI-22 (c), WORK_GRAPH and the PR body. They are MINOR and
  do not gate merge. F8–F11 are optional.
- No owner question.
