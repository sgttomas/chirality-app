# kty-content-remediate - Brief Schema

Use this skill with a generic TASK shell (no profile) like this:

```md
PURPOSE: Retire active KTY content after accepted SCA disposition.
RequestedBy: SCOPE_CHANGE

ScopePath: /abs/path/to/CAT-003_Operations/1_Working/KTY-03-02_Onboarding-Checklist
TaskSkill: kty-content-remediate
AllowedWriteTargets:
  - /abs/path/to/CAT-003_Operations/1_Working/KTY-03-02_Onboarding-Checklist/.Archive/SCA-004_2026-04-21_1510/
  - /abs/path/to/CAT-003_Operations/1_Working/KTY-03-02_Onboarding-Checklist/Scoping.md
  - /abs/path/to/CAT-003_Operations/1_Working/KTY-03-02_Onboarding-Checklist/KA-01_Guidance__Example.md
  - /abs/path/to/domain-root/_ScopeChange/SCA-004_2026-04-21_1510/Evidence/KTY-03-02_Content_Remediation.md
  - /abs/path/to/domain-root/_ScopeChange/SCA-004_2026-04-21_1510/Evidence/KTY-03-02_Content_Disposition.csv

RuntimeOverrides:
  KTY_PATH: /abs/path/to/CAT-003_Operations/1_Working/KTY-03-02_Onboarding-Checklist
  MODE: RETIRE_KTY
  DECOMPOSITION_REF: /abs/path/to/domain-root/_Decomposition
  SCA_SNAPSHOT_PATH: /abs/path/to/domain-root/_ScopeChange/SCA-004_2026-04-21_1510
  AMENDMENT_ID: SCA-004
  SUPERSESSION_MAP_PATH: /abs/path/to/domain-root/_ScopeChange/SCA-004_2026-04-21_1510/Supersession_Map.csv
  SOURCE_ACTION_REF: D-003
  ENTITY_TYPE: KNOWLEDGE_TYPE
  ENTITY_ID: KTY-03-02_Onboarding-Checklist
  AFFECTED_SUBJECTS: "SUB-03-02-01_Example"
  AFFECTED_HBK: "HBK-0123"
  CANONICAL_ROOT_NAME: Example_Domain_Root
  FACILITY_ID: 03-25
  REVIEW_OUTPUT_PATH: /abs/path/to/domain-root/_ScopeChange/SCA-004_2026-04-21_1510/Evidence/KTY-03-02_Content_Remediation.md
  DISPOSITION_EVIDENCE_PATH: /abs/path/to/domain-root/_ScopeChange/SCA-004_2026-04-21_1510/Evidence/KTY-03-02_Content_Disposition.csv
  ARCHIVE_RUN_ID: SCA-004_2026-04-21_1510
  EXPECTED_DISPOSITION: ARCHIVE_AND_STUB
```

## Required fields

| Field | Value | Notes |
|---|---|---|
| `TaskSkill` | `kty-content-remediate` | Must match skill folder name |
| `ScopePath` | Absolute path to one KTY folder | Normally equals `KTY_PATH` |
| `AllowedWriteTargets` | Archive path, tombstone paths for `RETIRE_KTY`, and evidence output paths | Keep single-KTY and snapshot-local |
| `RuntimeOverrides.KTY_PATH` | Absolute path to one KTY folder | Required |
| `RuntimeOverrides.MODE` | `RETIRE_KTY`, `VERIFY_KTY`, or `EMIT_DISPOSITION` | Required |
| `RuntimeOverrides.DECOMPOSITION_REF` | Admitted decomposition authority | Required |
| `RuntimeOverrides.SCA_SNAPSHOT_PATH` | Accepted SCOPE_CHANGE snapshot | Required |
| `RuntimeOverrides.AMENDMENT_ID` | `SCA-{NNN}` | Required |
| `RuntimeOverrides.REVIEW_OUTPUT_PATH` | Markdown evidence report | Required |

## Required for factual checks

