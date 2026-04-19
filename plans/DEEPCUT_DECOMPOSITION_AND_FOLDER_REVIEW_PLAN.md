# Deepcut Decomposition And Folder Review Plan

## Summary

This plan defines a systematic `Review + Repair` pass for `domain-test/domains/West_Doe_Deepcut_DBM` so another agent can execute it without making policy decisions.

The review targets the same failure modes found during the Comp & Liquids Phase 5/6 work:
- decomposition-local registers that drift out of parity with the main decomposition document
- incomplete or partially propagated `_ScopeChange` snapshots
- stale status / scope / identity pointers in KTY-local metadata
- stale terminology and shared-interface wording in KTY-local content
- downstream rerun sets that are incomplete or sequenced incorrectly

The executing agent is expected to repair decomposition-local truth and KTY-local metadata where the correction is mechanical and fully determined by the current authoritative decomposition state. The agent must not rewrite `Scoping.md` or `KA-*.md` during this pass; any content drift there becomes a downstream `TASK + domain-documents` rerun obligation.

## Root And Authorities

### Review root

- Root: `domain-test/domains/West_Doe_Deepcut_DBM`

### Current decomposition package

The Deepcut decomposition package currently uses the `DeepCut_*_v4` naming scheme and includes these authoritative files under `_Decomposition/`:

- `DeepCut_DOMAIN_DECOMP_FINAL_v4.md`
- `DeepCut_Category_Register_v4.csv`
- `DeepCut_Coverage_Telemetry_v4.json`
- `DeepCut_Domain_Ledger_v4.csv`
- `DeepCut_Knowledge_Subject_Register_v4.csv`
- `DeepCut_Knowledge_Type_Register_v4.csv`
- `DeepCut_Node_Summary_v4.csv`
- `DeepCut_Objective_Register_v4.csv`
- `DeepCut_Open_Issues_v4.csv`
- `DeepCut_Publication_Manifest_v4.md`
- `DeepCut_Scope_Boundary_Register_v4.csv`
- `DeepCut_Standalone_Subject_Coverage_v4.csv`
- `DeepCut_Vocabulary_Map_v4.csv`

`Archive.zip` is present in `_Decomposition/` but is not authoritative unless explicitly needed for forensic comparison.

### Scope-change chain

The active `_ScopeChange/_LATEST.md` currently points to `SCA-003_2026-04-19_0900/`. The review must treat the Deepcut `_ScopeChange` history as part of the system under review, not as archival background only.

### KTY-local review surface

The Deepcut root currently contains `132` `CAT-*/1_Working/KTY-*` folders. Every one of them is in scope for structural review.

### Governing contracts

The review must follow the current repository contracts, especially:
- revised `agents/AGENT_SCOPE_CHANGE.md`
- revised `plans/WEST_DOE_TWO_ROOT_DBM_REMEDIATION_AND_PUBLICATION_PLAN.md`
- revised `plans/WEST_DOE_EXECUTION_MODEL.md`
- revised `skills/domain-documents/{SKILL.md,QA_CHECKS.md,TOOL_POLICY.md}`

Those contracts establish:
- decomposition + decomposition-local annexes + `_ScopeChange` are valid direct-write surfaces for `DOMAIN`
- KTY-local metadata alignment after regeneration is a separate root-agent step
- `domain-documents` must never modify `_CONTEXT.md`, `_REFERENCES.md`, `_MEMORY.md`, or `_SEMANTIC.md`
- `Scoping.md` / `KA-*.md` content drift discovered during review is handled by reruns, not manual metadata-style patching

## Scope Boundaries

### In scope for direct review and possible repair

- `_Decomposition/` authoritative package
- `_ScopeChange/_LATEST.md`
- all Deepcut `SCA-*` snapshot folders
- KTY-local metadata files:
  - `_CONTEXT.md`
  - `_STATUS.md`
  - `_REFERENCES.md`

### In scope for review only, not direct content repair

- `Scoping.md`
- `KA-*.md`
- `_run_records/`
- `_DEPENDENCIES.md`
- `_MEMORY.md`
- `_SEMANTIC.md`

### Out of scope for direct writes in this review

- `_Aggregation/`
- hypergraph outputs
- publication outputs
- frozen planning artifacts outside the explicit review/reporting handoff
- source authority files under `_Sources/`

## Required Outputs

The executing agent must produce all of the following:

1. A Deepcut review run summary with:
   - repaired decomposition files
   - repaired `_ScopeChange` files
   - repaired KTY metadata files
   - unresolved findings
   - downstream rerun set
   - exact follow-on sequence
2. A parity matrix or equivalent structured checklist showing which decomposition-local surfaces were cross-checked
3. A KTY-level drift inventory grouped into:
   - metadata-aligned now
   - requires `domain-documents` rerun
   - unresolved / needs human decision
