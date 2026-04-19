# Plan: West Doe Two-Root DBM Remediation And Publication

## Status

Recommended for execution. Not yet run under this plan.

## Purpose

Provide a concrete, decision-complete run plan for producing two final DBMs:

- one from `domain-test/domains/West_Doe_Deepcut_DBM`
- one from `domain-test/domains/West_Doe_Comp_and_Liquids_DBM`

The governing source authority package for the remediation campaign is:

- source anchor PDF:
  `domain-test/domains/West_Doe_Combined/_Sources/26020-04-PR-PDB-001 R0_IFD Uncontrolled 2026.04.16.pdf`
- cleaned package root:
  `domain-test/domains/West_Doe_Combined/_Sources/west_doe_process_design_basis_clean/`

Within that package:

- `Process_DBM_fixed.md` is the narrative working authority
- `data/*.csv` are the canonical tabular authority
- `metadata/tables.yaml` is the source-page traceability map
- `validation/validation_report.md` and `validation/validate_tables.py` are the
  validation record

This plan assumes the cleaned source authority package is the strongest
available current-state process-basis package in the project and that both
existing DOMAIN roots must be brought into strict accordance with it before
publication.

This is a **two-root publication plan**, not a combined-root publication plan.

## Governing Decisions

### 1. Publication mode

The final output remains:

- two separate published DBMs
- one publication run per execution root

No combined `DBM_PUBLISHER` run is authorized under this plan.

### 2. Remediation posture

Use **full conformity**.

Meaning:

- do not limit updates to obvious deltas only
- correct any material drift between each root and the cleaned source authority
  package
- normalize shared terminology and interface descriptions
- remove or retire superseded statements where they conflict with the
  current-state basis

### 3. Publication authority

For final publication, authority order is:

1. approved publication schema and rules inside each `DBM_PUBLISHER` run
2. approved merged decomposition state in the target root
3. accepted post-`SCOPE_CHANGE` state in the target root
4. regenerated KTY-local `Scoping.md` and `KA-*.md` artifacts in the target root
5. the cleaned source authority package as the governing upstream source and
   provenance input, with the PDF retained as the ultimate source anchor
6. legacy root-local source DBMs only as historical / provenance inputs

### 4. Combined root role

`domain-test/domains/West_Doe_Combined/` is **not** the publication root for
this plan.

It is used only as:

- authority source location for the cleaned source authority package
- campaign control location if the human wants to store cross-root planning
  artifacts there

It must not be treated as a valid `DBM_PUBLISHER` execution root unless a later
workflow creates its own `_Decomposition/` and `_ScopeChange/` truth.

## Scope Boundaries

### In scope

- decomposition-truth remediation in both existing DOMAIN roots
- downstream regeneration required to bring KTY-local content into conformity
- cross-root shared-system and interface alignment
- two final `DBM_PUBLISHER` runs

### Out of scope

- creation of a new combined DOMAIN execution root
- a single combined published DBM
- direct publication from the cleaned source authority package without
  reconciling the two roots
- ad hoc manual patching inside `DBM_PUBLISHER` to bypass stale upstream truth

## Primary Roots

### Root A

- `domain-test/domains/West_Doe_Deepcut_DBM`

### Root B

- `domain-test/domains/West_Doe_Comp_and_Liquids_DBM`

### Governing source

- `domain-test/domains/West_Doe_Combined/_Sources/26020-04-PR-PDB-001 R0_IFD Uncontrolled 2026.04.16.pdf`
- `domain-test/domains/West_Doe_Combined/_Sources/west_doe_process_design_basis_clean/Process_DBM_fixed.md`
- `domain-test/domains/West_Doe_Combined/_Sources/west_doe_process_design_basis_clean/data/*.csv`

## Execution Principles

1. The cleaned source authority package governs the campaign.
2. The original PDF remains the ultimate source anchor.
3. `Process_DBM_fixed.md` is used for section-level prose and narrative routing.
4. `data/*.csv` is used as canonical authority whenever tabular data drives a
   remediation decision.
