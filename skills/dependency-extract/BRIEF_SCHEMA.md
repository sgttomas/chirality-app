# dependency-extract — Brief Schema

This skill is dispatched by ORCHESTRATOR (or other personas) via TASK with `TaskSkill: dependency-extract`. The following fields describe the brief expected by a single invocation.

## Required

- `SCOPE` — the deliverable(s) / package(s) / all-deliverables-under-run-root selector that defines what this extraction run processes. The skill walks each in-scope deliverable folder and produces one register per deliverable.

## Optional — run-root + decomposition

- `RUN_ROOT` — path to the run workspace (may be implied by invoker context).
- `DECOMPOSITION_PATH` — explicit path to the latest decomposition markdown. When omitted, the skill auto-discovers under `{RUN_ROOT}/_Decomposition/`. When no decomposition can be located, the run proceeds with a `[WARNING] MISSING_DECOMPOSITION` entry in Run Notes (validation/label resolution is marked degraded, not failed).

## Optional — source-document selection

- `SOURCE_DOCS` — `AUTO` (default) or explicit list of filenames/paths to scan per deliverable.
- `DOC_ROLE_MAP` — `DEFAULT` (default) or explicit mapping of doc roles (`ANCHOR_DOC` / `EXECUTION_DOCS`) to filename patterns.
- `ANCHOR_DOC` — `AUTO` (default) or explicit filename/path. Controls Pass 1 (Vertical / Tree anchoring).
- `EXECUTION_DOC_ORDER` — `AUTO` (default) or ordered list of filenames/paths. Controls Pass 2 (Horizontal / DAG execution-edge extraction).

## Optional — run controls

- `MODE` — `UPDATE` (default) or `RESET_EXTRACTED`.
- `STRICTNESS` — `CONSERVATIVE` (default) or `AGGRESSIVE`. `AGGRESSIVE` permits strongly-implied anchors marked `ASSUMPTION` with `Confidence=LOW`.
- `CONSUMER_CONTEXT` — `NONE` (default) | `TASK_ESTIMATING` | `AGGREGATION` | `RECONCILIATION`. When set to a non-`NONE` value, the skill adds a `## Downstream Handoff Notes` section and (for `TASK_ESTIMATING`) attempts to populate `ConsumerHint` and `EstimateImpactClass` extension columns.

## Deliverable-local read-only inputs (if present)

- `_REFERENCES.md` — used to resolve document pointers for `TargetType=DOCUMENT` rows.
- `Dependencies.csv` — existing register used for match/merge and preserving declared edges (`Origin=DECLARED`).
- `_DEPENDENCIES.md` — existing index used to preserve declared lists and append Run History.

## Example brief

```yaml
TaskSkill: dependency-extract
SCOPE: DEL-001
RUN_ROOT: /abs/path/to/run
DECOMPOSITION_PATH: /abs/path/to/run/_Decomposition/latest.md
MODE: UPDATE
STRICTNESS: CONSERVATIVE
CONSUMER_CONTEXT: NONE
```

## Output

Per in-scope deliverable:
- `{deliverable}/Dependencies.csv` (v3.1 schema, 29 required columns)
- `{deliverable}/_DEPENDENCIES.md` (declared lists + extracted summary + run notes + run history + lifecycle summary)

## Defaults are recorded

All defaults applied at runtime and all chosen paths (decomposition, anchor doc, execution doc order) MUST be recorded in `_DEPENDENCIES.md` Run Notes for auditability.
