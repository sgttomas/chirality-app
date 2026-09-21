# scope-change — contract

## Runtime variables and defaults

This file is **decomposition-generic**. Do not embed project-specific absolute paths.

Working definitions used throughout this protocol:
- `AUTHORITATIVE_TRUTH` = the decomposition document plus any variant-owned authoritative annex/register files that the originating decomposition defines as part of decomposition truth. This is the **canonical working package**: main decomposition document + authoritative companion registers + `_ScopeChange` state.
- `AUTHORITATIVE_COMPANION_REGISTER` = a CSV, JSON, or structured markdown file that holds heavy machine-truth as the primary working surface for that data (e.g., Domain Ledger, Knowledge Type Register, coverage telemetry). When a companion register exists, it is authoritative for machine-truth; the main document carries summaries, not exhaustive duplicates.
- `DERIVATIVE_PACKAGES` = any downstream package assembled from accepted authoritative truth but not itself authoritative truth, including regenerated KTY-local artifacts, `_Aggregation` outputs, hypergraph snapshots, audit snapshots, concordance packages, publication packages, and any single-file monolithic render of the decomposition. These are **derived publication artifacts** and must never be the default amendment target.
- `HANDOFF_STATE` = an explicit state record emitted at the end of the amendment run naming the accepted snapshot, derivative-package rerun status, closure verdict, remaining blockers, and next owning workflow
- `PACKAGE_ROLE_LABEL` = the explicit declaration of a file's role in the canonical working package: `working surface`, `authoritative companion register`, `snapshot / handoff artifact`, or `derived publication artifact`. WORKING_ITEMS must classify every touched surface by package role.

Defaults (only when not otherwise specified by the human):
- `DECOMP_VARIANT` = required; one of `PROJECT | SOFTWARE | DOMAIN`
- `CONTEXT_ROOT` = `execution/` when `DECOMP_VARIANT in {PROJECT, SOFTWARE}`; otherwise the nearest common parent that owns the domain decomposition document (or a human-provided root)
- `DECOMPOSITION_PATH` = discovered from `{CONTEXT_ROOT}/_Decomposition/` when that folder exists and contains a single `.md` file; otherwise explicitly provided by the human
- `SCOPE_CHANGE_ROOT = {CONTEXT_ROOT}/_ScopeChange/`
- `ALLOW_RENUMBERING = false` (stable IDs are preserved unless the human explicitly approves renumbering)
- `ALLOWED_PROPAGATION_WRITES` = variant-specific default write scope:
  - `PROJECT/SOFTWARE`: decomposition document + affected `_CONTEXT.md` and `_STATUS.md`
  - `DOMAIN`: decomposition document + decomposition annex CSVs under `_Decomposition/` + amendment snapshot and `_LATEST.md` under `_ScopeChange/`

---

## Non-negotiable invariants

- **Agent initiative, human-gated application.** WORKING_ITEMS may identify and
  propose a decomposition amendment when evidence exposes a gap, conflict,
  changed material basis, or downstream inconsistency. It records the proposal
  and supporting evidence without changing canonical truth. Application begins
  only after the human accepts checkpoint group 1 and remains bounded by the
  exact checkpoint-group-2 amendment and propagation decision.
- **Three grouped human checkpoints.** The agent prepares the full reviewable
  package before each checkpoint: (1) proposed change and impact; (2) exact
  amendment and propagation plan; and (3) audited poststate acceptance. Internal
  analysis, validation, remediation, and derivative-quality evidence do not add
  prompts.
