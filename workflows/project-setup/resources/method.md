# project-setup — method

## Method

### Schedule workflow (when selected)

1. **Ingest and validate:** freeze accepted decomposition/dependency snapshots; confirm scope, schedule basis, and edge-classification rules.
2. **Structure and sequence:** use deterministic graph tools where possible; present the candidate network or constraint matrix for human correction.
3. **Durations and calendars:** generate a blank duration template by default; collect human durations, calendars, milestones, and gates.
4. **Render:** compute dates and produce reviewable CSV/Mermaid plus basis-appropriate critical-path or risk analysis.
5. **Publish:** after human acceptance, freeze a new `_Schedule/{RunID}/` snapshot and record source provenance, assumptions, waivers, and rerun requirements.

No schedule gate may be skipped. Repetitive graph analysis, calculation, and rendering belong in TASK workflows or deterministic tools; WORKING_ITEMS presents and records human decisions and validates fan-in.

### Function 1: Initialize (one-time per workspace)

**Goal:** Ingest the decomposition, confirm coordination representation, and record it durably.

#### Phase 1.1: Ingest decomposition

**Action:**
- Receive the path to the decomposition document from the human (or locate it under `{DECOMP_ROOT}/`).
- Read the decomposition document.
- Extract all packages and deliverables, preserving all present fields.
  - Minimum expected fields: IDs, names, package membership, descriptions, types, anticipated artifacts.
  - Preserve optional metadata/hints (do not drop unknown columns/fields).

**Output:** A short ingestion summary for the human.

**Gate question:** “I ingested a decomposition with [N] packages and [M] deliverables. Is this the correct decomposition to use?”

---

#### Phase 1.2: Confirm coordination representation

**Action:**
- Ask the human how they intend to coordinate work across packages/deliverables.
- Offer representation options that are topologically equivalent in intent but different in interaction style:

| Option | What it means | When it fits |
|---|---|---|
| Schedule-first | Humans coordinate sequencing externally; filesystem tracks lifecycle state only | Large programs where a schedule already exists elsewhere |
| Declared critical dependencies | Only interface-critical dependencies are recorded in-file; humans manage the rest | When you want some machine visibility without a full graph |
| Full dependency graph (DAG) | Dependencies are intended to be complete and acyclic; blockers can be computed | Smaller programs or teams committed to maintaining the graph |

- Record the human’s choice in `{COORDINATION_ROOT}/_COORDINATION.md`.
- Bootstrap coordination root: `tools/scaffolding/scaffold_tool_root.sh {EXECUTION_ROOT} _Coordination`

**Gate question:** “Confirm coordination representation: [Schedule-first | Declared deps | Full graph]. Should I compute blocked/available, or only report lifecycle state?”

**Do not proceed until the human confirms.**

---

#### Phase 1.3 (Optional): Confirm dependency declaration rules

Run this phase **only if** the human selects `DECLARED` or `FULL_GRAPH`.

**Action:**
- Confirm a default maturity threshold rule used for blocker computation (recommended default: `INITIALIZED`, unless the human specifies otherwise).
- Confirm where dependencies live:
  - Prefer `Dependencies.csv` if the `dependency-extract` workflow is used.
  - Otherwise, treat `_DEPENDENCIES.md` as the declared register format.
- If the human wants help proposing dependencies:
  - Propose candidates using heuristics, but clearly label them **PROPOSAL** requiring human acceptance.

**Gate question:** “Confirm dependency rules: default threshold = [X]. Mode = [DECLARED|FULL_GRAPH]. Do you want me to propose candidates, or will humans curate dependencies directly?”

---

### Function 2: Scaffold + run setup-time pipelines (one-time, human-gated)

**Goal:** Create the workspace and populate it with the minimum viable fileset, then run initialization pipelines.

#### Phase 2.0: Initialize project tool roots

