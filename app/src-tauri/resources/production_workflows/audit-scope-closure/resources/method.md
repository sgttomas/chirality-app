# audit-scope-closure — method

This retained resource applies to DOMAIN and explicitly adopted legacy
phase/control-file projects. Current PROJECT/SOFTWARE amendment closure uses
[current-project.md](current-project.md). Its actual decision and locality
bindings replace the snapshot/control-file assumptions below for that use.

## Method

### Pass 0 — Preconditions

1. Confirm `EXECUTION_ROOT` exists and is readable.
2. Confirm `SCOPE_CHANGE_ROOT` exists (default: `{EXECUTION_ROOT}/_ScopeChange/`).
3. Locate the amendment snapshot for the specified `AMENDMENT_ID`:
   - Path pattern: `{SCOPE_CHANGE_ROOT}/{AMENDMENT_ID}_*/`, where `AMENDMENT_ID` is `SCA-{NNN}` or a project-qualified form such as `SCA-APP-{NNN}`. Match the full ID followed by `_`, so `SCA-001` never matches `SCA-APP-001`.
   - If not found: `FAILED_INPUTS` — cannot audit a scope change with no amendment record.
4. Resolve and parse the accepted action register:
   - Resolve the accepted checkpoint-group-2 decision snapshot (the amendment-qualified pointer `{SCOPE_CHANGE_ROOT}/{AMENDMENT_ID}_GROUP-2_AUTHORIZED.md`, or the latest `checkpoint_snapshots/{AMENDMENT_ID}_GROUP-2_*/` folder it names). Use the action register bound in its `ACCEPTED_MANIFEST.csv` and verify the recorded SHA-256.
   - Current runs bind `Amendment_Actions.csv`. A historical run may bind another name (for example `Amendment_Actions_CP2.csv`); use the bound file and record its name. `Intake_Actions.csv` holds group-1 `PROPOSED` rows and is never the register.
   - The register is the single manifest row whose path basename matches `Amendment_Actions*.csv`; none or more than one is `FAILED_INPUTS`.
   - Fallback only for an amendment with no `checkpoint_snapshots/{AMENDMENT_ID}_GROUP-*` folder (for example a gate-era run): use `Amendment_Actions.csv` in the amendment snapshot and record the fallback as an OBSERVATION. A run with a group-1 snapshot but no group-2 snapshot is `FAILED_INPUTS`.
   - If the bound register is missing, malformed or hash-mismatched: `FAILED_INPUTS`.
   - Later passes use this resolved register wherever this method names `Amendment_Actions.csv`.
5. Read `RUN_SUMMARY.md` from the snapshot for downstream rerun recommendations.
6. Read `Propagation_Plan.md` from the snapshot for expected filesystem changes.
7. Read `Handoff_State.md` from the snapshot and every later handoff record for this amendment: later checkpoint-snapshot `Handoff_State.md` files, `_PostAcceptanceValidation/{AMENDMENT_ID}_*/` records, and closeout or effective-state records under `{SCOPE_CHANGE_ROOT}`. Take each obligation's current disposition from the latest applicable record, including human deferrals and optional derivatives recorded as not activated, and cite the deciding record.
8. Verify amendment snapshot recency:
   - Determine amendment date from the snapshot's `Brief.md` or folder timestamp.
   - Record amendment recency as context only. Determine sufficiency from the actual declaration/source assessment or the derivative workflow's matching scope and input basis (see Pass 2), never from dates alone.
   - If amendment date is in the future (clock skew):
     - Record a MAJOR finding with uncertainty recorded separately: "Amendment snapshot timestamp is in the future; cannot audit."
     - Halt with `FAILED_INPUTS`.
9. Locate the decomposition document (`DECOMPOSITION_PATH` from brief or discovered from `{EXECUTION_ROOT}/_Decomposition/`).
10. Determine `DECOMP_VARIANT` from the brief or auto-detect from folder naming conventions.
    - Valid values: `PROJECT`, `SOFTWARE`, `DOMAIN`.
    - For `DOMAIN`, Pass 4 invokes `tools/validation/validate_domain_decomposition_integrity.py` against the active decomposition package and amendment snapshot; Pass 7 adds KTY content remediation verification.

