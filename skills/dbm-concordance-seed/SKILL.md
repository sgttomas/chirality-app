---
name: dbm-concordance-seed
description: Transform raw concordance evidence atoms and risk inventory rows into typed publication concordance candidates for register freeze review.
compatibility: Chirality TASK; dispatched by DBM_PUBLISHER after deterministic evidence extraction and before freezing the blocking concordance register.
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
  chirality-skill-status: LEGACY
---

# SKILL — dbm-concordance-seed

## Purpose

Transform raw concordance evidence atoms into **typed publication concordance candidates** for exactly one approved section, bounded section group, or strong-model consolidation pass. The deterministic tool produces raw evidence atoms with provenance and mechanical risk signals. This skill is the sole owner of determining which evidence atoms are concordance-relevant, type/domain classification, criticality assessment, authority section selection, comparison rule selection, normalization contract population, and source/reference-fidelity-critical designation.

The skill consumes the frozen publication planning artifacts plus evidence atoms and the risk inventory, reads only the mapped publication inputs for its assigned scope, and emits two outputs:
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
- `EVIDENCE_ATOMS_PATH`
- `RISK_INVENTORY_PATH`
- `CANDIDATE_OUTPUT_PATH`
- `SEED_QA_OUTPUT_PATH`
- `PUBLICATION_INPUT_MANIFEST`
- `PUBLICATION_SCHEMA_PATH`
- `SECTION_MAP_PATH`
- `PUBLICATION_RULES_PATH`
- `MAX_KA_FILES_TOTAL`

### Optional

- `CANDIDATE_INPUT_PATH` — optional draft candidate input for consolidation/rerun passes
- `PUBLICATION_CONCORDANCE_REGISTER_PATH`
- `SOURCE_DOMAIN`
- `ALLOW_PROSE_ONLY_DISCOVERY`
- `STRICT_REQUIRED_SECTION_MATCH`
- `HYPERGRAPH_USE_MODE`
- `HYPERGRAPH_SNAPSHOT_PATH`
- `HYPERGRAPH_QA_REPORT_PATH`
- `HYPERGRAPH_EVIDENCE_ROOT`

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `CONCORDANCE_SCOPE_ID` | Stable identity for this seeding run | **Required** | `SEC-##` for a single section or approved composite such as `SEC-03__SEC-04` |
| `CONCORDANCE_SCOPE_MODE` | Whether the run covers one section or a bounded group | **Required** | `SINGLE_SECTION`, `SECTION_GROUP` |
| `SECTION_IDS` | Approved section IDs included in this scope | **Required** | Non-empty list of approved section IDs |
| `EVIDENCE_ATOMS_PATH` | Raw evidence atoms from `extract_concordance_evidence.py` | **Required** | `Publication_Concordance_Evidence_Atoms.csv` under `_Publication/DBM/_Planning/` |
| `RISK_INVENTORY_PATH` | Mechanical risk inventory to cover or waive | **Required** | `Publication_Concordance_Risk_Inventory.csv` under `_Publication/DBM/_Planning/` |
| `CANDIDATE_OUTPUT_PATH` | Output path for this scope-local refined candidate CSV | **Required** | Path under `_Publication/DBM/_Planning/` |
| `SEED_QA_OUTPUT_PATH` | Output path for this scope-local seed QA artifact | **Required** | Path under `_Publication/DBM/_Planning/` |
| `PUBLICATION_INPUT_MANIFEST` | Frozen exact input-path manifest | **Required** | Markdown path |
| `PUBLICATION_SCHEMA_PATH` | Approved publication schema | **Required** | Markdown path |
| `SECTION_MAP_PATH` | Approved section map | **Required** | CSV path |
| `PUBLICATION_RULES_PATH` | Approved publication rules | **Required** | Markdown path |
| `MAX_KA_FILES_TOTAL` | Hard cap on total mapped KA files across the scope | **Required** | Positive integer |
| `CANDIDATE_INPUT_PATH` | Optional existing draft candidates to refine during consolidation/rerun passes | unset | CSV path under `_Publication/DBM/_Planning/` |
| `PUBLICATION_CONCORDANCE_REGISTER_PATH` | Existing frozen register to avoid duplicate key invention during reruns/expansion passes | unset | CSV path |
| `SOURCE_DOMAIN` | Source domain label for reporting | inferred | Non-empty string |
| `ALLOW_PROSE_ONLY_DISCOVERY` | Permit semantically grounded candidates discovered from prose when no structured row exists | `true` | `true`, `false` |
| `STRICT_REQUIRED_SECTION_MATCH` | Require every emitted candidate to map cleanly to the approved scope sections | `true` | `true`, `false` |
| `HYPERGRAPH_USE_MODE` | Whether hypergraph evidence is admitted for this run | `NONE` | `NONE`, `AUXILIARY_PLANNING`, `AUXILIARY_QA`, `AUXILIARY_PLANNING_AND_QA` |
| `HYPERGRAPH_SNAPSHOT_PATH` | Exact path to the admitted hypergraph snapshot | unset | Path under `_Aggregation/Hypergraph/` |
| `HYPERGRAPH_QA_REPORT_PATH` | Exact path to the hypergraph QA report | unset | Path |
| `HYPERGRAPH_EVIDENCE_ROOT` | Root folder containing hypergraph evidence CSVs | unset | Path under `_Aggregation/Hypergraph/` |

