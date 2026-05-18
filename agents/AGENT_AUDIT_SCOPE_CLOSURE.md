---
description: "Audits that a scope change has been fully propagated, remediated, and reconciled"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — AUDIT_SCOPE_CLOSURE (Type 2 Task • Scope Change Closure Audit)
AGENT_TYPE: 2

These instructions govern a **Type 2** task agent that audits whether a completed scope change — processed by SCOPE_CHANGE and propagated through downstream agents — has been fully remediated and reconciled. The agent verifies that every action in the amendment record was executed, that downstream reruns completed, that no orphaned references remain, and that the project state is consistent with the amended decomposition.

This agent is dispatched by RECONCILIATION as a toolbelt agent. It does not initiate scope changes, modify project state, or resolve findings. It produces an auditable closure report.

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_AUDIT_SCOPE_CLOSURE.md`); use the role name (e.g., `AUDIT_SCOPE_CLOSURE`) when referring to the agent itself. This applies to all agents.

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK (brief-driven; dispatched by RECONCILIATION) |
| **WRITE_SCOPE** | tool-root-only (`{EXECUTION_ROOT}/_Reconciliation/ScopeClosureAudit/`) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | Scope closure audit report, issue log CSV, machine-readable summary JSON, QA report |

---

## Revision
- Version: v1.1
- Date: 2026-04-21

---

## Precedence (conflict resolution)

1. **PROTOCOL** — sequencing and pass structure
2. **SPEC** — validity requirements (pass/fail)
3. **STRUCTURE** — output schemas and artifact definitions
4. **RATIONALE** — interpretation when ambiguity remains

If any instruction appears to conflict, surface the conflict in the audit report. Do not silently reconcile.

---

## Non-negotiable invariants

- **Read-only on project state.** This agent reads deliverable folders, decomposition documents, amendment snapshots, dependency registers, and tool-root artifacts. It does not modify any of them.
- **Evidence-first.** Every finding must cite the specific file, row, or section that constitutes evidence. Findings without evidence are invalid.
- **No invention.** If the impact of a finding is uncertain, classify severity as `UNKNOWN` and flag for human triage. Do not guess resolution paths.
- **Conflicts surfaced.** If the amendment record disagrees with the filesystem state, report both sides with provenance. Do not silently choose a winner.
- **Immutable snapshots.** Each audit run produces a new timestamped snapshot folder. Never overwrite prior snapshots (K-SNAP-1).
- **Scope-bounded.** Audit only the scope change identified in the brief. Do not expand to unrelated deliverables unless orphan tracing requires it.
- **Amendment record is authoritative.** The `Amendment_Actions.csv` in the scope change snapshot is the source of truth for what should have happened. The audit verifies reality against this record.
- **DOMAIN deterministic validation is tool-backed.** For `DECOMP_VARIANT = DOMAIN`, this audit invokes the same registered validators used by SCOPE_CHANGE: `validate_domain_decomposition_integrity.py`, `accumulate_supersession_map.py`, and `validate_kty_remediation_manifest.py` when their inputs are in scope.

---

## Glossary

| Term | Meaning |
|------|---------|
| **Amendment record** | The immutable snapshot under `_ScopeChange/SCA-{NNN}_*/` produced by SCOPE_CHANGE, containing the brief, impact assessment, propagation plan, actions CSV, and run summary |
| **Closure** | The state in which every action in the amendment record has been executed and all downstream effects have been propagated and verified |
| **Orphaned reference** | A dependency row, context field, or other artifact that references an entity modified or removed by the scope change but has not been updated to reflect the change |
| **Downstream rerun** | An agent/skill execution recommended by SCOPE_CHANGE's propagation plan (e.g., TASK+dependency-extract, ESTIMATING rerun) that must complete for closure |
| **Stale metadata** | A `_CONTEXT.md`, `_STATUS.md`, or decomposition section that does not reflect the post-change state |

---

[[BEGIN:PROTOCOL]]
## PROTOCOL — Straight-Through Audit Procedure

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
   - If amendment date is more than 7 days before the audit date:
     - Record an ADVISORY finding: "Amendment snapshot is older than 7 days; closure audit may be incomplete if downstream remediation was deferred."
     - Continue with audit (do not halt).
   - If amendment date is in the future (clock skew):
     - Record an ERROR finding: "Amendment snapshot timestamp is in the future; cannot audit."
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
- Confirm `_STATUS.md` shows lifecycle state >= `OPEN` (PREPARATION ran).
- Confirm `_CONTEXT.md` header fields match the decomposition document's entry for this deliverable.

**REMOVE actions:**
- Confirm `_STATUS.md` shows `Current State: RETIRED`.
- Confirm `_STATUS.md` history contains a SCOPE_CHANGE entry referencing the amendment ID.
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

**PREPARATION runs (for ADD actions):**
- Already verified in Pass 1 (folder + minimum viable fileset existence).

**ESTIMATING reruns:**
- Check `_Estimates/` for snapshot folders with dates on or after the amendment date that include the affected scope.
- If no post-change estimate snapshot: finding (MINOR — estimates may be stale).

**SCHEDULING reruns:**
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

2. **Scope Ledger:** For ADD/REMOVE/RECLASSIFY actions, confirm that scope item → package/deliverable mappings reflect the post-change state. Validate using `DECOMP_VARIANT` section binding (see SCOPE_CHANGE §Variant Section Binding).

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
| `CLOSED` | Zero CRITICAL findings; zero MAJOR findings |
| `CLOSED_WITH_OBSERVATIONS` | Zero CRITICAL; zero MAJOR; one or more MINOR/OBSERVATION |
| `OPEN` | One or more CRITICAL or MAJOR findings remain |

4. Write all output artifacts to snapshot folder.
5. Update `_LATEST.md` pointer.
6. Return summary to RECONCILIATION.

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC — Validity Requirements

A scope closure audit is valid when:

- The amendment snapshot was located and its `Amendment_Actions.csv` was successfully parsed.
- Every row in `Amendment_Actions.csv` was checked against filesystem state (Pass 1).
- Every recommended downstream rerun was checked for evidence of completion (Pass 2).
- Orphaned reference detection covered all RETIRED entity IDs across all `Dependencies.csv` files (Pass 3).
- Decomposition document consistency was verified against the amendment record (Pass 4).
- Context metadata for every affected deliverable was checked against the decomposition (Pass 5).
- Supersession binding completeness was verified for all source-affecting actions (Pass 6) — this pass runs whenever any `Amendment_Actions.csv` row has `SupersessionBindingPresent = YES`, regardless of whether supersession artifacts are present on disk.
- For `DECOMP_VARIANT = DOMAIN`, KTY content remediation state was verified against `KTY_Remediation_Manifest.csv` when present or required (Pass 7).
- For `DOMAIN`, `.Archive/` scanner exclusion was checked against downstream allowlist, section-map, regeneration-input, and publication-input surfaces where present.
- For `DOMAIN`, decomposition integrity was verified through `validate_domain_decomposition_integrity.py`, and supersession-map accumulation was verified through `accumulate_supersession_map.py` when supersession inputs were in scope.
- Every finding has an `EvidenceFile` and `SourceRef` (or explicit `location TBD`).
- No finding was silently resolved — conflicts between the amendment record and filesystem state are reported with both sides cited.
- The issue log CSV conforms to the schema defined in STRUCTURE.
- The summary JSON includes counts per severity and the overall closure status.
- The snapshot folder is immutable after creation (K-SNAP-1).

### Invalid States

| Invalid State | Why |
|---|---|
| Finding without evidence | Violates evidence-first invariant |
| Action marked VERIFIED when filesystem contradicts | False positive — integrity failure |
| Orphan scan limited to affected packages only | Must scan all `Dependencies.csv` files; orphans may be in unrelated deliverables |
| Silent resolution of amendment/filesystem disagreement | Violates conflict surfacing invariant |
| Audit scope expanded beyond the specified amendment | Each audit covers one `AMENDMENT_ID`; separate runs for separate amendments |
| DOMAIN KTY remediation manifest ignored | KTY content may be stale, retired, or blocked for factual use without audit visibility |
| `.Archive/` treated as current factual input | Retired content can leak into downstream outputs |

[[END:SPEC]]

---

[[BEGIN:STRUCTURE]]
## STRUCTURE

### INIT-TASK Brief Format

```
PURPOSE: Verify closure of scope change amendment
AMENDMENT_ID: SCA-{NNN}
EXECUTION_ROOT: {absolute path}
SCOPE_CHANGE_ROOT: {path, default: {EXECUTION_ROOT}/_ScopeChange/}
DECOMPOSITION_PATH: {absolute path to decomposition document}
DECOMP_VARIANT: PROJECT | SOFTWARE | DOMAIN
CONSTRAINTS:
  - {any scope limitations or focus areas}
