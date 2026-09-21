# dbm-section-publish contract

## Brief

This file defines the INIT-TASK dispatch contract for `TASK + dbm-section-publish`.

### Purpose

Use this workflow when dbm-publisher needs one approved DBM section synthesized from the frozen publication planning artifacts and the exact mapped KTY-local inputs for that section.

### Scope model

- `ScopePath` should normally be the section-local publication folder:
  - `{EXECUTION_ROOT}/_Publication/DBM/sections/{SECTION_ID}/`
- `AllowedWriteTargets` must name exactly two files:
  - section body markdown,
  - section QA markdown.

The brief must not grant broader publication-root or KTY-folder write access.

### Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why this section run exists | `Publish approved rewritten DBM section SEC-03.` |
| `ScopePath` | path | Section-local publication folder | `/abs/root/_Publication/DBM/sections/SEC-03/` |
| `Workflow` | string | Must equal the workflow folder/name | `dbm-section-publish` |
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

### Optional brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `RuntimeOverrides.DBM_OUTPUT_MODE` | enum | Publication output mode; defaults to full engineering DBM when omitted | `FULL_ENGINEERING_DBM` |
| `RuntimeOverrides.SOURCE_DOMAIN` | string | Domain label for the run | `West_Doe_Deepcut_DBM` |
| `RuntimeOverrides.SECTION_ORDER` | integer | Display/assembly order | `3` |
| `RuntimeOverrides.SECTION_CONTEXT_PATH` | path | Deterministic per-section structural context packet | `/.../_Planning/section-context/SEC-03_Context.md` |
| `RuntimeOverrides.OPEN_ITEM_PACKET` | block/path | Section-relevant unresolved human rulings, engineering TBDs, and decomposition/publication gaps from dbm-publisher's mapped-KTY scan | `OpenItemPacket: ...` |
| `RuntimeOverrides.ALLOW_CONTEXT_ONLY_DECOMP_FALLBACK` | boolean | Allow decomposition fallback for unready `CONTEXT_ONLY` inputs | `true` |
| `RuntimeOverrides.SUPERSESSION_MAP_PATH` | path | Frozen cumulative supersession map; blank `AppliesToSections` means global applicability, otherwise the row must include the current `SECTION_ID` | `/.../_ScopeChange/SCA-004_.../Supersession_Map.csv` |
| `RuntimeOverrides.ROOT_NAME` | string | Canonical root name for supersession applicability filtering | `West_Doe_Deepcut_DBM` |
| `RuntimeOverrides.FACILITY_ID` | string | Facility identifier for supersession applicability filtering | `04-25` |
| `RuntimeOverrides.HYPERGRAPH_USE_MODE` | enum | Whether hypergraph evidence is admitted for this run | `AUXILIARY_PLANNING` |
| `RuntimeOverrides.HYPERGRAPH_SNAPSHOT_PATH` | path | Exact path to the admitted hypergraph snapshot | `/.../_Aggregation/Hypergraph/snapshot/` |
| `RuntimeOverrides.HYPERGRAPH_NODES_PATH` | path | Exact path to the hypergraph nodes CSV | `/.../_Aggregation/Hypergraph/nodes.csv` |
| `RuntimeOverrides.HYPERGRAPH_HYPEREDGES_PATH` | path | Exact path to the hypergraph hyperedges CSV | `/.../_Aggregation/Hypergraph/hyperedges.csv` |
| `RuntimeOverrides.HYPERGRAPH_EVIDENCE_ROOT` | path | Root folder containing hypergraph evidence CSVs | `/.../_Aggregation/Hypergraph/evidence/` |
| `CustomInstructions` | string | Run-specific reinforcement only; must not restate the workflow contract | `Keep amendment notes especially brief in this run.` |
| `EXCLUSIONS` | list[string] | Extra run-local exclusions inside already-mapped artifacts | `Ignore superseded historical table under heading X.` |

### Runtime-override guidance

