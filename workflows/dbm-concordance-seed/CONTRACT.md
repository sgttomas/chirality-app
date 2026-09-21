# dbm-concordance-seed contract

## Brief

This file defines the INIT-TASK dispatch contract for `TASK + dbm-concordance-seed`.

### Purpose

Use this workflow when dbm-publisher needs a bounded reasoning pass over one approved section, one small approved section group, or one review consolidation scope to transform raw evidence atoms into typed concordance candidates before the blocking register is frozen.

### Scope model

- `ScopePath` should normally be the publication planning folder:
  - `{EXECUTION_ROOT}/_Publication/DBM/_Planning/`
- `AllowedWriteTargets` must name exactly two files:
  - one scope-local concordance candidate CSV,
  - one scope-local concordance seed QA markdown file.

The brief must not grant write access to section output folders, package folders, or any KTY-local source folder.

### Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why this seeding run exists | `Refine typed concordance candidates for SEC-03 before freezing the register.` |
| `ScopePath` | path | Publication planning folder | `/abs/root/_Publication/DBM/_Planning/` |
| `Workflow` | string | Must equal the workflow folder/name | `dbm-concordance-seed` |
| `AllowedWriteTargets` | list[path] | Exact writable outputs | `[/.../concordance-seed/SEC-03_Candidates.csv, /.../concordance-seed/SEC-03_CONCORDANCE_SEED_QA.md]` |
| `RuntimeOverrides.CONCORDANCE_SCOPE_ID` | string | Stable identity for the seeding scope | `SEC-03` |
| `RuntimeOverrides.CONCORDANCE_SCOPE_MODE` | enum | Whether the run covers one section or a group | `SINGLE_SECTION` |
| `RuntimeOverrides.SECTION_IDS` | list[string] | Approved section IDs in scope | `[SEC-03]` |
| `RuntimeOverrides.EVIDENCE_ATOMS_PATH` | path | Raw evidence atoms from deterministic extraction | `/.../_Planning/Publication_Concordance_Evidence_Atoms.csv` |
| `RuntimeOverrides.RISK_INVENTORY_PATH` | path | Mechanical risk inventory to cover or waive | `/.../_Planning/Publication_Concordance_Risk_Inventory.csv` |
| `RuntimeOverrides.CANDIDATE_OUTPUT_PATH` | path | Scope-local refined candidate output | `/.../_Planning/concordance-seed/SEC-03_Candidates.csv` |
| `RuntimeOverrides.SEED_QA_OUTPUT_PATH` | path | Scope-local QA output | `/.../_Planning/concordance-seed/SEC-03_CONCORDANCE_SEED_QA.md` |
| `RuntimeOverrides.PUBLICATION_INPUT_MANIFEST` | path | Frozen input manifest | `/.../_Planning/Publication_Input_Manifest.md` |
| `RuntimeOverrides.PUBLICATION_SCHEMA_PATH` | path | Approved publication schema | `/.../_Planning/Publication_Schema.md` |
| `RuntimeOverrides.SECTION_MAP_PATH` | path | Approved section map | `/.../_Planning/Section_Map.csv` |
| `RuntimeOverrides.PUBLICATION_RULES_PATH` | path | Approved publication rules | `/.../_Planning/Publication_Rules.md` |
| `RuntimeOverrides.MAX_KA_FILES_TOTAL` | integer | Hard cap on total mapped KAs for the scope | `20` |
| `ExpectedOutputs` | list[path] | Same two planning outputs | `[/.../SEC-03_Candidates.csv, /.../SEC-03_CONCORDANCE_SEED_QA.md]` |

### Optional brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `RuntimeOverrides.CANDIDATE_INPUT_PATH` | path | Optional draft candidate input for consolidation/rerun passes | `/.../_Planning/concordance-seed/DRAFT_Candidates.csv` |
| `RuntimeOverrides.PUBLICATION_CONCORDANCE_REGISTER_PATH` | path | Existing frozen register to consult during reruns or expansion passes | `/.../_Planning/Publication_Concordance_Register.csv` |
| `RuntimeOverrides.SOURCE_DOMAIN` | string | Domain label for the run | `West_Doe_Deepcut_DBM` |
| `RuntimeOverrides.ALLOW_PROSE_ONLY_DISCOVERY` | boolean | Permit semantically grounded prose-only candidate additions | `true` |
| `RuntimeOverrides.STRICT_REQUIRED_SECTION_MATCH` | boolean | Refuse candidates that cannot be tied cleanly to the approved scope sections | `true` |
| `RuntimeOverrides.HYPERGRAPH_USE_MODE` | enum | Whether hypergraph evidence is admitted for this run | `AUXILIARY_PLANNING` |
| `RuntimeOverrides.HYPERGRAPH_SNAPSHOT_PATH` | path | Exact path to the admitted hypergraph snapshot | `/.../_Aggregation/Hypergraph/snapshot/` |
| `RuntimeOverrides.HYPERGRAPH_QA_REPORT_PATH` | path | Exact path to the hypergraph QA report | `/.../_Aggregation/Hypergraph/QA_Report.md` |
| `RuntimeOverrides.HYPERGRAPH_EVIDENCE_ROOT` | path | Root folder containing hypergraph evidence CSVs | `/.../_Aggregation/Hypergraph/evidence/` |
| `CustomInstructions` | string | Run-specific reinforcement only; must not restate the workflow contract | `Be conservative about authority-section assignment for shared utility values.` |
| `EXCLUSIONS` | list[string] | Run-local exclusions inside already-mapped artifacts | `Ignore superseded historical value table under heading X.` |

