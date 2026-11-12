# scope-change — method

This retained resource applies to DOMAIN and explicitly adopted legacy
phase/control-file projects. Current PROJECT/SOFTWARE localities use
[current-project.md](current-project.md); do not import the lifecycle/control-file
or snapshot-register obligations below into that route.

## Method

### Checkpoint group 1 preparation, part A — change intake and validation

**Starting input:** A human-requested change or an agent-identified,
evidence-backed amendment proposal. An agent proposal changes no canonical
truth before the grouped human decisions.

For each accepted checkpoint, write a new immutable decision snapshot with
`DECISION.md`, `ACCEPTED_MANIFEST.csv`, and `Handoff_State.md`. Group-1 and
group-2 snapshots live under `_ScopeChange/checkpoint_snapshots/` and update
their amendment-qualified authorized pointers only after completion. The final
audited poststate becomes the immutable `SCA-*` snapshot and `_LATEST.md` only
after checkpoint group 3 acceptance. Each later stage resolves and consumes the
preceding accepted snapshot; it does not rely on the mutable preview alone.
Where the accepted register names an `ISSUED` deliverable with `MODIFY` or
scope-changing `RECLASSIFY`, also record the group-3 acceptance as a
`checkpoint_snapshots/{AMENDMENT_ID}_GROUP-3_{date}/` decision folder whose
`DECISION.md` first line is the heading
`# {AMENDMENT_ID} checkpoint group 3 — accepted …`, and commit it with the
accepted register and group-2 decision snapshot. When the human reopens the
deliverable, `write_status.sh --amendment` reads those records at the commit
the human cites as `--approval-sha`, which must be an ancestor of `HEAD`;
uncommitted records do not count. Each accepted amendment admits one
tool-recorded reopening per deliverable, and an amendment that removes the
deliverable admits none.

**Agent does:**

1) Resolve `DECOMP_VARIANT`, `CONTEXT_ROOT`, and `DECOMPOSITION_PATH`. Parse the current decomposition state using the semantic section binding table in [the contract](contract.md) (§Variant Section Binding).
2) Parse the human's request or the admitted evidence-backed proposal (including a `scope-change-packet` seed or bounded source-based dependency analysis) into one or more atomic actions:
   - `ActionType`
   - `EntityType`
   - `EntityID`
   - `RequestedChange`
   - `AffectedSections`
3) For each action, validate:
   - `ADD`: proposed ID/term does not already exist; parent entity exists (or is also being added); ID format is valid for the variant.
   - `REMOVE`: referenced entity exists in the decomposition and is not already retired.
   - `MODIFY`: referenced entity exists; proposed changes are to valid fields/columns/attributes.
   - `RECLASSIFY`: source and target parents both exist; ID retention vs explicit renumbering is recorded.
   - `MERGE`: all source entities exist; proposed successor entity/ID is valid; source IDs remain reserved.
   - `SPLIT`: source entity exists; proposed fragment IDs do not collide and the remapping intent is explicit.
   - **Parent-closure rule**:
     - any `REMOVE`, `RECLASSIFY`, `MERGE`, or `SPLIT` on a parent partition / parent entity is invalid unless the same amendment explicitly resolves every child entity, every parent-binding field, and every authoritative ledger mapping beneath it.
   - `PROJECT/SOFTWARE` specific:
     - package / deliverable lineage changes resolve the affected Scope Ledger rows in the same amendment,
     - package-level structural changes resolve every child deliverable and the affected `_CONTEXT.md` / `_STATUS.md` files or produce an explicit handoff set,
     - if the originating decomposition defines package-discipline isolation, artifact-kind deliverable granularity, or equivalent design-partition rules, the proposed change does not violate those rules unless it is surfaced as an explicit contract-level change for human approval.
   - `DOMAIN` specific:
     - every affected Handbook Unit (`HBA-<SOURCE_PREFIX>-NNNNN`) remains explicitly `IN | OUT | TBD`,
     - every `IN` Handbook Unit ends with exactly one `CategoryID`,
     - every `KTY-*` belongs to exactly one `Category`,
     - every `SUB-*` belongs to exactly one `KTY-*`,
     - every `KTY-*` ends with at least one `SUB-*`,
     - any `CAT-*` or `KTY-*` structural change resolves all child `KTY-*`, `SUB-*`, and `Domain Ledger` mappings in the same amendment,
     - vocabulary impacts are enumerated,
     - Coverage & Telemetry consequences are identified up front.
4) Assign `AMENDMENT_ID` (next available `SCA-{NNN}`). Scan existing: `tools/query/scan_next_amendment_id.sh {SCOPE_CHANGE_ROOT}` (or inline directory scan if no dedicated helper exists). Without a prefix the helper counts only unqualified `SCA-{NNN}` folders. A project whose accepted records use project-qualified IDs (for example `SCA-APP-{NNN}`) passes its prefix, `tools/query/scan_next_amendment_id.sh {SCOPE_CHANGE_ROOT} APP`, and keeps that form in every artifact.
5) Capture the **pre-change baseline**:
   - `PROJECT/SOFTWARE`: run a bounded coverage review of the affected packages/deliverables with the project's register validator (for example `tools/validation/validate_decomposition_registers.py`) and store its output path. The former `audit-decomp` workflow was removed on 2026-11-04 and is preserved in the private `sgttomas/chirality` repository.
   - `DOMAIN`: run the deterministic coverage serializer against the current frozen decomposition state:
     `python3 tools/reporting/synthesize_domain_coverage_json.py --decomposition-root {CONTEXT_ROOT}/_Decomposition --output-json {snapshot}/Pre_Change_Coverage.json --missing-manifest-state NOT_FORMALIZED`
   - An existing baseline audit may be reused instead of a fresh run when its
     recorded input decomposition and registers are byte-identical to the
     current pre-change state. Record the reused audit path, the compared input
     hashes and the reuse in `Brief.md` or `Impact_Assessment.md`.
