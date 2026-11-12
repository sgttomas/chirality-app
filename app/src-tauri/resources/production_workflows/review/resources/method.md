# review — method

Apply the [contract](contract.md)'s transitions table and its single severity
and disposition rule throughout. Governing text: `docs/COMPATIBILITY_FORMATS.md#historical-specification` §3.2–3.4.

## Method

### Gate 1 — Scope and Precondition Check

**Human provides:** Which deliverable to review, what review type, and the
intended transition (or withdrawal of a current check).

**Agent does:**

1) Resolve `DELIVERABLE_PATH`. Confirm the folder exists.
2) Read `_STATUS.md`. Validate lifecycle state:
   - For an `IN_PROGRESS → CHECKING` candidacy review: state must be
     `IN_PROGRESS`. There is no override from earlier states. `INITIALIZED` or
     `SEMANTIC_READY` first moves to `IN_PROGRESS` through its own authorized
     transition (SPEC §3.3); `OPEN` routes production through the currently
     authoritative format workflow.
   - For a `CHECKING → ISSUED` review: state must be `CHECKING`. Read the
     frozen candidate SHA recorded at entry (in the prior `_REVIEW.md` Freeze
     section or the entry snapshot) and confirm the deliverable's claim
     surfaces (contract, Frozen candidate) are unchanged since it, for example
     with `git diff --quiet {FROZEN_SHA} -- {deliverable_folder}` and
     `:(exclude)` pathspecs for the excluded records, paired with
     `git status --porcelain` on the same folder and exclusions so that
     untracked files are seen too. A changed frozen surface means the candidate
     under review is not the frozen one: stop and present the reversal branch
     of Gate 5.
   - If no frozen SHA or declared checking basis is recorded (for example, a
     deliverable that entered `CHECKING` under an earlier override), stop and
     surface the missing basis. Offer the human two routes: a committed ruling
     that records the checking basis and the entry-commit SHA as the frozen
     candidate, and either cites the entry evidence it relied on or directs
     the candidacy comparison to be run now at that SHA, after which this
     review continues; or the reversal branch of Gate 5.
   - For a withdrawn check (state `CHECKING`, human withdraws): go directly to
     the reversal branch of Gate 5 after recording the stated reason.
   - If state is `ISSUED`: stop. Changes to an accepted baseline use the
     governed scope-change process, not this workflow.
3) Read `_CONTEXT.md`. Extract identity and mappings, then resolve the
   production format. `SOW_V1` and complete `LEGACY_FOUR_DOC` are valid;
   `MIGRATION_DUAL` requires exact accepted path authority. Refuse all other
   states.
4) Identify the owning loop's lifecycle instruments from its instructions and
   `_harness/adapter.yaml`: the required ruling instrument, approval-SHA
   schema where applicable, current owner holds, issuance fences (for
   example, App F-APP-4: no `CHECKING → ISSUED`), and whether the loop has
   adopted SPEC §3.4 candidacy or still pins an earlier Remaining-based entry
   criterion. When a fence prohibits the intended transition, say so now; the
   review may still gather evidence, but Gate 5 will not record that
   transition.
5) If `DECOMPOSITION_PATH` is available: dispatch TASK (workflow: audit-decomp) scoped to this single deliverable (pass `DECOMP_VARIANT` if known; otherwise infer from the decomposition document's entity names). Report context validity:
   - `PASS`: decomposition and filesystem agree for this deliverable
   - `WARNING`: discrepancies exist (list them)
   - `SKIP`: no decomposition available (proceed with filesystem-only review)
6) Present precondition summary:
   - Deliverable identity and current state
   - Intended transition and review type selected
   - Context validity result
   - Owning-loop preflight, fences, and candidacy basis in force
   - Anticipated artifacts from decomposition
   - Any precondition warnings

Ask: "Proceed with review, or resolve precondition issues first?"

**Human confirms** to proceed.

---

### Gate 2 — Candidacy Account, Checking Basis, and Checklist

**Agent does:**