The native-needs clauses below apply only to `PROJECT`/`SOFTWARE` DEL identities.
For `DOMAIN`, check the existing non-dependency metadata and the accepted
amendment, decomposition, supersession and KTY remediation obligations. Do not
require KTY `deliverable.yaml`, dispatch DEL-native dependency authoring for a
KTY, or substitute a dependency CSV/Markdown route. If a handoff names an
unsupported KTY dependency task, report that limitation without declaring the
obligation completed or inventing a persistence format.

If preconditions fail, halt with `FAILED_INPUTS` and report what is missing.

**Input manifest and rerun of this audit.** Write `INPUT_MANIFEST.sha256` in the
audit snapshot, listing the SHA-256 of every input read (register, handoff
records, decomposition, affected metadata, local dependency declarations and tool
outputs). A prior audit snapshot remains sufficient only while its
`INPUT_MANIFEST.sha256` still matches the current inputs; its date does not
decide this. A prior snapshot without an input manifest cannot establish that
its inputs are current, so rerun the audit.

**Superseding snapshot.** To correct or refresh a published audit snapshot,
write a new snapshot; never edit the earlier one. The new snapshot records in
its report (or a `SUPERSESSION_NOTE.md`) the superseded snapshot path, the
reason, and what changed in inputs or evidence binding. Then update
`_LATEST.md` to the new snapshot. The earlier bytes remain historical evidence.

---

### Pass 1 — Amendment Action Verification

For each row in `Amendment_Actions.csv`, verify the action was executed:

**ADD actions:**
- Confirm the deliverable folder exists at the expected path under the correct package.
- Confirm the four non-dependency metadata files are present: `_STATUS.md`, `_CONTEXT.md`, `_REFERENCES.md` and `_SEMANTIC.md`.
- For `PROJECT`/`SOFTWARE` DEL identities only, also confirm `deliverable.yaml` and verify its identity against the accepted deliverable binding. An empty `needs` list is not evidence that dependency assessment is complete. No YAML declaration is required for a `DOMAIN` KTY.
- Confirm `_STATUS.md` shows lifecycle state >= `OPEN` (the `preparation` skill ran).
- Confirm `_CONTEXT.md` header fields match the decomposition document's entry for this deliverable.

**REMOVE actions:**
- Confirm the decomposition document's deliverable row is annotated with `[RETIRED — {AMENDMENT_ID}]`.
- Confirm `_STATUS.md` history contains an appended line recording the retirement under the amendment ID.
- Confirm the retirement left the lifecycle state unchanged: RETIRED is not a project lifecycle value (`docs/COMPATIBILITY_FORMATS.md#historical-specification` §3.2 lists no such state, and its historical-product extension says RETIRED is never an active project lifecycle value). If a historical run's accepted group-2 decision explicitly authorized a hand-authored `RETIRED` current state, verify against that decision and cite it rather than reporting a discrepancy.
- Confirm the deliverable folder still exists (non-destructive removal).

**MODIFY actions:**
- Confirm `_CONTEXT.md` reflects the modified fields per the propagation plan.
- Compare each modified field against the propagation plan's before→after specification.

**RECLASSIFY actions:**
- Same as MODIFY checks.
- Check whether folder relocation was recommended and whether it occurred (advisory finding if not).

**MERGE actions:**
- Verify REMOVE checks for all source entities.
- Verify ADD checks for the combined entity.
- For `PROJECT`/`SOFTWARE` DEL identities, check that needs referencing source entities were assessed against the accepted change and their actual conditions; do not assume retargeting is required.

**SPLIT actions:**
- Verify REMOVE checks for the source entity.
- Verify ADD checks for each fragment entity.
- For `PROJECT`/`SOFTWARE` DEL identities, check that needs referencing the source were assessed against the accepted change and their actual conditions; do not assume retargeting is required.

For each action, record: `ActionSeq`, `Expected`, `Actual`, `Status`, `Evidence`. Status values:

- `VERIFIED` — current state matches the action.
- `DISCREPANCY` — current state contradicts the action.
- `NOT_EXECUTED` — no evidence the action was applied and no recorded decision explains it.
- `DEFERRED_BY_HUMAN` — the action's application was deferred by a recorded human decision (cite the decision record and item). It is reported as an OBSERVATION and listed as open work; it is not counted as CRITICAL or MAJOR and not reported as done.
- `SUPERSEDED_BY:<ref>` — the action was applied or accepted, then superseded by a later accepted decision or amendment `<ref>`. Required evidence: the superseding accepted record, evidence that the action was applied or accepted before supersession (or that the superseding record withdrew it), and a check that current state matches the superseding record. Without that evidence, use `DISCREPANCY` or `NOT_EXECUTED`.

---

### Pass 2 — Downstream Rerun Verification

From `RUN_SUMMARY.md`, extract the list of recommended downstream reruns.

For each recommended rerun:

For derivative workflows that require run snapshots, a rerun is sufficient when its recorded input basis (an `INPUT_MANIFEST.sha256` or equivalent hash-bearing evidence) includes the accepted post-change hashes of the amended inputs and its scope covers the affected entities. Local dependency authoring is verified from the actual declarations and sources as specified below; it requires no separate extraction receipt. Dates are context only and do not establish sufficient assessment.

Before judging a rerun missing, apply the current disposition from the handoff records read in Pass 0. A rerun deferred by a recorded human decision is `DEFERRED_BY_HUMAN`; an optional derivative the accepted records leave unactivated is `NOT_ACTIVATED`. Cite the decision; report either as an OBSERVATION and list it as open work, not as MAJOR or MINOR.

**Local dependency authoring/refresh (`dependency-extract`; PROJECT/SOFTWARE DEL only):**
- Inspect the affected consumers' current `deliverable.yaml` declarations
  against the accepted action, amended scope/design and actual source
  conditions. Check the resulting changes and unchanged declarations that
  were reviewed; do not require an extraction receipt or timestamp refresh.
- Verify that each required semantic change is present and supported, with
  case, use, `when`, `gating`, unknown sources and outward obligations
  preserved. No wording rediscovery or endpoint-only match justifies deleting
  or merging a need.
- If a required assessment or correction is missing and no recorded deferral
  applies, report its actual consequence and evidence. Use MAJOR when the
  missing work may leave materially stale or unsupported dependency meaning.
  Presence of YAML alone is not completion evidence.

**`preparation` skill runs (for ADD actions):**
- Already verified in Pass 1 (folder + minimum viable fileset existence).

**Estimation-workflow reruns:**
- Check `_Estimates/` for a snapshot whose input manifest binds the affected scope at its post-change hashes.
- If no such post-change estimate snapshot and no recorded deferral: finding (MINOR — estimates may be stale).

**WORKING_ITEMS (workflow: project-setup-retained) scheduling workflow reruns:**
- Check `_Schedule/` for a snapshot whose input manifest binds the post-change basis.
- If no such post-change schedule snapshot and no recorded deferral: finding (MINOR — schedule may be stale).

For each recommended rerun, record: `Agent`, `Scope`, `Evidence of Completion`, `Status` (COMPLETED / NO_EVIDENCE / NOT_APPLICABLE / DEFERRED_BY_HUMAN / NOT_ACTIVATED / SUPERSEDED_BY:<ref>), with the deciding record for the last three.

---

### Pass 3 — Affected Reference Assessment

The native-needs assessment in this pass is for `PROJECT`/`SOFTWARE` DEL
identities only. Record it as `NOT_APPLICABLE` for `DOMAIN`; this does not skip
the DOMAIN amendment, context, decomposition, supersession or remediation
checks in the other passes.

1. Locate needs affected by REMOVE, MERGE, SPLIT, MODIFY or RECLASSIFY from
   all consumer-local `deliverable.yaml` files in the execution root.
   Query `tools.deliverables neighborhood` and `impact` for affected native
   IDs where available, then inspect each relevant source declaration. See
   `tools/deliverables/README.md` and `construct-local-work-graph`. The CLI
   requires the project root in a Git repository with HEAD and reads all
   project declarations/path-presence references. Use it only within the
   authorized read scope; bounded direct inspection is the fallback. Native-only cycle reporting does not cover
   external/unknown relations or establish input suitability.