6) Write the parsed actions to `Intake_Actions.csv` with every row
`Status = PROPOSED`. It is intake evidence, not the accepted register. A run
whose group-1 snapshot already binds `Amendment_Actions.csv` as its intake keeps
that file unchanged and writes its group-2 register under a distinct name (for
example `Amendment_Actions_CP2.csv`). Carry the
parsed action list, validation results, errors, warnings, unknowns, and
pre-change coverage into the impact assessment. Do not ask for a separate
intake decision.

---

### Checkpoint group 1 preparation, part B — impact assessment

**Agent does:**

For each validated action, trace impact across four lenses:

1) **Decomposition structure**
   - What sections, IDs, rows, and mappings will change?

2) **Variant-local metadata**
   - Which metadata files are inside write scope?
   - Which are only advisory / downstream?

3) **Downstream consumers**
   - Which workflows, generated artifacts, or audits may need reruns?
   - Which derivative packages become stale, and which owning workflow must close each one?

4) **Invariant / telemetry risk**
   - What could become orphaned, unmapped, stale, or semantically inconsistent?
   - What closure obligations must be completed in the same amendment for parent partitions / parent entities?
   - What closure obligations are deferred to downstream derivative-package owners and therefore must appear in `HANDOFF_STATE`?

Action-specific tracing rules:

**`ADD`**
- Identify required new rows/sections and any parent-binding obligations.
- If the addition creates a new parent partition / parent entity, identify the expected child-closure set and any companion rows that must be added in the same amendment.
- `PROJECT/SOFTWARE`: inspect sibling deliverables for likely dependency patterns; note that incremental setup (`project-setup-retained`, `INCREMENTAL` mode) will scaffold the addition with the effective source-qualified `preparation` skill and refresh its dependencies after acceptance.
- `DOMAIN`: identify whether the addition creates new Category / Knowledge Type / Knowledge Subject / Handbook Unit / Vocabulary obligations, including ledger mappings, subject-cardinality obligations, and telemetry deltas. New or modified Categories and Knowledge Types incur a retrieval-driven scope-ratification obligation during poststate validation.

**`REMOVE`**
- Trace every reference to the entity being retired.
- If the retired entity is a parent partition / parent entity, enumerate the full child-closure set and every ledger remapping that must be completed in the same amendment.
- `PROJECT/SOFTWARE`: derive the affected consumers with `tools.deliverables neighborhood` / `impact`, then inspect their actual local need conditions and estimate/schedule references. Use `construct-local-work-graph` and `tools/deliverables/README.md`; the CLI needs a project root in a Git repository with HEAD, and its cycles cover native deliverables only. Every query loads all project declarations/path-presence references; use it only within the authorized read scope. Otherwise inspect relevant `deliverable.yaml` sources directly and state reverse-link limits. Retirement alone does not invalidate an input artifact; assess its actual condition and accepted use before proposing a change.
- `DOMAIN`: enumerate affected `HBA-*`, `CAT-*`, `KTY-*`, `SUB-*`, and canonical term occurrences. Count potential orphan conditions:
  - `UnassignedINUnits`
  - `UnitsWithoutKnowledgeTypeMapping`
  - `TypesWithoutSubjects`
  - `SubjectsWithoutParentType`
  - `TerminologyViolations`

**`MODIFY`**
- List the specific fields, columns, or narrative sections that will change.
- `PROJECT/SOFTWARE`: if `Type`, `ResponsibleParty`, or `Name` changes, flag dependency / estimate / label implications; if the change alters package discipline, deliverable kind, or deliverable granularity, flag a decomposition-contract risk.
- `DOMAIN`: if scope descriptions, canonical schemas, or canonical terms change, flag downstream knowledge-artifact refresh needs and terminology consistency checks.

**`RECLASSIFY`**
- Same as `MODIFY`, plus parent-lineage changes.
- If the moved entity is a parent partition / parent entity, enumerate every child row and authoritative mapping that moves with it in the same amendment.
- `PROJECT/SOFTWARE`: flag folder relocation advisory when package lineage changes, and flag any breach of package-discipline isolation.
- `DOMAIN`: flag regrouping / reindex implications and explicitly note whether stable IDs are being retained even if their embedded prefix no longer reflects the new parent.

**`MERGE`**
- Union of `REMOVE` impacts for all sources.
- `ADD` impacts for the successor entity.
- If a parent partition / parent entity is being merged, enumerate the combined child-closure set and the successor bindings for every child row and authoritative mapping.
- Assess affected references against actual source conditions; list justified dependency changes without automatic retargeting.

**`SPLIT`**
- `REMOVE` impacts for the source entity.
- `ADD` impacts for each successor entity.
- If a parent partition / parent entity is being split, enumerate how every child row and authoritative mapping distributes across the successors.
- List all references that must be distributed across the successors.

