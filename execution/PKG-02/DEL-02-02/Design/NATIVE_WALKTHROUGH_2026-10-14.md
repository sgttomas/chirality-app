# Native workflow-making walkthrough, 2026-10-14 (observation record)

- **Status:** observation record of an exploratory walkthrough of the
  WR-VC-01 journey (VER-001). It marks no acceptance criterion, VER item,
  stage or qualification as met; that assessment is the owner's. Formal
  admission of a UI-automation tool (DEL-09-01 §8.3, EXP-DC-N2) and packaged
  qualification were not performed. Authenticated local-server and API-key
  conversations were not exercised.
- **Observed by:** HELP_HUMAN (Agent 0) with the owner present. The owner
  performed the registration act. HELP_HUMAN operated the act-free steps
  through macOS UI automation (not an admitted N-2 tool) and recorded the
  rows below during the run, from the App's screens and the scratch
  project's files. No screenshots are kept.
- **Scope of this record:** the second half of the walkthrough, from a
  relaunch onward, through J-9 on 2026-10-15. The first half (planning, real tools, the first draft,
  registration of revision 1, two reuses, a relaunch with re-confirmation,
  and the first refinement with its trials) was observed in an earlier
  session whose notes were not kept. Its outcome appears below only as the
  records found on disk at relaunch.
- **Candidate:** main `2cf49bfd97` (with #1379 and #1381), built from a clean
  checkout as a debug bundle with a walkthrough bundle identifier. Not a
  package candidate. The first half ran on earlier builds of the same
  launcher; the owner ruled on 2026-10-15: "I accept the earlier steps as
  carried over to build 2cf49bfd97."
- **Supplier:** stock Codex 0.160.0 (`codex-cli 0.160.0`), a complete cached
  npm vendor package; the App reported supplier standing
  *unverified-development* and verification *unverifiable*.
- **Codex home:** a scratch home made for the walkthrough, signed in with a
  ChatGPT account. Never `~/.codex`. The App showed "ChatGPT account (no
  email reported)", identity not verified.
- **Model:** `gpt-6.1-sol` via `openai`.
- **Workspace:** a scratch project with an explicit records store, recorded
  here as `<scratch project>`; paths below are relative to it. The workflow
  is `check-workshop-labels` (project library).
- **Redaction:** no absolute paths or user names. Thread IDs, record IDs and
  content identities are kept.

## Found on disk at relaunch

| Record | Content |
|---|---|
| `.chirality/workflow-registry.jsonl` line 1 | *registered*, new workflow, revision `b39a734e968e` (2026-10-14T18:48:53Z) |
| line 2 | *re-confirmed* `b39a734e968e` after a relaunch (2026-10-14T20:16:08Z) |
| Runs | `run:workflow:86194880…` (18:52–19:17Z) and `run:workflow:81e22e56…` (20:17–20:47Z), both of `b39a734e968e`, both *completed*, conversation `01a13acc-8c3d-7333-89b0-d03cf8b653c9`; their reports are in `walkthrough/reuse-1/` and `walkthrough/reuse-after-relaunch/` |
| Draft `check-workshop-labels` | Content `e2d85206b375` (first refinement: adds `summary.txt`), equal byte for byte to trial 3's snapshot |
| Trials | 1 delegated and 2 clean of `b39a734e968e`; 3 clean of `e2d85206b375`, trial conversation `01a13c34-2ebc-7ed1-b1b6-9200ebf8a6bc`; none brought back |

## Observed, in order

