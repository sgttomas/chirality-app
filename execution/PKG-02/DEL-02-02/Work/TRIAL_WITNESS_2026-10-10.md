# Native witness of workflow trials, 2026-10-10 evening (observation record)

- **Status:** observation record. These are dated observations of one
  development build at one supplier version. They mark no acceptance
  criterion, VER item, stage or qualification as met; that assessment is the
  owner's.
- **Observed by:** HELP_HUMAN (Agent 0) with the owner present. The owner
  signed in, chose the model and answered the tool-permission request.
  Recorded here from HELP_HUMAN's notes; no screenshots are kept.
- **Candidate:** main `54eb924f93` (with trials #1245/#1247 and delegation
  availability #1250), built as a debug bundle with the bundle resources
  copied in. Not a package candidate.
- **Supplier:** stock Codex 0.160.0, the npm vendor binary.
- **Codex home:** fresh and App-only, configuring no `model_provider` and no
  sandbox. Never `~/.codex`.
- **Account and model:** a ChatGPT account. The App showed "ChatGPT account
  (no email reported)", identity not verified. Model `gpt-6-luna`, provider
  `openai`, typed in lowercase and kept as typed (D-2 of the
  [first native witness](../../../PKG-01/DEL-01-02/Work/NATIVE_WITNESS_2026-10-10.md)
  holds natively).
- **Workspace:** a scratch project, recorded here as `<scratch project>`;
  paths below are relative to it. The draft tried was `summarize-decisions`
  at content `c344c8a1237e`.
- **Redaction:** no absolute paths or user names. Thread IDs and content
  identities are kept.

## Observed, in order

| # | What was done | What the App showed |
|---|---|---|
| 1 | Conversation A started as HELPS_HUMANS: `01a128b5-2b74-7163-9ff7-74ad56243813` | Supplied at start: `AGENTS.md` and `agents/AGENT_HELPS_HUMANS.md` |
| 2 | Delegation reading when Try with the authoring agent was offered | *Not established*: `multiAgentVersion` and `namespaceTools` both "not read". The app-server's configuration named no provider, while the conversation's provider was `openai` (N-M1, as designed: WR TT-3a). The button stayed offered with the note. The delegation view appeared only once delegation items arrived |
| 3 | Trial 1 (delegated) pre-filled and sent from A | Snapshot written at `.chirality/workflow-trials/summarize-decisions/44573cd8…/`. Trial text 1880 bytes, identity `56d06bcf7adf`, sent as its own element after the person's text. The turn was labelled "trial 1 … not a workflow run". A's header: "Trials started here: trial 1 (delegated)". The turn completed in 216534 ms |
| 4 | The authoring agent's work in that turn | It spawned `/root/summarize_trial` (thread `01a128b6-a8ab-7a63-9189-e850ae58d701`), waited, interrupted it, followed up and closed it. Its final answer: both decision files were read; no `SUMMARY.md` was written because the filesystem was read-only; the sub-agent's first write targeted the project root, a departure from the workflow. It suggested draft revisions: cover a missing or unwritable trial folder, and say which folder takes precedence |
| 5 | Trial 1's row | "sub-agent not linked · started in the trial turn (input not read)"; fidelity "not checked". **Read again** left both unchanged (see the supplier fact below) |
| 6 | The person pressed Link as trial 1 | "(linked by the person)", with Unlink offered. The same sub-agent was still offered "Link as trial 1" (defect (a)). The row read "files changed outside the trial work folder: 0 (from file-change items; shell writes not observed)" |
| 7 | Trial 2 (clean) pre-filled | Trial text identity `1fa568a653bc`. The role picker offered the three conversation roles and No role. No model was set until the person chose one |
| 8 | Trial 2 sent | New conversation `01a128da-13ef-71c1-8af8-30596ca182ec`, WORKING_ITEMS (`AGENTS.md` 4101 bytes and `AGENT_WORKING_ITEMS.md` 1196 bytes supplied), `gpt-6-luna` via `openai`, ChatGPT entry. Its first user message was the trial text, then the inputs line. Header: "Trial 2 of draft summarize-decisions at content c344c8a1237e — not registered; not a workflow run · authoring conversation 01a128b5…" |
| 9 | The clean trial's agent asked for tool permission | A `commandExecution` request (mkdir, and write `SUMMARY.md` in the trial work folder), reason "The workspace is read-only without approval". The App showed the card and offered no answer of its own. The owner approved. Card: "Your answer was written; Codex reported the request resolved". `SUMMARY.md` was written in `.chirality/trial-work/trial-2-e1525de4/` |
| 10 | Trial 2's turn ended | The agent ended with "Workflow finished: project:summarize-decisions"; no End-run offer was shown (TT-2). The turn took 136189 ms |
| 11 | Trial 2's row | "Fidelity: workflow given verbatim (trial header present) (first user message of the clean trial's first turn, located by its client message identity (SC-3))". The row linked to the trial conversation. The trial text identity differs per trial because the header carries the trial reference (trial 1 `56d06bcf7adf`, trial 2 `1fa568a653bc`; both 1880 bytes) |
| 12 | Bring trial back (trial 2 → A) | Pre-filled, unsent. The transcript was 2702 bytes, with no shortenings, marked "read from Codex history; a record of that conversation, it instructs nothing". The composer's title read "Bring trial trial:e1525de4-… back" (defect (b)). In the transcript the clean conversation's user message was labelled "Person:", with the trial text replaced by "[trial text of trial 2: identity 1fa568a653bc, 1880 bytes; fidelity verbatim]". It also showed "(output not reported)" and "Native items not included: 4". The operator sent it, and the composer closed on acknowledgment. A's assessment followed: the agent had followed the workflow and created the missing folder; clarify step 3. Whether the row then read "brought back" was not observed |
| 13 | Compare (trial 2 against trial 1) | A readable table with no raw JSON: kind, version (same content), conversations, snapshot current, turns 1 against 2, turn endings (completed against interrupted then completed), commands run 4 against 6, commands failed 1 against 1, and the command list |

