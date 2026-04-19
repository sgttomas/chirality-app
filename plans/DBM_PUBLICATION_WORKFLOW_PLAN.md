# Plan: DBM Publication Workflow From Approved DOMAIN State

## Status

Recommended for implementation planning. Not yet implemented.

## Purpose

Design a new Chirality workflow that rewrites a canonical Design Basis
Memorandum (DBM) from approved DOMAIN state.

This workflow is not a reverse mode of `DOMAIN_DECOMP`, and it is not a thin
variant of `domain-documents`.

It solves a different problem:

- `DOMAIN_DECOMP` normalizes source material into a governed domain structure.
- `domain-documents` materializes KTY-local knowledge artifacts from that
  structure.
- The new workflow publishes a new top-level engineering document from the
  approved domain state, using a human-approved target structure.

The publication authority is:

1. approved publication schema
2. accepted decomposition state
3. accepted scope changes merged into that state
4. KTY-local `Scoping.md` and `KA-*.md` artifacts
5. original source DBM only as provenance and historical reference

## Warranted Changes To The Prior Draft

Starting from the beginning of this session, the prior draft should be changed
in these ways:

1. The workflow should be explicitly **one execution root -> one rewritten DBM**
   in v1.
   Do not treat cross-domain consolidated publication as a core requirement.
   The workflow should be reusable across domains, but each run should target a
   single domain execution root unless a later requirement explicitly expands
   scope.

2. `dbm-publish` must **not** be described as a TASK skill that dispatches
   other TASK workers.
   `TASK` skills are bounded method packs, not orchestration layers.
   The Type 1 persona should dispatch section workers directly, then optionally
   dispatch a package-level TASK skill for final assembly and QA.

3. The new persona's write scope should not be `repo-metadata-only`.
   It should be **tool-root-only**, writing only to a new publication tool root
   under the domain execution root.

4. Scope-change resolution should not be left implicit.
   The workflow needs an explicit **Publication Input Manifest** that freezes
   the exact decomposition files, active `_ScopeChange/_LATEST.md` pointer,
   active amendment snapshot(s), and source DBM/TOC paths before any section
   synthesis begins.

5. The new workflow must not repeat the loose decomposition-file discovery
   assumptions seen in some existing DOMAIN methods.
   The two West Doe domains use different `_Decomposition` file naming
   conventions and do not expose a uniform `_Decomposition/Data/` layout.
   The publication workflow must consume explicit paths from the frozen input
   manifest, not guessed filenames.

6. A publication style and voice contract must be explicit.
   The human asked for a rewritten DBM, not a stitched artifact dump.
   Style, tone, section voice, amendment-note behavior, and traceability
   presentation need to be frozen in `Publication_Rules.md`.

7. `build_section_map.py` must not be asked to interpret free-text section
   rules.
   `Publication_Schema.md` should carry both human-readable section intent and
   machine-readable selector fields. The tool should generate a candidate
   section map from those selectors, then validate it. The persona and human
   should approve the final `Section_Map.csv`.

8. `DBM_PUBLISHER` needs explicit placement in the agent matrix.
   It should be added to `AGENTS.md` as an `EVALUATIVE x APPLYING` persona.

9. The persona needs a defined knowledge-landscape review method before schema
   design begins.
   The human should not be asked to design a target DBM structure blind.

10. Section-worker behavior must be more explicit than the prior draft.
    `MappingRole`, `ContributionScope`, KTY readiness gates, vocabulary-map
    usage, and oversized-section handling should be part of the skill contract,
    not left to worker improvisation.

11. Deterministic completeness and concordance checks belong in deterministic
    tools, but `dbm-publish` should remain in v1 as the package-quality gate.
    `assemble_publication.py` should own deterministic section-count, trace,
    and package-consistency validation. `check_concordance.py` should own
    deterministic cross-section assertion concordance checks. `dbm-publish`
    should invoke those tools, read their outputs, and produce a
    publication-readiness judgment before first human review.

12. Cross-section concordance must be a v1 hard gate, not a deferred concern.
    The workflow should freeze a `Publication_Concordance_Register.csv`,
    require per-section structured assertion outputs, and block publication on
    unresolved mismatches for concordance-critical values and technical states.

13. The workflow needs a deterministic dispatch-brief renderer in v1.
    Repetitive section dispatch payloads should not be hand-authored at scale.
    A tool should render valid section and package INIT-TASK briefs from the
    frozen planning artifacts.

14. The section taxonomy needs an `OVERVIEW` type.
    Framing sections such as facility overview, objectives, and scope
    boundaries do not fit the existing five section types.

15. `DBM_PUBLISHER` should be explicitly defined as a standalone peer to
    `ORCHESTRATOR`, not a new ORCHESTRATOR phase in v1.

16. Per-section QA output needs a fixed structure so package-level QA can be
    aggregated reliably.

17. Selector/prose divergence and decision-log use need explicit contracts.
    Machine-readable selectors drive deterministic mapping; approved
    `Section_Map.csv` supersedes both selectors and prose; decision logs should
    be included in the frozen input set when present and referenced explicitly
    where publication depends on them.

## Final Architecture

### Type 1 persona: `DBM_PUBLISHER`

Create a new human-facing Type 1 persona:

- role name: `DBM_PUBLISHER`
- instruction file: `agents/AGENT_DBM_PUBLISHER.md`
- matrix placement: `EVALUATIVE x APPLYING`
- `AGENT_CLASS: PERSONA`
- `INTERACTION_SURFACE: chat`
- `WRITE_SCOPE: tool-root-only`
- `BLOCKING: allowed`

Matrix rationale:

- `EVALUATIVE` because the persona judges accepted domain state, resolves
  publication design tradeoffs, and gates publication readiness
- `APPLYING` because it applies approved domain knowledge to produce a new
  governed engineering artifact rather than only reviewing another artifact

Responsibilities:

- intake and authority confirmation
- knowledge-landscape review
- publication schema design with the human
- section-map approval with the human
- concordance-register design with the human
- publication rule freeze
- dispatch of section-level publication workers
- dispatch of final assembly / QA
- final publication acceptance gate

It should write only under a new tool root:

- `{EXECUTION_ROOT}/_Publication/DBM/`

#### Relationship to `ORCHESTRATOR`

For v1, `DBM_PUBLISHER` should be a standalone peer persona invoked directly by
the human after `ORCHESTRATOR` and the DOMAIN pipeline have already prepared
the execution root.

Rules:

- `DBM_PUBLISHER` reuses the same execution root that prior workflow stages
  populated
- it is not added as a new ORCHESTRATOR phase in v1
- handoff is sequential: ORCHESTRATOR builds governed domain state;
  `DBM_PUBLISHER` publishes from that accepted state

#### Role Split With Adjacent Agents

This workflow should keep authoring responsibilities separate from runtime
publication responsibilities.

Governing note:

- `HELPS_HUMANS` remains the Type 0 workflow-design standard governing the
  overall shape of the new workflow, but it is not the runtime publication
  persona

Exact role split:

- `HELP_HUMAN`
  - classifies user intent and routes the user to the right workflow owner
  - may help draft briefs, checklists, or next-step cards
  - does not own publication-schema design, section-map approval, or package
    publication
- `ORCHESTRATOR`
  - owns upstream workspace / execution-root preparation and prior DOMAIN
    pipeline sequencing
  - is responsible for getting the domain state into a publishable precondition
  - does not own the DBM publication design loop and is not the publication
    persona in v1
- `DBM_PUBLISHER`
  - is the human-facing Type 1 persona that owns the runtime publication
    workflow after domain state is prepared
  - owns schema design, section-map approval, concordance-register approval,
    publication-rule freeze, section dispatch, package QA review, and final
    publication acceptance gates
  - does not redefine the upstream decomposition workflow
- `SKILLMAKER`
  - owns authoring and governance of the repo-native skill contracts for this
    workflow
  - is responsible for `skills/dbm-section-publish/*` and
    `skills/dbm-publish/*`
  - coordinates deterministic-tool needs with `TOOLMAKER`
  - does not act as the runtime publication persona
- `TOOLMAKER`
  - owns authoring and governance of the deterministic helpers for this
    workflow
  - is responsible for `tools/publication/build_section_map.py`,
    `assemble_publication.py`, `check_concordance.py`, and
    `render_dispatch_briefs.py`
  - does not own human gates or publication-acceptance decisions

Authoring responsibility split for implementation:

- overall workflow design authority: `HELPS_HUMANS`
- skill-contract design authority: `SKILLMAKER`
- tool-contract and tool-implementation authority: `TOOLMAKER`
- runtime publication persona authority: `DBM_PUBLISHER`
- user routing and lightweight brief support: `HELP_HUMAN`
- upstream execution-root and domain-state preparation: `ORCHESTRATOR`

#### Required knowledge-landscape review method

Before proposing a schema, the persona should:

1. read the category register and present category inventory with KTY counts
   and unit totals
2. read the KTY register and present knowledge types grouped by canonical
   schema / artifact type
3. read the objective register and summarize objective alignment
4. read active scope-change state and identify active, superseded, or retired
   areas where that status is explicit
5. present likely section-load hotspots, including any candidate section that
   appears likely to exceed section-size limits

The output of this step should be a readable summary for the human, not just a
machine artifact.

#### Required concordance-register authoring method

The persona should not ask the human to invent the concordance register from
scratch.

Required method:

1. during knowledge-landscape review, read the KTY register, subject register,
   and open-issues register to identify recurring parameters, technical states,
   and scope-change-sensitive values likely to recur across sections
2. after the draft schema and candidate section map exist, run
   `build_concordance_candidates.py` to produce
   `Publication_Concordance_Candidates.csv` and
   `Publication_Concordance_Coverage.md`
3. dispatch `dbm-concordance-seed` once per section or bounded section group to
   refine the deterministic candidate set and add grounded prose-adjacent
   candidates the tool cannot safely infer
4. freeze `Publication_Concordance_Register.csv` from the agent-generated
   candidate basis
5. pre-populate at least:
   - `AssertionKey`
   - `AssertionLabel`
   - `AssertionDomain`
   - `AssertionType`
   - `ComparisonParameter`
   - `DiscoverySource`
   - `NormalizationHint`
   - `Criticality`
   - `ComparisonRule`
   - `AuthoritySectionID`
   - `RequiredSectionIDs`
6. have the human review, add, remove, or reassign authority before the
   register is frozen

The concordance register should be derived from both recurring source values
and the approved publication structure, because `AuthoritySectionID` and
`RequiredSectionIDs` depend on the final section design. The agent should do
the bulk of concordance population; the human only resolves targeted ambiguity
and approves the frozen result.

### Type 2 bounded skills

Create three skills:

1. `dbm-concordance-seed`
   - bounded concordance-refinement unit
   - one approved section or one bounded section group per run
   - reads the deterministic candidate set plus mapped source content
   - writes one scope-local candidate CSV and one seed QA output

2. `dbm-section-publish`
   - primary authoring unit
   - one target DBM section per run
   - reads only the mapped KTY-local inputs for that section
   - writes one section output, one section QA output, one section
     assertions output, and one assertion-discovery output

3. `dbm-publish`
   - package-level bounded skill
   - does not dispatch other tasks
   - invokes deterministic assembly and concordance helpers
   - aggregates section-level assertion-discovery outputs into package-level
     expansion candidates
   - performs qualitative publication-readiness review on the assembled package
   - emits package-level readiness and rerun recommendations before human
     review

### Deterministic tools

Create five deterministic helpers:

1. `tools/publication/build_section_map.py`
   - consumes the approved publication schema and the frozen input manifest
   - uses machine-readable selectors only
   - emits a candidate `Section_Map.csv`
   - emits a coverage / validation report for selector results
   - validates coverage, duplicates, and section-load limits
   - does not interpret free-text inclusion or exclusion prose

2. `tools/publication/build_concordance_candidates.py`
   - consumes the frozen input manifest, approved publication schema, and
     approved section map
   - harvests typed concordance candidates from structured sources only:
     mapped KA metadata/tables, open issues, decision log, and active SCA
     amendment CSVs
   - emits:
     - `Publication_Concordance_Candidates.csv`
     - `Publication_Concordance_Coverage.md`
   - does not do prose-only inference

3. `tools/publication/assemble_publication.py`
   - consumes approved per-section outputs plus the frozen schema/map
   - owns deterministic completeness, trace, and package QA checks
   - emits:
     - `Rewritten_DBM.md`
     - `Trace_Appendix.md`
     - `Publication_Manifest.md`
     - `Publication_QA.md`
     - optional `_LATEST.md`

4. `tools/publication/check_concordance.py`
   - consumes the frozen concordance register and all per-section assertions
   - performs deterministic cross-section concordance checks
   - emits:
     - `Publication_Concordance_Report.md`
     - `Publication_Concordance_Findings.csv`

