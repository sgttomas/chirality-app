# Session comparison

This compares the App's account of a Codex session with Codex's own record of the same session, for a run in an examination root. It serves DEL-09-02 AC-005: "the candidate's presentation agrees with the supplier's actual events". Each comparison ends as one of REQ-007's five outcomes: passed, failed, blocked, not run or inconclusive.

It makes three comparisons of one thread every time: its turns (C2), their outcomes (C3), and the interrupts the App recorded (C4). In an examination root with one workflow run, it also compares the workflow supplied (W1). Children, items, outputs, conversations and order follow in later parts.

**The workflow comparison (W1) covers a root with one run.** How a run is associated with a Codex message in general did not settle in three readings, and is not reopened here. Nor are other runs interpreted: Agent 0 narrowed W1 to an examination root that holds one run. W1 passes only where all of these hold:
- the candidate's records store in the root holds records of exactly one run: exactly one run start, of any conversation, which must be of this thread, and otherwise only end notices and supply checks naming that same run;
- Codex's record of the thread holds exactly one line mentioning the workflow markers, a message, and within it one text element;
- `record/selected-workflow/` in the root holds the examiner's copy of the candidate's own bytes of that bundled workflow, tied to the candidate's identification and to every launch record of the root;
- the text element equals the run text the App composed, byte for byte. Its files line is the one the candidate's package makes, and its bytes between the markers are the candidate's own `WORKFLOW.md` of the selected revision. The run names that workflow's full source-qualified identity, as the candidate's bundled manifest gives it (DEL-02-02 AC-005, DEL-01-04 AC-011).

