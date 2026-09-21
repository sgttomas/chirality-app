# Deterministic evaluation tools

Run commands using the declared tool root. Input workspaces are read-only; only
explicit report destinations are written. Commands work independently of the
current working directory. Report paths must be outside production-unit source
paths. These commands perform mechanical checks; the invoking workflow interprets
their findings and owns acceptance.

## Dependency registers

```sh
python3 "$INSTRUCTION_ROOT/tools/evaluation/audit_dependencies.py" --root "$EXECUTION_ROOT" --output "$REPORT_DIR/dependencies.json"
```

The inventory contains every live PKG/DEL and CAT/KTY unit plus additional
`Dependencies.csv` files under `1_Working`, excluding `_Archive`. Missing
registers on discovered units are explicit findings. Exact required column names,
versions, all canonical enums and row semantics come from
`tools/validation/validate_dependencies_schema.py`. Extension columns remain
supported. Duplicate/empty headers and malformed row widths fail conformance.
Python's strict CSV reader handles quoted commas and multiline cells. Anchors
require both `DependencyClass=ANCHOR` and `AnchorType=IMPLEMENTS_NODE`; text in
another cell never counts as an anchor.

JSON v1 has `root`, `run_status`, `subject_status`, `issues`, `summary`, and
`files`. Each file records its path/hash, columns/extensions, schema validity,
logical record counts, readable/malformed record counts, enum valid/invalid
counts, row findings with logical record and physical ending line, anchor
counts, and evidence population. Evidence population checks cell presence; it
does not establish that the cited file resolves or that its contents warrant a
claim. Malformed-width records remain in the evidence denominator and contribute
no positive coverage. Header-invalid records are unassessable. Empty data yields
a null percentage. A CSV parse/read error marks `denominator_complete=false`;
preceding records remain visible and percentage is null rather than a misleading
complete rate. `schema_valid` describes schema/row checks separately from anchor
and evidence findings.

## Workspace structure

```sh
python3 "$INSTRUCTION_ROOT/tools/evaluation/audit_structure.py" --root "$EXECUTION_ROOT" --variant SOFTWARE --output "$REPORT_DIR/structure.json"
```

`--variant` is required: PROJECT and SOFTWARE discover immediate live
`PKG-*/1_Working/DEL-*` units; DOMAIN discovers `CAT-*/1_Working/KTY-*`. To audit an
accepted list, including missing units, supply `--inventory inventory.json`:

```json
{"schema_version":1,"units":[{"path":"PKG-01_Example/1_Working/DEL-01-01_Result","required_files":["Result.md"]}]}
```

Paths resolve within the execution root. Each unit is unique. `required_files`
extends the four required metadata files; DOMAIN content expectations use this
field because the PROJECT/SOFTWARE SOW transition does not define KTY content.
The selected inventory and actual materialized directories are different facts;
use a decomposition audit for full forward/reverse declaration reconciliation.

JSON v1 includes `variant`, `contract`, `inventory_source`, `units`, `partitions`,
`tool_roots`, `summary`, and `issues`, alongside common status fields. Unit rows
include presence by filename, current lifecycle state, format resolution, and
specific violations. Current State is parsed as an explicit Markdown/plain-text
field; explicit historical `State:` syntax is a compatibility input. Ambiguous
multiple current fields fail. Historical narrative state words are ignored.
RETIRED is recognized; retired units remain in the census without requiring
active production content. OPEN units may lack production content; initialized
and later active states require a valid production format. Any present partial
or invalid format is reported even for OPEN/RETIRED units.

PROJECT/SOFTWARE format uses the canonical SOW resolver and reports `SOW_V1`,
`LEGACY_FOUR_DOC`, `MIGRATION_DUAL`, `AMBIGUOUS`, or `INVALID` with its detailed
findings. `--isolated-migration --migration-authority <exact-authority>` passes
through to that resolver; authorized dual content has `accepted_baseline=false`.
DOMAIN format is `NOT_APPLICABLE`, with its declared content checked separately.
The report names `structure-audit/v1` and its SPEC basis for required partition
and tool directories; an audit result is limited to those checks.

