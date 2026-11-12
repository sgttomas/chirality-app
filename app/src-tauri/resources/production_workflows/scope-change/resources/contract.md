# scope-change — contract

This retained resource applies to DOMAIN and explicitly adopted legacy
phase/control-file projects. Current PROJECT/SOFTWARE localities use
[current-project.md](current-project.md); do not import the lifecycle/control-file
or snapshot-register obligations below into that route.

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
  - Either variant, only when the accepted checkpoint-group-2 write boundary names it exactly: an additional authoritative carrier of the changed truth, such as a deliverable `ScopeOfWork.md`, the project PRD, or an instruction file. Each carrier keeps its own authority and route: an instruction file also needs its own instruction-tranche manifest; an `ISSUED` deliverable changes only through its lifecycle route (`sgttomas/chirality:docs/COMPATIBILITY_FORMATS.md#historical-specification` (private archive) §3.3); a carrier the boundary does not name remains a downstream handoff.

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
- **Non-destructive.** Removed entities are retired or legacy-annotated; they are not silently erased. For `PROJECT/SOFTWARE`, a removed deliverable's decomposition row is annotated `[RETIRED — {AMENDMENT_ID}]` and its `_STATUS.md` gains an appended history line recording the retirement under the amendment; its lifecycle state is left unchanged (`sgttomas/chirality:docs/COMPATIBILITY_FORMATS.md#historical-specification` §3.2 lists no such state, and its historical-product extension says RETIRED is never an active project lifecycle value), and `tools/scaffolding/write_status.sh` is not used for it. Folders and files are never deleted. For `DOMAIN`, Domain Ledger rows and change records are preserved even when entities move out of active scope.
- **Reopening an `ISSUED` deliverable.** `ISSUED → IN_PROGRESS` is authorized only by an accepted amendment (its checkpoint group 3 accepted) whose accepted action register names that deliverable with action `MODIFY`, or `RECLASSIFY` where the reclassification changes the deliverable's scope, recorded as `ScopeChanging` `YES` (`sgttomas/chirality:docs/COMPATIBILITY_FORMATS.md#historical-specification` §3.3). The human records the transition in `_STATUS.md`, citing the accepted amendment snapshot. This happens after acceptance, at the `MODIFY` routing of `project-setup-retained` in `INCREMENTAL` mode, never in the candidate poststate; no agent records it. A group-1 or group-2 decision, a candidate snapshot, or an action other than `MODIFY` or scope-changing `RECLASSIFY` does not authorize it. `tools/scaffolding/write_status.sh` records the transition only for a `HUMAN` actor with `--approval-sha`, a commit that is an ancestor of `HEAD`, and `--amendment`, the amendment ID or snapshot path, that passes `tools/validation/check_amendment_reopen.py` with every amendment record read from that commit (see Deterministic Tool Contracts). In a legacy register accepted without the `ScopeChanging` column, the tool still admits `MODIFY` but refuses `RECLASSIFY`. It also refuses a run whose group 3 is not recorded as a decision snapshot or whose register is not hash-bound in a group-2 decision snapshot, an amendment that removes the deliverable, and a second reopening under an amendment already recorded in the deliverable's `_STATUS.md`. In those cases the human records a lawful reopening directly, citing the accepted snapshot. The App's lifecycle `transition.ts` still refuses `ISSUED → IN_PROGRESS` until it mirrors this check (D-GOV-51).
- **Impact before action.** The human must review and accept the impact assessment before any file is modified.
- **No direct collateral writes.** Except for an authoritative carrier the accepted checkpoint-group-2 write boundary names exactly (see `ALLOWED_PROPAGATION_WRITES`), WORKING_ITEMS does not directly modify deliverable scope carriers (`ScopeOfWork.md`, or the legacy four-document set only where a deliverable still pins it), `deliverable.yaml`, estimates, schedules, generated knowledge artifacts, or other downstream truth. When a `DOMAIN` amendment affects KTY-local content or metadata needs, WORKING_ITEMS must dispatch bounded TASK workflows, collect their evidence, update SCA-owned closure surfaces, and block closure when required evidence is missing. WORKING_ITEMS never edits active `Scoping.md`, `KA-*.md`, `_CONTEXT.md`, `_STATUS.md`, or `_REFERENCES.md` inside KTY folders itself.
- **Derivative packages are downstream only.** `DERIVATIVE_PACKAGES` may consume accepted decomposition truth, but they do not redefine it and they are never updated in place by WORKING_ITEMS except for the amendment snapshot artifacts WORKING_ITEMS itself owns.
- **KTY content one-writer rule.** (DOMAIN only.) `domain-documents` is the only writer of active DOMAIN KTY `Scoping.md` and `KA-*.md` factual content. `kty-content-remediate` may archive active-looking content and leave tombstone stubs, but it never writes regenerated active content.
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
  coordinated by `project-setup-retained` in `INCREMENTAL` mode (its Function 5) after
  checkpoint group 3 acceptance; delegation is optional.
