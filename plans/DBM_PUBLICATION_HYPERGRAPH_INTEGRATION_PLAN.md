# DBM Publication Hypergraph Integration Plan

## Summary

This plan defines the corrective work needed to let the DBM publication
workflow benefit from `DOMAIN_HYPERGRAPH` outputs without corrupting the
authority stack for section prose.

The key recommendation is:
- keep decomposition, accepted scope-change state, and KTY-local artifacts as
  the **content authority**
- admit hypergraph snapshots as **auxiliary structure evidence** for planning,
  concordance seeding, and package-level QA
- do not let hypergraph outputs author section prose or override decomposition
  truth

This plan complements, but does not replace:
- `plans/DBM_PUBLICATION_WORKFLOW_PLAN.md`
- `plans/DBM_PUBLICATION_GOVERNANCE_ALIGNMENT_PLAN.md`

Where the current workflow treats `_Aggregation/*` as excluded by default, this
plan introduces a controlled exception for hypergraph evidence only.

## Why Hypergraph Integration Is Worth Doing

The current DBM publication stack already has strong publication mechanics:
- frozen manifest
- section map
- typed concordance register
- section-level synthesis
- deterministic concordance gate

What it lacks is a root-wide structural-evidence layer that can help the
publisher:
- detect cross-KTY topic clusters before schema freeze
- identify section-load hotspots
- identify repeated technical states that should become concordance assertions
- detect missing participant sections in a cross-section assertion
- run a publication-oriented completeness check that is richer than plain
  section enumeration

The domain hypergraphs already contain useful structures for this:
- category, KTY, subject, artifact, objective, and ledger rows as typed nodes
- `IN_CATEGORY`, `HAS_SUBJECT`, `HAS_ARTIFACT`, `LEDGER_ROW`, and
  `KTY_SUPPORTS_OBJ` edges
- evidence CSVs that expose discovered categories, KTYs, subjects, objectives,
  ledger rows, and subject-artifact relationships

However, hypergraph quality is not uniform across roots. For example:
- Comp & Liquids currently has a clean hypergraph QA result
- Deepcut still has known artifact-node collision / merge-ambiguity blockers

Therefore, hypergraph integration must be **auxiliary and conditional**, not a
new content-authority layer.

## Core Policy

### Content authority remains unchanged

Section prose and package truth must still be derived from:
1. approved publication schema
2. approved publication rules
3. approved decomposition/package truth
4. accepted scope-change state
5. mapped KTY-local `Scoping.md` and `KA-*.md`
6. original DBM source as provenance only

Hypergraph outputs must not be inserted into that authority chain as section
content authority.

### Hypergraphs become auxiliary structure evidence

Hypergraph snapshots may be used only for:
- landscape review
- section-map design support
- concordance candidate discovery support
- package-level coverage / structure QA

They must not:
- author or rewrite section prose
- override decomposition mappings
- override KTY-local content
- replace deterministic concordance checking

## Hypergraph Use Modes

Add an explicit hypergraph-use-mode concept to the publisher workflow.

Allowed modes:
- `NONE`
- `AUXILIARY_PLANNING`
- `AUXILIARY_QA`
- `AUXILIARY_PLANNING_AND_QA`

Meaning:
- `NONE`
  - ignore hypergraph inputs entirely
- `AUXILIARY_PLANNING`
  - use hypergraph outputs during Gate 2 and Gate 4 only
- `AUXILIARY_QA`
  - use hypergraph outputs during Gate 6 only
- `AUXILIARY_PLANNING_AND_QA`
  - use hypergraph outputs during both planning and package QA

Default recommendation:
- if the latest hypergraph snapshot has non-blocking QA, default to
  `AUXILIARY_PLANNING_AND_QA`
- if the latest hypergraph snapshot has blockers, default to `NONE` unless the
  contract explicitly allows limited planning-only use with disclosed caveats

## Admission Rule

Hypergraph integration is allowed only when the frozen publication manifest
includes:
- `HYPERGRAPH_SNAPSHOT_PATH`
- `HYPERGRAPH_RUN_SUMMARY_PATH`
- `HYPERGRAPH_QA_REPORT_PATH`
- `HYPERGRAPH_USE_MODE`
- `HYPERGRAPH_QA_VERDICT`
- `HYPERGRAPH_LIMITATIONS`