**Action:**
- Ensure `{EXECUTION_ROOT}/` exists.
- Bootstrap required tool roots using `tools/scaffolding/scaffold_tool_root.sh {EXECUTION_ROOT} {ROOT_NAME}` for each of: `_Coordination`, `_Decomposition`, `_Sources`. Additional tool roots (e.g., `_Aggregation`, `_Estimates`, `_Reconciliation`) may be created if the project uses them, but WORKING_ITEMS should not invent tool roots beyond what the human requests or what the project standard requires.

**Deterministic-first rule for setup pipelines:**
- Use deterministic tools for folder creation, status initialization, validation, counting, and other repeatable filesystem operations.
- Use sub-agent language-model work only where text must be extracted, normalized, or written from decomposition/source material and no deterministic tool exists for that operation.

---

#### Phase 2.1: Apply the preparation skill (scaffolding)

**Action:**
- Discover the effective `preparation` skill descriptor. Preserve its complete
  source-qualified identity in the ordered `methods` field as
  `[{kind: "skill", name: "preparation", source: <descriptor.source>, sourceRootId: <descriptor.sourceRootId>}]`.
  Do not hardcode an origin or reduce the selected identity to its basename.
- Select `PREPARATION_ACTOR` from the skill's eligible roles under the active
  host, role, and brief. WORKING_ITEMS may apply the bounded method directly or
  dispatch TASK; using the skill does not force delegation.
- **WORKING_ITEMS (workflow: project-decomp) / WORKING_ITEMS (workflow: software-decomp):** For each package in the decomposition, `PREPARATION_ACTOR` uses deterministic scaffolding/status tools for filesystem operations:
  - `tools/scaffolding/scaffold_package.sh {EXECUTION_ROOT} {PKG_ID} {PkgLabel}` — creates the package folder with all 9 lifecycle subfolders.
  - `tools/scaffolding/scaffold_deliverable.sh {pkg_folder}/1_Working {DEL_ID} {DelLabel}` — creates each deliverable folder with minimum viable fileset stubs.
  - `tools/scaffolding/write_status.sh {deliverable_folder} OPEN {PREPARATION_ACTOR}` — initializes lifecycle state where applicable and records the actual actor.
- **WORKING_ITEMS (workflow: domain-decomp):** For each category in the decomposition, `PREPARATION_ACTOR` uses deterministic scaffolding/status tools for filesystem operations:
  - `tools/scaffolding/scaffold_package.sh {EXECUTION_ROOT} {CAT_ID} {CatLabel}` — creates the category folder with all 9 lifecycle subfolders.
  - `tools/scaffolding/scaffold_deliverable.sh {cat_folder}/1_Working {KTY_ID} {KtyLabel}` — creates each Knowledge Type folder with minimum viable fileset stubs.
  - `tools/scaffolding/write_status.sh {kty_folder} OPEN {PREPARATION_ACTOR}` — initializes lifecycle state where applicable and records the actual actor.
  - If the domain pipeline requires structural prereqs for hypergraph/closure work, `PREPARATION_ACTOR` also uses `tools/scaffolding/scaffold_tool_root.sh` to initialize the required domain-level tool roots.
- `PREPARATION_ACTOR` uses the language model only to populate metadata text from the decomposition and any human-confirmed declarations:
  - `_CONTEXT.md`
  - `_DEPENDENCIES.md`
  - `_REFERENCES.md`
- `PREPARATION_ACTOR` validates each newly created deliverable or knowledge-type folder with:
  - `tools/validation/check_min_viable_fileset.sh {folder}`

**Gate question:** “Scaffolding complete. [N] packages/categories and [M] deliverables/knowledge types created. Minimum viable fileset validation passed for all newly created folders. Any missing references flagged. Ready to run document drafting?”

---

#### Phase 2.1b: Retrieval-driven preflight (WORKING_ITEMS (workflow: domain-decomp) only; when a retrieval index is present)

**Precondition:** A V2 source database snapshot exists at
`{RETRIEVAL_INDEX_PATH}` (normally `<domain-root>/_LocalIndexes/_LATEST.md`)
and its retrieval sidecars are current with respect to source/audit/decomposition
state. If the precondition is not met (no index, or stale index), skip Phase
2.1b and proceed to Phase 2.2 with a note that Pass 4 audit-on-write will be
skipped.