- **Non-destructive.** Removed entities are retired or legacy-annotated; they are not silently erased. For `PROJECT/SOFTWARE`, removed deliverables are marked `RETIRED` in `_STATUS.md` and folders are never deleted. For `DOMAIN`, Domain Ledger rows and change records are preserved even when entities move out of active scope.
- **Impact before action.** The human must review and accept the impact assessment before any file is modified.
- **No direct collateral writes.** WORKING_ITEMS does not directly modify the four-doc set, `Dependencies.csv`, estimates, schedules, generated knowledge artifacts, or other downstream truth. When a `DOMAIN` amendment affects KTY-local content or metadata needs, WORKING_ITEMS must dispatch bounded TASK workflows, collect their evidence, update SCA-owned closure surfaces, and block closure when required evidence is missing. WORKING_ITEMS never edits active `Scoping.md`, `KA-*.md`, `_CONTEXT.md`, `_STATUS.md`, or `_REFERENCES.md` inside KTY folders itself.
- **Derivative packages are downstream only.** `DERIVATIVE_PACKAGES` may consume accepted decomposition truth, but they do not redefine it and they are never updated in place by WORKING_ITEMS except for the amendment snapshot artifacts WORKING_ITEMS itself owns.
- **KTY content one-writer rule.** `domain-documents` is the only writer of active DOMAIN KTY `Scoping.md` and `KA-*.md` factual content. `kty-content-remediate` may archive active-looking content and leave tombstone stubs, but it never writes regenerated active content.
- **Status-memory paired read.** Whenever WORKING_ITEMS or a WORKING_ITEMS-dispatched workflow reads a local `_STATUS.md`, it must also read sibling `_MEMORY.md` or `MEMORY.md` when present. Memory is non-authoritative operational context only; it may explain local continuity, caveats, or prior run notes, but it must never override accepted decomposition truth, structured SCA artifacts, supersession bindings, or source authority.
- **.Archive/ scanner exclusion.** `.Archive/` folders are retirement history and evidence only. They must be excluded from downstream scanners, allowlists, section maps, publication inputs, and regeneration inputs unless the task is explicitly a historical audit.
- **Stable IDs preserved.** Existing IDs are never reused for different entities. Removed IDs remain reserved. If a reclassification would make an embedded index or mnemonic stale, keep the existing ID unless the human explicitly approves renumbering and downstream ripple changes.
- **Structural closure required.** A parent partition or parent entity (`PACKAGE`, `CATEGORY`, `KNOWLEDGE_TYPE`, or any stricter variant-local equivalent) cannot be removed, merged, split, or reclassified unless all child entities and authoritative ledger bindings are retired, remapped, or explicitly preserved in the same amendment. No orphan children, no dangling parent bindings.
- **Closure is stateful.** An amendment is not closed when edits finish. Closure requires accepted authoritative truth, recorded downstream rerun obligations for every affected derivative package, explicit blocker disclosure, and a `HANDOFF_STATE` artifact that tells the next workflow what is current versus stale.
- **Variant invariants preserved.** WORKING_ITEMS must preserve the originating decomposition workflow's invariants. For `DOMAIN`, this includes flat Categories, exactly-one-Category assignment for every `IN` Handbook Unit, single-parent `KnowledgeType` / `KnowledgeSubject` relationships, at-least-one-`KnowledgeSubject` cardinality for every `KnowledgeType`, and an updated Domain Ledger + Coverage & Telemetry block. For `PROJECT/SOFTWARE`, package/deliverable integrity and the originating decomposition's invariants remain binding.
- **Full package truth for `DOMAIN`.** For `DOMAIN`, `AUTHORITATIVE_TRUTH` is the full active decomposition package: the main decomposition document, active decomposition-local annex / derivative surfaces under `_Decomposition/`, `_ScopeChange/_LATEST.md`, and the active snapshot state describing the amendment and its current handoff position.
- **Variant-local structural rules must be operationalized.** If the originating decomposition defines stricter structural rules than the generic model, WORKING_ITEMS must turn them into explicit checks for the affected amendment. For `PROJECT`, this includes package-discipline isolation, artifact-kind deliverable granularity, or any equivalent design-partition rule when those rules are present in the source decomposition.
- **Semantic binding first.** Protocol steps operate on semantic sections (`ledger`, `partitions`, `entities`, `objectives`, `change register`, `telemetry`) rather than hard-coded project vocabulary. Human-facing outputs MUST use the variant's canonical nouns.
- **Type-level change preference.** Prefer the smallest amendment that changes instances, mappings, or attributes before changing the decomposition contract itself. If the request would alter the decomposition ontology, canonical vocabulary, or section contract, flag it explicitly as a contract-level change.
- **Amendments operate on the canonical working package.** The amendment surface is the main decomposition document, authoritative companion registers, and `_ScopeChange` state. Derived publication artifacts (monolithic renders, publication bundles, review documents) must never be the default amendment target. If a derived artifact must be updated, it is regenerated from the amended canonical working package, not edited directly.
- **Package-role classification required.** Every surface touched or affected by an amendment must be classified by package role (`working surface`, `authoritative companion register`, `snapshot / handoff artifact`, or `derived publication artifact`). This classification must appear in the Impact Assessment and Propagation Plan.
- **Supersession binding required.** When an amendment action changes a fact that could conflict with an upstream admitted authority (source DBM, discipline DBM, vendor data, regulatory document, or other admitted authority), the action must produce a corresponding row in `Supersession_Delta.csv` that binds the SCA decision to the specific superseded authority fact. The binding must include the authority document path, the specific reference within it, the original value, and the replacement value. Without this binding, downstream consumers cannot distinguish intentional overrides from decomposition errors. A `SUPERSESSION` binding means the prior authority fact is overridden; a `SUPPLEMENTARY_EXTENSION` binding means the SCA adds detail without contradicting the prior authority.
- **Evidence-first.** Every impact claim traces to specific files, rows, or sections.
- **No invention.** If the impact or correct amendment is uncertain, mark it as `UNKNOWN` or `TBD` and surface it for human decision.
- **Immutable snapshots.** Each amendment produces a new snapshot folder under `_ScopeChange/`; never overwrite prior snapshots.
- **Checkpoint snapshots.** Checkpoint groups 1 and 2 each finalize an
  immutable decision snapshot before the next stage consumes their accepted
  state. Group 3 finalizes the immutable active amendment snapshot only after
  audited poststate acceptance. Each snapshot records its decision, manifest,
  upstream basis, derivative status, closure, reruns, and blockers.
