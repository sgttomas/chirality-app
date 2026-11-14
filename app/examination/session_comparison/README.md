# Session comparison

This compares the App's account of a Codex session with Codex's own record of the same session, for a run in an examination root. It serves DEL-09-02 AC-005: "the candidate's presentation agrees with the supplier's actual events". Each comparison ends as one of REQ-007's five outcomes: passed, failed, blocked, not run or inconclusive.

This is the first part:
- one thread's turns, their outcomes, and the interrupts the App recorded;
- the selected workflow's bytes.

Children, items, outputs, conversations and order follow in later parts.

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
- **Where it may be read.** It is read only inside an examination root: a folder `standalone/launch.py` made, with `home/`, `project/` and `record/`, and a launch record in `record/`.
  - The tool refuses any other folder, and the owner's Codex home.
  - It refuses any path that resolves outside the root.
  - It never copies a session file.
  - A session file never enters Git. The fixtures in `test_compare.py` are invented.

## The App's account

| Part | Read from |
|---|---|
| What the views show | A saved `host_status` answer, `record/host-status-<checkpoint>.json`, from a build that can save one (the scripted driver's test build). Turns come from `nativeView.turnRecords` and `nativeView.turns`. |
| Interrupts the App recorded | The recovery ledger (`recovery.ledger.sqlite`), opened read-only. The latest `stop_request` record of each stop request on the thread is used. |
| The workflow given | WR `run_text` records of the thread (`workflow_file.content`), and the bundled `MANIFEST.json` of the build examined (the WORKFLOW.md `sha256` of the selected name and revision). |

A candidate cannot save its views. On a candidate the tool writes `record/screen-list-<UTC>.jsonl` instead. It lists, from Codex's record alone, what the screen must be found to say of each turn. The operator checks each line against the screen, and sets `answer` (passed, failed or inconclusive) and `note`. Then `answers` turns those lines into rows; an unanswered line becomes `not run`. An answers file's header names its screen list (`answers_of`), and the examination table counts only the latest answers file of each screen list.

Where a saved view exists, the comparison is exact. It is never replaced by the operator's list.

## The comparisons and their outcomes

| | Codex's side | App's side | Outcome |
|---|---|---|---|
| C2 turns | each `task_started` turn | the view's turns | passed if both have it; failed if only one does (both directions) |
| C3 outcome | completed, failed (`task_complete` with `error`), interrupted (`turn_aborted`), or not reported | the view's status | passed if equal. Where Codex reported no end: failed if the App shows an end, passed if it shows none. Any other difference fails. |
| C4 interrupts | the turn's end | the stop record's `turnOutcome` | passed if equal, or if both have no end. Failed if the App records an end Codex did not record, or a stop of a turn Codex has no record of. Inconclusive if Codex recorded an end the App did not learn. |
| W1 workflow | the SHA-256 of the bytes between `<<<chirality-workflow NAME@REV begin>>>\n` and `\n<<<… end>>>` in a user message: exactly the WORKFLOW.md bytes `compose_run_text` puts there | the manifest's WORKFLOW.md digest and the `run_text` record's digest | passed if all three are equal. Failed if any differs, naming which. Blocked if any is missing. Not run if no workflow run was started in the thread. |

**What W1 establishes, and no more:** the selected workflow's bytes are what Codex recorded as the person's input for that turn. That is the part of exit criterion 1's "what the agent receives is the selected workflow, byte for byte" that the App answers for. What Codex adds around that input is the supplier's, and is not compared: its developer message, made from its base instructions, and its tool definitions.

**What W1 rests on, observed once:** that what Codex sent to the provider as the person's input matched its session file exactly. This was observed once, at the pin, with a scripted loopback provider, on three turns. The comparison does not re-establish it on each run.

When one side cannot be read, its comparisons are blocked, with the reason. A saved view is taken after the session ended. Comparing views at earlier points of a run is a later part.

## Output

The output is `record/session-comparison-<UTC>.jsonl`. It is always a new file: an existing name is never written over. It contains, in order:
1. a header line: `{"header": true, "candidate_key", "examination_root", "tool"}`;
2. one row per comparison: `{"comparison", "subject", "codex", "app", "outcome", "reason"}`;
3. a summary line: `{"summary": {comparison: {outcome: count}}}`.

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
