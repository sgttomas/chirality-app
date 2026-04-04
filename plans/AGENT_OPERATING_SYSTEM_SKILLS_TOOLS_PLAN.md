# Agent Operating System Skills And Tools Plan

## Status

Planning note only.

This document captures:

1. what was learned from the recent architecture work
2. what was changed in the repo and why
3. the assessment of the current agent operating system design
4. the recommended next steps for skill-use and tool-use maturity

It is intended to preserve the reasoning behind the recent changes so future
work can continue without reconstructing the discussion from chat history.

## Purpose

Strengthen the Chirality repository as an **agent operating system** rather
than a loose collection of prompts, tools, and helper documents.

The operating-system interpretation here means:

- agents are governed roles with explicit authority and write scope
- workflows are structured and auditable
- bounded work is dispatched through stable shells rather than ad hoc prompts
- method variability is expressed through reusable skills
- deterministic operations are pushed into tools
- state is durably represented in governed files rather than hidden runtime
  memory

This plan documents what has already been put in place and what should come
next to make the architecture more executable, less prose-dependent, and more
scalable.

---

## Part I — Assessment Of What Was Learned

## A. Core Architectural Lessons

### 1. The stable scaling axis is not “more agents”

The recent work confirmed that proliferating top-level agents is the wrong way
to capture method variability.

What scales better is:

- a small stable role taxonomy
- a generic bounded-task shell
- structural specializations where needed
- reusable skills for recurring task methods
- deterministic tools for mechanical sub-operations
- run-specific briefs for local variation

This is the most important architectural lesson from the work.

### 2. `WORKING_ITEMS` is the right human-facing choke point

The current architecture already had the correct place for bounded task
dispatch:

- humans collaborate with `WORKING_ITEMS`
- `WORKING_ITEMS` frames or confirms scope
- `WORKING_ITEMS` may dispatch bounded Type 2 work

That means the human-facing operating model did not need to be reinvented.
What needed to change was the execution substrate underneath it.

### 3. The original `TASK` agent was doing too much

The previous `TASK` instruction set mixed:

- generic bounded-task shell behavior
- deliverable-local subject-matter-helper behavior
- memory handling conventions
- document editing policy

That made `TASK` too specific to one recurring work style.

The lesson is:

- `TASK` should be a universal bounded-task shell
- deliverable-local document work should be preserved as a specialization, not
  the definition of `TASK`

### 4. Profiles and skills are different things

The recent work clarified an important distinction:

- **Task profile** = structural specialization
- **Skill** = method pack

Examples:

- `DELIVERABLE_TASK` is a profile because it defines scope, truth set,
  memory behavior, and edit policy.
- `deliverable-consistency` is a skill because it defines method, tool order,
  runtime overrides, and QA for one recurring task shape.

This distinction needs to remain sharp.

### 5. The deterministic boundary is a genuine strength

The repo already had a strong tool philosophy:

- deterministic operations belong in `tools/`
- reasoning-heavy interpretation belongs in agents

The recent work validated that this is one of the strongest parts of the
architecture and should be extended, not replaced.

The addition of a first deterministic helper for the deliverable consistency
skill was a proof point that this boundary can be operationalized well.

### 6. Repo-native skills are useful, but they need a clearer contract

The newly added `skills/` layer proved useful immediately, especially for:

- expressing task variability without minting new top-level agents
- naming reusable methods
- attaching tool policy to recurring work types
- supporting bounded run-specific overrides

However, the work also showed that skills remain partly documentary unless the
execution system treats them as resolved contracts rather than “instructions to
read.”

That is the main next-stage maturity gap.

### 7. Inventory drift is a real governance problem

The recent tool and agent changes revealed that counts of agents, tools, and
skills drift easily when they are embedded in many narrative documents.

The resulting lesson is simple:

- mutable counts must live in one canonical inventory file
- narrative documents should reference that file, not restate counts

This is an operating-system governance issue, not merely a thesis editing
issue.