5. `tools/publication/render_dispatch_briefs.py`
   - consumes the frozen planning artifacts
   - emits deterministic INIT-TASK briefs for section publication and package
     publication
   - renders briefs that conform to `AGENT_TASK.md` § INIT-TASK brief format
   - writes `TaskSkill` and required `RuntimeOverrides` for the target skill
   - validates rendered briefs against the target skill's `BRIEF_SCHEMA.md`
   - pre-creates required section output directories
   - supports selective re-render for targeted section reruns

These tools must be registered in `tools/REGISTRY.md`.

## Publication Package Contract

Recommended publication root:

- `{EXECUTION_ROOT}/_Publication/DBM/`

Recommended structure:

```text
_Publication/DBM/
  _Planning/
    Publication_Input_Manifest.md
    Publication_Schema.md
    Section_Map.csv
    Publication_Rules.md
    Publication_Concordance_Candidates.csv
    Publication_Concordance_Coverage.md
    Publication_Concordance_Register.csv
    concordance-seed/
      SEC-03_Candidates.csv
      SEC-03_CONCORDANCE_SEED_QA.md
  dispatch/
    DISPATCH_INDEX.csv
    SEC-01_INIT-TASK.md
    ...
    DBM_PUBLISH_INIT-TASK.md
  sections/
    SEC-01/
      SEC-01.md
      SEC-01_QA.md
      SEC-01_ASSERTIONS.csv
      SEC-01_ASSERTION_DISCOVERY.csv
    ...
  package/
    RUN-YYYYMMDD-HHMMSS/
      Rewritten_DBM.md
      Trace_Appendix.md
      Publication_Manifest.md
      Publication_QA.md
      Publication_Concordance_Report.md
      Publication_Concordance_Findings.csv
      Publication_Concordance_Expansion_Candidates.csv
      Publication_Readiness.md
      Rerun_Recommendations.csv
    _LATEST.md
```

Snapshot rule:

- package outputs should be immutable by run
- use run snapshot names of the form `RUN-YYYYMMDD-HHMMSS`
- `_LATEST.md` should point to the latest accepted run snapshot
- `render_dispatch_briefs.py` should pre-create `sections/SEC-##/` output
  directories so workers only write files, not structure

## Required Planning Artifacts

The persona must freeze these artifacts before any section synthesis runs:

### 1. `Publication_Input_Manifest.md`

Purpose:
- freeze exact input paths
- eliminate filename-guessing
- capture authority boundaries for the run

Required contents:

- `EXECUTION_ROOT`
- `PUBLICATION_ROOT`
- exact `_Decomposition` files to use:
  - domain decomposition markdown
  - category register
  - KTY register
  - subject register
  - domain ledger
  - objectives register
  - vocabulary map
  - decision log if present
  - open issues
  - scope boundary register if present
  - coverage / telemetry file(s)
- exact `_Sources` files:
  - source DBM markdown
  - source TOC markdown
- exact scope-change inputs:
  - `_ScopeChange/_LATEST.md`
  - active snapshot directory
  - prior snapshot if needed for amendment history
- explicitly banned authority inputs:
  - `_Aggregation/*` unless the human explicitly promotes them
  - `_Coordination/*`
  - `_Evaluation/*`
  - `_Reconciliation/*`
  - `_MEMORY.md`
  - `_SEMANTIC.md`

### 2. `Publication_Schema.md`

Purpose:
- define the human-approved target DBM structure

Minimum section table columns:

- `SectionID`
- `SectionOrder`
- `SectionTitle`
- `SectionType`
- `SectionPurpose`
- `InclusionRule`
- `ExclusionRule`
- `IncludeCategoryIDs`
- `IncludeKnowledgeTypeIDs`
- `IncludeCanonicalSchemas`
- `ExcludeCategoryIDs`
- `ExcludeKnowledgeTypeIDs`
- `ExpectedInputs`
- `ExpectedOutputShape`
- `MaxKAFiles`
- `SplitHint`

Rules:

- `InclusionRule` and `ExclusionRule` are human-readable only
- `build_section_map.py` consumes the machine-readable selector fields
- selector results are authoritative for tool output
- if selector output diverges from prose intent, the tool's coverage report
  should expose that gap for human review
- the human resolves divergence by editing selectors or the candidate map
- if human judgment changes the candidate mapping, the approved
  `Section_Map.csv` becomes the run authority

### 3. `Section_Map.csv`

Purpose:
- define the authoritative mapping from target sections to decomposed source
  artifacts

Minimum columns:

- `SectionID`
- `SectionTitle`
- `SectionType`
- `SourceDomain`
- `CategoryID`
- `KnowledgeTypeID`
- `SubjectID`
- `ArtifactPath`
- `MappingRole`
- `ContributionScope`
- `SCARefs`
- `DecisionRefs`
- `CurrentStateBasis`
- `Notes`

`MappingRole` values:

- `PRIMARY`
- `SUPPORTING`
- `CONFLICTING`
- `CONTEXT_ONLY`

`ContributionScope` values:

- `FULL_ARTIFACT`
- `TARGET_HEADING`
- `TABLE_ONLY`
- `VALUES_ONLY`
- `BACKGROUND_ONLY`

Notes:

- `SourceDomain` is expected to be constant within a v1 run; keep the column so
  the format can expand later without redesign
- the persona/human approves the final `Section_Map.csv`; tool output is only
  the candidate starting point

### 4. `Publication_Rules.md`

Purpose:
- freeze publication behavior that workers must not improvise

Required rules:

- voice and tone
- allowed section-heading style
- treatment of facility names and abbreviations
- traceability mode: appendix-only
- conflict precedence
- SCA treatment
- handling of gaps / `TBD`
- handling of open issues
- allowed use of historical pre-SCA state
- permitted and forbidden context-only sources

Required default template fields:

- `Voice`
- `Tense`
- `HeadingStyle`
- `FacilityNamingRule`
- `ConflictPrecedence`
- `TBDRule`
- `AmendmentNoteRule`
- `TraceAppendixMode`
- `CanonicalTerminologyRule`
- `LargeSectionRule`
- `ConcordanceRestatementRule`
- `OpenIssueRule`

Recommended default values:

- `Voice`: third-person technical
- `Tense`: present tense for current design basis; past tense only for
  decisions or superseded history
- `HeadingStyle`: numbered hierarchical headings
- `FacilityNamingRule`: full facility name on first use, approved abbreviation
  thereafter