### Runtime-override guidance

- `CONCORDANCE_SCOPE_MODE=SINGLE_SECTION` should normally be used unless dbm-publisher deliberately groups a small set of tightly coupled sections.
- `SECTION_IDS` must match approved section IDs present in `Section_Map.csv`.
- `CANDIDATE_OUTPUT_PATH` and `SEED_QA_OUTPUT_PATH` must both live under `_Publication/DBM/_Planning/`.
- `PUBLICATION_CONCORDANCE_REGISTER_PATH` is optional because the initial seed pass may run before the blocking register exists.
- `EVIDENCE_ATOMS_PATH` and `RISK_INVENTORY_PATH` are required for all new hardened publication runs.
- `CANDIDATE_INPUT_PATH` is optional and should be used for review consolidation or reruns over draft candidates; candidates from preliminary over-collection must remain `NEEDS_REVIEW` until consolidated.
- `MAX_KA_FILES_TOTAL` should reflect the approved bounded-scope design, not an ad hoc worker preference.

### Recommended CustomInstructions content

Use `CustomInstructions` only for run-specific reinforcement such as:
- emphasis on a domain where concordance undercoverage is especially risky,
- reminder that a specific section should normally own authority for a family of values,
- reminder to prefer explicit ambiguity over premature key merging,
- reminder that prose-only discovery should remain conservative for a given pilot.
- risk-class focus such as `Focus this SECTION_GROUP run on UTILITY_INTERFACE risks and confirm every matching risk inventory row is covered or explicitly unresolved.`

Do not use `CustomInstructions` to recreate the workflow contract. The brief declares the selected workflow and required CONTRACT.md resource; record the loading mechanism actually used.

### Example INIT-TASK brief

```md
PURPOSE: Refine typed concordance candidates for SEC-03 before freezing the register.
ScopePath: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/
Workflow: dbm-concordance-seed
AllowedWriteTargets:
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/concordance-seed/SEC-03_Candidates.csv
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/concordance-seed/SEC-03_CONCORDANCE_SEED_QA.md
RuntimeOverrides:
  CONCORDANCE_SCOPE_ID: SEC-03
  CONCORDANCE_SCOPE_MODE: SINGLE_SECTION
  SECTION_IDS:
    - SEC-03
  EVIDENCE_ATOMS_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Concordance_Evidence_Atoms.csv
  RISK_INVENTORY_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Concordance_Risk_Inventory.csv
  CANDIDATE_OUTPUT_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/concordance-seed/SEC-03_Candidates.csv
  SEED_QA_OUTPUT_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/concordance-seed/SEC-03_CONCORDANCE_SEED_QA.md
  PUBLICATION_INPUT_MANIFEST: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Input_Manifest.md
  PUBLICATION_SCHEMA_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Schema.md
  SECTION_MAP_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Section_Map.csv
  PUBLICATION_RULES_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Rules.md
  MAX_KA_FILES_TOTAL: 20
  ALLOW_PROSE_ONLY_DISCOVERY: true
ExpectedOutputs:
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/concordance-seed/SEC-03_Candidates.csv
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/concordance-seed/SEC-03_CONCORDANCE_SEED_QA.md
```

## Acceptance

### Minimum output validity checks

The run is valid only when all of the following are true:

1. Both required outputs exist:
   - one scope-local typed candidate CSV,
   - one scope-local concordance seed QA markdown file.
2. All writes stayed inside the approved `_Publication/DBM/_Planning/` paths named in the brief.
3. The candidate CSV contains the required typed columns, including:
   - `AssertionDomain`
   - `DiscoverySource`
   - `SourceKTYIDs`
   - `SourceSectionIDs`
   - `NormalizationHint`
   - `NormalizationContract`
   - `Criticality`
   - `ComparisonParameter`
   - `SourceFidelityCritical`
   - `SourceExpectedValue`
4. Every emitted row is tied to at least one approved section in `SECTION_IDS` through `AuthoritySectionID`, `RequiredSectionIDs`, or `SourceSectionIDs`, unless `ResolutionStatus=OUT_OF_SCOPE`.
5. `AssertionKey` values are stable uppercase snake case and do not encode ad hoc section-local prose.
6. Unsupported or ambiguous candidates remain explicit as `NEEDS_REVIEW`, `DUPLICATE_CANDIDATE`, or `OUT_OF_SCOPE` rather than being silently normalized into false certainty.
7. New candidate additions are grounded in mapped source content and do not rely on non-authoritative roots such as `_MEMORY.md` or `_SEMANTIC.md`.
8. The QA artifact uses the required stable block structure in the required order.
9. Every emitted candidate with `ResolutionStatus=READY_FOR_FREEZE` has a non-empty `NormalizationContract`.
10. Every evidence atom with `SOURCE_AUTHORITY` that the workflow deems concordance-relevant has `SourceFidelityCritical=YES` and a populated `SourceExpectedValue` in the emitted candidate.