1) **Candidacy account** (`IN_PROGRESS → CHECKING` only). Establish current
   candidate-bound evidence that accounts for the deliverable's applicable
   production obligations and shows that none remains unfulfilled within the
   proposed checking scope (SPEC §3.4 layer 1):
   - Identify the candidate commit SHA.
   - Consume `CANDIDACY_ACCOUNT` when it is a current whole-deliverable
     comparison bound to that commit: a bounded-reconciliation return, or a
     concordance `OBLIGATION_ACCOUNT.csv` covering this deliverable. Otherwise
     dispatch TASK (workflow: bounded-reconciliation) for a read-only
     comparison of this deliverable at the candidate commit; any warranted
     document edit it finds is production work outside this review.
   - The comparison covers the Scope of Work, actual outputs, dependencies,
     and required production verification. Closing graph nodes or deleting a
     list is not proof of coverage.
   - Where the owning loop still pins a Remaining-based entry criterion, apply
     it as the candidacy basis and record which basis applied.
   - Record the result in `_REVIEW.md` §Candidacy Account. If any production
     obligation is unfulfilled, including one needing a human decision or
     missing required production verification, the deliverable stays
     `IN_PROGRESS`: report each item with its owning graph node or decision,
     recommend `RECOMMEND_HOLD`, and route it to production or to the owning
     rescoping decision. There is no deferral path. The human may end the
     review here or continue gathering evidence; Gate 5 will not freeze while
     any obligation remains.

2) **Checking basis.** Draft the candidate-specific checking basis
   appropriate to the deliverable's claims and risk (SPEC §3.4 layer 2):
   review type, criteria and checklist scope, reviewers, and the evidence the
   check will append. Record it in `_REVIEW.md` §Checking Basis as a
   `PROPOSAL`; the human declares it at Gate 5. For `CHECKING → ISSUED`, the
   basis is the one declared at entry; a change to it requires a recorded
   human ruling.

3) **Checklist.** Generate a structured review checklist from multiple
   sources. Each checklist item has an ID, source reference, and a blank
   status field.

**Common checklist items (all review types):**

1) **Artifact Presence** (from `_CONTEXT.md` → AnticipatedArtifacts; for DOMAIN variants, AnticipatedArtifacts lists Knowledge Subjects):
   - For each anticipated artifact: is it present in the folder?
   - Legacy mode: check `Datasheet.md`, `Specification.md`, `Guidance.md`, and
     `Procedure.md`.
   - SOW mode: check validated `ScopeOfWork.md`. In authorized migration-dual
     review, also verify the four byte-preserved legacy sources for parity.
   - ID format: `AP-{NNN}`

2) **Acceptance Criteria**:
   - Legacy mode: scan `Specification.md` for testable acceptance criteria,
     requirements, or success conditions and assign review-local `AC-{NNN}`.
   - `SOW_V1` or authorized migration-dual mode: run
     `python3 {INSTRUCTION_ROOT}/tools/scope_of_work/derive_review_checklist.py {deliverable_folder}/ScopeOfWork.md --output {working_package}/review_checklist.json`
     (add `--isolated-migration --migration-authority {AUTHORITY}` only under
     exact accepted migration authority), or consume an artifact already
     produced by that registered tool. Verify its source SHA-256
     matches the current SOW source. Copy every emitted `AC-*` ID and text into
     the checklist in emitted order, together with its qualified identity,
     source line/hash binding, and linked `VER-*` or explicit human-review
     method. Do not independently scan, summarize, renumber, add, remove, or
     reorder SOW criteria. A tool failure blocks SOW checklist
     generation; it is not an invitation to reconstruct the rows agentically.
   - Each criterion becomes a checklist item: "Is this criterion addressed?"

3) **Objective Coverage** (from `_CONTEXT.md` → SupportsObjectives, cross-referenced with decomposition §6):
   - For each mapped objective: is it addressed in the deliverable content?
   - ID format: `OC-{NNN}`

4) **Production-Contract Consistency**:
   - Key parameters agree across Datasheet ↔ Specification (units, values, names)
   - Guidance rationale supports Specification requirements
   - Procedure steps address Specification requirements
   - ID format: `XD-{NNN}`
   - SOW mode: replace file-pair checks with registered-reference and
     cross-section checks among Ontology, Epistemology, Praxeology, and
     Axiology; confirm every `OUT-*`, `AC-*`, and `VER-*` closes through the
     output/evaluation matrix.