Produce `Impact_Assessment.md` with:
- Impact summary table (`action → affected sections/files/workflows`)
- Derivative-package status table (`package → owner → status after amendment → required rerun/closure action`)
- Derivative-surface classification table (`surface → DIRECT_EDIT|RECOMPUTE|NO_CHANGE → authority basis`)
- Orphan-risk summary (variant-specific counts)
- Estimate/schedule staleness risk or knowledge-regeneration risk, as applicable
- Active snapshot / handoff-state impact notes
- Recommended downstream reruns

**Checkpoint group 1 — proposed change and impact:** Present the parsed change,
validation results, pre-change baseline, Impact Assessment, affected identities,
downstream consumers, and unresolved risks as one reviewable package. The human
confirms or modifies the proposed change and its impact.

After acceptance, finalize the group-1 decision snapshot and pointer. Group-2
preparation must consume that accepted snapshot.

---

### Checkpoint group 2 preparation, part A — exact amendment

Resolve and consume the accepted group-1 decision snapshot before drafting the
exact amendment.

**Agent does:**

Draft the exact text changes to the decomposition document using **semantic sections**, not hard-coded project-only nouns:

1) **Change Register**
   - Add an amendment entry with:
     - `AMENDMENT_ID`
     - date
     - brief description
     - requested by `{human}`

2) **Primary Partition section** (`Packages` or `Categories`)
   - `ADD`: new row/entry
   - `REMOVE`: existing row annotated `[RETIRED — {AMENDMENT_ID}]` or equivalent legacy note
   - `MODIFY`: field updates shown as before → after
   - `MERGE/SPLIT/RECLASSIFY`: parent bindings, child-closure set, and retirement notes shown explicitly
   - A parent-partition amendment is not preview-complete unless every affected child row and authoritative ledger remap appears in the same diff

3) **Secondary Entity section** (`Deliverables` or `Knowledge Types`)
   - Apply the same add / retire / modify / lineage rules
   - `DOMAIN`: any amendment touching a `Knowledge Type` must preview the resulting subject set and show that at least one `Knowledge Subject` remains after the change

4) **Tertiary Entity section** (`Knowledge Subjects`, if any)
   - Apply the same add / retire / modify / lineage rules

5) **Unit Ledger** (`Scope Ledger` or `Domain Ledger`)
   - Update authoritative row-level mappings
   - `PROJECT/SOFTWARE`: scope item → package/deliverable mappings
   - `DOMAIN`: `HBA-*` rows, `CategoryID`, `KnowledgeTypeID(s)`, `SubjectID(s)`, `OpenIssue`, and decision refs

6) **Objectives** (`PROJECT/SOFTWARE` only — not applicable to `DOMAIN`)
   - Update objective statements or objective mappings
   - `SOFTWARE`: objective amendments are reflected in the Scope Ledger rather than a dedicated Objectives section

7) **Vocabulary Map** (`DOMAIN`, if affected)
   - Add / retire / modify canonical terms and synonym mappings
   - Enumerate any explicit terminology replacements required in the decomposition text

8) **Coverage / Telemetry / Open Issues**
   - Update the relevant summary block and open issue list
   - `DOMAIN`: preview the recomputed `UnitCount`, `CategoryCount`, `KnowledgeTypeCount`, `SubjectCount`, `UnassignedINUnits`, `UnitsWithoutKnowledgeTypeMapping`, `OpenIssuesByType`, and `Revision`; poststate preparation must verify the final amended annexes with `validate_domain_decomposition_integrity.py`
   - `PROJECT/SOFTWARE`: incorporate any audit-facing notes required by the change

9) **Derivative package / active snapshot state** (`DOMAIN`, if affected)
   - Preview every affected decomposition-local derivative surface with one of:
     - `DIRECT_EDIT`
     - `RECOMPUTE`
     - `NO_CHANGE`
   - Show the expected active snapshot state after execution, including the required handoff-state values

Prepare the full amendment as a diff-style preview in `Amendment_Preview.md`:
sections with before/after or additions/retirements clearly marked. Mark any
edit whose bytes depend on the future acceptance act (for example acceptance
dates, status header lines or pointer moves) as acceptance-conditional and state
its exact rule. Carry it into the propagation-plan package; do not ask for a
separate amendment decision.

---

### Checkpoint group 2 preparation, part B — propagation plan

**Agent does:**

Based on the approved amendment, produce a propagation plan **limited to the approved write scope**. If the amendment changes a parent partition / parent entity, the plan MUST enumerate the full child-closure set and every authoritative mapping change completed in the same amendment.

