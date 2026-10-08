# Native journey witness — PR 1113 candidate, 2026-10-08 UTC

**What this is.** HELP_HUMAN (Claude Opus 5.5) drove the ordinary connected
workflow journey in the real built App against stock Codex 0.160.0 and a real
model turn. The owner signed in through the App and gave the A15 act. This
is a native witness of one run on one artifact. It does not qualify the App,
the supplier or a release, and it does not bear on the 90% gate.

**Authorization.** See OWNER_DECISIONS "Native journey witness provider" and
"Native journey witness launch" (the answer "Approve, sign in via App").
Owner words given during the run are quoted below.

## Artifact and environment

- **Bundle.** Unsigned debug "Chirality v4 Journey Witness.app", built
  offline with `tauri build --debug --no-sign` from `4c77f34ea6`, whose App
  bytes equal `e653f93a1d`. Identifier `dev.chirality.v4.witness1113` (see
  `overlay.json`). Main binary sha256
  `23d4f56a9f01b4ed6253b3d07669fa4d16ed3c5d0f9336993f063f8cf5f22e48`,
  re-hashed at the second launch.
- **Supplier.** Stock Codex 0.160.0, complete package; `bin/codex` sha256
  `112fae7a…b4b`. `CHIRALITY_ALLOW_UNVERIFIED=1`; supplier standing shown
  as "unverified-development".
- **Codex home.** A fresh scratch home made with `mktemp -d` (plugins and
  analytics off), not `~/.codex`. Credentials were never seen or handled by
  an agent.
- **Workspace and library.** A synthetic workspace in a fresh temp root, used
  as the project workflow library. The development holding copy of
  `coordinated-knowledge-work` was in a separate `library/` folder, byte-equal
  to Root `workflows/coordinated-knowledge-work`.
- **Launches.** Launch 1 at 2026-10-08T00:32:13Z and launch 2 at 00:47:12Z.
  Each ended with Quit from the App menu, exit 0, and no remaining process
  (`launch-1.log`, `launch-2.log`).
- **Turns.** Model `gpt-6.1-sol`, provider `openai`, access entry "ChatGPT
  account in configured account home", no conversation role.

## Journey, as observed

| # | Step | Observed (screens in `evidence/NATIVE-JOURNEY-WITNESS-1113/screens/`) |
|---|---|---|
| 0 | Sign-in | The owner used "Sign in with your ChatGPT account (through Codex)…". The App reported "Matching sign-in completed". |
| 1 | Development selection | "Not runnable: … WR TT-1/TX-1 … (CONTRACT_ISSUES CI-18)"; Prepare disabled (`01`). |
| 2 | Registration | Draft created from the selection, review `review:826b73a1…`, native A15 by the owner (see D-1), then registered. Act captured 00:40:39.981Z (osAccount `ryan`, identity not verified); ledger `registered`, sequence 1, at 00:40:40.267Z. |
| 3 | Select and prepare | Hot registered copy selected, "Not runnable" gone. Prepare showed "prepared; not a run until its start turn is observed … not recorded … not sent", with CK-1 advisory and no R14. |
| 4 | Send | "selection and run_text recorded before send … native workflow-text turn observed; run opened", CK-2 advisory (`02`). The WR selection record (00:41:51.552Z) and run text (00:42:12.790Z) precede RS `run_opened` (00:42:24.470Z). |
| 5 | Model turn | The native item page shows the real user message beginning "[Chirality] Workflow run start: coordinated-knowledge-work from the project library … revision 1b1733864cd8 …". The model replied "I received the project's coordinated-knowledge-work workflow guidance, revision 1b1733864cd8." (`04`). That reply is the model's statement; adoption stays unknown. |
| 6 | Supply check | The first attempt was refused: "Select this original conversation in native History and load its turns before checking supply". After History select and Read turns: "2026-10-08T00:44:33.047Z: verified (supplied); check record recorded; R3 recorded" (`03`). |
| 7 | End | "Run: ended by the person … End notice: pending: the next ordinary turn in this conversation carries it" (`05`). RS `run_ended` at 00:44:48.871Z. |
| 8 | End notice | An ordinary message was sent. The WR end-notice `run_text` was published at 00:46:11.780Z, before the turn. The native user message begins "[Chirality] Workflow run ended: coordinated-knowledge-work revision 1b1733864cd8 (run run:workflow:1e09425a…, ended by the person). No workflow is in force.", and the model replied "No workflow is currently in force for this conversation." (`07`). |
| 9 | Quit and relaunch | Quit, exit 0; relaunched the same binary (new App session `c45e571e…`, same home). The fresh process had no selection and no live run. |
| 10 | Reopen | "Recorded runs (reopened from project records)": `run:workflow:1e09425a…` · conversation `01a118f0…` · **ended** ("ended by the person"); `revisionVerification: verified`; no limits or restart interruptions; "completion is never inferred from a native turn, and no live process run is claimed" (`06`). The durable supply read resolved all four WR records and R3. After restart, the native role binding was shown as "original App supplying binding not established; standing unknown". |

**Records.** The workspace records are retained byte for byte in
`evidence/…/workspace-records/.chirality/` (18 files):
- 4 WR records: selection, run-text start, supply check (verified), run-text end notice;
- the RS run log: `run_opened`, `supplied_guidance` (adoption unknown), `run_ended`;
- the library act log and capture;
- the ledger and stored revision.

## Defects and observations from the witness

- **D-1 (MAJOR, act control): the native A15 confirmation is unusable.**
  - `a15_native.rs` puts the full review JSON in the alert message. The alert is taller than the screen, and its buttons cannot be reached.
  - Owner, exactly: "It's too long to click.  The notification full of code and I can't see the bottom where I click."
  - HELP_HUMAN explained that Return = Register (the default) and Escape = Cancel. Owner, exactly: "I have no idea what i pressed because I couldn't see it.  I just hit enter."
  - Return activated Register. The act is genuine, but **it was given without the statement being visible**. The record must not be read as the person having read the statement.
  - The dialog must present a readable statement with reachable controls, with the full review available separately. This needs repair and its own re-witness.
- **D-2 (MINOR, UI):** after the verified check, the run summary line still read "Supplied: not yet checked", although the check row said "verified (supplied)".
- **D-3 (MINOR, UI):** the selection and library views print native paths as raw byte arrays, hundreds of lines long, which makes the panel very hard to navigate.
- **D-4 (NOTE, UX):** the supply check needs the person to select the conversation in native History and read its turns first. The App refuses clearly rather than guessing, but the step is easy to miss.
- **D-5 (NOTE):** the review's `base_comparison` for the bundled base reads "unavailable" with "No such file or directory (os error 2)". This needs confirming as the expected representation of a bundled base that has no library store copy.
- **D-6 (NOTE):** the A15 capture's `captures/pending/…json` remains after its record was written. It names the written `recordId`. Whether it should remain is for the AAC/REC owner to confirm.
- **D-7 (NOTE, process):** one stray `type` action during navigation landed on no visible input after a page re-render, and nothing was observed to change. Later actions were checked against screenshots.

## Limits

- One run, one artifact, one machine, one model.
- The supplier and the App are unverified-development, not signed, notarized or qualified.
- The actor identity is not verified.
- The 832ec9 development-selection witness stays historical (CI-18).
- Native Cancel is still not witnessed: the owner pressed Return, not Escape.
