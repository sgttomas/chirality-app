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
- **A strict model.** The session file's bytes are read once, and both its digest and the model are made from those same bytes.
  - Every line must be a session line.
  - The first line must be `session_meta` naming the thread and the pinned Codex version, `cli_version` `0.167.0`. A file written by another version is blocked, not read on a guess.
  - Every turn event must carry a turn identity.

  Otherwise every comparison is blocked. A turn whose events are not one start followed by at most one end is not one reading, and is never compared as agreeing. That covers a turn started twice, restarted after its end, ended without a start, or ended with an error that is neither absent, nor null, nor an object with a message.
- **The person's message.** Only a user message tagged `content_item_kinds` `["user.text"]` with `provenance {"type": "user"}` is the person's input. The environment context and the notice of an aborted turn carry `provenance {"type": "harness"}`, and are never the person's.
- **Where it may be read.** It is read only inside an examination root: a folder the examination launcher made, with `home/`, `project/` and `record/`, and a launch record in `record/`.
  - The tool refuses any other folder, and the owner's Codex home.
  - It refuses any path that resolves outside the root, the launch record and `record/` itself included.
  - It never copies a session file.
  - A session file never enters Git. The fixtures in `test_compare.py` are invented.

## The App's account

| Part | Read from |
|---|---|
| What the views show | A saved `host_status` answer, `record/host-status-<checkpoint>.json`, from a build that can save one (the scripted driver's test build). Turns come from `nativeView.turnRecords` and `nativeView.turns`, joined by turn identity as the App's view joins them, never by position. The view is blocked by a record naming no single turn of that identity, by a turn held twice, or by a turn with no record. |
| Interrupts the App recorded | The recovery ledger (`recovery.ledger.sqlite`), opened read-only. The latest `stop_request` record of each stop request on the thread is used. |
| The workflow given | WR `run_text` records of the thread (`workflow_file.content`), and the bundled `MANIFEST.json` of the build examined (the WORKFLOW.md `sha256` of the selected name and revision). |

A candidate cannot save its views, so its result comes in two steps.
1. `compare` without `--view` writes only `record/screen-list-<UTC>.jsonl`. It lists, from Codex's record alone, what the screen must be found to say:
   - of each turn, that it is shown (C2) and what it is shown as (C3);
   - that no other turn of the thread is shown.
2. The operator checks each item against the screen, and sets `answer` (passed, failed or inconclusive) and `note`.
3. `answers` writes the candidate's whole result: C2 and C3 from the answers, with C4 and W1.
   - Nothing in the list file is trusted. `answers` derives the list again from the session file's bytes as they are at that moment, and takes an answer only from a single line identical to an item it derives.
   - So an edited item, an invented item, or an item about a record that has since changed answers nothing, and that item is `not run`.
   - `passed` needs a note of what was seen; without one, and when there is no answer, the item is `not run`.
   - Rows carry the note's digest, never its text.
   - The answers file's header names its list (`answers_of`), and the examination table counts only the latest answers file of each list.

Where a saved view exists, the comparison is exact. It is never replaced by the operator's list.

## The comparisons and their outcomes

| | Codex's side | App's side | Outcome |
|---|---|---|---|
| C2 turns | each `task_started` turn | the view's turns | passed if both have it, by identity. Failed if only one does, in either direction. Not run if neither has a turn. |
| C3 outcome | completed (`task_complete` with no error), failed (with an error object), interrupted (`turn_aborted`), or not reported | the view's status (`inProgress`, `completed`, `failed` or `interrupted`) | passed if equal. Where Codex reported no end: failed if the App shows an end, passed if it shows `inProgress`. Any other difference fails. Inconclusive for a status outside those four, or for a Codex reading that is not one reading. Blocked where only one side has the turn. |
| C4 interrupts | the turn's end, with an abort's reason | the latest stop record's `turnOutcome` | Interrupted passes only against an abort for reason `interrupted`; any other reason fails. A completed or failed outcome passes if equal. Pending or unknown passes where Codex recorded no end, and is inconclusive where it recorded one the App did not learn. Failed if the App records an end Codex did not record, or a stop of a turn Codex has no record of. Inconclusive for an outcome outside the schema's five. Not run if no stop was requested. |
| W1 workflow | the SHA-256 of the bytes between `<<<chirality-workflow NAME@REV begin>>>\n` and `\n<<<… end>>>` (REV the revision's first 12 characters, exactly, with each marker exactly once), in the person's message for that run: exactly the WORKFLOW.md bytes `compose_run_text` puts there | the manifest's WORKFLOW.md digest and the `run_text` record's digest | W1 can pass only when exactly one person message has a first part that is the run's text (`text_identity`), exactly one record carries that text, no other part of the message carries a workflow block, and all three digests agree. Two messages or two records with that text are inconclusive. Failing an identified message, one message with this workflow's markers that no other run claims can show a difference (failed), never agreement (inconclusive). Blocked if any side is missing, or if a workflow record cannot be read. Inconclusive for a workflow in the person's input with no run record of it. Not run if no workflow run was started in the thread. |

**What W1 establishes, and no more:** the selected workflow's bytes are what Codex recorded as the person's input for that turn. That is the part of exit criterion 1's "what the agent receives is the selected workflow, byte for byte" that the App answers for. What Codex adds around that input is the supplier's, and is not compared: its developer message, made from its base instructions, and its tool definitions.

**What W1 rests on, observed once:** that what Codex sent to the provider as the person's input matched its session file exactly. This was observed once, at the pin, with a scripted loopback provider, on three turns. The comparison does not re-establish it on each run.

When one side cannot be read, its comparisons are blocked, with the reason. Once the root is admitted, nothing ends without rows: any refusal or unexpected failure writes blocked rows for every planned comparison. The reason names at most the kind of failure.

A saved view is taken after the session ended. Comparing views at earlier points of a run is a later part.

**Values by allowlist.** Every value written into a row is either from a closed set (statuses, abort reasons, stop outcomes, states and sources), or an identifier, a digest or a number matching its pattern. Anything else is written as `unrecognised`. A row naming anything unrecognised never passes, and the summary counts such rows apart. Reasons are the tool's own sentences: no text from any input reaches a row.

## Output

The output is `record/session-comparison-<UTC>.jsonl`. It is always a new file: an existing name is never written over. It contains, in order:
1. a header line: `{"header": true, "candidate_key", "examination_root", "tool", "tool_sha256", "model_version", "pinned_codex"}`, and on an answers file `answers_of`;
2. one row per comparison: `{"comparison", "subject", "codex", "app", "outcome", "reason"}`;
3. a summary line: `{"summary": {comparison: {outcome: count}}, "unrecognised": n}`. It is derived from the rows, and the tool refuses to write a file whose summary would disagree with its rows, or in which a planned comparison has no row.

File names end in a random suffix, and no existing file is written over.

Rows carry only identifiers, statuses, line numbers and digests, never message or output text. So they may be copied out of the root and read by any lane.

## Use

```sh
python3 app/examination/session_comparison/compare.py compare --root <examination root> --thread <threadId> \
    --manifest <the build's MANIFEST.json> [--view <root>/record/host-status-<checkpoint>.json]
python3 app/examination/session_comparison/compare.py answers --root <examination root> \
    --screen <root>/record/screen-list-<UTC>.jsonl --manifest <the build's MANIFEST.json>
python3 -B -m unittest discover -s app/examination/session_comparison -p 'test_*.py'
```

It uses the standard library only and sends nothing anywhere.