1) **For `ADD` actions**
   - `PROJECT/SOFTWARE`:
     - Plan the hand-back to `project-setup-retained` in `INCREMENTAL` mode (its
       Function 5), which runs after checkpoint group 3 against the accepted
       snapshot. For each added package or deliverable, name its accepted
       decomposition row, parent package and any human-declared
       dependencies. Incremental setup discovers the effective `preparation`
       skill descriptor, preserves it in the ordered `methods` field as
       `[{kind: "skill", name: "preparation", source: <descriptor.source>, sourceRootId: <descriptor.sourceRootId>}]`
       without hardcoding an origin, creates the folder structure and metadata
       files, and initializes production with `scope-of-work`, `MODE=INIT`.
     - Expected files after incremental setup: `_CONTEXT.md`, `_STATUS.md` (`OPEN`), `_REFERENCES.md`, `deliverable.yaml`, placeholder `_SEMANTIC.md`. Local needs retain the accepted identity; an empty list does not establish completeness.
     - Any propagation step or dispatched workflow that reads `_STATUS.md` must also read sibling `_MEMORY.md` / `MEMORY.md` when present as non-authoritative operational context.
   - `DOMAIN`:
     - Add new rows to the relevant decomposition annex CSVs (Domain Ledger, Knowledge Type Register, Knowledge Subject Register, Vocabulary Map, etc.)
     - Plan the hand-back of new `Category` / `Knowledge Type` folders and their initial KTY-local content to `project-setup-retained` in `INCREMENTAL` mode; new `Knowledge Subject` rows in an existing KTY follow the KTY remediation lanes below

2) **For `REMOVE` actions**
   - `PROJECT/SOFTWARE`:
     - Annotate the decomposition row `[RETIRED — {AMENDMENT_ID}]`.
     - Read the deliverable `_STATUS.md` and sibling `_MEMORY.md` / `MEMORY.md` when present, then plan one appended `_STATUS.md` history line recording the retirement under the amendment, for example `- {YYYY-MM-DD} — Retired under {AMENDMENT_ID}; lifecycle state remains {CURRENT_STATE} ({ACTOR})`. Leave `**Current State:**` unchanged (`sgttomas/chirality:docs/COMPATIBILITY_FORMATS.md#historical-specification` (private archive) §3.2 lists no such state, and its historical-product extension says RETIRED is never an active project lifecycle value), and `tools/scaffolding/write_status.sh` is not used for retirement.
     - Do **not** delete the folder or any files
     - If a `PACKAGE` is being retired, enumerate every child deliverable and Scope Ledger row being retired or remapped in the same amendment
   - `DOMAIN`:
     - Do **not** delete authoritative rows silently
     - If a `CATEGORY` or `KNOWLEDGE_TYPE` is being retired, enumerate every child `KTY-*` / `SUB-*` row and every affected `Domain Ledger` mapping being retired or remapped in the same amendment
     - Removing the last `Knowledge Subject` of a `Knowledge Type` is invalid unless the same amendment adds/remaps a successor subject or retires/remaps the parent `Knowledge Type`
     - List any downstream generated knowledge artifacts that should be marked review-needed / retired by their owning workflow

3) **For `MODIFY` actions**
   - `PROJECT/SOFTWARE`: list specific `_CONTEXT.md` edits per affected deliverable, and record each deliverable's lifecycle state. For an `ISSUED` deliverable, state in the plan that this amendment, once accepted at checkpoint group 3, is the record that authorizes its reopening (`ISSUED → IN_PROGRESS`, `sgttomas/chirality:docs/COMPATIBILITY_FORMATS.md#historical-specification` §3.3): the human records the transition after acceptance, citing the accepted snapshot (with `write_status.sh --amendment`, which checks the committed record at the approval SHA), and `project-setup-retained` in `INCREMENTAL` mode then routes the contract revision. For a `CHECKING` deliverable, state that the revision waits for a human reversal to `IN_PROGRESS`
   - `DOMAIN`: list exact edits to the decomposition document and affected annex CSVs, and list any downstream KTY-local artifacts or terminology indexes that should be refreshed by their owning workflow

4) **For `RECLASSIFY` actions**
   - `PROJECT/SOFTWARE`:
     - Same as `MODIFY`, plus folder relocation advisory if the folder path implies package lineage
     - Record `ScopeChanging` for each deliverable `RECLASSIFY`: `YES` when the reclassification changes the deliverable's scope (treated as `MODIFY` plus relocation), `NO` when it only moves the deliverable. Only a `YES` row authorizes reopening an `ISSUED` deliverable once the amendment is accepted; say which applies in the plan
     - If a `PACKAGE` is reclassified or merged/split across package boundaries, enumerate every child deliverable and Scope Ledger remap that moves with it
   - `DOMAIN`:
     - Same as `MODIFY`, plus regrouping / reindex advisory
     - If a `CATEGORY` or `KNOWLEDGE_TYPE` is reclassified, enumerate every child row and `Domain Ledger` remap that moves with it
     - Record whether IDs are intentionally retained despite parent-lineage change

5) **For `MERGE/SPLIT` actions**
   - Combine the relevant `REMOVE` + `ADD` propagation items
   - Explicitly list reference-assessment and rerun obligations; dependency retargeting requires the affected consumer's actual condition/use and the accepted change