Anything else, or anything unreadable or untied, is blocked, never passed and never inferred. With one of each read and tied, a difference fails. One conversation with one run is what J1 is. See [The workflow comparison](#the-workflow-comparison-w1) for what it reads and what it does not establish.

**The claim.** A row says passed only when both sides were read, were identified as the same subject by an identifier and not by position (for W1, by being the only run of the root and the only message mentioning the markers), and agree. Every other case is failed, inconclusive, blocked or not run. Every planned comparison yields at least one row, and no row carries message or output text.

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
  - Every line must be a session line, and no object in it may name a key twice.
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
3. `answers` writes the candidate's whole result: C2 and C3 from the answers, with C4, and W1 where the session has a workflow run or W1 was asked for. W1 is read from the records alone and is never asked of the operator.
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
| W1 workflow | the one text element of the one message mentioning the workflow markers | the root's one run start, and the candidate's own bytes of the selected workflow | Passed only where the root holds records of one run, both sides are read, the selected workflow's bytes are tied to the candidate, and the element equals the run text byte for byte. Its files line must be the package's, the candidate's own `WORKFLOW.md` must be between its markers, and the run must carry the candidate's identity of that workflow. Failed, with one of each read and tied, where the text, the markers, the files line, the bytes or the identity differ. Blocked for a record of another run in the root, any other count, or anything unreadable or untied. No row where the session has no workflow run, unless W1 was asked for by name. |

When one side cannot be read, its comparisons are blocked, with the reason. Once the root is admitted, nothing ends without rows: any refusal or unexpected failure writes blocked rows for every planned comparison. The reason names at most the kind of failure.

A saved view is taken after the session ended. Comparing views at earlier points of a run is a later part.

## The workflow comparison (W1)

A session has a workflow run to compare when a line of Codex's record mentions the workflow markers, when a run record of the store names the thread, or when the store cannot be read whole. W1 asked for by name (`--comparison W1`) always has its row, blocked where there is nothing to compare. A screen list made with `--comparison W1` says so in its header (`planned`), and its `answers` keep the row. That only plans a row: W1 is derived from the records then, never from the list or the answers. Otherwise, without any of these, there is no W1 row. Where the session cannot be read, the W1 row is blocked like the others.

**What is detected.** Every JSON value in this comparison is read strictly: an object that names a key twice, or a NaN or Infinity, is not read. In the session file that blocks every comparison, as any unreadable line does. A line mentions the workflow markers when the word `chirality-workflow`, case-folded, appears in its bytes or in any string or key of it once read as JSON. That is all that is detected. A form in which that word itself is spelled otherwise (its letters escaped, encoded or split) is not detected, and nothing here claims that no such line exists.

**Codex's side.**
- Exactly one line may mention the markers, and it must be a `response_item` message. None, two or more, or any other line mentioning them (an event of any kind, a reply, a tool's output), is blocked.
- The message must be the person's (`role` `user`) and name, in its metadata, a turn that the session's turn events hold. Every element must be a text element (`type` `input_text` and `text`, nothing else), and the markers must be in exactly one of them. Otherwise it is blocked.
- That element must mention the word exactly twice, in its one begin marker and its one end marker. Any other mention, in whatever form surrounds it, is blocked, even where the bytes would agree.

**The App's side: one run in the root.**
- **Where the records are read.** Only from the records store the App uses on this route, never by searching the root for names.
  - The launcher gives the App the root's `home/` as its home, and no `CHIRALITY_RECORDS_STORE` (its environment allowlist).
  - The custom-protocol feature makes Tauri's `is_dev()` false. This remains an identified development candidate; Tauri's mode controls the store placement here. The App keeps its store in its data folder: `home/Library/Application Support/<identifier>/records/`. The identifier is the one every launch record of the root names.
  - The records read are those in `projects/<key>/workflow/` of that store.
  - A person's chosen store (`records-store.json` in the App's data) blocks, because its place is not established here.
  - Records kept in place in the launcher's project (`project/.chirality/records`) are outside this case, and block.
  - So does an identification whose build lacks the custom protocol: Tauri's `is_dev()` mode keeps no store in its App data.
- **How they are opened.** Every folder from the root to each record folder is opened without following a link. A link, a non-folder or a folder that cannot be opened blocks, before any record is opened. A folder that does not exist means no record there.
  - In a record folder, every entry must be a plain `<id>.json` file with one name.
  - A link, a second hard link, a staging file, a subfolder or any other entry blocks. A link or alias is refused before it is opened.
- **What is counted.** Each record is read as the envelope the App publishes: exactly its seven fields, `version` 1, a `record_id` naming the file, a writer and a time, and a body naming a known kind (`selection_record`, `run_text` or `supply_check`) and a conversation.
  - A record that is not such an envelope may be a record of a run, and blocks.
  - A selection record must carry every field the App writes, and is not counted.
  - A run record is a `run_text` (purpose `run start` or `run end notice`) or a `supply_check`. Each names its run in `run`; the App copies a check's `run` from the run text it checks.
  - The store must hold exactly one run start, of any conversation, and it must be of this thread. A second run start blocks, even of the same run.
  - Every other run record must be an end notice (`run_text`, purpose `run end notice`) or a `supply_check`, and its `run` must be the run start's. Only its kind, purpose and `run` are read; nothing else in it is interpreted.
  - A run record of another run, one naming no `run`, or a `run_text` of no known purpose blocks. So does a record whose kind cannot be read.
  - The App publishes an end notice when a turn is sent after the person ends the run, and a supply check when the person asks it to check the supplied text. Both are of the same run, and leave it one run.
- **The fields validated** of that one run start:
  - `record_kind`, `purpose`, `framing` (`WR-FRAME-1`), `run`, `conversation`, `holding_library`, `selection` and `origin_of_start`, with their types and values;
  - `chain`, which must be null (a run following another is not compared);
  - `workflow`: exactly its kind, origin, source root, name, full revision and revision method;
  - `workflow_file` and `text_identity`, as exact-bytes digests with their byte counts;
  - `other_files`, the paths and digests;
  - `lines`: the start, proposal and files lines and the markers.

  The start and proposal lines and the markers must be the ones the App's composer makes from that identity and run. A files line must name a folder by the App's rule: relative to the project or `~/`, with no `"`, backslash or control character, and no empty, `.` or `..` component. `assurance` is only checked to be an object; it is not compared.

**The selected workflow's own bytes.** The examiner prepares `record/selected-workflow/` from the identified candidate before the walk. Preparing it is done outside the controls and is named as such in the step's record. It holds byte copies, never anything from the App's records or an installed App:
- `identification/candidate-identification.json` and the stored inventory beside it, from the candidate folder that the launcher admits;
- `MANIFEST.json`, the candidate's `Contents/Resources/workflows/MANIFEST.json`;
- `package/`, every file of the selected package, `Contents/Resources/workflows/<name>/`;
- `reference.json`, holding only `name` and `bundle_path` (`Contents/Resources/workflows/<name>`).

W1 recomputes every tie from these bytes and trusts no digest it is given:
- the identification record passes the candidate identification's own validation (`identify.py`, which uses `jsonschema`);
- the inventory's digest is the one the record names, and it yields the record's build identity;
- every launch record of the root (and `kept.json`, where there is one) names the record's candidate key and bundle identifier;
- each launch record's bundle is the one its candidate folder holds under the record's bundle name, and it was made no earlier than the candidate was identified;
- the package copy is the inventory's files under `bundle_path`, file for file, by size and digest;
- the manifest copy is the inventory's `MANIFEST.json`;
- the manifest names the package once, with its files and with the revision recomputed from the copied bytes by the App's package method.

Any of these missing or not holding is blocked. Only a bundled run is compared. A run of another origin, or of another name than the reference's, is blocked.

**The comparison.** With one of each read and tied, W1 fails where any of these differs, and passes only where none does:
- the element's begin and end lines and the record's markers;
- the element's digest and byte count and the record's text identity;
- the run's workflow identity and the candidate's: origin `bundled`, the manifest's `release_subject` as source root, name, full revision and revision method;
- the run's `other_files` and files line and those the candidate's package makes: every file but `WORKFLOW.md`, in path byte order, by path and digest, and no files line where there is none;
- the bytes between the record's frame and the candidate's own `WORKFLOW.md`;
- those bytes and the record's `WORKFLOW.md` digest and byte count.

The row carries:
- the selected workflow's origin, name and revision;
- the run and the record identifier;
- the message's line, turn and element index;
- the digests and byte counts of both sides;
- under `selected`, the candidate key, the manifest digest and the candidate's own `WORKFLOW.md` digest and byte count.

It never carries text. The copies stay in the examination root and never enter Git.

**What it does not establish.**
- A root holding records of more than one run is blocked as a whole: several runs, a run started from another, or a run of another conversation. Children's inputs are not compared.
- An end notice or supply check of the run is counted, not compared: W1 compares the run start's text only.
- The reference ties the copied bytes to the identified candidate. That the launched bundle is that candidate is the launcher's identification check at launch.
- That the reference was prepared before the walk is the examiner's attestation. The records hold no time for the copy: the launch record's `made_at` and the identification's `identified_at` are compared, but they order the launch after the identification, not the copy before the walk.
- Project and user workflows are not compared, since their bytes are not tied to the candidate.

## Output

The output is `record/session-comparison-<UTC>.jsonl`. It is always a new file: an existing name is never written over. It contains, in order:
1. a header line: `{"header": true, "candidate_key", "examination_root", "tool", "tool_sha256", "model_version", "pinned_codex", "compares", "workflow_scope", "saved_views_not_named"}`, and on an answers file `answers_of`. `model_version` is `session-comparison-model/2`. A file of version 1 carried `workflow_comparison`, "the workflow comparison is not available in this version", and its W1 rows are only blocked.
   - `saved_views_not_named` lists the saved views in `record/` that the command was not given, and the tool says the same on stderr. A view that exists is never passed over silently.
   - A file of blocked rows written after a failure carries the header without that list. Its fields read from files (`candidate_key`, `tool_sha256`) are null where reading them failed, so the header itself cannot stop the rows being written.
2. one row per comparison: `{"comparison", "subject", "codex", "app", "outcome", "reason"}`;
   A W1 row also carries `selected`, the candidate's own bytes of the selected workflow by digest.
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

Either command takes `--comparison C2`, `C3`, `C4` or `W1`. The first three are always made. W1 is made where the session has a workflow run, and always when it is asked for by name. Any other name is refused, and nothing is written.

It uses the standard library only, except that W1 runs the candidate identification's own validation (`identify.py`, with `jsonschema`), and it sends nothing anywhere.
