# Sign-in flow readings

A reading is a person's or an independent reviewer's reading of the sign-in flow that a candidate's
host source actually uses (DEL-01-06 VER-004). `app/packaging/terms/flow.py` binds its result to
one reading. It never writes a reading, and an agent that wrote the sign-in code does not write one.

A reading is one JSON file in this folder, made against the exact host source tree the tool reports
(`source.tree_sha256`). Any change under `app/src-tauri/src` makes it stale, so a reading is made
once, for the final candidate. The tool's `source.evidence` lists, by plain text search, every line
containing `account/login`, `login/start` or `LoginAccount`. That search can miss an unusual
spelling, so it is a starting point for the reader, not a substitute for reading.

Exactly these fields, and no others:

```json
{
  "format": "chirality-terms-sign-in-reading/v1",
  "source_tree_sha256": "<64 lowercase hex: source.tree_sha256 from the tool>",
  "pin": "<the candidate's declared pin, x.y.z>",
  "reader": {"name": "<who read it>", "role": "<owner or reviewer>", "did_not_write_the_sign_in_change": true},
  "date": "YYYY-MM-DD",
  "account_sign_in_types": ["<each type the host sends for account sign-in>"],
  "separate_credential_logins": [
    {"type": "<e.g. apiKey>", "home": "<the dedicated home it goes to>",
     "sent_from": [{"file": "<path relative to app/src-tauri/src>", "line": 1}]}
  ],
  "relied_on": [{"file": "<path relative to app/src-tauri/src>", "line": 1}]
}
```

Each `file` and `line` must exist in that source tree. A reading that is incomplete, has other
fields, or names a missing file or line makes the result unresolved. So does more than one reading
for the same tree.