6) **Downstream rerun advisory and KTY remediation dispatch plan**
   - `PROJECT/SOFTWARE`: incremental setup (`project-setup-retained`, `INCREMENTAL` mode) for added, retired and modified deliverables, including bounded local need assessment for them and affected consumers (derived on demand); estimate snapshot, scheduling, any scoped audits
   - `DOMAIN`: downstream knowledge-generation workflows, terminology QA / grep, and any coverage audit or regeneration workflow that consumes the decomposition
   - For `DOMAIN` amendments that affect KTY-local content, produce `KTY_Remediation_Manifest.csv` rows in the SCA snapshot plan. These rows are per-SCA action/evidence ledger rows, not a cumulative content-disposition surface.
   - Manifest actions drive post-acceptance dispatch.
     - `ARCHIVE_AND_STUB` -> `TASK + kty-content-remediate` with `MODE: RETIRE_KTY`
     - `REGENERATE_CONTENT` -> `TASK + domain-documents` with `AUTHORITY_MODE: SCA_DRIVEN`
     - `VERIFY_ONLY` -> `TASK + kty-content-remediate` with `MODE: VERIFY_KTY`
   - For `DOMAIN` amendments that require KTY-local metadata alignment after content remediation or decomposition annex changes, include a bounded `TASK + kty-metadata-align` dispatch plan. This plan must name each target KTY folder, allowed metadata write targets, mode (`REPORT_ONLY` or `ALIGN_METADATA`), expected evidence report path, and whether `_STATUS.md` append is authorized. The paired `_STATUS.md` / `_MEMORY.md` read rule applies.
   - For every affected derivative package, record whether the amendment leaves it `CURRENT`, `STALE_REBUILD_REQUIRED`, or `DEFERRED_BY_HUMAN`

7) **Derivative surface classification** (`DOMAIN`)
   - For every affected decomposition-local derivative surface, record:
     - surface path
     - classification: `DIRECT_EDIT` / `RECOMPUTE` / `NO_CHANGE`
     - upstream authority
   - Explicitly list active snapshot artifacts and handoff-state fields that must change

8) **Closure validation lane**
   - Separate the plan into:
     - direct authoritative package writes executed after checkpoint group 2,
     - downstream reruns not executed by WORKING_ITEMS,
     - closure validation steps required before the root can claim a later phase
   - Do not describe downstream reruns as already satisfied by the authoritative write pass

Produce:
- `Propagation_Plan.md`
- `Amendment_Actions.csv` — the exact action register proposed for acceptance.
  Only this file, accepted at checkpoint group 2 and bound by hash in that
  snapshot's `ACCEPTED_MANIFEST.csv`, is the authoritative register;
  `Intake_Actions.csv` remains group-1 evidence. Fill `ScopeChanging` (`YES`
  or `NO`) on every row; the human accepts it with the register. Write values
  without leading or trailing spaces. When a revised group-2 acceptance changes
  the register, bind the revised register in that acceptance's own
  `ACCEPTED_MANIFEST.csv`; the latest binding governs.

```csv
AmendmentID,ActionSeq,ActionType,EntityType,EntityID,Description,AffectedFiles,DownstreamReruns,SupersessionBindingPresent,ScopeChanging
```

**Checkpoint group 2 — exact amendment and propagation plan:** Present the
diff-style exact amendment (`Amendment_Preview.md`), `Propagation_Plan.md`, `Amendment_Actions.csv`,
write boundary, child-closure set, downstream ownership, and validation plan as
one reviewable package. The human accepts or revises the amendment and its
propagation together. This is the authority for the execution stage.

After acceptance, finalize the group-2 decision snapshot and pointer. The
execution stage must consume that accepted snapshot.

---

### Checkpoint group 3 preparation — execute, independently audit, and prepare the poststate

Resolve and consume the accepted group-2 decision snapshot before applying the
amendment and bind its path as `ACCEPTED_GROUP2_DECISION_SNAPSHOT`. Define one
`CANDIDATE_SNAPSHOT` path under `_ScopeChange/` for this poststate attempt. All
preparation, remediation, validation, review, and handoff-state evidence in
this checkpoint group uses that same candidate path. Any previously accepted
SCA remains current until checkpoint group 3 acceptance. Select exactly one
candidate pointer posture:

- `ACCEPTED_PREDECESSOR`: verify `_LATEST.md` names an accepted SCA snapshot and
  bind that path as `ACCEPTED_PREDECESSOR_SNAPSHOT`; keep the pointer unchanged.
- `FIRST_AMENDMENT`: verify `_LATEST.md` is absent and ground the candidate in
  the accepted decomposition plus `ACCEPTED_GROUP2_DECISION_SNAPSHOT`. Do not
  invent a predecessor or create `_LATEST.md` during preparation.

Before applying or dispatching work, verify that
`ACCEPTED_GROUP2_DECISION_SNAPSHOT` actually contains the accepted exact
amendment, `Amendment_Actions.csv` (or, for a historical run, the accepted
register its `ACCEPTED_MANIFEST.csv` names), `Propagation_Plan.md`, and every required
supersession input or a hash-bound reference to it. A pointer to an incomplete
decision record is not sufficient child authority; repair the group-2 snapshot
under its owning checkpoint rules before proceeding.

**Agent does:**

1) **Apply decomposition amendments**
   - Apply decomposition document amendments per the checkpoint-group-2 accepted text.
   - Record each edit action.

