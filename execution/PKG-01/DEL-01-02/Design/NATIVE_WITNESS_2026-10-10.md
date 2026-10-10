# First native App witness, 2026-10-10 (observation record)

- **Status:** observation record. These are dated observations of one
  development build at one supplier version. They mark no acceptance
  criterion, VER item, stage or qualification as met; that assessment is the
  owner's. A matching hash is a development assertion, not qualification.
- **Observed by:** HELP_HUMAN through computer use, with the owner present.
  The owner launched the App from a terminal, signed in and chose the model.
  Recorded here from HELP_HUMAN's notes; no screenshots are kept.
- **Candidate:** main `3a29171a44` (before #1236 and #1237), built offline with
  `tauri build --debug --bundles app` and `bundle.active` overridden to true.
  The unsigned packaging overlay was not used, so this was an improvised
  development bundle, not a package candidate (see item 1).
- **Supplier:** stock Codex 0.160.0 for macOS arm64, the npm vendor `bin/codex`
  (sha256 `112fae7a…1b4b`; archive sha256 `fc789bcd…7466`, the A-IN-S3
  reference of #1237). `CHIRALITY_CODEX_EXPECTED_SHA256` was set, together
  with `CHIRALITY_ALLOW_UNVERIFIED=1`. The App showed:
  - state ready, version `codex-cli 0.160.0`;
  - verification "main binary matches development assertion; qualified full
    distribution identity absent · unverifiable";
  - supplier standing **unverified-development**.
- **Workspace and home:** both made fresh with `mktemp`, never `~/.codex`.
  - The workspace was a scratch project with the FX-DP1 decisions copied in
    and `git init` run.
  - The home was App-only, with `plugins = false` and analytics disabled.
- **Account and model:** a ChatGPT account.
  - The owner used "Sign in with your ChatGPT account (through Codex)…" and
    finished the browser flow.
  - `account/read` returned
    `{"account":{"type":"chatgpt","detailsUnavailable":true},"requiresOpenaiAuth":true}`.
    The App showed "ChatGPT account (no email reported)", with identity not
    verified.
  - The owner chose model `gpt-6-luna`, provider `openai`, entry "ChatGPT
    account in configured account home", and No role.
- **Redaction:** no absolute paths or user names are recorded, and thread IDs
  are shortened.

## Observed, in order

The last column lists the Design cases each observation bears on. It is an
input to those cases, not their result.

| # | What was done | What the App showed | Bears on |
|---|---|---|---|
| 1 | First start, no role | Refused before sending: "role-set-invalid: packaged instruction missing, linked or unreadable". The bundle had no `Contents/Resources/instructions`. The start succeeded after `src-tauri/resources/*` was copied into the bundle (with `production_workflows` as `workflows`) and the App relaunched | App CONTRACT_ISSUES CI-31 |
| 2 | `thread/start`, no role | "Last start: response-observed · role none. Supplied at start: AGENTS.md (default, 4101 bytes); base instructions not set. Whether the model takes it up is unknown." The thread reported model `gpt-6-luna` via `openai` | ROLE no-role start (App display only; native bytes not captured); NIR VC-NIR-21 |
| 3 | Text turn | Streamed live. The user message was labelled "text Codex recorded as input; not an act". Agent commentary, then the command `/bin/zsh -lc 'ls -la'` completed: cwd the scratch project, source `unifiedExecStartup`, exit 0, 44 ms, output shown. Then the final answer. Turn completed in 8724 ms | NPTD NV-03 (command outcome) |
| 4 | Plan mode | "Check plan mode availability" reported it offered (`experimentalApi` declared, plan preset listed). "Send in plan mode (experimental)" completed in 7352 ms. It showed reasoning-summary rows ("none supplied"), read-only command rows and a native Plan item: "Plan · revision 1 in this conversation · completed · native status none in this item kind". Then: "Last mode this App requested for this conversation: plan (turn/start result received; Codex keeps this mode on later turns until another mode is sent)." | NPTD NV-02, NV-01 (live only); NIR VC-NIR-20; DEL-01-03 VER-007 |
| 5 | Default mode, then interrupt | "Send in default mode" asked for `sleep 90`, and the App then showed default as the last mode. The command row read "in progress · output: not supplied by Codex". The person selected the live turn and pressed "Interrupt selected live turn". The turn ended with native status `interrupted` after 48433 ms. Label: "interrupted by the person. Final status observed when the turn ended. Codex reported: interrupted… Record: recorded in the App ledger." The command row read "not completed (turn ended) · native status inProgress · turn ended without item completion", with "Recorded stop requests (1)" | RECOVERY VC-R-02, SR-06 (person's interrupt only: no waiting request, no child); NIR VC-NIR-10, VC-NIR-20, VC-NIR-25 (an open running command, not a reasoning item) |
| 6 | Restart Codex… | A native question appeared, shown through macOS UserNotificationCenter. It said "Observed: no live turns, waiting requests, delegated agents or workflow runs in force" and "None observed is not none: coverage is not complete". Its buttons were Cancel, Restart Codex and Keep Codex running (default). Restart Codex was pressed; the other two were not. Result: "Restart Codex confirmed by you at 2026-10-10T19:56:08.621Z · home account · Codex stopped. No live turn was observed, so no interrupt was sent. Stop Codex record: Recorded in the App ledger before any interrupt was sent. Codex started again in a new process. No conversation was continued automatically." The spawn counter went from 1 to 2 | RECOVERY VC-R-18 (no live turn at the stop) |
| 7 | History after the restart | "Read stored conversations" listed the conversation as `notLoaded`, with a preview of its first user message. Read turns showed three turns, newest first: interrupted, completed, completed. Read items for the interrupted turn worked. "Continue selected conversation" gave history state `resume-response-observed`, with resume eligibility true | RECOVERY VC-R-05 (restart with nothing live), R-4, R-6 |
| 8 | History of the interrupted turn | The `sleep 90` command item reads completed, exit 0, 90004 ms ("read from Codex history"). See the supplier observation below | NPTD TI-15; RECOVERY §3.4, §9 |
| 9 | New turn in the resumed conversation | Asked "After the restart: … what was the last shell command you started?". Completed in 2230 ms with "The last shell command I started was `sleep 90`." After the resume the earlier turns render in the activity view, and the interrupted one keeps its App-ledger label | RECOVERY R-6 |
| 10 | Continue as | The role list offered HELP_HUMAN, HELPS_HUMANS, WORKING_ITEMS and No role. The start display listed TASK as "Not offered as a conversation role here". "Continue as HELPS_HUMANS…" sent a visible summary-request turn. The draft appeared under "Handoff from conversation 01a1275c… (no role)", editable and not sent. The new conversation showed "Not started — no model selected" until a model, provider and entry were chosen. Then: "New conversation 01a12767… started with HELPS_HUMANS. Nothing has been sent to it." "Send this message to the new conversation" gave "Sent once as an ordinary message". The new header read "Role: HELPS_HUMANS. It is fixed for this conversation's life… Continues conversation 01a1275c… (its role: No role); a relation only: no history was carried." Its limit row read "Work within the brief's write targets: Stated, not enforced." The new conversation's turn completed in 2687 ms with a final answer | NIR VC-NIR-12, VC-NIR-24; ROLE CA-1…CA-3 and the limit account |

**Content note (not an App defect).** The source agent's handoff summary said
the sleep "was interrupted by you after about 15 seconds", but the turn lasted
48.4 s. The App presented the draft as the agent's, and editable.

## Delegation run, same day

The App was relaunched with the same candidate, Codex 0.160.0, `gpt-6-luna`
and ChatGPT account. Two conversations were started:
- **B**, with no role (`01a12781…`);
- **A**, as HELPS_HUMANS (`01a12782…`), shown as "Supplied at start:
  AGENTS.md (default, 4101 bytes) + agents/AGENT_HELPS_HUMANS.md (default,
  1084 bytes)".

| # | What was done | What the App showed | Bears on |
|---|---|---|---|
| 11 | A was asked to spawn one sub-agent (count the files in `project/decisions`, change nothing), wait, send one follow-up (the largest file), wait again, then close it | The turn completed in 18861 ms. The activity rows appeared in this order: "Subagent activity started · /root/decision_files (01a12784…)"; "Delegation wait · completed · from 01a12782… to no receivers reported · requested model: null (as supplied)"; "Subagent activity completed"; "Subagent activity interacted"; a second "Delegation wait"; "Subagent activity completed"; "Subagent activity interrupted" (the close). The final answer: "project/decisions contains 2 files. The largest is PKG-1.json at 948 bytes. The sub-agent's thread ID is /root/decision_files". The model knew the agent path, not the thread ID. The Descendants section read "01a12784… · last observed Codex status not reported · parent from subAgentActivity containing thread (inference) · guidance not known · return, review and integration not inferred" | DEL-01-03 REQ-003/AC-003 (NPTD §7, NV-03, VER-003); DEL-06-01 FLEET_RECORDS §4, §11 |
| 12 | A was asked to message B, which A had not spawned, by its conversation ID using its collaboration tools | `collaboration.send_message` to `01a12781…` returned "agent with id … not found". B then had its own completed turn ("Hello—understood."), and the retry returned the same. `collaboration.list_agents` returned only A's own spawn tree: `/root` (running) and `/root/decision_files` (completed, with its last message). Neither call produced a visible item in A's activity | FLEET_RECORDS §4; delegation reach |
| 13 | B was selected after A | **D-1 again:** A's HELPS_HUMANS role header stayed displayed above B's header | D-1 (below) |

**What this establishes, with its limits (one run, one model, one account
home).** Native delegation (spawn, wait, follow-up, close) worked on the stock
0.160.0 route hosted through the App Server. The App showed the child, its
activity and its descendant row without inventing a return, review or
integration. The limits:
- **Only `wait` appeared as a `collabAgentToolCall` item.** No item was shown
  for the spawn, the follow-up or the close, although the App renders collab
  call items generally (it rendered `wait`). So the spawn prompt (the spawn
  item's `prompt` field) was not available from the parent's items. Checking
  whether the prompt arrived verbatim would need a read of the child thread.
  Raw frames were not inspected.
- **The child was known from `subAgentActivity`,** and its parent only by
  inference from the containing thread. Its Codex status and guidance were not
  reported.
- **The tools carried the `collaboration` namespace names** (`send_message`,
  `list_agents`), which OBS-2 §6.1 lists under `multi_agent_v2`. Which feature
  setting produced them was not read.
- **An agent reached only its own spawn tree.** It could not message another
  conversation by ID. The owner reports that in the Codex Desktop App, agents
  in different conversations can message each other by conversation ID. That
  version and mechanism are not established here.

**Effect on Design text.**
- **FLEET_RECORDS §11's "Delegation on any stock route is unobserved"** is now
  observed with limits; updated in place.
- **FLEET_RECORDS §4 AS-2** records `dispatch_observed` "when a spawn
  completes", from the spawn item and its prompt. On this route no spawn item
  was shown, so AS-2's input, and AS-1's `brief:<briefId>` carriage in the
  spawn message, were not observable from the parent. This is recorded in
  FLEET_RECORDS §4 and §11 as an open matter, without changing the rule.
- **NPTD §7 and §14.1** (hash-pinned; not edited) state delegation as
  "observed through the adapter; absent on stock LM Studio". That now has a
  native stock observation, with the limits above: no spawn call item,
  inferred parent, and status not reported.
- Still not observed: NV-04 (a primary turn completing while a descendant is
  active); a TASK-role conversation that delegates (NV-05, K-10); interrupting
  a child, or a cascade from the parent; Stop Codex or quit with a child.

## Supplier observation at 0.160.0: an interrupt did not stop a running command

When the person interrupted the turn, the `sleep 90` unified-exec command was
running.
- **Live:** the turn ended `interrupted`. The command item received no
  `item/completed` and was shown "not completed (turn ended)", native status
  `inProgress`.
- **After Restart Codex:** Codex history for that turn reported the command
  item **completed, exit 0, duration 90004 ms**, and the resumed agent named
  `sleep 90` as its last command.

So at 0.160.0, interrupting the turn did not stop the running unified-exec
command. The command ran to completion, and Codex recorded it as completed.
This rests on one sample in one configuration.

Not observed:
- whether the process outlived the turn as a background process (the 90004 ms
  duration and exit 0 show only that it ran to completion);
- a running command at Stop Codex, quit or a kill;
- the `instant_interrupt` flag, which is under development and off by default.

The earlier dated observations still hold for what they saw. At 0.158.0 and
0.160.0, an open reasoning item never completed and was absent from history.
So was a command whose approval the interrupt resolved, which therefore never
ran (OBS-2 §4, §5.1; VERSION_ADVANCE §4.4 O-1, O-3). Codex's graceful-stop
note already says that running unified-exec processes "may still be running"
(OBS-2 §5.2).

**Effect on Design text.** These files are hash-pinned by the examination
inputs and are not edited here.
- **RECOVERY §3.4 "Items not completed" and the §9 row** "An item opened and
  never completed when its turn is interrupted, and absent from history" hold
  for the cases they cite. They do not hold for a running command, which can
  complete after its turn ends and then appear completed in history.
- **NPTD §6.1 `not-completed`**, "an item open at an interrupt never completes
  and is absent from history", needs the same qualification.
- **NPTD TI-15**, "History shows a completion after all … constructed case; not
  observed", now has an observed instance.
- **No App label or Design statement found claims that an interrupt stops
  running commands.** "Not completed (turn ended)" says only that the App saw
  no completion (RECOVERY §3.4). SR-06 records items that complete after the
  request "as observed, never as prevented". The stop request's
  `itemsNotCompleted` and the live row keep what was seen live, while history
  later reports completion. Nothing told the person that the command kept
  running.

## App defects seen

- **D-1, role headers accumulate.** After the resumed conversation was
  selected, the "Role: … / Continue as" header block rendered twice. After
  Continue as there were three blocks, one per conversation viewed, and only
  the last had live controls. The delegation run reproduced it (item 13).
  Expected: one header, for the selected conversation.
- **D-2, autocapitalisation and autocorrect in identifier fields.** Typed into
  the model and provider fields, "gpt-6-luna" became "Gpt-6-luna" and "openai"
  became "Open". A person could start a conversation with the wrong model or
  provider string.

Both were repaired in the change that added this note, branch
`codex/app-v4-native-witness-1`, with Node tests. Neither repair has been
witnessed natively.

## Not covered by this witness

- attachments and the run-end notice;
- workflow runs, registration and A15;
- native approval request cards (no approval prompt occurred);
- delegation beyond item 11: NV-04, a TASK-role delegation, interrupting a
  child, and Stop Codex or quit with a child;
- quit with its ask-first question (Restart Codex was exercised, with nothing
  live);
- the WebKit/Chromium interface matrix;
- a packaged or signed build.