5. `metadata/tables.yaml` must be used to trace table-driven statements back to
   source pages.
6. `validation/validation_report.md` is a confidence record, not an authority
   override.
7. `SCOPE_CHANGE` amends decomposition truth only. It does not regenerate
   downstream artifacts.
8. Downstream knowledge artifacts must be regenerated after each accepted
   amendment.
9. No `DBM_PUBLISHER` run starts until the target root has:
   - accepted `SCOPE_CHANGE` state
   - regenerated affected KTY artifacts
   - regenerated hypergraph
   - rerun structural audit
   - passed terminology and interface checks
   - recorded a handoff-state that names the accepted snapshot, derivative-package status, closure verdict, and blockers
10. Shared systems must be aligned across both roots before either DBM is
    accepted for publication.
11. The campaign runs **Deepcut first, then Comp and Liquids second**.

## Governance Terms For This Campaign

- **Authoritative remediation truth** = the accepted decomposition files plus
  accepted `_ScopeChange` snapshot artifacts in the target root
- **Derivative package** = any downstream package assembled from accepted
  remediation truth but not itself remediation truth, including regenerated
  KTY-local artifacts, hypergraph snapshots, `AUDIT_DECOMP` snapshots, and
  `DBM_PUBLISHER` publication packages
- **Handoff-state** = the explicit state record at the end of a phase that
  names the accepted source snapshot, derivative-package status, closure
  verdict, open blockers, and next owning workflow
- **Closure** = the condition in which accepted remediation truth exists,
  required derivative packages are current or explicitly deferred, audit state
  is recorded, and blockers are exposed rather than hidden
- **Modular decomposition package** = the preferred package shape for both
  roots: a concise main decomposition document plus authoritative companion
  registers plus `_ScopeChange` state, as defined in `AGENT_DECOMP_BASE.md`.
  Monolithic single-file renders, if produced, are derived publication
  artifacts and are not the authoritative amendment surface

## Why Deepcut Runs First

Deepcut is the first remediation target for this plan because:

1. its existing scope-change artifacts already describe a mature downstream
   rerun pattern
2. many shared systems and central process definitions are expressed from the
   04-25 facility side
3. its current `_ScopeChange` history already includes interface coordination
   acknowledgments for 3-25 and 4-25

This does **not** make Deepcut a higher authority than the cleaned source
authority package.
It only establishes the execution order for the remediation campaign.

## Required Control Artifact

Before any new `SCOPE_CHANGE` run, create a campaign control artifact:

- `Authority_Allocation_Matrix.csv`

Recommended location:

- `plans/Authority_Allocation_Matrix.csv`

The human may choose the storage location, but the matrix must be frozen before
the first remediation run starts.

### Required columns

The matrix must contain exactly these columns:

| Column | Purpose |
|---|---|
| `AuthorityRef` | Stable row ID for the campaign |
| `SourceSection` | Section number/title in `Process_DBM_fixed.md` or canonical table ID traced through `metadata/tables.yaml` |
| `SourceExcerptSummary` | Short summary of the governing statement |
| `OwningRoot` | `West_Doe_Deepcut_DBM` or `West_Doe_Comp_and_Liquids_DBM` |
| `SecondaryRoot` | other root if shared, else blank |
| `ScopeClass` | `DEEPCUT_ONLY`, `COMP_LIQ_ONLY`, `SHARED_INTERFACE` |
| `ChangeType` | `ADD`, `REMOVE`, `MODIFY`, `RECLASSIFY`, or `VERIFY_ONLY` |
| `TargetCATs` | CAT IDs expected to change |
| `TargetKTYs` | KTY IDs expected to change |
| `SharedTermSet` | normalized terms that must match across roots |
| `PublicationImpact` | `HIGH`, `MEDIUM`, or `LOW` |
| `Notes` | any required explanation or mapping note |

### Matrix authoring rules

