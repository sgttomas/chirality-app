# BRIEF SCHEMA — dbm-publish

This file defines the INIT-TASK dispatch contract for `TASK + dbm-publish`.

## Purpose

Use this skill after approved section outputs exist and DBM_PUBLISHER wants the package-level assembly, deterministic QA/concordance checks, and qualitative publication-readiness judgment.

## Scope model

- `ScopePath` should normally be the publication root or package root:
  - `{EXECUTION_ROOT}/_Publication/DBM/`
  - or `{EXECUTION_ROOT}/_Publication/DBM/package/`
- `AllowedWriteTargets` must remain inside the package snapshot subtree plus the package-level readiness artifacts for the current run.

The brief must not grant write access to KTY folders, decomposition truth, or unrelated tool roots.

## Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why the package run exists | `Assemble the rewritten DBM and classify publication readiness.` |
| `ScopePath` | path | Publication root or package root | `/abs/root/_Publication/DBM/` |
| `TaskSkill` | string | Must equal the skill folder/name | `dbm-publish` |
| `AllowedWriteTargets` | list[path/glob] | Package snapshot subtree and review outputs for the current run | `[/.../package/RUN-20260418-120000/*]` |
| `RuntimeOverrides.PUBLICATION_ROOT` | path | Publication tool root | `/.../_Publication/DBM/` |
| `RuntimeOverrides.PUBLICATION_INPUT_MANIFEST` | path | Frozen input manifest | `/.../_Planning/Publication_Input_Manifest.md` |
| `RuntimeOverrides.PUBLICATION_SCHEMA_PATH` | path | Approved publication schema | `/.../_Planning/Publication_Schema.md` |
| `RuntimeOverrides.SECTION_MAP_PATH` | path | Approved section map | `/.../_Planning/Section_Map.csv` |
| `RuntimeOverrides.PUBLICATION_RULES_PATH` | path | Approved publication rules | `/.../_Planning/Publication_Rules.md` |
| `RuntimeOverrides.PUBLICATION_CONCORDANCE_REGISTER_PATH` | path | Approved concordance register | `/.../_Planning/Publication_Concordance_Register.csv` |
| `RuntimeOverrides.SECTIONS_ROOT` | path | Current section output root | `/.../_Publication/DBM/sections/` |
| `RuntimeOverrides.PACKAGE_OUTPUT_ROOT` | path | Package snapshot root | `/.../_Publication/DBM/package/` |
| `ExpectedOutputs` | list[path] | Package outputs expected from the run | `[/.../Rewritten_DBM.md, /.../Publication_Readiness.md, ...]` |

## Optional brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `RuntimeOverrides.RUN_LABEL` | string | Human-friendly run label | `pilot-deepcut-round-1` |
| `RuntimeOverrides.SOURCE_DOMAIN` | string | Domain label for reporting | `West_Doe_Deepcut_DBM` |
| `CustomInstructions` | string | Run-specific emphasis only; must not restate the skill contract | `Be strict about sections that still read like stitched excerpts.` |

## Runtime-override guidance

- `PACKAGE_OUTPUT_ROOT` should be the immutable snapshot parent, not a mutable working directory.
- `AllowedWriteTargets` should constrain the run to the intended snapshot subtree and package-level readiness artifacts.
- The skill should always run against the latest complete current section set, not only against the rerun subset.

## Recommended CustomInstructions content

Use `CustomInstructions` only for run-specific reinforcement such as:
- a request to be especially strict about readability,
- a reminder that a known quality issue should remain non-blocking for this pilot,
- a reminder to emphasize terminology consistency or amendment-note discipline.

Do not use `CustomInstructions` to recreate deterministic tool contracts or the skill contract.

## Example INIT-TASK brief

```md
PURPOSE: Assemble the rewritten DBM and classify publication readiness.
ScopePath: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/
TaskSkill: dbm-publish
AllowedWriteTargets:
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/*
RuntimeOverrides:
  PUBLICATION_ROOT: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/
  PUBLICATION_INPUT_MANIFEST: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Input_Manifest.md
  PUBLICATION_SCHEMA_PATH: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Schema.md
  SECTION_MAP_PATH: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Section_Map.csv
  PUBLICATION_RULES_PATH: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Rules.md
  PUBLICATION_CONCORDANCE_REGISTER_PATH: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Concordance_Register.csv
  SECTIONS_ROOT: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/
  PACKAGE_OUTPUT_ROOT: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/
  RUN_LABEL: pilot-deepcut-round-1
ExpectedOutputs:
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/Rewritten_DBM.md
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/Trace_Appendix.md
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/Publication_Manifest.md
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/Publication_QA.md
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/Publication_Concordance_Report.md
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/Publication_Concordance_Findings.csv
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/Publication_Readiness.md
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/Rerun_Recommendations.csv
```