## Tool usage

- This is a reasoning-first concordance-seeding skill.
- It consumes deterministic candidate input produced upstream rather than invoking publication tools itself.
- The `allowed-tools` frontmatter field is intentionally omitted because this skill has no deterministic tool requirement of its own.

Disallowed behavior:
- No dispatching of other skills or agents.
- No mutation of any frozen planning artifact besides the two scope-local outputs named in the brief.
- No direct freezing of `Publication_Concordance_Register.csv`.
- No modification of any `CAT-* / 1_Working / KTY-*` input files.
- No use of `_Aggregation/*`, `_Coordination/*`, `_Evaluation/*`, `_Reconciliation/*`, `_MEMORY.md`, or `_SEMANTIC.md` as factual authority (exception: admitted hypergraph evidence under `_Aggregation/Hypergraph/` may be consumed as auxiliary structure evidence when `HYPERGRAPH_USE_MODE != NONE`). When this skill reads `_STATUS.md`, it must also read sibling `_MEMORY.md` when present as non-authoritative operational context.
- No guessed assertions that are unsupported by explicit mapped content. Hypergraph evidence may suggest candidates but cannot supply assertion values.

## Outputs

- `{CANDIDATE_OUTPUT_PATH}` — scope-local typed concordance candidate CSV
- `{SEED_QA_OUTPUT_PATH}` — scope-local concordance seed QA markdown

## Authority hierarchy

When refining or adding candidates, consult inputs in this order of authority:

1. approved `Publication_Schema.md`
2. approved `Publication_Rules.md`
3. approved `Section_Map.csv`
4. existing `Publication_Concordance_Register.csv`, when provided
5. current `Publication_Concordance_Evidence_Atoms.csv` and `Publication_Concordance_Risk_Inventory.csv`
6. frozen `Publication_Input_Manifest.md`
7. accepted scope-change state and approved decomposition state named in the manifest
8. exact mapped KTY-local files named by the section map for the assigned sections
9. vocabulary map, open-issues register, and decision log named in the manifest when required for typing, normalization, or state selection
10. original/reference markdown and reference/provenance tables as reference/provenance only; they do not override accepted DOMAIN/SCA state or mapped CAT/KTY/KA-local content

## Hypergraph evidence policy

**Authority statement:** Hypergraph evidence is auxiliary structure evidence only. It does not replace the content authority hierarchy defined above.

When `HYPERGRAPH_USE_MODE` includes planning (`AUXILIARY_PLANNING` or `AUXILIARY_PLANNING_AND_QA`) and `HYPERGRAPH_SNAPSHOT_PATH` and `HYPERGRAPH_EVIDENCE_ROOT` are provided, the skill may use hypergraph evidence to:
- suggest repeated-value/assertion clusters by identifying structural patterns across KTYs,
- identify additional participant sections that the deterministic tool may have missed,
- identify likely missing concordance candidates implied by graph adjacency.

The skill must not:
- invent assertion values from graph topology (e.g., deriving a numeric value from node/edge counts or labels),
- prefer graph structure over mapped CAT/KTY/KA-local content when the two conflict.

When a candidate row is discovered or strengthened by hypergraph evidence, it must be tagged with `DiscoverySource = HYPERGRAPH_AUXILIARY`. The seed QA output should note which candidates were influenced by hypergraph evidence and what structural pattern motivated the suggestion.

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
- `NormalizationContract` — machine-readable normalization specification section workers must follow. Use forms such as `ROUND_N:2`, `TOKEN_MATCH`, `EXACT`, `RANGE_MATCH`, or `SET_MATCH`.
- `Criticality`
- `CandidateValueExample`
- `SourceArtifact`
- `SourceRef`
- `SourceFidelityCritical` — `YES` when this key represents a value that should be checked against admitted reference/provenance material at Gate 6 for traceability and conflict detection. Use `YES` for equipment counts, specification values, scope inclusion/exclusion decisions, and any value where unexplained reference-vs-publication divergence would be a material error. Use `NO` for structural/organizational keys that don't have a direct reference counterpart.
- `SourceExpectedValue` — the normalized expected value from admitted reference/provenance material, when `SourceFidelityCritical = YES`. Extract this from admitted reference/provenance files (narrative or canonical CSVs) during seeding when a direct counterpart exists. Leave empty when the key has no direct counterpart or when `SourceFidelityCritical = NO`.
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
  - `HYPERGRAPH_AUXILIARY`
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