- `ConflictPrecedence`: accepted SCA > approved decomposition state > KTY-local
  content > original DBM source
- `TBDRule`: preserve as `TBD` with a note on what is missing
- `AmendmentNoteRule`: keep amendment notes short and only when materially
  useful
- `TraceAppendixMode`: appendix-only
- `CanonicalTerminologyRule`: prefer vocabulary-map canonical terms
- `LargeSectionRule`: split sections that exceed approved input limits rather
  than forcing oversized synthesis
- `ConcordanceRestatementRule`: prefer one authority section per
  concordance-critical value; other sections should reference that value rather
  than restating it unless the approved schema requires repetition
- `OpenIssueRule`: flatten unresolved open issues to readable `TBD`-style body
  prose when needed, but preserve detailed epistemic status in section QA

### 5. `Publication_Concordance_Register.csv`

Purpose:
- define the finite set of concordance-critical values and technical matters
  that must agree across sections

Minimum columns:

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
- `NormalizationHint`
- `Criticality`
- `Notes`

Supported `AssertionType` values:

- `NUMERIC`
- `RANGE`
- `ENUM`
- `BOOLEAN`
- `LOCATION`
- `STATE`
- `COMPOSITION`

Supported `AssertionDomain` values:

- `PROCESS_CONDITION`
- `UTILITY_CONDITION`
- `PRODUCT_SPEC`
- `EQUIPMENT_LIMIT`
- `OPERATING_TARGET`
- `SCOPE_STATE`
- `LOCATION_STATE`
- `REGULATORY_STATE`
- `CONTROL_LOGIC`

Supported `ComparisonRule` values:

- `EXACT`
- `ROUND_N`
- `TOKEN_MATCH`
- `SET_MATCH`
- `RANGE_MATCH`

Rules:

- this register is human-approved before section synthesis, but it should be
  derived from the agent-seeded candidate loop rather than authored freehand
- only assertions listed here are deterministically concordance-blocking in v1
- each assertion must identify one authority section and all other sections
  required to assert or reference it
- `AssertionKey` should be stable uppercase snake case and should not encode
  section IDs
- recommended naming pattern: `SYSTEM__ATTRIBUTE__UNIT_OR_STATE`
- examples:
  - `INLET_GAS__PRESSURE__PSIG`
  - `SALES_GAS__H2S__PPMV`
  - `SOC__LOCATION__STATE`
- `ComparisonParameter` carries rule-specific comparison detail, such as:
  - decimal precision for `ROUND_N`
  - expected set-membership normalization hints for `SET_MATCH`
  - range-normalization hints for `RANGE_MATCH`
- unresolved mismatches for required assertions block publication

### 6. `Publication_Concordance_Candidates.csv`

Purpose:
- hold the agent-generated typed concordance candidate set used to seed and
  refine the frozen blocking register

Minimum additional columns beyond the frozen register:

- `DiscoverySource`
- `SourceKTYIDs`
- `SourceSectionIDs`
- `NormalizationHint`
- `Criticality`
- `CandidateValueExample`
- `SourceArtifact`
- `SourceRef`
- `ResolutionStatus`

Rules:

- this candidate set is generated by the agent, not authored from scratch by
  the human
- it may be broader than the final frozen register
- it should bias toward over-discovery and later pruning, not under-discovery
- candidate provenance should be preserved so the human only resolves targeted
  ambiguity

### 7. `Publication_Concordance_Coverage.md`

Purpose:
- summarize typed concordance coverage before the blocking register is frozen

Minimum contents:

- candidate counts by discovery source
- candidate counts by assertion domain
- candidate counts by criticality
- resolution-status summary
- section coverage summary
- skipped or structurally unharvestable artifacts

## Authority And Source-Use Rules

These rules should be repeated in the persona and skill contracts.

### Non-negotiable authority stack

1. approved publication schema
2. approved publication rules
3. approved merged decomposition state
4. accepted SCA state
5. KTY-local `Scoping.md` and `KA-*.md`
6. original DBM source markdown as provenance only

### Non-authoritative-by-default inputs

The publication workflow should not use these as content authority unless the
human explicitly promotes them:

- `_Aggregation/*`
- `_Coordination/*`
- `_Evaluation/*`
- `_Reconciliation/*`
- `_MEMORY.md`
- `_SEMANTIC.md`

### Scope-change rule

Publication must present the **current approved post-SCA state** as primary
content.

Historical or superseded pre-SCA state may appear only when:

- it materially explains an engineering change, and
- it is placed in an amendment note, trace note, or QA note, not treated as
  current design basis.

## `dbm-section-publish` Skill Contract

### Purpose

Publish exactly one target DBM section from approved mapped inputs.

### Task shell mode

- generic `TASK`
- no profile

### Required runtime inputs

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

### Read boundary

The skill may read only:

- the five frozen planning artifacts
- the `Section_Map.csv` rows for this section
- the exact KTY-local files named in those rows
- the vocabulary map named in the manifest
- the open-issues register named in the manifest when mapped content or QA
  reporting depends on issue status
- the decision log named in the manifest when mapped rows or assertion refs
  depend on it
- the exact scope-change snapshot files named in the manifest when those rows
  reference SCA material

### Write boundary

The skill writes only:

- one section file
- one section QA file
- one section assertions file
- one section assertion-discovery file

It must not modify any `CAT-* / 1_Working / KTY-*` files.

### Mapping behavior definitions

These semantics should be explicit in the skill contract:

- `PRIMARY`: main source material that should anchor section narrative
- `SUPPORTING`: contextual or constraining content that informs the section but
  does not define its primary structure
- `CONFLICTING`: mapped input known to contradict other mapped inputs; the
  worker must surface the conflict in QA and avoid silent reconciliation
- `CONTEXT_ONLY`: background-only material that may inform interpretation but
  should not drive direct section claims unless the rules explicitly permit it

`ContributionScope` should control how a mapped artifact is used:

- `FULL_ARTIFACT`: whole artifact may contribute
- `TARGET_HEADING`: use only the heading or subsection named in `Notes`
- `TABLE_ONLY`: use tabular content only
- `VALUES_ONLY`: use only explicit values / parameters
- `BACKGROUND_ONLY`: background context only; do not rely on it for direct
  design-basis claims

### Required section types and templates

The skill contract must define default section templates for:

- `OVERVIEW`
- `PROCESS_BASIS`
- `PHILOSOPHY`
- `DATA_REFERENCE`
- `DISCIPLINE_BASIS`
- `REGULATORY`