---

## B. What Is Already Well Established

The following parts of the agent operating system are already strong and
should be treated as established architecture:

### 1. Type hierarchy and authority structure

Files:

- [`AGENTS.md`](/Users/ryan/ai-env/projects/chirality-app/AGENTS.md)
- [`docs/TYPES.md`](/Users/ryan/ai-env/projects/chirality-app/docs/TYPES.md)
- [`docs/DBM_Agent_Instruction_Architecture.md`](/Users/ryan/ai-env/projects/chirality-app/docs/DBM_Agent_Instruction_Architecture.md)

Why it is strong:

- roles are differentiated by epistemic posture and functional role
- authority is stratified
- Type 0, Type 1, and Type 2 responsibilities are clear
- write scopes are declared and meaningful

### 2. Filesystem-native state model

Why it is strong:

- durable state is inspectable
- recovery is possible
- hidden runtime memory is minimized
- change history and outputs can be governed through the filesystem

### 3. Write-scope and fault-containment model

Why it is strong:

- bounded agents cannot easily corrupt unrelated state
- tool-root outputs are separated from source truth
- cross-scope activity is made explicit

### 4. Human gate and responsibility model

Why it is strong:

- consequential decisions remain human-owned
- orchestration is explicit
- Type 2 execution remains bounded and auditable

### 5. Deterministic tool layer

Files:

- [`tools/REGISTRY.md`](/Users/ryan/ai-env/projects/chirality-app/tools/REGISTRY.md)

Why it is strong:

- mechanical work is increasingly isolated from probabilistic reasoning
- tools are named, registered, and documented
- the tool registry is becoming a real operating-system substrate

### 6. The move to `TASK + profile + skill + tools`

Why it is strong:

- it supports repeatability without freezing every task into one persona
- it preserves boundedness
- it supports variability without role explosion

This is the correct conceptual direction for the system.

---

## Part II — What Was Changed And Why

## A. `TASK` Was Refactored Into A Generic Shell

Files:

- [`agents/AGENT_TASK.md`](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_TASK.md)
- [`agents/AGENT_DELIVERABLE_TASK.md`](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_DELIVERABLE_TASK.md)

### What changed

`TASK` was split into:

- a thin generic bounded-task shell
- a preserved deliverable-local specialization in `DELIVERABLE_TASK`

### Why

The old `TASK` behavior was too specialized to function as the canonical
bounded-task entrypoint for multiple recurring task types.

The split preserves backward-compatible deliverable-local behavior while
making room for a broader execution model.

### Architectural effect

- `TASK` became the stable execution shell
- `DELIVERABLE_TASK` became the structural specialization for deliverable-local
  work
- future task methods can now plug into `TASK` without being forced into the
  old deliverable-local document-helper behavior

## B. Dual-Surface `INIT-TASK` Support Was Established

File:

- [`agents/AGENT_TASK.md`](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_TASK.md)

### What changed

`TASK` now supports:

- inline `INIT-TASK` briefs
- file-based `INIT-TASK.md`
- normalization rules when both are present

### Why

This makes the execution surface more flexible and more operationally useful:

- inline briefs are good for direct dispatch
- file-based briefs are good for durable task definitions, resume state, and
  handoff surfaces

### Architectural effect

The task shell now has a real control-surface model instead of a single
invocation assumption.

## C. A Repo-Native `skills/` Layer Was Added

Files:

- [`skills/README.md`](/Users/ryan/ai-env/projects/chirality-app/skills/README.md)
- [`skills/SKILL_TEMPLATE.md`](/Users/ryan/ai-env/projects/chirality-app/skills/SKILL_TEMPLATE.md)
- [`skills/pdf2md/SKILL.md`](/Users/ryan/ai-env/projects/chirality-app/skills/pdf2md/SKILL.md)
- [`skills/deliverable-consistency/SKILL.md`](/Users/ryan/ai-env/projects/chirality-app/skills/deliverable-consistency/SKILL.md)