4. A terminology/interface sweep result
5. A final recommendation stating whether:
   - `TASK + domain-documents` reruns are required
   - `DOMAIN_HYPERGRAPH` must be rerun
   - `AUDIT_DECOMP` must be rerun

## Execution Sequence

Execute the review in this exact order.

### Phase 1. Baseline inventory

Build a review inventory for the whole Deepcut root:
- enumerate all files under `_Decomposition/`
- enumerate `_ScopeChange/_LATEST.md` and every `SCA-*` snapshot
- enumerate all `CAT-*/1_Working/KTY-*` folders
- record counts for:
  - categories
  - KTY folders
  - decomposition package files
  - snapshot folders

Do not start repairing anything until the inventory is complete.

### Phase 2. `_ScopeChange` contract review

Audit the Deepcut `_ScopeChange` chain before touching decomposition truth:
- confirm `_LATEST.md` points to the active intended snapshot
- confirm each active snapshot satisfies the current `AGENT_SCOPE_CHANGE` snapshot layout contract
- identify any snapshot folders that contain:
  - missing required artifacts
  - stale handoff wording
  - outdated propagation assumptions
  - ad hoc scripts or logs that imply undocumented corrective work

Repair rules:
- repair `_LATEST.md` if it is incorrect
- repair missing required snapshot artifacts only if the missing content can be reconstructed from already accepted Gate outputs in the snapshot chain
- do not delete old scripts or historical files from snapshots
- record non-contract extra files as historical residue, not blockers, unless they contradict accepted truth

### Phase 3. Decomposition-package parity review

Treat `DeepCut_DOMAIN_DECOMP_FINAL_v4.md` as the primary narrative surface and every `DeepCut_*_v4` register as decomposition-local truth that must be kept in parity where fields overlap.

Build a parity matrix across at least these dimensions:

- revision / active amendment state
- category counts
- KTY counts
- subject counts
- IN / TBD / OUT counts
- objective mappings
- open issues
- decision references
- vocabulary/canonical terminology
- standalone subject coverage
- any boundary-rule or scope-boundary registers
- any node/summary or coverage telemetry derivatives

Required cross-checks:
- main document vs category register
- main document vs knowledge type register
- main document vs knowledge subject register
- main document vs domain ledger
- main document vs objective register
- main document vs vocabulary map
- main document vs open-issues register
- main document vs scope-boundary register
- main document vs coverage telemetry JSON
- main document vs standalone subject coverage
- derivative summary tables vs their primary upstream register

Special rule:
- if any duplicated field is wrong in one place, reconcile every duplicated occurrence in the same execution pass
- do not patch only the first visible inconsistency

### Phase 4. KTY-folder metadata review

For every one of the `132` KTY folders, inspect:
- `_CONTEXT.md`
- `_STATUS.md`
- `_REFERENCES.md`
- `Scoping.md`
- all `KA-*.md`
- `_run_records/` if present

For each KTY, verify:

#### `_CONTEXT.md`

- KTY ID matches decomposition
- Name matches decomposition
- Category matches decomposition
- type / basis label matches decomposition
- description is not stale relative to current decomposition truth
- decomposition pointer points to the current Deepcut decomposition artifact

#### `_STATUS.md`

- lifecycle state is syntactically valid
- state is not contradicted by local run history
- state is not clearly incompatible with the actual presence of generated artifacts

#### `_REFERENCES.md`

- decomposition reference points to `DeepCut_DOMAIN_DECOMP_FINAL_v4.md`
- source references point to the correct Deepcut source package
- no stale references to superseded decomposition paths

#### `Scoping.md`

- KTY identity matches decomposition
- subject inventory matches current decomposition subject structure
- subject-to-artifact mapping is complete
- conflict table entries are not obviously stale after accepted amendments

#### `KA-*.md`

- artifact set matches `Scoping.md`
- artifact identity blocks align with KTY and Subject IDs
- obvious terminology and interface wording is not stale relative to accepted root truth

### Phase 5. Drift classification

Classify every finding into one of these buckets:

1. `DECOMP_LOCAL_REPAIR`
   - decomposition or `_ScopeChange` truth is wrong
   - repair directly in this run
2. `KTY_METADATA_REPAIR`
   - `_CONTEXT.md`, `_STATUS.md`, or `_REFERENCES.md` is stale
   - repair directly in this run
3. `DOMAIN_DOCUMENTS_RERUN`
   - `Scoping.md` and/or `KA-*.md` is stale
   - do not hand-edit content; queue exact rerun
4. `HUMAN_DECISION_REQUIRED`
   - not mechanically decidable from accepted authority

### Phase 6. Targeted terminology and interface sweep

