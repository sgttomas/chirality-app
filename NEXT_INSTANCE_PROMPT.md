# Next Session Handoff Prompt

You are continuing a governance-and-architecture restructuring pass on the Chirality repository.

Start by reading, in order:

1. `INIT.md`
2. `agents/AGENT_HELPS_HUMANS.md`
3. `agents/AGENT_CONTEXT_TRANSPOSE.md`
4. `agents/AGENT_SKILLMAKER.md`
5. `agents/AGENT_TOOLMAKER.md`

Adopt the HELPS_HUMANS posture: workflow-design, least structure that works, rigor scaled to stakes, no invention, surface conflicts, preserve human decision rights, and prefer durable filesystem artifacts over ephemeral chat conclusions.

## Why this session exists

The previous session did not directly restructure the agent suite yet. It performed the prerequisite epistemic cleanup so that the upcoming restructuring can be done against a more coherent theory of knowledge, accountability, and governance.

The key judgment from the previous session was:

- the repo's intended theory is substantially coherent
- but its canonical docs had drifted in a few meaningful places
- that drift needed to be corrected before evaluating which agents should remain agents, which should become skills, which should call deterministic tools, and which should be retired

## What was done in the previous session

The previous session aligned the theory-of-knowledge layer and reduced duplication across governance docs.

### Canonical semantic changes made

The following were intentionally normalized:

- `ASSUMPTION` now means an inference grounded in cited material, not an unwarranted guess.
- A claim without warrant is always treated as a visible gap.
- `UNWARRANTED` now means `TBD` or uncited `PROPOSAL`.
- `CITED` now means `FACT`, `ASSUMPTION`, or cited `PROPOSAL`.
- `K-PROV-1` was broadened from dependency-row-only provenance to universal provenance for non-trivial governed claims, while still recognizing dependency rows as a schema-specific instance.

### Files changed

The worktree currently contains uncommitted edits in:

- `CHIRALITY_FRAMEWORK.md`
- `docs/TYPES.md`
- `docs/CONTRACT.md`
- `docs/DIRECTIVE.md`
- `docs/DBM_Agent_Instruction_Architecture.md`
- `PROFESSIONAL_ENGINEERING.md`
- `README.md`
- `docs/WHAT-IS-AN-AGENT.md`
- `AGENTS.md`

These edits are intentional and are the latest ground truth for this restructuring effort.

### Why those edits matter for the next session

The next session is about clarifying the boundaries between:

- persona agents
- bounded task agents
- repo-native skills
- deterministic tools
- things that should no longer exist in the working set

That classification must now be done against the normalized theory that:

- agents may produce claims, warrants, classifications, and bounded actions
- only humans complete accountable professional warranting
- agent teams are part of project-management structure
- governance distinctions like normative / operative / evaluative are structural and should not be blurred
- deterministic operations should be removed from agent reasoning whenever possible

## The actual next task

Evaluate the existing instruction files in `agents/` and determine:

1. Which should remain agents.
2. Which should be turned into skills for runtime invocation by another agent, especially by `TASK`.
3. Which should be modified to invoke existing or new deterministic tools.
4. Which should be modified to invoke skills rather than carrying method logic inline.
5. Which should be archived or removed from the active working set because they are no longer the right abstraction in this repo.

This is not a cosmetic cleanup. It is a boundary-setting exercise across the agent OS.

## The key perspective to use

Use the distinctions implied by `SKILLMAKER`, `TOOLMAKER`, and `CONTEXT_TRANSPOSE`.

### Skill boundary

A skill is a reusable bounded-task method pack:

- tool ordering
- method guidance
- QA expectations
- brief schema
- runtime alignment guidance

A skill is not:

- a persona
- a new authority surface
- a new write-scope regime
- a new conversational manager

### Tool boundary

A deterministic tool is:

- LLM-independent
- idempotent
- mechanical
- explicit in inputs/outputs
- suitable for direct invocation by agents or humans

A tool is not:

- drafting
- interpretation
- conflict adjudication
- scope determination
- orchestration judgment

### Agent boundary

An agent remains justified when it needs one or more of:

- a distinct interaction surface
- human gate management
- non-trivial orchestration
- authority separation
- write-scope specialization
- synthesis or judgment that is not reducible to deterministic execution
- cross-artifact or cross-context reasoning that is not just a bounded method pack

### Context-transpose perspective

Treat this task partly as template/OS maintenance, not only live workflow optimization.

Ask:

- is this instruction file a true role in the operating system?
- or is it carrying vocabulary, method, or deterministic logic that should be factored downward into skills/tools?
- or is it a context-specific relic that should be archived?

## What to pay special attention to

Pay particular attention to agents that may now be misclassified because they are really one of the following:

- a recurring method disguised as an agent
- a deterministic helper disguised as agent prose
- a repo/template-maintenance function that should be narrowed or consolidated
- a redundant persona whose human-facing surface is not truly necessary
- an older artifact preserved from earlier design stages that no longer earns its place

Likely high-interest candidates include, but are not limited to:

- `CHIRALITY_FRAMEWORK`
- `CHIRALITY_LENS`
- `CONTENT_DIGEST`
- `AGGREGATION`
- `CONTEXT_TRANSPOSE`
- `SKILLMAKER`
- `TOOLMAKER`

Do not assume these should be removed. Evaluate them cleanly.

## Expected output for this session

Produce a structured evaluation of the `agents/` working set with at least these categories:

- Keep as agent
- Convert to skill
- Keep as agent but make it invoke skill(s)
- Keep as agent but make it invoke deterministic tool(s)
- Archive/remove from active working set
- Needs decomposition because it mixes agent + skill + tool concerns

For each candidate, explain:

- why it belongs in that category
- what invariant or boundary it satisfies
- what would break if it were moved incorrectly
- what migration path would be required

## Constraints

- Do not casually widen scope or invent new subsystems.
- Do not silently preserve historical artifacts just because they already exist.
- Do not silently collapse authority-bearing personas into skills.
- Do not leave deterministic behavior embedded in agent instructions if it clearly belongs in a tool.
- Do not propose runtime skill loading outside the `TASK`-centered model unless there is a strong, explicit reason.
- Treat the recently edited governance docs as the current baseline unless you find a new contradiction.

## Important current workspace note

There is also an untracked `analysis/` directory in the repo root containing repository inventory artifacts. It was not touched during the previous session and is unrelated to the knowledge-theory alignment work. Do not assume it is part of the current restructuring unless you inspect it and decide it is relevant.

## Immediate practical next step

Before proposing any restructuring, inspect the current `agents/` directory and classify each instruction file against these three questions:

1. Is this fundamentally a persona / authority surface?
2. Is this fundamentally a reusable bounded method?
3. Is this fundamentally deterministic machinery?

Then identify the mixed cases, because those are the likely restructuring targets.
