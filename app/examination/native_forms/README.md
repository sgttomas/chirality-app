# Blank N-1 forms from standalone preparation

From `app/`, use the actual B7 preparation producer, then this consumer:

```sh
python3 examination/standalone/prepare.py prepare > /tmp/sq-preparation.json
python3 examination/native_forms/native_form.py generate --plan /tmp/sq-preparation.json --case V4-EXM-10 > /tmp/SQ10-N1-blank.md
python3 examination/native_forms/native_form.py check-blank --plan /tmp/sq-preparation.json --case V4-EXM-10 --form /tmp/SQ10-N1-blank.md
```

Repeat for V4-EXM-11 and V4-EXM-12. All operations are offline file operations.
Generation writes only stdout; it creates no examination, record id or run.
The B7 consumer and its local inputs are pinned here; B7 checks its own canonical
source lock before this consumer accepts a preparation. Altered source lists,
candidates, steps, order or case content refuse. No dated run artifact is a
runtime dependency.

EXP §8.2 supplies the header, step-table and close layout. Every observation,
time, actor, capture, candidate header and examiner statement starts blank.
Expected source actions are separately labelled guidance. B7's null candidate
slot remains unassigned; identifying a real candidate and completing the form
belongs to the examiner's later authorized run. Record-specific naming,
form_ref and evidence digest are instructions for that future completed form.

`check-blank` compares the exact generated blank artifact, including its case
and canonical-JSON preparation digest. Exit 0 establishes only preparation
fidelity. Edited or completed forms return 1; this command does not judge their
observations. It supplies no result schema validation, N-1 execution, route
admission, full support identity (CI26), qualification or acceptance. No new
canonical schema or identity encoding is introduced.