Required default templates:

#### `OVERVIEW`

- facility / project identity
- stated objectives
- scope boundaries
- key assumptions / constraints
- document applicability

#### `PROCESS_BASIS`

- purpose
- functional configuration
- design / operating basis
- interfaces
- controls / protection
- facility-specific notes

#### `PHILOSOPHY`

- governing principle
- applicability
- required design behavior
- exceptions / limits
- rationale

#### `DATA_REFERENCE`

- narrative introduction
- consolidated values / tables
- assumptions / caveats
- usage notes

#### `DISCIPLINE_BASIS`

- discipline scope
- governing basis
- required systems / components
- constraints / standards
- interfaces

#### `REGULATORY`

- governing obligation
- applicability
- facility impact
- compliance implications
- unresolved items

### Section QA output format

`SEC-##_QA.md` should use a stable structure with these required blocks:

1. section summary
2. coverage table
   - mapped KTYs / KAs consumed
   - mapped inputs skipped and why
3. readiness observations
   - any mapped KTYs below readiness threshold
4. conflict register
   - contradictory values / states
   - both positions and sources
5. terminology notes
   - canonical term normalizations applied
6. gap / `TBD` register
   - unsupported or incomplete claims surfaced in section body
   - preserve open-issue distinctions such as `TBD`, `ASSUMPTION`, and
     `DEFERRED_CONFIRMATION` in QA even when body prose is flattened
7. amendment notes
   - SCA- or decision-driven changes reflected in the section
8. assertion emission notes
   - required concordance assertions emitted or intentionally marked
     non-applicable
   - assertion-discovery candidates proposed for later expansion review

### Section assertions output format

Each section run must emit `SEC-##_ASSERTIONS.csv`.

Minimum columns:

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

- if the section is listed in `RequiredSectionIDs` for a concordance assertion,
  it must emit a row for that assertion
- if the section is the `AuthoritySectionID`, it must emit the authoritative
  asserted value or state
- the worker reads `Publication_Concordance_Register.csv`, filters rows where
  its `SECTION_ID` equals `AuthoritySectionID` or appears in
  `RequiredSectionIDs`, and emits one row per matched key
- emitted `NormalizedValue` must be suitable for deterministic comparison under
  the register's `ComparisonRule`
- a section should prefer `REFERRED` over duplicated restatement when the
  publication rules designate another section as authority for that assertion

### Section assertion discovery output format

Each section run must also emit `SEC-##_ASSERTION_DISCOVERY.csv`.

Minimum columns:

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

Rules:

- after emitting the required approved-register rows, the worker must search
  mapped content for materially repeated or technically important values/states
  not already represented in the approved register for that section scope
- these discoveries should be emitted rather than silently ignored
- ambiguity about whether a candidate duplicates an existing register key
  should be preserved in `Notes`, not silently suppressed

### KTY readiness gates

The skill must read each mapped KTY `_STATUS.md` before using its files.

Minimum rules:

- `PRIMARY` and `CONFLICTING` inputs must be at least `INITIALIZED`
- if a `PRIMARY` input is below that threshold, fail the section run with
  `FAILED_INPUTS`
- if a `CONFLICTING` input is below that threshold, fail the section run with
  `FAILED_INPUTS`
- if a `SUPPORTING` input is below that threshold, skip it and record a gap
  note in section QA
- if a `CONTEXT_ONLY` input is below that threshold, the worker may fall back
  to decomposition-level context only, with a QA note

The skill must not treat an `OPEN` or otherwise unready KTY as equivalent to a
fully authored source artifact.

### Terminology control

When the manifest provides a vocabulary map, the worker should:

- prefer the canonical term in the vocabulary map over KA-local synonyms
- retain a synonym in parentheses only when it materially helps recognition
- avoid producing mixed terminology for the same system within one section

### Cross-facility synthesis rules

These must be explicit in the skill contract.

1. If multiple mapped artifacts agree, synthesize them into one coherent
   section narrative.

2. If multiple mapped artifacts differ:
   - do not reconcile silently
   - if an accepted SCA or explicit publication rule resolves the difference,
     publish the resolved current-state position and record the prior state in
     QA or trace notes
   - otherwise record a publication conflict in the section QA output and use
     cautious wording in the narrative

3. If a system exists in only one facility/domain:
   - scope the section explicitly to that facility

4. If a system moved between facilities due to accepted SCA:
   - present the post-SCA arrangement as current-state content
   - keep prior placement only as audit context

5. If content is absent for a facility:
   - do not invent parity
   - use `TBD` or explicit scope note

### No-invention rules

- every substantive claim must be supported by mapped source artifacts
- unsupported statements become `TBD`
- uncertain synthesis becomes a publication conflict or explicitly labeled
  assumption
- no inline `[HBK-####]` style citations in the DBM body
- detailed traceability belongs in the trace appendix and section QA outputs

### Section-size control

The skill must fail fast with `FAILED_INPUTS` if:

- the mapped KA count exceeds `MAX_KA_FILES`, or
- the section input set exceeds the approved size rule in
  `Publication_Schema.md` / `Publication_Rules.md`

When that happens, the persona should split or refine the section design rather
than forcing the worker to synthesize an oversized input set.

## `dbm-publish` Skill Contract

Purpose:
- package-level bounded assembly and QA after section outputs already exist

It may:

- invoke `assemble_publication.py`
- invoke `check_concordance.py`
- aggregate per-section `SEC-##_ASSERTION_DISCOVERY.csv` files into
  `Publication_Concordance_Expansion_Candidates.csv`
- review the assembled package for qualitative publication readiness
- flag sections that still read like artifact dumps rather than engineering
  prose
- write `Publication_Readiness.md`
- write `Rerun_Recommendations.csv`

Deterministic checks should not remain in the skill. They belong in
`assemble_publication.py` and `check_concordance.py`, including:

- section completeness against `Publication_Schema.md`
- trace completeness against `Section_Map.csv`
- missing-section detection
- package manifest generation
- deterministic `Publication_QA.md` generation
- concordance checks against `Publication_Concordance_Register.csv`

It may not:

- dispatch other workers
- rewrite KTY-local truth
- re-author section prose except for package-level summaries

Required readiness classification:

- `READY`
- `READY_WITH_MAJOR_NOTES`
- `BLOCKED`

If readiness is `BLOCKED`, the skill should identify which sections require
rerun and why.

