# BRIEF SCHEMA — dbm-section-publish

This file defines the INIT-TASK dispatch contract for `TASK + dbm-section-publish`.

## Purpose

Use this skill when DBM_PUBLISHER needs one approved DBM section synthesized from the frozen publication planning artifacts and the exact mapped KTY-local inputs for that section.

## Scope model

- `ScopePath` should normally be the section-local publication folder:
  - `{EXECUTION_ROOT}/_Publication/DBM/sections/{SECTION_ID}/`
- `AllowedWriteTargets` must name exactly four files:
  - section body markdown,
  - section QA markdown,
  - section assertions CSV,
  - section assertion-discovery CSV.

The brief must not grant broader publication-root or KTY-folder write access.

## Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why this section run exists | `Publish approved rewritten DBM section SEC-03.` |
| `ScopePath` | path | Section-local publication folder | `/abs/root/_Publication/DBM/sections/SEC-03/` |
| `TaskSkill` | string | Must equal the skill folder/name | `dbm-section-publish` |
| `AllowedWriteTargets` | list[path] | Exact writable outputs | `[/.../SEC-03.md, /.../SEC-03_QA.md, /.../SEC-03_ASSERTIONS.csv, /.../SEC-03_ASSERTION_DISCOVERY.csv]` |
| `RuntimeOverrides.SECTION_ID` | string | Stable section identity | `SEC-03` |
| `RuntimeOverrides.SECTION_TITLE` | string | Approved section title | `Deep Cut Process Basis` |
| `RuntimeOverrides.SECTION_TYPE` | enum | Approved section taxonomy | `PROCESS_BASIS` |
| `RuntimeOverrides.SECTION_PURPOSE` | string | Human-approved section intent | `Explain current deep cut process basis and interfaces.` |
| `RuntimeOverrides.SECTION_OUTPUT_PATH` | path | Section body output | `/.../SEC-03.md` |
| `RuntimeOverrides.SECTION_QA_OUTPUT_PATH` | path | QA output | `/.../SEC-03_QA.md` |
| `RuntimeOverrides.SECTION_ASSERTIONS_OUTPUT_PATH` | path | Assertions output | `/.../SEC-03_ASSERTIONS.csv` |
| `RuntimeOverrides.SECTION_ASSERTION_DISCOVERY_OUTPUT_PATH` | path | Assertion-discovery output | `/.../SEC-03_ASSERTION_DISCOVERY.csv` |
| `RuntimeOverrides.PUBLICATION_INPUT_MANIFEST` | path | Frozen input manifest | `/.../_Planning/Publication_Input_Manifest.md` |
| `RuntimeOverrides.PUBLICATION_SCHEMA_PATH` | path | Approved publication schema | `/.../_Planning/Publication_Schema.md` |
| `RuntimeOverrides.SECTION_MAP_PATH` | path | Approved section map | `/.../_Planning/Section_Map.csv` |
| `RuntimeOverrides.PUBLICATION_RULES_PATH` | path | Approved publication rules | `/.../_Planning/Publication_Rules.md` |
| `RuntimeOverrides.PUBLICATION_CONCORDANCE_REGISTER_PATH` | path | Approved concordance register | `/.../_Planning/Publication_Concordance_Register.csv` |
| `RuntimeOverrides.MAX_KA_FILES` | integer | Hard cap on mapped KA files | `12` |
| `ExpectedOutputs` | list[path] | Same four section outputs | `[/.../SEC-03.md, /.../SEC-03_QA.md, /.../SEC-03_ASSERTIONS.csv, /.../SEC-03_ASSERTION_DISCOVERY.csv]` |

## Optional brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `RuntimeOverrides.SOURCE_DOMAIN` | string | Domain label for the run | `West_Doe_Deepcut_DBM` |
| `RuntimeOverrides.SECTION_ORDER` | integer | Display/assembly order | `3` |
| `RuntimeOverrides.ALLOW_CONTEXT_ONLY_DECOMP_FALLBACK` | boolean | Allow decomposition fallback for unready `CONTEXT_ONLY` inputs | `true` |
| `CustomInstructions` | string | Run-specific reinforcement only; must not restate the skill contract | `Keep amendment notes especially brief in this run.` |
| `EXCLUSIONS` | list[string] | Extra run-local exclusions inside already-mapped artifacts | `Ignore superseded historical table under heading X.` |

## Runtime-override guidance

- `SECTION_TYPE` must match the approved section taxonomy in `Publication_Schema.md`.
- `SECTION_OUTPUT_PATH`, `SECTION_QA_OUTPUT_PATH`, `SECTION_ASSERTIONS_OUTPUT_PATH`, and `SECTION_ASSERTION_DISCOVERY_OUTPUT_PATH` must all live inside `ScopePath`.
- `MAX_KA_FILES` should match the approved section design, not an ad hoc worker preference.
- The section worker should receive only the planning artifacts and mapped inputs already frozen for the run.
- The section worker is expected to read the concordance register and emit both required-key rows and discovery candidates.

## Recommended CustomInstructions content

Use `CustomInstructions` only for run-specific reinforcement such as:
- emphasis on a particular readability concern,
- reminder that a specific mapped artifact is context-only,
- reminder that a section is near its size limit,
- reminder that an authority section should use `ASSERTED` while the rest should prefer `REFERRED` for a given assertion.

Do not use `CustomInstructions` to recreate the skill contract. TASK hydration already loads the authoritative contract from the skill folder.

## Example INIT-TASK brief

```md
PURPOSE: Publish approved rewritten DBM section SEC-03.
ScopePath: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/
TaskSkill: dbm-section-publish
AllowedWriteTargets:
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/SEC-03.md
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/SEC-03_QA.md
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/SEC-03_ASSERTIONS.csv
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/SEC-03_ASSERTION_DISCOVERY.csv
RuntimeOverrides:
  SECTION_ID: SEC-03
  SECTION_TITLE: Deep Cut Process Basis
  SECTION_TYPE: PROCESS_BASIS
  SECTION_PURPOSE: Explain current deep cut process basis and interfaces.
  SECTION_OUTPUT_PATH: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/SEC-03.md
  SECTION_QA_OUTPUT_PATH: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/SEC-03_QA.md
  SECTION_ASSERTIONS_OUTPUT_PATH: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/SEC-03_ASSERTIONS.csv
  SECTION_ASSERTION_DISCOVERY_OUTPUT_PATH: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/SEC-03_ASSERTION_DISCOVERY.csv
  PUBLICATION_INPUT_MANIFEST: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Input_Manifest.md
  PUBLICATION_SCHEMA_PATH: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Schema.md
  SECTION_MAP_PATH: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Section_Map.csv
  PUBLICATION_RULES_PATH: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Rules.md
  PUBLICATION_CONCORDANCE_REGISTER_PATH: /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Concordance_Register.csv
  MAX_KA_FILES: 12
ExpectedOutputs:
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/SEC-03.md
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/SEC-03_QA.md
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/SEC-03_ASSERTIONS.csv
  - /repo/domain-test/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/SEC-03_ASSERTION_DISCOVERY.csv
```
