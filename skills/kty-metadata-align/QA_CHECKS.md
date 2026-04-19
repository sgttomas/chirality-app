# kty-metadata-align — QA Checks

Minimum checks for a valid run:

1. `KTY_PATH` exists and resolves to exactly one `KTY-*` folder.
2. The decomposition produced one unambiguous KTY truth row for the target
   folder.
3. The run classifies observed issues into:
   - `REPAIRED_NOW`
   - `RERUN_LATER`
   - `UNRESOLVED`
4. `REPORT_ONLY` runs do not modify metadata files.
5. `ALIGN_METADATA` runs modify only files explicitly authorized in
   `AllowedWriteTargets`.
6. Any `_STATUS.md` edit is append-only and evidence-backed.
7. No files other than `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md`, and the
   optional report were modified.

## `_CONTEXT.md` validation

When `_CONTEXT.md` is rewritten:

- the title matches `# Context: {KTY-ID}`
- the file contains `Name`, `Category`, `Discipline`, `Type`, `Responsible`,
  `CanonicalSchema`, `IntendedUsers`, `WhenUsed`, `Description`,
  `Anticipated Artifacts`, and `Decomposition Reference`
- missing decomposition values appear as `TBD`, not invented prose

## `_STATUS.md` validation

When `_STATUS.md` is modified:

- the change is append-only
- the appended line identifies the authoritative status or alignment basis
- the skill did not invent a lifecycle state not supported by the brief or
  existing evidence

## `_REFERENCES.md` validation

When `_REFERENCES.md` is rewritten:

- the file remains a references container
- authoritative references remain distinct from notes
- preserved manual notes, if any, are not silently promoted to authoritative
  pointers

## Follow-on action validation

If the run observes drift in `Scoping.md` or `KA-*.md`, the report or task
output must:

- name the affected file(s)
- state that no content-file edits were performed
- classify the issue as `RERUN_LATER` or `UNRESOLVED`

## Success case

A clean run reports:

- target KTY ID
- mode used
- files modified, if any
- whether any follow-on reruns remain
