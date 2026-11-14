# Session comparison

This compares the App's account of a Codex session with Codex's own record of the same session, for a run in an examination root. It serves DEL-09-02 AC-005: "the candidate's presentation agrees with the supplier's actual events". Each comparison ends as one of REQ-007's five outcomes: passed, failed, blocked, not run or inconclusive.

This is the first part:
- one thread's turns, their outcomes, and the interrupts the App recorded;
- the selected workflow's bytes.

Children, items, outputs, conversations and order follow in later parts.

**The claim.** A row says passed only when both sides were read, were identified as the same subject by an identifier and not by position, and agree. Every other case is failed, inconclusive, blocked or not run. Every planned comparison yields at least one row, and no row carries message or output text.

## Codex's record, and where it may be read

- **The reference.** It is the session file Codex writes under its home: `sessions/YYYY/MM/DD/rollout-<UTC time>-<threadId>.jsonl`, one `{timestamp, ordinal?, type, payload}` per line. It holds:
  - each turn's start: `event_msg` `task_started`;
  - each turn's end: `task_complete`, with `error` when the turn failed, or `turn_aborted`, with its reason;
  - the messages of the conversation: `response_item` messages. The person's input is kept verbatim, including a run text with its workflow.

  It does not hold everything the model was given. Codex sends each request with a developer message made from its base instructions, with some sections cut, and with its tool definitions; the file holds neither. It never holds approvals, requests to the person, warnings or errors other than a turn's own. None of these is compared here.
- **Checked against the real format.** The parser was checked against one real session file made at the pin, 0.167.0. That file was made with a scripted loopback provider, no model and no sign-in, in a scratch examination home.
  - Its three turns (completed, interrupted, failed on an error) and their lines read as the file records them.
  - The run text's workflow was found verbatim, in the person's message.
  - The file was removed after the check, and only notes on its format were kept.
- **Which file, and which lines.**
  - The file's first line must be `session_meta` naming the thread; otherwise every comparison is blocked.
  - Only a user message Codex tagged as the person's own text (`content_item_kinds` `["user.text"]`) is the person's input. The environment context and the notice of an aborted turn, which are user-role messages too, never are.
  - A turn started twice, ended twice, ended without a start, or ended with an error that is neither absent, nor null, nor an object with a message, is not one reading. Comparisons of it are inconclusive.
- **Where it may be read.** It is read only inside an examination root: a folder the examination launcher made, with `home/`, `project/` and `record/`, and a launch record in `record/`.
  - The tool refuses any other folder, and the owner's Codex home.
  - It refuses any path that resolves outside the root, the launch record and `record/` itself included.
  - It never copies a session file.
  - A session file never enters Git. The fixtures in `test_compare.py` are invented.

## The App's account

