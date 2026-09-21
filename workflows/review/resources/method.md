# review — method

## Method

### Gate 1 — Scope and Precondition Check

**Human provides:** Which deliverable to review and what review type.

**Agent does:**

1) Resolve `DELIVERABLE_PATH`. Confirm the folder exists.
2) Read `_STATUS.md`. Validate lifecycle state:
   - For `IN_PROGRESS → CHECKING` review: state must be `IN_PROGRESS` (or `SEMANTIC_READY` / `INITIALIZED` if the human explicitly overrides)
   - For `CHECKING → ISSUED` review: state must be `CHECKING`
   - If state is `OPEN`: warn that the deliverable has not been initialized and
     route production through the currently authoritative format workflow.
   - If state is `ISSUED`: warn — "Deliverable is already ISSUED; this would be a re-review"
3) Read `_CONTEXT.md`. Extract identity and mappings, then resolve the
   production format. `SOW_V1` and complete `LEGACY_FOUR_DOC` are valid;
   `MIGRATION_DUAL` requires exact accepted path authority. Refuse all other
   states.
4) If `DECOMPOSITION_PATH` is available: dispatch TASK (workflow: audit-decomp) scoped to this single deliverable (pass `DECOMP_VARIANT` if known; otherwise infer from the decomposition document's entity names). Report context validity:
   - `PASS`: decomposition and filesystem agree for this deliverable
   - `WARNING`: discrepancies exist (list them)
   - `SKIP`: no decomposition available (proceed with filesystem-only review)
5) Present precondition summary:
   - Deliverable identity and current state
   - Review type selected
   - Context validity result
   - Anticipated artifacts from decomposition
   - Any precondition warnings

Ask: "Proceed with review, or resolve precondition issues first?"

**Human confirms** to proceed.

---

### Gate 2 — Checklist Generation

**Agent does:**

Generate a structured review checklist from multiple sources. Each checklist item has an ID, source reference, and a blank status field.

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
   - `SOW_V1` or authorized migration-dual mode: invoke
     `tools/scope_of_work/derive_review_checklist.py` with the validated
     `ScopeOfWork.md` and exact accepted format basis, or consume an artifact
     already produced by that registered tool. Verify its source SHA-256
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

5) **Dependency Satisfaction** (from `Dependencies.csv`):
   - For each UPSTREAM dependency with `DependencyClass=EXECUTION` and `Status=ACTIVE`:
     - Is `SatisfactionStatus` recorded?
     - Is the upstream deliverable in a state that can provide the needed information?
   - ID format: `DS-{NNN}`

6) **TBD Inventory**:
   - Count `TBD` occurrences across the four documents in legacy mode; in
     SOW mode count registered `TBD-*` items plus unregistered TBD text.
   - If count > 0: checklist item "Remaining TBDs have been assessed and are acceptable for this review stage"
   - ID format: `TB-001`

**Review-type-specific items:**

7) **IDC additions** (when `REVIEW_TYPE = IDC`):
   - For each UPSTREAM and DOWNSTREAM dependency with `TargetType=DELIVERABLE`:
     - "Interface assumptions between this deliverable and {target} have been checked"
   - ID format: `IC-{NNN}`

8) **Independent Verification additions** (when `REVIEW_TYPE = INDEPENDENT_VERIFICATION`):
   - "Applicable codes and standards identified in the selected production contract have been verified"
   - "Regulatory/contractual requirements have been traced"
   - "Calculations/analysis methods are appropriate and correctly applied"
   - ID format: `IV-{NNN}`

9) **Custom items** (from `CUSTOM_CHECKLIST_ITEMS` input, if provided):
   - ID format: `CU-{NNN}`

Write `_REVIEW.md` to the deliverable folder with the complete checklist (status fields blank).

Present the checklist to the human. Ask: "Is this checklist adequate, or do
you want to add custom review items?" In SOW mode, additions use the
`CU-*` namespace and do not alter, replace, or remove the deterministic
`AC-*` rows.

**Human confirms** or modifies the checklist.

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
   - `FindingSeverity`: classify based on human's description:
     - `CRITICAL` — blocks issuance; safety, regulatory, or fundamental correctness issue
     - `MAJOR` — must resolve before advancing; significant technical issue
     - `MINOR` — should resolve; quality improvement
     - `OBSERVATION` — noted for record; no action required
   - `Description`: the finding as stated
   - `ProposedDisposition`: agent may suggest one of `ACCEPT_AS_IS`, `REVISE`, `DEFER`, `NOT_APPLICABLE` — always labeled as `PROPOSAL`
   - `HumanDisposition`: `TBD` (until human rules at Gate 4)
   - `Status`: `OPEN`
   - `ReviewerID`: from input or `TBD`
   - `Date`: current date

2) Append to `Review_Findings.csv` in the deliverable folder.

