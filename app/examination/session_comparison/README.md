# Session comparison

This compares the App's account of a Codex session with Codex's own record of the same session, for a run in an examination root. It serves DEL-09-02 AC-005: "the candidate's presentation agrees with the supplier's actual events". Each comparison ends as one of REQ-007's five outcomes: passed, failed, blocked, not run or inconclusive.

It makes three comparisons of one thread every time: its turns (C2), their outcomes (C3), and the interrupts the App recorded (C4). Where the thread holds one workflow run, it also compares the workflow supplied (W1). Children, items, outputs, conversations and order follow in later parts.

**The workflow comparison (W1) is bounded by uniqueness.** How a run is associated with a Codex message in general did not settle in three readings, and is not reopened here. W1 instead passes only where the thread holds exactly one of each:
- Codex's record of the thread holds exactly one message carrying the workflow markers, and within it exactly one text element carrying them;
- the App's records hold exactly one run-start text for the thread;
- that text element equals the run text the App composed, byte for byte, and its bytes between the markers equal the stored `WORKFLOW.md` bytes the App recorded (DEL-02-02 AC-005, DEL-01-04 AC-011).

Any other count, or anything unreadable, is blocked, never passed and never inferred. One conversation with one run is what J1 is. See [The workflow comparison](#the-workflow-comparison-w1) for what it reads and what it does not establish.

**The claim.** A row says passed only when both sides were read, were identified as the same subject by an identifier and not by position (for W1, by being the only one of its kind on each side), and agree. Every other case is failed, inconclusive, blocked or not run. Every planned comparison yields at least one row, and no row carries message or output text.

## Codex's record, and where it may be read

- **The reference.** It is the session file Codex writes under its home: `sessions/YYYY/MM/DD/rollout-<UTC time>-<threadId>.jsonl`, one `{timestamp, ordinal?, type, payload}` per line. It holds:
  - each turn's start: `event_msg` `task_started`;
  - each turn's end: `task_complete`, with `error` when the turn failed, or `turn_aborted`, with its reason;
  - the messages of the conversation: `response_item` messages, the person's input among them.

  It does not hold everything the model was given. Codex sends each request with a developer message made from its base instructions, with some sections cut, and with its tool definitions; the file holds neither. It never holds approvals, requests to the person, warnings or errors other than a turn's own. None of these is compared here.
- **Checked against the real format.** The parser was checked against one real session file made at the pin, 0.169.0. That file was made by the pinned app server alone over stdio, its binary first checked against the pin's `GENERATION.json`, with the scripted loopback provider of `app/supplier_checks/recording_provider.py`, no model and no sign-in, in a fresh examination home with the supplier's default sandbox settings.
  - Its three turns (completed, interrupted, failed on a scripted provider error) and their lines read as the file records them: each turn's `task_started` and its end, `task_complete` with no `error` key, `turn_aborted` with reason `interrupted`, and `task_complete` with an `error` object of `message` and `codex_error_info`. Every turn event carried `turn_id`.
  - Lines the model does not read were there and change no reading: a top-level `metadata` on response items, `session_id` beside `id` in `session_meta`, and `thread_settings_applied` and `token_usage_record` lines.
  - Not seen in that file, and so read as the model already did: an `error` of null, the `turn_started` and `turn_complete` names, and abort reasons other than `interrupted`.
  - The file was removed after the check, and only notes on its format were kept. This check replaces the earlier one at 0.167.0, and a file of 0.167.0 is now blocked like any other version. `TheRealFormat` in the tests is an invented session laid out as the 0.169.0 file was.
- **A strict model.** The session file's bytes are read once, and both its digest and the model are made from those same bytes.
  - Every line must be a session line.
  - The first line must be `session_meta` naming the thread and the pinned Codex version, `cli_version` exactly `0.169.0`. A file written by any other version is blocked, not read on a guess. A new pin needs its own check against a real file before this changes.
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
3. `answers` writes the candidate's whole result: C2 and C3 from the answers, with C4, and W1 where the session has a workflow run. W1 is read from the records alone and is never asked of the operator.
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
| W1 workflow | the one text element of the one message carrying the workflow markers | the one run-start text record of the thread | Passed only where both are unique and read, and the element equals the run text byte for byte with the stored `WORKFLOW.md` bytes between its markers. Failed, with one of each, where the text differs, where the bytes between the markers differ, or where the markers name another workflow or revision. Blocked for any other count or anything unreadable. No row where the session has no workflow run. |

When one side cannot be read, its comparisons are blocked, with the reason. Once the root is admitted, nothing ends without rows: any refusal or unexpected failure writes blocked rows for every planned comparison. The reason names at most the kind of failure.

A saved view is taken after the session ended. Comparing views at earlier points of a run is a later part.

## The workflow comparison (W1)

A session has a workflow run to compare when a line of Codex's record carries the workflow markers, when a run text record names the thread, or when a workflow record cannot be read. Without any of these there is no W1 row. Where the session cannot be read, the W1 row is blocked like the others.

**Codex's side.** Every string of every line is searched for the markers' start, `<<<chirality-workflow`, case-folded, as it is and as decoded up to three times (HTML entities, `\u` and `\x` escapes, percent-encoding, and JSON held in a string); the line's bytes are searched the same way.
- The candidate is the one `response_item` message among the lines found. None, or two or more, is blocked. So is a message that is not the person's (`role` other than `user`), markers anywhere in the message other than its text elements, markers in more than one text element (the run text in one and the person's brief in another, say), and markers present only in an encoded form.
- Any other line carrying the markers blocks, unless it is an `event_msg` line of the same turn whose every marked string equals that text element exactly. Such a copy is counted (`copies`), not taken as a second candidate. A copy that differs in any byte, such as the run text joined to the brief, blocks.
- The element must carry exactly two markers (one begin and one end). Any other number is blocked, even where the bytes would agree, because a body that holds a marker makes its delimiters ambiguous.