5) **Dependency conditions**:
   - Read this consumer's `deliverable.yaml` needs and the relevant scope,
     design and actual input evidence at the review basis. Assess each
     applicable `condition` with its `when`, case, maturity and technical
     holds. Cite the source file and need index; preserve distinct needs
     between the same endpoints.
   - Use `tools.deliverables neighborhood` for relevant reverse links when
     available; see `tools/deliverables/README.md` and
     `construct-local-work-graph`. The CLI needs a Git repository with HEAD
     and the project root, and loads all project declarations/path-presence
     references. Use it only within the authorized read scope; otherwise
     inspect the relevant declarations directly and state reverse-link limits.
     A bounded query is not a completeness claim.
   - Record `SATISFIED`, `UNSATISFIED`, `UNKNOWN` or `NOT_APPLICABLE` for
     this review's condition assessment, with evidence and rationale. These
     are review observations, not persisted dependency satisfaction states.
     File presence, producer lifecycle or merge status does not establish
     suitability. An unresolved source remains unknown.
   - Keep external inputs distinct from `direction: downstream` outward
     obligations. Outward obligations are not this consumer's prerequisites;
     assess their actual recipient/use where relevant to the review.
   - Preserve `gating` as declared. `gating: false` does not waive a technical
     condition. Report reciprocal needs without automatically holding or
     making them non-gating; the CLI's cycle list covers native deliverables
     only and does not assess technical readiness. Identify the specific
     unmet condition and its effect on the reviewed scope before treating
     it as an unfulfilled production obligation.
   - ID format: `DS-{NNN}`

6) **TBD Inventory**:
   - Count `TBD` occurrences across the four documents in legacy mode; in
     SOW mode count registered `TBD-*` items plus unregistered TBD text.
   - Classify each: an unfulfilled production obligation (it blocks entry to
     `CHECKING` and belongs in the candidacy account), or outside the proposed
     checking scope by a cited owning decision. A TBD is never accepted "for
     this review stage".
   - ID format: `TB-001`

**Review-type-specific items:**

7) **IDC additions** (when `REVIEW_TYPE = IDC`):
   - For each relevant local need and derived consumer relationship:
     - "Interface assumptions for {source file and need index}, including
       its condition, case and intended use, have been checked"
   - ID format: `IC-{NNN}`

8) **Independent Verification additions** (when `REVIEW_TYPE = INDEPENDENT_VERIFICATION`):
   - "Applicable codes and standards identified in the selected production contract have been verified"
   - "Regulatory/contractual requirements have been traced"
   - "Calculations/analysis methods are appropriate and correctly applied"
   - ID format: `IV-{NNN}`

9) **Custom items** (from `CUSTOM_CHECKLIST_ITEMS` input, if provided):
   - ID format: `CU-{NNN}`

Write `_REVIEW.md` to the deliverable folder with the candidacy account (when
applicable), the proposed checking basis, and the complete checklist (status
fields blank). Start the run-local working review package (see Gate 5) with
the checklist artifact.

Present the candidacy account, proposed checking basis, and checklist to the
human. Ask: "Is this checklist and checking basis adequate, or do you want to
add custom review items?" In SOW mode, additions use the `CU-*` namespace and
do not alter, replace, or remove the deterministic `AC-*` rows.

**Human confirms** or modifies the checklist and basis.

---

### Gate 3 — Findings Capture (Iterative)

This gate is iterative. The human provides findings across multiple conversation turns. The agent records each finding and maintains a running summary.

**Human provides:** Review findings — observations, comments, non-conformances, questions.

**Agent does for each finding:**

1) Parse the finding into structured fields:
   - `FindingID`: `RF-{NNN}` (sequential)
   - `ChecklistItemRef`: which checklist item this relates to (or `GENERAL` if none)
   - `Document`: which document the finding pertains to
   - `SectionRef`: specific section/heading (best-effort)
   - `ClaimRef`: qualified SOW claim/criterion ID or `N/A`
   - `EvidenceRefs`: source and verification references or `N/A`
   - `FindingSeverity`: classify from the human's description using the
     contract's severity table (`CRITICAL`, `MAJOR`, `MINOR`, `OBSERVATION`);
     flag uncertain classifications for human confirmation
   - `Description`: the finding as stated
   - `ProposedDisposition`: agent may suggest one of `ACCEPT_AS_IS`, `REVISE`, `DEFER`, `NOT_APPLICABLE` — always labeled as `PROPOSAL`; never propose `DEFER` as a path into `CHECKING`, or for a `CRITICAL` or `MAJOR` finding
   - `HumanDisposition`: `TBD` (until human rules at Gate 4)
   - `Status`: `OPEN`
   - `ReviewerID`: from input or `TBD`
   - `Date`: current date

2) Append to `Review_Findings.csv` in the deliverable folder.