2. Compare each affected need with the accepted change and the actual
   artifact needed for its stated condition, use, case and trigger. Retirement
   of production scope does not automatically make an existing artifact
   unusable. Preserve a supported historical input where its condition still
   holds; cite the evidence and accepted change. Report an unresolved binding
   or unfulfilled condition with its actual consequence and uncertainty.
   Never retarget, delete or fail a need merely because its producer retired.

3. For reclassification, verify the accepted identity/parent binding from
   decomposition and locality sources; do not manufacture engineering needs
   to represent tree membership. A label change warrants correction only
   where it makes the actual reference misleading or ambiguous.

4. Preserve distinct same-endpoint needs, `when`, `gating`, external inputs,
   unknown sources and outward downstream obligations. Reciprocal needs are
   observations for assessment, not automatic non-gating or closure cases.
   A structurally valid query is not a satisfaction or readiness verdict.

---

### Pass 4 — Decomposition Consistency

Verify that the decomposition document's current state is consistent with the amendment:

For `DECOMP_VARIANT = DOMAIN`, run the registered DOMAIN integrity validator and incorporate its findings into this pass:

```bash
python3 tools/validation/validate_domain_decomposition_integrity.py \
  --decomposition-root {EXECUTION_ROOT}/_Decomposition \
  --scope-change-snapshot {AMENDMENT_SNAPSHOT} \
  --output-report {AUDIT_SNAPSHOT}/Domain_Integrity_Report.md \
  --output-findings {AUDIT_SNAPSHOT}/Domain_Integrity_Findings.csv
```

Treat `CRITICAL` and `MAJOR` validator findings as blocking decomposition-consistency findings. The tool covers DOMAIN annex referential integrity, KTY/category and subject/KTY cardinality, objective reconciliation, coverage telemetry reconciliation, active snapshot artifact completeness, `_LATEST.md` parity, and KTY remediation rollup consistency. Do not restate those checks as independent inline audit logic.

1. **Change Log:** Confirm the amendment entry exists with the correct `AMENDMENT_ID`, date, and description.

2. **Scope Ledger:** For ADD/REMOVE/RECLASSIFY actions, confirm that scope item → package/deliverable mappings reflect the post-change state. Validate using `DECOMP_VARIANT` section binding (see WORKING_ITEMS (workflow: scope-change) §Variant Section Binding).

3. **Packages section:** For ADD/REMOVE package actions, confirm rows are present or annotated as RETIRED.

4. **Deliverables section:** For all actions, confirm rows reflect the post-change state.

5. **Coverage check:** If `Pre_Change_Coverage.json` and `Post_Change_Coverage.json` exist in the amendment snapshot (a historical run may instead cite pre- and post-change audit `coverage_summary.json` outputs), compare:
   - Forward coverage should not have regressed (unless intentional REMOVE).
   - No new unassigned scope items (unless from ADD not yet fully propagated).

---

### Pass 5 — Context Metadata Consistency

For every deliverable affected by the scope change (listed in `Amendment_Actions.csv`):

1. Read `_CONTEXT.md` and verify:
   - `Name` matches the decomposition document's entry.
   - `Package` matches the decomposition document's entry.
   - `Discipline`, `Type`, `Responsible` match (if these were modified by the amendment).
   - `Decomposition Reference` points to the correct decomposition document.
   - `Scope Traceability` section lists the correct SOW-IDs and OBJ-IDs per the Scope Ledger.

2. Read `_STATUS.md` and verify:
   - Lifecycle state is consistent with expectations (unchanged by retirement for removed entities, which carry the retirement history line instead, unless an accepted decision recorded otherwise; >= OPEN for added entities).
   - History section contains entries consistent with the scope change timeline.

---

### Pass 6 — Supersession Binding Completeness

This pass runs whenever any row in `Amendment_Actions.csv` has `SupersessionBindingPresent = YES`. If supersession files (`Supersession_Delta.csv` and `Supersession_Map.csv`) are missing when `SupersessionBindingPresent = YES` actions exist, emit a CRITICAL finding: "Required supersession artifacts are missing despite source-affecting actions." Do not skip this pass when files are absent — absence is the failure this pass must catch.