Recommended `HYPERGRAPH_QA_VERDICT` values:
- `NON_BLOCKING`
- `BLOCKED`
- `NOT_USED`

Recommended `HYPERGRAPH_LIMITATIONS` values:
- free-text list of known defects that constrain allowed use

Admission rules:
- if `HYPERGRAPH_USE_MODE = NONE`, no hypergraph evidence is consumed
- if `HYPERGRAPH_USE_MODE != NONE`, the publisher must freeze exact hypergraph
  paths in the manifest
- if hypergraph QA is blocking, the publisher must not use the snapshot for QA
  or content-adjacent decisions
- if planning-only use is allowed despite blockers, the contract must state
  that the hypergraph is advisory and limited to non-authoritative clustering
  assistance

## Required Contract Revisions

### 1. `agents/AGENT_DBM_PUBLISHER.md`

Revise the publisher contract in these exact ways.

#### Runtime defaults

Add new runtime variables:
- `HYPERGRAPH_USE_MODE = NONE`
- `HYPERGRAPH_SNAPSHOT_PATH = optional`
- `HYPERGRAPH_RUN_SUMMARY_PATH = optional`
- `HYPERGRAPH_QA_REPORT_PATH = optional`
- `HYPERGRAPH_NODES_PATH = optional`
- `HYPERGRAPH_HYPEREDGES_PATH = optional`
- `HYPERGRAPH_EVIDENCE_ROOT = optional`

#### Non-authoritative inputs section

Replace the blanket exclusion of `{EXECUTION_ROOT}/_Aggregation/*` with a more
precise rule:
- `_Aggregation/*` remains non-authoritative for section prose by default
- a frozen hypergraph snapshot under `_Aggregation/Hypergraph/` may be consumed
  as auxiliary structure evidence when explicitly admitted in the manifest

#### Gate 1

Gate 1 must freeze hypergraph evidence when used:
- exact hypergraph snapshot path
- run summary path
- QA report path
- chosen use mode
- QA verdict
- limitations / caveats

The manifest must explicitly distinguish:
- `content authority`
- `admission / closure evidence`
- `auxiliary structure evidence`

#### Gate 2

Add optional hypergraph-assisted landscape review:
- use node/edge counts to identify dense KTY clusters
- use `KTY_SUPPORTS_OBJ` edges to identify objective-centered hubs
- use subject/artifact adjacency to detect likely section-load hotspots
- use ledger coverage in the hypergraph to identify unusually broad KTYs

The Gate 2 summary must label any hypergraph-derived observation as:
- `AUXILIARY_STRUCTURE_EVIDENCE`

#### Gate 4

Add optional hypergraph-assisted section-map and concordance support:
- use adjacency to suggest likely multi-KTY section clusters
- use repeated objective/KTY participation to suggest authority sections for
  recurring technical states
- use subject/artifact relationships to identify omitted participant sections
  in candidate assertions
- use node/edge neighborhoods to propose concordance-expansion candidates

The Gate 4 contract must forbid:
- using hypergraph structure alone to create a section mapping that contradicts
  the approved decomposition and mapped KTY-local inputs

#### Gate 6

Add optional package-level hypergraph QA:
- verify all section-mapped KTYs appear in the admitted hypergraph
- verify no major connected cluster implied by the section map is silently
  absent from the section set
- verify authority-section coverage for concordance-critical clusters
- flag orphaned or weakly represented structural clusters as publication QA
  warnings or blockers according to configured severity

#### Invariants

Add explicit invariants:
- hypergraph outputs are auxiliary only
- blocked hypergraph QA cannot silently power package QA
- hypergraph evidence may refine concordance coverage but cannot replace the
  frozen concordance register

### 2. `skills/dbm-concordance-seed/*`

Revise the skill so it can consume an admitted hypergraph snapshot in a bounded
way.

Required changes:
- add optional brief fields:
  - `HYPERGRAPH_USE_MODE`
  - `HYPERGRAPH_SNAPSHOT_PATH`
  - `HYPERGRAPH_QA_REPORT_PATH`
  - `HYPERGRAPH_EVIDENCE_ROOT`
