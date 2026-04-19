---
name: dbm-concordance-seed
description: Refine and augment typed concordance candidates for one approved DBM section or one bounded section group from frozen planning artifacts and mapped source content.
compatibility: Chirality TASK; dispatched by DBM_PUBLISHER after deterministic candidate generation and before freezing the blocking concordance register.
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — dbm-concordance-seed

## Purpose

Refine and augment **typed publication concordance candidates** for exactly one approved section or one bounded section group. The skill consumes the frozen publication planning artifacts plus the current candidate register, reads only the mapped source content for its assigned scope, and emits two outputs:
- one scope-local typed candidate CSV,
- one scope-local seed QA markdown file.

This skill is the reasoning layer between deterministic candidate harvesting and the final frozen `Publication_Concordance_Register.csv`. It is **not** a section writer, **not** a package gate, and **not** a dispatcher.

## Suitable agent shells

- `TASK` (generic shell mode, no profile)

Typical dispatcher: `DBM_PUBLISHER` during the concordance seeding / freeze phase.

## Inputs

### Required

- `CONCORDANCE_SCOPE_ID`
- `CONCORDANCE_SCOPE_MODE`
- `SECTION_IDS`
- `CANDIDATE_INPUT_PATH`
- `CANDIDATE_OUTPUT_PATH`
- `SEED_QA_OUTPUT_PATH`
- `PUBLICATION_INPUT_MANIFEST`
- `PUBLICATION_SCHEMA_PATH`
- `SECTION_MAP_PATH`
- `PUBLICATION_RULES_PATH`
- `MAX_KA_FILES_TOTAL`

### Optional

- `PUBLICATION_CONCORDANCE_REGISTER_PATH`
- `SOURCE_DOMAIN`
- `ALLOW_PROSE_ONLY_DISCOVERY`
- `STRICT_REQUIRED_SECTION_MATCH`

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `CONCORDANCE_SCOPE_ID` | Stable identity for this seeding run | **Required** | `SEC-##` for a single section or approved composite such as `SEC-03__SEC-04` |
| `CONCORDANCE_SCOPE_MODE` | Whether the run covers one section or a bounded group | **Required** | `SINGLE_SECTION`, `SECTION_GROUP` |
| `SECTION_IDS` | Approved section IDs included in this scope | **Required** | Non-empty list of approved section IDs |
| `CANDIDATE_INPUT_PATH` | Current deterministic or merged candidate register to refine | **Required** | Path under `_Publication/DBM/_Planning/` |
| `CANDIDATE_OUTPUT_PATH` | Output path for this scope-local refined candidate CSV | **Required** | Path under `_Publication/DBM/_Planning/` |
| `SEED_QA_OUTPUT_PATH` | Output path for this scope-local seed QA artifact | **Required** | Path under `_Publication/DBM/_Planning/` |
| `PUBLICATION_INPUT_MANIFEST` | Frozen exact input-path manifest | **Required** | Markdown path |
| `PUBLICATION_SCHEMA_PATH` | Approved publication schema | **Required** | Markdown path |
| `SECTION_MAP_PATH` | Approved section map | **Required** | CSV path |
| `PUBLICATION_RULES_PATH` | Approved publication rules | **Required** | Markdown path |
| `MAX_KA_FILES_TOTAL` | Hard cap on total mapped KA files across the scope | **Required** | Positive integer |
| `PUBLICATION_CONCORDANCE_REGISTER_PATH` | Existing frozen register to avoid duplicate key invention during reruns/expansion passes | unset | CSV path |
| `SOURCE_DOMAIN` | Source domain label for reporting | inferred | Non-empty string |
| `ALLOW_PROSE_ONLY_DISCOVERY` | Permit semantically grounded candidates discovered from prose when no structured row exists | `true` | `true`, `false` |
| `STRICT_REQUIRED_SECTION_MATCH` | Require every emitted candidate to map cleanly to the approved scope sections | `true` | `true`, `false` |

## Tool usage

- This is a reasoning-first concordance-seeding skill.
- It consumes deterministic candidate input produced upstream rather than invoking publication tools itself.
- The `allowed-tools` frontmatter field is intentionally omitted because this skill has no deterministic tool requirement of its own.