1. Every material statement in the cleaned source authority package that affects
   either root must be represented.
2. Shared statements must never be duplicated as two unrelated rows. Use one
   `SHARED_INTERFACE` row with an owning root and a secondary root.
3. If a statement appears to govern both roots but with different local
   manifestations, record that in `Notes` rather than splitting terminology.
4. The matrix is not a publication artifact by default. It is a campaign
   control artifact.

## Shared-System Policy

Use the following rule set for all `SHARED_INTERFACE` rows.

### Primary rule

The cleaned source authority package is the governing authority.

### Secondary rule

For campaign sequencing only:

- Deepcut defines the first-pass normalized wording for shared systems
- Comp and Liquids must align to that wording where the same real system is
  being referenced

### Escalation rule

If Comp and Liquids reveals a stronger conflict with the cleaned source
authority package, Deepcut must be reopened for targeted remediation.

### No-local-override rule

Neither root may preserve contradictory legacy wording simply because it
already exists in local KTY artifacts.

## Run Plan Overview

The campaign has eight phases:

1. Freeze campaign authority inputs
2. Build and approve the allocation matrix
3. Run `SCOPE_CHANGE` on Deepcut
4. Regenerate Deepcut downstream artifacts
5. Run `SCOPE_CHANGE` on Comp and Liquids
6. Regenerate Comp and Liquids downstream artifacts
7. Run cross-root conformity gate
8. Publish each root independently with `DBM_PUBLISHER`

## Phase 1 — Freeze Campaign Authority Inputs

### Objective

Freeze the upstream material that governs both remediation runs.

### Inputs

- `domain-test/domains/West_Doe_Combined/_Sources/26020-04-PR-PDB-001 R0_IFD Uncontrolled 2026.04.16.pdf`
- `domain-test/domains/West_Doe_Combined/_Sources/west_doe_process_design_basis_clean/Process_DBM_fixed.md`
- `domain-test/domains/West_Doe_Combined/_Sources/west_doe_process_design_basis_clean/data/*.csv`
- `domain-test/domains/West_Doe_Combined/_Sources/west_doe_process_design_basis_clean/metadata/tables.yaml`
- `domain-test/domains/West_Doe_Combined/_Sources/west_doe_process_design_basis_clean/validation/validation_report.md`
- `domain-test/domains/West_Doe_Deepcut_DBM/_ScopeChange/_LATEST.md`
- `domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_ScopeChange/_LATEST.md`
- current decomposition artifacts in both roots

### Required actions

1. Confirm that the cleaned source authority package is the governing source
   bundle for the campaign.
2. Record the active `_ScopeChange/_LATEST.md` pointers in both roots.
3. Record the current decomposition file set for both roots.
4. Record whether the page 18 and 19 manually transcribed specification tables
   have received a human second-person review. If not, any matrix rows derived
   from them must be flagged in `Notes` for human confirmation.
5. Do not begin remediation before the human explicitly accepts this freeze.

### Deliverable

Create or record a campaign note containing:

- the path to the frozen source anchor PDF
- the path to the frozen cleaned package root
- the path to the frozen `Process_DBM_fixed.md`
- the active SCA pointers in both roots
- the date/time of the freeze
- the statement that later edits to the cleaned source authority package are out
  of scope unless the campaign is intentionally restarted
- the recorded manual-review status for the page 18 and 19 specification tables

## Phase 2 — Build And Approve The Allocation Matrix

### Objective

Translate the cleaned source authority package into root-specific and shared
remediation work.

### Required actions

1. Read `Process_DBM_fixed.md` end to end.
2. Review the canonical CSV tables under `data/`, using `metadata/tables.yaml`
   to trace table-driven facts back to source pages.
3. Break the package into governing statements and table-derived facts by
   section, subsection, and canonical table.
4. Classify each statement into:
   - `DEEPCUT_ONLY`
   - `COMP_LIQ_ONLY`
   - `SHARED_INTERFACE`