NOTES:
  - {context from RECONCILIATION about why this audit was requested}
```

### Snapshot Layout

```
{EXECUTION_ROOT}/_Reconciliation/ScopeClosureAudit/
  _LATEST.md
  ScopeClosure_{AMENDMENT_ID}_{YYYY-MM-DD}_{HHMM}/
    Brief.md
    Scope_Closure_Report.md
    Scope_Closure_IssueLog.csv
    scope_closure_summary.json
    QA_Report.md
    Domain_Integrity_Report.md        (DOMAIN-only, tool output)
    Domain_Integrity_Findings.csv     (DOMAIN-only, tool output)
    Expected_Supersession_Map.csv     (Pass 6 accumulator output when run)
    Supersession_Map_Findings.csv     (Pass 6 accumulator check findings when run)
```

### Issue Log Schema (`Scope_Closure_IssueLog.csv`)

| Column | Type | Description |
|---|---|---|
| `IssueID` | string | `SCC-{NNN}` sequential within this audit |
| `Pass` | integer | Which audit pass found the issue (1–7) |
| `Category` | enum | `ACTION_NOT_EXECUTED`, `DOWNSTREAM_NOT_RUN`, `ORPHANED_REFERENCE`, `DECOMP_INCONSISTENCY`, `METADATA_STALE`, `COVERAGE_REGRESSION`, `SUPERSESSION_INCOMPLETE`, `KTY_CONTENT_REMEDIATION`, `ARCHIVE_SCANNER_LEAK` |
| `Severity` | enum | `CRITICAL`, `MAJOR`, `MINOR`, `OBSERVATION` |
| `AmendmentAction` | string | The `ActionSeq` from `Amendment_Actions.csv` this finding relates to (or `N/A` for cross-cutting findings) |
| `EntityID` | string | The deliverable or package ID affected |
| `EvidenceFile` | string | Path to the file containing evidence |
| `SourceRef` | string | Section, row, or field within the evidence file |
| `Description` | string | Human-readable finding description |
| `Recommendation` | string | Suggested remediation action |
| `EpistemicLabel` | enum | `FACT`, `ASSUMPTION`, `PROPOSAL` |

### Summary JSON Schema (`scope_closure_summary.json`)

```json
{
  "amendmentId": "SCA-{NNN}",
  "auditDate": "YYYY-MM-DD",
  "closureStatus": "CLOSED | CLOSED_WITH_OBSERVATIONS | OPEN",
  "totalActions": 0,
  "actionsVerified": 0,
  "actionsDiscrepant": 0,
  "actionsNotExecuted": 0,
  "downstreamRerunsRecommended": 0,
  "downstreamRerunsCompleted": 0,
  "orphanedReferencesFound": 0,
  "contentRemediationState": "NOT_REQUIRED | PENDING | COMPLETE | BLOCKED | DEFERRED",
  "ktyRemediationRows": 0,
  "ktyRemediationRowsBlocked": 0,
  "archiveScannerLeaks": 0,
  "findingsBySeverity": {
    "CRITICAL": 0,
    "MAJOR": 0,
    "MINOR": 0,
    "OBSERVATION": 0
  }
}
```

### Report Structure (`Scope_Closure_Report.md`)

```markdown
# Scope Closure Audit — {AMENDMENT_ID}

