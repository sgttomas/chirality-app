# Session comparison

This compares the App's account of a Codex session with Codex's own record of the same session, for a run in an examination root. It serves DEL-09-02 AC-005: "the candidate's presentation agrees with the supplier's actual events". Each comparison ends as one of REQ-007's five outcomes: passed, failed, blocked, not run or inconclusive.

This is the first part. It makes exactly three comparisons of one thread: its turns (C2), their outcomes (C3), and the interrupts the App recorded (C4). Children, items, outputs, conversations and order follow in later parts.

**The workflow comparison (W1) is not available in this version.** It would compare the selected workflow with what Codex recorded as the person's input. Its association of a run with a Codex message needed a new rule in each of three independent readings, so it comes in a change of its own, with its own reading. Its claim will require the run reference in the run text's own first line to equal the record's run. Until then, nothing this tool writes establishes that the selected workflow reached Codex, and a result of three passes is not that check.
- Where a session has a workflow run to compare, the tool writes one W1 row with the outcome blocked and the reason "the workflow comparison is not available in this version". A session has one when a line of Codex's record carries the workflow markers, in its bytes or in any value once decoded, when a run text record names the thread, or when a workflow record cannot be read. W1 is never passed and never left out. Where the session cannot be read, whether it has a run is not known, so the W1 row is written blocked as well.
- Every header and every summary, the screen list's header among them, names the three comparisons (`compares`) and carries `workflow_comparison`: "the workflow comparison is not available in this version".
- Asking for it by name (`--comparison W1` or `--comparison workflow`) is refused with that sentence, and nothing is written.

**The claim.** A row says passed only when both sides were read, were identified as the same subject by an identifier and not by position, and agree. Every other case is failed, inconclusive, blocked or not run. Every planned comparison yields at least one row, and no row carries message or output text.

## Codex's record, and where it may be read

- **The reference.** It is the session file Codex writes under its home: `sessions/YYYY/MM/DD/rollout-<UTC time>-<threadId>.jsonl`, one `{timestamp, ordinal?, type, payload}` per line. It holds:
  - each turn's start: `event_msg` `task_started`;
  - each turn's end: `task_complete`, with `error` when the turn failed, or `turn_aborted`, with its reason;
  - the messages of the conversation: `response_item` messages, the person's input among them.

  It does not hold everything the model was given. Codex sends each request with a developer message made from its base instructions, with some sections cut, and with its tool definitions; the file holds neither. It never holds approvals, requests to the person, warnings or errors other than a turn's own. None of these is compared here.
- **Checked against the real format.** The parser was checked against one real session file made at the pin, 0.167.0. That file was made with a scripted loopback provider, no model and no sign-in, in a scratch examination home.
  - Its three turns (completed, interrupted, failed on an error) and their lines read as the file records them.
  - The file was removed after the check, and only notes on its format were kept.
- **A strict model.** The session file's bytes are read once, and both its digest and the model are made from those same bytes.
  - Every line must be a session line.
  - The first line must be `session_meta` naming the thread and the pinned Codex version, `cli_version` `0.167.0`. A file written by another version is blocked, not read on a guess.
  - Every turn event must carry a turn identity.

  Otherwise every comparison is blocked. A turn whose events are not one start followed by at most one end is not one reading, and its outcome is never compared as agreeing: C3 is inconclusive. C2 still says only that both sides have a turn of that identity. That covers a turn started twice, restarted after its end, ended without a start, or ended with an error that is neither absent, nor null, nor an object with a message.
- **Where it may be read.** It is read only inside an examination root: a folder the examination launcher made, with `home/`, `project/` and `record/` all present, and a launch record in `record/`. A folder missing any of the three is refused.
  - The tool refuses any other folder, and the owner's Codex home.
  - It refuses any path that resolves outside the root, `record/` itself included. A launch record that resolves outside the root refuses the whole root.
  - It never copies a session file.
  - A session file never enters Git. The fixtures in `test_compare.py` are invented.

## The App's account