**The App's side.** Every `*.json` file under a `records/…/workflow/` folder of the root is read as the envelope the App publishes: `version` 1, a `record_id` naming the file, and a `body`. A file that is not one is unreadable and blocks W1, since it may name the thread.
- Of the `run_text` bodies naming the thread, the `run start` ones are counted, and there must be exactly one. An end notice of the same run is counted apart and changes nothing; an end notice of another run blocks. A run start that follows an earlier run (a `chain`) blocks: several runs in one thread are not compared.
- The record must identify its text and `WORKFLOW.md` by `chirality.app.exact-bytes.sha256/v1` digests with their byte counts, and name markers that are its own workflow's name and revision. Otherwise it blocks.

**The comparison.** The record gives the frame: its start, proposal and files lines and its begin marker, each followed by a line break, then the workflow bytes, then a line break and the end marker. The element passes only where:
- its digest and byte count equal the record's text identity;
- its begin and end lines are the record's markers; and
- the bytes between that frame equal the record's `WORKFLOW.md` digest and byte count.

With one of each, a difference in any of these fails. The row carries the selected workflow's origin, name and revision, the run, the record identifier, the message's line, turn and element index, and the digests and byte counts of both sides. It never carries text.

**What it does not establish.**
- Several runs in one thread, a run started from another, and children's inputs are not compared: they are blocked or out of scope.
- The stored side is the digest of `WORKFLOW.md` that the App recorded when it composed the run text from the revision it verified. This tool does not read the revision store again. For a bundled workflow, that store is in the App's bundle, outside the examination root. That the recorded revision is the candidate's bundled one is a separate check against the candidate's manifest.
- That Codex's own copies of the message (`event_msg` lines) take the form allowed here was not checked against a real file at 0.169.0. A form that differs blocks; it never passes.
- Only the encodings named above are decoded. A marker hidden in another encoding (base64, say) is not found. Its line is then not a candidate, so it cannot add a pass.

**Values by allowlist.** Every value written into a row is either from a closed set (statuses, abort reasons, stop outcomes, states and sources), or an identifier, a digest or a number matching its pattern. Anything else is written as `unrecognised`. A row naming anything unrecognised never passes, and the summary counts such rows apart. Reasons are the tool's own sentences: no text from any input reaches a row.

## Output

The output is `record/session-comparison-<UTC>.jsonl`. It is always a new file: an existing name is never written over. It contains, in order:
1. a header line: `{"header": true, "candidate_key", "examination_root", "tool", "tool_sha256", "model_version", "pinned_codex", "compares", "workflow_scope", "saved_views_not_named"}`, and on an answers file `answers_of`. `model_version` is `session-comparison-model/2`. A file of version 1 carried `workflow_comparison`, "the workflow comparison is not available in this version", and its W1 rows are only blocked.
   - `saved_views_not_named` lists the saved views in `record/` that the command was not given, and the tool says the same on stderr. A view that exists is never passed over silently.
   - A file of blocked rows written after a failure carries the header without that list. Its fields read from files (`candidate_key`, `tool_sha256`) are null where reading them failed, so the header itself cannot stop the rows being written.
2. one row per comparison: `{"comparison", "subject", "codex", "app", "outcome", "reason"}`;
3. a summary line: `{"summary": {comparison: {outcome: count}}, "unrecognised": n, "compares", "workflow_scope"}`. A W1 row is counted under `W1` with its outcome. It is derived from the rows, and the tool refuses to write a file whose summary would disagree with its rows, or in which a planned comparison has no row.

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

Either command takes `--comparison C2`, `C3`, `C4` or `W1`. The first three are always made, and W1 is made where the session has a workflow run. Any other name is refused, and nothing is written.

It uses the standard library only and sends nothing anywhere.
