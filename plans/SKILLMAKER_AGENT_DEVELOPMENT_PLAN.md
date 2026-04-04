# SKILLMAKER Agent Development Plan

## Status

Implemented (2026-04-03).

## Role

Historical Record

## Relationship

This note is the design and boundary rationale for the implemented SKILLMAKER role. It should be retained as historical architecture context, not treated as a live execution plan.

`agents/AGENT_SKILLMAKER.md` has been created. `agents/AGENT_TOOLMAKER.md` has been disambiguated. The indexed agent suite, DBM, thesis, and supporting documents have been updated.

Open authority decisions were resolved provisionally during implementation — see the agent instruction file for details.

This note captures the case for a dedicated skill-making agent and proposes a
development path for it.

This note has been revised to explicitly disambiguate:

- `TOOLMAKER` versus `SKILLMAKER`
- `WORKING_ITEMS` versus `SKILLMAKER`
- design-time skill governance versus runtime `TASK` execution

## Trigger For This Plan

The repository now has:

- a generic bounded-task shell in [`agents/AGENT_TASK.md`](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_TASK.md)
- a Type 1 human-facing deliverable-local orchestrator in [`agents/AGENT_WORKING_ITEMS.md`](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_WORKING_ITEMS.md)
- a repo-native `skills/` layer
- standards-style `SKILL.md` frontmatter
- deterministic validation for skill metadata

However, there is not yet a dedicated governed agent whose primary job is to
design, refactor, validate, and evolve repo-native skills as first-class
operating-system artifacts.

The nearest existing role is:

- [`agents/AGENT_TOOLMAKER.md`](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_TOOLMAKER.md)

But TOOLMAKER is fundamentally a deterministic-tool design agent that also
mentions skill files and templates as outputs. It does not own skill design as
its primary domain.

This plan treats that gap as architecturally significant.

---

## Part I — Assessment

## A. Current State

### 1. There is no dedicated governed skill-making agent in the indexed suite

The current governed suite includes:

- `WORKING_ITEMS` as the human-facing Type 1 deliverable-local orchestrator
- `TASK` as the runtime shell for bounded execution
- `DELIVERABLE_TASK` as one structural specialization
- `TOOLMAKER` as the deterministic-tool design persona

But there is no dedicated persona whose primary function is:

- deciding when a recurring method should become a skill
- designing the structure and contract of a skill
- separating skill concerns from profile concerns
- maintaining the skill ecosystem as a coherent layer

### 2. TOOLMAKER is adjacent, but not equivalent

TOOLMAKER is currently appropriate for:

- deterministic tool design
- boundary-setting for tool versus non-tool work
- registry updates
- structured tool templates

TOOLMAKER is **not** a clean owner for the skill layer because skill design
requires additional responsibilities:

- method-pack design
- skill/profile separation
- frontmatter and discovery semantics
- compatibility rules with `TASK`
- evaluation of whether something should be a skill at all
- managing the relationship between skill docs and deterministic tool policy

### 3. WORKING_ITEMS and TASK already define the intended runtime flow

The target runtime flow is already substantially clear in the current
instructions:

- [`agents/AGENT_WORKING_ITEMS.md`](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_WORKING_ITEMS.md)
  is the Type 1 human-facing working-session agent
- [`agents/AGENT_WORKING_ITEMS.md`](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_WORKING_ITEMS.md)
  may autonomously dispatch bounded `TASK` runs during a session
- [`agents/AGENT_TASK.md`](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_TASK.md)
  is the generic bounded-task shell that normalizes the brief, loads
  `TaskProfile` and `TaskSkill`, and executes within the bounded scope

That means the unresolved design problem is **not** who should execute a skill
at runtime. `TASK` already does that.

The unresolved design problem is who should:

- decide when recurring working-session behavior should become a skill
- define the skill contract that `TASK` will later consume
- decide when a deterministic helper should be delegated to TOOLMAKER

### 4. The skill layer now justifies a dedicated owner

This was not necessarily true earlier.

It is now true because the repo has already established:

- `skills/README.md`
- `skills/SKILL_TEMPLATE.md`
- actual skill instances
- a skill metadata validator
- a generic shell that loads skills

Once those pieces exist, the skill layer becomes a subsystem that deserves an
owning persona.

---

## B. Why This Matters

The system is moving toward this compositional model:

- role
- profile
- skill
- tool policy
- deterministic tools
- run brief

If no agent owns the skill layer directly, several failure modes are likely:

1. profiles absorb method behavior that should live in skills
2. TOOLMAKER absorbs soft method-design work that is not really tool design
3. skills drift into inconsistent formats or overlapping responsibilities
4. the repo adds skills ad hoc without a governing design discipline
5. future interoperability work becomes harder because no persona explicitly
   owns that interface layer