2) **Apply accepted propagation writes**
   - `PROJECT/SOFTWARE`:
     - `REMOVE`: apply the `[RETIRED — {AMENDMENT_ID}]` decomposition-row annotation and append the planned `_STATUS.md` history line; leave the lifecycle state unchanged and do not use `write_status.sh`
     - `MODIFY/RECLASSIFY`: update `_CONTEXT.md`; the production contract
       (`ScopeOfWork.md`) changes here only when the accepted write boundary
       names it, and otherwise its update is handed to `project-setup-retained` in
       `INCREMENTAL` mode (`scope-of-work` `MODE=REVISE`). Do not change the
       lifecycle state of an `ISSUED` or `CHECKING` deliverable in the
       candidate; an `ISSUED` deliverable is reopened only after acceptance,
       by the human, as the reopening rule in the contract states
     - `ADD`: do not scaffold in the candidate. Record the hand-back to
       `project-setup-retained` in `INCREMENTAL` mode in `Handoff_State.md`; it
       scaffolds the addition after checkpoint group 3 acceptance, against the
       accepted snapshot. An audit finding that an accepted addition has no
       folder yet is an `EXPECTED_CONSEQUENCE` of that hand-back; a
       post-acceptance examination after incremental setup is the check that
       the addition was scaffolded
     - `MERGE/SPLIT`: combine the above
     - Before any `_STATUS.md` read or update, read sibling `_MEMORY.md` / `MEMORY.md` when present as non-authoritative operational context only.
   - `DOMAIN`:
     - Update the decomposition document and all affected decomposition annex / derivative surfaces under `_Decomposition/` (Domain Ledger, Knowledge Type Register, Knowledge Subject Register, Vocabulary Map, Coverage & Telemetry, Open Issues Register, mapping tables, validation tables, telemetry derivatives, etc.)
     - Every derivative surface classified as `DIRECT_EDIT` or `RECOMPUTE` in checkpoint group 2 must be handled explicitly; contradictory or missing active derivatives are blockers, not advisory notes
     - Write amendment artifacts to `CANDIDATE_SNAPSHOT`; do not update
       `_LATEST.md` during preparation
     - Do not directly write to KTY-local folders, `_Aggregation`, hypergraph, or publication outputs. KTY-local content remediation and accepted metadata alignment are handled only through the dispatch lanes below; other derivative packages are flagged as downstream reruns.

3) **DOMAIN KTY remediation orchestration** (only when `DECOMP_VARIANT = DOMAIN` and checkpoint group 2 produced manifest rows)
   - Create or update `KTY_Remediation_Manifest.csv` in `CANDIDATE_SNAPSHOT` as the per-SCA action/evidence ledger.
   - Every child remediation brief names
     `SCA_SNAPSHOT_PATH=ACCEPTED_GROUP2_DECISION_SNAPSHOT` as its accepted
     amendment, action, and propagation authority. Send review, disposition,
     regeneration, and validation evidence to the authorized locations under
     `CANDIDATE_SNAPSHOT`. Do not supply the unaccepted candidate poststate as
     factual or overwrite authority. Supply accepted supersession inputs
     separately and record their paths and hashes in the candidate evidence.
   - For each manifest row:
     - `ARCHIVE_AND_STUB`: dispatch `TASK + kty-content-remediate` with `MODE: RETIRE_KTY` and `SCA_SNAPSHOT_PATH=ACCEPTED_GROUP2_DECISION_SNAPSHOT`.
     - `REGENERATE_CONTENT`: dispatch `TASK + domain-documents` with `AUTHORITY_MODE: SCA_DRIVEN`, `SCA_SNAPSHOT_PATH=ACCEPTED_GROUP2_DECISION_SNAPSHOT`, the accepted and hash-recorded `SUPERSESSION_MAP_PATH`, and `ALLOW_OVERWRITE_OVERRIDE: SCA_AUTHORIZED` when overwrite of active KTY files is required.
     - `VERIFY_ONLY`: dispatch `TASK + kty-content-remediate` with `MODE: VERIFY_KTY` and `SCA_SNAPSHOT_PATH=ACCEPTED_GROUP2_DECISION_SNAPSHOT`.
   - Every WORKING_ITEMS dispatch brief for a workflow that reads `_STATUS.md` must reinforce the paired-read rule: read sibling `_MEMORY.md` / `MEMORY.md` when present, treat it as non-authoritative operational context only, and record any material caveat in evidence rather than using it as authority.
   - `kty-content-remediate` emits evidence and never updates the manifest directly. `domain-documents` emits regeneration evidence and remains the only writer of active `Scoping.md` / `KA-*.md` factual content.
   - WORKING_ITEMS collects task evidence, updates manifest rows, and records `EntityType`, `EntityID`, `AffectedSubjects`, `AffectedHBK`, `CanonicalRootName`, `FacilityID`, `CONTENT_DISPOSITION_STATE`, `FACTUAL_USE_GATE`, `AUTHORITY_BASIS`, `SOURCE_ACTION_REF`, `ArchivePath`, `LAST_VERIFIED_AT`, evidence paths, and blocker notes.
   - Run the deterministic manifest validator when the tool is available:
     `python3 tools/validation/validate_kty_remediation_manifest.py --manifest {CANDIDATE_SNAPSHOT}/KTY_Remediation_Manifest.csv --amendment-actions {CANDIDATE_SNAPSHOT}/Amendment_Actions.csv`
   - Any blocking validator finding prevents `ContentRemediationState = COMPLETE` and must be reflected in `RUN_SUMMARY.md` and `Handoff_State.md`.
   - `.Archive/` scanner exclusion is mandatory: archived content must not appear in downstream allowlists, section maps, publication inputs, regeneration inputs, or factual current-content scans.