3) After each finding or batch of findings, present running summary:
   - Findings by severity: CRITICAL ({n}), MAJOR ({n}), MINOR ({n}), OBSERVATION ({n})
   - Open/Resolved counts
   - Any findings the agent flagged for severity confirmation

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
   - Update `Status` to `RESOLVED` if disposition is final, or `DEFERRED` if deferred with rationale

3) Compile review summary:
   - **Finding totals** by severity and status
   - **All CRITICAL findings** with dispositions (must all be dispositioned)
   - **All MAJOR findings** with dispositions (must all be dispositioned)
   - **MINOR/OBSERVATION** summary counts
   - **Checklist completion**: items checked vs total
   - **TBD inventory**: remaining TBDs in deliverable content
   - **Transition readiness assessment**:
     - For `IN_PROGRESS → CHECKING`: all CRITICAL findings dispositioned (resolved, deferred with rationale, or accepted)
     - For `CHECKING → ISSUED`: all CRITICAL findings RESOLVED; all MAJOR findings RESOLVED or DEFERRED with documented rationale; zero TBD dispositions remain for CRITICAL/MAJOR

4) Update `_REVIEW.md` with the summary section.

5) Prepare a run-local working review package. After the Gate 5 decision, finalize a new immutable snapshot using: `tools/scaffolding/create_snapshot_folder.sh {REVIEWS_ROOT} REV {DeliverableID}`
   Stage these members in the working package; copy them to the snapshot only after the Gate 5 decision is recorded:
   - `Brief.md` (deliverable, review type, reviewers)
   - `RUN_SUMMARY.md` (complete review summary)
   - `Review_Summary.md` (human-readable narrative)
   - `Decision_Log.md` (all gate decisions + finding dispositions)
   - `QA_Report.md` (checklist coverage, mechanical check results)

6) After Gate 5 and snapshot finalization, update the authorized pointer: `tools/scaffolding/update_latest_pointer.sh {REVIEWS_ROOT} {snapshot_folder_name}`

Present the review summary and transition readiness assessment. Ask: "Are all dispositions final?"

**Human confirms** dispositions are complete.

---

### Gate 5 — Lifecycle Transition

**Agent does:**

1) Evaluate transition readiness based on the review summary:

   **For `IN_PROGRESS → CHECKING`:**
   - Required: all CRITICAL findings have a non-TBD disposition
   - Required: checklist has been populated (Gate 2 completed)
   - Recommended: MAJOR findings dispositioned (warn if not)
   - Present: `RECOMMEND_ADVANCE` or `RECOMMEND_HOLD` with reasons

   **For `CHECKING → ISSUED`:**
   - Required: all CRITICAL findings are RESOLVED
   - Required: all MAJOR findings are RESOLVED or DEFERRED with documented rationale
   - Required: zero `HumanDisposition = TBD` for any CRITICAL or MAJOR finding
   - Recommended: MINOR findings dispositioned (warn if not)
   - Present: `RECOMMEND_ADVANCE` or `RECOMMEND_HOLD` with reasons

2) Present the recommendation with evidence summary.

3) Ask: "Do you approve advancing {DeliverableID} to {target state}?"

**If human approves:**

4) Record the human approval through the owning loop’s ruling instrument. Resolve the exact ruling path and approval commit required by that root’s `_harness/adapter.yaml`. If the required committed ruling or reachable approval SHA is not yet available, carry the approved decision to the owning change workflow and hold the status write until those inputs exist.

   Invoke the guarded transition from the declared tool root:
   ```text
   zsh {INSTRUCTION_ROOT}/tools/scaffolding/write_status.sh {deliverable_folder} {TARGET_STATE} HUMAN --ruling {RULING_PATH} --approval-sha {APPROVAL_SHA}
   ```
   HUMAN identifies the recorded decision-maker; WORKING_ITEMS is the executing recorder and records that distinction in the review evidence. CHECKING and ISSUED require a human decision. Supply `--ruling` whenever required by the adapter (including the default committed-ruling rule in Git roots); supply `--approval-sha` when the adapter declares that schema. Where the root explicitly does not require an approval SHA, omit that option and retain the tool’s REVIEW note. Do not invent a ruling/SHA or use an override to bypass missing inputs. The tool updates Current State and appends history only after its checks pass.

5) Present handoff to WORKING_ITEMS (workflow: change):
   - Files modified: `_REVIEW.md`, `Review_Findings.csv`, `_STATUS.md`
   - Recommended commit message:
     ```
     review: {DeliverableID} — {target state} ({total} findings, {open} open)
     ```

**If human declines:**

6) Do NOT update `_STATUS.md`.
7) Record the decision in the working package’s `Decision_Log.md`, then finalize the snapshot and pointer as specified in Gate 4: "Human declined transition at Gate 5. Reason: {stated reason or 'not stated'}."
8) Present options:
   - Return to Gate 3 to capture additional findings
   - Return to Gate 4 to revise dispositions
   - End review session (findings preserved for future review)

---
