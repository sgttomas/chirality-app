# Recording delegated work

This applies only when you delegate a bounded piece of work to a sub-agent. If you do the work yourself, write none of it.

When you do delegate, record it in files, so that the person can follow it in the App's Delegated work view and the work can be picked up again from the files alone. You write these records with your ordinary file tools; the App reads them and never writes them for you.

Three hands write, and each writes only its own:
- You write the brief, the work graph, and the records of the returns, reviews and integrations you yourself receive or perform.
- The App writes what it observes of Codex: that a sub-agent was started, what Codex last reported of it, and when it stopped being observed. Never write a line of kind `dispatch_observed`, `child_observed`, `observation_ended` or `related_conversation`, and never name the App as a recorder.
- The person performs the acts that are theirs, in the App. Never write a record that a person decided, accepted, approved or checked anything.

Everything is JSON under `.chirality/fleet/` in the project folder. A file is written once and never edited: a change is a new file or a new line. Every record starts with the same fields, shown here as `HEADER`:

```json
"format": "chirality.fleet.record", "formatVersion": "0.1",
"recordId": "fl:<unique within the project>", "kind": "<kind>",
"undertaking": "<one short name for this whole piece of work>",
"recorder": {"kind": "agent", "identity": "<a stable name for you>", "role": "<your role>"},
"writtenAt": "<date and time>"
```

A role is one of `HELP_HUMAN`, `HELPS_HUMANS`, `WORKING_ITEMS`, `TASK`, `none` or `not known`. A `recordId` is `fl:` followed by letters, digits and `. _ : / -`.

## To delegate one piece of work

1. **Write the brief**, one file for one work item, `briefs/<item>.json`. Use only letters, digits, `.`, `_` and `-` in the file name; the App resolves no other name:

```json
{HEADER, "kind": "brief", "body": {
  "briefId": "brief:<item>", "workItem": "<item>",
  "purpose": "<what is wanted and why>",
  "basis": [{"kind": "file", "ref": "<path of what it rests on>"}],
  "context": [{"kind": "file", "ref": "<path of what else to read>"}],
  "authority": {"mayDecide": ["<what the delegate may decide>"],
    "escalate": ["<what it must bring back>"],
    "reservedToPerson": ["<what only the person decides>"]},
  "tools": [{"tool": "<tool>", "limit": {"statement": "<the limit>", "standing": "stated-not-enforced"}}],
  "writeScope": [{"target": "<path>", "limit": {"statement": "write only <path>", "standing": "stated-not-enforced"}}],
  "expectedReturn": {"description": "<what comes back>", "form": "file and message", "returnPath": "<where it comes back>"},
  "preparedBy": {"kind": "agent", "identity": "<you>", "role": "<your role>"},
  "delegateRole": "TASK",
  "limits": [{"statement": "a task agent does not delegate", "standing": "stated-not-enforced"}]}}
```

   A limit you state prevents nothing by itself. Write `"standing": "stated-not-enforced"` unless you can name what enforces it; then write `"enforced-by-supplier"` or `"enforced-by-host"` with a `"mechanism"`.

2. **Write the work graph**, one numbered revision file for the undertaking, `graphs/<undertaking>/r<n>.json`. It lists the selected work: every item with its outcome, its owner, its brief and what it needs first.

```json
{HEADER, "kind": "work_graph", "body": {"revision": 1, "projectDagRef": "<the project's dependency graph, or none>",
  "items": [{"itemId": "<item>", "outcome": "<the result wanted>",
    "owner": {"kind": "agent", "identity": "<who does it>", "role": "TASK"},
    "brief": "brief:<item>", "selected": true, "next": "<what follows>",
    "needs": [{"kind": "item", "ref": "<another item that must be integrated first>"}]}]}}
```

   A need is one of: `"item"` (another item's integrated result), `"input"` (a file under `.chirality/fleet/`, by its path there), or `"decision"` (a decision package, below, by its path in the project, `project/decisions/<name>.json`). Leave `needs` empty when there is none.

3. **Make that revision current.** Append one line to `coordination.fleet.jsonl`:

```json
{HEADER, "kind": "current_graph", "body": {"graph": "<the graph file's recordId>",
  "graphContent": {"method": "chirality.app.exact-bytes.sha256/v1", "value": "<SHA-256 of the graph file, lowercase hex>"}}}
```

4. **Start the sub-agent with this line in its prompt, on a line of its own:**

```
Chirality-Brief: briefs/<item>.json sha256:<SHA-256 of the brief file, lowercase hex>
```

   This line is the only thing that ties the sub-agent to its work item on the graph. Compute the digest from the file as written (`shasum -a 256 <file>`). The line names the brief; it does not deliver it. Put what the sub-agent must know, including what it owes back and where, in the prompt as well.

## When work comes back

A sub-agent finishing is not a return until you have received what it produced and recorded that. Append one line to `coordination.fleet.jsonl` for each fact, when it happens and only if it happened:

```json
{HEADER, "kind": "return_recorded", "body": {"workItem": "<item>", "brief": "brief:<item>",
  "returnedBy": {"kind": "agent", "identity": "<who returned it>", "role": "TASK"},
  "returned": [{"kind": "file", "ref": "<path of what came back>"}],
  "evidence": [{"kind": "file", "ref": "<path that shows it>"}]}}
{HEADER, "kind": "review_recorded", "body": {"workItem": "<item>", "returnRef": "<the return's recordId>",
  "reviewer": {"kind": "agent", "identity": "<who examined it>", "role": "<role>"},
  "verdict": "no blocking findings", "findings": [{"kind": "file", "ref": "<path of the findings>"}]}}
{HEADER, "kind": "integration_recorded", "body": {"workItem": "<item>", "returnRef": "<the return's recordId>",
  "integrator": {"kind": "agent", "identity": "<who integrated it>", "role": "<role>"},
  "evidence": [{"kind": "file", "ref": "<path that shows it>"}]}}
```

A review's verdict is `"no blocking findings"`, `"findings to repair"` or `"not concluded"`. If something the work rests on changes, append a line naming the changed file and the items it affects:

```json
{HEADER, "kind": "basis_changed", "body": {"changed": {"kind": "file", "ref": "<path of what changed>"}, "affectedItems": ["<item>"]}}
```

## A decision that is the person's

Do not decide it, and do not record that the person decided. Write a decision package, `project/decisions/<name>.json` in the project folder, and tell the person it is waiting:

```json
{"format": "chirality.decision-package", "formatVersion": "0.1", "packageId": "pkg:<name>", "actKind": "A16",
 "subject": ["<what is to be decided>"], "purpose": "<why>", "scope": "<what it covers>",
 "reservedBy": [{"ref": "<the brief or instruction that reserves it>", "statement": "<what it says>"}],
 "alternatives": [{"id": "ALT-1", "statement": "<one course>", "consequences": ["<what follows>"]},
                  {"id": "ALT-2", "statement": "<another course>", "consequences": ["<what follows>"]}]}
```

The person decides in the App. Only that makes it decided: your message, a tool's success or a return never does. State each alternative and its consequences evenly, and recommend nothing inside the package.
