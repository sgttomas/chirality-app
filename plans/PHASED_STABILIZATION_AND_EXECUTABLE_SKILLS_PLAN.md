# Phased Stabilization And Executable Skills Plan

## Status

Active. This is the single carried-forward master plan for post-SKILLMAKER architecture work.

## Role

Master Execution Plan

## Relationship

This is the governing roadmap for stabilization, executable skill resolution, standard run records, validation, and related follow-on work. Other plan files in `plans/` should be treated as supporting work packages, policy inputs, historical records, or deferred concepts unless explicitly promoted back into active execution.

This plan is intentionally written before further architecture code changes.

Its purpose is to convert two broad recommendations into an execution-ready
sequence:

1. stabilize the recent architecture shift with validation and commit
   discipline
2. make the `skills/` layer more executable through resolved skill state and
   standard run records

This note also identifies where work can be delegated to subagents and where
parallel execution is beneficial.

---

## Purpose

Recent architecture work moved the repository in the right direction:

- `TASK` became a generic bounded-task shell
- `DELIVERABLE_TASK` preserved deliverable-local specialization
- repo-native skills were introduced
- standards-style skill frontmatter was adopted
- deterministic skill validation was added
- canonical mutable counts were centralized

However, two practical next steps now matter more than adding further design
surface area:

1. the current architecture changes need a stabilization pass so they become a
   durable baseline rather than a large ambiguous working tree
2. the `skills/` layer needs to become more executable so `TASK` resolves and
   records what it is actually doing, rather than only loading skill files as
   narrative method guidance

This plan gives a concrete implementation sequence for both.

## Plan Hierarchy

Use this file as the single active master plan.

Related plan roles:

- Supporting work package:
  - [`plans/AGENT_SOURCE_GROUNDING_INSTRUCTION_UPDATE_PLAN.md`](/Users/ryan/ai-env/projects/chirality-app/plans/AGENT_SOURCE_GROUNDING_INSTRUCTION_UPDATE_PLAN.md)

- Policy inputs:
  - [`plans/DOMAIN_DOCUMENTS_SOURCE_GROUNDING_POLICY.md`](/Users/ryan/ai-env/projects/chirality-app/plans/DOMAIN_DOCUMENTS_SOURCE_GROUNDING_POLICY.md)
  - [`plans/FOUR_DOCUMENTS_SOURCE_GROUNDING_POLICY.md`](/Users/ryan/ai-env/projects/chirality-app/plans/FOUR_DOCUMENTS_SOURCE_GROUNDING_POLICY.md)
  - [`plans/DOCUMENT_DISCOVERY_POLICY_PLAN.md`](/Users/ryan/ai-env/projects/chirality-app/plans/DOCUMENT_DISCOVERY_POLICY_PLAN.md)

- Architectural rationale / historical record:
  - [`plans/AGENT_OPERATING_SYSTEM_SKILLS_TOOLS_PLAN.md`](/Users/ryan/ai-env/projects/chirality-app/plans/AGENT_OPERATING_SYSTEM_SKILLS_TOOLS_PLAN.md)
  - [`plans/SKILLMAKER_AGENT_DEVELOPMENT_PLAN.md`](/Users/ryan/ai-env/projects/chirality-app/plans/SKILLMAKER_AGENT_DEVELOPMENT_PLAN.md)

- Deferred concept:
  - [`plans/DOMAIN_KNOWLEDGE_INDEXING_PLAN.md`](/Users/ryan/ai-env/projects/chirality-app/plans/DOMAIN_KNOWLEDGE_INDEXING_PLAN.md)

---

## Current Assessment

## A. Why The Stabilization Path Has Merit

The repository currently contains a broad working tree with mixed change
classes:

- architecture and agent-instruction changes
- thesis and documentation changes
- tool and extraction work
- new plan notes and skills

That means the next durable move should include:

- cleaning accidental artifacts
- validating new governance surfaces
- grouping work into coherent commit units

Without that step, the architecture shift remains real but operationally
fragile.