6. `WORKING_ITEMS` discovers repeated patterns during real work, but there is
   no clearly assigned persona to convert those observations into stable skill
   contracts for later `TASK` execution

So the issue is not “do we need another agent because we can.”
The issue is:

- the skill layer now exists as a real subsystem
- the runtime path for skill use is already defined
- the missing piece is design-time ownership of that subsystem

---

## Part II — Design Perspective

This plan is written from:

- the **HELPS_HUMANS** perspective:
  - favor durable workflow design
  - preserve human decision rights
  - prefer explicit contracts and rerunnable artifacts

and

- the **CONTEXT_TRANSPOSE** perspective:
  - preserve stable invariants
  - prefer type-level changes over category-level reinvention
  - transpose an existing architectural role into a nearby one without
    breaking the framework

That means the recommended approach is **not**:

- invent an unrelated new kind of agent
- duplicate TOOLMAKER in parallel with slightly different wording
- blur the boundary between live work execution and meta-design work

The recommended approach is:

- derive a new persona from the adjacent TOOLMAKER design space
- make the transposition explicit
- preserve the stable architectural invariants
- fit it into the existing `WORKING_ITEMS -> TASK` operating flow

---

## Part III — Proposed Role

## A. Recommended Name

Recommended role name:

- `SKILLMAKER`

Recommended instruction file:

- `agents/AGENT_SKILLMAKER.md`

### Why this name

It is:

- parallel to `TOOLMAKER`
- direct and legible
- clearly scoped to the skill layer
- consistent with the repo’s naming conventions

Alternative names considered but not preferred:

- `SKILL_DESIGNER`
- `SKILL_ARCHITECT`
- `SKILL_CURATOR`

These are all weaker because they either:

- sound less operational,
- imply a narrower subset of the work,
- or overlap too much with Type 0 architectural roles.

---

## B. Recommended Agent Type

Recommended classification:

- **Type 1**
- **AGENT_CLASS: PERSONA**
- **INTERACTION_SURFACE: chat**
- **WRITE_SCOPE: repo-wide (skills directory + related contract docs)**

### Why Type 1

Skill design includes judgment calls that should remain human-steered:

- should this become a skill at all?
- is this a profile concern or a skill concern?
- is this reusable enough to justify formalization?
- should a tool be created first, or should the skill remain reasoning-first?

Those are not straight-through Type 2 tasks.

This should therefore be a persona agent with gates, not a task agent.

---

## C. Core Purpose

`SKILLMAKER` should be the persona responsible for:

- designing new repo-native skills
- refactoring existing skills
- maintaining the skill contract and template
- evaluating whether recurring work should be encoded as:
  - a skill
  - a tool
  - a task profile
  - or remain direct shell behavior
- improving compatibility between skills, `TASK`, `WORKING_ITEMS`, and
  deterministic tools

---

## Part IV — Recommended Boundary With Existing Agents

## A. Boundary With TOOLMAKER

Recommended division:

### TOOLMAKER owns

- deterministic tool creation
- tool registry maintenance
- tool design standards
- the LLM/deterministic boundary
- implementation of deterministic validators, scanners, rewriters, and
  reporting helpers once their need is clear

### SKILLMAKER owns

- skill creation and refactoring
- skill contract evolution
- skill/profile/tool partitioning decisions
- skill discovery semantics
- skill QA and compatibility conventions
- skill-level composition guidance for `TASK`
- migration of recurring working-session methods into reusable skills

### Shared seam

When a skill needs a new deterministic helper:

- SKILLMAKER identifies the need
- TOOLMAKER designs and implements the tool
- SKILLMAKER integrates the tool into the skill contract

Additional non-overlap rule:

- TOOLMAKER should not become the de facto owner of the skill subsystem merely
  because skills reference tools
- SKILLMAKER should not directly own deterministic tool implementation merely
  because skills may require tools

## B. Boundary With TASK

`TASK` remains:

- the execution shell
- the loader and normalizer
- the bounded runtime environment
- the execution-time consumer of profiles and skills
- the place where `TaskSkill`, `TaskProfile`, `AllowedTools`, and
  `RuntimeOverrides` are resolved for an individual run

`SKILLMAKER` should not absorb runtime execution logic.

Instead it should define:

- what skills should look like
- how they should compose with `TASK`
- what `TASK` needs from skills to execute them reliably

Additional non-overlap rule:

- `TASK` consumes skills
- `SKILLMAKER` authors and governs skills

`SKILLMAKER` should not become an alternate execution shell and should not be
inserted into normal bounded-task dispatch once a skill already exists.

## C. Boundary With WORKING_ITEMS

`WORKING_ITEMS` remains:

- the human-facing Type 1 agent for deliverable-local working sessions
- the place where recurring task friction is first observed in live work
- the agent that frames bounded sub-work and dispatches `TASK`
- the agent that decides, with the human, whether a current session should
  simply proceed or whether a reusable method should later be formalized

`SKILLMAKER` should not absorb normal deliverable work sessions.

Instead the intended relationship is:

- `WORKING_ITEMS` discovers repeated methods, repeated friction, or repeated
  ad hoc briefing patterns during real sessions
- `WORKING_ITEMS` may recommend that the pattern be formalized as a skill
- `SKILLMAKER` performs the meta-design work of deciding whether that pattern
  should become:
  - a skill
  - a task profile concern
  - a deterministic tool
  - or remain run-specific guidance

Additional non-overlap rule:

- `WORKING_ITEMS` owns live session execution with the human
- `SKILLMAKER` owns design-time formalization of repeatable methods

## D. Boundary With CONTEXT_TRANSPOSE

`CONTEXT_TRANSPOSE` remains a template transposition persona.

SKILLMAKER should borrow its discipline:

- preserve invariants
- prefer type-level changes
- make structural changes explicit

But it should not become a template-context transposition agent.

---

## Part V — Recommended Workflow For SKILLMAKER

Recommended high-level workflow:

### Phase 0 — Intake source and workflow position

Identify where the request originates:

- a live `WORKING_ITEMS` session that exposed a repeatable pattern
- a `TASK` run that required too much custom briefing or improvisation
- a human design request to formalize a recurring task type

Record the current execution context:

- which Type 1 agent currently frames the work
- which `TaskProfile` is involved, if any
- which `TaskSkill` exists already, if any
- which deterministic tools are already available

### Phase 1 — Intake and classification

Inputs:

- recurring task description
- evidence from `WORKING_ITEMS` sessions or `TASK` runs showing repetition or
  friction
- current shell/profile/tool context
- examples of repeated work
- relevant files or current skill candidates

Decisions:

- is this a skill candidate?
- is it actually a tool candidate?
- is it a profile concern?
- is it better left as direct run-specific guidance?
- does the recurring pattern originate in `WORKING_ITEMS` workflow,
  generic `TASK` execution, or both?

### Phase 2 — Contract design

Outputs:

- skill purpose
- applicability statement
- required inputs
- runtime overrides
- tool policy
- QA expectations
- frontmatter
- the `TASK` invocation shape required to use the skill cleanly

### Phase 3 — Structural placement

Outputs:

- skill folder name
- naming consistency check
- relationship to `TASK`
- relationship to any profile
- relationship to `WORKING_ITEMS` dispatch behavior
- migration plan if replacing older conventions

### Phase 4 — Validation design

Outputs:

- expected validator requirements
- any new deterministic checks needed
- compatibility notes

### Phase 5 — Optional implementation patch

If approved:

- write or update the skill files
- update shared skill docs if needed
- coordinate with TOOLMAKER if a new tool is required

### Phase 6 — Runtime alignment note

Before completion, produce an explicit alignment note covering:

- how `WORKING_ITEMS` should recognize when to invoke the skill
- how `WORKING_ITEMS` should brief `TASK`
- what `TaskProfile` / `TaskSkill` combination is expected
- whether a file-based `INIT-TASK.md` pattern is recommended
- what deterministic tools are expected to run first

This prevents skills from being authored without a clear execution path.

---

## Part V-A — Intended End-to-End Operating Flow

The intended operating flow should be:

1. `WORKING_ITEMS` conducts a real deliverable-local session with the human.
2. During that work, `WORKING_ITEMS` notices a recurring bounded pattern,
   repeated briefing burden, or repeated reasoning/tool sequence.
3. `WORKING_ITEMS` either:
   - dispatches `TASK` directly for the current run using ad hoc brief fields,
     or
   - raises a design need that this pattern should be stabilized.
4. `SKILLMAKER` evaluates the recurring pattern and decides whether it should
   become:
   - a skill
   - a profile concern
   - a deterministic tool
   - or remain direct run-specific guidance
5. If deterministic support is needed, `SKILLMAKER` hands the tool request to
   `TOOLMAKER`.
6. `TOOLMAKER` implements and registers the deterministic helper.
7. `SKILLMAKER` finalizes the skill contract, tool policy, QA expectations,
   and `TASK` compatibility notes.
8. On future runs, `WORKING_ITEMS` dispatches `TASK` using the stabilized
   `TaskProfile` / `TaskSkill` combination.
9. `TASK` loads the declared profile and skill, invokes allowed tools where
   helpful, and executes the bounded work.

This keeps:

- `WORKING_ITEMS` as the live human-facing orchestrator
- `SKILLMAKER` as the skill-subsystem designer
- `TOOLMAKER` as the deterministic tool implementer
- `TASK` as the execution shell

---