4) **DOMAIN KTY metadata alignment orchestration** (only when `DECOMP_VARIANT = DOMAIN` and checkpoint group 2 accepted metadata alignment dispatch)
   - Dispatch `TASK + kty-metadata-align` for each approved KTY metadata target.
   - Use `REPORT_ONLY` when WORKING_ITEMS needs drift evidence but does not own the metadata transition.
   - Use `ALIGN_METADATA` only when checkpoint group 2 accepted exact KTY metadata write targets in `AllowedWriteTargets`.
   - WORKING_ITEMS collects metadata-alignment evidence and updates `MetadataAlignmentState`; it does not edit KTY-local `_CONTEXT.md`, `_STATUS.md`, or `_REFERENCES.md` directly.
   - Any `_STATUS.md` read in the metadata alignment task must be paired with sibling `_MEMORY.md` / `MEMORY.md` when present as non-authoritative operational context only.

5) **Post-change validation and independent review**
   - Generate the cumulative supersession map through the deterministic accumulator whenever any prior accepted `Supersession_Map.csv` or current `Supersession_Delta.csv` must contribute to the candidate snapshot:
     `python3 tools/coordination/accumulate_supersession_map.py --prior-map {prior_snapshot}/Supersession_Map.csv --delta {CANDIDATE_SNAPSHOT}/Supersession_Delta.csv --output-map {CANDIDATE_SNAPSHOT}/Supersession_Map.csv`
   - If the current SCA introduces no new supersession delta, omit `--delta` and carry forward accepted prior map rows through the same tool. Do not hand-merge cumulative supersession CSV rows.
   - If no prior map and no current delta exist, run the same tool with `--allow-empty` to create the header-only candidate map.
   - Capture the post-change baseline using the variant's authoritative coverage source:
     - `PROJECT/SOFTWARE`: repeat the bounded coverage review and compare pre/post coverage outputs
     - `DOMAIN`: run `python3 tools/reporting/synthesize_domain_coverage_json.py --decomposition-root {CONTEXT_ROOT}/_Decomposition --scope-change-snapshot {CANDIDATE_SNAPSHOT} --output-json {CANDIDATE_SNAPSHOT}/Post_Change_Coverage.json`
   - Compare pre-change vs post-change state:
     - Confirm intended amendments occurred
     - Confirm no unintended coverage regression (unless an intentional `REMOVE`)
     - Confirm no new orphan conditions beyond those explicitly accepted by the human
     - Confirm no parent-partition / parent-entity change left orphaned child rows or dangling authoritative mappings
     - Classify every post-change audit or validator finding as either
       `EXPECTED_CONSEQUENCE`, when it stems only from a consequence the
       accepted group-2 decision deferred or excluded (cite that decision and
       item), or new. Do not repair or hide an expected consequence; handle a
       new finding on its own merits. Report both the raw `AuditState` over all
       findings (the `AuditState` field) and the `AdjustedAuditState` excluding `EXPECTED_CONSEQUENCE`
       findings, with the classification table
     - `PROJECT/SOFTWARE` specific:
       - no package change left deliverables or Scope Ledger rows parentless
       - when the originating decomposition defines package-discipline isolation, artifact-kind deliverable granularity, or equivalent design-partition rules, the changed rows still satisfy those rules and the check is recorded explicitly in the run summary
     - `DOMAIN` specific:
       - in `ACCEPTED_PREDECESSOR` posture, run `python3 tools/validation/validate_domain_decomposition_integrity.py --decomposition-root {CONTEXT_ROOT}/_Decomposition --scope-change-snapshot {CANDIDATE_SNAPSHOT} --scope-change-snapshot-mode candidate --expected-active-snapshot {ACCEPTED_PREDECESSOR_SNAPSHOT} --output-report {CANDIDATE_SNAPSHOT}/Domain_Integrity_Report.md --output-findings {CANDIDATE_SNAPSHOT}/Domain_Integrity_Findings.csv`
       - in `FIRST_AMENDMENT` posture, run the same candidate-mode command with
         `--expected-no-active-snapshot` instead of
         `--expected-active-snapshot`; `_LATEST.md` must remain absent
       - the resulting pointer check is evidence that accepted current state was
         preserved, not authority to change the pointer. Any other
         `CRITICAL` or `MAJOR` finding blocks closure until resolved or
         explicitly accepted as a non-closure state
       - the validator covers full decomposition package checks, including `UnassignedINUnits`, KTY/category and subject/KTY cardinality, coverage telemetry reconciliation, candidate artifact completeness, KTY remediation rollup consistency, and the candidate/current pointer distinction
       - any `ADD` or `MODIFY` of a `CategoryID` or `KnowledgeTypeID` (including the successor entities of `MERGE`, `SPLIT`, or `RECLASSIFY` actions) MUST pass retrieval-driven scope ratification with a `CLUSTER_COHERENT` verdict against the current V2 source index (see the Category and Knowledge Type checks in `sgttomas/chirality:workflows/domain-decomp/resources/method.md`, preserved in the private archive). The ratification register rows are appended to `CANDIDATE_SNAPSHOT`. If the source database or retrieval sidecars are stale relative to post-amendment source/audit/decomposition state, rebuild them with `tools/source_catalog/build_source_database.py` and `tools/retrieval/build_source_index.py` before ratification opens. A blocking verdict (`SCOPE_TOO_BROAD`, `SCOPE_TOO_NARROW`, or `SCOPE_REFINEMENT_NEEDED`) blocks poststate acceptance until resolved.
       - terminology changes are reflected consistently in changed sections
       - manifest evidence exists for every `ARCHIVE_AND_STUB`, `REGENERATE_CONTENT`, and `VERIFY_ONLY` row
       - no row with `FACTUAL_USE_GATE = BLOCK_FACTUAL_USE` is presented as ready for factual downstream use
       - `.Archive/` paths are excluded from downstream scanner and publication input surfaces where present
       - open issues reflect every unresolved best-effort gap

   - Dispatch a separate review instance that did not author or apply the
     candidate. It audits the complete poststate against checkpoint groups 1
     and 2, the originating decomposition invariants, write containment,
     pre/post coverage, derivative disposition, and closure claims.

