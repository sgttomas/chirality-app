# review — contract

## Runtime variables and defaults

This file is **project-generic**. Do not embed project-specific absolute paths.

Defaults (only when not otherwise specified by the human):
- `EXECUTION_ROOT = execution/`
- `REVIEWS_ROOT = {EXECUTION_ROOT}/_Evaluation/Reviews/`
- `DECOMPOSITION_PATH` = discovered from `{EXECUTION_ROOT}/_Decomposition/`

---

## Non-negotiable invariants

- **Read-only on deliverable content.** WORKING_ITEMS does not modify `Datasheet.md`,
  `Specification.md`, `Guidance.md`, `Procedure.md`, `ScopeOfWork.md`,
  `Dependencies.csv`, or `_CONTEXT.md`. It reads the production contract
  selected by the accepted basis for checklist derivation and consistency.
- **Writes only review artifacts.** WORKING_ITEMS writes `_REVIEW.md`, `Review_Findings.csv` (deliverable-local), and `_STATUS.md` (lifecycle transition only, with human approval). It writes review snapshots to `_Evaluation/Reviews/`.
- **Human-gated transitions.** Lifecycle state changes (`IN_PROGRESS → CHECKING`, `CHECKING → ISSUED`) require explicit human approval at Gate 5. WORKING_ITEMS does not auto-advance.
- **Findings are human-owned.** Substantive engineering findings originate from human reviewers. WORKING_ITEMS may also produce *mechanical check findings* (e.g., cross-document inconsistencies, missing fields, TBD counts) and record them as findings **only** when clearly labeled `Origin: AGENT_CHECK`. These are not human judgments; the human may accept, downgrade, or dismiss them.
- **Dispositions are human-owned.** WORKING_ITEMS may propose dispositions (labeled `PROPOSAL`) but the `HumanDisposition` field remains `TBD` until the human rules.
- **Evidence-first.** Every checklist item traces to a selected production
  source, decomposition artifact, or objective. Every finding references its
  source artifact, section or claim ID, and evidence references.
- **No invention.** If review information is ambiguous or incomplete, mark as `TBD` and surface.
- **Immutable snapshots.** Review snapshots under `_Evaluation/Reviews/` are immutable. `_LATEST.md` may be overwritten as a pointer.
- **One deliverable per review.** Each review workflow targets exactly one deliverable. For batch review across multiple deliverables, the human runs WORKING_ITEMS once per deliverable (or a future batch orchestration layer manages the fan-out).
- **Format migration review is lifecycle-neutral.** WORKING_ITEMS resolves
  `SOW_V1` or transitional `LEGACY_FOUR_DOC`; it accepts `MIGRATION_DUAL` only
  under exact isolated migration authority and never treats it as an accepted
  baseline. Missing, partial, invalid, ambiguous, and unauthorized dual input
  fails closed.
- **SOW criteria are deterministically compiled.** WORKING_ITEMS must run or
  receive `tools/scope_of_work/derive_review_checklist.py` output bound to the
  current validated `ScopeOfWork.md` and accepted format basis. It consumes all `AC-*` items in the
  emitted order with exact IDs and text. It does not re-extract, paraphrase,
  reorder, renumber, or omit them. Agent judgment is limited to the actual
  human-gated review after this mechanical derivation.

---

## Review undertaking boundaries

The selected review undertaking collects evidence, records human findings and dispositions, and performs authorized lifecycle recording. Content repairs use a separately authorized implementation workflow so their authoring and verification remain distinct from review judgment. WORKING_ITEMS may coordinate those phases within the accepted undertaking; when another instance or loop owns the production scope, route the finding to that owner.

Use the change workflow for authorized Git closeout and TASK with the audit-decomp workflow for the bounded decomposition precondition check. Workflow selection preserves the current undertaking’s ownership and does not itself expand its write targets or decision rights.

---

## Review Types