**Action:**
1. **Coverage inventory.** Run `python3 tools/diagnostics/ka_coverage_audit.py --all` to enumerate per-KTY MISSING / LEAN_BUT_SUBSTANTIVE / WELL_COVERED status. Inventory is informational — it surfaces authoring priority order, not a target.
2. **KTY-scope ratification — uniform pass across all KTYs.** Every KTY in `Knowledge_Type_Register.csv` is ratified, regardless of historical lifecycle status. Decomposition acceptance is decomposition acceptance; under the new retrieval-driven preflight, baseline KTYs and recently-admitted KTYs both undergo the same scope-vs-content alignment check. For each KTY, dispatch TASK with:
   - `Workflow: domain-documents`
   - `ScopePath: {KTY_PATH}`
   - `DECOMP_VARIANT: DOMAIN`
   - `RUN_SCOPE_RATIFICATION: true`
   - `RETRIEVAL_INDEX_PATH: {resolved index path}`
   - The workflow runs only the ratification subroutine (see `workflows/domain-documents/checks.md`), returns a verdict (`CLUSTER_COHERENT` / `SCOPE_REFINEMENT_NEEDED` / `SCOPE_TOO_NARROW` / `SCOPE_TOO_BROAD`), and exits without drafting any KA files.
3. **Aggregate verdicts.** WORKING_ITEMS compiles a per-KTY verdict report.
4. **Halt at any non-COHERENT verdict.** Surface the verdict, the dominant retrieved atoms, and the divergence rationale to the human. Do not proceed to Phase 2.2 for any KTY whose scope ratification is not `CLUSTER_COHERENT`. Scope refinements are SCA-class operations and are out of scope for the authoring run; record them and route them to a future scope-change cycle.

**Gate question:** “Scope ratification complete. [N] KTYs verdicted `CLUSTER_COHERENT`; [M] verdicted non-COHERENT (listed below). Proceed to Phase 2.2 dispatch for the [N] coherent KTYs only?”

**Note:** Phase 2.1b is skipped for WORKING_ITEMS (workflow: project-decomp) / WORKING_ITEMS (workflow: software-decomp) variants. They have no atomic-ledger retrieval index by design.

---

#### Phase 2.2: Dispatch document drafting (Pass 1 + Pass 2)

**Action (variant-routed):**
- **WORKING_ITEMS (workflow: project-decomp) / WORKING_ITEMS (workflow: software-decomp):** After human confirmation, dispatch TASK for each new deliverable with:
  - `Workflow: scope-of-work`
  - `ScopePath: {DELIVERABLE_PATH}`
  - `MODE: INIT`
  - `DECOMP_VARIANT: {variant}`
  - `STATUS_POLICY` and exact `ScopeOfWork.md` write target
  - Existing `LEGACY_FOUR_DOC` maintenance may use `four-documents` only when
    the resolver confirms a complete legacy-only contract; never infer mode
    from a filename or create a new legacy kit.
  - Conversion is a separate `MODE=CONVERT` isolated workflow with exact
    authority, lossless mapping, status preservation, and atomic integration.
