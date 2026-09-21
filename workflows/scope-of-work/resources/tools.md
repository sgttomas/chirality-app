# TOOL POLICY — scope-of-work

## Required order

1. Read and hash the authoritative source kit and `_STATUS.md`.
2. In `CONVERT`, run `convert_four_documents_to_scope_of_work.py` only under
   exact accepted path-scoped migration authority. `INIT` is source-grounded
   authoring and `VERIFY` is read-only on production content.
3. In `CONVERT`, refine the evidence candidate through bounded reasoning
   without removing source markers. In `INIT`, author the production
   `ScopeOfWork.md` directly from accepted decomposition and source evidence;
   there is no evidence candidate to refine.
4. In `CONVERT`, run `map_scope_of_work_claims.py` and
   `report_scope_of_work_parity.py` independently of the authoring judgment.
   Both tools require `--source-dir` and are structurally conversion-only; they
   are not run under `INIT` or `VERIFY`.
5. In `CONVERT`, run `finalize_scope_of_work.py` into a distinct
   production-candidate path; rerun mapping and parity with
   `--production-scope-of-work` so both bind and verify that exact clean
   artifact. `INIT` has no finalization step: the authored contract is the
   production contract.
6. Run `validate_scope_of_work.py` against the production contract — in
   `CONVERT` the clean finalized candidate produced by step 5, in `INIT` the
   `ScopeOfWork.md` authored in step 3. Steps 6–8 take the same production
   contract as input in every mode; only how it was produced differs.
7. Run `derive_review_checklist.py` against that production contract; preserve
   its exact `AC-*` order, text, source binding, and matrix linkage.
8. Run `render_scope_of_work.py` only from that production contract and only
   when a derivative was requested.
9. Run `check_boundary_owner_resolution.py` against the production contract for
   QA item 21, writing any JSON report to a run-local path. It is read-only and
   mode-agnostic. `UNRESOLVED_OWNER` and `UNDEFINED_CLAIM` are failures.
   `NOT_CHECKABLE` (a per-act exclusion clause) and `NO_CITED_CLAIM` (a
   whole-requirement exclusion citing no claim) are neither passes nor
   failures: both route that requirement to the workflow's own boundary-owner QA
   method. `NOT_APPLICABLE` marks a contract outside the `REQ-NNN` grammar.

## Allowed tools

- `tools/scope_of_work/convert_four_documents_to_scope_of_work.py`
- `tools/scope_of_work/finalize_scope_of_work.py`
- `tools/scope_of_work/validate_scope_of_work.py`
- `tools/scope_of_work/map_scope_of_work_claims.py`
- `tools/scope_of_work/report_scope_of_work_parity.py`
- `tools/scope_of_work/derive_review_checklist.py`
- `tools/scope_of_work/render_scope_of_work.py`
- `tools/scope_of_work/check_boundary_owner_resolution.py`

The tools are deterministic and local. They do not use a network or LLM and
do not modify lifecycle state. The converter writes only the evidence
candidate and the finalizer writes only its explicit clean production and
report paths; other report and checklist tools write only their explicit
output paths. Checklist derivation is idempotent and read-only on the production contract; it
fails before output for invalid or unauthorized ambiguous input.

## Disallowed use

- In `CONVERT`, no `--force` unless the brief explicitly authorizes replacement
  in the same isolated candidate workspace.
- No converter use on `ISSUED` without exact human-approved administrative
  representation-replacement authority and bound hashes.
- No write to legacy production documents or underscore files.
- No HTML tracking as canonical or accepted truth.
- In `CONVERT`, no checklist, HTML rendering, or integration from an
  evidence-rich candidate.
- No removal of `workflows/four-documents`, legacy readers, or compatibility callers.