| # | What was done | What the App or the files showed |
|---|---|---|
| 1 | The App was relaunched through the walkthrough launcher | The launched process was the candidate bundle. The Codex host became *ready*. No workflow library was open and the draft list read "No drafts in this library" |
| 2 | Open this App project's workflow library | The draft listed as "draft — not registered", content `e2d85206b375`, 3 files, App-recorded base `b39a734e968e`; trials 1–3 listed with their content identities; revision 1 listed as "registered — re-confirm to use in this App session"; the two quoted registration claims shown with "identity not verified" |
| 3 | Review for registration… | `review:49740eb8-1621-45c2-a818-f48b5e02a6a9`, disposition *new revision*, derived from `b39a734e968e`, `stale_base` false, no hygiene findings, state "reviewed; native A15 not captured". The host's review digest `470763a57035…` equalled the view's recomputation. The file list and base comparison matched the draft and installed files on disk. "Last clean trial: content e2d85206b375 — matches the version under review". Nothing was written |
| 4 | Independent check of the content identity | Recomputing `chirality.app.workflow-package.sha256/v1` from the draft's files gave `e2d85206b375…598e6`; the installed revision gave `b39a734e968e…` |
| 5 | The owner registered through the native A15 confirmation | Act record seq 3 `rec:app:564a5697…`, A15, bound content `e2d85206b375`, decision actor identity not verified; capture `cap:1190724f…` naming `descriptor:review:49740eb8…` and offer `offer:c3e4db8c…`; ledger line 3 *registered*, *new revision*, sequence 2, prior revision `b39a734e968e`, written 2026-10-15T01:42:15Z. The act record's line chain held. The installed copy and the revision store held `e2d85206b375`; revision 1's store copy was kept |
| 6 | The draft list after registration | Until Refresh draft list it still showed the listing taken before registration (base `b39a734e968e`). After it: "registered, unchanged since", App-recorded base `e2d85206b375`, "Same bytes as registered revision 2"; revision 2 listed as "selectable in this App session" |
| 7 | Read stored conversations; select `01a13acc…`; Read metadata | History state *indexed-read-only*, current resume eligibility false, App role in force unknown ("original App supply binding not established"), native agentRole null |
| 8 | Continue selected conversation | State *resume-response-observed*, resume eligibility true. The conversation appeared as the current-generation conversation, `gpt-6.1-sol` via `openai`, role "Role not established in this App process", with "Trials started here: trial 1 … trial 2 … trial 3"; delegation read *available* |
| 9 | Second refinement requested in that conversation, stating only the intent: source-line references for duplicate labels | Turn `01a13d42-7e51-7730-994d-7da3e35c5340` completed in 59573 ms with no request to the person. The agent chose the report itself: `duplicate-source-lines.txt`, one row per duplicate label with its ascending 1-based line numbers by `str.splitlines()`, in `duplicate-counts.txt`'s order; the three existing reports unchanged. It ran the draft's tests (8 passed), a compatibility check of the existing reports against revision 2 over six cases, and a check that the 56 files outside the draft were unchanged. Its final answer stated the new report and the checks, and "Ready for App trial and review. No registration or acceptance occurred." It did not name its format choices as choices for the person |
| 10 | Independent check of the refined draft | Only the three draft files changed; content `4094b24f8281`. The tests passed in a separate scratch workspace and left the draft unchanged; a sample with a blank line, CRLF and an unterminated last line gave the expected references |
| 11 | The owner asked, through the authoring conversation, to "Add the workflow's declared part to the current draft, along with the second refinement." | Turn `01a13d6b-83b0-7f30-bd69-662254baccea` completed in 7505 ms without editing. The agent asked what "declared part" meant ("for example, a role declaration or a specific App metadata field?"). The App's bundled guidance does not describe the declared part or its carriage, which DEL-02-01 holds PROPOSED pending consumer confirmation (U-01, U-02). The owner chose to finish without a declaration |
| 12 | Refresh draft list; choose `01a13acc…` as authoring conversation | "draft — not registered", content `4094b24f8281`, App-recorded base `e2d85206b375`; attribution "last change seen in Codex file-change item … (conversation 01a13acc…)" |
| 13 | Try in a fresh conversation; inputs naming a new person-supplied file (`walkthrough/trial-4/input.txt`: duplicates, a blank line, surrounding spaces, a case variant); no role; `gpt-6.1-sol` via `openai`, ChatGPT entry; sent | Trial 4, trial text 9136 bytes, identity `24c41694d813`; new conversation `01a13d78-0b8b-7793-bc3a-62d24094910e`, header "Trial 4 … not registered; not a workflow run · authoring conversation 01a13acc…". No request to the person. Reports in the trial work folder equalled the expected bytes (`bucket 2,8`, `clamp 1,4`, `gauge 5,7`; summary hash equal to the input's); input unchanged. The agent ended "Acceptance remains pending your review. This was an unregistered trial, not a workflow run" and "Workflow finished: project:check-workshop-labels". Row: "workflow given verbatim (trial header present)", files changed outside the trial work folder 0 |
| 14 | Review for registration… | `review:c6dc25d7-015b-4ef0-ab64-b2b83679526a`, disposition *new revision*, base `e2d85206b375` with lineage to `b39a734e968e`, `stale_base` false, no hygiene findings; the declared-part reading *undeclared* in all five categories with no findings; file digests equal to the draft's; "Last clean trial: content 4094b24f8281 — matches the version under review". Host review digest `08c074b5b83d…` equalled the view's recomputation. The previous review showed as "Retained review" |
| 15 | The owner registered through the native A15 confirmation | Act record seq 4 `rec:app:1b90b41f…`, bound content `4094b24f8281`; capture `cap:093d4ce6…` naming `descriptor:review:c6dc25d7…`; ledger line 4 *registered*, *new revision*, sequence 3, prior `e2d85206b375`, written 2026-10-15T11:09:57Z. The line chain held; the installed copy and store hold `4094b24f8281`; revisions 1 and 2 kept |
| 16 | Workflow chat `01a13acc…`; Select revision 3 | "Selected: check-workshop-labels (project), revision 4094b24f8281 · registered revision · can be run." "This workflow declares no requirements part; its text is the whole method," then Inputs, Tools, Checkpoints (plan guidance), Outputs and Evidence returned each "Not declared" |
| 17 | Person text naming a new input (`walkthrough/reuse-rev3/input.txt`: a CRLF line, an unterminated last line, surrounding spaces); Prepare exact selected workflow text; Record, then send original prepared text once | `run:workflow:c09eefc0-01a8-40cc-b826-7fcf11b7112a` opened (2026-10-15T11:14:00Z) for `4094b24f8281`; advisory CK-1 and CK-2 "requirement check not established … it never decides whether the run starts", role "not established" after the restart. The agent ran the tests and its own exact-byte checks, and ended "Paused for human review; acceptance remains unperformed" and "Workflow finished: project:check-workshop-labels". The reports equalled the expected bytes (`hammer 1,3,8`, `tape 5,9`, `wrench 2,6`; 9 nonblank, 5 unique, 3 duplicate, 4 extra); input unchanged |
| 18 | End run (the run card's control), at the owner's direction | `run_ended` 2026-10-15T11:21:49Z, cause "ended by the person". The End run offered beneath the "Workflow finished" message, which records "completed", was not the one used |

## Notes

- **No App defect was found in the steps observed.** Rows 3, 5, 6, 14 and 15
  behave as §5 and the registration rules describe: the review names exactly
  the listed content, the capture binds the review and its content, and the
  draft list is an observation taken when listed. With J-9 the journey has
  three registered revisions in one lineage and a run of each of revisions 1
  and 3 on new inputs.
- **The declared part is read and shown, but none was authored.** Every
  review, the selection view and the run card show the reading, *undeclared*
  in all five categories; a prose-only workflow is valid (HY-6, WD E5). The
  authoring agent did not recognize the term when asked (row 11): nothing the
  App supplies to it describes the declared part, whose carriage and field
  names remain PROPOSED (DEL-02-01 U-01, U-02). Whether the undeclared
  reading meets AC-001's declared-part clause is the owner's judgement.
- **The authoring agent settles open choices itself.** Given only an intent,
  it decided the report format without asking and reported the result, not
  the choices. The person sees the choices only by reading the workflow text
  at review. No commitment requires otherwise (V4-WF-02 holds: the change
  stays a draft until review and registration); this is recorded for the
  owner's assessment of the authoring experience.
- **Two End run controls record different causes.** The run card's control
  records "ended by the person"; the control offered beneath the agent's
  "Workflow finished" message records "completed" (row 18), as the run card's
  own text states.
- **The stored-conversation, current-conversation, workflow-chat, authoring
  and access-entry selectors** could not be operated by background UI
  automation; selecting a conversation needed
  foreground control. This is a fact about the automation used, not about
  the App.

## Not exercised

A delegated trial from a conversation resumed after a cold restart; bringing
a trial back; Compare across a relaunch; a run of revision 2; a workflow with
a declared part; the person's acceptance of either run's result.
