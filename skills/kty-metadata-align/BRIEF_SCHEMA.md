# kty-metadata-align — Brief Schema

Use this skill with a generic TASK shell (no profile) like this:

```md
PURPOSE: Align one KTY's metadata after DOMAIN regeneration.
RequestedBy: ORCHESTRATOR

ScopePath: /abs/path/to/CAT-003_Operations/1_Working/KTY-03-02_Onboarding-Checklist
TaskSkill: kty-metadata-align
AllowedWriteTargets:
  - /abs/path/to/CAT-003_Operations/1_Working/KTY-03-02_Onboarding-Checklist/_CONTEXT.md
  - /abs/path/to/CAT-003_Operations/1_Working/KTY-03-02_Onboarding-Checklist/_STATUS.md
  - /abs/path/to/CAT-003_Operations/1_Working/KTY-03-02_Onboarding-Checklist/_REFERENCES.md
  - /abs/path/to/CAT-003_Operations/1_Working/KTY-03-02_Onboarding-Checklist/2_Checking/From/KTY_Metadata_Alignment.md

RuntimeOverrides:
  KTY_PATH: /abs/path/to/CAT-003_Operations/1_Working/KTY-03-02_Onboarding-Checklist
  DECOMPOSITION_REF: /abs/path/to/_Decomposition
  SOURCES_ROOT: /abs/path/to/_Sources
  REVIEW_OUTPUT_PATH: /abs/path/to/CAT-003_Operations/1_Working/KTY-03-02_Onboarding-Checklist/2_Checking/From/KTY_Metadata_Alignment.md
  MODE: ALIGN_METADATA
  REWRITE_REFERENCES: true
  ALLOW_STATUS_APPEND: true
```

## Required fields

| Field | Value | Notes |
|---|---|---|
| `TaskSkill` | `kty-metadata-align` | Must match skill folder name |
| `ScopePath` | Absolute path to one `KTY-*` folder | Normally equals `KTY_PATH` |
| `AllowedWriteTargets` | Narrow list of metadata files and optional report path | Single-KTY scope only |
| `RuntimeOverrides.KTY_PATH` | Absolute path to one KTY folder | Required |
| `RuntimeOverrides.DECOMPOSITION_REF` | Decomposition truth source | Required |
| `RuntimeOverrides.MODE` | Review or metadata-alignment mode | `REPORT_ONLY` or `ALIGN_METADATA` |

## Optional fields

| Field | Default | Allowed values | Notes |
|---|---|---|---|
| `RuntimeOverrides.SOURCES_ROOT` | omitted | Absolute path | Used only to resolve authoritative source pointers |
| `RuntimeOverrides.REVIEW_OUTPUT_PATH` | omitted | Absolute path | Optional report output |
| `RuntimeOverrides.REWRITE_REFERENCES` | `true` | `true`, `false` | Set `false` to leave `_REFERENCES.md` untouched |
| `RuntimeOverrides.ALLOW_STATUS_APPEND` | `true` | `true`, `false` | Set `false` when `_STATUS.md` must remain read-only |
| `RuntimeOverrides.AUTHORITATIVE_STATUS_STATE` | omitted | Known lifecycle token | Use when the caller owns the lifecycle transition |

## TaskProfile

`NONE` — this skill runs in generic TASK shell mode without a profile.

## Read boundary

The skill reads:

- `{KTY_PATH}/_CONTEXT.md`
- `{KTY_PATH}/_STATUS.md`
- `{KTY_PATH}/_REFERENCES.md`
- optional `Scoping.md` / `KA-*.md` for drift observation only
- decomposition material under `{DECOMPOSITION_REF}`
- source pointer paths under `{SOURCES_ROOT}` only when needed

## Write boundary

The skill may write only:

- `{KTY_PATH}/_CONTEXT.md`
- `{KTY_PATH}/_STATUS.md`
- `{KTY_PATH}/_REFERENCES.md`
- optional `REVIEW_OUTPUT_PATH`

It must not write `Scoping.md`, `KA-*.md`, or any decomposition file.

## Typical tasks

- align `_CONTEXT.md` after a KTY rename, category move, or scope change
- append a lifecycle correction to `_STATUS.md` when the invoking workflow owns
  the authoritative state
- refresh `_REFERENCES.md` after decomposition or source-pointer changes
- classify remaining stale `Scoping.md` / `KA-*` files as rerun work

## Notes

- This skill is metadata-only by design.
- `REPORT_ONLY` is safe for audit follow-up.
- Use `domain-documents` for content regeneration, not this skill.