WORKING_ITEMS supports four review types. The human selects the type at Gate 1. Each type adds specific checklist items on top of the common checklist.

| Review Type | Description | Additional Checklist Focus |
|-------------|-------------|---------------------------|
| `SELF_CHECK` | Producer reviews own work | Completeness, internal consistency, TBD reduction |
| `PEER_REVIEW` | Another practitioner reviews | Technical accuracy, methodology, assumptions validity |
| `IDC` | Interdisciplinary check | Interface consistency, cross-discipline assumptions, shared parameters |
| `INDEPENDENT_VERIFICATION` | QA/compliance check | Code/standard compliance, regulatory requirements, traceability |

---

## Inputs

### Required (at Gate 1)
- `DELIVERABLE_PATH`: path to the deliverable folder (or DeliverableID to resolve)
- `REVIEW_TYPE`: `SELF_CHECK` | `PEER_REVIEW` | `IDC` | `INDEPENDENT_VERIFICATION`

### Optional
- `EXECUTION_ROOT`: default `execution/`
- `REVIEWER_IDS`: list of reviewer identifiers (default `TBD`)
- `PRIOR_REVIEW`: path to a prior `_REVIEW.md` for continuation/re-review
- `CUSTOM_CHECKLIST_ITEMS`: additional checklist items provided by the human

---

## Validity

A review cycle is valid when:

- The review targets exactly one deliverable.
- The review type was explicitly selected by the human.
- Precondition checks ran at Gate 1 (context validity, lifecycle state).
- A checklist was generated and confirmed at Gate 2.
- In `SOW_V1` or authorized migration-dual mode, the checklist source is valid
  `chirality-review-checklist/v1` output whose source SHA matches the
  reviewed `ScopeOfWork.md`; every emitted `AC-*` appears exactly once in the
  emitted order with byte-for-byte criterion text and its verification
  linkage.
- All findings in `Review_Findings.csv` have:
  - `FindingID`, `FindingSeverity`, `Description`, `Document`, `Status` populated
  - `ProposedDisposition` labeled as `PROPOSAL`
  - `HumanDisposition` either `TBD` (pre-Gate 4) or a human-assigned value (post-Gate 4)
- For lifecycle transitions:
  - `IN_PROGRESS → CHECKING`: all CRITICAL findings have non-TBD `HumanDisposition`
  - `CHECKING → ISSUED`: all CRITICAL and MAJOR findings have non-TBD `HumanDisposition`; all CRITICAL findings are RESOLVED
- `_STATUS.md` was modified only at Gate 5 with explicit human approval.
- No deliverable content files were modified (`Datasheet.md`,
  `Specification.md`, `Guidance.md`, `Procedure.md`, `ScopeOfWork.md`,
  `Dependencies.csv`, and `_CONTEXT.md` are read-only).
- An immutable review snapshot exists under `_Evaluation/Reviews/`.
- `_REVIEW.md` and `Review_Findings.csv` exist in the deliverable folder.

---

## Artifacts and schemas

### Deliverable-local artifacts

```
{deliverable_folder}/
  _REVIEW.md              (checklist + summary; created at Gate 2, updated at Gate 4)
  Review_Findings.csv     (finding register; created at Gate 3, updated through Gate 4)
```

### Tool-root layout

```
{EXECUTION_ROOT}/_Evaluation/Reviews/
  _LATEST.md
  REV_{DeliverableID}_{YYYY-MM-DD}_{HHMM}/
    Brief.md
    RUN_SUMMARY.md
    Review_Summary.md
    Decision_Log.md
    QA_Report.md
```

### _REVIEW.md Template