### What changed

A formal repo-native skill layer was created with:

- a root contract
- a skill template
- initial example skills

### Why

The architecture needed a place to put recurring methods without creating more
top-level agents.

### Architectural effect

Task variability can now be expressed as:

- shell
- profile
- skill
- tool recipe
- runtime overrides

This is a major step toward scalable bounded task execution.

## D. Standards-Style `SKILL.md` Frontmatter Was Adopted

Files:

- [`skills/pdf2md/SKILL.md`](/Users/ryan/ai-env/projects/chirality-app/skills/pdf2md/SKILL.md)
- [`skills/deliverable-consistency/SKILL.md`](/Users/ryan/ai-env/projects/chirality-app/skills/deliverable-consistency/SKILL.md)

### What changed

Each current skill now uses a `SKILL.md` file with YAML frontmatter including:

- `name`
- `description`
- optional compatibility and metadata fields

### Why

This aligns the repo-native skill layer with the emerging public ecosystem
around skill discovery while still preserving Chirality-specific companion
files.

### Architectural effect

The skills are now more portable, more discoverable, and easier to validate.

## E. The Deliverable Consistency Skill Was Backed By A Deterministic Tool

Files:

- [`tools/validation/scan_deliverable_consistency.py`](/Users/ryan/ai-env/projects/chirality-app/tools/validation/scan_deliverable_consistency.py)
- [`skills/deliverable-consistency/TOOL_POLICY.md`](/Users/ryan/ai-env/projects/chirality-app/skills/deliverable-consistency/TOOL_POLICY.md)

### What changed

The first deterministic deliverable-local helper was added to support the
`deliverable-consistency` skill.

### Why

The architecture needed a proof point that a skill could be:

- method-level reusable
- tool-backed
- bounded by profile
- still supervised by agent reasoning where interpretation is required

### Architectural effect

This was the first real demonstration of:

`TASK` + `DELIVERABLE_TASK` + `skill` + `tool`

working together as intended.

## F. Skill Validation Was Added

File:

- [`tools/validation/validate_skill_metadata.py`](/Users/ryan/ai-env/projects/chirality-app/tools/validation/validate_skill_metadata.py)

### What changed

A deterministic validator was added for the repo-native skill layer.

It checks:

- every skill folder has `SKILL.md`
- frontmatter exists
- `name` and `description` exist
- `name` matches the folder
- names are lowercase/hyphenated

### Why

The skill layer should not depend solely on convention and careful reading.

### Architectural effect

The skills layer now has the beginning of operating-system-grade hygiene:

- naming rules
- structural validation
- deterministic enforcement of metadata expectations

## G. Canonical Inventory Handling Was Added

File:

- [`docs/REPO_INVENTORY.md`](/Users/ryan/ai-env/projects/chirality-app/docs/REPO_INVENTORY.md)

### What changed

A single canonical inventory file was created for mutable counts of:

- indexed agents
- repo-native skills
- registered deterministic tools

Thesis documents were updated to reference that file instead of embedding
mutable counts directly.

### Why

Inventory drift across multiple documents is a governance failure mode.

### Architectural effect

One class of documentation inconsistency has now been structurally reduced.

---

## Part III — Current Assessment Of The Agent Operating System

## A. Overall Assessment

The project now has the foundation of a real agent operating system.

The strongest current interpretation is:

- **governed roles** instead of free-floating prompts
- **filesystem authority** instead of hidden transient state
- **bounded execution** instead of unconstrained agent improvisation
- **deterministic tools** for mechanical work
- **skills** for recurring methods
- **human-controlled orchestration** for consequential decisions

This is already materially better than most agent systems that:

- conflate role and method
- bury authority in prose
- allow tools without scope discipline
- treat memory as opaque session state
- proliferate agents as soon as a task varies slightly

## B. What Is Strong Right Now

### 1. Role clarity

The role model is already strong and should be preserved.

