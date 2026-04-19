# Comp And Liquids Decomposition And Folder Review Plan

## Summary

This plan defines a systematic post-Phase-6 `Review + Repair` pass for `domain-test/domains/West_Doe_Comp_and_Liquids_DBM` so another agent can execute it without making policy decisions.

The review targets the same failure modes surfaced during the Comp & Liquids SCA-003 Phase 5/6 implementation:
- decomposition-local annexes that drift out of parity with the main decomposition document
- incomplete or historically inconsistent `_ScopeChange` snapshots and pointers
- stale status / scope / identity pointers in KTY-local metadata
- stale terminology, routing, and shared-interface wording in KTY-local content
- incomplete downstream rerun closure after accepted decomposition amendments

This is a stabilization and closure review, not a duplicate of the live Phase 6 reruns. The executing agent is expected to run this review after the current Phase 6 regeneration work is complete, then repair decomposition-local truth and KTY-local metadata where the correction is mechanical and fully determined by the current authoritative decomposition state.

The agent must not rewrite `Scoping.md` or `KA-*.md` during this pass. Any content drift there becomes a downstream `TASK + domain-documents` rerun obligation.

## Root And Authorities

### Review root

- Root: `domain-test/domains/West_Doe_Comp_and_Liquids_DBM`

### Current decomposition package

The Comp & Liquids decomposition package currently uses the `WEST_DOE_DOMAIN_DECOMPOSITION.md` plus annex CSV naming scheme and includes these authoritative files under `_Decomposition/`:

- `WEST_DOE_DOMAIN_DECOMPOSITION.md`
- `annex_categories.csv`
- `annex_category_telemetry.csv`
- `annex_coverage_telemetry.csv`
- `annex_decision_log.csv`
- `annex_domain_ledger.csv`
- `annex_inventory.csv`
- `annex_knowledge_subjects.csv`
- `annex_knowledge_types.csv`
- `annex_kty_category_mapping.csv`
- `annex_objective_kty_mapping.csv`
- `annex_objectives.csv`
- `annex_open_issues.csv`
- `annex_unit_category_assignment.csv`
- `annex_unit_subject_mapping.csv`
- `annex_validation_checks.csv`
- `annex_vocabulary_map.csv`

`Archive.zip`, `README.txt`, and `_KTY_SCAFFOLD_BRIEF.md` may be useful for forensic review but are not primary truth surfaces unless a contradiction requires them.

### Scope-change chain

The active `_ScopeChange/_LATEST.md` currently points to `SCA-003_2026-04-19_0900/`.

The live `_ScopeChange/` surface also contains historical anomalies that must be treated as part of the system under review:
- a bare `SCA-001/` directory containing `Value_Engineering_Tracker.csv`
- `SCA-001_2026-04-14_0000/` with the full eight-artifact snapshot set
- `SCA-002_2026-04-14_0000/` with only `Pre_Change_Coverage.json`, `Post_Change_Coverage.json`, and `RUN_SUMMARY.md`
- `SCA-003_2026-04-19_0900/` with the full eight-artifact snapshot set

The review must treat the `_ScopeChange` history as part of the Comp & Liquids package under review, not as archival background only.

### KTY-local review surface

The Comp & Liquids root currently contains `111` `CAT-*/1_Working/KTY-*` folders. Every one of them is in scope for structural review.

The review must additionally give deeper attention to the `23` KTYs explicitly identified by the SCA-003 Phase 5 handoff as requiring Phase 6 regeneration:

- `KTY-01-01`
- `KTY-01-02`
- `KTY-01-03`
- `KTY-01-04`
- `KTY-02-01`
- `KTY-03-01`
- `KTY-03-02`
- `KTY-03-03`
- `KTY-04-01`
- `KTY-04-02`
- `KTY-04-05`
- `KTY-04-08`
- `KTY-04-09`
- `KTY-04-11`
- `KTY-04-12`
- `KTY-04-13`
- `KTY-04-14`
- `KTY-05-01`
- `KTY-05-02`
- `KTY-05-04`
- `KTY-05-05`
- `KTY-05-07`
- `KTY-12-04`

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
- all Comp & Liquids `SCA-*` snapshot folders
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

1. A Comp & Liquids review run summary with:
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
   - additional `TASK + domain-documents` reruns are required
   - `DOMAIN_HYPERGRAPH` must be rerun
   - `AUDIT_DECOMP` must be rerun
   - publication-readiness blockers remain

## Execution Sequence

Execute the review in this exact order.

### Phase 1. Baseline inventory

Build a review inventory for the whole Comp & Liquids root:
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

