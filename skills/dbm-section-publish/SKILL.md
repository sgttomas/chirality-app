---
name: dbm-section-publish
description: Publish exactly one rewritten DBM section from approved mapped DOMAIN inputs and emit fixed QA artifacts.
compatibility: Chirality TASK; dispatched by DBM_PUBLISHER after the publication planning artifacts are frozen.
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — dbm-section-publish

## Purpose

Publish **exactly one target DBM section** from approved mapped inputs. The skill consumes frozen publication planning artifacts, reads only the mapped KTY-local inputs for its assigned section, and emits two outputs:
- one section body,
- one section QA artifact.

This skill is the primary publication authoring unit in v1. It is **not** a dispatcher and it does **not** redesign the publication schema or section map.

## Suitable agent shells

- `TASK` (generic shell mode, no profile)

Typical dispatcher: `DBM_PUBLISHER` after human approval of the frozen planning artifacts.

## Inputs

### Required

- `SECTION_ID`
- `SECTION_TITLE`
- `SECTION_TYPE`
- `SECTION_PURPOSE`
- `SECTION_OUTPUT_PATH`
- `SECTION_QA_OUTPUT_PATH`
- `PUBLICATION_INPUT_MANIFEST`
- `PUBLICATION_SCHEMA_PATH`
- `SECTION_MAP_PATH`
- `PUBLICATION_RULES_PATH`
- `MAX_KA_FILES`

### Optional

- `DBM_OUTPUT_MODE` — `FULL_ENGINEERING_DBM|DBM_DIGEST`, default `FULL_ENGINEERING_DBM`
- `SOURCE_DOMAIN`
- `SECTION_ORDER`
- `SECTION_CONTEXT_PATH` — deterministic per-section structural context packet
- `OPEN_ITEM_PACKET` — section-relevant human rulings, engineering TBDs, and decomposition/publication gaps supplied by DBM_PUBLISHER as operational caveat context
- `ALLOW_CONTEXT_ONLY_DECOMP_FALLBACK` — `true|false`, default `true`
- `HYPERGRAPH_USE_MODE`
- `HYPERGRAPH_SNAPSHOT_PATH`
- `HYPERGRAPH_NODES_PATH`
- `HYPERGRAPH_HYPEREDGES_PATH`
- `HYPERGRAPH_EVIDENCE_ROOT`

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `SECTION_ID` | Stable section identity for this run | **Required** | `SEC-##` or approved equivalent |
| `SECTION_TITLE` | Approved section title | **Required** | Non-empty string |
| `SECTION_TYPE` | Approved section taxonomy | **Required** | `OVERVIEW`, `PROCESS_BASIS`, `PHILOSOPHY`, `DATA_REFERENCE`, `DISCIPLINE_BASIS`, `REGULATORY` |
| `SECTION_PURPOSE` | Human-approved intent for the section | **Required** | Non-empty string |
| `SECTION_OUTPUT_PATH` | Output path for the section body | **Required** | Path under `_Publication/DBM/sections/{SECTION_ID}/` |
| `SECTION_QA_OUTPUT_PATH` | Output path for stable QA markdown | **Required** | Path under `_Publication/DBM/sections/{SECTION_ID}/` |
| `PUBLICATION_INPUT_MANIFEST` | Frozen exact input-path manifest | **Required** | Markdown path |
| `PUBLICATION_SCHEMA_PATH` | Approved publication schema | **Required** | Markdown path |
| `SECTION_MAP_PATH` | Approved section map | **Required** | CSV path |
| `PUBLICATION_RULES_PATH` | Approved publication rules | **Required** | Markdown path |
| `MAX_KA_FILES` | Hard cap on mapped KA files for this section | **Required** | Positive integer |
| `DBM_OUTPUT_MODE` | Publication output mode for the run | `FULL_ENGINEERING_DBM` | `FULL_ENGINEERING_DBM`, `DBM_DIGEST` |
| `SOURCE_DOMAIN` | Source domain label for the run | inferred | Non-empty string |
| `SECTION_ORDER` | Display/assembly order | inferred | Positive integer |
| `SECTION_CONTEXT_PATH` | Deterministic per-section structural context packet | unset | Path under `_Publication/DBM/_Planning/section-context/` |
| `OPEN_ITEM_PACKET` | Section-relevant unresolved items from DBM_PUBLISHER's mapped-KTY scan | unset | Brief block or path supplied by dispatcher |
| `ALLOW_CONTEXT_ONLY_DECOMP_FALLBACK` | Allow decomposition-level context when a `CONTEXT_ONLY` KTY is below readiness threshold | `true` | `true`, `false` |
| `HYPERGRAPH_USE_MODE` | Whether hypergraph evidence is admitted for this run | `NONE` | `NONE`, `AUXILIARY_PLANNING`, `AUXILIARY_QA`, `AUXILIARY_PLANNING_AND_QA` |
| `HYPERGRAPH_SNAPSHOT_PATH` | Exact path to the admitted hypergraph snapshot | unset | Path under `_Aggregation/Hypergraph/` |
| `HYPERGRAPH_NODES_PATH` | Exact path to the hypergraph nodes CSV | unset | Path |
| `HYPERGRAPH_HYPEREDGES_PATH` | Exact path to the hypergraph hyperedges CSV | unset | Path |
| `HYPERGRAPH_EVIDENCE_ROOT` | Root folder containing hypergraph evidence CSVs | unset | Path under `_Aggregation/Hypergraph/` |
| `SUPERSESSION_MAP_PATH` | Path to the frozen cumulative supersession map | unset | CSV path; when present, the section worker filters to rows whose root/facility applicability matches the run. Blank `AppliesToSections` means the binding applies globally; otherwise `AppliesToSections` must include the current `SECTION_ID`. |
| `ROOT_NAME` | Canonical root name for supersession applicability filtering | unset | String such as `West_Doe_Deepcut_DBM` |
| `FACILITY_ID` | Facility identifier for supersession applicability filtering | unset | String such as `04-25` |

