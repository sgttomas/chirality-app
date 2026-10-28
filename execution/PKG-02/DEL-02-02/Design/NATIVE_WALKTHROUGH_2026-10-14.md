# Native workflow-making walkthrough, 2026-10-14 (observation record)

- **Status:** observation record of an exploratory walkthrough of the
  WR-VC-01 journey (VER-001), with HELP_HUMAN's assessment against AC-001
  (last section). The assessment is not the owner's acceptance and marks no
  VER item, stage or qualification as met. Formal
  admission of a UI-automation tool (DEL-09-01 §8.3, EXP-DC-N2) and packaged
  qualification were not performed. Authenticated local-server and API-key
  conversations were not exercised.
- **Observed by:** HELP_HUMAN (Agent 0) with the owner present. The owner
  performed the registration act. HELP_HUMAN operated the act-free steps
  through macOS UI automation (not an admitted N-2 tool) and recorded the
  rows below during the run, from the App's screens and the scratch
  project's files. No screenshots are kept. In the declared-part
  refinement (2026-10-16) a Codex child agent dispatched by HELP_HUMAN
  operated the App through Codex computer use (equally not admitted) and
  reported the screens; HELP_HUMAN checked each report against the files,
  the records and the Codex session history.
- **Scope of this record:** the second half of the walkthrough, from a
  relaunch onward, through J-9 on 2026-10-15 and a further refinement as
  J-9 that adds the declared part, on 2026-10-16. The first half (planning, real tools, the first draft,
  registration of revision 1, two reuses, a relaunch with re-confirmation,
  and the first refinement with its trials) was observed in an earlier
  session whose notes were not kept. Its outcome appears below only as the
  records found on disk at relaunch.