Audit the Comp & Liquids `_ScopeChange` chain before touching decomposition truth:
- confirm `_LATEST.md` points to the active intended snapshot
- confirm the active snapshot satisfies the current `AGENT_SCOPE_CHANGE` snapshot layout contract
- review older snapshots for:
  - missing required artifacts
  - stale handoff wording
  - outdated propagation assumptions
  - stray non-snapshot directories that may confuse future agents
  - historical residue that implies undocumented corrective work

Specific review targets:
- confirm `SCA-003_2026-04-19_0900/` still contains all eight required artifacts
- review `SCA-002_2026-04-14_0000/` as known incomplete historical residue
- classify the bare `SCA-001/` directory as either valid auxiliary residue or cleanup-needed ambiguity

Repair rules:
- repair `_LATEST.md` if it is incorrect
- repair active-snapshot artifact gaps only if the missing content can be reconstructed from already accepted Gate outputs
- do not delete old scripts, trackers, or historical files from snapshots unless explicitly instructed
- record non-contract extra files as historical residue, not blockers, unless they contradict accepted truth

### Phase 3. Decomposition-package parity review

Treat `WEST_DOE_DOMAIN_DECOMPOSITION.md` as the primary narrative surface and every annex CSV as decomposition-local truth that must be kept in parity where fields overlap.

Build a parity matrix across at least these dimensions:

- revision / active amendment state
- category counts
- KTY counts
- subject counts
- IN / TBD / OUT counts
- objective mappings
- open issues
- decision references
- vocabulary / canonical terminology
- KTY-to-category mappings
- unit-to-category mappings
- unit-to-subject mappings
- coverage telemetry and validation evidence
- inventory completeness

Required cross-checks:
- main document vs `annex_categories.csv`
- main document vs `annex_category_telemetry.csv`
- main document vs `annex_coverage_telemetry.csv`
- main document vs `annex_validation_checks.csv`
- main document vs `annex_domain_ledger.csv`
- main document vs `annex_knowledge_subjects.csv`
- main document vs `annex_knowledge_types.csv`
- main document vs `annex_objectives.csv`
- main document vs `annex_objective_kty_mapping.csv`
- main document vs `annex_kty_category_mapping.csv`
- main document vs `annex_open_issues.csv`
- main document vs `annex_decision_log.csv`
- main document vs `annex_vocabulary_map.csv`
- `annex_domain_ledger.csv` vs `annex_unit_category_assignment.csv`
- `annex_domain_ledger.csv` vs `annex_unit_subject_mapping.csv`
- `annex_knowledge_subjects.csv` vs `annex_unit_subject_mapping.csv`
- `annex_categories.csv` vs `annex_category_telemetry.csv`
- `annex_knowledge_types.csv` vs `annex_objective_kty_mapping.csv`
- `annex_inventory.csv` vs the actual decomposition package contents where relevant

Special rule:
- if any duplicated field is wrong in one place, reconcile every duplicated occurrence in the same execution pass
- do not patch only the first visible inconsistency

### Phase 4. KTY-folder review

For every one of the `111` KTY folders, inspect:
- `_CONTEXT.md`
- `_STATUS.md`
- `_REFERENCES.md`
- `Scoping.md`
- all `KA-*.md`
- `_run_records/` if present

For each KTY, verify:

#### `_CONTEXT.md`

- KTY ID matches decomposition
- name matches decomposition
- category matches decomposition
- type / basis label matches decomposition
- description is not stale relative to current decomposition truth
- decomposition pointer points to `WEST_DOE_DOMAIN_DECOMPOSITION.md`

#### `_STATUS.md`

- lifecycle state is syntactically valid
- state is not contradicted by local run history
- state is not clearly incompatible with the actual presence of generated artifacts

#### `_REFERENCES.md`

- decomposition reference points to `WEST_DOE_DOMAIN_DECOMPOSITION.md`
- source references point to the correct Comp & Liquids source package
- no stale references to superseded decomposition paths or retired amendment assumptions

#### `Scoping.md`

- KTY identity matches decomposition
- subject inventory matches current decomposition subject structure
- subject-to-artifact mapping is complete
- conflict table entries are not obviously stale after accepted amendments

#### `KA-*.md`

- artifact set matches `Scoping.md`
- artifact identity blocks align with KTY and Subject IDs
- obvious terminology and interface wording is not stale relative to accepted root truth

For the `23` Phase 6 KTYs named above, perform a deeper post-regeneration review that explicitly checks whether the rerun actually closed the intended correction set.

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
- `NRM NEBC Connector`
- `LPG`
- `NGL`
- `LACT`
- `incinerator`
- `flare`
- `services 4-25 equipment only`
- `4-25 service only`
- shared utility wording
- cross-facility / cross-fence wording
- dual-LACT assertions
- `5,000 hp`
- `5,200 hp`

