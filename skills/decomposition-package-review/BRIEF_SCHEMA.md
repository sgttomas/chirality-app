# decomposition-package-review — Brief Schema

Use this skill with a generic TASK shell (no profile) like this:

```md
PURPOSE: Review the active DOMAIN decomposition package after a scope change.
RequestedBy: SCOPE_CHANGE

ScopePath: /abs/path/to/domain-root
TaskSkill: decomposition-package-review
AllowedWriteTargets:
  - /abs/path/to/domain-root/2_Checking/From/Decomposition_Package_Review.md
  - /abs/path/to/domain-root/2_Checking/From/Decomposition_Package_Findings.csv
  - /abs/path/to/domain-root/2_Checking/From/Decomposition_Package_Parity.csv

RuntimeOverrides:
  ROOT_PATH: /abs/path/to/domain-root
  DECOMPOSITION_ROOT: /abs/path/to/domain-root/_Decomposition
  SCOPE_CHANGE_ROOT: /abs/path/to/domain-root/_ScopeChange
  REVIEW_OUTPUT_PATH: /abs/path/to/domain-root/2_Checking/From/Decomposition_Package_Review.md
  FINDINGS_CSV_PATH: /abs/path/to/domain-root/2_Checking/From/Decomposition_Package_Findings.csv
  PARITY_MATRIX_PATH: /abs/path/to/domain-root/2_Checking/From/Decomposition_Package_Parity.csv
  MODE: REVIEW_ONLY
```

## Required fields

| Field | Value | Notes |
|---|---|---|
| `TaskSkill` | `decomposition-package-review` | Must match skill folder name |
| `ScopePath` | Absolute path to one DOMAIN root | Normally equals `ROOT_PATH` |
| `AllowedWriteTargets` | Report paths and any explicitly authorized package-local repair targets | Keep narrow |
| `RuntimeOverrides.ROOT_PATH` | Absolute path to the root under review | One root only |
| `RuntimeOverrides.DECOMPOSITION_ROOT` | Absolute path to `_Decomposition/` | Required |
| `RuntimeOverrides.SCOPE_CHANGE_ROOT` | Absolute path to `_ScopeChange/` | Required |
| `RuntimeOverrides.REVIEW_OUTPUT_PATH` | Markdown report path | Must be inside `AllowedWriteTargets` |
| `RuntimeOverrides.MODE` | Review or bounded repair mode | `REVIEW_ONLY` or `REVIEW_AND_REPAIR` |

## Optional fields

| Field | Default | Allowed values | Notes |
|---|---|---|---|
| `RuntimeOverrides.FINDINGS_CSV_PATH` | omitted | Absolute path | Optional structured findings log |
| `RuntimeOverrides.PARITY_MATRIX_PATH` | omitted | Absolute path | Optional parity matrix |
| `RuntimeOverrides.ACTIVE_SNAPSHOT_PATH` | autodetect via `_LATEST.md` | Absolute path | Use only when `_LATEST.md` should not decide |
| `RuntimeOverrides.MAX_FINDINGS` | `80` | Positive integer | Soft cap on findings |

## TaskProfile

`NONE` — this skill runs in generic TASK shell mode without a profile.

## Read boundary

The skill reads only:

- `{DECOMPOSITION_ROOT}/`
- `{SCOPE_CHANGE_ROOT}/_LATEST.md`
- the active `_ScopeChange/SCA-*` snapshot

Do not use this brief to authorize KTY-local, hypergraph, audit, or publication
reads.

## Write boundary

The skill always writes:

- `REVIEW_OUTPUT_PATH`
- optional `FINDINGS_CSV_PATH`
- optional `PARITY_MATRIX_PATH`

Only when `MODE = REVIEW_AND_REPAIR`, the brief may additionally authorize
explicit package-local repair targets under `_Decomposition/` or `_ScopeChange/`.

## Typical tasks

- verify that a `DOMAIN` root's active decomposition package is internally
  consistent after `SCOPE_CHANGE`
- verify active snapshot completeness and `_LATEST.md` parity
- separate package-local repair work from downstream reruns
- produce root-level closure evidence before Phase 7 / publication gating

## Notes

- One invocation reviews one DOMAIN root only.
- `REVIEW_ONLY` is the safe default.
- Use `kty-metadata-align` for KTY-local metadata drift; do not widen this
  review run into folder-local repair.