| Part | Read from |
|---|---|
| What the views show | A saved `host_status` answer, `record/host-status-<checkpoint>.json`, from a build that can save one (the scripted driver's test build). The turns shown in the thread are, as the App's panel shows them, the union of two sets. The first is the turn records (`nativeView.turnRecords`, joined to `nativeView.turns` by turn identity, never by position), each with its native status. The second is the turns named by the thread's items, checklist revisions, turn errors and unreadable turn errors. A turn of the second set with no native turn is shown with no status. The view is blocked by a record naming no single turn of that identity, by a turn held twice, by a turn with no record, or by an entry naming no readable turn. |
| Interrupts the App recorded | The recovery ledger (`recovery.ledger.sqlite`), opened read-only. The latest `stop_request` record of each stop request on the thread is used. |

A candidate cannot save its views, so its result comes in two steps.
1. `compare` without `--view` writes only `record/screen-list-<UTC>.jsonl`. It lists, from Codex's record alone, what the screen must be found to say:
   - of each turn, that it is shown (C2) and what it is shown as (C3);
   - that no other turn of the thread is shown.
2. The operator checks each item against the screen, and sets `answer` (passed, failed or inconclusive) and `note`.
3. `answers` writes the candidate's whole result: C2 and C3 from the answers, with C4, and W1 blocked where the session has a workflow run.
   - Nothing in the list file is trusted except its thread, which only selects the session file to derive from. `answers` derives the list again from the session file's bytes as they are at that moment, and takes an answer only from a single line identical to an item it derives.
   - So an edited item, an invented item, or an item about a record that has since changed answers nothing, and that item is `not run`.
   - `passed` needs a note of what was seen; without one, and when there is no answer, the item is `not run`.
   - Rows carry the note's digest, never its text.
   - The answers file's header names its list (`answers_of`), and the examination table counts only the latest answers file of each list.

Where a saved view exists, the comparison is exact. It is never replaced by the operator's list: while any `record/host-status-*.json` exists, `compare` without `--view` and `answers` are both refused, with blocked rows.

## The comparisons and their outcomes

| | Codex's side | App's side | Outcome |
|---|---|---|---|
| C2 turns | each turn with a start or end event | the view's turns | passed if both have it, by identity. Failed if only one does, in either direction. Not run if neither has a turn. |
| C3 outcome | completed (`task_complete` with no error), failed (with an error object), interrupted (`turn_aborted`), or not reported | the view's status (`inProgress`, `completed`, `failed` or `interrupted`) | passed if equal. Where Codex reported no end: failed if the App shows an end, passed if it shows `inProgress`. Any other difference fails. Inconclusive for a status outside those four, for a turn the view shows with no native status, or for a Codex reading that is not one reading. Blocked where only one side has the turn. |
| C4 interrupts | the turn's end, with an abort's reason | the latest stop record's `turnOutcome` | Interrupted passes only against an abort for reason `interrupted`; any other reason fails. A completed or failed outcome passes if equal. Pending or unknown passes where Codex recorded no end, and is inconclusive where it recorded one the App did not learn. Failed if the App records an end Codex did not record, or a stop of a turn Codex has no record of. Inconclusive for an outcome outside the schema's five. Not run if no stop was requested. |
| W1 workflow | not compared in this version | not compared in this version | Blocked, with the reason "the workflow comparison is not available in this version", where the session has a workflow run to compare; otherwise no row. Never passed. |

When one side cannot be read, its comparisons are blocked, with the reason. Once the root is admitted, nothing ends without rows: any refusal or unexpected failure writes blocked rows for every planned comparison. The reason names at most the kind of failure.

A saved view is taken after the session ended. Comparing views at earlier points of a run is a later part.

**Values by allowlist.** Every value written into a row is either from a closed set (statuses, abort reasons, stop outcomes, states and sources), or an identifier, a digest or a number matching its pattern. Anything else is written as `unrecognised`. A row naming anything unrecognised never passes, and the summary counts such rows apart. Reasons are the tool's own sentences: no text from any input reaches a row.

## Output

The output is `record/session-comparison-<UTC>.jsonl`. It is always a new file: an existing name is never written over. It contains, in order:
1. a header line: `{"header": true, "candidate_key", "examination_root", "tool", "tool_sha256", "model_version", "pinned_codex", "compares", "workflow_comparison", "saved_views_not_named"}`, and on an answers file `answers_of`.
   - `saved_views_not_named` lists the saved views in `record/` that the command was not given, and the tool says the same on stderr. A view that exists is never passed over silently.
   - A file of blocked rows written after a failure carries the header without that list. Its fields read from files (`candidate_key`, `tool_sha256`) are null where reading them failed, so the header itself cannot stop the rows being written.
2. one row per comparison: `{"comparison", "subject", "codex", "app", "outcome", "reason"}`;
3. a summary line: `{"summary": {comparison: {outcome: count}}, "unrecognised": n, "compares", "workflow_comparison"}`. A W1 row is counted under `W1`, as blocked. It is derived from the rows, and the tool refuses to write a file whose summary would disagree with its rows, or in which a planned comparison has no row.

File names end in a random suffix, and no existing file is written over.

Rows carry only identifiers, statuses, line numbers and digests, never message or output text. So they may be copied out of the root and read by any lane.

## Use

```sh
python3 app/examination/session_comparison/compare.py compare --root <examination root> --thread <threadId> \
    [--view <root>/record/host-status-<checkpoint>.json]
python3 app/examination/session_comparison/compare.py answers --root <examination root> \
    --screen <root>/record/screen-list-<UTC>.jsonl
python3 -B -m unittest discover -s app/examination/session_comparison -p 'test_*.py'
```

Either command takes `--comparison C2`, `C3` or `C4` (all three are always made). `--comparison W1` or `--comparison workflow` is refused: the workflow comparison is not available in this version.

It uses the standard library only and sends nothing anywhere.