## Tool usage

- This is a reasoning-first synthesis skill.
- It consumes deterministic planning artifacts produced outside the skill.
- The `allowed-tools` frontmatter field is intentionally omitted because this skill has no deterministic tool requirements of its own.

Disallowed behavior:
- No dispatching other tasks.
- No writes outside the four section output paths.
- No modification of any `CAT-* / 1_Working / KTY-*` files.
- No guessed discovery outside the frozen planning artifacts and approved section-map rows.
- No use of `_MEMORY.md` or `_SEMANTIC.md` as factual authority. When the skill reads a mapped KTY `_STATUS.md`, it must also read sibling `_MEMORY.md` when present as non-authoritative operational context.
- Hypergraph evidence, when admitted, is read-only for local QA checks and must not drive section body synthesis.
- No conversion of unresolved human rulings, engineering TBDs, assumptions, deferred confirmations, or decomposition/publication gaps into confirmed design claims.
- In `FULL_ENGINEERING_DBM` mode, no raw caveat dump, file-path inventory, or trace scaffold may stand in as the main body structure.

## Outputs

- `{SECTION_OUTPUT_PATH}` — one rewritten DBM section body
- `{SECTION_QA_OUTPUT_PATH}` — stable section QA artifact

## Authority hierarchy

When synthesizing a section, consult inputs in this order of authority:

1. approved `Publication_Schema.md`
2. approved `Publication_Rules.md`
3. approved `Section_Map.csv`
4. frozen `Publication_Input_Manifest.md`
5. section context packet when provided, as structural context for framing and completeness checks only
6. accepted scope-change state and approved decomposition state named in the manifest
7. exact mapped KTY-local files named in the section map
8. vocabulary map, decision log, and open-issues register named in the manifest when required by the mapped rows or QA work
9. original/reference markdown and reference/provenance tables as reference/provenance only; they do not override accepted DOMAIN/SCA state or mapped CAT/KTY/KA-local content

## DBM output mode behavior

`FULL_ENGINEERING_DBM` is the default. In this mode, the section body must be a DBM-native engineering section, not a digest or current-state summary. It must carry the core design basis needed by a reader without reopening KA files for material values, capacities, configurations, interfaces, assumptions, design constraints, TBDs, and applicable tables.

`DBM_DIGEST` is allowed only when the dispatch brief or frozen publication rules explicitly select it. Digest mode may be concise, but the section QA must state that digest mode was used and must not present the output as a full governing DBM section.

## Open-item treatment