3) After each finding or batch of findings, present running summary:
   - Findings by severity: CRITICAL ({n}), MAJOR ({n}), MINOR ({n}), OBSERVATION ({n})
   - Open/Resolved counts
   - Any findings the agent flagged for severity confirmation
   - While `CHECKING`: any finding that would require correcting the frozen
     candidate (a candidate for an unsuccessful check)

**Agent may perform mechanical checks** and present results either as checklist outcomes or as findings entries.

If recorded as findings, they must be clearly labeled: `Origin: AGENT_CHECK` (vs `Origin: REVIEWER` for human-provided findings). The human may accept, downgrade, or dismiss them.

Typical mechanical checks:
- Cross-document parameter mismatches detected during checklist analysis
- TBD count changes since last check
- Dependency satisfaction gaps

**Human signals completion:** "Findings capture is complete" or equivalent.

---

### Gate 4 — Disposition Review and Summary

**Agent does:**

1) Present all findings with `HumanDisposition = TBD`:
   - For each: FindingID, severity, description, proposed disposition
   - Ask the human to rule on each

2) Record human rulings in `Review_Findings.csv`:
   - Update `HumanDisposition` from `TBD` to the human's choice
   - Update `Status` to `RESOLVED`, `WITHDRAWN`, or (only at issuance, and only
     for a `MINOR` or `OBSERVATION` finding) `DEFERRED` with the human's
     rationale; a finding awaiting correction stays `OPEN`

3) If a `REVISE` ruling during a candidacy review is corrected through
   separately authorized production work, re-run the checklist derivation and
   recheck the affected candidacy comparison against the corrected candidate
   commit before relying on them.

4) Compile review summary:
   - **Finding totals** by severity and status
   - **All CRITICAL and MAJOR findings** with dispositions
   - **MINOR/OBSERVATION** summary counts
   - **Checklist completion**: items checked vs total
   - **Candidacy account result** and TBD classification (entry to `CHECKING`)
   - **Transition readiness assessment** against the contract's severity and
     disposition rule for the intended transition; while `CHECKING`, name
     any finding that makes the check unsuccessful

5) Update `_REVIEW.md` with the summary section.

6) Stage the run-local working review package. It is finalized as an
   immutable snapshot only at Gate 5:
   - `Brief.md` (deliverable, transition, review type, reviewers, checking basis)
   - `RUN_SUMMARY.md` (complete review summary)
   - `Review_Summary.md` (human-readable narrative)
   - `Decision_Log.md` (all gate decisions + finding dispositions)
   - `QA_Report.md` (checklist coverage, candidacy account, mechanical check results)

Present the review summary and transition readiness assessment. Ask: "Are all dispositions final?"

**Human confirms** dispositions are complete.

---

### Gate 5 — Lifecycle Decision

**Agent does:**

1) Evaluate readiness under the contract's severity and disposition rule:

   **For `IN_PROGRESS → CHECKING` (candidacy and freeze):**
   - Required: `_REVIEW.md` §Candidacy Account shows `NO_UNFULFILLED_OBLIGATION`
     bound to the current candidate commit (or the loop's pinned criterion is
     met).
   - Required: checklist populated (Gate 2) and bound to the same candidate.
   - Required: findings meet the entry rule — no `TBD`, no `DEFER`/`DEFERRED`,
     no `OPEN`, every `REVISE` resolved.
   - Present: `RECOMMEND_ADVANCE` or `RECOMMEND_HOLD` with reasons.

   **For `CHECKING → ISSUED`:**
   - Required: frozen claim surfaces unchanged since the frozen candidate SHA.
   - Required: findings meet the issuance rule.
   - Present: `RECOMMEND_ADVANCE`, `RECOMMEND_HOLD` (continue checking), or
     `RECOMMEND_REVERSAL` (unsuccessful check) with reasons.

2) Check current product issuance boundaries and explicit owner holds. Do not
   infer authorization from this workflow or a passing check. An applicable hold
   prevents the transition until its decision owner resolves it.

3) Present the recommendation with evidence summary. Ask the question for the
   transition:
   - Entry: "Do you declare this checking basis and freeze {DeliverableID} at
     candidate {SHA}, advancing it to `CHECKING`?"
   - Issuance: "Do you approve issuing {DeliverableID}, continue checking, or
     rule a reversal to `IN_PROGRESS`?"

**If the human approves (freeze or issuance):**

