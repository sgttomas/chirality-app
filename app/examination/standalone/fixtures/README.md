# Invented workflow fixture pack

These four packages are unregistered test inputs for B7. They are kept outside
workflow discovery. Each has matching folder/frontmatter name and a WD-v0.8
declaration read by the actual App consumer. The selected authoring method was
`chirality-root:bundled:workflow:create-workflow`; this fixture-only destination
is the assigned test boundary, not a project or personal library registration.

| Package | Intended later use | Distinct behavior |
|---|---|---|
| revision-1/invented-pipe-inventory | J-3/J-4 draft, future J-5/J-6 review/registration | Total invented pipe pieces |
| revision-2/invented-pipe-inventory | J-8 first refinement | Adds material subtotals |
| revision-3/invented-pipe-inventory | J-9 second refinement | Also rejects duplicate item identifiers |
| user-collision/invented-pipe-inventory | Future ST-2 same name in user origin | Counts rows instead of pieces, visibly distinct |

`inputs/` contains initial, reuse and refinement CSVs plus an explicit duplicate
negative. Package `tally.py` reads an identified input and prints JSON with its
digest; it writes no file or record. For a future authorized tool action:

```sh
python3 <package>/tally.py <input.csv>
```

Review stdout and exit status before saving successful JSON to the scratch
project's `inventory-summary.json`. Missing/malformed input produces no output.
The method declares inputs, shell capability, outputs and evidence. It declares
an empty checkpoint list: workflow registration remains the person's separate
A15 act, and a routine tool permission is not an act or professional approval.

## Offline consumer preflight

From `app/`, with the approved dependencies already cached:

```sh
CARGO_NET_OFFLINE=true CHIRALITY_SKIP_CODEX=1 python3 tests/group_b_fixture_preflight.py
```

Set `CARGO_HOME` to an existing approved cache if required; no download occurs.
Use this worktree's default target or an isolated `CARGO_TARGET_DIR`. The test-only
crate hook calls production WD `read`, WR `Snapshot::capture`, `Review::open`,
`collisions`, and EXEC `Compatibility::check`. It checks all four packages,
changed-byte and wrong-name refusal, duplicate-declaration refusal, distinct
origins/revisions and unknown tool availability. Separate tool tests execute
actual fixture CSV computations and refusal cases. JSON stdout binds every
fixture byte; success means only offline fixture consumption.

## Native case staging remains ahead

Do not populate the future initial project before J-1: it begins empty. These
are examiner preparation examples for subsequent drafting, not a replacement
for the person's plan, execution, draft trial or review. Before native use the
examiner binds the selected fixture bytes and any changed draft in the case
definition. The person reviews/registers each revision through the App. These
files contain no A15, registration ledger, runnable selection or EXP result.
The collision is not installed by this preflight; the examiner must arrange
its actual user-origin entry as declared before J-5.

ST-1 still requires J-7's actual selection/run to retain revision 1 after J-8's
registration. Static snapshot preservation does not perform that stimulus.
ST-2 still requires the actual discovery notice, choices and non-rebinding.
ST-3 still requires the native unconfirmed-control wait, agent claim and draft
tool success with no A15; this tool's success is no native evidence. Required
ST-4/ST-5, N-1, executable candidate, configuration, permission requests and
three access modes remain with the existing case plan and their owners. None
is fulfilled by this pack, and no examination is opened.
