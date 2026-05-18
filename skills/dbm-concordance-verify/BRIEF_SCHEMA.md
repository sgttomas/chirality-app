# BRIEF SCHEMA - dbm-concordance-verify

This file defines the INIT-TASK dispatch contract for `TASK + dbm-concordance-verify`.

## Purpose

Use this skill after deterministic package concordance and source-supersession checks have produced findings, but before DBM_PUBLISHER accepts package readiness.

## Scope model

- `ScopePath` should be the immutable package snapshot directory.
- `AllowedWriteTargets` must name exactly:
  - `Publication_Concordance_Verification.md`
  - `Publication_Concordance_Verification_Findings.csv`

The brief must not grant write access to section folders, planning artifacts, KTY folders, or source authority files.

## Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why verification is being run | `Verify semantic concordance before package readiness.` |
| `ScopePath` | path | Package snapshot directory | `/abs/root/_Publication/DBM/package/RUN-20260421-120000/` |
| `TaskSkill` | string | Must equal this skill name | `dbm-concordance-verify` |
| `AllowedWriteTargets` | list[path] | Exact verification outputs | `[/.../Publication_Concordance_Verification.md, /.../Publication_Concordance_Verification_Findings.csv]` |
| `RuntimeOverrides.SECTIONS_ROOT` | path | Current section outputs root | `/.../_Publication/DBM/sections/` |
| `RuntimeOverrides.CONCORDANCE_REGISTER_PATH` | path | Frozen register | `/.../_Planning/Publication_Concordance_Register.csv` |
| `RuntimeOverrides.CONCORDANCE_FINDINGS_PATH` | path | Deterministic concordance findings | `/.../Publication_Concordance_Findings.csv` |
| `RuntimeOverrides.OUTPUT_VERIFICATION_PATH` | path | Markdown verification output | `/.../Publication_Concordance_Verification.md` |
| `RuntimeOverrides.OUTPUT_VERIFICATION_FINDINGS_PATH` | path | CSV verification findings output | `/.../Publication_Concordance_Verification_Findings.csv` |
| `ExpectedOutputs` | list[path] | Same two verification outputs | `[/.../Publication_Concordance_Verification.md, /.../Publication_Concordance_Verification_Findings.csv]` |

## Optional brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `RuntimeOverrides.SOURCE_SUPERSESSION_FINDINGS_PATH` | path | Source-supersession findings when validation ran | `/.../Source_Supersession_Findings.csv` |
| `RuntimeOverrides.PUBLICATION_RULES_PATH` | path | Approved publication rules | `/.../_Planning/Publication_Rules.md` |
| `RuntimeOverrides.PUBLICATION_INPUT_MANIFEST` | path | Frozen manifest | `/.../_Planning/Publication_Input_Manifest.md` |
| `RuntimeOverrides.PACKAGE_SNAPSHOT_PATH` | path | Package snapshot root | `/.../_Publication/DBM/package/RUN-20260421-120000/` |
| `CustomInstructions` | string | Run-specific emphasis only | `Pay special attention to shared utility values.` |

## Runtime-override guidance

- `SECTIONS_ROOT` must contain complete current section bundles.
- The skill reads synthesized section outputs only. It must not be asked to inspect raw KTY-local source files.
- `SOURCE_SUPERSESSION_FINDINGS_PATH` should be provided whenever `validate_source_supersession.py` ran.

## Example INIT-TASK brief

```md
PURPOSE: Verify semantic concordance before final DBM readiness.
ScopePath: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260421-120000/
TaskSkill: dbm-concordance-verify
AllowedWriteTargets:
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260421-120000/Publication_Concordance_Verification.md
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260421-120000/Publication_Concordance_Verification_Findings.csv
RuntimeOverrides:
  SECTIONS_ROOT: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/
  CONCORDANCE_REGISTER_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Concordance_Register.csv
  CONCORDANCE_FINDINGS_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260421-120000/Publication_Concordance_Findings.csv
  OUTPUT_VERIFICATION_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260421-120000/Publication_Concordance_Verification.md
  OUTPUT_VERIFICATION_FINDINGS_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260421-120000/Publication_Concordance_Verification_Findings.csv
ExpectedOutputs:
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260421-120000/Publication_Concordance_Verification.md
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260421-120000/Publication_Concordance_Verification_Findings.csv
```