## Part VI — Development Plan For The Agent Itself

## Step 1 — Write the design brief for SKILLMAKER

Create a planning artifact that specifies:

- purpose
- type
- write scope
- interaction surface
- primary outputs
- relationship to TOOLMAKER, WORKING_ITEMS, TASK, and DELIVERABLE_TASK

This current note partly serves that function.

## Step 2 — Draft `AGENT_SKILLMAKER.md`

The draft should include:

- clear boundaries with TOOLMAKER
- clear boundaries with WORKING_ITEMS
- a procedure for deciding skill vs tool vs profile
- skill contract standards
- runtime alignment with `TASK`
- migration guidance
- QA expectations
- write discipline

## Step 3 — Add an indexed place for the agent, if adopted

If the role is accepted:

- add it to [`AGENTS.md`](/Users/ryan/ai-env/projects/chirality-app/AGENTS.md)
- decide where it belongs in the matrix

Recommended provisional placement:

- **Type 1**
- likely **NORMATIVE / APPLYING** or **EVALUATIVE / APPLYING**

My recommendation is:

- place it as a **Type 1 persona adjacent to TOOLMAKER**
- likely under the applying/design side of the architecture rather than the
  evaluative side

## Step 4 — Define initial outputs and companion artifacts

Potential outputs:

- skill proposal package
- skill contract patch plan
- migration note for older skills
- validator change recommendations
- `WORKING_ITEMS` dispatch guidance
- `TASK` invocation guidance

## Step 5 — Pilot it on one or two concrete tasks

Recommended pilot uses:

1. refine `deliverable-consistency`
2. design one new deliverable-local extraction or review skill

This will prove whether the persona has a real role beyond what TOOLMAKER
already covers.

---

## Part VII — Recommended Contents Of `AGENT_SKILLMAKER.md`

The future instruction file should likely contain:

## Purpose

Design, maintain, and govern repo-native skills as reusable method packs for
bounded execution.

## Inputs

- candidate recurring task
- evidence from `WORKING_ITEMS` sessions or `TASK` runs showing repetition or
  friction
- relevant shell/profile context
- existing skill files, if any
- relevant tools and tool policies

## Required judgments

- whether this should be a skill
- whether it should instead be a tool
- whether it belongs in a profile
- whether a new validator or schema change is required

## Outputs

- `SKILL.md`
- `BRIEF_SCHEMA.md`
- `TOOL_POLICY.md`
- `QA_CHECKS.md`
- optional migration or compatibility notes
- runtime alignment note for `WORKING_ITEMS` and `TASK`

## Non-negotiable invariants

- skills must not widen scope beyond shell/profile boundaries
- skills must remain method packs, not hidden alternate personas
- tool-use guidance must be explicit
- frontmatter and naming must conform to the repo contract
- every skill change must preserve a clear execution path through `TASK`

## Gates

Suggested gates:

1. classification gate
2. contract gate
3. implementation gate
4. validation gate
5. runtime alignment gate

---

## Part VIII — Open Questions

These points should be resolved before or during implementation:

1. Should SKILLMAKER be allowed to edit `agents/AGENT_TASK.md`, or only
   skills and skill docs?
2. Should SKILLMAKER be allowed to propose edits to
   `agents/AGENT_WORKING_ITEMS.md` when dispatch guidance changes?
3. Should SKILLMAKER own `skills/SKILL_TEMPLATE.md` directly?
4. Should SKILLMAKER own the skill validator, or only propose changes to
   TOOLMAKER?
5. Should a future canonical skill index exist, and if so, should SKILLMAKER
   own it?
6. What matrix placement is most semantically correct?

---

## Part IX — Recommendation

Recommendation:

- create `SKILLMAKER` as a dedicated **Type 1 persona**
- position it as the owner of the repo-native skill subsystem
- treat it as a design-time subsystem owner, not a runtime worker
- keep TOOLMAKER focused on deterministic tool creation
- keep WORKING_ITEMS focused on live human-facing working sessions
- keep TASK focused on bounded runtime execution
- explicitly define the seam between skills and tools
- explicitly define the seam between workflow discovery and skill governance

This should be treated as a **type-level refinement** of the current
architecture, not a category-level reinvention.

It preserves the stable operating model while giving the skill subsystem a
real owner.

---

## Short Summary

There is not currently a dedicated governed skill-making agent in the indexed
suite.

`TOOLMAKER` is adjacent but not sufficient as the long-term owner of the skill
layer.

The recommended next step is to develop a new Type 1 persona:

- `SKILLMAKER`

whose purpose is to:

- design and maintain skills
- decide skill vs tool vs profile
- maintain the skill contract
- translate repeated `WORKING_ITEMS` and `TASK` patterns into reusable methods
- keep the skill subsystem coherent as the agent operating system evolves