When `OPEN_ITEM_PACKET` is supplied, treat it as operational caveat context for this section. It does not authorize new body claims or expand the mapped input set.

The section worker must:
- surface section-relevant human authority rulings in section QA and, when they affect the current design basis, in the section body as unresolved decisions rather than confirmed facts,
- write engineering uncertainty as explicit `TBD`, `to be confirmed`, or `assumed` statements in body prose when body treatment is needed,
- preserve original labels such as `TBD`, `ASSUMPTION`, `DEFERRED_CONFIRMATION`, `ExternalResponsibility`, and human-ruling status in section QA,
- identify decomposition/publication gaps as limitations or required follow-up, not as content to invent,
- treat retired, tombstoned, archived-stubbed, or no-factual-use KTYs as non-authoring inputs unless the approved section map and publication rules explicitly allow context-only treatment,
- preserve accepted SCA supersession state without inferring additional supersessions from prose.

## Hypergraph evidence policy

Hypergraph evidence is **read-only auxiliary structure evidence** for section workers. It does not enter the content authority stack for section body synthesis.

When `HYPERGRAPH_USE_MODE != NONE` and hypergraph inputs are provided in the brief, the section worker may use hypergraph evidence only for local QA checks:
- did the mapped KTY set omit an obviously connected supporting KTY implied by graph adjacency?
- does the section appear to restate a known cross-section state that should be verified for consistency?

Hypergraph evidence must not be used to:
- author or rewrite section body prose,
- override mapped CAT/KTY/KA-local content,
- contradict the approved section map or decomposition mappings.

Any hypergraph-derived QA concern must be labeled `AUXILIARY_STRUCTURE_WARNING` in the section QA output. The section worker must not block its own output on hypergraph QA findings; those findings are advisory for the package gate to consume.

## Mapping behavior definitions

### `MappingRole`

- `PRIMARY` — mapped CAT/KTY/KA-local material that anchors section narrative and structure
- `SUPPORTING` — contextual or constraining content that informs the section but does not define its primary structure
- `CONFLICTING` — mapped input known to contradict other mapped inputs; the skill must surface the conflict in QA and avoid silent reconciliation
- `CONTEXT_ONLY` — background-only material that may inform interpretation but should not drive direct design-basis claims unless the publication rules explicitly permit it

### `ContributionScope`

- `FULL_ARTIFACT` — the whole artifact may contribute
- `TARGET_HEADING` — use only the heading/subsection named in the section-map `Notes`
- `TABLE_ONLY` — use tabular content only
- `VALUES_ONLY` — use only explicit values/parameters
- `BACKGROUND_ONLY` — background context only; do not rely on it for direct design-basis claims

## Default section templates

### `OVERVIEW`
- facility/project identity
- stated objectives
- scope boundaries
- key assumptions/constraints
- document applicability

Authority expansion for `OVERVIEW` sections: this is the one section type where structural context from `SECTION_CONTEXT_PATH` may become body-authoring authority for facility-level framing. The worker may synthesize facility identity, design objectives, scope boundaries, and document applicability from the context packet's objectives and category/KTY descriptions even when no single KA file states the overview in the same wording. This expansion is limited to facility/document framing. It does not permit inventing design values, equipment requirements, operating conditions, capacities, limits, product specifications, or other technical claims.

### `PROCESS_BASIS`
- purpose
- functional configuration
- design/operating basis
- interfaces
- controls/protection
- facility-specific notes

### `PHILOSOPHY`
- governing principle
- applicability
- required design behavior
- exceptions/limits
- rationale

### `DATA_REFERENCE`
- narrative introduction
- consolidated values/tables
- assumptions/caveats
- usage notes

### `DISCIPLINE_BASIS`
- discipline scope
- governing basis
- required systems/components
- constraints/standards
- interfaces

### `REGULATORY`
- governing obligation
- applicability
- facility impact
- compliance implications
- unresolved items

## Full engineering DBM adequacy expectations

In `FULL_ENGINEERING_DBM` mode, the templates above are minimum outlines only. The worker must assess the mapped active material against these design-basis content classes and include every applicable class in the body or explain the omission in section QA:

- governing design criteria
- capacities, rates, loads, compositions, emissions, utility demands, or similar design values
- equipment and package configuration
- operating modes and design cases
- controls, safeguards, shutdowns, relief, alarms, permissives, or other protective functions
- materials, standards, codes, environmental limits, or regulatory constraints
- interfaces with other systems, areas, facilities, disciplines, or external parties
- assumptions, TBDs, exclusions, and design-development requirements
- tabular data that is part of the design basis

Section-type emphasis:
- `OVERVIEW`: facility identity, document applicability, scope boundaries, current-state basis, and major unresolved limitations; do not invent technical values from structural context.
- `PROCESS_BASIS`: design/operating cases, process configuration, design values, equipment/package roles, process controls/protection, utilities, interfaces, and open design-development requirements.
- `PHILOSOPHY`: governing principles, applicability limits, required design behavior, exceptions, rationale, and related standards or owner decisions.
- `DATA_REFERENCE`: body tables or consolidated table equivalents for design-basis values, plus usage constraints and assumptions.
- `DISCIPLINE_BASIS`: discipline scope, governing criteria, required systems/components, standards/codes, interfaces, constraints, and unresolved discipline inputs.
- `REGULATORY`: obligations, applicability, compliance basis, facility impact, monitoring/reporting or design constraints, and unresolved regulatory items.

If the approved section design cannot carry the applicable material without collapsing systems, tables, or design cases into a digest, emit `UNDERDEVELOPED_SECTION` in section QA and explain the required split or schema repair.

### Table treatment

Design-basis tables in mapped material must be preserved, consolidated, split, or reconstructed as equivalent body tables when they contain material engineering values. The worker must not omit such tables merely because detailed provenance has moved to the trace appendix.

Allowed table treatments:
- `INCLUDED`
- `CONSOLIDATED`
- `SPLIT`
- `OMITTED_WITH_RATIONALE`
- `TRACE_ONLY`
- `DEFERRED_UPSTREAM_MISSING`
- `NONE_APPLICABLE`

`TRACE_ONLY` is valid only for trace, index, provenance, reference-list, or non-design-basis tables. A design-basis table omitted without rationale is an `UNJUSTIFIED_TABLE_OMISSION` finding.

## KTY readiness gates

The skill must treat the frozen `Publication_Input_Manifest.md` as the primary freshness boundary for the run.

Before reading mapped KTY-local files, the skill must confirm that the manifest records publication admission for the root via:
- the active root `Handoff_State.md`,
- publication-admission / closure evidence for the admitted snapshot,
- non-blocking audit evidence for the admitted current-state root package.

If the manifest is missing that evidence, or records the root as not publication-admissible, fail with `FAILED_INPUTS`.

After the root publication-admission check passes, the skill must read each mapped KTY `_STATUS.md` before using its files, and must read sibling `_MEMORY.md` whenever `_STATUS.md` is read. `_MEMORY.md` may inform operational continuity or known local caveats but must not become factual authority for published DBM claims.

Minimum rules:
- `PRIMARY` and `CONFLICTING` inputs must be at least `INITIALIZED`.
- If a `PRIMARY` input is below that threshold, fail with `FAILED_INPUTS`.
- If a `CONFLICTING` input is below that threshold, fail with `FAILED_INPUTS`.
- If a `SUPPORTING` input is below that threshold, skip it and record a gap note in section QA.
- If a `CONTEXT_ONLY` input is below that threshold, the skill may fall back to decomposition-level context only when `ALLOW_CONTEXT_ONLY_DECOMP_FALLBACK=true`, with a QA note.
- If manifest/root publication-admission evidence and local `_STATUS.md` materially disagree, fail with `FAILED_INPUTS` and record the mismatch in section QA.

The skill must not treat local `_STATUS.md` files as sufficient publication admission evidence on their own, and it must not treat an `OPEN` or otherwise unready KTY as equivalent to a fully authored KTY artifact.

## Terminology control

When the manifest provides a vocabulary map, the skill should:
- prefer the canonical term over KA-local synonyms,
- retain a synonym in parentheses only when it materially helps recognition,
- avoid mixed terminology for the same system within one section.

## Cross-facility synthesis rules