## B. Why The Executable-Skills Path Has Merit

The repository now has a viable `skills/` layer, but the main execution shell
still stops short of treating skill resolution as a first-class persisted
object.

What is present already:

- `TaskSkill` selection
- skill folder resolution
- companion-file loading
- a returned textual run report shape in
  [`agents/AGENT_TASK.md`](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_TASK.md)

What is still missing:

- a normalized resolved-skill state per run
- a persisted standard run record
- explicit capture of effective tool policy
- explicit capture of effective runtime overrides
- a durable record of what was actually executed

Without those pieces, skills remain partly documentary.

## C. Recommended Overall Position

Proceed down **both** paths.

Do not treat them as competing alternatives.

The right sequence is:

1. short stabilization pass
2. executable skill resolution
3. standard run records
4. stronger validation and auditing

This order preserves what has already been built and then turns it into a more
mechanically inspectable operating substrate.

---

## Guiding Principles

1. Preserve the existing operating flow:
   `WORKING_ITEMS` frames and dispatches, `TASK` executes, skills supply
   method, tools supply deterministic helpers.
2. Make the next steps executable before making them expansive.
3. Prefer one clear run artifact over more prose.
4. Separate stabilization work from feature work whenever practical.
5. Use subagents for bounded review and classification work, not for the main
   critical-path design decisions.

---

## Phase 0 — Stabilize The Current Architecture Shift

## Goal

Create a clean, validated baseline for the recent architecture changes before
adding more execution machinery.

## Scope

This phase is about:

- cleanup
- validation
- commit grouping
- governance checks

It is not about changing the design of `TASK` or the skill contract yet.

## Concrete Work

1. Remove accidental artifacts from the working tree.
   - especially `__pycache__` directories under tool folders

2. Run existing validators against the new architecture surfaces.
   - validate skill metadata over [`skills/`](/Users/ryan/ai-env/projects/chirality-app/skills)
   - run compile checks on new Python validation tools
   - verify referenced tools exist for new registry entries

3. Review governance consistency across the newly important indexes.
   - [`AGENTS.md`](/Users/ryan/ai-env/projects/chirality-app/AGENTS.md)
   - [`docs/REPO_INVENTORY.md`](/Users/ryan/ai-env/projects/chirality-app/docs/REPO_INVENTORY.md)
   - [`skills/`](/Users/ryan/ai-env/projects/chirality-app/skills)
   - [`tools/REGISTRY.md`](/Users/ryan/ai-env/projects/chirality-app/tools/REGISTRY.md)

4. Separate the current work into coherent commit units.
   - architecture / bounded-task shell / skills
   - inventory / thesis count cleanup
   - drawing-extract or other unrelated tool work

5. Commit the stabilized baseline in small coherent units.

## Acceptance Criteria

The phase is successful when:

1. accidental runtime byproducts are absent
2. the current skill metadata validator passes
3. registry / inventory / indexed-suite drift has been reviewed explicitly
4. the architecture changes are no longer trapped inside one ambiguous working
   tree state

## Delegation And Parallelization

This phase parallelizes well.

Candidate delegated subtasks:

- **Governance sweep subagent**
  Compare [`AGENTS.md`](/Users/ryan/ai-env/projects/chirality-app/AGENTS.md),
  [`docs/REPO_INVENTORY.md`](/Users/ryan/ai-env/projects/chirality-app/docs/REPO_INVENTORY.md),
  [`skills/`](/Users/ryan/ai-env/projects/chirality-app/skills), and
  [`tools/REGISTRY.md`](/Users/ryan/ai-env/projects/chirality-app/tools/REGISTRY.md)
  for drift.

- **Commit classification subagent**
  Group the current working tree into commit units by intent and file set.

- **Unrelated subtree subagent**
  Review drawing-extract or other non-skill architecture changes separately so
  they do not contaminate the stabilization pass.

Local critical-path work that should stay in the main thread:

- final decision on commit boundaries
- final judgment on which governance mismatches are acceptable versus blocking
- final sequencing of the post-stabilization phases

