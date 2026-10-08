# Native re-witness — readable A15 dialogs and re-confirmation, 2026-10-08 UTC

**What this is.** HELP_HUMAN (Claude Opus 5.5) drove the App and observed
it. The owner pressed every dialog key and button personally. This
re-witness covers the J6 dialog repair (D-1) and the J8 identical-content
re-confirmation (CC-WR-RECONFIRM) on one artifact. It is a native witness
of one run. It does not qualify the App, the supplier or a release, and it
does not bear on the 90% gate.

**Authorization.** OWNER_DECISIONS "Native re-witness launch — 2026-10-08",
answer "Approve; reuse sign-in (Recommended)". Owner words given during the
run are quoted below.

## Artifact and environment

- **Bundle.** Unsigned debug "Chirality v4 Reconfirm Witness.app", built
  offline with `tauri build --debug --no-sign` from `8cd69ff7fc`. Its app
  bytes equal `7f0300cfe2` plus CI-24 text. Identifier
  `dev.chirality.v4.rewitness` (`overlay.json`). Main binary sha256
  `63f2d8d048d35b5dea9c65c3bf7b92b0e82b087b8cad63f0891b01eb66e555a1`,
  re-hashed at both launches (`launch-1.log`, `launch-2.log`).
- **Supplier.** Stock Codex 0.160.0, complete package; `bin/codex` sha256
  `112fae7a…b4b`; `CHIRALITY_ALLOW_UNVERIFIED=1`.
- **Codex home.** The scratch home from the first witness, which holds the
  owner's sign-in, as approved. It is not `~/.codex`. No credential was seen
  or handled by an agent.
- **Workspace.** A fresh synthetic workspace in a new temp root, opened as
  the project workflow library. The development holding copy was in a
  separate `library/` folder, byte-equal to Root
  `workflows/coordinated-knowledge-work`.
- **Launches.** Launch 1 at 02:53:24Z, launch 2 at 03:04:24Z. Each was ended
  with the App menu's Quit, exited 0 and left no process.
- **Screens.** The native alert belongs to `UserNotificationCenter`.
  HELP_HUMAN was granted screenshot access to it, to record what it showed,
  and never clicked it.

## Observed