```markdown
# Review: {DeliverableID}

**Review Type:** {SELF_CHECK | PEER_REVIEW | IDC | INDEPENDENT_VERIFICATION}
**Reviewer(s):** {reviewer IDs or TBD}
**Date Initiated:** {YYYY-MM-DD}
**Status:** {IN_PROGRESS | DISPOSITIONS_COMPLETE | ADVANCED | HELD}

## Precondition Check
- Decomposition coverage: {PASS | WARNING | SKIP} {snapshot ref}
- Lifecycle state: {current state}
- Context validity: {PASS | WARNING with details}

## Checklist

### Artifact Presence
| ID | Artifact | Present | Notes |
|----|----------|---------|-------|
| AP-001 | {name} | {Y/N} | |

### Acceptance Criteria (from selected legacy Specification.md or validated ScopeOfWork.md)
| ID | Criterion | Verification | Source binding | Addressed |
|----|-----------|--------------|----------------|-----------|
| AC-001 | {exact criterion text} | {VER-* or HUMAN_REVIEW method} | {qualified ID; ScopeOfWork SHA-256; line} | {Y/N/PARTIAL} |

### Objective Coverage
| ID | Objective | Addressed | Document §Section |
|----|-----------|-----------|-------------------|
| OC-001 | {OBJ-ID}: {description} | {Y/N/PARTIAL} | |

### Cross-Document Consistency
| ID | Check | Result | Notes |
|----|-------|--------|-------|
| XD-001 | {description} | {PASS/FAIL} | |

### Dependency Satisfaction
| ID | Dependency | Target | Satisfaction | Notes |
|----|------------|--------|-------------|-------|
| DS-001 | {DependencyID} | {TargetDeliverableID} | {SATISFIED/UNSATISFIED/TBD} | |

### TBD Inventory
| ID | Check | Result | Notes |
|----|-------|--------|-------|
| TB-001 | Remaining TBDs assessed | {count} TBDs remaining | |

### Review-Type-Specific
| ID | Check | Result | Notes |
|----|-------|--------|-------|
| {IC/IV/CU}-001 | {description} | | |

## Findings Summary
| Severity | Total | Resolved | Open | Deferred |
|----------|-------|----------|------|----------|
| CRITICAL | | | | |
| MAJOR | | | | |
| MINOR | | | | |
| OBSERVATION | | | | |

## Transition Readiness
**Target transition:** {IN_PROGRESS → CHECKING | CHECKING → ISSUED}
**Recommendation:** {RECOMMEND_ADVANCE | RECOMMEND_HOLD}
**Rationale:** {evidence-based explanation}
```

### Review_Findings.csv Schema

| Column | Type | Description |
|--------|------|-------------|
| `FindingID` | string | `RF-{NNN}` sequential within review |
| `ChecklistItemRef` | string | Checklist item ID (e.g., `AC-003`) or `GENERAL` |
| `Document` | string | selected source artifact (`Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`, `ScopeOfWork.md`) or `GENERAL` |
| `SectionRef` | string | Section heading, registered local ID, or `N/A` |
| `ClaimRef` | string | Qualified SOW claim/criterion ID or `N/A` |
| `EvidenceRefs` | string | Semicolon-delimited source and verification references or `N/A` |
| `FindingSeverity` | enum | `CRITICAL` / `MAJOR` / `MINOR` / `OBSERVATION` |
| `Description` | string | The finding as stated |
| `Origin` | enum | `REVIEWER` (human-provided) / `AGENT_CHECK` (mechanical check) |
| `ProposedDisposition` | enum | `ACCEPT_AS_IS` / `REVISE` / `DEFER` / `NOT_APPLICABLE` — labeled PROPOSAL |
| `HumanDisposition` | enum | `TBD` / `ACCEPT_AS_IS` / `REVISE` / `DEFER` / `NOT_APPLICABLE` / `WITHDRAWN` |
| `Status` | enum | `OPEN` / `RESOLVED` / `DEFERRED` / `WITHDRAWN` |
| `ReviewerID` | string | Reviewer identifier or `TBD` |
| `Date` | string | `YYYY-MM-DD` |

### Recommended Commit Message Format

```
review: {DeliverableID} — {CHECKING|ISSUED} ({finding_count} findings, {open_count} open)
```

---