- **Snapshot before handoff.** No handoff to downstream reruns, audits, or publication planning is valid until the new immutable amendment snapshot exists and the `HANDOFF_STATE` points to it.
- **Active snapshot integrity matters.** `_LATEST.md` must point to exactly one active snapshot. The active snapshot must contain every required artifact. Historical incomplete snapshots may remain as residue, but they must not be treated as current truth.
- **Candidate posture is exclusive.** Checkpoint-group-3 preparation uses
  exactly one pointer posture: either `_LATEST.md` continues to name a verified
  accepted SCA predecessor, or this is the first amendment and `_LATEST.md` is
  absent. The first-amendment posture is grounded in the accepted decomposition
  and accepted group-2 decision snapshot; it does not invent a predecessor or
  create `_LATEST.md` before group-3 acceptance.
- **Affected-decision reopening.** If accepted material basis changes after a
  checkpoint, reopen only the decisions whose warrants, scope, propagation, or
  closure consequences are affected. Refresh their dependent evidence and
  preserve unaffected accepted decisions.

---

## Explicit non-ownership

- **The actual eligible actor using the selected `preparation` skill** owns
  creating new deliverable folders and metadata files for `PROJECT/SOFTWARE`
  within its existing role and brief. The selection uses the effective
  source-qualified skill descriptor in the ordered `methods` field and is
  coordinated through WORKING_ITEMS with project-setup; delegation is optional.
- **The responsible current role** receives repository-change evidence and the
  exact change scope. It follows the applicable project's change skill or
  repository conventions when present. This current workflow does not require
  Git or select the retained legacy `change` workflow; explicitly selected
  historical identities keep their legacy procedure.
- The **`dependency-extract` workflow (dispatched via TASK)** owns dependency re-extraction. WORKING_ITEMS recommends reruns; does not execute them.
- The **`estimate-snapshot` workflow (dispatched via TASK)** and **WORKING_ITEMS (workflow: project-setup) scheduling workflow** own estimate/schedule updates. WORKING_ITEMS recommends reruns; does not execute them.
- **Downstream knowledge-production workflows** own creation, regeneration, and retirement of structured knowledge artifacts derived from a `DOMAIN` decomposition, including KTY-local documents (`Scoping.md`, `KA-*.md`, `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md`), `_Aggregation` outputs, hypergraph outputs, and publication outputs. For SCA-required KTY-local content disposition and approved metadata alignment, WORKING_ITEMS owns dispatch-and-block orchestration through bounded TASK workflows and records evidence in the SCA snapshot; it does not perform the KTY-local edits directly. Other derivative-package reruns remain handoff work unless this protocol explicitly adds an orchestration lane.
- **Downstream owners close derivative packages.** The owning downstream workflow is responsible for regenerating, validating, and closing any derivative package that WORKING_ITEMS marks stale. WORKING_ITEMS records required closure state; it does not satisfy it on their behalf.
- A **dedicated audit workflow**, where available, owns deep decomposition audit. WORKING_ITEMS consumes that output for pre/post comparison; if no dedicated auditor exists for the variant, it synthesizes a baseline from the authoritative decomposition artifact.

---

## Action Types

WORKING_ITEMS classifies every change request into one or more atomic actions:

| Action Type | Description | Decomposition Effect | Propagation Effect |
|-------------|-------------|----------------------|-------------------|
| `ADD` | New entity or new authoritative row in the decomposition | New row(s) in the relevant semantic section(s) | Variant-specific initialization or rerun advisory |
| `REMOVE` | Retire an existing entity non-destructively | Existing row annotated as `RETIRED`/legacy; downstream mappings remapped or flagged | Variant-specific retirement or rerun advisory |
| `MODIFY` | Change attributes, descriptions, schemas, notes, or non-lineage mappings of an existing entity | Field updates in the relevant section(s) | Metadata updates or rerun advisory |
| `RECLASSIFY` | Move an existing entity or unit to a different parent partition / parent entity while preserving stable identity by default | Parent binding fields updated; decision log records ID-retention vs renumbering | Folder relocation, regrouping, or reindex advisory |
| `MERGE` | Combine two or more entities into a successor entity | Source rows retired; successor row added or elected; references remapped | Union of `REMOVE` + `ADD` propagation impacts |
| `SPLIT` | Split one entity into two or more successor entities | Source row retired; fragment rows added; references remapped | Union of `REMOVE` + `ADD` propagation impacts |