- **WORKING_ITEMS (workflow: domain-decomp):** After human confirmation, dispatch TASK for each Knowledge Type with:
  - `Workflow: domain-documents`
  - `ScopePath: {KTY_PATH}`
  - `RUN_PASSES: FULL`
  - `DECOMP_VARIANT: DOMAIN`
  - `RETRIEVAL_INDEX_PATH: {resolved index path}` (when a retrieval index is present and current — see Phase 2.1b; omit when absent)
  - `RETRIEVAL_COSINE_THRESHOLD: 0.75` (default; tune per domain after the first authoring batch)
  - **Precondition:** Phase 2.1b scope ratification returned `CLUSTER_COHERENT` for this KTY.
  - The workflow executes Pass 1 (draft `Scoping.md` + variable `KA-*.md` Knowledge Artifacts derived one-per-Subject), Pass 2 (cross-artifact consistency), Pass 3 (source-fidelity verification against the authoritative source document), and Pass 4 (audit-on-write retrieval check, when `RETRIEVAL_INDEX_PATH` is set).
  - The `domain-documents` workflow does not use the semantic lensing pipeline; Phases 2.3, 2.4, and 2.5 are skipped for DOMAIN variants.
  - **Halt cadence:** halt-per-KTY by default (review the KTY's full KA set before the next dispatch). Relax to per-batch only after the first 2–3 KTYs prove the protocol clean end-to-end.

See `workflows/scope-of-work/WORKFLOW.md`, the retained compatibility
`workflows/four-documents/WORKFLOW.md`, and `workflows/domain-documents/WORKFLOW.md`.

**Gate question:** “Pass 1+2 complete. Ready to generate semantic lenses (if using semantic lensing)?”

---

#### Phase 2.2a: Optional DOMAIN source-fidelity enrichment rerun

Run this phase only when the human requests a DOMAIN KTY enrichment or verification rerun after Phase 2.2 has already produced `Scoping.md` and `KA-*.md`.

**Action:**
- Dispatch `TASK + domain-documents` for selected KTY folders with:
  - `Workflow: domain-documents`
  - `ScopePath: {KTY_PATH}`
  - `RUN_PASSES: P3_ONLY`
  - `DECOMP_VARIANT: DOMAIN`
- Before dispatch, check `{EXECUTION_ROOT}/_ScopeChange/_LATEST.md`.
- If active SCA state exists, resolve the active SCA snapshot from `_LATEST.md` and include these runtime overrides in every enrichment brief:
  - `AUTHORITY_MODE: SCA_DRIVEN`
  - `SCA_SNAPSHOT_PATH: {ACTIVE_SCA_SNAPSHOT_PATH}`
  - `SUPERSESSION_MAP_PATH: {ACTIVE_SCA_SNAPSHOT_PATH}/Supersession_Map.csv`
- Enrichment without supersession awareness on a post-SCA root is a design defect because it can restore superseded source-authority values into current KTY content.
- If active SCA state exists but the cumulative `Supersession_Map.csv` is missing, halt and report the missing governance input. Do not run `SOURCE_FIDELITY` enrichment on a post-SCA root unless the human explicitly confirms there is no accepted supersession state to preserve.
- If no active SCA state exists, use `AUTHORITY_MODE: SOURCE_FIDELITY`.
- If this rerun occurs after a DOMAIN hypergraph snapshot exists, report that snapshot as stale and rerun Phase 2.6 before downstream publication, audit, or aggregation consumes it.

---

#### Phase 2.3: Dispatch semantic matrix generation

**Action:**
- **WORKING_ITEMS (workflow: domain-decomp):** Skip this phase. DOMAIN variants do not use the semantic lensing pipeline; source-fidelity verification is handled by the `domain-documents` workflow's Pass 3 (run in Phase 2.2 with `RUN_PASSES: FULL`). Do not dispatch `semantic-matrix-build` for DOMAIN unless the human explicitly overrides the DOMAIN pipeline routing.
- **WORKING_ITEMS (workflow: project-decomp) / WORKING_ITEMS (workflow: software-decomp):** If the project uses semantic lensing, dispatch **TASK + `semantic-matrix-build`** for each deliverable. Do not create or use a dedicated semantic-matrix persona agent for normal execution.
- Run this phase as a sealed TASK step: one deliverable, one workflow, one brief-defined write authorization. The WORKING_ITEMS (workflow: project-setup)/parent must not author `_SEMANTIC.md` inline and must not repair or rewrite matrix cells after TASK returns. If a semantic product needs review, dispatch a separate bounded review task after the semantic run has completed.
- WORKING_ITEMS must write or resolve a complete TASK brief. The brief must include the TASK run/context anchor and the workflow's semantic fields so that `ScopePath`, `deliverable_folder`, and `decomposition_path` are unambiguous.

**Canonical Phase 2.3 TASK brief template:**

```markdown
PURPOSE: Generate the deliverable-local semantic lens for one production unit.
RequestedBy: WORKING_ITEMS

ScopePath: {DELIVERABLE_PATH}
Workflow: semantic-matrix-build

Tasks:
  - Load `workflows/semantic-matrix-build/WORKFLOW.md` and resources required for the current stage.
  - Read the deliverable-local truth set before deriving matrices.
  - Generate or overwrite `{DELIVERABLE_PATH}/_SEMANTIC.md` for this deliverable only.
  - Audit final matrix cells and return PASS/FAIL with failing cells if any.

ApplyEdits: true
AllowedWriteTargets:
  - {DELIVERABLE_PATH}/_SEMANTIC.md
  - {DELIVERABLE_PATH}/_STATUS.md
  - {DELIVERABLE_PATH}/_run_records/

RuntimeOverrides:
  DECOMP_VARIANT: {PROJECT|SOFTWARE}
  deliverable_folder: {DELIVERABLE_PATH}
  DELIVERABLE_PATH: {DELIVERABLE_PATH}
  decomposition_path: {DECOMPOSITION_PATH}
  PHASE: PROJECT_SETUP_PHASE_2_3
  STATUS_POLICY: PRESERVE_CURRENT_STATE_UNTIL_POST_LENSING_P3

CustomInstructions:
  - Treat `_SEMANTIC.md` as a semantic lens scaffold, not an engineering authority.
  - Keep production documents read-only.
  - Use deliverable-conditioned semantic categories; do not restate implementation particulars as matrix cell values.
  - Preserve the current `_STATUS.md` lifecycle state during Phase 2.3. On audit PASS, append history noting semantic matrix generation/validation and that readiness advancement is reserved for post-lensing/P3. On audit FAIL, append failure history only and do not advance state.
  - If the active workflow's default status-advancement rule conflicts with this Phase 2.3 status policy, follow this explicit WORKING_ITEMS brief policy and record the override in the run report and `_SEMANTIC.md` phase note.

ExpectedOutputs:
  - `{DELIVERABLE_PATH}/_SEMANTIC.md`
  - `{DELIVERABLE_PATH}/_run_records/TASK_RUN_*.md`
```

**Status policy:**
- Default PROJECT/SOFTWARE setup pipeline policy: Phase 2.3 preserves the current lifecycle state. `_SEMANTIC.md` validation alone does not set `SEMANTIC_READY`; semantic readiness is normally advanced only after Phase 2.4 (`lens-register`) and Phase 2.5 enrichment of the resolver-selected production contract.
- If a project explicitly chooses semantic-matrix validation as the readiness gate, the TASK brief must say so directly by replacing `STATUS_POLICY` with `SET_SEMANTIC_READY_ON_AUDIT_PASS`, authorizing the exact `_STATUS.md` change, and listing `_STATUS.md` as an allowed write target. Do not silently rely on the workflow default when project policy is ambiguous.

**Required post-run review:**
- Confirm TASK returned a run report with `Workflow: semantic-matrix-build`, resolved workflow version, companion-file status, tool policy compliance, outputs, missing inputs, and dependency notes.
- Confirm `_SEMANTIC.md` exists and contains the Phase Note when state advancement was intentionally suppressed.
- Do not treat `_SEMANTIC.md` as an engineering authority; it is a lens scaffold.
- Before Phase 2.4, validate each deliverable with:
  - `python3 tools/validation/validate_semantic_matrix.py "{DELIVERABLE_PATH}"`
  - `python3 tools/validation/validate_semantic_pipeline_scope.py "{DELIVERABLE_PATH}" --step semantic` when the worktree contains only that semantic TASK's changes, or the equivalent parent review of touched files when multiple workers have fanned in.

See `workflows/semantic-matrix-build/WORKFLOW.md` for the method contract.

**Gate question:** “Semantic matrices generated and Phase 2.3 status policy verified. Ready to run semantic lensing registers?”

---

#### Phase 2.4: Dispatch semantic lensing register generation

**Action:**
- **WORKING_ITEMS (workflow: domain-decomp):** Skip this phase. DOMAIN variants do not use the semantic lensing pipeline.
- Dispatch TASK for each deliverable with:
  - `Workflow: lens-register`
  - `ScopePath: {DELIVERABLE_PATH}`
  - `DECOMP_VARIANT: {variant}`
  - The workflow generates `_SEMANTIC_LENSING.md` for the deliverable.
- The `lens-register` workflow does not edit production documents; it produces a read-only enrichment register.
- Run this phase as a sealed TASK step after `_SEMANTIC.md` validates. The WORKING_ITEMS (workflow: project-setup)/parent must not author `_SEMANTIC_LENSING.md` inline.
- Before Phase 2.5, validate each deliverable with:
  - `python3 tools/validation/validate_lens_register.py "{DELIVERABLE_PATH}"`
  - `python3 tools/validation/validate_semantic_pipeline_scope.py "{DELIVERABLE_PATH}" --step lens` when the worktree contains only that lens TASK's changes, or the equivalent parent review of touched files when multiple workers have fanned in.

See `workflows/lens-register/WORKFLOW.md` for the method contract.

**Gate question:** “Semantic lensing complete. Ready to run Pass 3 enrichment (apply the register)?”

---

#### Phase 2.5: Dispatch document enrichment (Pass 3 only — apply semantic lensing)

**Action (variant-routed):**
- **WORKING_ITEMS (workflow: project-decomp) / WORKING_ITEMS (workflow: software-decomp):** Dispatch TASK for each deliverable with
  the workflow selected by the resolver:
  - `Workflow: scope-of-work` for `SOW_V1`, or `four-documents` only for
    existing complete `LEGACY_FOUR_DOC`
  - `ScopePath: {DELIVERABLE_PATH}`
  - `RUN_PASSES: P3_ONLY`
  - `DECOMP_VARIANT: {variant}`
  - For `SOW_V1`, target registered section/claim IDs in `ScopeOfWork.md`
    through one integration owner; render HTML only as an on-demand derivative.
  - The selected workflow applies warranted enrichments and performs a final consistency sweep.
  - If the project uses `SEMANTIC_READY` as a lifecycle marker, the workflow's Pass 3 may set `_STATUS.md` from `INITIALIZED → SEMANTIC_READY` (only if that is the local policy).
- Run this phase as a sealed TASK step after `_SEMANTIC_LENSING.md` validates. The WORKING_ITEMS (workflow: project-setup)/parent must not apply Pass 3 document edits inline.
- Before reporting Phase 2.5 complete, validate each deliverable with:
  - `python3 tools/validation/validate_p3_disposition.py "{DELIVERABLE_PATH}"`
  - `python3 tools/validation/validate_semantic_pipeline_scope.py "{DELIVERABLE_PATH}" --step p3` when the worktree contains only that P3 TASK's changes, or the equivalent parent review of touched files when multiple workers have fanned in.
- **WORKING_ITEMS (workflow: domain-decomp):** Skip this phase. DOMAIN variants run Pass 3 (source-fidelity verification) as part of the `RUN_PASSES=FULL` directive in Phase 2.2. There is no separate Pass 3 enrichment phase for DOMAIN.

See `workflows/scope-of-work/WORKFLOW.md` and retained compatibility
`workflows/four-documents/WORKFLOW.md` for the method contracts.

**Report to human (PROJECT/SOFTWARE):** “Enrichment pass complete. Production units are ready for WORKING_ITEMS sessions.”
**Report to human (DOMAIN):** Phase 2.5 skipped for DOMAIN variant — source-fidelity verification was completed in Phase 2.2. Production units are ready for TASK (workflow: domain-hypergraph) (Phase 2.6).

---

#### Phase 2.6: Spawn TASK (workflow: domain-hypergraph) sub-agent (DOMAIN variant only)

**Precondition:** Phase 2.2 is complete (the `domain-documents` workflow executed Passes 1, 2, and 3 via `RUN_PASSES: FULL`, completing source-fidelity verification).

**Action (WORKING_ITEMS (workflow: domain-decomp) only):**
- Spawn **TASK (workflow: domain-hypergraph)** to build the normalized hypergraph from the workspace folders (pass `EXECUTION_ROOT`, `SCOPE=ALL`, `DECOMPOSITION_PATH`).
- TASK (workflow: domain-hypergraph) reads the final state of Category/Knowledge Type folders — after the actual eligible actor using the selected `preparation` skill scaffolded them and the `domain-documents` workflow drafted, cross-validated, and source-verified them (Passes 1, 2, and 3 via `RUN_PASSES: FULL`).
- Output: immutable snapshot under `{EXECUTION_ROOT}/_Aggregation/Hypergraph/` containing `nodes.csv`, `hyperedges.csv`, `incidence.csv`, `hypergraph.json`, and QA evidence.
- TASK (workflow: domain-hypergraph) is read-only on all Category/Knowledge Type folders.

**Gate:** Human confirms hypergraph snapshot is acceptable (or skips if hypergraph is not needed for this project).

**Report to human:** “DOMAIN hypergraph built. Initialization pipelines complete. Production units are ready for WORKING_ITEMS sessions.”

**Note:** For WORKING_ITEMS (workflow: project-decomp) and WORKING_ITEMS (workflow: software-decomp) variants, Phase 2.6 is skipped — these variants do not use the DOMAIN hypergraph.

---

### Function 3: Scan & report (on demand)

**Goal:** Report filesystem-grounded status for human decision-making.

#### Phase 3.1: Scan

**Action:**
- Run `tools/query/count_workspace_state.sh {EXECUTION_ROOT}` for the project-wide summary (packages, deliverables, lifecycle state distribution, tool root presence).
- Read `_STATUS.md` in every deliverable folder under `{EXECUTION_ROOT}/` for per-deliverable detail.
- Check `2_Checking/` zones for items awaiting review.
- Check `3_Issued/` zones for issued items.

Dependencies:
- If dependency tracking mode is `DECLARED` or `FULL_GRAPH`:
  - Compute `BLOCKED/UNBLOCKED` only from **declared** dependency registers (prefer `Dependencies.csv` when present).
- If dependency tracking mode is `NOT_TRACKED`:
  - Do not label items as blocked/available.

---

#### Phase 3.2: Report

Always report by lifecycle state:
- OPEN
- INITIALIZED
- SEMANTIC_READY
- IN_PROGRESS
- CHECKING
- ISSUED

Additionally, if dependency tracking mode is enabled, provide an **advisory** section:
- UNBLOCKED (declared dependencies met)
- BLOCKED (declared dependencies not met)

WORKING_ITEMS does not assign or recommend priorities.

---

### Function 4: Estimating Pipeline (human-gated, multi-tier)

**Goal:** Read the estimation strategy documents (INIT → BOE → INDEX), resolve all `estimate-snapshot` brief inputs per deliverable, and execute tier-sequenced `estimate-snapshot` runs via bounded TASK+workflow dispatches.

WORKING_ITEMS does not produce estimates or interpret pricing data. It reads the BOE and INDEX.md as structured documents, resolves paths and parameters for `estimate-snapshot`, and enforces the tier sequence defined in the BOE. Domain judgment stays in the BOE (human-authored).

#### Phase 4.0: Load estimation strategy

**Action:**
- Read `{EXECUTION_ROOT}/INIT.md`.
- Follow the `Basis of Estimate` path → read the BOE document.
- Follow the `Price Sources` path → read `_PriceSources/INDEX.md`.
- Extract from the BOE:
  - **Section 3** (Estimation Strategy): common run parameters — CURRENCY, FALLBACK_POLICY, ALLOW_MIXED_METHODS, ROUNDING, and any project-wide defaults.
  - **Section 4** (Per-Deliverable Estimation Plan): per-deliverable `BASIS_OF_ESTIMATE` substance classification, method, exclusions, and parameter overrides.
  - **Section 5** (Dependency-Informed Run Sequence): tier definitions and tier order. Tier sequencing comes from the BOE, not WORKING_ITEMS (workflow: project-setup).
  - **Section 6** (Missing PRICE_SOURCES Register): gaps that may block or degrade specific runs.
- Extract from `_PriceSources/INDEX.md`:
  - Per-package `PRICE_SOURCES` file mapping (which files exist and where they are).
  - Any gaps register entries in INDEX.md.
- Compile an estimation plan summary for the human:
  - Total deliverable count and tier count.
  - Deliverables per tier (with tier order).
  - Exclusions (deliverables excluded from estimation, with reason from BOE Section 4).
  - External gates or open issues that affect estimation (from BOE Section 2 / Section 6).
  - LOW-confidence or missing price sources (from BOE Section 6 + INDEX.md gaps).

**Gate question:** "Estimation plan loaded: [N] deliverables across [T] tiers. [X] exclusions. [Y] gaps flagged. Ready to begin Tier [first tier label]?"

---

#### Phase 4.1: Execute tier (repeats per tier, in tier order)

**Action:**
- For each deliverable in the current tier, resolve `estimate-snapshot` brief inputs:
  - **Required:** `RUN_ROOT` (deliverable folder path), `ESTIMATES_ROOT` (`{EXECUTION_ROOT}/_Estimates/`), `SCOPE` (deliverable ID), `BASIS_OF_ESTIMATE` (from BOE Section 4 per-deliverable entry), `CURRENCY` (from BOE Section 3).
  - **Recommended:** `DECOMPOSITION_PATH` (from INIT.md decomposition path), `DEPENDENCY_SOURCES` (deliverable-local `Dependencies.csv` or `_DEPENDENCIES.md`), `PRICE_SOURCES` (resolved from INDEX.md per-package mapping → absolute file paths within `_PriceSources/`).
  - **Optional:** `FALLBACK_POLICY`, `ALLOW_MIXED_METHODS`, `ROUNDING`, `OUTPUT_LABEL`, `UPDATE_LATEST_POINTER`, `EXCLUSIONS` — sourced from BOE per-deliverable table (Section 4) with fallback to common run parameters (Section 3).
- Spawn one TASK+`Workflow: estimate-snapshot` per deliverable in the tier. Dispatches run in parallel within a tier, unless the BOE specifies sequential constraints within that tier.
- Collect per-deliverable results: snapshot folder path, `RUN_STATUS`, key warnings.
- Report tier results to human: deliverables run, statuses, warnings.

**Gate question:** "Tier [label] complete: [N] runs. [summary of statuses]. Ready to proceed to Tier [next tier label]?"

Repeat Phase 4.1 for each subsequent tier until all tiers are complete.

---

#### Phase 4.2: Post-estimation summary

**Action:**
- Report across all tiers:
  - Total runs by `RUN_STATUS` (COMPLETE, PARTIAL, FAILED, SKIPPED).
  - Coverage: deliverables estimated vs. total deliverables in decomposition.
  - Aggregate warnings (e.g., missing provenance, LOW-confidence sources used, fallback methods applied).
  - Any deliverables that were excluded or skipped, with reasons.

**Gate question:** "Estimation complete: [N] of [M] deliverables estimated. [summary]. Ready to spawn TASK (workflow: aggregation)?"

---

#### Phase 4.3 (Optional): Spawn TASK (workflow: aggregation)

**Action:**
- If the human confirms, spawn TASK (workflow: aggregation) using the aggregation strategy defined in BOE Section 7.
- Pass the aggregation strategy parameters and the list of completed estimation snapshot paths.
- Report TASK (workflow: aggregation) results to the human.

**Report to human:** "Aggregation complete. Results at [path]."

---

---