- `SECTION_TYPE` must match the approved section taxonomy in `Publication_Schema.md`.
- `SECTION_OUTPUT_PATH` and `SECTION_QA_OUTPUT_PATH` must both live inside `ScopePath`.
- `MAX_KA_FILES` should match the approved section design, not an ad hoc worker preference.
- The section worker should receive only the planning artifacts and mapped inputs already frozen for the run.
- `SECTION_CONTEXT_PATH`, when provided, is read-only structural context for framing, completeness checks, and QA. It is not a writable target and does not replace mapped KA content as body-authoring authority.
- `OPEN_ITEM_PACKET`, when provided, is operational caveat context for QA/body uncertainty handling. It does not expand body-authoring authority or permit unmapped content.
- `DBM_OUTPUT_MODE` defaults to `FULL_ENGINEERING_DBM`. `DBM_DIGEST` must be explicit in the brief and publication rules when selected by the human.
- In `FULL_ENGINEERING_DBM` mode, the brief should include the approved body completeness standard, expected body components, expected design-basis tables/data classes, source DBM geometry treatment, and section-specific adequacy risks from `Publication_Schema.md` / `Publication_Rules.md`.
- When a supersession map is admitted, `ROOT_NAME` should use the canonical root name for the run and `FACILITY_ID` should match the manifest's facility identifier so applicability filtering is unambiguous.

### Recommended CustomInstructions content

Use `CustomInstructions` only for run-specific reinforcement such as:
- emphasis on a particular readability concern,
- reminder that a specific mapped artifact is context-only,
- reminder that a section is near its size limit,
- reminder that a section is near its size limit.

Do not use `CustomInstructions` to recreate the workflow contract. The brief declares the selected workflow and required CONTRACT.md resource; record the loading mechanism actually used.

### Example INIT-TASK brief

```md
PURPOSE: Publish approved rewritten DBM section SEC-03.
ScopePath: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/SEC-03/
Workflow: dbm-section-publish
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

## Acceptance

### Minimum output validity checks

The run is valid only when all of the following are true:

1. Both required outputs exist:
   - section body markdown,
   - section QA markdown.
2. The section body reads as coherent engineering prose under `Publication_Rules.md` rather than as a concatenated artifact dump.
3. The section body reflects current post-SCA state when mapped sources require a state choice.
4. Unsupported claims are surfaced as `TBD`, assumptions, or conflicts rather than silently guessed.
5. The section body does not use detailed inline source citations; detailed provenance belongs in QA and the package trace appendix.
6. The section QA artifact uses the required stable block structure in the required order.
7. All writes stayed inside the approved section-local publication folder.
8. When `SECTION_CONTEXT_PATH` is provided, the section QA records whether structural context was consumed and flags any mapped `PRIMARY` KTY that produced no material body contribution.
13. Body prose uses only reader-facing epistemic labels (`TBD`, `to be confirmed`, `assumed`); original governance-state labels remain in QA.
14. In `FULL_ENGINEERING_DBM` mode, the body is usable for core engineering design basis without reopening KA files for material values, capacities, configurations, interfaces, assumptions, TBDs, or design constraints.
15. In `FULL_ENGINEERING_DBM` mode, the body uses DBM-native engineering structure; mapped assertions, controlled assertions, raw caveat dumps, file-path inventories, and trace scaffolds do not stand in for the section body.
16. Design-basis tables are included, consolidated, split, or explicitly omitted/deferred with rationale. Trace-only treatment is not used for body-worthy design-basis tables.
17. `PRIMARY` KTYs with multiple material facts, tables, or open requirements are not collapsed to token mentions or one generic sentence.

### Required QA artifact structure

`SEC-##_QA.md` must contain these H2 headings in this order:

1. `## Section Summary`
2. `## Coverage Table`
3. `## Design Basis Content Coverage`
4. `## Table Treatment`
5. `## Section Adequacy Findings`
6. `## Readiness Observations`
7. `## Conflict Register`
8. `## Terminology Notes`
9. `## Gap / TBD Register`
10. `## Amendment Notes`