- add authority language:
  - hypergraph is auxiliary evidence only
- allow the skill to use hypergraph evidence to:
  - suggest repeated-value/assertion clusters
  - identify additional participant sections
  - identify likely missing concordance candidates
- forbid the skill from:
  - inventing assertion values from graph topology
  - preferring graph structure over mapped source content

Expected output enhancement:
- seed QA should report when a candidate was strengthened or suggested by
  hypergraph evidence
- each such row should be tagged with a discovery source such as
  `HYPERGRAPH_AUXILIARY`

### 3. `skills/dbm-section-publish/*`

Keep the section worker content-authority stack unchanged.

Required changes:
- add optional read-only hypergraph inputs in the brief
- allow the section worker to use hypergraph evidence only for local QA checks:
  - did the mapped KTY set omit an obviously connected supporting KTY?
  - does the section appear to restate a known cross-section state that should
    be emitted as an assertion?
- keep hypergraph evidence out of section body synthesis authority
- require QA output to label any hypergraph-derived concern as
  `AUXILIARY_STRUCTURE_WARNING`

No write-scope expansion is needed.

### 4. `skills/dbm-publish/*`

This is the most important skill-level integration point.

Required changes:
- add optional manifest fields for admitted hypergraph evidence
- add a package-level hypergraph QA sub-check when
  `HYPERGRAPH_USE_MODE` includes QA
- the skill should classify hypergraph results separately from deterministic
  concordance results:
  - `CONCORDANCE_BLOCKER`
  - `HYPERGRAPH_QA_WARNING`
  - `HYPERGRAPH_QA_BLOCKER`
- blocked hypergraph QA must only block package readiness if:
  - the manifest opted into hypergraph QA, and
  - the configured policy says hypergraph QA is binding for the run

The package summary should explicitly report:
- whether hypergraph evidence was used
- whether it was planning-only or QA-binding
- which limitations were applied

## Publication Tooling Changes

### 1. `tools/publication/build_concordance_candidates.py`

Add optional hypergraph-assisted candidate enrichment.

Required changes:
- accept optional hypergraph inputs from the manifest
- when present and allowed, read:
  - nodes
  - hyperedges
  - evidence files such as discovered KTYs, subjects, objectives, and artifact
    mappings
- use those inputs only to:
  - identify repeated structural patterns across mapped sections
  - identify likely omitted participant sections
  - suggest new candidate rows for human/agent review

The tool must emit:
- `DiscoverySource = HYPERGRAPH_AUXILIARY` for hypergraph-suggested candidates
- a coverage summary field stating whether hypergraph evidence was used

It must not:
- generate canonical assertion values from graph topology
- override candidate values already grounded in mapped source content

### 2. `tools/publication/check_concordance.py`

Do not turn this into a graph-analysis tool.

Required changes:
- optionally consume the hypergraph use mode and binding policy from the
  manifest
- report hypergraph-related QA findings separately from concordance findings
- keep deterministic approved-register concordance checks as the core function

If hypergraph QA is included, it should remain a supplementary block of checks,
not a rewrite of the concordance engine.

### 3. `tools/publication/build_section_map.py`

Add optional hypergraph-assisted diagnostics, not authoritative remapping.

Required changes:
- when hypergraph evidence is admitted, use it to emit advisory diagnostics:
  - likely overloaded section clusters
  - likely omitted supporting KTYs
  - likely cross-section adjacency hotspots
- diagnostics must remain advisory until the human approves the final section
  map

### 4. `tools/publication/assemble_publication.py`

No authority change is needed, but package metadata should include:
- whether hypergraph evidence was used in the run
- which hypergraph snapshot was admitted
- whether hypergraph QA was binding or advisory

## Manifest And Artifact Changes

### `Publication_Input_Manifest.md`

Add these optional sections:

- `Auxiliary Structure Evidence`
  - `HYPERGRAPH_USE_MODE`
  - `HYPERGRAPH_SNAPSHOT_PATH`
  - `HYPERGRAPH_RUN_SUMMARY_PATH`
  - `HYPERGRAPH_QA_REPORT_PATH`
  - `HYPERGRAPH_QA_VERDICT`
  - `HYPERGRAPH_LIMITATIONS`

