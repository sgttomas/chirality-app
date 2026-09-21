# Validation tools

## Path portability

`validate_path_anchors.py` checks executable repo-level instructions and
project live-entry surfaces for machine-local home paths. For a project that
declares `validation/portability_policy.json`, it also scans active AgentRuns
records and consumes the shared `tools/practitioner_harness/surface_roles.py`
classification:

- active `CONTROL` records must use repo-relative paths or root tokens;
- active `EVIDENCE` records may preserve exact machine provenance;
- active `UNCLASSIFIED` records with machine paths fail closed;
- hash-bound historical exceptions are acknowledged only while every ledger
  field and the target file remain exact.

The validator reports semantic invariant counts rather than pinning aggregate
finding totals or a full-tree path list. Historical/non-active plans and
decisions are outside its execution-entry boundary; changed coordination files
remain protected by practitioner-harness `coord-check`.

Raw reproduction stdout/stderr storage is independent of path portability.
The piping `.gitattributes` rules apply `-diff -merge -text` only to those
checksum-governed `.txt` artifacts. Authored text remains under ordinary Git
diff inspection.

## Candidate whitespace

`validate_candidate_whitespace.py` preserves `git diff --check` for staged,
unstaged, and optional committed-range changes. It also closes Git's untracked
file seam by scanning non-ignored, non-binary untracked text candidates for
trailing spaces/tabs and surplus terminal blank lines. It reports exact paths
and lines and never rewrites files.

```bash
python3 tools/validation/validate_candidate_whitespace.py
python3 tools/validation/validate_candidate_whitespace.py --base-ref origin/main
```

This is an optional local diagnostic, not a commit or merge gate. Cosmetic
whitespace does not block CI. `validate_conflict_markers.py --base <ref>`
retains Git's unresolved-conflict-marker protection without gating whitespace. The former versioned pre-commit hook has been
removed; clones configured with `core.hooksPath=.githooks` no longer invoke it.
No Git configuration change is required.

Root `.editorconfig` settings may trim trailing whitespace in compatible
editors. Preserve intentional Markdown hard breaks and raw evidence bytes;
formatting alone does not warrant an evidence-repair or approval cycle.

## Four-role and workflow validation

Run `python3 tools/validation/validate_agent_instructions.py --json` and
`python3 tools/validation/validate_workflow_metadata.py --json` for the current
Root contract. Agent runtime configuration lives in `agents/registry.json`;
workflow resources are optional and restrictions live in `execution.json`.
Explicit historical instruction snapshots and skill directories retain their
old reader contracts. Root G2/G3/G4 checks recognize `workflows/` as an
instruction surface alongside historical `skills/` inputs.