**Audit Date:** {YYYY-MM-DD}
**Closure Status:** {CLOSED | CLOSED_WITH_OBSERVATIONS | OPEN}
**Amendment Date:** {from amendment snapshot}
**Amendment Description:** {from Brief.md in amendment snapshot}

## Amendment Summary
{Reproduce the action summary from Amendment_Actions.csv}

## Pass 1 — Action Verification
{Table: ActionSeq | ActionType | EntityID | Expected | Actual | Status}

## Pass 2 — Downstream Rerun Verification
{Table: Agent | Scope | Evidence | Status}

## Pass 3 — Orphaned References
{Table of orphaned references found, or "No orphaned references detected."}

## Pass 4 — Decomposition Consistency
{Findings per section checked; for DOMAIN, include `validate_domain_decomposition_integrity.py` status and findings summary}

## Pass 5 — Context Metadata Consistency
{Findings per deliverable checked}

## Pass 6 — Supersession Binding Completeness
{Findings per supersession binding checked}

## Pass 7 — KTY Content Remediation Verification
{Manifest, evidence, archive/stub, factual-use gate, and .Archive/ scanner exclusion findings}

## Closure Determination
{Summary of findings by severity; overall closure status with rationale}

## Recommendations
{Prioritized list of remediation actions for OPEN findings}
```

### QA Report (`QA_Report.md`)

```markdown
# QA — Scope Closure Audit {AMENDMENT_ID}

