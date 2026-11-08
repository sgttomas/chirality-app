# Reader brief — reconstruction rehearsal on FX-DP1 (v0.2)

v0.2 adds step 3, how to name a claim's subject and state an absence (after RR-E; RRM §4). RR-E's reader received v0.1 (sha256 4bf425b9…26aa).

For a **fresh** reader with no part in the run. The coordinator dispatches the reader and records exactly what it supplied: this brief, the input-set manifest and a copy of the listed files. That record is the reader's separation evidence (R23-10).

You are the reader for a reconstruction rehearsal. Someone else produced the files you are given. You took no part in that work.

**You are given:**
- a folder holding the files listed in `IS-FX-DP1.input-set.json`, each with its sha256;
- the manifest itself;
- the account schema `rrm.reconstruction-account.schema.json`.

**You may read only those files.** Do not open any other file, repository, history, session or conversation. If you need something that is not in the set, write it down as an unknown.

**Do this:**

1. Check each file's sha256 against the manifest. Report any mismatch, then stop.
2. From the files whose standing is `record` or `project_file`, reconstruct:
   - what was requested (each decision package: the act asked for, its subject, its alternatives and their consequences, and who asked);
   - what was decided (by whom, and which alternative), and who recorded it;
   - whether anything shows that the package changed after the decision;
   - what changed or happened afterwards.
3. Name each claim's subject in `about` by its identifier as it appears in the files: for a decision package, its `packageId` (for example `PKG-1`), its file path or its request record id. State an absence with the absence kinds — `no_decision`, `no_change` or `no_outcome` — not as an `outcome` or `change` claim.
4. Cite every claim's sources by path and locator. A file whose standing is `not_authority` may be read but never supports a claim. If you read one, list it under `not_authority_read`.
5. Where the files do not establish something, list it under `unknowns`. Never fill it from what seems likely.
6. Write one account that is valid against the schema:
   - your identity and kind (`agent`), your model identity, and `separation`: "fresh instance; supplied context recorded by the coordinator at ‹reference›";
   - `input_set` with the manifest's `input_set_id` and the manifest file's sha256;
   - today's date as `observed_clock`.

Return the account file and nothing else.
