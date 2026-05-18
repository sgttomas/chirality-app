# BRIEF SCHEMA — dbm-section-publish

This file defines the INIT-TASK dispatch contract for `TASK + dbm-section-publish`.

## Purpose

Use this skill when DBM_PUBLISHER needs one approved DBM section synthesized from the frozen publication planning artifacts and the exact mapped KTY-local inputs for that section.

## Scope model

- `ScopePath` should normally be the section-local publication folder:
  - `{EXECUTION_ROOT}/_Publication/DBM/sections/{SECTION_ID}/`
- `AllowedWriteTargets` must name exactly two files:
  - section body markdown,
  - section QA markdown.

The brief must not grant broader publication-root or KTY-folder write access.

## Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why this section run exists | `Publish approved rewritten DBM section SEC-03.` |
| `ScopePath` | path | Section-local publication folder | `/abs/root/_Publication/DBM/sections/SEC-03/` |
| `TaskSkill` | string | Must equal the skill folder/name | `dbm-section-publish` |
| `AllowedWriteTargets` | list[path] | Exact writable outputs | `[/.../SEC-03.md, /.../SEC-03_QA.md]` |
| `RuntimeOverrides.SECTION_ID` | string | Stable section identity | `SEC-03` |
| `RuntimeOverrides.SECTION_TITLE` | string | Approved section title | `Deep Cut Process Basis` |
| `RuntimeOverrides.SECTION_TYPE` | enum | Approved section taxonomy | `PROCESS_BASIS` |
| `RuntimeOverrides.SECTION_PURPOSE` | string | Human-approved section intent | `Explain current deep cut process basis and interfaces.` |
| `RuntimeOverrides.SECTION_OUTPUT_PATH` | path | Section body output | `/.../SEC-03.md` |
| `RuntimeOverrides.SECTION_QA_OUTPUT_PATH` | path | QA output | `/.../SEC-03_QA.md` |
| `RuntimeOverrides.PUBLICATION_INPUT_MANIFEST` | path | Frozen input manifest | `/.../_Planning/Publication_Input_Manifest.md` |
| `RuntimeOverrides.PUBLICATION_SCHEMA_PATH` | path | Approved publication schema | `/.../_Planning/Publication_Schema.md` |
| `RuntimeOverrides.SECTION_MAP_PATH` | path | Approved section map | `/.../_Planning/Section_Map.csv` |
| `RuntimeOverrides.PUBLICATION_RULES_PATH` | path | Approved publication rules | `/.../_Planning/Publication_Rules.md` |
| `RuntimeOverrides.MAX_KA_FILES` | integer | Hard cap on mapped KA files | `12` |
| `ExpectedOutputs` | list[path] | Same two section outputs | `[/.../SEC-03.md, /.../SEC-03_QA.md]` |

## Optional brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `RuntimeOverrides.DBM_OUTPUT_MODE` | enum | Publication output mode; defaults to full engineering DBM when omitted | `FULL_ENGINEERING_DBM` |
| `RuntimeOverrides.SOURCE_DOMAIN` | string | Domain label for the run | `West_Doe_Deepcut_DBM` |
| `RuntimeOverrides.SECTION_ORDER` | integer | Display/assembly order | `3` |
| `RuntimeOverrides.SECTION_CONTEXT_PATH` | path | Deterministic per-section structural context packet | `/.../_Planning/section-context/SEC-03_Context.md` |
| `RuntimeOverrides.OPEN_ITEM_PACKET` | block/path | Section-relevant unresolved human rulings, engineering TBDs, and decomposition/publication gaps from DBM_PUBLISHER's mapped-KTY scan | `OpenItemPacket: ...` |
| `RuntimeOverrides.ALLOW_CONTEXT_ONLY_DECOMP_FALLBACK` | boolean | Allow decomposition fallback for unready `CONTEXT_ONLY` inputs | `true` |
| `RuntimeOverrides.SUPERSESSION_MAP_PATH` | path | Frozen cumulative supersession map; blank `AppliesToSections` means global applicability, otherwise the row must include the current `SECTION_ID` | `/.../_ScopeChange/SCA-004_.../Supersession_Map.csv` |
| `RuntimeOverrides.ROOT_NAME` | string | Canonical root name for supersession applicability filtering | `West_Doe_Deepcut_DBM` |
| `RuntimeOverrides.FACILITY_ID` | string | Facility identifier for supersession applicability filtering | `04-25` |
| `RuntimeOverrides.HYPERGRAPH_USE_MODE` | enum | Whether hypergraph evidence is admitted for this run | `AUXILIARY_PLANNING` |
| `RuntimeOverrides.HYPERGRAPH_SNAPSHOT_PATH` | path | Exact path to the admitted hypergraph snapshot | `/.../_Aggregation/Hypergraph/snapshot/` |
| `RuntimeOverrides.HYPERGRAPH_NODES_PATH` | path | Exact path to the hypergraph nodes CSV | `/.../_Aggregation/Hypergraph/nodes.csv` |
| `RuntimeOverrides.HYPERGRAPH_HYPEREDGES_PATH` | path | Exact path to the hypergraph hyperedges CSV | `/.../_Aggregation/Hypergraph/hyperedges.csv` |
| `RuntimeOverrides.HYPERGRAPH_EVIDENCE_ROOT` | path | Root folder containing hypergraph evidence CSVs | `/.../_Aggregation/Hypergraph/evidence/` |
| `CustomInstructions` | string | Run-specific reinforcement only; must not restate the skill contract | `Keep amendment notes especially brief in this run.` |
| `EXCLUSIONS` | list[string] | Extra run-local exclusions inside already-mapped artifacts | `Ignore superseded historical table under heading X.` |