Run a targeted sweep over both decomposition-local files and KTY-local content for these terms/patterns:

- `Pembina HVP Pipeline`
- `LPG`
- `NRM NEBC Connector`
- `LACT`
- `incinerator`
- `flare`
- shared utility wording
- cross-facility / cross-fence wording
- future-scope terms that may have been normalized inconsistently

At minimum, explicitly review these Deepcut KTYs because they are already known to be higher-risk:
- `KTY-04-16_LPG-Mercaptan-Treating-FUTURE`
- `KTY-04-17_LPG-Molecular-Seive-MS-Dehydration-FUTURE`
- `KTY-05-08_Process-Analyzers-and-Special-Instrumentation`
- any KTY flagged by grep with current-use `Pembina HVP Pipeline` or `LPG`

Also review any Deepcut KTYs named in the Deepcut terminology decisions or the authority allocation matrix as shared-interface normalizers.

### Phase 7. Repair execution

Apply repairs in this exact order:

1. `_ScopeChange` contract repairs
2. `_Decomposition` parity repairs
3. KTY-local metadata repairs
4. downstream rerun advisory generation

Direct repair rules:
- KTY-local metadata may be repaired only when the correct target state is fully determined by current decomposition truth
- do not rewrite `Scoping.md`
- do not rewrite `KA-*.md`
- do not mutate `_Aggregation`, hypergraph, or publication outputs

### Phase 8. Downstream rerun planning

For every KTY classified as `DOMAIN_DOCUMENTS_RERUN`, record:
- KTY ID
- exact reason for rerun
- whether the issue is identity drift, subject inventory drift, terminology drift, interface drift, or source-fidelity drift
- whether metadata alignment must follow the rerun

If any decomposition or metadata repair occurred, the follow-on sequence must be recorded exactly as:

1. `TASK + domain-documents` for affected KTYs
2. KTY-local metadata alignment check
3. `DOMAIN_HYPERGRAPH`
4. `AUDIT_DECOMP`
5. terminology QA sweep
6. targeted reruns for any failed or contradictory KTYs

## Deepcut-Specific Checks

The executing agent must include these Deepcut-specific checks.

### A. Future / current-scope framing

Verify that current Deepcut decomposition truth consistently distinguishes:
- active current-scope process units
- explicitly future units
- retired or superseded units

Pay special attention to:
- `KTY-04-16`
- `KTY-04-17`
- any KTY whose title or description still embeds `LPG` rather than normalized terminology

### B. Shared-interface normalization ownership

Confirm that Deepcut still carries the expected normalization-owner role for shared-interface rows referenced by:
- `plans/Authority_Allocation_Matrix.csv`
- `plans/Deepcut_Terminology_Decisions.md`

If a Deepcut shared-interface row is stale, repair Deepcut decomposition-local truth first, then record any required C&L follow-on only as a note, not as an edit to the C&L root.

### C. Snapshot residue

Review the Deepcut `SCA-*` snapshots for:
- missing required artifacts
- historical patch/apply scripts
- ledger-correction logs
- inconsistent run summaries

Historical residue may remain, but any active contradiction with accepted truth must be repaired or explicitly explained.

## Acceptance Criteria

The review is complete only when all of the following are true:

1. No internal contradiction remains across Deepcut decomposition-local registers for any duplicated count, status, objective, open-issue, or terminology field.
2. `_ScopeChange/_LATEST.md` is correct and active snapshots satisfy the current snapshot contract.
3. No repairable drift remains in Deepcut `_CONTEXT.md`, `_STATUS.md`, or `_REFERENCES.md`.
4. Every remaining `Scoping.md` / `KA-*.md` inconsistency is captured in an explicit `TASK + domain-documents` rerun set.
5. The final run summary clearly separates:
   - repaired now
   - rerun later
   - unresolved and why
6. The final handoff is decision complete and does not leave policy choices to the next agent.

## Explicit Defaults

These defaults are fixed for the executing agent:

- Review mode: `Review + Repair`
- Deepcut decomposition naming scheme remains `DeepCut_*_v4`; this review does not rename the package
- Direct repair scope includes `_Decomposition/`, `_ScopeChange/`, `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md`
- Direct repair scope excludes `Scoping.md`, `KA-*.md`, `_Aggregation`, hypergraph outputs, publication outputs
- Any content-level drift in `Scoping.md` / `KA-*.md` becomes a downstream rerun, not a manual patch
- The review must be executed entirely within the Deepcut root and must not mutate the Comp & Liquids root

## Handoff Instruction

The executing agent should begin by confirming the live inventory against this plan, then execute the review exactly in the sequence above. If the live Deepcut package shape differs materially from the assumptions here, the agent must stop and record the divergence before making repairs.
