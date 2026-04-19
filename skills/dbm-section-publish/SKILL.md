---
name: dbm-section-publish
description: Publish exactly one rewritten DBM section from approved mapped DOMAIN inputs and emit fixed QA plus concordance assertion artifacts.
compatibility: Chirality TASK; dispatched by DBM_PUBLISHER after the publication planning artifacts are frozen.
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — dbm-section-publish

## Purpose

Publish **exactly one target DBM section** from approved mapped inputs. The skill consumes frozen publication planning artifacts, reads only the mapped KTY-local sources for its assigned section, and emits four outputs:
- one section body,
- one section QA artifact,
- one section assertions CSV,
- one section assertion-discovery CSV.

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
- `SECTION_ASSERTIONS_OUTPUT_PATH`
- `SECTION_ASSERTION_DISCOVERY_OUTPUT_PATH`
- `PUBLICATION_INPUT_MANIFEST`
- `PUBLICATION_SCHEMA_PATH`
- `SECTION_MAP_PATH`
- `PUBLICATION_RULES_PATH`
- `PUBLICATION_CONCORDANCE_REGISTER_PATH`
- `MAX_KA_FILES`

### Optional

- `SOURCE_DOMAIN`
- `SECTION_ORDER`
- `ALLOW_CONTEXT_ONLY_DECOMP_FALLBACK` — `true|false`, default `true`

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `SECTION_ID` | Stable section identity for this run | **Required** | `SEC-##` or approved equivalent |
| `SECTION_TITLE` | Approved section title | **Required** | Non-empty string |
| `SECTION_TYPE` | Approved section taxonomy | **Required** | `OVERVIEW`, `PROCESS_BASIS`, `PHILOSOPHY`, `DATA_REFERENCE`, `DISCIPLINE_BASIS`, `REGULATORY` |
| `SECTION_PURPOSE` | Human-approved intent for the section | **Required** | Non-empty string |
| `SECTION_OUTPUT_PATH` | Output path for the section body | **Required** | Path under `_Publication/DBM/sections/{SECTION_ID}/` |
| `SECTION_QA_OUTPUT_PATH` | Output path for stable QA markdown | **Required** | Path under `_Publication/DBM/sections/{SECTION_ID}/` |
| `SECTION_ASSERTIONS_OUTPUT_PATH` | Output path for structured assertion rows | **Required** | Path under `_Publication/DBM/sections/{SECTION_ID}/` |
| `SECTION_ASSERTION_DISCOVERY_OUTPUT_PATH` | Output path for structured assertion-discovery rows | **Required** | Path under `_Publication/DBM/sections/{SECTION_ID}/` |
| `PUBLICATION_INPUT_MANIFEST` | Frozen exact input-path manifest | **Required** | Markdown path |
| `PUBLICATION_SCHEMA_PATH` | Approved publication schema | **Required** | Markdown path |
| `SECTION_MAP_PATH` | Approved section map | **Required** | CSV path |
| `PUBLICATION_RULES_PATH` | Approved publication rules | **Required** | Markdown path |
| `PUBLICATION_CONCORDANCE_REGISTER_PATH` | Approved concordance register | **Required** | CSV path |
| `MAX_KA_FILES` | Hard cap on mapped KA files for this section | **Required** | Positive integer |
| `SOURCE_DOMAIN` | Source domain label for the run | inferred | Non-empty string |
| `SECTION_ORDER` | Display/assembly order | inferred | Positive integer |
| `ALLOW_CONTEXT_ONLY_DECOMP_FALLBACK` | Allow decomposition-level context when a `CONTEXT_ONLY` KTY is below readiness threshold | `true` | `true`, `false` |

## Tool usage

- This is a reasoning-first synthesis skill.
- It consumes deterministic planning artifacts produced outside the skill.
- The `allowed-tools` frontmatter field is intentionally omitted because this skill has no deterministic tool requirements of its own.

Disallowed behavior:
- No dispatching other tasks.
- No writes outside the four section output paths.
- No modification of any `CAT-* / 1_Working / KTY-*` files.
- No guessed discovery outside the frozen planning artifacts and approved section-map rows.
- No use of `_MEMORY.md` or `_SEMANTIC.md` as authority.

## Outputs

