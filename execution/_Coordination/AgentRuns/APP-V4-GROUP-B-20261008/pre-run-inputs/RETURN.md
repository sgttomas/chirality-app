# B7 exact pre-run input preparation — author return

Completed the confirmed bounded helper and connected blank-form wrapper on
base `31cdbc9e17`, branch `codex/app-v4-b7-pre-run-inputs`. The commit carrying
this return identifies the author candidate. Independent review and integration
on the manager's current main remain separate; no push was performed.

## Produced contribution

`app/examination/standalone/pre_run_inputs.py` validates the unchanged B7 plan
and freezes its exact file digest with 46 pinned source files, 13 explicit
maintained fixture roles, and the fixed full canonical EXP support selection.
It checks a separately frozen exact selection digest and rejects missing/extra
fields, duplicate JSON keys, source/fixture drift, mixed support identities and
readiness/result injections. Descriptor-based no-follow reads refuse symlinks,
traversal and special files. Unlisted fixture companions/directories also refuse.
The captures identify bytes for this check; they do not authenticate external
custody or supply an atomic snapshot against arbitrary concurrent writes.

`app/examination/native_forms/pre_run_form.py` uses that checked preparation,
then calls the unchanged original blank-form producer. Its output preserves the
entire original form as the prefix and appends a labelled exact-input preparation
attachment. All record/candidate/actor/date/observation fields remain blank.
The exact generated form and selection digest are required for `check-blank`.
Edited or completed forms are outside that check.

New helper/wrapper pins are separate from all old source locks. Existing
prepare.py, native_form.py, their old locks, canonical support sources, Design
and fixture bytes are preserved. Only the two READMEs gain additive usage text.
No canonical schema, EXP sidecar, executed result or dossier is invented.

## Governing boundary

SQ §3 requires the examiner's later pre-run case definition and actual selected
material to be identified and digested; this increment supplies a concrete
preparation input contribution without opening that examination. EXP support
selection is source correspondence only, not verified producer use or SQ/native
result-consumer adoption. Existing null candidate and complete historical
missing-input text remain unchanged; they are not reinterpreted as live status.

J-1 still starts empty. The maintained fixture pack contains examiner examples
for later drafting, not substitutes for the person's plan, draft trial, review or
A15. Neither a collision origin nor a workflow is installed or registered. A
changed actual draft requires a fresh exact binding; it cannot pass this fixed
maintained selection. Fixtures are copied as data into a scratch source snapshot,
never executed or imported. Original source readers run from that checked snapshot,
which is removed afterward.

## Verification and reproducible evidence

**40 tests passed**, no skips: 12 new pre-run tests, 9 preserved standalone,
8 preserved native-form, 11 preserved canonical-support tests. Raw outputs are
in `evidence/*.log`. The first connected prepare → exact selection → blank form
path passed for all three scenarios before broader test construction.

The recorded actual CLI path is `evidence/CONNECTED_CHECK.json`, using:

- `evidence/plan.json`: original preparation output bytes.
- `evidence/selection.json`: selection SHA-256
  `a07350bc32b6deb0c6f91d2c479496218241be9cdb3df5b172733d2b1e1db134`.
- `evidence/SQ10-blank-with-preparation.md`: form SHA-256
  `138b77e8e068083a443aa051deb1554fec6b76ef4a9c6dfd467f37bedc31fc65`.

The check passes preparation fidelity and reports native run, result recorded
and qualification false. Maintained tests depend on maintained sources only,
never this dated evidence. `CHECKED_FILES.json` binds the candidate source/tests.

Staged diff and private-term screening are required before the author commit;
local host terms stay only in process memory/environment, never in files or
messages. Git identity is Ryan C Tufts <ryan@chirality.ai>.

## Return

WORKING_ITEMS `/root/group_b_successor` receives this increment for independent
review, current-main checks and integration. Manager/reviewer reserved files
were not authored. No native launch, download, supplier execution, credentials,
MEMORY, workflow authoring/registration, H3B/S1/Host or Group C changes occurred.
No readiness, examination, observation, native qualification, stage gate or
release follows from this preparation.