| Field | Value | Notes |
|---|---|---|
| `RuntimeOverrides.SUPERSESSION_MAP_PATH` | Path to accepted `Supersession_Map.csv` | Required when checking current factual validity |
| `RuntimeOverrides.SOURCE_ACTION_REF` | Amendment action or decision id | Required when emitting disposition evidence |

Do not infer supersessions from SCA prose. Structured SCA artifacts and
`Supersession_Map.csv` are the authority basis.

## Optional fields

| Field | Default | Allowed values | Notes |
|---|---|---|---|
| `RuntimeOverrides.DISPOSITION_EVIDENCE_PATH` | omitted | Absolute path | Optional structured evidence CSV |
| `RuntimeOverrides.ENTITY_TYPE` | omitted | Known manifest entity type | Triggering entity type for SCOPE_CHANGE evidence |
| `RuntimeOverrides.ENTITY_ID` | omitted | Stable id or term string | Triggering entity id |
| `RuntimeOverrides.AFFECTED_SUBJECTS` | omitted | Semicolon-separated `SUB-*` ids | Subject-level traceability |
| `RuntimeOverrides.AFFECTED_HBK` | omitted | Semicolon-separated `HBK-*` ids | Handbook-unit traceability |
| `RuntimeOverrides.CANONICAL_ROOT_NAME` | omitted | Canonical root token | Multi-root disambiguation |
| `RuntimeOverrides.FACILITY_ID` | omitted | Facility id or blank | Facility-scope disambiguation |
| `RuntimeOverrides.ARCHIVE_RUN_ID` | `{AMENDMENT_ID}_{timestamp}` | Filesystem-safe token | Archive subfolder name |
| `RuntimeOverrides.EXPECTED_DISPOSITION` | `UNKNOWN` | `ARCHIVE_AND_STUB`, `VERIFY_ONLY`, `NO_ACTION`, `UNKNOWN` | Used to detect mismatched dispatch |
| `RuntimeOverrides.MAX_FILES` | `100` | Positive integer | Soft cap on `KA-*.md` inspection |

## TaskProfile

`NONE` - this skill runs in generic TASK shell mode without a profile.

## Mode write rules

| Mode | Write behavior |
|---|---|
| `RETIRE_KTY` | May write `.Archive/{ARCHIVE_RUN_ID}/`, tombstone stubs at original `Scoping.md` / `KA-*.md` paths, and evidence outputs. |
| `VERIFY_KTY` | May write only evidence outputs. |
| `EMIT_DISPOSITION` | May write only evidence outputs. |

## Read boundary

The skill reads:

- root-level `{KTY_PATH}/Scoping.md`
- root-level `{KTY_PATH}/KA-*.md`
- `{KTY_PATH}/.Archive/` only for archive-collision and prior-evidence checks
- `DECOMPOSITION_REF`
- `SCA_SNAPSHOT_PATH`
- `SUPERSESSION_MAP_PATH`

It must not scan sibling KTY folders. `.Archive/` is excluded from current
content enumeration.

## Write boundary

The skill may write only:

- `{KTY_PATH}/.Archive/{ARCHIVE_RUN_ID}/...`
- original `{KTY_PATH}/Scoping.md` and `{KTY_PATH}/KA-*.md` tombstone stubs in
  `RETIRE_KTY`
- `REVIEW_OUTPUT_PATH`
- optional `DISPOSITION_EVIDENCE_PATH`

It must not write active factual KTY content, metadata files, decomposition
files, SCOPE_CHANGE manifests, or publication outputs.

## Typical tasks

- retire a KTY's current active content after its scope is removed or replaced
- verify that current KTY content agrees with admitted SCA/decomposition truth
- emit disposition evidence for `KTY_Remediation_Manifest.csv`

## Notes

- SCOPE_CHANGE owns manifest updates; this skill emits evidence only.
- `domain-documents` owns active content regeneration.
- `.Archive/` scanner exclusion must be preserved by every consumer.