---

## Phase 1 — Make Skill Resolution Executable

## Goal

Make `TASK` resolve skills into a normalized execution object rather than
simply reading skill files as narrative guidance.

## Core Idea

Each bounded run should have one resolved method state that explains exactly
what was loaded and what the effective method contract is.

## Concrete Work

1. Define a resolved-skill model inside `TASK`.

2. Capture, at minimum:
   - normalized `ScopePath`
   - active `TaskProfile`
   - requested `TaskSkill`
   - resolved canonical skill identity
   - resolved skill folder
   - parsed skill frontmatter
   - companion files found
   - effective `AllowedTools`
   - effective `RuntimeOverrides`

3. Make `TASK` record the active method stack explicitly.
   - shell
   - profile
   - skill
   - brief overrides

4. Decide what remains descriptive versus machine-consumed in skill
   frontmatter.

## Acceptance Criteria

The phase is successful when:

1. `TASK` can explain exactly which skill was resolved and from where
2. effective tool policy and runtime overrides are visible as normalized run
   state
3. skill loading no longer depends purely on human interpretation of prose

## Delegation And Parallelization

This phase also parallelizes well.

Candidate delegated subtasks:

- **Schema review subagent**
  Compare current skill files and propose the minimal resolved-skill fields
  that cover both `pdf2md` and `deliverable-consistency`.

- **Compatibility review subagent**
  Check where `AGENT_TASK.md`, `skills/SKILL_TEMPLATE.md`, and current skill
  folders need to stay aligned.

Local critical-path work that should stay in the main thread:

- final resolved-skill shape
- precedence rules between brief fields, profiles, and skills
- decision on whether frontmatter grows machine-consumed fields now or later

---

## Phase 2 — Persist Standard Run Records

**Status: Done** (2026-04-03)

## Goal

Make every bounded Type 2 run produce one durable run artifact with a stable
shape.

## Core Idea

The run record should extend the existing run-report headings in
[`agents/AGENT_TASK.md`](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_TASK.md)
rather than inventing an unrelated second reporting model.

## Design Decisions Resolved

1. **Format:** Markdown with YAML frontmatter. YAML carries machine-parseable
   fields (run-id, timestamps, resolved state). Markdown body carries the same
   headings TASK already emits in conversation.

2. **Location:** `{ScopePath}/_run_records/TASK_RUN_{YYYY-MM-DD}_{HHmm}.md`.
   Stays within TASK's existing `deliverable-local` WRITE_SCOPE (K-WRITE-1).
   The `_` prefix convention marks it as metadata, consistent with `_STATUS.md`,
   `_CONTEXT.md`, etc.

3. **Lifecycle:** Two-phase write. Created at normalization with
   `run-status: PENDING`. Updated at completion with final status and results.
   Immutable after the owning run completes.

4. **Interaction with existing state files:** Independent from `MEMORY.md`
   (working memory) and `NEXT_INSTANCE_STATE.md` (control-loop handoff).
   No coupling needed.

## Concrete Work

1. Define one first-pass run-record schema.

2. Persist the run record immediately after normalization, before work begins.

3. Update the same record at completion with execution outcomes.

4. Keep the first version simple.
   - Markdown with YAML frontmatter
   - one artifact per run
   - generic-shell runs and skill-driven runs use the same overall shape

## Minimum First-Version Fields

- control surface
- normalized scope
- profile
- requested skill
- resolved skill
- allowed tools
- runtime overrides
- requested tasks
- expected outputs
- timestamp
- `RUN_STATUS`
- tools actually used
- outputs produced
- missing items
- human rulings needed
- proposed or applied changes

## Acceptance Criteria

The phase is successful when:

1. every Type 2 run can emit one stable run artifact
2. the run artifact captures both pre-execution normalization and
   post-execution results
3. later audits can reason about what happened without reconstructing the run
   from chat alone

## Implementation

All changes landed in `agents/AGENT_TASK.md` (five additive edits):