**Interpretation note:** pure mapping corrections use `MODIFY` unless the parent partition / parent entity changes, in which case use `RECLASSIFY`.

**Structural-change rule:** a `REMOVE`, `RECLASSIFY`, `MERGE`, or `SPLIT` affecting a parent partition or parent entity is invalid unless the same amendment explicitly resolves the full child-closure set and every authoritative ledger remapping.

---

## Inputs

### Required before checkpoint group 1
- A human request or an evidence-backed agent proposal for a decomposition
  change (natural language or structured)

### Resolved before checkpoint group 1
- `DECOMP_VARIANT`
- `CONTEXT_ROOT`
- `DECOMPOSITION_PATH`
- Parsed decomposition state (resolved via semantic section binding):
  - Change Register
  - Unit Ledger
  - Objectives
  - Primary Partitions
  - Secondary Entities
  - Tertiary Entities (if any)
  - Vocabulary Map (if any)
  - Coverage basis / telemetry

### Required
- `DECOMP_VARIANT`: `PROJECT` | `SOFTWARE` | `DOMAIN`

### Optional
- `AMENDMENT_ID`: human-assigned `SCA-{NNN}` (default: next available scanned from `_ScopeChange/` folder names)
- `ALLOW_RENUMBERING`: `true|false` (default `false`)
- `ALLOWED_PROPAGATION_WRITES`: explicit narrower write list if the human wants stricter write quarantine than the defaults

### Deterministic Tool Contracts

WORKING_ITEMS may interpret findings, decide handoff state, and write human-facing summaries, but it must not reimplement deterministic CSV merge, coverage serialization, or DOMAIN referential-integrity validation in prose. Use these registered tools when the corresponding artifact is required:

- `tools/reporting/synthesize_domain_coverage_json.py` for DOMAIN `Pre_Change_Coverage.json` and `Post_Change_Coverage.json`.
- `tools/coordination/accumulate_supersession_map.py` for cumulative `Supersession_Map.csv` generation and optional check-mode comparison.
- `tools/validation/validate_domain_decomposition_integrity.py` for DOMAIN annex integrity, coverage telemetry reconciliation, active snapshot artifact checks, `_LATEST.md` parity, and KTY remediation rollup consistency.
- `tools/validation/validate_kty_remediation_manifest.py` for KTY remediation manifest schema, dispatch mapping, evidence, closure-state, and scanner-exclusion checks.

**Layout convention (DOMAIN):** `--decomposition-root` resolves the canonical annexes-at-`_Decomposition`-root layout by default. The synthesizer and integrity validator also accept `--package-subfolder {NAME}` (or auto-descend when a single subfolder is present) as a transitional / forward-compatible accommodation for packages still using a nested-snapshot layout. Both invocation forms are valid; pass `--package-subfolder` only when the root contains no annex files directly.

### Variant Section Binding

All protocol steps reference sections by **semantic name** and then bind those semantics to the originating decomposition variant **by heading text, never by section number**, using the normalization and rank-order matching defined in `workflows/audit-decomp/resources/contract.md#variant-section-binding`. If no rank yields a hit, stop and report an unresolved binding rather than resolving by position.

| Semantic section | WORKING_ITEMS (workflow: project-decomp) | WORKING_ITEMS (workflow: software-decomp) | WORKING_ITEMS (workflow: domain-decomp) | Notes |
|------------------|----------------|-----------------|---------------|-------|
| Change Register | `Change Log` | `Decision Log` and/or `Revision History` | `Decision Log / Change Log` | Bind by heading text, never by number. `WORKING_ITEMS (workflow: software-decomp)` may split this across two headings; read both when both exist |
| Unit Ledger | `Scope Ledger` | `Scope Ledger` | `Domain Ledger` | Authoritative row-level mapping table |
| Objectives | `Objectives` | `Objectives` where present, otherwise the `ObjectiveID(s)` column of `Scope Ledger` | — | `WORKING_ITEMS (workflow: domain-decomp)` does not have an Objectives layer |
| Primary Partitions | `Packages` | `Packages` | `Categories` | Flat partition primitive |
| Secondary Entities | `Deliverables` | `Deliverables` | `Knowledge Types` | Parented to the primary partition |
| Tertiary Entities | — | — | `Knowledge Subjects` | Parented to `Knowledge Types` |
| Vocabulary Map | — | — | `Vocabulary Map` | Canonical terms and synonyms |
| Coverage Basis | `TASK (workflow: audit-decomp)` output | `TASK (workflow: audit-decomp)` output | `Coverage & Telemetry` + `Domain Ledger` export | Used for pre/post comparison |

### Variant-specific ID formats

When validating or proposing IDs, use the originating decomposition's grammar:

- `WORKING_ITEMS (workflow: project-decomp)`: `PKG-XX` / `DEL-XX-YY_{desc}`
- `WORKING_ITEMS (workflow: software-decomp)`: `PKG-XX` / `DEL-XX-YY`
- `WORKING_ITEMS (workflow: domain-decomp)`:
  - `HBA-####` (accepted source identifier; read historical HBK aliases only when the accepted basis supplies their mapping)
  - `OBJ-###`
  - `CAT-###`
  - `KTY-CC-TT_{shortDescription}`
  - `SUB-CC-TT-SS_{shortDescription}`

**Vocabulary note:** vocabulary amendments in `DOMAIN` use the canonical term string as the action register reference unless the local decomposition schema defines a stronger identifier.

---

## Validity

A decomposition amendment cycle is valid when:

- The change has a human-accepted checkpoint-group-1 basis, whether first
  requested by the human or identified as an evidence-backed agent proposal.
- All three grouped checkpoints received explicit human confirmation before
  the workflow claimed accepted closure.
- The decomposition document was modified only per the checkpoint-group-2
  accepted amendment.
- Variant-local metadata files were modified only per the checkpoint-group-2
  accepted propagation plan.
- No files outside the approved write scope were modified.
- An immutable amendment snapshot exists under `_ScopeChange/` with all required artifacts.
- For `DOMAIN`, the full active decomposition package is internally consistent: main markdown, affected decomposition-local derivatives, `_LATEST.md`, and active snapshot state all agree.
- Pre-change and post-change baselines both completed using the variant-appropriate coverage source.
- The decomposition document's Change Register contains the amendment entry.
- Stable IDs were preserved unless the human explicitly approved renumbering.
- Retired / removed source IDs were not reused.
- `Amendment_Actions.csv` accounts for every atomic change.
- `Decision_Log.md` records all human decisions at each checkpoint.
- `Handoff_State.md` exists and names the accepted snapshot, derivative-package status, closure verdict, blockers, and next owning workflow.
- Every affected `DOMAIN` derivative surface was classified as `DIRECT_EDIT`, `RECOMPUTE`, or `NO_CHANGE`, and the active state matches that classification.
- `_LATEST.md` points to exactly one active snapshot.
- The active snapshot contains every required artifact.
- Historical incomplete snapshots may remain only as explicitly non-current residue; they are not treated as active truth.
- `RUN_SUMMARY.md` and `Handoff_State.md` do not imply a later phase than the artifacts support.
- The originating decomposition variant's invariants remain satisfied after the amendment.
- No parent partition / parent entity change left orphaned child entities or dangling authoritative mappings.
- Any variant-local structural rule stricter than the generic model was validated explicitly for the affected rows; generic reminders are not sufficient.
- Any derivative package left stale by the amendment is explicitly recorded as open work in `Handoff_State.md`; no stale downstream state is represented as closed.
- Additional `DOMAIN` validity requirements:
  - `Domain Ledger` remains present and updated
  - `Coverage & Telemetry` remains present and updated
  - every `IN` Handbook Unit has exactly one `CategoryID`
  - every `Knowledge Type` contains at least one `Knowledge Subject`
  - every `Knowledge Subject` belongs to exactly one `Knowledge Type`
  - the `Vocabulary Map` is updated when terminology changes are part of the amendment
  - when KTY-local content is affected, `KTY_Remediation_Manifest.csv` exists in the active SCA snapshot and every row is resolved to `ARCHIVED_STUBBED`, `REGENERATED`, `VERIFIED`, `DEFERRED`, `BLOCKED`, or `NOT_REQUIRED`
  - `PENDING` KTY remediation rows block closure
  - `BLOCKED` KTY remediation rows cap `ReadyForNextPhase = NO`
  - `DEFERRED` KTY remediation rows require substantive blocker notes and cap `ReadyForNextPhase = REGEN_ONLY`
  - `PHASE7_REVIEW` and `PUBLICATION_GATED` are forbidden while any KTY remediation row is pending, deferred, blocked for factual use, or missing required evidence
  - when KTY-local metadata alignment is accepted in checkpoint group 2, WORKING_ITEMS records `TASK + kty-metadata-align` evidence and does not directly edit `_CONTEXT.md`, `_STATUS.md`, or `_REFERENCES.md`
  - `.Archive/` scanner exclusion is recorded for any downstream allowlist, section map, regeneration input, or publication input present in the snapshot
  - a Phase-5-only closeout may set `ReadyForNextPhase = REGEN_ONLY` but must not imply downstream regeneration complete
  - a post-regeneration closeout may set `ReadyForNextPhase = PHASE7_REVIEW` only when downstream reruns, metadata alignment, audit, and terminology checks are all recorded non-blocking

---

## Artifacts and schemas

### Snapshot layout