Required execution method:

1. invoke `assemble_publication.py`
2. if assembly exits non-zero, emit `BLOCKED` and record the tool failure
3. invoke `check_concordance.py`
4. read the assembled DBM body and assess whether each section reads like
   coherent engineering prose under `Publication_Rules.md`, rather than as a
   concatenated artifact dump
5. read all `SEC-##_QA.md` files and aggregate:
   - total conflicts
   - total `TBD` / assumption / deferred-confirmation items
   - total skipped inputs
   - total material terminology normalizations
6. classify readiness:
   - `BLOCKED` if required sections are missing, assembly failed, blocking
     concordance findings exist, or unresolved `HIGH` expansion candidates
     remain
   - `READY_WITH_MAJOR_NOTES` if no blocking condition remains but unresolved
     `NORMAL` expansion candidates or other material quality / QA issues remain
   - `READY` only if deterministic concordance passes and no material
     expansion candidates remain unresolved
7. emit `Publication_Readiness.md`
8. emit `Rerun_Recommendations.csv`

`Rerun_Recommendations.csv` should include at least:

- `SectionID`
- `RerunReason`
- `BlockingLevel`
- `SpecificFinding`
- `RecommendedAction`
- `Notes`

## Trace Appendix Format

`Trace_Appendix.md` should use a stable, readable structure:

1. top-level summary table with:
   - `SectionID`
   - `SectionTitle`
   - mapped KTY count
   - mapped KA count
   - evidence / source-reference count if available
   - conflict count
2. one detailed block per section
3. one trace table per section with at least:
   - `SectionID`
   - `SectionTitle`
   - `KnowledgeTypeID`
   - `SubjectID`
   - `ArtifactPath`
   - `MappingRole`
   - `ContributionScope`
   - `SourceRef` or evidence-unit reference
   - `SCARefs`
   - `CurrentStateBasis`

Trace blocks should identify sources and evidence only. They should not repeat
long narrative content from the DBM body.

## Concordance Checking

`Publication_Concordance_Report.md` should summarize:

1. total assertions checked
2. passed assertions
3. blocked mismatches
4. missing required assertions
5. sections implicated by each finding

`Publication_Concordance_Findings.csv` should include at least:

- `AssertionKey`
- `AssertionLabel`
- `AuthoritySectionID`
- `SectionID`
- `FindingType`
- `ExpectedNormalizedValue`
- `ObservedNormalizedValue`
- `ComparisonRule`
- `Blocking`
- `Notes`

Hard concordance rules:

- every required assertion must exist in its authority section
- every required section must either assert or explicitly reference the
  assertion
- repeated assertions must normalize to concordant value / state under the
  configured comparison rule
- unresolved mismatches are publication blockers
- package publication always performs a full concordance re-check against the
  latest complete set of section outputs, even when only a subset of sections
  was rerun

## Files That Must Be Read During Authoring

The implementing agent should read these files before authoring any new
contracts, skills, or tools.

### A. Core bootstrap and index

- [INIT.md](/Users/ryan/ai-env/projects/chirality-app/INIT.md)
- [AGENTS.md](/Users/ryan/ai-env/projects/chirality-app/AGENTS.md)

### B. Governing workflow and skill standards

- [agents/AGENT_HELPS_HUMANS.md](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_HELPS_HUMANS.md)
- [agents/AGENT_SKILLMAKER.md](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_SKILLMAKER.md)
- [skills/README.md](/Users/ryan/ai-env/projects/chirality-app/skills/README.md)
- [skills/SKILL_TEMPLATE.md](/Users/ryan/ai-env/projects/chirality-app/skills/SKILL_TEMPLATE.md)
- [tools/validation/validate_skill_metadata.py](/Users/ryan/ai-env/projects/chirality-app/tools/validation/validate_skill_metadata.py)

### C. Task-shell and orchestration contracts

- [agents/AGENT_TASK.md](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_TASK.md)
- [agents/AGENT_ORCHESTRATOR.md](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_ORCHESTRATOR.md)
- [agents/AGENT_HELP_HUMAN.md](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_HELP_HUMAN.md)

### D. DOMAIN decomposition and amendment contracts

- [agents/AGENT_DECOMP_BASE.md](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_DECOMP_BASE.md)
- [agents/AGENT_DOMAIN_DECOMP.md](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_DOMAIN_DECOMP.md)
- [agents/AGENT_SCOPE_CHANGE.md](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_SCOPE_CHANGE.md)

### E. Repo architecture and specification references

- [docs/DBM_Agent_Instruction_Architecture.md](/Users/ryan/ai-env/projects/chirality-app/docs/DBM_Agent_Instruction_Architecture.md)
- [docs/SPEC.md](/Users/ryan/ai-env/projects/chirality-app/docs/SPEC.md)
- [docs/TYPES.md](/Users/ryan/ai-env/projects/chirality-app/docs/TYPES.md)
- [tools/REGISTRY.md](/Users/ryan/ai-env/projects/chirality-app/tools/REGISTRY.md)

### F. Existing DOMAIN execution-skill precedents

- [skills/domain-documents/SKILL.md](/Users/ryan/ai-env/projects/chirality-app/skills/domain-documents/SKILL.md)
- [skills/domain-documents/BRIEF_SCHEMA.md](/Users/ryan/ai-env/projects/chirality-app/skills/domain-documents/BRIEF_SCHEMA.md)
- [skills/domain-documents/TOOL_POLICY.md](/Users/ryan/ai-env/projects/chirality-app/skills/domain-documents/TOOL_POLICY.md)
- [skills/domain-documents/QA_CHECKS.md](/Users/ryan/ai-env/projects/chirality-app/skills/domain-documents/QA_CHECKS.md)
- [skills/four-documents/SKILL.md](/Users/ryan/ai-env/projects/chirality-app/skills/four-documents/SKILL.md)
- [skills/content-digest/SKILL.md](/Users/ryan/ai-env/projects/chirality-app/skills/content-digest/SKILL.md)

### G. West Doe Deepcut execution-root inputs