1. For every row in `Amendment_Actions.csv` where `SupersessionBindingPresent = YES`, derive the expected supersession decision identifier as `D-{ActionSeq}` (zero-padded to match the action's sequence formatting) and verify that at least one corresponding row exists in `Supersession_Delta.csv` with the same `AmendmentID` and derived `DecisionID`. For decision-log-only bindings with no formal amendment action, accept `DL-{reference}` rows as the valid producer-side convention.
2. For every row in `Supersession_Delta.csv`, verify that `SupersededAuthorityPath` resolves to an existing admitted authority file.
3. For every `SUPERSESSION` row, verify that `SupersededAuthorityRef` is non-empty — the binding must point to a specific source location (section, line, table, or cell reference), not just a file.
4. Verify cumulative map accumulation by invoking the registered accumulator in check mode:
   `python3 tools/coordination/accumulate_supersession_map.py --prior-map {prior_snapshot}/Supersession_Map.csv --delta {AMENDMENT_SNAPSHOT}/Supersession_Delta.csv --output-map {AUDIT_SNAPSHOT}/Expected_Supersession_Map.csv --check-map {AMENDMENT_SNAPSHOT}/Supersession_Map.csv --output-findings {AUDIT_SNAPSHOT}/Supersession_Map_Findings.csv`
   - Omit `--delta` when the audited SCA introduces no delta.
   - Use `--allow-empty` when no prior map and no current delta exist.
   - If the prior accepted snapshot's `Supersession_Map.csv` is missing but prior accepted maps or deltas exist, reconstruct the expected prior map by replaying the accepted chain through the same accumulator from the latest available accepted map into the audit snapshot (for example `Reconstructed_{PRIOR_ID}_Backfill.csv`), record every source path and hash, and report the reconstruction as an OBSERVATION. If the chain cannot be reconstructed from accepted records, emit a MAJOR finding with `Assessment: UNKNOWN`; never hand-author the missing map.
   - Incorporate `MISSING_EXPECTED_ROW` and `UNEXPECTED_ROW` findings into this pass.
5. Verify that surviving rows use canonical applicability fields: canonical root names in `AppliesToRoots`, canonical facility IDs in `AppliesToFacilities`, and either explicit section IDs or an intentionally blank `AppliesToSections` field indicating global scope.

Finding severities:
- `CRITICAL`: An action claims `SupersessionBindingPresent = YES` but has no matching supersession row.
- `MAJOR`: A supersession row has an empty or unresolvable `SupersededAuthorityPath` or `SupersededAuthorityRef`, or uses invalid applicability tokens in `AppliesToRoots` / `AppliesToFacilities`.
- `MINOR`: A `SUPPLEMENTARY_EXTENSION` row lacks a `SupersededAuthorityRef` (less critical since it does not override).

A scope-change snapshot should not be considered publication-ready (`PUBLICATION_GATED` in the `ReadyForNextPhase` field) if it contains source-affecting decisions with incomplete supersession bindings.

---

### Pass 7 — KTY Content Remediation Verification

This pass runs when `DECOMP_VARIANT = DOMAIN` or when the amendment snapshot
contains `KTY_Remediation_Manifest.csv`.

1. Confirm manifest handling:
   - If the amendment affects KTY-local content, verify
     `KTY_Remediation_Manifest.csv` exists in the amendment snapshot.
   - If no manifest exists and no KTY-local content impact is recorded, mark
     this pass `NOT_APPLICABLE`.
   - If a manifest is required but missing, emit a CRITICAL finding.

2. Validate manifest schema and dispositions:
   - If `tools/validation/validate_kty_remediation_manifest.py` is available,
     run it against the manifest and `Amendment_Actions.csv`; incorporate its
     blocking findings into this pass.
   - Required fields include `EntityType`, `EntityID`, `KTYID`, `KTYPath`,
     `CONTENT_DISPOSITION_STATE`, `FACTUAL_USE_GATE`, `AUTHORITY_BASIS`,
     `SOURCE_ACTION_REF`, and `LAST_VERIFIED_AT`.
   - Informational fields `AffectedSubjects`, `AffectedHBK`,
     `CanonicalRootName`, and `FacilityID` must be present; blanks are valid
     only when the field is not applicable or the root/facility scope is
     unambiguous.
   - `CONTENT_DISPOSITION_STATE` must be one of `PENDING`,
     `ARCHIVED_STUBBED`, `REGENERATED`, `VERIFIED`, `DEFERRED`, `BLOCKED`, or
     `NOT_REQUIRED`.
   - `PENDING` rows are CRITICAL.
   - `DEFERRED` rows must include substantive blocker notes and cap factual
     readiness at regeneration-only.
   - `BLOCKED` rows must include evidence-backed blocker notes and cap factual
     readiness at no next phase.

3. Verify evidence paths:
   - Every `ARCHIVE_AND_STUB`, `REGENERATE_CONTENT`, and `VERIFY_ONLY` row must
     have resolvable evidence paths or explicit `location TBD` with blocker
     notes.
   - `ARCHIVE_AND_STUB` rows must have a non-empty, resolvable `ArchivePath`
     or explicit blocker notes.
   - `ARCHIVE_AND_STUB` rows must cite `kty-content-remediate` evidence.
   - `REGENERATE_CONTENT` rows must cite `domain-documents` evidence with
     `AUTHORITY_MODE: SCA_DRIVEN`.
   - `VERIFY_ONLY` rows must cite `kty-content-remediate` verification
     evidence.

4. Verify archive/stub completeness for `ARCHIVE_AND_STUB` rows:
   - Archived copies exist under the row's `ArchivePath`.
   - Root-level retired `Scoping.md` / `KA-*.md` paths, when listed, begin with
     `[RETIRED]` tombstone stubs.
   - Tombstone stubs cite the amendment id, source action reference, and
     archive path.
   - `.Archive/` content is not treated as current factual authority.

5. Verify factual-use gate consistency:
   - `FACTUAL_USE_GATE = ALLOW_FACTUAL_USE` requires regenerated or verified
     evidence and no unresolved blockers.
   - `FACTUAL_USE_GATE = REGEN_ONLY` is inconsistent with
     `ReadyForNextPhase = PHASE7_REVIEW` or `PUBLICATION_GATED`.
   - `FACTUAL_USE_GATE = BLOCK_FACTUAL_USE` is inconsistent with any closure
     claim that permits factual downstream use.
   - `FACTUAL_USE_GATE = RETIRED_NO_FACTUAL_USE` requires archived/tombstoned
     or otherwise retired evidence.

6. Verify `.Archive/` scanner exclusion:
   - Inspect downstream allowlist, section-map, regeneration-input, and
     publication-input files named in the snapshot where present.
   - Emit a MAJOR finding if any such current-input surface includes `.Archive/`
     as factual input.
   - Emit an OBSERVATION if no downstream input surfaces are present to inspect.

### Pass 8 — Synthesis and Output

1. Compile all findings from Passes 1–7.

2. Classify each finding by severity:

| Severity | Meaning |
|---|---|
| `CRITICAL` | Scope change action was not executed, or an affected reference demonstrably compromises project integrity; retirement alone does not establish this consequence |
| `MAJOR` | Downstream rerun did not occur, or metadata is inconsistent with the amendment — work products may be stale (a `DEFERRED_BY_HUMAN` or `NOT_ACTIVATED` item citing its decision is not MAJOR) |
| `MINOR` | Cosmetic inconsistency (stale name reference, advisory folder relocation not performed) — does not affect integrity |
| `OBSERVATION` | No action required in this audit; noted for completeness, including `DEFERRED_BY_HUMAN`, `NOT_ACTIVATED` and evidenced `SUPERSEDED_BY:<ref>` items |

3. Determine overall closure status:

| Status | Condition |
|---|---|
| `CLOSED` | Zero findings of every severity; all required checks complete |
| `CLOSED_WITH_OBSERVATIONS` | All required checks complete; zero CRITICAL or MAJOR; one or more MINOR/OBSERVATION |
| `OPEN` | One or more CRITICAL or MAJOR findings remain |
| `FAILED_INPUTS` | Pass 0 preconditions failed; no closure determination was made |

`CLOSED` and `CLOSED_WITH_OBSERVATIONS` do not claim that deferred or
not-activated obligations are complete; the report lists them as open work with
their deciding records.

4. Write all output artifacts to snapshot folder.
5. Update `_LATEST.md` pointer.
6. Return the summary to its caller.

---