```
{SCOPE_CHANGE_ROOT}/
  _LATEST.md
  SCA-{NNN}_{YYYY-MM-DD}_{HHMM}/
    Brief.md                       (human's original request + parsed actions)
    Impact_Assessment.md           (checkpoint-group-1 output)
    Propagation_Plan.md            (checkpoint-group-2 output)
    Amendment_Actions.csv          (machine-readable action register)
    Pre_Change_Coverage.json       (audit output copy or synthesized baseline)
    Post_Change_Coverage.json      (audit output copy or synthesized baseline)
    Decision_Log.md                (all checkpoint decisions)
    Handoff_State.md               (closure + downstream ownership state)
    RUN_SUMMARY.md                 (final summary + handoffs)
    Domain_Integrity_Report.md     (DOMAIN-only deterministic integrity validator output)
    Domain_Integrity_Findings.csv  (DOMAIN-only deterministic integrity validator findings)
    Supersession_Delta.csv         (new supersession bindings introduced by this SCA — required when any action changes a fact that could conflict with an upstream admitted authority)
    Supersession_Map.csv           (cumulative active supersession map — all accepted SCAs to date; enables downstream consumers to read one file instead of reassembling history)
    KTY_Remediation_Manifest.csv   (per-SCA KTY content action/evidence ledger; not a cumulative disposition surface)
    Evidence/                      (TASK evidence for kty-content-remediate, domain-documents, and kty-metadata-align dispatches)
```

### `RUN_SUMMARY.md` / `Handoff_State.md` state fields

The active snapshot must expose these fixed state fields across `RUN_SUMMARY.md` and/or `Handoff_State.md`:

| Field | Allowed values | Meaning |
|---|---|---|
| `DecompositionTruthState` | `INCOMPLETE` / `COMPLETE` | Whether the main decomposition document amendments are complete |
| `DerivativePackageState` | `INCOMPLETE` / `COMPLETE` | Whether affected decomposition-local derivative surfaces are in parity |
| `ContentRemediationState` | `NOT_REQUIRED` / `PENDING` / `COMPLETE` / `BLOCKED` / `DEFERRED` | Rollup state for SCA-owned KTY content remediation manifest rows |
| `DownstreamRerunState` | `NOT_REQUIRED` / `FROZEN` / `IN_PROGRESS` / `COMPLETE` / `BLOCKED` | Whether downstream reruns are pending or complete |
| `MetadataAlignmentState` | `NOT_REQUIRED` / `NOT_STARTED` / `IN_PROGRESS` / `COMPLETE` / `BLOCKED` | Whether post-regeneration metadata alignment is complete |
| `AuditState` | `NOT_RUN` / `WARNINGS` / `NON_BLOCKING_PASS` / `BLOCKED` | Current audit / verification state |
| `ReadyForNextPhase` | `NO` / `REGEN_ONLY` / `PHASE7_REVIEW` / `PUBLICATION_GATED` | Highest phase the current artifact state actually supports |

### KTY Remediation Closure Rules

These rules apply when `KTY_Remediation_Manifest.csv` exists or when any
`DOMAIN` amendment affects KTY-local content needs:

- `PENDING` rows block closure.
- `BLOCKED` rows resolve the manifest administratively only when blocker notes
  are substantive and evidence-backed; they cap `ReadyForNextPhase = NO`.
- `DEFERRED` rows require substantive blocker notes and cap
  `ReadyForNextPhase = REGEN_ONLY`.
- `PHASE7_REVIEW` and `PUBLICATION_GATED` are forbidden while any manifest row
  is pending, deferred, blocked for factual use, or missing required evidence.
- Any row with `FACTUAL_USE_GATE = BLOCK_FACTUAL_USE` blocks factual downstream
  use of that KTY content.
- `.Archive/` scanner exclusion must be evidenced anywhere downstream
  allowlists, section maps, regeneration inputs, or publication inputs are
  present.

`ContentRemediationState` rollup:

- `NOT_REQUIRED` when no KTY-local content remediation manifest is required.
- `PENDING` when any manifest row remains `PENDING` or lacks required evidence.
- `BLOCKED` when any row is `BLOCKED`.
- `DEFERRED` when no row is blocked or pending and one or more rows are
  `DEFERRED`.
- `COMPLETE` when all required rows are `ARCHIVED_STUBBED`, `REGENERATED`,
  `VERIFIED`, or `NOT_REQUIRED` and all required evidence is present.

### Amendment Actions Schema

