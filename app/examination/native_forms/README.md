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

## Connected exact-input preparation wrapper

`pre_run_form.py` consumes the separate frozen selection from
`standalone/pre_run_inputs.py`. It calls the unchanged blank-form producer and
preserves its entire output as the prefix, appending a clearly labelled
**preparation attachment** with exact plan/selection/source identities, all
selected fixture roles and the complete selected EXP tuple. This is not a
result sidecar or completed form; every original field stays blank.

From `app/`, with the exact plan and frozen input selection prepared as described
in `../standalone/README.md`:

```sh
python3 -B examination/native_forms/pre_run_form.py generate \
  --plan /private/tmp/b7-plan.json --selection /private/tmp/b7-inputs.json \
  --selection-sha256 <previously-frozen-selection-sha256> --case V4-EXM-10 \
  > /private/tmp/b7-form.md
shasum -a 256 /private/tmp/b7-form.md
python3 -B examination/native_forms/pre_run_form.py check-blank \
  --plan /private/tmp/b7-plan.json --selection /private/tmp/b7-inputs.json \
  --selection-sha256 <previously-frozen-selection-sha256> --case V4-EXM-10 \
  --form /private/tmp/b7-form.md --form-sha256 <previously-frozen-form-sha256>
```

V4-EXM-11 and V4-EXM-12 use the same selection with their own case argument.
A changed plan, selection, fixture/source or form refuses. An edited or completed
form is outside `check-blank`; its observations require the later examination
route. A successful check means preparation fidelity only, with native run,
result and qualification flags false. The wrapper uses new fixed dependency
pins; it leaves the original blank helper and source lock byte-for-byte intact.
J-1 remains empty and examples are not installed or registered. Actual drafting,
trial, review, A15, candidate selection and native observations remain ahead.