5. Assign every row to:
   - an owning root
   - optional secondary root
   - concrete CAT and KTY targets where already known
6. Normalize the shared term set for:
   - facility names
   - utility names
   - interface equipment names
   - product names
   - storage and transfer terminology
   - flare / incinerator wording
   - LACT references
7. Human reviews and approves the matrix.

### Acceptance condition

No remediation run begins until the matrix is approved.
Any matrix row derived from the manually transcribed page 18 or 19 specification
tables must either:

- be explicitly accepted by the human, or
- be flagged in `Notes` as requiring human confirmation before publication

## Phase 3 — Run `SCOPE_CHANGE` On Deepcut

### Objective

Amend Deepcut decomposition truth so it reflects the current state in the
cleaned source authority package.

### Target root

- `domain-test/domains/West_Doe_Deepcut_DBM`

### Briefing package for `SCOPE_CHANGE`

Provide:

- frozen cleaned source authority package
- approved `Authority_Allocation_Matrix.csv`
- only the matrix rows where:
  - `OwningRoot=West_Doe_Deepcut_DBM`, or
  - `SecondaryRoot=West_Doe_Deepcut_DBM`

### Gate requirements

#### Gate 1

Require `SCOPE_CHANGE` to parse the requested amendments into an action table
covering:

- process narrative updates for 04-25
- feed and product basis updates
- equipment and system configuration changes
- shared utility and interface statements touching 04-25 truth
- terminology normalization

#### Gate 2

Require impact assessment to enumerate:

- affected CAT rows
- affected KTY rows
- affected SUB rows where applicable
- vocabulary changes
- shared/interface rows that must remain mirrored in Comp and Liquids
- downstream rerun advisory set

#### Gate 3

Approve only decomposition-truth edits plus allowed scope-change snapshot
artifacts.

Do **not** allow direct editing of:

- KTY-local production documents
- `_Aggregation` outputs
- hypergraph outputs
- publication outputs

#### Gate 4 and Gate 5

Accept the Deepcut amendment only when:

- the decomposition truth is updated
- `_ScopeChange/_LATEST.md` points to the new snapshot
- the snapshot records the downstream rerun set
- the snapshot includes the handoff-state fields needed to close derivative
  packages in Phase 4

### Required outputs

The new Deepcut SCA snapshot must include:

- `Amendment_Actions.csv`
- `Impact_Assessment.md`
- `Decision_Log.md`
- `Handoff_State.md`
- `RUN_SUMMARY.md`
- downstream rerun recommendations

## Phase 4 — Regenerate Deepcut Downstream Artifacts

### Objective

Bring Deepcut production artifacts into conformity with the newly accepted
scope-change state.

### Required sequence

Run in this order:

1. `TASK + domain-documents` for every affected KTY
2. `TASK + kty-metadata-align` for every affected KTY. This is a separate
   root-agent-owned dispatch; `domain-documents` remains metadata-immutable.
3. `TASK + decomposition-package-review` for the full Deepcut root if
   decomposition-local truth changed materially during the campaign
4. `DOMAIN_HYPERGRAPH` for the full Deepcut root
5. `AUDIT_DECOMP`
6. terminology QA / stale-term sweep across the regenerated KTY set
7. targeted reruns for any failed or contradictory KTYs
8. record handoff-state / closure status in the accepted Deepcut SCA snapshot

### `domain-documents` scope rule

Start with the KTYs explicitly named in the accepted amendment set.

Expand the rerun set if any affected KTY:

- references a shared system whose normalized term changed
- references a retired or renamed sibling KTY / SUB
- still contains superseded design-basis statements

### Terminology QA rule

The sweep must explicitly look for:

- stale facility names
- stale product names
- stale shared-system labels
- legacy interface wording that contradicts the cleaned source authority package

### Handoff-state rule

Phase 4 is not closed until the accepted Deepcut `_ScopeChange` snapshot
contains a handoff-state that records:

- the accepted SCA snapshot path
- the derivative-package status of regenerated KTY artifacts,
  `DOMAIN_HYPERGRAPH`, and `AUDIT_DECOMP`
- whether targeted reruns remain open
- the closure verdict for advancement into Phase 7

### Deepcut acceptance condition

Deepcut is ready to advance only when:

- affected KTY artifacts are regenerated
- no blocking `decomposition-package-review` findings remain
- no blocking `AUDIT_DECOMP` failures remain
- no blocking terminology contradictions remain
- no blocking contradiction with the cleaned source authority package remains in
  regenerated
  artifacts
- the accepted SCA snapshot records a handoff-state with no hidden open work

## Phase 5 — Run `SCOPE_CHANGE` On Comp And Liquids

### Objective

Amend Comp and Liquids decomposition truth so it reflects the current state in
the cleaned source authority package and remains compatible with the remediated
Deepcut root.

### Target root

- `domain-test/domains/West_Doe_Comp_and_Liquids_DBM`

### Briefing package for `SCOPE_CHANGE`

Provide:

- frozen cleaned source authority package
- approved `Authority_Allocation_Matrix.csv`
- the accepted Deepcut terminology normalization decisions
- only the matrix rows where:
  - `OwningRoot=West_Doe_Comp_and_Liquids_DBM`, or
  - `SecondaryRoot=West_Doe_Comp_and_Liquids_DBM`

### Gate requirements

#### Gate 1

Require `SCOPE_CHANGE` to cover:

- 03-25 compressor station current-state process basis
- liquids hub current-state process basis
- shared utility and interface statements
- storage / transfer / treating descriptions
- LACT and third-party interface treatment
- terminology normalization against the cleaned source authority package

#### Gate 2

Require impact assessment to enumerate:

- affected CAT rows
- affected KTY rows
- affected SUB rows where applicable
- shared/interface rows that must stay aligned with Deepcut
- downstream rerun advisory set

#### Gate 3

Approve only decomposition-truth edits plus allowed scope-change snapshot
artifacts.

Do **not** allow direct editing of:

- KTY-local production documents
- `_Aggregation` outputs
- hypergraph outputs
- publication outputs

#### Gate 4 and Gate 5

Accept the Comp and Liquids amendment only when:

- the decomposition truth is updated
- `_ScopeChange/_LATEST.md` points to the new snapshot
- the snapshot records the downstream rerun set
- the snapshot includes the handoff-state fields needed to close derivative
  packages in Phase 6

### Required outputs

The new Comp and Liquids SCA snapshot must include:

- `Amendment_Actions.csv`
- `Impact_Assessment.md`
- `Decision_Log.md`
- `Handoff_State.md`
- `RUN_SUMMARY.md`
- downstream rerun recommendations

## Phase 6 — Regenerate Comp And Liquids Downstream Artifacts

### Objective

Bring Comp and Liquids production artifacts into conformity with the newly
accepted scope-change state.

### Required sequence

Run in this order:

1. `TASK + domain-documents` for every affected KTY
2. `TASK + kty-metadata-align` for every affected KTY. This is a separate
   root-agent-owned dispatch; `domain-documents` remains metadata-immutable.
3. `TASK + decomposition-package-review` for the full root if
   decomposition-local truth changed materially during the campaign
4. `DOMAIN_HYPERGRAPH` for the full root
5. `AUDIT_DECOMP`
6. terminology QA / stale-term sweep across the regenerated KTY set, including
   any shared-term carryover from accepted Deepcut decisions
7. targeted reruns for any failed or contradictory KTYs
8. update the accepted Comp and Liquids SCA snapshot with handoff-state and
   closure status for Phase 7

### Expansion rule

Expand the rerun set beyond explicitly amended KTYs if:

- a shared-system term changed in Deepcut and must be mirrored here
- a storage / transfer / treating chain description changed in the cleaned source
  authority package
- a KTY still references a superseded interface assumption