- **`project-setup-retained` in `INCREMENTAL` mode** owns setup of the amended scope
  after acceptance: scaffolding additions, recording retirements without
  deletion, routing modified deliverables to their production contract's
  update path, and refreshing their dependency and coordination records. This
  workflow names that hand-back in `Handoff_State.md`; it does not perform it.
- **The responsible implementation owner** receives repository-change evidence
  and the exact change scope. It follows applicable repository conventions;
  a consumer may explicitly select its own supporting skill. This current workflow
  does not require Git or select the retired `change` workflow. Historical identities remain
  readable at their recorded source revision; they are not a current invocation.
- The **`dependency-extract` workflow (dispatched via TASK)** owns consumer-local need authoring/refresh in `deliverable.yaml`. WORKING_ITEMS identifies affected consumers and recommends bounded assessment; it does not author their declarations.
- The **`estimate-snapshot` workflow (dispatched via TASK)** and **WORKING_ITEMS (workflow: project-setup-retained) scheduling workflow** own estimate/schedule updates. WORKING_ITEMS recommends reruns; does not execute them.
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

**Interpretation note:** pure mapping corrections use `MODIFY` unless the parent partition / parent entity changes, in which case use `RECLASSIFY`. For PROJECT/SOFTWARE local needs, the affected consumer assesses the accepted change against its actual condition and use. A retired production obligation may leave a usable historical artifact; reference remapping is never automatic. Preserve distinct cases, triggers, technical holds and unresolved source bindings.

**Structural-change rule:** a `REMOVE`, `RECLASSIFY`, `MERGE`, or `SPLIT` affecting a parent partition or parent entity is invalid unless the same amendment explicitly resolves the full child-closure set and every authoritative ledger remapping.

---

## Inputs

### Required before checkpoint group 1
- A human request or an evidence-backed agent proposal for a decomposition
  change (natural language or structured). A `scope-change-packet` seed or
  a bounded analysis of actual input conditions may supply intake evidence;
  neither is an accepted action. The checkpoint-group-1 decision still
  applies. `tools/validation/validate_scope_change_packet.py` validates only
  the seed-packet form, not arbitrary dependency observations or this
  workflow's own artifacts.

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
- `AMENDMENT_ID`: human-assigned `SCA-{NNN}` (default: next available scanned from `_ScopeChange/` folder names). A project whose accepted records use a project-qualified form (for example `SCA-APP-{NNN}`) keeps that form; scan with its prefix (see method step 4). Wherever this contract writes `SCA-{NNN}`, read the project's qualified form.
- `ALLOW_RENUMBERING`: `true|false` (default `false`)
- `ALLOWED_PROPAGATION_WRITES`: explicit narrower write list if the human wants stricter write quarantine than the defaults

### Deterministic Tool Contracts

WORKING_ITEMS may interpret findings, decide handoff state, and write human-facing summaries, but it must not reimplement deterministic CSV merge, coverage serialization, or DOMAIN referential-integrity validation in prose. Use these registered tools when the corresponding artifact is required:

- `tools/reporting/synthesize_domain_coverage_json.py` for DOMAIN `Pre_Change_Coverage.json` and `Post_Change_Coverage.json`.
- `tools/coordination/accumulate_supersession_map.py` for cumulative `Supersession_Map.csv` generation and optional check-mode comparison.
- `tools/validation/validate_domain_decomposition_integrity.py` for DOMAIN annex integrity, coverage telemetry reconciliation, active snapshot artifact checks, `_LATEST.md` parity, and KTY remediation rollup consistency.
- `tools/validation/validate_kty_remediation_manifest.py` for KTY remediation manifest schema, dispatch mapping, evidence, closure-state, and scanner-exclusion checks.
- `tools/validation/check_amendment_reopen.py` for the amendment record behind reopening an `ISSUED` deliverable; `tools/scaffolding/write_status.sh --amendment` runs it as `--at-commit <approval SHA>`. In that mode it reads every record it relies on from that commit through git, never from the working tree: the group-3 `DECISION.md` and `ACCEPTED_MANIFEST.csv`, every group-2 `ACCEPTED_MANIFEST.csv`, and the register. It lists `checkpoint_snapshots/` from the commit's tree, so untracked or uncommitted folders do not count, and it refuses a commit that is not an ancestor of `HEAD`. Its git reads ignore local replace refs and grafts. Run without `--at-commit`, it reads the working tree and reports the result as unanchored; that mode is for inspection only, and `write_status.sh` never uses it. It admits only when all of these checks pass:
  - a decision folder `checkpoint_snapshots/{AMENDMENT_ID}_GROUP-3_[AMENDMENT-{K}_]{YYYY-MM-DD}[_{N}]/` holds `ACCEPTED_MANIFEST.csv` and a `DECISION.md` whose first non-blank line is the heading `# {AMENDMENT_ID} checkpoint group 3 — accepted …`, with `accepted` directly after the dash and followed by a space, `.`, `,`, `;` or the end of the line. A folder with any other name, such as a candidate, does not count. Group 3 either accepts or returns the poststate, so a qualified acceptance (for example `accepted with a limited basis`) is the accepted outcome; the tool does not interpret its qualifications;
  - the governing group-2 decision snapshot binds the register, and the register's SHA-256 still matches. The governing snapshot is the latest `{AMENDMENT_ID}_GROUP-2_*` folder whose `ACCEPTED_MANIFEST.csv` binds a register: highest `AMENDMENT-{K}` first, then date, then `_{N}`. A revised group-2 acceptance therefore replaces an earlier binding, and one that binds no register leaves the earlier binding in force. The register is the row whose file name begins `Amendment_Actions` and ends `.csv`; where one manifest binds several such rows, it is the single row whose `Role` is `action register` or `exact final action register` (case-insensitive, optionally followed by a parenthesized note), matched as the whole value;
  - the register rows naming the deliverable have `EntityType` `DELIVERABLE`, `EntityID` equal to the deliverable ID (or the ID followed by `_` and a label), and `AmendmentID` equal to the amendment ID or blank (a row carrying another amendment ID does not count). No such row is `REMOVE`, even when another row modifies the deliverable. One row is `MODIFY`, or `RECLASSIFY` with `ScopeChanging` `YES`. Values are read as recorded: a leading or trailing space in one of these values or column names is refused as a schema error;
  - given the deliverable's `_STATUS.md` (as `write_status.sh` passes it), its history does not already record `reopened from ISSUED; amendment: {AMENDMENT_ID}`. Each accepted amendment admits one tool-recorded reopening; a human may still record a further reopening directly.

  The scope-change root is the `_ScopeChange/` folder of the deliverable's execution root (`{CONTEXT_ROOT}` for `PROJECT`/`SOFTWARE`): the deliverable's outermost `execution/` ancestor, which the project's adapter manifest must agree with where one exists. A `_ScopeChange/` inside a package or deliverable folder is not used. The tool reads only inside that root. It refuses a path, or a symlink entry, that leaves it. It checks recorded structure and hashes; it does not establish that the human's act was genuine, that the cited commit records it, or interpret the decision beyond its heading. Refusal codes: `AMENDMENT_UNRESOLVED`, `SCOPE_CHANGE_ROOT_NOT_FOUND`, `PATH_ESCAPE`, `AMENDMENT_OUTSIDE_DELIVERABLE_ROOT`, `APPROVAL_SHA_UNREACHABLE`, `APPROVAL_SHA_NOT_ANCESTOR`, `AMENDMENT_ALREADY_USED`, `GROUP3_NOT_ACCEPTED`, `GROUP2_MANIFEST_MISSING`, `MANIFEST_SCHEMA`, `REGISTER_NOT_BOUND`, `REGISTER_AMBIGUOUS`, `REGISTER_MISSING`, `REGISTER_HASH_MISMATCH`, `REGISTER_SCHEMA`, `NO_DELIVERABLE_ACTION`, `DELIVERABLE_REMOVED`, `RECLASSIFY_LEGACY_REGISTER`, `RECLASSIFY_NOT_SCOPE_CHANGING`, `ACTION_NOT_AUTHORIZING`.