- [domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_DOMAIN_DECOMP_FINAL_v4.md](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_DOMAIN_DECOMP_FINAL_v4.md)
- [domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Domain_Ledger_v4.csv](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Domain_Ledger_v4.csv)
- [domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Category_Register_v4.csv](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Category_Register_v4.csv)
- [domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Knowledge_Type_Register_v4.csv](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Knowledge_Type_Register_v4.csv)
- [domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Knowledge_Subject_Register_v4.csv](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Knowledge_Subject_Register_v4.csv)
- [domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Objective_Register_v4.csv](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Objective_Register_v4.csv)
- [domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Scope_Boundary_Register_v4.csv](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Scope_Boundary_Register_v4.csv)
- [domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Vocabulary_Map_v4.csv](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Vocabulary_Map_v4.csv)
- [domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Open_Issues_v4.csv](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Open_Issues_v4.csv)
- [domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Node_Summary_v4.csv](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Node_Summary_v4.csv)
- [domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Coverage_Telemetry_v4.json](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Coverage_Telemetry_v4.json)
- [domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Publication_Manifest_v4.md](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Publication_Manifest_v4.md)
- [domain-test/domains/West_Doe_Deepcut_DBM/_Sources/W235633-PRC-DBM-000001-001_(4-25_Doe)_DBM.md](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Deepcut_DBM/_Sources/W235633-PRC-DBM-000001-001_(4-25_Doe)_DBM.md)
- [domain-test/domains/West_Doe_Deepcut_DBM/_Sources/TOC_Deepcut.md](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Deepcut_DBM/_Sources/TOC_Deepcut.md)
- [domain-test/domains/West_Doe_Deepcut_DBM/_ScopeChange/_LATEST.md](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Deepcut_DBM/_ScopeChange/_LATEST.md)

The implementing agent must also inspect the active Deepcut SCA snapshot pointed
to by `_ScopeChange/_LATEST.md`.

### H. West Doe Comp and Liquids execution-root inputs

- [domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/WEST_DOE_DOMAIN_DECOMPOSITION.md](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/WEST_DOE_DOMAIN_DECOMPOSITION.md)
- [domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_domain_ledger.csv](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_domain_ledger.csv)
- [domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_categories.csv](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_categories.csv)
- [domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_knowledge_types.csv](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_knowledge_types.csv)
- [domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_knowledge_subjects.csv](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_knowledge_subjects.csv)
- [domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_objectives.csv](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_objectives.csv)
- [domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_vocabulary_map.csv](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_vocabulary_map.csv)
- [domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_open_issues.csv](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_open_issues.csv)
- [domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_decision_log.csv](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_decision_log.csv)
- [domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_validation_checks.csv](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_validation_checks.csv)
- [domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/README.txt](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/README.txt)
- [domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Sources/W242510-PRC-DBM-000001-001_(3-25_Doe)_DBM.md](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Sources/W242510-PRC-DBM-000001-001_(3-25_Doe)_DBM.md)
- [domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Sources/TOC_Compression_Liquids.md](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Sources/TOC_Compression_Liquids.md)
- [domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_ScopeChange/_LATEST.md](/Users/ryan/ai-env/projects/chirality-app/domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_ScopeChange/_LATEST.md)

The implementing agent must also inspect the active Comp/Liquids SCA snapshot
pointed to by `_ScopeChange/_LATEST.md`.

### I. KTY-local files that section workers must use

For every mapped KTY included in a target section, the worker must read:

- `{KTY_PATH}/Scoping.md`
- all mapped `{KTY_PATH}/KA-*.md`
- `{KTY_PATH}/_CONTEXT.md`
- `{KTY_PATH}/_REFERENCES.md`
- `{KTY_PATH}/_STATUS.md`

Optional contextual reads only when explicitly required by the section map or
publication rules:

- `{KTY_PATH}/_DEPENDENCIES.md`

Non-authoritative and excluded by default:

- `{KTY_PATH}/_MEMORY.md`
- `{KTY_PATH}/_SEMANTIC.md`

The worker should also read the vocabulary map frozen in
`Publication_Input_Manifest.md` when terminology normalization is required.

## Expected Edit Targets If This Plan Is Implemented

New files:

- `agents/AGENT_DBM_PUBLISHER.md`
- `skills/dbm-section-publish/SKILL.md`
- `skills/dbm-section-publish/BRIEF_SCHEMA.md`
- `skills/dbm-section-publish/TOOL_POLICY.md`
- `skills/dbm-section-publish/QA_CHECKS.md`
- `skills/dbm-concordance-seed/SKILL.md`
- `skills/dbm-concordance-seed/BRIEF_SCHEMA.md`
- `skills/dbm-concordance-seed/TOOL_POLICY.md`
- `skills/dbm-concordance-seed/QA_CHECKS.md`
- `skills/dbm-publish/SKILL.md`
- `skills/dbm-publish/BRIEF_SCHEMA.md`
- `skills/dbm-publish/TOOL_POLICY.md`
- `skills/dbm-publish/QA_CHECKS.md`
- `tools/publication/build_section_map.py`
- `tools/publication/build_concordance_candidates.py`
- `tools/publication/assemble_publication.py`
- `tools/publication/check_concordance.py`
- `tools/publication/render_dispatch_briefs.py`

Updated files:

- `AGENTS.md`
- `skills/README.md`
- `tools/REGISTRY.md`
- `docs/DBM_Agent_Instruction_Architecture.md`

## Detailed Implementation Sequence

### Phase 1 — Author workflow contracts

1. Read the files listed in sections A through I above.
2. Confirm the actual decomposition filename patterns used by both West Doe
   domains.
3. Draft `AGENT_DBM_PUBLISHER.md`.
4. In `AGENTS.md`, place `DBM_PUBLISHER` in the `EVALUATIVE x APPLYING` cell.
5. Define the persona's knowledge-landscape review method before schema-design
   prompts are written.
6. Draft the `Publication_Rules.md` default template.
7. Draft machine-readable selector fields for `Publication_Schema.md`.
8. Draft `Section_Map.csv` semantics for `MappingRole` and `ContributionScope`.
9. Draft the typed concordance candidate / freeze loop:
    - `Publication_Concordance_Candidates.csv`
    - `Publication_Concordance_Coverage.md`
    - `Publication_Concordance_Register.csv`
10. Define the fixed `SEC-##_QA.md`, `SEC-##_ASSERTIONS.csv`, and
    `SEC-##_ASSERTION_DISCOVERY.csv` formats.
11. Define selector/prose divergence handling and decision-log use.
12. Add the `OVERVIEW` section type.
13. Define the concordance-register authoring method and `AssertionKey`
    naming rules.