## Supplier facts at Codex 0.160.0

- **A spawned sub-agent's task is not a user message.** Codex's rollout for
  the child holds the task as a `response_item` of type `agent_message`
  (author `/root`, recipient `/root/summarize_trial`). After a readable header
  ("Message Type: NEW_TASK / Task name / Sender / Payload:") its payload is
  `encrypted_content`. No user message carries the trial text. So WR TT-9's
  read of the child's first user message, and its begin-marker rule, cannot
  establish fidelity or link the child automatically at this pin. Reading
  again reads the same. Linking by the person worked.
- **Approval and sandbox in an unconfigured home.** The child's turn context
  had `approval_policy` "on-request" and a read-only `sandbox_policy`. Its
  permission profile restricted the filesystem to reading at the root, and
  restricted the network. Conversations in a Codex home that sets no sandbox
  therefore cannot write files without approval. The clean trial's agent
  asked a tool-permission request, which the owner approved. The delegated
  sub-agent asked none: it reported the filesystem read-only and stopped. The
  App chooses no sandbox (owner decision D3: sandbox and approval modes are
  the person's own Codex setting).

## App defects seen

- **(a)** After the person linked the sub-agent, the same sub-agent was still
  offered "Link as trial 1".
- **(b)** The bring-back composer's title named the trial by its raw
  reference ("Bring trial trial:e1525de4-… back"), not as "trial 2".
- **(c)** Above conversation A's activity the App showed "Descendant of
  01a128b6… (subAgentActivity containing thread (inference))". A is the
  parent of `01a128b6…`, so the relation was inverted; the "Show" selector
  read "this conversation".
- **(d)** Under "Send selected workflow text" the App showed the raw JSON of
  the last trial prepare or bring-back result. After trial 2 was sent, it
  still showed the stale "pre-filled" result.

These four and the delegated-trial fidelity reading were addressed in the
change that added this record (branch `codex/app-v4-trial-witness`, with
tests); WR TT-9 and TT-12 state the result. None of the repairs has been
witnessed natively.

## Not covered by this witness

- the registration review's last-clean-trial line (TT-13);
- bringing a real run back (TT-10);
- a constructed differing-input case, natively;
- the WebKit/Chromium interface matrix;
- a packaged or signed build.