Disallowed behavior:
- No dispatching of other skills or agents.
- No mutation of any frozen planning artifact besides the two scope-local outputs named in the brief.
- No direct freezing of `Publication_Concordance_Register.csv`.
- No modification of any `CAT-* / 1_Working / KTY-*` source files.
- No use of `_Aggregation/*`, `_Coordination/*`, `_Evaluation/*`, `_Reconciliation/*`, `_MEMORY.md`, or `_SEMANTIC.md` as authority.
- No guessed assertions that are unsupported by explicit mapped content.

## Outputs

- `{CANDIDATE_OUTPUT_PATH}` — scope-local typed concordance candidate CSV
- `{SEED_QA_OUTPUT_PATH}` — scope-local concordance seed QA markdown

## Authority hierarchy

When refining or adding candidates, consult inputs in this order of authority:

1. approved `Publication_Schema.md`
2. approved `Publication_Rules.md`
3. approved `Section_Map.csv`
4. existing `Publication_Concordance_Register.csv`, when provided
5. current `Publication_Concordance_Candidates.csv`
6. frozen `Publication_Input_Manifest.md`
7. accepted scope-change state and approved decomposition state named in the manifest
8. exact mapped KTY-local files named by the section map for the assigned sections
9. vocabulary map, open-issues register, and decision log named in the manifest when required for typing, normalization, or state selection
10. original DBM source markdown as provenance/history only

## Typed concordance fields

Every emitted candidate row must preserve or fill these typed fields:

- `AssertionKey`
- `AssertionLabel`
- `AssertionDomain`
- `AssertionType`
- `CanonicalTerm`
- `Unit`
- `ComparisonRule`
- `ComparisonParameter`
- `AuthoritySectionID`
- `RequiredSectionIDs`
- `FacilityScope`
- `CurrentStateBasis`
- `DecisionRefs`
- `DiscoverySource`
- `SourceKTYIDs`
- `SourceSectionIDs`
- `NormalizationHint`
- `Criticality`
- `CandidateValueExample`
- `SourceArtifact`
- `SourceRef`
- `Notes`
- `ResolutionStatus`

### Required field semantics

- `AssertionDomain` should classify the engineering role of the candidate:
  - `PROCESS_CONDITION`
  - `UTILITY_CONDITION`
  - `PRODUCT_SPEC`
  - `EQUIPMENT_LIMIT`
  - `OPERATING_TARGET`
  - `SCOPE_STATE`
  - `LOCATION_STATE`
  - `REGULATORY_STATE`
  - `CONTROL_LOGIC`
- `DiscoverySource` should record where the candidate came from:
  - `STRUCTURED_TABLE`
  - `METADATA_FIELD`
  - `PROSE_EXTRACTION`
  - `OPEN_ISSUE`
  - `DECISION_LOG`
  - `SCOPE_CHANGE`
  - `HUMAN_ADDED`
  - `SECTION_DISCOVERY`
- `Criticality` should be one of:
  - `HIGH`
  - `NORMAL`
  - `LOW`
- `ComparisonParameter` carries rule-specific details such as rounding precision for `ROUND_N` or normalization expectations for set/range comparison.
- `NormalizationHint` should state how later section workers should normalize emitted values consistently.
- `SourceKTYIDs` should identify the KTYs supporting the candidate.
- `SourceSectionIDs` should identify the approved publication sections in scope that this candidate touches.
- `ResolutionStatus` should be one of:
  - `READY_FOR_FREEZE`
  - `NEEDS_REVIEW`
  - `DUPLICATE_CANDIDATE`
  - `OUT_OF_SCOPE`

## Candidate seeding rules

The skill should bias toward over-discovery, not under-discovery, but only when grounded in mapped content.

Always look for repeated or technically central items such as:
- pressures,
- temperatures,
- flow rates,
- compositions/specifications,
- recoveries/yields,
- capacities,
- design limits / MAWP,
- utility setpoints/conditions,
- facility/location/state assignments,
- scope/responsibility assignments,
- regulatory or compliance state,
- control/protection states repeated across sections.