1. If multiple mapped artifacts agree, synthesize them into one coherent narrative.
2. If mapped artifacts differ:
   - do not reconcile silently,
   - first determine row eligibility using the admitted supersession map: root/facility must match the current run; blank `AppliesToSections` remains globally eligible; populated `AppliesToSections` must include the current `SECTION_ID`,
   - if a `SUPERSESSION` binding exists in the eligible supersession rows for the differing fact: apply the replacement value and record the binding reference (AmendmentID, DecisionID, SupersededAuthorityRef) in section QA,
   - if a `SUPPLEMENTARY_EXTENSION` binding exists: preserve the accepted current-state KTY/decomposition basis and record the supplementary detail in QA/trace when relevant,
   - if mapped KTY-local or decomposition-state content contradicts admitted reference/provenance material and no accepted SCA/decomposition evidence resolves the difference: record the conflict in QA — do not silently prefer either reference material or KTY-local content,
   - otherwise record any publication conflict in section QA and use cautious wording in the narrative.
3. If a system exists in only one facility/domain, scope the section explicitly to that facility.
4. If a system moved between facilities due to accepted SCA, present the post-SCA arrangement as current-state content and keep prior placement only as audit context.
5. If content is absent for a facility, do not invent parity; use `TBD` or an explicit scope note.

### Supersession body-note heuristic

Default: supersession history appears in section QA and `Trace_Appendix.md`, not in section body prose. A section may include a short supersession note in body prose only when all of the following are true:
- the supersession affects a current design-basis value or scope state that is stated in the body,
- the superseded value or state is likely to remain visible in admitted reference/provenance material or legacy project references that the reader may encounter,
- omitting the note could reasonably cause a reader to treat the current published value as an error,
- the note can be written in one concise engineering sentence without governance process history.

Acceptable pattern: "Current design basis is 150 psig; legacy 175 psig references are superseded for this facility scope."

Do not write process-history notes such as "This was revised per SCA-005 after assessment determined prior routing assumptions were stale." When in doubt, omit the body note and record the amendment context in section QA; the trace appendix carries the full history.

## No-invention rules

- Every substantive claim must be supported by mapped CAT/KTY/KA-local artifacts or approved planning artifacts.
- Unsupported statements become `TBD`.
- Uncertain synthesis becomes an exposed conflict or explicitly labeled assumption.
- No inline `[HBK-####]`-style citations in the DBM body.
- Detailed traceability belongs in the trace appendix and section QA outputs.
- Body prose normalizes unresolved states to reader-appropriate labels: `TBD` for information not yet available, `to be confirmed` for stated but unvalidated information, and `assumed` for a value used pending confirmation. Governance-state labels such as `DEFERRED`, `BLOCKED`, `PENDING`, or `DEFERRED_CONFIRMATION` must not appear in body prose. Preserve the original epistemic state in section QA.

## Coverage expectation rules

- Every `PRIMARY` mapped KTY should contribute all material design-basis facts, tables, constraints, interfaces, assumptions, and TBDs that apply to the approved section scope unless the worker records a clear skip, insufficiency, consolidation, or deferral reason in section QA.
- One sentence per `PRIMARY` KTY is insufficient when the KTY contains multiple material facts, design-basis tables, operating cases, equipment/configuration details, or open design requirements.
- If a `PRIMARY` KTY is reduced to a token mention or one generic sentence despite containing material section-scope basis, emit `PRIMARY_KTY_COLLAPSED` in section QA.
- `SUPPORTING` artifacts qualify, constrain, or trace claims anchored by `PRIMARY` artifacts. They should not create standalone claims unless the approved section map or publication rules assign that role.
- `CONTEXT_ONLY` artifacts do not produce body claims. They may shape QA, trace, framing checks, or explicit scope exclusions.

## Section-size control

Fail fast with `FAILED_INPUTS` if:
- mapped KA count exceeds `MAX_KA_FILES`, or
- the section input set exceeds the approved size rule in `Publication_Schema.md` / `Publication_Rules.md`.

When that happens, DBM_PUBLISHER must split/refine the section design rather than forcing oversized synthesis.

## Method