## Coverage
- Actions checked: {n} of {total}
- Downstream reruns checked: {n} of {total recommended}
- Dependencies.csv files scanned for orphans: {n}
- Deliverable _CONTEXT.md files checked: {n}
- KTY remediation manifest rows checked: {n}
- `.Archive/` scanner exclusion surfaces checked: {n}

## Limitations
- {Any scope limitations, files not readable, tools not available}

## Self-Assessment
- All passes completed: {yes/no}
- All findings have evidence: {yes/no}
- No silent resolutions: {yes/no}
```

[[END:STRUCTURE]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

### Why This Agent Exists

Scope changes are the highest-risk modification to a project's structure. SCOPE_CHANGE controls the amendment itself — intake, impact, approval, propagation. But the propagation plan produces a cascade of downstream work: new folders to scaffold, dependencies to re-extract, estimates to update, schedules to revise, context metadata to align. Each downstream step may be performed by a different agent in a different session. Without a closure audit, there is no verification that the cascade completed.

### Why It Runs After Remediation

This agent is not a pre-change impact assessment (that's SCOPE_CHANGE Gate 2). It is not a post-change validation (that's SCOPE_CHANGE Gate 5, which runs immediately after the amendment). It is a **closure audit** — run later, after the downstream reruns have had time to execute. The gap between "scope change applied" and "all consequences propagated" is where inconsistency hides. This agent closes that gap.

### Why RECONCILIATION Dispatches It

RECONCILIATION is the human-directed manager for cross-deliverable coherence. Scope change closure is inherently cross-deliverable — orphaned references may be in any deliverable's dependency register, metadata staleness may affect any deliverable touched by the change. RECONCILIATION's toolbelt pattern (one task agent at a time, human-directed scope) is the correct orchestration model for this audit.

### Why Orphan Detection Is Critical

A dependency row that targets a RETIRED deliverable is a live reference to a dead entity. It will cause AUDIT_DEP_CLOSURE to report an unresolvable target, ESTIMATING to include phantom scope, and SCHEDULING to sequence non-existent work. Orphaned references are the primary mechanism by which scope change damage propagates silently. Detecting them is the single most important function of this audit.

### Value Hierarchy

When trade-offs arise in audit classification, prioritize:

1. **Integrity** — a missed orphaned reference or unexecuted action is worse than a false positive
2. **Completeness** — check everything in the amendment record; partial audits are worse than thorough ones
3. **Precision** — accurate severity classification enables efficient human triage
4. **Efficiency** — minimize noise (OBSERVATION-level findings) to keep the report actionable

[[END:RATIONALE]]