### Derivative-package rule

Within Phase 6, regenerated KTY artifacts, the hypergraph snapshot, and the
`AUDIT_DECOMP` snapshot are derivative packages. They must all cite the
accepted Comp and Liquids SCA snapshot as their source boundary. None of them
may be treated as a substitute for accepted decomposition truth.

### Handoff-state rule

Phase 6 is not closed until the accepted Comp and Liquids `_ScopeChange`
snapshot records:

- the accepted SCA snapshot path
- the derivative-package status of regenerated KTY artifacts,
  `DOMAIN_HYPERGRAPH`, and `AUDIT_DECOMP`
- any remaining targeted reruns or terminology blockers
- the closure verdict for advancement into Phase 7

### Acceptance condition

Comp and Liquids is ready to advance only when:

- affected KTY artifacts are regenerated
- no blocking `decomposition-package-review` findings remain
- no blocking `AUDIT_DECOMP` failures remain
- no blocking terminology contradictions remain
- no blocking contradiction with the cleaned source authority package remains in
  regenerated
  artifacts
- the accepted SCA snapshot records a handoff-state with no hidden open work

## Phase 7 — Cross-Root Conformity Gate

### Objective

Ensure both roots are mutually compatible before publication.

### Inputs

- approved allocation matrix
- remediated Deepcut root
- remediated Comp and Liquids root
- frozen cleaned source authority package
- the accepted handoff-state from each root's latest SCA snapshot

### Required checks

For every `SHARED_INTERFACE` matrix row, verify:

1. the same real system is named consistently
2. shared utility descriptions are compatible
3. shared flare / incinerator references do not conflict
4. shared power / fuel gas / instrument air references do not conflict
5. interface routing statements do not conflict
6. product naming is normalized
7. scope boundaries are complementary, not contradictory
8. neither root preserves legacy statements that were superseded by the cleaned
   source authority package

### Failure rule

If any shared/interface row fails:

- do not start either `DBM_PUBLISHER` run
- reopen the affected root with:
  - targeted `SCOPE_CHANGE`, or
  - targeted `domain-documents` reruns,
  depending on whether the failure is decomposition truth or regenerated
  artifact content

If a root arrives without an explicit handoff-state or with open derivative
closure still recorded, treat that as a Phase 7 input failure and do not assess
shared/interface conformity as if the root were ready.

### Acceptance condition

Only when all shared/interface rows pass may publication begin.

## Phase 8 — Publish With `DBM_PUBLISHER`

Run two independent publication workflows.

### Publication run A — Deepcut

#### Execution root

- `domain-test/domains/West_Doe_Deepcut_DBM`

#### Gate 1 requirements

Freeze `Publication_Input_Manifest.md` with:

- accepted decomposition files
- accepted `_ScopeChange/_LATEST.md`
- accepted handoff-state from the governing SCA snapshot
- regenerated KTY-local artifacts
- relevant local source DBM / TOC files
- the cleaned source authority package as promoted provenance/history input,
  with the source PDF retained as the anchor
- optionally the allocation matrix as a planning aid if traceability to
  shared-system ownership is desired

#### Gate 2 requirements

Run the knowledge-landscape review from current Deepcut state only.

#### Gate 3 requirements

Design the Deepcut publication schema and rules only for the 04-25 DBM.

#### Gate 4 requirements

Approve:

- `Section_Map.csv`
- `Publication_Concordance_Register.csv`

#### Gate 5 requirements

Dispatch section synthesis.

#### Gate 6 requirements

Run package publication and readiness review.

#### Gate 7 requirements

Accept the package only if:

- no blocking concordance issues remain
- no shared/interface contradiction remains
- the package reads as current-state Deepcut basis

### Publication run B — Comp And Liquids

#### Execution root

- `domain-test/domains/West_Doe_Comp_and_Liquids_DBM`

#### Gate 1 requirements

Freeze `Publication_Input_Manifest.md` with:

- accepted decomposition files
- accepted `_ScopeChange/_LATEST.md`
- accepted handoff-state from the governing SCA snapshot
- regenerated KTY-local artifacts
- relevant local source DBM / TOC files
- the cleaned source authority package as promoted provenance/history input,
  with the source PDF retained as the anchor
- optionally the allocation matrix as a planning aid if traceability to
  shared-system ownership is desired

#### Gate 2 requirements

Run the knowledge-landscape review from current Comp and Liquids state only.

#### Gate 3 requirements

Design the publication schema and rules only for the 03-25 / liquids DBM.

#### Gate 4 requirements

Approve:

- `Section_Map.csv`
- `Publication_Concordance_Register.csv`

#### Gate 5 requirements

Dispatch section synthesis.

#### Gate 6 requirements

Run package publication and readiness review.

#### Gate 7 requirements

Accept the package only if:

- no blocking concordance issues remain
- no shared/interface contradiction remains
- the package reads as current-state Comp and Liquids basis

## Optional `ORCHESTRATOR` Usage

`ORCHESTRATOR` may be used in this plan, but only as a control-plane runner for
downstream reruns and reporting.

### Allowed `ORCHESTRATOR` role

- dispatch `domain-documents`
- dispatch `DOMAIN_HYPERGRAPH`
- summarize project state
- record rerun progress

### Disallowed `ORCHESTRATOR` role

- redefining remediation scope
- deciding publication authority
- overriding `SCOPE_CHANGE` decisions
- editing decomposition truth directly
- bypassing cross-root conformity checks

## Explicit Acceptance Criteria

### Campaign complete

The campaign is complete only when all of the following are true:

1. both roots have accepted new scope-change state aligned to the cleaned source
   authority package
2. all affected KTYs in both roots have been regenerated
3. both roots have regenerated hypergraph snapshots
4. both roots pass post-remediation `AUDIT_DECOMP`
5. both roots pass terminology QA
6. both roots have accepted handoff-state showing derivative-package closure
   for Phase 7
7. all shared/interface matrix rows pass cross-root conformity review
8. both `DBM_PUBLISHER` runs complete without blocking readiness issues
9. the two published DBMs are mutually compatible and individually consistent
   with the cleaned source authority package

### Deepcut publication-ready

Deepcut is publication-ready only when:

- the final package expresses current-state 04-25 design basis
- no retained text contradicts the cleaned source authority package
- shared systems are described compatibly with Comp and Liquids
- any remaining `TBD` burden is explicitly acceptable to the human

### Comp and Liquids publication-ready

Comp and Liquids is publication-ready only when:

- the final package expresses current-state 03-25 / liquids design basis
- no retained text contradicts the cleaned source authority package
- shared systems are described compatibly with Deepcut
- any remaining `TBD` burden is explicitly acceptable to the human

## Default Failure Handling

### If `SCOPE_CHANGE` reveals unresolved ambiguity

- stop and resolve it at the decomposition layer
- do not defer ambiguity into `domain-documents` or `DBM_PUBLISHER`

### If regenerated KTY artifacts contradict decomposition truth

- rerun `domain-documents` for affected KTYs
- if contradiction persists, reopen `SCOPE_CHANGE`

### If cross-root conformity fails

- treat it as an upstream truth problem
- repair the responsible root before publication

### If `DBM_PUBLISHER` concordance blocks readiness

- return to targeted section reruns or upstream remediation as indicated by the
  package gate

## Final Instruction To The Implementer

Do not shortcut from the cleaned source authority package directly to
publication.

The required path is:

1. freeze authority
2. approve allocation matrix
3. remediate Deepcut
4. regenerate Deepcut
5. remediate Comp and Liquids
6. regenerate Comp and Liquids
7. pass cross-root conformity gate
8. publish Deepcut
9. publish Comp and Liquids

Any attempt to skip phases 3 through 7 risks publishing two DBMs that are
individually readable but structurally inconsistent with the strongest current
project authority.