| Column | Type | Description |
|--------|------|-------------|
| `AmendmentID` | string | `SCA-{NNN}` |
| `ActionSeq` | integer | Sequential within amendment |
| `ActionType` | enum | `ADD` / `REMOVE` / `MODIFY` / `RECLASSIFY` / `MERGE` / `SPLIT` |
| `EntityType` | enum | `PACKAGE` / `DELIVERABLE` / `CATEGORY` / `KNOWLEDGE_TYPE` / `KNOWLEDGE_SUBJECT` / `OBJECTIVE` / `HANDBOOK_UNIT` / `VOCAB_TERM` / `OTHER` (note: `OBJECTIVE` applies only to `PROJECT`/`SOFTWARE` variants; `DOMAIN` does not have an Objectives layer) |
| `EntityID` | string | Stable ID of affected entity, or canonical term string for `VOCAB_TERM` |
| `Description` | string | Human-readable description |
| `AffectedFiles` | string | Semicolon-separated list of file paths modified |
| `DownstreamReruns` | string | Comma-separated list of agent / workflow names to rerun |
| `SupersessionBindingPresent` | boolean | `YES` if this action has one or more corresponding surviving rows in `Supersession_Delta.csv`; `NO` for structural/organizational actions that do not affect authority facts. Actions that change a value conflicting with an admitted authority (e.g., retiring equipment, changing a design parameter, renaming a canonical term) must be `YES` while at least one admitted supersession row survives. |

### KTY Remediation Manifest Schema

`KTY_Remediation_Manifest.csv` is a per-SCA action/evidence ledger owned by
WORKING_ITEMS (workflow: scope-change). It is not a cumulative content-disposition register and must not
be treated as current KTY factual content.

#### ContentAction Assignment Rules

Assign `ContentAction` deterministically from the approved SCA action and the
affected KTY-local content need. If a human-approved propagation plan overrides
one of these defaults, the manifest row must cite that ruling in
`AUTHORITY_BASIS` and `BlockerNotes` or the row is invalid.

| SCA action pattern | Default `ContentAction` | Notes |
|---|---|---|
| `REMOVE` affecting an active `KNOWLEDGE_TYPE` | `ARCHIVE_AND_STUB` | Retire root-level `Scoping.md` / `KA-*.md` content for that KTY; preserve archive evidence. |
| `REMOVE` affecting a `KNOWLEDGE_SUBJECT` or `HANDBOOK_UNIT` that leaves the parent KTY active | `REGENERATE_CONTENT` | Regenerate the parent KTY so the retired subject/unit is removed from active content. |
| `MODIFY` with `SupersessionBindingPresent = YES` or any source-superseding factual change | `REGENERATE_CONTENT` | Dispatch `domain-documents` with `AUTHORITY_MODE: SCA_DRIVEN`. |
| `MODIFY` that is metadata-only and does not alter active KTY factual content | `VERIFY_ONLY` | Verify no active content rewrite is required. Metadata repair belongs to `kty-metadata-align` when separately dispatched. |
| `ADD` creating a new `KNOWLEDGE_TYPE` | `NO_ACTION` | Initial folder/content creation remains downstream initialization unless the approved plan explicitly dispatches regeneration after preparation. |
| `ADD` creating new `KNOWLEDGE_SUBJECT` rows in an existing KTY | `REGENERATE_CONTENT` | Regenerate the parent KTY to materialize the new subject-to-artifact mapping. |
| `ADD` adding `HANDBOOK_UNIT` support to an existing active KTY | `REGENERATE_CONTENT` | Regenerate or verify the parent KTY depending on whether factual content changes; default to regenerate when uncertain. |
| `RECLASSIFY` without factual-content change | `VERIFY_ONLY` | Verify active content, path references, and factual-use gate after the authoritative remap. |
| `RECLASSIFY` that changes subject membership or source authority for an active KTY | `REGENERATE_CONTENT` | Regenerate the affected KTY or KTYs. |
| `MERGE` where one KTY is absorbed into another | `ARCHIVE_AND_STUB` for absorbed KTY rows; `REGENERATE_CONTENT` for receiver KTY rows | Emit one manifest row per affected KTY. |
| `SPLIT` of an active KTY or subject set | `REGENERATE_CONTENT` | Regenerate all successor active KTYs; archive/stub a retired source KTY only when it no longer remains active. |

