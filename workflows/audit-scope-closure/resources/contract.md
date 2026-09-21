# audit-scope-closure — contract

## Non-negotiable invariants

- **Read-only on project state.** This agent reads deliverable folders, decomposition documents, amendment snapshots, dependency registers, and tool-root artifacts. It does not modify any of them.
- **Evidence-first.** Every finding must cite the specific file, row, or section that constitutes evidence. Findings without evidence are invalid.
- **No invention.** If the impact of a finding is uncertain, record `Assessment: UNKNOWN`, use the observed consequence to select a provisional severity, and flag for human triage. Do not guess resolution paths.
- **Conflicts surfaced.** If the amendment record disagrees with the filesystem state, report both sides with provenance. Do not silently choose a winner.
- **Immutable snapshots.** Each audit run produces a new timestamped snapshot folder. Never overwrite prior snapshots (K-SNAP-1).
- **Scope-bounded.** Audit only the scope change identified in the brief. Do not expand to unrelated deliverables unless orphan tracing requires it.
- **Amendment record is authoritative.** The `Amendment_Actions.csv` in the scope change snapshot is the source of truth for what should have happened. The audit verifies reality against this record.
- **DOMAIN deterministic validation is tool-backed.** For `DECOMP_VARIANT = DOMAIN`, this audit invokes the same registered validators used by WORKING_ITEMS (workflow: scope-change): `validate_domain_decomposition_integrity.py`, `accumulate_supersession_map.py`, and `validate_kty_remediation_manifest.py` when their inputs are in scope.

---

## Glossary

| Term | Meaning |
|------|---------|
| **Amendment record** | The immutable snapshot under `_ScopeChange/SCA-{NNN}_*/` produced by WORKING_ITEMS (workflow: scope-change), containing the brief, impact assessment, propagation plan, actions CSV, and run summary |
| **Closure** | The state in which every action in the amendment record has been executed and all downstream effects have been propagated and verified |
| **Orphaned reference** | A dependency row, context field, or other artifact that references an entity modified or removed by the scope change but has not been updated to reflect the change |
| **Downstream rerun** | An agent/workflow execution recommended by WORKING_ITEMS (workflow: scope-change)'s propagation plan (e.g., TASK+dependency-extract or a TASK estimation workflow rerun) that must complete for closure |
| **Stale metadata** | A `_CONTEXT.md`, `_STATUS.md`, or decomposition section that does not reflect the post-change state |

---

## Validity

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

---

## Artifacts and schemas

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
  - {context from WORKING_ITEMS about why this audit was requested}
```

### Snapshot Layout

```
{EXECUTION_ROOT}/_Evaluation/ScopeClosureAudit/
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
| `Assessment` | enum | `DETERMINATE`, `UNKNOWN`; uncertainty is independent of severity |
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

---
