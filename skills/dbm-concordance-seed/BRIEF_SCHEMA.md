# BRIEF SCHEMA — dbm-concordance-seed

This file defines the INIT-TASK dispatch contract for `TASK + dbm-concordance-seed`.

## Purpose

Use this skill when DBM_PUBLISHER needs a bounded reasoning pass over one approved section or one small approved section group to refine and augment typed concordance candidates before the blocking register is frozen.

## Scope model

- `ScopePath` should normally be the publication planning folder:
  - `{EXECUTION_ROOT}/_Publication/DBM/_Planning/`
- `AllowedWriteTargets` must name exactly two files:
  - one scope-local concordance candidate CSV,
  - one scope-local concordance seed QA markdown file.

The brief must not grant write access to section output folders, package folders, or any KTY-local source folder.

## Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why this seeding run exists | `Refine typed concordance candidates for SEC-03 before freezing the register.` |
| `ScopePath` | path | Publication planning folder | `/abs/root/_Publication/DBM/_Planning/` |
| `TaskSkill` | string | Must equal the skill folder/name | `dbm-concordance-seed` |
| `AllowedWriteTargets` | list[path] | Exact writable outputs | `[/.../concordance-seed/SEC-03_Candidates.csv, /.../concordance-seed/SEC-03_CONCORDANCE_SEED_QA.md]` |
| `RuntimeOverrides.CONCORDANCE_SCOPE_ID` | string | Stable identity for the seeding scope | `SEC-03` |
| `RuntimeOverrides.CONCORDANCE_SCOPE_MODE` | enum | Whether the run covers one section or a group | `SINGLE_SECTION` |
| `RuntimeOverrides.SECTION_IDS` | list[string] | Approved section IDs in scope | `[SEC-03]` |
| `RuntimeOverrides.CANDIDATE_INPUT_PATH` | path | Current candidate register to refine | `/.../_Planning/Publication_Concordance_Candidates.csv` |
| `RuntimeOverrides.CANDIDATE_OUTPUT_PATH` | path | Scope-local refined candidate output | `/.../_Planning/concordance-seed/SEC-03_Candidates.csv` |
| `RuntimeOverrides.SEED_QA_OUTPUT_PATH` | path | Scope-local QA output | `/.../_Planning/concordance-seed/SEC-03_CONCORDANCE_SEED_QA.md` |
| `RuntimeOverrides.PUBLICATION_INPUT_MANIFEST` | path | Frozen input manifest | `/.../_Planning/Publication_Input_Manifest.md` |
| `RuntimeOverrides.PUBLICATION_SCHEMA_PATH` | path | Approved publication schema | `/.../_Planning/Publication_Schema.md` |
| `RuntimeOverrides.SECTION_MAP_PATH` | path | Approved section map | `/.../_Planning/Section_Map.csv` |
| `RuntimeOverrides.PUBLICATION_RULES_PATH` | path | Approved publication rules | `/.../_Planning/Publication_Rules.md` |
| `RuntimeOverrides.MAX_KA_FILES_TOTAL` | integer | Hard cap on total mapped KAs for the scope | `20` |
| `ExpectedOutputs` | list[path] | Same two planning outputs | `[/.../SEC-03_Candidates.csv, /.../SEC-03_CONCORDANCE_SEED_QA.md]` |

## Optional brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `RuntimeOverrides.PUBLICATION_CONCORDANCE_REGISTER_PATH` | path | Existing frozen register to consult during reruns or expansion passes | `/.../_Planning/Publication_Concordance_Register.csv` |
| `RuntimeOverrides.SOURCE_DOMAIN` | string | Domain label for the run | `West_Doe_Deepcut_DBM` |
| `RuntimeOverrides.ALLOW_PROSE_ONLY_DISCOVERY` | boolean | Permit semantically grounded prose-only candidate additions | `true` |
| `RuntimeOverrides.STRICT_REQUIRED_SECTION_MATCH` | boolean | Refuse candidates that cannot be tied cleanly to the approved scope sections | `true` |
| `CustomInstructions` | string | Run-specific reinforcement only; must not restate the skill contract | `Be conservative about authority-section assignment for shared utility values.` |
| `EXCLUSIONS` | list[string] | Run-local exclusions inside already-mapped artifacts | `Ignore superseded historical value table under heading X.` |

## Runtime-override guidance

- `CONCORDANCE_SCOPE_MODE=SINGLE_SECTION` should normally be used unless DBM_PUBLISHER deliberately groups a small set of tightly coupled sections.
- `SECTION_IDS` must match approved section IDs present in `Section_Map.csv`.
- `CANDIDATE_OUTPUT_PATH` and `SEED_QA_OUTPUT_PATH` must both live under `_Publication/DBM/_Planning/`.
- `PUBLICATION_CONCORDANCE_REGISTER_PATH` is optional because the initial seed pass may run before the blocking register exists.
- `MAX_KA_FILES_TOTAL` should reflect the approved bounded-scope design, not an ad hoc worker preference.

## Recommended CustomInstructions content

Use `CustomInstructions` only for run-specific reinforcement such as:
- emphasis on a domain where concordance undercoverage is especially risky,
- reminder that a specific section should normally own authority for a family of values,
- reminder to prefer explicit ambiguity over premature key merging,
- reminder that prose-only discovery should remain conservative for a given pilot.

Do not use `CustomInstructions` to recreate the skill contract. TASK hydration already loads the authoritative contract from the skill folder.

## Example INIT-TASK brief

```md
PURPOSE: Refine typed concordance candidates for SEC-03 before freezing the register.
ScopePath: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/
TaskSkill: dbm-concordance-seed
AllowedWriteTargets:
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/concordance-seed/SEC-03_Candidates.csv
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/concordance-seed/SEC-03_CONCORDANCE_SEED_QA.md
RuntimeOverrides:
  CONCORDANCE_SCOPE_ID: SEC-03
  CONCORDANCE_SCOPE_MODE: SINGLE_SECTION
  SECTION_IDS:
    - SEC-03
  CANDIDATE_INPUT_PATH: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Concordance_Candidates.csv
  CANDIDATE_OUTPUT_PATH: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/concordance-seed/SEC-03_Candidates.csv
  SEED_QA_OUTPUT_PATH: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/concordance-seed/SEC-03_CONCORDANCE_SEED_QA.md
  PUBLICATION_INPUT_MANIFEST: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Input_Manifest.md
  PUBLICATION_SCHEMA_PATH: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Schema.md
  SECTION_MAP_PATH: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Section_Map.csv
  PUBLICATION_RULES_PATH: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Rules.md
  MAX_KA_FILES_TOTAL: 20
  ALLOW_PROSE_ONLY_DISCOVERY: true
ExpectedOutputs:
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/concordance-seed/SEC-03_Candidates.csv
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/concordance-seed/SEC-03_CONCORDANCE_SEED_QA.md
```
