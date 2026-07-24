# TOOL POLICY — scope-of-work

## Required order

1. Read and hash the authoritative source kit and `_STATUS.md`.
2. In `CONVERT`, run `convert_four_documents_to_scope_of_work.py` only under
   exact accepted path-scoped migration authority. `INIT` is source-grounded
   authoring and `VERIFY` is read-only on production content.
3. Refine the evidence candidate through bounded reasoning without removing
   source markers.
4. Run `map_scope_of_work_claims.py` and
   `report_scope_of_work_parity.py` independently of the authoring judgment.
5. Run `finalize_scope_of_work.py` into a distinct production-candidate path;
   rerun mapping and parity with `--production-scope-of-work` so both bind and
   verify that exact clean artifact.
6. Run `validate_scope_of_work.py` against the clean production candidate.
7. Run `derive_review_checklist.py` against the clean production SOW; preserve
   its exact `AC-*` order, text, source binding, and matrix linkage.
8. Run `render_scope_of_work.py` only from the clean production SOW and only
   when a derivative was requested.

## Allowed tools

- `tools/scope_of_work/convert_four_documents_to_scope_of_work.py`
- `tools/scope_of_work/finalize_scope_of_work.py`
- `tools/scope_of_work/validate_scope_of_work.py`
- `tools/scope_of_work/map_scope_of_work_claims.py`
- `tools/scope_of_work/report_scope_of_work_parity.py`
- `tools/scope_of_work/derive_review_checklist.py`
- `tools/scope_of_work/render_scope_of_work.py`

The tools are deterministic and local. They do not use a network or LLM and
do not modify lifecycle state. The converter writes only the evidence
candidate and the finalizer writes only its explicit clean production and
report paths; other report and checklist tools write only their explicit
output paths. Checklist derivation is idempotent and read-only on the clean SOW source; it
fails before output for invalid or unauthorized ambiguous input.

## Disallowed use

- No `--force` unless the brief explicitly authorizes replacement in the same
  isolated candidate workspace.
- No converter use on `ISSUED` without exact human-approved administrative
  representation-replacement authority and bound hashes.
- No write to legacy production documents or underscore files.
- No HTML tracking as canonical or accepted truth.
- No checklist, HTML rendering, or integration from an evidence-rich candidate.
- No removal of `skills/four-documents`, legacy readers, or compatibility callers.
