# audit-scope-closure — contract

This retained resource applies to DOMAIN and explicitly adopted legacy
phase/control-file projects. Current PROJECT/SOFTWARE amendment closure uses
[current-project.md](current-project.md). Its actual decision and locality
bindings replace the snapshot/control-file assumptions below for that use.

## Non-negotiable invariants

- **Read-only on project state.** This agent reads deliverable folders, decomposition documents, amendment snapshots, local dependency declarations, and tool-root artifacts. It does not modify any of them.
- **Evidence-first.** Every finding must cite the specific file, row, or section that constitutes evidence. Findings without evidence are invalid.
- **No invention.** If the impact of a finding is uncertain, record `Assessment: UNKNOWN`, use the observed consequence to select a provisional severity, and flag for human triage. Do not guess resolution paths.
- **Conflicts surfaced.** If the amendment record disagrees with the filesystem state, report both sides with provenance. Do not silently choose a winner.
- **Immutable snapshots.** Each audit run produces a new timestamped snapshot folder. Never overwrite prior snapshots ([K-SNAP-1 (historical)](https://github.com/sgttomas/chirality/blob/archive/pre-docs-cleanup-1/docs/CONTRACT.md)).
- **Scope-bounded.** Audit only the scope change identified in the brief. Do not expand to unrelated deliverables unless tracing affected references requires it.
- **Amendment record is authoritative.** The accepted action register is the source of truth for what should have happened: the register bound by hash in the accepted checkpoint-group-2 snapshot's `ACCEPTED_MANIFEST.csv` (currently `Amendment_Actions.csv`; historical runs may bind another name such as `Amendment_Actions_CP2.csv`). A run with no group-2 checkpoint snapshot falls back to `Amendment_Actions.csv` in the amendment snapshot, recorded as a fallback. `Intake_Actions.csv` is group-1 proposal evidence, never the register. Later accepted handoff records supply each obligation's current disposition. The audit verifies reality against this record.
- **DOMAIN deterministic validation is tool-backed.** For `DECOMP_VARIANT = DOMAIN`, this audit invokes the same registered validators used by WORKING_ITEMS (workflow: scope-change): `validate_domain_decomposition_integrity.py`, `accumulate_supersession_map.py`, and `validate_kty_remediation_manifest.py` when their inputs are in scope.
- **Native needs are DEL-only.** YAML dependency-file requirements, local need authoring checks and native affected-reference coverage apply only to `PROJECT`/`SOFTWARE` DEL identities. For `DOMAIN`, retain its non-dependency metadata and other applicable checks; do not require KTY YAML or add an alternate dependency route.

---

## Glossary

| Term | Meaning |
|------|---------|
| **Amendment record** | The immutable snapshot under `_ScopeChange/{AMENDMENT_ID}_*/` produced by WORKING_ITEMS (workflow: scope-change), containing the brief, impact assessment, propagation plan, actions CSV, handoff state and run summary, together with its accepted checkpoint snapshots and later handoff records. `AMENDMENT_ID` is `SCA-{NNN}` or a project-qualified form such as `SCA-APP-{NNN}` |
| **Closure** | The state in which every action in the amendment record has been executed and all downstream effects have been propagated and verified |
| **Affected reference** | A local need, context field or artifact whose meaning may be affected by the accepted change. It is orphaned only where its actual binding or required condition is unsupported; retirement alone does not establish this |
| **Downstream rerun** | An agent/workflow execution recommended by WORKING_ITEMS (workflow: scope-change)'s propagation plan (e.g., TASK+dependency-extract or a TASK estimation workflow rerun) that must complete for closure |
| **Stale metadata** | A `_CONTEXT.md`, `_STATUS.md`, or decomposition section that does not reflect the post-change state |

---

## Validity

A scope closure audit is valid when:

- The amendment snapshot was located and its accepted action register was resolved, hash-checked where bound, and parsed.
- `Handoff_State.md` and later handoff records for the amendment were read, and every `DEFERRED_BY_HUMAN`, `NOT_ACTIVATED` or `SUPERSEDED_BY:<ref>` status cites its deciding record.
- `INPUT_MANIFEST.sha256` records the hash of every input read.
- Every row in the resolved accepted register was checked against filesystem state (Pass 1).
- Every recommended downstream rerun was checked for evidence of completion (Pass 2).
- For `PROJECT`/`SOFTWARE` DEL identities, affected-reference assessment covered needs referencing the changed or retired entities across all consumer-local `deliverable.yaml` files (Pass 3), preserving supported historical inputs. The native-needs pass is `NOT_APPLICABLE` for `DOMAIN`; its other applicable passes remain required.
- Decomposition document consistency was verified against the amendment record (Pass 4).
- Context metadata for every affected deliverable was checked against the decomposition (Pass 5).
- Supersession binding completeness was verified for all source-affecting actions (Pass 6) — this pass runs whenever any row of the resolved accepted register has `SupersessionBindingPresent = YES`, regardless of whether supersession artifacts are present on disk.
- For `DECOMP_VARIANT = DOMAIN`, KTY content remediation state was verified against `KTY_Remediation_Manifest.csv` when present or required (Pass 7).
- For `DOMAIN`, `.Archive/` scanner exclusion was checked against downstream allowlist, section-map, regeneration-input, and publication-input surfaces where present.
- For `DOMAIN`, decomposition integrity was verified through `validate_domain_decomposition_integrity.py`, and supersession-map accumulation was verified through `accumulate_supersession_map.py` when supersession inputs were in scope.
- Every finding has an `EvidenceFile` and `SourceRef` (or explicit `location TBD`).
- No finding was silently resolved — conflicts between the amendment record and filesystem state are reported with both sides cited.
- The issue log CSV conforms to the Issue Log Schema below.
- The summary JSON includes counts per severity and the overall closure status.
- The snapshot folder is immutable after creation ([K-SNAP-1 (historical)](https://github.com/sgttomas/chirality/blob/archive/pre-docs-cleanup-1/docs/CONTRACT.md)).

### Invalid States

| Invalid State | Why |
|---|---|
| Finding without evidence | Violates evidence-first invariant |
| Action marked VERIFIED when filesystem contradicts | False positive — integrity failure |
| Rerun judged sufficient from dates alone | Inspect actual local declaration/source changes; derivative snapshots require matching scope and input basis |
| Prior audit snapshot edited in place | Corrections use a new superseding snapshot |
| PROJECT/SOFTWARE native affected-reference search limited to changed packages only | Search all consumer-local DEL `deliverable.yaml` files for references to the changed entities; consumers may be in other packages. This native-needs requirement does not apply to DOMAIN KTY identities |
| Silent resolution of amendment/filesystem disagreement | Violates conflict surfacing invariant |
| Audit scope expanded beyond the specified amendment | Each audit covers one `AMENDMENT_ID`; separate runs for separate amendments |
| DOMAIN KTY remediation manifest ignored | KTY content may be stale, retired, or blocked for factual use without audit visibility |
| `.Archive/` treated as current factual input | Retired content can leak into downstream outputs |

---

## Artifacts and schemas

### Brief Format

```
PURPOSE: Verify closure of scope change amendment
AMENDMENT_ID: SCA-{NNN} | SCA-{PREFIX}-{NNN}
EXECUTION_ROOT: {absolute path}
SCOPE_CHANGE_ROOT: {path, default: {EXECUTION_ROOT}/_ScopeChange/}
DECOMPOSITION_PATH: {absolute path to decomposition document}
DECOMP_VARIANT: PROJECT | SOFTWARE | DOMAIN
CONSTRAINTS:
  - {any scope limitations or focus areas}
NOTES:
  - {context from WORKING_ITEMS about why this audit was requested}
```

### Snapshot Layout

```
{EXECUTION_ROOT}/_Evaluation/ScopeClosureAudit/
  _LATEST.md
  ScopeClosure_{AMENDMENT_ID}_{YYYY-MM-DD}_{HHMM}/
    Brief.md
    INPUT_MANIFEST.sha256             (SHA-256 of every input read)
    Scope_Closure_Report.md
    Scope_Closure_IssueLog.csv
    scope_closure_summary.json
    QA_Report.md
    Domain_Integrity_Report.md        (DOMAIN-only, tool output)
    Domain_Integrity_Findings.csv     (DOMAIN-only, tool output)
    Expected_Supersession_Map.csv     (Pass 6 accumulator output when run)
    Supersession_Map_Findings.csv     (Pass 6 accumulator check findings when run)
    Reconstructed_{PRIOR_ID}_Backfill.csv  (Pass 6 reconstructed prior map when the prior map was missing)
    SUPERSESSION_NOTE.md              (only in a snapshot that supersedes an earlier audit snapshot)
```

A superseding snapshot names the superseded snapshot, the reason and the changed
inputs or evidence binding; the superseded snapshot's bytes stay unchanged and
`_LATEST.md` moves to the new snapshot.

### Issue Log Schema (`Scope_Closure_IssueLog.csv`)

| Column | Type | Description |
|---|---|---|
| `IssueID` | string | `ASC-ISS-{NNN}` sequential within this audit. Historical logs using `SCC-{NNN}` remain readable as written; the prefix distinguishes audit findings from historical cycle identifiers and project-qualified amendment IDs |
| `Pass` | integer | Which audit pass found the issue (1–7) |
| `Category` | enum | `ACTION_NOT_EXECUTED`, `DOWNSTREAM_NOT_RUN`, `ORPHANED_REFERENCE`, `DECOMP_INCONSISTENCY`, `METADATA_STALE`, `COVERAGE_REGRESSION`, `SUPERSESSION_INCOMPLETE`, `KTY_CONTENT_REMEDIATION`, `ARCHIVE_SCANNER_LEAK` |
| `Severity` | enum | `CRITICAL`, `MAJOR`, `MINOR`, `OBSERVATION` |
| `Assessment` | enum | `DETERMINATE`, `UNKNOWN`; uncertainty is independent of severity |
| `AmendmentAction` | string | The `ActionSeq` from the accepted action register this finding relates to (or `N/A` for cross-cutting findings) |
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
  "closureStatus": "CLOSED | CLOSED_WITH_OBSERVATIONS | OPEN | FAILED_INPUTS",
  "actionRegister": "{path of the accepted action register}",
  "totalActions": 0,
  "actionsVerified": 0,
  "actionsDiscrepant": 0,
  "actionsNotExecuted": 0,
  "actionsDeferredByHuman": 0,
  "actionsSuperseded": 0,
  "downstreamRerunsRecommended": 0,
  "downstreamRerunsCompleted": 0,
  "downstreamRerunsDeferredOrNotActivated": 0,
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
**Closure Status:** {CLOSED | CLOSED_WITH_OBSERVATIONS | OPEN | FAILED_INPUTS}
**Amendment Date:** {from amendment snapshot}
**Amendment Description:** {from Brief.md in amendment snapshot}

## Amendment Summary
{Reproduce the action summary from the accepted action register, naming the register file and how it was resolved}

## Pass 1 — Action Verification
{Table: ActionSeq | ActionType | EntityID | Expected | Actual | Status}

## Pass 2 — Downstream Rerun Verification
{Table: Agent | Scope | Evidence | Status}

## Pass 3 — Affected References
{Each relevant local need, its accepted-change/condition assessment, evidence and required action or supported unchanged use. Count only demonstrably unsupported bindings as orphaned references.}

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
- PROJECT/SOFTWARE DEL deliverable.yaml files searched for affected references: {n; NOT_APPLICABLE for DOMAIN}
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

---