1. Agent header: PRIMARY_OUTPUTS updated to reference run record
2. SPEC "In scope": run record creation added
3. SPEC: new "Run record persistence" subsection (lifecycle, location, edge cases)
4. STRUCTURE: new "Run-record file format" subsection (YAML frontmatter schema + Markdown body headings)
5. PROTOCOL: steps 1, 5, and 6 extended with run-record creation and update

No other files changed. WRITE_SCOPE remains `deliverable-local`. No new
K-* invariants introduced.

---

## Phase 3 — Add Light Validation Around Resolved State

**Status: Done** (2026-04-03)

## Goal

Validate the new execution substrate without overreaching into heavy auditing
too early.

## Concrete Work

Validate now:

- resolved skill folder exists
- referenced companion files are either present or explicitly absent
- allowed tools resolve to real paths
- write targets stay within normalized scope
- required run-record fields are present

Defer until later:

- strict proof that the first-declared tool was used first
- deep semantic validation of skill content
- cross-run analytics
- strict tool-policy auditing across all task types

## Acceptance Criteria

The phase is successful when:

1. obvious structural errors in resolved skill state are caught
2. run records are structurally complete
3. validation load remains small enough to adopt quickly

## Implementation

Added a "Structural validation" subsection to `agents/AGENT_TASK.md` SPEC
section collecting all five checks into a named, auditable checklist:

- **Pre-execution checks** (4 items): skill folder existence, tool path
  resolution, profile compatibility, write target scope — all were already
  enforced as hard errors; now formalized in a table.
- **Post-execution checks** (4 items): scope violation, tool allowlist
  compliance, run-record frontmatter completeness, run-record heading
  completeness.
- **Companion file reporting** tightened: all three slots are now explicitly
  checked and reported as `found` or `absent` (previously only listed what
  was found).

No new validation tooling introduced. The validation load is minimal — it
formalizes existing error paths and adds two lightweight post-execution checks.

---

## Phase 4 — Strengthen Tool-Use Auditing

**Status: Done** (2026-04-03)

## Goal

Move from declared tool policy toward inspectable actual tool usage.

## Concrete Work

1. Standardize how effective tool policy is represented in resolved state.
2. Capture actual tool usage in the run record.
3. Add later-stage checks for:
   - tool use outside allowlist
   - unexpected write paths
   - declared-first tool not invoked where the skill requires it

## Acceptance Criteria

The phase is successful when:

1. declared and actual tool usage can be compared
2. obvious tool-policy violations are detectable after the run
3. skill tool policies have more than documentary force

## Implementation

Changes to `agents/AGENT_TASK.md`:

1. **Conversational output format**: `ToolsUsed` entries now use
   `<interpreter> <tool-path>` format matching the `allowed-tools` spec.
   Added `ToolPolicyCompliance: PASS | VIOLATION | N/A` field.
2. **Run-record body**: added `## Tool Policy Compliance` heading alongside
   the structured `## Tools Used` format.
3. **Structural validation**: added three post-execution checks — tool format
   compliance, declared-first tool ordering, write-path scope enforcement.
4. **PROTOCOL step 5**: tool-policy comparison is now an explicit QA sub-step.

Declared and actual tool usage are now in the same format and compared
explicitly in every run.

---

## Phase 5 — Tighten Profile / Skill Separation

**Status: Done** (2026-04-03)

## Goal

Reduce remaining overlap between structural specialization and method
specialization.

## Concrete Work

1. Review [`agents/AGENT_DELIVERABLE_TASK.md`](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_DELIVERABLE_TASK.md)
   for behavior that should move into deliverable-local skills.
2. Keep profiles focused on:
   - scope
   - truth set
   - write discipline
   - artifact discipline
3. Keep skills focused on:
   - method
   - preferred tool order
   - runtime overrides
   - QA expectations

## Acceptance Criteria

The phase is successful when:

1. profiles are mostly structural contracts
2. skills are mostly method contracts
3. future task methods no longer pressure `TASK` or profiles to grow new
   role-like prose