## Runtime-override guidance

- `SECTION_TYPE` must match the approved section taxonomy in `Publication_Schema.md`.
- `SECTION_OUTPUT_PATH` and `SECTION_QA_OUTPUT_PATH` must both live inside `ScopePath`.
- `MAX_KA_FILES` should match the approved section design, not an ad hoc worker preference.
- The section worker should receive only the planning artifacts and mapped inputs already frozen for the run.
- `SECTION_CONTEXT_PATH`, when provided, is read-only structural context for framing, completeness checks, and QA. It is not a writable target and does not replace mapped KA content as body-authoring authority.
- `OPEN_ITEM_PACKET`, when provided, is operational caveat context for QA/body uncertainty handling. It does not expand body-authoring authority or permit unmapped content.
- `DBM_OUTPUT_MODE` defaults to `FULL_ENGINEERING_DBM`. `DBM_DIGEST` must be explicit in the brief and publication rules when selected by the human.
- In `FULL_ENGINEERING_DBM` mode, the brief should include the approved body completeness standard, expected body components, expected design-basis tables/data classes, source DBM geometry treatment, and section-specific adequacy risks from `Publication_Schema.md` / `Publication_Rules.md`.
- When a supersession map is admitted, `ROOT_NAME` should use the canonical root name for the run and `FACILITY_ID` should match the manifest's facility identifier so applicability filtering is unambiguous.

## Recommended CustomInstructions content

Use `CustomInstructions` only for run-specific reinforcement such as:
- emphasis on a particular readability concern,
- reminder that a specific mapped artifact is context-only,
- reminder that a section is near its size limit,
- reminder that a section is near its size limit.

Do not use `CustomInstructions` to recreate the skill contract. TASK hydration already loads the authoritative contract from the skill folder.

## Example INIT-TASK brief

```md
PURPOSE: Publish approved rewritten DBM section SEC-03.
ScopePath: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/
TaskSkill: dbm-section-publish
AllowedWriteTargets:
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/SEC-03.md
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/SEC-03_QA.md
RuntimeOverrides:
  SECTION_ID: SEC-03
  SECTION_TITLE: Deep Cut Process Basis
  SECTION_TYPE: PROCESS_BASIS
  SECTION_PURPOSE: Explain current deep cut process basis and interfaces.
  SECTION_OUTPUT_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/SEC-03.md
  SECTION_QA_OUTPUT_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/SEC-03_QA.md
  PUBLICATION_INPUT_MANIFEST: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Input_Manifest.md
  PUBLICATION_SCHEMA_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Schema.md
  SECTION_MAP_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Section_Map.csv
  PUBLICATION_RULES_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Rules.md
  MAX_KA_FILES: 12
  DBM_OUTPUT_MODE: FULL_ENGINEERING_DBM
  SECTION_CONTEXT_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/section-context/SEC-03_Context.md
ExpectedOutputs:
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/SEC-03.md
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/SEC-03_QA.md
```