| # | Step | Observed (screens in `evidence/NATIVE-RECONFIRM-WITNESS-8cd69ff7/screens/`) |
|---|---|---|
| 1 | Setup | Development selection "not runnable" (CI-18). Paths are shown as text, not byte arrays (D-3 repaired). Draft created; review `a77c04d8…`, digest `1fc901a5…277df`. |
| 2 | A15 dialog is readable (D-1) | The alert "Chirality — register workflow" showed the bounded statement: act, revision, workflow, library, purpose, the review named by id and sha-256 digest, the offer and its digest, the consequence, the actor, and the button meanings. The buttons were **[Cancel] … [Register] [Don't register]**. All were visible and reachable. The App window stayed rendered and readable beside the alert (`01`). |
| 3 | **Escape** (owner) | The owner focused the alert and pressed Escape, then said "dialog closed". The App reported "native confirmation dismissed; no capture/registration" (`02`). The workspace had no capture, act-log entry or ledger line. **Escape did not act.** The App cannot show whether Escape went to Cancel or to Don't register; both record nothing. |
| 4 | Default button | A new review, `f440554a…`, digest `ddef582c…`. **"Don't register" was highlighted as the default** (`03`). |
| 5 | **Return** (owner) | The owner pressed Return, then said "done". The App again reported "native confirmation dismissed; no capture/registration" (`04`). There was no capture, act-log entry or ledger line. **Return chose "Don't register".** |
| 6 | **Register** (owner) | A new review, `1db6946a…`, digest `e7ead527…` (`05`). The owner clicked the middle "Register" button, then said "done". The ledger got `registered`, sequence 1, at 03:03:57.410Z for revision `1b1733864cd8…`. One capture, an act-log entry, one revision-store folder and a published copy were written. |
| 7 | Quit and relaunch | Quit, exit 0. Relaunched the same binary (re-hashed). The fresh process had no selection. |
| 8 | Listing (V15 F5) | After the library was reopened, the revision read "registered — re-confirm to use in this App session", offered "Refine (RF-1); Review a draft with its bytes (DS-8)" (`06`). |
| 9 | DS-8 | Reviewing the unchanged draft gave review `c0000a8f…`, digest `06736e59…09c5`: "Identical to revision 1, registered earlier (not verified in this session). Re-confirm revision 1 for use in this App session; no new revision is registered." (`07`) |
| 10 | Re-confirm dialog | The statement began "re-confirm workflow revision for use (A15)", purpose "make it available again in this App session from the project library". It read "Re-confirm revision 1b1733864cd8 of project:coordinated-knowledge-work for use in this App session. This registers no new revision." The buttons were **[Cancel] [Re-confirm] [Don't re-confirm]**, and "Don't re-confirm" was the default (`08`). |
| 11 | **Re-confirm** (owner) | The owner clicked "Re-confirm", then said "done". The ledger got a second line: `re-confirmed`, disposition *re-confirmation*, **sequence 1**, at 03:05:35.355Z, with `reconfirms` citing revision 1. No new revision-store folder or published copy was written. Status read `"newRevision": false`, `"selectable": "in this App session only"`, `"state": "re-confirmed"`, and the listing read "registered — selectable in this App session" (`09`). |
| 12 | Select, prepare, send | The re-confirmed hot copy was selected: `runnable: true`, standing "registered revision". The run was prepared with the CK-1 advisory and sent: "selection and run_text recorded before send … run opened" with CK-2 (`10`). RS `run_opened` cites `coordinated-knowledge-work`, origin `project`, revision `1b1733864cd8…`. |
| 13 | Model turn | `gpt-6.1-sol` (openai). The native user message began "[Chirality] Workflow run start: coordinated-knowledge-work from the project library … revision 1b1733864cd8, run run:workflow:b58720ac…". The model replied: "I received the project workflow guidance “coordinated-knowledge-work,” revision `1b1733864cd8`, for run `run:workflow:b58720ac-aa08-42a8-a063-6979c2b3766b`." That is the model's statement; adoption stays unknown. The run was left open and was not ended. |

**Records.** The workspace records are kept byte for byte in
`evidence/…/workspace-records/.chirality/`: captures, the act log, the
2-line ledger, the run log and the WR records. Hashes are in `SHA256SUMS`.

## Findings from this witness

- **D-1 repaired, and witnessed.** The statement is readable, the buttons
  are reachable, and the review is named by digest. The App window stays
  readable while the alert is open.
- **V14-R1 R1-1 settled for this platform.** Escape did not act: nothing
  was captured or registered. Return chose "Don't register", and only the
  middle button acted. This holds for A15 on macOS 26 (Darwin 25.6), with
  the parentless alert, on this machine. The A16 and request-answer dialogs
  share the button code but were not witnessed natively.
- **Native Cancel.** This is still not witnessed as such. Escape closed the
  dialog with no act, but the App does not show which non-act slot Escape
  took, and the owner did not click the Cancel button.
- **J8 re-confirmation witnessed end to end** after a relaunch: DS-8, the
  re-confirm statement and buttons, one *re-confirmed* line with no new
  revision, selectable in this process only, and a real run of the same
  revision.
- **O-1 (MINOR, UI).** The alert title still reads "Chirality — register
  workflow" for a re-confirmation.
- **O-2 (MINOR, UI).** The App's act button falls back to "Register this
  review…" while the dialog is open and after the result. The review
  paragraph also says "before choosing Register" after a re-confirmation.
  Both come from the presentation being withdrawn.
- **O-3 (NOTE, UX).** The page re-renders and jumps to the bottom after each
  native dialog. Combined with the long review JSON, finding the act button
  takes a lot of scrolling.
- **O-4 (NOTE).** Background clicks from the computer-use harness do not
  reach the Tauri web view, so full-screen control was needed. This is a
  witness-tooling limit, not an App defect.
- **O-5 (NOTE).** The `captures/pending/…json` file still remains after each
  record is written (as witness 1113, D-6).

## Limits

- One run, one artifact, one machine, one model. Unsigned
  unverified-development App and supplier; actor identity not verified.
- File acts keep their two-slot layout (CI-22 (c)). Logout, A16 and request
  answers were not exercised.
- No supply check or end was performed this time; those were witnessed in
  1113.
- The scratch Codex home still holds the owner's sign-in. Whether to clean
  it up is the owner's choice.