The skill should bias toward over-discovery, not under-discovery, but only when grounded in evidence atoms or mapped content.

Two-tier model guidance:
- Smaller models may be used only for per-section over-collection. Those outputs must be marked `NEEDS_REVIEW` and are not eligible for register freeze.
- Strong-model consolidation is required for any output eligible for register freeze. Only rows reviewed by the strong-model consolidation pass and marked `READY_FOR_FREEZE` may be merged into `Publication_Concordance_Register.csv`.
- Risk-class sweeps always require a strong model because they require cross-section reasoning and multi-KTY context.

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
1. evidence atoms in `EVIDENCE_ATOMS_PATH`, using `NearbyContext`, `HeadingPath`, `TableCaption`, and `RiskSignals`,
2. risk inventory rows in `RISK_INVENTORY_PATH`,
3. draft candidate rows already present in `CANDIDATE_INPUT_PATH`, when provided,
4. KA metadata fields,
5. explicit design/value tables,
6. open-issues items affecting values or epistemic state,
7. decision-log entries,
8. accepted scope-change artifacts,
9. prose-only assertions from mapped KA content when `ALLOW_PROSE_ONLY_DISCOVERY=true`.

When an evidence atom carries the legacy `SOURCE_AUTHORITY` extraction signal and the skill determines the atom is concordance-critical, treat it as reference/provenance evidence: set `SourceFidelityCritical=YES` and populate `SourceExpectedValue` from the atom's `RawValue` after applying the candidate's `NormalizationContract`.

When the dispatcher provides `CustomInstructions` naming a specific risk class, prioritize all risk inventory rows of that class within the scoped sections and verify that each is covered by a candidate, waived, deferred as blocking, or explicitly out of scope.

## No-invention rules

- Every emitted candidate must be supported by explicit mapped content.
- If a value or state is important but ambiguous, emit the candidate with `ResolutionStatus=NEEDS_REVIEW` rather than inventing a normalized value.
- Do not invent units, section ownership, or authority sections.
- Do not promote a prose hint into a precise numeric assertion unless the mapped text states the value.
- If a candidate duplicates an existing key but the semantic match is uncertain, preserve both with explicit duplicate notes rather than silently merging.

## Method

1. **Validate scope and write boundary.** Confirm required runtime overrides are present, all outputs fall under `_Publication/DBM/_Planning/`, and `SECTION_IDS` is non-empty.
2. **Read the frozen planning artifacts.** Determine the approved section set, section-map rows, publication rules, evidence atom baseline, risk inventory, and optional draft candidate baseline for this scope.
3. **Read only mapped publication inputs.** For KTYs mapped to the assigned sections, read:
   - `Scoping.md`
   - mapped `KA-*.md`
   - `_CONTEXT.md`
   - `_REFERENCES.md`
   - `_STATUS.md`
   - `_MEMORY.md` whenever `_STATUS.md` is read, as non-authoritative operational context only
   - optional `_DEPENDENCIES.md` only when section-map notes or publication rules make interface context material
4. **Apply scope and readiness discipline.** Refuse unmapped or out-of-scope content. Fail if total mapped KA count exceeds `MAX_KA_FILES_TOTAL`.
5. **Transform evidence atoms into candidates.** Use atom context and risk signals to decide which atoms represent concordance-worthy values, states, or relationships.
6. **Refine existing draft candidates when provided.** Fill missing typed fields, normalize labels/keys, and mark unresolved ambiguity with `ResolutionStatus`.
7. **Add newly discovered candidates.** Add only candidates supported by evidence atoms or mapped content and relevant to the assigned sections.
8. **Assign section ownership conservatively.** Use the approved schema and section map to propose `AuthoritySectionID` and `RequiredSectionIDs`; if authority is ambiguous, mark `NEEDS_REVIEW`.
9. **Populate normalization and source-fidelity fields.** Every `READY_FOR_FREEZE` row must have `NormalizationContract`; reference-fidelity-critical rows must have `SourceFidelityCritical=YES` and `SourceExpectedValue` when a direct admitted reference counterpart exists.
10. **Emit stable outputs.** Write the scope-local candidate CSV and the fixed seed QA artifact.

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
- `NormalizationContract`
- `Criticality`
- `CandidateValueExample`
- `SourceArtifact`
- `SourceRef`
- `SourceFidelityCritical`
- `SourceExpectedValue`
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