1. **Validate inputs and write boundary.** Confirm all required runtime overrides are present and all output paths fall under the approved section directory.
2. **Read the frozen planning artifacts and confirm root publication admission.** Determine the section's approved structure, mapped rows, relevant publication rules, and manifest-recorded admission basis.
2a. **Read the section context packet when provided.** `SECTION_CONTEXT_PATH` is structural context, not a substitute for mapped KA content. Use it to:
   - understand why mapped KTYs matter, including objectives served and category/KTY descriptions,
   - verify completeness: does mapped KA content cover what the context packet says the section should contain,
   - check factual-use eligibility; if a mapped KTY has `FACTUAL_USE_GATE = BLOCK_FACTUAL_USE`, do not use that KTY for body claims even when the section map lists it as `PRIMARY`; treat it as `CONTEXT_ONLY` and record the override in section QA,
   - identify applicable supersession bindings before reading KA content,
   - identify open issues that should surface as body `TBD`, `to be confirmed`, or `assumed` notes.
2b. **Read the open-item packet when provided.** Use `OPEN_ITEM_PACKET` to determine section-relevant human rulings, engineering TBDs, and decomposition/publication gaps. Preserve these items in QA even when body prose flattens them for readability.
3. **Read only mapped publication inputs.** For each mapped KTY, read:
   - `Scoping.md`
   - all mapped `KA-*.md`
   - `_CONTEXT.md`
   - `_REFERENCES.md`
   - `_STATUS.md`
   - `_MEMORY.md` whenever `_STATUS.md` is read, as non-authoritative operational context only
   - optional `_DEPENDENCIES.md` only when explicitly required by the section map or publication rules
4. **Apply root-admission, readiness gates, and selector semantics.** Enforce publication-admission evidence, `MappingRole`, `ContributionScope`, KTY readiness, and publication-rule precedence.
5. **Draft the section body.** Follow the approved template for `SECTION_TYPE`, the publication rules, `DBM_OUTPUT_MODE`, the body completeness standard, expected body components, and expected design-basis table treatment. In `FULL_ENGINEERING_DBM` mode, use DBM-native engineering headings and subsections rather than QA/export artifact structures.
6. **Assess section adequacy.** Before finalizing QA, evaluate whether the section is standalone for core engineering basis, whether the DBM-native structure is adequate, whether applicable design-basis content classes were covered, whether design-basis tables were included/consolidated/split or rationally omitted, and whether `PRIMARY` KTY material was materially used.
7. **Emit stable section QA.** Use the fixed structure defined below.
8. **Return status conservatively.** Use `FAILED_INPUTS` for invalid/missing inputs or oversize sections; otherwise complete with explicit gaps/conflicts surfaced in the outputs.

## Section QA output format

`SEC-##_QA.md` must contain these blocks in order:
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
11. `## Assertion Emission Notes`
12. `## Auxiliary Structure Warnings` (present only when hypergraph evidence was consumed; each item labeled `AUXILIARY_STRUCTURE_WARNING`)

The QA artifact must preserve distinctions such as `TBD`, `ASSUMPTION`, and `DEFERRED_CONFIRMATION` even when body prose flattens unresolved items for readability.

Content expectations by block:
- `Coverage Table` records mapped KTYs/KAs consumed plus mapped inputs skipped and why.
- `Design Basis Content Coverage` records each applicable content class as `INCLUDED`, `OMITTED_WITH_RATIONALE`, `DEFERRED_UPSTREAM_MISSING`, or `NOT_APPLICABLE`, with concise rationale for omissions.
- `Table Treatment` records design-basis table handling as `INCLUDED`, `CONSOLIDATED`, `SPLIT`, `OMITTED_WITH_RATIONALE`, `TRACE_ONLY`, `DEFERRED_UPSTREAM_MISSING`, or `NONE_APPLICABLE`; `TRACE_ONLY` must not be used for body-worthy design-basis tables.
- `Section Adequacy Findings` records any fixed finding codes: `UNDERDEVELOPED_SECTION`, `UNJUSTIFIED_TABLE_OMISSION`, `PRIMARY_KTY_COLLAPSED`, `MISSING_DESIGN_BASIS_CLASS`, `QA_SCAFFOLD_BODY_LEAKAGE`, or `NON_STANDALONE_CORE_BASIS`.
- `Readiness Observations` records KTY readiness issues.
- `Conflict Register` records contradictory values/states and both mapped positions with provenance.
- `Gap / TBD Register` preserves distinctions such as human authority ruling, `TBD`, `ASSUMPTION`, `DEFERRED_CONFIRMATION`, external responsibility, and decomposition/publication gap.