## Implementation

1. Added "Profile / skill separation" guidance subsection to
   `agents/AGENT_TASK.md` SPEC section defining the principle: profiles own
   *where and what* (scope, truth set, write discipline, artifact discipline);
   skills own *how* (method, tools, overrides, QA).

2. Added classification note to `agents/AGENT_DELIVERABLE_TASK.md` RATIONALE
   section identifying structural sections (scope, initialization, file edit
   policy, variant awareness, identity normalization, working memory) and
   method-like sections (semantic lensing, proposal format, baseline scan
   defaults). Method-like sections are retained for continuity but marked as
   skill-extractable.

3. No refactoring performed — the existing separation is already mostly clean.
   The principle is documented so future additions follow it rather than
   growing the profile.

---

## Phase 6 — Commit Discipline And Release Hardening

**Status: Done** (2026-04-03)

## Goal

Turn the architecture shift into a durable maintained baseline rather than an
extended working-tree experiment.

## Concrete Work

1. Define validation gates that should pass before architecture commits.
2. Define coherent commit-unit conventions for:
   - agent / shell / profile changes
   - skill-layer changes
   - validator / tool-layer changes
   - thesis and narrative documentation changes
3. Prefer small commits whose messages describe one architectural change.
4. After the executable-skill substrate lands, perform a brief release-quality
   review of:
   - updated indexes
   - updated templates
   - updated validators
   - plan notes that should remain as plans versus those that should be turned
     into adopted policy or implementation

## Acceptance Criteria

The phase is successful when:

1. architecture changes can be reviewed and reverted in coherent units
2. validation runs are attached to the relevant change set
3. the repo baseline is easier to maintain after the shift than before it

## Implementation

Commit conventions applied across Phases 0–5:

1. **Validation gate**: `validate_skill_metadata.py skills` run before each
   architecture commit. All 3 skills pass.
2. **Two-commit convention**: canonical governance changes (agent instructions)
   committed separately from tracking artifacts (plans, handoff).
3. **Commit history** (Phases 0–5):
   - `fe989d4` — Phase 0 stabilization
   - `f19050a` — EQUIPMENT_EXTRACT → skill conversion
   - `417559d` — Phase 1 resolved-skill model
   - `ce1929f` — Phases 2–5 agent instruction changes
   - `ca2c759` — plan and handoff status updates
4. **Release review**: all architecture changes are now committed. Indexes
   (`AGENTS.md`, `tools/REGISTRY.md`) unchanged by Phases 2–5 (no new agents
   or tools). Skill template unchanged. Master plan reflects all phase
   completions.

---

## Recommended Execution Order

Recommended order:

1. Phase 0 — stabilize the current architecture shift
2. Phase 1 — make skill resolution executable
3. Phase 2 — persist standard run records
4. Phase 3 — add light validation around resolved state
5. Phase 4 — strengthen tool-use auditing
6. Phase 5 — tighten profile / skill separation
7. Phase 6 — commit discipline and release hardening

## Why This Order

- stabilization comes first because the current architecture shift should not
  continue to accumulate inside a large mixed working tree
- skill resolution comes before run records because the run record should
  capture resolved state rather than vague skill references
- run records come before stronger auditing because later audits need a stable
  artifact to inspect
- profile / skill cleanup should follow the improved substrate, not precede it

---

## Immediate Next Recommended Task

If work resumes from this plan, the next best concrete step is:

**Perform Phase 0 as a short stabilization pass, then begin Phase 1 by
designing the resolved-skill model and the first-version run-record schema
together.**

That sequence preserves the current architecture shift and turns it into a
more executable operating substrate with the least wasted motion.

---

## Short Summary

The repository should proceed down both paths that were previously identified:

- stabilization with validation and commit discipline
- executable skill resolution with standard run records

They should be executed in sequence, not treated as alternatives.

The best next move is:

1. stabilize the recent architecture shift
2. add resolved skill state to `TASK`
3. persist standard run records
4. build enforcement and cleanup on top of that substrate