6) **Produce `RUN_SUMMARY.md`**
   - Amendment ID and description
   - Actions taken (with file paths)
   - Pre-change vs post-change comparison
   - Recommended downstream reruns (not executed)
   - Explicit handoff-state fields:
     - `DecompositionTruthState`
     - `DerivativePackageState`
     - `ContentRemediationState`
     - `DownstreamRerunState`
     - `MetadataAlignmentState`
     - `AuditState`
     - `ReadyForNextPhase`
   - Repository-change evidence for the responsible current role: modified files
     plus a recommended commit message; the receiver uses applicable project
     change conventions or skill when present

7) **Produce `Handoff_State.md`**
   - Candidate amendment snapshot path and pointer posture; accepted predecessor
     snapshot path when posture is `ACCEPTED_PREDECESSOR`, otherwise the
     accepted decomposition and group-2 bases for `FIRST_AMENDMENT`
   - Authoritative truth changed in this run
   - Authoritative action register: `Amendment_Actions.csv` (or the distinct name bound in the group-2 manifest for a run whose group-1 snapshot already bound that file) as accepted in the
     group-2 snapshot (path and hash); `Intake_Actions.csv` is group-1 evidence only
   - Derivative-package state table (`package`, `owner`, `status`, `evidence`, `next required action`)
   - Active derivative-surface state table (`surface`, `classification`, `status`, `evidence`)
   - KTY remediation manifest summary (`pending`, `deferred`, `blocked`, `complete`, evidence coverage)
   - KTY metadata-alignment summary when applicable (`not required`, `report-only`, `aligned`, `blocked`, evidence coverage)
   - Candidate/current snapshot state (`candidate`, pointer posture, accepted
     predecessor or first-amendment basis, artifact completeness, and expected
     pre-acceptance pointer state)
   - Closure verdict: `CLOSED_FOR_SCOPE_CHANGE_ONLY` or `OPEN_PENDING_DERIVATIVE_CLOSURE`
   - Remaining blockers / human decisions, including each `ISSUED`
     deliverable this amendment authorizes the human to reopen once accepted
     and each `CHECKING` deliverable held for a human reversal
   - Next owning workflow(s); name `project-setup-retained` in `INCREMENTAL` mode
     wherever added, retired or modified entities need setup, and the
     post-acceptance closure examination of that setup and of any other
     implementation and downstream reruns

8) Write all artifacts to a candidate snapshot folder that is not yet active:
   - `{SCOPE_CHANGE_ROOT}/SCA-{NNN}_{YYYY-MM-DD}_{HHMM}/`

9) Do not update `_LATEST.md` before checkpoint group 3 acceptance.

Present to the human:
- Summary of what changed
- Post-change validation result, with raw and adjusted `AuditState` and each
  `EXPECTED_CONSEQUENCE` citation
- The exact acceptance-conditional edit list
- Recommended downstream reruns
- Handoff-state / closure verdict
- Repository-change evidence and exact scope for the responsible current role,
  which uses the applicable project change conventions or skill when present

**Checkpoint group 3 — audited poststate acceptance:** The human accepts or
returns the audited poststate, its closure verdict, and its explicitly open
downstream obligations. Output and snapshot writing around the accepted state
does not create an additional checkpoint.

**Acceptance-conditional edits (all variants).** The group-3 package lists
every edit that may be applied only after acceptance, exactly: file, before and
after bytes or the slot rule, and the expected resulting hash where
determinable. This includes `_LATEST.md` and any other pointer moves, status or
header lines, and acceptance-date slots. None is applied before acceptance.

After acceptance, finalize the candidate as the immutable group-3 amendment
snapshot, record the accepted decision, and apply exactly the listed
acceptance-conditional edits, including updating `_LATEST.md`. An edit not on
the list returns to the human rather than being applied. Then verify the
applied state in a new append-only postacceptance record under
`{SCOPE_CHANGE_ROOT}/_PostAcceptanceValidation/{AMENDMENT_ID}_{UTC}/`:

- all variants: compare the applied bytes or hashes with the listed edits;
- `PROJECT/SOFTWARE`: rerun the project's register validator
  against the applied state;
- `DOMAIN`: rerun the validator against the now-active snapshot in its default
  active mode (or with `--scope-change-snapshot-mode active`).

Do not overwrite the candidate validation bytes that were reviewed (for
`DOMAIN`, `Domain_Integrity_Report.md` and `Domain_Integrity_Findings.csv`).
Downstream handoff consumes that accepted snapshot. A returned candidate remains
non-current evidence and cannot become the active pointer target.

If accepted material basis changes after either earlier checkpoint, identify
the affected decisions and reopen only those parts of checkpoint group 1 or 2.
Refresh dependent pre/post evidence and the independent audit before presenting
checkpoint group 3; preserve unaffected decisions and stable identity.

---