- `{SECTION_OUTPUT_PATH}` — one rewritten DBM section body
- `{SECTION_QA_OUTPUT_PATH}` — stable section QA artifact
- `{SECTION_ASSERTIONS_OUTPUT_PATH}` — stable section assertion rows for concordance checking
- `{SECTION_ASSERTION_DISCOVERY_OUTPUT_PATH}` — stable assertion-discovery rows for package-level concordance expansion

## Authority hierarchy

When synthesizing a section, consult inputs in this order of authority:

1. approved `Publication_Schema.md`
2. approved `Publication_Rules.md`
3. approved `Section_Map.csv`
4. approved `Publication_Concordance_Register.csv`
5. frozen `Publication_Input_Manifest.md`
6. accepted scope-change state and approved decomposition state named in the manifest
7. exact mapped KTY-local files named in the section map
8. vocabulary map, decision log, and open-issues register named in the manifest when required by the mapped rows or QA/assertion work
9. original DBM source markdown as provenance/history only

## Mapping behavior definitions

### `MappingRole`

- `PRIMARY` — main source material that anchors section narrative and structure
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

## KTY readiness gates

The skill must read each mapped KTY `_STATUS.md` before using its files.

Minimum rules:
- `PRIMARY` and `CONFLICTING` inputs must be at least `INITIALIZED`.
- If a `PRIMARY` input is below that threshold, fail with `FAILED_INPUTS`.
- If a `CONFLICTING` input is below that threshold, fail with `FAILED_INPUTS`.
- If a `SUPPORTING` input is below that threshold, skip it and record a gap note in section QA.
- If a `CONTEXT_ONLY` input is below that threshold, the skill may fall back to decomposition-level context only when `ALLOW_CONTEXT_ONLY_DECOMP_FALLBACK=true`, with a QA note.

The skill must not treat an `OPEN` or otherwise unready KTY as equivalent to a fully authored source artifact.

## Terminology control

When the manifest provides a vocabulary map, the skill should:
- prefer the canonical term over KA-local synonyms,
- retain a synonym in parentheses only when it materially helps recognition,
- avoid mixed terminology for the same system within one section.

## Cross-facility synthesis rules

1. If multiple mapped artifacts agree, synthesize them into one coherent narrative.
2. If mapped artifacts differ:
   - do not reconcile silently,
   - if an accepted SCA or explicit publication rule resolves the difference, publish the resolved current-state position and record the prior state in QA or trace notes,
   - otherwise record a publication conflict in section QA and use cautious wording in the narrative.
3. If a system exists in only one facility/domain, scope the section explicitly to that facility.
4. If a system moved between facilities due to accepted SCA, present the post-SCA arrangement as current-state content and keep prior placement only as audit context.
5. If content is absent for a facility, do not invent parity; use `TBD` or an explicit scope note.

## No-invention rules

- Every substantive claim must be supported by mapped source artifacts.
- Unsupported statements become `TBD`.
- Uncertain synthesis becomes an exposed conflict or explicitly labeled assumption.
- No inline `[HBK-####]`-style citations in the DBM body.
- Detailed traceability belongs in the trace appendix and section QA outputs.

## Section-size control

Fail fast with `FAILED_INPUTS` if:
- mapped KA count exceeds `MAX_KA_FILES`, or
- the section input set exceeds the approved size rule in `Publication_Schema.md` / `Publication_Rules.md`.

When that happens, DBM_PUBLISHER must split/refine the section design rather than forcing oversized synthesis.

## Method

1. **Validate inputs and write boundary.** Confirm all required runtime overrides are present and all output paths fall under the approved section directory.
2. **Read the five frozen planning artifacts.** Determine the section's approved structure, mapped rows, relevant publication rules, and relevant concordance assertions.
3. **Read only mapped source inputs.** For each mapped KTY, read:
   - `Scoping.md`
   - all mapped `KA-*.md`
   - `_CONTEXT.md`
   - `_REFERENCES.md`
   - `_STATUS.md`
   - optional `_DEPENDENCIES.md` only when explicitly required by the section map or publication rules
