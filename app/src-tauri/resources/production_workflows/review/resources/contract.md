# review — contract

## Runtime variables and defaults

This file is **project-generic**. Do not embed project-specific absolute paths.

Defaults (only when not otherwise specified by the human):
- `EXECUTION_ROOT = execution/`
- `REVIEWS_ROOT = {EXECUTION_ROOT}/_Evaluation/Reviews/`
- `DECOMPOSITION_PATH` = discovered from `{EXECUTION_ROOT}/_Decomposition/`
- `INSTRUCTION_ROOT` = the Chirality instruction root that supplies this
  workflow and its tools (the Root checkout or the App's bundled root). Every
  tool command in this workflow is anchored to it.

---

## Non-negotiable invariants

- **Read-only on deliverable content.** WORKING_ITEMS does not modify `Datasheet.md`,
  `Specification.md`, `Guidance.md`, `Procedure.md`, `ScopeOfWork.md`,
  `deliverable.yaml`, or `_CONTEXT.md`. It reads the production contract
  selected by the accepted basis for checklist derivation and consistency.
- **Writes only review artifacts.** WORKING_ITEMS writes `_REVIEW.md`, `Review_Findings.csv` (deliverable-local), and `_STATUS.md` (lifecycle transition only, through the guarded tool with a human decision). It writes review snapshots to `_Evaluation/Reviews/` and updates `_LATEST.md`.
- **Human-gated transitions.** Lifecycle state changes (`IN_PROGRESS → CHECKING`, `CHECKING → ISSUED`, and the reversal `CHECKING → IN_PROGRESS`) require an explicit human decision at Gate 5, recorded through a committed ruling. WORKING_ITEMS does not auto-advance or auto-reverse.
- **No deferral into CHECKING.** Entry to `CHECKING` follows `docs/COMPATIBILITY_FORMATS.md#historical-specification`
  §3.4: a current candidate-bound account showing no unfulfilled production
  obligation in the proposed checking scope, a declared checking basis, and the
  human declaration that freezes the candidate at a recorded commit. There are
  no disclosed-deferral carve-outs: an unfulfilled obligation, including one
  needing a human decision, keeps the deliverable `IN_PROGRESS` until it is
  fulfilled or rescoped through the owning decision before freeze. Where the
  owning loop still pins an earlier Remaining-based entry criterion, that
  pinned criterion is the candidacy basis until the loop adopts §3.4; it never
  adds a deferral path.
- **Frozen candidate.** While `CHECKING`, the deliverable's claim surfaces
  (every file in the deliverable folder except the review, status, context,
  dependency, memory and run records: `_REVIEW.md`, `Review_Findings.csv`,
  `_STATUS.md`, `_CONTEXT.md`, `deliverable.yaml`,
  `MEMORY.md` or legacy `_MEMORY.md`, and run-record folders such as
  `_run_records/`) are frozen at the recorded candidate SHA. Review evidence appends to `_REVIEW.md`,
  `Review_Findings.csv`, and review snapshots, never to the frozen claim
  surfaces. Any correction requires the human-ruled reversal to `IN_PROGRESS`;
  `ISSUED` changes use the governed scope-change process only.
- **Owning-loop fences.** Honour current product issuance boundaries and explicit
  owner holds. The retired administrative hold-register preflight is not required.
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
  receive `{INSTRUCTION_ROOT}/tools/scope_of_work/derive_review_checklist.py`
  output bound to the current validated `ScopeOfWork.md` and accepted format
  basis. It consumes all `AC-*` items in the
  emitted order with exact IDs and text. It does not re-extract, paraphrase,
  reorder, renumber, or omit them. Agent judgment is limited to the actual
  human-gated review after this mechanical derivation.

---

## Review undertaking boundaries

The selected review undertaking collects evidence, records human findings and dispositions, and performs authorized lifecycle recording. Content repairs use a separately authorized implementation workflow so their authoring and verification remain distinct from review judgment. WORKING_ITEMS may coordinate those phases within the accepted undertaking; when another instance or loop owns the production scope, route the finding to that owner.

Git closeout belongs to the responsible implementation owner under the
repository's authorization and Git conventions (AGENTS.md for Chirality Root). Use
TASK with the audit-decomp workflow for the bounded decomposition precondition
check, and a current bounded-reconciliation (or concordance) comparison for the
candidacy account. Workflow selection preserves the current undertaking’s
ownership and does not itself expand its write targets or decision rights.

---

## Transitions reviewed

| Transition | Kind | Entry state | Gate 5 outcomes |
|---|---|---|---|
| `IN_PROGRESS → CHECKING` | Candidacy check and human freeze | `IN_PROGRESS` | Freeze (advance) or decline (remain `IN_PROGRESS`) |
| `CHECKING → ISSUED` | Check of the frozen candidate against its declared basis | `CHECKING` | Issue, continue checking, or reversal |
| `CHECKING → IN_PROGRESS` | Human-ruled reversal, the sole exit from an unsuccessful or withdrawn check | `CHECKING` | Reversal recorded with a committed ruling |

Earlier states (`OPEN`, `INITIALIZED`, `SEMANTIC_READY`) reach `IN_PROGRESS`
through their own authorized transitions before a candidacy review; this
workflow has no override that promotes them directly to `CHECKING`. An
`ISSUED` deliverable is changed only through the governed scope-change process.

---

## Severity and disposition rule

This is the single rule for how findings affect each transition.

| Severity | Meaning |
|---|---|
| `CRITICAL` | Safety, regulatory, or fundamental correctness issue; blocks both entry to `CHECKING` and issuance |
| `MAJOR` | Significant technical issue; must be closed before entry to `CHECKING` and before issuance, as below |
| `MINOR` | Quality improvement |
| `OBSERVATION` | Noted for record; no action required |

- **Entry to `CHECKING`.** No finding has `HumanDisposition = TBD` or `DEFER`,
  and no finding has `Status = OPEN` or `DEFERRED`. Every `REVISE` finding is
  `RESOLVED` by an authorized correction to the candidate (after which the
  checklist and candidacy account are re-bound to the corrected candidate) or
  by a cited owning rescoping decision. Deferral is not an entry path.
- **Closing a `CRITICAL` or `MAJOR` finding (entry and issuance alike).** A
  `CRITICAL` finding closes only with `Status = RESOLVED` by correction or
  appended evidence (never by `ACCEPT_AS_IS`), or with
  `HumanDisposition = NOT_APPLICABLE`, or with `HumanDisposition = WITHDRAWN`
  (`Status = WITHDRAWN`). A `MAJOR` finding closes in the same ways or with
  `HumanDisposition = ACCEPT_AS_IS` (`Status = RESOLVED`) when the human rules
  that no correction is required. Neither is ever `DEFER` or `DEFERRED`.
- **`CHECKING → ISSUED`.** The frozen candidate cannot be corrected in place.
  Every `CRITICAL` and `MAJOR` finding is closed under the rule above, where
  `RESOLVED` means resolved without changing the frozen claim surfaces (for
  example, by appended evidence). `MINOR` findings should be dispositioned; a
  `MINOR` or `OBSERVATION` finding that is a quality item, not unfinished
  production work, may be `DEFERRED` with documented human
  rationale as a known limitation of the issued baseline, whose later
  treatment flows only through governed scope change.
- **Unsuccessful check.** A `CRITICAL` or `MAJOR` finding that cannot close
  under the rule above without correcting the frozen candidate makes the check
  unsuccessful. Its exit is the human-ruled reversal to `IN_PROGRESS`, with the
  correction carried in authorized work. A `MINOR` finding that needs
  correction is either `DEFERRED` as above or, if the human chooses, corrected
  through the same reversal.

The issuance judgment itself remains human ([K-GATE-1 (historical)](https://github.com/sgttomas/chirality/blob/archive/pre-docs-cleanup-1/docs/CONTRACT.md)); this rule states what
the review evidence must show, not a machine block.

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
- `CANDIDACY_ACCOUNT`: path to a current candidate-bound comparison covering
  the whole deliverable (for example, a bounded-reconciliation return or a
  concordance `OBLIGATION_ACCOUNT.csv`)
- `PROMOTION_PREFLIGHT`: the owning loop's required preflight command, when
  not discoverable from its instructions

---

## Validity

A review cycle is valid when:

- The review targets exactly one deliverable.
- The review type was explicitly selected by the human.
- Precondition checks ran at Gate 1 (context validity, lifecycle state,
  owning-loop fences).
- A checklist was generated and confirmed at Gate 2.
- In `SOW_V1` or authorized migration-dual mode, the checklist source is valid
  `chirality-review-checklist/v1` output whose source SHA matches the
  reviewed `ScopeOfWork.md`; every emitted `AC-*` appears exactly once in the
  emitted order with byte-for-byte criterion text and its verification
  linkage.
- For entry to `CHECKING`: `_REVIEW.md` records a candidacy account bound to
  the candidate commit that shows no unfulfilled production obligation in the
  proposed checking scope, the declared checking basis, and, after the human
  freeze, the frozen candidate SHA.
- For `CHECKING → ISSUED`: the frozen claim surfaces are unchanged from the
  recorded frozen candidate SHA.
- All findings in `Review_Findings.csv` have:
  - `FindingID`, `FindingSeverity`, `Description`, `Document`, `Status` populated
  - `ProposedDisposition` labeled as `PROPOSAL`
  - `HumanDisposition` either `TBD` (pre-Gate 4) or a human-assigned value (post-Gate 4)
- Findings satisfy the severity and disposition rule above for the recorded
  transition.
- The owning loop's promotion preflight passed and no issuance fence applied
  before any lifecycle write.
- `_STATUS.md` was modified only at Gate 5 through the guarded
  `write_status.sh` with an explicit human decision and committed ruling
  (including a reversal).
- No deliverable content files were modified (`Datasheet.md`,
  `Specification.md`, `Guidance.md`, `Procedure.md`, `ScopeOfWork.md`,
  `deliverable.yaml`, and `_CONTEXT.md` are read-only).
- A new immutable `REV_*` snapshot was finalized at Gate 5 under
  `_Evaluation/Reviews/`, recording the Gate 5 outcome (approve, decline, or
  reversal), and `_LATEST.md` points to it. A review cycle without its
  finalized snapshot is incomplete.
- `_REVIEW.md` and `Review_Findings.csv` exist in the deliverable folder.

---

## Artifacts and schemas

### Deliverable-local artifacts

```
{deliverable_folder}/
  _REVIEW.md              (candidacy account, checking basis, checklist, summary, freeze record; created at Gate 2, updated through Gate 5)
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
**Status:** {IN_PROGRESS | DISPOSITIONS_COMPLETE | ADVANCED | HELD | REVERSED}

## Precondition Check
- Decomposition coverage: {PASS | WARNING | SKIP} {snapshot ref}
- Lifecycle state: {current state}
- Context validity: {PASS | WARNING with details}
- Owning-loop fences: {preflight command and result | NONE}; {issuance fence | NONE}

## Candidacy Account (entry to CHECKING)
- Candidate commit: {SHA}
- Comparison source: {bounded-reconciliation return | concordance OBLIGATION_ACCOUNT | pinned Remaining-based criterion} {path}
- Scope compared: Scope of Work, actual outputs, dependencies, required production verification
- Result: {NO_UNFULFILLED_OBLIGATION | UNFULFILLED: list with owning graph node or decision}

## Checking Basis
- Declared by: {human} on {YYYY-MM-DD} ({ruling path})
- Basis: {review type, criteria, checklist scope, reviewers, evidence expected}

## Freeze
- Frozen candidate SHA: {commit SHA}
- ScopeOfWork SHA-256: {hash}
- Freeze ruling: {ruling path}; approval SHA: {SHA | not declared by root}

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

### Dependency Conditions
| ID | Need source | From/recipient | Condition assessment | Evidence and effect on reviewed scope |
|----|-------------|----------------|----------------------|---------------------------------------|
| DS-001 | {deliverable.yaml path and need index} | {from; direction where outward} | {SATISFIED/UNSATISFIED/UNKNOWN/NOT_APPLICABLE} | {condition, when/case, evidence and rationale} |

### TBD Inventory
| ID | Check | Result | Notes |
|----|-------|--------|-------|
| TB-001 | Each remaining TBD is outside the proposed checking scope by a cited owning decision; none is an unfulfilled production obligation | {count} TBDs remaining | {decision refs} |

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
**Target transition:** {IN_PROGRESS → CHECKING | CHECKING → ISSUED | CHECKING → IN_PROGRESS (reversal)}
**Recommendation:** {RECOMMEND_ADVANCE | RECOMMEND_HOLD | RECOMMEND_REVERSAL}
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
| `ProposedDisposition` | enum | `ACCEPT_AS_IS` / `REVISE` / `DEFER` / `NOT_APPLICABLE` — labeled PROPOSAL; `DEFER` is never an entry path to `CHECKING` and at issuance applies only to `MINOR` or `OBSERVATION` findings |
| `HumanDisposition` | enum | `TBD` / `ACCEPT_AS_IS` / `REVISE` / `DEFER` / `NOT_APPLICABLE` / `WITHDRAWN` |
| `Status` | enum | `OPEN` / `RESOLVED` / `DEFERRED` / `WITHDRAWN` |
| `ReviewerID` | string | Reviewer identifier or `TBD` |
| `Date` | string | `YYYY-MM-DD` |

### Recommended Commit Message Format

```
review: {DeliverableID} — {CHECKING|ISSUED|IN_PROGRESS (reversal)|HELD} ({finding_count} findings, {open_count} open)
```

---