**Layout convention (DOMAIN):** `--decomposition-root` resolves the canonical annexes-at-`_Decomposition`-root layout by default. The synthesizer and integrity validator also accept `--package-subfolder {NAME}` (or auto-descend when a single subfolder is present) as a transitional / forward-compatible accommodation for packages still using a nested-snapshot layout. Both invocation forms are valid; pass `--package-subfolder` only when the root contains no annex files directly.

### Variant Section Binding

All protocol steps reference sections by **semantic name** and then bind those semantics to the originating decomposition variant **by heading text, never by section number**, using the normalization and rank-order matching defined in `sgttomas/chirality:workflows/audit-decomp/resources/contract.md#variant-section-binding` (private archive). If no rank yields a hit, stop and report an unresolved binding rather than resolving by position.

| Semantic section | WORKING_ITEMS (workflow: project-decomp) | WORKING_ITEMS (workflow: software-decomp) | WORKING_ITEMS (workflow: domain-decomp) | Notes |
|------------------|----------------|-----------------|---------------|-------|
| Change Register | `Change Log` | `Decision Log` and/or `Revision History` | `Decision Log / Change Log` | Bind by heading text, never by number. `WORKING_ITEMS (workflow: software-decomp)` may split this across two headings; read both when both exist |
| Unit Ledger | `Scope Ledger` | `Scope Ledger` | `Domain Ledger` | Authoritative row-level mapping table |
| Objectives | `Objectives` | `Objectives` where present, otherwise the `ObjectiveID(s)` column of `Scope Ledger` | — | `WORKING_ITEMS (workflow: domain-decomp)` does not have an Objectives layer |
| Primary Partitions | `Packages` | `Packages` | `Categories` | Flat partition primitive |
| Secondary Entities | `Deliverables` | `Deliverables` | `Knowledge Types` | Parented to the primary partition |
| Tertiary Entities | — | — | `Knowledge Subjects` | Parented to `Knowledge Types` |
| Vocabulary Map | — | — | `Vocabulary Map` | Canonical terms and synonyms |
| Coverage Basis | Bounded register-validator coverage output | Bounded register-validator coverage output | `Coverage & Telemetry` + `Domain Ledger` export | Used for pre/post comparison |

### Variant-specific ID formats

When validating or proposing IDs, use the originating decomposition's grammar:

- `WORKING_ITEMS (workflow: project-decomp)`: `PKG-XX` / `DEL-XX-YY_{desc}`
- `WORKING_ITEMS (workflow: software-decomp)`: `PKG-XX` / `DEL-XX-YY`
- `WORKING_ITEMS (workflow: domain-decomp)` (grammar owned by `sgttomas/chirality:workflows/domain-decomp/resources/contract.md`, private archive):
  - `HBA-<SOURCE_PREFIX>-NNNNN` for Handbook Units / atomic units (read historical `HBK-*` or unprefixed `HBA-####` aliases only when the accepted basis supplies their mapping)
  - no `OBJ-*` layer; `DOMAIN` has no Objectives section
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
- `Amendment_Actions.csv` (or the distinct name bound in the group-2 manifest for a run whose group-1 snapshot already bound that file), the accepted checkpoint-group-2 action register, accounts for every atomic change; `Handoff_State.md` names it as the authoritative register.
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
  _LATEST.md                       (active accepted SCA snapshot; moved only after checkpoint-group-3 acceptance)
  SCA-{NNN}_GROUP-{N}_AUTHORIZED.md  (amendment-qualified pointer to the accepted group-1 or group-2 decision snapshot; written after that snapshot is complete)
  checkpoint_snapshots/
    SCA-{NNN}_GROUP-{N}_{YYYY-MM-DD}/  (immutable decision snapshot per accepted checkpoint; a revised acceptance adds a new folder, e.g. `..._AMENDMENT-{K}_...`)
      DECISION.md                  (the human's actual act, verbatim where available, and its recorded interpretation)
      ACCEPTED_MANIFEST.csv        (path, SHA-256, role and acceptance boundary of each accepted artifact)
      Handoff_State.md             (what the next stage consumes and what remains unauthorized)
  _PostAcceptanceValidation/
    {AMENDMENT_ID}_{UTC}/          (append-only verification of acceptance-conditional edits and the now-active snapshot)
  SCA-{NNN}_{YYYY-MM-DD}_{HHMM}/
    Brief.md                       (human's original request + parsed actions)
    Intake_Actions.csv             (checkpoint-group-1 parsed actions; every row `Status = PROPOSED`)
    Impact_Assessment.md           (checkpoint-group-1 output)
    Amendment_Preview.md           (checkpoint-group-2 diff-style exact amendment, including acceptance-conditional edits)
    Propagation_Plan.md            (checkpoint-group-2 output)
    Amendment_Actions.csv          (accepted checkpoint-group-2 action register; bound by hash in the group-2 `ACCEPTED_MANIFEST.csv`)
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

The role that presents a checkpoint to the human writes that checkpoint's
decision snapshot from the human's actual act. It records only what the human
had in front of them and did; it claims no inspection the human did not
perform. Checkpoint group 3 may also be recorded as a `checkpoint_snapshots/`
decision folder; the accepted `SCA-*` snapshot remains the `_LATEST.md` target.
An amendment that authorizes reopening an `ISSUED` deliverable records group 3
this way, in a folder named `{AMENDMENT_ID}_GROUP-3_{YYYY-MM-DD}`, with a
`DECISION.md` whose first line is the heading
`# {AMENDMENT_ID} checkpoint group 3 — accepted …`, and commits it, so that
`write_status.sh` can check it at the approval commit. A revised group-2
acceptance (`{AMENDMENT_ID}_GROUP-2_AMENDMENT-{K}_{YYYY-MM-DD}`) that changes
the register binds the revised register in its own `ACCEPTED_MANIFEST.csv`;
the latest such binding governs.

Historical runs remain readable as written. A run that predates this layout may
carry its accepted register under another name (for example
`Amendment_Actions_CP2.csv`, bound in its group-2 `ACCEPTED_MANIFEST.csv`) or
gate-numbered handoff files; consumers resolve the register through the
accepted manifest and do not rewrite those runs. A run whose group-1 snapshot
already binds `Amendment_Actions.csv` as its intake keeps that file unchanged
and writes its group-2 register under a distinct name (for example
`Amendment_Actions_CP2.csv`), bound in the group-2 `ACCEPTED_MANIFEST.csv` and
named in `Handoff_State.md`.

### `RUN_SUMMARY.md` / `Handoff_State.md` state fields

The active snapshot must expose these fixed state fields across `RUN_SUMMARY.md` and/or `Handoff_State.md`:

| Field | Allowed values | Meaning |
|---|---|---|
| `DecompositionTruthState` | `NOT_STARTED` / `INCOMPLETE` / `COMPLETE` | Whether the main decomposition document amendments are complete; `NOT_STARTED` before any accepted amendment is applied |
| `DerivativePackageState` | `INCOMPLETE` / `COMPLETE` | Whether affected decomposition-local derivative surfaces are in parity |
| `ContentRemediationState` | `NOT_REQUIRED` / `PENDING` / `COMPLETE` / `BLOCKED` / `DEFERRED` | Rollup state for SCA-owned KTY content remediation manifest rows |
| `DownstreamRerunState` | `NOT_REQUIRED` / `FROZEN` / `IN_PROGRESS` / `COMPLETE` / `BLOCKED` | Whether downstream reruns are pending or complete |
| `MetadataAlignmentState` | `NOT_REQUIRED` / `NOT_STARTED` / `IN_PROGRESS` / `COMPLETE` / `BLOCKED` | Whether post-regeneration metadata alignment is complete |
| `AuditState` | `NOT_RUN` / `WARNINGS` / `NON_BLOCKING_PASS` / `BLOCKED` | Current audit / verification state over all findings (raw) |
| `AdjustedAuditState` | same values | Audit state excluding findings classified `EXPECTED_CONSEQUENCE`; recorded with that classification table |
| `ReadyForNextPhase` | `NO` / `REGEN_ONLY` / `PHASE7_REVIEW` / `PUBLICATION_GATED` / `NOT_APPLICABLE` | Highest phase the current artifact state actually supports; `NOT_APPLICABLE` when the variant has no such phase ladder (for example `PROJECT/SOFTWARE`) |

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

`Amendment_Actions.csv` is the accepted checkpoint-group-2 register.
`Intake_Actions.csv` uses the same columns plus a trailing `Status` column whose
value is `PROPOSED`; it is intake evidence and never becomes the accepted
register by renaming.

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
| `ScopeChanging` | enum | `YES` / `NO`. `YES` when the action changes the scope of the entity it names, `NO` otherwise. A `PROJECT`/`SOFTWARE` deliverable `RECLASSIFY` that `scope-change` treats as `MODIFY` plus relocation is `YES`. Checkpoint-group-2 preparation records it on every row, and the human accepts it with the register. `Intake_Actions.csv` may leave it blank. For a `DELIVERABLE` `RECLASSIFY` it decides whether the accepted amendment authorizes reopening an `ISSUED` deliverable; a `MODIFY` authorizes reopening whatever its value. A register accepted without this column is a legacy register: tools admit reopening only for its `MODIFY` rows (see the reopening invariant). |

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
| `ADD` creating a new `KNOWLEDGE_TYPE` | `NO_ACTION` | Initial folder/content creation is downstream initialization by `project-setup-retained` in `INCREMENTAL` mode unless the approved plan explicitly dispatches regeneration after preparation. |
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
| `AffectedHBK` | string | Semicolon-separated Handbook Unit ids (`HBA-<SOURCE_PREFIX>-NNNNN`; historical `HBK-*` aliases only where the accepted basis maps them) affected by this row, or blank when not applicable. The column name is retained for validator and historical compatibility |
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
| `AppliesToRoots` | string | Semicolon-separated list of affected canonical root names (for example `Example_Compression_DBM;Example_Gas_Plant_DBM`) |
| `AppliesToFacilities` | string | Semicolon-separated list of affected canonical facility IDs (for example `03-25; 04-25`) |
| `AppliesToSections` | string | Semicolon-separated list of publication section IDs where the override is relevant. When empty, the binding applies globally across all sections in the listed roots/facilities. |
| `Notes` | string | Additional context |

### Recommended Commit Message Format

The project's own change conventions or change skill govern commit messages
when present. Otherwise this form may be used:

```text
scope: SCA-{NNN} — {brief description}

Variant: {DECOMP_VARIANT}
Actions: {count} ({ADD:n, REMOVE:n, MODIFY:n, ...})
Affected entities: {list}
```

---