- **Candidate:** main `2cf49bfd97` (with #1379 and #1381), built from a clean
  checkout as a debug bundle with a walkthrough bundle identifier. Not a
  package candidate. The first half ran on earlier builds of the same
  launcher; the owner ruled on 2026-10-15: "I accept the earlier steps as
  carried over to build 2cf49bfd97." The declared-part refinement ran on main
  `7e98019027` (with #1386), built the same way into the same launcher
  target; it differs from `2cf49bfd97` in the App only by the bundled
  guidance's declared-part section, its source binding, the schema pin and
  a test.
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
| 11 | The owner asked, through the authoring conversation, to "Add the workflow's declared part to the current draft, along with the second refinement." | Turn `01a13d6b-83b0-7f30-bd69-662254baccea` completed in 7505 ms without editing. The agent asked what "declared part" meant ("for example, a role declaration or a specific App metadata field?"). The App's bundled guidance does not describe the declared part or its carriage, which DEL-02-01 then held PROPOSED pending consumer confirmation (U-01, U-02; settled later on 2026-10-15). The owner chose to finish without a declaration |
| 12 | Refresh draft list; choose `01a13acc…` as authoring conversation | "draft — not registered", content `4094b24f8281`, App-recorded base `e2d85206b375`; attribution "last change seen in Codex file-change item … (conversation 01a13acc…)" |
| 13 | Try in a fresh conversation; inputs naming a new person-supplied file (`walkthrough/trial-4/input.txt`: duplicates, a blank line, surrounding spaces, a case variant); no role; `gpt-6.1-sol` via `openai`, ChatGPT entry; sent | Trial 4, trial text 9136 bytes, identity `24c41694d813`; new conversation `01a13d78-0b8b-7793-bc3a-62d24094910e`, header "Trial 4 … not registered; not a workflow run · authoring conversation 01a13acc…". No request to the person. Reports in the trial work folder equalled the expected bytes (`bucket 2,8`, `clamp 1,4`, `gauge 5,7`; summary hash equal to the input's); input unchanged. The agent ended "Acceptance remains pending your review. This was an unregistered trial, not a workflow run" and "Workflow finished: project:check-workshop-labels". Row: "workflow given verbatim (trial header present)", files changed outside the trial work folder 0 |
| 14 | Review for registration… | `review:c6dc25d7-015b-4ef0-ab64-b2b83679526a`, disposition *new revision*, base `e2d85206b375` with lineage to `b39a734e968e`, `stale_base` false, no hygiene findings; the declared-part reading *undeclared* in all five categories with no findings; file digests equal to the draft's; "Last clean trial: content 4094b24f8281 — matches the version under review". Host review digest `08c074b5b83d…` equalled the view's recomputation. The previous review showed as "Retained review" |
| 15 | The owner registered through the native A15 confirmation | Act record seq 4 `rec:app:1b90b41f…`, bound content `4094b24f8281`; capture `cap:093d4ce6…` naming `descriptor:review:c6dc25d7…`; ledger line 4 *registered*, *new revision*, sequence 3, prior `e2d85206b375`, written 2026-10-15T11:09:57Z. The line chain held; the installed copy and store hold `4094b24f8281`; revisions 1 and 2 kept |
| 16 | Workflow chat `01a13acc…`; Select revision 3 | "Selected: check-workshop-labels (project), revision 4094b24f8281 · registered revision · can be run." "This workflow declares no requirements part; its text is the whole method," then Inputs, Tools, Checkpoints (plan guidance), Outputs and Evidence returned each "Not declared" |
| 17 | Person text naming a new input (`walkthrough/reuse-rev3/input.txt`: a CRLF line, an unterminated last line, surrounding spaces); Prepare exact selected workflow text; Record, then send original prepared text once | `run:workflow:c09eefc0-01a8-40cc-b826-7fcf11b7112a` opened (2026-10-15T11:14:00Z) for `4094b24f8281`; advisory CK-1 and CK-2 "requirement check not established … it never decides whether the run starts", role "not established" after the restart. The agent ran the tests and its own exact-byte checks, and ended "Paused for human review; acceptance remains unperformed" and "Workflow finished: project:check-workshop-labels". The reports equalled the expected bytes (`hammer 1,3,8`, `tape 5,9`, `wrench 2,6`; 9 nonblank, 5 unique, 3 duplicate, 4 extra); input unchanged |
| 18 | End run (the run card's control), at the owner's direction | `run_ended` 2026-10-15T11:21:49Z, cause "ended by the person". The End run offered beneath the "Workflow finished" message, which records "completed", was not the one used |

## Notes

- **No App defect was found in the steps observed.** Rows 3, 5, 6, 14, 15,
  24 and 25 behave as §5 and the registration rules describe: the review
  names exactly the listed content, the capture binds the review and its
  content, and the draft list is an observation taken when listed. With the
  refinement the journey has four registered revisions in one lineage and
  runs of revisions 1, 3 and 4 on new inputs. The role-supply notice below
  has no established cause.
- **The declared part: none through J-9, authored in the refinement.**
  Through J-9 every review, the selection view and the run card showed the
  reading *undeclared* in all five categories; a prose-only workflow is valid
  (HY-6, WD E5). The authoring agent did not recognize the term when asked
  (row 11): nothing the App then supplied to it described the declared part,
  whose carriage and field names were then PROPOSED (DEL-02-01 U-01, U-02;
  settled later on 2026-10-15). The question arrived as an agent message:
  Codex's `request_user_input_async` returned `{"accepted":true}` at once and
  delivered the question as an `AgentMessage` item with `delivery: "async"`,
  so no native request was left waiting. In the refinement, with the
  guidance's declared-part section supplied, a new authoring conversation
  wrote a block in one turn without asking (row 20), and the App read it as
  *recognized* at review, selection and run (rows 24, 26 and 27).
- **New guidance reached the new conversation only by hand.** A rebuilt App
  keeps an existing install's stored guidance. The instruction store never
  updates an existing copy for a new release; GS-6's update of an unmodified
  copy is PROPOSED (DEL-02-04 U-R9); and the UI has no restore-default
  control. Without the owner's hand restore (before row 19), the new
  conversation would have received the earlier guidance, with no
  declared-part section, as in row 11.
- **The authoring agent settles open choices itself.** Given only an intent,
  it decided the report format without asking and reported the result, not
  the choices. In the refinement it likewise chose the checkpoint's act and
  the tool's class without naming either (row 21). The person sees the
  choices only by reading the workflow text at review. No commitment requires
  otherwise (V4-WF-02 holds: the change stays a draft until review and
  registration); this is recorded for the owner's assessment of the
  authoring experience.
- **Both element findings follow from the guidance text.**
  - **FB-16.** The guidance glosses `A5` as "accept" and gives the checkpoint
    form "for a review of an output", and the agent combined the two. The App's
    reader accepts `A5` only when it is reached on a queued host outcome for
    the change items of a named proposal. The guidance leaves that rule to "the
    App's findings name them".
  - **FB-21.** The guidance calls `read_through` "a declared host operation".
    The agent named the operation `exec_command`, but the reader expects the
    name of a declared `host_operation` tool element, here
    `local-python-command`.
  - **Test coverage.** The guidance's regression test writes an `A4` checkpoint
    and a `harness_capability` tool, with no `host_read` input, so it covers
    neither path.
  - **Correction.** The findings reach the person only in the review. The
    authoring conversation does not receive them, and correcting the draft from
    them was not exercised.
- **Attribution and outside-folder counts miss shell writes.** The agent
  wrote the declaration with a shell command. The draft row therefore read
  "Attribution: not observed" (row 22), and trial 5's count of files changed
  outside the trial work folder covers file-change items only, as its row
  states (row 23).
- **Role-supply history was not confirmed at two thread starts.**
  - **What happened.** At row 19 the App reported that the role observation log
    "changed or was replaced before append" and wrote no row; trial 5's start
    (row 23) wrote one. Trial 4's start (row 13) also left no row.
  - **What changed.** At row 19 the log's content and modification time were
    unchanged; only its inode change time had moved, within a second of the
    start.
  - **Cause.** Not established. A candidate is macOS adding file-provenance
    metadata on a rebuilt binary's first write to the file, which the App's
    log-basis check would read as a replacement.
- **Two End run controls record different causes.** The run card's control
  records "ended by the person"; the control offered beneath the agent's
  "Workflow finished" message records "completed" (row 18), as the run card's
  own text states. In revision 4's run the agent paused at the declared
  review point and wrote no finished line, so only the run card's control was
  offered (rows 27 and 28).
- **A declaration finding hides every output's standing on the run card.**
  - **What the run card showed.** The App recorded its own FB-16 finding in
    the run record at the open. The run card's output view does not read
    `declaration_finding` entries, so every standing facet of `review-package`
    read "unknown" (row 27).
  - **Why that is broader than the finding.** The finding concerns the
    checkpoint, not the output. Any run whose record holds a declaration
    finding therefore shows no output standing.
  - **Elsewhere on the card.** The checkpoint itself reads "not listed", with
    its finding and no arrival.
- **The stored-conversation, current-conversation, workflow-chat, authoring
  and access-entry selectors** could not be operated by background UI
  automation; selecting a conversation needed
  foreground control. This is a fact about the automation used, not about
  the App.

## Declared-part refinement (as J-9), 2026-10-16

A further refinement as J-9: the owner's steer was to have the authoring
agent, in a new authoring conversation, add the declared part to
`check-workshop-labels`, then trial it, review and register it as revision
4, and run revision 4 on a new input.

Before the rows below: the App was quit with no live turn or open offer,
rebuilt from `7e98019027` and relaunched through the same launcher. The
rebuilt bundle did not change the guidance the App supplies. The stored
copy of `AGENTS.md` in the App's data still held the earlier default
(`cb8d7206…`), and the App's instruction store never updates an existing
copy for a new release (GS-6 and U-R9 are still PROPOSED; the UI offers no
restore-default control). New conversations would have received guidance
without the declared-part section. By the owner's choice, HELP_HUMAN backed
up the stored copy and overwrote it in place with the bundled default
(`1abc7974…`), standing in for the restore GS-3 and GS-6 describe. No other
App data was changed.

| # | What was done | What the App or the files showed |
|---|---|---|
| 19 | Start thread: no role (preselected "No role: product guidance only."), `gpt-6.1-sol`, `openai`, entry "ChatGPT account in configured account home" | Conversation `01a1427a-a501-75b1-9cde-7e4000ff9e6d`. "Supplied at start (retained original receipt): AGENTS.md (default, 7343 bytes)"; content `1abc7974…`. The conversation's first native developer message holds the stored file byte for byte, declared-part section included. The App also showed "Role-supply history was not confirmed: role observation log changed or was replaced before append; no replacement written" (see Notes) |
| 20 | The owner's request, sent as text: "Add the workflow's declared part to the check-workshop-labels draft." | Turn `01a1427b-3c6d-7c81-8ece-5f0459848897` completed in 45100 ms with no request to the person. The agent found the draft, read it, and wrote the block and one prose sentence with a Python script run as a shell command, then checked that the JSON parsed and the element names were unique. No file-change item appeared. Final answer: "Added the WD-v0.8 declaration to the draft WORKFLOW.md, covering inputs, tools, outputs, evidence, and human acceptance. JSON validation passed. App review findings remain unverified." |
| 21 | Independent check of the draft | Only `WORKFLOW.md` changed; the installed revision 3 and all other project files were unchanged. Content `422c24e6bee5`. Step 5 of the prose gained "Present this package under the exact designating line `Workshop label review package`." One `workflow-declaration` block after the prose: inputs `label-input` (file supplied), `workspace-and-paths` (person supplied) and `package-resources` (host read through `exec_command`); tool `local-python-command` (`host_operation` `exec_command`); output `review-package` (message with that designating line); evidence `input-identity` and `verification-results`; checkpoint `accept-results` (A5, the person, reached when `review-package` is produced). The App's reader, run offline on these bytes from the build's own crate, and the DEL-02-01 prototype both read the part as recognized in all five categories, with two element findings: `accept-results` invalid ("FB-16: A5 combination invalid") and `package-resources` not established ("FB-21: read_through must name usable host operation"). The agent chose A5 and `exec_command` itself and named neither choice to the person |
| 22 | Open this App project's workflow library; Refresh draft list; choose `01a1427a…` as authoring conversation | "draft — not registered", content `422c24e6bee5`, 3 files, App-recorded base `4094b24f8281`; "Attribution: not observed"; trials 1–4 listed |
| 23 | Try in a fresh conversation; inputs naming a new person-supplied file (`walkthrough/trial-5/input.txt`: surrounding spaces, a blank line, CRLF, a trailing tab, a leading no-break space, a case variant, an unterminated last line); no role; `gpt-6.1-sol` via `openai`, ChatGPT entry; sent | Trial 5, trial text 13322 bytes, identity `f2fd4e19c3b6`, holding the draft verbatim with its block; new conversation `01a14281-2fd7-7a30-a74b-12ed04fd48e9`, header "Trial 5 … not registered; not a workflow run · authoring conversation 01a1427a…". Turn `01a14281-3076-7ac1-9837-e875ddf30084` completed in 39421 ms with no request. Its answer opened with the designating line "Workshop label review package", gave the input identity, the four reports and the checks (8 tests passed), and ended "Ready for your review and acceptance or corrections. Human acceptance has not been recorded." The reports equalled the expected bytes (`drill bit 1,4`, `level 6,7`, `socket set 2,8`; 8 nonblank, 5 unique, 3 duplicate, 3 extra); input unchanged; only the trial work folder and the App's trial snapshot were added. Row: "workflow given verbatim (trial header present)", files changed outside the trial work folder 0 "(from file-change items; shell writes not observed)" |
| 24 | Refresh draft list; Review for registration… | `review:7a11fc16-9d7f-4967-9647-0bc0d1685a4c`, disposition *new revision*, content `422c24e6bee5`, base and prior `4094b24f8281` with lineage to `e2d85206b375` and `b39a734e968e`, `stale_base` false, no hygiene findings. Declared part: reading *recognized*, no findings; all five categories *recognized*; elements as in row 21 (six recognized, `accept-results` invalid with FB-16, `package-resources` not established with FB-21). File digests equal to the draft's. "Last clean trial: content 422c24e6bee5 — matches the version under review." Host review digest `1557ad605c3f…` equalled the view's recomputation |
| 25 | The owner registered through the native A15 confirmation, as reviewed, with both element findings standing | Act record seq 5 `rec:app:7fb92ce1…`, bound content `422c24e6bee5`; capture `cap:a92c2ce0…` naming `descriptor:review:7a11fc16…`; ledger line 5 *registered*, *new revision*, sequence 4, prior `4094b24f8281`, written 2026-10-16T07:51:01Z. The line chain held; the installed copy and store hold `422c24e6bee5`, recomputed independently; revisions 1–3 kept. The findings did not refuse registration (HY-6) |
| 26 | Workflow chat `01a1427a…`; Select revision 4 (in the library's list of registered revisions) | Revision 4's row read "registered — selectable in this App session", revisions 1–3 "re-confirm to use in this App session". "Selected: check-workshop-labels (project), revision 422c24e6bee5 · registered revision · can be run." The declared part was shown under Inputs, Tools, Checkpoints (plan guidance), Outputs and Evidence returned, with each element's meaning; all five categories *recognized*. `package-resources` was marked "not established: FB-21: read_through must name usable host operation". `accept-results` read "Declaration finding: invalid (FB-16: A5 combination invalid). It is listed as written and treated as nothing more", and its act "with the App act control, which you open yourself; nothing opens because the work reached the checkpoint". "Written for roles: not stated (any role). Tool ceiling: none declared." |
| 27 | Person text naming a new input (`walkthrough/reuse-rev4/input.txt`: surrounding spaces, two blank lines, a case variant, a label three times, an unterminated last line); Prepare exact selected workflow text; Record, then send original prepared text once | `run:workflow:a86bfe6d-be4b-4fa8-83f6-58b3fe5550f3` opened 2026-10-16T07:59:43Z for `422c24e6bee5`, revision verification *verified*. Its first entries were `run_opened` and a `declaration_finding` (`accept-results`, FB-16, invalid). The run-start text held the registered `WORKFLOW.md` verbatim, block included. Advisory CK-1 and CK-2 read "requirement check not established … it never decides whether the run starts", now naming the declared tool: "local-python-command: not established: catalog unreadable or not read". The checkpoint gained "Run record: not listed: reported as a declaration finding (invalid, FB-16); no arrival is recorded for it (CE-2)". Every standing facet of `review-package` read "unknown", because "the run record holds declaration_finding entries whose bodies this view does not read". Turn `01a143b9-5af0-7503-bf39-9813bc758b77` completed in 39769 ms with no request. It ran four shell commands, all exit 0: a check of paths, input and package hashes; the 8 tests; the helper; and an exact-byte check. The answer opened with the designating line and ended "Paused for your review and acceptance or requested corrections. Human acceptance remains pending.", with no "Workflow finished" line. The reports equalled the expected bytes (`clamp 2,8`, `vise 1,3,10`, `Clamp` kept distinct; 8 nonblank, 5 unique, 2 duplicate, 3 extra); input unchanged. The only other project change was the agent's own evidence file `walkthrough/reuse-rev4/verification-run-a86bfe6d.json`, beside the output folder |
| 28 | End run (the run card's control) | `run_ended` 2026-10-16T08:02:49Z, cause "ended by the person"; "End notice: pending: the next ordinary turn in this conversation carries it". No "Workflow finished" offer had appeared |

## First half, from the authoring conversation's history

The Codex session history of `01a13acc…` (scratch home, read-only) carries
the first half the earlier notes lost, in UTC:

- **Plan and revision (J-1).** 14:33 "Help me plan a small reusable workflow
  for checking an invented list of workshop-kit item labels…"; 14:48 "Revise
  the plan to trim surrounding whitespace and ignore blank labels…", then
  implement and check the example.
- **Real tools (J-2).** The first tool calls at 14:48 failed: the supplier
  package then lacked `codex-code-mode-host`. After the owner restored the
  complete package, from 15:40 the agent ran shell commands and file patches,
  and an independent check found and the agent repaired a preservation bug
  (16:00). At 15:40 the project held only `.chirality/project.json` and two
  decision-package files from an earlier stage: no workflow, draft or library.
- **Draft (J-3)** written at 16:02 under `.chirality/workflow-drafts/`, and
  revised at 16:18 for two reuse issues before any trial.
- **Trial, review, registration (J-4–J-6).** Delegated trial 1 at 18:13;
  registration of revision 1 at 18:48 (ledger line 1).
- **Reuse (J-7).** Runs at 18:52 and, after a relaunch and re-confirmation
  (20:16), 20:17, on inputs differing from the example.
- **Native requests.** A command-approval request denied by the person
  (19:22) and a separate one approved (19:31); two long-command interruption
  checks (19:36, 19:53).
- **First refinement (J-8)** from 20:49.

## Receiving joins (Design §7)

| Join | Observed | Gap or limit |
|---|---|---|
| DEL-01-03 plans, tools, delegation | Tool items (commands, file changes, outputs, statuses) in every conversation; delegation read *available*; delegated trial 1 with a sub-agent the person linked | No plan items: plan mode "not checked for this Codex connection" (J-1 proceeded in prose, as K-5 allows). No delegated trial after the cold restart |
| DEL-01-04 requests, outcomes, draft view, trial messages | Approval requests answered both ways; trial texts pre-filled and sent once; a clean trial opened its own conversation; the review package (RB-2); run start and end marks | Bring-back not exercised; in the second half, trial 4's text and revision 3's run text were sent by HELP_HUMAN at the owner's direction, and in the refinement trial 5's text and revision 4's run text by the Codex operator |
| DEL-01-04 act control | Five A15 captures from the native confirmation (registrations of revisions 1–4 and one DS-8 re-confirmation), each naming its review's descriptor and binding its content | Actor identity not verified (stated by the App); the act control's refusal of automation (EXP-DC-N2 DC-N2) not tested |
| DEL-02-01 portable contract | Identity tuples and revisions agree with independent recomputation of `chirality.app.workflow-package.sha256/v1`; the declared-part reader's result in every review, the selection and the run card. In the refinement a block written from the guidance read *recognized* in all five categories, as the prototype read it (rows 21, 24) | Through J-9 no declared part was authored (row 11; carriage and fields then PROPOSED, settled later on 2026-10-15 as U-01, U-02). The refinement's two element findings, FB-16 (`A5`) and FB-21 (`read_through`), follow from the guidance's wording (Notes); revision algorithm U-03 open |
| DEL-02-03 execution, compatibility | Four runs started from registered revisions; advisory CK-1/CK-2 shown, never deciding; the supply check of revision 3's run *verified* against native turn `01a13f44-dce6-7e31-ba00-3211873dc55b`. Revision 4's run recorded the App's own declaration finding at the open, and showed the declared part with the checkpoint as plan guidance (row 27) | Requirement checks "not established", with nothing declared and again with a declared tool ("catalog unreadable or not read"); the supply check needs that turn read in native History first, otherwise it reports "turn not received in this selected history", and was not run for revision 4. A `declaration_finding` entry leaves every output's standing facets "unknown" (Notes) |
| DEL-02-04 role guidance | Roles shown per conversation; trials 4 and 5 started with no role; the new conversation of row 19 received the stored guidance, declared-part section included, byte for byte | After the cold restart the authoring conversation's role reads "not established"; nothing flows for workflows (Design §7). A rebuilt App leaves an existing install's stored guidance unchanged and offers no restore (GS-6, U-R9 PROPOSED); the new section arrived only by the owner's hand restore. The section's `A5` and `read_through` wording leads to the two findings, and its regression test covers neither path. Role-supply history was not confirmed at two thread starts (Notes) |
| DEL-04-01 / DEL-04-03 acts and records | A15 records in one intact line chain; ledger lines cite them; run records open, model turns, end and supply | — |
| DEL-01-02 recovery | Relaunch, resumption of the authoring conversation from history, runs before and after relaunch | — |
| DEL-01-05 access | Trial 4's conversation started with no model until one was chosen | — |
| DEL-01-01 supplier | `fileChange` attribution of the draft's last change before the refinement | A draft change written by a shell command is not attributed (row 22); Codex 0.160.0 unverified-development; the qualification pin is not established |

## Not exercised

A delegated trial from a conversation resumed after a cold restart; bringing
a trial back; Compare across a relaunch; a run of revision 2; correcting a
draft from the review's declared-part findings; a declared part with every
element recognized; the person's acceptance of any run's result.

## Assessment against AC-001 (HELP_HUMAN)

AC-001 is **met on this evidence** for build `2cf49bfd97`, with the earlier
steps carried over by the owner's ruling (Candidate, above):

- plan creation and revision, real tool execution, draft creation, actual
  review and registration, reuse on new inputs, and two refinements each
  tried, reviewed, registered and, for the second, reused: observed (rows
  above and the first-half history);
- the declared part observable: the reader's result is shown at review,
  selection and run, as TT-6 and RB-2 design it. Through J-9 it read
  *undeclared*, which is valid (HY-6). In the refinement a declared workflow
  was authored, tried, reviewed, registered and run, and each of those views
  showed the five categories with their actual readings, two element findings
  included (rows 24, 26 and 27);
- native transitions observable: turns, items, requests, captures and run
  marks were shown and recorded;
- gaps at every receiving join: the table above.

The declared-part refinement ran on build `7e98019027`. It adds no new
journey step and does not change this assessment. It removes the earlier
limit that no declared workflow was exercised.

Limits that do not change the assessment:
- an exploratory walkthrough with non-admitted UI automation (DEL-09-01 §8.1
  N-2);
- a debug bundle rather than a package candidate;
- a project folder holding only the App project file and two decision
  packages at the start;
- the refinement's guidance arrived only through the owner's hand restore,
  and the registered revision 4 keeps two element findings;
- the items under *Not exercised*.