Content expectations by block:
- `Coverage Table` records mapped KTYs/KAs consumed plus mapped inputs skipped and why.
- `Coverage Table` must identify `PRIMARY` KTYs that materially contributed to body prose and any `PRIMARY` KTYs with zero visible body contribution.
- `Design Basis Content Coverage` records applicable content classes as `INCLUDED`, `OMITTED_WITH_RATIONALE`, `DEFERRED_UPSTREAM_MISSING`, or `NOT_APPLICABLE`.
- `Table Treatment` records design-basis table handling as `INCLUDED`, `CONSOLIDATED`, `SPLIT`, `OMITTED_WITH_RATIONALE`, `TRACE_ONLY`, `DEFERRED_UPSTREAM_MISSING`, or `NONE_APPLICABLE`.
- `Section Adequacy Findings` records fixed finding codes when present: `UNDERDEVELOPED_SECTION`, `UNJUSTIFIED_TABLE_OMISSION`, `PRIMARY_KTY_COLLAPSED`, `MISSING_DESIGN_BASIS_CLASS`, `QA_SCAFFOLD_BODY_LEAKAGE`, `NON_STANDALONE_CORE_BASIS`.
- `Readiness Observations` records KTY readiness issues.
- `Conflict Register` records contradictory values/states and both mapped positions.
- `Gap / TBD Register` preserves distinctions such as human authority rulings, `TBD`, `ASSUMPTION`, `DEFERRED_CONFIRMATION`, external responsibility, and decomposition/publication gaps.

### Failure reporting expectations

Use `FAILED_INPUTS` when:
- required runtime overrides are missing,
- mapped `PRIMARY` or `CONFLICTING` inputs are below readiness threshold,
- the section input set exceeds `MAX_KA_FILES` or the approved size limit,
- output paths fall outside the approved section-local publication folder.

Use `FAILED` when:
- a required output cannot be written despite valid inputs,
- an internal run error prevents the stable outputs from being emitted.

Even on non-blocking runs, QA must surface:
- skipped supporting inputs,
- terminology normalizations,
- remaining conflicts,
- remaining `TBD` / assumption / deferred-confirmation items,
- any reliance on amendment notes or decision-log references,
- any supersession note intentionally included in body prose under the body-note heuristic,
- any context-packet factual-use override,
- any content-adequacy fixed finding code,
- any design-basis table omitted, consolidated, split, or deferred,
- any design-basis table omitted, consolidated, split, or deferred.

## Tool use

### Preferred tool order

1. Read the frozen publication planning artifacts.
2. Read the deterministic `SECTION_CONTEXT_PATH` packet when provided as structural context for framing, completeness checks, factual-use eligibility, open items, and QA.
3. Read only the mapped KTY-local files permitted by the approved section map.
4. Use direct reasoning to synthesize the section body and QA artifact.

### Allowed deterministic tools

#### Operationally invoked

None by this workflow. It consumes deterministic planning outputs produced upstream rather than invoking tools itself.

### Expected use of reasoning

This workflow is reasoning-heavy. It must:
- interpret mapped inputs under `MappingRole` / `ContributionScope`,
- use section context packets without promoting them to body-authoring authority except for the narrow `OVERVIEW` framing exception,
- apply publication-rule precedence,
- synthesize coherent engineering prose,
- in `FULL_ENGINEERING_DBM` mode, preserve material engineering detail and design-basis tables in DBM-native body structure,
- preserve uncertainty as `TBD`, assumptions, or conflicts rather than inventing reconciliations,
- preserve uncertainty as `TBD`, assumptions, or conflicts rather than inventing reconciliations.

### Disallowed use

- No dispatching of other workflows or agents.
- No guessed discovery of inputs outside the frozen planning artifacts.
- No use of `_Aggregation/*`, `_Coordination/*`, `_Evaluation/*`, `_Reconciliation/*`, `_MEMORY.md`, or `_SEMANTIC.md` as content authority. `_MEMORY.md` may be read only as non-authoritative operational context whenever `_STATUS.md` is read.
- No modification of any `CAT-* / 1_Working / KTY-*` source files.
- No package-level assembly.
- No use of QA/export scaffolds as the default body structure in `FULL_ENGINEERING_DBM` mode.

### Write boundary

The workflow may write only:
- one section body markdown file,
- one section QA markdown file.

All writes must remain inside the section-local publication folder named in the INIT-TASK brief.
