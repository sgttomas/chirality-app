# audit-scope-closure — method

## Method

### Pass 0 — Preconditions

1. Confirm `EXECUTION_ROOT` exists and is readable.
2. Confirm `SCOPE_CHANGE_ROOT` exists (default: `{EXECUTION_ROOT}/_ScopeChange/`).
3. Locate the amendment snapshot for the specified `AMENDMENT_ID`:
   - Path pattern: `{SCOPE_CHANGE_ROOT}/SCA-{NNN}_*/`
   - If not found: `FAILED_INPUTS` — cannot audit a scope change with no amendment record.
4. Read and parse `Amendment_Actions.csv` from the snapshot.
   - If missing or malformed: `FAILED_INPUTS`.
5. Read `RUN_SUMMARY.md` from the snapshot for downstream rerun recommendations.
6. Read `Propagation_Plan.md` from the snapshot for expected filesystem changes.
7. Verify amendment snapshot recency:
   - Determine amendment date from the snapshot's `Brief.md` or folder timestamp.
   - Record amendment recency as context. Determine rerun sufficiency from matching scope, input hashes, and successful run receipts.
   - If amendment date is in the future (clock skew):
     - Record a MAJOR finding with uncertainty recorded separately: "Amendment snapshot timestamp is in the future; cannot audit."
     - Halt with `FAILED_INPUTS`.
8. Locate the decomposition document (`DECOMPOSITION_PATH` from brief or discovered from `{EXECUTION_ROOT}/_Decomposition/`).
9. Determine `DECOMP_VARIANT` from the brief or auto-detect from folder naming conventions.
   - Valid values: `PROJECT`, `SOFTWARE`, `DOMAIN`.
   - For `DOMAIN`, Pass 4 invokes `tools/validation/validate_domain_decomposition_integrity.py` against the active decomposition package and amendment snapshot; Pass 7 adds KTY content remediation verification.

If preconditions fail, halt with `FAILED_INPUTS` and report what is missing.

---

### Pass 1 — Amendment Action Verification

For each row in `Amendment_Actions.csv`, verify the action was executed:

**ADD actions:**
- Confirm the deliverable folder exists at the expected path under the correct package.
- Confirm minimum viable fileset is present: `_STATUS.md`, `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`.
- Confirm `_STATUS.md` shows lifecycle state >= `OPEN` (TASK (workflow: preparation) ran).
- Confirm `_CONTEXT.md` header fields match the decomposition document's entry for this deliverable.

**REMOVE actions:**
- Confirm `_STATUS.md` shows `Current State: RETIRED`.
- Confirm `_STATUS.md` history contains a WORKING_ITEMS (workflow: scope-change) entry referencing the amendment ID.
- Confirm the deliverable folder still exists (non-destructive removal).
- Confirm the decomposition document's deliverable row is annotated with `[RETIRED — SCA-{NNN}]`.

**MODIFY actions:**
- Confirm `_CONTEXT.md` reflects the modified fields per the propagation plan.
- Compare each modified field against the propagation plan's before→after specification.

**RECLASSIFY actions:**
- Same as MODIFY checks.
- Check whether folder relocation was recommended and whether it occurred (advisory finding if not).

**MERGE actions:**
- Verify REMOVE checks for all source entities.
- Verify ADD checks for the combined entity.
- Check that dependencies previously targeting source entities have been re-targeted or flagged.

**SPLIT actions:**
- Verify REMOVE checks for the source entity.
- Verify ADD checks for each fragment entity.
- Check that dependencies previously targeting the source have been re-targeted or flagged.

For each action, record: `ActionSeq`, `Expected`, `Actual`, `Status` (VERIFIED / DISCREPANCY / NOT_EXECUTED).

---

### Pass 2 — Downstream Rerun Verification

From `RUN_SUMMARY.md`, extract the list of recommended downstream reruns.

For each recommended rerun:

**TASK+dependency-extract re-extraction:**
- Check whether `Dependencies.csv` exists in the affected deliverable folder.
- If it existed before the scope change, check `LastSeen` dates — a rerun should show dates on or after the amendment date.
- If no evidence of rerun: finding (MAJOR — dependencies may reference stale or phantom entities).

**TASK (workflow: preparation) runs (for ADD actions):**
- Already verified in Pass 1 (folder + minimum viable fileset existence).

**Estimation-workflow reruns:**
- Check `_Estimates/` for snapshot folders with dates on or after the amendment date that include the affected scope.
- If no post-change estimate snapshot: finding (MINOR — estimates may be stale).

**WORKING_ITEMS (workflow: project-setup) scheduling workflow reruns:**
- Check `_Schedule/` for snapshot folders with dates on or after the amendment date.
- If no post-change schedule snapshot: finding (MINOR — schedule may be stale).

For each recommended rerun, record: `Agent`, `Scope`, `Evidence of Completion`, `Status` (COMPLETED / NO_EVIDENCE / NOT_APPLICABLE).

---

### Pass 3 — Orphaned Reference Detection

Scan for references that target entities affected by REMOVE, MERGE, or RECLASSIFY actions:

1. For each RETIRED entity ID, search all `Dependencies.csv` files across the execution root for rows where `TargetDeliverableID` matches the retired ID and `Status = ACTIVE`.
   - Use: `python3 tools/coordination/analyze_dep_closure.py {EXECUTION_ROOT}` if available, or manual CSV scanning.
   - Each match is an orphaned reference (CRITICAL — active dependency targets a retired deliverable).

2. For RECLASSIFY actions where the package changed, check that ANCHOR rows (`IMPLEMENTS_NODE`) in the reclassified deliverable's `Dependencies.csv` reference the correct parent package.

3. For MODIFY actions where the deliverable name changed, check `TargetName` fields in other deliverables' `Dependencies.csv` for stale name references (MINOR — cosmetic but may cause confusion).

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

5. **Coverage check:** If pre-change and post-change `coverage_summary.json` files exist in the amendment snapshot, compare:
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
   - Lifecycle state is consistent with expectations (RETIRED for removed entities; >= OPEN for added entities).
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
| `CRITICAL` | Scope change action was not executed, or orphaned dependency targets a retired deliverable — project integrity compromised |
| `MAJOR` | Downstream rerun did not occur, or metadata is inconsistent with the amendment — work products may be stale |
| `MINOR` | Cosmetic inconsistency (stale name reference, advisory folder relocation not performed) — does not affect integrity |
| `OBSERVATION` | No action required; noted for completeness |

3. Determine overall closure status:

| Status | Condition |
|---|---|
| `CLOSED` | Zero findings of every severity; all required checks complete |
| `CLOSED_WITH_OBSERVATIONS` | All required checks complete; zero CRITICAL or MAJOR; one or more MINOR/OBSERVATION |
| `OPEN` | One or more CRITICAL or MAJOR findings remain |

4. Write all output artifacts to snapshot folder.
5. Update `_LATEST.md` pointer.
6. Return summary to WORKING_ITEMS (workflow: evaluation-protocol).

---
