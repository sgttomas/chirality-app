# Sign-in flow readings

A reading is a person's reading of the sign-in flow that a candidate's source actually uses
(DEL-01-06 VER-004). `app/packaging/terms/flow.py` binds its result to one reading. It never writes
a reading, and the agent that wrote the sign-in code does not write one.

## What the tool checks, and what it cannot

The tool reads everything from the Git object store at one named commit. It refuses a working
tree that differs from that commit under `app/`. The **bound set** is every file Git tracks under
`app/` at that commit except this folder. Its digest is the one the tool reports as
`bound_set.sha256`, in the form stated in its output (`bound_set_form`).

The tool checks that exactly one reading tracked in this folder at that commit:
- names a commit whose bound set has that digest;
- matches the candidate's pin;
- states the account sign-in types `chatgpt` and `chatgptDeviceCode`;

and that the reading is well formed.

**It cannot establish that an independent reading occurred.** A reading's truth rests on the review
of the pull request that commits it and on the named reader, not on the tool.

These are operator-run checks on stable inputs. They are built so that an observation that was not
made, that failed, or that is incomplete cannot come out as success, and so that drift and mistakes
are caught. They are not built to withstand a writer changing the inputs during the run, nor
someone with write access forging a reading.

**What makes a reading stale:** any change to a tracked file under `app/` other than this folder.
Committing the reading itself does not, so a reading is made once, for the final candidate, and
committed afterwards.

The tool's `evidence.lines` lists every line containing `account/login`, `login/start` or
`LoginAccount` in tracked files under `app/src-tauri` and `app/src`. That plain text search can
miss an unusual spelling. It is a starting point for the reader, not a substitute for reading.

## Format

Exactly these fields, and no field more than once:

```json
{
  "format": "chirality-terms-sign-in-reading/v2",
  "commit": "<full 40-hex commit the reader read>",
  "bound_set_sha256": "<the tool's bound_set.sha256 at that commit>",
  "pin": "<the candidate's declared pin, x.y.z>",
  "reader": {"name": "<who read it>", "role": "owner | independent reviewer"},
  "date": "YYYY-MM-DD",
  "how_read": "<in the reader's words: which commit, what was searched, what was read>",
  "account_sign_in_types": ["<each type the host sends for account sign-in>"],
  "separate_credential_logins": [
    {"type": "<e.g. apiKey>", "home": "<the dedicated home it goes to>",
     "sent_from": [{"file": "app/src-tauri/src/<file>", "line": 1}]}
  ],
  "relied_on": [{"file": "app/<path>", "line": 1}]
}
```

- `role` is `owner` or `independent reviewer`. The tool itself, an agent that wrote the change, and
  an empty name are not readers.
- Each `file` must be in the bound set, and each `line` must exist in it.
- A reading that is incomplete, repeats a field, has other fields, or names a commit whose bound set
  differs makes the result unresolved. So does more than one reading for the same bound set.