### 2. Execution boundedness

Bounded Type 2 work is one of the best parts of the system.

### 3. Recoverability

The filesystem-centered design is operationally sound.

### 4. Compositional direction

The move toward:

- shell
- profile
- skill
- tool
- run brief

is the correct long-term architecture.

## C. Main Current Weaknesses

### 1. Skills are still partly documentary

At present, skills are mostly:

- structured guidance
- declared tool policy
- metadata and QA notes

They are not yet fully resolved into executable run contracts.

### 2. Tool policy is declared more than enforced

The architecture says what tools should be used, but the run-time discipline
around actual tool usage is still largely instruction-following rather than
mechanically checked behavior.

### 3. Profiles and skills still overlap in some places

This is acceptable during transition, but it should be tightened over time.

### 4. Per-run execution records are not yet uniform

The architecture would be stronger if every Type 2 run produced a standard run
record that captured:

- normalized brief
- resolved profile
- resolved skill
- tools allowed
- tools used
- outputs produced
- QA checks run
- unresolved rulings

### 5. Indexed suite versus filesystem reality is not fully audited

The distinction between:

- indexed operating roles
- auxiliary instruction files
- templates
- legacy or experimental instruction files

should be made more mechanically explicit.

---

## Part IV — Recommended Next Steps

## Phase 1 — Make Skills More Executable

### Goal

Move from “skills as method notes” toward “skills as resolved execution
contracts.”

### Recommended work

1. Add a normalized skill-resolution model to `TASK`
   - resolved skill name
   - resolved folder
   - parsed frontmatter
   - runtime defaults
   - companion files present
   - tool policy source
   - QA policy source

2. Define what `TASK` must do after loading a skill
   - normalize skill identity
   - load and merge companion-file guidance
   - record the resolved method stack in the run report

3. Decide whether skill frontmatter will remain descriptive only or grow to
   include machine-consumed execution fields

### Acceptance criteria

The phase is successful when:

1. skill resolution has an explicit normalized representation
2. `TASK` can explain exactly what skill was resolved and from where
3. skill loading no longer depends on loose narrative interpretation alone

## Phase 2 — Add Standard Run Records For Type 2 Execution

### Goal

Make every bounded execution more auditable and more inspectable.

### Recommended work

Create a standard run-record schema containing:

- control surface used
- normalized scope
- profile
- skill
- runtime overrides
- allowed tools
- tools used
- outputs expected
- outputs produced
- QA checks
- missing items
- human rulings needed

### Why this matters

Without a standard run record, the operating system is only partially
observable.

### Acceptance criteria

The phase is successful when:

1. every Type 2 run can emit a structured run record
2. run records use one stable shape
3. later audits can reason about what the agent actually did

## Phase 3 — Sharpen The Profile / Skill Boundary

### Goal

Reduce overlap between structural specialization and method specialization.

### Recommended rule

- Profiles define:
  - truth set
  - scope
  - memory behavior
  - write policy
  - artifact discipline

- Skills define:
  - preferred tool order
  - method steps
  - runtime overrides
  - QA checks
  - expected outputs

### Immediate target

Review [`agents/AGENT_DELIVERABLE_TASK.md`](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_DELIVERABLE_TASK.md)
for behavior that should eventually move into deliverable-local skills rather
than remaining in the profile.

### Acceptance criteria

The phase is successful when:

1. profile files are mostly structural contracts
2. method variability is mostly skill-owned
3. future bounded task methods no longer require new profile-like prose to be
   added to `TASK`

## Phase 4 — Improve Tool-Use Enforcement

### Goal

Move from “declared allowlist” to “more inspectable and enforceable tool
usage.”

### Recommended work

1. standardize tool declarations in briefs and resolved skill state
2. capture actual tool usage in run records
3. add validation or audit checks for:
   - tool use outside allowlist
   - missing declared-first tool invocation
   - unexpected write paths

### Acceptance criteria

The phase is successful when:

1. tool use can be compared against declared policy
2. violations are detectable after the run
3. skill tool policies have more than documentary force

## Phase 5 — Add More Real Skills

### Goal

Prove the architecture on multiple recurring task shapes.

### Recommended next skills

1. a deliverable-local extraction skill
2. a table-reflow or structure-normalization skill
3. a requirements-extraction or clause-audit skill

### Why

The architecture becomes convincing when multiple different task methods can
run through the same shell/profile/tool system cleanly.

### Acceptance criteria

The phase is successful when:

1. at least two additional skills exist beyond the current seed set
2. each has a clear tool policy or explicit reasoning-first posture
3. each is actually usable through `TASK`

## Phase 6 — Add Deterministic Validation For The Indexed Agent Suite

### Goal

Bring agent inventory governance closer to the skill-layer standard.

### Recommended work

Create a validator that checks:

- every indexed role in [`AGENTS.md`](/Users/ryan/ai-env/projects/chirality-app/AGENTS.md)
  has a matching instruction file
- every indexed instruction file exists
- the indexed suite can be distinguished from auxiliary `AGENT_*.md` files
- inventory drift is surfaced deterministically

### Acceptance criteria

The phase is successful when:

1. the indexed agent suite has deterministic structural validation
2. auxiliary instruction files are visibly distinct from indexed operating
   roles
3. `docs/REPO_INVENTORY.md` can be maintained with less ambiguity

---

## Part V — Suggested Execution Order

Recommended implementation order:

1. Phase 1 — executable skill resolution
2. Phase 2 — standard run records
3. Phase 4 — tool-use enforcement
4. Phase 3 — profile/skill boundary cleanup
5. Phase 5 — additional real skills
6. Phase 6 — indexed-agent validation

### Why this order

- skill resolution must come before stronger run recording
- run recording should exist before tool-use auditing becomes serious
- the profile/skill split can be improved more confidently once the skill
  execution substrate is stronger
- additional skills are a better proof after the substrate is improved
- agent inventory validation is important but less blocking than making skill
  execution itself more concrete

---

## Part VI — Immediate Next Recommended Task

If work resumes from this plan, the next best concrete task is:

**Implement a normalized skill-resolution contract inside `TASK`, and define a
standard Type 2 run-record shape that captures resolved profile, resolved
skill, tools allowed, tools used, and outputs produced.**

This is the most leverage-bearing next step because it turns the current
architecture from:

- governed roles
- reusable skills
- deterministic tools

into a more fully inspectable execution system where the relationship among
those layers is explicit in every run.

---

## Short Summary

The recent work validated the following thesis:

- the Chirality architecture is strongest when agents are treated as operating
  roles, not just prompts
- the right scaling pattern is `TASK + profile + skill + tools + run brief`
- the deterministic boundary is one of the system's strongest architectural
  assets
- the next maturity step is to make skill resolution, tool usage, and run
  recording more executable and less prose-dependent

What was changed already was directionally correct:

- `TASK` became a generic shell
- `DELIVERABLE_TASK` preserved structural specialization
- repo-native skills were added
- standards-style `SKILL.md` frontmatter was adopted
- deterministic helper tools were added
- skill validation was added
- inventory counts were centralized

What comes next is to convert these good architectural pieces into a more
fully operational substrate:

- resolved skill contracts
- standard run records
- stronger tool-use enforcement
- more real skills
- deterministic validation of the indexed agent suite

---

## Part VII — SKILLMAKER Agent Created (2026-04-03)

SKILLMAKER has been created as a dedicated Type 1 persona governing the repo-native skill subsystem. TOOLMAKER has been disambiguated to own deterministic tools only. The shared seam: SKILLMAKER identifies tool needs, TOOLMAKER implements, SKILLMAKER integrates.

This addresses the ownership gap in the skill subsystem by establishing a dedicated design-time governor. It does not address the executability gap — executable skill resolution and standard run records remain separate work per the phased roadmap.