At minimum, explicitly review these KTYs because they were already identified as higher-risk by the SCA-003 handoff:
- `KTY-04-05` for the `5,000 hp` / `5,200 hp` basis contradiction
- `KTY-04-09` for incinerator framing and cleared `CONFLICT-01`
- `KTY-04-11` for LACT routing and preserved `SUB-04-11-12 OUT`
- `KTY-01-04` for flare exclusion language
- `KTY-05-05` for the resolved flare conflict table and five subjects now `IN`
- `KTY-03-04`, `KTY-04-06`, `KTY-04-07`, and `KTY-05-08` as known expansion/sweep candidates

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

## Comp And Liquids-Specific Checks

The executing agent must include these Comp & Liquids-specific checks.

### A. SCA-003 stabilization hotspots

Confirm that the SCA-003 change set remains fully propagated across every duplicated decomposition-local surface, especially:
- the five flare subjects that moved from `TBD` to `IN`
- incinerator framing as shared `03-25/04-25`, not `4-25`-only
- LACT routing as one NRM LACT to `NRM NEBC Connector`
- CAT-004 and CAT-005 reconciled counts
- objective mappings with retired KTY supporters removed
- the unified KTY-count convention: `84 active (4 retired, 88 total)`

### B. Secondary mapping annex parity

Comp & Liquids already demonstrated that secondary mapping annexes can lag behind primary truth. The review must therefore explicitly treat these as high-risk parity surfaces:
- `annex_unit_category_assignment.csv`
- `annex_unit_subject_mapping.csv`
- `annex_kty_category_mapping.csv`
- `annex_objective_kty_mapping.csv`
- `annex_inventory.csv`

No decomposition review is complete if these remain inconsistent with the main document and primary annexes.

### C. Historical snapshot residue

Review the Comp & Liquids `SCA-*` snapshots for:
- missing required artifacts
- incomplete older snapshots
- stale gate sequencing language
- ambiguous historical directories such as the bare `SCA-001/`
- inconsistent run summaries

Historical residue may remain, but any active contradiction with accepted truth must be repaired or explicitly explained.

### D. Post-regeneration closure

Because this plan is meant to run after Phase 6, the executing agent must verify not only that the reruns happened, but that they actually closed the intended correction set for the 23 named KTYs.

For each of those 23 KTYs, verify:
- regenerated `Scoping.md` reflects the current decomposition truth
- regenerated `KA-*.md` set is complete and consistent
- post-regeneration `_CONTEXT.md` and `_STATUS.md` alignment occurred
- no stale pre-SCA-003 terminology or routing basis remains

## Acceptance Criteria

The review is complete only when all of the following are true:

1. No internal contradiction remains across Comp & Liquids decomposition-local registers for any duplicated count, status, objective, open-issue, decision, or terminology field.
2. `_ScopeChange/_LATEST.md` is correct and the active snapshot satisfies the current snapshot contract.
3. Historical snapshot anomalies are either repaired where appropriate or explicitly classified as non-blocking residue.
4. No repairable drift remains in Comp & Liquids `_CONTEXT.md`, `_STATUS.md`, or `_REFERENCES.md`.
5. Every remaining `Scoping.md` / `KA-*.md` inconsistency is captured in an explicit `TASK + domain-documents` rerun set.
6. The final run summary clearly separates:
   - repaired now
   - rerun later
   - unresolved and why
7. The final handoff is decision complete and does not leave policy choices to the next agent.

## Explicit Defaults

These defaults are fixed for the executing agent:

- Review mode: `Review + Repair`
- This is a post-Phase-6 stabilization review, not a replacement for the live Phase 6 run
- Comp & Liquids decomposition naming remains `WEST_DOE_DOMAIN_DECOMPOSITION.md` plus annex CSVs; this review does not rename the package
- Direct repair scope includes `_Decomposition/`, `_ScopeChange/`, `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md`
- Direct repair scope excludes `Scoping.md`, `KA-*.md`, `_Aggregation`, hypergraph outputs, publication outputs
- Any content-level drift in `Scoping.md` / `KA-*.md` becomes a downstream rerun, not a manual patch
- The review must be executed entirely within the Comp & Liquids root and must not mutate the Deepcut root

## Handoff Instruction

The executing agent should begin by confirming the live inventory against this plan, then execute the review exactly in the sequence above. If the live Comp & Liquids package shape differs materially from the assumptions here, the agent must stop and record the divergence before making repairs.