Preferred discovery order:
1. deterministic candidate rows already present in `CANDIDATE_INPUT_PATH`,
2. KA metadata fields,
3. explicit design/value tables,
4. open-issues items affecting values or epistemic state,
5. decision-log entries,
6. accepted scope-change artifacts,
7. prose-only assertions from mapped KA content when `ALLOW_PROSE_ONLY_DISCOVERY=true`.

## No-invention rules

- Every emitted candidate must be supported by explicit mapped content.
- If a value or state is important but ambiguous, emit the candidate with `ResolutionStatus=NEEDS_REVIEW` rather than inventing a normalized value.
- Do not invent units, section ownership, or authority sections.
- Do not promote a prose hint into a precise numeric assertion unless the mapped text states the value.
- If a candidate duplicates an existing key but the semantic match is uncertain, preserve both with explicit duplicate notes rather than silently merging.

## Method

1. **Validate scope and write boundary.** Confirm required runtime overrides are present, all outputs fall under `_Publication/DBM/_Planning/`, and `SECTION_IDS` is non-empty.
2. **Read the frozen planning artifacts.** Determine the approved section set, section-map rows, publication rules, and current candidate baseline for this scope.
3. **Read only mapped source inputs.** For KTYs mapped to the assigned sections, read:
   - `Scoping.md`
   - mapped `KA-*.md`
   - `_CONTEXT.md`
   - `_REFERENCES.md`
   - `_STATUS.md`
   - optional `_DEPENDENCIES.md` only when section-map notes or publication rules make interface context material
4. **Apply scope and readiness discipline.** Refuse unmapped or out-of-scope content. Fail if total mapped KA count exceeds `MAX_KA_FILES_TOTAL`.
5. **Refine existing candidates first.** For candidate rows already associated with the scope, fill missing typed fields, normalize labels/keys, and mark unresolved ambiguity with `ResolutionStatus`.
6. **Add newly discovered candidates.** Add only candidates supported by mapped content and relevant to the assigned sections.
7. **Assign section ownership conservatively.** Use the approved schema and section map to propose `AuthoritySectionID` and `RequiredSectionIDs`; if authority is ambiguous, mark `NEEDS_REVIEW`.
8. **Emit stable outputs.** Write the scope-local candidate CSV and the fixed seed QA artifact.

## Seed QA output format

`*_CONCORDANCE_SEED_QA.md` must contain these blocks in order:
1. `## Scope Summary`
2. `## Inputs Consumed`
3. `## Candidate Refinements`
4. `## New Candidate Additions`
5. `## Ambiguities Requiring Review`
6. `## Duplicate / Merge Notes`
7. `## Normalization Guidance`

The QA artifact should make targeted unresolved questions obvious without requiring the human to reconstruct the candidate set from scratch.

## Candidate output format

`{CANDIDATE_OUTPUT_PATH}` must be a CSV containing at least these columns:
- `AssertionKey`
- `AssertionLabel`
- `AssertionDomain`
- `AssertionType`
- `CanonicalTerm`
- `Unit`
- `ComparisonRule`
- `ComparisonParameter`
- `AuthoritySectionID`
- `RequiredSectionIDs`
- `FacilityScope`
- `CurrentStateBasis`
- `DecisionRefs`
- `DiscoverySource`
- `SourceKTYIDs`
- `SourceSectionIDs`
- `NormalizationHint`
- `Criticality`
- `CandidateValueExample`
- `SourceArtifact`
- `SourceRef`
- `Notes`
- `ResolutionStatus`

## Failure behavior

Use `FAILED_INPUTS` when:
- required runtime overrides are missing,
- output paths fall outside `_Publication/DBM/_Planning/`,
- `SECTION_IDS` are empty or do not match the approved section map,
- total mapped KA count exceeds `MAX_KA_FILES_TOTAL`,
- the assigned scope requires inputs that are missing from the frozen planning artifacts.

Use `FAILED` when:
- a required output cannot be written despite valid inputs,
- an internal run error prevents the stable outputs from being emitted.

Even on successful runs, unresolved semantic duplicates, unclear authority assignment, or ambiguous normalization must remain explicit in the output CSV and QA markdown rather than being silently guessed.