| Part | Read from |
|---|---|
| What the views show | A saved `host_status` answer, `record/host-status-<checkpoint>.json`, from a build that can save one (the scripted driver's test build). Turns come from `nativeView.turnRecords` and `nativeView.turns`, joined by turn identity as the App's view joins them, never by position. A record naming a turn with no turn of that identity, or a turn held twice, blocks the view. |
| Interrupts the App recorded | The recovery ledger (`recovery.ledger.sqlite`), opened read-only. The latest `stop_request` record of each stop request on the thread is used. |
| The workflow given | WR `run_text` records of the thread (`workflow_file.content`), and the bundled `MANIFEST.json` of the build examined (the WORKFLOW.md `sha256` of the selected name and revision). |

A candidate cannot save its views. On a candidate the tool writes `record/screen-list-<UTC>.jsonl` instead. It lists, from Codex's record alone, what the screen must be found to say:
- of each turn;
- that the screen shows no other turn of the thread.

The operator checks each line against the screen, and sets `answer` (passed, failed or inconclusive) and `note`. Then `answers` turns those lines into rows. The list binds its answers in five ways:
- Its header carries every item with a digest of its comparison, subject and requirement. An edited or added item refuses the whole file, and a deleted item becomes `not run`.
- Its header carries the tool's own digest and the session file's digest. A list written by another version of the tool, or about a session file that has since changed, is refused, as is a list written for another root or candidate.
- `passed` needs a note of what was seen; without one the line is `not run`. So is an unanswered line.
- Rows carry the note's digest, never its text.
- An answers file's header names its screen list (`answers_of`), and the examination table counts only the latest answers file of each screen list.

Where a saved view exists, the comparison is exact. It is never replaced by the operator's list.

## The comparisons and their outcomes

| | Codex's side | App's side | Outcome |
|---|---|---|---|
| C2 turns | each `task_started` turn | the view's turns | passed if both have it, by identity. Failed if only one does, in either direction. Not run if neither has a turn. |
| C3 outcome | completed (`task_complete` with no error), failed (with an error object), interrupted (`turn_aborted`), or not reported | the view's status (`inProgress`, `completed`, `failed` or `interrupted`) | passed if equal. Where Codex reported no end: failed if the App shows an end, passed if it shows `inProgress`. Any other difference fails. Inconclusive for a status outside those four, or for a Codex reading that is not one reading. Blocked where only one side has the turn. |
| C4 interrupts | the turn's end, with an abort's reason | the latest stop record's `turnOutcome` | Interrupted passes only against an abort for reason `interrupted`; any other reason fails. A completed or failed outcome passes if equal. Pending or unknown passes where Codex recorded no end, and is inconclusive where it recorded one the App did not learn. Failed if the App records an end Codex did not record, or a stop of a turn Codex has no record of. Inconclusive for an outcome outside the schema's five. Not run if no stop was requested. |
| W1 workflow | the SHA-256 of the bytes between `<<<chirality-workflow NAME@REV begin>>>\n` and `\n<<<… end>>>` (REV the revision's first 12 characters, exactly), in the person's message for that run: exactly the WORKFLOW.md bytes `compose_run_text` puts there | the manifest's WORKFLOW.md digest and the `run_text` record's digest | The person's message for a run is the one whose whole text has the record's `text_identity`, and only then can W1 pass. Failing that, a message with this workflow's markers that no other run claims can show a difference (failed), never agreement (inconclusive). Blocked if any side is missing, or if a workflow record cannot be read. Inconclusive for a workflow in the person's input with no run record of it. Not run if no workflow run was started in the thread. |

**What W1 establishes, and no more:** the selected workflow's bytes are what Codex recorded as the person's input for that turn. That is the part of exit criterion 1's "what the agent receives is the selected workflow, byte for byte" that the App answers for. What Codex adds around that input is the supplier's, and is not compared: its developer message, made from its base instructions, and its tool definitions.

**What W1 rests on, observed once:** that what Codex sent to the provider as the person's input matched its session file exactly. This was observed once, at the pin, with a scripted loopback provider, on three turns. The comparison does not re-establish it on each run.

When one side cannot be read, its comparisons are blocked, with the reason. A saved view is taken after the session ended. Comparing views at earlier points of a run is a later part.

## Output

The output is `record/session-comparison-<UTC>.jsonl`. It is always a new file: an existing name is never written over. It contains, in order:
1. a header line: `{"header": true, "candidate_key", "examination_root", "tool", "tool_sha256"}`, and on an answers file `answers_of`;
2. one row per comparison: `{"comparison", "subject", "codex", "app", "outcome", "reason"}`;
3. a summary line: `{"summary": {comparison: {outcome: count}}}`. It is derived from the rows, and the tool refuses to write one that disagrees with them.

Rows carry only identifiers, statuses, line numbers and digests, never message or output text. So they may be copied out of the root and read by any lane.

## Use

```sh
python3 app/examination/session_comparison/compare.py compare --root <examination root> --thread <threadId> \
    --manifest <the build's MANIFEST.json> [--view <root>/record/host-status-<checkpoint>.json]
python3 app/examination/session_comparison/compare.py answers --root <examination root> \
    --screen <root>/record/screen-list-<UTC>.jsonl
python3 -B -m unittest discover -s app/examination/session_comparison -p 'test_*.py'
```

It uses the standard library only and sends nothing anywhere.