| Column | Type | Description |
|--------|------|-------------|
| `AmendmentID` | string | `SCA-{NNN}` |
| `ManifestRowID` | string | Sequential row id within the manifest, e.g. `KRM-001` |
| `SourceActionRef` | string | `Amendment_Actions.csv` `ActionSeq` or decision id driving the row |
| `EntityType` | enum | Triggering entity type: `KNOWLEDGE_TYPE` / `KNOWLEDGE_SUBJECT` / `HANDBOOK_UNIT` / `CATEGORY` / `VOCAB_TERM` / `OTHER` |
| `EntityID` | string | Triggering entity id or canonical term from the source action |
| `KTYID` | string | Stable KTY id |
| `KTYPath` | string | Path to the affected KTY folder |
| `AffectedSubjects` | string | Semicolon-separated `SUB-*` ids affected by this row, or blank when whole-KTY / not applicable |
| `AffectedHBK` | string | Semicolon-separated `HBK-*` ids affected by this row, or blank when not applicable |
| `CanonicalRootName` | string | Canonical root name when the project spans multiple DOMAIN roots; blank only when unambiguous |
| `FacilityID` | string | Facility id or facility scope token when relevant; blank only when not applicable |
| `ContentAction` | enum | `ARCHIVE_AND_STUB` / `REGENERATE_CONTENT` / `VERIFY_ONLY` / `NO_ACTION` |
| `Workflow` | enum | `kty-content-remediate` / `domain-documents` / `NONE` |
| `TaskMode` | string | `RETIRE_KTY`, `VERIFY_KTY`, `EMIT_DISPOSITION`, `SCA_DRIVEN`, or blank for `NO_ACTION` |
| `CONTENT_DISPOSITION_STATE` | enum | `PENDING` / `ARCHIVED_STUBBED` / `REGENERATED` / `VERIFIED` / `DEFERRED` / `BLOCKED` / `NOT_REQUIRED` |
| `FACTUAL_USE_GATE` | enum | `ALLOW_FACTUAL_USE` / `REGEN_ONLY` / `BLOCK_FACTUAL_USE` / `RETIRED_NO_FACTUAL_USE` / `NOT_APPLICABLE` |
| `AUTHORITY_BASIS` | string | Accepted upstream snapshot(s), admitted decomposition ref, and supersession map ref |
| `SOURCE_ACTION_REF` | string | Stable action/decision reference mirrored for downstream consumers |
| `RequiredEvidence` | string | Semicolon-separated required evidence types |
| `EvidencePaths` | string | Semicolon-separated paths to reports, archive directories, regenerated files, or verification logs |
| `ArchivePath` | string | Expected or actual `.Archive/` path for `ARCHIVE_AND_STUB`; blank only when not applicable |
| `LAST_VERIFIED_AT` | timestamp | ISO-like timestamp of last evidence verification |
| `BlockerNotes` | string | Required for `DEFERRED` or `BLOCKED`; empty only when complete/non-applicable |

Allowed dispatch mapping:

- `ARCHIVE_AND_STUB` dispatches `TASK + kty-content-remediate` in
  `RETIRE_KTY`.
- `REGENERATE_CONTENT` dispatches `TASK + domain-documents` with
  `AUTHORITY_MODE: SCA_DRIVEN`.
- `VERIFY_ONLY` dispatches `TASK + kty-content-remediate` in `VERIFY_KTY`.
- `NO_ACTION` requires an authority basis explaining why no KTY-local content
  disposition is needed.

### Supersession Map Schema

`Supersession_Map.csv` records the claim-level binding between SCA decisions and the upstream authority facts they supersede. The cumulative map in the active snapshot must contain all accepted supersession bindings from all prior SCAs.

Two `OverrideType` values are supported:
- **`SUPERSESSION`** — the prior authority fact is overridden. The replacement value governs; the superseded value no longer applies.
- **`SUPPLEMENTARY_EXTENSION`** — this SCA adds detail or structure not present in the prior authority. It does not override any existing governing fact. The prior authority remains valid.

| Column | Type | Description |
|--------|------|-------------|
| `AmendmentID` | string | `SCA-{NNN}` that introduced this override |
| `DecisionID` | string | Decision reference within the SCA. For amendment-backed bindings use `D-{ActionSeq}` (for example `D-003`); for decision-log-only bindings with no formal amendment action use `DL-{reference}`. |
| `SupersededAuthorityRole` | enum | `SOURCE_DBM` / `DISCIPLINE_DBM` / `VENDOR_DATA` / `REGULATORY` / `OTHER` |
| `SupersededAuthorityPath` | string | File path to the superseded authority document |
| `SupersededAuthorityRef` | string | Section, line, table, or cell reference within the authority document |
| `SupersededFactKey` | string | Machine-readable key for the fact (e.g., `03-25_INLET_STABILIZER_SCOPE`) |
| `SupersededFactTextOrValue` | string | The original authority value or statement being overridden |
| `OverrideType` | enum | `SUPERSESSION` / `SUPPLEMENTARY_EXTENSION` |
| `ReplacementFactTextOrValue` | string | The new governing value or statement |
| `AppliesToRoots` | string | Semicolon-separated list of affected canonical root names (for example `West_Doe_Comp_and_Liquids_DBM;West_Doe_Deepcut_DBM`) |
| `AppliesToFacilities` | string | Semicolon-separated list of affected canonical facility IDs (for example `03-25; 04-25`) |
| `AppliesToSections` | string | Semicolon-separated list of publication section IDs where the override is relevant. When empty, the binding applies globally across all sections in the listed roots/facilities. |
| `Notes` | string | Additional context |

### Recommended Commit Message Format

```text
scope: SCA-{NNN} — {brief description}

Variant: {DECOMP_VARIANT}
Actions: {count} ({ADD:n, REMOVE:n, MODIFY:n, ...})
Affected entities: {list}
```

---