- `Authority Roles`
  - `ContentAuthority`
  - `AdmissionEvidence`
  - `AuxiliaryStructureEvidence`

### `Publication_Handoff_State.md`

Add fields:
- `HypergraphUseMode`
- `HypergraphSnapshot`
- `HypergraphQAVerdict`
- `HypergraphLimitations`
- `HypergraphInfluencedPlanning`
- `HypergraphInfluencedQA`

## Binding Policy

To avoid accidental overreach, add a binding-policy concept for hypergraph QA.

Recommended values:
- `ADVISORY_ONLY`
- `BLOCK_ON_BINDING_FAILURE`

Default:
- `ADVISORY_ONLY`

Rationale:
- C&L’s current hypergraph is clean enough that binding QA may be reasonable
- Deepcut’s current hypergraph still has known blockers, so advisory-only is
  the safer default there

## Current Root-Specific Guidance

### Comp & Liquids

The current hypergraph snapshot is suitable for controlled auxiliary use.

Recommended default:
- `HYPERGRAPH_USE_MODE = AUXILIARY_PLANNING_AND_QA`
- `HYPERGRAPH_QA_BINDING_POLICY = ADVISORY_ONLY` initially

Once the publication workflow proves stable, the root may later opt into
binding hypergraph QA if desired.

### Deepcut

The current reviewed hypergraph still carries known artifact-node collision and
merge-ambiguity blockers. Therefore:

Recommended default:
- `HYPERGRAPH_USE_MODE = AUXILIARY_PLANNING`
- or `NONE`

Do not use the current Deepcut hypergraph as binding package QA until the known
graph-quality issues are resolved.

## Implementation Phases

### Phase 1. Contract update

Revise:
- `agents/AGENT_DBM_PUBLISHER.md`
- `skills/dbm-concordance-seed/*`
- `skills/dbm-section-publish/*`
- `skills/dbm-publish/*`

so hypergraph use modes, authority boundaries, and QA semantics are explicit.

### Phase 2. Tool update

Revise:
- `tools/publication/build_section_map.py`
- `tools/publication/build_concordance_candidates.py`
- `tools/publication/check_concordance.py`
- `tools/publication/assemble_publication.py`

to support optional admitted hypergraph evidence.

### Phase 3. Manifest and handoff update

Add the required hypergraph fields to:
- `Publication_Input_Manifest.md`
- `Publication_Handoff_State.md`

### Phase 4. Controlled rehearsal

Rehearse the updated workflow on:
- Comp & Liquids with auxiliary planning + auxiliary QA
- Deepcut with planning-only or none

Verify the workflow remains stable even when one root has lower-quality
hypergraph evidence.

## Verification

The implementation is successful only when all of the following are true:

1. `DBM_PUBLISHER` can freeze an admitted hypergraph snapshot in the manifest
   without promoting it to content authority.

2. `dbm-concordance-seed` can use hypergraph evidence to improve candidate
   coverage and participant discovery without inventing values.

3. `dbm-section-publish` can emit hypergraph-informed QA warnings without using
   the graph as prose authority.

4. `dbm-publish` can run optional hypergraph QA and report it separately from
   deterministic concordance results.

5. `build_concordance_candidates.py` and `build_section_map.py` can consume
   admitted hypergraph evidence and emit advisory structural findings.

6. A clean hypergraph snapshot can enhance planning/QA, while a blocked
   hypergraph snapshot can be safely downgraded to advisory-only or excluded.

7. Publication readiness still depends first on:
   - upstream closure
   - approved mapping
   - section completeness
   - deterministic concordance

and not on hypergraph evidence alone.

## Assumptions

- Hypergraph outputs remain derivative artifacts, not decomposition truth.
- The publisher should become hypergraph-aware, not hypergraph-dependent.
- Existing concordance architecture remains valid and is enhanced rather than
  replaced.
- Deepcut and Comp & Liquids may temporarily use different hypergraph modes
  until graph-quality normalization improves.