## Status and shell compatibility

Both audit CLIs accept `--output -` for JSON on stdout. A completed observation
has `run_status=COMPLETE` and exits 0 even when `subject_status=FAIL`. Bad invocation
or unavailable audit input/output exits 2. A valid empty scope is
`NOT_ASSESSED`, not evidence of subject conformity. Callers must inspect both
statuses and findings. Invalid subject CSV contents are successful observations
of defects, not failed audit execution.

The historical `check_dependency_schema.sh`, `check_implements_node.sh`, and
`check_evidence_coverage.sh` entrypoints accept their original positional root
and now return the complete dependency JSON report. `count_deliverable_files.sh`
and `extract_lifecycle_states.sh` return the SOFTWARE structure JSON report;
the former retains its migration flags. Consumers requiring another variant use
the explicit Python CLI. The old human-readable line formats are superseded.

## Dependency closure

```sh
python3 "$INSTRUCTION_ROOT/tools/coordination/analyze_dep_closure.py" "$EXECUTION_ROOT" --output-dir "$REPORT_DIR/closure" --scope ALL --filter-active-only true --normalize-ids true --hub-threshold 20 --max-cycles 10000
```

The historical positional root and optional output directory remain supported.
Brief fields bind as follows:

| Brief field | CLI |
|---|---|
| SCOPE | `--scope ALL`, IDs, package IDs, or unit/package/register paths |
| FILTER_ACTIVE_ONLY | `--filter-active-only true` or `false` |
| NORMALIZE_IDS | `--normalize-ids true` or `false` |
| EDGE_FILTER.DependencyClass | `--dependency-class EXECUTION` or `ANCHOR` |
| EDGE_FILTER.TargetType | `--target-type DELIVERABLE`; other target classes have no production-unit graph and are rejected |
| HUB_THRESHOLD | `--hub-threshold <positive integer>` |
| MAX_CYCLES | `--max-cycles <nonnegative integer>` |
| PRIOR_RUN_LABEL | Owner resolves the accepted label to an explicit `--prior-summary <closure_summary.json>` |

Normalization strips descriptive suffixes from DEL/KTY/PKG/CAT IDs for analysis
only. Source text stays unchanged. Direction remains dependent-to-prerequisite:
UPSTREAM uses From→Target; DOWNSTREAM reverses it. Header-invalid/unreadable files
and malformed or semantically invalid rows supply no topology. Other valid rows
remain analyzable and exclusion findings stay visible. Invalid direction is an
explicit schema finding, not an invented edge. The inventory includes units
without registers. Scope is the set of source units; referenced targets outside
scope remain graph endpoints and are distinguished from targets missing from the
entire workspace.

`closure_summary.json` is schema v2, with COMPLETE/FAILED_INPUTS and
PASS/FAIL/NOT_ASSESSED distinctions; completed observation exits 0. Missing
registers, invalid schema, missing source/target units, and SCCs produce subject
FAIL. Missing anchors, isolated units, hubs and bidirectional pairs are reported
signals for workflow interpretation. Empty graphs never imply accepted closure.

Outputs include `coverage.csv`, `scc_summary.csv`, `cycles_sample.csv`, `hubs.csv`,
`bidirectional_pairs.csv`, and `id_normalization.csv`. One deterministic cycle
representative is produced per SCC up to MAX_CYCLES, including self-loops; this
is a bounded representative set, not an enumeration of every simple cycle.

The corrected `orphans.csv` contains unresolved target references with source,
target, dependency ID, file, record and status. `isolated.csv` now carries the
zero-edge unit list formerly mislabeled as orphans. `outside_scope.csv` carries
resolved workspace targets outside the selected scope. Accordingly
`orphan_count` means unresolved target records and `isolated_count` means
zero-edge units. Historical summaries keep their old meaning; comparisons omit
the incompatible orphan metric. The legacy Python `find_orphans` function is
retained as an explicitly documented isolated-unit adapter.