14. Draft `dbm-section-publish` with:
   - section templates
   - mapping-role behavior
   - contribution-scope behavior
   - KTY readiness gates
   - terminology normalization rules
   - open-issue handling rules
   - concordance assertion emission rules
   - large-section limits
   - cross-facility synthesis rules
   - no-invention rules
   - appendix-style traceability rules
15. Draft `dbm-concordance-seed` as the bounded reasoning layer between the
    deterministic candidate builder and the frozen blocking register.
16. Draft `dbm-publish` as the package-quality gate that invokes deterministic
    assembly and concordance tools, aggregates assertion-discovery expansion
    candidates, and does not dispatch other tasks.

### Phase 2 — Author deterministic tools

1. Implement `build_section_map.py`.
2. Implement `build_concordance_candidates.py`.
3. Implement `assemble_publication.py`.
4. Implement `check_concordance.py`.
5. Implement `render_dispatch_briefs.py`.
6. Add all tools to `tools/REGISTRY.md`.
7. Ensure script headers define:
   - inputs
   - outputs
   - exit codes
   - scope boundary
8. Ensure `build_section_map.py` uses machine-readable selectors only and
   generates a candidate map.
9. Ensure `assemble_publication.py` owns deterministic completeness, trace, and
   package QA checks.
10. Ensure `check_concordance.py` blocks unresolved assertion mismatches.
11. Ensure `build_concordance_candidates.py` remains deterministic and
    structured-source-only.
12. Ensure `render_dispatch_briefs.py` can emit section briefs and targeted
    rerun briefs deterministically.
13. Ensure rendered briefs conform to `AGENT_TASK.md` § INIT-TASK brief format
    and the target skill's `BRIEF_SCHEMA.md`.

### Phase 3 — Validate skill layer

1. Ensure all three publication skills follow `skills/SKILL_TEMPLATE.md`.
2. Validate with:
   - `python3 tools/validation/validate_skill_metadata.py skills`
3. Fix any metadata or companion-file violations before proceeding.

### Phase 4 — Pilot on one domain

1. Use one execution root only.
2. Have the persona freeze:
   - `Publication_Input_Manifest.md`
   - `Publication_Schema.md`
   - `Publication_Rules.md`
   - `Publication_Concordance_Candidates.csv`
   - `Publication_Concordance_Register.csv`
3. Run `build_section_map.py`.
4. Run `build_concordance_candidates.py`.
5. Review candidate-map and concordance-candidate output:
   - unmapped rows
   - conflicting rows
   - section-size warnings
   - any selector-driven overreach that needs human correction
   - unresolved high-criticality candidate gaps
6. Dispatch `dbm-concordance-seed` for one overview section and one process
   section, then freeze the blocking register.
7. Approve the final `Section_Map.csv` and `Publication_Concordance_Register.csv`.
8. Run `render_dispatch_briefs.py`.
9. Pilot a small section set:
   - one overview section
   - one process section
   - one philosophy section
   - one discipline section
   - one regulatory section
10. Review:
   - readability
   - traceability
   - conflict behavior
   - amendment handling
   - terminology consistency
   - section-size behavior
   - concordance assertion emission quality
   - assertion-discovery quality

### Phase 5 — Full publication run

1. Persona dispatches `TASK + dbm-section-publish` once per approved section,
   using the rendered INIT-TASK briefs.
2. Persona resolves any section QA conflicts that block publication.
3. Persona dispatches `TASK + dbm-publish` once section outputs are complete.
4. `dbm-publish` invokes `assemble_publication.py` and
   `check_concordance.py`.
5. `dbm-publish` also aggregates `SEC-##_ASSERTION_DISCOVERY.csv` outputs into
   `Publication_Concordance_Expansion_Candidates.csv`.
6. If readiness is `BLOCKED`, the persona uses targeted rerun briefs for only
   the affected sections, then repeats package publication.
7. Human reviews the package and either:
   - accepts it
   - requests schema/rule changes and rerun

Rerun semantics:

- a section rerun overwrites that section's current output bundle
- package publication always re-assembles the full document from the latest
  complete set of section outputs
- targeted rerun does not imply partial concordance checking; concordance is
  always re-checked across the full current section set

## Validation And Acceptance

### Contract checks

- new skills pass metadata validation
- new tools are registered
- persona gates are decision-complete

### Behavioral checks

- section workers never write inside KTY folders
- package assembly is deterministic apart from timestamps
- candidate section mapping is deterministic apart from approved human edits
- structured concordance-candidate harvesting is deterministic apart from
  approved human pruning or authority reassignment
- brief rendering is deterministic from frozen planning artifacts
- the final DBM body reads as a coherent engineering document
- detailed provenance appears in the trace appendix, not inline in body prose
- unresolved contradictions surface as section/package QA findings, not silent
  edits
- accepted SCA state is reflected as current-state publication content
- canonical terminology is consistent within each section when vocabulary maps
  are available
- oversized sections fail fast and are pushed back to schema redesign rather
  than being forced through synthesis
- section QA outputs follow a fixed structure
- concordance-critical values and technical states are emitted as structured
  section assertions
- section workers emit assertion-discovery candidates rather than silently
  ignoring uncovered repeated values/states
- unresolved cross-section assertion mismatches block publication
- unresolved `HIGH` concordance-expansion candidates block readiness even when
  the frozen register itself passes deterministic checking
- decision references are preserved where publication relies on them
- rendered TASK briefs validate against the target skill contract
- open-issue statuses remain distinguishable in QA even when body prose is
  simplified for readability

### Minimum v1 acceptance

- one execution root can produce one rewritten DBM package
- the human can approve schema and rules before synthesis
- section workers can handle multi-KTY synthesis without inventing reconciliation
- final package is auditable back to decomposition and accepted SCA state
- the package receives a publication-readiness judgment before first human
  review
- all assertions in `Publication_Concordance_Register.csv` pass concordance
  checks or block publication pending rerun
- the agent does the bulk of concordance population and typed coverage work
  before the human freeze gate

## Defaults And Out-Of-Scope

Defaults:

- one execution root per publication run
- Markdown publication only in v1
- appendix-only detailed traceability
- merged-SCA current state as publication baseline
- selective section rerun is designed in through deterministic brief rendering,
  even though each accepted output is published as a full-document snapshot

Out of scope for v1:

- combined multi-domain publication in one DBM
- PDF export as a first-class workflow concern
- using `_Aggregation`, `_Coordination`, or `_Evaluation` outputs as content
  authority
- automatic reconciliation of unresolved cross-facility contradictions
- mutation of decomposition truth or KTY-local artifacts during publication