4) Record the human decision through the owning loop’s ruling instrument. For
   entry, the ruling names the declared checking basis and the frozen
   candidate SHA; record both in `_REVIEW.md` §Checking Basis and §Freeze.
   Resolve the exact ruling path and approval commit required by that root’s
   `_harness/adapter.yaml`. If the required committed ruling or reachable
   approval SHA is not yet available, carry the approved decision to the
   Git handoff (step 9) and hold the status write until those inputs exist.

5) Invoke the guarded transition:
   ```text
   zsh {INSTRUCTION_ROOT}/tools/scaffolding/write_status.sh {deliverable_folder} {TARGET_STATE} HUMAN --ruling {RULING_PATH} --approval-sha {APPROVAL_SHA}
   ```
   HUMAN identifies the recorded decision-maker; WORKING_ITEMS is the executing recorder and records that distinction in the review evidence. CHECKING and ISSUED require a human decision. Supply `--ruling` whenever required by the adapter (including the default committed-ruling rule in Git roots); supply `--approval-sha` when the adapter declares that schema. Where the root explicitly does not require an approval SHA, omit that option and retain the tool’s REVIEW note. Do not invent a ruling/SHA or use an override to bypass missing inputs. The tool updates Current State and appends history only after its checks pass.

**If the human rules a reversal (`CHECKING → IN_PROGRESS`):**

This is the sole exit from an unsuccessful or withdrawn check (SPEC §3.3).

6) Record the human ruling through the owning loop’s ruling instrument,
   stating whether the check was unsuccessful or withdrawn, the findings or
   reason, and where the required correction is carried in authorized work
   (graph node or decision). Commit it, then invoke:
   ```text
   zsh {INSTRUCTION_ROOT}/tools/scaffolding/write_status.sh {deliverable_folder} IN_PROGRESS HUMAN --ruling {RULING_PATH} --approval-sha {APPROVAL_SHA}
   ```
   The reversal always requires a committed `--ruling`; supply
   `--approval-sha` when the adapter declares that schema. The tool records
   `[reversal from CHECKING; ruling: …]` in the history line. Set
   `_REVIEW.md` Status to `REVERSED`. Prior review evidence and the frozen
   candidate record remain history; a later entry to `CHECKING` needs a new
   candidacy account, basis, and freeze.

**If the human declines, or a preflight or fence holds the transition:**

7) Do NOT update `_STATUS.md`. From `IN_PROGRESS`, the deliverable remains
   `IN_PROGRESS`. From `CHECKING`, the check continues against the frozen
   candidate; its only other exit is the reversal branch above. Record in the
   working package’s `Decision_Log.md`: "Human declined transition at Gate 5
   (or transition held by {preflight/fence}). Reason: {stated reason or 'not
   stated'}." Set `_REVIEW.md` Status to `HELD`. Present options:
   - Return to Gate 3 to capture additional findings
   - Return to Gate 4 to revise dispositions
   - Route unfulfilled obligations or corrections to production work
   - End review session (findings preserved for future review)

**In every branch:**

8) Finalize the review snapshot after the Gate 5 outcome is recorded (for an
   approved or reversal branch, after the guarded status write succeeds; a
   status write still pending its ruling or SHA (step 4) keeps the package
   run-local until it completes or is abandoned, and an abandoned write is
   recorded as a hold). A withdrawn check that skipped Gate 4 stages at least
   `Brief.md` (with the stated reason) and `Decision_Log.md` first:
   ```text
   zsh {INSTRUCTION_ROOT}/tools/scaffolding/create_snapshot_folder.sh {REVIEWS_ROOT} REV {DeliverableID}
   ```
   Copy the staged members into the new folder, including the Gate 5 outcome
   in `Decision_Log.md`; never modify an existing snapshot. Then update the
   authorized pointer:
   ```text
   zsh {INSTRUCTION_ROOT}/tools/scaffolding/update_latest_pointer.sh {REVIEWS_ROOT} {snapshot_folder_name}
   ```

9) Present the Git handoff to the responsible implementation owner under the
   project's authorization and Git conventions (AGENTS.md for Chirality Root).
   - Files modified: `_REVIEW.md`, `Review_Findings.csv`, `_STATUS.md` (when
     written), the ruling record (when this review created it), the new
     `REV_*` snapshot folder, and `_LATEST.md`
   - Recommended commit message:
     ```
     review: {DeliverableID} — {CHECKING|ISSUED|IN_PROGRESS (reversal)|HELD} ({total} findings, {open} open)
     ```

---