### Required QA artifact structure

`*_CONCORDANCE_SEED_QA.md` must contain these H2 headings in this order:

1. `## Scope Summary`
2. `## Inputs Consumed`
3. `## Candidate Refinements`
4. `## New Candidate Additions`
5. `## Ambiguities Requiring Review`
6. `## Duplicate / Merge Notes`
7. `## Normalization Guidance`

Content expectations by block:
- `Inputs Consumed` records candidate input path, planning artifacts consulted, sections covered, and mapped source inputs materially used.
- `Candidate Refinements` records existing candidate rows that were materially completed or corrected.
- `New Candidate Additions` records genuinely added candidates and their engineering rationale.
- `Ambiguities Requiring Review` records unresolved authority ownership, semantic duplication, or normalization uncertainty.
- `Duplicate / Merge Notes` records rows that look semantically related but were not safely merged.
- `Normalization Guidance` records how later section workers should normalize comparison values consistently.

### Required candidate CSV schema

`{CANDIDATE_OUTPUT_PATH}` must contain at least these columns:
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

Allowed `ResolutionStatus` values:
- `READY_FOR_FREEZE`
- `NEEDS_REVIEW`
- `DUPLICATE_CANDIDATE`
- `OUT_OF_SCOPE`

Additional checks:
- `Criticality` must be one of `HIGH`, `NORMAL`, or `LOW`.
- `DiscoverySource` must record whether the row came from structured data, prose extraction, open issues, decision log, scope change, or another approved source class.
- `ComparisonParameter` must be populated when `ComparisonRule` requires extra rule detail such as rounding precision.
- `SourceKTYIDs` and `SourceSectionIDs` must identify the mapped source/support footprint for the row.
- `NormalizationHint` must be present whenever a later section worker could normalize the same value in multiple valid ways.
- `NormalizationContract` must be present for `READY_FOR_FREEZE` rows.
- `SourceFidelityCritical=YES` rows must include `SourceExpectedValue` or remain `NEEDS_REVIEW`.

### Failure reporting expectations

Use `FAILED_INPUTS` when:
- required runtime overrides are missing,
- output paths fall outside `_Publication/DBM/_Planning/`,
- `SECTION_IDS` do not match the approved section map,
- the mapped input set exceeds `MAX_KA_FILES_TOTAL`,
- required planning artifacts or candidate input files are missing.

Use `FAILED` when:
- a required output cannot be written despite valid inputs,
- an internal run error prevents the stable outputs from being emitted.

Even on successful runs, QA must surface:
- unresolved authority-section ownership,
- unresolved duplicate candidates,
- ambiguous normalization behavior,
- material open-issue / decision-log / SCA dependencies,
- any candidates deliberately left `OUT_OF_SCOPE`.

## Tool use

### Preferred tool order

1. Read the frozen publication planning artifacts, evidence atoms, risk inventory, and any optional draft candidate input.
2. Read only the mapped KTY-local files permitted by the approved section map for the assigned sections.
3. Use direct reasoning to transform evidence atoms into typed candidates, refine draft candidates when provided, and add grounded new candidates.
4. Write exactly one scope-local candidate CSV and one scope-local QA markdown file.

### Allowed deterministic tools

#### Operationally invoked

None by this workflow. It consumes deterministic evidence atoms and risk inventory produced upstream rather than invoking tools itself.

### Expected use of reasoning

This workflow is reasoning-heavy. It must:
- interpret raw evidence atoms and risk inventory rows in light of the approved section map and publication rules,
- infer appropriate typed fields such as `AssertionDomain`, `ComparisonRule`, `ComparisonParameter`, `NormalizationHint`, `NormalizationContract`, and `Criticality` from explicit mapped content,
- propose authority / required-section ownership conservatively,
- preserve ambiguity as `NEEDS_REVIEW` rather than inventing certainty,
- distinguish genuine new candidates from duplicates or out-of-scope noise.

### Disallowed use

- No dispatching of other workflows or agents.
- No use of `_Aggregation/*`, `_Coordination/*`, `_Evaluation/*`, `_Reconciliation/*`, `_MEMORY.md`, or `_SEMANTIC.md` as concordance authority. `_MEMORY.md` may be read only as non-authoritative operational context when `_STATUS.md` is read.
- No mutation of `Publication_Concordance_Register.csv`, `Publication_Concordance_Evidence_Atoms.csv`, `Publication_Concordance_Risk_Inventory.csv`, `Section_Map.csv`, or any other frozen planning artifact besides the two scope-local outputs named in the brief.
- No writing to section output folders, package folders, or KTY-local source folders.
- No section-body authoring or package-readiness judgment.

### Write boundary

The workflow may write only:
- one scope-local concordance candidate CSV,
- one scope-local concordance seed QA markdown file.

Both writes must remain inside `_Publication/DBM/_Planning/` and within the exact paths named by the INIT-TASK brief.