4. **Apply readiness gates and selector semantics.** Enforce `MappingRole`, `ContributionScope`, readiness, and publication-rule precedence.
5. **Draft the section body.** Follow the approved template for `SECTION_TYPE` and the publication rules.
6. **Emit stable section QA.** Use the fixed structure defined below.
7. **Emit required structured assertions conservatively.** Filter the concordance register to rows where `SECTION_ID` is the authority section or appears in `RequiredSectionIDs`, then emit exactly one row per matched assertion key in `SEC-##_ASSERTIONS.csv`. Do not silently drop matched keys; if value extraction is ambiguous, emit the row with explicit uncertainty in `Notes`.
8. **Emit assertion discovery candidates.** After required-key emission, search mapped content for repeated or technically important values/states not already represented in the approved register for this section scope. Emit those candidates in `SEC-##_ASSERTION_DISCOVERY.csv` rather than silently ignoring them.
9. **Return status conservatively.** Use `FAILED_INPUTS` for invalid/missing inputs or oversize sections; otherwise complete with explicit gaps/conflicts surfaced in the outputs.

## Section QA output format

`SEC-##_QA.md` must contain these blocks in order:
1. `## Section Summary`
2. `## Coverage Table`
3. `## Readiness Observations`
4. `## Conflict Register`
5. `## Terminology Notes`
6. `## Gap / TBD Register`
7. `## Amendment Notes`
8. `## Assertion Emission Notes`

The QA artifact must preserve distinctions such as `TBD`, `ASSUMPTION`, and `DEFERRED_CONFIRMATION` even when body prose flattens unresolved items for readability.

Content expectations by block:
- `Coverage Table` records mapped KTYs/KAs consumed plus mapped inputs skipped and why.
- `Readiness Observations` records KTY readiness issues.
- `Conflict Register` records contradictory values/states and both source positions.
- `Gap / TBD Register` preserves distinctions such as `TBD`, `ASSUMPTION`, and `DEFERRED_CONFIRMATION`.
- `Assertion Emission Notes` records required assertions emitted, unclear or unresolved matched keys, normalization issues, and discovery candidates proposed.

## Section assertions output format

`SEC-##_ASSERTIONS.csv` minimum columns:
- `SectionID`
- `AssertionKey`
- `AssertionStatus`
- `DisplayValue`
- `NormalizedValue`
- `Units`
- `SourceArtifact`
- `SourceRef`
- `SCARefs`
- `DecisionRefs`
- `Notes`

Supported `AssertionStatus` values:
- `ASSERTED`
- `REFERRED`
- `NOT_APPLICABLE`
- `CONFLICT_UNRESOLVED`

Rules:
- If the section is listed in `RequiredSectionIDs`, it must emit one row for that assertion key.
- If the section is the `AuthoritySectionID`, it must emit the authoritative asserted value/state unless the source state is genuinely unresolved.
- `NormalizedValue` must be suitable for deterministic comparison under the register's `ComparisonRule`.
- Prefer `REFERRED` over duplicated restatement when the publication rules designate another section as authority.
- Do not use `NOT_APPLICABLE` for a matched key unless the section map or publication rules clearly exclude that assertion from this section's current scope.
- If competing mapped inputs cannot be resolved under approved authority, use `CONFLICT_UNRESOLVED` and surface the issue in section QA.

## Section assertion discovery output format

`SEC-##_ASSERTION_DISCOVERY.csv` minimum columns:
- `SectionID`
- `SuggestedAssertionKey`
- `AssertionLabel`
- `AssertionDomain`
- `AssertionType`
- `SuggestedComparisonRule`
- `SuggestedComparisonParameter`
- `SuggestedAuthoritySectionID`
- `SuggestedRequiredSectionIDs`
- `Criticality`
- `DiscoverySource`
- `CandidateValueExample`
- `SourceArtifact`
- `SourceRef`
- `Notes`

Discovery rules:
- Emit discovery rows only for materially repeated or technically important values/states not already covered by the approved register for this section scope.
- Prefer typed candidates such as process conditions, utility conditions, product specs, equipment limits, operating targets, scope state, location state, regulatory state, and control logic.
- `SuggestedAssertionKey` should use stable uppercase snake case and remain semantic rather than section-derived.
- If the worker is unsure whether a candidate is already covered semantically, still emit it and explain the ambiguity in `Notes`.
