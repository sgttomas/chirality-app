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
diff and whitespace validation.
